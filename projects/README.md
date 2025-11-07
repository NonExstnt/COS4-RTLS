# RTLS Analysis Projects

This folder contains self-contained Python scripts for analyzing Real-Time Location System (RTLS) data from workshop demonstrations.

## Overview

The analysis is divided into 5 tasks, grouped into 4 Python files:

1. **Spaghetti Chart** - Visualize movement paths
2. **Station Boundaries** - K-means clustering with optimal k determination (k=3-9 using silhouette analysis)
3. **Dwell Time Analysis** - Time spent at each station (handles sensor drift)
4. **Transition & Production Time** - Movement time and total time analysis

## Requirements

Using `uv` (recommended):
```bash
# uv will automatically handle dependencies
uv run 1_spaghetti_chart.py
```

Or with pip:
```bash
pip install pandas numpy matplotlib scikit-learn
```

Python version: 3.11.x

## File Structure

```
projects/
├── 1_spaghetti_chart.py              # Task 1: Movement visualization
├── 2_station_boundaries.py           # Task 2: Station detection with K-means
├── 3_dwell_time.py                   # Task 3: Time at each station
├── 4_5_transition_production_time.py # Tasks 4-5: Transition & production time
└── README.md                         # This file
```

## How to Run

### Step 0: Prepare data (first time only)
```bash
cd ../src
python split_data.py
```

This creates individual group files in `data/split/` from the raw workshop CSV files.

### Option 1: Run all analyses at once (recommended)
```bash
uv run run_all.py
```

### Option 2: Run scripts individually
Execute the scripts as needed (station boundaries must be run before dwell time and transition analyses):

```bash
# Step 1: Create spaghetti charts (independent)
uv run 1_spaghetti_chart.py

# Step 2: Detect station boundaries (required for Steps 3-4)
uv run 2_station_boundaries.py

# Step 3: Calculate dwell times (requires Step 2)
uv run 3_dwell_time.py

# Step 4-5: Analyze transitions and production time (requires Step 2)
uv run 4_5_transition_production_time.py
```

## Output Structure

Results are saved to the `../output/` folder (at the project root level):

```
output/
├── spaghetti/                      # Movement path visualizations
│   ├── workshop1_spaghetti.png
│   ├── workshop2_spaghetti.png
│   └── workshop3_spaghetti.png
├── boundaries/                     # K-means station definitions
│   ├── workshop1_stations.png      # Combined workshop visualization
│   ├── w1_g1_stations.png          # Individual group visualizations
│   ├── w1_g2_stations.png          # (18 group charts total)
│   ├── ...
│   └── station_boundaries.json     # Station center coordinates & radii
├── dwell_time/                     # Time spent at each station
│   ├── workshop1_dwell_comparison.png  # Stacked bar chart comparing groups
│   ├── workshop1_dwell_times.csv       # Combined workshop data
│   ├── w1_g1_dwell_times.csv           # Individual group data (18 files)
│   ├── w1_g1_dwell_chart.png           # Individual group charts (18 files)
│   └── ...
└── transition_production_time/     # Transition & total time
    ├── workshop1_transition_comparison.png  # Stacked bar chart
    ├── workshop1_production_time.png
    ├── workshop1_transitions.csv
    ├── workshop1_production.csv
    └── ...
```

## Key Features

### Dynamic K-Means Clustering
The station boundary detection automatically determines the optimal number of stations (k) for each workshop using silhouette analysis (testing k=3-9). This ensures each workshop's unique layout is properly captured rather than forcing a fixed number of stations.

### Anti-Backtracking Logic
The analysis assumes workers don't backtrack. If sensors show a return to an earlier station, it's treated as sensor drift and ignored.

### Consistent Visualizations
All spaghetti charts use the same X/Y axis limits for easy comparison across workshops.

### Stacked Bar Charts
Dwell time and transition time comparisons use stacked bar charts to show how different groups perform.

## Data Format

Input CSV files should have columns:
- `name`: Group identifier (e.g., "Group 1")
- `x`: X coordinate
- `y`: Y coordinate  
- `time`: Timestamp

**Note**: The analysis uses split group files from `data/split/` (e.g., w1_g1.csv, w1_g2.csv). These files are created by running `python split_data.py` from the `src/` folder.

## Workshop Files

The scripts process three workshop files:
- `Workshop1.csv`
- `Workshop2.csv`
- `Workshop3.csv`

Each workshop is analyzed independently (no data combination).

## Troubleshooting

- **Missing dependencies**: Run `pip install pandas numpy matplotlib scikit-learn`
- **File not found errors**: Ensure you run scripts from the `projects/` directory
- **No output**: Check that split files exist in `../data/split/` - run `cd ../src && python split_data.py` if needed

## Notes

- Each script is self-contained with clear comments
- Progress messages are printed to console
- All intermediate results are saved to CSV files
- Visualizations are saved as PNG files at 150 DPI
