# Signal Diagnosis Framework

## The Diagnostic Mindset

**DON'T** apply techniques by habit.
**DO** diagnose the problem first, then choose the appropriate technique.

## Diagnostic Questions

### 1. IC Too Low (< 0.02)?

**Ask first:**
- Is the signal too noisy? → Smooth it
- Is the lookback period wrong? → Test different periods
- Is the signal delayed? → Check timing alignment
- Is the relationship non-linear? → Try rank transformation

**Common fixes:**
```python
# Smoothing (if noisy)
signal_smooth = signal.rolling(5).mean()

# Different lookback
for lookback in [5, 10, 20, 60]:
    sig = close.pct_change(lookback)
    ic = calculate_ic(sig, returns)
    print(f"Lookback {lookback}: IC = {ic.mean():.4f}")

# Rank transformation (if non-linear)
signal_rank = signal.rank(axis=1, pct=True)
```

### 2. IC Inconsistent (Win Rate < 55%)?

**Ask first:**
- Are there regime changes? → Split by market condition
- Is it sector-specific? → Check sector breakdown
- Is it time-varying? → Check rolling IC

**Diagnostic code:**
```python
# Rolling IC (check stability)
rolling_ic = ic.rolling(60).mean()
rolling_ic.plot(title='60-day Rolling IC')

# Market regime split
bull = returns.mean(axis=1) > 0
print(f"Bull market IC: {ic[bull].mean():.4f}")
print(f"Bear market IC: {ic[~bull].mean():.4f}")
```

### 3. Turnover Too High?

**Ask first:**
- Is the signal too noisy? → Smooth or decay
- Are you chasing micro-movements? → Increase lookback
- Is ranking unstable? → Use band-pass filter

**Diagnostic code:**
```python
# Check rank stability
ranks = signal.rank(axis=1, pct=True)
rank_changes = ranks.diff().abs().sum(axis=1)
print(f"Avg daily rank changes: {rank_changes.mean():.1f}")

# If high, try smoothing
signal_smooth = signal.ewm(halflife=5).mean()
ranks_smooth = signal_smooth.rank(axis=1, pct=True)
rank_changes_smooth = ranks_smooth.diff().abs().sum(axis=1)
print(f"After smoothing: {rank_changes_smooth.mean():.1f}")
```

### 4. Too Many Outliers?

**Ask first:**
- Are outliers informative or noise? → Analyze IC by quantile
- Is it data quality issue? → Check source
- Is winsorizing appropriate? → Test different thresholds

**Diagnostic code:**
```python
# IC by signal quantile
for q in [0.1, 0.25, 0.5, 0.75, 0.9]:
    mask = signal > signal.quantile(q, axis=1)
    ic_subset = calculate_ic(signal[mask], returns[mask])
    print(f"Q{q:.0%}: IC = {ic_subset.mean():.4f}")

# If outliers are noise, winsorize
signal_win = signal.clip(
    lower=signal.quantile(0.01, axis=1),
    upper=signal.quantile(0.99, axis=1),
    axis=0
)
```

## Decision Tree

```
Signal Created
      │
      ▼
  Calculate IC
      │
      ├─ IC < 0.02 ────────────► Diagnose: noise? lookback? timing?
      │                                    │
      │                                    ▼
      │                              Try fixes, recalculate
      │                                    │
      │                                    ├─ Still < 0.02 → STOP
      │                                    └─ > 0.02 → Continue
      │
      ├─ Win Rate < 55% ───────► Diagnose: regime? sector? time-varying?
      │                                    │
      │                                    ▼
      │                              Analyze breakdown
      │                                    │
      │                                    ├─ Can't fix → STOP
      │                                    └─ Can filter → Continue
      │
      └─ Pass ─────────────────► Check turnover
                                       │
                                       ├─ > 15,000% annual → Diagnose
                                       └─ < 15,000% annual → finter-alpha
```

## The Golden Rule

**Never implement alpha.py without completing this diagnosis.**

Time spent diagnosing = Time saved debugging bad backtests.
