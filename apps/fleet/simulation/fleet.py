import simpy
import random
import pandas as pd
from datetime import datetime, timedelta

class Vehicle:
    def __init__(self, env, id, battery_capacity, efficiency, state_log):
        self.env = env
        self.id = id
        self.battery_capacity = battery_capacity  # kWh
        self.efficiency = efficiency  # miles per kWh
        self.battery_level = battery_capacity
        self.state = "idle"
        self.km_traveled = 0
        self.trips_completed = 0
        self.state_log = state_log
        
    def set_state(self, new_state):
        if new_state != self.state:
            # Print to console
            print(f"Vehicle {self.id} state change: {self.state} -> {new_state} | "
                  f"KM_TRAVELED: {self.km_traveled:.1f} | "
                  f"BATTERY_CHARGE_LEVEL: {(self.battery_level/self.battery_capacity)*100:.1f}% | "
                  f"TRIPS_COMPLETED: {self.trips_completed}")
            
            # Log to DataFrame
            self.state_log.append({
                'timestamp': self.env.now,
                'vehicle_id': self.id,
                'old_state': self.state,
                'new_state': new_state,
                'km_traveled': self.km_traveled,
                'battery_level_pct': (self.battery_level/self.battery_capacity)*100,
                'trips_completed': self.trips_completed
            })
            
            self.state = new_state

    def drive(self, distance_miles, is_repositioning=False, maintain_state=False):
        """
        Drive the vehicle a certain distance.
        maintain_state: If True, don't change state at start/end (used for en_route_to_depot)
        """
        if not (is_repositioning or maintain_state):
            self.set_state("on_trip")
            
        # Convert miles to km for tracking
        distance_km = distance_miles * 1.60934
        
        # Calculate energy usage (repositioning uses less energy due to lighter traffic)
        energy_used = distance_miles / (self.efficiency * (1.2 if is_repositioning else 1.0))
        self.battery_level -= energy_used
        
        # Update distance in km
        self.km_traveled += distance_km
        
        # Driving time calculation:
        if is_repositioning:
            # Faster average speed during repositioning (less traffic)
            drive_time_minutes = (distance_miles / 35) * 60
            total_time_seconds = drive_time_minutes * 60
        else:
            # Regular trip timing with pickup/dropoff
            drive_time_minutes = (distance_miles / 30) * 60
            service_time_minutes = random.uniform(5, 10)
            total_time_seconds = (drive_time_minutes + service_time_minutes) * 60
        
        yield self.env.timeout(total_time_seconds)
        if not (is_repositioning or maintain_state):
            self.trips_completed += 1
            self.set_state("idle")

    def reposition(self):
        """Simulate vehicle repositioning during idle time."""
        # Shorter distances for repositioning (1-3 miles)
        distance_miles = random.uniform(1, 3)
        yield self.env.process(self.drive(distance_miles, is_repositioning=True))

    def charge(self, charger):
        """Actually charge the vehicle once a charger is available."""
        self.set_state("charging")
        required_energy = self.battery_capacity - self.battery_level
        # Charging time in minutes, convert to seconds for timeout
        charge_time_seconds = (required_energy / charger.power) * 60 * 60
        yield self.env.timeout(charge_time_seconds)
        self.battery_level = self.battery_capacity
        self.set_state("idle")

    def go_to_depot(self):
        """Travel to the charging depot."""
        # Assume average 2-4 miles to depot
        distance_miles = random.uniform(2, 4)
        yield self.env.process(self.drive(distance_miles, is_repositioning=True, maintain_state=True))
