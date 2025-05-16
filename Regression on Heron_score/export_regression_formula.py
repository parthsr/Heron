 import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

NORMALIZED_CSV = 'Regression on Heron_score/company_metrics_wide_normalized.csv'
COEFS_CSV = 'Regression on Heron_score/regression_coefficients.csv'
FORMULA_TXT = 'Regression on Heron_score/regression_formula.txt'
EVAL_TXT = 'Regression on Heron_score/regression_evaluation.txt'

def load_data(path):
    """Load normalized data and split features/target."""
    df = pd.read_csv(path)
    X = df.drop(columns=['heron_id', 'heron_score_latest'])
    y = df['heron_score_latest']
    return X, y

def train_and_save_regression(X, y):
    """Train regression, save coefficients, formula, and evaluation metrics."""
    model = LinearRegression()
    model.fit(X, y)
    # Save coefficients
    coefs = pd.DataFrame({'feature': X.columns, 'coefficient': model.coef_})
    coefs.to_csv(COEFS_CSV, index=False)
    # Save regression formula
    with open(FORMULA_TXT, 'w') as f:
        f.write(f'heron_score_latest = {model.intercept_:.4f}')
        for feat, coef in zip(X.columns, model.coef_):
            f.write(f' + ({coef:.4f} * {feat})')
    # Evaluate model
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    with open(EVAL_TXT, 'w') as f:
        f.write(f'R2: {r2:.4f}\nRMSE: {rmse:.4f}\nMAE: {mae:.4f}\n')
    print('Regression formula, coefficients, and evaluation metrics saved to Regression on Heron_score/.')

def main():
    X, y = load_data(NORMALIZED_CSV)
    train_and_save_regression(X, y)

if __name__ == "__main__":
    main() 