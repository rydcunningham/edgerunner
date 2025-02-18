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
from scipy.spatial.distance import cdist
from shapely.geometry import LineString

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

        # Parallel precompute decision tree
        self.tuning_factor = tuning_factor # for parallel precompute
        ## Initial testing indicates parallel precompute is only beneficial for radius >= 6 (100,000+ pairs)
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

            # Preserve road geometry if available
            road_geometry = data.get('geometry', None)
            if road_geometry is None:
                # If no geometry, create a straight-line path
                u_coords = np.array((self.G_nx.nodes[u]['y'], self.G_nx.nodes[u]['x']))
                v_coords = np.array((self.G_nx.nodes[v]['y'], self.G_nx.nodes[v]['x']))
                road_geometry = LineString([u_coords, v_coords])  # Create simple line

            # Add edge with geometry stored
            self.G_rx.add_edge(u_idx, v_idx, (weight, road_geometry))
        print(f"Population of G_rx with {len(self.G_rx.nodes())} nodes and {len(self.G_rx.edges())} edges completed in {time.time() - start} seconds.")

    def compute_shortest_path(self, origin_rx_idx, dest_rx_idx):
        """Compute shortest path between origin and destination nodes and return path, distance, and geometry."""
        
        path_dict = dict(rx.dijkstra_shortest_paths(
            self.G_rx,
            source=origin_rx_idx,
            target=dest_rx_idx,
            weight_fn=lambda x: float(x[0])  # ✅ Extract weight only
        ))

        if dest_rx_idx in path_dict:
            path_to_dest = np.array(path_dict[dest_rx_idx])  # ✅ Extract path sequence
            distance = 0
            geometries = []

            # Iterate through path edges to sum distances and collect geometries
            for i in range(len(path_to_dest) - 1):
                edge_data = self.G_rx.get_edge_data(path_to_dest[i], path_to_dest[i + 1])
                edge_weight, edge_geometry = edge_data  # ✅ Extract weight & geometry
                
                distance += edge_weight  # ✅ Sum total path distance
                if isinstance(edge_geometry, LineString):
                    geometries.append(edge_geometry)  # ✅ Store road segment geometry

            # ✅ Combine individual segments into a single LineString
            full_geometry = LineString([coord for geom in geometries for coord in geom.coords])

            return (origin_rx_idx, dest_rx_idx), {'path': path_to_dest, 'distance': distance, 'geometry': full_geometry}

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
                    processed_pairs.add((origin, dest))

        print(f"Single-threaded precomputation of {len(self.cell_pair_indices)} cell pairs completed in {time.time() - start} seconds.")
        return path_cache
    
    def compute_batch_shortest_paths(self, batch):
        """Compute multiple shortest paths in a batch, including full geometries."""
        
        batch_results = {}

        for origin, dest in batch:
            path_dict = dict(rx.dijkstra_shortest_paths(
                self.G_rx,
                source=origin,
                target=dest,
                weight_fn=lambda x: float(x[0])  # ✅ Extract weight only
            ))

            if dest in path_dict:
                path_to_dest = np.array(path_dict[dest])  # ✅ Extract path sequence
                distance = 0
                geometries = []

                # ✅ Collect path segment distances and geometries
                for i in range(len(path_to_dest) - 1):
                    edge_data = self.G_rx.get_edge_data(path_to_dest[i], path_to_dest[i + 1])
                    edge_weight, edge_geometry = edge_data  # ✅ Extract weight & geometry
                    
                    distance += edge_weight  # ✅ Sum total path distance
                    if isinstance(edge_geometry, LineString):
                        geometries.append(edge_geometry)  # ✅ Store road segment geometry

                # ✅ Merge all geometries into one LineString
                full_geometry = LineString([coord for geom in geometries for coord in geom.coords])

                # ✅ Store path results in batch
                batch_results[(origin, dest)] = {'path': path_to_dest, 'distance': distance, 'geometry': full_geometry}

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
    
    def get_node_attributes(self, selector: str, lookup_value: object, attribute: str):
        return self.node_mapping[self.node_mapping[selector] == lookup_value][attribute][0]

    @lru_cache(maxsize=1024)
    def _get_nearest_node(self, lat: float, lon: float, exclude_node: int = None) -> int:
        """
        Get the nearest node to a location, using H3 cell for initial filtering if possible.
        Falls back to checking all nodes with vectorized haversine distance calculation.
        """
        cell = h3.latlng_to_cell(lat, lon, 9)

        # Convert input lat/lon into a NumPy array for vectorized operations
        input_coords = np.array([[lat, lon]])

        if cell in self.cell_nodes:
            # Get nodes in the same hex cell
            nodes_in_cell = np.array(list(self.cell_nodes[cell]))

            if exclude_node is not None:
                nodes_in_cell = nodes_in_cell[nodes_in_cell != exclude_node]

            if len(nodes_in_cell) > 0:
                # Retrieve corresponding lat/lon values from node_mapping
                cell_coords = np.column_stack((
                    self.node_mapping['lat'][nodes_in_cell],
                    self.node_mapping['lon'][nodes_in_cell]
                ))

                # Compute haversine distances in a vectorized manner
                dists = cdist(input_coords, cell_coords, metric='euclidean')[0]
                nearest_idx = np.argmin(dists)
                return nodes_in_cell[nearest_idx]

        # Fallback: Compute distance across all nodes
        all_nodes = self.node_mapping['rx_idx']

        if exclude_node is not None:
            all_nodes = all_nodes[all_nodes != exclude_node]

        all_coords = np.column_stack((self.node_mapping['lat'][all_nodes], self.node_mapping['lon'][all_nodes]))
        
        # Compute haversine distances in a vectorized manner
        dists = cdist(input_coords, all_coords, metric='euclidean')[0]
        nearest_idx = np.argmin(dists)
        distance = dists[nearest_idx]

        return (all_nodes[nearest_idx], distance)
    
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

    def get_network_polygon(self) -> dict:
        """Generate a GeoJSON representation of the network graph using precomputed edge geometries."""
        features = []

        # Zip edge_list() with edges() to get (origin, dest, (weight, geometry))
        for (origin, dest), (edge_data) in zip(self.G_rx.edge_list(), self.G_rx.edges()):
            weight, geometry = edge_data  # ✅ Unpack weight & geometry

            if isinstance(geometry, LineString):  # ✅ Ensure valid geometry
                coordinates = list(geometry.coords)  # Extract full road shape
            else:
                # Fallback: reconstruct from node locations
                origin_lat = self.get_node_attributes(selector='rx_idx', lookup_value=origin, attribute='lat')
                origin_lon = self.get_node_attributes(selector='rx_idx', lookup_value=origin, attribute='lon')
                dest_lat = self.get_node_attributes(selector='rx_idx', lookup_value=dest, attribute='lat')
                dest_lon = self.get_node_attributes(selector='rx_idx', lookup_value=dest, attribute='lon')
                coordinates = [[origin_lon, origin_lat], [dest_lon, dest_lat]]

            # Create GeoJSON feature
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                },
                "properties": {
                    "length": weight  # ✅ Include road length
                }
            })

        # Construct final GeoJSON object
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