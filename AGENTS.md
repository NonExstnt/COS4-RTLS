# RTLS Analysis Project - Agent Guidelines

## Build/Run Commands
- **Run all analyses**: `cd projects && uv run run_all.py`
- **Run single script**: `cd projects && uv run <script_name>.py` (e.g., `uv run 1_spaghetti_chart.py`)
- **Dependencies**: pandas, numpy, matplotlib, scikit-learn (managed by `uv`)
- **Python version**: 3.11.x

## Code Style

### Structure
- All analysis scripts in `projects/`, data scripts in `src/`
- Configuration constants at top (ALL_CAPS): `DATA_FOLDER`, `OUTPUT_FOLDER`, `WORKSHOP_FILES`
- Create output directories with `os.makedirs(folder, exist_ok=True)`

### Imports
Order: standard library → third-party → local. Example:
```python
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
```

### Functions & Documentation
- Use docstrings with triple quotes for all functions
- Keep functions focused and single-purpose
- Use descriptive names: `load_workshop_data()`, `create_spaghetti_chart()`

### Output & Logging
- Print progress messages with clear section headers using `=` separators
- Use checkmarks (✓) for completed tasks
- Save outputs: `projects/` scripts use `../output/<category>/`, `project-individual/` scripts use `./output/<category>/`
- Save plots as PNG at 150 DPI: `fig.savefig(path, dpi=150, bbox_inches='tight')`

### Data Handling
- Use pandas for CSV I/O: `pd.read_csv()`, `df.to_csv()`
- Convert time columns immediately: `df['time'] = pd.to_datetime(df['time'])`
- Sort by time when processing sequential data: `df.sort_values('time')`

### Error Handling
- Check file existence before processing
- Validate expected columns in dataframes
- Print clear error messages with context

# Tasks, Context, and expected Output of the project
1. Create a spaghetti chart 4.0
2. Define boundaries of the stations: k-means clustering
3. Cell Dwell Time - Time within a boundary (The data is somewhat inconsistent, but assume a worker won't back track, so if it seems like they've left a station and then returned, they didn't leave the station it was just sensor drift)

These two are grouped:
4. Cell Transition Time - How long did it take to move from one station to the next
5. Total Production Time - How long did it take to go from the start of the "Production" to the end

Problem Context:
-
- I have 3 workshop files with data "Workshop1.csv", "Workshop2.csv", "Workshop3.csv"
- These workshop files have Columns in this order: "name", "x", "y", "z", "time"
- Ignore the z axis in the data
- Each Workshop file is different Demonstrations on different days so ensure to use the same x and y sizes for the visuals but don't combine the data
- Under the "name" category is groups such as "Group 1" or "group 4" etc.. these groups go to all the same stations, but starting at different locations
- The tags should have reported data every second


The Output I want:
-
- Self-Explaining SIMPLE Python files using Python 3.11.x
- I want the code to be as simple as possible
- I want simple visuals to show progress
- For the comparison between groups of the same workshop, create stacked bar charts for comparison of dwell-time and transition-time
