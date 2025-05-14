from metric_validator_base import MetricValidatorBase
import pandas as pd
import numpy as np

class RiskValidator(MetricValidatorBase):
    def __init__(self):
        super().__init__('outputs/risk')
        self.risk_metrics = [
            'deposit_days',
            'nsf_fees',
            'nsf_days',
            'debt_collection',
            'atm_withdrawals',
            'tax_payments',
            'tax_payment_amount',
            'negative_balance_days',
            'negative_balance_days_by_account'
        ]
        
    def validate_risk_consistency(self, company_data):
        """Check consistency between different risk metrics"""
        consistency_checks = []
        
        # Check if NSF days match NSF fees
        if all(metric in company_data for metric in ['nsf_days', 'nsf_fees']):
            nsf_days = company_data['nsf_days'].iloc[0]
            nsf_fees = company_data['nsf_fees'].iloc[0]
            
            if nsf_days > nsf_fees:
                consistency_checks.append({
                    'type': 'warning',
                    'description': 'Number of NSF days exceeds number of NSF fees',
                    'metrics': ['nsf_days', 'nsf_fees'],
                    'values': [nsf_days, nsf_fees]
                })
        
        # Check if negative balance days match by account
        if all(metric in company_data for metric in ['negative_balance_days', 'negative_balance_days_by_account']):
            total_days = company_data['negative_balance_days'].iloc[0]
            account_days = company_data['negative_balance_days_by_account'].iloc[0]
            
            if account_days < total_days:
                consistency_checks.append({
                    'type': 'warning',
                    'description': 'Account-specific negative balance days less than total negative balance days',
                    'metrics': ['negative_balance_days', 'negative_balance_days_by_account'],
                    'values': [total_days, account_days]
                })
        
        return consistency_checks
    
    def validate_risk_trends(self, company_data):
        """Check for significant changes in risk metrics"""
        trend_checks = []
        
        # Check NSF frequency
        if all(metric in company_data for metric in ['nsf_days', 'deposit_days']):
            nsf_days = company_data['nsf_days'].iloc[0]
            deposit_days = company_data['deposit_days'].iloc[0]
            
            if deposit_days > 0:
                nsf_ratio = nsf_days / deposit_days
                if nsf_ratio > 0.1:  # 10% threshold
                    trend_checks.append({
                        'type': 'warning',
                        'description': 'High frequency of NSF occurrences',
                        'metrics': ['nsf_days', 'deposit_days'],
                        'values': [nsf_days, deposit_days],
                        'ratio': nsf_ratio
                    })
        
        # Check negative balance frequency
        if 'negative_balance_days' in company_data:
            negative_days = company_data['negative_balance_days'].iloc[0]
            if negative_days > 5:  # Threshold of 5 days
                trend_checks.append({
                    'type': 'warning',
                    'description': 'High number of negative balance days',
                    'metric': 'negative_balance_days',
                    'value': negative_days
                })
        
        return trend_checks
    
    def validate(self):
        """Main validation method for risk metrics"""
        self.load_data()
        
        results = {
            'distribution_analysis': {},
            'anomaly_detection': [],
            'consistency_checks': {},
            'trend_analysis': {},
            'data_quality_checks': {}
        }
        
        for metric in self.risk_metrics:
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
            consistency_checks = self.validate_risk_consistency(company_data)
            if consistency_checks:
                results['consistency_checks'][company_id] = consistency_checks
            
            # Trend checks
            trend_checks = self.validate_risk_trends(company_data)
            if trend_checks:
                if company_id not in results['trend_analysis']:
                    results['trend_analysis'][company_id] = {}
                results['trend_analysis'][company_id]['risk_trends'] = trend_checks
        
        # Save results
        self.save_results(results, 'risk_analysis.json')
        
        return results 