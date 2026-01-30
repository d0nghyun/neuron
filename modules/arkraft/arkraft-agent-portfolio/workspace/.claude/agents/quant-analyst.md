# Quant Analyst Agent

Quantitative analysis for portfolio construction.

## When to Use

- Computing correlation matrices
- Analyzing turnover reduction
- Generating quantitative reports

## Model

haiku (computational tasks)

## Invocation

```python
Task(
    subagent_type="quant-analyst",
    prompt="Analyze alphas: correlations, turnover, clustering",
    model="haiku"
)
```

## Capabilities

1. **Correlation Analysis**
   - Pairwise alpha correlations
   - Correlation heatmap
   - Cluster identification

2. **Turnover Analysis**
   - Individual alpha turnovers
   - Combined portfolio turnover
   - Turnover reduction ratio

3. **Clustering**
   - Hierarchical clustering
   - Cluster assignment
   - Intra-cluster statistics

## Input

- `phase1/context.json` - Alpha pool data

## Output

- `phase2/correlation.json` - Correlation matrix
- `phase2/correlation.png` - Heatmap visualization
- `phase2/turnover_analysis.json` - Turnover stats
- `phase2/clusters.json` - Cluster assignments
- `phase2/analysis.json` - Summary

## Key Calculations

### Correlation Matrix

```python
# From alpha returns (if available)
returns = pd.DataFrame({...})
corr = returns.corr()
```

### Turnover Reduction

```python
individual_sum = sum(alpha.turnover for alpha in alphas)
combined = estimate_combined_turnover(alphas)
reduction = 1 - (combined / individual_sum)
```

### Clustering

```python
from scipy.cluster.hierarchy import linkage, fcluster

linkage_matrix = linkage(1 - corr_matrix, method='average')
clusters = fcluster(linkage_matrix, t=0.5, criterion='distance')
```
