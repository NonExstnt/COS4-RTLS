# RTLS Individual Group Analysis

This folder contains analysis scripts that process each group individually, rather than comparing groups within a workshop.

## Scripts

### 2_station_boundaries.py
Detects station boundaries for each individual group using K-means clustering. Each group gets its own station definitions based on its specific movement patterns.

**Output:**
- `{group_name}_stations.png` - Visualization of detected stations for each group
- `station_boundaries_individual.json` - Station definitions for all groups

### 3_dwell_time.py
Calculates the time each group spent at each station using the group's individual station boundaries.

**Output:**
- `{group_name}_dwell_times.csv` - Dwell time data for each group
- `{group_name}_dwell_chart.png` - Bar chart showing dwell times by station

### 4_5_transition_production_time.py
Analyzes transition times between stations and total production time for each group individually.

**Output:**
- `{group_name}_transitions.csv` - Transition time data
- `{group_name}_transition_chart.png` - Visualization of transitions
- `{group_name}_production.csv` - Production time data
- `{group_name}_production_summary.png` - Production time summary

## Running the Analysis

### Run all scripts in sequence:
```bash
cd project-individual
uv run run_all.py
```

### Run individual scripts:
```bash
cd project-individual
uv run 2_station_boundaries.py
uv run 3_dwell_time.py
uv run 4_5_transition_production_time.py
```

## Output Location

All outputs (images and CSV files) are saved to `project-individual/output/`

## Key Differences from Main Project

- **Individual Station Definitions**: Each group has its own station boundaries rather than using shared workshop boundaries
- **Focused Analysis**: Results are specific to each group's movement pattern
- **Self-contained Output**: All outputs are stored within the project-individual folder
- **No Group Comparisons**: Charts focus on individual group performance rather than comparing multiple groups

## Notes

- Station boundaries are detected independently for each group based on their specific data
- Minimum station dwell time is 30 seconds to filter out sensor drift
- All visualizations use consistent axis limits for comparison
- Groups are identified as `w{workshop}_g{group}` (e.g., w1_g1, w2_g3)
