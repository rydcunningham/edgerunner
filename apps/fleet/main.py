import simpy
from utils.io import load_config
from simulation.simulation import simulate
from utils.geo import Location
from utils.network import RoadNetwork
from utils.timing import timer
from utils.visualization import prepare_kepler_data
import pandas as pd
import os
from datetime import datetime
import glob
import time
import sys

def get_latest_log_files():
    """Get the most recent vehicle and depot log files from outputs directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'outputs')
    
    vehicle_files = glob.glob(os.path.join(output_dir, 'vehicle_states_*.jsonl'))
    depot_files = glob.glob(os.path.join(output_dir, 'depot_events_*.jsonl'))
    trip_files = glob.glob(os.path.join(output_dir, 'trip_events_*.jsonl'))
    
    if not vehicle_files or not depot_files or not trip_files:
        raise FileNotFoundError("Log files not found in outputs directory")
        
    return (max(f, key=os.path.getctime) for f in [vehicle_files, depot_files, trip_files])

def main():
    """Main simulation entry point."""
    print("\nStarting simulation...")
    simulation_start_time = time.time()
    
    # Load config and run simulation
    config = load_config("inputs/config.yaml")
    
    env = simpy.Environment()
    env.process(simulate(env, config))
    env.run(until=config['simulation']['simulation_duration'])
    
    # Small delay to ensure files are written
    time.sleep(1)
    
    # Process results and create visualization
    vehicle_log, depot_log, trip_log = get_latest_log_files()
    vehicle_df = pd.read_json(vehicle_log, lines=True)
    trip_df = pd.read_json(trip_log, lines=True)
    
    depot_location = Location(
        lat=config['geospatial']['depot']['lat'],
        lon=config['geospatial']['depot']['lon']
    )
    road_network = RoadNetwork(
        center=depot_location,
        radius_miles=config['geospatial']['service_area']['radius']
    )
    
    kepler_dir = prepare_kepler_data(vehicle_df, trip_df, depot_location, road_network)
    
    # Print total time
    total_time = time.time() - simulation_start_time
    print(f"Simulation completed in {total_time:.2f} seconds")
    print(f"Results available in {kepler_dir}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
