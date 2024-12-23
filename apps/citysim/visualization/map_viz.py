"""
Visualization module for CitySim.
Handles map-based visualizations using kepler.gl and other tools.
"""

from typing import Dict, List, Optional, Union
import pandas as pd
import geopandas as gpd
from keplergl import KeplerGl
import folium

class MapVisualizer:
    """Handles map-based visualizations for CitySim."""
    
    def __init__(self, city_name: str):
        """
        Initialize the visualizer.
        
        Args:
            city_name: Name of the city being visualized
        """
        self.city_name = city_name
        self.map_config = {
            "version": "v1",
            "config": {
                "visState": {
                    "filters": [],
                    "layers": []
                }
            }
        }
    
    def create_kepler_map(
        self,
        vehicles_df: Optional[pd.DataFrame] = None,
        stations_df: Optional[pd.DataFrame] = None,
        demand_df: Optional[pd.DataFrame] = None,
        height: int = 600
    ) -> KeplerGl:
        """
        Create an interactive Kepler.gl map visualization.
        
        Args:
            vehicles_df: DataFrame containing vehicle positions and states
            stations_df: DataFrame containing charging station locations
            demand_df: DataFrame containing demand points
            height: Height of the map in pixels
        
        Returns:
            KeplerGl map object
        """
        map_instance = KeplerGl(height=height)
        
        if vehicles_df is not None:
            map_instance.add_data(data=vehicles_df, name="vehicles")
        
        if stations_df is not None:
            map_instance.add_data(data=stations_df, name="stations")
        
        if demand_df is not None:
            map_instance.add_data(data=demand_df, name="demand")
        
        return map_instance
    
    def create_folium_map(
        self,
        center: List[float],
        zoom_start: int = 12
    ) -> folium.Map:
        """
        Create a Folium map for static visualization.
        
        Args:
            center: [latitude, longitude] of map center
            zoom_start: Initial zoom level
        
        Returns:
            folium.Map object
        """
        return folium.Map(
            location=center,
            zoom_start=zoom_start,
            tiles="cartodbpositron"
        ) 