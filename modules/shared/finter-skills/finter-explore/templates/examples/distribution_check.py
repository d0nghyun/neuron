"""
Distribution Check Template
Copy this to Jupyter and modify the signal calculation section.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. LOAD DATA (modify this section)
# =============================================================================
from finter.data import ContentFactory

cf = ContentFactory("kr_stock", 20200101, 20241231)
close = cf.get_df("price_close")

# =============================================================================
# 2. CALCULATE SIGNAL (modify this section)
# =============================================================================
signal = close.pct_change(20)

# =============================================================================
# 3. DISTRIBUTION ANALYSIS (do not modify)
# =============================================================================
print("=" * 50)
print("SIGNAL DISTRIBUTION ANALYSIS")
print("=" * 50)

# Basic stats
print(f"\n1. Basic Statistics:")
print(f"   Shape: {signal.shape} (days x stocks)")
print(f"   Mean:  {signal.mean().mean():.6f}")
print(f"   Std:   {signal.std().mean():.6f}")
print(f"   Min:   {signal.min().min():.4f}")
print(f"   Max:   {signal.max().max():.4f}")

# NaN analysis
nan_ratio = signal.isna().sum().sum() / signal.size
print(f"\n2. Missing Values:")
print(f"   NaN ratio: {nan_ratio:.1%}")
if nan_ratio > 0.2:
    print("   ⚠️  WARNING: >20% missing values")

# Outlier analysis
mean_val = signal.mean().mean()
std_val = signal.std().mean()
outliers = ((signal > mean_val + 3*std_val) | (signal < mean_val - 3*std_val)).sum().sum()
outlier_ratio = outliers / signal.size
print(f"\n3. Outliers (> 3 std):")
print(f"   Count: {outliers:,}")
print(f"   Ratio: {outlier_ratio:.2%}")
if outlier_ratio > 0.01:
    print("   ⚠️  WARNING: >1% outliers - consider winsorizing")

# Skewness and kurtosis
skew = signal.stack().skew()
kurt = signal.stack().kurtosis()
print(f"\n4. Distribution Shape:")
print(f"   Skewness: {skew:.4f}")
print(f"   Kurtosis: {kurt:.4f}")
if abs(skew) > 1:
    print("   ⚠️  WARNING: Highly skewed - consider log transform")
if kurt > 3:
    print("   ⚠️  WARNING: Heavy tails - use rank transformation")

# =============================================================================
# 4. TURNOVER CHECK
# =============================================================================
print(f"\n5. Turnover Analysis:")
ranks = signal.rank(axis=1, pct=True)
daily_rank_changes = ranks.diff().abs().sum(axis=1).mean()
annual_turnover_est = daily_rank_changes * 252 * 100  # rough estimate
print(f"   Avg daily rank change: {daily_rank_changes:.2f}")
print(f"   Est. annual turnover: {annual_turnover_est:.0f}%")
if annual_turnover_est > 15000:
    print("   ⚠️  WARNING: High turnover - consider smoothing")

# =============================================================================
# 5. VISUALIZATION
# =============================================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Overall distribution
signal.stack().hist(bins=100, ax=axes[0, 0], edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Signal Distribution (All Observations)')
axes[0, 0].set_xlabel('Signal Value')

# Time series of mean
signal.mean(axis=1).plot(ax=axes[0, 1])
axes[0, 1].set_title('Signal Mean Over Time')
axes[0, 1].axhline(0, color='k', linestyle='--', alpha=0.3)

# Box plot by year
yearly = signal.groupby(signal.index.year).apply(lambda x: x.stack())
yearly.unstack(level=0).boxplot(ax=axes[1, 0])
axes[1, 0].set_title('Signal Distribution by Year')

# NaN ratio over time
nan_by_day = signal.isna().sum(axis=1) / signal.shape[1]
nan_by_day.plot(ax=axes[1, 1])
axes[1, 1].set_title('NaN Ratio Over Time')
axes[1, 1].set_ylabel('NaN Ratio')

plt.tight_layout()
plt.show()

# =============================================================================
# 6. SUMMARY
# =============================================================================
print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
issues = []
if nan_ratio > 0.2:
    issues.append("High NaN ratio")
if outlier_ratio > 0.01:
    issues.append("Many outliers")
if abs(skew) > 1:
    issues.append("High skewness")
if annual_turnover_est > 15000:
    issues.append("High turnover")

if issues:
    print(f"⚠️  Issues found: {', '.join(issues)}")
    print("   Address these before IC analysis")
else:
    print("✅ Distribution looks healthy - proceed to IC analysis")
