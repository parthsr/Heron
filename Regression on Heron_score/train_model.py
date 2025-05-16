import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import MinMaxScaler, StandardScaler, PolynomialFeatures
from sklearn.feature_selection import SelectFromModel
import joblib
import logging
import argparse
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_outliers(data, columns, method='iqr'):
    """Handle outliers using IQR method"""
    for col in columns:
        if col in ['heron_id', 'heron_score_latest']:
            continue
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        data[col] = data[col].clip(lower=lower_bound, upper=upper_bound)
    return data

def create_interaction_features(data):
    """Create interaction features between important metrics"""
    # Balance and revenue interactions
    data['balance_revenue_ratio'] = data['balance_average_last_180_days'] / (data['revenue_last_6_calendar_months'] + 1)
    data['balance_cashflow_ratio'] = data['balance_average_last_180_days'] / (data['net_operating_cashflow_daily_average_last_180_days'] + 1)
    
    # Growth and stability metrics
    data['revenue_growth_stability'] = data['revenue_growth_rate_last_6_calendar_months'] * data['confidence_latest']
    
    # Risk metrics
    data['risk_score'] = (data['nsf_days_last_90_days'] * data['negative_balance_days_last_90_days']) / (data['deposit_days_last_90_days'] + 1)
    
    return data

def load_and_prepare_data(data_path):
    """Load and prepare data for training."""
    logger.info("Loading data from %s", data_path)
    data = pd.read_csv(data_path)
    
    # Handle missing values
    data = data.fillna(0)
    
    # Handle outliers for numerical columns
    numerical_cols = data.select_dtypes(include=[np.number]).columns
    data = handle_outliers(data, numerical_cols)
    
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

    # Group columns by their type
    financial_cols = []
    count_cols = []
    growth_cols = []
    ratio_cols = []
    data_quality_cols = []

    for col in data.columns:
        if col == 'heron_id' or col == 'heron_score_latest':
            continue
        if any(col.startswith(prefix) for prefix in financial_prefixes):
            financial_cols.append(col)
        elif any(col.startswith(prefix) for prefix in count_prefixes):
            count_cols.append(col)
        elif any(col.startswith(prefix) for prefix in growth_prefixes):
            growth_cols.append(col)
        elif any(col.startswith(prefix) for prefix in ratio_prefixes):
            ratio_cols.append(col)
        elif any(col.startswith(prefix) for prefix in data_quality_prefixes):
            data_quality_cols.append(col)

    # Process financial metrics
    if financial_cols:
        logger.info("\nProcessing financial metrics:")
        for col in financial_cols:
            logger.info(f"\nColumn: {col}")
            # Log original values for specific companies
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"Original values - Company A: {company_a}, Company B: {company_b}")
            
            # Handle negative values
            min_val = data[col].min()
            if min_val < 0:
                data[col] = data[col] - min_val
                company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
                company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
                logger.info(f"After handling negatives - Company A: {company_a}, Company B: {company_b}")
            
            # Apply log transformation
            original_skew = data[col].skew()
            logger.info(f"Skewness: {original_skew}")
            if original_skew > 1:
                data[col] = np.log1p(data[col])
                company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
                company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
                logger.info(f"After log transform - Company A: {company_a}, Company B: {company_b}")
            
            # Normalize
            scaler = MinMaxScaler()
            data[col] = scaler.fit_transform(data[[col]])
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"After normalization - Company A: {company_a}, Company B: {company_b}")
            
            # Log min and max values
            logger.info(f"Min value: {data[col].min()}, Max value: {data[col].max()}")

    # Process count metrics
    if count_cols:
        logger.info("\nProcessing count metrics:")
        for col in count_cols:
            logger.info(f"\nColumn: {col}")
            # Log original values
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"Original values - Company A: {company_a}, Company B: {company_b}")
            
            # Apply log transformation
            data[col] = np.log1p(data[col])
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"After log transform - Company A: {company_a}, Company B: {company_b}")
            
            # Normalize
            scaler = MinMaxScaler()
            data[col] = scaler.fit_transform(data[[col]])
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"After normalization - Company A: {company_a}, Company B: {company_b}")
            
            # Log min and max values
            logger.info(f"Min value: {data[col].min()}, Max value: {data[col].max()}")

    # Process growth metrics
    if growth_cols:
        logger.info("\nProcessing growth metrics:")
        for col in growth_cols:
            logger.info(f"\nColumn: {col}")
            # Log original values
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"Original values - Company A: {company_a}, Company B: {company_b}")
            
            # Normalize
            scaler = StandardScaler()
            data[col] = scaler.fit_transform(data[[col]])
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"After normalization - Company A: {company_a}, Company B: {company_b}")
            
            # Log mean and std
            logger.info(f"Mean: {data[col].mean()}, Std: {data[col].std()}")

    # Process ratio metrics
    if ratio_cols:
        logger.info("\nProcessing ratio metrics:")
        for col in ratio_cols:
            logger.info(f"\nColumn: {col}")
            # Log original values
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"Original values - Company A: {company_a}, Company B: {company_b}")
            
            # Normalize
            scaler = MinMaxScaler()
            data[col] = scaler.fit_transform(data[[col]])
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"After normalization - Company A: {company_a}, Company B: {company_b}")
            
            # Log min and max values
            logger.info(f"Min value: {data[col].min()}, Max value: {data[col].max()}")

    # Process data quality metrics
    if data_quality_cols:
        logger.info("\nProcessing data quality metrics:")
        for col in data_quality_cols:
            logger.info(f"\nColumn: {col}")
            # Log original values
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"Original values - Company A: {company_a}, Company B: {company_b}")
            
            # Normalize
            scaler = MinMaxScaler()
            data[col] = scaler.fit_transform(data[[col]])
            company_a = data[data['heron_id'] == 'eus_2RywWUaewnrMgB8oukeRTp'][col].values[0]
            company_b = data[data['heron_id'] == 'eus_4C4mJ7cAbSFhHGkpo4dYs4'][col].values[0]
            logger.info(f"After normalization - Company A: {company_a}, Company B: {company_b}")
            
            # Log min and max values
            logger.info(f"Min value: {data[col].min()}, Max value: {data[col].max()}")

    return data

