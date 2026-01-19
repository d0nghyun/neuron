---
name: flexible-report-generator
description: Generate analyst-quality reports with flexible layouts. Data-driven component selection and AI layout planning. HTML/Tailwind output with optional PDF export.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Flexible Report Generator

Generate professional, analyst-quality reports with dynamic layouts based on data characteristics.

## When to Apply

Activate this skill when:
- User needs to generate a data report/dashboard
- Creating analyst-style presentations (stock, crypto, macro)
- Converting raw data into visual narratives
- Building executive summaries with charts/metrics

Keywords: report, dashboard, analyst, visualization, metrics, KPI, chart, summary

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Report Generation Flow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Data (JSON) ──► SchemaAdapter ──► Analyzer ──► Component       │
│    Any format     Auto-detect       Profile     Selector        │
│                                                                 │
│                              ▼                                  │
│                                                                 │
│  Layout Planner ◄── Design Selector ◄── Purpose + Style         │
│    AI judgment      Color/Typography    User input              │
│                                                                 │
│                              ▼                                  │
│                                                                 │
│  HTML Render ──► [Optional] ──► PDF Export                      │
│    Jinja2 +       Playwright                                    │
│    Tailwind                                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Bounded Creativity [P10]

### Constraints (Fixed)
- Component library (defined set of components)
- Color palettes (per purpose/style)
- Output schema (HTML/PDF structure)
- Required sections per report type

### Creativity (AI Judgment)
- Which components to use
- Layout arrangement
- Section emphasis
- Chart type selection

## Schema Support

Supports three data formats:

### 1. New Schema (report-schema.md compliant)
```json
{
  "metadata": {"type": "stock", "title": "Analysis Report"},
  "sections": {
    "cover": {"headline": "Title", "hero_metrics": [...]},
    "executive_summary": {"key_points": [...]},
    "data_analysis": [{"title": "...", "visualizations": [...]}]
  }
}
```

### 2. Legacy Schema (original format)
```json
{
  "metrics": {"revenue": {"value": 1500000, "delta": 23}},
  "time_series": {"labels": [...], "datasets": [...]},
  "table": {"columns": [...], "rows": [...]}
}
```

### 3. Arbitrary JSON (auto-detected)
```json
{
  "revenue": 1500000,
  "quarterly_data": [100, 120, 140],
  "products": [{"name": "A", "sales": 500}]
}
```

## Component Library

### Metrics
| Component | Best For | Data |
|-----------|----------|------|
| HeroMetric | KPI headlines | value, delta, label, unit |
| TrendIndicator | Quick status | value, delta, direction |

### Charts
| Component | Best For | Data |
|-----------|----------|------|
| LineChart | Trends over time | labels[], datasets[] |
| BarChart | Category comparisons | labels[], datasets[] |
| DonutChart | Part-to-whole | labels[], data[] |
| ScatterPlot | Correlations | datasets[], x_label, y_label |
| Heatmap | Intensity matrices | columns[], rows[], row_labels |
| WaterfallChart | Change breakdown | labels[], datasets[] |

### Content
| Component | Best For | Data |
|-----------|----------|------|
| DataTable | Detailed data | columns[], rows[] |
| InsightCard | Key observations | headline, body, source |
| CalloutBox | Warnings/highlights | type, title, body |
| CoverPage | Report cover | headline, hero_metrics, rating |

## Layout Patterns

| Pattern | Best For | Grid |
|---------|----------|------|
| Executive Summary | C-level reports | 2-column hero, then grid |
| Data Deep Dive | Analyst reports | Single column, progressive |
| Dashboard Grid | Real-time monitoring | Dense 4-column grid |
| Storytelling | Narrative reports | Single column, prose |
| Comparison Focus | A/B analysis | 2-column throughout |

## Report Types

| Type | Data Skills | Analyst Agent |
|------|-------------|---------------|
| stock | finance-data | stock-analyst |
| crypto | crypto-data | crypto-analyst |
| macro | macro-data | macro-analyst |
| market | finance-data | market-analyst |
| custom | user-provided | - |

## Usage

### CLI
```bash
python3 .claude/skills/flexible-report-generator/scripts/report_cli.py \
  data.json \
  --title "Q4 Performance Report" \
  --purpose executive \
  --style witty \
  --output report.html
```

### Python
```python
from scripts.report_generator import ReportGenerator
from scripts.schema_adapter import SchemaAdapter

# Auto-adapt any schema
adapter = SchemaAdapter()
data = adapter.adapt(raw_data)

# Generate report
generator = ReportGenerator()
html = generator.generate(
    data=data,
    title="Analysis Report",
    purpose="analyst",
    style="formal"
)
```

## Related Files

- `knowledge/report-schema.md` - Universal report structure
- `knowledge/report-constraints.yaml` - Guardrails
- `.claude/agents/report-generator.md` - Orchestrator agent
- `.claude/agents/stock-analyst.md` - Stock analysis
- `.claude/agents/crypto-analyst.md` - Crypto analysis
- `.claude/agents/macro-analyst.md` - Macro analysis

## Dependencies

```bash
pip install jinja2
# For PDF export:
pip install playwright && playwright install chromium
```
