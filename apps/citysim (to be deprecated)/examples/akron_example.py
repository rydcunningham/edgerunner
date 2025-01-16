"""
Example script demonstrating CitySim with Akron, Ohio data.
Downloads OSM data and visualizes it using kepler.gl.
"""

import os
import pickle
from pathlib import Path
from datetime import datetime, timedelta

import osmnx as ox
import pandas as pd
import geopandas as gpd
from keplergl import KeplerGl
import networkx as nx
from shapely.geometry import Point, LineString, box, Polygon
import numpy as np

def get_cache_path(city_name: str, network_type: str) -> Path:
    """Get the path for cached network data."""
    # Create cache directory if it doesn't exist
    cache_dir = Path(__file__).parent.parent / "data" / "osm_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a filename from the city name and network type
    safe_name = city_name.lower().replace(", ", "_").replace(" ", "_")
    return cache_dir / f"{safe_name}_{network_type}.pkl"

def load_cached_network(cache_path: Path, max_age_days: int = 30) -> nx.MultiDiGraph:
    """Load network from cache if it exists and isn't too old."""
    if not cache_path.exists():
        return None
        
    # Check if cache is too old
    cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
    if datetime.now() - cache_time > timedelta(days=max_age_days):
        print(f"Cache is older than {max_age_days} days, will download fresh data...")
        return None
    
    print("Loading network from cache...")
    with open(cache_path, 'rb') as f:
        return pickle.load(f)

def save_network_cache(G: nx.MultiDiGraph, cache_path: Path) -> None:
    """Save network to cache."""
    print("Saving network to cache...")
    with open(cache_path, 'wb') as f:
        pickle.dump(G, f)

def download_city_network(city_name: str = "Akron, Ohio", network_type: str = "drive") -> nx.MultiDiGraph:
    """Download the city's road network from OpenStreetMap or load from cache."""
    # Try to load from cache first
    cache_path = get_cache_path(city_name, network_type)
    G = load_cached_network(cache_path)
    
    if G is None:
        print("Downloading network from OpenStreetMap...")
        # Configure OSMnx settings
        ox.settings.log_console = True
        ox.settings.use_cache = True
        
        # Download the network
        G = ox.graph_from_place(city_name, network_type=network_type)
        
        # Project the graph to UTM
        G = ox.project_graph(G)
        
        # Save to cache
        save_network_cache(G, cache_path)
    
    return G

def create_network_layers(G: nx.MultiDiGraph):
    """Convert network data to GeoDataFrames for visualization."""
    # Get nodes and edges as GeoDataFrames
    nodes, edges = ox.graph_to_gdfs(G)
    
    # Reset indices
    nodes = nodes.reset_index()
    edges = edges.reset_index()
    
    # Convert to lat/lon for kepler.gl
    nodes = nodes.to_crs("EPSG:4326")
    edges = edges.to_crs("EPSG:4326")
    
    # Create a simpler DataFrame for nodes
    nodes_df = pd.DataFrame({
        'node_id': nodes.index,
        'latitude': nodes.geometry.y,
        'longitude': nodes.geometry.x
    })
    
    # Create a simpler DataFrame for edges with coordinates
    edges_df = pd.DataFrame({
        'edge_id': edges.index,
        'highway': edges['highway'],
        'coordinates': edges.geometry.apply(lambda x: [[p[1], p[0]] for p in x.coords])
    })
    
    # Create bounding box
    bounds = nodes.total_bounds  # minx, miny, maxx, maxy
    bbox_coords = [
        [bounds[1], bounds[0]],  # SW
        [bounds[1], bounds[2]],  # SE
        [bounds[3], bounds[2]],  # NE
        [bounds[3], bounds[0]],  # NW
        [bounds[1], bounds[0]]   # SW again to close the polygon
    ]
    bbox_df = pd.DataFrame({
        'name': ['Akron Boundary'],
        'coordinates': [bbox_coords]
    })
    
    return nodes_df, edges_df, bbox_df

