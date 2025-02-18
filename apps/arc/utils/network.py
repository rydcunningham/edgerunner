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
import multiprocessing
from joblib import Parallel, delayed
import time

class RoadNetwork:
    def __init__(self, center: Location, radius_miles: float, parallel_precompute: bool = False, tuning_factor: float = 6.0):
        self.center = center
        self.radius_miles = radius_miles
        
        # Convert radius to meters for OSM
        radius_meters = radius_miles * 1609.34
        
        # Download the road network using OSMnx
        start = time.time()
        self.G_nx = ox.graph_from_point((center.lat, center.lon), dist=radius_meters, network_type='drive')
        print(f"Download of G_nx with {len(self.G_nx.nodes())} nodes and {len(self.G_nx.edges())} edges completed in {time.time() - start} seconds.")
        
        # Convert NetworkX graph to rustworkx graph
        self.G_rx = rx.PyDiGraph()
        # Add nodes with their attributes
        # Define the dtype for our structured array
        node_dtype = np.dtype([
            ('nx_id', object),    # NetworkX node ID
            ('lon', np.float64),    # longitude
            ('lat', np.float64),    # latitude
            ('hex_id', object),     # H3 hex ID at default resolution=9
            ('rx_idx', np.int64)    # Rustworkx index
        ])
        self.G_nx_nodes = list(self.G_nx.nodes(data=True))
        self.node_mapping = np.empty(len(self.G_nx_nodes), dtype=node_dtype)
        self.cell_nodes: Dict(str, Set[int]) = {}
        self._populate_G_rx()

        self.unique_cells = np.unique(self.node_mapping['hex_id'])
        for node in self.node_mapping:
            if node['hex_id'] not in self.cell_nodes:
                self.cell_nodes[node['hex_id']] = set()
            self.cell_nodes[node['hex_id']].add(node['rx_idx'])
        
        self.cell_anchor_nodes = {cell: next(iter(nodes)) for cell, nodes in self.cell_nodes.items()}
        self.cell_pairs = np.array([(x, y) for x in self.unique_cells for y in self.unique_cells if x != y])
        self.cell_pair_indices = np.array([(self.cell_anchor_nodes[x], self.cell_anchor_nodes[y]) for x, y in self.cell_pairs])

        self.tuning_factor = tuning_factor # for parallel precompute
        if self.radius_miles >= 6:
            if parallel_precompute is not False:
                # Parallel precompute
                self.path_cache = self._precompute_shortest_cell_paths_parallel()
            else:
                # Single-threaded precompute
                self.path_cache = self._precompute_shortest_cell_paths()
        else: self.path_cache = self._precompute_shortest_cell_paths()
        
        self.hex_path_cache = self._path_cache_rx_to_hex()
        
        # Cache for interpolated paths
        self.interpolation_cache: Dict[str, List[Location]] = {}
    
    def _populate_G_rx(self):
        start = time.time()
        # Fill node_mapping array with node information
        for i, (nx_id, data) in enumerate(self.G_nx_nodes):
            lat, lon = data['y'], data['x']
            hex_id = h3.latlng_to_cell(lat, lon, 9)
            rx_idx = self.G_rx.add_node(i) # store node data in G_rx
            
            self.node_mapping[i] = (nx_id, lon, lat, hex_id, rx_idx)
        
        # Add edges with their attributes
        for u, v, data in self.G_nx.edges(data=True):
            # Use searchsorted for efficient index lookup
            u_mask = self.node_mapping['nx_id'] == u
            v_mask = self.node_mapping['nx_id'] == v
            u_idx = self.node_mapping['rx_idx'][u_mask][0]
            v_idx = self.node_mapping['rx_idx'][v_mask][0]
            weight = data.get('length', 1.0)
            self.G_rx.add_edge(u_idx, v_idx, weight)
        print(f"Population of G_rx with {len(self.G_rx.nodes())} nodes and {len(self.G_rx.edges())} edges completed in {time.time() - start} seconds.")

    def compute_shortest_path(self, origin_rx_idx, dest_rx_idx):
        """Compute shortest path between origin and destination nodes."""
        path_dict = dict(rx.dijkstra_shortest_paths(self.G_rx, source=origin_rx_idx, target=dest_rx_idx, weight_fn=lambda x: float(x)))
        
        if dest_rx_idx in path_dict:
            path_to_dest = np.array(path_dict[dest_rx_idx])
            distance = sum(
                self.G_rx.get_edge_data(path_to_dest[i], path_to_dest[i + 1])
                for i in range(len(path_to_dest) - 1)
            )
            return (origin_rx_idx, dest_rx_idx), {'path': path_to_dest, 'distance': distance}
        
        return None  # No valid path
    def _precompute_shortest_cell_paths(self):
        start = time.time()
        path_cache = {}
        processed_pairs = set()

        for origin, dest in self.cell_pair_indices:
            if (origin, dest) not in processed_pairs:
                result = self.compute_shortest_path(origin, dest)
                if result is not None:
                    (origin, dest), path_data = result

                    # Store forward and reverse paths
                    path_cache[(origin, dest)] = path_data
                    path_cache[(dest, origin)] = {'path': path_data['path'][::-1], 'distance': path_data['distance']}

                    processed_pairs.add((origin, dest))
                    processed_pairs.add((dest, origin))

        print(f"Single-threaded precomputation of {len(self.cell_pair_indices)} cell pairs completed in {time.time() - start} seconds.")
        return path_cache
    
    def compute_batch_shortest_paths(self, batch):
        """Compute multiple shortest paths in a batch to reduce multiprocessing overhead."""
        batch_results = {}
        for origin, dest in batch:
            path_dict = dict(rx.dijkstra_shortest_paths(self.G_rx, source=origin, target=dest, weight_fn=lambda x: float(x)))
            if dest in path_dict:
                path_to_dest = np.array(path_dict[dest])
                distance = sum(
                    self.G_rx.get_edge_data(path_to_dest[i], path_to_dest[i + 1])
                    for i in range(len(path_to_dest) - 1)
                )
                batch_results[(origin, dest)] = {'path': path_to_dest, 'distance': distance}
                batch_results[(dest, origin)] = {'path': path_to_dest[::-1], 'distance': distance}
        return batch_results
    
    def _precompute_shortest_cell_paths_parallel(self):
        """
        Uses multiprocessing to precompute shortest paths between anchor nodes in batches.
        """
        start = time.time()
        path_cache = {}
        num_cores = min(8, multiprocessing.cpu_count())  # Limit CPU usage to avoid excessive overhead

        batch_size = int(round(len(self.cell_pair_indices) / (num_cores * self.tuning_factor), -3))
        print(f"Beginning parallel precomputation with batch size {batch_size} for {len(self.cell_pair_indices)} cell pairs...")
        # ✅ Directly use self.cell_pair_indices (already computed in __init__)
        anchor_pairs = self.cell_pair_indices

        # Break anchor pairs into batches
        batches = [anchor_pairs[i:i + batch_size] for i in range(0, len(anchor_pairs), batch_size)]

        # Run parallel execution across available CPU cores
        results = Parallel(n_jobs=num_cores)(
            delayed(self.compute_batch_shortest_paths)(batch) for batch in batches
        )

        # Merge results
        for batch_result in results:
            path_cache.update(batch_result)

        print(f"Parallel precomputation of {len(self.cell_pair_indices)} cell pairs completed using {num_cores} cores with batch size {batch_size} in {time.time() - start:.2f} seconds.")
        return path_cache

    def _path_cache_rx_to_hex(self):
        rx_to_hex = {node['rx_idx']: node['hex_id'] for node in self.node_mapping}
        hex_path_cache = {}

        for (origin_rx, dest_rx), entry in self.path_cache.items():
            origin_hex, dest_hex = rx_to_hex[origin_rx], rx_to_hex[dest_rx]
            hex_path_cache[(origin_hex, dest_hex)] = entry

        return hex_path_cache

    def rx_to_hex(self, rx_idx: int) -> str:
        return self.node_mapping[self.node_mapping['rx_idx'] == rx_idx]['hex_id'][0]
    
    def nx_to_hex(self, nx_id: int) -> str:
        return self.node_mapping[self.node_mapping['nx_id'] == nx_id]['hex_id'][0]
    
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
        idx = np.random.randint(self.G_rx.num_nodes())
        coords = self.G_rx.get_node_data(idx)
        return coords
    
    def get_path_coordinates(self, path: List) -> List[Location]:
        """Convert path nodes to list of locations using vectorized operations."""
        if not path:
            return []
        
        # Get coordinates directly from node data
        path_coords = np.array([self.G.get_node_data(node) for node in path])
        
        # Convert to list of Locations
        return [Location(lat, lon) for lat, lon in path_coords]
    
    def get_path(self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float) -> Tuple[np.ndarray, float]:
        """Retrieve the path and distance between two points, leveraging precomputed caches."""
        # Determine H3 cells and nearest nodes
        origin_cell = h3.latlng_to_cell(origin_lat, origin_lon, 9)
        dest_cell = h3.latlng_to_cell(dest_lat, dest_lon, 9)

        origin_node = self._get_nearest_node(origin_lat, origin_lon, origin_cell)
        dest_node = self._get_nearest_node(dest_lat, dest_lon, dest_cell)

        # 1. If origin and destination are the same node
        if origin_node == dest_node:
            return np.array([origin_node]), 0.0

        # 2. If origin and destination are in the same H3 cell, try a short path (<= 4 segments)
        if origin_cell == dest_cell:
            try:
                path_dict = rx.dijkstra_shortest_paths(
                    self.G_rx, source=origin_node, target=dest_node, weight_fn=lambda x: float(x)
                )
                path = np.array(path_dict[dest_node])
                if len(path) <= 5:  # 4 segments = 5 nodes
                    distance = sum(self.G_rx.get_edge_data(path[i], path[i + 1]) for i in range(len(path) - 1))
                    return path, distance
            except KeyError:
                pass  # No valid short path, fallback below

        # 3. Check precomputed hex_path_cache for cell-to-cell path
        cell_pair = (origin_cell, dest_cell)
        cache_match = self.hex_path_cache[self.hex_path_cache['pair'] == cell_pair]
        if cache_match.size > 0:
            precomputed_path = cache_match[0]['path']
            precomputed_distance = cache_match[0]['distance']

            # Optional: Stitch paths from precomputed anchor nodes to nearest nodes
            anchor_origin = self.cell_anchor_nodes[origin_cell]
            anchor_dest = self.cell_anchor_nodes[dest_cell]

            # Path from origin_node -> anchor_origin
            origin_to_anchor_path, origin_to_anchor_dist = self._dijkstra_path(origin_node, anchor_origin)

            # Path from anchor_dest -> dest_node
            anchor_to_dest_path, anchor_to_dest_dist = self._dijkstra_path(anchor_dest, dest_node)

            # Combine paths
            full_path = np.concatenate([origin_to_anchor_path[:-1], precomputed_path, anchor_to_dest_path[1:]])
            full_distance = origin_to_anchor_dist + precomputed_distance + anchor_to_dest_dist

            return full_path, full_distance

        # 4. Full Dijkstra path search as a fallback (origin_node -> dest_node)
        return self._dijkstra_path(origin_node, dest_node)
    
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