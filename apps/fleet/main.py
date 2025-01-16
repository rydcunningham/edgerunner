import simpy
from utils.io import load_config
from simulation.simulation import simulate
import pandas as pd
import os
from datetime import datetime, timedelta
import glob
import time

def get_latest_log_files():
    """Get the most recent vehicle and depot log files from outputs directory."""
    # Get the directory where main.py is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'outputs')
    
    # Use absolute paths for glob
    vehicle_files = glob.glob(os.path.join(output_dir, 'vehicle_states_*.jsonl'))
    depot_files = glob.glob(os.path.join(output_dir, 'depot_events_*.jsonl'))
    
    if not vehicle_files or not depot_files:
        print(f"Searching in directory: {output_dir}")
        print(f"Found vehicle files: {vehicle_files}")
        print(f"Found depot files: {depot_files}")
        raise FileNotFoundError("Log files not found in outputs directory")
        
    # Get most recent files based on timestamp in filename
    latest_vehicle = max(vehicle_files, key=os.path.getctime)
    latest_depot = max(depot_files, key=os.path.getctime)
    
    return latest_vehicle, latest_depot

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
        vehicle_log_file, depot_log_file = get_latest_log_files()
        print(f"\nReading log files:\n{vehicle_log_file}\n{depot_log_file}")
        
        # Read logs into DataFrames
        vehicle_df = pd.read_json(vehicle_log_file, lines=True)
        depot_df = pd.read_json(depot_log_file, lines=True)
        
        # Add human-readable timestamps
        sim_start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        vehicle_df['datetime'] = vehicle_df['timestamp'].apply(
            lambda x: sim_start_time + timedelta(seconds=x)
        )
        depot_df['datetime'] = depot_df['timestamp'].apply(
            lambda x: sim_start_time + timedelta(seconds=x)
        )
        
        # Save processed DataFrames as CSV
        vehicle_df.to_csv(vehicle_log_file.replace('.jsonl', '.csv'), index=False)
        depot_df.to_csv(depot_log_file.replace('.jsonl', '.csv'), index=False)
        
        # Basic analysis
        print("\n=== Simulation Summary ===")
        
        # Vehicle statistics
        print("\nVehicle Statistics:")
        final_states = vehicle_df.groupby('vehicle_id').last()
        print(f"Total vehicles: {len(final_states)}")
        print(f"Average distance per vehicle: {final_states['km_traveled'].mean():.1f} km")
        print(f"Average trips per vehicle: {final_states['trips_completed'].mean():.1f}")
        
        # Calculate distance traveled by state
        print("\nDistance by State:")
        # Calculate distance traveled between each state change
        vehicle_df = vehicle_df.sort_values(['vehicle_id', 'timestamp'])
        vehicle_df['next_km'] = vehicle_df.groupby('vehicle_id')['km_traveled'].shift(-1).fillna(vehicle_df['km_traveled'])
        vehicle_df['distance_in_state'] = vehicle_df['next_km'] - vehicle_df['km_traveled']
        
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
