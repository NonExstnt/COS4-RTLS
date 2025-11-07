# RTLS Individual Group Analysis

This folder contains analysis scripts that process each group individually, rather than comparing groups within a workshop.

## Scripts

### 2_station_boundaries.py
Detects station boundaries for each individual group using K-means clustering. The number of stations is automatically determined using **silhouette analysis** on workshop-level data, then applied to each group individually.

**Method:**
- Combines all groups from a workshop to determine optimal k
- Tests k-means clustering for k=3 to k=9
- Calculates inertia and silhouette score for each k value
- Selects optimal k based on highest silhouette score
- All groups within a workshop use the same number of stations (optimal k)
- Each group gets its own specific station centers and radii based on their individual movement data

**Output:**
- `boundaries/{group_name}_stations.png` - Visualization of detected stations for each group
- `boundaries/station_boundaries_individual.json` - Station definitions for all groups

### 3_dwell_time.py
Calculates the time each group spent at each station using the group's individual station boundaries.

**Output:**
- `dwell_time/{group_name}_dwell_times.csv` - Dwell time data for each group
- `dwell_time/{group_name}_dwell_chart.png` - Bar chart showing dwell times by station

### 4_5_transition_production_time.py
Analyzes transition times between stations and total production time for each group individually.

**Output:**
- `transition_production_time/{group_name}_transitions.csv` - Transition time data
- `transition_production_time/{group_name}_transition_chart.png` - Visualization of transitions
- `transition_production_time/{group_name}_production.csv` - Production time data
- `transition_production_time/{group_name}_production_summary.png` - Production time summary

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

All outputs (images and CSV files) are saved to `project-individual/output/` in subdirectories:
- `output/boundaries/` - Station visualizations and JSON
- `output/dwell_time/` - Dwell time CSVs and charts
- `output/transition_production_time/` - Transition and production data

## Key Differences from Main Project

- **Automatic Station Detection**: Uses silhouette analysis to determine optimal number of stations (not hardcoded)
- **Individual Station Definitions**: Each group has its own station boundaries rather than using shared workshop boundaries
- **Workshop-level Consistency**: Number of stations is consistent per workshop, but positions/radii are group-specific
- **Focused Analysis**: Results are specific to each group's movement pattern
- **Self-contained Output**: All outputs are stored within the project-individual folder
- **No Group Comparisons**: Charts focus on individual group performance rather than comparing multiple groups

## Station Detection Algorithm

For each workshop:
1. Combine all group data from that workshop
2. Test k-means clustering for k ∈ [3, 9]
3. For each k, calculate:
   - **Inertia**: Within-cluster sum of squares (lower is better)
   - **Silhouette Score**: Cluster separation quality [-1, 1] (higher is better)
4. Select k with highest silhouette score
5. Apply this k to each group individually to find their specific station centers and radii

## Notes

- Station boundaries are detected independently for each group based on their specific data
- The number of stations is determined automatically per workshop using silhouette analysis
- Minimum station dwell time is 30 seconds to filter out sensor drift
- All visualizations use consistent axis limits for comparison
- Groups are identified as `w{workshop}_g{group}` (e.g., w1_g1, w2_g3)
- Silhouette scores closer to 1 indicate well-separated clusters
- Each workshop may have a different optimal number of stations

## Dependencies

- pandas
- numpy
- matplotlib
- scikit-learn (KMeans, silhouette_score)

Python version: 3.11.x
