from metric_validator_base import MetricValidatorBase
import pandas as pd
import numpy as np

class BalanceValidator(MetricValidatorBase):
    def __init__(self):
        super().__init__('outputs/balance')
        self.balance_metrics = [
            'inflow_growth_rate',
            'inflow_daily_average',
            'outflow_daily_average',
            'latest_balance',
            'balance_minimum',
            'balance_average',
            'change_in_balance',
            'weekday_balance_average',
            'weekday_with_highest_avg',
            'weekday_with_lowest_avg'
        ]
        
    def validate_balance_consistency(self, company_data):
        """Check consistency between different balance metrics"""
        consistency_checks = []
        
        # Check if minimum balance is less than latest balance
        if 'balance_minimum' in company_data and 'latest_balance' in company_data:
            min_balance = company_data['balance_minimum'].iloc[0]
            latest_balance = company_data['latest_balance'].iloc[0]
            if min_balance > latest_balance:
                consistency_checks.append({
                    'type': 'warning',
                    'description': 'Minimum balance is greater than latest balance',
                    'metrics': ['balance_minimum', 'latest_balance'],
                    'values': [min_balance, latest_balance]
                })
        
        # Check if average balance is between min and latest
        if all(metric in company_data for metric in ['balance_average', 'balance_minimum', 'latest_balance']):
            avg_balance = company_data['balance_average'].iloc[0]
            min_balance = company_data['balance_minimum'].iloc[0]
            latest_balance = company_data['latest_balance'].iloc[0]
            if not (min_balance <= avg_balance <= latest_balance):
                consistency_checks.append({
                    'type': 'warning',
                    'description': 'Average balance is not between minimum and latest balance',
                    'metrics': ['balance_minimum', 'balance_average', 'latest_balance'],
                    'values': [min_balance, avg_balance, latest_balance]
                })
        
        return consistency_checks
    
    def validate_balance_trends(self, company_data):
        """Check for significant changes in balance metrics"""
        trend_checks = []
        
        # Check inflow growth rate
        if 'inflow_growth_rate' in company_data:
            growth_rate = company_data['inflow_growth_rate'].iloc[0]
            if abs(growth_rate) > 0.5:  # 50% change threshold
                trend_checks.append({
                    'type': 'warning',
                    'description': 'Significant inflow growth rate detected',
                    'metric': 'inflow_growth_rate',
                    'value': growth_rate
                })
        
        # Check change in balance
        if 'change_in_balance' in company_data:
            change = company_data['change_in_balance'].iloc[0]
            if abs(change) > 1000:  # Example threshold
                trend_checks.append({
                    'type': 'warning',
                    'description': 'Large change in balance detected',
                    'metric': 'change_in_balance',
                    'value': change
                })
        
        return trend_checks
    
    def validate(self):
        """Main validation method for balance metrics"""
        self.load_data()
        
        results = {
            'distribution_analysis': {},
            'anomaly_detection': [],
            'consistency_checks': {},
            'trend_analysis': {},
            'data_quality_checks': {}
        }
        
        for metric in self.balance_metrics:
            metric_data = self.get_metric_data(metric)
            if len(metric_data) > 0:
                # Data quality checks
                quality_checks = self.check_data_quality(metric_data, metric)
                if quality_checks:
                    results['data_quality_checks'][metric] = quality_checks
                
                # Distribution analysis
                dist_stats = self.analyze_distribution(metric_data, metric)
                results['distribution_analysis'][metric] = dist_stats
                
                # Anomaly detection
                anomalies = self.detect_anomalies(metric_data, metric)
                if anomalies:
                    results['anomaly_detection'].append(anomalies)
                
                # Trend analysis
                trends = self.analyze_trends(metric_data, metric)
                if trends:
                    results['trend_analysis'][metric] = trends
        
        # Company-specific checks
        for company_id in self.company_metrics_df['heron_id'].unique():
            company_data = self.company_metrics_df[self.company_metrics_df['heron_id'] == company_id]
            
            # Consistency checks
            consistency_checks = self.validate_balance_consistency(company_data)
            if consistency_checks:
                results['consistency_checks'][company_id] = consistency_checks
            
            # Trend checks
            trend_checks = self.validate_balance_trends(company_data)
            if trend_checks:
                if company_id not in results['trend_analysis']:
                    results['trend_analysis'][company_id] = {}
                results['trend_analysis'][company_id]['balance_trends'] = trend_checks
        
        # Save results
        self.save_results(results, 'balance_analysis.json')
        
        return results 