# Portfolio Output Schema

## portfolio.json

```json
{
  "metadata": {
    "universe": "us_stock",
    "created_at": "2026-01-29T00:00:00Z",
    "total_alphas": 10,
    "weight_method": "cluster_equal",
    "turnover_reduction": 0.4
  },
  "alphas": [
    {
      "alpha_id": "abc123",
      "title": "Momentum Strategy",
      "category": "momentum",
      "weight": 0.15,
      "cluster": 1,
      "sharpe_ratio": 1.5,
      "cagr_pct": 12.5,
      "mdd_pct": -15.2,
      "rationale": "Core momentum exposure with strong economic basis",
      "evaluation": {
        "rationale_alignment": "aligned",
        "economic_sense": "strong",
        "portfolio_fit": "core",
        "red_flags": []
      }
    }
  ],
  "clusters": [
    {
      "cluster_id": 1,
      "name": "Momentum",
      "alpha_count": 3,
      "total_weight": 0.33,
      "avg_correlation": 0.65
    }
  ],
  "portfolio_metrics": {
    "expected_sharpe": 2.0,
    "expected_cagr_pct": 15.0,
    "expected_mdd_pct": -12.0,
    "diversification_ratio": 1.5,
    "avg_pairwise_correlation": 0.35,
    "combined_turnover": 400,
    "individual_turnover_sum": 1600,
    "turnover_reduction": 0.75
  }
}
```

## Field Descriptions

### metadata

| Field | Type | Description |
|-------|------|-------------|
| universe | string | Target market (us_stock, kr_stock, etc.) |
| created_at | ISO datetime | Creation timestamp |
| total_alphas | int | Number of alphas in portfolio |
| weight_method | string | cluster_equal, equal, risk_parity |
| turnover_reduction | float | 0-1, how much turnover reduced |

### alphas[]

| Field | Type | Description |
|-------|------|-------------|
| alpha_id | string | Unique alpha identifier |
| title | string | Alpha name/title |
| category | string | momentum, value, quality, etc. |
| weight | float | Portfolio weight (0-1) |
| cluster | int | Cluster assignment |
| sharpe_ratio | float | Individual Sharpe |
| rationale | string | Why included |
| evaluation | object | PM evaluation details |

### clusters[]

| Field | Type | Description |
|-------|------|-------------|
| cluster_id | int | Cluster identifier |
| name | string | Cluster description |
| alpha_count | int | Alphas in cluster |
| total_weight | float | Combined weight |
| avg_correlation | float | Avg intra-cluster corr |

### portfolio_metrics

| Field | Type | Description |
|-------|------|-------------|
| expected_sharpe | float | Portfolio Sharpe estimate |
| diversification_ratio | float | > 1 means diversified |
| turnover_reduction | float | Cost saving ratio |
