# Heron Score Regression Analysis

## Overview
This directory contains the complete regression analysis system for the Heron score, including model training, evaluation, and score calculation. The system uses various company metrics to predict and calculate Heron scores through a regression-based approach.

## Components

### 1. Data Preparation and Analysis
- `prepare_data.py`: Prepares and preprocesses data for model training
- `calculate_normalized_correlations.py`: Computes normalized correlations between metrics
- `heron_score_correlations.csv`: Raw correlation coefficients
- `heron_score_normalized_correlations.csv`: Normalized correlation coefficients

### 2. Model Training and Export
- `train_model.py`: Main script for training the regression model
  - Feature selection
  - Model training
  - Cross-validation
  - Performance evaluation
- `model.pkl`: Trained model file
- `regression_coefficients.csv`: Model coefficients for each feature
- `regression_formula.txt`: Complete regression formula
- `export_regression_formula.py`: Exports the regression formula

### 3. Score Calculation
- `calculate_scores.py`: Calculates Heron scores using the trained model
- `heron_calculator.py`: Core calculator class for Heron score computation

## Usage

### Training the Model
```python
# Train the model
python train_model.py
```

### Calculating Scores
```python
# Calculate scores for new data
python calculate_scores.py
```

### Exporting Formula
```python
# Export the regression formula
python export_regression_formula.py
```

## Dependencies
See `requirements.txt` for full list:
- pandas
- numpy
- scikit-learn
- joblib

## Model Details

### Features
The model uses various company metrics including:
- Revenue metrics
- Operating metrics
- Balance metrics
- Tax and payment metrics
- Debt and investment metrics
- NSF-related metrics

### Output
- Trained model file (`model.pkl`)
- Regression coefficients (`regression_coefficients.csv`)
- Regression formula (`regression_formula.txt`)
- Correlation analysis results
- Score calculations

## Analysis Files

### Correlation Analysis
- `heron_score_correlations.csv`: Raw correlations with Heron score
- `heron_score_normalized_correlations.csv`: Normalized correlations

### Model Outputs
- `regression_coefficients.csv`: Feature importance and coefficients
- `regression_formula.txt`: Complete scoring formula
- `model.pkl`: Serialized model for predictions

## Notes
- The regression model is trained on historical company data
- Features are selected based on correlation analysis
- The model is validated using cross-validation
- Scores are normalized to a standard scale
- The system includes both training and prediction capabilities

## Model Performance
Current model performance metrics:
- R² Score: 0.8268 (82.68% of variance explained)
- RMSE: 142.5139
- MAE: 184.4260

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
- The script will:
  - Handle outliers using IQR method
  - Create interaction features
  - Dynamically normalize all relevant columns based on their name patterns

### 2. Train the Model
To train the model using historical data:
```bash
python Regression\ on\ Heron_score/train_model.py --input company_metrics_wide.csv --model-output Regression\ on\ Heron_score/model.pkl
```
- This will:
  - Handle outliers and create interaction features
  - Dynamically normalize all relevant metrics
  - Perform feature selection
  - Train a Random Forest model
  - Save outputs in `Regression on Heron_score/`:
    - `company_metrics_wide_normalized.csv` (normalized data)
    - `model.pkl` (trained model and feature selector)
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

## Model Features

### Base Features
- Financial metrics (balance, revenue, cashflow)
- Operational metrics (transactions, customer data)
- Risk indicators (NSF days, negative balance days)
- Data quality metrics (confidence, coverage)

### Interaction Features
- `balance_revenue_ratio`: Balance to revenue ratio
- `balance_cashflow_ratio`: Balance to cashflow ratio
- `revenue_growth_stability`: Revenue growth × confidence
- `risk_score`: Combined risk metric from NSF and negative balance days

### Feature Importance
Top 3 most important features:
1. `confidence_latest` (0.9308)
2. `merchant_coverage_latest` (0.0395)
3. `change_in_balance_last_90_days` (0.0298)

#### How Feature Importance is Calculated
The Random Forest model calculates feature importance using the following method:

1. **Mean Decrease in Impurity (MDI)**:
   - For each feature, the model tracks how much the impurity (variance) in the target variable decreases when that feature is used for splitting
   - The importance is normalized so that all features sum to 1.0
   - Higher values indicate features that are more important for making accurate predictions

2. **Calculation Process**:
   - Each tree in the forest calculates feature importance independently
   - For each node in each tree:
     - Calculate the impurity before the split
     - Calculate the impurity after the split
     - The difference is weighted by the number of samples in the node
   - The final importance is the average across all trees

3. **Interpretation**:
   - Values range from 0 to 1
   - A value of 0.9308 for `confidence_latest` means this feature is responsible for 93.08% of the model's predictive power
   - Features with very low importance (close to 0) have minimal impact on predictions

4. **Advantages of This Method**:
   - Captures non-linear relationships
   - Accounts for feature interactions
   - Robust to outliers
   - Provides a normalized measure of importance

## Output Files
- `company_metrics_wide_normalized.csv`: Normalized data used for regression and scoring
- `model.pkl`: Trained Random Forest model and feature selector
- `feature_importance.csv`: Feature importances from the model
- `regression_coefficients.csv`: All regression coefficients
- `regression_formula.txt`: Full regression formula
- `regression_evaluation.txt`: Model evaluation metrics (R², RMSE, MAE)

## Essential Scripts
- `train_model.py`: Train and normalize the regression model
- `export_regression_formula.py`: Export formula, coefficients, and evaluation metrics
- `calculate_scores.py`: Score new data using the trained model

## Notes
- The model uses Random Forest with feature selection for better accuracy
- Outliers are handled using the IQR method
- Interaction features are automatically created to capture complex relationships
- Data quality metrics are crucial for accurate predictions
- All outputs are saved in the `Regression on Heron_score` folder for organization

## Interpreting Outputs
- **regression_formula.txt**: Shows the full regression equation for `heron_score_latest`
- **regression_coefficients.csv**: Lists the coefficient for each feature
- **regression_evaluation.txt**: Shows R² (explained variance), RMSE (root mean squared error), and MAE (mean absolute error) for the model
- **feature_importance.csv**: Shows the relative importance of each feature in the Random Forest model

## File Structure
- `Regression on Heron_score/`: All scripts and outputs
- `company_metrics_wide.csv`: Input data (wide format)

## Contact
For questions or issues, contact the project maintainer. 