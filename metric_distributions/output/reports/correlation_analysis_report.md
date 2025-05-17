# Metric Correlation Analysis

## Correlations for Date Range: last_365_days

### Strong Correlations

| Metric 1 | Group | Metric 2 | Group | Correlation |
|----------|-------|----------|-------|-------------|
| balance_average | balance | balance_minimum | balance | 0.989 |
| net_operating_cashflow_daily_average | profit_and_loss | opex_daily_average | profit_and_loss | -0.979 |
| nsf_days | risk_flag | nsf_fees | risk_flag | 0.948 |
| opex_daily_average | profit_and_loss | outflow_daily_average | balance | -0.938 |
| inflow_daily_average | balance | revenue_daily_average | profit_and_loss | 0.898 |
| net_operating_cashflow_daily_average | profit_and_loss | outflow_daily_average | balance | 0.897 |
| gross_operating_cashflow_daily_average | profit_and_loss | revenue_daily_average | profit_and_loss | 0.853 |
| cogs_daily_average | profit_and_loss | inflow_daily_average | balance | 0.752 |

#### Correlations with BALANCE metrics

- balance_average (balance) and balance_minimum (balance): 0.989
- opex_daily_average (profit_and_loss) and outflow_daily_average (balance): -0.938
- inflow_daily_average (balance) and revenue_daily_average (profit_and_loss): 0.898
- net_operating_cashflow_daily_average (profit_and_loss) and outflow_daily_average (balance): 0.897
- cogs_daily_average (profit_and_loss) and inflow_daily_average (balance): 0.752

#### Correlations with PROFIT_AND_LOSS metrics

- net_operating_cashflow_daily_average (profit_and_loss) and opex_daily_average (profit_and_loss): -0.979
- opex_daily_average (profit_and_loss) and outflow_daily_average (balance): -0.938
- inflow_daily_average (balance) and revenue_daily_average (profit_and_loss): 0.898
- net_operating_cashflow_daily_average (profit_and_loss) and outflow_daily_average (balance): 0.897
- gross_operating_cashflow_daily_average (profit_and_loss) and revenue_daily_average (profit_and_loss): 0.853
- cogs_daily_average (profit_and_loss) and inflow_daily_average (balance): 0.752

#### Correlations with RISK_FLAG metrics

- nsf_days (risk_flag) and nsf_fees (risk_flag): 0.948

## Correlations for Date Range: last_6_calendar_months

### Strong Correlations

| Metric 1 | Group | Metric 2 | Group | Correlation |
|----------|-------|----------|-------|-------------|
| annualized_revenue | profit_and_loss | annualized_revenue_profit_and_loss | profit_and_loss | 1.000 |
| cogs | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 1.000 |
| revenue | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| opex | profit_and_loss | opex_profit_and_loss | profit_and_loss | 1.000 |
| net_operating_cashflow | profit_and_loss | net_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 |
| gross_operating_cashflow | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 |
| revenue_monthly_average | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| net_operating_cashflow_profit_and_loss | profit_and_loss | opex_profit_and_loss | profit_and_loss | -0.979 |
| net_operating_cashflow_profit_and_loss | profit_and_loss | opex | profit_and_loss | -0.979 |
| net_operating_cashflow | profit_and_loss | opex_profit_and_loss | profit_and_loss | -0.979 |
| net_operating_cashflow | profit_and_loss | opex | profit_and_loss | -0.979 |
| inflow_amount | data_quality | revenue_monthly_average | profit_and_loss | 0.918 |
| inflow_amount | data_quality | revenue_profit_and_loss | profit_and_loss | 0.918 |
| inflow_amount | data_quality | revenue | profit_and_loss | 0.918 |
| annualized_revenue | profit_and_loss | inflow_amount | data_quality | 0.917 |
| annualized_revenue_profit_and_loss | profit_and_loss | inflow_amount | data_quality | 0.917 |
| annualized_revenue | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 0.868 |
| annualized_revenue_profit_and_loss | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 0.868 |
| annualized_revenue | profit_and_loss | gross_operating_cashflow | profit_and_loss | 0.868 |
| annualized_revenue_profit_and_loss | profit_and_loss | gross_operating_cashflow | profit_and_loss | 0.868 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.866 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 0.866 |
| gross_operating_cashflow | profit_and_loss | revenue | profit_and_loss | 0.866 |
| gross_operating_cashflow | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.866 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.866 |
| gross_operating_cashflow | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.866 |
| cogs_profit_and_loss | profit_and_loss | inflow_amount | data_quality | 0.768 |
| cogs | profit_and_loss | inflow_amount | data_quality | 0.768 |
| average_credit_card_spend | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 0.718 |
| average_credit_card_spend | profit_and_loss | cogs | profit_and_loss | 0.718 |

