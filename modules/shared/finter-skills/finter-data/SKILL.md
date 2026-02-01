---
name: finter-data
description: Data loading and preparation for Finter platform. Use when you need to load data, handle preprocessing, or work with different universes (e.g., "load kr_stock data", "handle missing values", "use Symbol search", "calculate ROE with financial data").
---

# Finter Data Preparation

Load and preprocess data from Finter platform for quantitative research.

## ⚠️ CRITICAL RULES (MUST FOLLOW)

### Request Type Routing (IMPORTANT!)

**1. Framework/API Usage Questions** (e.g., "How to use ContentFactory?", "get_fc usage", "fc usage", "Symbol search method"):
- ❌ DO NOT use cf.search() for API questions - search is for data discovery
- ✅ **Read skill references/ documents FIRST:**
  - `references/framework.md` - ContentFactory (cf), Symbol, get_df usage
  - `references/financial_calculator.md` - FinancialCalculator (fc), get_fc() usage
  - `references/preprocessing.md` - Preprocessing methods
  - `references/universes/*.md` - Universe-specific details

**2. Data Item Discovery** (e.g., "find close price data", "what data for ROE calculation"):
- ✅ **Use `cf.search()` in Jupyter** - Search items in current universe
- ⚠️ **ENGLISH ONLY** - `cf.search('close')` ✅, `cf.search('종가')` ❌
- ✅ **Use `cf.usage()` for guidance** - Check general or item-specific usage
- ✅ **Crypto (`btcusdt_spot_binance`)** - search works, items: `price_close`, `volume`

**NEVER guess item names. Always search first for DATA items!**

**ContentFactory Usage:**
```python
# ✅ CORRECT - All parameters in constructor
cf = ContentFactory("kr_stock", 20200101, int(datetime.now().strftime("%Y%m%d")))
data = cf.get_df("price_close")

# ❌ WRONG - Parameters in get_df
cf = ContentFactory("kr_stock")
data = cf.get_df("price_close", 20230101, 20241231)  # NO!
```

**Method Selection:**
- **Market data** (price, volume): Use `get_df()` → pandas DataFrame
- **Financial data** (statements): Use `get_fc()` → FinancialCalculator (fluent API)
  - kr_stock: search `krx-spot-*` prefix
  - us_stock: search `pit-*` prefix (see financial_calculator.md)
  - id_stock: search item (no prefix)

### cf vs fc (IMPORTANT!)

| Abbrev | Class | Creation | Purpose |
|--------|-------|----------|---------|
| **cf** | ContentFactory | `cf = ContentFactory(universe, start, end)` | Data search/load (search, get_df, get_fc) |
| **fc** | FinancialCalculator | `fc = cf.get_fc(items)` | Financial calculations (apply_rolling, apply_expression, to_wide) |

**Relationship:**
```python
# cf is a ContentFactory instance
cf = ContentFactory("kr_stock", 20200101, 20241231)

# fc is returned by cf.get_fc() (FinancialCalculator instance)
fc = cf.get_fc({'income': 'krx-spot-owners_of_parent_net_income'})

# fc chaining
result = fc.apply_rolling(4, 'sum').to_wide()
```

**cf methods:** `search()`, `get_df()`, `get_fc()`, `usage()`, `summary()`
**fc methods:** `apply_rolling()`, `apply_expression()`, `filter()`, `to_wide()`

→ fc details: `references/financial_calculator.md`

**Common Mistakes:**

**Mistake 1: Guessing item names**
```python
# ❌ WRONG - Guessing names
close = cf.get_df("closing_price")  # KeyError!

# ✅ CORRECT - Search first
results = cf.search("close")
print(results)  # ['price_close', 'adj_close', ...]
close = cf.get_df("price_close")  # Use exact name!
```

**Mistake 2: Ignoring NaN values**
```python
# ❌ WRONG - Using data without checking
close = cf.get_df("price_close")
returns = close.pct_change()  # May have NaN!

# ✅ CORRECT - Check and handle NaN
close = cf.get_df("price_close")
print(f"NaN ratio: {close.isna().sum().sum() / close.size:.2%}")
close_clean = close.ffill().bfill()  # Handle missing values
returns = close_clean.pct_change()
```

**Mistake 3: Not handling outliers**
```python
# ❌ WRONG - Raw data with extreme values
factor = cf.get_df("some_ratio")
positions = factor * 1e8  # Extreme positions!

# ✅ CORRECT - Handle outliers first
def winsorize(df, lower=0.01, upper=0.99):
    return df.clip(
        lower=df.quantile(lower, axis=1),
        upper=df.quantile(upper, axis=1),
        axis=0
    )

factor = cf.get_df("some_ratio")
factor_clean = winsorize(factor, 0.01, 0.99)
positions = factor_clean * 1e8  # Controlled positions
```

