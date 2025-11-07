"""
Master script to run all RTLS analyses in sequence
Executes all 5 analysis scripts in the correct order
"""

import subprocess
import sys
import os

# Define scripts in execution order
SCRIPTS = [
    '1_spaghetti_chart.py',
    '2_station_boundaries.py',
    '3_dwell_time.py',
    '4_5_transition_production_time.py'
]

def run_script(script_name):
    """Run a Python script and display output"""
    print("\n" + "=" * 70)
    print(f"RUNNING: {script_name}")
    print("=" * 70 + "\n")
    
    result = subprocess.run(['uv', 'run', script_name], 
                          capture_output=False, 
                          text=True)
    
    if result.returncode != 0:
        print(f"\n❌ ERROR: {script_name} failed with return code {result.returncode}")
        return False
    
    print(f"\n✓ {script_name} completed successfully")
    return True

def main():
    """Run all analysis scripts in sequence"""
    print("\n" + "=" * 70)
    print("RTLS ANALYSIS - MASTER SCRIPT")
    print("Running all analyses in sequence...")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists('1_spaghetti_chart.py'):
        print("\n❌ ERROR: Please run this script from the 'projects' directory")
        return
    
    # Run each script
    success_count = 0
    for script in SCRIPTS:
        if run_script(script):
            success_count += 1
        else:
            print(f"\n⚠ Stopping execution due to error in {script}")
            break
    
    # Summary
    print("\n" + "=" * 70)
    print("EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Completed: {success_count}/{len(SCRIPTS)} scripts")
    
    if success_count == len(SCRIPTS):
        print("\n🎉 ALL ANALYSES COMPLETED SUCCESSFULLY!")
        print("\nResults are saved in the '../output/' folder:")
        print("  - Spaghetti charts: ../output/spaghetti_charts/")
        print("  - Station boundaries: ../output/station_boundaries/")
        print("  - Dwell times: ../output/dwell_time/")
        print("  - Transitions & production: ../output/transition_production_time/")
    else:
        print("\n⚠ Some analyses failed. Check error messages above.")
    
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
