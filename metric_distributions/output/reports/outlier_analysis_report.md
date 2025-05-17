# Outlier Analysis Report
## BALANCE METRICS
## DATA_QUALITY METRICS
## DEBT METRICS
### debt_service_coverage_ratio (ratio)
**Description**: Net income / Debt repayment; how many times can debt be repaid
#### Z-score Outliers (threshold=3.0)
Found 2 outliers using Z-score method.
Top outliers:
1. Value: -621609.38 (ratio), Date Range: last_12_calendar_months, Z-score: 62.87
2. Value: -58859.33 (ratio), Date Range: last_3_calendar_months, Z-score: 5.94

#### IQR Outliers (threshold=1.5)
Found 1293 outliers using IQR method.
Top outliers:
1. Value: -621609.38 (ratio), Date Range: last_12_calendar_months, IQR Distance: 336576.29
2. Value: -58859.33 (ratio), Date Range: last_3_calendar_months, IQR Distance: 31869.54
3. Value: 18465.12 (ratio), Date Range: last_6_calendar_months, IQR Distance: 9997.57
4. Value: 18111.41 (ratio), Date Range: last_3_calendar_months, IQR Distance: 9806.05
5. Value: -9155.08 (ratio), Date Range: last_3_calendar_months, IQR Distance: 4956.66

## HERON METRICS
### merchant_heron_ids (array)
**Description**: The merchant heron ids

### predicted_nsf_fees (probability)
**Description**: The likelihood that the company will incur 1 or more NSF fees, based on current scorecard metrics
#### Z-score Outliers (threshold=3.0)
Found 138 outliers using Z-score method.
Top outliers:
1. Value: 0.99 (probability), Date Range: next_90_days, Z-score: 4.02
2. Value: 0.99 (probability), Date Range: next_90_days, Z-score: 4.01
3. Value: 0.99 (probability), Date Range: next_90_days, Z-score: 4.00
4. Value: 0.99 (probability), Date Range: next_90_days, Z-score: 4.00
5. Value: 0.99 (probability), Date Range: next_90_days, Z-score: 4.00

#### IQR Outliers (threshold=1.5)
Found 458 outliers using IQR method.
Top outliers:
1. Value: 0.99 (probability), Date Range: next_90_days, IQR Distance: 14.31
2. Value: 0.99 (probability), Date Range: next_90_days, IQR Distance: 14.28
3. Value: 0.99 (probability), Date Range: next_90_days, IQR Distance: 14.24
4. Value: 0.99 (probability), Date Range: next_90_days, IQR Distance: 14.24
5. Value: 0.99 (probability), Date Range: next_90_days, IQR Distance: 14.24

### predicted_balance_daily_average (amount)
**Description**: The predicted daily average balance
#### Z-score Outliers (threshold=3.0)
Found 6 outliers using Z-score method.
Top outliers:
1. Value: 182581794.50 (amount), Date Range: next_30_days, Z-score: 29.58
2. Value: 182581794.50 (amount), Date Range: next_60_days, Z-score: 29.58
3. Value: 182581794.50 (amount), Date Range: next_90_days, Z-score: 29.58
4. Value: -67491219.27 (amount), Date Range: next_30_days, Z-score: 10.97
5. Value: -67491219.27 (amount), Date Range: next_60_days, Z-score: 10.97

#### IQR Outliers (threshold=1.5)
Found 366 outliers using IQR method.
Top outliers:
1. Value: 182581794.50 (amount), Date Range: next_60_days, IQR Distance: 8145.38
2. Value: 182581794.50 (amount), Date Range: next_90_days, IQR Distance: 8145.38
3. Value: 182581794.50 (amount), Date Range: next_30_days, IQR Distance: 8145.38
4. Value: -67491219.27 (amount), Date Range: next_90_days, IQR Distance: 3011.34
5. Value: -67491219.27 (amount), Date Range: next_60_days, IQR Distance: 3011.34

### heron_score (n)
**Description**: The likelihood that the company will default, based on current scorecard metrics

#### IQR Outliers (threshold=1.5)
Found 38 outliers using IQR method.
Top outliers:
1. Value: 985.00 (n), Date Range: latest, IQR Distance: 1.67
2. Value: 983.00 (n), Date Range: latest, IQR Distance: 1.67
3. Value: 979.00 (n), Date Range: latest, IQR Distance: 1.65
4. Value: 978.00 (n), Date Range: latest, IQR Distance: 1.65
5. Value: 978.00 (n), Date Range: latest, IQR Distance: 1.65

### distinct_mcas_from_outflows (n)
**Description**: The number of distinct MCAs extracted from outflow transactions

### distinct_mcas_from_inflows (n)
**Description**: The number of distinct MCAs extracted from inflow transactions

## PROCESSING_QUALITY METRICS
### category_coverage (ratio)
**Description**: The ratio of transactions that have a category label

### merchant_coverage (ratio)
**Description**: The ratio of transactions that have a merchant label
#### Z-score Outliers (threshold=3.0)
Found 1 outliers using Z-score method.
Top outliers:
1. Value: 0.85 (ratio), Date Range: latest, Z-score: 3.21

#### IQR Outliers (threshold=1.5)
Found 1 outliers using IQR method.
Top outliers:
1. Value: 0.85 (ratio), Date Range: latest, IQR Distance: 1.52

### unconnected_account_ratio (ratio)
**Description**: The total amount value of intra-company accounts normalised by total amount of revenue
#### Z-score Outliers (threshold=3.0)
Found 3 outliers using Z-score method.
Top outliers:
1. Value: 1656.92 (ratio), Date Range: last_365_days, Z-score: 24.39
2. Value: 1221.10 (ratio), Date Range: last_365_days, Z-score: 17.95
3. Value: 560.48 (ratio), Date Range: last_365_days, Z-score: 8.20

