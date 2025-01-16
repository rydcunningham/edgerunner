import simpy
import random
import pandas as pd
from datetime import datetime, timedelta
from utils.geo import Location, haversine_distance, random_point_in_radius, is_point_in_service_area

class Vehicle:
    def __init__(self, env, id, battery_capacity, efficiency, state_log, depot_location, initial_radius):
        self.env = env
        self.id = id
        self.battery_capacity = battery_capacity  # kWh
        self.efficiency = efficiency  # miles per kWh
        self.battery_level = battery_capacity
        self.state = "idle"
        self.km_traveled = 0
        self.trips_completed = 0
        self.state_log = state_log
        
        # Initialize location randomly within initial radius of depot
        self.current_location = random_point_in_radius(depot_location, initial_radius)
        self.depot_location = depot_location
        
    def set_state(self, new_state):
        if new_state != self.state:
            # Print to console
            print(f"Vehicle {self.id} state change: {self.state} -> {new_state} | "
                  f"KM_TRAVELED: {self.km_traveled:.1f} | "
                  f"BATTERY_CHARGE_LEVEL: {(self.battery_level/self.battery_capacity)*100:.1f}% | "
                  f"TRIPS_COMPLETED: {self.trips_completed} | "
                  f"LOCATION: ({self.current_location.lat:.3f}, {self.current_location.lon:.3f})")
            
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
                'lon': self.current_location.lon
            })
            
            self.state = new_state

    def update_location(self, new_location: Location, distance_miles: float):
        """Update vehicle location and energy usage based on distance traveled."""
        self.current_location = new_location
        energy_used = distance_miles / self.efficiency
        self.battery_level -= energy_used
        self.km_traveled += distance_miles * 1.60934  # Convert miles to km

    def drive_to_location(self, destination: Location, is_repositioning=False):
        """Drive to a specific location."""
        distance = haversine_distance(self.current_location, destination)
        
        # Calculate driving time based on distance and speed
        if is_repositioning:
            speed = 25  # mph during repositioning
        else:
            speed = 15  # mph in city traffic
        
        drive_time_minutes = (distance / speed) * 60
        total_time_seconds = drive_time_minutes * 60
        
        # Update location and energy
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
        """Travel to the charging depot."""
        distance = haversine_distance(self.current_location, self.depot_location)
        yield self.env.process(self.drive_to_location(self.depot_location, is_repositioning=True))

    def go_to_rider(self, pickup_location: Location):
        """Travel to pick up a rider."""
        self.set_state("en_route_to_rider")
        yield self.env.process(self.drive_to_location(pickup_location, is_repositioning=True))

    def start_trip(self, origin: Location, destination: Location):
        """Start a trip from origin to destination."""
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
