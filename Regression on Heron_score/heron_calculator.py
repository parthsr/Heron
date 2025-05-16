import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import joblib
import os
from sklearn.metrics import roc_curve, mean_squared_error, r2_score
from scipy import stats

class HeronCalculator:
    def __init__(self, model_path='models/heron_model.joblib'):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = [
            # Balance Metrics
            'inflow_growth_rate',
            'inflow_daily_average',
            'outflow_daily_average',
            'latest_balance',
            'balance_minimum',
            'balance_average',
            'change_in_balance',
            'weekday_balance_average',
            'weekday_with_highest_avg',
            'weekday_with_lowest_avg',
            
            # Data Quality Metrics
            'data_volume',
            'date_range',
            'data_freshness',
            'has_balance_ratio',
            'data_coverage',
            'accounts',
            'potentially_duplicated_account_pairs',
            'inflows',
            'outflows',
            'inflow_amount',
            'confidence',
            'revenue_anomalies',
            
            # Debt Metrics
            'last_debt_investment',
            'last_debt_investment_days',
            'debt_repayment_daily_average',
            'debt_investment',
            'debt_investors',
            'debt_investment_count',
            'debt_repayment',
            'debt_service_coverage_ratio',
            
            # Heron Metrics
            'merchant_heron_ids',
            'predicted_nsf_fees',
            'predicted_balance_daily_average',
            'distinct_mcas_from_outflows',
            'distinct_mcas_from_inflows',
            
            # Processing Quality Metrics
            'category_coverage',
            'merchant_coverage',
            'unconnected_account_ratio',
            
            # Profit and Loss Metrics
            'revenue_daily_average',
            'cogs_daily_average',
            'opex_daily_average',
            'revenue_sources',
            'revenue',
            'annualized_revenue',
            'cogs',
            'average_credit_card_spend',
            'opex',
            'revenue_profit_and_loss',
            'annualized_revenue_profit_and_loss',
            'cogs_profit_and_loss',
            'opex_profit_and_loss',
            'revenue_monthly_average',
            'revenue_growth_rate',
            'gross_operating_cashflow_daily_average',
            'net_operating_cashflow_daily_average',
            'gross_operating_cashflow',
            'net_operating_cashflow',
            'gross_operating_cashflow_profit_and_loss',
            'net_operating_cashflow_profit_and_loss',
            
            # Risk Flag Metrics
            'deposit_days',
            'nsf_fees',
            'nsf_days',
            'debt_collection',
            'atm_withdrawals',
            'tax_payments',
            'tax_payment_amount',
            'negative_balance_days',
            'negative_balance_days_by_account'
        ]
        
        # Load model if it exists
        if os.path.exists(model_path):
            self.load_model()
        else:
            self.initialize_model()

    def initialize_model(self):
        """Initialize a new model and scaler"""
        self.model = LinearRegression()
        self.scaler = StandardScaler()

    def load_model(self):
        """Load existing model and scaler"""
        saved_data = joblib.load(self.model_path)
        self.model = saved_data['model']
        self.scaler = saved_data['scaler']

    def save_model(self):
        """Save model and scaler"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, self.model_path)

    def preprocess_features(self, X, fit=False):
        """Preprocess features for prediction"""
        # Convert to numpy array if needed
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        # Scale features
        if fit:
            self.scaler.fit(X)
        X = self.scaler.transform(X)
        
        return X

    def calculate_score(self, data):
        """
        Calculate Heron score for given data
        
        Args:
            data (pd.DataFrame): DataFrame containing the required features
            
        Returns:
            float: Heron score (probability of default)
        """
        if self.model is None:
            raise ValueError("Model not initialized. Please train the model first.")
        
        X = self.preprocess_features(data)
        probabilities = self.model.predict(X)
        
        # Return probability of default (class 1)
        return probabilities

    def train(self, X, y):
        """Train the model"""
        # Preprocess features
        X_processed = self.preprocess_features(X, fit=True)
        
        # Train the model
        self.model.fit(X_processed, y)
        
        # Save the model and scaler
        self.save_model()

    def evaluate(self, X, y):
        """
        Evaluate regression model performance
        """
        X_processed = self.preprocess_features(X)
        y_pred = self.model.predict(X_processed)
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        return {
            'mse': mse,
            'r2': r2
        }

    def get_regression_formula(self):
        """
        Get the regression formula showing the relationship between features and heron_score
        """
        if self.model is None:
            raise ValueError("Model not initialized. Please train the model first.")
        coefficients = self.model.coef_
        intercept = self.model.intercept_
        formula = f"heron_score = {intercept:.4f}"
        for i, coef in enumerate(coefficients):
            if abs(coef) > 1e-10:
                formula += f" + ({coef:.4f} × x{i})"
        return formula

    def get_feature_importances(self, top_n=None):
        """
        Get the importance of each feature in predicting heron_score
        """
        if self.model is None:
            raise ValueError("Model not initialized. Please train the model first.")
        importance = np.abs(self.model.coef_)
        importance_df = pd.DataFrame({
            'feature': [f"x{i}" for i in range(len(importance))],
            'coefficient': self.model.coef_,
            'importance': importance
        })
        importance_df = importance_df.sort_values('importance', ascending=False)
        if top_n is not None:
            importance_df = importance_df.head(top_n)
        return importance_df

    def print_model_summary(self):
        if self.model is None:
            raise ValueError("Model not initialized. Please train the model first.")
        print("\n=== Heron Score Regression Model Summary ===\n")
        print("Regression Formula:")
        print(self.get_regression_formula())
        print("\n")
        print("Top 10 Most Important Features:")
        importance_df = self.get_feature_importances(top_n=10)
        print(importance_df[['feature', 'coefficient', 'importance']].to_string(index=False))
        print("\n") 