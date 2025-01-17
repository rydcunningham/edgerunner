import simpy
import pandas as pd
import h3
from utils.geo import Location

class Charger:
    def __init__(self, id, power):
        self.id = id
        self.power = power  # kW
        self.total_energy_delivered = 0  # kWh

class ChargingDepot:
    def __init__(self, env, num_chargers, charger_power, depot_log, write_log_fn, location: Location):
        self.env = env
        self.chargers = simpy.Resource(env, num_chargers)
        self.charger_power = charger_power
        self.total_energy_delivered = 0  # kWh
        self.num_chargers = num_chargers
        self.depot_log = depot_log
        self.write_log_fn = write_log_fn
        self.location = location
        
        # Track service area hexagons (1 hex radius around depot)
        self.service_area_cells = {location.h3_cell}
        self.service_area_cells.update(h3.grid_ring(location.h3_cell, 1))
        
    def is_in_service_area(self, vehicle_location: Location) -> bool:
        """Check if a vehicle is in the depot's service area using H3."""
        return vehicle_location.h3_cell in self.service_area_cells
    
    def get_vehicles_in_range(self, vehicles: list) -> list:
        """Find all vehicles within the depot's service area."""
        return [v for v in vehicles if self.is_in_service_area(v.current_location)]
        
    def log_charging_event(self, vehicle_id, energy_delivered, charge_duration):
        # Print to console
        print(f"Charging Event | Depot Usage: Vehicle {vehicle_id} | "
              f"Energy Delivered: {energy_delivered:.1f} kWh | "
              f"Duration: {charge_duration/60:.1f} min | "
              f"Total Depot Energy: {self.total_energy_delivered:.1f} kWh | "
              f"Chargers Available: {self.chargers.capacity - len(self.chargers.queue) - len(self.chargers.users)}/{self.num_chargers}")
        
        # Log to list
        self.depot_log.append({
            'timestamp': self.env.now,
            'vehicle_id': vehicle_id,
            'energy_delivered': energy_delivered,
            'charge_duration_minutes': charge_duration/60,
            'total_depot_energy': self.total_energy_delivered,
            'chargers_in_use': len(self.chargers.users),
            'vehicles_queued': len(self.chargers.queue),
            'depot_lat': self.location.lat,
            'depot_lon': self.location.lon,
            'depot_h3_cell': str(self.location.h3_cell),
            'service_area_cells': [str(cell) for cell in self.service_area_cells]
        })
        
        # Write logs if we have enough entries
        if len(self.depot_log) >= 10:
            self.write_log_fn()

    def charge_vehicle(self, vehicle):
        # Vehicle is already in in_charger_queue state from go_to_depot()
        with self.chargers.request() as req:
            yield req
            
            # Calculate charging metrics
            required_energy = vehicle.battery_capacity - vehicle.battery_level
            charge_time_seconds = (required_energy / self.charger_power) * 60 * 60
            
            # Update vehicle - this will change state to charging
            yield self.env.process(vehicle.charge(Charger(0, self.charger_power)))
            
            # Update depot metrics
            self.total_energy_delivered += required_energy
            
            # Log the charging event
            self.log_charging_event(vehicle.id, required_energy, charge_time_seconds)
