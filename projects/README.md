# RTLS Analysis Projects

This folder contains self-contained Python scripts for analyzing Real-Time Location System (RTLS) data from workshop demonstrations.

## Overview

The analysis is divided into 7 tasks, grouped into 5 Python files:

1. **Spaghetti Chart** - Visualize movement paths
2. **Station Boundaries** - K-means clustering to define work stations
3. **Dwell Time Analysis** - Time spent at each station (handles sensor drift)
4. **Transition & Production Time** - Movement time and total time analysis
5. **Prediction Models** - Random Forest models for time prediction

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
├── 6_7_prediction_models.py          # Tasks 6-7: Predictive models
└── README.md                         # This file
```

## How to Run

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

# Step 6-7: Train prediction models (requires Step 2)
uv run 6_7_prediction_models.py
```

## Output Structure

Results are saved to the `output/` folder:

```
output/
├── spaghetti_charts/           # Movement path visualizations
├── station_boundaries/         # K-means station definitions (JSON + plots)
├── dwell_time/                 # Time spent at each station (CSV + plots)
├── transition_production_time/ # Transition & total time (CSV + plots)
└── prediction_models/          # ML prediction results (plots)
```

## Key Features

### Anti-Backtracking Logic
The analysis assumes workers don't backtrack. If sensors show a return to an earlier station, it's treated as sensor drift and ignored.

### Consistent Visualizations
All spaghetti charts use the same X/Y axis limits for easy comparison across workshops.

### Stacked Bar Charts
Dwell time and transition time comparisons use stacked bar charts to show how different groups perform.

### Simple Random Forest Models
Prediction models use scikit-learn's RandomForestRegressor with basic parameters for interpretability.

## Data Format

Input CSV files should have columns in this order:
- `name`: Group identifier (e.g., "Group 1")
- `x`: X coordinate
- `y`: Y coordinate  
- `z`: Z coordinate (ignored)
- `time`: Timestamp

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
- **Prediction warnings**: Some workshops may not have enough data for reliable predictions

## Notes

- Each script is self-contained with clear comments
- Progress messages are printed to console
- All intermediate results are saved to CSV files
- Visualizations are saved as PNG files at 150 DPI
