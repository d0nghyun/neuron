# Data Quality Mental Models

> **Purpose:** This document teaches *how to think* about data quality issues, not *what to do*.
> The right technique depends on your diagnosis. Don't default to any specific fix.

---

## The Data Quality Framework

Every dataset has four dimensions of quality:

```
                  COMPLETE
                      │
         ┌───────────┼───────────┐
         │           │           │
  BIASED │    ❌     │    ⚠️     │ UNBIASED
         │  (worst)  │  (fixable)│
         │           │           │
         ├───────────┼───────────┤
         │           │           │
         │    ⚠️     │    ✅     │
         │ (fixable) │   (best)  │
         │           │           │
         └───────────┴───────────┘
                 INCOMPLETE

Also consider:
- Freshness (how old is the data?)
- Accuracy (are values correct?)
- Consistency (same definition over time?)
```

**Before applying any fix, diagnose which quadrant you're in.**

---

## Problem 1: Missing Values (NaN)

### Diagnostic Questions

1. **Why is the data missing?**
   - Random: Technical glitch, truly missing
   - Structural: Company didn't exist, delisted, IPO
   - Informational: No trading (zero volume), suspended

2. **Is missingness informative?**
   - Yes: Delisting often precedes bankruptcy → informational
   - No: Random API failures → not informational

3. **What's the pattern?**
   - Sporadic: Random holes in the data
   - Systematic: All values missing before certain date
   - Edge: Missing at start/end only

### Mental Model: Missing Value Decision Tree

```
Why is the value missing?
│
├── STRUCTURAL (company didn't exist)
│   │
│   └── Leave as NaN or exclude from universe
│       → Filling creates fake data
│       → "Company had zero revenue before IPO" is WRONG
│
├── INFORMATIONAL (no trading, suspended)
│   │
│   └── Consider what NaN means:
│       • No trading volume → might indicate illiquidity
│       • Suspension → might precede news
│       → Don't blindly fill; the absence IS information
│
└── RANDOM (technical, sporadic)
    │
    ├── Is the gap short (1-3 days)?
    │   └── Forward fill is usually safe
    │
    ├── Is the gap long (weeks)?
    │   └── Consider:
    │       • Interpolation (if smooth series)
    │       • Leave as NaN (if discontinuous)
    │       • Exclude asset from analysis
    │
    └── Is it at the edge (start/end)?
        └── Backward fill for start, leave end as NaN
```

### Filling Techniques (When Appropriate)

| Technique | When to Use | Danger |
|-----------|-------------|--------|
| Forward Fill (ffill) | Short random gaps in time series | Creates stale data, hides real gaps |
| Backward Fill (bfill) | Edge cases at start only | Can introduce look-ahead bias |
| Interpolation | Smooth continuous series | Assumes linear relationship |
| Mean/Median Fill | Cross-sectional random gaps | Destroys variation, biases toward average |
| Leave as NaN | Informational missingness | Some operations will fail |

### Key Insight: NaN Can Be Information

**Not all missing values should be filled.**

- Delisted stocks have NaN prices → filling them is creating fake data
- Zero volume days might indicate illiquidity → that's real information
- Suspended trading might precede news → filling hides this signal

**Ask:** "If I fill this NaN, am I creating information that doesn't exist?"

---

## Problem 2: Outliers and Extreme Values

### Diagnostic Questions

1. **Is the extreme value real or an error?**
   - Real: Stock went up 500% on acquisition news
   - Error: Data entry mistake, wrong decimal point

2. **Is the extreme value informative or noise?**
   - Informative: Extreme momentum predicts extreme returns
   - Noise: One-time corporate action distorting the series

3. **What's causing the extreme?**
   - Market event: Earnings, M&A, news
   - Corporate action: Split, dividend, spinoff
   - Data error: Wrong decimal, currency mismatch

### Mental Model: Outlier Decision Tree

```
Is this extreme value real?
│
├── NO (data error)
│   │
│   └── Fix at source if possible
│       Otherwise exclude the data point
│       → Don't just clip; you're hiding errors
│
└── YES (real market event)
    │
    ├── Is it from a corporate action?
    │   │
    │   ├── YES → Use adjusted data if available
    │   │         Or exclude the transition period
    │   │
    │   └── NO → Real market move
    │
    └── Is the extreme informative?
        │
        ├── YES (extreme momentum → extreme returns)
        │   │
        │   └── Keep the value
        │       Consider: Does your model handle extremes well?
        │
        └── NO (one-time event, not predictive)
            │
            └── Options:
                • Winsorize (clip to percentile)
                • Rank transform (remove magnitude)
                • Exclude the period
```

