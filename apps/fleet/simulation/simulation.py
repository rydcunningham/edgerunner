from simulation.fleet import Vehicle
from simulation.chargers import ChargingDepot
from utils.geo import Location, random_point_in_radius, is_point_in_service_area, find_nearest_vehicle, haversine_distance
from utils.network import RoadNetwork
import random
import pandas as pd
import json
from datetime import datetime
import os

def get_surge_multiplier(env_time, config):
    """Get the surge multiplier based on time of day."""
    if (config['pricing']['surge_periods']['morning_rush']['start_time'] <= env_time < 
        config['pricing']['surge_periods']['morning_rush']['end_time']):
        return config['pricing']['surge_periods']['morning_rush']['multiplier']
    elif (config['pricing']['surge_periods']['evening_rush']['start_time'] <= env_time < 
          config['pricing']['surge_periods']['evening_rush']['end_time']):
        return config['pricing']['surge_periods']['evening_rush']['multiplier']
    return config['pricing']['surge_periods']['default']['multiplier']

def calculate_trip_fare(distance_miles, env_time, config):
    """Calculate trip fare based on distance and time of day."""
    surge = get_surge_multiplier(env_time, config)
    return (config['pricing']['base_pickup_fee'] + 
            config['pricing']['per_mile_rate'] * distance_miles * surge)

