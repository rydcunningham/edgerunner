from simulation.fleet import Vehicle
from simulation.chargers import ChargingDepot
import random
import pandas as pd
import json
from datetime import datetime, timedelta
import os

def simulate(env, config):
    # Ensure output directory exists
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create files for logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    vehicle_log_file = f"{output_dir}/vehicle_states_{timestamp}.jsonl"
    depot_log_file = f"{output_dir}/depot_events_{timestamp}.jsonl"
    
    # Initialize logging lists for batch writing
    vehicle_state_log = []
    depot_log = []
    
    def write_vehicle_log():
        nonlocal vehicle_state_log
        if vehicle_state_log:
            # Create a copy of the current logs
            logs_to_write = vehicle_state_log.copy()
            # Clear the main log list
            vehicle_state_log.clear()
            # Write the copied logs
            with open(vehicle_log_file, 'a') as f:
                for entry in logs_to_write:
                    json.dump(entry, f)
                    f.write('\n')
            
    def write_depot_log():
        nonlocal depot_log
        if depot_log:
            # Create a copy of the current logs
            logs_to_write = depot_log.copy()
            # Clear the main log list
            depot_log.clear()
            # Write the copied logs
            with open(depot_log_file, 'a') as f:
                for entry in logs_to_write:
                    json.dump(entry, f)
                    f.write('\n')
    
    # Initialize fleet and depot with logging
    fleet = [
        Vehicle(env, i, config['fleet']['battery_capacity'], 
               config['fleet']['average_miles_per_kwh'],
               vehicle_state_log)
        for i in range(config['fleet']['fleet_size'])
    ]
    depot = ChargingDepot(env, config['charging_infrastructure']['chargers_per_depot'], 
                         250, depot_log, write_depot_log)

    def vehicle_behavior(vehicle):
        while True:
            if vehicle.state == "idle":
                if vehicle.battery_level < vehicle.battery_capacity * 0.2:
                    # Set state and write log before traveling
                    vehicle.set_state("en_route_to_depot")
                    write_vehicle_log()
                    yield env.process(vehicle.go_to_depot())
                    
                    # Set queue state and write log before charging
                    vehicle.set_state("in_charger_queue")
                    write_vehicle_log()
                    yield env.process(depot.charge_vehicle(vehicle))
                    write_vehicle_log()  # Capture the final state after charging
                else:
                    # Calculate wait time based on utilization
                    avg_minutes_between_trips = 60 / config['fleet']['utilization']
                    # Add some randomness with exponential distribution
                    wait_time_minutes = random.expovariate(1 / avg_minutes_between_trips)
                    
                    # During this wait time, reposition with 70% probability
                    if random.random() < 0.7:
                        yield env.process(vehicle.reposition())
                    else:
                        # If not repositioning, just wait
                        wait_time_seconds = wait_time_minutes * 60
                        yield env.timeout(wait_time_seconds)
                    
                    # Simulate a trip
                    trip_distance = random.uniform(*config['fleet']['trip_distance_range'])
                    yield env.process(vehicle.drive(trip_distance))
            
            # Write vehicle logs periodically and after state changes
            if len(vehicle_state_log) >= 100:
                write_vehicle_log()

    # Start the simulation for each vehicle
    for vehicle in fleet:
        env.process(vehicle_behavior(vehicle))
    
    # Run until simulation duration
    end_time = config['simulation']['simulation_duration']
    while env.now < end_time:
        yield env.timeout(config['simulation']['time_step'])
    
    # Write any remaining logs
    write_vehicle_log()
    write_depot_log()
    
    return vehicle_log_file, depot_log_file
