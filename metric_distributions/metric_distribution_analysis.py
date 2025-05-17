#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import logging
import shutil
import gc
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('metric_distribution_analysis.log')
    ]
)

# Set output directories
PLOT_DIR = os.path.join('metric_distributions', 'output', 'plots')
REPORT_DIR = os.path.join('metric_distributions', 'output', 'reports')

def cleanup_outputs():
    """Clean up previous output files and directories"""
    logging.info("Cleaning up previous outputs...")
    
    # Remove plot directory if it exists
    if os.path.exists(PLOT_DIR):
        shutil.rmtree(PLOT_DIR)
        logging.info(f"Removed plot directory: {PLOT_DIR}")
    
    # Remove report directory if it exists
    if os.path.exists(REPORT_DIR):
        shutil.rmtree(REPORT_DIR)
        logging.info(f"Removed report directory: {REPORT_DIR}")
    
    # Create fresh directories
    os.makedirs(PLOT_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    logging.info("Created fresh output directories")

def load_metrics_definitions():
    """Load only the metrics definitions"""
    logging.info("Loading metrics definitions from metrics.csv...")
    metrics_df = pd.read_csv('metrics.csv')
    logging.info(f"Loaded {len(metrics_df)} metric definitions")
    return metrics_df

def process_metric_data(metric_name, metric_group, chunk_size=10000):
    """Process data for a single metric in chunks"""
    logging.info(f"Processing data for metric: {metric_name}")
    
    # Initialize empty list to store processed chunks
    processed_chunks = []
    
    # Read and process data in chunks
    for chunk in pd.read_csv('company_metrics.csv', chunksize=chunk_size):
        # Filter for current metric
        metric_chunk = chunk[chunk['metric_label'] == metric_name].copy()
        
        if not metric_chunk.empty:
            # Convert to numeric and handle non-numeric values
            metric_chunk['metric_value'] = pd.to_numeric(metric_chunk['metric_value'], errors='coerce')
            metric_chunk = metric_chunk.dropna(subset=['metric_value'])
            
            if not metric_chunk.empty:
                processed_chunks.append(metric_chunk)
        
        # Clear memory
        del chunk
        del metric_chunk
        gc.collect()
    
    # Combine processed chunks
    if processed_chunks:
        return pd.concat(processed_chunks, ignore_index=True)
    return pd.DataFrame()

def detect_outliers(df, column='metric_value', method='zscore', threshold=3):
    """Detect outliers in the data using various methods"""
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    logging.debug(f"Detecting outliers using {method} method with threshold {threshold}")
    if method == 'zscore':
        z_scores = np.abs(stats.zscore(df[column], nan_policy='omit'))
        outliers = df[z_scores > threshold]
        return outliers, df[~df.index.isin(outliers.index)]
    elif method == 'iqr':
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (threshold * iqr)
        upper_bound = q3 + (threshold * iqr)
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        return outliers, df[~df.index.isin(outliers.index)]
    else:
        raise ValueError(f"Unknown outlier detection method: {method}")

def analyze_metric(metric_name, metric_group, unit=''):
    """Analyze a single metric"""
    logging.info(f"Analyzing metric: {metric_name}")
    
    # Process data in chunks
    metric_df = process_metric_data(metric_name, metric_group)
    
    if len(metric_df) < 5:
        logging.warning(f"Insufficient data for {metric_name}: {len(metric_df)} records")
        del metric_df
        gc.collect()
        return None
    
    # Calculate basic statistics
    stats_dict = {
        'data_points': len(metric_df),
        'mean': metric_df['metric_value'].mean(),
        'median': metric_df['metric_value'].median(),
        'std': metric_df['metric_value'].std(),
        'min': metric_df['metric_value'].min(),
        'max': metric_df['metric_value'].max()
    }
    
    # Detect outliers
    outliers_zscore, _ = detect_outliers(metric_df, method='zscore')
    outliers_iqr, _ = detect_outliers(metric_df, method='iqr')
    
    logging.info(f"Found {len(outliers_zscore)} Z-score outliers and {len(outliers_iqr)} IQR outliers for {metric_name}")
    
    # Generate plots
    plot_distribution(metric_df, metric_name, metric_group, unit)
    
    # Clear memory
    del metric_df
    gc.collect()
    
    return {
        'stats': stats_dict,
        'zscore_outliers': len(outliers_zscore),
        'iqr_outliers': len(outliers_iqr)
    }

def plot_distribution(df, metric_name, metric_group, unit_str=''):
    """Create a probability density plot for a specific metric (linear scale only)"""
    plt.figure(figsize=(8, 6))
    
    # Calculate statistics for better plot scaling
    mean_val = df['metric_value'].mean()
    std_val = df['metric_value'].std()
    median_val = df['metric_value'].median()
    
    fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
    
    # Regular scale plot
    try:
        # Try using KDE first
        kde = stats.gaussian_kde(df['metric_value'].dropna())
        x_range = np.linspace(df['metric_value'].min(), df['metric_value'].max(), 1000)
        density = kde(x_range)
        # Normalize the density to ensure it integrates to 1
        density = density / np.trapz(density, x_range)
        
        ax1.plot(x_range, density, label='Density')
        ax1.fill_between(x_range, density, alpha=0.3)
    except np.linalg.LinAlgError:
        # Fall back to histogram if KDE fails
        hist, bins = np.histogram(df['metric_value'].dropna(), bins=50, density=True)
        ax1.hist(df['metric_value'].dropna(), bins=50, density=True, alpha=0.3, label='Histogram')
        ax1.plot(bins[:-1], hist, label='Density')
    
    ax1.set_title(f'Probability Density of {metric_name}{unit_str} (Linear Scale)')
    ax1.set_xlabel(f'Value{unit_str}')
    ax1.set_ylabel('Probability Density')
    
    # Add vertical lines for mean and median
    ax1.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:,.2f}')
    ax1.axvline(median_val, color='green', linestyle='--', label=f'Median: {median_val:,.2f}')
    ax1.legend()
    
    plt.tight_layout()
    filename = f"{metric_group}_{metric_name}_density.png"
    plt.savefig(os.path.join(PLOT_DIR, filename))
    plt.clf()
    plt.close()
    gc.collect()

