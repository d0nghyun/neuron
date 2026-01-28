# IC (Information Coefficient) Analysis

## What is IC?

IC measures correlation between signal (today) and returns (tomorrow).
- **Rank IC** (Spearman): Correlation of ranks - robust to outliers
- **Raw IC** (Pearson): Correlation of values - sensitive to outliers

## Interpretation (Context-Dependent)

| IC Range | Typical Interpretation | Context Considerations |
|----------|----------------------|------------------------|
| > 0.05 | Strong signal | Check for overfitting, data mining bias |
| 0.02 - 0.05 | Moderate signal | Often sufficient for diversified strategies |
| 0.01 - 0.02 | Weak but potentially useful | May work in multi-factor or with other edges |
| < 0.01 | Very weak | Understand why before deciding |
| < 0 | Inverse relationship | Intentional? Check for bugs |

**Your job**: Interpret in context (universe, strategy type, holding period), then make a reasoned judgment.

## IC Sharpe (IC_IR)

`IC_Sharpe = mean(IC) / std(IC) * sqrt(252)`

| IC Sharpe | Typical Reading | Note |
|-----------|-----------------|------|
| > 2.0 | Strong consistency | Rare - verify not overfit |
| 1.0 - 2.0 | Good signal | Commonly seen in production factors |
| 0.5 - 1.0 | Moderate | May still be useful in combination |
| < 0.5 | High variance | Understand the source of variance |

## Win Rate

`Win Rate = % of days with IC > 0`

| Win Rate | Typical Reading | Note |
|----------|-----------------|------|
| > 60% | High consistency | Mean-reversion often lower |
| 50% - 60% | Normal range | Most factors fall here |
| < 50% | Inconsistent | May still work if wins are larger |

**Caveat**: Win rate alone is misleading. A 45% win rate with 2:1 reward/risk beats 60% with 1:2.

## Complete IC Analysis Code

```python
from scipy.stats import spearmanr, pearsonr
import pandas as pd
import numpy as np

def analyze_ic(signal, returns, name="Signal"):
    """Complete IC analysis with all metrics"""
    forward_returns = returns.shift(-1)

    rank_ic = []
    raw_ic = []

    for i in range(len(signal) - 1):
        s = signal.iloc[i]
        r = forward_returns.iloc[i]
        valid = (~s.isna()) & (~r.isna())

        if valid.sum() > 30:
            rank_ic.append(spearmanr(s[valid], r[valid])[0])
            raw_ic.append(pearsonr(s[valid], r[valid])[0])

    rank_ic = pd.Series(rank_ic)
    raw_ic = pd.Series(raw_ic)

    print(f"\n=== {name} IC Analysis ===")
    print(f"Rank IC:  {rank_ic.mean():.4f} (std: {rank_ic.std():.4f})")
    print(f"Raw IC:   {raw_ic.mean():.4f} (std: {raw_ic.std():.4f})")
    print(f"IC Sharpe: {rank_ic.mean() / rank_ic.std() * np.sqrt(252):.2f}")
    print(f"Win Rate: {(rank_ic > 0).mean():.1%}")

    # Interpretation guide (reference only - you decide)
    print("\n--- Interpretation Guide ---")
    print("IC < 0.02: Weak for single-factor, may be fine in multi-factor")
    print("IC 0.02-0.05: Moderate - consider strategy context")
    print("IC > 0.05: Strong - but check for overfitting")
    print("\nYour judgment: Consider universe, strategy type, holding period")

    return rank_ic, raw_ic
```

## Common IC Pitfalls

1. **Lookahead bias**: Using same-day returns instead of forward returns
2. **Survivorship bias**: Not handling delisted stocks
3. **Too few observations**: Need 30+ valid pairs per day
4. **Outlier dominance**: Use rank IC instead of raw IC
