# vn_stock

Vietnam stock market data.

## Search Pattern

PascalCase naming:

```python
cf = ContentFactory('vn_stock', 20200101, 20241201)

cf.search('Close')
cf.search('Price')
cf.search('EPS')
```

## Common Items

| Category | Item | Description |
|----------|------|-------------|
| Price | `ClosePrice` | Close price |
| Volume | `TotalVolume` | Trading volume |
| Financial | `EPS` | Earnings per share |
| Financial | `total_assets` | Total assets |
| Classification | `fiintek-gics` | GICS code |

## ID System

- Irregular ID lengths (3-11 digits)
- String IDs
- IDs are consistent across datasets (coverage may differ)

## Code Maps

```python
cf.code_map('gics')  # GICS industry codes
```

**GICS data:** `fiintek-gics`. See `gics.md` for sector analysis patterns.

## Gotchas

- Column counts differ by item (coverage difference, not ID mismatch)
- Some `total_assets` values are negative (data issue?)
- Use inner join when merging different items
