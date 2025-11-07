# Project-Individual Summary

## What Was Created

A complete set of analysis scripts that process each workshop group **individually** rather than comparing groups within workshops.

## Folder Structure

```
project-individual/
├── 2_station_boundaries.py          # Detect stations per group
├── 3_dwell_time.py                  # Calculate dwell times per group
├── 4_5_transition_production_time.py # Analyze transitions & production per group
├── run_all.py                       # Run all scripts in sequence
├── README.md                        # Documentation
├── SUMMARY.md                       # This file
└── output/                          # Created when scripts run
    ├── w1_g1_stations.png
    ├── w1_g1_dwell_times.csv
    ├── w1_g1_dwell_chart.png
    ├── w1_g1_transitions.csv
    ├── w1_g1_transition_chart.png
    ├── w1_g1_production.csv
    ├── w1_g1_production_summary.png
    └── ... (repeated for all 18 groups: w1_g1-6, w2_g1-6, w3_g1-6)
```

## Key Features

### 1. Station Boundaries (2_station_boundaries.py)
- **Individual Detection**: Each group gets its own station boundaries using K-means
- **Output**: 
  - 18 PNG images (one per group) showing station boundaries
  - 1 JSON file with all station definitions

### 2. Dwell Time Analysis (3_dwell_time.py)
- **Individual Calculation**: Uses each group's specific station boundaries
- **Output**:
  - 18 CSV files with dwell time data
  - 18 PNG charts showing dwell times by station

### 3. Transition & Production Time (4_5_transition_production_time.py)
- **Individual Analysis**: Calculates transitions and total production time per group
- **Output**:
  - Up to 18 transition CSV files (if group moved between stations)
  - Up to 18 transition charts
  - 18 production CSV files
  - 18 production summary charts

## How to Run

```bash
cd project-individual
uv run run_all.py
```

This will:
1. Detect station boundaries for all 18 groups individually
2. Calculate dwell times for each group
3. Analyze transitions and production times for each group
4. Save all outputs to `project-individual/output/`

## Total Output Files

For 18 groups (3 workshops × 6 groups):
- **54+ PNG images** (stations + dwell + transitions/production)
- **54+ CSV files** (dwell + transitions + production)
- **1 JSON file** (all station boundaries)

## Differences from Main Project

| Aspect | Main Project | Project-Individual |
|--------|-------------|-------------------|
| Station Boundaries | Shared per workshop | Individual per group |
| Comparisons | Between groups | None (individual focus) |
| Output Location | `../output/*` folders | `./output/` (self-contained) |
| Charts | Stacked comparisons | Individual bar charts |
| Focus | Workshop-level | Group-level |

## Use Cases

- **Individual Performance**: See how each specific group performed
- **Pattern Analysis**: Identify unique movement patterns per group
- **Detailed Investigation**: Deep dive into a single group's behavior
- **Custom Boundaries**: Use group-specific station definitions
