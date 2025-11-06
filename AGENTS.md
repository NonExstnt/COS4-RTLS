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
- Save all outputs to `../output/<category>/` folders
- Save plots as PNG at 150 DPI: `fig.savefig(path, dpi=150, bbox_inches='tight')`

### Data Handling
- Use pandas for CSV I/O: `pd.read_csv()`, `df.to_csv()`
- Convert time columns immediately: `df['time'] = pd.to_datetime(df['time'])`
- Sort by time when processing sequential data: `df.sort_values('time')`

### Error Handling
- Check file existence before processing
- Validate expected columns in dataframes
- Print clear error messages with context
