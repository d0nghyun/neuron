# Portfolio Construction Orchestrator

Multi-agent workflow for portfolio construction from alpha pool.

## Critical Rules

1. **MCP-First**: Alpha-pool MCP is the source of truth
2. **PM Persona**: Evaluate like a rational Portfolio Manager
3. **Cost-Aware**: Turnover reduction is key value
4. **File-Based Results**: Save all outputs to phase folders

## Folder Structure

```
workspace/
├── CLAUDE.md
├── phase1/
│   └── context.json          # Alpha pool context
├── phase2/
│   ├── correlation.png       # Correlation matrix
│   ├── turnover_analysis.json
│   └── analysis.json         # Quantitative analysis
├── phase3/
│   └── evaluations.json      # PM evaluations
├── phase4/
│   ├── portfolio_state.json  # Final state
│   └── portfolio.json        # Output for API
└── output/
    └── portfolio.json        # Final output (symlink)
```

## Agents

| Agent | Layer | Model | Role |
|-------|-------|-------|------|
| portfolio-manager | business | sonnet | Evaluate, select, weight |
| quant-analyst | worker | haiku | Correlation, turnover analysis |

## Workflow

### Phase 1: FETCH CONTEXT

Fetch alpha pool from MCP:

```python
# List available alphas
mcp__alpha_pool__search_alphas(
    query="*",
    universe="us_stock",
    verdict="DEPLOYED"
)
```

Save to `phase1/context.json`:
- Alpha metadata (id, title, category)
- Performance metrics (sharpe, cagr, mdd)
- Document (hypothesis, findings)

### Phase 2: QUANTITATIVE ANALYSIS

```python
Task(
    subagent_type="quant-analyst",
    prompt="Analyze alphas in phase1/context.json: correlations, turnover",
    model="haiku"
)
```

Output files:
- `phase2/correlation.png` - Heatmap
- `phase2/turnover_analysis.json` - Individual vs combined
- `phase2/analysis.json` - Summary stats

**Key Insight**: Combined turnover << Sum of individual turnovers (position offsetting)

### Phase 3: PM EVALUATION

```python
Task(
    subagent_type="portfolio-manager",
    prompt="Evaluate alphas using 4 perspectives",
    model="sonnet"
)
```

**4 Evaluation Perspectives**:

| Perspective | Question |
|-------------|----------|
| Rationale Alignment | 가설과 실제 포지션이 일치하는가? |
| Economic Sense | 투자 논리가 경제적으로 타당한가? |
| Portfolio Fit | 기존 알파들과 차별화된 가치가 있는가? |
| Red Flags | 의심스러운 패턴이 있는가? |

Output: `phase3/evaluations.json`

```json
{
  "evaluations": [
    {
      "alpha_id": "abc123",
      "rationale_alignment": "aligned",
      "economic_sense": "strong",
      "portfolio_fit": "core",
      "red_flags": [],
      "recommendation": "select",
      "reasoning": "..."
    }
  ]
}
```

### Phase 4: BUILD PORTFOLIO

```python
# Calculate weights (equal weight MVP)
selected = [e for e in evaluations if e.recommendation == "select"]
weights = {alpha.id: 1.0 / len(selected) for alpha in selected}
```

**CRITICAL - NO EXCLUSION for correlation/turnover!**

Instead use cluster-based weighting:
- High correlation alphas → Same cluster → Lower individual weight
- High turnover alphas → Value from position offsetting

Output files:
- `phase4/portfolio_state.json` - Full state
- `phase4/portfolio.json` - API output format

### Phase 5: SAVE TO ALPHA-POOL

```python
# Save portfolio result
portfolio_data = json.load(open("phase4/portfolio.json"))

mcp__alpha_pool__create_alpha({
    "title": f"Portfolio: {len(selected)} alphas",
    "category": "portfolio",
    "universe": portfolio_data["metadata"]["universe"],
    "verdict": "DEPLOYED",
    "document": json.dumps(portfolio_data),
    "sharpe_ratio": portfolio_data["portfolio_metrics"]["expected_sharpe"]
})
```

## MCP Servers

- **alpha-pool**: Alpha storage (read alphas, write portfolio)

## Skills

| Skill | Used By |
|-------|---------|
| portfolio | All agents |

## Decision Guidelines

**SELECT (default)**: Include in portfolio
- Use cluster-based weighting for similar alphas
- High-turnover alphas valuable when combined

**EXCLUDE**: ONLY for critical issues
- Data bugs (look-ahead bias)
- Completely broken backtest
- NOT for high correlation
- NOT for high turnover

**REVIEW**: Human needed
- Mixed signals
- Edge cases

## Output Schema

`output/portfolio.json`:

```json
{
  "metadata": {
    "universe": "us_stock",
    "created_at": "2026-01-29T00:00:00Z",
    "total_alphas": 5,
    "weight_method": "cluster_equal"
  },
  "alphas": [
    {
      "alpha_id": "abc123",
      "title": "Momentum strategy",
      "weight": 0.2,
      "cluster": 1,
      "sharpe_ratio": 1.5,
      "rationale": "Core momentum exposure"
    }
  ],
  "portfolio_metrics": {
    "expected_sharpe": 2.0,
    "diversification_ratio": 1.5,
    "turnover_reduction": 0.4
  }
}
```

## Reference

- PM Evaluation Guide: `.claude/skills/portfolio/references/pm_evaluation_guide.md`
- Output Schema: `.claude/skills/portfolio/references/output-schema.md`
