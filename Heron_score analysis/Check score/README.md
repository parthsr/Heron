# Feature Selection Analysis for Heron Score Prediction

## Model Performance Comparison

| Model | R² Score |
|-------|----------|
| Baseline Linear Regression (all features) | -0.826 |
| SelectKBest (k=20) | 0.354 |
| PCA (n_components=20) | -0.034 |

## Impact of confidence_latest Feature

Analysis of the importance of the `confidence_latest` feature:

| Model Configuration | R² Score |
|---------------------|----------|
| With confidence_latest | 0.298 |
| Without confidence_latest | -0.003 |

This analysis shows that `confidence_latest` is a critical feature for model performance. Removing it causes the model to perform worse than random guessing (negative R²), while including it provides a moderate positive R² score of 0.298.

## Top 20 Selected Features

The following features were selected by SelectKBest as the most predictive for `heron_score_latest`:

1. confidence_latest
2. debt_service_coverage_ratio_last_12_calendar_months
3. debt_service_coverage_ratio_last_3_calendar_months
4. debt_service_coverage_ratio_last_6_calendar_months
5. gross_operating_cashflow_daily_average_last_120_days
6. gross_operating_cashflow_daily_average_last_180_days
7. gross_operating_cashflow_daily_average_last_365_days
8. net_operating_cashflow_daily_average_last_120_days
9. net_operating_cashflow_daily_average_last_365_days
10. revenue_daily_average_last_120_days
11. revenue_daily_average_last_180_days
12. revenue_daily_average_last_30_days
13. revenue_daily_average_last_365_days
14. revenue_daily_average_last_90_days
15. revenue_last_3_calendar_months
16. revenue_monthly_average_last_12_calendar_months
17. revenue_monthly_average_last_3_calendar_months
18. revenue_profit_and_loss_last_3_calendar_months
19. tax_payments_last_365_days
20. unconnected_account_ratio_last_365_days

## Key Observations

1. Feature selection significantly improved model performance, changing R² from -0.826 to 0.354
2. The selected features are primarily related to:
   - Cash flow metrics
   - Revenue metrics
   - Debt service coverage ratios
   - Tax payments
   - Account connectivity

## Methodology

- Used SelectKBest with f_regression scoring function
- Selected top 20 features based on statistical significance
- Applied SimpleImputer for handling missing values
- Used Linear Regression as the base model 