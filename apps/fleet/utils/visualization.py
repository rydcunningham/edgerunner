import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from utils.geo import Location
from utils.timing import timer
from utils.optimized import (
    haversine_distance_numba,
    interpolate_path_numba,
    generate_timestamps_numba,
    process_coordinates_batch_numba
)
from multiprocessing import Pool, cpu_count
from itertools import islice
from typing import List, Dict, Tuple, Any

# Base UNIX timestamp for simulation start
BASE_TIMESTAMP = 1564184363
# Number of paths to process in each batch
BATCH_SIZE = 50
# Number of logs to buffer before writing
LOG_BATCH_SIZE = 100
# Number of processes to use (leave some cores free for system)
NUM_PROCESSES = max(1, cpu_count() - 1)

class LogBuffer:
    def __init__(self, filename: str, batch_size: int = LOG_BATCH_SIZE):
        self.filename = filename
        self.batch_size = batch_size
        self.buffer = []
        
    def append(self, entry: Dict):
        self.buffer.append(entry)
        if len(self.buffer) >= self.batch_size:
            self.flush()
            
    def flush(self):
        if self.buffer:
            with open(self.filename, 'a') as f:
                for entry in self.buffer:
                    json.dump(entry, f)
                    f.write('\n')
            self.buffer.clear()

def create_path_coords(start_loc: Location, end_loc: Location, road_network) -> Tuple[List[Tuple[float, float]], float]:
    """Get path coordinates between two locations."""
    path, distance = road_network.get_shortest_path(start_loc, end_loc)
    if not path:
        return None, 0
    return road_network.get_path_coordinates(path), distance

def process_vehicle_paths_batch(paths: List[Tuple]) -> List[Dict]:
    """Process a batch of vehicle paths in parallel."""
    results = []
    
    for start_data, end_data, road_network in paths:
        # Get path between points
        start_loc = Location(start_data['lat'], start_data['lon'])
        end_loc = Location(end_data['lat'], end_data['lon'])
        
        path, distance = road_network.get_shortest_path(start_loc, end_loc)
        
        if path:
            # Get interpolated points
            points = road_network.interpolate_path(path)
            
            # Convert points to arrays for faster processing
            num_points = len(points)
            coord_array = np.array([[p.lon, p.lat] for p in points])
            
            # Create evenly spaced timestamps
            start_time = int(BASE_TIMESTAMP + start_data['timestamp'])
            end_time = int(BASE_TIMESTAMP + end_data['timestamp'])
            times = np.linspace(start_time, end_time, num_points)
            
            # Create GeoJSON feature using optimized arrays
            coordinates = np.column_stack((
                coord_array,
                np.zeros(num_points, dtype=np.float64),
                times
            ))
            
            geojson = {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {
                        "vehicle_id": start_data['vehicle_id'],
                        "old_state": start_data['old_state'],
                        "new_state": start_data['new_state'],
                        "battery_level_pct": float(start_data['battery_level_pct'])
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coordinates.tolist()
                    }
                }]
            }
            
            results.append({
                'vehicle_id': start_data['vehicle_id'],
                'old_state': start_data['old_state'],
                'new_state': start_data['new_state'],
                'battery_level_pct': float(start_data['battery_level_pct']),
                'distance': float(end_data['km_traveled'] - start_data['km_traveled']),
                'timestamp': int(BASE_TIMESTAMP + start_data['timestamp']),
                '_geojson': geojson
            })
    
    return results

def process_trip_paths_batch(trips: List[Tuple]) -> List[Dict]:
    """Process a batch of trip paths in parallel using Numba-optimized functions."""
    results = []
    
    with timer.timer("trip_path_batch_processing"):
        for trip, road_network in trips:
            with timer.timer("single_trip_path_processing"):
                origin = Location(lat=trip['origin_lat'], lon=trip['origin_lon'])
                destination = Location(lat=trip['destination_lat'], lon=trip['destination_lon'])
                
                with timer.timer("trip_coordinate_generation"):
                    coords, distance = create_path_coords(origin, destination, road_network)
                if not coords:
                    continue
                
                # Convert coordinates to numpy array for Numba processing
                coords_array = np.array([(loc.lat, loc.lon) for loc in coords])
                num_points = len(coords)
                
                # Use Numba-optimized coordinate processing
                with timer.timer("coordinate_array_creation"):
                    coord_array = process_coordinates_batch_numba(coords_array)
                
                # Use Numba-optimized timestamp generation
                with timer.timer("trip_timestamp_generation"):
                    start_time = BASE_TIMESTAMP + int(trip['timestamp'])
                    trip_duration_seconds = (distance / 15) * 3600  # Assume 15 mph average speed
                    end_time = start_time + int(trip_duration_seconds)
                    times = generate_timestamps_numba(start_time, end_time, num_points)
                
                # Create GeoJSON feature using optimized arrays
                with timer.timer("trip_geojson_feature_creation"):
                    # Stack coordinates, elevation (zeros), and times in one operation
                    coordinates = np.column_stack((
                        coord_array,
                        np.zeros(num_points, dtype=np.float64),
                        times
                    ))
                    
                    geojson = {
                        "type": "FeatureCollection",
                        "features": [{
                            "type": "Feature",
                            "properties": {
                                "trip_id": str(trip['trip_id']),
                                "vehicle_id": str(trip['vehicle_id']),
                                "fare": float(trip['fare']),
                                "distance_miles": float(trip['distance_miles'])
                            },
                            "geometry": {
                                "type": "LineString",
                                "coordinates": coordinates.tolist()
                            }
                        }]
                    }
                
                results.append({**trip, '_geojson': geojson})
    
    return results

