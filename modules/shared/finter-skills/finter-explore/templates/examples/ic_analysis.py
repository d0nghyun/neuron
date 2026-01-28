"""
IC Analysis Template
Copy this to Jupyter and modify the signal calculation section.
"""

from scipy.stats import spearmanr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. LOAD DATA (modify this section)
# =============================================================================
from finter.data import ContentFactory

cf = ContentFactory("kr_stock", 20200101, 20241231)
close = cf.get_df("price_close")
returns = close.pct_change()

# =============================================================================
# 2. CALCULATE SIGNAL (modify this section)
# =============================================================================
# Example: 20-day momentum
signal = close.pct_change(20)

# =============================================================================
# 3. IC ANALYSIS (do not modify)
# =============================================================================
def calculate_daily_ic(signal, returns):
    """Calculate daily rank IC"""
    forward_returns = returns.shift(-1)
    ic_values = []
    dates = []

    for i in range(len(signal) - 1):
        s = signal.iloc[i]
        r = forward_returns.iloc[i]
        valid = (~s.isna()) & (~r.isna())

        if valid.sum() > 30:
            ic, _ = spearmanr(s[valid], r[valid])
            ic_values.append(ic)
            dates.append(signal.index[i])

    return pd.Series(ic_values, index=dates)

ic = calculate_daily_ic(signal, returns)

# Print results
print("=" * 50)
print("IC ANALYSIS RESULTS")
print("=" * 50)
print(f"Mean IC:    {ic.mean():.4f}")
print(f"IC Std:     {ic.std():.4f}")
print(f"IC Sharpe:  {ic.mean() / ic.std() * np.sqrt(252):.2f}")
print(f"Win Rate:   {(ic > 0).mean():.1%}")
print(f"Observations: {len(ic)}")
print("=" * 50)

# Quality gate check
passed = True
if ic.mean() < 0.02:
    print("⚠️  FAIL: IC < 0.02 (weak signal)")
    passed = False
if (ic > 0).mean() < 0.55:
    print("⚠️  FAIL: Win rate < 55% (inconsistent)")
    passed = False

if passed:
    print("✅ PASSED: Proceed to finter-alpha")
else:
    print("❌ STOP: Diagnose signal issues before implementing alpha")

# =============================================================================
# 4. VISUALIZATION
# =============================================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# IC time series
axes[0, 0].plot(ic.index, ic.values, alpha=0.5)
axes[0, 0].axhline(0, color='k', linestyle='--', alpha=0.3)
axes[0, 0].axhline(ic.mean(), color='r', linestyle='-', label=f'Mean: {ic.mean():.4f}')
axes[0, 0].set_title('Daily IC Over Time')
axes[0, 0].legend()

# IC histogram
axes[0, 1].hist(ic, bins=50, edgecolor='black', alpha=0.7)
axes[0, 1].axvline(0, color='k', linestyle='--', alpha=0.5)
axes[0, 1].axvline(ic.mean(), color='r', linestyle='-')
axes[0, 1].set_title('IC Distribution')

# Rolling IC
rolling_ic = ic.rolling(60).mean()
axes[1, 0].plot(rolling_ic.index, rolling_ic.values)
axes[1, 0].axhline(0, color='k', linestyle='--', alpha=0.3)
axes[1, 0].set_title('60-day Rolling IC')

# Cumulative IC
cum_ic = ic.cumsum()
axes[1, 1].plot(cum_ic.index, cum_ic.values)
axes[1, 1].set_title('Cumulative IC')

plt.tight_layout()
plt.show()