#### Correlations with DATA_QUALITY metrics

- inflow_amount (data_quality) and revenue_monthly_average (profit_and_loss): 0.918
- inflow_amount (data_quality) and revenue_profit_and_loss (profit_and_loss): 0.918
- inflow_amount (data_quality) and revenue (profit_and_loss): 0.918
- annualized_revenue (profit_and_loss) and inflow_amount (data_quality): 0.917
- annualized_revenue_profit_and_loss (profit_and_loss) and inflow_amount (data_quality): 0.917
- cogs_profit_and_loss (profit_and_loss) and inflow_amount (data_quality): 0.768
- cogs (profit_and_loss) and inflow_amount (data_quality): 0.768

#### Correlations with PROFIT_AND_LOSS metrics

- annualized_revenue (profit_and_loss) and annualized_revenue_profit_and_loss (profit_and_loss): 1.000
- cogs (profit_and_loss) and cogs_profit_and_loss (profit_and_loss): 1.000
- revenue (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- opex (profit_and_loss) and opex_profit_and_loss (profit_and_loss): 1.000
- net_operating_cashflow (profit_and_loss) and net_operating_cashflow_profit_and_loss (profit_and_loss): 1.000
- gross_operating_cashflow (profit_and_loss) and gross_operating_cashflow_profit_and_loss (profit_and_loss): 1.000
- revenue_monthly_average (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- revenue (profit_and_loss) and revenue_monthly_average (profit_and_loss): 1.000
- annualized_revenue_profit_and_loss (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- annualized_revenue (profit_and_loss) and revenue (profit_and_loss): 1.000

## Correlations for Date Range: last_90_days

### Strong Correlations

| Metric 1 | Group | Metric 2 | Group | Correlation |
|----------|-------|----------|-------|-------------|
| balance_average | balance | weekday_balance_average | balance | 1.000 |
| balance_average | balance | change_in_balance | balance | -0.991 |
| change_in_balance | balance | weekday_balance_average | balance | -0.990 |
| net_operating_cashflow_daily_average | profit_and_loss | opex_daily_average | profit_and_loss | -0.984 |
| nsf_days | risk_flag | nsf_fees | risk_flag | 0.941 |
| gross_operating_cashflow_daily_average | profit_and_loss | revenue_daily_average | profit_and_loss | 0.855 |
| negative_balance_days | risk_flag | negative_balance_days_by_account | risk_flag | 0.703 |
| cogs_daily_average | profit_and_loss | revenue_daily_average | profit_and_loss | 0.701 |

#### Correlations with BALANCE metrics

- balance_average (balance) and weekday_balance_average (balance): 1.000
- balance_average (balance) and change_in_balance (balance): -0.991
- change_in_balance (balance) and weekday_balance_average (balance): -0.990

#### Correlations with PROFIT_AND_LOSS metrics

- net_operating_cashflow_daily_average (profit_and_loss) and opex_daily_average (profit_and_loss): -0.984
- gross_operating_cashflow_daily_average (profit_and_loss) and revenue_daily_average (profit_and_loss): 0.855
- cogs_daily_average (profit_and_loss) and revenue_daily_average (profit_and_loss): 0.701

#### Correlations with RISK_FLAG metrics

- nsf_days (risk_flag) and nsf_fees (risk_flag): 0.941
- negative_balance_days (risk_flag) and negative_balance_days_by_account (risk_flag): 0.703

## Correlations for Date Range: last_30_days

### Strong Correlations

| Metric 1 | Group | Metric 2 | Group | Correlation |
|----------|-------|----------|-------|-------------|
| net_operating_cashflow_daily_average | profit_and_loss | opex_daily_average | profit_and_loss | -0.982 |
| balance_minimum | balance | change_in_balance | balance | -0.960 |
| balance_average | balance | debt_repayment_daily_average | debt | 0.944 |
| nsf_days | risk_flag | nsf_fees | risk_flag | 0.937 |
| gross_operating_cashflow_daily_average | profit_and_loss | revenue_daily_average | profit_and_loss | 0.908 |
| cogs_daily_average | profit_and_loss | revenue_daily_average | profit_and_loss | 0.734 |
| balance_average | balance | debt_investment | debt | 0.724 |
| debt_repayment_daily_average | debt | opex_daily_average | profit_and_loss | 0.708 |
| negative_balance_days | risk_flag | negative_balance_days_by_account | risk_flag | 0.708 |
| balance_average | balance | opex_daily_average | profit_and_loss | 0.707 |

#### Correlations with BALANCE metrics

- balance_minimum (balance) and change_in_balance (balance): -0.960
- balance_average (balance) and debt_repayment_daily_average (debt): 0.944
- balance_average (balance) and debt_investment (debt): 0.724
- balance_average (balance) and opex_daily_average (profit_and_loss): 0.707

#### Correlations with DEBT metrics

- balance_average (balance) and debt_repayment_daily_average (debt): 0.944
- balance_average (balance) and debt_investment (debt): 0.724
- debt_repayment_daily_average (debt) and opex_daily_average (profit_and_loss): 0.708

#### Correlations with PROFIT_AND_LOSS metrics

- net_operating_cashflow_daily_average (profit_and_loss) and opex_daily_average (profit_and_loss): -0.982
- gross_operating_cashflow_daily_average (profit_and_loss) and revenue_daily_average (profit_and_loss): 0.908
- cogs_daily_average (profit_and_loss) and revenue_daily_average (profit_and_loss): 0.734
- debt_repayment_daily_average (debt) and opex_daily_average (profit_and_loss): 0.708
- balance_average (balance) and opex_daily_average (profit_and_loss): 0.707

#### Correlations with RISK_FLAG metrics

- nsf_days (risk_flag) and nsf_fees (risk_flag): 0.937
- negative_balance_days (risk_flag) and negative_balance_days_by_account (risk_flag): 0.708

## Correlations for Date Range: last_180_days

### Strong Correlations

| Metric 1 | Group | Metric 2 | Group | Correlation |
|----------|-------|----------|-------|-------------|
| balance_average | balance | change_in_balance | balance | -0.992 |
| net_operating_cashflow_daily_average | profit_and_loss | opex_daily_average | profit_and_loss | -0.981 |
| nsf_days | risk_flag | nsf_fees | risk_flag | 0.956 |
| gross_operating_cashflow_daily_average | profit_and_loss | revenue_daily_average | profit_and_loss | 0.867 |
| negative_balance_days | risk_flag | negative_balance_days_by_account | risk_flag | 0.721 |

#### Correlations with BALANCE metrics

- balance_average (balance) and change_in_balance (balance): -0.992

#### Correlations with PROFIT_AND_LOSS metrics

- net_operating_cashflow_daily_average (profit_and_loss) and opex_daily_average (profit_and_loss): -0.981
- gross_operating_cashflow_daily_average (profit_and_loss) and revenue_daily_average (profit_and_loss): 0.867

#### Correlations with RISK_FLAG metrics

- nsf_days (risk_flag) and nsf_fees (risk_flag): 0.956
- negative_balance_days (risk_flag) and negative_balance_days_by_account (risk_flag): 0.721

## Correlations for Date Range: last_1_calendar_months

### Strong Correlations

| Metric 1 | Group | Metric 2 | Group | Correlation |
|----------|-------|----------|-------|-------------|
| annualized_revenue | profit_and_loss | annualized_revenue_profit_and_loss | profit_and_loss | 1.000 |
| gross_operating_cashflow | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 |
| net_operating_cashflow | profit_and_loss | net_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 |
| opex | profit_and_loss | opex_profit_and_loss | profit_and_loss | 1.000 |
| revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| revenue | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| revenue_monthly_average | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| cogs | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| net_operating_cashflow_profit_and_loss | profit_and_loss | opex | profit_and_loss | -0.984 |
| net_operating_cashflow | profit_and_loss | opex | profit_and_loss | -0.984 |
| net_operating_cashflow_profit_and_loss | profit_and_loss | opex_profit_and_loss | profit_and_loss | -0.984 |
| net_operating_cashflow | profit_and_loss | opex_profit_and_loss | profit_and_loss | -0.984 |
| annualized_revenue_profit_and_loss | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 0.853 |
| annualized_revenue_profit_and_loss | profit_and_loss | gross_operating_cashflow | profit_and_loss | 0.853 |
| annualized_revenue | profit_and_loss | gross_operating_cashflow | profit_and_loss | 0.853 |
| annualized_revenue | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 0.853 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.853 |
| gross_operating_cashflow | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.853 |
| gross_operating_cashflow | profit_and_loss | revenue | profit_and_loss | 0.853 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 0.853 |
| gross_operating_cashflow | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.853 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.853 |
| cogs | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.745 |
| cogs | profit_and_loss | revenue | profit_and_loss | 0.745 |
| cogs | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.745 |
| cogs_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.745 |
| cogs_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 0.745 |
| cogs_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.745 |
| annualized_revenue | profit_and_loss | cogs | profit_and_loss | 0.744 |
| annualized_revenue_profit_and_loss | profit_and_loss | cogs | profit_and_loss | 0.744 |
| annualized_revenue | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 0.744 |
| annualized_revenue_profit_and_loss | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 0.744 |

#### Correlations with PROFIT_AND_LOSS metrics

- annualized_revenue (profit_and_loss) and annualized_revenue_profit_and_loss (profit_and_loss): 1.000
- gross_operating_cashflow (profit_and_loss) and gross_operating_cashflow_profit_and_loss (profit_and_loss): 1.000
- net_operating_cashflow (profit_and_loss) and net_operating_cashflow_profit_and_loss (profit_and_loss): 1.000
- opex (profit_and_loss) and opex_profit_and_loss (profit_and_loss): 1.000
- revenue (profit_and_loss) and revenue_monthly_average (profit_and_loss): 1.000
- revenue (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- revenue_monthly_average (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- cogs (profit_and_loss) and cogs_profit_and_loss (profit_and_loss): 1.000
- annualized_revenue (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- annualized_revenue_profit_and_loss (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000

## Correlations for Date Range: last_3_calendar_months

### Strong Correlations

| Metric 1 | Group | Metric 2 | Group | Correlation |
|----------|-------|----------|-------|-------------|
| revenue_monthly_average | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| gross_operating_cashflow | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 |
| net_operating_cashflow | profit_and_loss | net_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 |
| opex | profit_and_loss | opex_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | annualized_revenue_profit_and_loss | profit_and_loss | 1.000 |
| revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| revenue | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| cogs | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| net_operating_cashflow_profit_and_loss | profit_and_loss | opex | profit_and_loss | -0.980 |
| net_operating_cashflow | profit_and_loss | opex | profit_and_loss | -0.980 |
| net_operating_cashflow_profit_and_loss | profit_and_loss | opex_profit_and_loss | profit_and_loss | -0.980 |
| net_operating_cashflow | profit_and_loss | opex_profit_and_loss | profit_and_loss | -0.980 |
| annualized_revenue_profit_and_loss | profit_and_loss | gross_operating_cashflow | profit_and_loss | 0.825 |
| annualized_revenue_profit_and_loss | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 0.825 |
| annualized_revenue | profit_and_loss | gross_operating_cashflow | profit_and_loss | 0.825 |
| annualized_revenue | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 0.825 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 0.825 |
| gross_operating_cashflow | profit_and_loss | revenue | profit_and_loss | 0.825 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.825 |
| gross_operating_cashflow | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.825 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.825 |
| gross_operating_cashflow | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.825 |

#### Correlations with PROFIT_AND_LOSS metrics

- revenue_monthly_average (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- gross_operating_cashflow (profit_and_loss) and gross_operating_cashflow_profit_and_loss (profit_and_loss): 1.000
- net_operating_cashflow (profit_and_loss) and net_operating_cashflow_profit_and_loss (profit_and_loss): 1.000
- opex (profit_and_loss) and opex_profit_and_loss (profit_and_loss): 1.000
- annualized_revenue (profit_and_loss) and annualized_revenue_profit_and_loss (profit_and_loss): 1.000
- revenue (profit_and_loss) and revenue_monthly_average (profit_and_loss): 1.000
- revenue (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- cogs (profit_and_loss) and cogs_profit_and_loss (profit_and_loss): 1.000
- annualized_revenue (profit_and_loss) and revenue (profit_and_loss): 1.000
- annualized_revenue_profit_and_loss (profit_and_loss) and revenue (profit_and_loss): 1.000

## Correlations for Date Range: last_12_calendar_months

### Strong Correlations

| Metric 1 | Group | Metric 2 | Group | Correlation |
|----------|-------|----------|-------|-------------|
| revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 |
| revenue_monthly_average | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| revenue | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| opex | profit_and_loss | opex_profit_and_loss | profit_and_loss | 1.000 |
| net_operating_cashflow | profit_and_loss | net_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 |
| gross_operating_cashflow | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 |
| cogs | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | annualized_revenue_profit_and_loss | profit_and_loss | 1.000 |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue | profit_and_loss | 1.000 |
| annualized_revenue | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 |
| net_operating_cashflow_profit_and_loss | profit_and_loss | opex_profit_and_loss | profit_and_loss | -0.977 |
| net_operating_cashflow_profit_and_loss | profit_and_loss | opex | profit_and_loss | -0.977 |
| net_operating_cashflow | profit_and_loss | opex_profit_and_loss | profit_and_loss | -0.977 |
| net_operating_cashflow | profit_and_loss | opex | profit_and_loss | -0.977 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.849 |
| annualized_revenue_profit_and_loss | profit_and_loss | gross_operating_cashflow | profit_and_loss | 0.849 |
| annualized_revenue | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 0.849 |
| gross_operating_cashflow | profit_and_loss | revenue | profit_and_loss | 0.849 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 0.849 |
| gross_operating_cashflow | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 0.849 |
| annualized_revenue | profit_and_loss | gross_operating_cashflow | profit_and_loss | 0.849 |
| annualized_revenue_profit_and_loss | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 0.849 |
| gross_operating_cashflow_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.849 |
| gross_operating_cashflow | profit_and_loss | revenue_monthly_average | profit_and_loss | 0.849 |
| average_credit_card_spend | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 0.702 |
| average_credit_card_spend | profit_and_loss | cogs | profit_and_loss | 0.702 |

#### Correlations with PROFIT_AND_LOSS metrics

- revenue (profit_and_loss) and revenue_monthly_average (profit_and_loss): 1.000
- annualized_revenue (profit_and_loss) and revenue_monthly_average (profit_and_loss): 1.000
- annualized_revenue_profit_and_loss (profit_and_loss) and revenue_monthly_average (profit_and_loss): 1.000
- revenue_monthly_average (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- annualized_revenue_profit_and_loss (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- revenue (profit_and_loss) and revenue_profit_and_loss (profit_and_loss): 1.000
- opex (profit_and_loss) and opex_profit_and_loss (profit_and_loss): 1.000
- net_operating_cashflow (profit_and_loss) and net_operating_cashflow_profit_and_loss (profit_and_loss): 1.000
- gross_operating_cashflow (profit_and_loss) and gross_operating_cashflow_profit_and_loss (profit_and_loss): 1.000
- cogs (profit_and_loss) and cogs_profit_and_loss (profit_and_loss): 1.000

## Correlations for Date Range: last_120_days

### Strong Correlations

| Metric 1 | Group | Metric 2 | Group | Correlation |
|----------|-------|----------|-------|-------------|
| net_operating_cashflow_daily_average | profit_and_loss | opex_daily_average | profit_and_loss | -0.982 |
| nsf_days | risk_flag | nsf_fees | risk_flag | 0.946 |
| gross_operating_cashflow_daily_average | profit_and_loss | revenue_daily_average | profit_and_loss | 0.848 |
| negative_balance_days | risk_flag | negative_balance_days_by_account | risk_flag | 0.711 |

#### Correlations with PROFIT_AND_LOSS metrics

- net_operating_cashflow_daily_average (profit_and_loss) and opex_daily_average (profit_and_loss): -0.982
- gross_operating_cashflow_daily_average (profit_and_loss) and revenue_daily_average (profit_and_loss): 0.848

#### Correlations with RISK_FLAG metrics

- nsf_days (risk_flag) and nsf_fees (risk_flag): 0.946
- negative_balance_days (risk_flag) and negative_balance_days_by_account (risk_flag): 0.711

## Correlations for Date Range: latest

## Correlations for Date Range: next_30_days

## Correlations for Date Range: next_60_days

## Correlations for Date Range: next_90_days

## Correlations for Date Range: next_180_days


## Top Correlations Across All Date Ranges

| Metric 1 | Group | Metric 2 | Group | Correlation | Date Range |
|----------|-------|----------|-------|-------------|------------|
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 | last_12_calendar_months |
| revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 | last_12_calendar_months |
| annualized_revenue | profit_and_loss | revenue_monthly_average | profit_and_loss | 1.000 | last_12_calendar_months |
| revenue_monthly_average | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 | last_12_calendar_months |
| annualized_revenue | profit_and_loss | annualized_revenue_profit_and_loss | profit_and_loss | 1.000 | last_1_calendar_months |
| revenue_monthly_average | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 | last_3_calendar_months |
| net_operating_cashflow | profit_and_loss | net_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 | last_1_calendar_months |
| net_operating_cashflow | profit_and_loss | net_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 | last_12_calendar_months |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue | profit_and_loss | 1.000 | last_12_calendar_months |
| gross_operating_cashflow | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 | last_6_calendar_months |
| annualized_revenue_profit_and_loss | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 | last_12_calendar_months |
| cogs | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 1.000 | last_6_calendar_months |
| cogs | profit_and_loss | cogs_profit_and_loss | profit_and_loss | 1.000 | last_12_calendar_months |
| gross_operating_cashflow | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 | last_12_calendar_months |
| annualized_revenue | profit_and_loss | revenue | profit_and_loss | 1.000 | last_12_calendar_months |
| annualized_revenue | profit_and_loss | annualized_revenue_profit_and_loss | profit_and_loss | 1.000 | last_12_calendar_months |
| opex | profit_and_loss | opex_profit_and_loss | profit_and_loss | 1.000 | last_6_calendar_months |
| net_operating_cashflow | profit_and_loss | net_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 | last_6_calendar_months |
| gross_operating_cashflow | profit_and_loss | gross_operating_cashflow_profit_and_loss | profit_and_loss | 1.000 | last_1_calendar_months |
| revenue | profit_and_loss | revenue_profit_and_loss | profit_and_loss | 1.000 | last_6_calendar_months |

## Metric Group Correlation Analysis


### Group Correlations for Date Range: last_365_days

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|

### Group Correlations for Date Range: last_6_calendar_months

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|
| profit_and_loss | data_quality | 0.549 |

### Group Correlations for Date Range: last_90_days

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|

### Group Correlations for Date Range: last_30_days

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|

### Group Correlations for Date Range: last_180_days

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|

### Group Correlations for Date Range: last_1_calendar_months

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|

### Group Correlations for Date Range: last_3_calendar_months

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|

### Group Correlations for Date Range: last_12_calendar_months

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|

### Group Correlations for Date Range: last_120_days

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|

### Group Correlations for Date Range: latest

Strong correlations between metric groups:

| Group 1 | Group 2 | Average Correlation |
|---------|---------|---------------------|
