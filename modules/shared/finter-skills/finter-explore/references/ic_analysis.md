# IC (Information Coefficient) Analysis

## What is IC?

IC measures correlation between signal (today) and returns (tomorrow).
- **Rank IC** (Spearman): Correlation of ranks - robust to outliers
- **Raw IC** (Pearson): Correlation of values - sensitive to outliers

## Interpretation

| IC Range | Interpretation | Action |
|----------|---------------|--------|
| > 0.05 | Strong signal | Proceed to alpha |
| 0.02 - 0.05 | Moderate signal | Proceed with caution |
| 0 - 0.02 | Weak signal | Consider improvements |
| < 0 | Inverse signal | Check for bugs or flip sign |

## IC Sharpe (IC_IR)

`IC_Sharpe = mean(IC) / std(IC) * sqrt(252)`

| IC Sharpe | Interpretation |
|-----------|---------------|
| > 2.0 | Excellent - consistent alpha |
| 1.0 - 2.0 | Good - reliable signal |
| 0.5 - 1.0 | Moderate - usable |
| < 0.5 | Weak - high variance |

## Win Rate

`Win Rate = % of days with IC > 0`

| Win Rate | Interpretation |
|----------|---------------|
| > 60% | Consistent |
| 55% - 60% | Acceptable |
| 50% - 55% | Borderline |
| < 50% | Unreliable |

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

    # Quality gate check
    if rank_ic.mean() < 0.02:
        print("\n⚠️ WEAK SIGNAL - IC < 0.02")
        print("   Consider: different lookback, data transformation, or abandon")
    elif (rank_ic > 0).mean() < 0.55:
        print("\n⚠️ INCONSISTENT - Win rate < 55%")
        print("   Consider: regime filtering or parameter tuning")
    else:
        print("\n✅ PASSED quality gates - proceed to finter-alpha")

    return rank_ic, raw_ic
```

## Common IC Pitfalls

1. **Lookahead bias**: Using same-day returns instead of forward returns
2. **Survivorship bias**: Not handling delisted stocks
3. **Too few observations**: Need 30+ valid pairs per day
4. **Outlier dominance**: Use rank IC instead of raw IC
