# Finter API Reference

Quick reference for Finter data access and backtesting methods.

## ContentFactory

Load market data across FINTER universes.

### Initialization

```python
from finter.data import ContentFactory
from helpers import get_start_date

# Basic usage
cf = ContentFactory(
    universe="kr_stock",  # See universe_reference.md for all available universes
    start=get_start_date(20240101, buffer=365),
    end=20240201
)
```

### Key Methods

#### get_df(item_name)

Returns DataFrame with dates as index, stocks as columns.

```python
# Basic price data (works across all universes)
close = cf.get_df("price_close")
open_price = cf.get_df("price_open")
high = cf.get_df("price_high")
low = cf.get_df("price_low")

# Always search first - item names vary by universe!
# See universe_reference.md for available items
results = cf.search("volume")  # Find volume-related items
results = cf.search("book")    # Find value factors
```

**Returns:** `pd.DataFrame` with shape (dates, stocks)

#### summary()

Prints available data categories. Returns `None`.

```python
cf.summary()
# Output categories:
# - Economic
# - Event
# - Financial
# - Index
# - Market
# - Quantitative
# - Unstructured
```

#### search(term)

Find data items containing search term.

```python
# Find all price-related items
price_items = cf.search("price")
# Returns: ['price_close', 'price_open', 'price_high', 'price_low', ...]

# Find volume items
volume_items = cf.search("volume")

# Find ratio items
ratio_items = cf.search("ratio")
```

**Returns:** List of matching item names

**For available data items by universe, see `universe_reference.md`.**

### Best Practices

#### Load with Buffer

Always load more historical data than needed:

```python
from helpers import get_start_date

# ✓ Correct - load extra historical data
cf = ContentFactory("kr_stock", get_start_date(start, buffer=365), end)
```

#### Handle Missing Data

```python
# Check for missing values
data = cf.get_df("price_close")
print(f"Missing values: {data.isnull().sum().sum()}")

# Forward fill missing values
data_filled = data.fillna(method='ffill')

# Or drop stocks with too many missing values
threshold = 0.9  # At least 90% data
valid_stocks = data.notna().sum() / len(data) >= threshold
data_clean = data.loc[:, valid_stocks]
```

## Symbol Search

Find FINTER IDs for specific stocks.

### Correct Usage (Must instantiate first!)

```python
from finter.data import Symbol

# ✓ CORRECT - Create instance first, then search
symbol = Symbol("us_stock")  # Create instance with universe
result = symbol.search("palantir")  # Returns DataFrame!

# IMPORTANT: result is a DataFrame with FINTER IDs in the INDEX
finter_id = result.index[0]  # Get FINTER ID from index
print(f"FINTER ID: {finter_id}")

# ❌ WRONG - This will not work!
result = Symbol.search("palantir", universe="us_stock")  # NO!
```

**Result Format:**
- Returns: `pd.DataFrame` with stock information
- FINTER ID location: `result.index` (NOT a column!)
- Get first match: `result.index[0]`

### Find Multiple Stock IDs

```python
from finter.data import Symbol

# Korean stocks
symbol = Symbol("kr_stock")
samsung_id = symbol.search("삼성전자").index[0]
sk_id = symbol.search("SK하이닉스").index[0]
naver_id = symbol.search("NAVER").index[0]

print(f"Samsung: {samsung_id}")
print(f"SK Hynix: {sk_id}")
print(f"NAVER: {naver_id}")

# US stocks
us_symbol = Symbol("us_stock")
pltr_id = us_symbol.search("palantir").index[0]
print(f"Palantir: {pltr_id}")
```

### Use in Alpha Strategy

**IMPORTANT**: Find IDs first, then hardcode them.

```python
# Step 1: Find IDs (run this ONCE, outside Alpha class)
from finter.data import Symbol

symbol = Symbol("us_stock")
pltr_id = symbol.search("palantir").index[0]
nvda_id = symbol.search("nvidia").index[0]
# Output: pltr_id = "12345", nvda_id = "67890"

# Step 2: Hardcode IDs in your Alpha class
class Alpha(BaseAlpha):
    def get(self, start, end):
        target_ids = ["12345", "67890"]  # Hardcoded from above
        close = cf.get_df("price_close")[target_ids]
        # ...
```

**Why FINTER IDs?** FINTER uses unique numeric IDs instead of tickers to prevent symbol conflicts over time.

See `templates/examples/stock_selection.py` for complete example.

## Backtest Simulator

Test alpha strategies with realistic market conditions.

### Basic Usage

```python
from finter.backtest import Simulator

# Initialize simulator
simulator = Simulator(market_type="kr_stock")

# Run backtest
result = simulator.run(position=positions)

# Access results
stats = result.statistics
summary = result.summary
```

### Market Types

Supported market types: `kr_stock`, `us_stock`, `crypto_test`, and more.

**See `universe_reference.md` for complete list and universe-specific details.**

```python
# Example
simulator = Simulator(market_type="kr_stock")
```

### Result Analysis

