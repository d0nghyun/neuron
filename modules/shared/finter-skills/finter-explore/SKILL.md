---
name: finter-explore
description: Signal analysis and visualization for quantitative research. Use when you need to explore signal distributions, calculate IC, analyze correlations, or diagnose signal quality BEFORE implementing alpha strategies.
---

# Finter Signal Exploration

Explore, visualize, and diagnose signal quality for quantitative research.

> **Role in workflow**: Use between `finter-data` (data loading) and `finter-alpha` (strategy implementation).

## ⚠️ CRITICAL RULES (MUST FOLLOW)

### Diagnose First, Implement Later

**ALWAYS explore signal BEFORE implementing alpha:**
```
❌ FORBIDDEN: Hypothesis → Implement alpha.py → Backtest → "Sharpe is bad"
✅ CORRECT:   Hypothesis → Explore signal → Validate IC → THEN implement
```

### Quality Assessment (YOUR JUDGMENT)

After calculating metrics, **you decide** whether to proceed. Consider:

| Metric | Typical Range | Context Matters |
|--------|---------------|-----------------|
| IC (rank) | 0.01 ~ 0.10 | Crypto tolerates lower; HFT needs higher |
| IC win rate | 50% ~ 70% | Mean-reversion may have lower win rate but larger wins |
| Coverage | 70% ~ 95% | Depends on universe size and strategy |
| Turnover | varies | High-freq strategies tolerate high turnover |

**Your job:**
1. Calculate the metrics
2. Interpret in context (universe, strategy type, market regime)
3. Make a judgment: proceed, modify, or stop
4. **Explain your reasoning** - why you made this decision

### Never Save Figures

```python
# ❌ WRONG - Causes API errors in Jupyter
plt.savefig('plot.png')

# ✅ CORRECT - Let Jupyter display inline
plt.show()  # Or just let it display automatically
```

## Common Mistakes

**Mistake 1: Skipping IC calculation**
```python
# ❌ WRONG - Implementing without validation
signal = close.pct_change(20)
# Immediately go to alpha.py...

# ✅ CORRECT - Calculate IC first
ic = calculate_ic(signal, forward_returns)
print(f"IC: {ic.mean():.4f}, Win rate: {(ic > 0).mean():.1%}")
# Interpret IC in context, then make your judgment
```

**Mistake 2: Using wrong IC calculation**
```python
# ❌ WRONG - Correlation with same-day returns (lookahead bias!)
ic = signal.corrwith(returns)

# ✅ CORRECT - Correlation with NEXT-day returns
forward_returns = returns.shift(-1)  # Tomorrow's return
ic = calculate_daily_ic(signal, forward_returns)
```

**Mistake 3: Ignoring NaN in IC calculation**
```python
# ❌ WRONG - NaN causes incorrect IC
from scipy.stats import spearmanr
ic, _ = spearmanr(signal.iloc[i], returns.iloc[i+1])  # NaN → wrong result

# ✅ CORRECT - Filter valid observations
valid = (~signal.iloc[i].isna()) & (~returns.iloc[i+1].isna())
if valid.sum() > 30:  # Minimum observations
    ic, _ = spearmanr(signal.iloc[i][valid], returns.iloc[i+1][valid])
```

**Mistake 4: Not checking turnover before implementation**
```python
# ❌ WRONG - Discover high turnover after full backtest
alpha = Alpha()
result = sim.run(position=alpha.get(...))
# "Turnover: 50,000%!" - wasted time

# ✅ CORRECT - Check signal stability first
daily_changes = (signal.rank(axis=1).diff().abs() > 0).sum(axis=1).mean()
print(f"Avg daily rank changes: {daily_changes:.0f} stocks")
# If too high → diagnose before implementing
```

## 📋 Workflow

1. **Load Data**: Use `finter-data` skill
2. **Calculate Signal**: In Jupyter notebook
3. **Run Diagnostics**: IC, distribution, turnover, stationarity
4. **Interpret Results**: What do these numbers mean for THIS strategy?
5. **Make Decision**: Proceed, modify, or stop - with documented reasoning

## ⚡ Quick Reference

**Essential IC calculation:**
```python
from scipy.stats import spearmanr
import pandas as pd
import numpy as np

def calculate_daily_ic(signal, returns):
    """Calculate daily IC between signal and next-period returns"""
    forward_returns = returns.shift(-1)
    ic_series = []

    for i in range(len(signal) - 1):
        s = signal.iloc[i]
        r = forward_returns.iloc[i]
        valid = (~s.isna()) & (~r.isna())

        if valid.sum() > 30:
            ic, _ = spearmanr(s[valid], r[valid])
            ic_series.append(ic)

    return pd.Series(ic_series)

# Usage
ic = calculate_daily_ic(signal, returns)
print(f"Mean IC: {ic.mean():.4f}")
print(f"IC Std: {ic.std():.4f}")
print(f"IC Sharpe: {ic.mean() / ic.std() * np.sqrt(252):.2f}")
print(f"Win Rate: {(ic > 0).mean():.1%}")
```

**Quick distribution check:**
```python
print(f"Signal stats:")
print(f"  Mean: {signal.mean().mean():.4f}")
print(f"  Std: {signal.std().mean():.4f}")
print(f"  NaN ratio: {signal.isna().sum().sum() / signal.size:.1%}")
print(f"  Range: [{signal.min().min():.2f}, {signal.max().max():.2f}]")

signal.mean(axis=1).hist(bins=50, figsize=(10, 4))
```

**Quick turnover check:**
```python
# Rank-based turnover (more robust)
ranks = signal.rank(axis=1, pct=True)
daily_changes = ranks.diff().abs().sum(axis=1).mean()
print(f"Avg daily rank change: {daily_changes:.2f}")

# Threshold: if > 0.5 (50% of positions change daily) → investigate
```

**Stationarity test:**
```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(signal.mean(axis=1).dropna())
print(f"ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
print(f"Stationary: {'Yes' if result[1] < 0.05 else 'No'}")
```

## 📚 Documentation

### MUST READ (Before Exploration)
| Doc | Purpose |
|-----|---------|
| `references/ic_analysis.md` | IC calculation methods and interpretation |
| `references/mental_models/signal_diagnosis.md` | Diagnostic framework |

### Reference During Analysis
| Doc | Purpose |
|-----|---------|
| `templates/examples/ic_analysis.py` | Working IC calculation template |
| `templates/examples/distribution_check.py` | Distribution diagnostics |

## 🔍 When to Use This Skill

**Use finter-explore when:**
- ✅ Testing new hypothesis/signal before alpha implementation
- ✅ Calculating IC and predictive power metrics
- ✅ Diagnosing signal issues (turnover, outliers, stationarity)
- ✅ Comparing multiple signals/factors
- ✅ Deciding whether to proceed with alpha implementation

**Don't use for:**
- ❌ Loading data (use finter-data)
- ❌ Implementing alpha class (use finter-alpha)
- ❌ Running backtests (use finter-alpha)

**Workflow integration:**
```
finter-data → finter-explore → finter-alpha
   (load)        (validate)      (implement)
```
