import pandas as pd
import numpy as np

# Load normalized data
df = pd.read_csv('Regression on Heron_score/company_metrics_wide_normalized.csv')

# Drop heron_id column before calculating correlations
df = df.drop(columns=['heron_id'])

# Calculate correlations with heron_score_latest
correlations = df.corr()['heron_score_latest'].sort_values(ascending=False)

# Save correlations to CSV
correlations.to_csv('Regression on Heron_score/heron_score_normalized_correlations.csv')

# Print top 10 correlations
print("\nTop 10 correlations with heron_score_latest:")
print(correlations.head(10))
print("\nBottom 10 correlations with heron_score_latest:")
print(correlations.tail(10)) 