import numpy as np
from numba import jit, float64, int64
import math

@jit(float64(float64, float64, float64, float64), nopython=True)
def haversine_distance_numba(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Optimized haversine distance calculation using Numba."""
    R = 6371.0  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

@jit(nopython=True)
def interpolate_path_numba(coords: np.ndarray, num_points: int) -> np.ndarray:
    """Optimized path interpolation using Numba."""
    if len(coords) < 2:
        return coords
        
    result = np.empty((num_points, 2), dtype=np.float64)
    alphas = np.linspace(0, 1, num_points)
    
    segment_length = len(coords) - 1
    points_per_segment = num_points // segment_length
    remainder = num_points % segment_length
    
    current_idx = 0
    for i in range(segment_length):
        n_points = points_per_segment + (1 if i < remainder else 0)
        segment_alphas = np.linspace(0, 1, n_points)
        
        for j in range(n_points):
            alpha = segment_alphas[j]
            result[current_idx] = coords[i] + alpha * (coords[i+1] - coords[i])
            current_idx += 1
    
    return result

@jit(nopython=True)
def generate_timestamps_numba(start_time: int64, end_time: int64, num_points: int) -> np.ndarray:
    """Generate evenly spaced timestamps using Numba."""
    return np.linspace(start_time, end_time, num_points).astype(np.int64)

@jit(nopython=True)
def process_coordinates_batch_numba(coords: np.ndarray) -> np.ndarray:
    """Process a batch of coordinates using Numba."""
    num_points = len(coords)
    result = np.empty((num_points, 2), dtype=np.float64)
    
    for i in range(num_points):
        result[i, 0] = coords[i, 1]  # longitude
        result[i, 1] = coords[i, 0]  # latitude
        
    return result 