import math
import random
import h3
from dataclasses import dataclass
from typing import Tuple
from utils.optimized import haversine_distance_numba

class Location:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        # Add H3 hexagon ID at resolution 7 using H3 4.0+ method
        self.h3_cell = h3.latlng_to_cell(lat, lon, 7)
    
    def __str__(self):
        return f"({self.lat}, {self.lon})"
    
    def __repr__(self):
        return self.__str__()
        
    def __iter__(self):
        """Make Location iterable to support tuple unpacking of (lat, lon)."""
        yield self.lat
        yield self.lon

def haversine_distance(loc1: Location, loc2: Location) -> float:
    """Calculate the great circle distance between two points on Earth using Numba-optimized function."""
    return haversine_distance_numba(loc1.lat, loc1.lon, loc2.lat, loc2.lon)

def random_point_in_radius(center: Location, radius_miles: float) -> Location:
    """Generate a random point within radius miles of center."""
    # Convert miles to km
    radius_km = radius_miles * 1.60934
    
    # Convert radius from km to degrees (approximate, assuming spherical Earth)
    radius_deg = radius_km / 111.32  # 1 degree is approximately 111.32 km
    
    while True:
        # Generate random angle and radius
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, radius_deg)
        
        # Convert to lat/lon offset
        dlat = r * math.cos(angle)
        dlon = r * math.sin(angle) / math.cos(math.radians(center.lat))
        
        # Calculate new point
        new_lat = center.lat + dlat
        new_lon = center.lon + dlon
        
        # Create new location
        new_loc = Location(new_lat, new_lon)
        
        # Check if point is within service area
        if is_point_in_service_area(new_loc, center, radius_miles):
            return new_loc

def is_point_in_service_area(point: Location, center: Location, radius_miles: float) -> bool:
    """Check if a point is within the service area."""
    distance_km = haversine_distance(point, center)
    distance_miles = distance_km / 1.60934
    return distance_miles <= radius_miles

def find_nearest_vehicle(origin: Location, vehicles: list, max_distance_miles: float = float('inf')) -> tuple:
    """Find the nearest available vehicle within max_distance_miles."""
    min_distance = float('inf')
    nearest_idx = -1
    
    for i, vehicle in enumerate(vehicles):
        if vehicle.state != "idle":
            continue
            
        distance_km = haversine_distance(origin, vehicle.current_location)
        distance_miles = distance_km / 1.60934
        
        if distance_miles <= max_distance_miles and distance_miles < min_distance:
            min_distance = distance_miles
            nearest_idx = i
    
    return nearest_idx, min_distance 