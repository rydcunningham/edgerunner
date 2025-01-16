# Autonomous Rideshare Fleet Simulation

This project simulates the operations of a fleet of autonomous electric rideshare vehicles using the SimPy library. The simulation models vehicle usage, battery management, and charging logistics to optimize fleet efficiency.

## Features
- Simulates a fleet of 50 electric vehicles.
- Configurable battery capacities, charging speeds, and trip characteristics.
- Models charging infrastructure with Level 3 fast chargers.
- Fully configurable via a YAML file for easy experimentation.

## Project Structure

- `inputs/config.yaml`: Configuration file for the simulation.
- `simulation/fleet.py`: Defines the vehicle class and its behavior.
- `simulation/chargers.py`: Defines the charging infrastructure.
- `simulation/simulation.py`: Main simulation logic.
- `main.py`: Entry point for running the simulation.
- `requirements.txt`: Lists dependencies.

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the simulation: `python main.py`