def simulate(env, config):
    """Run the simulation with the given configuration."""
    # Get output directories from environment
    output_dir = os.environ.get('SIMULATION_OUTPUT_DIR', 'outputs')
    logs_dir = os.path.join(output_dir, 'logs')
    
    # Ensure logs directory exists
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create files for logging
    vehicle_log_file = os.path.join(logs_dir, 'vehicle_states.jsonl')
    depot_log_file = os.path.join(logs_dir, 'depot_events.jsonl')
    trip_log_file = os.path.join(logs_dir, 'trip_events.jsonl')
    
    # Initialize empty log files
    for log_file in [vehicle_log_file, depot_log_file, trip_log_file]:
        with open(log_file, 'w') as f:
            pass  # Create empty file
    
    # Initialize logging lists for batch writing
    vehicle_state_log = []
    depot_log = []
    trip_log = []
    
    def write_vehicle_log():
        nonlocal vehicle_state_log
        if vehicle_state_log:
            logs_to_write = vehicle_state_log.copy()
            vehicle_state_log.clear()
            with open(vehicle_log_file, 'a') as f:
                for entry in logs_to_write:
                    # Add maintenance costs based on distance traveled
                    if 'distance_in_state' in entry:
                        entry['maintenance_cost'] = entry['distance_in_state'] * (
                            config['costs']['maintenance']['vehicle_capex_per_mile'] + 
                            config['costs']['maintenance']['battery_capex_per_mile']
                        )
                    json.dump(entry, f)
                    f.write('\n')
    
    def write_depot_log():
        nonlocal depot_log
        if depot_log:
            logs_to_write = depot_log.copy()
            depot_log.clear()
            with open(depot_log_file, 'a') as f:
                for entry in logs_to_write:
                    # Add energy cost for charging event
                    entry['energy_cost'] = entry['energy_delivered'] * config['costs']['energy']['price_per_kwh']
                    json.dump(entry, f)
                    f.write('\n')

    def write_trip_log():
        nonlocal trip_log
        if trip_log:
            logs_to_write = trip_log.copy()
            trip_log.clear()
            with open(trip_log_file, 'a') as f:
                for entry in logs_to_write:
                    json.dump(entry, f)
                    f.write('\n')
    
    # Create depot and service area locations from config
    depot_location = Location(
        lat=config['geospatial']['depot']['lat'],
        lon=config['geospatial']['depot']['lon']
    )
    service_area_center = Location(
        lat=config['geospatial']['service_area']['center']['lat'],
        lon=config['geospatial']['service_area']['center']['lon']
    )
    service_area_radius = config['geospatial']['service_area']['radius']
    
    # Initialize road network
    road_network = RoadNetwork(service_area_center, service_area_radius)
    
    # Initialize fleet and depot with logging
    fleet = [
        Vehicle(env, i, 
               config['fleet']['battery_capacity'], 
               config['fleet']['average_miles_per_kwh'],
               vehicle_state_log,
               depot_location,
               config['fleet']['initial_spread_radius'],
               road_network)
        for i in range(config['fleet']['fleet_size'])
    ]
    depot = ChargingDepot(env, 
                         config['charging_infrastructure']['chargers_per_depot'], 
                         250,  # charger power
                         depot_log, 
                         write_depot_log,
                         location=depot_location)  # Add depot location
    
    def generate_trip_request():
        """Generate a random trip request within the service area."""
        trip_counter = 0  # Initialize counter for trip IDs
        while True:
            # Generate origin and destination from road network nodes
            origin = road_network.get_random_node_location()
            destination = road_network.get_random_node_location()
            
            # Calculate trip distance using road network
            _, trip_distance = road_network.get_shortest_path(origin, destination)
            
            # Calculate fare
            surge = get_surge_multiplier(env.now, config)
            trip_fare = calculate_trip_fare(trip_distance, env.now, config)
            
            # Log trip request with unique ID and pricing
            trip_log.append({
                'trip_id': f"TRIP_{trip_counter:06d}",
                'timestamp': env.now,
                'origin_lat': origin.lat,
                'origin_lon': origin.lon,
                'origin_h3_cell': str(origin.h3_cell),
                'destination_lat': destination.lat,
                'destination_lon': destination.lon,
                'destination_h3_cell': str(destination.h3_cell),
                'distance_miles': trip_distance,
                'surge_multiplier': surge,
                'fare': trip_fare,
                'status': 'requested'
            })
            
            # Find available vehicle
            available_vehicles = [v for v in fleet if v.state == "idle"]
            if available_vehicles:
                vehicle_idx, pickup_distance = find_nearest_vehicle(origin, available_vehicles)
                if vehicle_idx != -1:
                    # Calculate pickup time in minutes (using repositioning speed)
                    pickup_time_minutes = (pickup_distance / config['geospatial']['average_speed']['repositioning']) * 60
                    
                    if pickup_time_minutes <= 15:  # Only assign if pickup time is <= 15 minutes
                        vehicle = available_vehicles[vehicle_idx]
                        
                        # Calculate total trip energy requirements
                        # 1. Energy to get to pickup
                        pickup_energy = pickup_distance / vehicle.efficiency
                        
                        # 2. Energy for trip to destination
                        trip_energy = trip_distance / vehicle.efficiency
                        
                        # 3. Energy to return to depot from destination
                        _, depot_return_distance = road_network.get_shortest_path(destination, vehicle.depot_location)
                        depot_return_energy = depot_return_distance / vehicle.efficiency
                        
                        # Total energy required
                        total_energy_required = pickup_energy + trip_energy + depot_return_energy
                        
                        # Check if vehicle has enough battery to complete trip and return to depot
                        if vehicle.battery_level >= total_energy_required:
                            # Update trip log with assignment
                            trip_log[-1].update({
                                'vehicle_id': vehicle.id,
                                'pickup_distance': pickup_distance,
                                'pickup_time_minutes': pickup_time_minutes,
                                'status': 'assigned'
                            })
                            write_trip_log()
                            
                            # Dispatch vehicle
                            env.process(vehicle.start_trip(origin, destination))
                        else:
                            # Log as unfulfilled due to insufficient battery
                            trip_log[-1].update({
                                'status': 'unfulfilled',
                                'reason': 'insufficient_battery',
                                'nearest_pickup_distance': pickup_distance,
                                'nearest_pickup_time': pickup_time_minutes,
                                'missed_revenue': trip_fare,
                                'battery_level': vehicle.battery_level,
                                'energy_required': total_energy_required
                            })
                            write_trip_log()
                    else:
                        # Log as unfulfilled due to excessive pickup time
                        trip_log[-1].update({
                            'status': 'unfulfilled',
                            'reason': 'excessive_pickup_time',
                            'nearest_pickup_distance': pickup_distance,
                            'nearest_pickup_time': pickup_time_minutes,
                            'missed_revenue': trip_fare
                        })
                        write_trip_log()
            else:
                # Log as unfulfilled due to no available vehicles
                trip_log[-1].update({
                    'status': 'unfulfilled',
                    'reason': 'no_available_vehicles',
                    'missed_revenue': trip_fare
                })
                write_trip_log()
            
            # Increment trip counter
            trip_counter += 1
            
            # Wait for next trip request based on utilization
            avg_minutes_between_trips = 60 / (config['fleet']['utilization'] * len(fleet))
            wait_time = random.expovariate(1 / avg_minutes_between_trips)
            yield env.timeout(wait_time * 60)  # Convert to seconds

    def vehicle_behavior(vehicle):
        """Control the behavior of a single vehicle."""
        while True:
            if vehicle.state == "idle":
                # Calculate distance to depot using road network
                _, depot_distance = road_network.get_shortest_path(vehicle.current_location, vehicle.depot_location)
                
                # Calculate energy required to return to depot
                depot_return_energy = depot_distance / vehicle.efficiency
                
                # Check if battery is below 20% OR if battery is insufficient for depot return
                if (vehicle.battery_level < vehicle.battery_capacity * 0.2 or 
                    vehicle.battery_level < depot_return_energy * 1.1):  # 10% buffer
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
                    # Only reposition if no trip is currently being assigned
                    if random.random() < 0.3:  # Reduced probability since we have actual trips now
                        yield env.process(vehicle.reposition())
                    else:
                        # Wait for trip assignment
                        yield env.timeout(60)  # Check every minute
            
            # Write vehicle logs periodically
            if len(vehicle_state_log) >= 100:
                write_vehicle_log()
            
            # Small delay to prevent tight loops
            yield env.timeout(1)

    # Start the simulation processes
    for vehicle in fleet:
        env.process(vehicle_behavior(vehicle))
    
    # Start trip generation process
    env.process(generate_trip_request())
    
    # Run until simulation duration
    end_time = config['simulation']['simulation_duration']
    while env.now < end_time:
        yield env.timeout(config['simulation']['time_step'])
    
    # Write any remaining logs
    write_vehicle_log()
    write_depot_log()
    write_trip_log()
    
    return vehicle_log_file, depot_log_file, trip_log_file
