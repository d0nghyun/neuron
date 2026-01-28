# BaseAlpha Framework

Core concepts and rules for developing alpha strategies with the BaseAlpha framework.

## Overview

BaseAlpha provides a simple interface for alpha development. Implement a single method that returns position DataFrame.

## Core Structure

```python
from finter import BaseAlpha
from finter.data import ContentFactory
import pandas as pd
from helpers import get_start_date

class Alpha(BaseAlpha):
    """Your strategy description"""

    def get(self, start: int, end: int, **kwargs) -> pd.DataFrame:
        """
        Generate alpha positions for date range.

        Parameters
        ----------
        start : int
            Start date in YYYYMMDD format (e.g., 20240101)
        end : int
            End date in YYYYMMDD format (e.g., 20241231)
        **kwargs : dict
            Strategy parameters for customization

        Returns
        -------
        pd.DataFrame
            Position DataFrame with:
            - Index: Trading dates
            - Columns: Stock tickers (FINTER IDs)
            - Values: Position sizes (money allocated, row sum ≤ 1e8)
        """
        # Implementation here
        pass
```

## Required Rules

### 1. Class Name Must Be "Alpha"

```python
# ✓ Correct
class Alpha(BaseAlpha):
    pass

# ❌ Wrong - will not be recognized
class MyAlpha(BaseAlpha):
    pass
```

### 2. Method Signature

Must accept `start` and `end` parameters:

```python
def get(self, start: int, end: int, **kwargs) -> pd.DataFrame:
    pass
```

### 3. Always Use fill_method=None with pct_change()

**CRITICAL**: Default `fill_method='pad'` causes path dependency with delisted stocks:

```python
# ❌ Wrong - Default pad causes path dependency
momentum = close.pct_change(20)  # fill_method='pad' by default!
# Delisted stock: start=2024-01-01 → 0.0, start=2024-06-01 → NaN

# ✓ Correct - Always specify fill_method=None
momentum = close.pct_change(20, fill_method=None)
```

**Why it matters**: Delisted stocks have NaN after delisting. `fill_method='pad'` pads with last valid price, but only if that price is in the loaded data. Different `start` dates load different data → same date gets different values.

### 4. Always Shift Positions

**CRITICAL**: Use `.shift(1)` to avoid look-ahead bias:

```python
# ❌ Wrong - using same day's signal
def get(self, start, end):
    momentum = close.pct_change(20, fill_method=None)
    positions = (momentum > 0).astype(float) * 1e8 / 10
    return positions.loc[str(start):str(end)]  # Look-ahead bias!

# ✓ Correct - using previous day's signal
def get(self, start, end):
    momentum = close.pct_change(20, fill_method=None)
    positions = (momentum > 0).astype(float) * 1e8 / 10
    return positions.shift(1).loc[str(start):str(end)]
```

### 5. Load Data with Buffer

Always load extra historical data for calculations:

```python
from helpers import get_start_date

# ❌ Wrong - insufficient data
def get(self, start, end):
    cf = ContentFactory("kr_stock", start, end)  # Not enough history
    momentum = close.pct_change(60, fill_method=None)  # Will have NaN at start

# ✓ Correct - load with proper buffer
def get(self, start, end):
    # Rule of thumb: buffer = 2x longest lookback + 250 days
    cf = ContentFactory("kr_stock", get_start_date(start, 60 * 2 + 250), end)
    momentum = close.pct_change(60, fill_method=None)  # Has enough history
```

### 6. Align to trading_days (for resampled data)

When using `resample()`, month-end dates may be non-business days. Use `-np.inf` to protect intentional NaN from ffill:

```python
positions = positions.fillna(-np.inf)  # Protect delisted NaN
full_range = pd.date_range(positions.index.min(), cf.trading_days.max(), freq='D')
positions = positions.reindex(full_range, method='ffill')
positions = positions.reindex(cf.trading_days).replace(-np.inf, np.nan)
```

### 7. Respect Position Constraints

**Long-Only (Default)**:
- Row sum ≤ 1e8
- All position values ≥ 0

