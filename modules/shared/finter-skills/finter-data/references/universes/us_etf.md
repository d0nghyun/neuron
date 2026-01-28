# us_etf

US ETF market data.

## Search Pattern

```python
from finter.data import ContentFactory
cf = ContentFactory('us_etf', 20200101, 20241201)

# Market data
cf.search('price')
cf.search('volume')
cf.search('return')
```

## Common Items

| Category | Item | Description |
|----------|------|-------------|
| Price | `price_close` | Close price |
| Price | `price_open` | Open price |
| Price | `price_high` | High price |
| Price | `price_low` | Low price |
| Volume | `trading_volume` | Trading volume |
| Factor | `adjust_factor` | Adjustment factor |
| Factor | `total_return_factor` | Total return factor |

## ID System

- Uses 8-digit gvkeyiid format (same as us_stock)
- Example: `00135201`, `01034201`

## Gotchas

- **No financial data**: ETFs don't have quarterly statements
- **No pit- items**: Only market data available
- Limited to ~14 market items

## Example

```python
cf = ContentFactory('us_etf', 20200101, 20241201)

# Load ETF prices
close = cf.get_df('price_close')
volume = cf.get_df('trading_volume')

# Calculate returns
returns = close.pct_change()
```
