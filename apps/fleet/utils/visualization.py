import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from utils.geo import Location
from utils.timing import timer
from multiprocessing import Pool, cpu_count
from itertools import islice
from typing import List, Dict, Tuple, Any

# Base UNIX timestamp for simulation start
BASE_TIMESTAMP = 1564184363
# Number of paths to process in each batch
BATCH_SIZE = 50
# Number of processes to use (leave some cores free for system)
NUM_PROCESSES = max(1, cpu_count() - 1)

def create_path_coords(start_loc: Location, end_loc: Location, road_network) -> Tuple[List[Tuple[float, float]], float]:
    """Get path coordinates between two locations."""
    path, distance = road_network.get_shortest_path(start_loc, end_loc)
    if not path:
        return None, 0
    return road_network.get_path_coordinates(path), distance

def process_vehicle_path_batch(args: Tuple[List[Dict], Any]) -> List[Dict]:
    """Process a batch of vehicle paths in parallel."""
    paths, road_network = args
    results = []
    
    with timer.timer("vehicle_path_batch_processing"):
        for path_data in paths:
            with timer.timer("single_vehicle_path_processing"):
                start = path_data['start']
                end = path_data['end']
                
                if start['lon'] == end['lon'] and start['lat'] == end['lat']:
                    continue
                    
                start_loc = Location(lat=start['lat'], lon=start['lon'])
                end_loc = Location(lat=end['lat'], lon=end['lon'])
                
                with timer.timer("path_coordinate_generation"):
                    coords, _ = create_path_coords(start_loc, end_loc, road_network)
                if not coords:
                    continue
                    
                # Create timestamps for each point
                with timer.timer("timestamp_generation"):
                    num_points = len(coords)
                    times = np.linspace(
                        BASE_TIMESTAMP + start['timestamp'],
                        BASE_TIMESTAMP + end['timestamp'],
                        num_points
                    )
                
                # Create GeoJSON feature
                with timer.timer("geojson_feature_creation"):
                    geojson = {
                        "type": "FeatureCollection",
                        "features": [{
                            "type": "Feature",
                            "properties": {
                                "vehicle_id": str(start['vehicle_id']),
                                "old_state": str(start['old_state']),
                                "new_state": str(start['new_state']),
                                "battery_level_pct": float(start['battery_level_pct'])
                            },
                            "geometry": {
                                "type": "LineString",
                                "coordinates": [[float(lon), float(lat), 0, int(time)] 
                                            for (lat, lon), time in zip(coords, times)]
                            }
                        }]
                    }
                
                results.append({
                    'vehicle_id': str(start['vehicle_id']),
                    'old_state': str(start['old_state']),
                    'new_state': str(start['new_state']),
                    'battery_level_pct': float(start['battery_level_pct']),
                    'distance': float(end['km_traveled'] - start['km_traveled']),
                    'timestamp': int(BASE_TIMESTAMP + start['timestamp']),
                    'datetime': str(start['datetime']),
                    '_geojson': geojson
                })
    
    return results

def process_trip_path_batch(args: Tuple[List[Dict], Any]) -> List[Dict]:
    """Process a batch of trip paths in parallel."""
    trips, road_network = args
    results = []
    
    with timer.timer("trip_path_batch_processing"):
        for trip in trips:
            with timer.timer("single_trip_path_processing"):
                origin = Location(lat=trip['origin_lat'], lon=trip['origin_lon'])
                destination = Location(lat=trip['destination_lat'], lon=trip['destination_lon'])
                
                with timer.timer("trip_coordinate_generation"):
                    coords, distance = create_path_coords(origin, destination, road_network)
                if not coords:
                    continue
                    
                # Create timestamps for each point
                with timer.timer("trip_timestamp_generation"):
                    num_points = len(coords)
                    start_time = BASE_TIMESTAMP + int(trip['timestamp'])
                    trip_duration_seconds = (distance / 15) * 3600  # Assume 15 mph average speed
                    times = np.linspace(start_time, start_time + trip_duration_seconds, num_points)
                
                # Create GeoJSON feature
                with timer.timer("trip_geojson_feature_creation"):
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
                                "coordinates": [[float(lon), float(lat), 0, int(time)] 
                                            for (lat, lon), time in zip(coords, times)]
                            }
                        }]
                    }
                
                results.append({**trip, '_geojson': geojson})
    
    return results

def batch_items(items: List[Any], batch_size: int):
    """Yield successive batch_size-sized chunks from items."""
    iterator = iter(items)
    return iter(lambda: list(islice(iterator, batch_size)), [])

