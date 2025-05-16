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
        logging.FileHandler('correlation_analysis.log')
    ]
)

# Set output directories
PLOT_DIR = os.path.join('metric_distributions', 'output', 'plots', 'correlations')
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
    
    # Filter out non-numeric values
    logging.info("Converting metric values to numeric and removing non-numeric values...")
    company_metrics_df['metric_value'] = pd.to_numeric(company_metrics_df['metric_value'], errors='coerce')
    original_len = len(company_metrics_df)
    company_metrics_df = company_metrics_df.dropna(subset=['metric_value'])
    logging.info(f"Removed {original_len - len(company_metrics_df)} non-numeric values")
    
    return company_metrics_df

def pivot_data_for_correlation(df):
    """Pivot the data for correlation analysis"""
    logging.info("Preparing data for correlation analysis...")
    
    # Filter for common date ranges to ensure comparable metrics
    date_range_counts = df['metric_date_range'].value_counts()
    common_date_ranges = date_range_counts[date_range_counts > 10].index.tolist()
    logging.info(f"Found {len(common_date_ranges)} common date ranges with sufficient data")
    
    correlation_data = {}
    
    for date_range in common_date_ranges:
        logging.info(f"Processing date range: {date_range}")
        # Get data for this date range
        range_df = df[df['metric_date_range'] == date_range]
        
        # Pivot the data to have metrics as columns
        pivot_df = range_df.pivot_table(index='heron_id', columns='metric_label', values='metric_value')
        logging.info(f"Created pivot table with {pivot_df.shape[1]} metrics for {date_range}")
        
        # Store for analysis
        correlation_data[date_range] = pivot_df
        
    return correlation_data

