#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import logging
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('outlier_analysis.log')
    ]
)

# Set output directories
PLOT_DIR = os.path.join('metric_distributions', 'output', 'plots', 'outliers')
REPORT_DIR = os.path.join('metric_distributions', 'output', 'reports')
os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

def load_data():
    """Load the company metrics and metric definitions data"""
    logging.info("Starting data loading process...")
    
    # Load metrics definitions
    logging.info("Loading metrics definitions from metrics.csv...")
    metrics_df = pd.read_csv('metrics.csv')
    logging.info(f"Loaded {len(metrics_df)} metric definitions")
    
    # Load company metrics data (using full dataset)
    logging.info("Loading company metrics from company_metrics.csv...")
    company_metrics_df = pd.read_csv('company_metrics.csv')
    logging.info(f"Loaded {len(company_metrics_df)} metric records")
    
    return metrics_df, company_metrics_df

def prepare_data(metrics_df, company_metrics_df):
    """Prepare and merge the data for analysis"""
    logging.info("Starting data preparation...")
    
    # Create a metric_info dictionary with metric_group mapping
    metric_info = dict(zip(metrics_df['metric_label'], metrics_df['metric_group']))
    logging.info(f"Created mapping for {len(metric_info)} metrics")
    
    # Add metric_group to company metrics
    company_metrics_df['metric_group'] = company_metrics_df['metric_label'].map(metric_info)
    
    # Add metric_unit to company metrics
    metric_units = dict(zip(metrics_df['metric_label'], metrics_df['metric_unit']))
    company_metrics_df['metric_unit'] = company_metrics_df['metric_label'].map(metric_units)
    
    # Add metric_description
    metric_descriptions = dict(zip(metrics_df['metric_label'], metrics_df['metric_description']))
    company_metrics_df['metric_description'] = company_metrics_df['metric_label'].map(metric_descriptions)
    
    # Filter out non-numeric values
    logging.info("Converting metric values to numeric and removing non-numeric values...")
    company_metrics_df['metric_value'] = pd.to_numeric(company_metrics_df['metric_value'], errors='coerce')
    original_len = len(company_metrics_df)
    company_metrics_df = company_metrics_df.dropna(subset=['metric_value'])
    logging.info(f"Removed {original_len - len(company_metrics_df)} non-numeric values")
    
    return company_metrics_df

def detect_outliers(df, column='metric_value', method='zscore', threshold=3.0):
    """Detect outliers in the data using various methods"""
    logging.debug(f"Detecting outliers using {method} method with threshold {threshold}")
    if method == 'zscore':
        z_scores = np.abs(stats.zscore(df[column], nan_policy='omit'))
        outlier_indices = np.where(z_scores > threshold)[0]
        if len(outlier_indices) > 0:
            return df.iloc[outlier_indices].copy(), z_scores[outlier_indices]
        return pd.DataFrame(), np.array([])
    elif method == 'iqr':
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (threshold * iqr)
        upper_bound = q3 + (threshold * iqr)
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)].copy()
        
        # Calculate how many IQRs away each outlier is
        if not outliers.empty:
            outliers['iqr_distance'] = outliers[column].apply(
                lambda x: abs(x - q3) / iqr if x > upper_bound else abs(x - q1) / iqr
            )
            return outliers, outliers['iqr_distance'].values
        return pd.DataFrame(), np.array([])
    else:
        raise ValueError(f"Unknown outlier detection method: {method}")

