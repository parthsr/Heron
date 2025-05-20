# Metric Distributions Analysis Suite

## Overview
This directory contains a comprehensive suite of scripts for analyzing the distributions and relationships of company metrics. The analysis helps understand metric behaviors, identify outliers, and discover correlations between different metrics.

## Scripts

### 1. run_all_analyses.py
The main orchestrator script that runs all analyses in sequence:
- Metric distribution analysis
- Correlation analysis
- Outlier analysis

### 2. metric_distribution_analysis.py
Analyzes the statistical distributions of individual metrics:
- Calculates descriptive statistics (mean, median, std, etc.)
- Generates distribution plots
- Identifies distribution types
- Handles missing values and extreme values

### 3. correlation_analysis.py
Analyzes relationships between metrics:
- Computes correlation coefficients
- Identifies strong correlations
- Generates correlation matrices
- Creates correlation visualizations
- Helps identify redundant or highly related metrics

### 4. outlier_analysis.py
Identifies and analyzes outliers in the metrics:
- Detects statistical outliers
- Analyzes outlier patterns
- Generates outlier reports
- Helps identify potential data quality issues

## Output
All analysis results are saved in the `output/` directory:
- Distribution plots
- Correlation matrices
- Statistical reports
- Outlier reports
- Summary statistics

## Usage
```python
# Run all analyses
python run_all_analyses.py

# Run individual analyses
python metric_distribution_analysis.py
python correlation_analysis.py
python outlier_analysis.py
```

## Dependencies
- pandas
- numpy
- scipy
- matplotlib
- seaborn
- os

## Analysis Types

### Distribution Analysis
- Statistical measures
- Distribution plots
- Normality tests
- Skewness and kurtosis
- Percentile analysis

### Correlation Analysis
- Pearson correlation
- Spearman correlation
- Correlation matrices
- Correlation heatmaps
- Strong correlation identification

### Outlier Analysis
- Z-score based detection
- IQR based detection
- Outlier patterns
- Impact analysis
- Data quality assessment

## Notes
- All analyses are designed to work with the Heron metrics data format
- Results help in:
  - Understanding metric behaviors
  - Identifying data quality issues
  - Feature selection for models
  - Metric validation
  - System improvement 