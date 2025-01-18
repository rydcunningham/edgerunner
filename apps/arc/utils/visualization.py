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
from numba import jit

# Base UNIX timestamp for simulation start
BASE_TIMESTAMP = 1564184363
# Number of paths to process in each batch
BATCH_SIZE = 50
# Number of logs to buffer before writing
LOG_BATCH_SIZE = 100
# Number of processes to use (leave some cores free for system)
NUM_PROCESSES = max(1, cpu_count() - 1)

def jsonl_to_geojson(jsonl_path: str) -> dict:
    # Read entire file at once - pandas handles JSON parsing efficiently
    df = pd.read_json(jsonl_path, lines=True)
    
    # Vectorized extraction of features
    features = (df['_geojson']
               .apply(lambda x: x['features'][0] if x and 'features' in x else None)
               .dropna()
               .tolist())
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

def generate_geojson_files(output_dir: str):
    """Generate GeoJSON files from JSONL files after simulation completion."""
    # Convert vehicle paths JSONL to GeoJSON
    vehicle_paths_jsonl = os.path.join(output_dir, 'vehicle_paths.jsonl')
    vehicle_paths_geojson = os.path.join(output_dir, 'vehicle_paths.geojson')
    if os.path.exists(vehicle_paths_jsonl):
        with open(vehicle_paths_geojson, 'w') as f:
            json.dump(jsonl_to_geojson(vehicle_paths_jsonl), f)
    
    # Convert trip paths JSONL to GeoJSON
    #trip_paths_jsonl = os.path.join(output_dir, 'trip_paths.jsonl')
    #trip_paths_geojson = os.path.join(output_dir, 'trip_paths.geojson')
    #if os.path.exists(trip_paths_jsonl):
    #    with open(trip_paths_geojson, 'w') as f:
    #        json.dump(jsonl_to_geojson(trip_paths_jsonl), f)

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

def process_vehicle_paths_batch(paths: List[Tuple]) -> List[Dict]:
    results = []
    for start_data, end_data, road_network in paths:
        start_loc = Location(start_data['lat'], start_data['lon'])
        end_loc = Location(end_data['lat'], end_data['lon'])
        
        properties = {
            "vehicle_id": start_data['vehicle_id'],
            "old_state": start_data['old_state'],
            "new_state": start_data['new_state'],
            "battery_level_pct": float(start_data['battery_level_pct'])
        }
        
        # Use the stored path from the vehicle state
        path = start_data.get('current_path')
        if path is None:
            print(f"Warning: No path found for vehicle {start_data['vehicle_id']} at timestamp {start_data['timestamp']}")
            continue

        result = process_path_optimized(
            start_loc, end_loc, road_network,
            int(BASE_TIMESTAMP + start_data['timestamp']),
            int(BASE_TIMESTAMP + end_data['timestamp']),
            properties,
            path=path
        )
        
        if result:
            results.append({
                'vehicle_id': start_data['vehicle_id'],
                'old_state': start_data['old_state'],
                'new_state': start_data['new_state'],
                'battery_level_pct': float(start_data['battery_level_pct']),
                'distance': float(end_data['km_traveled'] - start_data['km_traveled']),
                'timestamp': int(BASE_TIMESTAMP + start_data['timestamp']),
                '_geojson': result['_geojson']
            })
    
    return results

"""
def process_trip_paths_batch(trips: List[Tuple]) -> List[Dict]:
    #Process a batch of trip paths using vectorized operations where possible.
    results = []
    
    with timer.timer("trip_path_batch_processing"):
        # Precompute trip durations and start times
        trip_durations = np.array([trip['distance_miles'] / 15 * 3600 for trip, _ in trips])
        start_times = np.array([BASE_TIMESTAMP + int(trip['timestamp']) for trip, _ in trips])
        
        for i, (trip, road_network) in enumerate(trips):
            with timer.timer("single_trip_path_processing"):
                origin = Location(lat=trip['origin_lat'], lon=trip['origin_lon'])
                destination = Location(lat=trip['destination_lat'], lon=trip['destination_lon'])
                
                properties = {
                    "trip_id": str(trip['trip_id']),
                    "vehicle_id": str(trip['vehicle_id']),
                    "fare": float(trip['fare']),
                    "distance_miles": float(trip['distance_miles'])
                }
                
                result = process_path_optimized(
                    origin, destination, road_network,
                    start_times[i], start_times[i] + int(trip_durations[i]),
                    properties
                )
                
                if result:
                    results.append({**trip, '_geojson': result['_geojson']})
    
    return results
"""
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
        #trip_log_buffer = LogBuffer(os.path.join(output_dir, 'trip_paths.jsonl'))
        
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
        """
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
        """
        generate_geojson_files(output_dir)
        
        return output_dir

def process_path_optimized(start_loc: Location, end_loc: Location, road_network, start_time: int, end_time: int, properties: dict, path: List[int] = None) -> dict:
    """Process a path between two locations using numba-optimized functions."""
    # Check if path is None
    if path is None:
        print(f"Warning: No path found for vehicle {properties['vehicle_id']} from {start_loc} to {end_loc}")
        return None

    # Calculate distance using rustworkx's edge data access
    try:
        distance = sum(float(road_network.G.get_edge_data(path[i], path[i+1])) for i in range(len(path)-1)) / 1609.34  # Convert meters to miles
    except (TypeError, IndexError) as e:
        print(f"Error calculating distance for path: {e}")
        return None

    if not path:
        return None
    
    # Get coordinates for all nodes in path at once
    coords = np.array([road_network.G.get_node_data(i) for i in path])
    
    # Calculate number of points based on path length
    total_distance = sum(float(road_network.G.get_edge_data(path[i], path[i+1]) or 0) for i in range(len(path)-1))
    num_points = min(40, max(10, int(total_distance / 400)))
    
    # Use Numba-optimized interpolation
    interpolated_coords = interpolate_path_numba(coords, num_points)
    
    # Use Numba-optimized coordinate processing (swap lat/lon for GeoJSON)
    coord_array = process_coordinates_batch_numba(interpolated_coords)
    
    # Generate timestamps using Numba
    times = generate_timestamps_numba(start_time, end_time, num_points)
    
    # Stack coordinates, elevation (zeros), and times in one operation
    coordinates = np.column_stack((
        coord_array,
        np.zeros(num_points, dtype=np.float64),
        times
    ))
    
    # Create GeoJSON feature
    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": properties,
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates.tolist()
            }
        }]
    }
    
    return {
        'distance': distance,
        '_geojson': geojson
    }