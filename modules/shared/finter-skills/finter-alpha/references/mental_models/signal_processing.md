# Signal Processing Mental Models for Quant Research

> **Purpose:** This document teaches *how to think* about signal processing, not *what to do*.
> Read this when your signal has quality issues. The right technique depends on your answers to the diagnostic questions.

---

## The Signal Quality Framework

Every trading signal has four dimensions of quality:

```
                    HIGH
                      │
         ┌───────────┼───────────┐
         │           │           │
    NOISY│    ❌     │    ⚠️     │CLEAN
         │  (worst)  │  (fixable)│
         │           │           │
         ├───────────┼───────────┤
         │           │           │
         │    ⚠️     │    ✅     │
         │ (fixable) │   (best)  │
         │           │           │
         └───────────┴───────────┘
                    LOW
              ← LATENCY →

Also consider:
- Distribution shape (normal? fat-tailed? bounded?)
- Stationarity (stable over time? regime-dependent?)
```

**Before applying any technique, diagnose which quadrant you're in.**

---

## Problem 1: Noisy Signals

### Diagnostic Questions

1. **Is the noise random or structured?**
   - Random: Different each day, no pattern
   - Structured: Correlated with market events, time-of-day, etc.

2. **What's the frequency of noise vs signal?**
   - If noise is daily but signal is weekly → filtering can help
   - If noise and signal have same frequency → filtering destroys signal too

3. **Is the noise symmetric or directional?**
   - Symmetric: Equally likely up or down
   - Directional: Biased (e.g., always overestimates on earnings days)

### Mental Model: Smoothing Decision Tree

```
Is noise frequency >> signal frequency?
│
├── YES → Smoothing can help
│         │
│         ├── Is signal regime-dependent?
│         │   │
│         │   ├── YES → Adaptive smoothing (respond to regime changes)
│         │   └── NO  → Simple smoothing (rolling mean/median)
│         │
│         └── Does smoothing kill the edge?
│             → Test: Compare IC of raw vs smoothed at target horizon
│             → If smoothed IC drops significantly, DON'T smooth
│
└── NO → Smoothing will destroy signal
         │
         └── Consider instead:
             • Better data source
             • Signal combination (ensemble)
             • Accept noise, size positions smaller
```

### Smoothing Techniques (When Appropriate)

| Technique | When to Use | Tradeoff |
|-----------|-------------|----------|
| Rolling Mean | Noise is symmetric, no regime changes | Adds lag, dampens fast signals |
| Rolling Median | Noise has outliers | Even more lag than mean |
| Exponential Weighted | Recent data more important | Harder to tune, still adds lag |
| Adaptive Window | Regime changes matter | Complex, can overfit |

### Key Insight: The Smoothing Paradox

**More smoothing ≠ better signal.**

