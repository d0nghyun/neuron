# Agent Autonomy Guide

Decision guide for balancing quantitative guidance vs. agent judgment.

## Core Principle

**Think, Don't Threshold**

Numbers inform judgment, they don't replace it.

## The Hard Threshold Anti-Pattern

### What It Looks Like

```markdown
WRONG:
- IC < 0.03 → STOP
- Win Rate < 55% → REJECT
- Sharpe < 1.0 → FAIL

RIGHT:
- IC below expectation → Diagnose → Document reasoning → YOU decide
- Win Rate Context: Strategy type, universe, holding period matter
- Sharpe Reference: Citadel targets 2.0+, but context-dependent
```

### Why It's Harmful

Hard thresholds kill creativity and judgment:

1. **Context Blindness**: Same number means different things
   - IC 0.02 in high-frequency vs. monthly rebalance
   - Win rate 52% in pairs trading vs. momentum
   - Sharpe 1.5 in crypto vs. equities

2. **False Security**: Agents follow rules without thinking
   - "IC is 0.035, we're good" (no diagnosis of WHY)
   - "Win rate is 54.9%, failed" (ignores context)

3. **Lost Insights**: Diagnostic thinking stops
   - No investigation into signal quality
   - No understanding of strategy mechanics
   - No learning from edge cases

## When to Use Each Approach

### Use Reference Points When

```
Q1. Does the number need context to interpret?
    YES → Reference point (e.g., "Citadel targets IC > 0.03, but...")
    NO  → Q2

Q2. Does interpretation require domain knowledge?
    YES → Reference point
    NO  → Q3

Q3. Are there legitimate exceptions?
    YES → Reference point
    NO  → Hard boundary OK (e.g., "P-value must be < 0.05")
```

### Examples

| Metric | Approach | Reason |
|--------|----------|--------|
| IC | Reference | Context-dependent (strategy, universe, frequency) |
| Win Rate | Reference | Depends on strategy mechanics |
| Sharpe | Reference | Market regime and strategy type matter |
| P-value | Hard | Statistical significance is binary |
| Position limit | Hard | Risk management rule |

## Implementation Patterns

### Pattern 1: Quality Assessment (Reference Only)

```markdown
## Quality Assessment (Reference Only)

**Citadel-grade benchmarks**:
- IC: 0.03-0.05 (monthly rebalance, large cap US)
- Win Rate: 55-60% (depends on strategy mechanics)
- Sharpe: 2.0+ (pre-cost, annual)

**Your job**: Diagnose signal quality, understand context, document reasoning.

Numbers below reference? → Investigate WHY → Make judgment call.
```

### Pattern 2: Verdict Guidance (Not Rules)

```markdown
## Verdict Guidance (Reference Framework)

**STRONG_BUY considerations**:
- IC consistently above 0.04
- Win rate > 58% with clear edge
- Robust across regimes

**But YOU make final call**:
- Is the signal novel?
- Does backtest methodology match reality?
- What does diagnosis tell you?
```

### Pattern 3: Diagnostic-First Decision Tree

```markdown
## Signal Diagnosis Flow

1. Compute IC/win-rate/Sharpe
2. Below Citadel reference? → Investigate:
   - Data quality issues?
   - Signal construction problems?
   - Strategy mechanics explanation?
3. Document findings
4. **YOU decide**: Proceed or stop?

Context matters. Trust your judgment.
```

## Migration Checklist

When updating existing docs:

- [ ] Replace "MUST" with "Consider" for quality metrics
- [ ] Change "Rules" to "Guidance" or "Reference Framework"
- [ ] Add "YOU make the final call" language
- [ ] Remove hard boundaries like "IC < X → STOP"
- [ ] Add context considerations
- [ ] Emphasize diagnostic thinking over threshold checking

## Quick Reference

| Signal | Old (Hard) | New (Think) |
|--------|-----------|-------------|
| Low IC | "STOP" | "Diagnose WHY → Document → Decide" |
| Low Win Rate | "REJECT" | "Understand mechanics → Context → Decide" |
| Low Sharpe | "FAIL" | "Check assumptions → Compare regime → Decide" |

## Related

- Mental Models: `modules/shared/finter-skills/finter-explore/references/mental_models/`
- Signal Diagnosis: `signal_diagnosis.md`
- Alpha Strategy Validation: `ref-alpha-strategy-validation.md`
