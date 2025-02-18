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

# Performance Optimizations in RoadNetwork Simulation

## 🚀 Overview
This document summarizes key **parallelization improvements** in precomputing shortest paths and the **optimized approach** for reducing path lookup times.

## 🔥 Key Findings

### **1️⃣ Parallel Precomputation of Shortest Paths**
- **Objective:** Improve precompute time for large road networks by parallelizing shortest path calculations between unique hex anchor nodes.
- **Optimization:** Batched parallel Dijkstra executions using `joblib`, tuning batch size dynamically.
- **Results:**
  - **7-mile radius (~930,260 node pairs)**:
    - **Single-threaded:** **91.28s**
    - **Parallel (8 cores, batch size 19,000):** **30.67s** (~**3× speedup**)
  - **Smaller networks (≤3 miles)** perform **better in single-threaded mode** due to process-spawning overhead.
  - **Parallelization benefits networks with ≥100,000 node pairs** and continues scaling for larger graphs.

### **2️⃣ Optimized Path Lookup Time (Hex-Based Caching)**
- **Objective:** Reduce per-query shortest path lookup time by leveraging precomputed paths at the **H3 hex level**.
- **Optimizations:**
  1. **Hex-to-hex path caching** (precompute anchor node paths).
  2. **Fast retrieval of precomputed paths** (O(1) dictionary lookup).
  3. **Lazy Dijkstra fallback** for missing paths.
- **Results:**
  - **Path lookup time reduced by an order of magnitude**.
  - **Caching hits increase over multiple lookups**, reducing the need for recomputation.

## 📈 Summary of Improvements

| Optimization                          | Before                      | After                   | Improvement |
|---------------------------------------|-----------------------------|-------------------------|-------------|
| **Parallel Precompute (7-mile area)** | **91.28s (single-threaded)** | **30.67s (parallel)**   | **~3× faster** |
| **Path Lookup Time**                  | **Runs Dijkstra every time** | **Uses cached paths**   | **10× faster** |

## 🚀 Next Steps
- **Auto-detect when to use parallelization** (e.g., only for networks **≥6 miles**).
- **Benchmark even larger graphs (10-15 miles) to test further scaling**.
- **Optimize memory usage for large batch sizes**.