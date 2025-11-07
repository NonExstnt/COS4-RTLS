# RTLS Analysis Projects

This folder contains self-contained Python scripts for analyzing Real-Time Location System (RTLS) data from workshop demonstrations.

## Overview

The analysis is divided into 5 tasks, grouped into 4 Python files:

1. **Spaghetti Chart** - Visualize movement paths
2. **Station Boundaries** - K-means clustering to define work stations
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

### Step 0: Preprocess data (first time only)
```bash
cd ../src
uv run preprocess_data.py
```

This creates cleaned CSV files in `data/processed/` with the `z` column removed.

### Option 1: Run all analyses at once (recommended)
```bash
uv run run_all.py
```

### Option 2: Run scripts individually
Execute the scripts **in order** (each script builds on previous outputs):

```bash
# Step 1: Create spaghetti charts
uv run 1_spaghetti_chart.py

# Step 2: Detect station boundaries
uv run 2_station_boundaries.py

# Step 3: Calculate dwell times (requires Step 2)
uv run 3_dwell_time.py

# Step 4-5: Analyze transitions and production time (requires Step 2)
uv run 4_5_transition_production_time.py
```

## Output Structure

Results are saved to the `output/` folder:

```
output/
├── spaghetti_charts/           # Movement path visualizations
├── station_boundaries/         # K-means station definitions (JSON + plots)
├── dwell_time/                 # Time spent at each station (CSV + plots)
├── transition_production_time/ # Transition & total time (CSV + plots)
```

## Key Features

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

**Note**: Raw data files in `data/raw/` include a `z` column which is removed during preprocessing. All analysis scripts use the processed data from `data/processed/` or `data/split`.

## Workshop Files

The scripts process three workshop files:
- `Workshop1.csv`
- `Workshop2.csv`
- `Workshop3.csv`

Each workshop is analyzed independently (no data combination).

## Troubleshooting

- **Missing dependencies**: Run `pip install pandas numpy matplotlib scikit-learn`
- **File not found errors**: Ensure you run scripts from the `projects/` directory
- **No output**: Check that workshop CSV files exist in `../data/raw/`

## Notes

- Each script is self-contained with clear comments
- Progress messages are printed to console
- All intermediate results are saved to CSV files
- Visualizations are saved as PNG files at 150 DPI
