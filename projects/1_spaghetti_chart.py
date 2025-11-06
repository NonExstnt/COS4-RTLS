"""
Spaghetti Chart 4.0 - Visualize movement paths for all groups in each workshop
Shows the trajectory of each group through the workshop space
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration
DATA_FOLDER = '../data/raw'
WORKSHOP_FILES = ['Workshop1.csv', 'Workshop2.csv', 'Workshop3.csv']
OUTPUT_FOLDER = '../output/spaghetti_charts'

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def load_workshop_data(filepath):
    """Load workshop CSV file"""
    df = pd.read_csv(filepath)
    df['time'] = pd.to_datetime(df['time'])
    return df

def get_axis_limits(all_workshops):
    """Get consistent x and y limits across all workshops"""
    all_x = []
    all_y = []
    
    for df in all_workshops:
        all_x.extend(df['x'].tolist())
        all_y.extend(df['y'].tolist())
    
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    
    # Add padding
    x_padding = (x_max - x_min) * 0.05
    y_padding = (y_max - y_min) * 0.05
    
    return (x_min - x_padding, x_max + x_padding), (y_min - y_padding, y_max + y_padding)

def create_spaghetti_chart(df, workshop_name, x_lim, y_lim):
    """Create spaghetti chart for a single workshop"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get unique groups
    groups = sorted(df['name'].unique())
    colors = plt.cm.tab10(range(len(groups)))
    
    # Plot each group's path
    for i, group in enumerate(groups):
        group_data = df[df['name'] == group].sort_values('time')
        ax.plot(group_data['x'], group_data['y'], 
               color=colors[i], alpha=0.7, linewidth=1.5, label=group)
        
        # Mark start and end points
        ax.scatter(group_data['x'].iloc[0], group_data['y'].iloc[0], 
                  color=colors[i], marker='o', s=100, edgecolors='black', zorder=5)
        ax.scatter(group_data['x'].iloc[-1], group_data['y'].iloc[-1], 
                  color=colors[i], marker='s', s=100, edgecolors='black', zorder=5)
    
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    ax.set_xlabel('X Position (m)', fontsize=12)
    ax.set_ylabel('Y Position (m)', fontsize=12)
    ax.set_title(f'{workshop_name} - Movement Paths\n(○ = Start, □ = End)', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Main execution
print("=" * 60)
print("SPAGHETTI CHART 4.0")
print("=" * 60)

# Load all workshop data
all_workshops = []
for workshop_file in WORKSHOP_FILES:
    filepath = os.path.join(DATA_FOLDER, workshop_file)
    df = load_workshop_data(filepath)
    all_workshops.append(df)
    print(f"\nLoaded {workshop_file}: {len(df)} records, {df['name'].nunique()} groups")

# Get consistent axis limits
x_lim, y_lim = get_axis_limits(all_workshops)
print(f"\nUsing consistent axis limits:")
print(f"  X: {x_lim[0]:.2f} to {x_lim[1]:.2f}")
print(f"  Y: {y_lim[0]:.2f} to {y_lim[1]:.2f}")

# Create spaghetti chart for each workshop
print("\nCreating spaghetti charts...")
for i, (df, workshop_file) in enumerate(zip(all_workshops, WORKSHOP_FILES)):
    workshop_name = workshop_file.replace('.csv', '')
    
    fig = create_spaghetti_chart(df, workshop_name, x_lim, y_lim)
    
    # Save figure
    output_path = os.path.join(OUTPUT_FOLDER, f'{workshop_name}_spaghetti.png')
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved: {output_path}")
    
    plt.close(fig)

print("\n" + "=" * 60)
print("COMPLETE! Charts saved to:", OUTPUT_FOLDER)
print("=" * 60)