```python
result = simulator.run(position=positions)

# Performance metrics (pd.Series)
stats = result.statistics

print(f"Total Return: {stats['Total Return (%)']:.2f}%")
print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"Max Drawdown: {stats['Max Drawdown (%)']:.2f}%")
print(f"Hit Ratio: {stats['Hit Ratio (%)']:.2f}%")

# Daily data (pd.DataFrame)
summary = result.summary

nav = summary['nav']                    # Net asset value (starts at 1000)
daily_returns = summary['daily_return'] # Daily returns
costs = summary['cost']                 # Transaction costs (fee + tax)
slippage = summary['slippage']          # Slippage costs
target_turnover = summary['target_turnover']  # Daily turnover ratio (1.0 = 100% of AUM)

# Turnover ratio calculation (annualized)
# target_turnover is already a ratio (1.0 = 100% of AUM)
avg_daily_turnover = target_turnover.mean()
annual_turnover_ratio = avg_daily_turnover * 252  # e.g., 0.05 daily → 12.6x annual

# Cost vs Return analysis
avg_aum = summary['aum'].mean()
total_cost = costs.sum() + slippage.sum()
gross_return = (nav.iloc[-1] / nav.iloc[0] - 1) * 100
cost_drag = (total_cost / avg_aum) * 100  # Cost as % of AUM

# IMPORTANT: NAV starts at 1000 (NOT 1e8!)
# Position AUM = 1e8, but NAV = 1000
# Final NAV = 1000 * (1 + Total Return / 100)
```

### Key Performance Metrics

Available in `result.statistics`:

- `Total Return (%)`: Total portfolio return for the entire backtest period.
- `CAGR (%)`: Compound Annual Growth Rate (mean annualized return).
- `Volatility (%)`: Annualized standard deviation of returns.
- `Hit Ratio (%)`: Proportion of profitable days.
- `Sharpe Ratio`: Annualized risk-adjusted return.
- `Sortino Ratio`: Downside risk-adjusted return.
- `Max Drawdown (%)`: Largest peak-to-trough loss during the backtest.
- `Mean Drawdown (%)`: Average drawdown size.
- `Calmar Ratio`: Total return divided by absolute maximum drawdown.
- `Avg Tuw`: Average time underwater (days with drawdown).
- `Max Tuw`: Maximum time underwater during the backtest.
- `Skewness`: Skewness of daily returns distribution.
- `Kurtosis`: Kurtosis of daily returns distribution.
- `VaR 95% (%)`: 95% Value-at-Risk (downside risk).
- `VaR 99% (%)`: 99% Value-at-Risk (larger downside risk).
- `Positive HHI`: Herfindahl-Hirschman Index for positive returns concentration.
- `Negative HHI`: Herfindahl-Hirschman Index for negative returns concentration.
- `K Ratio`: Slope of equity curve divided by its standard error (performance persistence).

**IMPORTANT**: There is NO `Annual Return (%)` field! Use `Total Return (%)` instead.

### Position DataFrame Format

```python
import pandas as pd

# Positions must be DataFrame with:
# - Index: Trading dates
# - Columns: Stock tickers (FINTER IDs)
# - Values: Money allocated (≤ 1e8 total per row)

positions = pd.DataFrame({
    'STOCK_A': [5e7, 4e7, 3e7],
    'STOCK_B': [3e7, 4e7, 5e7],
    'STOCK_C': [2e7, 2e7, 2e7]
}, index=pd.date_range('2024-01-01', periods=3))

# Row sums: 1e8, 1e8, 1e8 ✓
```

## Common DataFrame Operations

### Ranking

```python
# Percentile rank (0-1)
rank_pct = df.rank(pct=True, axis=1)

# Absolute rank
rank_abs = df.rank(axis=1)

# Descending rank
rank_desc = df.rank(ascending=False, axis=1)
```

### Rolling Calculations

```python
# Rolling mean
rolling_mean = df.rolling(window=20).mean()

# Rolling standard deviation
rolling_std = df.rolling(window=20).std()

# Exponential weighted moving average
ewma = df.ewm(span=20).mean()
```

### Cross-Sectional Operations

```python
# Row-wise operations (per date)
row_sum = df.sum(axis=1)
row_mean = df.mean(axis=1)
row_std = df.std(axis=1)

# Normalize each row
normalized = df.div(df.sum(axis=1), axis=0)

# Z-score per row (cross-sectional)
mean = df.mean(axis=1)
std = df.std(axis=1)
z_score = df.sub(mean, axis=0).div(std, axis=0)
```

### Filtering

```python
# Keep only values above threshold
filtered = df[df > threshold]

# Replace values below threshold with 0
filtered = df.where(df > threshold, 0)

# Select top K stocks per day
top_k = df.rank(axis=1, ascending=False) <= k
```

## Date Formatting

Always use YYYYMMDD integer format:

```python
# ✓ Correct formats
start = 20240101
end = 20241231

# Convert datetime to YYYYMMDD
from datetime import datetime
dt = datetime(2024, 1, 1)
date_int = int(dt.strftime("%Y%m%d"))  # 20240101

# Convert YYYYMMDD to string for DataFrame indexing
date_str = str(20240101)  # "20240101"
data.loc[date_str:date_str]
```

## See Also

- `framework.md` - BaseAlpha framework overview
- `../templates/` - Ready-to-use strategy templates
- `troubleshooting.md` - Common mistakes and solutions
