# COS4-RTLS: Real-Time Location System Analysis

Comprehensive analysis toolkit for RTLS (Real-Time Location System) workshop data using Python and K-means clustering.

## Project Overview

This project analyzes movement data from workshop demonstrations where different groups navigate through multiple work stations. The analysis provides insights into:
- Movement patterns (spaghetti charts)
- Station locations and boundaries (K-means clustering)
- Time spent at each station (dwell time)
- Transition times between stations
- Total production time

## Project Structure

```
COS4-RTLS/
├── data/                    # Data storage
│   ├── raw/                 # Original workshop CSV files
│   ├── processed/           # Cleaned data (z-axis removed)
│   ├── split/               # Individual group files (w{workshop}_g{group}.csv)
│   └── combined/            # All data combined
│
├── projects/                # Group comparison analysis
│   ├── 1_spaghetti_chart.py
│   ├── 2_station_boundaries.py (uses N_STATIONS=6)
│   ├── 3_dwell_time.py
│   ├── 4_5_transition_production_time.py
│   ├── run_all.py
│   └── README.md
│
├── project-individual/      # Individual group analysis
│   ├── 2_station_boundaries.py (auto-detects N_STATIONS)
│   ├── 3_dwell_time.py
│   ├── 4_5_transition_production_time.py
│   ├── run_all.py
│   ├── README.md
│   └── SUMMARY.md
│
├── src/                     # Data preprocessing utilities
│   ├── preprocess_data.py   # Remove z-axis, clean data
│   ├── split_data.py        # Split by groups
│   └── combine_data.py      # Combine all data
│
└── README.md                # This file
```

## Two Analysis Approaches

### 1. Projects Folder (Group Comparison)
**Purpose:** Compare groups within each workshop

**Features:**
- Uses **hardcoded N_STATIONS=6** for all workshops
- Shared station boundaries per workshop
- Creates stacked bar charts comparing groups
- Outputs to `../output/` folders

**Use when:** You want to compare how different groups performed in the same workshop

### 2. Project-Individual Folder (Individual Analysis)
**Purpose:** Deep dive into each group's specific patterns

**Features:**
- **Auto-detects optimal N_STATIONS** using silhouette analysis (k=3-9)
- Workshop-level optimal k determination, applied individually per group
- Individual station boundaries per group
- Focused charts per group (no comparisons)
- Self-contained `./output/` folder

**Use when:** You want to analyze individual group behavior or find optimal station configurations

## Quick Start

### Prerequisites
- Python 3.11.x
- `uv` package manager (recommended) or pip

### Installation
```bash
# Install dependencies manually if not using uv
pip install pandas numpy matplotlib scikit-learn
```

### Data Preparation (First Time Setup)
Before running any analysis, you need to split the raw workshop data by groups:

```bash
cd src
python split_data.py
```

This creates individual group files in `data/split/` (e.g., w1_g1.csv, w1_g2.csv, etc.)

### Running Analysis

#### Option 1: Group Comparison Analysis
```bash
cd projects
uv run run_all.py
```

#### Option 2: Individual Group Analysis
```bash
cd project-individual
uv run run_all.py
```

#### Option 3: Run specific scripts
```bash
cd projects  # or project-individual
uv run 2_station_boundaries.py
uv run 3_dwell_time.py
uv run 4_5_transition_production_time.py
```

## Data Format

Input CSV files (in `data/raw/` or `data/split/`):
```csv
name,x,y,z,time
Group 1,10.5,20.3,0.0,2024-01-01 10:00:00
Group 1,10.6,20.4,0.0,2024-01-01 10:00:01
...
```

**Note:** The `z` column is removed during preprocessing as only 2D analysis is performed.

## Key Analysis Components

### 1. Spaghetti Charts
Visualize movement paths for all groups in each workshop with consistent axis scaling.

### 2. Station Boundary Detection
**Projects:** Uses K-means with N_STATIONS=6 (hardcoded)
**Project-Individual:** Uses elbow method + silhouette analysis to auto-detect optimal k

