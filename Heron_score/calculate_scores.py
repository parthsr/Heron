import pandas as pd
import numpy as np
from heron_calculator import HeronCalculator
import logging
import argparse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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