def analyze_outliers(df):
    """Perform detailed outlier analysis for each metric"""
    logging.info("Starting outlier analysis...")
    report_lines = []
    report_lines.append("# Outlier Analysis Report\n")
    
    # Group metrics by their group
    metrics_by_group = df.groupby('metric_group')
    logging.info(f"Found {len(metrics_by_group)} metric groups to analyze")
    
    # Track significant outliers across all metrics
    all_significant_outliers = pd.DataFrame()
    
    for group_name, group_df in metrics_by_group:
        if pd.isna(group_name):
            continue
            
        logging.info(f"Analyzing outliers for group: {group_name}")
        report_lines.append(f"## {group_name.upper()} METRICS\n")
        
        # Get unique metrics in this group
        unique_metrics = group_df['metric_label'].unique()
        logging.info(f"Found {len(unique_metrics)} unique metrics in group {group_name}")
        
        for metric in unique_metrics:
            logging.info(f"Processing metric: {metric}")
            metric_df = group_df[group_df['metric_label'] == metric].copy()
            
            # Skip if less than 5 data points
            if len(metric_df) < 5:
                logging.warning(f"Insufficient data for {metric}: {len(metric_df)} records")
                continue
                
            # Get metric units and description
            unit = metric_df['metric_unit'].iloc[0] if not pd.isna(metric_df['metric_unit'].iloc[0]) else ''
            unit_str = f" ({unit})" if unit else ""
            description = metric_df['metric_description'].iloc[0] if not pd.isna(metric_df['metric_description'].iloc[0]) else 'No description available'
            
            report_lines.append(f"### {metric}{unit_str}\n")
            report_lines.append(f"**Description**: {description}\n")
            
            # Detect outliers with Z-score
            logging.info(f"Detecting Z-score outliers for {metric}")
            outliers_z, z_scores = detect_outliers(metric_df, method='zscore', threshold=3.0)
            
            # Detect outliers with IQR
            logging.info(f"Detecting IQR outliers for {metric}")
            outliers_iqr, iqr_distances = detect_outliers(metric_df, method='iqr', threshold=1.5)
            
            # Combine outlier results
            if not outliers_z.empty:
                outliers_z['outlier_score'] = z_scores
                outliers_z['outlier_method'] = 'Z-score'
                outliers_z['metric_name'] = metric
                outliers_z['metric_group'] = group_name
                all_significant_outliers = pd.concat([all_significant_outliers, outliers_z])
                
                logging.info(f"Found {len(outliers_z)} Z-score outliers for {metric}")
                report_lines.append(f"#### Z-score Outliers (threshold=3.0)\n")
                report_lines.append(f"Found {len(outliers_z)} outliers using Z-score method.\n")
                
                if len(outliers_z) > 0:
                    # Sort by outlier score
                    outliers_z = outliers_z.sort_values(by='outlier_score', ascending=False)
                    
                    # Display top 5 outliers
                    report_lines.append("Top outliers:\n")
                    for idx, (_, row) in enumerate(outliers_z.head(5).iterrows()):
                        report_lines.append(f"{idx+1}. Value: {row['metric_value']:.2f}{unit_str}, "
                                            f"Date Range: {row['metric_date_range']}, "
                                            f"Z-score: {row['outlier_score']:.2f}\n")
                    
                    # Plot outliers
                    logging.info(f"Generating Z-score outlier plots for {metric}")
                    plot_outliers(metric_df, outliers_z, metric, group_name, 'zscore', unit_str)
            
            if not outliers_iqr.empty:
                outliers_iqr['outlier_score'] = iqr_distances
                outliers_iqr['outlier_method'] = 'IQR'
                outliers_iqr['metric_name'] = metric
                outliers_iqr['metric_group'] = group_name
                all_significant_outliers = pd.concat([all_significant_outliers, outliers_iqr])
                
                logging.info(f"Found {len(outliers_iqr)} IQR outliers for {metric}")
                report_lines.append(f"\n#### IQR Outliers (threshold=1.5)\n")
                report_lines.append(f"Found {len(outliers_iqr)} outliers using IQR method.\n")
                
                if len(outliers_iqr) > 0:
                    # Sort by outlier score
                    outliers_iqr = outliers_iqr.sort_values(by='outlier_score', ascending=False)
                    
                    # Display top 5 outliers
                    report_lines.append("Top outliers:\n")
                    for idx, (_, row) in enumerate(outliers_iqr.head(5).iterrows()):
                        report_lines.append(f"{idx+1}. Value: {row['metric_value']:.2f}{unit_str}, "
                                            f"Date Range: {row['metric_date_range']}, "
                                            f"IQR Distance: {row['outlier_score']:.2f}\n")
                    
                    # Plot outliers
                    logging.info(f"Generating IQR outlier plots for {metric}")
                    plot_outliers(metric_df, outliers_iqr, metric, group_name, 'iqr', unit_str)
            
            report_lines.append("\n")
    
    # Generate comprehensive report of outliers
    logging.info("Generating summary of most significant outliers")
    report_lines.append("## Summary of Most Significant Outliers Across All Metrics\n")
    
    if not all_significant_outliers.empty:
        # Get the top 20 most significant outliers
        all_significant_outliers = all_significant_outliers.sort_values(by='outlier_score', ascending=False)
        top_outliers = all_significant_outliers.head(20)
        
        report_lines.append("| Metric Group | Metric | Value | Date Range | Method | Score |\n")
        report_lines.append("|-------------|--------|-------|------------|--------|-------|\n")
        
        for _, row in top_outliers.iterrows():
            report_lines.append(f"| {row['metric_group']} | {row['metric_name']} | "
                                f"{row['metric_value']:.2f} | {row['metric_date_range']} | "
                                f"{row['outlier_method']} | {row['outlier_score']:.2f} |\n")
    
    return ''.join(report_lines)