def generate_report(analysis_results):
    """Generate the analysis report"""
    logging.info("Generating analysis report...")
    
    report_lines = ["# Metric Distribution Analysis\n\n"]
    report_lines.append("This report contains analysis of metric distributions, including basic statistics and outlier detection.\n\n")
    
    for group, metrics in analysis_results.items():
        report_lines.append(f"\n## {group.upper()} METRICS\n")
        report_lines.append(f"Number of metrics analyzed: {len(metrics)}\n")
        
        for metric_name, results in metrics.items():
            if results is None:
                report_lines.append(f"\n### {metric_name}\n")
                report_lines.append("Insufficient data for analysis\n")
                continue
            
            stats = results['stats']
            report_lines.append(f"\n### {metric_name}\n")
            report_lines.append(f"Data points: {stats['data_points']}\n")
            report_lines.append(f"Mean: {stats['mean']:.2f}\n")
            report_lines.append(f"Median: {stats['median']:.2f}\n")
            report_lines.append(f"Std Dev: {stats['std']:.2f}\n")
            report_lines.append(f"Min: {stats['min']:.2f}\n")
            report_lines.append(f"Max: {stats['max']:.2f}\n")
            report_lines.append(f"Z-score outliers: {results['zscore_outliers']}\n")
            report_lines.append(f"IQR outliers: {results['iqr_outliers']}\n")
    
    # Save report
    with open(os.path.join(REPORT_DIR, 'metric_distribution_analysis.md'), 'w') as f:
        f.write('\n'.join(report_lines))
    
    logging.info("Report generated successfully")

def main():
    """Main function to run the analysis"""
    logging.info("Starting metric distribution analysis...")
    
    try:
        # Clean up previous outputs
        cleanup_outputs()
        
        # Load metrics definitions
        metrics_df = load_metrics_definitions()
        
        # Initialize results dictionary
        analysis_results = {}
        
        # Process each metric group
        for group in metrics_df['metric_group'].unique():
            if pd.isna(group):
                continue
                
            logging.info(f"Processing group: {group}")
            analysis_results[group] = {}
            
            # Get metrics for this group
            group_metrics = metrics_df[metrics_df['metric_group'] == group]
            
            # Process each metric
            for _, metric_row in group_metrics.iterrows():
                metric_name = metric_row['metric_label']
                unit = metric_row['metric_unit'] if not pd.isna(metric_row['metric_unit']) else ''
                unit_str = f" ({unit})" if unit else ""
                
                # Analyze metric
                results = analyze_metric(metric_name, group, unit_str)
                analysis_results[group][metric_name] = results
                
                # Clear memory
                gc.collect()
        
        # Generate final report
        generate_report(analysis_results)
        
        logging.info(f"Analysis complete. Check reports in {REPORT_DIR} and plots in {PLOT_DIR}")
        
    except Exception as e:
        logging.error(f"An error occurred during analysis: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 