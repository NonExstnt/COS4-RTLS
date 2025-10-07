import pandas as pd
import os
from pathlib import Path
import re

def split_workshop_files():
    """
    Split workshop CSV files by group, creating individual files for each group.
    Output format: w<workshop_number>_g<group_number>.csv
    """
    # Define paths
    raw_data_folder = Path("../data/raw")
    split_data_folder = Path("../data/split")
    
    # Get all workshop CSV files (excluding combined folder)
    workshop_files = [f for f in raw_data_folder.glob("*.csv")]
    
    if not workshop_files:
        print("No workshop CSV files found in the data folder.")
        return
    
    print(f"Found {len(workshop_files)} workshop files:")
    for file in workshop_files:
        print(f"  - {file.name}")
    
    total_files_created = 0
    
    for workshop_file in workshop_files:
        print(f"\nProcessing {workshop_file.name}...")
        
        try:
            # Read the workshop data
            df = pd.read_csv(workshop_file)
            print(f"  Loaded {len(df)} rows")
            
            # Extract workshop number from filename (e.g., "Workshop1.csv" -> "1")
            workshop_match = re.search(r'Workshop(\d+)', workshop_file.stem)
            if not workshop_match:
                print(f"  Warning: Could not extract workshop number from {workshop_file.name}")
                continue
            
            workshop_num = workshop_match.group(1)
            
            # Check if 'name' column exists
            if 'name' not in df.columns:
                print(f"  Error: 'name' column not found in {workshop_file.name}")
                continue
            
            print(f"  Groups found: {sorted(df['name'].unique())}")
            
            # Group by 'name' column and save each group
            for group_name, group_data in df.groupby('name'):
                # Extract group number from group name (e.g., "Group 1" -> "1", "group 4" -> "4")
                group_match = re.search(r'group\s*(\d+)', group_name.lower())
                if not group_match:
                    print(f"    Warning: Could not extract group number from '{group_name}'")
                    continue
                
                group_num = group_match.group(1)
                
                # Create output filename
                output_filename = f"w{workshop_num}_g{group_num}.csv"
                output_path = split_data_folder / output_filename
                
                # Save the group data
                group_data.to_csv(output_path, index=False)
                print(f"    Created {output_filename} with {len(group_data)} rows")
                total_files_created += 1
                
        except Exception as e:
            print(f"  Error processing {workshop_file.name}: {str(e)}")
    
    print(f"\n✅ Successfully created {total_files_created} group files in the data folder.")

def main():
    """Main function to run the splitting process."""
    print("RTLS Data Splitter")
    print("=" * 50)
    print("Splitting workshop files by group...")
    
    split_workshop_files()
    
    print("\n" + "=" * 50)
    print("Process completed!")

if __name__ == "__main__":
    main()