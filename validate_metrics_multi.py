import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
from pathlib import Path

# Create output directories
Path("outputs/multi/distributions").mkdir(parents=True, exist_ok=True)
Path("outputs/multi/anomalies").mkdir(parents=True, exist_ok=True)
Path("outputs/multi/trends").mkdir(parents=True, exist_ok=True)
Path("outputs/multi/relationships").mkdir(parents=True, exist_ok=True)
Path("outputs/multi/consistency").mkdir(parents=True, exist_ok=True)

# Define metric-specific validation rules
METRIC_RULES = {
    'balance': {
        'min_value': 0,  # Balance should not be negative
        'anomaly_threshold': 3,  # Z-score threshold
        'trend_threshold': 0.5,  # 50% change threshold
        'consistency_threshold': 0.3  # 30% difference between related metrics
    },
    'revenue': {
        'min_value': 0,  # Revenue should not be negative
        'anomaly_threshold': 2.5,  # Lower threshold for revenue anomalies
        'trend_threshold': 0.3,  # 30% change threshold
        'consistency_threshold': 0.1  # 10% difference between related metrics
    },
    'transaction': {
        'min_value': 0,  # Transaction count should not be negative
        'anomaly_threshold': 4,  # Higher threshold for transaction anomalies
        'trend_threshold': 0.7,  # 70% change threshold
        'consistency_threshold': 0.2  # 20% difference between related metrics
    }
}

def load_data():
    # Load metrics definitions
    metrics_df = pd.read_csv('metrics.csv')
    
    # Load company metrics with proper data types
    company_metrics_df = pd.read_csv('company_metrics.csv', 
                                   dtype={
                                       'heron_id': str,
                                       'metric_label': str,
                                       'metric_date_range': str,
                                       'metric_value': float
                                   })
    
    return metrics_df, company_metrics_df

def get_metric_type(metric_name):
    """Determine the type of metric based on its name"""
    metric_name = metric_name.lower()
    if 'balance' in metric_name:
        return 'balance'
    elif 'revenue' in metric_name:
        return 'revenue'
    elif 'transaction' in metric_name:
        return 'transaction'
    return 'default'

def get_metric_rules(metric_name):
    """Get validation rules for a specific metric"""
    metric_type = get_metric_type(metric_name)
    return METRIC_RULES.get(metric_type, {
        'min_value': 0,
        'anomaly_threshold': 3,
        'trend_threshold': 0.5,
        'consistency_threshold': 0.3
    })

def analyze_distribution(metric_data, metric_name, metric_info):
    """Analyze distribution of a single metric across companies with metric-specific rules"""
    rules = get_metric_rules(metric_name)
    
    # Basic statistics
    stats_dict = {
        'count': len(metric_data),
        'mean': metric_data.mean(),
        'median': metric_data.median(),
        'std': metric_data.std(),
        'min': metric_data.min(),
        'max': metric_data.max(),
        'q1': metric_data.quantile(0.25),
        'q3': metric_data.quantile(0.75),
        'iqr': metric_data.quantile(0.75) - metric_data.quantile(0.25)
    }
    
    # Add metric-specific validations
    if metric_data.min() < rules['min_value']:
        stats_dict['warning'] = f"Values below minimum threshold of {rules['min_value']} detected"
    
    # Create distribution plot
    plt.figure(figsize=(10, 6))
    sns.histplot(data=metric_data, kde=True)
    plt.title(f'Distribution of {metric_name} Across Companies')
    plt.xlabel(metric_name)
    plt.ylabel('Frequency')
    plt.axvline(rules['min_value'], color='r', linestyle='--', label='Minimum Threshold')
    plt.legend()
    plt.savefig(f'outputs/multi/distributions/{metric_name}_distribution.png')
    plt.close()
    
    # Create box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=metric_data)
    plt.title(f'Box Plot of {metric_name} Across Companies')
    plt.axhline(rules['min_value'], color='r', linestyle='--', label='Minimum Threshold')
    plt.legend()
    plt.savefig(f'outputs/multi/distributions/{metric_name}_boxplot.png')
    plt.close()
    
    return stats_dict

def detect_anomalies(metric_data, metric_name, threshold=None):
    """Detect anomalies using metric-specific rules"""
    rules = get_metric_rules(metric_name)
    threshold = threshold or rules['anomaly_threshold']
    
    z_scores = np.abs(stats.zscore(metric_data))
    anomalies = metric_data[z_scores > threshold]
    
    if len(anomalies) > 0:
        anomaly_dict = {
            'metric': metric_name,
            'anomaly_count': len(anomalies),
            'anomaly_values': anomalies.tolist(),
            'anomaly_percentage': (len(anomalies) / len(metric_data)) * 100,
            'threshold_used': threshold,
            'metric_type': get_metric_type(metric_name)
        }
        return anomaly_dict
    return None