### Outlier Handling Techniques (When Appropriate)

| Technique | When to Use | Danger |
|-----------|-------------|--------|
| Winsorization | Real but non-informative extremes | Loses information about "how extreme" |
| Rank Transform | Care only about ordering | Loses all magnitude information |
| Exclusion | Data errors, corporate actions | Reduces sample size |
| Keep As-Is | Extremes are informative | Model may be unstable |

### Key Insight: Understand Before Clipping

**Don't winsorize by default.**

Before clipping any value, ask:
1. Is this a data error? → Fix at source
2. Is this a corporate action? → Use adjusted data
3. Is this informative? → Maybe keep it

**Winsorization is not data cleaning; it's information destruction.**

---

## Problem 3: Survivorship Bias

### Diagnostic Questions

1. **Does your dataset include dead companies?**
   - Yes: Good, but check for delisting bias
   - No: Serious survivorship bias

2. **When were companies added to the dataset?**
   - Point-in-time: Companies appear when they actually existed
   - Backfilled: Current constituents applied to past

3. **How are delistings handled?**
   - Included until delisting: Correct
   - Excluded entirely: Biased
   - Returns truncated at delisting: Partially correct

### Mental Model: Survivorship Bias Check

```
Ask these questions about your data:
│
├── 1. "Does my backtest include companies that later failed?"
│   │
│   ├── YES → Good, but verify:
│   │         • Are delisting returns included?
│   │         • Is delisting coded correctly (not as NaN)?
│   │
│   └── NO → Survivorship bias!
│           Your backtest will be too optimistic
│
├── 2. "Am I using today's index constituents for historical analysis?"
│   │
│   ├── YES → Look-ahead bias!
│   │         Example: Testing "S&P 500 momentum" using current S&P 500 list
│   │         → Companies are IN the index because they did well
│   │
│   └── NO → Good, but verify point-in-time accuracy
│
└── 3. "Do I have data before a company existed?"
    │
    ├── YES → Data error or IPO handling issue
    │         → Cannot have prices before IPO
    │
    └── NO → Good
```

### Key Insight: The Winner's Curse

**Survivorship bias makes everything look good.**

If your dataset only includes companies that survived to today:
- Failed companies (the worst performers) are excluded
- You're testing on winners only
- Backtest Sharpe will be inflated

**The fix is in the data source, not in post-processing.**

---

## Problem 4: Look-Ahead Bias

### Diagnostic Questions

1. **When was this data point actually available?**
   - Real-time: Available at market close
   - Delayed: Published days/weeks later
   - Restated: Original value was different

2. **Am I using future information?**
   - Direct: Using tomorrow's price in today's signal
   - Indirect: Using revised data that wasn't available

3. **Is my data point-in-time correct?**
   - Yes: Using data as it was known at the time
   - No: Using revised/final values

### Mental Model: Point-in-Time Check

```
For each data item, ask:
│
├── "When was this number ACTUALLY AVAILABLE to traders?"
│   │
│   ├── Market data (prices, volume)
│   │   └── Usually available at market close (T+0)
│   │
│   ├── Financial statements
│   │   └── Available at filing date, NOT quarter end
│   │       Q1 ends Mar 31, but filed ~May 15
│   │       → 6-week lag is common
│   │
│   ├── Analyst estimates
│   │   └── Available when published, but may be revised
│   │
│   └── Economic data
│       └── Initial release vs. revised
│       → GDP revised multiple times
│
└── "Am I using the ORIGINAL value or a REVISED value?"
    │
    ├── Using original (point-in-time) → Correct
    │
    └── Using revised → Look-ahead bias!
        Most fundamental data gets revised
```

### Common Look-Ahead Traps

| Data Type | Trap | Reality |
|-----------|------|---------|
| Quarterly Earnings | Using Q1 data starting Apr 1 | Filed in May, use after filing date |
| Index Constituents | Using current S&P 500 list historically | Companies added after good performance |
| Adjusted Prices | Using today's adjustment factors | Splits/dividends weren't known before |
| Analyst Estimates | Using consensus as of report date | Estimates updated throughout quarter |

