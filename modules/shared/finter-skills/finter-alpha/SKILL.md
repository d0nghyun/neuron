---
name: finter-alpha
description: Quantitative trading alpha strategy development using the Finter Python library. Use when user requests to create, modify, or analyze alpha strategies (e.g., "create RSI strategy", "momentum alpha", "create momentum strategy", "combine value and momentum factors"). Supports the BaseAlpha framework with automated backtesting and result analysis.
---

# Finter Alpha Strategy Development

Develop quantitative trading alpha strategies using the Finter framework.

## ⚠️ CRITICAL: VERIFY BEFORE SAVING alpha.py

**EVERY alpha.py MUST have these 3 things. Check before saving:**

```python
# ✅ CHECK 1: Class name is exactly "Alpha"
class Alpha(BaseAlpha):  # ❌ NOT MyAlpha, MomentumAlpha, etc.

# ✅ CHECK 2: Return ends with .shift(1).fillna(0)
return positions.shift(1).fillna(0)  # ❌ NOT .shift(1) alone

# ✅ CHECK 3: pct_change has fill_method=None
close.pct_change(20, fill_method=None)  # ❌ NOT pct_change(20)
```

**Pre-save checklist:**
- [ ] `class Alpha(BaseAlpha)` - not any other name
- [ ] `return ....shift(1).fillna(0)` - both shift AND fillna
- [ ] All `pct_change()` calls have `fill_method=None`
- [ ] Position constraint:
  - Long-only: `row_sum <= 1e8`
  - Long-short: `abs_sum <= 1e8` (positive=Long, negative=Short)

## ⛔ NO SELF-FEEDBACK (CRITICAL)

**Single pass only.** Backtest → Report → DONE. Fund Manager decides next steps.

```
❌ FORBIDDEN: "Sharpe 0.8, let me try different parameters..." → Backtest again
✅ CORRECT: Explore → Implement → Backtest → Report → STOP
```

## 💰 TURNOVER CHECK (Before Backtest)

**Check signal stability BEFORE full backtest.**

```python
# Quick turnover check on your signal
daily_changes = (signal.diff() != 0).sum(axis=1).mean()
print(f"Avg daily changes: {daily_changes:.0f} stocks")
```

**If turnover seems high, DIAGNOSE first before applying any fix.**
→ Read `references/mental_models/signal_processing.md` for decision framework.

DON'T default to any specific technique. Ask:
1. Is the noise frequency >> signal frequency?
2. Are extreme values informative or noise?
3. Does the fix actually improve IC?

## 📋 Workflow

1. **Read Framework**: `references/framework.md` (REQUIRED)
2. **Read Mental Models**: `references/mental_models/signal_processing.md` (REQUIRED)
3. **Explore Data**: Load data in Jupyter, check distributions
4. **Diagnose Signal Quality**: Before implementing, ask the diagnostic questions
5. **Find Template**: Copy from `templates/examples/`
6. **Implement & Backtest**: Write Alpha class, run Simulator
7. **Save alpha.py**: Use Write tool (NOT Jupyter)
8. **Finalize**: Run ONE command to generate all outputs
9. **Report & STOP**: Report results, let Fund Manager evaluate

## 🎯 Templates

| Pattern | Template |
|---------|----------|
| Momentum/Technical | `templates/examples/technical_analysis.py` |
| Multi-factor | `templates/examples/multi_factor.py` |
| Stock Selection | `templates/examples/stock_selection.py` |
| Long-Short | `templates/examples/long_short.py` |
| Crypto (BETA) | `templates/examples/crypto_bitcoin.py` |

**Copy and modify templates - don't write from scratch!**

## ⚡ Quick Backtest

```python
from finter import BaseAlpha
from finter.backtest import Simulator

alpha = Alpha()
positions = alpha.get(20200101, 20241213)

sim = Simulator(market_type="kr_stock")
result = sim.run(position=positions)

print(f"Sharpe: {result.statistics['Sharpe Ratio']:.2f}")
print(f"Return: {result.statistics['Total Return (%)']:.1f}%")
print(f"MaxDD: {result.statistics['Max Drawdown (%)']:.1f}%")
```

## ⚠️ Simulator Result API (EXACT)

**Available attributes:**
```python
result.statistics   # pd.Series - Sharpe Ratio, Total Return (%), Max Drawdown (%), etc.
result.summary      # pd.DataFrame - nav, daily_return, cost, slippage, target_turnover, aum
```

**These do NOT exist (don't try):**
```python
result.plot()            # ❌ NO - use matplotlib with result.summary['nav']
result.cumulative_return # ❌ NO - use result.summary['nav']
result.daily_return      # ❌ NO - use result.summary['daily_return']
result.nav               # ❌ NO - use result.summary['nav']
result.performance()     # ❌ NO - use result.statistics
result.pnl               # ❌ NO - use result.summary['nav']
```

**Turnover & Cost calculation:**
```python
# Annual turnover (target_turnover is daily ratio, 1.0 = 100% of AUM)
annual_turnover = result.summary['target_turnover'].mean() * 252

# Cost drag as % of AUM
total_cost = result.summary['cost'].sum() + result.summary['slippage'].sum()
cost_drag_pct = (total_cost / result.summary['aum'].mean()) * 100
```

## 🚀 FINAL STEP (ONE COMMAND)

After saving alpha.py, run `finalize.py`:

```bash
python .claude/skills/finter-alpha/scripts/finalize.py \
    --code alpha.py \
    --universe kr_stock \
    --title "Strategy Name" \
    --category momentum
```

**What finalize.py does:**
1. **Validates** - class name, position format, path independence
2. **Backtests** - runs Simulator, calculates metrics
3. **Generates** - chart.png, info.json, CSV files

**Output files:**
- `backtest_summary.csv`, `backtest_stats.csv`
- `chart.png`
- `info.json`

If validation fails, fix alpha.py and re-run.

**Categories**: momentum | value | quality | growth | size | low_vol | technical | macro | stat_arb | event | ml | composite

**Universes**: kr_stock | us_stock | us_etf | vn_stock | id_stock | crypto_test

## 📚 Documentation

### MUST READ (Before Implementation)
| Doc | Purpose |
|-----|---------|
| `references/framework.md` | BaseAlpha rules, position format |
| `references/mental_models/signal_processing.md` | Signal quality diagnosis & techniques |

### Reference During Coding
| Doc | Purpose |
|-----|---------|
| `references/troubleshooting.md` | Common mistakes with ❌/✅ examples |
| `references/api_reference.md` | ContentFactory, Simulator API |
| `references/universe_reference.md` | Data items per universe |

## ⚡ Data Loading Reference

```python
from finter.data import ContentFactory
from helpers import get_start_date  # Included in templates

# Load with buffer (rule: 2x lookback + 250 days)
cf = ContentFactory("kr_stock", get_start_date(start, 300), end)

# Discover data items
print(cf.search('volume').to_string())
cf.usage('price_close')

# Load data
close = cf.get_df("price_close")
```

| Universe | Notes |
|----------|-------|
| kr_stock, us_stock | Full support, 1000+ items |
| us_etf | Market data only |
| vn_stock | **PascalCase**: `ClosePrice` |
| id_stock | Use `volume_sum` |
| crypto_test | 8H candles, BTC only |

See `finter-data` skill for detailed data loading guide.
