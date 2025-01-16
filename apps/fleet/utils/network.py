import networkx as nx
import osmnx as ox
from utils.geo import Location, haversine_distance
from typing import List, Tuple, Dict
import numpy as np
import os
import hashlib
import json

class RoadNetwork:
    def __init__(self, service_area_center: Location, service_area_radius: float):
        """Initialize road network for the service area.
        
        Args:
            service_area_center: Center point of service area
            service_area_radius: Radius in miles to define the service area
        """
        # Convert radius to meters for OSMnx
        radius_meters = service_area_radius * 1609.34
        
        # Create cache directory if it doesn't exist
        cache_dir = "cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            
        # Create cache key from parameters
        cache_params = {
            "lat": service_area_center.lat,
            "lon": service_area_center.lon,
            "radius_meters": radius_meters,
            "network_type": "drive"
        }
        cache_key = hashlib.sha1(json.dumps(cache_params, sort_keys=True).encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f"{cache_key}.graphml")
        
        if os.path.exists(cache_file):
            print("\nLoading road network from cache...")
            self.G = ox.load_graphml(cache_file)
            print(f"Loaded network with {len(self.G.nodes)} nodes and {len(self.G.edges)} edges")
        else:
            print("\nDownloading road network from OpenStreetMap...")
            print(f"Center: ({service_area_center.lat:.4f}, {service_area_center.lon:.4f})")
            print(f"Radius: {service_area_radius:.1f} miles ({radius_meters:.0f} meters)")
            
            # Download and create road network graph
            self.G = ox.graph_from_point(
                (service_area_center.lat, service_area_center.lon),
                dist=radius_meters,
                network_type='drive'
            )
            
            print(f"Downloaded network with {len(self.G.nodes)} nodes and {len(self.G.edges)} edges")
            print("Saving network to cache...")
            ox.save_graphml(self.G, cache_file)
        
        print("Projecting network to UTM coordinates...")
        # Project graph to UTM for accurate distance calculations
        self.G_proj = ox.project_graph(self.G)
        
        # Cache nearest nodes for frequently accessed locations
        self.node_cache: Dict[Tuple[float, float], int] = {}
        
    def get_nearest_node(self, location: Location) -> int:
        """Get the nearest node in the road network to a given location."""
        loc_key = (location.lat, location.lon)
        if loc_key not in self.node_cache:
            self.node_cache[loc_key] = ox.nearest_nodes(
                self.G, location.lon, location.lat
            )
        return self.node_cache[loc_key]
    
    def get_shortest_path(self, origin: Location, destination: Location) -> Tuple[List[int], float]:
        """Find the shortest path between two locations using the road network.
        
        Returns:
            Tuple containing:
            - List of node IDs representing the path
            - Total path distance in miles
        """
        # Get nearest nodes to origin and destination
        origin_node = self.get_nearest_node(origin)
        dest_node = self.get_nearest_node(destination)
        
        try:
            # Get shortest path using NetworkX
            path = nx.shortest_path(
                self.G_proj,
                origin_node,
                dest_node,
                weight='length'  # Use length attribute for shortest path
            )
            
            # Calculate total path length in meters, handling multigraph edges
            path_length = 0
            for i in range(len(path)-1):
                # Get the shortest edge between these nodes if there are multiple
                edge_data = min(
                    self.G_proj.get_edge_data(path[i], path[i+1]).values(),
                    key=lambda x: x['length']
                )
                path_length += edge_data['length']
            
            # Convert to miles
            path_length_miles = path_length / 1609.34
            
            return path, path_length_miles
            
        except nx.NetworkXNoPath:
            # If no path found, return None and use haversine as fallback
            print(f"Warning: No path found between nodes {origin_node} and {dest_node}. Using direct distance.")
            return None, haversine_distance(origin, destination)
    
    def get_path_coordinates(self, path: List[int]) -> List[Tuple[float, float]]:
        """Convert a path of node IDs to a list of (lat, lon) coordinates."""
        return [
            (self.G.nodes[node]['y'], self.G.nodes[node]['x'])
            for node in path
        ]
    
    def interpolate_path(self, path: List[int], num_points: int = 10) -> List[Location]:
        """Interpolate points along a path for visualization or tracking.
        
        Args:
            path: List of node IDs representing the path
            num_points: Number of points to interpolate
            
        Returns:
            List of Location objects representing interpolated points along the path
        """
        if not path:
            return []
            
        # Get coordinates for path
        coords = self.get_path_coordinates(path)
        
        # Calculate cumulative distances
        distances = [0]
        for i in range(1, len(coords)):
            prev = Location(lat=coords[i-1][0], lon=coords[i-1][1])
            curr = Location(lat=coords[i][0], lon=coords[i][1])
            distances.append(distances[-1] + haversine_distance(prev, curr))
        
        # Create evenly spaced points
        total_distance = distances[-1]
        if total_distance == 0:
            return [Location(lat=coords[0][0], lon=coords[0][1])] * num_points
            
        points = []
        for i in range(num_points):
            target_dist = (i / (num_points - 1)) * total_distance
            
            # Find segment containing target distance
            for j in range(len(distances) - 1):
                if distances[j] <= target_dist <= distances[j + 1]:
                    # Interpolate within segment
                    ratio = (target_dist - distances[j]) / (distances[j + 1] - distances[j])
                    lat = coords[j][0] + ratio * (coords[j + 1][0] - coords[j][0])
                    lon = coords[j][1] + ratio * (coords[j + 1][1] - coords[j][1])
                    points.append(Location(lat=lat, lon=lon))
                    break
                    
        return points 