"""
Station Boundary Detection - Use K-means clustering to define station locations
Uses split group files from data/split/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from matplotlib.patches import Circle
import os
import json
from glob import glob

# Configuration
SPLIT_FOLDER = "/Users/michaelUni/workspace/GitHub/NonExstnt/COS4-RTLS/data/split"
OUTPUT_FOLDER = "../output/boundaries"
WORKSHOP_IDS = ["1", "2", "3"]

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def load_split_group_files(workshop_id):
    """Load all group files for a given workshop"""
    pattern = os.path.join(SPLIT_FOLDER, f"w{workshop_id}_g*.csv")
    abs_pattern = os.path.abspath(pattern)
    print(f"  Searching for files with pattern: {abs_pattern}")
    files = sorted(glob(abs_pattern))
    print(f"  Found files for workshop {workshop_id}: {files}")
    dfs = [pd.read_csv(f) for f in files]
    for df in dfs:
        df["time"] = pd.to_datetime(df["time"])
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def determine_optimal_clusters(df):
    """
    Determine optimal number of clusters using elbow method and silhouette analysis
    Returns the optimal k value
    """
    coords = df[["x", "y"]].values

    # Elbow method and silhouette analysis
    k_range = range(3, 10)
    inertias = []
    silhouette_scores_list = []

    print("\n  Analyzing optimal number of stations:")
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
        labels = kmeans.fit_predict(coords)
        inertias.append(kmeans.inertia_)
        silhouette_scores_list.append(silhouette_score(coords, labels))
        print(
            f"    k={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={silhouette_scores_list[-1]:.3f}"
        )

    # Find optimal k based on highest silhouette score
    # (silhouette score ranges from -1 to 1, higher is better)
    optimal_k = k_range[np.argmax(silhouette_scores_list)]
    max_silhouette = max(silhouette_scores_list)

    print(
        f"\n  → Selected k={optimal_k} (highest silhouette score: {max_silhouette:.3f})"
    )

    return optimal_k


def detect_stations(df, n_stations):
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
    ax.scatter(df["x"], df["y"], alpha=0.1, s=1, color="gray", label="All positions")
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
print("STATION BOUNDARY DETECTION (K-MEANS, Split Files)")
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

    # Load combined workshop data
    df = load_split_group_files(wid)
    print(f"  Loaded {len(df)} records")

    # Determine optimal number of stations from workshop-level data
    n_stations = determine_optimal_clusters(df)

    # Detect stations for combined workshop
    station_info = detect_stations(df, n_stations)
    all_station_info[f"workshop{wid}"] = station_info
    print(f"  Detected {len(station_info)} stations:")
    for station in station_info:
        print(
            f"    Station {station['station_id']}: ({station['center_x']:.2f}, {station['center_y']:.2f}) radius={station['radius']:.2f}m [{station['num_points']} points]"
        )

    # Save combined workshop visualization
    fig = visualize_stations(
        df,
        station_info,
        f"Workshop {wid} - Detected Stations (K-means, n={n_stations})",
        xlim,
        ylim,
    )
    output_path = os.path.join(OUTPUT_FOLDER, f"workshop{wid}_stations.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"  ✓ Saved combined visualization: {output_path}")
    plt.close(fig)

    # Process individual groups
    print(f"\n  Processing individual groups...")
    pattern = os.path.join(SPLIT_FOLDER, f"w{wid}_g*.csv")
    group_files = sorted(glob(pattern))

    for group_file in group_files:
        group_name = os.path.basename(group_file).replace(".csv", "")
        group_df = pd.read_csv(group_file)
        group_df["time"] = pd.to_datetime(group_df["time"])

        # Create visualization for individual group using workshop station boundaries
        fig = visualize_stations(
            group_df,
            station_info,
            f"Workshop {wid} - {group_name.upper()} - Station Boundaries (n={n_stations})",
            xlim,
            ylim,
        )
        group_output_path = os.path.join(OUTPUT_FOLDER, f"{group_name}_stations.png")
        fig.savefig(group_output_path, dpi=150, bbox_inches="tight")
        print(f"    ✓ Saved {group_name}: {group_output_path}")
        plt.close(fig)

# Save station information to JSON
json_path = os.path.join(OUTPUT_FOLDER, "station_boundaries.json")
with open(json_path, "w") as f:
    json.dump(all_station_info, f, indent=2)
print(f"\n✓ Saved station boundaries to: {json_path}")

print("\n" + "=" * 60)
print("COMPLETE! Station boundaries detected and saved.")
print("=" * 60)
