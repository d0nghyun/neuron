# GICS Usage Guide

GICS (Global Industry Classification Standard) sector analysis patterns.

## Loading by Universe

| Universe | Item Name | Value Type | Notes |
|----------|-----------|------------|-------|
| kr_stock | `krx-spot-gics` | str | - |
| us_stock | `gics` | float | `stock_level=True` required |
| vn_stock | `fiintek-gics` | float | - |
| id_stock | - | - | No GICS data |

```python
# kr_stock
gics = cf.get_df('krx-spot-gics').ffill()

# us_stock (stock_level required for price merge!)
gics = cf.get_df('gics', stock_level=True).ffill()

# vn_stock
gics = cf.get_df('fiintek-gics').ffill()
```

**Column alignment with price:**
```python
price = cf.get_df('price_close')
common = price.columns.intersection(gics.columns)
price, gics = price[common], gics[common]
```

## Sector Code Extraction

8-digit GICS → 2-digit sector:

```python
# Convert to numeric first (kr_stock returns str)
gics_num = gics.apply(pd.to_numeric, errors='coerce')

# Extract sector (first 2 digits)
sector = (gics_num // 1000000).astype(float)
```

**Sector codes:**
| Code | Sector |
|------|--------|
| 10 | Energy |
| 15 | Materials |
| 20 | Industrials |
| 25 | Consumer Discretionary |
| 30 | Consumer Staples |
| 35 | Health Care |
| 40 | Financials |
| 45 | Information Technology |
| 50 | Communication Services |
| 55 | Utilities |
| 60 | Real Estate |

## Code Map API

```python
cf.code_map('gics')              # Sector (11)
cf.code_map('gics', level=2)     # Industry Group (27)
cf.code_map('gics', level=3)     # Industry (84)
cf.code_map('gics', level=4)     # Sub-Industry (215)
cf.code_map('gics', level=0)     # All (337)
```

**Returns DataFrame (NOT dict!):**
```
                 description     type status
code
10                    Energy  GSECTOR      A
15                 Materials  GSECTOR      A
20               Industrials  GSECTOR      A
25    Consumer Discretionary  GSECTOR      A
...
60               Real Estate  GSECTOR      A
```

```python
# index: str, columns: description, type, status
cm = cf.code_map('gics')
cm.loc['10', 'description']  # 'Energy'

# Convert to dict if needed
sector_map = dict(zip(cm.index, cm['description']))
# {'10': 'Energy', '15': 'Materials', ...}
```

## Sector-Level Analysis

**Sector average returns:**
```python
ret = price.pct_change()

# Long format
ret_long = ret.stack().rename('return')
sector_long = sector.stack().rename('sector')
df = pd.concat([ret_long, sector_long], axis=1).dropna()

# Sector mean
sector_ret = df.groupby([df.index.get_level_values(0), 'sector'])['return'].mean().unstack()
```

## Sector Neutralization

Remove sector effects from factors:

```python
def sector_neutralize(factor_df, gics_df):
    """Subtract sector mean from factor values."""
    gics_num = gics_df.apply(pd.to_numeric, errors='coerce')
    sector = (gics_num // 1000000).astype(float)

    f_long = factor_df.stack().rename('factor')
    s_long = sector.stack().rename('sector')
    df = pd.concat([f_long, s_long], axis=1).dropna()

    df['neutral'] = df.groupby(
        [df.index.get_level_values(0), 'sector']
    )['factor'].transform(lambda x: x - x.mean())

    return df['neutral'].unstack()

# Usage
momentum = price.pct_change(252)
neutral_mom = sector_neutralize(momentum, gics)  # mean ≈ 0
```

## Gotchas

- **us_stock**: Must use `stock_level=True` (GICS is company-level by default)
- **kr_stock**: Returns string type, convert with `pd.to_numeric()`
- **ffill()**: Always apply to handle update delays
- **id_stock**: No GICS data available