```python
# Validate long-only positions
row_sums = positions.sum(axis=1)
assert (row_sums <= 1e8).all(), f"Row sums exceed AUM: {row_sums.max()}"
assert (positions >= 0).all().all(), "Long-only: no negative positions allowed"
```

**Long-Short**:
- Abs sum ≤ 1e8: `positions.abs().sum(axis=1) ≤ 1e8`
- Positive = Long, Negative = Short
- Cash = 1e8 - abs_sum

```python
# Validate long-short positions
abs_sums = positions.abs().sum(axis=1)
assert (abs_sums <= 1e8).all(), f"Abs sums exceed AUM: {abs_sums.max()}"

# Cash calculation
cash = 1e8 - abs_sums
```

**Long-Short Examples**:
| Long | Short | abs_sum | Cash | Description |
|------|-------|---------|------|-------------|
| 0.5e8 | -0.5e8 | 1e8 | 0 | 1:1 L/S, fully invested |
| 0.4e8 | -0.4e8 | 0.8e8 | 0.2e8 | 20% cash |
| 0.3e8 | -0.3e8 | 0.6e8 | 0.4e8 | 40% cash |

## Position Value Semantics

**IMPORTANT**: Positions represent **absolute holding amounts**, not signals.

```python
# Long-Only position values:
# 1e8 = Hold 100% of AUM in that stock
# 5e7 = Hold 50% of AUM
# 0 = No position (cash or fully sold)

# Long-Short position values:
# 5e7 = Long 50% of AUM
# -5e7 = Short 50% of AUM
# abs_sum = total notional exposure
```

### Position Continuity

Positions are **持续的** - you must specify position size **every day**:

```python
# Example: Buy and hold Samsung, then partially sell
positions = pd.DataFrame({
    'SAMSUNG': [0,    1e8,  1e8,  1e8,  0.5e8, 0    ],
}, index=[         'D1', 'D2', 'D3', 'D4', 'D5', 'D6'])

# Interpretation:
# D1: No position (cash)
# D2: Buy Samsung with 100% AUM
# D3-D4: Hold Samsung at 100%
# D5: Reduce to 50% AUM (sell half)
# D6: Exit position completely (sell remaining)
```

**Key Concept**: This is NOT a signal (1/-1), it's the actual position size you want to hold.

## Return DataFrame Format

```python
# Example valid positions DataFrame
positions = pd.DataFrame({
    'STOCK_A': [5e7, 3e7, 2e7],
    'STOCK_B': [3e7, 5e7, 4e7],
    'STOCK_C': [2e7, 2e7, 4e7]
}, index=['2024-01-01', '2024-01-02', '2024-01-03'])

# Row sums: 1e8, 1e8, 1e8 ✓
```

**Requirements:**
- **Index**: Trading dates (datetime or string format)
- **Columns**: Stock tickers (FINTER IDs)
- **Values**: Position sizes in monetary units
- **Constraint**: Row sum ≤ 1e8 (100 million = total AUM)

## Data Loading

### Using ContentFactory

```python
from finter.data import ContentFactory
from helpers import get_start_date

# Initialize
cf = ContentFactory(
    universe="kr_stock",  # or "us_stock", "crypto_test"
    start=get_start_date(start, buffer=365),
    end=end
)

# Load data (always search first!)
close = cf.get_df("price_close")

# Find other items specific to your universe
# cf.search("volume")  # Discover volume items
# cf.search("book")    # Discover valuation items
```

### Data Discovery

Item names vary by universe. **Always use `cf.search()` first!**

```python
# Example: finding volume data
results = cf.search("volume")
print(results)  # ['volume_sum', ...]

volume = cf.get_df("volume_sum")  # Use exact name from search

# For complete data reference, see references/universe_reference.md
```

## Complete Minimal Example