### Key Insight: If It Seems Too Good, Check for Look-Ahead

**Strategies with Sharpe > 2.0 often have look-ahead bias.**

Common patterns:
- Fundamental data used before filing date
- Index reconstitution anticipated perfectly
- Perfect timing around corporate actions

**Ask:** "Could I have actually known this at the time?"

---

## Problem 5: Data Consistency

### Diagnostic Questions

1. **Has the definition changed over time?**
   - Accounting standards: GAAP vs IFRS changes
   - Index methodology: Reconstitution rules change
   - Data vendor: Coverage expansion, calculation changes

2. **Are there structural breaks?**
   - Market structure: Decimalization, circuit breakers
   - Regulatory: New disclosure requirements
   - Coverage: Data vendor started covering mid-series

3. **Is the data comparable across assets?**
   - Same definition: All companies use same accounting
   - Same timing: All data points same frequency
   - Same currency: Or properly converted

### Mental Model: Consistency Check

```
Before using historical data, ask:
│
├── "Has the definition of this data item changed?"
│   │
│   ├── Accounting standards
│   │   └── IFRS adoption dates vary by country
│   │       Pre/post comparisons may be invalid
│   │
│   ├── Vendor methodology
│   │   └── "Adjusted close" calculation may have changed
│   │       Historical values might be recalculated
│   │
│   └── Market structure
│       └── Trading hours, tick sizes, circuit breakers
│           Pre-2001 US stocks traded in fractions
│
├── "Is there a structural break in my series?"
│   │
│   └── Check for:
│       • Sudden changes in mean or variance
│       • Coverage jumps (new countries/assets added)
│       • Definition changes (new accounting rule)
│
└── "Can I compare this across assets?"
    │
    └── Watch for:
        • Different fiscal year ends
        • Different currencies
        • Different accounting standards
```

### Key Insight: Data That Looks Continuous May Not Be

**Long time series often hide regime changes.**

Examples:
- "30 years of S&P 500 data" spans multiple index methodologies
- "Global equity data" mixes different accounting standards
- "US stock prices" includes pre/post decimalization

**Don't assume stationarity. Test for structural breaks.**

---

## How to Use This Document

### In Data Loading (finter-data)

1. **Before loading:** What quality issues might this data have?
2. **After loading:** Run diagnostic checks (NaN ratio, outlier count, date range)
3. **Before using:** Did I handle issues appropriately for my use case?

### In Alpha Research (finter-alpha)

1. **Check data quality** before building signals
2. **Document assumptions** about how you handled issues
3. **Validate** that your fixes don't introduce new biases

### Diagnostic Code Patterns

```python
# NaN diagnosis
print(f"NaN ratio: {df.isna().sum().sum() / df.size:.2%}")
print(f"Rows with any NaN: {df.isna().any(axis=1).sum()}")
print(f"Columns with >50% NaN: {(df.isna().mean() > 0.5).sum()}")

# Outlier diagnosis
print(f"Values > 3 std: {(df > df.mean() + 3*df.std()).sum().sum()}")
print(f"Min: {df.min().min()}, Max: {df.max().max()}")

# Coverage diagnosis
print(f"Date range: {df.index.min()} to {df.index.max()}")
print(f"Assets at start: {df.iloc[0].notna().sum()}")
print(f"Assets at end: {df.iloc[-1].notna().sum()}")

# Structural break detection (simple)
mid = len(df) // 2
print(f"Mean (first half): {df.iloc[:mid].mean().mean():.4f}")
print(f"Mean (second half): {df.iloc[mid:].mean().mean():.4f}")
```

### Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| "Always ffill then bfill" | Hides structural missingness, creates fake data |
| "Winsorize at 1%/99%" | Arbitrary threshold, might be destroying signal |
| "Drop rows with any NaN" | Loses too much data, introduces selection bias |
| "Interpolate everything" | Assumes linear relationships that may not exist |
| "Use the latest data version" | May have look-ahead bias from revisions |

---

## Summary: The Meta-Mental-Model

**Before handling any data quality issue:**

1. **Why does this issue exist?** (structural, informational, random)
2. **Is this issue informative?** (missingness/extremes might be signals)
3. **What bias does my fix introduce?** (every fix has tradeoffs)
4. **How will I validate my fix worked?** (before/after comparison)

**The technique should follow from the diagnosis, not precede it.**
