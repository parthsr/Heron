import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import logging
import argparse
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_and_prepare_data(data_path):
    """Load and prepare data for training."""
    logger.info("Loading data from %s", data_path)
    data = pd.read_csv(data_path)

    # Handle missing values
    data = data.fillna(0)
    return data

def dynamic_normalize(data):
    """
    Dynamically normalize columns based on their name patterns.
    - Financial metrics: log+MinMax if right-skewed
    - Count metrics: log+MinMax
    - Growth metrics: StandardScaler
    - Ratio metrics: MinMax
    - Data quality metrics: MinMax
    """
    financial_prefixes = [
        'annualized_revenue', 'balance_average', 'balance_minimum',
        'latest_balance', 'inflow_amount', 'outflows', 'revenue',
        'tax_payment_amount', 'gross_operating_cashflow',
        'net_operating_cashflow', 'cogs', 'opex', 'average_credit_card_spend',
        'gross_operating_cashflow_profit_and_loss', 'net_operating_cashflow_profit_and_loss',
        'revenue_profit_and_loss', 'opex_profit_and_loss', 'revenue_monthly_average'
    ]
    count_prefixes = [
        'inflows', 'outflows', 'tax_payments', 'debt_investment_count',
        'negative_balance_days', 'nsf_days', 'deposit_days',
        'distinct_mcas_from_inflows', 'distinct_mcas_from_outflows',
        'atm_withdrawals', 'debt_investors', 'debt_collection', 'merchant_heron_ids'
    ]
    growth_prefixes = [
        'inflow_growth_rate', 'revenue_growth_rate', 'change_in_balance'
    ]
    ratio_prefixes = [
        'debt_service_coverage_ratio', 'has_balance_ratio'
    ]
    data_quality_prefixes = [
        'confidence', 'coverage', 'freshness', 'data_volume', 'date_range',
        'category_coverage', 'merchant_coverage', 'unconnected_account_ratio',
        'data_coverage', 'accounts', 'potentially_duplicated_account_pairs'
    ]

    scaler_minmax = MinMaxScaler()
    scaler_standard = StandardScaler()

    for col in data.columns:
        if col == 'heron_id' or col == 'heron_score_latest':
            continue
        # Financial metrics
        if any(col.startswith(prefix) for prefix in financial_prefixes):
            original_skew = data[col].skew()
            min_val = data[col].min()
            if min_val < 0:
                data[col] = data[col] - min_val
            if original_skew > 1:
                data[col] = np.log1p(data[col])
            data[col] = scaler_minmax.fit_transform(data[[col]])
        # Count metrics
        elif any(col.startswith(prefix) for prefix in count_prefixes):
            data[col] = np.log1p(data[col])
            data[col] = scaler_minmax.fit_transform(data[[col]])
        # Growth metrics
        elif any(col.startswith(prefix) for prefix in growth_prefixes):
            data[col] = scaler_standard.fit_transform(data[[col]])
        # Ratio metrics
        elif any(col.startswith(prefix) for prefix in ratio_prefixes):
            data[col] = scaler_minmax.fit_transform(data[[col]])
        # Data quality metrics
        elif any(col.startswith(prefix) for prefix in data_quality_prefixes):
            data[col] = scaler_minmax.fit_transform(data[[col]])
        # Otherwise, skip or leave as is
    return data

def train_model(X, y):
    """Train the regression model"""
    logger.info("Training regression model")
    model = LinearRegression()
    model.fit(X, y)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the model performance"""
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    logger.info("Model Performance:")
    logger.info("R2 Score: %.4f", r2)
    logger.info("RMSE: %.4f", rmse)
    
    return r2, rmse

def save_model(model, model_path):
    """Save the trained model"""
    logger.info("Saving model to %s", model_path)
    joblib.dump(model, model_path)

def main():
    parser = argparse.ArgumentParser(description='Train Heron score regression model')
    parser.add_argument('--input', required=True, help='Path to input data CSV')
    parser.add_argument('--model-output', required=True, help='Path to save trained model')
    parser.add_argument('--test-size', type=float, default=0.2, help='Test set size (default: 0.2)')
    args = parser.parse_args()
    
    # Load and prepare data
    data = load_and_prepare_data(args.input)
    
    # Dynamically normalize metrics
    logger.info("Dynamically normalizing metrics")
    data = dynamic_normalize(data)
    
    # Save normalized data
    normalized_path = 'Regression on Heron_score/company_metrics_wide_normalized.csv'
    data.to_csv(normalized_path, index=False)
    logger.info(f"Normalized data saved to {normalized_path}")
    
    # Prepare features and target
    X = data.drop(columns=['heron_id', 'heron_score_latest'])
    y = data['heron_score_latest']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42
    )
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    r2, rmse = evaluate_model(model, X_test, y_test)
    
    # Save model
    save_model(model, args.model_output)
    
    # Log feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'coefficient': model.coef_
    })
    feature_importance = feature_importance.sort_values('coefficient', ascending=False)
    
    logger.info("\nTop 10 most important features:")
    for _, row in feature_importance.head(10).iterrows():
        logger.info("%s: %.4f", row['feature'], row['coefficient'])
    
    # Save feature importance to CSV in the Regression on Heron_score folder
    feature_importance.to_csv('Regression on Heron_score/feature_importance.csv', index=False)
    logger.info("Feature importance saved to Regression on Heron_score/feature_importance.csv")

if __name__ == "__main__":
    main() 