def analyze_trends(company_metrics_df, metric_name):
    """Analyze trends in metric values over time for each company with metric-specific rules"""
    rules = get_metric_rules(metric_name)
    trend_results = {}
    
    for company_id in company_metrics_df['heron_id'].unique():
        company_data = company_metrics_df[
            (company_metrics_df['heron_id'] == company_id) & 
            (company_metrics_df['metric_label'] == metric_name)
        ]
        
        if len(company_data) > 1:
            # Group by date range and calculate statistics
            trend_data = company_data.groupby('metric_date_range')['metric_value'].agg(['mean', 'std', 'count'])
            
            # Calculate growth rates
            growth_rates = trend_data['mean'].pct_change()
            
            # Identify significant changes
            significant_changes = growth_rates[abs(growth_rates) > rules['trend_threshold']]
            
            # Create trend plot
            plt.figure(figsize=(10, 6))
            trend_data['mean'].plot(kind='line', marker='o')
            plt.title(f'Trend Analysis for {metric_name} - Company {company_id}')
            plt.xlabel('Date Range')
            plt.ylabel('Mean Value')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Add significant change markers
            for date in significant_changes.index:
                plt.axvline(x=date, color='r', linestyle='--', alpha=0.3)
            
            plt.savefig(f'outputs/multi/trends/{metric_name}_company_{company_id}_trend.png')
            plt.close()
            
            trend_results[company_id] = {
                'trend_data': trend_data.to_dict(),
                'significant_changes': significant_changes.to_dict(),
                'threshold_used': rules['trend_threshold']
            }
    
    return trend_results

def analyze_metric_relationships(company_metrics_df, metrics_df):
    """Analyze relationships between related metrics for each company with metric-specific rules"""
    relationships = {}
    
    for company_id in company_metrics_df['heron_id'].unique():
        company_data = company_metrics_df[company_metrics_df['heron_id'] == company_id]
        company_relationships = []
        
        # Balance-related checks
        balance_metrics = company_data[company_data['metric_label'].str.contains('balance', na=False)]
        if len(balance_metrics) > 0:
            rules = get_metric_rules('balance')
            latest_balance = balance_metrics[balance_metrics['metric_label'] == 'latest_balance']['metric_value'].iloc[0]
            min_balance = balance_metrics[balance_metrics['metric_label'] == 'balance_minimum']['metric_value'].iloc[0]
            
            if min_balance < rules['min_value']:
                company_relationships.append({
                    'type': 'warning',
                    'description': 'Negative minimum balance detected',
                    'metrics': ['balance_minimum'],
                    'values': [min_balance],
                    'threshold': rules['min_value']
                })
        
        # Revenue-related checks
        revenue_metrics = company_data[company_data['metric_label'].str.contains('revenue', na=False)]
        if len(revenue_metrics) > 0:
            rules = get_metric_rules('revenue')
            annualized_revenue = revenue_metrics[revenue_metrics['metric_label'] == 'annualized_revenue']['metric_value'].iloc[0]
            revenue = revenue_metrics[revenue_metrics['metric_label'] == 'revenue']['metric_value'].iloc[0]
            
            if annualized_revenue < revenue:
                company_relationships.append({
                    'type': 'warning',
                    'description': 'Annualized revenue is less than total revenue',
                    'metrics': ['annualized_revenue', 'revenue'],
                    'values': [annualized_revenue, revenue],
                    'threshold': rules['consistency_threshold']
                })
        
        if company_relationships:
            relationships[company_id] = company_relationships
    
    return relationships

def analyze_metric_consistency(company_metrics_df, metrics_df):
    """Check for consistency in metric calculations for each company with metric-specific rules"""
    consistency_checks = {}
    
    for company_id in company_metrics_df['heron_id'].unique():
        company_data = company_metrics_df[company_metrics_df['heron_id'] == company_id]
        company_checks = []
        
        # Check balance-related calculations
        balance_metrics = company_data[company_data['metric_label'].str.contains('balance', na=False)]
        if len(balance_metrics) > 0:
            rules = get_metric_rules('balance')
            latest_balance = balance_metrics[balance_metrics['metric_label'] == 'latest_balance']['metric_value'].iloc[0]
            avg_balance = balance_metrics[balance_metrics['metric_label'] == 'balance_average']['metric_value'].iloc[0]
            
            if abs(latest_balance - avg_balance) / avg_balance > rules['consistency_threshold']:
                company_checks.append({
                    'type': 'warning',
                    'description': 'Large difference between latest and average balance',
                    'metrics': ['latest_balance', 'balance_average'],
                    'values': [latest_balance, avg_balance],
                    'threshold': rules['consistency_threshold']
                })
        
        # Check revenue-related calculations
        revenue_metrics = company_data[company_data['metric_label'].str.contains('revenue', na=False)]
        if len(revenue_metrics) > 0:
            rules = get_metric_rules('revenue')
            daily_revenue = revenue_metrics[revenue_metrics['metric_label'] == 'revenue_daily_average']['metric_value'].iloc[0]
            annualized_revenue = revenue_metrics[revenue_metrics['metric_label'] == 'annualized_revenue']['metric_value'].iloc[0]
            
            expected_annualized = daily_revenue * 365
            if abs(annualized_revenue - expected_annualized) / expected_annualized > rules['consistency_threshold']:
                company_checks.append({
                    'type': 'warning',
                    'description': 'Annualized revenue calculation may be inconsistent',
                    'metrics': ['revenue_daily_average', 'annualized_revenue'],
                    'values': [daily_revenue, annualized_revenue],
                    'expected': expected_annualized,
                    'threshold': rules['consistency_threshold']
                })
        
        if company_checks:
            consistency_checks[company_id] = company_checks
    
    return consistency_checks

