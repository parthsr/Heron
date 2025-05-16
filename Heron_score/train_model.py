import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from heron_calculator import HeronCalculator
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_data(data_path):
    """Load and prepare training data"""
    logger.info("Loading data from %s", data_path)
    data = pd.read_csv(data_path)
    return data

def prepare_features(data):
    """Prepare features for training"""
    logger.info("Preparing features")
    
    # First, extract heron_score as the target variable
    heron_scores = data[data['metric_label'] == 'heron_score'].copy()
    if heron_scores.empty:
        raise ValueError("heron_score not found in the data. Please ensure it is available.")
    
    # Keep only the latest heron_score for each company
    heron_scores = heron_scores[heron_scores['metric_date_range'] == 'latest']
    y = heron_scores.set_index('heron_id')['metric_value']
    
    # Remove heron_score from the features
    data = data[data['metric_label'] != 'heron_score']
    
    # Combine metric_label and metric_date_range to create unique feature names
    if 'metric_date_range' in data.columns:
        data['feature_name'] = data['metric_label'] + '_' + data['metric_date_range'].astype(str)
    else:
        data['feature_name'] = data['metric_label']
    
    # Pivot the data to wide format using the new feature names
    logger.info("Transforming data to wide format with all metrics")
    wide_data = data.pivot(
        index='heron_id',
        columns='feature_name',
        values='metric_value'
    )
    
    # Fill missing values with 0
    wide_data = wide_data.fillna(0)
    
    # Ensure X and y have the same index
    X = wide_data.loc[y.index]
    
    return X, y

def main():
    # Load data
    data_path = '../company_metrics.csv'
    data = load_data(data_path)
    
    # Prepare features and target
    X, y = prepare_features(data)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Initialize calculator
    calculator = HeronCalculator()
    
    # Train model
    logger.info("Training model")
    calculator.train(X_train, y_train)
    
    # Evaluate model
    logger.info("Evaluating model")
    metrics = calculator.evaluate(X_test, y_test)
    
    # Log results
    logger.info("\n=== Model Performance Metrics ===\n")
    
    # Regression Metrics
    logger.info("Regression Metrics:")
    logger.info("------------------------")
    logger.info("Mean Squared Error: %.4f", metrics['mse'])
    logger.info("R-squared: %.4f", metrics['r2'])
    
    # Print model summary
    calculator.print_model_summary()
    
    # Save output to markdown file
    output_file = 'model_output.md'
    with open(output_file, 'w') as f:
        f.write("# Model Output\n\n")
        f.write("## Regression Formula\n")
        f.write(calculator.get_regression_formula())
        f.write("\n\n## Feature Importances\n")
        importances_df = calculator.get_feature_importances(top_n=20)
        # Map feature indices to actual metric names
        importances_df['feature'] = importances_df['feature'].apply(lambda x: X.columns[int(x[1:])] if x.startswith('x') else x)
        f.write(importances_df.to_markdown(index=False))
        f.write("\n\n## Evaluation Metrics\n")
        f.write("Mean Squared Error: {:.4f}\n".format(metrics['mse']))
        f.write("R-squared: {:.4f}\n".format(metrics['r2']))
    
    logger.info("Model output saved to %s", output_file)

if __name__ == "__main__":
    main() 