```python
from finter import BaseAlpha
from finter.data import ContentFactory
import pandas as pd
from helpers import get_start_date


class Alpha(BaseAlpha):
    """Simple momentum strategy."""

    def get(self, start: int, end: int, period: int = 20) -> pd.DataFrame:
        # Load data with buffer
        cf = ContentFactory("kr_stock", get_start_date(start, period * 2 + 250), end)
        close = cf.get_df("price_close")

        # Calculate momentum (always use fill_method=None!)
        momentum = close.pct_change(period, fill_method=None)

        # Select positive momentum stocks
        selected = momentum > 0

        # Equal weight, 1e8 == 100% of AUM
        positions = selected.div(selected.sum(axis=1), axis=0) * 1e8

        # CRITICAL: Always shift positions to avoid look-ahead bias
        return positions.shift(1).loc[str(start):str(end)]
```

## Parameter Handling

```python
class Alpha(BaseAlpha):
    """Parameterized strategy."""

    def get(self, start: int, end: int, **kwargs) -> pd.DataFrame:
        # Extract with defaults
        momentum_period = kwargs.get("momentum_period", 20)
        top_percent = kwargs.get("top_percent", 0.9)

        # Implementation...
```

## Turnover Management

### Why Turnover Matters

Every position change has costs (commissions, slippage, market impact). High turnover can destroy an otherwise good strategy.

```
Example: 2000 stock universe, daily rebalancing
- 50% of positions change daily → 1000 trades/day
- Annual turnover: ~25,000%
- At 0.1% cost per trade: 25% annual drag
- Your 30% gross return → 5% net return
```

### Check Signal Stability BEFORE Full Backtest

```python
# After creating your signal, BEFORE positions:
signal = momentum_score  # or whatever your signal is

# Count how many stocks change signal direction each day
daily_changes = (signal.diff() != 0).sum(axis=1)
print(f"Avg daily changes: {daily_changes.mean():.0f} / {len(signal.columns)} stocks")
print(f"Max daily changes: {daily_changes.max():.0f}")

# Rule of thumb:
# - < 10% of universe changing daily → OK for daily rebalancing
# - 10-30% changing daily → consider weekly rebalancing
# - > 30% changing daily → signal is too noisy, needs smoothing or monthly rebalancing
```

### Signal Smoothing Techniques

**When signal is too noisy:**

```python
# Option 1: Rolling average (smooths the signal)
smoothed_signal = signal.rolling(5).mean()

# Option 2: Reduce rebalancing frequency (monthly)
monthly_signal = signal.resample('ME').last()
positions = monthly_signal.reindex(trading_days, method='ffill')

# Option 3: Require consecutive signals (confirmation)
confirmed = (signal > 0) & (signal.shift(1) > 0) & (signal.shift(2) > 0)
```

### DON'T Over-Smooth

**Smoothing is NOT always better.** Consider the signal type:

| Signal Type | Natural Frequency | Smoothing Advice |
|-------------|-------------------|------------------|
| Momentum (20d+) | Slow | Usually OK as-is |
| Mean reversion | Medium | Light smoothing or weekly |
| News/Events | Fast | DON'T smooth - capture the edge quickly |
| Earnings | Event-driven | DON'T smooth - trade around event |

**Key insight:** If your signal is SUPPOSED to be fast (event-driven), smoothing destroys the edge. If it's supposed to be slow (value/momentum), daily noise is just noise.

### Turnover Estimation

```python
# Estimate turnover from positions
def estimate_turnover(positions: pd.DataFrame) -> float:
    """Estimate annual turnover percentage."""
    daily_turnover = positions.diff().abs().sum(axis=1) / positions.abs().sum(axis=1)
    annual_turnover = daily_turnover.mean() * 252 * 100  # Convert to %
    return annual_turnover

turnover = estimate_turnover(positions)
print(f"Estimated annual turnover: {turnover:.0f}%")

# Guidelines:
# < 500%: Low turnover (value/quality strategies)
# 500-2000%: Medium turnover (momentum strategies)
# > 2000%: High turnover - check if signal warrants it
```

## See Also

- `../templates/` - Ready-to-use strategy templates
- `api_reference.md` - ContentFactory and data access methods
- `research_process.md` - Research methodology
- `troubleshooting.md` - Common mistakes and debugging