def analyze_company_metrics(company_metrics_df, metrics_df):
    """Analyze metrics for each company with metric-specific rules"""
    company_analysis = {}
    
    for company_id in company_metrics_df['heron_id'].unique():
        company_data = company_metrics_df[company_metrics_df['heron_id'] == company_id]
        
        # Calculate basic statistics for each metric
        company_stats = {}
        for metric in company_data['metric_label'].unique():
            metric_data = company_data[company_data['metric_label'] == metric]['metric_value']
            if len(metric_data) > 0:
                rules = get_metric_rules(metric)
                company_stats[metric] = {
                    'count': len(metric_data),
                    'mean': metric_data.mean(),
                    'min': metric_data.min(),
                    'max': metric_data.max(),
                    'metric_type': get_metric_type(metric),
                    'min_threshold': rules['min_value'],
                    'anomaly_threshold': rules['anomaly_threshold'],
                    'trend_threshold': rules['trend_threshold'],
                    'consistency_threshold': rules['consistency_threshold']
                }
        
        company_analysis[company_id] = company_stats
    
    return company_analysis

def main():
    # Load data
    metrics_df, company_metrics_df = load_data()
    
    # Initialize results storage
    distribution_results = {}
    anomaly_results = []
    trend_results = {}
    relationship_results = {}
    consistency_results = {}
    company_results = {}
    
    # Process each metric
    for _, metric_info in metrics_df.iterrows():
        metric_name = metric_info['metric_label']
        metric_data = company_metrics_df[company_metrics_df['metric_label'] == metric_name]['metric_value']
        
        if len(metric_data) > 0:
            # Analyze distribution
            dist_stats = analyze_distribution(metric_data, metric_name, metric_info)
            distribution_results[metric_name] = dist_stats
            
            # Detect anomalies
            anomalies = detect_anomalies(metric_data, metric_name)
            if anomalies:
                anomaly_results.append(anomalies)
            
            # Analyze trends
            trends = analyze_trends(company_metrics_df, metric_name)
            if trends:
                trend_results[metric_name] = trends
    
    # Analyze relationships and consistency
    relationship_results = analyze_metric_relationships(company_metrics_df, metrics_df)
    consistency_results = analyze_metric_consistency(company_metrics_df, metrics_df)
    
    # Analyze metrics for each company
    company_results = analyze_company_metrics(company_metrics_df, metrics_df)
    
    # Save results
    with open('outputs/multi/distribution_analysis.json', 'w') as f:
        json.dump(distribution_results, f, indent=2)
    
    with open('outputs/multi/anomaly_detection.json', 'w') as f:
        json.dump(anomaly_results, f, indent=2)
    
    with open('outputs/multi/trend_analysis.json', 'w') as f:
        json.dump(trend_results, f, indent=2)
    
    with open('outputs/multi/relationship_analysis.json', 'w') as f:
        json.dump(relationship_results, f, indent=2)
    
    with open('outputs/multi/consistency_analysis.json', 'w') as f:
        json.dump(consistency_results, f, indent=2)
    
    with open('outputs/multi/company_analysis.json', 'w') as f:
        json.dump(company_results, f, indent=2)
    
    # Generate summary
    summary = {
        'total_companies': len(company_metrics_df['heron_id'].unique()),
        'total_metrics': len(metrics_df),
        'metrics_with_anomalies': len(anomaly_results),
        'total_anomalies': sum(a['anomaly_count'] for a in anomaly_results),
        'companies_with_warnings': len(relationship_results) + len(consistency_results),
        'total_warnings': sum(len(w) for w in relationship_results.values()) + 
                         sum(len(w) for w in consistency_results.values()),
        'metric_types': {
            metric_type: len([m for m in metrics_df['metric_label'] if get_metric_type(m) == metric_type])
            for metric_type in METRIC_RULES.keys()
        }
    }
    
    with open('outputs/multi/summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main() 