#!/usr/bin/env python3

import os
import subprocess
import time

def main():
    """Run all metric distribution analysis scripts"""
    start_time = time.time()
    print("Starting comprehensive metric analysis...")
    
    # Define scripts to run
    scripts = [
        "metric_distribution_analysis.py",
        "outlier_analysis.py",
        "correlation_analysis.py"
    ]
    
    # Ensure output directories exist
    os.makedirs(os.path.join('metric_distributions', 'output', 'reports'), exist_ok=True)
    os.makedirs(os.path.join('metric_distributions', 'output', 'plots'), exist_ok=True)
    os.makedirs(os.path.join('metric_distributions', 'output', 'plots', 'outliers'), exist_ok=True)
    os.makedirs(os.path.join('metric_distributions', 'output', 'plots', 'correlations'), exist_ok=True)
    
    # Run each script
    for script in scripts:
        script_path = os.path.join('metric_distributions', script)
        print(f"\n{'='*50}")
        print(f"Running {script}...")
        print(f"{'='*50}\n")
        
        try:
            # Run the script
            subprocess.run(['python', script_path], check=True)
            print(f"\n✅ {script} completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error running {script}: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error running {script}: {e}")
    
    # Calculate total runtime
    total_time = time.time() - start_time
    minutes, seconds = divmod(total_time, 60)
    
    print("\n" + "="*50)
    print(f"All analyses completed in {int(minutes)} minutes and {int(seconds)} seconds.")
    print("="*50)
    
    # Print summary of outputs
    report_dir = os.path.join('metric_distributions', 'output', 'reports')
    plot_dir = os.path.join('metric_distributions', 'output', 'plots')
    
    print("\nReports generated:")
    for report in os.listdir(report_dir):
        print(f"- {os.path.join(report_dir, report)}")
    
    print("\nVisualization directories:")
    print(f"- {plot_dir}")
    print(f"- {os.path.join(plot_dir, 'outliers')}")
    print(f"- {os.path.join(plot_dir, 'correlations')}")

if __name__ == "__main__":
    main() 