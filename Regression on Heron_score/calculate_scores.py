import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# ------------------------------------------------------------------
# Load the raw, wide-format company metrics that you uploaded earlier
# ------------------------------------------------------------------
raw_path = "/mnt/data/company_metrics_wide.csv"
df = pd.read_csv(raw_path)

# ------------------------------------------------------
# Utility: normalise a list of columns with given scaler
# ------------------------------------------------------
def normalise_columns(frame, cols, *, use_log, scaler_cls):
    """
    Normalise the columns `cols` of `frame` in-place.

    Parameters
    ----------
    frame : pandas.DataFrame  – the data to edit.
    cols  : iterable[str]     – column names to process.
    use_log : bool            – apply log1p when skew > 1.
    scaler_cls : sklearn scaler class – MinMaxScaler, StandardScaler, …
    """
    for col in cols:
        if col not in frame.columns:
            continue

        # ensure numeric (silently converts non-numeric to NaN)
        s = pd.to_numeric(frame[col], errors="coerce").astype(float)

        # shift negatives so min ≥ 0
        if s.min(skipna=True) < 0:
            s = s - s.min(skipna=True)

        # optional log-transform for right-skewed data
        if use_log and s.skew(skipna=True) > 1:
            s = np.log1p(s)

        # fit-transform with a *fresh* scaler each time
        scaler = scaler_cls()
        # reshape needed because scalers expect 2-D array
        scaled = scaler.fit_transform(s.values.reshape(-1, 1)).flatten()

        frame[col] = scaled

    return frame


# ---------------------------------------------
# 1. Detect which columns belong to which block
# ---------------------------------------------
financial_prefixes = [
    "annualized_revenue",
    "balance_average",
    "balance_minimum",
    "latest_balance",
    "inflow_amount",
    "outflows",
    "revenue",
    "tax_payment_amount",
    "gross_operating_cashflow",
    "net_operating_cashflow",
]

fin_cols   = [c for c in df.columns if any(c.startswith(p) for p in financial_prefixes)]
growth_cols = [c for c in df.columns if c.endswith("_growth_rate")]
count_cols  = [
    c for c in df.columns
    if c.endswith("_count") or c.endswith("_days") or c in ["inflows", "outflows", "tax_payments"]
]

# --------------------------------------------------
# 2. Apply the three different normalisation schemes
# --------------------------------------------------
df = normalise_columns(df, fin_cols,   use_log=True,  scaler_cls=MinMaxScaler)
df = normalise_columns(df, growth_cols, use_log=False, scaler_cls=StandardScaler)
df = normalise_columns(df, count_cols,  use_log=True,  scaler_cls=MinMaxScaler)

# ------------------------------------------------------
# 3. Save the fully-normalised data for you to download
# ------------------------------------------------------
output_path = "/mnt/data/company_metrics_wide_normalized_fixed.csv"
df.to_csv(output_path, float_format="%.9f", index=False)

output_path
