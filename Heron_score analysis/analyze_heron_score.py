import pandas as pd
import numpy as np

# Read the company metrics data
df = pd.read_csv('/Users/parthsrivastava/Heron/company_metrics.csv')

# Split companies into high and low heron score groups
high_score_companies = df[df['metric_label'] == 'heron_score'][df['metric_value'] > 1]
low_score_companies = df[df['metric_label'] == 'heron_score'][df['metric_value'] <= 1]

# Get the heron_ids for each group
high_score_ids = high_score_companies['heron_id'].unique()
low_score_ids = low_score_companies['heron_id'].unique()

# Get all metrics for both groups
high_score_metrics = df[df['heron_id'].isin(high_score_ids)]
low_score_metrics = df[df['heron_id'].isin(low_score_ids)]

# Get unique metric labels
all_metrics = df['metric_label'].unique()

# Create a comparison DataFrame
comparison_data = []

for metric in all_metrics:
    high_metric_data = high_score_metrics[high_score_metrics['metric_label'] == metric]['metric_value']
    low_metric_data = low_score_metrics[low_score_metrics['metric_label'] == metric]['metric_value']
    
    if not high_metric_data.empty and not low_metric_data.empty:
        comparison_data.append({
            'metric': metric,
            'high_score_count': len(high_metric_data),
            'low_score_count': len(low_metric_data),
            'high_score_mean': high_metric_data.mean(),
            'low_score_mean': low_metric_data.mean(),
            'high_score_median': high_metric_data.median(),
            'low_score_median': low_metric_data.median(),
            'high_score_std': high_metric_data.std(),
            'low_score_std': low_metric_data.std(),
            'high_score_min': high_metric_data.min(),
            'low_score_min': low_metric_data.min(),
            'high_score_max': high_metric_data.max(),
            'low_score_max': low_metric_data.max(),
            'mean_difference': high_metric_data.mean() - low_metric_data.mean(),
            'median_difference': high_metric_data.median() - low_metric_data.median()
        })

# Convert to DataFrame
comparison_df = pd.DataFrame(comparison_data)

# Sort by absolute mean difference to find most different metrics
comparison_df['abs_mean_diff'] = comparison_df['mean_difference'].abs()
comparison_df = comparison_df.sort_values('abs_mean_diff', ascending=False)

# Print summary
print(f"\nComparison between companies with heron_score > 1 (n={len(high_score_ids)}) and heron_score <= 1 (n={len(low_score_ids)})")
print("\nTop 20 metrics with largest differences between groups:")

# Format the output for better readability
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# Select and display the most different metrics
top_metrics = comparison_df.head(20)
print("\nMetric comparisons (high score vs low score):")
for _, row in top_metrics.iterrows():
    print(f"\n{row['metric']}:")
    print(f"  High Score (n={row['high_score_count']}):")
    print(f"    Mean: {row['high_score_mean']:.3f}")
    print(f"    Median: {row['high_score_median']:.3f}")
    print(f"    Std: {row['high_score_std']:.3f}")
    print(f"    Range: [{row['high_score_min']:.3f}, {row['high_score_max']:.3f}]")
    print(f"  Low Score (n={row['low_score_count']}):")
    print(f"    Mean: {row['low_score_mean']:.3f}")
    print(f"    Median: {row['low_score_median']:.3f}")
    print(f"    Std: {row['low_score_std']:.3f}")
    print(f"    Range: [{row['low_score_min']:.3f}, {row['low_score_max']:.3f}]")
    print(f"  Difference (High - Low):")
    print(f"    Mean diff: {row['mean_difference']:.3f}")
    print(f"    Median diff: {row['median_difference']:.3f}")

# Save detailed comparison to CSV
comparison_df.to_csv('heron_score_comparison.csv', index=False)
print("\nDetailed comparison has been saved to 'heron_score_comparison.csv'") 