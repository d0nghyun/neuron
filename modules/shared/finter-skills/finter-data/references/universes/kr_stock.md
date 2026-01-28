# kr_stock

Korean stock market data.

## Search Pattern

Use `krx-spot-` prefix for financial data:

```python
from finter.data import ContentFactory
cf = ContentFactory('kr_stock', 20200101, 20241201)

# Financial items
cf.search('krx-spot-')
cf.search('krx-spot-sales')
cf.search('krx-spot-owners')

# Market items
cf.search('price')
cf.search('volume')
```

## Common Items

| Category | Item | Description |
|----------|------|-------------|
| Price | `price_close` | Close price |
| Volume | `volume_sum` | Trading volume |
| Financial | `krx-spot-sales` | Revenue |
| Financial | `krx-spot-operating_income` | Operating income |
| Financial | `krx-spot-owners_of_parent_net_income` | Net income |
| Financial | `krx-spot-owners_of_parent_equity` | Equity |
| Financial | `krx-spot-total_assets` | Total assets |

## ID System

- Single ID system (int64)
- No conversion needed between price and financial data

## Code Maps

```python
cf.code_map('gics')  # GICS industry codes (11 sectors)
```

**GICS data:** `krx-spot-gics` (returns str). See `gics.md` for sector analysis patterns.

## Gotchas

**krx-spot with get_df():**
```python
# ⚠️ krx-spot items may return dict values with get_df()
df = cf.get_df('krx-spot-sales')

# ✅ Use get_fc() instead
fc = cf.get_fc('krx-spot-sales')
df = fc.to_wide()
```

## Example: ROE

```python
cf = ContentFactory('kr_stock', 20200101, 20241201)

roe = (cf.get_fc({
    'income': 'krx-spot-owners_of_parent_net_income',
    'equity': 'krx-spot-owners_of_parent_equity'
})
    .apply_rolling(4, 'sum', variables=['income'])
    .apply_rolling(4, 'mean', variables=['equity'])
    .apply_expression('income / equity')
    .to_wide())
```
