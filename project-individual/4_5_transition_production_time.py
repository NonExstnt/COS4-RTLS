"""
Transition Time & Total Production Time Analysis - Individual Groups
Uses split group files from data/split/
Calculates transition and production times for each individual group separately
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from glob import glob

# Configuration
SPLIT_FOLDER = "/Users/michaelUni/workspace/GitHub/NonExstnt/COS4-RTLS/data/split"
STATION_FILE = "./output/boundaries/station_boundaries_individual.json"
OUTPUT_FOLDER = "./output/transition_production_times"
WORKSHOP_IDS = ["1", "2", "3"]
MIN_STATION_DWELL_SECONDS = 30  # Minimum time in station to count as a real visit

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


def analyze_transitions_and_production(df, stations, group_name):
    """Calculate transition times and total production time for a single group"""
    # Assign stations
    df["station"] = df.apply(
        lambda row: assign_station(row["x"], row["y"], stations), axis=1
    )

    # Track station entries (no anti-backtracking)
    current_station = None
    entry_time = None
    last_timestamp = None
    station_sequence = []

    for idx, row in df.iterrows():
        station = row["station"]
        timestamp = row["time"]

        # Skip None stations (in transit)
        if station is None or pd.isna(station):
            continue

        # Detect station change
        if station != current_station:
            if current_station is not None:
                # Record station exit
                station_sequence.append(
                    {
                        "station": current_station,
                        "entry_time": entry_time,
                        "exit_time": last_timestamp,
                    }
                )

            # Enter new station
            current_station = station
            entry_time = timestamp

        # Update last timestamp
        last_timestamp = timestamp

    # Close last station
    if current_station is not None and entry_time is not None:
        station_sequence.append(
            {
                "station": current_station,
                "entry_time": entry_time,
                "exit_time": df["time"].iloc[-1],
            }
        )

    # Filter out very short station visits (likely sensor drift)
    filtered_sequence = []
    for visit in station_sequence:
        dwell_time = (visit["exit_time"] - visit["entry_time"]).total_seconds()
        if dwell_time >= MIN_STATION_DWELL_SECONDS:
            filtered_sequence.append(visit)

    station_sequence = filtered_sequence

    # Calculate transitions
    transition_results = []
    for i in range(len(station_sequence) - 1):
        from_station = station_sequence[i]
        to_station = station_sequence[i + 1]

        transition_time = (
            to_station["entry_time"] - from_station["exit_time"]
        ).total_seconds()

        transition_results.append(
            {
                "group": group_name,
                "from_station": from_station["station"],
                "to_station": to_station["station"],
                "transition_time_seconds": transition_time,
                "transition_time_minutes": transition_time / 60,
            }
        )

    # Calculate total production time
    production_results = []
    if station_sequence:
        start_time = station_sequence[0]["entry_time"]
        end_time = station_sequence[-1]["exit_time"]
        total_time = (end_time - start_time).total_seconds()

        production_results.append(
            {
                "group": group_name,
                "start_time": start_time,
                "end_time": end_time,
                "total_production_seconds": total_time,
                "total_production_minutes": total_time / 60,
                "stations_visited": len(station_sequence),
            }
        )

    return transition_results, production_results


def create_transition_chart(transition_df, group_name):
    """Create bar chart for transition times"""
    if transition_df.empty:
        return None

    # Create transition labels
    transition_df["transition"] = transition_df.apply(
        lambda row: f"S{int(row['from_station'])}→S{int(row['to_station'])}", axis=1
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    transitions = transition_df["transition"]
    times = transition_df["transition_time_minutes"]

    bars = ax.bar(range(len(transitions)), times, color="skyblue", edgecolor="black", alpha=0.8)

    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_xlabel("Transition", fontsize=12, fontweight="bold")
    ax.set_ylabel("Transition Time (minutes)", fontsize=12, fontweight="bold")
    ax.set_title(
        f"{group_name.upper()} - Station Transition Times",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xticks(range(len(transitions)))
    ax.set_xticklabels(transitions, rotation=45, ha="right")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    return fig


def create_production_summary_chart(production_row, group_name):
    """Create simple summary chart for production time"""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Display as text summary
    ax.axis('off')
    
    summary_text = f"""
    {group_name.upper()}
    
    Production Time Summary
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Total Production Time: {production_row['total_production_minutes']:.1f} minutes
    
    Stations Visited: {production_row['stations_visited']}
    
    Start Time: {production_row['start_time'].strftime('%H:%M:%S')}
    End Time: {production_row['end_time'].strftime('%H:%M:%S')}
    """
    
    ax.text(0.5, 0.5, summary_text, 
            ha='center', va='center',
            fontsize=12, fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    return fig


# Main execution
print("=" * 60)
print("TRANSITION & PRODUCTION TIME ANALYSIS - INDIVIDUAL GROUPS")
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
        
        # Analyze transitions and production
        transitions, production = analyze_transitions_and_production(df, stations, group_name)

        # Create dataframes
        transition_df = pd.DataFrame(transitions)
        production_df = pd.DataFrame(production)

        # Save transition times
        if not transition_df.empty:
            trans_csv_path = os.path.join(OUTPUT_FOLDER, f"{group_name}_transitions.csv")
            transition_df.to_csv(trans_csv_path, index=False)
            print(f"    ✓ Saved transition times to: {trans_csv_path}")

            # Display transition summary
            print(f"\n    Transition Times (minutes):")
            for _, row in transition_df.iterrows():
                print(
                    f"      Station {row['from_station']} → {row['to_station']}: "
                    f"{row['transition_time_minutes']:.2f} min"
                )

            # Create transition chart
            fig = create_transition_chart(transition_df, group_name)
            if fig:
                plot_path = os.path.join(OUTPUT_FOLDER, f"{group_name}_transition_chart.png")
                fig.savefig(plot_path, dpi=150, bbox_inches="tight")
                print(f"    ✓ Saved transition chart: {plot_path}")
                plt.close(fig)
        else:
            print(f"    No transitions detected (single station visit)")

        # Save production times
        if not production_df.empty:
            prod_csv_path = os.path.join(OUTPUT_FOLDER, f"{group_name}_production.csv")
            production_df.to_csv(prod_csv_path, index=False)
            print(f"    ✓ Saved production times to: {prod_csv_path}")

            # Display production summary
            print(f"\n    Total Production Time:")
            row = production_df.iloc[0]
            print(
                f"      {row['total_production_minutes']:.2f} min "
                f"({row['stations_visited']} stations)"
            )

            # Create production summary chart
            fig = create_production_summary_chart(row, group_name)
            plot_path = os.path.join(OUTPUT_FOLDER, f"{group_name}_production_summary.png")
            fig.savefig(plot_path, dpi=150, bbox_inches="tight")
            print(f"    ✓ Saved production summary: {plot_path}")
            plt.close(fig)

print("\n" + "=" * 60)
print("COMPLETE! Individual group analysis finished.")
print("=" * 60)