def prepare_kepler_data(vehicle_df: pd.DataFrame, trip_df: pd.DataFrame, depot_location: Location, road_network) -> str:
    """Prepare data for Kepler.gl visualization using parallel processing."""
    with timer.timer("prepare_kepler_data_total"):
        # 1. Vehicle paths over time
        with timer.timer("prepare_vehicle_paths"):
            # First sort by vehicle and timestamp to get proper path sequence
            with timer.timer("vehicle_path_data_prep"):
                vehicle_df = vehicle_df.sort_values(['vehicle_id', 'timestamp'])
                
                # Prepare path data for parallel processing
                path_data = []
                for vehicle_id, group in vehicle_df.groupby('vehicle_id'):
                    for i in range(len(group) - 1):
                        path_data.append({
                            'start': group.iloc[i].to_dict(),
                            'end': group.iloc[i + 1].to_dict()
                        })
            
            # Process paths in parallel batches
            vehicle_paths = []
            with Pool(NUM_PROCESSES) as pool:
                # Create batches of paths
                with timer.timer("vehicle_path_batch_creation"):
                    batches = list(batch_items(path_data, BATCH_SIZE))
                    batch_args = [(batch, road_network) for batch in batches]
                
                with timer.timer("vehicle_path_parallel_processing"):
                    results = pool.map(process_vehicle_path_batch, batch_args)
                    # Flatten results
                    vehicle_paths = [path for batch in results for path in batch]
                    
        vehicle_paths_df = pd.DataFrame(vehicle_paths)
        
        # 2. Trip paths with interpolated points
        with timer.timer("prepare_trip_paths"):
            # Get completed trips
            with timer.timer("trip_path_data_prep"):
                completed_trips = trip_df[trip_df['status'] == 'assigned'].copy()
                trip_records = completed_trips.to_dict('records')
            
            # Process trip paths in parallel batches
            with Pool(NUM_PROCESSES) as pool:
                # Create batches of trips
                with timer.timer("trip_path_batch_creation"):
                    batches = list(batch_items(trip_records, BATCH_SIZE))
                    batch_args = [(batch, road_network) for batch in batches]
                
                with timer.timer("trip_path_parallel_processing"):
                    results = pool.map(process_trip_path_batch, batch_args)
                    # Flatten results
                    processed_trips = [trip for batch in results for trip in batch]
            
            # Convert back to DataFrame
            with timer.timer("trip_path_dataframe_conversion"):
                trip_paths_df = pd.DataFrame(processed_trips)
                # Convert numeric columns to Python types
                for col in ['fare', 'distance_miles', 'pickup_time_minutes']:
                    if col in trip_paths_df.columns:
                        trip_paths_df[col] = trip_paths_df[col].astype(float)
                
                # Select required columns
                trip_paths_df = trip_paths_df[['trip_id', 'vehicle_id', 'datetime', '_geojson', 'fare', 
                                           'distance_miles', 'pickup_time_minutes', 'status',
                                           'origin_lat', 'origin_lon', 'destination_lat', 'destination_lon']].copy()
        
        # 3. Unfulfilled trips and depot points
        with timer.timer("point_data_preparation"):
            unfulfilled = trip_df[trip_df['status'] == 'unfulfilled'].copy()
            unfulfilled_points = unfulfilled[['trip_id', 'datetime', 'origin_lat', 'origin_lon',
                                          'reason', 'missed_revenue']].copy()
            
            depot_df = pd.DataFrame([{
                'name': 'Main Depot',
                'lat': depot_location.lat,
                'lon': depot_location.lon,
                'type': 'charging_depot'
            }])
        
        # Save to Kepler.gl compatible format
        output_dir = "outputs/kepler"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save layers
        with timer.timer("save_output_files"):
            # Save GeoJSON for vehicle paths
            with timer.timer("vehicle_paths_geojson_creation"):
                vehicle_paths_geojson = {
                    "type": "FeatureCollection",
                    "features": [path['_geojson']['features'][0] for path in vehicle_paths]
                }
                with open(f"{output_dir}/vehicle_paths_{timestamp}.geojson", 'w') as f:
                    json.dump(vehicle_paths_geojson, f, default=str)
            
            # Save GeoJSON for trip paths
            with timer.timer("trip_paths_geojson_creation"):
                trip_paths_geojson = {
                    "type": "FeatureCollection",
                    "features": [path['_geojson']['features'][0] for path in trip_paths_df.to_dict('records')]
                }
                with open(f"{output_dir}/trip_paths_{timestamp}.geojson", 'w') as f:
                    json.dump(trip_paths_geojson, f, default=str)
            
            with timer.timer("point_data_export"):
                unfulfilled_points.to_csv(f"{output_dir}/unfulfilled_trips_{timestamp}.csv", index=False)
                depot_df.to_csv(f"{output_dir}/depots_{timestamp}.csv", index=False)
            
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
                with open(f"{output_dir}/kepler_config_{timestamp}.json", 'w') as f:
                    json.dump(kepler_config, f)
        
        return output_dir 