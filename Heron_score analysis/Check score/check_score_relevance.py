import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
# from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.decomposition import PCA

# 1. Load the wide-format metrics file
df_wide = pd.read_csv('./company_metrics_wide.csv')

# Drop only the heron_id column
if 'heron_id' in df_wide.columns:
    df_wide = df_wide.drop(columns=['heron_id'])

# 2. Identify the target and the key feature we're stress‑testing
TARGET_COL = 'heron_score_latest'
DROP_COL   = 'confidence_latest'

X_full = df_wide.drop(columns=[TARGET_COL])
y      = df_wide[TARGET_COL]

# 3a. Baseline Linear Regression WITH confidence_latest
X_train, X_test, y_train, y_test = train_test_split(
    X_full, y, test_size=0.2, random_state=30)

pipe_full = Pipeline([
    ('imp', SimpleImputer(strategy='median')),
    ('lr',  LinearRegression()),
])
pipe_full.fit(X_train, y_train)
pred_full = pipe_full.predict(X_test)
r2_full = r2_score(y_test, pred_full)

# 3b. Linear Regression WITHOUT confidence_latest
X_without_confidence = X_full.drop(columns=[DROP_COL])
X_train_without, X_test_without, y_train, y_test = train_test_split(
    X_without_confidence, y, test_size=0.3, random_state=30)

pipe_without = Pipeline([
    ('imp', SimpleImputer(strategy='median')),
    ('lr', LinearRegression()),
])
pipe_without.fit(X_train_without, y_train)
pred_without = pipe_without.predict(X_test_without)
r2_without = r2_score(y_test, pred_without)

# 4. Report
print(f"Baseline Linear Regression R² WITH {DROP_COL}: {r2_full:0.3f}")
print(f"Linear Regression R² WITHOUT {DROP_COL}: {r2_without:0.3f}")