Smoothing reduces noise but also:
- Adds lag (you're always behind)
- Dampens true signal (extreme values might be informative!)
- Creates path-dependency issues

**The test:** Does smoothed IC at horizon H beat raw IC at horizon H?
If not, the smoothing is hurting you.

---

## Problem 2: Extreme Values / Fat Tails

### Diagnostic Questions

1. **Are extreme values informative or noise?**
   - Informative: Extreme momentum predicts extreme returns
   - Noise: Extreme values are data errors or one-time events

2. **Is the relationship with returns linear or non-linear?**
   - Linear: 2x signal → 2x expected return
   - Non-linear: Diminishing returns, or threshold effects

3. **How often do extremes occur?**
   - Rare: Might be fitting to outliers
   - Common: Might be real regime indicator

### Mental Model: Transformation Decision Tree

```
Are extreme values informative?
│
├── YES → Keep them, but consider:
│         │
│         ├── Is relationship linear?
│         │   │
│         │   ├── YES → Use raw values
│         │   └── NO  → Use rank or appropriate non-linear transform
│         │
│         └── Do extremes dominate portfolio?
│             │
│             ├── YES → Consider concentration limits
│             └── NO  → Raw values are fine
│
└── NO → Compress extremes
         │
         ├── How aggressive?
         │   │
         │   ├── Mild: Winsorization (clip at percentile)
         │   ├── Moderate: Rank transformation (uniform distribution)
         │   └── Aggressive: Sigmoid-like (compress to bounded range)
         │
         └── Does compression kill the edge?
             → Test: Compare IC before/after transformation
```

### Transformation Techniques (When Appropriate)

| Technique | Effect | When to Use |
|-----------|--------|-------------|
| Winsorization | Clips extremes at percentile | Extremes are noise, keep relative ordering |
| Rank Transform | Uniform distribution | Care only about ordering, not magnitude |
| Z-score | Standard normal | Need comparability across assets/time |
| Sigmoid/Tanh | Bounded, smooth compression | Diminishing returns to extreme values |
| Log Transform | Compress large, expand small | Multiplicative relationships (returns, ratios) |

### Key Insight: Information Content

**Every transformation destroys information.**

- Winsorization: Loses info about "how extreme"
- Rank: Loses all magnitude information
- Z-score: Loses non-Gaussian structure

**The question:** Is the destroyed information noise or signal?

---

## Problem 3: Signal Lag / Staleness

### Diagnostic Questions

1. **How old is the signal by the time you can trade?**
   - Real-time: Minutes to hours
   - End-of-day: 1 day lag
   - Fundamental: Days to weeks (filing delays)

2. **How fast does the alpha decay?**
   - Event-driven: Hours to days
   - Technical: Days to weeks
   - Fundamental: Weeks to months

3. **Is the lag predictable or variable?**
   - Predictable: Always T+1
   - Variable: Depends on data source, market conditions

### Mental Model: Lag-Adjusted Expectations

```
Signal Freshness vs Alpha Decay:

Signal Age    Alpha Remaining
─────────────────────────────
  0 (fresh)   ████████████ 100%
  1 day       ████████     ~80%
  1 week      █████        ~50%
  1 month     ██           ~20%

Question: By the time you trade, how much alpha is left?

If signal lag >= alpha half-life → signal is worthless
```

### Lag Mitigation Techniques (When Appropriate)

| Technique | When to Use | Tradeoff |
|-----------|-------------|----------|
| Prediction/Nowcasting | Lag is predictable, signal has momentum | Can be wrong, adds model risk |
| Lead-lag relationships | Other assets/signals predict your signal | Adds complexity, may not be stable |
| Accept lag, lower frequency | Lag is fundamental to data source | Less trading opportunity |
| Better data source | Lag is artificial (processing delay) | May cost more |

### Key Insight: Lag is Fundamental

You cannot "fix" lag with clever processing. If:
- Signal is based on quarterly earnings
- Earnings are reported 30 days after quarter end
- Your signal has minimum 30-day lag

**No amount of Kalman filtering will give you "real-time" quarterly earnings.**

---

## Problem 4: Non-Stationarity / Regime Changes

### Diagnostic Questions

1. **Does signal strength vary over time?**
   - Stable: Consistent IC across years
   - Varying: IC is 0.05 in 2015-2018, 0.01 in 2019-2022

2. **Are there identifiable regimes?**
   - Yes: Bull/bear, high/low volatility, risk-on/risk-off
   - No: Random variation

3. **Can you predict regime changes?**
   - Yes: Some leading indicators
   - No: Only know in hindsight

### Mental Model: Regime-Aware Research

```
Is signal strength regime-dependent?
│
├── YES →
│   │
│   ├── Can you predict regimes?
│   │   │
│   │   ├── YES → Regime-switching model (trade only in favorable regimes)
│   │   └── NO  →
│   │            │
│   │            ├── Diversify: Combine signals that work in different regimes
│   │            └── Accept: Size positions based on average performance
│   │
│   └── Is regime-dependence a bug or feature?
│       │
│       ├── Bug: Signal should work always → investigate why it doesn't
│       └── Feature: Exploit regime timing → but be honest about in-sample fit
│
└── NO → Simpler is better, no regime logic needed
```

### Regime-Related Techniques (When Appropriate)

| Technique | When to Use | Tradeoff |
|-----------|-------------|----------|
| Regime Detection (HMM, etc.) | Distinct regimes exist and matter | Prone to overfitting, hindsight bias |
| Adaptive Parameters | Gradual changes over time | Model complexity, parameter instability |
| Ensemble/Diversification | Can't predict which signal will work | Dilutes best signal in good times |
| Fixed Model | Signal is actually stable | May miss regime changes |

### Key Insight: Regime Fitting Trap

**It's easy to fit regimes in-sample. It's hard to predict them out-of-sample.**

Before adding regime logic, ask:
- Could I have identified this regime in real-time?
- Am I just labeling good/bad periods after seeing returns?

---

## Problem 5: Signal Combination

### Diagnostic Questions

1. **Are signals correlated with each other?**
   - High correlation: Combining adds little
   - Low correlation: Combining is valuable

2. **Do signals work in the same or different conditions?**
   - Same: Redundant
   - Different: Complementary

3. **What's the goal of combining?**
   - Noise reduction: Average out individual errors
   - Coverage: Work in more conditions
   - Enhancement: 1+1 > 2 interaction effects

### Mental Model: Combination Logic

```
Why are you combining signals?
│
├── Noise Reduction →
│   │
│   └── Signals must be:
│       • Targeting same phenomenon
│       • Independently noisy (errors uncorrelated)
│       • Similar in scale and timing
│
│   Technique: Simple average, weighted by IC
│
├── Coverage →
│   │
│   └── Signals must be:
│       • Targeting different conditions
│       • Not conflicting (one says buy, other says sell)
│       • Regime-aware or adaptive
│
│   Technique: Conditional combination, regime switching
│
└── Enhancement →
    │
    └── Signals must be:
        • Interaction effect is real (not data-mined)
        • Economically justifiable

    Technique: Non-linear combination, but BEWARE of overfitting
```

### Combination Techniques (When Appropriate)

| Technique | When to Use | Tradeoff |
|-----------|-------------|----------|
| Equal Weight | No prior on which is better | Ignores signal quality differences |
| IC-Weighted | Historical IC is predictive | Chases past performance |
| Orthogonalization | Remove overlap before combining | Can create unstable residuals |
| Stacking/ML | Complex interactions exist | Black box, overfitting risk |

### Key Insight: Combination is Not Always Better

**Two weak signals don't make a strong signal.**

If both signals have IC = 0.01 and correlation = 0.8:
- Combined IC ≈ 0.01 (barely better)
- But you've doubled complexity

Only combine when: `IC_combined >> max(IC_1, IC_2)`

---

## How to Use This Document

### In Alpha Research (Phase 2a/3)

1. **Diagnose first:** What's the problem with the raw signal?
2. **Ask the questions:** Go through the diagnostic tree
3. **Choose technique based on answers:** Not based on habit
4. **Validate:** Does the technique actually improve IC/Sharpe?

### In Manager Review (Phase 2c/4)

1. **Check reasoning:** Did Alpha justify technique choice?
2. **Question defaults:** "Why rolling mean and not rank transform?"
3. **Verify improvement:** Before/after comparison of signal quality

### Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| "Always use rolling mean" | Ignores signal characteristics |
| "Smooth everything" | Destroys fast signals |
| "Rank transform everything" | Loses valuable magnitude info |
| "More processing = better" | Overfitting risk, complexity |
| "Copy technique from last project" | Different problem may need different solution |

---

## Problem 6: High Turnover / Edge Efficiency

### Diagnostic Questions

1. **How much does the signal change day-to-day?**
   - Stable: Position changes < 5% of portfolio daily
   - Volatile: Position changes > 20% of portfolio daily

2. **Is the turnover inherent to the strategy or fixable?**
   - Inherent: Short-horizon mean reversion, event-driven
   - Fixable: Noisy signal that could be smoothed

3. **What's the expected return per unit of turnover?**
   - High efficiency: Strong edge justifies frequent trading
   - Low efficiency: Edge doesn't survive trading costs

### Mental Model: Edge Efficiency Lens

```
Is turnover a concern for this signal?
│
├── LOW turnover (< 200% annual) → Probably fine, proceed
│
└── HIGH turnover (> 300% annual) →
    │
    ├── Is this inherent to the strategy?
    │   │
    │   ├── YES (e.g., short-term reversal) →
    │   │       Does edge justify the activity?
    │   │       • Return per 100% turnover > cost per 100% turnover?
    │   │       • If YES → proceed, this is the nature of the strategy
    │   │       • If NO → strategy may not be viable
    │   │
    │   └── NO (noisy signal) →
    │           Can smoothing reduce turnover without killing edge?
    │           → See Problem 1: Noisy Signals
    │
    └── Quick check (optional):
        Return per Turnover = Expected Annual Return / (Annual Turnover / 100)

        Example: 15% return, 500% turnover → 3% per 100% TO
        If Finter cost ~0.3% per 100% TO → net 2.7% per 100% TO → viable
```

### When This Lens is Useful

| Situation | Useful? |
|-----------|---------|
| High-frequency signal (daily changes) | ✅ Yes |
| Comparing two approaches with different turnover | ✅ Yes |
| Low-frequency strategy (monthly rebalancing) | ❌ Not really |
| Turnover is core to the edge (stat arb, etc.) | ⚠️ Partially |

### When This Lens is NOT Useful

- **Already committed to a frequency:** If the hypothesis requires daily rebalancing, checking "return per turnover" won't change that
- **Turnover IS the edge:** Some strategies profit from providing liquidity; low turnover would eliminate the edge
- **Comparing across different universes:** Cost structures vary (US vs KR vs crypto)

### Key Insight: Turnover is Not Inherently Bad

**High turnover with strong edge > Low turnover with weak edge.**

The question isn't "is turnover high?" but "is the edge worth the activity?"

A 1000% turnover strategy with 30% annual return (3% per 100% TO)
may be better than a 100% turnover strategy with 5% return (5% per 100% TO)
— depends on your cost structure and capacity constraints.

**Don't reject high-turnover strategies automatically. Evaluate efficiency.**

---

## Summary: The Meta-Mental-Model

**Before applying any signal processing:**

1. **What problem am I solving?** (noise, extremes, lag, regimes, combination)
2. **What are the characteristics of my signal?** (frequency, distribution, stationarity)
3. **What tradeoff does this technique make?** (lag vs noise, information loss, complexity)
4. **How will I know if it worked?** (IC comparison, out-of-sample test)

**The technique should follow from the diagnosis, not precede it.**
