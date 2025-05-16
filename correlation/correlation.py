import matplotlib.pyplot as plt
import seaborn as sns

# Compute full correlation matrix including heron_score
corr_matrix = metrics_wide_df.corr()

# Set up the matplotlib figure
plt.figure(figsize=(12, 10))

# Generate a mask for the upper triangle (optional for cleaner display)
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# Draw the heatmap
sns.heatmap(corr_matrix, mask=mask, cmap='coolwarm', center=0,
            square=True, linewidths=0.5, cbar_kws={"shrink": .5})

plt.title('Correlation Matrix Including Heron Score')
plt.tight_layout()
plt.show()
