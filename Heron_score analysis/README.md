# Heron Score Analysis

## Overview
The `analyze_heron_score.py` script performs statistical analysis to compare companies with high Heron scores (>500) versus low Heron scores (≤500). This analysis helps identify which metrics most significantly differentiate between high and low-scoring companies.

## Functionality

### Statistical Analysis
The script performs the following operations:
1. Reads company metrics data from `company_metrics.csv`
2. Splits companies into two groups based on Heron score threshold (500)
3. For each metric, performs:
   - T-test comparison between high and low score groups
   - Calculation of descriptive statistics (mean, median, std, min, max)
   - Computation of differences between groups
4. Generates a comprehensive comparison report
5. Saves detailed results to `heron_score_comparison.csv`

### Output Analysis
The script provides:
- Top 20 metrics with largest differences between groups
- Statistical significance indicators (*** for p < 0.05)
- Detailed statistics for each metric including:
  - Sample sizes
  - Mean and median values
  - Standard deviations
  - Value ranges
  - Mean and median differences
  - P-values
- Summary of statistically significant metrics

## Usage
```python
# Run the analysis script
python analyze_heron_score.py
```

## Output Files
- `heron_score_comparison.csv`: Detailed comparison data including:
  - Metric names
  - Sample sizes for both groups
  - Statistical measures
  - Significance indicators
  - P-values

## Dependencies
- pandas
- numpy
- scipy.stats
- os

## Statistical Methodology
- Uses Welch's t-test (unequal variances assumed)
- Significance threshold: p < 0.05
- Metrics are sorted by absolute mean difference
- Handles missing data appropriately

## Notes
- The analysis helps identify which metrics are most predictive of Heron scores
- Results can be used to:
  - Validate the Heron scoring system
  - Identify key performance indicators
  - Guide feature selection for machine learning models
  - Understand what differentiates high-performing companies 