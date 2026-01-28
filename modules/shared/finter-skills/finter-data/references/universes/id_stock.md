# id_stock

Indonesian stock market data.

## Search Pattern

```python
cf = ContentFactory('id_stock', 20200101, 20241201)

cf.search('price')
cf.search('volume')
cf.search('sector')
```

## Common Items

| Category | Item | Description |
|----------|------|-------------|
| Price | `price_close` | Close price |
| Volume | `volume_sum` | Trading volume (**not** `trading_volume`!) |
| Other | `sharia` | Sharia compliance (binary) |
| Other | `sector_code` | Sector classification |
| Other | `adjust_factor` | Adjustment factor |

## ID System

- Ticker-style IDs (e.g., 'AADI', 'AALI', 'BBCA')
- Consistent across datasets

## FinancialCalculator (FC) Support

id_stock supports `get_fc()` for financial statement data.

```python
cf = ContentFactory("id_stock", 20230101, 20250101)

# Single item
fc = cf.get_fc("assets")
df = fc.to_wide()

# Rolling calculation (4-quarter sum)
df = cf.get_fc("assets").apply_rolling(quarters=4, operation='sum').to_wide()

# Multiple items + expression
df = cf.get_fc({
    'assets': 'assets',
    'current': 'current_assets'
}).apply_expression('assets - current').to_wide()
```

**Available financial items:**
- Financial Statements: `assets`, `current_assets`, `gross_profit`, `cost_of_sales_and_revenue`, etc.
- Ratios: `asset_turnover`, `gross_profit_margin`, `net_profit_margin`, etc.

**Note:** `get_fc()` is for Financial category items only. Use `get_df()` for Market category (price, volume).

## Gotchas

**Volume item name:**
```python
# ❌ Wrong
cf.get_df('trading_volume')  # Not found!

# ✅ Correct
cf.get_df('volume_sum')
```

Use `cf.search()` to check available items before loading.
