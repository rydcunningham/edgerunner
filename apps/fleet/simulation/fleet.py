import simpy
import random
import pandas as pd
import h3
from datetime import datetime, timedelta
from utils.geo import Location, haversine_distance, random_point_in_radius, is_point_in_service_area

class VehicleStateBuffer:
    def __init__(self, batch_size=100):
        self.buffer = []
        self.batch_size = batch_size
    
    def log_state_change(self, vehicle):
        """Buffer a state change message."""
        message = (f"Vehicle {vehicle.id} state change: {vehicle.state} -> {vehicle.new_state} | "
                  f"KM_TRAVELED: {vehicle.km_traveled:.1f} | "
                  f"BATTERY_CHARGE_LEVEL: {(vehicle.battery_level/vehicle.battery_capacity)*100:.1f}% | "
                  f"TRIPS_COMPLETED: {vehicle.trips_completed} | "
                  f"LOCATION: ({vehicle.current_location.lat:.3f}, {vehicle.current_location.lon:.3f})")
        self.buffer.append(message)
        
        if len(self.buffer) >= self.batch_size:
            self.flush()
    
    def flush(self):
        """Print all buffered messages."""
        if self.buffer:
            print("\n".join(self.buffer))
            self.buffer.clear()

# Global state buffer
state_buffer = VehicleStateBuffer()

class Vehicle:
    def __init__(self, env, id, battery_capacity, efficiency, state_log, depot_location, initial_radius, road_network):
        self.env = env
        self.id = id
        self.battery_capacity = battery_capacity  # kWh
        self.efficiency = efficiency  # miles per kWh
        self.battery_level = battery_capacity
        self.state = "idle"
        self.new_state = None  # For logging purposes
        self.km_traveled = 0
        self.trips_completed = 0
        self.state_log = state_log
        self.road_network = road_network
        
        # Initialize location randomly within initial radius of depot
        self.current_location = random_point_in_radius(depot_location, initial_radius)
        self.depot_location = depot_location
        
        # Track visited H3 cells
        self.visited_cells = {self.current_location.h3_cell}
        
    def set_state(self, new_state):
        if new_state != self.state:
            self.new_state = new_state  # Store new state for logging
            
            # Buffer the console output
            state_buffer.log_state_change(self)
            
            # Log to DataFrame
            self.state_log.append({
                'timestamp': self.env.now,
                'vehicle_id': self.id,
                'old_state': self.state,
                'new_state': new_state,
                'km_traveled': self.km_traveled,
                'battery_level_pct': (self.battery_level/self.battery_capacity)*100,
                'trips_completed': self.trips_completed,
                'lat': self.current_location.lat,
                'lon': self.current_location.lon,
                'h3_cell': self.current_location.h3_cell,  # Store as integer
                'visited_cells_count': len(self.visited_cells)
            })
            
            self.state = new_state

    def update_location(self, new_location: Location, distance_miles: float):
        """Update vehicle location and energy usage based on distance traveled."""
        self.current_location = new_location
        # Track new H3 cell
        self.visited_cells.add(new_location.h3_cell)
        energy_used = distance_miles / self.efficiency
        self.battery_level -= energy_used
        self.km_traveled += distance_miles * 1.60934  # Convert miles to km
    
    def get_nearby_vehicles(self, vehicles: list, radius_hexes: int = 1) -> list:
        """Find vehicles within radius_hexes of current location using H3."""
        current_cell = self.current_location.h3_cell
        nearby_cells = {current_cell}
        
        # Get ring of cells at each radius
        for k in range(1, radius_hexes + 1):
            ring_cells = h3.grid_ring(current_cell, k)
            nearby_cells.update(ring_cells)
        
        # Find vehicles in nearby cells
        nearby = []
        for v in vehicles:
            if v.id != self.id and v.current_location.h3_cell in nearby_cells:
                nearby.append(v)
        
        return nearby
    
    def get_coverage_stats(self) -> dict:
        """Get statistics about the vehicle's coverage area."""
        return {
            'unique_cells_visited': len(self.visited_cells),
            'current_cell': str(self.current_location.h3_cell),
            'current_cell_neighbors': [str(c) for c in h3.grid_ring(self.current_location.h3_cell, 1)]
        }

    def drive_to_location(self, destination: Location, is_repositioning=False):
        """Drive to a specific location using road network."""
        # Get shortest path and distance from road network
        path, distance = self.road_network.get_shortest_path(self.current_location, destination)
        
        # Calculate driving time based on distance and speed
        if is_repositioning:
            speed = 25  # mph during repositioning
        else:
            speed = 15  # mph in city traffic
        
        drive_time_minutes = (distance / speed) * 60
        total_time_seconds = drive_time_minutes * 60
        
        # Get interpolated points along the path
        if path:
            waypoints = self.road_network.interpolate_path(path)
            # Move through each waypoint
            for point in waypoints:
                # Calculate segment distance
                segment_distance = distance / len(waypoints)
                # Update location and energy for this segment
                self.update_location(point, segment_distance)
                # Small delay for segment
                yield self.env.timeout(total_time_seconds / len(waypoints))
        else:
            # Fallback to direct route if no path found
            self.update_location(destination, distance)
            yield self.env.timeout(total_time_seconds)

    def drive(self, distance_miles, is_repositioning=False, maintain_state=False):
        """
        Drive the vehicle a certain distance.
        maintain_state: If True, don't change state at start/end (used for en_route_to_depot)
        """
        if not (is_repositioning or maintain_state):
            self.set_state("on_trip")
        
        # Generate a random destination within the given distance
        destination = random_point_in_radius(self.current_location, distance_miles)
        yield self.env.process(self.drive_to_location(destination, is_repositioning))
        
        if not (is_repositioning or maintain_state):
            self.trips_completed += 1
            self.set_state("idle")

    def go_to_depot(self):
        """Travel to the charging depot using road network."""
        self.set_state("en_route_to_depot")
        yield self.env.process(self.drive_to_location(self.depot_location, is_repositioning=True))

    def go_to_rider(self, pickup_location: Location):
        """Travel to pick up a rider using road network."""
        self.set_state("en_route_to_rider")
        yield self.env.process(self.drive_to_location(pickup_location, is_repositioning=True))

    def start_trip(self, origin: Location, destination: Location):
        """Start a trip from origin to destination using road network."""
        # First go to pick up the rider
        yield self.env.process(self.go_to_rider(origin))
        
        # Small delay for pickup
        yield self.env.timeout(60)  # 1 minute for pickup
        
        # Then drive to the destination
        self.set_state("on_trip")
        yield self.env.process(self.drive_to_location(destination, is_repositioning=False))
        
        # Small delay for dropoff
        yield self.env.timeout(30)  # 30 seconds for dropoff
        
        self.trips_completed += 1
        self.set_state("idle")

    def reposition(self):
        """Simulate vehicle repositioning during idle time."""
        # Shorter distances for repositioning (1-3 miles)
        distance_miles = random.uniform(1, 3)
        destination = random_point_in_radius(self.current_location, distance_miles)
        yield self.env.process(self.drive_to_location(destination, is_repositioning=True))

    def charge(self, charger):
        """Actually charge the vehicle once a charger is available."""
        self.set_state("charging")
        required_energy = self.battery_capacity - self.battery_level
        # Charging time in minutes, convert to seconds for timeout
        charge_time_seconds = (required_energy / charger.power) * 60 * 60
        yield self.env.timeout(charge_time_seconds)
        self.battery_level = self.battery_capacity
        self.set_state("idle")
