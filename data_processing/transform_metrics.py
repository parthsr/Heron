import pandas as pd
import os

def transform_metrics_to_wide():
    # Read the validated metrics file
    input_file = 'validation_system/validation_results/company_metrics_validated.csv'
    output_file = 'data/company_metrics_wide.csv'
    
    # Read the CSV file
    print("Reading the metrics file...")
    df = pd.read_csv(input_file)
    
    # Combine metric_label and metric_date_range for unique columns
    df['metric_label_date'] = df['metric_label'].astype(str) + '_' + df['metric_date_range'].astype(str)
    
    # Transform from long to wide format, handling duplicates by taking the first value
    print("Transforming to wide format...")
    df_wide = df.pivot_table(
        index='heron_id',
        columns='metric_label_date',
        values='metric_value',
        aggfunc='first'  # Take the first value if duplicates exist
    ).reset_index()
    
    # Save the transformed data
    print("Saving the transformed data...")
    df_wide.to_csv(output_file, index=False)
    print(f"Transformation complete. Output saved to {output_file}")

if __name__ == "__main__":
    transform_metrics_to_wide() 