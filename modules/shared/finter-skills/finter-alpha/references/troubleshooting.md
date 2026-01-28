# Troubleshooting Guide

Debug strategies for common alpha development issues. For rule definitions, see `framework.md`.

## Quick Diagnosis

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Sharpe > 5 | Look-ahead bias | Add `.shift(1)` |
| "All NaN detected" on submit | Missing fillna | Add `.fillna(0)` |
| Different results for same date | Path dependency | Use `fill_method=None` |
| Position row sum > 1e8 | Wrong normalization | Divide by `sum(axis=1)` |
| "Alpha class not found" | Wrong class name | Rename to `Alpha` |
| Validation fails (trading days) | resample() misalignment | Align to `cf.trading_days` |

## Debugging Strategies

### 1. Check Intermediate Results

```python
def get(self, start, end):
    cf = ContentFactory("kr_stock", get_start_date(start), end)
    close = cf.get_df("price_close")

    # Debug: Check data
    print(f"Close shape: {close.shape}")
    print(f"NaN count: {close.isnull().sum().sum()}")

    momentum = close.pct_change(20, fill_method=None)

    # Debug: Check momentum
    print(f"Momentum NaN: {momentum.isnull().sum().sum()}")

    selected = momentum > 0
    positions = selected.div(selected.sum(axis=1), axis=0) * 1e8

    # Debug: Check positions
    print(f"Row sums: min={positions.sum(axis=1).min():.0f}, max={positions.sum(axis=1).max():.0f}")
    print(f"Stocks per day: {(positions > 0).sum(axis=1).mean():.1f}")

    return positions.shift(1).fillna(0).loc[str(start):str(end)]
```

### 2. Validate Before Returning

```python
from helpers import validate_positions

def get(self, start, end):
    # ... strategy logic ...

    # Validate
    validate_positions(positions)

    return positions.shift(1).fillna(0).loc[str(start):str(end)]
```

### 3. Sanity Check Backtest

```python
stats = result.statistics

# Red flags
assert stats['Sharpe Ratio'] < 5, "Too high - check look-ahead bias"
assert stats['Hit Ratio (%)'] < 90, "Too high - suspicious"
assert stats['Max Drawdown (%)'] < -1, "No drawdown - data issue?"
```

## Common Error Messages

### "All NaN detected"

**When**: Finter submit validation
**Cause**: Rows where ALL columns are NaN
**Fix**:
```python
# Before
return positions.shift(1)

# After
return positions.shift(1).fillna(0)
```

### "Class must be named 'Alpha'"

**When**: finalize.py validation step
**Cause**: Class named `MomentumAlpha`, `MyStrategy`, etc.
**Fix**: Rename to `class Alpha(BaseAlpha):`

### Path Independence Failure

**When**: alpha_validator.py check
**Cause**: Usually `pct_change()` without `fill_method=None`
**Detection**:
```python
# Same date, different start → different values?
pos1 = alpha.get(20200101, 20211231)  # includes delisted stock history
pos2 = alpha.get(20210601, 20211231)  # starts after delisting
# If pos1 and pos2 differ on overlapping dates → path dependent
```
**Fix**:
```python
momentum = close.pct_change(20, fill_method=None)
```

### Trading Days Validation Failure

**When**: alpha_validator.py check
**Cause**: `resample('ME')` creates dates not in trading calendar
**Fix**:
```python
# Align monthly signals to trading days
positions = positions.fillna(-np.inf)
full_range = pd.date_range(positions.index.min(), cf.trading_days.max(), freq='D')
positions = positions.reindex(full_range, method='ffill')
positions = positions.reindex(cf.trading_days).replace(-np.inf, np.nan)
```

## Performance Issues

### Slow Backtest

```python
# ❌ Slow - row iteration
for date in close.index:
    row = close.loc[date]
    # process row...

# ✅ Fast - vectorized
momentum = close.pct_change(20, fill_method=None)  # operates on entire DataFrame
```

### Memory Issues

```python
# ❌ Loading unnecessary data
open_p = cf.get_df("price_open")
high = cf.get_df("price_high")
low = cf.get_df("price_low")
close = cf.get_df("price_close")  # Only need this one

# ✅ Load only what you need
close = cf.get_df("price_close")
```

## Validation Script

Run before backtest to catch issues early:

```bash
python scripts/alpha_validator.py --code alpha.py --universe kr_stock
```

Checks:
- **Class Name**: Must be "Alpha"
- **Path Independence**: Same dates must return same values
- **Trading Days**: Position index must match universe calendar

## See Also

- `framework.md` - Rule definitions and examples
- `../scripts/finalize.py` - All-in-one validation, backtest, chart, info
