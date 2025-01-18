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
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    vehicle_files = glob.glob(os.path.join(output_dir, '**/logs/vehicle_states.jsonl'), recursive=True)
    depot_files = glob.glob(os.path.join(output_dir, '**/logs/depot_events.jsonl'), recursive=True)
    trip_files = glob.glob(os.path.join(output_dir, '**/logs/trip_events.jsonl'), recursive=True)
        
    return (max(f, key=os.path.getctime) for f in [vehicle_files, depot_files, trip_files])

def print_summary_statistics(vehicle_df: pd.DataFrame, trip_df: pd.DataFrame, depot_df: pd.DataFrame, config: dict):
    """Print summary statistics for the simulation run."""
    print("\nSimulation Summary:")
    print("-" * 50)
    
    # Trip statistics
    total_trips = len(trip_df)
    completed_trips = len(trip_df[trip_df['status'] == 'assigned'])
    unfulfilled_trips = len(trip_df[trip_df['status'] == 'unfulfilled'])
    
    print(f"\nTrip Statistics:")
    print(f"Total Trips Requested: {total_trips}")
    print(f"Completed Trips: {completed_trips} ({(completed_trips/total_trips)*100:.1f}%)")
    print(f"Unfulfilled Trips: {unfulfilled_trips} ({(unfulfilled_trips/total_trips)*100:.1f}%)")
    
    if 'reason' in trip_df.columns:
        reasons = trip_df[trip_df['status'] == 'unfulfilled']['reason'].value_counts()
        print("\nUnfulfilled Trip Reasons:")
        for reason, count in reasons.items():
            print(f"- {reason}: {count} ({(count/unfulfilled_trips)*100:.1f}%)")
    
    # Vehicle statistics
    total_vehicles = len(vehicle_df['vehicle_id'].unique())
    total_distance = vehicle_df['km_traveled'].max()
    avg_battery = vehicle_df['battery_level_pct'].mean()
    
    print(f"\nVehicle Statistics:")
    print(f"Total Vehicles: {total_vehicles}")
    print(f"Total Distance Traveled: {total_distance:.1f} km")
    print(f"Average Battery Level: {avg_battery:.1f}%")
    
    # State distribution
    if 'new_state' in vehicle_df.columns:
        states = vehicle_df['new_state'].value_counts()
        print("\nVehicle State Distribution:")
        for state, count in states.items():
            print(f"- {state}: {count} ({(count/len(vehicle_df))*100:.1f}%)")
    
    # Depot statistics
    total_energy = depot_df['energy_delivered'].sum()
    total_charging_events = len(depot_df)
    avg_charge_duration = depot_df['charge_duration_minutes'].mean()
    total_energy_cost = depot_df['energy_cost'].sum()
    charger_utilization = (depot_df['chargers_in_use'].mean() / 
                          config['charging_infrastructure']['chargers_per_depot']) * 100
    
    print(f"\nDepot Statistics:")
    print(f"Total Energy Delivered: {total_energy:.1f} kWh")
    print(f"Total Charging Events: {total_charging_events}")
    print(f"Average Charge Duration: {avg_charge_duration:.1f} minutes")
    print(f"Charger Utilization: {charger_utilization:.1f}%")
    print(f"Total Energy Cost: ${total_energy_cost:.2f}")
    
    # Operating Income Statement
    print(f"\nOperating Income Statement:")
    print("-" * 50)
    
    # Revenue
    completed_trips_revenue = trip_df[trip_df['status'] == 'assigned']['fare'].sum() if 'fare' in trip_df.columns else 0
    # Handle missing missed_revenue column
    if 'missed_revenue' in trip_df.columns:
        missed_revenue = trip_df[trip_df['status'] == 'unfulfilled']['missed_revenue'].sum()
    else:
        # Calculate missed revenue from fare if available
        missed_revenue = trip_df[trip_df['status'] == 'unfulfilled']['fare'].sum() if 'fare' in trip_df.columns else 0
    
    # Costs
    maintenance_costs = vehicle_df['maintenance_cost'].sum() if 'maintenance_cost' in vehicle_df.columns else 0
    energy_costs = total_energy_cost if 'energy_cost' in depot_df.columns else 0
    
    # Calculate metrics
    gross_revenue = completed_trips_revenue
    total_costs = maintenance_costs + energy_costs
    operating_income = gross_revenue - total_costs
    operating_margin = (operating_income / gross_revenue * 100) if gross_revenue > 0 else 0
    
    print(f"Revenue:")
    print(f"  Completed Trips Revenue: ${completed_trips_revenue:.2f}")
    print(f"  Missed Revenue: ${missed_revenue:.2f}")
    print(f"\nCosts:")
    print(f"  Energy Costs: ${energy_costs:.2f}")
    print(f"  Maintenance Costs: ${maintenance_costs:.2f}")
    print(f"  Total Costs: ${total_costs:.2f}")
    print(f"\nOperating Metrics:")
    print(f"  Gross Revenue: ${gross_revenue:.2f}")
    print(f"  Operating Income: ${operating_income:.2f}")
    print(f"  Operating Margin: {operating_margin:.1f}%")

def main():
    """Main simulation entry point."""
    print("\nStarting simulation...")
    simulation_start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create output directory structure
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sim_dir = os.path.join(base_dir, 'outputs', timestamp)
    logs_dir = os.path.join(sim_dir, 'logs')
    csv_dir = os.path.join(sim_dir, 'csv')
    kepler_dir = os.path.join(sim_dir, 'kepler')
    
    # Create all directories
    for directory in [logs_dir, csv_dir, kepler_dir]:
        os.makedirs(directory, exist_ok=True)
    
    # Set environment variable for simulation output directory
    os.environ['SIMULATION_OUTPUT_DIR'] = sim_dir
    
    # Load config and run simulation
    config = load_config("inputs/config.yaml")
    
    env = simpy.Environment()
    env.process(simulate(env, config))
    env.run(until=config['simulation']['simulation_duration'])
    
    # Small delay to ensure files are written
    time.sleep(1)
    
    # Process results and create visualization
    vehicle_log = os.path.join(logs_dir, 'vehicle_states.jsonl')
    depot_log = os.path.join(logs_dir, 'depot_events.jsonl')
    trip_log = os.path.join(logs_dir, 'trip_events.jsonl')
    
    vehicle_df = pd.read_json(vehicle_log, lines=True)
    trip_df = pd.read_json(trip_log, lines=True)
    depot_df = pd.read_json(depot_log, lines=True)
    
    # Print summary statistics
    print_summary_statistics(vehicle_df, trip_df, depot_df, config)
    
    # Save summary CSVs
    vehicle_df.to_csv(os.path.join(csv_dir, 'vehicle_states.csv'), index=False)
    trip_df.to_csv(os.path.join(csv_dir, 'trip_events.csv'), index=False)
    depot_df.to_csv(os.path.join(csv_dir, 'depot_events.csv'), index=False)
    
    depot_location = Location(
        lat=config['geospatial']['depot']['lat'],
        lon=config['geospatial']['depot']['lon']
    )
    road_network = RoadNetwork(
        center=depot_location,
        radius_miles=config['geospatial']['service_area']['radius']
    )
    
    # Save network polygon to kepler directory
    road_network.save_network_polygon(sim_dir)
    
    # Prepare Kepler visualization (it will save files to kepler_dir)
    prepare_kepler_data(vehicle_df, trip_df, depot_location, road_network, output_dir=kepler_dir)
    
    # Print total time
    total_time = time.time() - simulation_start_time
    print(f"\nSimulation completed in {total_time:.2f} seconds")
    print(f"Results available in {sim_dir}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
