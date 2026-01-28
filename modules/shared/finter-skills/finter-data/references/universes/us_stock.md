# us_stock

US stock market data (Compustat).

## Search Pattern

Use `pit-` prefix or English description:

```python
from finter.data import ContentFactory
cf = ContentFactory('us_stock', 20200101, 20241201)

# By prefix
cf.search('pit-')
cf.search('pit-sale')

# By description (English keywords)
cf.search('Revenue')
#                        description  note
# pit-revtq        Revenue - Total   None
# pit-drcq   Deferred Revenue - Cur   None

cf.search('Assets')
cf.search('Income')
```

## Item Description

```python
# Get description and usage notes
cf.get_description('gics')
# ('GICS Industry Classification Code', "cf.code_map('gics', level=...)")

cf.get_description('pit-atq')
# ('Assets - Total', None)
```

## Common Items (Compustat Mnemonics)

| Mnemonic | Description |
|----------|-------------|
| `price_close` | Close price |
| `trading_volume` | Trading volume |
| `pit-saleq` | Sales/Revenue - Quarterly |
| `pit-revtq` | Revenue - Total |
| `pit-niq` | Net Income |
| `pit-atq` | Assets - Total |
| `pit-seqq` | Stockholders Equity |
| `pit-cogsq` | Cost of Goods Sold |
| `pit-oiadpq` | Operating Income After Depreciation |

## ID System ⚠️

**Two ID types:**

| Term | Description | Example |
|------|-------------|---------|
| gvkey | Company ID (6-digit) | 001004 |
| gvkeyiid | Security ID (8-digit) | 00100401 |
| iid | Security suffix (2-digit) | 01 |

Relation: `gvkeyiid = gvkey + iid`

**Data by ID type:**

| Data Type | Method | ID Format |
|-----------|--------|-----------|
| Price/Market | `get_df()` | gvkeyiid (8-digit) |
| Financial | `get_fc()` | gvkey (6-digit) |

## ID Conversion

**Automatic (recommended):**
```python
fc = cf.get_fc('pit-saleq')
df = fc.to_wide()  # Automatically converts to gvkeyiid
```

**Manual:**
```python
df = cf.get_df('saleq')  # 6-digit gvkey columns
df_security = cf.to_security(df)  # 8-digit gvkeyiid columns
```

**Note:** `to_security()` is us_stock only.

## Code Maps

```python
cf.code_map('gics')              # Sector (11)
cf.code_map('gics', level=2)     # Industry Group (27)
cf.code_map('gics', level=3)     # Industry (84)
cf.code_map('gics', level=4)     # Sub-Industry (215)
cf.code_map('gics', level=0)     # All (337)
```

## Gotchas

- `pit-` prefix auto-applies `mode='original'` for fiscal info preservation
- Price data (8-digit) and financial data (6-digit) have different ID systems
- Use `to_wide()` or `to_security()` for ID alignment
- **GICS**: Use `stock_level=True` when merging with price data (see `gics.md`)

## Example: ROE

```python
cf = ContentFactory('us_stock', 20200101, 20241201)

roe = (cf.get_fc({
    'income': 'pit-niq',
    'equity': 'pit-seqq'
})
    .apply_rolling(4, 'sum', variables=['income'])
    .apply_rolling(4, 'mean', variables=['equity'])
    .apply_expression('income / equity')
    .to_wide())  # Auto-converts to gvkeyiid
```
