"""
Configuration loader for CitySim.
Handles loading and validating YAML configuration files.
"""

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field, validator


class BatteryConfig(BaseModel):
    capacity_kwh: float
    range_km: float
    charging_rate_kw: float
    fast_charging_compatible: bool


class SpeedConfig(BaseModel):
    max_kph: float
    urban_average_kph: float


class VehicleType(BaseModel):
    type: str
    capacity: Optional[int] = None
    cargo_capacity_kg: Optional[float] = None
    battery: BatteryConfig
    speed: SpeedConfig
    cost_per_km: float


class ChargingStationType(BaseModel):
    power_output_kw: float
    connector_types: List[str]
    cost_per_kwh: float
    setup_time_minutes: float
    compatible_vehicle_types: List[str]


class Location(BaseModel):
    lat: float
    lon: float

    @validator('lat')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @validator('lon')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v


class OperatingHours(BaseModel):
    start: str
    end: str

    @validator('start', 'end')
    def validate_time_format(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('Time must be in HH:MM format')
        return v


class ChargingStation(BaseModel):
    type: Union[str, List[str]]
    location: Location
    num_ports: Union[int, Dict[str, int]]
    operating_hours: OperatingHours


class DemandPattern(BaseModel):
    start: str
    end: str
    multiplier: float


class TripDistance(BaseModel):
    min: float
    max: float
    mean: float
    std_dev: float


class ServiceType(BaseModel):
    vehicle_type: str
    percentage: float


class DemandType(BaseModel):
    base_rate_per_hour: float
    service_types: List[ServiceType]
    typical_trip_distance_km: TripDistance


class DemandHotspot(BaseModel):
    center: Location
    radius_km: float
    demand_multiplier: float
    active_types: List[str]


class ConfigLoader:
    """Handles loading and validating configuration files for CitySim."""

    def __init__(self, config_dir: Union[str, Path]):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir: Path to the configuration directory
        """
        self.config_dir = Path(config_dir)
        self.vehicle_types: Dict[str, VehicleType] = {}
        self.charging_stations: Dict[str, ChargingStation] = {}
        self.demand_patterns: Dict[str, DemandPattern] = {}
        self.demand_types: Dict[str, DemandType] = {}
        self.demand_hotspots: Dict[str, DemandHotspot] = {}

    def load_all(self, simulation_config_path: Union[str, Path]) -> dict:
        """
        Load and validate all configuration files specified in the simulation config.
        
        Args:
            simulation_config_path: Path to the main simulation configuration file
        
        Returns:
            dict: Complete validated configuration
        """
        with open(simulation_config_path) as f:
            sim_config = yaml.safe_load(f)

        config_files = sim_config['simulation']['config_files']
        
        # Load vehicle types
        with open(self.config_dir / config_files['vehicle_types']) as f:
            vehicle_data = yaml.safe_load(f)
            for name, config in vehicle_data['vehicle_types'].items():
                self.vehicle_types[name] = VehicleType(**config)

        # Load charging infrastructure
        with open(self.config_dir / config_files['charging_infrastructure']) as f:
            charging_data = yaml.safe_load(f)
            for name, config in charging_data['charging_stations'].items():
                self.charging_stations[name] = ChargingStation(**config)

        # Load demand patterns
        with open(self.config_dir / config_files['demand_patterns']) as f:
            demand_data = yaml.safe_load(f)
            self.demand_patterns = demand_data['time_periods']
            self.demand_types = demand_data['demand_types']
            self.demand_hotspots = demand_data['demand_hotspots']

        return {
            'simulation': sim_config['simulation'],
            'vehicle_types': self.vehicle_types,
            'charging_stations': self.charging_stations,
            'demand_patterns': self.demand_patterns,
            'demand_types': self.demand_types,
            'demand_hotspots': self.demand_hotspots
        }

    def validate_config_compatibility(self) -> List[str]:
        """
        Validate compatibility between different configuration components.
        
        Returns:
            List[str]: List of validation warnings/errors
        """
        warnings = []
        
        # Check if vehicle types referenced in charging stations exist
        for station_name, station in self.charging_stations.items():
            station_types = [station.type] if isinstance(station.type, str) else station.type
            for station_type in station_types:
                for vehicle_type in self.vehicle_types:
                    if vehicle_type not in self.vehicle_types:
                        warnings.append(f"Unknown vehicle type {vehicle_type} in charging station {station_name}")

        # Check if vehicle types referenced in demand types exist
        for demand_name, demand in self.demand_types.items():
            for service in demand.service_types:
                if service.vehicle_type not in self.vehicle_types:
                    warnings.append(f"Unknown vehicle type {service.vehicle_type} in demand type {demand_name}")

        return warnings 