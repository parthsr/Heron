import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
# from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 1. Load the wide-format metrics file
df_wide = pd.read_csv('./company_metrics_wide_normalized.csv')

# Drop only the heron_id column
if 'heron_id' in df_wide.columns:
    df_wide = df_wide.drop(columns=['heron_id'])

# 2. Identify the target and the key feature we're stress‑testing
TARGET_COL = 'heron_score_latest'
DROP_COL   = 'confidence_latest'

X_full = df_wide.drop(columns=[TARGET_COL])
y      = df_wide[TARGET_COL]

# 3a. Surrogate model WITH confidence_latest
X_train, X_test, y_train, y_test = train_test_split(
    X_full, y, test_size=0.3, random_state=42)

pipe_full = Pipeline([
    ('imp', SimpleImputer(strategy='median')),
    ('lr',  LinearRegression()),
])
pipe_full.fit(X_train, y_train)
pred_full = pipe_full.predict(X_test)
r2_full = r2_score(y_test, pred_full)

# 3b. Surrogate model WITHOUT confidence_latest
X_no_conf = X_full.drop(columns=[DROP_COL])
Xtr2, Xts2, ytr2, yts2 = train_test_split(
    X_no_conf, y, test_size=0.3, random_state=42)

pipe_nc = Pipeline([
    ('imp', SimpleImputer(strategy='median')),
    ('lr',  LinearRegression()),
])
pipe_nc.fit(Xtr2, ytr2)
pred_nc = pipe_nc.predict(Xts2)
r2_nc = r2_score(yts2, pred_nc)

# 4. Report
print(f"R² WITH  {DROP_COL}: {r2_full:0.3f}")
print(f"R² WITHOUT {DROP_COL}: {r2_nc:0.3f}")
print(f"ΔR² (drop-column importance): {r2_full - r2_nc:+0.3f}")
