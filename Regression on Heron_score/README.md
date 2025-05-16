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

## Workflow

### 1. Prepare Data
- Ensure your data is in wide format (e.g., `company_metrics_wide.csv` in the project root).
- The script will dynamically detect and normalize all relevant columns based on their name patterns (no need to manually specify columns).

### 2. Train the Model
To train the model using historical data:
```bash
python Regression\ on\ Heron_score/train_model.py --input company_metrics_wide.csv --model-output Regression\ on\ Heron_score/model.pkl
```
- This will:
  - Dynamically normalize all relevant metrics
  - Train a regression model
  - Save outputs in `Regression on Heron_score/`:
    - `company_metrics_wide_normalized.csv` (normalized data)
    - `model.pkl` (trained model)
    - `feature_importance.csv` (feature importances)

### 3. Export Regression Formula and Evaluation
To export the regression formula, coefficients, and evaluation metrics:
```bash
python Regression\ on\ Heron_score/export_regression_formula.py
```
- This will create:
  - `regression_coefficients.csv` (all regression coefficients)
  - `regression_formula.txt` (full regression formula)
  - `regression_evaluation.txt` (R², RMSE, MAE)

### 4. Calculate Scores for New Data
To calculate Heron scores for new data:
```bash
python Regression\ on\ Heron_score/calculate_scores.py --input path/to/input.csv --output path/to/output.csv
```
- The input CSV should contain all required features (see wide format).
- The output will be a CSV file with the calculated scores.

## Output Files
- `company_metrics_wide_normalized.csv`: Normalized data used for regression and scoring
- `model.pkl`: Trained regression model
- `feature_importance.csv`: Feature importances from the regression model
- `regression_coefficients.csv`: All regression coefficients
- `regression_formula.txt`: Full regression formula
- `regression_evaluation.txt`: Model evaluation metrics (R², RMSE, MAE)

## Essential Scripts
- `train_model.py`: Train and normalize the regression model
- `export_regression_formula.py`: Export formula, coefficients, and evaluation metrics
- `calculate_scores.py`: Score new data using the trained model

## Notes
- The normalization is dynamic: any new columns with relevant prefixes will be normalized automatically.
- You do **not** need to keep all intermediate files; only the outputs you care about for future runs or documentation.
- All outputs are saved in the `Regression on Heron_score` folder for organization.

## Interpreting Outputs
- **regression_formula.txt**: Shows the full regression equation for `heron_score_latest`.
- **regression_coefficients.csv**: Lists the coefficient for each feature.
- **regression_evaluation.txt**: Shows R² (explained variance), RMSE (root mean squared error), and MAE (mean absolute error) for the model.

## File Structure
- `Regression on Heron_score/`: All scripts and outputs
- `company_metrics_wide.csv`: Input data (wide format)

## Contact
For questions or issues, contact the project maintainer. 