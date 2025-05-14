# Heron Metrics Validation

This project provides tools to validate and analyze metrics from the Heron system. The validation process includes three main components:

1. **Distribution Analysis**
   - Generates histograms and box plots for each metric
   - Calculates basic statistics (mean, median, std dev, quartiles)
   - Outputs saved as PNG files in `outputs/distributions/`
   - Statistical summary saved in `outputs/distribution_analysis.json`

2. **Anomaly Detection**
   - Uses Z-score method to detect outliers
   - Identifies values that deviate significantly from the mean
   - Results saved in `outputs/anomaly_detection.json`

3. **Trend Analysis**
   - Analyzes metric values across different time periods
   - Generates trend plots for metrics with multiple date ranges
   - Outputs saved as PNG files in `outputs/trends/`
   - Trend data saved in `outputs/trend_analysis.json`

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the analysis:
```bash
python validate_metrics.py
```

## Output Structure

The analysis generates three types of outputs:

1. **Distribution Analysis**
   - Visualizations: `outputs/distributions/{metric_name}_distribution.png`
   - Box plots: `outputs/distributions/{metric_name}_boxplot.png`
   - Statistics: `outputs/distribution_analysis.json`

2. **Anomaly Detection**
   - JSON file with detected anomalies: `outputs/anomaly_detection.json`
   - Includes count, values, and percentage of anomalies for each metric

3. **Trend Analysis**
   - Trend plots: `outputs/trends/{metric_name}_trend.png`
   - Trend data: `outputs/trend_analysis.json`

## Validation Criteria

The validation process checks for:

1. **Data Quality**
   - Completeness of metrics
   - Presence of outliers
   - Distribution characteristics

2. **Temporal Patterns**
   - Trends over time
   - Seasonal patterns
   - Stability of metrics

3. **Anomalies**
   - Statistical outliers (Z-score > 3)
   - Unusual patterns in time series
   - Inconsistencies in related metrics 