**Mistake 4: Saving figures**
```python
# ❌ WRONG - Causes API errors
import matplotlib.pyplot as plt
close.plot(figsize=(12, 6))
plt.savefig('plot.png')  # ERROR!

# ✅ CORRECT - Let Jupyter display automatically
close.plot(figsize=(12, 6))  # Displays inline, no save needed
```

### fc (FinancialCalculator) Common Mistakes

**Mistake 5: Loading items separately instead of together**
```python
# ❌ WRONG - Separate fc objects can't be combined
fc_income = cf.get_fc('krx-spot-owners_of_parent_net_income')
fc_equity = cf.get_fc('krx-spot-owners_of_parent_equity')
# These are separate! Can't calculate income/equity!

# ✅ CORRECT - Load all items at once with aliases
fc = cf.get_fc({
    'income': 'krx-spot-owners_of_parent_net_income',
    'equity': 'krx-spot-owners_of_parent_equity'
})
# Now you can: fc.apply_expression('income / equity')
```

**Mistake 6: Single item without dict - column is 'value'**
```python
# ⚠️ Single item loads as 'value' column
fc = cf.get_fc('krx-spot-owners_of_parent_net_income')
print(fc.columns)  # ['pit', 'id', 'fiscal', 'value'] - NOT item name!

# ✅ Use dict for explicit alias
fc = cf.get_fc({'income': 'krx-spot-owners_of_parent_net_income'})
print(fc.columns)  # ['pit', 'id', 'fiscal', 'income']
```

**Mistake 7: Forgetting variables parameter with multiple items**
```python
# ❌ WRONG - Missing variables parameter
fc = cf.get_fc({'income': '...', 'equity': '...'})
fc.apply_rolling(4, 'sum')  # ValueError! Which column to roll?

# ✅ CORRECT - Specify variables
fc.apply_rolling(4, 'sum', variables=['income'])  # Rolls only income
```

**Mistake 8: MultiIndex columns after to_wide() without expression**
```python
fc = cf.get_fc({'income': '...', 'equity': '...'})

# Without expression → MultiIndex columns (variable, stock_id)
wide = fc.to_wide()
wide[12170]  # KeyError! MultiIndex needs different access

# ✅ Access MultiIndex correctly
wide.xs('12170', level=1, axis=1)  # Returns income, equity for stock

# With expression → Simple columns (stock_id only)
wide2 = fc.apply_expression('income / equity').to_wide()
wide2[12170]  # Works! Simple index after expression
```

**Mistake 9: Wrong operation order**
```python
# ⚠️ Expression BEFORE rolling - semantically wrong
fc.apply_expression('income / equity').apply_rolling(4, 'mean')
# This calculates ratio first, then averages the ratio

# ✅ Rolling BEFORE expression - correct for financial ratios
fc.apply_rolling(4, 'sum', variables=['income'])  # TTM income
  .apply_rolling(4, 'mean', variables=['equity'])  # Avg equity
  .apply_expression('income / equity')  # ROE = TTM income / Avg equity
```

## 📋 Workflow