def create_kepler_map(nodes_df: pd.DataFrame, edges_df: pd.DataFrame, bbox_df: pd.DataFrame, height: int = 800):
    """Create an interactive Kepler.gl map."""
    # Initialize Kepler map
    map_1 = KeplerGl(height=height)
    
    # Configure the map style
    map_config = {
        "version": "v1",
        "config": {
            "visState": {
                "filters": [],
                "layers": [
                    # Bounding box layer
                    {
                        "id": "bbox",
                        "type": "polygon",
                        "config": {
                            "dataId": "bbox",
                            "label": "City Boundary",
                            "color": [255, 0, 0],
                            "columns": {
                                "polygon": "coordinates"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.1,
                                "strokeOpacity": 0.8,
                                "thickness": 1,
                                "strokeColor": [255, 0, 0],
                                "filled": True
                            }
                        }
                    },
                    # Node layer
                    {
                        "id": "nodes",
                        "type": "point",
                        "config": {
                            "dataId": "nodes",
                            "label": "Nodes",
                            "color": [255, 153, 31],
                            "columns": {
                                "lat": "latitude",
                                "lng": "longitude"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "radius": 3,
                                "fixedRadius": False,
                                "opacity": 0.8
                            }
                        }
                    },
                    # Edge layer
                    {
                        "id": "edges",
                        "type": "line",
                        "config": {
                            "dataId": "edges",
                            "label": "Road Network",
                            "color": [23, 184, 190],
                            "columns": {
                                "line": "coordinates"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.8,
                                "thickness": 1
                            }
                        }
                    }
                ]
            }
        }
    }
    
    # Add data to the map
    map_1.add_data(data=bbox_df, name="bbox")
    map_1.add_data(data=nodes_df, name="nodes")
    map_1.add_data(data=edges_df, name="edges")
    
    # Update the map configuration
    map_1.config = map_config
    
    return map_1

def calculate_network_area(G: nx.MultiDiGraph) -> float:
    """Calculate the area of the network in square meters."""
    # Get the nodes GeoDataFrame
    nodes = ox.graph_to_gdfs(G, edges=False)
    
    # Get the bounds
    bounds = nodes.total_bounds  # Returns (minx, miny, maxx, maxy)
    
    # Create a box from the bounds
    bbox = box(*bounds)
    
    # Calculate area in square meters (the graph is already projected to UTM)
    return bbox.area

def main():
    # Download Akron's road network
    print("Downloading Akron's road network...")
    G = download_city_network()
    
    # Convert network to DataFrames
    print("Processing network data...")
    nodes_df, edges_df, bbox_df = create_network_layers(G)
    
    # Create and save the visualization
    print("Creating visualization...")
    map_1 = create_kepler_map(nodes_df, edges_df, bbox_df)
    
    # Save the map to HTML
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    html_path = output_dir / "akron_network.html"
    map_1.save_to_html(file_name=str(html_path))
    print(f"Map saved to: {html_path}")
    
    # Print some network statistics
    print("\nNetwork Statistics:")
    print(f"Number of nodes: {len(nodes_df)}")
    print(f"Number of edges: {len(edges_df)}")
    stats = ox.basic_stats(G)
    print(f"Total road length: {stats['edge_length_total']/1000:.2f} km")
    
    # Calculate area and density
    area_m2 = calculate_network_area(G)
    area_km2 = area_m2 / 1_000_000  # Convert m² to km²
    density = (stats['edge_length_total'] / 1000) / area_km2  # km/km²
    print(f"Area: {area_km2:.2f} km²")
    print(f"Street density: {density:.2f} km/km²")
    
    # Print bounding box coordinates
    print("\nBounding Box Coordinates:")
    for i, coord in enumerate(bbox_df['coordinates'].iloc[0]):
        if i < 4:  # Skip the last point since it's the same as the first
            print(f"Corner {i+1}: ({coord[0]:.4f}°N, {coord[1]:.4f}°E)")

if __name__ == "__main__":
    main() 