def train_model(X, y):
    """Train the regression model using Random Forest"""
    logger.info("Training Random Forest model")
    
    # Initial model for feature selection
    initial_model = RandomForestRegressor(n_estimators=100, random_state=42)
    initial_model.fit(X, y)
    
    # Feature selection
    selector = SelectFromModel(initial_model, prefit=True)
    X_selected = selector.transform(X)
    selected_features = X.columns[selector.get_support()]
    
    # Final model with selected features
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    model.fit(X_selected, y)
    
    return model, selector, selected_features

def evaluate_model(model, selector, X_test, y_test):
    """Evaluate the model performance"""
    X_test_selected = selector.transform(X_test)
    y_pred = model.predict(X_test_selected)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    logger.info("Model Performance:")
    logger.info("R2 Score: %.4f", r2)
    logger.info("RMSE: %.4f", rmse)
    
    return r2, rmse

def save_model(model, selector, selected_features, model_path):
    """Save the trained model and feature selector"""
    logger.info("Saving model to %s", model_path)
    joblib.dump({
        'model': model,
        'selector': selector,
        'selected_features': selected_features
    }, model_path)

def main():
    parser = argparse.ArgumentParser(description='Train Heron score regression model')
    parser.add_argument('--input', required=True, help='Path to input data CSV')
    parser.add_argument('--model-output', required=True, help='Path to save trained model')
    parser.add_argument('--test-size', type=float, default=0.2, help='Test set size (default: 0.2)')
    args = parser.parse_args()
    
    # Load and prepare data
    data = load_and_prepare_data(args.input)
    
    # Create interaction features
    logger.info("Creating interaction features")
    data = create_interaction_features(data)
    
    # Dynamically normalize metrics
    logger.info("Dynamically normalizing metrics")
    data = dynamic_normalize(data)
    
    # Save normalized data
    normalized_path = 'Regression on Heron_score/company_metrics_wide_normalized.csv'
    data.to_csv(normalized_path, index=False, float_format='%.9f')
    logger.info(f"Normalized data saved to {normalized_path}")
    
    # Prepare features and target
    X = data.drop(columns=['heron_id', 'heron_score_latest'])
    y = data['heron_score_latest']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42
    )
    
    # Train model
    model, selector, selected_features = train_model(X_train, y_train)
    
    # Evaluate model
    r2, rmse = evaluate_model(model, selector, X_test, y_test)
    
    # Save model
    save_model(model, selector, selected_features, args.model_output)
    
    # Log feature importance
    feature_importance = pd.DataFrame({
        'feature': selected_features,
        'importance': model.feature_importances_
    })
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    
    logger.info("\nTop 10 most important features:")
    for _, row in feature_importance.head(10).iterrows():
        logger.info("%s: %.4f", row['feature'], row['importance'])
    
    # Save feature importance to CSV
    feature_importance.to_csv('Regression on Heron_score/feature_importance.csv', index=False)
    logger.info("Feature importance saved to Regression on Heron_score/feature_importance.csv")

if __name__ == "__main__":
    main() 