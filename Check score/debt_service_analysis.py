import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# Set style for better visualizations
plt.style.use('default')
sns.set_theme()

# Load the data
df = pd.read_csv('Check score/company_metrics_wide.csv')

# Select relevant columns
dscr_columns = [col for col in df.columns if 'debt_service_coverage_ratio' in col]
target_col = 'heron_score_latest'

# Create a figure for subplots
plt.figure(figsize=(15, 10))

# Dictionary to store results
results = {}

# Analyze each DSCR metric
for i, dscr_col in enumerate(dscr_columns, 1):
    # Prepare data
    X = df[[dscr_col]].values
    y = df[target_col].values
    
    # Handle missing values
    imputer = SimpleImputer(strategy='median')
    X = imputer.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Fit model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Store results
    results[dscr_col] = {
        'r2': r2,
        'rmse': rmse,
        'coefficient': model.coef_[0],
        'intercept': model.intercept_
    }
    
    # Create subplot
    plt.subplot(2, 2, i)
    plt.scatter(X_test, y_test, alpha=0.5, label='Actual')
    plt.plot(X_test, y_pred, color='red', label='Predicted')
    plt.xlabel(dscr_col)
    plt.ylabel('Heron Score')
    plt.title(f'DSCR vs Heron Score\nR² = {r2:.3f}, RMSE = {rmse:.3f}')
    plt.legend()

plt.tight_layout()
plt.savefig('Check score/dscr_analysis.png')
plt.close()

# Print detailed results
print("\nDetailed Analysis Results:")
print("-" * 50)
for dscr_col, metrics in results.items():
    print(f"\n{dscr_col}:")
    print(f"R² Score: {metrics['r2']:.3f}")
    print(f"RMSE: {metrics['rmse']:.3f}")
    print(f"Coefficient: {metrics['coefficient']:.3f}")
    print(f"Intercept: {metrics['intercept']:.3f}")
    print(f"Equation: Heron Score = {metrics['coefficient']:.3f} × DSCR + {metrics['intercept']:.3f}") 