def analyze_correlations(correlation_data, metrics_df):
    """Analyze correlations between metrics"""
    logging.info("Starting correlation analysis...")
    report_lines = []
    report_lines.append("# Metric Correlation Analysis\n\n")
    
    # Group metrics by their group
    metric_groups = metrics_df.groupby('metric_group')
    logging.info(f"Found {len(metric_groups)} metric groups to analyze")
    
    # For storing the most significant correlations
    top_correlations = []
    
    for date_range, pivot_df in correlation_data.items():
        logging.info(f"Analyzing correlations for date range: {date_range}")
        report_lines.append(f"## Correlations for Date Range: {date_range}\n\n")
        
        # Ensure data is numeric
        pivot_df = pivot_df.apply(pd.to_numeric, errors='coerce')
        
        # Calculate correlation matrix
        logging.info("Calculating correlation matrix...")
        corr_matrix = pivot_df.corr(method='pearson')
        
        # Plot full correlation matrix
        logging.info("Generating correlation matrix heatmap...")
        plt.figure(figsize=(16, 14))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, cmap='coolwarm', center=0, 
                    square=True, linewidths=.5, annot=False, fmt=".2f", 
                    vmin=-1, vmax=1)
        plt.title(f'Correlation Matrix for Date Range: {date_range}')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, f'correlation_matrix_{date_range}.png'))
        plt.close()
        
        # Find strong correlations
        logging.info("Identifying strong correlations...")
        strong_corr = pd.DataFrame(columns=['metric1', 'metric2', 'correlation', 'group1', 'group2'])
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                metric1 = corr_matrix.columns[i]
                metric2 = corr_matrix.columns[j]
                corr_value = corr_matrix.iloc[i, j]
                
                # Skip if NaN
                if pd.isna(corr_value):
                    continue
                
                # Only consider strong correlations (positive or negative)
                if abs(corr_value) >= 0.7:
                    # Get metric groups
                    group1 = metrics_df[metrics_df['metric_label'] == metric1]['metric_group'].iloc[0] if len(metrics_df[metrics_df['metric_label'] == metric1]) > 0 else 'unknown'
                    group2 = metrics_df[metrics_df['metric_label'] == metric2]['metric_group'].iloc[0] if len(metrics_df[metrics_df['metric_label'] == metric2]) > 0 else 'unknown'
                    
                    strong_corr = pd.concat([strong_corr, pd.DataFrame([{
                        'metric1': metric1,
                        'metric2': metric2,
                        'correlation': corr_value,
                        'group1': group1,
                        'group2': group2,
                        'date_range': date_range
                    }])], ignore_index=True)
        
        logging.info(f"Found {len(strong_corr)} strong correlations for {date_range}")
        
        # Add to top correlations
        top_correlations.append(strong_corr)
        
        # Report strong correlations
        if not strong_corr.empty:
            report_lines.append("### Strong Correlations\n\n")
            report_lines.append("| Metric 1 | Group | Metric 2 | Group | Correlation |\n")
            report_lines.append("|----------|-------|----------|-------|-------------|\n")
            
            # Sort by absolute correlation value
            strong_corr = strong_corr.sort_values(by='correlation', key=abs, ascending=False)
            
            for _, row in strong_corr.iterrows():
                report_lines.append(f"| {row['metric1']} | {row['group1']} | {row['metric2']} | {row['group2']} | {row['correlation']:.3f} |\n")
            
            # Plot top correlations by group
            for group_name, group_df in metric_groups:
                if pd.isna(group_name):
                    continue
                
                logging.info(f"Analyzing correlations for group: {group_name}")
                # Get metrics in this group
                group_metrics = group_df['metric_label'].tolist()
                
                # Find correlations with metrics in this group
                group_corr = strong_corr[
                    (strong_corr['metric1'].isin(group_metrics)) | 
                    (strong_corr['metric2'].isin(group_metrics))
                ]
                
                if not group_corr.empty:
                    logging.info(f"Found {len(group_corr)} correlations for group {group_name}")
                    report_lines.append(f"\n#### Correlations with {group_name.upper()} metrics\n\n")
                    
                    # List top correlations
                    for _, row in group_corr.head(10).iterrows():
                        report_lines.append(f"- {row['metric1']} ({row['group1']}) and {row['metric2']} ({row['group2']}): {row['correlation']:.3f}\n")
                    
                    # Create visualization for top correlating pairs
                    for _, row in group_corr.head(5).iterrows():
                        metric1 = row['metric1']
                        metric2 = row['metric2']
                        
                        logging.info(f"Generating correlation plot for {metric1} and {metric2}")
                        # Extract data for these metrics
                        data = pivot_df[[metric1, metric2]].dropna()
                        
                        if len(data) >= 5:  # Ensure we have enough data points
                            plt.figure(figsize=(10, 6))
                            sns.regplot(x=metric1, y=metric2, data=data, scatter_kws={'alpha':0.5})
                            plt.title(f'Correlation between {metric1} and {metric2}\nCorrelation: {row["correlation"]:.3f}')
                            plt.tight_layout()
                            plt.savefig(os.path.join(PLOT_DIR, f'correlation_{metric1}_{metric2}_{date_range}.png'))
                            plt.close()
            
            report_lines.append("\n")
    
    # Combine all strong correlations
    all_strong_corr = pd.concat(top_correlations, ignore_index=True) if top_correlations else pd.DataFrame()
    
    if not all_strong_corr.empty:
        logging.info("Generating summary of top correlations across all date ranges")
        report_lines.append("\n## Top Correlations Across All Date Ranges\n\n")
        report_lines.append("| Metric 1 | Group | Metric 2 | Group | Correlation | Date Range |\n")
        report_lines.append("|----------|-------|----------|-------|-------------|------------|\n")
        
        # Sort by absolute correlation value
        all_strong_corr = all_strong_corr.sort_values(by='correlation', key=abs, ascending=False)
        
        for _, row in all_strong_corr.head(20).iterrows():
            report_lines.append(f"| {row['metric1']} | {row['group1']} | {row['metric2']} | {row['group2']} | {row['correlation']:.3f} | {row['date_range']} |\n")
    
    return ''.join(report_lines)

