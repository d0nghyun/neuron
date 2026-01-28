# crypto_test (Crypto Perpetuals)

High-frequency cryptocurrency data - Binance Perpetual USDT margin (10-minute candles).

## Quick Start

```python
from finter.data import ContentFactory
from finter.backtest import Simulator

# ContentFactory
cf = ContentFactory('crypto_test', start=20241201, end=20241210)

# Simulator
sim = Simulator('crypto_test', start=20241201, end=20241210)
```

## Available Items

### Price (bnp_usdt) - Basic OHLCV

| Item | Description |
|------|-------------|
| `open` | 10-min candle open price |
| `high` | 10-min candle high price |
| `low` | 10-min candle low price |
| `close` | 10-min candle close price |
| `volume` | Trading volume (base currency) |
| `turnover` | Trading value (USDT) |
| `trade_count` | Number of trades |
| `taker_buy_volume` | Taker buy volume |
| `taker_buy_turnover` | Taker buy value |

### Premium Index (bnp_premium_index_usdt)

| Item | Description |
|------|-------------|
| `premium_open` | Premium Index open |
| `premium_high` | Premium Index high |
| `premium_low` | Premium Index low |
| `premium_close` | Premium Index close |

### Liquidation (bnp_forced_orders_usdt)

| Item | Description |
|------|-------------|
| `liq_buy_volume` | Forced liquidation buy volume |
| `liq_buy_turnover` | Forced liquidation buy value |
| `liq_sell_volume` | Forced liquidation sell volume |
| `liq_sell_turnover` | Forced liquidation sell value |

## Usage Examples

```python
# Basic usage
close = cf.get_df('close')
volume = cf.get_df('volume')

# Load all OHLCV
ohlcv = {item: cf.get_df(item) for item in ['open', 'high', 'low', 'close', 'volume']}

# Premium Index
premium = cf.get_df('premium_close')

# Liquidation
liq_buy = cf.get_df('liq_buy_volume')
liq_sell = cf.get_df('liq_sell_volume')
```

## Data Format

- **Index**: DatetimeIndex (timezone-naive, UTC based)
- **Columns**: Asset codes (BTCUSDT, ETHUSDT, ...)
- **Frequency**: 10-minute candles (600 seconds)
- **Values**: float64

```python
df = cf.get_df('close')
print(df.shape)                        # (rows, cols)
print(df.index[1] - df.index[0])       # 0 days 00:10:00
print(df.columns.tolist()[:5])         # ['BTCUSDT', 'ETHUSDT', ...]
```

## Simulator Backtest

### Settings

| Parameter | Value | Description |
|-----------|-------|-------------|
| initial_cash | $100,000 | Initial capital (USD) |
| buy_fee_tax | 7.5bp | Buy commission (BNB discount applied) |
| sell_fee_tax | 7.5bp | Sell commission |
| slippage | 3bp | Slippage (measured at $100k) |
| base_currency | USD | Base currency |

### Position Units

**IMPORTANT**: Position values are USD amounts (NOT ratios 0-1)

```python
import pandas as pd

# WRONG - using ratios
# position['BTCUSDT'] = 0.5  # WRONG!

# CORRECT - using USD amounts
position = pd.DataFrame(0.0, index=close.index, columns=close.columns)
position['BTCUSDT'] = 50_000  # $50k
position['ETHUSDT'] = 50_000  # $50k
```

### Running Backtest

```python
result = sim.run(position=position)

# Check results
result.summary        # NAV, returns, etc.
result.statistics     # Sharpe, MDD, etc.

# Visualization
result.summary['nav'].plot(title='NAV (10min frequency)')
```

## Time Conversion

- 1 period = 10 minutes
- 6 periods = 1 hour
- 144 periods = 1 day
- 1008 periods = 1 week

## Search & Help

```python
# Item list
cf.item_list

# Search
cf.search('volume')      # volume-related items
cf.search('liquidation') # liquidation-related items

# Usage info
cf.usage('close')
cf.usage('liq_buy_volume')
```

## Notes

- **Test universe**: Universe name may change in production release
- **High-frequency data**: 10-min candles (144x more data than daily)
- **Position units**: USD amounts (NOT ratios)
- **Submit**: Currently not available (backtest only)