def plot_outliers(df, outliers_df, metric_name, metric_group, method, unit_str=''):
    """Create outlier visualizations"""
    logging.debug(f"Creating outlier plots for {metric_name} using {method} method")
    plt.figure(figsize=(12, 10))
    
    # Create subplots
    fig, axs = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Box plot with outliers highlighted
    sns.boxplot(x=df['metric_value'], ax=axs[0])
    
    if not outliers_df.empty:
        # Overlay outliers as scatter points
        y_pos = [0] * len(outliers_df)  # All points at the same y-level
        axs[0].scatter(outliers_df['metric_value'], y_pos, color='red', s=50, zorder=5)
    
    axs[0].set_title(f'Boxplot of {metric_name}{unit_str} with Outliers Highlighted')
    axs[0].set_xlabel(f'Value{unit_str}')
    
    # Plot 2: Histogram with outliers marked
    sns.histplot(df['metric_value'], kde=True, ax=axs[1])
    
    if not outliers_df.empty:
        # Mark outliers with vertical lines
        for value in outliers_df['metric_value']:
            axs[1].axvline(x=value, color='red', linestyle='--', alpha=0.7)
    
    axs[1].set_title(f'Distribution of {metric_name}{unit_str} with Outliers Marked')
    axs[1].set_xlabel(f'Value{unit_str}')
    axs[1].set_ylabel('Frequency')
    
    plt.tight_layout()
    
    # Save plot
    method_str = 'zscore' if method == 'zscore' else 'iqr'
    filename = f"{metric_group}_{metric_name}_outliers_{method_str}.png"
    plt.savefig(os.path.join(PLOT_DIR, filename))
    plt.close()
    logging.debug(f"Saved outlier plot to {filename}")

def generate_outlier_report(report_content):
    """Save the outlier analysis report"""
    logging.info("Generating outlier analysis report...")
    with open(os.path.join(REPORT_DIR, 'outlier_analysis_report.md'), 'w') as f:
        f.write(report_content)
    logging.info("Outlier analysis report generated successfully")

def main():
    """Main function to run the outlier analysis"""
    logging.info("Starting outlier analysis...")
    
    try:
        # Load data
        metrics_df, company_metrics_df = load_data()
        
        # Prepare data
        company_metrics_df = prepare_data(metrics_df, company_metrics_df)
        
        # Analyze outliers
        outlier_report = analyze_outliers(company_metrics_df)
        
        # Generate report
        generate_outlier_report(outlier_report)
        
        logging.info(f"Outlier analysis complete. Check report in {REPORT_DIR} and plots in {PLOT_DIR}")
    except Exception as e:
        logging.error(f"An error occurred during analysis: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 