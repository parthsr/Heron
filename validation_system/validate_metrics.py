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
        metric_name = row['metric_label']
        metric_value = row['metric_value']
        metric_date_range = row.get('metric_date_range', 'None')  # Use a default string for missing date range
        
        if company_id not in metrics_dict:
            metrics_dict[company_id] = {}
        
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
        
        # Store value under a key that includes both metric name and date range
        # Using a tuple (metric_name, date_range) as the key
        metric_key = (metric_name, metric_date_range)
        metrics_dict[company_id][metric_key] = value

    return metrics_dict

def check_companies_metric_completeness(metrics_data: dict) -> dict:
    """Check if each company has all required metrics defined in the rules, considering time ranges."""
    
    # Collect all unique (metric_name, date_range) combinations across all companies
    all_metric_time_ranges = set()
    for company_metrics in metrics_data.values():
        for metric_key in company_metrics.keys():
            all_metric_time_ranges.add(metric_key)
    
    # Check each company for missing metric-time range combinations
    completeness_results = {}
    for company_id, company_metrics in metrics_data.items():
        company_metric_time_ranges = set(company_metrics.keys())
        missing_metric_time_ranges = all_metric_time_ranges - company_metric_time_ranges
        
        # Group missing combinations by metric name
        missing_by_metric = defaultdict(list)
        for metric_name, date_range in missing_metric_time_ranges:
             missing_by_metric[metric_name].append(date_range)
        
        # Calculate the number of unique metric names for the company
        unique_metric_names = set()
        for metric_name, date_range in company_metrics.keys():
            unique_metric_names.add(metric_name)
        
        completeness_results[company_id] = {
            'has_all_metric_time_ranges': len(missing_metric_time_ranges) == 0,
            'missing_count': len(missing_metric_time_ranges),
            'missing_metric_time_ranges': sorted(list(missing_metric_time_ranges)), # Sort for consistent output
            'missing_by_metric': dict(missing_by_metric),
            'total_metric_time_ranges': len(company_metric_time_ranges),
            'coverage_percentage': (len(company_metric_time_ranges) / len(all_metric_time_ranges)) * 100 if all_metric_time_ranges else 100,
            'total_unique_metrics': len(unique_metric_names) # Add total unique metrics
        }
    
    # Calculate summary statistics
    total_companies = len(completeness_results)
    companies_with_missing = sum(1 for r in completeness_results.values() if not r['has_all_metric_time_ranges'])
    all_missing_combinations = set()
    for result in completeness_results.values():
        all_missing_combinations.update(result['missing_metric_time_ranges'])
    
    # Count how many companies are missing each combination
    combination_missing_counts = defaultdict(int)
    for result in completeness_results.values():
        for combination in result['missing_metric_time_ranges']:
            combination_missing_counts[combination] += 1
    
    summary = {
        'total_companies': total_companies,
        'companies_with_missing_metric_time_ranges': companies_with_missing,
        'companies_with_all_metric_time_ranges': total_companies - companies_with_missing,
        'percent_complete_combinations': ((total_companies - companies_with_missing) / total_companies) * 100 if total_companies else 0,
        'unique_missing_combinations': len(all_missing_combinations),
        'most_frequently_missing_combinations': dict(sorted(combination_missing_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    }
    
    return completeness_results, summary

def get_metric_group(metric_name, validator):
    """Get the group a metric belongs to"""
    for group_name, rules in validator.metric_rules.rules.items():
        if any(rule.metric_name == metric_name for rule in rules):
            return group_name
    return None

def validate_metrics(input_csv: str, output_csv: str, output_summary: str):
    """Validate all metrics and produce a comprehensive CSV file and summary JSON, considering time ranges."""
    start_time = time.time()
    validator = MetricValidator()

    # Read the input CSV
    df = pd.read_csv(input_csv)

    # Get the metrics dictionary for completeness checking (keys are now (metric_name, date_range))
    metrics_data = load_company_metrics(input_csv)

    # Check for metric completeness including time ranges
    completeness_results, completeness_summary = check_companies_metric_completeness(metrics_data)

    # Prepare additional columns for the output
    validation_passed = []
    validation_message = []
    expected_min = []
    expected_max = []
    severity = []
    metric_group = []
    is_missing_combination = [] # Renamed to reflect checking combinations
    company_has_all_combinations = [] # Renamed to reflect checking combinations

    # Initialize statistics collectors
    # Stats will be per (metric_name, date_range) combination
    combination_stats = defaultdict(lambda: {
        'total_validations': 0,
        'success_count': 0,
        'error_count': 0,
        'severity_counts': defaultdict(int),
        'values': [],
        'metric_name': None,
        'date_range': None,
        'group': None
    })

    # Process each row from the original DataFrame to add validation results and stats
    for idx, row in df.iterrows():
        company_id = row['heron_id']
        metric_name = row['metric_label']
        metric_value = row['metric_value']
        metric_date_range = row.get('metric_date_range', 'None')

        # Form the key for the metric-time range combination
        metric_key = (metric_name, metric_date_range)

        # Get metric group for the base metric name
        group = get_metric_group(metric_name, validator)
        metric_group.append(group)

        # Add company completeness info for this specific combination
        if company_id in completeness_results:
            # Check if this specific combination is missing for this company
            is_missing = metric_key in completeness_results[company_id]['missing_metric_time_ranges']
            is_missing_combination.append(is_missing)
            company_has_all_combinations.append(completeness_results[company_id]['has_all_metric_time_ranges'])
        else:
            # Should not happen if company was processed by load_company_metrics
            is_missing_combination.append(False)
            company_has_all_combinations.append(True)

        # Convert to proper type for validation (using the value from the row directly)
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

        # Validate the metric (using the base metric name and value)
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

        # Update combination statistics
        combination_stats[metric_key]['total_validations'] += 1
        combination_stats[metric_key]['success_count'] += int(result.is_valid)
        combination_stats[metric_key]['error_count'] += int(not result.is_valid)
        combination_stats[metric_key]['severity_counts'][result.severity.value] += 1
        if result.value is not None:
            combination_stats[metric_key]['values'].append(result.value)
        combination_stats[metric_key]['metric_name'] = metric_name
        combination_stats[metric_key]['date_range'] = metric_date_range
        combination_stats[metric_key]['group'] = group


    # Add columns to the DataFrame
    df['validation_passed'] = validation_passed
    df['validation_message'] = validation_message
    df['expected_min'] = expected_min
    df['expected_max'] = expected_max
    df['severity'] = severity
    df['metric_group'] = metric_group
    df['is_missing_combination'] = is_missing_combination # Renamed column
    df['company_has_all_combinations'] = company_has_all_combinations # Renamed column

    # Process combination statistics
    processed_combination_stats = {}
    for combination_key, stats in combination_stats.items():
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
        processed_combination_stats[f"{combination_key[0]} ({combination_key[1]})"] = stats # Format key for readability

    # Recalculate group statistics based on combination stats
    group_stats = defaultdict(lambda: {
        'total_validations': 0,
        'success_count': 0,
        'error_count': 0,
        'metrics_and_ranges': set() # Store combinations here
    })

    for combination_key, stats in combination_stats.items():
        group = stats['group']
        if group:
            group_stats[group]['total_validations'] += stats['total_validations']
            group_stats[group]['success_count'] += stats['success_count']
            group_stats[group]['error_count'] += stats['error_count']
            group_stats[group]['metrics_and_ranges'].add(combination_key)

    for group, stats in group_stats.items():
        stats['success_rate'] = stats['success_count'] / stats['total_validations'] if stats['total_validations'] > 0 else 0
        stats['metrics_and_ranges'] = sorted([f"{m} ({dr})" for m, dr in list(stats['metrics_and_ranges'])]) # Format and sort

    # Calculate validation statistics
    execution_time = time.time() - start_time
    total_companies = len(metrics_data)

    # Count companies with validation errors (based on validation_passed column)
    companies_with_errors = df[df['validation_passed'] == False]['heron_id'].nunique()

    companies_missing_combinations = completeness_summary['companies_with_missing_metric_time_ranges'] # Get from completeness_summary
    total_combinations_in_data = len(df) # Total rows in the input data is the total combinations present
    total_errors = sum(1 for passed in validation_passed if not passed)

    # Generate comprehensive summary
    summary = {
        'execution_info': {
            'total_companies': total_companies,
            'companies_with_validation_errors': companies_with_errors, # Renamed key
            'companies_missing_combinations': companies_missing_combinations, # Renamed key
            'total_combinations_in_data': total_combinations_in_data, # Renamed key
            'total_validation_errors': total_errors, # Renamed key
            'execution_time_seconds': execution_time
        },
        'error_distribution_by_combination': {
             f"{combination_key[0]} ({combination_key[1]})": stats['error_count'] # Format key
             for combination_key, stats in sorted(
                combination_stats.items(),
                key=lambda item: item[1]['error_count'],
                reverse=True
            )
        },
        'severity_distribution': {
            severity: sum(stats['severity_counts'].get(severity, 0) for stats in combination_stats.values())
            for severity in ValidationSeverity.__members__
        },
        'combination_statistics': processed_combination_stats, # Renamed key
        'group_statistics': dict(group_stats),
        'completeness_summary': completeness_summary
    }

    # Ensure output directories exist
    Path(output_csv).parent.mkdir(exist_ok=True)

    # Save the validated DataFrame as CSV
    df.to_csv(output_csv, index=False)

    # Save summary as JSON
    with open(output_summary, 'w') as f:
        # Convert tuple keys and values to strings for JSON serialization
        serializable_summary = summary.copy()

        # Process the completeness_results (per-company details) for JSON serialization
        processed_company_completeness_details = {}
        for company_id, result in completeness_results.items(): # Iterate over original completeness_results
            # Convert list of tuples to list of strings
            processed_missing_metric_time_ranges = [f"{m} ({dr})" for m, dr in result['missing_metric_time_ranges']]
            # The missing_by_metric keys are already strings, values are lists of strings
            processed_company_completeness_details[company_id] = {
                'has_all_metric_time_ranges': result['has_all_metric_time_ranges'],
                'missing_count': result['missing_count'],
                'missing_metric_time_ranges': processed_missing_metric_time_ranges,
                'missing_by_metric': result['missing_by_metric'], # Already has string keys and list of strings values
                'total_metric_time_ranges': result['total_metric_time_ranges'],
                'coverage_percentage': result['coverage_percentage'],
                'total_unique_metrics': result['total_unique_metrics']
            }
        serializable_summary['company_completeness_details'] = processed_company_completeness_details # Add processed details to summary

        # Process error_distribution_by_combination keys for JSON serialization
        processed_error_distribution = {}
        # Iterate over original combination_stats to get error counts
        for combination_key, stats in combination_stats.items():
             processed_error_distribution[f"{combination_key[0]} ({combination_key[1]})"] = stats['error_count']
        # Sort the processed error distribution by count
        sorted_error_distribution_items = sorted(
            processed_error_distribution.items(),
            key=lambda item: item[1],
            reverse=True
        )
        serializable_summary['error_distribution_by_combination'] = dict(sorted_error_distribution_items[:10]) # Slice the list before converting to dict

        # Process most_frequently_missing_combinations keys for JSON serialization
        processed_missing_combinations_summary = {}
        for combination_key, count in serializable_summary['completeness_summary']['most_frequently_missing_combinations'].items():
            processed_missing_combinations_summary[f"{combination_key[0]} ({combination_key[1]})"] = count
        serializable_summary['completeness_summary']['most_frequently_missing_combinations'] = processed_missing_combinations_summary

        # combination_statistics is already processed into processed_combination_stats with string keys
        # group_statistics already has string keys and values are serializable
        # completeness_summary (overall summary) is already serializable, except for the missing combinations part we just fixed

        json.dump(serializable_summary, f, indent=2)

    # Log summary information
    logger.info(f"Validation results saved to:")
    logger.info(f"- CSV: {output_csv}")
    logger.info(f"- Summary JSON: {output_summary}")
    logger.info(f"Total companies validated: {total_companies}")
    logger.info(f"Companies with validation errors: {companies_with_errors}")
    logger.info(f"Companies missing combinations: {companies_missing_combinations}")
    logger.info(f"Total combinations validated: {total_combinations_in_data}")
    logger.info(f"Total validation errors: {total_errors}")
    logger.info(f"Execution time: {execution_time:.2f} seconds")

    # Log missing combinations information
    if completeness_summary['most_frequently_missing_combinations']:
        logger.info("\nMost frequently missing combinations:")
        for combination, count in list(completeness_summary['most_frequently_missing_combinations'].items())[:5]:
            logger.info(f"- {combination}: missing in {count} companies")

    # Log top combinations with most errors
    top_error_combinations = sorted(
        combination_stats.items(),
        key=lambda item: item[1]['error_count'],
        reverse=True
    )[:5]
    if top_error_combinations:
        logger.info("\nTop combinations with most errors:")
        for combination_key, stats in top_error_combinations:
            if stats['error_count'] > 0:
                logger.info(f"- {combination_key[0]} ({combination_key[1]}): {stats['error_count']} errors")

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