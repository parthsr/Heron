import pandas as pd
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def prepare_wide_format_data(input_path, output_path):
    """Transform data from long to wide format"""
    logger.info("Loading data from %s", input_path)
    data = pd.read_csv(input_path)
    
    # Create unique feature names by combining metric_label and metric_date_range
    data['feature_name'] = data['metric_label'] + '_' + data['metric_date_range'].astype(str)
    
    # Pivot the data to wide format
    logger.info("Transforming data to wide format")
    wide_data = data.pivot(
        index='heron_id',
        columns='feature_name',
        values='metric_value'
    )
    
    # Reset index to make heron_id a column
    wide_data = wide_data.reset_index()
    
    # Save the wide format data
    logger.info("Saving wide format data to %s", output_path)
    wide_data.to_csv(output_path, index=False)
    
    return wide_data

if __name__ == "__main__":
    input_path = "company_metrics.csv"
    output_path = "company_metrics_wide.csv"
    prepare_wide_format_data(input_path, output_path) 