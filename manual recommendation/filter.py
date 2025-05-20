import pandas as pd
import numpy as np

def process_company_metrics():
    # Read the company metrics data
    try:
        df = pd.read_csv('../company_metrics.csv')
        
        # Create a unique identifier for each metric by combining label and date range
        df['metric_key'] = df['metric_label'] + '_' + df['metric_date_range']
        
        # Pivot the data to wide format
        wide_df = df.pivot(index='heron_id', 
                          columns='metric_key', 
                          values='metric_value')
        
        # Reset index to make heron_id a column
        wide_df = wide_df.reset_index()
        
        # Display basic information about the wide format dataset
        print("\nWide Format Dataset Info:")
        print(wide_df.info())
        
        # Display first few rows of the wide format
        print("\nFirst few rows of the wide format data:")
        print(wide_df.head())
        
        # Check for missing values
        missing_values = wide_df.isnull().sum()
        print("\nMissing values per column:")
        print(missing_values[missing_values > 0])
        
        # Fill missing values with appropriate methods
        # For numeric columns, fill with median
        numeric_columns = wide_df.select_dtypes(include=[np.number]).columns
        wide_df[numeric_columns] = wide_df[numeric_columns].fillna(wide_df[numeric_columns].median())
        
        # Save the processed data
        wide_df.to_csv('company_metrics_wide.csv', index=False)
        print("\nProcessed data saved to 'company_metrics_wide.csv'")
        
        return wide_df
    
    except Exception as e:
        print(f"Error processing the data: {str(e)}")
        return None

def select_and_save_columns():
    try:
        # Read the wide format company metrics data
        wide_df = pd.read_csv('company_metrics_wide.csv')
        
        # Define the exact list of columns requested by the user
        selected_columns = [
            'heron_id',
            'annualized_revenue_last_12_calendar_months',
            'balance_average_last_365_days',
            'balance_minimum_last_365_days',
            'cogs_daily_average_last_365_days',
            'confidence_latest',
            'debt_investment_count_last_365_days',
            'debt_investment_last_365_days',
            'debt_investors_last_365_days',
            'debt_repayment_daily_average_last_365_days',
            'debt_service_coverage_ratio_last_12_calendar_months',
            'debt_service_coverage_ratio_last_1_calendar_months',
            'debt_service_coverage_ratio_last_3_calendar_months',
            'debt_service_coverage_ratio_last_6_calendar_months',
            'gross_operating_cashflow_last_12_calendar_months',
            'heron_score_latest',
            'inflow_daily_average_last_365_days',
            'inflow_growth_rate_last_6_calendar_months',
            'last_debt_investment_days_latest',
            'last_debt_investment_latest',
            'latest_balance_latest',
            'negative_balance_days_by_account_last_365_days',
            'negative_balance_days_last_365_days',
            'net_operating_cashflow_daily_average_last_365_days',
            'outflows_last_365_days',
            'potentially_duplicated_account_pairs_latest',
            'revenue_growth_rate_last_6_calendar_months',
            'revenue_last_12_calendar_months'
        ]

        # Select the specified columns
        df_selected = wide_df[selected_columns]
        
        # Save the selected data to a new CSV file
        output_filename = 'company_metrics_specific_columns.csv'
        df_selected.to_csv(output_filename, index=False)
        
        print(f"\nSelected columns saved to '{output_filename}'")
        print(f"Shape of the selected data: {df_selected.shape}")
        print("First few rows of the selected data:")
        print(df_selected.head())
        
    except FileNotFoundError:
        print("Error: 'company_metrics_wide.csv' not found. Please ensure the previous step ran successfully.")
    except KeyError as e:
        print(f"Error selecting columns: {e}. One or more specified columns were not found.")
    except Exception as e:
        print(f"Error processing the data: {str(e)}")

if __name__ == "__main__":
    # processed_df = process_company_metrics()
    # if processed_df is not None:
    #     print("\nData processing completed successfully!")
    #     print(f"Final shape of the dataset: {processed_df.shape}")
    select_and_save_columns()
