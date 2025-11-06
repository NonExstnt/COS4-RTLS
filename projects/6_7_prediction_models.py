"""
Predictive Models using Random Forest Regression
1. Transition Time Prediction - When will they reach the next station
2. Production Time Prediction - How long will production take
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Configuration
DATA_FOLDER = "../data/raw"
WORKSHOP_FILES = ["Workshop1.csv", "Workshop2.csv", "Workshop3.csv"]
STATION_FILE = "../output/station_boundaries/station_boundaries.json"
OUTPUT_FOLDER = "../output/prediction_models"

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def load_workshop_data(filepath):
    """Load workshop CSV file"""
    df = pd.read_csv(filepath)
    df["time"] = pd.to_datetime(df["time"])
    return df


def load_station_boundaries(filepath):
    """Load station boundary definitions"""
    with open(filepath, "r") as f:
        return json.load(f)


def assign_station(x, y, stations):
    """Assign a position to the nearest station within radius"""
    for station in stations:
        distance = np.sqrt(
            (x - station["center_x"]) ** 2 + (y - station["center_y"]) ** 2
        )
        if distance <= station["radius"]:
            return station["station_id"]
    return None


def extract_features_for_prediction(df, stations):
    """Extract features for prediction models"""
    transition_features = []
    production_features = []

    for group_name in sorted(df["name"].unique()):
        group_data = (
            df[df["name"] == group_name].sort_values("time").reset_index(drop=True)
        )

        # Assign stations
        group_data["station"] = group_data.apply(
            lambda row: assign_station(row["x"], row["y"], stations), axis=1
        )

        # Track station visits
        current_station = None
        entry_time = None
        dwell_time = None
        station_sequence = []
        max_station_reached = 0

        for idx, row in group_data.iterrows():
            station = row["station"]
            timestamp = row["time"]

            # Skip None stations (in transit)
            if station is None:
                continue

            # Anti-backtracking
            if station < max_station_reached:
                continue

            if station != current_station:
                if current_station is not None:
                    exit_time = timestamp
                    dwell = (exit_time - entry_time).total_seconds()

                    station_sequence.append(
                        {
                            "station": current_station,
                            "entry_time": entry_time,
                            "exit_time": exit_time,
                            "dwell_seconds": dwell,
                        }
                    )

                current_station = station
                entry_time = timestamp
                max_station_reached = max(max_station_reached, station)

        # Close last station
        if current_station is not None and entry_time is not None:
            exit_time = group_data["time"].iloc[-1]
            dwell = (exit_time - entry_time).total_seconds()
            station_sequence.append(
                {
                    "station": current_station,
                    "entry_time": entry_time,
                    "exit_time": exit_time,
                    "dwell_seconds": dwell,
                }
            )

        # Build transition features
        for i in range(len(station_sequence) - 1):
            from_station = station_sequence[i]
            to_station = station_sequence[i + 1]

            transition_time = (
                to_station["entry_time"] - from_station["exit_time"]
            ).total_seconds()

            # Features: from_station, to_station, dwell_at_from_station
            transition_features.append(
                {
                    "from_station": from_station["station"],
                    "to_station": to_station["station"],
                    "dwell_at_from": from_station["dwell_seconds"],
                    "transition_time": transition_time,
                }
            )

        # Build production features
        if len(station_sequence) >= 2:
            total_time = (
                station_sequence[-1]["exit_time"] - station_sequence[0]["entry_time"]
            ).total_seconds()
            total_dwell = sum([s["dwell_seconds"] for s in station_sequence])
            num_stations = len(station_sequence)

            production_features.append(
                {
                    "num_stations": num_stations,
                    "avg_dwell_time": total_dwell / num_stations,
                    "first_station": station_sequence[0]["station"],
                    "last_station": station_sequence[-1]["station"],
                    "total_production_time": total_time,
                }
            )

    return pd.DataFrame(transition_features), pd.DataFrame(production_features)


def train_transition_model(transition_df):
    """Train Random Forest model to predict transition time"""
    if len(transition_df) < 5:
        print("  ⚠ Not enough data for transition prediction")
        return None, None

    # Prepare features and target
    X = transition_df[["from_station", "to_station", "dwell_at_from"]]
    y = transition_df["transition_time"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results = {"mae": mae, "rmse": rmse, "r2": r2, "y_test": y_test, "y_pred": y_pred}

    return model, results


def train_production_model(production_df):
    """Train Random Forest model to predict total production time"""
    if len(production_df) < 3:
        print("  ⚠ Not enough data for production prediction")
        return None, None

    # Prepare features and target
    X = production_df[
        ["num_stations", "avg_dwell_time", "first_station", "last_station"]
    ]
    y = production_df["total_production_time"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results = {"mae": mae, "rmse": rmse, "r2": r2, "y_test": y_test, "y_pred": y_pred}

    return model, results


def plot_prediction_results(results, title, ylabel):
    """Plot actual vs predicted values"""
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(
        results["y_test"], results["y_pred"], alpha=0.6, s=100, edgecolors="black"
    )

    # Perfect prediction line
    min_val = min(results["y_test"].min(), results["y_pred"].min())
    max_val = max(results["y_test"].max(), results["y_pred"].max())
    ax.plot(
        [min_val, max_val],
        [min_val, max_val],
        "r--",
        linewidth=2,
        label="Perfect Prediction",
    )

    ax.set_xlabel(f"Actual {ylabel}", fontsize=12, fontweight="bold")
    ax.set_ylabel(f"Predicted {ylabel}", fontsize=12, fontweight="bold")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add metrics text
    metrics_text = f"MAE: {results['mae']:.2f}\nRMSE: {results['rmse']:.2f}\nR²: {results['r2']:.3f}"
    ax.text(
        0.05,
        0.95,
        metrics_text,
        transform=ax.transAxes,
        fontsize=11,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    plt.tight_layout()
    return fig


# Main execution
print("=" * 60)
print("PREDICTIVE MODELS (RANDOM FOREST REGRESSION)")
print("=" * 60)

# Load station boundaries
station_boundaries = load_station_boundaries(STATION_FILE)
print(f"\nLoaded station boundaries from {STATION_FILE}")

for workshop_file in WORKSHOP_FILES:
    workshop_name = workshop_file.replace(".csv", "")
    print(f"\n{'=' * 60}")
    print(f"Processing {workshop_name}...")
    print("=" * 60)

    # Load data
    filepath = os.path.join(DATA_FOLDER, workshop_file)
    df = load_workshop_data(filepath)

    # Get station info
    stations = station_boundaries[workshop_name]

    # Extract features
    transition_df, production_df = extract_features_for_prediction(df, stations)

    print(f"\nExtracted {len(transition_df)} transition records")
    print(f"Extracted {len(production_df)} production records")

    # Train transition prediction model
    print("\n--- Transition Time Prediction ---")
    trans_model, trans_results = train_transition_model(transition_df)

    if trans_results:
        print(f"  MAE: {trans_results['mae']:.2f} seconds")
        print(f"  RMSE: {trans_results['rmse']:.2f} seconds")
        print(f"  R² Score: {trans_results['r2']:.3f}")

        # Plot
        fig = plot_prediction_results(
            trans_results,
            f"{workshop_name} - Transition Time Prediction",
            "Time (seconds)",
        )
        plot_path = os.path.join(
            OUTPUT_FOLDER, f"{workshop_name}_transition_prediction.png"
        )
        fig.savefig(plot_path, dpi=150, bbox_inches="tight")
        print(f"  ✓ Saved plot: {plot_path}")
        plt.close(fig)

    # Train production prediction model
    print("\n--- Production Time Prediction ---")
    prod_model, prod_results = train_production_model(production_df)

    if prod_results:
        print(
            f"  MAE: {prod_results['mae']:.2f} seconds ({prod_results['mae'] / 60:.2f} minutes)"
        )
        print(
            f"  RMSE: {prod_results['rmse']:.2f} seconds ({prod_results['rmse'] / 60:.2f} minutes)"
        )
        print(f"  R² Score: {prod_results['r2']:.3f}")

        # Plot
        fig = plot_prediction_results(
            prod_results,
            f"{workshop_name} - Production Time Prediction",
            "Time (seconds)",
        )
        plot_path = os.path.join(
            OUTPUT_FOLDER, f"{workshop_name}_production_prediction.png"
        )
        fig.savefig(plot_path, dpi=150, bbox_inches="tight")
        print(f"  ✓ Saved plot: {plot_path}")
        plt.close(fig)

print("\n" + "=" * 60)
print("COMPLETE! Prediction models trained and evaluated.")
print("=" * 60)
