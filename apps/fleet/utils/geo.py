import math
import random
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Location:
    lat: float
    lon: float

def haversine_distance(loc1: Location, loc2: Location) -> float:
    """Calculate the great circle distance between two points in miles."""
    R = 3959.87433  # Earth's radius in miles

    lat1, lon1 = math.radians(loc1.lat), math.radians(loc1.lon)
    lat2, lon2 = math.radians(loc2.lat), math.radians(loc2.lon)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def random_point_in_radius(center: Location, radius_miles: float) -> Location:
    """Generate a random point within radius miles of center."""
    # Convert radius from miles to degrees (rough approximation)
    radius_deg = radius_miles / 69.0  # 69 miles per degree of latitude
    
    # Generate random angle and radius
    angle = random.uniform(0, 2 * math.pi)
    r = radius_deg * math.sqrt(random.uniform(0, 1))
    
    # Convert back to lat/lon
    dx = r * math.cos(angle)
    dy = r * math.sin(angle)
    
    return Location(
        lat=center.lat + dy,
        lon=center.lon + dx / math.cos(math.radians(center.lat))
    )

def is_point_in_service_area(point: Location, center: Location, radius_miles: float) -> bool:
    """Check if a point is within the service area."""
    return haversine_distance(point, center) <= radius_miles

def find_nearest_vehicle(trip_origin: Location, available_vehicles: list) -> Tuple[int, float]:
    """Find the nearest available vehicle to a trip origin.
    Returns (vehicle_index, distance_miles)"""
    if not available_vehicles:
        return -1, float('inf')
    
    distances = [
        (i, haversine_distance(trip_origin, v.current_location))
        for i, v in enumerate(available_vehicles)
    ]
    return min(distances, key=lambda x: x[1]) 