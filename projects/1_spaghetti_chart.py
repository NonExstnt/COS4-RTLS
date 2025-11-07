"""
Spaghetti Chart 4.0 - Visualize movement paths for all groups in each workshop
Uses split group files from data/split/
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob

# Configuration
SPLIT_FOLDER = "../data/split"
OUTPUT_FOLDER = "../output/spaghetti"
WORKSHOP_IDS = ["1", "2", "3"]

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def load_split_group_files(workshop_id):
    """Load all group files for a given workshop"""
    pattern = os.path.join(SPLIT_FOLDER, f"w{workshop_id}_g*.csv")
    files = sorted(glob(pattern))
    dfs = [pd.read_csv(f) for f in files]
    for df in dfs:
        df["time"] = pd.to_datetime(df["time"])
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def get_axis_limits(all_workshops):
    """Get consistent x and y limits across all workshops"""
    all_x = []
    all_y = []
    for df in all_workshops:
        all_x.extend(df["x"].tolist())
        all_y.extend(df["y"].tolist())
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)

    # Add padding
    x_padding = (x_max - x_min) * 0.05
    y_padding = (y_max - y_min) * 0.05
    return (x_min - x_padding, x_max + x_padding), (
        y_min - y_padding,
        y_max + y_padding,
    )


def create_spaghetti_chart(df, workshop_id, x_lim, y_lim):
    """Create spaghetti chart for a single workshop"""
    fig, ax = plt.subplots(figsize=(12, 8))
    groups = sorted(df["name"].unique())
    cmap = plt.get_cmap("tab10")
    colors = [cmap(i) for i in range(len(groups))]
    for i, group in enumerate(groups):
        group_data = df[df["name"] == group].sort_values("time")
        ax.plot(
            group_data["x"],
            group_data["y"],
            color=colors[i],
            alpha=0.7,
            linewidth=1.5,
            label=group,
        )

        # Mark start and end points
        ax.scatter(
            group_data["x"].iloc[0],
            group_data["y"].iloc[0],
            color=colors[i],
            marker="o",
            s=100,
            edgecolors="black",
            zorder=5,
        )
        ax.scatter(
            group_data["x"].iloc[-1],
            group_data["y"].iloc[-1],
            color=colors[i],
            marker="s",
            s=100,
            edgecolors="black",
            zorder=5,
        )
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    ax.set_xlabel("X Position (m)", fontsize=12)
    ax.set_ylabel("Y Position (m)", fontsize=12)
    ax.set_title(
        f"Workshop {workshop_id} - Movement Paths\n(○ = Start, □ = End)",
        fontsize=14,
        fontweight="bold",
    )
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


# Main execution
print("=" * 60)
print("SPAGHETTI CHART 4.0 (Split Files)")
print("=" * 60)

# Load all workshops
all_workshops = []
for wid in WORKSHOP_IDS:
    df = load_split_group_files(wid)
    all_workshops.append(df)
    print(f"\nLoaded Workshop {wid}: {len(df)} records, {df['name'].nunique()} groups")

# Get consistent axis limits
x_lim, y_lim = get_axis_limits(all_workshops)
print(f"\nUsing consistent axis limits:")
print(f"  X: {x_lim[0]:.2f} to {x_lim[1]:.2f}")
print(f"  Y: {y_lim[0]:.2f} to {y_lim[1]:.2f}")

# Create spaghetti chart for each workshop
print("\nCreating spaghetti charts...")
for i, wid in enumerate(WORKSHOP_IDS):
    df = all_workshops[i]
    fig = create_spaghetti_chart(df, wid, x_lim, y_lim)
    output_path = os.path.join(OUTPUT_FOLDER, f"workshop{wid}_spaghetti.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"  ✓ Saved: {output_path}")
    plt.close(fig)

print("\n" + "=" * 60)
print("COMPLETE! Charts saved to:", OUTPUT_FOLDER)
print("=" * 60)
