import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
from pathlib import Path

class MetricValidatorBase:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_data(self):
        """Load the metrics data"""
        self.metrics_df = pd.read_csv('metrics.csv')
        self.company_metrics_df = pd.read_csv('company_metrics.csv', 
                                            dtype={
                                                'heron_id': str,
                                                'metric_label': str,
                                                'metric_date_range': str,
                                                'metric_value': float
                                            })
    
    def get_metric_data(self, metric_name):
        """Get data for a specific metric"""
        return self.company_metrics_df[self.company_metrics_df['metric_label'] == metric_name]
    
    def check_data_quality(self, metric_data, metric_name):
        """Check for data quality issues"""
        quality_checks = []
        
        # Check for missing data
        missing_count = metric_data['metric_value'].isna().sum()
        if missing_count > 0:
            quality_checks.append({
                'type': 'error',
                'description': f'Found {missing_count} missing values',
                'metric': metric_name
            })
        
        # Check for zero values where they might be suspicious
        zero_count = (metric_data['metric_value'] == 0).sum()
        if zero_count > 0:
            # For certain metrics, zero values might be suspicious
            suspicious_zero_metrics = [
                'revenue', 'revenue_daily_average', 'revenue_monthly_average',
                'balance_average', 'balance_minimum', 'latest_balance',
                'inflow_daily_average', 'outflow_daily_average'
            ]
            if metric_name in suspicious_zero_metrics:
                quality_checks.append({
                    'type': 'warning',
                    'description': f'Found {zero_count} zero values which might be suspicious for this metric',
                    'metric': metric_name
                })
        
        # Check for negative values where they shouldn't exist
        negative_metrics = ['revenue', 'revenue_daily_average', 'revenue_monthly_average',
                          'balance_average', 'balance_minimum', 'latest_balance']
        if metric_name in negative_metrics:
            negative_count = (metric_data['metric_value'] < 0).sum()
            if negative_count > 0:
                quality_checks.append({
                    'type': 'error',
                    'description': f'Found {negative_count} negative values which are not expected for this metric',
                    'metric': metric_name
                })
        
        # Check for data completeness
        expected_companies = self.company_metrics_df['heron_id'].nunique()
        actual_companies = metric_data['heron_id'].nunique()
        if actual_companies < expected_companies:
            quality_checks.append({
                'type': 'warning',
                'description': f'Data missing for {expected_companies - actual_companies} companies',
                'metric': metric_name
            })
        
        # Check for extreme values
        q1 = metric_data['metric_value'].quantile(0.25)
        q3 = metric_data['metric_value'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 3 * iqr
        upper_bound = q3 + 3 * iqr
        
        extreme_values = metric_data[
            (metric_data['metric_value'] < lower_bound) | 
            (metric_data['metric_value'] > upper_bound)
        ]
        
        if len(extreme_values) > 0:
            quality_checks.append({
                'type': 'warning',
                'description': f'Found {len(extreme_values)} extreme values outside the expected range',
                'metric': metric_name,
                'range': [lower_bound, upper_bound]
            })
        
        return quality_checks
    
    def analyze_distribution(self, metric_data, metric_name):
        """Base distribution analysis"""
        stats_dict = {
            'count': len(metric_data),
            'mean': metric_data['metric_value'].mean(),
            'median': metric_data['metric_value'].median(),
            'std': metric_data['metric_value'].std(),
            'min': metric_data['metric_value'].min(),
            'max': metric_data['metric_value'].max(),
            'q1': metric_data['metric_value'].quantile(0.25),
            'q3': metric_data['metric_value'].quantile(0.75),
            'iqr': metric_data['metric_value'].quantile(0.75) - metric_data['metric_value'].quantile(0.25)
        }
        
        # Create distribution plot
        plt.figure(figsize=(10, 6))
        sns.histplot(data=metric_data['metric_value'], kde=True)
        plt.title(f'Distribution of {metric_name}')
        plt.xlabel(metric_name)
        plt.ylabel('Frequency')
        plt.savefig(self.output_dir / f'{metric_name}_distribution.png')
        plt.close()
        
        return stats_dict
    
    def detect_anomalies(self, metric_data, metric_name, threshold=3):
        """Base anomaly detection"""
        z_scores = np.abs(stats.zscore(metric_data['metric_value']))
        anomalies = metric_data[z_scores > threshold]
        
        if len(anomalies) > 0:
            return {
                'metric': metric_name,
                'anomaly_count': len(anomalies),
                'anomaly_values': anomalies['metric_value'].tolist(),
                'anomaly_percentage': (len(anomalies) / len(metric_data)) * 100
            }
        return None
    
    def analyze_trends(self, metric_data, metric_name):
        """Base trend analysis"""
        trend_results = {}
        
        for company_id in metric_data['heron_id'].unique():
            company_data = metric_data[metric_data['heron_id'] == company_id]
            
            if len(company_data) > 1:
                trend_data = company_data.groupby('metric_date_range')['metric_value'].agg(['mean', 'std', 'count'])
                
                plt.figure(figsize=(10, 6))
                trend_data['mean'].plot(kind='line', marker='o')
                plt.title(f'Trend Analysis for {metric_name} - Company {company_id}')
                plt.xlabel('Date Range')
                plt.ylabel('Mean Value')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(self.output_dir / f'{metric_name}_company_{company_id}_trend.png')
                plt.close()
                
                trend_results[company_id] = trend_data.to_dict()
        
        return trend_results
    
    def save_results(self, results, filename):
        """Save results to JSON file"""
        with open(self.output_dir / filename, 'w') as f:
            json.dump(results, f, indent=2)
    
    def validate(self):
        """Base validation method to be overridden by specific validators"""
        raise NotImplementedError("Each metric validator must implement its own validation logic") 