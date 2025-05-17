import pandas as pd
import os

# Define file paths
correlation_file = 'Check score/heron_score_correlations.csv'
metrics_file = '/Users/parthsrivastava/Heron/Regression on Heron_score/company_metrics_wide_normalized.csv'
output_file = 'Check score/company_metrics_highly_correlated.csv'

# List of P&L duplicate columns to remove
pl_duplicate_columns = [
    'annualized_revenue_profit_and_loss_last_12_calendar_months',
    'annualized_revenue_profit_and_loss_last_1_calendar_months',
    'annualized_revenue_profit_and_loss_last_3_calendar_months',
    'annualized_revenue_profit_and_loss_last_6_calendar_months',
    'cogs_profit_and_loss_last_12_calendar_months',
    'cogs_profit_and_loss_last_1_calendar_months',
    'cogs_profit_and_loss_last_3_calendar_months',
    'cogs_profit_and_loss_last_6_calendar_months',
    'gross_operating_cashflow_profit_and_loss_last_12_calendar_months',
    'gross_operating_cashflow_profit_and_loss_last_1_calendar_months',
    'gross_operating_cashflow_profit_and_loss_last_3_calendar_months',
    'gross_operating_cashflow_profit_and_loss_last_6_calendar_months',
    'net_operating_cashflow_profit_and_loss_last_12_calendar_months',
    'net_operating_cashflow_profit_and_loss_last_1_calendar_months',
    'net_operating_cashflow_profit_and_loss_last_3_calendar_months',
    'net_operating_cashflow_profit_and_loss_last_6_calendar_months',
    'opex_profit_and_loss_last_12_calendar_months',
    'opex_profit_and_loss_last_1_calendar_months',
    'opex_profit_and_loss_last_3_calendar_months',
    'opex_profit_and_loss_last_6_calendar_months',
    'revenue_profit_and_loss_last_12_calendar_months',
    'revenue_profit_and_loss_last_1_calendar_months',
    'revenue_profit_and_loss_last_3_calendar_months',
    'revenue_profit_and_loss_last_6_calendar_months'
]

# Read the correlation file and identify columns with insignificant correlation
try:
    correlations_df = pd.read_csv(correlation_file)
    # Assuming the correlation value is in the second column
    # Note: Using .abs() >= -0.1 and <= 0.1 is equivalent to .abs() <= 0.1 for positive values
    # A clearer condition for insignificant correlation between -0.1 and 0.1 is (corr > -0.1) & (corr < 0.1)
    # However, based on the previous request to remove -0.1 to 0.1, I'll stick to inclusive boundaries for now.
    low_correlation_columns = correlations_df[
        (correlations_df.iloc[:, 1] >= -0.1) & (correlations_df.iloc[:, 1] <= 0.1) &
        (correlations_df.iloc[:, 0] != 'heron_score_latest') # Don't remove the target column itself
    ].iloc[:, 0].tolist()
except FileNotFoundError:
    print(f"Error: Correlation file not found at {correlation_file}")
    exit()
except Exception as e:
    print(f"Error reading correlation file: {e}")
    exit()

# Combine the lists of columns to remove, ensuring no duplicates
columns_to_remove = list(set(pl_duplicate_columns + low_correlation_columns))

# Read the main metrics file and drop the identified columns
try:
    # Read only the header first to check if columns exist before reading the whole file
    metrics_header = pd.read_csv(metrics_file, nrows=0).columns.tolist()
    
    # Filter columns_to_remove to only include columns actually present in the metrics file
    columns_to_remove_present = [col for col in columns_to_remove if col in metrics_header]
    
    if len(columns_to_remove_present) != len(columns_to_remove):
        missing_cols = set(columns_to_remove) - set(columns_to_remove_present)
        print(f"Warning: Some columns to remove were not found in the metrics file: {missing_cols}")
        
    # Read the full metrics file, dropping columns that exist
    # Using usecols=lambda ensures only necessary columns are read, which is efficient for large files
    metrics_df = pd.read_csv(metrics_file, usecols=lambda column: column not in columns_to_remove_present)

except FileNotFoundError:
    print(f"Error: Metrics file not found at {metrics_file}")
    exit()
except Exception as e: 
    print(f"Error reading metrics file: {e}")
    exit()


# Save the filtered DataFrame to a new CSV file
try:
    metrics_df.to_csv(output_file, index=False)
    print(f"Successfully created {output_file} with specified columns removed.")
    print(f"Removed {len(columns_to_remove_present)} columns.")
except Exception as e:
    print(f"Error saving the output file: {e}") 