#### IQR Outliers (threshold=1.5)
Found 117 outliers using IQR method.
Top outliers:
1. Value: 1656.92 (ratio), Date Range: last_365_days, IQR Distance: 3294.17
2. Value: 1221.10 (ratio), Date Range: last_365_days, IQR Distance: 2427.44
3. Value: 560.48 (ratio), Date Range: last_365_days, IQR Distance: 1113.62
4. Value: 150.01 (ratio), Date Range: last_365_days, IQR Distance: 297.30
5. Value: 109.96 (ratio), Date Range: last_365_days, IQR Distance: 217.65

## PROFIT_AND_LOSS METRICS
### revenue_daily_average (amount)
**Description**: Average revenue (per day) across transactions with categories in the 'revenue' analytics group
#### Z-score Outliers (threshold=3.0)
Found 137 outliers using Z-score method.
Top outliers:
1. Value: 75295.98 (amount), Date Range: last_30_days, Z-score: 25.85
2. Value: 53131.03 (amount), Date Range: last_90_days, Z-score: 18.16
3. Value: 52157.41 (amount), Date Range: last_30_days, Z-score: 17.82
4. Value: 50804.43 (amount), Date Range: last_120_days, Z-score: 17.35
5. Value: 49802.70 (amount), Date Range: last_30_days, Z-score: 17.00

#### IQR Outliers (threshold=1.5)
Found 1319 outliers using IQR method.
Top outliers:
1. Value: 75295.98 (amount), Date Range: last_30_days, IQR Distance: 159.58
2. Value: 53131.03 (amount), Date Range: last_90_days, IQR Distance: 112.31
3. Value: 52157.41 (amount), Date Range: last_30_days, IQR Distance: 110.23
4. Value: 50804.43 (amount), Date Range: last_120_days, IQR Distance: 107.35
5. Value: 49802.70 (amount), Date Range: last_30_days, IQR Distance: 105.21

