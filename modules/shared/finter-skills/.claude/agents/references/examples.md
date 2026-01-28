# Quant Analyst Examples

## Anti-Patterns (FORBIDDEN)

```
❌ "IC > 0.03이므로 통과" (applying fixed threshold without defining why)
❌ "신호가 좋아 보인다" (judgment without measurement)
❌ "표준적인 수준이므로 기준으로 삼음" (criterion without independent reasoning)
❌ "아마 다음 분기에도 작동할 것이다" (stability claim without analysis)
```

## Correct Pattern

```
Q2: Is the predictive power sufficient to cover transaction costs?

Criterion: I define "sufficient" as annual return > 2.5% after 20bps round-trip costs
Why: At 2.5% annual return with 50% Sharpe, marginal return justifies operational overhead

Measurement:
- Simulated returns with signal-based rebalancing: 3.2% annual
- Transaction costs (20bps round-trip, quarterly rebalance): 0.4% annual
- Net return: 2.8% annual

Judgment: YES
Reasoning: 2.8% net return > 2.5% threshold I defined. This covers costs with margin.

What could change my mind:
- If transaction costs rise above 30bps (threshold drops to 1.8%)
- If signal decay accelerates in out-of-sample period
- If market regime shifts reduce correlation stability
```
