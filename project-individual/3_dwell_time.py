"""
Cell Dwell Time Analysis - Individual Groups
Uses split group files from data/split/
Calculates dwell time for each individual group separately
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from glob import glob

# Configuration
SPLIT_FOLDER = "/Users/michaelUni/workspace/GitHub/NonExstnt/COS4-RTLS/data/split"
STATION_FILE = "./output/station_boundaries_individual.json"
OUTPUT_FOLDER = "./output"
WORKSHOP_IDS = ["1", "2", "3"]

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def load_station_boundaries(filepath):
    """Load station boundary definitions from JSON"""
    with open(filepath, "r") as f:
        return json.load(f)


def load_group_file(filepath):
    """Load a single group CSV file"""
    df = pd.read_csv(filepath)
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time").reset_index(drop=True)
    return df


def assign_station(x, y, stations):
    """Assign a position to the nearest station within radius"""
    for station in stations:
        distance = np.sqrt(
            (x - station["center_x"]) ** 2 + (y - station["center_y"]) ** 2
        )
        if distance <= station["radius"]:
            return station["station_id"]
    return None


def calculate_dwell_times(df, stations, group_name):
    """Calculate dwell time at each station for a group"""
    # Assign stations to each record
    df["station"] = df.apply(
        lambda row: assign_station(row["x"], row["y"], stations), axis=1
    )

    # Calculate time intervals between consecutive records
    df["time_delta"] = df["time"].diff().dt.total_seconds()

    # For the first record, assume 0 dwell time
    df.loc[0, "time_delta"] = 0

    # Aggregate dwell time per station
    results = []
    for station_id in range(1, len(stations) + 1):
        # Sum all time deltas where the station matches
        station_data = df[df["station"] == station_id]
        total_dwell = station_data["time_delta"].sum()

        results.append(
            {
                "group": group_name,
                "station": station_id,
                "dwell_time_seconds": total_dwell,
                "dwell_time_minutes": total_dwell / 60,
            }
        )

    return results


def create_dwell_chart(dwell_df, group_name):
    """Create bar chart for a group's dwell times"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Filter out zero values
    plot_data = dwell_df[dwell_df["dwell_time_minutes"] > 0]

    if len(plot_data) == 0:
        plt.close(fig)
        return None

    stations = plot_data["station"].values
    dwell_times = plot_data["dwell_time_minutes"].values

    bars = ax.bar(stations, dwell_times, width=0.6, edgecolor="black", linewidth=1.5)

    # Color bars
    cmap = plt.get_cmap("tab10")
    for i, bar in enumerate(bars):
        bar.set_color(cmap(int(stations[i]) - 1))

    ax.set_xlabel("Station", fontsize=12, fontweight="bold")
    ax.set_ylabel("Dwell Time (minutes)", fontsize=12, fontweight="bold")
    ax.set_title(
        f"{group_name.upper()} - Station Dwell Times",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xticks(stations)
    ax.grid(axis="y", alpha=0.3)

    # Add value labels on top of bars
    for i, (station, time) in enumerate(zip(stations, dwell_times)):
        ax.text(
            station, time, f"{time:.1f}", ha="center", va="bottom", fontweight="bold"
        )

    plt.tight_layout()
    return fig


# Main execution
print("=" * 60)
print("CELL DWELL TIME ANALYSIS - INDIVIDUAL GROUPS")
print("=" * 60)

# Load station boundaries
station_boundaries = load_station_boundaries(STATION_FILE)
print(f"\n✓ Loaded station boundaries from {STATION_FILE}")

for wid in WORKSHOP_IDS:
    print(f"\n{'=' * 60}")
    print(f"Processing Workshop {wid}...")
    print("=" * 60)

    # Get all group files for this workshop
    pattern = os.path.join(SPLIT_FOLDER, f"w{wid}_g*.csv")
    group_files = sorted(glob(pattern))
    print(f"  Found {len(group_files)} group files")

    for group_file in group_files:
        group_name = os.path.basename(group_file).replace(".csv", "")
        print(f"\n  Processing {group_name}...")
        
        df = load_group_file(group_file)
        
        # Get station info for this specific group
        stations = station_boundaries[group_name]
        
        # Calculate dwell times
        results = calculate_dwell_times(df, stations, group_name)
        dwell_df = pd.DataFrame(results)

        # Save results
        csv_path = os.path.join(OUTPUT_FOLDER, f"{group_name}_dwell_times.csv")
        dwell_df.to_csv(csv_path, index=False)
        print(f"    ✓ Saved dwell times to: {csv_path}")

        # Display summary
        print(f"\n    Dwell Time Summary (minutes):")
        total_time = dwell_df["dwell_time_minutes"].sum()
        print(f"      Total: {total_time:.2f} min")
        for _, row in dwell_df.iterrows():
            if row["dwell_time_minutes"] > 0:
                print(
                    f"        Station {row['station']}: {row['dwell_time_minutes']:.2f} min"
                )

        # Create visualization
        fig = create_dwell_chart(dwell_df, group_name)
        if fig:
            plot_path = os.path.join(OUTPUT_FOLDER, f"{group_name}_dwell_chart.png")
            fig.savefig(plot_path, dpi=150, bbox_inches="tight")
            print(f"    ✓ Saved chart: {plot_path}")
            plt.close(fig)

print("\n" + "=" * 60)
print("COMPLETE! Individual group dwell time analysis finished.")
print("=" * 60)
