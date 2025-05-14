from metric_validator_base import MetricValidatorBase
import pandas as pd
import numpy as np

class RevenueValidator(MetricValidatorBase):
    def __init__(self):
        super().__init__('outputs/revenue')
        self.revenue_metrics = [
            'revenue_daily_average',
            'revenue',
            'annualized_revenue',
            'revenue_sources',
            'revenue_monthly_average',
            'revenue_growth_rate',
            'revenue_profit_and_loss',
            'annualized_revenue_profit_and_loss'
        ]
        
    def validate_revenue_consistency(self, company_data):
        """Check consistency between different revenue metrics"""
        consistency_checks = []
        
        # Check if annualized revenue matches daily average * 365
        if all(metric in company_data for metric in ['revenue_daily_average', 'annualized_revenue']):
            daily_revenue = company_data['revenue_daily_average'].iloc[0]
            annualized_revenue = company_data['annualized_revenue'].iloc[0]
            expected_annualized = daily_revenue * 365
            
            if abs(annualized_revenue - expected_annualized) / expected_annualized > 0.1:  # 10% threshold
                consistency_checks.append({
                    'type': 'warning',
                    'description': 'Annualized revenue calculation may be inconsistent',
                    'metrics': ['revenue_daily_average', 'annualized_revenue'],
                    'values': [daily_revenue, annualized_revenue],
                    'expected': expected_annualized
                })
        
        # Check if revenue matches P&L revenue
        if all(metric in company_data for metric in ['revenue', 'revenue_profit_and_loss']):
            revenue = company_data['revenue'].iloc[0]
            pnl_revenue = company_data['revenue_profit_and_loss'].iloc[0]
            
            if abs(revenue - pnl_revenue) / revenue > 0.05:  # 5% threshold
                consistency_checks.append({
                    'type': 'warning',
                    'description': 'Revenue values from different sources do not match',
                    'metrics': ['revenue', 'revenue_profit_and_loss'],
                    'values': [revenue, pnl_revenue]
                })
        
        return consistency_checks
    
    def validate_revenue_trends(self, company_data):
        """Check for significant changes in revenue metrics"""
        trend_checks = []
        
        # Check revenue growth rate
        if 'revenue_growth_rate' in company_data:
            growth_rate = company_data['revenue_growth_rate'].iloc[0]
            if abs(growth_rate) > 0.3:  # 30% change threshold
                trend_checks.append({
                    'type': 'warning',
                    'description': 'Significant revenue growth rate detected',
                    'metric': 'revenue_growth_rate',
                    'value': growth_rate
                })
        
        # Check monthly vs daily averages
        if all(metric in company_data for metric in ['revenue_monthly_average', 'revenue_daily_average']):
            monthly_avg = company_data['revenue_monthly_average'].iloc[0]
            daily_avg = company_data['revenue_daily_average'].iloc[0]
            expected_monthly = daily_avg * 30  # Approximate
            
            if abs(monthly_avg - expected_monthly) / expected_monthly > 0.2:  # 20% threshold
                trend_checks.append({
                    'type': 'warning',
                    'description': 'Monthly average revenue does not align with daily average',
                    'metrics': ['revenue_monthly_average', 'revenue_daily_average'],
                    'values': [monthly_avg, daily_avg],
                    'expected': expected_monthly
                })
        
        return trend_checks
    
    def validate(self):
        """Main validation method for revenue metrics"""
        self.load_data()
        
        results = {
            'distribution_analysis': {},
            'anomaly_detection': [],
            'consistency_checks': {},
            'trend_analysis': {},
            'data_quality_checks': {}
        }
        
        for metric in self.revenue_metrics:
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
            consistency_checks = self.validate_revenue_consistency(company_data)
            if consistency_checks:
                results['consistency_checks'][company_id] = consistency_checks
            
            # Trend checks
            trend_checks = self.validate_revenue_trends(company_data)
            if trend_checks:
                if company_id not in results['trend_analysis']:
                    results['trend_analysis'][company_id] = {}
                results['trend_analysis'][company_id]['revenue_trends'] = trend_checks
        
        # Save results
        self.save_results(results, 'revenue_analysis.json')
        
        return results 