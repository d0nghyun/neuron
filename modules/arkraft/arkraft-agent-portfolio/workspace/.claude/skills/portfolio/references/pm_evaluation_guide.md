# PM Evaluation Guide

Detailed guidance for evaluating alphas across the four perspectives.

## 1. Rationale Alignment (가설-포지션 일치)

**Question**: "가설이 말하는 것과 실제 포지션이 일치하는가?"

### How to Assess

1. Read the alpha document to understand the hypothesis
2. Review what the alpha actually does
3. Compare: Does the position implement the hypothesis?

### Examples

**Aligned**:
- Hypothesis: "High momentum stocks outperform"
- Position: Long stocks with highest 12-month returns
- Assessment: aligned

**Partial**:
- Hypothesis: "Momentum with quality filter"
- Position: Pure momentum, no quality filter
- Assessment: partial

**Misaligned**:
- Hypothesis: "Value stocks with low P/E"
- Position: Long high-momentum stocks
- Assessment: misaligned

---

## 2. Economic Sense (투자 논리)

**Question**: "이 투자 논리가 경제적으로 타당한가?"

### Ratings

**Strong**:
- Well-documented academic factor
- Clear behavioral/structural explanation
- Long history across markets

**Moderate**:
- Reasonable hypothesis with evidence
- May work in specific conditions
- Plausible but not proven

**Weak**:
- Thin rationale
- Relies on patterns without theory
- "It just works" reasoning

**Questionable**:
- No logical explanation
- Likely curve-fitting
- Too good to be true

---

## 3. Portfolio Fit (포트폴리오 적합성)

**Question**: "기존 선택한 알파들과 차별화된 가치가 있는가?"

### Roles

**Core**:
- Strong standalone performance
- Low correlation with others
- Significant weight justified

**Diversifier**:
- Moderate performance
- Low correlation - adds diversification
- Complements core strategies

**Hedge**:
- May have lower Sharpe
- Negative correlation with core
- Provides downside protection

**Redundant**:
- High correlation (>0.7) with existing
- BUT: Don't exclude! Use cluster weighting instead

### Correlation Thresholds

| Correlation | Assessment |
|-------------|------------|
| < 0.3 | Excellent diversification |
| 0.3 - 0.5 | Good diversification |
| 0.5 - 0.7 | Moderate overlap → same cluster |
| > 0.7 | High overlap → same cluster, lower weight |

---

## 4. Red Flags (경고 신호)

**Question**: "의심스러운 패턴이 있는가?"

### Real Red Flags (Exclude)

| Flag | Symptom | Severity |
|------|---------|----------|
| **Sharpe > 3.0** | Likely bug/overfit | Critical |
| **Perfect backtest** | No drawdowns | Critical |
| **Data snooping** | Complex params | High |
| **Look-ahead bias** | Uses future info | Critical |

### NOT Red Flags (Don't Exclude)

| NOT a Red Flag | Why | Action |
|----------------|-----|--------|
| High turnover | Position offsetting reduces cost | Include |
| High correlation | Cluster weighting handles it | Include |
| Similar strategy | Noise reduction value | Include |

---

## Decision Framework

### SELECT (Default)

- Rationale: aligned or partial
- Economic sense: strong or moderate
- No critical red flags
- Any portfolio fit (cluster weighting handles redundancy)

### EXCLUDE (Rare)

- Critical red flags ONLY:
  - Sharpe > 3.0 (likely bug)
  - Look-ahead bias
  - Completely broken

### REVIEW

- Mixed signals
- Edge cases
- Need human judgment
