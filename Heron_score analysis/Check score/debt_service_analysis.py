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
analysis_columns = [col for col in df.columns if 'debt_service_coverage_ratio' in col]
target_cols = ['predicted_nsf_fees_next_30_days', 'predicted_nsf_fees_next_60_days', 'predicted_nsf_fees_next_90_days']

# Analyze each target metric against DSCR columns
for target_col in target_cols:
    print(f"\nAnalyzing {target_col} against DSCR columns...")
    # Determine grid size for subplots dynamically
    num_independent_vars = len(analysis_columns)
    n_rows = int(np.ceil(num_independent_vars / 2))
    n_cols = 2
    plt.figure(figsize=(15, n_rows * 5)) # Adjust figure size based on number of rows

    # Dictionary to store results for the current target variable
    results = {}

    # Analyze each DSCR metric
    for i, col_to_analyze in enumerate(analysis_columns, 1):
        # Prepare data
        X = df[[col_to_analyze]].values
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
        results[col_to_analyze] = {
            'r2': r2,
            'rmse': rmse,
            'coefficient': model.coef_[0],
            'intercept': model.intercept_
        }

        # Create subplot
        plt.subplot(n_rows, n_cols, i)
        plt.scatter(X_test, y_test, alpha=0.5, label='Actual')
        plt.plot(X_test, y_pred, color='red', label='Predicted')
        plt.xlabel(col_to_analyze)
        plt.ylabel(target_col) # Use the current target column name for ylabel
        plt.title(f'{col_to_analyze} vs {target_col}\nR² = {r2:.3f}, RMSE = {rmse:.3f}') # Use current target column name in title
        plt.legend()

    plt.tight_layout()
    # Save figure with a filename indicating the target variable
    plt.savefig(f'Check score/dscr_vs_{target_col}_analysis.png')
    plt.close()

    # Print detailed results for the current target variable
    print(f"\nDetailed Analysis Results for {target_col}:")
    print("-" * 50)
    for col_to_analyze, metrics in results.items():
        print(f"\n{col_to_analyze}:")
        print(f"R² Score: {metrics['r2']:.3f}")
        print(f"RMSE: {metrics['rmse']:.3f}")
        print(f"Coefficient: {metrics['coefficient']:.3f}")
        print(f"Intercept: {metrics['intercept']:.3f}")
        print(f"Equation: {target_col} = {metrics['coefficient']:.3f} × {col_to_analyze} + {metrics['intercept']:.3f}") 