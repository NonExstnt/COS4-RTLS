"""
Preprocess raw workshop data:
- Remove 'z' column (not needed for 2D analysis)
- Save cleaned data to data/processed/ folder
"""

import pandas as pd
import os

# Configuration
RAW_DATA_FOLDER = "../data/raw"
PROCESSED_DATA_FOLDER = "../data/processed"
WORKSHOP_FILES = ["Workshop1.csv", "Workshop2.csv", "Workshop3.csv"]

# Create processed data folder
os.makedirs(PROCESSED_DATA_FOLDER, exist_ok=True)

print("=" * 60)
print("DATA PREPROCESSING")
print("=" * 60)
print(f"\nRemoving 'z' column from workshop data files...")
print(f"Input folder:  {RAW_DATA_FOLDER}")
print(f"Output folder: {PROCESSED_DATA_FOLDER}\n")

for workshop_file in WORKSHOP_FILES:
    input_path = os.path.join(RAW_DATA_FOLDER, workshop_file)
    output_path = os.path.join(PROCESSED_DATA_FOLDER, workshop_file)

    # Read raw data
    df = pd.read_csv(input_path)

    # Remove z column if it exists
    if "z" in df.columns:
        df = df.drop(columns=["z"])

    # Save processed data
    df.to_csv(output_path, index=False)

    print(f"✓ Processed {workshop_file}: {len(df)} records")
    print(f"  Columns: {', '.join(df.columns)}")

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETE!")
print("=" * 60)
