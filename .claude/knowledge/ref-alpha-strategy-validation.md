# Alpha Strategy Validation

Reference for validating alpha hypothesis before backtest.

## Phase Sequence

| Phase | Tool | Purpose | Kill Criteria |
|-------|------|---------|---------------|
| 1. IC Analysis | finter-explore | Predictive power | IC near zero or wrong sign |
| 2. Turnover Check | (manual) | Transaction cost feasibility | Annual turnover > 1000% |
| 3. Backtest | finter-alpha | Full simulation | Risk-adjusted return, drawdown |

## Critical Learning

**Good IC ≠ Profitable Strategy**

Example from 2026-01-28 session:
- Hypothesis: 52-week high breakout
- IC: 0.039 (1d), 0.082 (20d) - excellent predictive power
- Backtest: -96.3% return due to 16,553% annual turnover
- Issue: Daily rebalancing + frequent signals = transaction costs destroy alpha

## Turnover Estimation

Before running backtest, estimate turnover:

```python
# Rough heuristic
signal_frequency = len(universe) * signal_trigger_rate * rebalance_frequency
annual_turnover = signal_frequency * avg_position_size

# Example:
# 100 stocks * 10% trigger rate * 252 trading days = 2,520 trades/year
# If each trade is 1% of portfolio: 25.2x turnover (2,520%)
```

**Guidelines:**
- < 100% turnover: Acceptable for most strategies
- 100-500%: High, but feasible with low-cost execution
- > 500%: Very high, transaction costs likely dominant
- > 1000%: Almost certainly unprofitable after costs

## Mitigation Strategies

If IC is good but turnover is too high:

1. **Reduce rebalancing frequency**: Daily → Weekly → Monthly
2. **Add signal persistence**: Require N consecutive days
3. **Increase signal threshold**: Top 5% → Top 1%
4. **Portfolio constraints**: Max X% new positions per rebalance

## Reference

Session: 2026-01-28, arkraft-agent-alpha testing
Cost: $2.43, 51 turns
Hypothesis tested: 52-week high breakout momentum
