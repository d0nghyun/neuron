# Universe Reference

Special cases and exceptions for Finter data universes.

## Overview

All universes use the **same framework** (BaseAlpha, ContentFactory, Simulator). For quick comparison, see SKILL.md.

**This document covers ONLY special cases and exceptions.**

**General rule**: Use `cf.search()` and `cf.summary()` to explore data - don't memorize item names!

## Standard Usage (Most Universes)

Works for: `kr_stock`, `us_stock`, `us_etf`, `id_stock`

```python
from finter.data import ContentFactory

# 1. Initialize
cf = ContentFactory("kr_stock", 20200101, int(datetime.now().strftime("%Y%m%d")))

# 2. Explore (DON'T SKIP THIS!)
cf.summary()  # View categories
results = cf.search("price")  # Find items

# 3. Load data
close = cf.get_df("price_close")
```

**Minor differences:**
- `id_stock`: Use `volume_sum` instead of `trading_volume`
- `us_etf`: Market data only (no fundamentals)

**Symbol search** works for all universes - use `Symbol(universe).search(ticker)` to find FINTER IDs.

## Special Case 1: Vietnamese Stocks (vn_stock)

### PascalCase Naming Convention

⚠️ **vn_stock uses PascalCase**, unlike all other universes:

```python
from finter.data import ContentFactory

cf = ContentFactory("vn_stock", 20200101, int(datetime.now().strftime("%Y%m%d")))

# ⚠️ Use PascalCase names
close = cf.get_df("ClosePrice")      # NOT price_close
open_price = cf.get_df("OpenPrice")  # NOT price_open
high = cf.get_df("HighestPrice")     # NOT price_high
low = cf.get_df("LowestPrice")       # NOT price_low

# cf.search() still works!
price_items = cf.search("price")
print(price_items)  # ['AveragePrice', 'ClosePrice', 'HighestPrice', ...]
```

**Why PascalCase?** Different data provider convention. Always `cf.search()` first!

## Special Case 2: Cryptocurrency (btcusdt_spot_binance)

### Features

Multi-crypto perpetual futures with high-frequency data:
- **~378 assets**: BTC, ETH, and major altcoins
- **10-minute candles**: High-frequency trading
- **Rich data**: OHLCV, premium index, liquidation data
- **Position units**: USD amounts (NOT ratios)

### ⚠️ CRITICAL: Memory Constraints

**USE ONLY 1 YEAR OF DATA (2024)**. 10-minute candles are VERY memory-intensive:

```
378 coins × 144 bars/day × 365 days = 19.8 million rows
378 coins × 144 bars/day × 365 days × 5 years = 99 million rows (WILL CRASH!)
```

```python
# ✅ CORRECT - 1 year maximum
cf = ContentFactory('btcusdt_spot_binance', 20240101, 20241231)

# ❌ WRONG - Will cause memory crash
cf = ContentFactory('btcusdt_spot_binance', 20200101, 20241231)  # 5 years = OOM!
cf = ContentFactory('btcusdt_spot_binance', 20220101, 20241231)  # 3 years = OOM!
```

**Rule**: Always use `20240101` as start date for btcusdt_spot_binance. Never load more than 1 year.

### Data Access

```python
from finter.data import ContentFactory

cf = ContentFactory('btcusdt_spot_binance', 20241201, int(datetime.now().strftime("%Y%m%d")))

# Search works
cf.search("volume")  # Returns volume-related items

# Load data
close = cf.get_df('close')
volume = cf.get_df('volume')
premium = cf.get_df('premium_close')
liq_buy = cf.get_df('liq_buy_volume')
```

**Available items:**
- Price: `open`, `high`, `low`, `close`, `volume`, `turnover`, `trade_count`
- Taker: `taker_buy_volume`, `taker_buy_turnover`
- Premium: `premium_open`, `premium_high`, `premium_low`, `premium_close`
- Liquidation: `liq_buy_volume`, `liq_buy_turnover`, `liq_sell_volume`, `liq_sell_turnover`

### Time Resolution: 10-Minute Candles

Unlike daily resolution for stocks, crypto uses **10-minute candles**:

```python
# Time conversions
# 1 period = 10 minutes
# 6 periods = 1 hour
# 144 periods = 1 day
# 1008 periods = 1 week

# Example: 1-day momentum
momentum = close.pct_change(144)  # 144 periods = 1 day
```

### Position Units: USD Amounts

**CRITICAL**: Positions are USD amounts, NOT ratios!

```python
import pandas as pd

# Create position DataFrame
position = pd.DataFrame(0.0, index=close.index, columns=close.columns)

# Assign USD amounts (NOT ratios)
position['BTCUSDT'] = 50_000  # $50k in BTC
position['ETHUSDT'] = 30_000  # $30k in ETH
```

### Complete Crypto Example

```python
from finter import BaseAlpha
from finter.data import ContentFactory
from finter.backtest import Simulator

class Alpha(BaseAlpha):
    def get(self, start: int, end: int, **kwargs):
        cf = ContentFactory('btcusdt_spot_binance', 20241101, end)
        close = cf.get_df('close')

        # 144 periods = 1 day (10-min candles)
        momentum = close.pct_change(144, fill_method=None)

        # Rank and select top 5
        ranks = momentum.rank(axis=1, ascending=False)
        selected = ranks <= 5

        # Position: $50k per selected asset
        positions = selected.astype(float) * 50_000

        return positions.shift(1).loc[str(start):str(end)]

# Backtest
alpha = Alpha()
positions = alpha.get(20241201, int(datetime.now().strftime("%Y%m%d")))

simulator = Simulator("btcusdt_spot_binance", 20241201, int(datetime.now().strftime("%Y%m%d")))
result = simulator.run(position=positions)
```

**See `../templates/examples/crypto_multi.py` for full working example.**

### When to Use Crypto

✅ **Suitable for:**
- Multi-crypto cross-sectional strategies
- High-frequency signals (10-min resolution)
- Momentum/trend strategies across crypto universe
- Liquidation and premium-based strategies

❌ **NOT suitable for:**
- Fundamental analysis (no fundamental data)
- Submit to production (test universe only)

## Data Discovery Best Practices

**Rule: ALWAYS search before loading data**

```python
# ✅ CORRECT workflow
cf = ContentFactory("kr_stock", 20200101, int(datetime.now().strftime("%Y%m%d")))
cf.summary()  # View categories
items = cf.search("earnings")  # Find items
print(items)  # ['earnings-to-price', 'eps_basic', ...]
data = cf.get_df("earnings-to-price")  # Use exact name

# ❌ WRONG - guessing names
data = cf.get_df("eps")  # KeyError!
data = cf.get_df("price_earnings_ratio")  # KeyError!
```

**Crypto (`btcusdt_spot_binance`)**: Search works. Use `cf.item_list` for all 17 items.

## See Also

- `../SKILL.md` - Universe comparison table (quick reference)
- `framework.md` - BaseAlpha framework rules
- `api_reference.md` - ContentFactory and Simulator API
- `../templates/examples/` - Working examples for each universe
