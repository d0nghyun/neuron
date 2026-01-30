---
name: portfolio
description: Build and optimize portfolios from alpha pool. Use when constructing
  multi-alpha portfolios, calculating weights, or analyzing risk.
---

# Portfolio Construction Skill

Build portfolios from alpha pool with PM-level evaluation.

## MENTAL MODEL

```
"나는 이성적인 Portfolio Manager다.
 각 알파를 투자 관점에서 평가하고,
 포트폴리오 전체의 조화를 고려하여 선택한다."
```

## Workflow

```
FETCH → ANALYZE → EVALUATE → WEIGHT → SAVE
```

### Phase 1: FETCH

Get alphas from alpha-pool MCP:

```python
# Search deployed alphas
result = mcp__alpha_pool__search_alphas(
    query="*",
    universe="us_stock",
    verdict="DEPLOYED",
    limit=50
)

# Save context
import json
with open("phase1/context.json", "w") as f:
    json.dump(result, f, indent=2)
```

### Phase 2: ANALYZE

Quantitative analysis (delegate to quant-analyst):

1. **Correlation Matrix**
   - Pairwise alpha correlations
   - Identify clusters (corr > 0.5)

2. **Turnover Analysis**
   - Individual alpha turnovers
   - Combined portfolio turnover
   - **Turnover reduction ratio** (key metric!)

```bash
# Run analysis
python .claude/skills/portfolio/scripts/analyze_alphas.py \
    --input phase1/context.json \
    --output phase2/
```

### Phase 3: EVALUATE

PM evaluation using 4 perspectives:

| Perspective | Question | Options |
|-------------|----------|---------|
| Rationale Alignment | 가설 = 포지션? | aligned / partial / misaligned |
| Economic Sense | 논리적으로 타당? | strong / moderate / weak / questionable |
| Portfolio Fit | 차별화 가치? | core / diversifier / hedge / redundant |
| Red Flags | 의심 패턴? | list of flags |

**Final recommendation**: select / exclude / review

See `references/pm_evaluation_guide.md` for details.

### Phase 4: WEIGHT

**Cluster-based Equal Weight** (default):

```python
from scipy.cluster.hierarchy import linkage, fcluster

# 1. Cluster by correlation
corr_matrix = pd.read_json("phase2/correlation.json")
linkage_matrix = linkage(1 - corr_matrix, method='average')
clusters = fcluster(linkage_matrix, t=0.5, criterion='distance')

# 2. Equal weight per CLUSTER
n_clusters = len(set(clusters))
cluster_weight = 1.0 / n_clusters

# 3. Equal weight within cluster
weights = {}
for alpha_id, cluster_id in zip(alpha_ids, clusters):
    cluster_size = sum(1 for c in clusters if c == cluster_id)
    weights[alpha_id] = cluster_weight / cluster_size
```

**Why cluster weighting?**
- High-corr alphas share cluster → lower individual weight
- Preserves all alpha information (no exclusion)
- Factor diversity ensured

### Phase 5: SAVE

Save to `output/portfolio.json`:

```json
{
  "metadata": {
    "universe": "us_stock",
    "created_at": "2026-01-29T00:00:00Z",
    "total_alphas": 10,
    "weight_method": "cluster_equal"
  },
  "alphas": [
    {
      "alpha_id": "string",
      "title": "Alpha title",
      "weight": 0.15,
      "cluster": 1,
      "sharpe_ratio": 1.5,
      "rationale": "Core momentum - strong economic basis"
    }
  ],
  "portfolio_metrics": {
    "expected_sharpe": 2.0,
    "diversification_ratio": 1.5,
    "turnover_reduction": 0.4
  }
}
```

## Key Insights

### Turnover Reduction Effect

The main value of combining alphas:

```
Individual Alphas:
- Alpha A: 500% turnover, Sharpe 1.5
- Alpha B: 800% turnover, Sharpe 1.2
- Alpha C: 300% turnover, Sharpe 0.9

Combined Portfolio:
- Net Turnover: 400% (not 1600%!)
- Position offsetting: A longs what B shorts
- Cost savings: 75% reduction!
```

**High-turnover alphas are valuable when combined!**

### NOT Red Flags

| NOT a Red Flag | Why | What To Do |
|----------------|-----|------------|
| High turnover | Position offsetting | Include, show cost reduction |
| High correlation | Still adds info | Include with cluster weight |
| Similar strategy | Noise reduction | Include in same cluster |

### Real Red Flags

| Red Flag | Symptom | Action |
|----------|---------|--------|
| Sharpe > 3.0 | Likely bug/overfit | Check code |
| No drawdowns | Perfect backtest | Likely bug |
| Hypothesis mismatch | Position != thesis | Mark misaligned |

## Quality Bar

- Diversified: avg pairwise corr < 0.5
- Risk-adjusted: portfolio Sharpe > avg individual
- Documented: clear rationale for each selection
- Cost-efficient: turnover reduction > 20%
