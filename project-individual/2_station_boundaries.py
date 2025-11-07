"""
Station Boundary Detection - Individual Groups
Uses split group files from data/split/
Generates station boundaries for each individual group
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.patches import Circle
import os
import json
from glob import glob

# Configuration
SPLIT_FOLDER = "/Users/michaelUni/workspace/GitHub/NonExstnt/COS4-RTLS/data/split"
OUTPUT_FOLDER = "./output"
WORKSHOP_IDS = ["1", "2", "3"]
N_STATIONS = 6  # Expected number of stations

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def load_group_file(filepath):
    """Load a single group CSV file"""
    df = pd.read_csv(filepath)
    df["time"] = pd.to_datetime(df["time"])
    return df


def detect_stations(df, n_stations=N_STATIONS):
    """Use K-means to detect station centers"""
    positions = df[["x", "y"]].values
    kmeans = KMeans(n_clusters=n_stations, random_state=42, n_init="auto")
    kmeans.fit(positions)
    station_centers = kmeans.cluster_centers_
    station_info = []
    for i in range(n_stations):
        cluster_points = positions[kmeans.labels_ == i]
        center = station_centers[i]
        distances = np.sqrt(np.sum((cluster_points - center) ** 2, axis=1))
        radius = np.percentile(distances, 75)
        station_info.append(
            {
                "station_id": i,
                "center_x": float(center[0]),
                "center_y": float(center[1]),
                "radius": float(radius),
                "num_points": len(cluster_points),
            }
        )
    station_info = sorted(station_info, key=lambda s: s["center_x"])
    for i, station in enumerate(station_info):
        station["station_id"] = i + 1
    return station_info


def visualize_stations(df, station_info, title, xlim=None, ylim=None):
    """Visualize detected stations with boundaries"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.scatter(df["x"], df["y"], alpha=0.2, s=2, color="gray", label="All positions")
    cmap = plt.get_cmap("Set3")
    colors = [cmap(i) for i in range(len(station_info))]
    for i, station in enumerate(station_info):
        circle = Circle(
            (station["center_x"], station["center_y"]),
            station["radius"],
            facecolor=colors[i],
            alpha=0.3,
            linewidth=2,
            edgecolor="black",
            fill=True,
        )
        ax.add_patch(circle)
        ax.scatter(
            station["center_x"],
            station["center_y"],
            color="red",
            marker="x",
            s=200,
            linewidths=3,
            zorder=10,
        )
        ax.text(
            station["center_x"],
            station["center_y"],
            f"Station {station['station_id']}",
            fontsize=12,
            fontweight="bold",
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )
    ax.set_xlabel("X Position (m)", fontsize=12)
    ax.set_ylabel("Y Position (m)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)

    # Set consistent axis limits if provided
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    plt.tight_layout()
    return fig


# Main execution
print("=" * 60)
print("STATION BOUNDARY DETECTION - INDIVIDUAL GROUPS")
print("=" * 60)

# Calculate global axis limits from ALL data
print("\nCalculating global axis limits from all workshops...")
all_dfs = []
for wid in WORKSHOP_IDS:
    pattern = os.path.join(SPLIT_FOLDER, f"w{wid}_g*.csv")
    group_files = sorted(glob(pattern))
    for f in group_files:
        df = pd.read_csv(f)
        all_dfs.append(df)

combined_data = pd.concat(all_dfs, ignore_index=True)
x_min, x_max = combined_data["x"].min(), combined_data["x"].max()
y_min, y_max = combined_data["y"].min(), combined_data["y"].max()

# Add small padding
x_padding = (x_max - x_min) * 0.02
y_padding = (y_max - y_min) * 0.02
xlim = (x_min - x_padding, x_max + x_padding)
ylim = (y_min - y_padding, y_max + y_padding)

print(f"Using consistent axis limits:")
print(f"  X: {xlim[0]:.2f} to {xlim[1]:.2f}")
print(f"  Y: {ylim[0]:.2f} to {ylim[1]:.2f}")

all_station_info = {}

for wid in WORKSHOP_IDS:
    print(f"\n{'=' * 60}")
    print(f"Processing Workshop {wid}...")
    print("=" * 60)

    pattern = os.path.join(SPLIT_FOLDER, f"w{wid}_g*.csv")
    group_files = sorted(glob(pattern))
    print(f"  Found {len(group_files)} group files")

    for group_file in group_files:
        group_name = os.path.basename(group_file).replace(".csv", "")
        print(f"\n  Processing {group_name}...")
        
        df = load_group_file(group_file)
        print(f"    Loaded {len(df)} records")

        # Detect stations for this group
        station_info = detect_stations(df, n_stations=N_STATIONS)
        all_station_info[group_name] = station_info
        
        print(f"    Detected {len(station_info)} stations:")
        for station in station_info:
            print(
                f"      Station {station['station_id']}: ({station['center_x']:.2f}, {station['center_y']:.2f}) "
                f"radius={station['radius']:.2f}m [{station['num_points']} points]"
            )

        # Save visualization
        fig = visualize_stations(
            df,
            station_info,
            f"{group_name.upper()} - Detected Stations (K-means)",
            xlim,
            ylim,
        )
        output_path = os.path.join(OUTPUT_FOLDER, f"{group_name}_stations.png")
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"    ✓ Saved visualization: {output_path}")
        plt.close(fig)

# Save station information to JSON
json_path = os.path.join(OUTPUT_FOLDER, "station_boundaries_individual.json")
with open(json_path, "w") as f:
    json.dump(all_station_info, f, indent=2)
print(f"\n✓ Saved all station boundaries to: {json_path}")

print("\n" + "=" * 60)
print("COMPLETE! Individual group station boundaries detected.")
print("=" * 60)
