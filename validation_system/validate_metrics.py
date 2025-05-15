import pandas as pd
import json
import logging
from pathlib import Path
from validators.metric_validator import MetricValidator
from validators.base_validator import ValidationSeverity
import argparse
import time
from collections import defaultdict
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define fixed output locations
OUTPUT_DIR = Path(__file__).parent / "validation_results"
OUTPUT_CSV = OUTPUT_DIR / "company_metrics_validated.csv"
OUTPUT_SUMMARY_JSON = OUTPUT_DIR / "validation_summary.json"

def load_company_metrics(file_path: str) -> dict:
    """Load company metrics from CSV file for company-level validation"""
    df = pd.read_csv(file_path)
    metrics_dict = {}
    for _, row in df.iterrows():
        company_id = row['heron_id']
        if company_id not in metrics_dict:
            metrics_dict[company_id] = {}
        metric_name = row['metric_label']
        metric_value = row['metric_value']
        # Convert string values to appropriate types
        if pd.isna(metric_value):
            value = None
        else:
            value = metric_value
            if isinstance(value, str):
                try:
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                except ValueError:
                    pass
        metrics_dict[company_id][metric_name] = value
    return metrics_dict

def check_companies_metric_completeness(metrics_data: dict) -> dict:
    """Check if each company has all required metrics defined in the rules"""
    validator = MetricValidator()
    required_metrics = set()
    
    # Collect all metric names from the rules
    for group_rules in validator.metric_rules.rules.values():
        for rule in group_rules:
            required_metrics.add(rule.metric_name)
    
    # Check each company for missing metrics
    completeness_results = {}
    for company_id, company_metrics in metrics_data.items():
        company_metrics_set = set(company_metrics.keys())
        missing_metrics = required_metrics - company_metrics_set
        
        # Group missing metrics by category
        missing_by_group = defaultdict(list)
        for metric in missing_metrics:
            for group, rules in validator.metric_rules.rules.items():
                if any(rule.metric_name == metric for rule in rules):
                    missing_by_group[group].append(metric)
                    break
        
        completeness_results[company_id] = {
            'has_all_metrics': len(missing_metrics) == 0,
            'missing_count': len(missing_metrics),
            'missing_metrics': list(missing_metrics),
            'missing_by_group': dict(missing_by_group),
            'total_metrics': len(company_metrics_set),
            'coverage_percentage': (len(company_metrics_set) / len(required_metrics)) * 100 if required_metrics else 100
        }
    
    # Calculate summary statistics
    total_companies = len(completeness_results)
    companies_with_missing = sum(1 for r in completeness_results.values() if not r['has_all_metrics'])
    all_missing_metrics = set()
    for result in completeness_results.values():
        all_missing_metrics.update(result['missing_metrics'])
    
    # Count how many companies are missing each metric
    metric_missing_counts = defaultdict(int)
    for result in completeness_results.values():
        for metric in result['missing_metrics']:
            metric_missing_counts[metric] += 1
    
    summary = {
        'total_companies': total_companies,
        'companies_with_missing_metrics': companies_with_missing,
        'companies_with_all_metrics': total_companies - companies_with_missing,
        'percent_complete': ((total_companies - companies_with_missing) / total_companies) * 100 if total_companies else 0,
        'unique_missing_metrics': len(all_missing_metrics),
        'most_frequently_missing': dict(sorted(metric_missing_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    }
    
    return completeness_results, summary

def get_metric_group(metric_name, validator):
    """Get the group a metric belongs to"""
    for group_name, rules in validator.metric_rules.rules.items():
        if any(rule.metric_name == metric_name for rule in rules):
            return group_name
    return None

def validate_metrics(input_csv: str, output_csv: str, output_summary: str):
    """Validate all metrics and produce a comprehensive CSV file and summary JSON"""
    start_time = time.time()
    validator = MetricValidator()
    
    # Read the input CSV
    df = pd.read_csv(input_csv)
    
    # Get the metrics dictionary for completeness checking
    metrics_data = load_company_metrics(input_csv)
    
    # Check for metric completeness
    completeness_results, completeness_summary = check_companies_metric_completeness(metrics_data)
    
    # Prepare additional columns for the output
    validation_passed = []
    validation_message = []
    expected_min = []
    expected_max = []
    severity = []
    metric_group = []
    missing_metric = []
    company_has_all_metrics = []
    
    # Initialize statistics collectors
    metric_stats = defaultdict(lambda: {
        'total_validations': 0,
        'success_count': 0,
        'error_count': 0,
        'severity_counts': defaultdict(int),
        'values': [],
        'group': None
    })
    
    group_stats = defaultdict(lambda: {
        'total_validations': 0,
        'success_count': 0,
        'error_count': 0,
        'metrics': set()
    })
    
    # Add validation results to each row
    for idx, row in df.iterrows():
        company_id = row['heron_id']
        metric_name = row['metric_label']
        metric_value = row['metric_value']
        
        # Get metric group
        group = get_metric_group(metric_name, validator)
        metric_group.append(group)
        
        # Add company completeness info
        if company_id in completeness_results:
            is_missing = metric_name in completeness_results[company_id]['missing_metrics']
            missing_metric.append(is_missing)
            company_has_all_metrics.append(completeness_results[company_id]['has_all_metrics'])
        else:
            missing_metric.append(False)
            company_has_all_metrics.append(True)
        
        # Convert to proper type for validation
        if pd.isna(metric_value):
            value = None
        else:
            value = metric_value
            if isinstance(value, str):
                try:
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                except ValueError:
                    pass
        
        # Validate the metric
        result = validator.validate(value, metric_name)
        validation_passed.append(result.is_valid)
        validation_message.append(result.message)
        
        # Extract expected range
        if result.expected_range and len(result.expected_range) == 2:
            expected_min.append(result.expected_range[0])
            expected_max.append(result.expected_range[1])
        else:
            expected_min.append(None)
            expected_max.append(None)
        
        severity.append(result.severity.value)
        
        # Update metric statistics
        metric_stats[metric_name]['total_validations'] += 1
        metric_stats[metric_name]['success_count'] += int(result.is_valid)
        metric_stats[metric_name]['error_count'] += int(not result.is_valid)
        metric_stats[metric_name]['severity_counts'][result.severity.value] += 1
        if result.value is not None:
            metric_stats[metric_name]['values'].append(result.value)
        metric_stats[metric_name]['group'] = group
        
        # Update group statistics
        if group:
            group_stats[group]['total_validations'] += 1
            group_stats[group]['success_count'] += int(result.is_valid)
            group_stats[group]['error_count'] += int(not result.is_valid)
            group_stats[group]['metrics'].add(metric_name)
    
    # Add columns to the DataFrame
    df['validation_passed'] = validation_passed
    df['validation_message'] = validation_message
    df['expected_min'] = expected_min
    df['expected_max'] = expected_max
    df['severity'] = severity
    df['metric_group'] = metric_group
    df['is_missing'] = missing_metric
    df['company_has_all_metrics'] = company_has_all_metrics
    
    # Process metric statistics
    for metric, stats in metric_stats.items():
        stats['success_rate'] = stats['success_count'] / stats['total_validations'] if stats['total_validations'] > 0 else 0
        if stats['values']:
            stats['value_stats'] = {
                'min': float(np.min(stats['values'])),
                'max': float(np.max(stats['values'])),
                'mean': float(np.mean(stats['values'])),
                'median': float(np.median(stats['values'])),
                'std': float(np.std(stats['values']))
            }
        else:
            stats['value_stats'] = None
        del stats['values']  # Remove raw values to keep JSON size manageable
    
    # Process group statistics
    for group, stats in group_stats.items():
        stats['success_rate'] = stats['success_count'] / stats['total_validations'] if stats['total_validations'] > 0 else 0
        stats['metrics'] = list(stats['metrics'])
    
    # Calculate validation statistics
    execution_time = time.time() - start_time
    total_companies = len(metrics_data)
    
    # Count companies with validation errors
    companies_with_errors = 0
    for company_id in metrics_data:
        company_df = df[df['heron_id'] == company_id]
        non_missing_metrics = company_df[~company_df['is_missing']]
        if not non_missing_metrics.empty and (non_missing_metrics['validation_passed'] == False).any():
            companies_with_errors += 1
    
    companies_missing_metrics = sum(1 for company_id in completeness_results if not completeness_results[company_id]['has_all_metrics'])
    total_metrics_validated = len(df)
    total_errors = sum(1 for passed in validation_passed if not passed)
    
    # Generate comprehensive summary
    summary = {
        'execution_info': {
            'total_companies': total_companies,
            'companies_with_errors': companies_with_errors,
            'companies_missing_metrics': companies_missing_metrics,
            'total_metrics_validated': total_metrics_validated,
            'total_errors': total_errors,
            'execution_time_seconds': execution_time
        },
        'error_distribution': {
            metric: count for metric, count in sorted(
                {m: s['error_count'] for m, s in metric_stats.items()}.items(),
                key=lambda x: x[1],
                reverse=True
            )
        },
        'severity_distribution': {
            severity: sum(s['severity_counts'].get(severity, 0) for s in metric_stats.values())
            for severity in ValidationSeverity.__members__
        },
        'metric_statistics': dict(metric_stats),
        'group_statistics': dict(group_stats),
        'completeness_summary': completeness_summary
    }
    
    # Ensure output directories exist
    Path(output_csv).parent.mkdir(exist_ok=True)
    
    # Save the validated DataFrame as CSV
    df.to_csv(output_csv, index=False)
    
    # Save summary as JSON
    with open(output_summary, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Log summary information
    logger.info(f"Validation results saved to:")
    logger.info(f"- CSV: {output_csv}")
    logger.info(f"- Summary JSON: {output_summary}")
    logger.info(f"Total companies validated: {total_companies}")
    logger.info(f"Companies with validation errors: {companies_with_errors}")
    logger.info(f"Companies missing metrics: {companies_missing_metrics}")
    logger.info(f"Total metrics validated: {total_metrics_validated}")
    logger.info(f"Total validation errors: {total_errors}")
    logger.info(f"Execution time: {execution_time:.2f} seconds")
    
    # Log missing metrics information
    if completeness_summary['most_frequently_missing']:
        logger.info("\nMost frequently missing metrics:")
        for metric, count in list(completeness_summary['most_frequently_missing'].items())[:5]:
            logger.info(f"- {metric}: missing in {count} companies")
    
    if summary['error_distribution']:
        logger.info("\nTop metrics with most errors:")
        for metric, count in list(summary['error_distribution'].items())[:5]:
            if count > 0:
                logger.info(f"- {metric}: {count} errors")

def main():
    parser = argparse.ArgumentParser(description="Validate company metrics.")
    parser.add_argument('--input', default='company_metrics.csv', help='Input CSV file')
    args = parser.parse_args()
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Validate metrics and generate CSV + summary JSON
    validate_metrics(args.input, str(OUTPUT_CSV), str(OUTPUT_SUMMARY_JSON))
    
    logger.info(f"Validation complete.")

if __name__ == "__main__":
    main() 