### cogs_daily_average (amount)
**Description**: Average cogs (per day) for transactions with categories in the 'cost of goods sold' analytics group`
#### Z-score Outliers (threshold=3.0)
Found 19 outliers using Z-score method.
Top outliers:
1. Value: 46291.08 (amount), Date Range: last_120_days, Z-score: 24.22
2. Value: 45384.25 (amount), Date Range: last_30_days, Z-score: 23.74
3. Value: 44043.96 (amount), Date Range: last_90_days, Z-score: 23.04
4. Value: 40399.90 (amount), Date Range: last_180_days, Z-score: 21.12
5. Value: 40043.07 (amount), Date Range: last_120_days, Z-score: 20.93

#### IQR Outliers (threshold=1.5)
Found 830 outliers using IQR method.
Top outliers:
1. Value: 46291.08 (amount), Date Range: last_120_days, IQR Distance: 2183.36
2. Value: 45384.25 (amount), Date Range: last_30_days, IQR Distance: 2140.57
3. Value: 44043.96 (amount), Date Range: last_90_days, IQR Distance: 2077.33
4. Value: 40399.90 (amount), Date Range: last_180_days, IQR Distance: 1905.37
5. Value: 40043.07 (amount), Date Range: last_120_days, IQR Distance: 1888.53

### opex_daily_average (amount)
**Description**: Average opex (per day) for transactions with categories in the 'operational expenses' analytics group
#### Z-score Outliers (threshold=3.0)
Found 25 outliers using Z-score method.
Top outliers:
1. Value: 345146.76 (amount), Date Range: last_30_days, Z-score: 24.18
2. Value: 323409.84 (amount), Date Range: last_30_days, Z-score: 22.65
3. Value: 316520.14 (amount), Date Range: last_90_days, Z-score: 22.17
4. Value: 302296.00 (amount), Date Range: last_180_days, Z-score: 21.16
5. Value: 294005.19 (amount), Date Range: last_120_days, Z-score: 20.58

#### IQR Outliers (threshold=1.5)
Found 610 outliers using IQR method.
Top outliers:
1. Value: 345146.76 (amount), Date Range: last_30_days, IQR Distance: 333.71
2. Value: 323409.84 (amount), Date Range: last_30_days, IQR Distance: 312.62
3. Value: 316520.14 (amount), Date Range: last_90_days, IQR Distance: 305.94
4. Value: 302296.00 (amount), Date Range: last_180_days, IQR Distance: 292.14
5. Value: 294005.19 (amount), Date Range: last_120_days, IQR Distance: 284.09

### revenue_sources (n)
**Description**: Count of distinct merchants with categories in the 'revenue' analytics group
#### Z-score Outliers (threshold=3.0)
Found 22 outliers using Z-score method.
Top outliers:
1. Value: 25.00 (n), Date Range: last_365_days, Z-score: 8.91
2. Value: 19.00 (n), Date Range: last_365_days, Z-score: 6.60
3. Value: 17.00 (n), Date Range: last_365_days, Z-score: 5.83
4. Value: 17.00 (n), Date Range: last_365_days, Z-score: 5.83
5. Value: 16.00 (n), Date Range: last_365_days, Z-score: 5.44

#### IQR Outliers (threshold=1.5)
Found 41 outliers using IQR method.
Top outliers:
1. Value: 25.00 (n), Date Range: last_365_days, IQR Distance: 7.33
2. Value: 19.00 (n), Date Range: last_365_days, IQR Distance: 5.33
3. Value: 17.00 (n), Date Range: last_365_days, IQR Distance: 4.67
4. Value: 17.00 (n), Date Range: last_365_days, IQR Distance: 4.67
5. Value: 16.00 (n), Date Range: last_365_days, IQR Distance: 4.33

### revenue (amount)
**Description**: All transactions associated to categories in the 'revenue' analytics group
#### Z-score Outliers (threshold=3.0)
Found 63 outliers using Z-score method.
Top outliers:
1. Value: 14562046.58 (amount), Date Range: last_12_calendar_months, Z-score: 19.73
2. Value: 14307805.03 (amount), Date Range: last_12_calendar_months, Z-score: 19.38
3. Value: 9948327.87 (amount), Date Range: last_12_calendar_months, Z-score: 13.37
4. Value: 9554127.53 (amount), Date Range: last_12_calendar_months, Z-score: 12.83
5. Value: 9288053.34 (amount), Date Range: last_12_calendar_months, Z-score: 12.46

#### IQR Outliers (threshold=1.5)
Found 510 outliers using IQR method.
Top outliers:
1. Value: 14562046.58 (amount), Date Range: last_12_calendar_months, IQR Distance: 85.05
2. Value: 14307805.03 (amount), Date Range: last_12_calendar_months, IQR Distance: 83.55
3. Value: 9948327.87 (amount), Date Range: last_12_calendar_months, IQR Distance: 57.77
4. Value: 9554127.53 (amount), Date Range: last_12_calendar_months, IQR Distance: 55.44
5. Value: 9288053.34 (amount), Date Range: last_12_calendar_months, IQR Distance: 53.87

### annualized_revenue (amount)
**Description**: The annualized amount for all transactions with categories in the 'revenue' analytics group
#### Z-score Outliers (threshold=3.0)
Found 72 outliers using Z-score method.
Top outliers:
1. Value: 24156677.49 (amount), Date Range: last_1_calendar_months, Z-score: 18.07
2. Value: 17848284.77 (amount), Date Range: last_3_calendar_months, Z-score: 13.25
3. Value: 17667180.97 (amount), Date Range: last_3_calendar_months, Z-score: 13.11
4. Value: 17595688.40 (amount), Date Range: last_1_calendar_months, Z-score: 13.06
5. Value: 16627631.39 (amount), Date Range: last_6_calendar_months, Z-score: 12.32

#### IQR Outliers (threshold=1.5)
Found 464 outliers using IQR method.
Top outliers:
1. Value: 24156677.49 (amount), Date Range: last_1_calendar_months, IQR Distance: 55.44
2. Value: 17848284.77 (amount), Date Range: last_3_calendar_months, IQR Distance: 40.68
3. Value: 17667180.97 (amount), Date Range: last_3_calendar_months, IQR Distance: 40.25
4. Value: 17595688.40 (amount), Date Range: last_1_calendar_months, IQR Distance: 40.09
5. Value: 16627631.39 (amount), Date Range: last_6_calendar_months, IQR Distance: 37.82

### cogs (amount)
**Description**: The total amount from all transactions with categories in the 'cost of goods sold' analytics group
#### Z-score Outliers (threshold=3.0)
Found 19 outliers using Z-score method.
Top outliers:
1. Value: 14082378.88 (amount), Date Range: last_12_calendar_months, Z-score: 37.79
2. Value: 12769082.26 (amount), Date Range: last_12_calendar_months, Z-score: 34.26
3. Value: 7129642.54 (amount), Date Range: last_6_calendar_months, Z-score: 19.09
4. Value: 6974767.16 (amount), Date Range: last_6_calendar_months, Z-score: 18.68
5. Value: 4921562.92 (amount), Date Range: last_12_calendar_months, Z-score: 13.15

#### IQR Outliers (threshold=1.5)
Found 650 outliers using IQR method.
Top outliers:
1. Value: 14082378.88 (amount), Date Range: last_12_calendar_months, IQR Distance: 4252.86
2. Value: 12769082.26 (amount), Date Range: last_12_calendar_months, IQR Distance: 3856.15
3. Value: 7129642.54 (amount), Date Range: last_6_calendar_months, IQR Distance: 2152.65
4. Value: 6974767.16 (amount), Date Range: last_6_calendar_months, IQR Distance: 2105.86
5. Value: 4921562.92 (amount), Date Range: last_12_calendar_months, IQR Distance: 1485.65

### average_credit_card_spend (amount)
**Description**: Average credit card spend for the last X full calendar months
#### Z-score Outliers (threshold=3.0)
Found 18 outliers using Z-score method.
Top outliers:
1. Value: 1265492.58 (amount), Date Range: last_12_calendar_months, Z-score: 32.16
2. Value: 1174497.97 (amount), Date Range: last_6_calendar_months, Z-score: 29.84
3. Value: 1075608.25 (amount), Date Range: last_3_calendar_months, Z-score: 27.31
4. Value: 1072373.59 (amount), Date Range: last_1_calendar_months, Z-score: 27.23
5. Value: 269017.58 (amount), Date Range: last_3_calendar_months, Z-score: 6.71

#### IQR Outliers (threshold=1.5)
Found 437 outliers using IQR method.
Top outliers:
1. Value: 1265492.58 (amount), Date Range: last_12_calendar_months, IQR Distance: 307.92
2. Value: 1174497.97 (amount), Date Range: last_6_calendar_months, IQR Distance: 285.70
3. Value: 1075608.25 (amount), Date Range: last_3_calendar_months, IQR Distance: 261.56
4. Value: 1072373.59 (amount), Date Range: last_1_calendar_months, IQR Distance: 260.77
5. Value: 269017.58 (amount), Date Range: last_3_calendar_months, IQR Distance: 64.67

### opex (amount)
**Description**: The total amount from transactions with categories in the 'operational expenses' analytics group
#### Z-score Outliers (threshold=3.0)
Found 18 outliers using Z-score method.
Top outliers:
1. Value: 100808471.30 (amount), Date Range: last_12_calendar_months, Z-score: 38.55
2. Value: 65313155.83 (amount), Date Range: last_12_calendar_months, Z-score: 24.93
3. Value: 61266587.85 (amount), Date Range: last_12_calendar_months, Z-score: 23.38
4. Value: 52027840.29 (amount), Date Range: last_6_calendar_months, Z-score: 19.83
5. Value: 37525883.53 (amount), Date Range: last_6_calendar_months, Z-score: 14.27

#### IQR Outliers (threshold=1.5)
Found 521 outliers using IQR method.
Top outliers:
1. Value: 100808471.30 (amount), Date Range: last_12_calendar_months, IQR Distance: 639.87
2. Value: 65313155.83 (amount), Date Range: last_12_calendar_months, IQR Distance: 414.18
3. Value: 61266587.85 (amount), Date Range: last_12_calendar_months, IQR Distance: 388.46
4. Value: 52027840.29 (amount), Date Range: last_6_calendar_months, IQR Distance: 329.71
5. Value: 37525883.53 (amount), Date Range: last_6_calendar_months, IQR Distance: 237.51

### revenue_profit_and_loss (amount)
**Description**: Total revenue from P&L view
#### Z-score Outliers (threshold=3.0)
Found 63 outliers using Z-score method.
Top outliers:
1. Value: 14562046.58 (amount), Date Range: last_12_calendar_months, Z-score: 19.73
2. Value: 14307805.03 (amount), Date Range: last_12_calendar_months, Z-score: 19.38
3. Value: 9948327.87 (amount), Date Range: last_12_calendar_months, Z-score: 13.37
4. Value: 9554127.53 (amount), Date Range: last_12_calendar_months, Z-score: 12.83
5. Value: 9288053.34 (amount), Date Range: last_12_calendar_months, Z-score: 12.46

#### IQR Outliers (threshold=1.5)
Found 510 outliers using IQR method.
Top outliers:
1. Value: 14562046.58 (amount), Date Range: last_12_calendar_months, IQR Distance: 85.05
2. Value: 14307805.03 (amount), Date Range: last_12_calendar_months, IQR Distance: 83.55
3. Value: 9948327.87 (amount), Date Range: last_12_calendar_months, IQR Distance: 57.77
4. Value: 9554127.53 (amount), Date Range: last_12_calendar_months, IQR Distance: 55.44
5. Value: 9288053.34 (amount), Date Range: last_12_calendar_months, IQR Distance: 53.87

### annualized_revenue_profit_and_loss (amount)
**Description**: the daily average revenue for the date range multiplied by 365 from P&L view
#### Z-score Outliers (threshold=3.0)
Found 72 outliers using Z-score method.
Top outliers:
1. Value: 24156677.49 (amount), Date Range: last_1_calendar_months, Z-score: 18.07
2. Value: 17848284.77 (amount), Date Range: last_3_calendar_months, Z-score: 13.25
3. Value: 17667180.97 (amount), Date Range: last_3_calendar_months, Z-score: 13.11
4. Value: 17595688.40 (amount), Date Range: last_1_calendar_months, Z-score: 13.06
5. Value: 16627631.39 (amount), Date Range: last_6_calendar_months, Z-score: 12.32

#### IQR Outliers (threshold=1.5)
Found 464 outliers using IQR method.
Top outliers:
1. Value: 24156677.49 (amount), Date Range: last_1_calendar_months, IQR Distance: 55.44
2. Value: 17848284.77 (amount), Date Range: last_3_calendar_months, IQR Distance: 40.68
3. Value: 17667180.97 (amount), Date Range: last_3_calendar_months, IQR Distance: 40.25
4. Value: 17595688.40 (amount), Date Range: last_1_calendar_months, IQR Distance: 40.09
5. Value: 16627631.39 (amount), Date Range: last_6_calendar_months, IQR Distance: 37.82

### cogs_profit_and_loss (amount)
**Description**: Total COGS from P&L view
#### Z-score Outliers (threshold=3.0)
Found 19 outliers using Z-score method.
Top outliers:
1. Value: 14082378.88 (amount), Date Range: last_12_calendar_months, Z-score: 37.79
2. Value: 12769082.26 (amount), Date Range: last_12_calendar_months, Z-score: 34.26
3. Value: 7129642.54 (amount), Date Range: last_6_calendar_months, Z-score: 19.09
4. Value: 6974767.16 (amount), Date Range: last_6_calendar_months, Z-score: 18.68
5. Value: 4921562.92 (amount), Date Range: last_12_calendar_months, Z-score: 13.15

#### IQR Outliers (threshold=1.5)
Found 650 outliers using IQR method.
Top outliers:
1. Value: 14082378.88 (amount), Date Range: last_12_calendar_months, IQR Distance: 4252.86
2. Value: 12769082.26 (amount), Date Range: last_12_calendar_months, IQR Distance: 3856.15
3. Value: 7129642.54 (amount), Date Range: last_6_calendar_months, IQR Distance: 2152.65
4. Value: 6974767.16 (amount), Date Range: last_6_calendar_months, IQR Distance: 2105.86
5. Value: 4921562.92 (amount), Date Range: last_12_calendar_months, IQR Distance: 1485.65

### opex_profit_and_loss (amount)
**Description**: Total Opex from P&L view
#### Z-score Outliers (threshold=3.0)
Found 18 outliers using Z-score method.
Top outliers:
1. Value: 100808471.30 (amount), Date Range: last_12_calendar_months, Z-score: 38.55
2. Value: 65313155.83 (amount), Date Range: last_12_calendar_months, Z-score: 24.93
3. Value: 61266587.85 (amount), Date Range: last_12_calendar_months, Z-score: 23.38
4. Value: 52027840.29 (amount), Date Range: last_6_calendar_months, Z-score: 19.83
5. Value: 37525883.53 (amount), Date Range: last_6_calendar_months, Z-score: 14.27

#### IQR Outliers (threshold=1.5)
Found 521 outliers using IQR method.
Top outliers:
1. Value: 100808471.30 (amount), Date Range: last_12_calendar_months, IQR Distance: 639.87
2. Value: 65313155.83 (amount), Date Range: last_12_calendar_months, IQR Distance: 414.18
3. Value: 61266587.85 (amount), Date Range: last_12_calendar_months, IQR Distance: 388.46
4. Value: 52027840.29 (amount), Date Range: last_6_calendar_months, IQR Distance: 329.71
5. Value: 37525883.53 (amount), Date Range: last_6_calendar_months, IQR Distance: 237.51

### revenue_monthly_average (amount)
**Description**: Average monthly revenue for the last X full calendar months across transactions with categories in the 'revenue' analytics group
#### Z-score Outliers (threshold=3.0)
Found 71 outliers using Z-score method.
Top outliers:
1. Value: 2051663.02 (amount), Date Range: last_1_calendar_months, Z-score: 18.31
2. Value: 1499581.92 (amount), Date Range: last_3_calendar_months, Z-score: 13.28
3. Value: 1494428.33 (amount), Date Range: last_1_calendar_months, Z-score: 13.23
4. Value: 1484365.89 (amount), Date Range: last_3_calendar_months, Z-score: 13.14
5. Value: 1381839.69 (amount), Date Range: last_6_calendar_months, Z-score: 12.20

#### IQR Outliers (threshold=1.5)
Found 460 outliers using IQR method.
Top outliers:
1. Value: 2051663.02 (amount), Date Range: last_1_calendar_months, IQR Distance: 56.37
2. Value: 1499581.92 (amount), Date Range: last_3_calendar_months, IQR Distance: 40.91
3. Value: 1494428.33 (amount), Date Range: last_1_calendar_months, IQR Distance: 40.76
4. Value: 1484365.89 (amount), Date Range: last_3_calendar_months, IQR Distance: 40.48
5. Value: 1381839.69 (amount), Date Range: last_6_calendar_months, IQR Distance: 37.61

### revenue_growth_rate (ratio)
**Description**: The growth of in average monthly inflow amounts between 1st half and 2nd half of the time period
#### Z-score Outliers (threshold=3.0)
Found 4 outliers using Z-score method.
Top outliers:
1. Value: 3265.91 (ratio), Date Range: last_6_calendar_months, Z-score: 29.58
2. Value: 796.74 (ratio), Date Range: last_6_calendar_months, Z-score: 7.17
3. Value: 703.77 (ratio), Date Range: last_6_calendar_months, Z-score: 6.33
4. Value: 483.70 (ratio), Date Range: last_6_calendar_months, Z-score: 4.33

#### IQR Outliers (threshold=1.5)
Found 87 outliers using IQR method.
Top outliers:
1. Value: 3265.91 (ratio), Date Range: last_6_calendar_months, IQR Distance: 4693.19
2. Value: 796.74 (ratio), Date Range: last_6_calendar_months, IQR Distance: 1144.50
3. Value: 703.77 (ratio), Date Range: last_6_calendar_months, IQR Distance: 1010.88
4. Value: 483.70 (ratio), Date Range: last_6_calendar_months, IQR Distance: 694.60
5. Value: 235.92 (ratio), Date Range: last_6_calendar_months, IQR Distance: 338.48

### gross_operating_cashflow_daily_average (amount)
**Description**: Average daily gross operating cashflow
#### Z-score Outliers (threshold=3.0)
Found 109 outliers using Z-score method.
Top outliers:
1. Value: 41081.57 (amount), Date Range: last_30_days, Z-score: 14.13
2. Value: 36664.11 (amount), Date Range: last_30_days, Z-score: 12.56
3. Value: 36070.72 (amount), Date Range: last_120_days, Z-score: 12.35
4. Value: 31371.26 (amount), Date Range: last_180_days, Z-score: 10.68
5. Value: 27587.25 (amount), Date Range: last_30_days, Z-score: 9.34

#### IQR Outliers (threshold=1.5)
Found 580 outliers using IQR method.
Top outliers:
1. Value: 41081.57 (amount), Date Range: last_30_days, IQR Distance: 36.33
2. Value: 36664.11 (amount), Date Range: last_30_days, IQR Distance: 32.30
3. Value: 36070.72 (amount), Date Range: last_120_days, IQR Distance: 31.76
4. Value: 31371.26 (amount), Date Range: last_180_days, IQR Distance: 27.48
5. Value: 27587.25 (amount), Date Range: last_30_days, IQR Distance: 24.04

### net_operating_cashflow_daily_average (amount)
**Description**: Average daily net operating cashflow, taking revenue_daily_average - cogs_daily_average - opex_daily_average
#### Z-score Outliers (threshold=3.0)
Found 26 outliers using Z-score method.
Top outliers:
1. Value: -306345.08 (amount), Date Range: last_30_days, Z-score: 23.30
2. Value: -304065.18 (amount), Date Range: last_30_days, Z-score: 23.13
3. Value: -301325.70 (amount), Date Range: last_90_days, Z-score: 22.92
4. Value: -287534.08 (amount), Date Range: last_180_days, Z-score: 21.87
5. Value: -275511.33 (amount), Date Range: last_365_days, Z-score: 20.95

#### IQR Outliers (threshold=1.5)
Found 923 outliers using IQR method.
Top outliers:
1. Value: -306345.08 (amount), Date Range: last_30_days, IQR Distance: 901.12
2. Value: -304065.18 (amount), Date Range: last_30_days, IQR Distance: 894.41
3. Value: -301325.70 (amount), Date Range: last_90_days, IQR Distance: 886.35
4. Value: -287534.08 (amount), Date Range: last_180_days, IQR Distance: 845.76
5. Value: -275511.33 (amount), Date Range: last_365_days, IQR Distance: 810.37

### gross_operating_cashflow (amount)
**Description**: Total gross operating cashflow
#### Z-score Outliers (threshold=3.0)
Found 79 outliers using Z-score method.
Top outliers:
1. Value: 9288053.34 (amount), Date Range: last_12_calendar_months, Z-score: 15.64
2. Value: 8636476.77 (amount), Date Range: last_12_calendar_months, Z-score: 14.52
3. Value: 8416438.84 (amount), Date Range: last_12_calendar_months, Z-score: 14.14
4. Value: 7226309.64 (amount), Date Range: last_12_calendar_months, Z-score: 12.09
5. Value: 6648879.57 (amount), Date Range: last_12_calendar_months, Z-score: 11.09

#### IQR Outliers (threshold=1.5)
Found 503 outliers using IQR method.
Top outliers:
1. Value: 9288053.34 (amount), Date Range: last_12_calendar_months, IQR Distance: 56.34
2. Value: 8636476.77 (amount), Date Range: last_12_calendar_months, IQR Distance: 52.31
3. Value: 8416438.84 (amount), Date Range: last_12_calendar_months, IQR Distance: 50.96
4. Value: 7226309.64 (amount), Date Range: last_12_calendar_months, IQR Distance: 43.60
5. Value: 6648879.57 (amount), Date Range: last_12_calendar_months, IQR Distance: 40.03

### net_operating_cashflow (amount)
**Description**: Total net operating cashflow
#### Z-score Outliers (threshold=3.0)
Found 18 outliers using Z-score method.
Top outliers:
1. Value: -95463244.29 (amount), Date Range: last_12_calendar_months, Z-score: 39.28
2. Value: -61266587.85 (amount), Date Range: last_12_calendar_months, Z-score: 25.19
3. Value: -56676679.06 (amount), Date Range: last_12_calendar_months, Z-score: 23.30
4. Value: -49289194.65 (amount), Date Range: last_6_calendar_months, Z-score: 20.26
5. Value: -32535693.88 (amount), Date Range: last_6_calendar_months, Z-score: 13.35

#### IQR Outliers (threshold=1.5)
Found 903 outliers using IQR method.
Top outliers:
1. Value: -95463244.29 (amount), Date Range: last_12_calendar_months, IQR Distance: 2399.90
2. Value: -61266587.85 (amount), Date Range: last_12_calendar_months, IQR Distance: 1540.04
3. Value: -56676679.06 (amount), Date Range: last_12_calendar_months, IQR Distance: 1424.63
4. Value: -49289194.65 (amount), Date Range: last_6_calendar_months, IQR Distance: 1238.87
5. Value: -32535693.88 (amount), Date Range: last_6_calendar_months, IQR Distance: 817.61

### gross_operating_cashflow_profit_and_loss (amount)
**Description**: Total gross operating cashflow from P&L view
#### Z-score Outliers (threshold=3.0)
Found 79 outliers using Z-score method.
Top outliers:
1. Value: 9288053.34 (amount), Date Range: last_12_calendar_months, Z-score: 15.64
2. Value: 8636476.77 (amount), Date Range: last_12_calendar_months, Z-score: 14.52
3. Value: 8416438.84 (amount), Date Range: last_12_calendar_months, Z-score: 14.14
4. Value: 7226309.64 (amount), Date Range: last_12_calendar_months, Z-score: 12.09
5. Value: 6648879.57 (amount), Date Range: last_12_calendar_months, Z-score: 11.09

#### IQR Outliers (threshold=1.5)
Found 503 outliers using IQR method.
Top outliers:
1. Value: 9288053.34 (amount), Date Range: last_12_calendar_months, IQR Distance: 56.34
2. Value: 8636476.77 (amount), Date Range: last_12_calendar_months, IQR Distance: 52.31
3. Value: 8416438.84 (amount), Date Range: last_12_calendar_months, IQR Distance: 50.96
4. Value: 7226309.64 (amount), Date Range: last_12_calendar_months, IQR Distance: 43.60
5. Value: 6648879.57 (amount), Date Range: last_12_calendar_months, IQR Distance: 40.03

### net_operating_cashflow_profit_and_loss (amount)
**Description**: Total net operating cashflow from P&L view
#### Z-score Outliers (threshold=3.0)
Found 18 outliers using Z-score method.
Top outliers:
1. Value: -95463244.29 (amount), Date Range: last_12_calendar_months, Z-score: 39.28
2. Value: -61266587.85 (amount), Date Range: last_12_calendar_months, Z-score: 25.19
3. Value: -56676679.06 (amount), Date Range: last_12_calendar_months, Z-score: 23.30
4. Value: -49289194.65 (amount), Date Range: last_6_calendar_months, Z-score: 20.26
5. Value: -32535693.88 (amount), Date Range: last_6_calendar_months, Z-score: 13.35

#### IQR Outliers (threshold=1.5)
Found 903 outliers using IQR method.
Top outliers:
1. Value: -95463244.29 (amount), Date Range: last_12_calendar_months, IQR Distance: 2399.90
2. Value: -61266587.85 (amount), Date Range: last_12_calendar_months, IQR Distance: 1540.04
3. Value: -56676679.06 (amount), Date Range: last_12_calendar_months, IQR Distance: 1424.63
4. Value: -49289194.65 (amount), Date Range: last_6_calendar_months, IQR Distance: 1238.87
5. Value: -32535693.88 (amount), Date Range: last_6_calendar_months, IQR Distance: 817.61

## RISK_FLAG METRICS
### deposit_days (day)
**Description**: Total distinct days where a deposit occurred
#### Z-score Outliers (threshold=3.0)
Found 243 outliers using Z-score method.
Top outliers:
1. Value: 363.00 (day), Date Range: last_12_calendar_months, Z-score: 4.96
2. Value: 363.00 (day), Date Range: last_365_days, Z-score: 4.96
3. Value: 362.00 (day), Date Range: last_12_calendar_months, Z-score: 4.94
4. Value: 361.00 (day), Date Range: last_365_days, Z-score: 4.93
5. Value: 358.00 (day), Date Range: last_365_days, Z-score: 4.88

#### IQR Outliers (threshold=1.5)
Found 660 outliers using IQR method.
Top outliers:
1. Value: 363.00 (day), Date Range: last_365_days, IQR Distance: 4.61
2. Value: 363.00 (day), Date Range: last_12_calendar_months, IQR Distance: 4.61
3. Value: 362.00 (day), Date Range: last_12_calendar_months, IQR Distance: 4.60
4. Value: 361.00 (day), Date Range: last_365_days, IQR Distance: 4.58
5. Value: 358.00 (day), Date Range: last_365_days, IQR Distance: 4.53

### nsf_fees (n)
**Description**: Total count NSF transactions
#### Z-score Outliers (threshold=3.0)
Found 50 outliers using Z-score method.
Top outliers:
1. Value: 1044.00 (n), Date Range: last_365_days, Z-score: 46.79
2. Value: 509.00 (n), Date Range: last_6_calendar_months, Z-score: 22.75
3. Value: 498.00 (n), Date Range: last_180_days, Z-score: 22.25
4. Value: 422.00 (n), Date Range: last_365_days, Z-score: 18.84
5. Value: 313.00 (n), Date Range: last_120_days, Z-score: 13.94

#### IQR Outliers (threshold=1.5)
Found 118 outliers using IQR method.
Top outliers:
1. Value: 1044.00 (n), Date Range: last_365_days, IQR Distance: 46.92
2. Value: 509.00 (n), Date Range: last_6_calendar_months, IQR Distance: 22.87
3. Value: 498.00 (n), Date Range: last_180_days, IQR Distance: 22.38
4. Value: 422.00 (n), Date Range: last_365_days, IQR Distance: 18.96
5. Value: 313.00 (n), Date Range: last_120_days, IQR Distance: 14.07

### nsf_days (day)
**Description**: Total distinct days where an NSF transaction occurred
#### Z-score Outliers (threshold=3.0)
Found 83 outliers using Z-score method.
Top outliers:
1. Value: 337.00 (day), Date Range: last_365_days, Z-score: 47.18
2. Value: 248.00 (day), Date Range: last_365_days, Z-score: 34.68
3. Value: 173.00 (day), Date Range: last_180_days, Z-score: 24.14
4. Value: 131.00 (day), Date Range: last_180_days, Z-score: 18.25
5. Value: 113.00 (day), Date Range: last_120_days, Z-score: 15.72

#### IQR Outliers (threshold=1.5)
Found 538 outliers using IQR method.
Top outliers:
1. Value: 337.00 (day), Date Range: last_365_days, IQR Distance: 536.77
2. Value: 248.00 (day), Date Range: last_365_days, IQR Distance: 394.75
3. Value: 173.00 (day), Date Range: last_180_days, IQR Distance: 275.07
4. Value: 131.00 (day), Date Range: last_180_days, IQR Distance: 208.04
5. Value: 113.00 (day), Date Range: last_120_days, IQR Distance: 179.32

### debt_collection (amount)
**Description**: Total amount from debt collection agency transactions

### atm_withdrawals (amount)
**Description**: Total amount from atm withdrawal transactions
#### Z-score Outliers (threshold=3.0)
Found 13 outliers using Z-score method.
Top outliers:
1. Value: 638664.65 (amount), Date Range: last_365_days, Z-score: 16.79
2. Value: 474443.36 (amount), Date Range: last_365_days, Z-score: 12.42
3. Value: 453108.75 (amount), Date Range: last_365_days, Z-score: 11.86
4. Value: 332366.62 (amount), Date Range: last_365_days, Z-score: 8.64
5. Value: 320999.70 (amount), Date Range: last_365_days, Z-score: 8.34

#### IQR Outliers (threshold=1.5)
Found 172 outliers using IQR method.
Top outliers:
1. Value: 638664.65 (amount), Date Range: last_365_days, IQR Distance: 318.33
2. Value: 474443.36 (amount), Date Range: last_365_days, IQR Distance: 236.22
3. Value: 453108.75 (amount), Date Range: last_365_days, IQR Distance: 225.55
4. Value: 332366.62 (amount), Date Range: last_365_days, IQR Distance: 165.18
5. Value: 320999.70 (amount), Date Range: last_365_days, IQR Distance: 159.50

### tax_payments (n)
**Description**: Total count of tax payments
#### Z-score Outliers (threshold=3.0)
Found 15 outliers using Z-score method.
Top outliers:
1. Value: 461.00 (n), Date Range: last_365_days, Z-score: 13.81
2. Value: 405.00 (n), Date Range: last_365_days, Z-score: 12.08
3. Value: 397.00 (n), Date Range: last_365_days, Z-score: 11.83
4. Value: 211.00 (n), Date Range: last_365_days, Z-score: 6.08
5. Value: 168.00 (n), Date Range: last_365_days, Z-score: 4.75

#### IQR Outliers (threshold=1.5)
Found 124 outliers using IQR method.
Top outliers:
1. Value: 461.00 (n), Date Range: last_365_days, IQR Distance: 29.73
2. Value: 405.00 (n), Date Range: last_365_days, IQR Distance: 26.00
3. Value: 397.00 (n), Date Range: last_365_days, IQR Distance: 25.47
4. Value: 211.00 (n), Date Range: last_365_days, IQR Distance: 13.07
5. Value: 168.00 (n), Date Range: last_365_days, IQR Distance: 10.20

### tax_payment_amount (amount)
**Description**: Total amount of tax payments (categories assigned to 'tax_expenses' analytics group)
#### Z-score Outliers (threshold=3.0)
Found 13 outliers using Z-score method.
Top outliers:
1. Value: 2243604.92 (amount), Date Range: last_365_days, Z-score: 20.51
2. Value: 931604.53 (amount), Date Range: last_365_days, Z-score: 8.33
3. Value: 667484.44 (amount), Date Range: last_365_days, Z-score: 5.88
4. Value: 649675.15 (amount), Date Range: last_365_days, Z-score: 5.71
5. Value: 639241.42 (amount), Date Range: last_365_days, Z-score: 5.62

#### IQR Outliers (threshold=1.5)
Found 158 outliers using IQR method.
Top outliers:
1. Value: 2243604.92 (amount), Date Range: last_365_days, IQR Distance: 110.62
2. Value: 931604.53 (amount), Date Range: last_365_days, IQR Distance: 45.35
3. Value: 667484.44 (amount), Date Range: last_365_days, IQR Distance: 32.21
4. Value: 649675.15 (amount), Date Range: last_365_days, IQR Distance: 31.32
5. Value: 639241.42 (amount), Date Range: last_365_days, IQR Distance: 30.80

### negative_balance_days (day)
**Description**: Total number of days where the balance was less than 0
#### Z-score Outliers (threshold=3.0)
Found 142 outliers using Z-score method.
Top outliers:
1. Value: 364.00 (day), Date Range: last_365_days, Z-score: 7.12
2. Value: 357.00 (day), Date Range: last_365_days, Z-score: 6.98
3. Value: 355.00 (day), Date Range: last_365_days, Z-score: 6.94
4. Value: 348.00 (day), Date Range: last_365_days, Z-score: 6.79
5. Value: 342.00 (day), Date Range: last_365_days, Z-score: 6.67

#### IQR Outliers (threshold=1.5)
Found 789 outliers using IQR method.
Top outliers:
1. Value: 364.00 (day), Date Range: last_365_days, IQR Distance: 18.16
2. Value: 357.00 (day), Date Range: last_365_days, IQR Distance: 17.79
3. Value: 355.00 (day), Date Range: last_365_days, IQR Distance: 17.68
4. Value: 348.00 (day), Date Range: last_365_days, IQR Distance: 17.32
5. Value: 342.00 (day), Date Range: last_365_days, IQR Distance: 17.00

### negative_balance_days_by_account (day)
**Description**: Total number of account / day pairs where the ending balance was less than 0 for that account / day
#### Z-score Outliers (threshold=3.0)
Found 3 outliers using Z-score method.
Top outliers:
1. Value: 39654.00 (day), Date Range: last_365_days, Z-score: 72.78
2. Value: 11187.00 (day), Date Range: last_365_days, Z-score: 20.45
3. Value: 2310.00 (day), Date Range: last_365_days, Z-score: 4.13

#### IQR Outliers (threshold=1.5)
Found 736 outliers using IQR method.
Top outliers:
1. Value: 39654.00 (day), Date Range: last_365_days, IQR Distance: 733.33
2. Value: 11187.00 (day), Date Range: last_365_days, IQR Distance: 206.17
3. Value: 2310.00 (day), Date Range: last_365_days, IQR Distance: 41.78
4. Value: 1216.00 (day), Date Range: last_365_days, IQR Distance: 21.52
5. Value: 1208.00 (day), Date Range: last_365_days, IQR Distance: 21.37

## Summary of Most Significant Outliers Across All Metrics
| Metric Group | Metric | Value | Date Range | Method | Score |
|-------------|--------|-------|------------|--------|-------|
| debt | debt_service_coverage_ratio | -621609.38 | last_12_calendar_months | IQR | 336576.29 |
| debt | debt_service_coverage_ratio | -58859.33 | last_3_calendar_months | IQR | 31869.54 |
| debt | debt_service_coverage_ratio | 18465.12 | last_6_calendar_months | IQR | 9997.57 |
| debt | debt_service_coverage_ratio | 18111.41 | last_3_calendar_months | IQR | 9806.05 |
| heron | predicted_balance_daily_average | 182581794.50 | next_90_days | IQR | 8145.38 |
| heron | predicted_balance_daily_average | 182581794.50 | next_60_days | IQR | 8145.38 |
| heron | predicted_balance_daily_average | 182581794.50 | next_30_days | IQR | 8145.38 |
| debt | debt_service_coverage_ratio | -9155.08 | last_3_calendar_months | IQR | 4956.66 |
| profit_and_loss | revenue_growth_rate | 3265.91 | last_6_calendar_months | IQR | 4693.19 |
| debt | debt_service_coverage_ratio | 8005.42 | last_1_calendar_months | IQR | 4334.06 |
| profit_and_loss | cogs | 14082378.88 | last_12_calendar_months | IQR | 4252.86 |
| profit_and_loss | cogs_profit_and_loss | 14082378.88 | last_12_calendar_months | IQR | 4252.86 |
| profit_and_loss | cogs_profit_and_loss | 12769082.26 | last_12_calendar_months | IQR | 3856.15 |
| profit_and_loss | cogs | 12769082.26 | last_12_calendar_months | IQR | 3856.15 |
| processing_quality | unconnected_account_ratio | 1656.92 | last_365_days | IQR | 3294.17 |
| debt | debt_service_coverage_ratio | -6066.01 | last_12_calendar_months | IQR | 3284.05 |
| debt | debt_service_coverage_ratio | -5623.44 | last_3_calendar_months | IQR | 3044.42 |
| heron | predicted_balance_daily_average | -67491219.27 | next_60_days | IQR | 3011.34 |
| heron | predicted_balance_daily_average | -67491219.27 | next_90_days | IQR | 3011.34 |
| heron | predicted_balance_daily_average | -67491219.27 | next_30_days | IQR | 3011.34 |
