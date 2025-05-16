# Heron Score Calculation System

This system calculates the Heron score, a metric that indicates the likelihood of company default based on various financial and operational metrics.

## Overview

The Heron score is calculated using a machine learning model that takes into account multiple features including:
- Financial metrics (inflow growth rate, latest balance, debt repayment)
- Operational metrics (transaction counts, customer interactions)
- Risk indicators (fraud scores, risk assessments)

A score greater than 1 indicates a higher likelihood of company default.

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Training the Model

To train the model using historical data:

```bash
python train_model.py
```

The script expects a CSV file at `data/historical_data.csv` with the following:
- All required features (see `heron_calculator.py` for complete list)
- A 'default' column indicating historical default events (1 for default, 0 for non-default)

### Calculating Scores

To calculate Heron scores for new data:

```bash
python calculate_scores.py --input path/to/input.csv --output path/to/output.csv
```

The input CSV should contain all required features. The output will be a CSV file with the calculated scores.

## Model Details

The system uses a logistic regression model with the following features:
- inflow_growth_rate
- latest_balance
- debt_repayment_daily_average
- debt_repayment_monthly_average
- debt_repayment_weekly_average
- debt_repayment_yearly_average
- debt_repayment_weekly_std
- debt_repayment_monthly_std
- debt_repayment_yearly_std
- debt_repayment_weekly_median
- debt_repayment_monthly_median
- debt_repayment_yearly_median
- debt_repayment_weekly_min
- debt_repayment_monthly_min
- debt_repayment_yearly_min
- debt_repayment_weekly_max
- debt_repayment_monthly_max
- debt_repayment_yearly_max
- debt_repayment_weekly_sum
- debt_repayment_monthly_sum
- debt_repayment_yearly_sum
- debt_repayment_weekly_count
- debt_repayment_monthly_count
- debt_repayment_yearly_count
- debt_repayment_weekly_mean
- debt_repayment_monthly_mean
- debt_repayment_yearly_mean
- debt_repayment_weekly_skew
- debt_repayment_monthly_skew
- debt_repayment_yearly_skew
- debt_repayment_weekly_kurtosis
- debt_repayment_monthly_kurtosis
- debt_repayment_yearly_kurtosis
- debt_repayment_weekly_variance
- debt_repayment_monthly_variance
- debt_repayment_yearly_variance
- debt_repayment_weekly_std_normalized
- debt_repayment_monthly_std_normalized
- debt_repayment_yearly_std_normalized
- debt_repayment_weekly_median_normalized
- debt_repayment_monthly_median_normalized
- debt_repayment_yearly_median_normalized
- debt_repayment_weekly_mean_normalized
- debt_repayment_monthly_mean_normalized
- debt_repayment_yearly_mean_normalized

## Performance Metrics

The model's performance is evaluated using:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC

## File Structure

- `heron_calculator.py`: Main calculator class
- `train_model.py`: Script for training the model
- `calculate_scores.py`: Script for calculating scores
- `requirements.txt`: Project dependencies
- `README.md`: This documentation

## Notes

- The model is saved in the `models` directory after training
- All features are automatically scaled using StandardScaler
- The system includes comprehensive logging for monitoring and debugging 