def batch_items(items: List[Any], batch_size: int):
    """Yield successive batch_size-sized chunks from items."""
    iterator = iter(items)
    return iter(lambda: list(islice(iterator, batch_size)), [])

def prepare_kepler_data(vehicle_df: pd.DataFrame, trip_df: pd.DataFrame, depot_location: Location, road_network, output_dir: str = None) -> str:
    """Prepare data for Kepler.gl visualization using parallel processing."""
    with timer.timer("prepare_kepler_data_total"):
        # Use provided output directory or create default
        if output_dir is None:
            output_dir = "outputs/kepler"
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Initialize log buffers
        vehicle_log_buffer = LogBuffer(os.path.join(output_dir, 'vehicle_paths.jsonl'))
        trip_log_buffer = LogBuffer(os.path.join(output_dir, 'trip_paths.jsonl'))
        
        # 1. Vehicle paths over time
        with timer.timer("prepare_vehicle_paths"):
            # First sort by vehicle and timestamp to get proper path sequence
            with timer.timer("vehicle_path_data_prep"):
                vehicle_df = vehicle_df.sort_values(['vehicle_id', 'timestamp'])
                
                # Group vehicles by H3 cell for spatial indexing
                vehicle_groups = {}
                
                for vehicle_id, group in vehicle_df.groupby('vehicle_id'):
                    for i in range(len(group) - 1):
                        start_data = group.iloc[i].to_dict()
                        end_data = group.iloc[i + 1].to_dict()
                        path_info = (start_data, end_data, road_network)
                        
                        # Group by start cell for parallel processing
                        start_cell = start_data['h3_cell']
                        if start_cell not in vehicle_groups:
                            vehicle_groups[start_cell] = []
                        vehicle_groups[start_cell].append(path_info)
            
            # Process paths in parallel batches by cell
            with Pool(NUM_PROCESSES) as pool:
                # Create batches maintaining spatial locality
                with timer.timer("vehicle_path_batch_creation"):
                    batches = []
                    current_batch = []
                    current_size = 0
                    
                    for cell, paths in vehicle_groups.items():
                        if current_size + len(paths) > BATCH_SIZE:
                            if current_batch:
                                batches.append(current_batch)
                            current_batch = paths
                            current_size = len(paths)
                        else:
                            current_batch.extend(paths)
                            current_size += len(paths)
                    
                    if current_batch:
                        batches.append(current_batch)
                
                with timer.timer("vehicle_path_parallel_processing"):
                    for batch_results in pool.starmap(process_vehicle_paths_batch, [(batch,) for batch in batches]):
                        for result in batch_results:
                            vehicle_log_buffer.append(result)
        
        # Ensure all vehicle logs are written
        vehicle_log_buffer.flush()
        
        # 2. Trip paths with interpolated points
        with timer.timer("prepare_trip_paths"):
            # Get completed trips
            with timer.timer("trip_path_data_prep"):
                completed_trips = trip_df[trip_df['status'] == 'assigned'].copy()
                
                # Group trips by origin H3 cell
                trip_groups = {}
                for _, trip in completed_trips.iterrows():
                    origin_cell = trip['origin_h3_cell']
                    if origin_cell not in trip_groups:
                        trip_groups[origin_cell] = []
                    trip_groups[origin_cell].append((trip, road_network))
            
            # Process trip paths in parallel batches by cell
            with Pool(NUM_PROCESSES) as pool:
                with timer.timer("trip_path_batch_creation"):
                    batches = []
                    current_batch = []
                    current_size = 0
                    
                    for cell, trips in trip_groups.items():
                        if current_size + len(trips) > BATCH_SIZE:
                            if current_batch:
                                batches.append(current_batch)
                            current_batch = trips
                            current_size = len(trips)
                        else:
                            current_batch.extend(trips)
                            current_size += len(trips)
                    
                    if current_batch:
                        batches.append(current_batch)
                
                with timer.timer("trip_path_parallel_processing"):
                    for batch_results in pool.starmap(process_trip_paths_batch, [(batch,) for batch in batches]):
                        for result in batch_results:
                            trip_log_buffer.append(result)
        
        # Ensure all trip logs are written
        trip_log_buffer.flush()
        
        # 3. Unfulfilled trips and depot points
        with timer.timer("point_data_preparation"):
            unfulfilled = trip_df[trip_df['status'] == 'unfulfilled'].copy()
            # Select only the fields we need and ensure they exist
            unfulfilled_fields = ['trip_id', 'timestamp', 'origin_lat', 'origin_lon', 'reason', 'missed_revenue']
            # Add any missing fields with default values
            for field in unfulfilled_fields:
                if field not in unfulfilled.columns:
                    if field == 'missed_revenue':
                        unfulfilled[field] = 0.0
                    elif field == 'reason':
                        unfulfilled[field] = 'unknown'
                    else:
                        unfulfilled[field] = None
            
            unfulfilled_points = unfulfilled[unfulfilled_fields].copy()
            
            depot_df = pd.DataFrame([{
                'name': 'Main Depot',
                'lat': depot_location.lat,
                'lon': depot_location.lon,
                'type': 'charging_depot'
            }])
        
        # Save layers
        with timer.timer("save_output_files"):
            # Save GeoJSON for vehicle paths
            with timer.timer("vehicle_paths_geojson_creation"):
                vehicle_paths_geojson = {
                    "type": "FeatureCollection",
                    "features": []
                }
                # Process each buffered result
                for batch_results in vehicle_log_buffer.buffer:
                    if '_geojson' in batch_results:
                        vehicle_paths_geojson['features'].append(batch_results['_geojson']['features'][0])
                
                with open(os.path.join(output_dir, 'vehicle_paths.geojson'), 'w') as f:
                    json.dump(vehicle_paths_geojson, f, default=str)
            
            # Save GeoJSON for trip paths
            with timer.timer("trip_paths_geojson_creation"):
                trip_paths_geojson = {
                    "type": "FeatureCollection",
                    "features": []
                }
                # Process each buffered result
                for batch_results in trip_log_buffer.buffer:
                    if '_geojson' in batch_results:
                        trip_paths_geojson['features'].append(batch_results['_geojson']['features'][0])
                
                with open(os.path.join(output_dir, 'trip_paths.geojson'), 'w') as f:
                    json.dump(trip_paths_geojson, f, default=str)
            
            with timer.timer("point_data_export"):
                unfulfilled_points.to_csv(os.path.join(output_dir, 'unfulfilled_trips.csv'), index=False)
                depot_df.to_csv(os.path.join(output_dir, 'depots.csv'), index=False)
            
            # Update Kepler config for new format
            with timer.timer("kepler_config_generation"):
                kepler_config = {
                    "version": "v1",
                    "config": {
                        "visState": {
                            "layers": [
                                {
                                    "id": "vehicle_paths",
                                    "type": "trip",
                                    "config": {
                                        "dataId": "vehicle_paths",
                                        "columns": {
                                            "geojson": "_geojson"
                                        },
                                        "isVisible": True,
                                        "colorField": "new_state",
                                        "sizeField": "battery_level_pct",
                                        "visConfig": {
                                            "trailLength": 10,
                                            "animation": True
                                        }
                                    }
                                },
                                {
                                    "id": "trip_paths",
                                    "type": "trip",
                                    "config": {
                                        "dataId": "trip_paths",
                                        "columns": {
                                            "geojson": "_geojson"
                                        },
                                        "isVisible": True,
                                        "colorField": "fare",
                                        "sizeField": "distance_miles",
                                        "visConfig": {
                                            "trailLength": 10,
                                            "animation": True
                                        }
                                    }
                                },
                                {
                                    "id": "unfulfilled_trips",
                                    "type": "point",
                                    "config": {
                                        "dataId": "unfulfilled_trips",
                                        "columns": {
                                            "lat": "origin_lat",
                                            "lng": "origin_lon"
                                        },
                                        "isVisible": True,
                                        "colorField": "reason",
                                        "sizeField": "missed_revenue"
                                    }
                                },
                                {
                                    "id": "depots",
                                    "type": "point",
                                    "config": {
                                        "dataId": "depots",
                                        "columns": {
                                            "lat": "lat",
                                            "lng": "lon"
                                        },
                                        "isVisible": True,
                                        "color": [255, 0, 0]  # Red for depots
                                    }
                                }
                            ]
                        }
                    }
                }
                
                # Save Kepler config
                with open(os.path.join(output_dir, 'kepler_config.json'), 'w') as f:
                    json.dump(kepler_config, f)
        
        return output_dir 