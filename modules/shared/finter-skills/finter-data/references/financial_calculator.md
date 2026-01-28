# FinancialCalculator API Reference

API reference for working with quarterly financial statement data using get_fc().

## Overview

FinancialCalculator provides a fluent API for:
1. Loading multiple financial items with aliases
2. Applying rolling operations (TTM, averages)
3. Calculating ratios and expressions
4. Filtering specific companies
5. Converting to wide format (pandas DataFrame)

**Internal:** Uses Polars DataFrame internally for efficient computation. Methods return FinancialCalculator (chainable) except:
- `filter()` → returns `polars.DataFrame`
- `to_wide()` → returns `pandas.DataFrame`

**When to use:** Quarterly financial statements (income, balance sheet, cash flow)

**When NOT to use:** Market data (price, volume) → use `get_df()` instead

---

## Common API

### cf.get_fc()

Load financial items with aliases for calculation.

```python
fc = cf.get_fc(item_name: str | dict, **kwargs) -> FinancialCalculator
```

**Single item:**
```python
fc = cf.get_fc('krx-spot-owners_of_parent_net_income')
```

**Multiple items (recommended):**
```python
fc = cf.get_fc({
    'alias1': 'full-item-name-1',
    'alias2': 'full-item-name-2',
})
```

**Why use dict with aliases?**
- Shorter names in expressions: `'income / equity'` vs `'krx-spot-owners_of_parent_net_income / krx-spot-owners_of_parent_equity'`
- Clearer code intent
- Auto-join multiple items on (id, pit, fiscal)

### fc.apply_rolling()

Apply rolling window operations for TTM calculations or averages.

```python
fc.apply_rolling(
    quarters: int,
    operation: str,
    variables: list[str] | None = None
) -> FinancialCalculator
```

**Parameters:**
- `quarters`: Window size (4 = TTM, 0 = latest)
- `operation`: 'sum', 'mean', 'diff', 'last'
- `variables`: **REQUIRED** when multiple columns exist

| Operation | Description | Common Use |
|-----------|-------------|------------|
| `'sum'` | Sum over N quarters | TTM revenue, TTM income |
| `'mean'` | Average over N quarters | Average equity, average assets |
| `'diff'` | Current - N quarters ago | YoY change |
| `'last'` | Latest quarter (quarters=0) | Latest balance sheet |

### fc.apply_expression()

Calculate ratios using column aliases.

```python
fc.apply_expression(expression: str) -> FinancialCalculator
```

**Example:**
```python
roe = fc.apply_expression('income / equity')
```

### fc.filter()

Filter for specific companies using Polars expressions.

```python
fc.filter(condition) -> polars.DataFrame
```

**Note:** Returns Polars DataFrame, not FinancialCalculator!

```python
import polars as pl
samsung = fc.filter(pl.col('id') == 12170)
```

### fc.to_wide()

Convert to pandas DataFrame (dates × stocks) for Alpha usage.

```python
fc.to_wide() -> pd.DataFrame
```

**Returns:** Pandas DataFrame with:
- Index: Trading dates (daily)
- Columns: Depends on whether expression was applied
  - **With expression**: Simple Int64Index (Finter IDs)
  - **Without expression**: MultiIndex (variable name, Finter ID)
- Values: Calculated values, forward-filled to trading dates

**Column behavior:**

| Scenario | Column Type | Access Pattern |
|----------|-------------|----------------|
| After `apply_expression()` | Simple index | `df[12170]` |
| Multiple variables, no expression | MultiIndex | `df.xs(12170, level=1, axis=1)` |

---

## Workflow Summary

```python
# 1. Load with aliases
fc = cf.get_fc({
    'alias1': 'item-name-1',
    'alias2': 'item-name-2'
})

# 2. Apply rolling (if needed)
fc = fc.apply_rolling(4, 'sum', variables=['alias1'])
fc = fc.apply_rolling(4, 'mean', variables=['alias2'])

# 3. Calculate ratio
fc = fc.apply_expression('alias1 / alias2')

# 4. Filter (optional, for inspection)
import polars as pl
filtered = fc.filter(pl.col('id') == 12170)

# 5. Convert to wide for Alpha
result_df = fc.to_wide()

# 6. Use in Alpha
positions = result_df.rank(axis=1, pct=True) * 1e8
```

---

## Common Mistakes

### Mistake 1: Loading items separately
```python
# ❌ WRONG - Can't combine separate fc objects
fc_income = cf.get_fc('krx-spot-owners_of_parent_net_income')
fc_equity = cf.get_fc('krx-spot-owners_of_parent_equity')

# ✅ CORRECT - Load all at once
fc = cf.get_fc({
    'income': 'krx-spot-owners_of_parent_net_income',
    'equity': 'krx-spot-owners_of_parent_equity'
})
```

### Mistake 2: Single item without dict
```python
# ⚠️ Column is 'value', not item name
fc = cf.get_fc('krx-spot-owners_of_parent_net_income')
fc.columns  # ['pit', 'id', 'fiscal', 'value']

# ✅ Use dict for explicit alias
fc = cf.get_fc({'income': 'krx-spot-owners_of_parent_net_income'})
fc.columns  # ['pit', 'id', 'fiscal', 'income']
```

### Mistake 3: Missing variables parameter
```python
# ❌ ValueError when multiple columns exist
fc = cf.get_fc({'income': '...', 'equity': '...'})
fc.apply_rolling(4, 'sum')  # Error!

# ✅ Specify which columns to roll
fc.apply_rolling(4, 'sum', variables=['income'])
```

### Mistake 4: MultiIndex column access
```python
# Without expression → MultiIndex (variable, stock_id)
wide = fc.to_wide()
wide[12170]  # KeyError!
wide.xs('12170', level=1, axis=1)  # ✅ Correct

# With expression → Simple index
wide = fc.apply_expression('income / equity').to_wide()
wide[12170]  # ✅ Works
```

### Mistake 5: Wrong operation order
```python
# ⚠️ Ratio first, then average (usually wrong)
fc.apply_expression('income / equity').apply_rolling(4, 'mean')

# ✅ Rolling first, then ratio (correct for most financial ratios)
fc.apply_rolling(4, 'sum', variables=['income'])
  .apply_rolling(4, 'mean', variables=['equity'])
  .apply_expression('income / equity')
```

---

## See Also

- `framework.md` - ContentFactory API (search, get_df, code_map)
- `universes/` - Universe-specific patterns and gotchas
  - `universes/kr_stock.md` - krx-spot- prefix, examples
  - `universes/us_stock.md` - pit- prefix, gvkey/gvkeyiid conversion
  - `universes/id_stock.md` - String IDs (ticker format)
- `templates/examples/` - Financial ratio examples
