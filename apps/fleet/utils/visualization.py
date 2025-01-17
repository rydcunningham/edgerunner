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

def jsonl_to_geojson(jsonl_path: str) -> dict:
    """Convert a JSONL file containing GeoJSON features to a single GeoJSON FeatureCollection."""
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    with open(jsonl_path, 'r') as f:
        for line in f:
            entry = json.loads(line)
            if '_geojson' in entry:
                geojson['features'].append(entry['_geojson']['features'][0])
    return geojson

def generate_geojson_files(output_dir: str):
    """Generate GeoJSON files from JSONL files after simulation completion."""
    # Convert vehicle paths JSONL to GeoJSON
    vehicle_paths_jsonl = os.path.join(output_dir, 'vehicle_paths.jsonl')
    vehicle_paths_geojson = os.path.join(output_dir, 'vehicle_paths.geojson')
    if os.path.exists(vehicle_paths_jsonl):
        with open(vehicle_paths_geojson, 'w') as f:
            json.dump(jsonl_to_geojson(vehicle_paths_jsonl), f)
    
    # Convert trip paths JSONL to GeoJSON
    trip_paths_jsonl = os.path.join(output_dir, 'trip_paths.jsonl')
    trip_paths_geojson = os.path.join(output_dir, 'trip_paths.geojson')
    if os.path.exists(trip_paths_jsonl):
        with open(trip_paths_geojson, 'w') as f:
            json.dump(jsonl_to_geojson(trip_paths_jsonl), f)

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
        
        # Process and write vehicle paths
        with timer.timer("prepare_vehicle_paths"):
            vehicle_df = vehicle_df.sort_values(['vehicle_id', 'timestamp'])
            vehicle_groups = {}
            
            for vehicle_id, group in vehicle_df.groupby('vehicle_id'):
                for i in range(len(group) - 1):
                    start_data = group.iloc[i].to_dict()
                    end_data = group.iloc[i + 1].to_dict()
                    path_info = (start_data, end_data, road_network)
                    start_cell = start_data['h3_cell']
                    if start_cell not in vehicle_groups:
                        vehicle_groups[start_cell] = []
                    vehicle_groups[start_cell].append(path_info)
            
            with Pool(NUM_PROCESSES) as pool:
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
                
                for batch_results in pool.starmap(process_vehicle_paths_batch, [(batch,) for batch in batches]):
                    for result in batch_results:
                        vehicle_log_buffer.append(result)
        
        vehicle_log_buffer.flush()
        
        # Process and write trip paths
        with timer.timer("prepare_trip_paths"):
            completed_trips = trip_df[trip_df['status'] == 'assigned'].copy()
            trip_groups = {}
            
            for _, trip in completed_trips.iterrows():
                origin_cell = trip['origin_h3_cell']
                if origin_cell not in trip_groups:
                    trip_groups[origin_cell] = []
                trip_groups[origin_cell].append((trip, road_network))
            
            with Pool(NUM_PROCESSES) as pool:
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
                
                for batch_results in pool.starmap(process_trip_paths_batch, [(batch,) for batch in batches]):
                    for result in batch_results:
                        trip_log_buffer.append(result)
        
        trip_log_buffer.flush()

        generate_geojson_files(output_dir)
        
        return output_dir