def analyze_metric_group_correlations(correlation_data, metrics_df):
    """Analyze correlations between metric groups"""
    logging.info("Starting metric group correlation analysis...")
    report_lines = []
    report_lines.append("\n## Metric Group Correlation Analysis\n\n")
    
    for date_range, pivot_df in correlation_data.items():
        if pivot_df.shape[1] < 5:  # Skip if too few metrics
            logging.warning(f"Skipping {date_range} due to insufficient metrics: {pivot_df.shape[1]}")
            continue
            
        logging.info(f"Analyzing group correlations for date range: {date_range}")
        report_lines.append(f"\n### Group Correlations for Date Range: {date_range}\n\n")
        
        # Map metrics to groups
        metric_to_group = dict(zip(metrics_df['metric_label'], metrics_df['metric_group']))
        
        # Calculate correlations
        logging.info("Calculating correlation matrix...")
        corr_matrix = pivot_df.corr(method='pearson')
        
        # Create group correlation matrix
        groups = {}
        
        for col in corr_matrix.columns:
            group = metric_to_group.get(col)
            if pd.isna(group):
                continue
                
            if group not in groups:
                groups[group] = []
                
            groups[group].append(col)
        
        logging.info(f"Found {len(groups)} metric groups for correlation analysis")
        
        # Calculate average correlation between groups
        group_corr = pd.DataFrame(index=groups.keys(), columns=groups.keys())
        
        for group1 in groups:
            for group2 in groups:
                # Get all metrics in these groups
                metrics1 = groups[group1]
                metrics2 = groups[group2]
                
                # Calculate average correlation
                correlations = []
                
                for m1 in metrics1:
                    for m2 in metrics2:
                        if m1 != m2:  # Avoid self-correlation
                            corr_value = corr_matrix.loc[m1, m2]
                            if not pd.isna(corr_value):
                                correlations.append(corr_value)
                
                if correlations:
                    group_corr.loc[group1, group2] = np.mean(correlations)
                else:
                    group_corr.loc[group1, group2] = np.nan
        
        # Convert to numeric before plotting
        group_corr = group_corr.apply(pd.to_numeric, errors='coerce')
        
        # Plot group correlation matrix
        logging.info("Generating group correlation heatmap...")
        plt.figure(figsize=(12, 10))
        sns.heatmap(group_corr, cmap='coolwarm', center=0, 
                    square=True, linewidths=.5, annot=True, fmt=".2f",
                    vmin=-1, vmax=1)
        plt.title(f'Average Correlation Between Metric Groups for {date_range}')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, f'group_correlation_{date_range}.png'))
        plt.close()
        
        # Report strong group correlations
        logging.info("Identifying strong group correlations...")
        report_lines.append("Strong correlations between metric groups:\n\n")
        report_lines.append("| Group 1 | Group 2 | Average Correlation |\n")
        report_lines.append("|---------|---------|---------------------|\n")
        
        # Get upper triangle of the matrix
        for i in range(len(group_corr.index)):
            for j in range(i+1, len(group_corr.columns)):
                if i < len(group_corr.index) and j < len(group_corr.columns):
                    group1 = group_corr.index[i]
                    group2 = group_corr.columns[j]
                    corr_value = group_corr.iloc[i, j]
                    
                    if not pd.isna(corr_value) and abs(corr_value) >= 0.5:
                        report_lines.append(f"| {group1} | {group2} | {corr_value:.3f} |\n")
    
    return ''.join(report_lines)

def generate_correlation_report(correlation_report, group_correlation_report):
    """Save the correlation analysis report"""
    logging.info("Generating correlation analysis report...")
    with open(os.path.join(REPORT_DIR, 'correlation_analysis_report.md'), 'w') as f:
        f.write(correlation_report)
        f.write(group_correlation_report)
    logging.info("Correlation analysis report generated successfully")

def main():
    """Main function to run the correlation analysis"""
    logging.info("Starting correlation analysis...")
    
    try:
        # Load data
        metrics_df, company_metrics_df = load_data()
        
        # Prepare data
        company_metrics_df = prepare_data(metrics_df, company_metrics_df)
        
        # Pivot data for correlation analysis
        correlation_data = pivot_data_for_correlation(company_metrics_df)
        
        # Analyze correlations
        correlation_report = analyze_correlations(correlation_data, metrics_df)
        
        # Analyze group correlations
        group_correlation_report = analyze_metric_group_correlations(correlation_data, metrics_df)
        
        # Generate report
        generate_correlation_report(correlation_report, group_correlation_report)
        
        logging.info(f"Correlation analysis complete. Check report in {REPORT_DIR} and plots in {PLOT_DIR}")
    except Exception as e:
        logging.error(f"An error occurred during analysis: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 