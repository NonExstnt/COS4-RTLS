"""
Cell Dwell Time Analysis - Calculate time spent at each station
Uses split group files from data/split/
Calculates dwell time as ANY time within station boundaries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from glob import glob

# Configuration
SPLIT_FOLDER = "/Users/michaelUni/workspace/GitHub/NonExstnt/COS4-RTLS/data/split"
STATION_FILE = "../output/boundaries/station_boundaries.json"
OUTPUT_FOLDER = "../output/dwell_time"
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


def calculate_group_dwell_times(df, stations, group_name):
    """Calculate dwell time at each station for a single group"""
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


def create_dwell_comparison_chart(dwell_df, workshop_id):
    """Create stacked bar chart comparing dwell times across groups"""
    # Pivot data for stacked bar chart
    pivot_data = dwell_df.pivot(
        index="group", columns="station", values="dwell_time_minutes"
    )
    pivot_data = pivot_data.fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))

    # Create stacked bar chart
    pivot_data.plot(
        kind="bar", stacked=True, ax=ax, colormap="tab10", width=0.7, edgecolor="black"
    )

    ax.set_xlabel("Group", fontsize=12, fontweight="bold")
    ax.set_ylabel("Dwell Time (minutes)", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Workshop {workshop_id} - Station Dwell Time Comparison",
        fontsize=14,
        fontweight="bold",
    )
    ax.legend(title="Station", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    return fig


# Main execution
print("=" * 60)
print("CELL DWELL TIME ANALYSIS (Split Files)")
print("=" * 60)

# Load station boundaries
station_boundaries = load_station_boundaries(STATION_FILE)
print(f"\n✓ Loaded station boundaries from {STATION_FILE}")

for wid in WORKSHOP_IDS:
    print(f"\n{'=' * 60}")
    print(f"Processing Workshop {wid}...")
    print("=" * 60)

    # Get station info for this workshop
    stations = station_boundaries[f"workshop{wid}"]

    # Load all group files for this workshop
    pattern = os.path.join(SPLIT_FOLDER, f"w{wid}_g*.csv")
    group_files = sorted(glob(pattern))
    print(f"  Found {len(group_files)} group files")

    # Calculate dwell times for each group
    all_results = []
    for group_file in group_files:
        group_name = (
            os.path.basename(group_file).replace(".csv", "").replace("_", " ").title()
        )
        df = load_group_file(group_file)
        results = calculate_group_dwell_times(df, stations, group_name)
        all_results.extend(results)

    # Create results dataframe
    dwell_df = pd.DataFrame(all_results)

    # Save results
    csv_path = os.path.join(OUTPUT_FOLDER, f"workshop{wid}_dwell_times.csv")
    dwell_df.to_csv(csv_path, index=False)
    print(f"  ✓ Saved dwell times to: {csv_path}")

    # Display summary
    print("\n  Dwell Time Summary (minutes):")
    for group in sorted(dwell_df["group"].unique()):
        group_data = dwell_df[dwell_df["group"] == group]
        total_time = group_data["dwell_time_minutes"].sum()
        print(f"    {group} (Total: {total_time:.2f} min)")
        for _, row in group_data.iterrows():
            if row["dwell_time_minutes"] > 0:
                print(
                    f"      Station {row['station']}: {row['dwell_time_minutes']:.2f} min"
                )

    # Create visualization
    fig = create_dwell_comparison_chart(dwell_df, wid)
    plot_path = os.path.join(OUTPUT_FOLDER, f"workshop{wid}_dwell_comparison.png")
    fig.savefig(plot_path, dpi=150, bbox_inches="tight")
    print(f"  ✓ Saved comparison chart: {plot_path}")
    plt.close(fig)

print("\n" + "=" * 60)
print("COMPLETE! Dwell time analysis finished.")
print("=" * 60)