### For Simple Questions (explanation, usage, concepts)
1. **Read references/** - Find relevant documentation
2. **Answer directly** - No need to load data or run code

### For Data Tasks (load, explore, preprocess)
1. **Read Mental Models**: `references/mental_models/data_quality.md` (REQUIRED)
2. **Discovery**: `cf.search()` → find item names
3. **Load**: Use ContentFactory with correct parameters
4. **Diagnose Quality**: Ask the diagnostic questions (NaN, outliers, bias)
5. **Handle Issues**: Choose technique based on diagnosis, not habit
6. **Feature Engineering**: Transform, rank, combine (if needed)
7. **Validate**: Verify data quality before using in alpha

**⚠️ NEVER skip quality checks for data tasks!**
**⚠️ DO NOT load data unnecessarily for simple questions!**
**⚠️ DON'T default to any technique - diagnose first!**

## 🎯 First Steps

### Read the Framework First
**BEFORE loading data, read `references/framework.md`** - it explains:
- ContentFactory API (search, get_df, get_fc, usage)
- Symbol search for company IDs
- Data quality principles
- Complete discovery workflow

### Know Your Data Type
**Choose the right method:**
- **Market data** (price, volume) → `get_df()` (see framework.md)
- **Financial data** (statements) → `get_fc()` (see financial_calculator.md)

### Know Your Universe
**Each universe has different patterns.** See `references/universes/`:

| Universe | Volume Item | Financial Prefix | Guide |
|----------|-------------|------------------|-------|
| kr_stock | `volume_sum` | `krx-spot-` | `universes/kr_stock.md` |
| us_stock | `trading_volume` | `pit-` | `universes/us_stock.md` |
| us_etf | `trading_volume` | not available | `universes/us_etf.md` |
| vn_stock | `TotalVolume` | not available | `universes/vn_stock.md` |
| id_stock | `volume_sum` | ``, (no prefix) | `universes/id_stock.md` |
| btcusdt_spot_binance | `price_close`, `volume` | - | `universes/btcusdt_spot_binance.md` |

### Review Preprocessing Patterns
**See `references/preprocessing.md` for:**
- Missing value strategies
- Outlier handling methods
- Normalization techniques

## 📚 Documentation

### MUST READ (Before Data Tasks)
| Doc | Purpose |
|-----|---------|
| `references/framework.md` | ContentFactory API and data loading |
| `references/mental_models/data_quality.md` | Data quality diagnosis framework |

### Reference During Coding
| Doc | Purpose |
|-----|---------|
| `references/financial_calculator.md` | get_fc() for financial data |
| `references/preprocessing.md` | Preprocessing methods |
| `references/gics.md` | GICS sector analysis |
| `templates/examples/` | Working examples |

## ⚡ Quick Reference

**Essential imports:**
```python
from finter.data import ContentFactory, Symbol
import pandas as pd
```

**Discovery pattern:**
```python
cf = ContentFactory('kr_stock', 20230101, 20241231)

# Check usage first
cf.usage()  # General guide

# Search for items - returns DataFrame with description & note
results = cf.search('close')
print(results.to_string())  # Use .to_string() to see full results (default output truncates)
#              description  note
# price_close         None  None
# adj_close           None  None

# Get item name from index
item_name = results.index[0]  # 'price_close'

# For financial data, search with prefix
results = cf.search('krx-spot-sales')  # More specific!

# Check categories
cf.summary()  # Shows: Economic, Financial, Market, ...
```

**Symbol search (find company ID):**
```python
symbol = Symbol('kr_stock')
result = symbol.search('삼성전자')
finter_id = result.index[0]  # 12170 (ID is in INDEX, not column!)
```

**Market data loading:**
```python
# Price and volume data
close = cf.get_df('price_close')

# Volume: Use cf.search('volume') to find exact name!
# kr_stock/id_stock: 'volume_sum'  |  us_stock/us_etf: 'trading_volume'
volume = cf.get_df('volume_sum')  # kr_stock example

# Returns pandas DataFrame (dates × stocks)
print(close.shape)  # (dates, stocks)
```

**Financial data loading:**
```python
# For financial statements, use get_fc()
fc = cf.get_fc({
    'income': 'krx-spot-owners_of_parent_net_income',
    'equity': 'krx-spot-owners_of_parent_equity'
})

# Fluent API for calculations
roe = (fc
    .apply_rolling(4, 'sum', variables=['income'])
    .apply_rolling(4, 'mean', variables=['equity'])
    .apply_expression('income / equity')
    .to_wide())  # Convert to pandas DataFrame

# IMPORTANT: Single expression → simple columns
#            No expression → MultiIndex columns (level=0: variable, level=1: stock_id)
#            Use .xs(stock_id, level=1, axis=1) to access specific stock

# See financial_calculator.md for details
```

**Quality checks:**
```python
# Check NaN
print(f"NaN ratio: {close.isna().sum().sum() / close.size:.2%}")

# Check distributions
print(close.describe())

# Check outliers
print(f"Min: {close.min().min()}, Max: {close.max().max()}")
```

**Visualization (IMPORTANT):**
```python
# NEVER set font family - causes errors in Jupyter environment
# ❌ WRONG
plt.rcParams['font.family'] = 'sans-serif'  # Will error!

# ✅ CORRECT - Use default settings
close.plot(figsize=(12, 6), title='Price History')  # Just plot!
close.hist(bins=50, figsize=(10, 6))
```

**Data quality handling:**

DON'T default to any specific technique. Before handling NaN, outliers, or normalization:

1. **Diagnose the issue** - Read `references/mental_models/data_quality.md`
2. **Ask diagnostic questions** - Why is this value missing/extreme?
3. **Choose technique based on diagnosis** - Not based on habit

```python
# Diagnosis first
print(f"NaN ratio: {df.isna().sum().sum() / df.size:.2%}")
print(f"Values > 3 std: {(df > df.mean() + 3*df.std()).sum().sum()}")

# Then decide on technique based on your diagnosis
# See references/mental_models/data_quality.md for decision frameworks
```

## 🔍 When to Use This Skill

**Use finter-data when:**
- ✅ Loading data from Finter (any universe, any data type)
- ✅ Discovering available data items
- ✅ Handling missing values or outliers
- ✅ Normalizing or transforming features
- ✅ Finding company IDs by name (Symbol search)
- ✅ Working with financial statements (get_fc)
- ✅ Checking data quality before analysis

**Don't use for:**
- ❌ Alpha strategy logic (use finter-alpha)
- ❌ Portfolio optimization (use finter-portfolio)
- ❌ Performance evaluation (use finter-evaluation)

**Workflow integration:**
- finter-data → **Load & preprocess data**
- finter-alpha → **Generate alpha signals**
- finter-evaluation → **Evaluate strategy**
- finter-portfolio → **Optimize portfolio**
