# Heron Scoring System

## Overview
The Heron Scoring System is a comprehensive platform for calculating and analyzing company performance scores based on various financial, operational, and data quality metrics. The system includes data validation, metric analysis, regression modeling, and score calculation components.

## System Components

### 1. Validation System (`validation_system/`)
Ensures data quality and reliability through comprehensive validation checks.

#### Key Features
- Financial metric validation
- Operational metric validation
- Data quality validation
- Automated validation rules
- Quality assessment reports

#### Usage
```python
python validate_metrics.py --input path/to/metrics.csv --output validation_results/
```

### 2. Metric Distributions Analysis (`metric_distributions/`)
Analyzes the statistical distributions and relationships of company metrics.

#### Key Features
- Distribution analysis
- Correlation analysis
- Outlier detection
- Statistical reporting
- Visualization tools

#### Usage
```python
# Run all analyses
python run_all_analyses.py

# Run individual analyses
python metric_distribution_analysis.py
python correlation_analysis.py
python outlier_analysis.py
```

### 3. Regression Analysis (`Regression on Heron_score/`)
Implements the regression model for Heron score calculation.

#### Key Features
- Model training
- Feature selection
- Score calculation
- Formula export
- Performance evaluation

#### Usage
```python
# Train the model
python train_model.py --input company_metrics_wide.csv --model-output model.pkl

# Calculate scores
python calculate_scores.py --input path/to/input.csv --output path/to/output.csv

# Export formula
python export_regression_formula.py
```

### 4. Heron Score Analysis (`Heron_score analysis/`)
Analyzes the differences between high and low-scoring companies.

#### Key Features
- Statistical comparison
- Feature importance analysis
- Performance metrics
- Group analysis
- Detailed reporting

#### Usage
```python
python analyze_heron_score.py
```

## Data Processing

### Transform Metrics (`data_processing/`)
Transforms metrics data from long to wide format for analysis.

#### Key Features
- Data transformation
- Format standardization
- Feature combination
- Data cleaning

#### Usage
```python
from transform_metrics import transform_metrics_to_wide
transform_metrics_to_wide()
```

## Model Details

### Features
The system uses various company metrics including:
- Revenue metrics (daily, monthly, calendar-based)
- Operating metrics (cashflow, expenses)
- Balance metrics
- Tax and payment metrics
- Debt and investment metrics
- NSF-related metrics
- Data quality metrics

### Model Performance
- R² Score: 0.8268 (82.68% of variance explained)
- RMSE: 142.5139
- MAE: 184.4260

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies
- pandas
- numpy
- scikit-learn
- scipy
- matplotlib
- seaborn
- joblib
- logging
- json

## Workflow

1. **Data Validation**
   - Validate input metrics
   - Ensure data quality
   - Generate validation reports

2. **Data Analysis**
   - Analyze metric distributions
   - Identify correlations
   - Detect outliers

3. **Model Training**
   - Prepare and normalize data
   - Train regression model
   - Evaluate performance
   - Export formula

4. **Score Calculation**
   - Calculate Heron scores
   - Generate reports
   - Analyze results

## Output Files

### Validation
- `company_metrics_validated.csv`
- `validation_report.csv`
- `quality_assessment.txt`

### Analysis
- Distribution plots
- Correlation matrices
- Statistical reports
- Outlier reports

### Model
- `model.pkl`
- `regression_coefficients.csv`
- `regression_formula.txt`
- `feature_importance.csv`

## Notes
- All components are designed to work together seamlessly
- Data quality is crucial for accurate scoring
- The system is regularly updated with new features
- Results are used for business decision-making
- The system includes both automated and manual checks

## Contact
For questions or issues, contact the project maintainer. 