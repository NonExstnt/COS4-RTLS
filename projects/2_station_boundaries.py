"""
Station Boundary Detection - Use K-means clustering to define station locations
Identifies work stations based on where workers spend time
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import json

# Configuration
DATA_FOLDER = "../data/processed"
WORKSHOP_FILES = ["Workshop1.csv", "Workshop2.csv", "Workshop3.csv"]
OUTPUT_FOLDER = "../output/station_boundaries"
N_STATIONS = 6  # Expected number of stations

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def load_workshop_data(filepath):
    """Load workshop CSV file"""
    df = pd.read_csv(filepath)
    df["time"] = pd.to_datetime(df["time"])
    return df


def detect_stations(df, n_stations=N_STATIONS):
    """Use K-means to detect station centers"""
    # Get all x, y coordinates
    positions = df[["x", "y"]].values

    # Apply K-means clustering
    kmeans = KMeans(n_clusters=n_stations, random_state=42, n_init=10)
    kmeans.fit(positions)

    # Get station centers
    station_centers = kmeans.cluster_centers_

    # Calculate boundary radius for each station (using std deviation)
    station_info = []
    for i in range(n_stations):
        cluster_points = positions[kmeans.labels_ == i]
        center = station_centers[i]

        # Calculate distances from center
        distances = np.sqrt(np.sum((cluster_points - center) ** 2, axis=1))
        radius = np.percentile(distances, 75)  # Use 75th percentile as radius

        station_info.append(
            {
                "station_id": i,
                "center_x": float(center[0]),
                "center_y": float(center[1]),
                "radius": float(radius),
                "num_points": len(cluster_points),
            }
        )

    # Sort by x-coordinate for logical ordering
    station_info = sorted(station_info, key=lambda s: s["center_x"])

    # Reassign station IDs based on x-position
    for i, station in enumerate(station_info):
        station["station_id"] = i + 1

    return station_info


def visualize_stations(df, station_info, workshop_name):
    """Visualize detected stations with boundaries"""
    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot all points as background
    ax.scatter(df["x"], df["y"], alpha=0.1, s=1, color="gray", label="All positions")

    # Plot stations
    colors = plt.cm.Set3(range(len(station_info)))
    for i, station in enumerate(station_info):
        # Draw circle for station boundary
        circle = plt.Circle(
            (station["center_x"], station["center_y"]),
            station["radius"],
            facecolor=colors[i],
            alpha=0.3,
            linewidth=2,
            edgecolor="black",
            fill=True,
        )
        ax.add_patch(circle)

        # Mark center
        ax.scatter(
            station["center_x"],
            station["center_y"],
            color="red",
            marker="x",
            s=200,
            linewidths=3,
            zorder=10,
        )

        # Add label
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
    ax.set_title(
        f"{workshop_name} - Detected Stations (K-means)", fontsize=14, fontweight="bold"
    )
    ax.grid(True, alpha=0.3)
    ax.axis("equal")

    plt.tight_layout()
    return fig


# Main execution
print("=" * 60)
print("STATION BOUNDARY DETECTION (K-MEANS)")
print("=" * 60)

all_station_info = {}

for workshop_file in WORKSHOP_FILES:
    workshop_name = workshop_file.replace(".csv", "")
    print(f"\nProcessing {workshop_name}...")

    # Load data
    filepath = os.path.join(DATA_FOLDER, workshop_file)
    df = load_workshop_data(filepath)
    print(f"  Loaded {len(df)} records")

    # Detect stations
    station_info = detect_stations(df, n_stations=N_STATIONS)
    all_station_info[workshop_name] = station_info

    print(f"  Detected {len(station_info)} stations:")
    for station in station_info:
        print(
            f"    Station {station['station_id']}: "
            f"({station['center_x']:.2f}, {station['center_y']:.2f}) "
            f"radius={station['radius']:.2f}m "
            f"[{station['num_points']} points]"
        )

    # Visualize
    fig = visualize_stations(df, station_info, workshop_name)
    output_path = os.path.join(OUTPUT_FOLDER, f"{workshop_name}_stations.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"  ✓ Saved visualization: {output_path}")
    plt.close(fig)

# Save station information to JSON
json_path = os.path.join(OUTPUT_FOLDER, "station_boundaries.json")
with open(json_path, "w") as f:
    json.dump(all_station_info, f, indent=2)
print(f"\n✓ Saved station boundaries to: {json_path}")

print("\n" + "=" * 60)
print("COMPLETE! Station boundaries detected and saved.")
print("=" * 60)