### 3. Dwell Time Analysis
Calculates time spent at each station, handling sensor drift with a minimum 30-second threshold.

### 4. Transition Time Analysis
Measures time to move between stations with anti-backtracking logic.

### 5. Production Time Analysis
Total time from entering first station to exiting last station.

## Key Features

### Anti-Backtracking Logic
Assumes workers don't backtrack. Apparent returns to earlier stations are treated as sensor drift.

### Sensor Drift Handling
Minimum 30-second dwell time filters out brief sensor noise.

### Consistent Visualizations
All charts use the same axis limits across workshops for easy comparison.

### Silhouette Analysis (project-individual)
Automatically determines optimal number of stations:
- Tests k=3 to k=9 on combined workshop data
- Calculates inertia and silhouette score for each k
- Selects k with highest silhouette score
- Applies optimal k to each group individually with group-specific station centers
- Ensures data-driven station detection

## Outputs

### Projects Folder Outputs (in `output/` at root level)
```
output/
├── spaghetti/
│   ├── workshop1_spaghetti.png
│   ├── workshop2_spaghetti.png
│   └── workshop3_spaghetti.png
├── boundaries/
│   ├── workshop1_stations.png (combined workshop view)
│   ├── w1_g1_stations.png (individual group views)
│   ├── w1_g2_stations.png
│   ├── station_boundaries.json
│   └── ... (18 group visualizations total)
├── dwell_time/
│   ├── workshop1_dwell_comparison.png (stacked bar chart)
│   ├── workshop1_dwell_times.csv
│   ├── w1_g1_dwell_times.csv (individual group data)
│   ├── w1_g1_dwell_chart.png
│   └── ... (18 group charts + CSVs)
└── transition_production_time/
    ├── workshop1_transition_comparison.png (stacked bar chart)
    ├── workshop1_production_time.png
    ├── workshop1_transitions.csv
    └── workshop1_production.csv
```

### Project-Individual Outputs (in `project-individual/output/`)
```
project-individual/output/
├── boundaries/
│   ├── w1_g1_stations.png
│   ├── w1_g2_stations.png
│   ├── ... (all 18 groups)
│   └── station_boundaries_individual.json
├── dwell_time/
│   ├── w1_g1_dwell_times.csv
│   ├── w1_g1_dwell_chart.png
│   └── ... (all 18 groups)
└── transition_production_time/
    ├── w1_g1_transitions.csv
    ├── w1_g1_transition_chart.png
    ├── w1_g1_production.csv
    ├── w1_g1_production_summary.png
    └── ... (all 18 groups)
```

## Workshop Data

The project analyzes data from 3 workshops:
- **Workshop 1-3:** Each with 6 groups (18 groups total)
- **Groups:** Identified as w1_g1, w1_g2, ..., w3_g6
- **Stations:** Typically 6 stations per workshop (auto-detected in project-individual)

## Troubleshooting

### Missing dependencies
```bash
pip install pandas numpy matplotlib scikit-learn
```

### File not found errors
Ensure you're running scripts from the correct directory:
- `projects/` scripts: run from `projects/` folder
- `project-individual/` scripts: run from `project-individual/` folder

### No output generated
- Check that data files exist in `data/split/`
- Run data preparation: `cd src && python split_data.py`

### Different number of stations detected
This is expected! The silhouette analysis may find different optimal k values for different workshops based on actual movement patterns.

## Development Notes

- All scripts use absolute paths for data folders
- Output folders are created automatically
- Scripts print progress with clear section headers
- CSV files store all intermediate results
- PNG files saved at 150 DPI for quality

## Code Style

- Configuration constants at top (ALL_CAPS)
- Clear docstrings for all functions
- Progress messages with ✓ checkmarks
- Imports ordered: standard library → third-party → local
- Simple, self-explaining code with minimal complexity

## Requirements

- **Python:** 3.11.x
- **pandas:** Data manipulation
- **numpy:** Numerical operations
- **matplotlib:** Visualization
- **scikit-learn:** K-means clustering, silhouette analysis

## Acknowledgments

Developed for COS40004 course RTLS analysis project.
