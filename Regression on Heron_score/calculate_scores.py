import pandas as pd
import numpy as np
from heron_calculator import HeronCalculator
import logging
import argparse
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def normalize_financial_metrics(data):
    """Normalize financial metrics using Min-Max scaling"""
    financial_metrics = [
        'annualized_revenue', 'balance_average', 'balance_minimum',
        'latest_balance', 'inflow_amount', 'outflows', 'revenue',
        'tax_payment_amount', 'gross_operating_cashflow',
        'net_operating_cashflow'
    ]
    
    scaler = MinMaxScaler()
    for metric in financial_metrics:
        if metric in data.columns:
            # Handle any negative values by adding minimum value
            min_val = data[metric].min()
            if min_val < 0:
                data[metric] = data[metric] - min_val
            # Apply log transformation if data is right-skewed
            if data[metric].skew() > 1:
                data[metric] = np.log1p(data[metric])
            # Normalize
            data[metric] = scaler.fit_transform(data[[metric]])
    
    return data

def normalize_growth_metrics(data):
    """Normalize growth metrics using Standard scaling"""
    growth_metrics = ['inflow_growth_rate', 'revenue_growth_rate']
    
    scaler = StandardScaler()
    for metric in growth_metrics:
        if metric in data.columns:
            data[metric] = scaler.fit_transform(data[[metric]])
    
    return data

def normalize_count_metrics(data):
    """Normalize count-based metrics using log transformation and Min-Max scaling"""
    count_metrics = [
        'inflows', 'outflows', 'tax_payments',
        'debt_investment_count', 'negative_balance_days',
        'nsf_days'
    ]
    
    scaler = MinMaxScaler()
    for metric in count_metrics:
        if metric in data.columns:
            # Apply log transformation
            data[metric] = np.log1p(data[metric])
            # Normalize
            data[metric] = scaler.fit_transform(data[[metric]])
    
    return data

def load_data(data_path):
    """Load input data"""
    logger.info("Loading data from %s", data_path)
    data = pd.read_csv(data_path)
    return data

def save_scores(scores, output_path):
    """Save calculated scores to file"""
    logger.info("Saving scores to %s", output_path)
    scores_df = pd.DataFrame(scores)
    scores_df.to_csv(output_path, index=False)

def main():
    parser = argparse.ArgumentParser(description='Calculate Heron scores for input data')
    parser.add_argument('--input', required=True, help='Path to input data CSV')
    parser.add_argument('--output', required=True, help='Path to save output scores CSV')
    args = parser.parse_args()
    
    # Load data
    data = load_data(args.input)
    
    # Normalize metrics
    logger.info("Normalizing metrics")
    data = normalize_financial_metrics(data)
    data = normalize_growth_metrics(data)
    data = normalize_count_metrics(data)
    
    # Initialize calculator
    calculator = HeronCalculator()
    
    try:
        # Load existing model
        calculator.load_model()
    except FileNotFoundError:
        logger.error("No trained model found. Please train the model first using train_model.py")
        return
    
    # Calculate scores
    logger.info("Calculating scores")
    scores = calculator.calculate_score(data)
    
    # Save results
    save_scores(scores, args.output)
    
    # Log summary statistics
    logger.info("Score statistics:")
    logger.info("Mean: %.2f", np.mean(scores))
    logger.info("Median: %.2f", np.median(scores))
    logger.info("Min: %.2f", np.min(scores))
    logger.info("Max: %.2f", np.max(scores))
    logger.info("Standard Deviation: %.2f", np.std(scores))

if __name__ == "__main__":
    main() 