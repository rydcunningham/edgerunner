import math
import random
import h3
from dataclasses import dataclass
from typing import Tuple, Dict, Set
from utils.optimized import haversine_distance_numba
from functools import lru_cache

# Global H3 caches
_grid_ring_cache: Dict[int, Set[int]] = {}
_cell_distance_cache: Dict[Tuple[int, int], float] = {}

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

@lru_cache(maxsize=1024)
def get_grid_ring(cell: int, k: int) -> Set[int]:
    """Cached version of h3.grid_ring."""
    cache_key = cell
    if cache_key not in _grid_ring_cache:
        _grid_ring_cache[cache_key] = set(h3.grid_ring(cell, k))
    return _grid_ring_cache[cache_key]

def get_cell_distance(cell1: int, cell2: int) -> float:
    """Get cached distance between two H3 cells."""
    # Sort the cells to ensure consistent cache key regardless of order
    cache_key = tuple(sorted([cell1, cell2]))
    if cache_key not in _cell_distance_cache:
        lat1, lon1 = h3.cell_to_latlng(cell1)
        lat2, lon2 = h3.cell_to_latlng(cell2)
        _cell_distance_cache[cache_key] = haversine_distance_numba(lat1, lon1, lat2, lon2)
    return _cell_distance_cache[cache_key]

def haversine_distance(loc1: Location, loc2: Location) -> float:
    """Calculate the great circle distance between two points on Earth using Numba-optimized function."""
    # Try cell-based distance first if cells are different
    if loc1.h3_cell != loc2.h3_cell:
        return get_cell_distance(loc1.h3_cell, loc2.h3_cell)
    # Fall back to exact calculation for same cell or very close points
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

def find_nearest_vehicle(origin: Location, vehicles: list, max_distance_miles: float = 10.0) -> tuple:
    """Find the nearest available vehicle within max_distance_miles."""
    min_distance = float('inf')
    nearest_idx = -1
    
    # Get all cells within rough distance of origin
    origin_cell = origin.h3_cell  # Keep as integer
    search_radius = min(3, int(max_distance_miles / 2))  # Convert miles to rough H3 resolution 7 hexes
    nearby_cells = {origin_cell}
    
    # Add rings of cells
    for k in range(1, search_radius + 1):
        nearby_cells.update(get_grid_ring(origin_cell, k))
    
    # First check vehicles in nearby cells
    for i, vehicle in enumerate(vehicles):
        if vehicle.state != "idle":
            continue
        
        if vehicle.current_location.h3_cell in nearby_cells:
            distance_km = haversine_distance(origin, vehicle.current_location)
            distance_miles = distance_km / 1.60934
            
            if distance_miles <= max_distance_miles and distance_miles < min_distance:
                min_distance = distance_miles
                nearest_idx = i
    
    return nearest_idx, min_distance 