import simpy
from utils.io import load_config
from simulation.simulation import simulate
from utils.geo import Location, random_point_in_radius, is_point_in_service_area, find_nearest_vehicle, haversine_distance
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import os
from datetime import datetime, timedelta
import glob
import time
import json
import numpy as np

def prepare_kepler_data(vehicle_df, trip_df, depot_location, road_network):
    """Prepare data for Kepler.gl visualization."""
    # Base UNIX timestamp for simulation start
    BASE_TIMESTAMP = 1564184363
    
    # 1. Vehicle paths over time
    # First sort by vehicle and timestamp to get proper path sequence
    vehicle_df = vehicle_df.sort_values(['vehicle_id', 'timestamp'])
    
    # Create GeoJSON paths for vehicles
    def create_vehicle_path(start, end):
        if start['lon'] == end['lon'] and start['lat'] == end['lat']:
            return None
            
        # Get path from road network
        start_loc = Location(lat=start['lat'], lon=start['lon'])
        end_loc = Location(lat=end['lat'], lon=end['lon'])
        path, _ = road_network.get_shortest_path(start_loc, end_loc)
        
        if not path:
            return None
            
        # Get coordinates for the path
        coords = road_network.get_path_coordinates(path)
        
        # Create timestamps for each point
        num_points = len(coords)
        times = np.linspace(
            BASE_TIMESTAMP + start['timestamp'],
            BASE_TIMESTAMP + end['timestamp'],
            num_points
        )
        
        # Create GeoJSON feature with timestamps
        return {
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
    
    # Create path GeoJSON for each vehicle movement
    vehicle_paths = []
    for vehicle_id, group in vehicle_df.groupby('vehicle_id'):
        for i in range(len(group) - 1):
            start = group.iloc[i]
            end = group.iloc[i + 1]
            path = create_vehicle_path(start, end)
            if path:
                vehicle_paths.append({
                    'vehicle_id': str(vehicle_id),
                    'old_state': str(start['old_state']),
                    'new_state': str(start['new_state']),
                    'battery_level_pct': float(start['battery_level_pct']),
                    'distance': float(end['km_traveled'] - start['km_traveled']),
                    'timestamp': int(BASE_TIMESTAMP + start['timestamp']),
                    'datetime': str(start['datetime']),
                    '_geojson': path
                })
    
    vehicle_paths_df = pd.DataFrame(vehicle_paths)
    
    # 2. Trip paths with interpolated points
    def create_trip_path(trip):
        # Get path from road network
        origin = Location(lat=trip['origin_lat'], lon=trip['origin_lon'])
        destination = Location(lat=trip['destination_lat'], lon=trip['destination_lon'])
        path, distance = road_network.get_shortest_path(origin, destination)
        
        if not path:
            return None
            
        # Get coordinates for the path
        coords = road_network.get_path_coordinates(path)
        
        # Create timestamps for each point
        num_points = len(coords)
        start_time = BASE_TIMESTAMP + int(trip['timestamp'])
        # Estimate end time based on distance and average speed
        trip_duration_seconds = (distance / 15) * 3600  # Assume 15 mph average speed in city
        times = np.linspace(start_time, start_time + trip_duration_seconds, num_points)
        
        # Create GeoJSON feature with timestamps
        return {
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
    
    # Create paths for completed trips
    completed_trips = trip_df[trip_df['status'] == 'assigned'].copy()
    completed_trips['_geojson'] = completed_trips.apply(create_trip_path, axis=1)
    # Remove trips where no path was found
    completed_trips = completed_trips[completed_trips['_geojson'].notna()]
    # Convert numeric columns to Python types
    for col in ['fare', 'distance_miles', 'pickup_time_minutes']:
        completed_trips[col] = completed_trips[col].astype(float)
    
    trip_paths_df = completed_trips[['trip_id', 'vehicle_id', 'datetime', '_geojson', 'fare', 
                                   'distance_miles', 'pickup_time_minutes', 'status',
                                   'origin_lat', 'origin_lon', 'destination_lat', 'destination_lon']].copy()
    
    # 3. Unfulfilled trips
    unfulfilled = trip_df[trip_df['status'] == 'unfulfilled'].copy()
    unfulfilled_points = unfulfilled[['trip_id', 'datetime', 'origin_lat', 'origin_lon',
                                    'reason', 'missed_revenue']].copy()
    
    # 4. Depot location
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
    # Save GeoJSON for vehicle paths
    vehicle_paths_geojson = {
        "type": "FeatureCollection",
        "features": [path['_geojson']['features'][0] for path in vehicle_paths]
    }
    with open(f"{output_dir}/vehicle_paths_{timestamp}.geojson", 'w') as f:
        json.dump(vehicle_paths_geojson, f, default=str)
    
    # Save GeoJSON for trip paths
    trip_paths_geojson = {
        "type": "FeatureCollection",
        "features": [path['_geojson']['features'][0] for path in trip_paths_df.to_dict('records')]
    }
    with open(f"{output_dir}/trip_paths_{timestamp}.geojson", 'w') as f:
        json.dump(trip_paths_geojson, f, default=str)
    
    unfulfilled_points.to_csv(f"{output_dir}/unfulfilled_trips_{timestamp}.csv", index=False)
    depot_df.to_csv(f"{output_dir}/depots_{timestamp}.csv", index=False)
    
    # Update Kepler config for new format
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

def get_latest_log_files():
    """Get the most recent vehicle and depot log files from outputs directory."""
    # Get the directory where main.py is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'outputs')
    
    # Use absolute paths for glob
    vehicle_files = glob.glob(os.path.join(output_dir, 'vehicle_states_*.jsonl'))
    depot_files = glob.glob(os.path.join(output_dir, 'depot_events_*.jsonl'))
    trip_files = glob.glob(os.path.join(output_dir, 'trip_events_*.jsonl'))
    
    if not vehicle_files or not depot_files or not trip_files:
        print(f"Searching in directory: {output_dir}")
        print(f"Found vehicle files: {vehicle_files}")
        print(f"Found depot files: {depot_files}")
        print(f"Found trip files: {trip_files}")
        raise FileNotFoundError("Log files not found in outputs directory")
        
    # Get most recent files based on timestamp in filename
    latest_vehicle = max(vehicle_files, key=os.path.getctime)
    latest_depot = max(depot_files, key=os.path.getctime)
    latest_trip = max(trip_files, key=os.path.getctime)
    
    return latest_vehicle, latest_depot, latest_trip

def main():
    # Load config and run simulation
    config = load_config("inputs/config.yaml")
    env = simpy.Environment()
    
    print("Starting simulation...")
    env.process(simulate(env, config))
    env.run(until=config['simulation']['simulation_duration'])
    print("Simulation complete. Processing results...")
    
    # Small delay to ensure files are fully written
    time.sleep(1)
    
    # Get the most recent log files
    try:
        vehicle_log_file, depot_log_file, trip_log_file = get_latest_log_files()
        print(f"\nReading log files:\n{vehicle_log_file}\n{depot_log_file}\n{trip_log_file}")
        
        # Read logs into DataFrames
        vehicle_df = pd.read_json(vehicle_log_file, lines=True)
        depot_df = pd.read_json(depot_log_file, lines=True)
        trip_df = pd.read_json(trip_log_file, lines=True)
        
        # Add human-readable timestamps
        sim_start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        vehicle_df['datetime'] = vehicle_df['timestamp'].apply(
            lambda x: sim_start_time + timedelta(seconds=x)
        )
        depot_df['datetime'] = depot_df['timestamp'].apply(
            lambda x: sim_start_time + timedelta(seconds=x)
        )
        trip_df['datetime'] = trip_df['timestamp'].apply(
            lambda x: sim_start_time + timedelta(seconds=x)
        )
        
        # Save processed DataFrames as CSV
        vehicle_df.to_csv(vehicle_log_file.replace('.jsonl', '.csv'), index=False)
        depot_df.to_csv(depot_log_file.replace('.jsonl', '.csv'), index=False)
        trip_df.to_csv(trip_log_file.replace('.jsonl', '.csv'), index=False)
        
        # Prepare Kepler.gl visualization data
        depot_location = Location(
            lat=config['geospatial']['depot']['lat'],
            lon=config['geospatial']['depot']['lon']
        )
        service_area_center = Location(
            lat=config['geospatial']['service_area']['center']['lat'],
            lon=config['geospatial']['service_area']['center']['lon']
        )
        service_area_radius = config['geospatial']['service_area']['radius']
        
        # Create road network for path visualization (will use cache if available)
        from utils.network import RoadNetwork
        road_network = RoadNetwork(service_area_center, service_area_radius)
        
        kepler_dir = prepare_kepler_data(vehicle_df, trip_df, depot_location, road_network)
        print(f"\nKepler.gl data saved to: {kepler_dir}")
        
        # Basic analysis
        print("\n=== Simulation Summary ===")
        
        # Calculate distance traveled by state first
        vehicle_df = vehicle_df.sort_values(['vehicle_id', 'timestamp'])
        vehicle_df['next_km'] = vehicle_df.groupby('vehicle_id')['km_traveled'].shift(-1).fillna(vehicle_df['km_traveled'])
        vehicle_df['distance_in_state'] = vehicle_df['next_km'] - vehicle_df['km_traveled']
        
        # Calculate maintenance cost per state change
        vehicle_df['maintenance_cost'] = vehicle_df['distance_in_state'] * (
            config['costs']['maintenance']['vehicle_capex_per_mile'] + 
            config['costs']['maintenance']['battery_capex_per_mile']
        ) * 0.621371  # Convert km to miles for cost calculation
        
        # Now calculate financial metrics
        print("\nFinancial Performance:")
        total_revenue = trip_df[trip_df['status'] == 'assigned']['fare'].sum()
        total_energy_cost = depot_df['energy_cost'].sum()
        total_maintenance_cost = vehicle_df['maintenance_cost'].sum()
        
        # Calculate unfulfilled trip metrics
        unfulfilled_trips = trip_df[trip_df['status'] == 'unfulfilled']
        total_unfulfilled = len(unfulfilled_trips)
        total_missed_revenue = unfulfilled_trips['missed_revenue'].sum()
        unfulfilled_by_reason = unfulfilled_trips['reason'].value_counts()
        
        print(f"Total Revenue: ${total_revenue:,.2f}")
        print(f"Missed Revenue: ${total_missed_revenue:,.2f}")
        print(f"Operating Costs:")
        print(f"  Energy: ${total_energy_cost:,.2f}")
        print(f"  Maintenance: ${total_maintenance_cost:,.2f}")
        total_costs = total_energy_cost + total_maintenance_cost
        operating_income = total_revenue - total_costs
        print(f"Total Operating Costs: ${total_costs:,.2f}")
        print(f"Operating Income: ${operating_income:,.2f}")
        print(f"Operating Margin: {(operating_income/total_revenue)*100:.1f}%")
        
        print("\nTrip Fulfillment:")
        total_trips = len(trip_df)
        print(f"Total Trips Requested: {total_trips}")
        print(f"Trips Fulfilled: {len(trip_df[trip_df['status'] == 'assigned'])}")
        print(f"Trips Unfulfilled: {total_unfulfilled}")
        print(f"Fulfillment Rate: {(1 - total_unfulfilled/total_trips)*100:.1f}%")
        print("\nUnfulfilled Trip Reasons:")
        for reason, count in unfulfilled_by_reason.items():
            print(f"  {reason}: {count} ({count/total_unfulfilled*100:.1f}%)")
        
        # Vehicle statistics
        print("\nVehicle Statistics:")
        final_states = vehicle_df.groupby('vehicle_id').last()
        print(f"Total vehicles: {len(final_states)}")
        print(f"Average distance per vehicle: {final_states['km_traveled'].mean():.1f} km")
        print(f"Average trips per vehicle: {final_states['trips_completed'].mean():.1f}")
        
        # Get all unique states from both old_state and new_state
        all_states = sorted(set(vehicle_df['old_state'].unique()) | set(vehicle_df['new_state'].unique()))
        
        # Group by new_state to capture distances in each state
        state_metrics = {}
        for state in all_states:
            # Count occurrences (state transitions)
            occurrences = len(vehicle_df[vehicle_df['new_state'] == state])
            # Sum distances while in this state
            total_distance = vehicle_df[vehicle_df['new_state'] == state]['distance_in_state'].sum()
            # Calculate average
            avg_distance = total_distance / occurrences if occurrences > 0 else 0
            
            state_metrics[state] = {
                'occurrences': occurrences,
                'total_distance': total_distance,
                'avg_distance': avg_distance
            }
        
        # Print state metrics
        for state in all_states:
            metrics = state_metrics[state]
            print(f"{state}:")
            print(f"  Occurrences: {metrics['occurrences']}")
            print(f"  Total distance: {metrics['total_distance']:.1f} km")
            print(f"  Average per occurrence: {metrics['avg_distance']:.1f} km")
        
        # State transitions
        print("\nState Transitions:")
        transitions = vehicle_df.groupby(['old_state', 'new_state']).size().reset_index(name='count')
        transitions = transitions.sort_values('count', ascending=False)
        
        for _, row in transitions.iterrows():
            print(f"{row['old_state']} -> {row['new_state']}: {row['count']}")
        
        # Charging statistics
        print("\nCharging Depot Statistics:")
        print(f"Total energy delivered: {depot_df['total_depot_energy'].max():.1f} kWh")
        print(f"Total charging events: {len(depot_df)}")
        print(f"Average energy per charging event: {depot_df['energy_delivered'].mean():.1f} kWh")
        print(f"Average charging duration: {depot_df['charge_duration_minutes'].mean():.1f} minutes")
        
        # Queue statistics
        print(f"Max vehicles in queue: {depot_df['vehicles_queued'].max()}")
        print(f"Average queue length: {depot_df['vehicles_queued'].mean():.2f}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure the simulation has generated log files in the outputs directory")

if __name__ == "__main__":
    main()
