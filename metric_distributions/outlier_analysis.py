#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import logging
import gc
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

def load_data(chunk_size=5000):
    """Load the company metrics and metric definitions data in chunks"""
    logging.info("Starting data loading process...")
    
    # Load metrics definitions
    logging.info("Loading metrics definitions from metrics.csv...")
    metrics_df = pd.read_csv('metrics.csv')
    logging.info(f"Loaded {len(metrics_df)} metric definitions")
    
    # Create metric info dictionaries
    metric_info = dict(zip(metrics_df['metric_label'], metrics_df['metric_group']))
    metric_units = dict(zip(metrics_df['metric_label'], metrics_df['metric_unit']))
    metric_descriptions = dict(zip(metrics_df['metric_label'], metrics_df['metric_description']))
    
    # Process company metrics in chunks
    logging.info(f"Processing company metrics in chunks of {chunk_size}...")
    chunks = []
    total_records = 0
    
    for chunk in pd.read_csv('company_metrics.csv', chunksize=chunk_size):
        try:
            # Add metric information
            chunk['metric_group'] = chunk['metric_label'].map(metric_info)
            chunk['metric_unit'] = chunk['metric_label'].map(metric_units)
            chunk['metric_description'] = chunk['metric_label'].map(metric_descriptions)
            
            # Convert to numeric and handle non-numeric values
            chunk['metric_value'] = pd.to_numeric(chunk['metric_value'], errors='coerce')
            chunk = chunk.dropna(subset=['metric_value'])
            
            if not chunk.empty:
                chunks.append(chunk)
                total_records += len(chunk)
            
            # Clear memory
            del chunk
            gc.collect()
            
            # Log progress
            logging.info(f"Processed {total_records} records so far...")
            
        except Exception as e:
            logging.error(f"Error processing chunk: {str(e)}")
            continue
    
    # Combine processed chunks
    if chunks:
        logging.info("Combining processed chunks...")
        company_metrics_df = pd.concat(chunks, ignore_index=True)
        logging.info(f"Processed {len(company_metrics_df)} metric records")
        
        # Clear memory
        del chunks
        gc.collect()
        
        return metrics_df, company_metrics_df
    else:
        logging.warning("No valid data found in company metrics")
        return metrics_df, pd.DataFrame()

def prepare_data(metrics_df, company_metrics_df):
    """Prepare the data for analysis"""
    logging.info("Starting data preparation...")
    
    # Group metrics by their group
    metrics_by_group = company_metrics_df.groupby('metric_group')
    logging.info(f"Found {len(metrics_by_group)} metric groups to analyze")
    
    return metrics_by_group

def detect_outliers(df, column='metric_value', method='zscore', threshold=3.0):
    """Detect outliers in the data using various methods"""
    logging.debug(f"Detecting outliers using {method} method with threshold {threshold}")
    
    # Handle extreme values by using log transformation for very large numbers
    if df[column].abs().max() > 1e9:  # If max absolute value is greater than 1 billion
        logging.info(f"Applying log transformation for extreme values in {column}")
        # Add small constant to handle negative values
        df = df.copy()
        df[f'{column}_transformed'] = np.log1p(df[column].abs()) * np.sign(df[column])
        column = f'{column}_transformed'
    
    if method == 'zscore':
        # Use standard Z-score calculation
        z_scores = np.abs(stats.zscore(df[column], nan_policy='omit'))
        outlier_indices = np.where(z_scores > threshold)[0]
        if len(outlier_indices) > 0:
            return df.iloc[outlier_indices].copy(), z_scores[outlier_indices]
        return pd.DataFrame(), np.array([])
    elif method == 'iqr':
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:  # Handle case where IQR is 0
            iqr = df[column].std()
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

