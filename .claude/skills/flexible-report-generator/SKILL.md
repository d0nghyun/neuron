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
- Creating analyst-style presentations
- Converting raw data into visual narratives
- Building executive summaries with charts/metrics

Keywords: report, dashboard, analyst, visualization, metrics, KPI, chart, summary

## Architecture

```
Data (JSON) → Analyzer → Component Selector → Layout Planner → HTML Render → [PDF Export]
  확정적        확정적         AI 판단          AI 판단         확정적         선택적
```

## Workflow

### Step 1: Prepare Data (JSON format)

```json
{
  "metrics": {
    "revenue": {"value": 1500000, "delta": 23, "label": "Total Revenue", "unit": "$"},
    "users": {"value": 50000, "delta": 15, "label": "Active Users"}
  },
  "time_series": {
    "labels": ["Jan", "Feb", "Mar", "Apr"],
    "datasets": [
      {"label": "Revenue", "data": [100, 120, 140, 180]},
      {"label": "Users", "data": [1000, 1200, 1500, 2000]}
    ]
  },
  "table": {
    "columns": ["Product", "Revenue", "Growth"],
    "rows": [
      ["Product A", "$500K", "+12%"],
      ["Product B", "$300K", "+8%"]
    ]
  },
  "insights": [
    {"headline": "Key Finding", "body": "Revenue grew 23% this quarter"}
  ]
}
```

### Step 2: Generate Report

```bash
python3 .claude/skills/flexible-report-generator/scripts/report_cli.py \
  data.json \
  --title "Q4 Performance Report" \
  --purpose executive \
  --style witty \
  --output report.html
```

### Step 3: Export to PDF (Optional)

```bash
python3 .claude/skills/flexible-report-generator/scripts/report_cli.py \
  data.json \
  --title "Q4 Performance Report" \
  --format pdf \
  --output report.pdf
```

## Component Library

| Component | Type | Best For | Layout Weight |
|-----------|------|----------|---------------|
| HeroMetric | metric | KPI headlines, key findings | 1 |
| TrendIndicator | metric | Quick status indicators | 1 |
| LineChart | chart | Trends over time | 2 |
| BarChart | chart | Category comparisons | 2 |
| DonutChart | chart | Part-to-whole relationships | 1 |
| DataTable | table | Detailed data display | 2-3 |
| InsightCard | insight | Key observations | 1 |
| QuoteBlock | insight | Impactful statements | 1 |
| ComparisonGrid | comparison | A/B comparisons | 2 |

## Layout Patterns

| Pattern | Best For | Grid |
|---------|----------|------|
| Executive Summary | C-level reports | 2-column hero, then grid |
| Data Deep Dive | Analyst reports | Single column, progressive detail |
| Dashboard Grid | Real-time monitoring | Dense 4-column grid |
| Storytelling | Narrative reports | Single column, prose width |

## Analyst Styles

| Style | Tone | Example Headline |
|-------|------|------------------|
| witty | Sharp, clever | "The Numbers Don't Lie (But They Do Exaggerate)" |
| formal | Professional | "Q4 Performance: Key Metrics" |
| storyteller | Narrative | "The Hidden Pattern in Your Data" |
| minimalist | Clean, factual | "Revenue: +23%" |

## Output

- **HTML**: Tailwind CSS styling, Chart.js visualizations, responsive design
- **PDF**: Optional export via Playwright (requires `playwright install chromium`)

## Dependencies

```bash
pip install jinja2
# For PDF export:
pip install playwright && playwright install chromium
```

## Example

```python
from scripts.report_generator import ReportGenerator

generator = ReportGenerator()
html = generator.generate(
    data=your_data,
    title="Q4 Report",
    purpose="executive",
    style="witty"
)
```
