import rustworkx as rx
import osmnx as ox
from utils.geo import Location, haversine_distance
from utils.optimized import interpolate_path_numba
from typing import List, Tuple, Dict, Set
import numpy as np
import os
import hashlib
import json
import h3
from functools import lru_cache
import scipy.sparse as sp

class RoadNetwork:
    def __init__(self, center: Location, radius_miles: float):
        self.center = center
        self.radius_miles = radius_miles
        
        # Convert radius to meters for OSM
        radius_meters = radius_miles * 1609.34
        
        # Download the road network using OSMnx
        nx_graph = ox.graph_from_point((center.lat, center.lon), dist=radius_meters, network_type='drive')
        
        # Convert NetworkX graph to rustworkx graph
        self.G = rx.PyDiGraph()
        
        # Add nodes with their attributes
        node_mapping = {}  # Map old node IDs to new indices
        nodes = list(nx_graph.nodes(data=True))
        for node_id, data in nodes:
            idx = self.G.add_node((data['y'], data['x']))  # Store coordinates as node data
            node_mapping[node_id] = idx
        
        # Add edges with their attributes
        for u, v, data in nx_graph.edges(data=True):
            self.G.add_edge(node_mapping[u], node_mapping[v], data['length'])
        
        # Cache for paths between H3 cells
        self.path_cache: Dict[Tuple[str, str], Tuple[List, float]] = {}
        
        # Cache for interpolated paths
        self.interpolation_cache: Dict[str, List[Location]] = {}
        
        # Create H3 cell to node mapping
        self.cell_nodes: Dict[str, Set[int]] = {}
        
        # Store node coordinates as numpy arrays for efficient operations
        self.node_ids = np.array(list(range(self.G.num_nodes())))
        self.node_coords = np.array([self.G.get_node_data(i) for i in range(self.G.num_nodes())])
        
        # Create a coordinate lookup array for quick access
        self.node_index_to_coords = self.node_coords.copy()
        
        # Create H3 cell mapping
        for i in range(self.G.num_nodes()):
            coords = self.node_coords[i]
            cell = h3.latlng_to_cell(coords[0], coords[1], 7)
            if str(cell) not in self.cell_nodes:
                self.cell_nodes[str(cell)] = set()
            self.cell_nodes[str(cell)].add(i)
        
        # Store nodelist as an instance variable
        self.nodelist = list(range(self.G.num_nodes()))
    
    @lru_cache(maxsize=1024)
    def _get_nearest_node(self, lat: float, lon: float, cell: str, exclude_node: int = None) -> int:
        """Get nearest node to a location, using H3 cell for initial filtering, with an option to exclude a node."""
        if cell in self.cell_nodes:
            # First check nodes in the same cell using vectorized operations
            cell_nodes = np.array(list(self.cell_nodes[cell]))
            if exclude_node is not None:
                cell_nodes = cell_nodes[cell_nodes != exclude_node]
            
            if len(cell_nodes) > 0:
                # Get coordinates for cell nodes
                cell_coords = np.array([self.G.get_node_data(node) for node in cell_nodes])
                
                # Vectorized distance calculation
                dists = np.sum((cell_coords - np.array([lat, lon])) ** 2, axis=1)
                nearest_idx = np.argmin(dists)
                return cell_nodes[nearest_idx]
        
        # Fallback to checking all nodes
        all_coords = np.array([self.G.get_node_data(i) for i in range(self.G.num_nodes())])
        if exclude_node is not None:
            mask = np.ones(len(all_coords), dtype=bool)
            mask[exclude_node] = False
            all_coords = all_coords[mask]
        
        dists = np.sum((all_coords - np.array([lat, lon])) ** 2, axis=1)
        nearest_idx = np.argmin(dists)
        return nearest_idx if exclude_node is None else nearest_idx + (nearest_idx >= exclude_node)
    
    def snap_to_node(self, location: Location) -> Location:
        """Snap a location to the nearest node in the road network."""
        node = self._get_nearest_node(location.lat, location.lon, str(location.h3_cell))
        coords = self.G.get_node_data(node)
        return Location(coords[0], coords[1])
    
    def get_random_node_location(self) -> Location:
        """Get a random node location from the road network within service area."""
        idx = np.random.randint(self.G.num_nodes())
        coords = self.G.get_node_data(idx)
        return Location(coords[0], coords[1])
    
    def get_path_coordinates(self, path: List) -> List[Location]:
        """Convert path nodes to list of locations using vectorized operations."""
        if not path:
            return []
        
        # Get coordinates directly from node data
        path_coords = np.array([self.G.get_node_data(node) for node in path])
        
        # Convert to list of Locations
        return [Location(lat, lon) for lat, lon in path_coords]
    
    def get_path(self, start_cell: str, end_cell: str) -> Tuple[List, float]:
        """Retrieve or calculate the path between two H3 cells."""
        if (start_cell, end_cell) in self.path_cache:
            return self.path_cache[(start_cell, end_cell)]
        
        # Get a random node from each cell as representative points
        start_nodes = list(self.cell_nodes.get(start_cell, set()))
        end_nodes = list(self.cell_nodes.get(end_cell, set()))
        
        if not start_nodes or not end_nodes:
            return None, 0
        
        # Use the first node in each cell (they're close enough for our purposes)
        start_node = start_nodes[0]
        end_node = end_nodes[0]
        
        # Use rustworkx's Dijkstra algorithm
        path = rx.dijkstra_path(self.G, start_node, end_node, weight_fn=lambda x: float(x))
        
        # Calculate total distance in miles
        distance = sum(self.G.get_edge_data(path[i], path[i+1]) for i in range(len(path)-1)) / 1609.34
        
        # Cache the result
        self.path_cache[(start_cell, end_cell)] = (path, distance)
        return path, distance
    
    def interpolate_path(self, path: List) -> List[Location]:
        """Interpolate points along a path using Numba-optimized function."""
        if not path or len(path) < 2:
            return []
        
        # Check cache first
        path_key = '-'.join(map(str, path))
        if path_key in self.interpolation_cache:
            return self.interpolation_cache[path_key]
        
        # Get coordinates for all nodes in path
        coords = np.array([self.G.get_node_data(i) for i in path])
        
        # Calculate total distance with safe edge weight access
        total_distance = sum(self._get_edge_weight(path[i], path[i+1]) for i in range(len(path)-1))
        num_points = min(50, max(10, int(total_distance / 200)))
        
        # Use Numba-optimized interpolation
        interpolated_coords = interpolate_path_numba(coords, num_points)
        
        points = [Location(lat, lon) for lat, lon in interpolated_coords]
        
        # Cache the result
        self.interpolation_cache[path_key] = points
        return points
    
    def _convert_graph_to_sparse_matrix(self):
        """Convert the rustworkx graph to a sparse matrix."""
        # Get the adjacency matrix in sparse format
        adjacency_matrix = rx.adjacency_matrix(self.G, weight_fn=lambda x: float(x))
        
        # Create a mapping from node IDs to indices (already 0-based in rustworkx)
        self.node_id_to_index = {i: i for i in range(self.G.num_nodes())}
        
        return adjacency_matrix

    def get_shortest_path(self, start: Location, end: Location) -> Tuple[List, float]:
        """Get shortest path between two locations using rustworkx's Dijkstra algorithm."""
        # Get nearest nodes
        start_node = self._get_nearest_node(start.lat, start.lon, str(start.h3_cell))
        end_node = self._get_nearest_node(end.lat, end.lon, str(end.h3_cell), exclude_node=start_node)

        try:
            # Use rustworkx's built-in Dijkstra algorithm with safe weight access
            paths = rx.dijkstra_shortest_paths(self.G, start_node, end_node, weight_fn=lambda x: float(x) if x is not None else float('inf'))
            
            if end_node not in paths:
                return None, 0
            
            # Convert NodeIndices to a regular Python list
            path = list(paths[end_node])
            
            # Calculate total distance in miles using safe edge weight access
            distance = sum(self._get_edge_weight(path[i], path[i+1]) for i in range(len(path)-1)) / 1609.34
            
            return path, distance
        except Exception as e:
            print(f"Error finding path: {e}")
            return None, 0
    
    def _get_path_key(self, path: List[int]) -> str:
        """Generate a unique key for a path for caching."""
        return '-'.join(map(str, path)) 

    def get_network_polygon(self) -> dict:
        """Generate a GeoJSON representation of the network graph as LineString features."""
        features = []
        
        # Get all edges as (source, target, weight) tuples
        for start_node, end_node in self.G.edge_list():
            start_coords = self.G.get_node_data(start_node)
            end_coords = self.G.get_node_data(end_node)
            
            # Create a LineString feature for each edge
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[start_coords[1], start_coords[0]], [end_coords[1], end_coords[0]]]  # [lon, lat] format for GeoJSON
                }
            }
            features.append(feature)
        
        # Create GeoJSON FeatureCollection
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return geojson

    def save_network_polygon(self, output_dir: str):
        """Save the GeoJSON representation of the network to a file in the kepler subfolder."""
        # Generate the GeoJSON network
        geojson_network = self.get_network_polygon()
        
        # Define the output file path in the kepler subfolder
        kepler_dir = os.path.join(output_dir, 'kepler')
        output_file = os.path.join(kepler_dir, 'network.geojson')
        
        # Ensure the kepler directory exists
        os.makedirs(kepler_dir, exist_ok=True)
        
        # Write the GeoJSON to a file
        with open(output_file, 'w') as f:
            json.dump(geojson_network, f, indent=2)
        
        print(f"Network saved to {output_file}")

    def _get_edge_weight(self, u: int, v: int) -> float:
        """Safely get edge weight between two nodes."""
        try:
            weight = self.G.get_edge_data(u, v)
            return float(weight) if weight is not None else float('inf')
        except (KeyError, TypeError):
            return float('inf') 