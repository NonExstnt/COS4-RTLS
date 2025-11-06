"""
Transition Time & Total Production Time Analysis
- Transition Time: Time to move from one station to the next
- Total Production Time: Time from start to end of production
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# Configuration
DATA_FOLDER = '../data/raw'
WORKSHOP_FILES = ['Workshop1.csv', 'Workshop2.csv', 'Workshop3.csv']
STATION_FILE = '../output/station_boundaries/station_boundaries.json'
OUTPUT_FOLDER = '../output/transition_production_time'

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def load_workshop_data(filepath):
    """Load workshop CSV file"""
    df = pd.read_csv(filepath)
    df['time'] = pd.to_datetime(df['time'])
    return df

def load_station_boundaries(filepath):
    """Load station boundary definitions"""
    with open(filepath, 'r') as f:
        return json.load(f)

def assign_station(x, y, stations):
    """Assign a position to the nearest station within radius"""
    for station in stations:
        distance = np.sqrt((x - station['center_x'])**2 + (y - station['center_y'])**2)
        if distance <= station['radius']:
            return station['station_id']
    return None

def analyze_transitions_and_production(df, stations):
    """Calculate transition times and total production time for each group"""
    transition_results = []
    production_results = []
    
    for group_name in sorted(df['name'].unique()):
        group_data = df[df['name'] == group_name].sort_values('time').reset_index(drop=True)
        
        # Assign stations
        group_data['station'] = group_data.apply(
            lambda row: assign_station(row['x'], row['y'], stations), axis=1
        )
        
        # Track station entries with anti-backtracking
        current_station = None
        entry_time = None
        station_sequence = []
        max_station_reached = 0
        
        for idx, row in group_data.iterrows():
            station = row['station']
            timestamp = row['time']
            
            # Anti-backtracking logic
            if station is not None and station < max_station_reached:
                station = current_station
            
            # Detect station change
            if station is not None and station != current_station:
                if current_station is not None:
                    # Record station exit
                    station_sequence.append({
                        'station': current_station,
                        'entry_time': entry_time,
                        'exit_time': timestamp
                    })
                
                # Enter new station
                current_station = station
                entry_time = timestamp
                max_station_reached = max(max_station_reached, station)
        
        # Close last station
        if current_station is not None and entry_time is not None:
            station_sequence.append({
                'station': current_station,
                'entry_time': entry_time,
                'exit_time': group_data['time'].iloc[-1]
            })
        
        # Calculate transitions (time between stations)
        for i in range(len(station_sequence) - 1):
            from_station = station_sequence[i]
            to_station = station_sequence[i + 1]
            
            transition_time = (to_station['entry_time'] - from_station['exit_time']).total_seconds()
            
            transition_results.append({
                'group': group_name,
                'from_station': from_station['station'],
                'to_station': to_station['station'],
                'transition_time_seconds': transition_time,
                'transition_time_minutes': transition_time / 60
            })
        
        # Calculate total production time
        if station_sequence:
            start_time = station_sequence[0]['entry_time']
            end_time = station_sequence[-1]['exit_time']
            total_time = (end_time - start_time).total_seconds()
            
            production_results.append({
                'group': group_name,
                'start_time': start_time,
                'end_time': end_time,
                'total_production_seconds': total_time,
                'total_production_minutes': total_time / 60,
                'stations_visited': len(station_sequence)
            })
    
    return pd.DataFrame(transition_results), pd.DataFrame(production_results)

def create_transition_comparison_chart(transition_df, workshop_name):
    """Create stacked bar chart for transition times"""
    if transition_df.empty:
        return None
    
    # Create transition labels
    transition_df['transition'] = transition_df.apply(
        lambda row: f"S{row['from_station']}→S{row['to_station']}", axis=1
    )
    
    # Pivot data
    pivot_data = transition_df.pivot(index='group', columns='transition', 
                                     values='transition_time_minutes')
    pivot_data = pivot_data.fillna(0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    pivot_data.plot(kind='bar', stacked=True, ax=ax, 
                   colormap='Set3', width=0.7, edgecolor='black')
    
    ax.set_xlabel('Group', fontsize=12, fontweight='bold')
    ax.set_ylabel('Transition Time (minutes)', fontsize=12, fontweight='bold')
    ax.set_title(f'{workshop_name} - Station Transition Time Comparison', 
                fontsize=14, fontweight='bold')
    ax.legend(title='Transition', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig

def create_production_time_chart(production_df, workshop_name):
    """Create bar chart for total production times"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    groups = production_df['group']
    times = production_df['total_production_minutes']
    
    bars = ax.bar(groups, times, color='steelblue', edgecolor='black', alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.1f}',
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Group', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Production Time (minutes)', fontsize=12, fontweight='bold')
    ax.set_title(f'{workshop_name} - Total Production Time by Group', 
                fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    # Add average line
    avg_time = times.mean()
    ax.axhline(avg_time, color='red', linestyle='--', linewidth=2, 
              label=f'Average: {avg_time:.1f} min')
    ax.legend()
    
    plt.tight_layout()
    return fig

# Main execution
print("=" * 60)
print("TRANSITION TIME & TOTAL PRODUCTION TIME ANALYSIS")
print("=" * 60)

# Load station boundaries
station_boundaries = load_station_boundaries(STATION_FILE)
print(f"\nLoaded station boundaries from {STATION_FILE}")

for workshop_file in WORKSHOP_FILES:
    workshop_name = workshop_file.replace('.csv', '')
    print(f"\n{'='*60}")
    print(f"Processing {workshop_name}...")
    print('='*60)
    
    # Load data
    filepath = os.path.join(DATA_FOLDER, workshop_file)
    df = load_workshop_data(filepath)
    
    # Get station info
    stations = station_boundaries[workshop_name]
    
    # Analyze
    transition_df, production_df = analyze_transitions_and_production(df, stations)
    
    # Save transition times
    trans_csv_path = os.path.join(OUTPUT_FOLDER, f'{workshop_name}_transitions.csv')
    transition_df.to_csv(trans_csv_path, index=False)
    print(f"✓ Saved transition times to: {trans_csv_path}")
    
    # Save production times
    prod_csv_path = os.path.join(OUTPUT_FOLDER, f'{workshop_name}_production.csv')
    production_df.to_csv(prod_csv_path, index=False)
    print(f"✓ Saved production times to: {prod_csv_path}")
    
    # Display transition summary
    print("\nTransition Times (minutes):")
    for group in sorted(transition_df['group'].unique()):
        group_data = transition_df[transition_df['group'] == group]
        print(f"\n  {group}:")
        for _, row in group_data.iterrows():
            print(f"    Station {row['from_station']} → {row['to_station']}: "
                  f"{row['transition_time_minutes']:.2f} min")
    
    # Display production summary
    print("\nTotal Production Times:")
    for _, row in production_df.iterrows():
        print(f"  {row['group']}: {row['total_production_minutes']:.2f} min "
              f"({row['stations_visited']} stations)")
    
    # Create visualizations
    if not transition_df.empty:
        fig1 = create_transition_comparison_chart(transition_df, workshop_name)
        if fig1:
            plot_path = os.path.join(OUTPUT_FOLDER, f'{workshop_name}_transition_comparison.png')
            fig1.savefig(plot_path, dpi=150, bbox_inches='tight')
            print(f"\n✓ Saved transition chart: {plot_path}")
            plt.close(fig1)
    
    fig2 = create_production_time_chart(production_df, workshop_name)
    plot_path = os.path.join(OUTPUT_FOLDER, f'{workshop_name}_production_time.png')
    fig2.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"✓ Saved production chart: {plot_path}")
    plt.close(fig2)

print("\n" + "=" * 60)
print("COMPLETE! Transition and production time analysis finished.")
print("=" * 60)
