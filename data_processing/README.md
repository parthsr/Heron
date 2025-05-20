# Data Processing - Transform Metrics

## Overview
The `transform_metrics.py` script is responsible for transforming company metrics data from a long format to a wide format, making it more suitable for analysis and machine learning applications. This transformation is particularly important for the Heron scoring system, which uses various financial and operational metrics to assess company performance.

## Functionality

### transform_metrics_to_wide()
This function performs the following operations:
1. Reads validated metrics from `validation_system/validation_results/company_metrics_validated.csv`
2. Transforms the data from long format to wide format by:
   - Combining `metric_label` and `metric_date_range` to create unique column names
   - Pivoting the data using `heron_id` as the index
   - Handling duplicate values by taking the first occurrence
3. Saves the transformed data to `data/company_metrics_wide.csv`

## Input/Output

### Input
- File: `validation_system/validation_results/company_metrics_validated.csv`
- Format: Long format with columns:
  - heron_id
  - metric_label
  - metric_date_range
  - metric_value

### Output
- File: `data/company_metrics_wide.csv`
- Format: Wide format with:
  - heron_id as index
  - Combined metric columns (metric_label_metric_date_range)
  - Metric values as cell values

## Usage
```python
from transform_metrics import transform_metrics_to_wide

# Transform metrics to wide format
transform_metrics_to_wide()
```

## Related Metrics
The transformation handles various types of metrics including:
- Revenue metrics (daily, monthly, and calendar-based)
- Operating metrics (cashflow, expenses)
- Balance metrics
- Tax and payment metrics
- Debt and investment metrics
- NSF (Non-Sufficient Funds) related metrics

## Dependencies
- pandas
- os

## Notes
- The script handles duplicate values by taking the first occurrence
- All metrics are preserved in the transformation
- The output format is optimized for machine learning and analysis purposes 