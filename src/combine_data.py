import os
import pandas as pd
import glob
from pathlib import Path

# Load all CSV files from the data folder
data_folder = Path("data/raw")
output_file = Path("data/combined/all_combined.csv")

csv_files = [f for f in data_folder.glob("*.csv")]

# Load and combine all data
all_data = []
for file in csv_files:
    df = pd.read_csv(file)
    df['workshop'] = os.path.basename(file).replace('.csv', '')
    all_data.append(df)

# Combine all workshops into one dataframe
combined_df = pd.concat(all_data, ignore_index=True)

print(f"Loaded {len(csv_files)} files:")
for file in csv_files:
    print(f"  - {os.path.basename(file)}")

print(f"\nCombined dataset shape: {combined_df.shape}")
print(f"\nColumn names: {list(combined_df.columns)}")
print(f"\nUnique groups: {sorted(combined_df['name'].unique())}")
print(f"\nWorkshops: {sorted(combined_df['workshop'].unique())}")

# Display first few rows
print(f"\nFirst 5 rows:")
combined_df.head()

# Save the combined dataframe to a new CSV file
combined_df.to_csv(output_file, index=False)
print(f"\nCombined data saved to {output_file}")
