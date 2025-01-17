import networkx as nx
import osmnx as ox
from utils.geo import Location, haversine_distance
from typing import List, Tuple, Dict, Set
import numpy as np
import os
import hashlib
import json
import h3
from functools import lru_cache

class RoadNetwork:
    def __init__(self, center: Location, radius_miles: float):
        self.center = center
        self.radius_miles = radius_miles
        
        # Convert radius to meters for OSM
        radius_meters = radius_miles * 1609.34
        
        # Download and create the road network
        self.G = ox.graph_from_point((center.lat, center.lon), dist=radius_meters, network_type='drive')
        
        # Cache for paths between H3 cells
        self.path_cache: Dict[Tuple[str, str], Tuple[List, float]] = {}
        
        # Create H3 cell to node mapping
        self.cell_nodes: Dict[str, Set[int]] = {}
        for node, data in self.G.nodes(data=True):
            cell = h3.latlng_to_cell(data['y'], data['x'], 7)
            if str(cell) not in self.cell_nodes:
                self.cell_nodes[str(cell)] = set()
            self.cell_nodes[str(cell)].add(node)
    
    def _get_nearest_node(self, location: Location) -> int:
        """Get nearest node to a location, using H3 cell for initial filtering."""
        cell = str(location.h3_cell)
        if cell in self.cell_nodes:
            # First check nodes in the same cell
            min_dist = float('inf')
            nearest_node = None
            for node in self.cell_nodes[cell]:
                node_y = self.G.nodes[node]['y']
                node_x = self.G.nodes[node]['x']
                dist = (location.lat - node_y)**2 + (location.lon - node_x)**2
                if dist < min_dist:
                    min_dist = dist
                    nearest_node = node
            if nearest_node is not None:
                return nearest_node
        
        # Fallback to checking neighboring cells or full graph
        return ox.nearest_nodes(self.G, location.lon, location.lat)
    
    @lru_cache(maxsize=1024)
    def _get_cached_path(self, start_cell: str, end_cell: str) -> Tuple[List, float]:
        """Get cached path between H3 cells, computing if not found."""
        cache_key = (start_cell, end_cell)
        if cache_key not in self.path_cache:
            # Get representative nodes for cells
            start_nodes = self.cell_nodes.get(start_cell, set())
            end_nodes = self.cell_nodes.get(end_cell, set())
            
            if not start_nodes or not end_nodes:
                return None, 0
            
            # Use center nodes of cells
            start_node = list(start_nodes)[0]
            end_node = list(end_nodes)[0]
            
            try:
                path = nx.shortest_path(self.G, start_node, end_node, weight='length')
                distance = sum(self.G[path[i]][path[i+1]][0]['length'] for i in range(len(path)-1))
                self.path_cache[cache_key] = (path, distance / 1609.34)  # Convert meters to miles
            except nx.NetworkXNoPath:
                self.path_cache[cache_key] = (None, 0)
        
        return self.path_cache[cache_key]
    
    def get_shortest_path(self, start: Location, end: Location) -> Tuple[List, float]:
        """Get shortest path between two locations using H3 cells for optimization."""
        # First check if we have a cached path between the H3 cells
        start_cell = str(start.h3_cell)
        end_cell = str(end.h3_cell)
        
        if start_cell == end_cell:
            # For same cell, compute direct path
            start_node = self._get_nearest_node(start)
            end_node = self._get_nearest_node(end)
            try:
                path = nx.shortest_path(self.G, start_node, end_node, weight='length')
                distance = sum(self.G[path[i]][path[i+1]][0]['length'] for i in range(len(path)-1))
                return path, distance / 1609.34  # Convert meters to miles
            except nx.NetworkXNoPath:
                return None, 0
        
        # Get cached path between cells
        cell_path, cell_distance = self._get_cached_path(start_cell, end_cell)
        if cell_path:
            # Extend path to exact start/end points
            start_node = self._get_nearest_node(start)
            end_node = self._get_nearest_node(end)
            
            try:
                prefix = nx.shortest_path(self.G, start_node, cell_path[0], weight='length')
                suffix = nx.shortest_path(self.G, cell_path[-1], end_node, weight='length')
                
                # Combine paths and calculate total distance
                full_path = prefix[:-1] + cell_path + suffix[1:]
                distance = sum(self.G[full_path[i]][full_path[i+1]][0]['length'] for i in range(len(full_path)-1))
                return full_path, distance / 1609.34
            except nx.NetworkXNoPath:
                pass
        
        # Fallback to direct path finding
        start_node = self._get_nearest_node(start)
        end_node = self._get_nearest_node(end)
        try:
            path = nx.shortest_path(self.G, start_node, end_node, weight='length')
            distance = sum(self.G[path[i]][path[i+1]][0]['length'] for i in range(len(path)-1))
            return path, distance / 1609.34
        except nx.NetworkXNoPath:
            return None, 0
    
    def get_path_coordinates(self, path: List) -> List[Location]:
        """Convert path nodes to list of locations."""
        if not path:
            return []
        return [Location(self.G.nodes[node]['y'], self.G.nodes[node]['x']) for node in path]
    
    def interpolate_path(self, path: List) -> List[Location]:
        """Interpolate points along a path using numpy for efficiency."""
        if not path or len(path) < 2:
            return []
        
        # Extract coordinates
        coords = np.array([(self.G.nodes[node]['y'], self.G.nodes[node]['x']) for node in path])
        
        # Calculate number of points based on path length
        total_distance = sum(self.G[path[i]][path[i+1]][0]['length'] for i in range(len(path)-1))
        num_points = max(10, int(total_distance / 100))  # One point every 100 meters
        
        # Create interpolated points
        alphas = np.linspace(0, 1, num_points)
        points = []
        
        for i in range(len(coords) - 1):
            segment_points = np.array([
                coords[i] + alpha * (coords[i+1] - coords[i])
                for alpha in alphas
            ])
            points.extend([Location(lat, lon) for lat, lon in segment_points[:-1]])
        
        # Add final point
        points.append(Location(coords[-1][0], coords[-1][1]))
        return points 