def analyze_outliers(metrics_by_group):
    """Perform detailed outlier analysis for each metric"""
    logging.info("Starting outlier analysis...")
    report_lines = []
    report_lines.append("# Outlier Analysis Report\n")
    
    # Create a temporary directory for storing outliers
    temp_dir = os.path.join('metric_distributions', 'output', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Track significant outliers across all metrics
    outlier_files = []
    
    # Flag to start processing from debt_service_coverage_ratio
    start_processing = False
    
    for group_name, group_df in metrics_by_group:
        if pd.isna(group_name):
            continue
            
        logging.info(f"Analyzing outliers for group: {group_name}")
        report_lines.append(f"## {group_name.upper()} METRICS\n")
        
        # Get unique metrics in this group
        unique_metrics = group_df['metric_label'].unique()
        logging.info(f"Found {len(unique_metrics)} unique metrics in group {group_name}")
        
        # Process metrics in smaller batches
        batch_size = 5
        for i in range(0, len(unique_metrics), batch_size):
            batch_metrics = unique_metrics[i:i + batch_size]
            
            for metric in batch_metrics:
                # Skip until we reach debt_service_coverage_ratio
                if not start_processing:
                    if metric == 'debt_service_coverage_ratio':
                        start_processing = True
                    else:
                        continue
                
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
                
                try:
                    # Detect outliers with Z-score
                    logging.info(f"Detecting Z-score outliers for {metric}")
                    outliers_z, z_scores = detect_outliers(metric_df, method='zscore', threshold=3.0)
                    
                    # Detect outliers with IQR
                    logging.info(f"Detecting IQR outliers for {metric}")
                    outliers_iqr, iqr_distances = detect_outliers(metric_df, method='iqr', threshold=1.5)
                    
                    # Process Z-score outliers
                    if not outliers_z.empty:
                        outliers_z['outlier_score'] = z_scores
                        outliers_z['outlier_method'] = 'Z-score'
                        outliers_z['metric_name'] = metric
                        outliers_z['metric_group'] = group_name
                        
                        # Save outliers to disk
                        zscore_file = os.path.join(temp_dir, f"{group_name}_{metric}_zscore_outliers.csv")
                        outliers_z.to_csv(zscore_file, index=False)
                        outlier_files.append(zscore_file)
                        
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
                    
                    # Process IQR outliers
                    if not outliers_iqr.empty:
                        outliers_iqr['outlier_score'] = iqr_distances
                        outliers_iqr['outlier_method'] = 'IQR'
                        outliers_iqr['metric_name'] = metric
                        outliers_iqr['metric_group'] = group_name
                        
                        # Save outliers to disk
                        iqr_file = os.path.join(temp_dir, f"{group_name}_{metric}_iqr_outliers.csv")
                        outliers_iqr.to_csv(iqr_file, index=False)
                        outlier_files.append(iqr_file)
                        
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
                    
                except Exception as e:
                    logging.error(f"Error processing metric {metric}: {str(e)}")
                    report_lines.append(f"Error processing metric: {str(e)}\n\n")
                
                finally:
                    # Clear memory
                    del metric_df
                    if 'outliers_z' in locals():
                        del outliers_z
                    if 'outliers_iqr' in locals():
                        del outliers_iqr
                    gc.collect()
            
            # Clear memory after each batch
            gc.collect()
    
    # Generate comprehensive report of outliers
    logging.info("Generating summary of most significant outliers")
    report_lines.append("## Summary of Most Significant Outliers Across All Metrics\n")
    
    if outlier_files:
        try:
            # Read and combine all outlier files
            all_outliers = []
            for file in outlier_files:
                try:
                    outliers = pd.read_csv(file)
                    all_outliers.append(outliers)
                    # Delete the file after reading
                    os.remove(file)
                except Exception as e:
                    logging.error(f"Error reading outlier file {file}: {str(e)}")
            
            if all_outliers:
                # Combine all outliers and get top 20
                all_significant_outliers_df = pd.concat(all_outliers, ignore_index=True)
                all_significant_outliers_df = all_significant_outliers_df.sort_values(by='outlier_score', ascending=False)
                top_outliers = all_significant_outliers_df.head(20)
                
                report_lines.append("| Metric Group | Metric | Value | Date Range | Method | Score |\n")
                report_lines.append("|-------------|--------|-------|------------|--------|-------|\n")
                
                for _, row in top_outliers.iterrows():
                    report_lines.append(f"| {row['metric_group']} | {row['metric_name']} | "
                                        f"{row['metric_value']:.2f} | {row['metric_date_range']} | "
                                        f"{row['outlier_method']} | {row['outlier_score']:.2f} |\n")
                
                # Clear memory
                del all_outliers
                del all_significant_outliers_df
                del top_outliers
                gc.collect()
            
        except Exception as e:
            logging.error(f"Error generating summary: {str(e)}")
            report_lines.append(f"Error generating summary: {str(e)}\n")
    
    # Clean up temp directory
    try:
        os.rmdir(temp_dir)
    except Exception as e:
        logging.warning(f"Could not remove temp directory: {str(e)}")
    
    return ''.join(report_lines)

def plot_outliers(df, outliers_df, metric_name, metric_group, method, unit_str=''):
    """Create outlier visualizations"""
    logging.debug(f"Creating outlier plots for {metric_name} using {method} method")
    
    try:
        # Create figure and subplots
        fig, axs = plt.subplots(2, 1, figsize=(12, 10))
        
        # Handle extreme values for plotting
        plot_df = df.copy()
        if plot_df['metric_value'].abs().max() > 1e9:
            plot_df['metric_value'] = np.log1p(plot_df['metric_value'].abs()) * np.sign(plot_df['metric_value'])
            if not outliers_df.empty:
                outliers_df = outliers_df.copy()
                outliers_df['metric_value'] = np.log1p(outliers_df['metric_value'].abs()) * np.sign(outliers_df['metric_value'])
        
        # For debt_service_coverage_ratio, use a more aggressive sampling
        if metric_name == 'debt_service_coverage_ratio':
            # Use a smaller sample size for this metric
            sample_size = min(1000, len(plot_df))
            plot_df = plot_df.sample(n=sample_size, random_state=42)
            if not outliers_df.empty:
                # Keep only the most extreme outliers for plotting
                outliers_df = outliers_df.nlargest(10, 'outlier_score')
        
        # Plot 1: Box plot with outliers highlighted
        sns.boxplot(x=plot_df['metric_value'], ax=axs[0])
        
        if not outliers_df.empty:
            # Overlay outliers as scatter points
            y_pos = [0] * len(outliers_df)  # All points at the same y-level
            axs[0].scatter(outliers_df['metric_value'], y_pos, color='red', s=50, zorder=5)
        
        axs[0].set_title(f'Boxplot of {metric_name}{unit_str} with Outliers Highlighted')
        axs[0].set_xlabel(f'Value{unit_str}')
        
        # Plot 2: Histogram with outliers marked
        # Use fewer bins for large datasets
        bins = min(50, len(plot_df) // 10)  # Adjust number of bins based on data size
        sns.histplot(plot_df['metric_value'], bins=bins, kde=True, ax=axs[1])
        
        if not outliers_df.empty:
            # Mark outliers with vertical lines
            for value in outliers_df['metric_value']:
                axs[1].axvline(x=value, color='red', linestyle='--', alpha=0.7)
        
        axs[1].set_title(f'Distribution of {metric_name}{unit_str} with Outliers Marked')
        axs[1].set_xlabel(f'Value{unit_str}')
        axs[1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        # Save plot with lower DPI to reduce memory usage
        method_str = 'zscore' if method == 'zscore' else 'iqr'
        filename = f"{metric_group}_{metric_name}_outliers_{method_str}.png"
        plt.savefig(os.path.join(PLOT_DIR, filename), dpi=72, bbox_inches='tight')
        
        # Clean up
        plt.close(fig)
        del fig
        del axs
        del plot_df
        if not outliers_df.empty:
            del outliers_df
        gc.collect()
        
        logging.debug(f"Saved outlier plot to {filename}")
        
    except Exception as e:
        logging.error(f"Error creating plot for {metric_name}: {str(e)}")
        # Ensure figure is closed even if there's an error
        plt.close('all')
        gc.collect()

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
        metrics_by_group = prepare_data(metrics_df, company_metrics_df)
        
        # Analyze outliers
        outlier_report = analyze_outliers(metrics_by_group)
        
        # Generate report
        generate_outlier_report(outlier_report)
        
        logging.info(f"Outlier analysis complete. Check report in {REPORT_DIR} and plots in {PLOT_DIR}")
    except Exception as e:
        logging.error(f"An error occurred during analysis: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 