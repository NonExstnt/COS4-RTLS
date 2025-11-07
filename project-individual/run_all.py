"""
Run All Individual Group Analyses
Executes all analysis scripts in the correct order
"""

import subprocess
import sys
import os

# List of scripts to run in order
SCRIPTS = [
    "2_station_boundaries.py",
    "3_dwell_time.py",
    "4_5_transition_production_time.py",
]


def run_script(script_name):
    """Run a single Python script"""
    print(f"\n{'=' * 70}")
    print(f"RUNNING: {script_name}")
    print("=" * 70)

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True,
        )
        print(f"\n✓ {script_name} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {script_name} failed with error code {e.returncode}")
        return False


def main():
    """Main execution"""
    print("=" * 70)
    print("RTLS INDIVIDUAL GROUP ANALYSIS - RUN ALL SCRIPTS")
    print("=" * 70)
    print(f"\nRunning {len(SCRIPTS)} analysis scripts in sequence...")

    # Check if output folder exists, create if not
    output_folder = "./output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"\n✓ Created output folder: {output_folder}")

    success_count = 0
    failed_scripts = []

    for script in SCRIPTS:
        if run_script(script):
            success_count += 1
        else:
            failed_scripts.append(script)

    # Summary
    print("\n" + "=" * 70)
    print("EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Total scripts: {len(SCRIPTS)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(failed_scripts)}")

    if failed_scripts:
        print("\nFailed scripts:")
        for script in failed_scripts:
            print(f"  - {script}")
        sys.exit(1)
    else:
        print("\n✓ All analyses completed successfully!")
        print(f"\nResults saved to: {os.path.abspath(output_folder)}")


if __name__ == "__main__":
    main()
