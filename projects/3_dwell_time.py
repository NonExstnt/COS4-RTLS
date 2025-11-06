"""
Cell Dwell Time Analysis - Calculate time spent at each station
Handles sensor drift by preventing false exits (no backtracking assumption)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# Configuration
DATA_FOLDER = "../data/processed"
WORKSHOP_FILES = ["Workshop1.csv", "Workshop2.csv", "Workshop3.csv"]
STATION_FILE = "../output/station_boundaries/station_boundaries.json"
OUTPUT_FOLDER = "../output/dwell_time"

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def load_workshop_data(filepath):
    """Load workshop CSV file"""
    df = pd.read_csv(filepath)
    df["time"] = pd.to_datetime(df["time"])
    return df


def load_station_boundaries(filepath):
    """Load station boundary definitions"""
    with open(filepath, "r") as f:
        return json.load(f)


def assign_station(x, y, stations):
    """Assign a position to the nearest station within radius"""
    for station in stations:
        distance = np.sqrt(
            (x - station["center_x"]) ** 2 + (y - station["center_y"]) ** 2
        )
        if distance <= station["radius"]:
            return station["station_id"]
    return None  # Not in any station


def calculate_dwell_times(df, stations):
    """Calculate dwell time at each station for each group"""
    results = []

    for group_name in sorted(df["name"].unique()):
        group_data = (
            df[df["name"] == group_name].sort_values("time").reset_index(drop=True)
        )

        # Assign stations to each record
        group_data["station"] = group_data.apply(
            lambda row: assign_station(row["x"], row["y"], stations), axis=1
        )

        # Track station visits with anti-backtracking logic
        current_station = None
        last_real_station = None
        entry_time = None
        station_visits = []
        max_station_reached = 0

        for idx, row in group_data.iterrows():
            station = row["station"]
            timestamp = row["time"]

            # Skip None/NaN stations (in transit / sensor drift)
            if station is None or pd.isna(station):
                continue

            # Apply anti-backtracking: don't go back to earlier stations
            if station < max_station_reached:
                # This is sensor drift - ignore this reading
                continue

            # Check if we're entering a new station
            if station != current_station:
                # Exit previous station
                if current_station is not None and entry_time is not None:
                    exit_time = timestamp
                    dwell_seconds = (exit_time - entry_time).total_seconds()
                    station_visits.append(
                        {
                            "station": current_station,
                            "entry_time": entry_time,
                            "exit_time": exit_time,
                            "dwell_seconds": dwell_seconds,
                        }
                    )

                # Enter new station
                current_station = station
                entry_time = timestamp
                max_station_reached = max(max_station_reached, station)

        # Close last station
        if current_station is not None and entry_time is not None:
            exit_time = group_data["time"].iloc[-1]
            dwell_seconds = (exit_time - entry_time).total_seconds()
            station_visits.append(
                {
                    "station": current_station,
                    "entry_time": entry_time,
                    "exit_time": exit_time,
                    "dwell_seconds": dwell_seconds,
                }
            )

        # Aggregate dwell time per station
        for station_id in range(1, len(stations) + 1):
            station_times = [
                v["dwell_seconds"] for v in station_visits if v["station"] == station_id
            ]
            total_dwell = sum(station_times) if station_times else 0

            results.append(
                {
                    "group": group_name,
                    "station": station_id,
                    "dwell_time_seconds": total_dwell,
                    "dwell_time_minutes": total_dwell / 60,
                }
            )

    return pd.DataFrame(results)


def create_dwell_comparison_chart(dwell_df, workshop_name):
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
        f"{workshop_name} - Station Dwell Time Comparison",
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
print("CELL DWELL TIME ANALYSIS")
print("=" * 60)

# Load station boundaries
station_boundaries = load_station_boundaries(STATION_FILE)
print(f"\nLoaded station boundaries from {STATION_FILE}")

for workshop_file in WORKSHOP_FILES:
    workshop_name = workshop_file.replace(".csv", "")
    print(f"\n{'=' * 60}")
    print(f"Processing {workshop_name}...")
    print("=" * 60)

    # Load data
    filepath = os.path.join(DATA_FOLDER, workshop_file)
    df = load_workshop_data(filepath)

    # Get station info for this workshop
    stations = station_boundaries[workshop_name]

    # Calculate dwell times
    dwell_df = calculate_dwell_times(df, stations)

    # Save results
    csv_path = os.path.join(OUTPUT_FOLDER, f"{workshop_name}_dwell_times.csv")
    dwell_df.to_csv(csv_path, index=False)
    print(f"✓ Saved dwell times to: {csv_path}")

    # Display summary
    print("\nDwell Time Summary (minutes):")
    for group in sorted(dwell_df["group"].unique()):
        group_data = dwell_df[dwell_df["group"] == group]
        total_time = group_data["dwell_time_minutes"].sum()
        print(f"\n  {group} (Total: {total_time:.2f} min):")
        for _, row in group_data.iterrows():
            print(f"    Station {row['station']}: {row['dwell_time_minutes']:.2f} min")

    # Create visualization
    fig = create_dwell_comparison_chart(dwell_df, workshop_name)
    plot_path = os.path.join(OUTPUT_FOLDER, f"{workshop_name}_dwell_comparison.png")
    fig.savefig(plot_path, dpi=150, bbox_inches="tight")
    print(f"\n✓ Saved comparison chart: {plot_path}")
    plt.close(fig)

print("\n" + "=" * 60)
print("COMPLETE! Dwell time analysis finished.")
print("=" * 60)
