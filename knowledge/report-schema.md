# Report Schema - Universal Analyst Report Structure

> SSOT for all analyst report types (stock, crypto, macro, market)

## Core Philosophy

**Bounded Creativity [P10]:**
- **Constraints**: Section structure, data sources, output format
- **Creativity**: Emphasis, narrative, visualization selection

## Universal Report Interface

```yaml
Report:
  metadata:
    type: enum[stock, crypto, macro, market, custom]
    title: string
    subtitle: string?
    date: ISO8601
    author: string?
    version: string?
    data_sources: DataSource[]

  sections:
    cover: CoverSection              # Required
    executive_summary: SummarySection # Required
    thesis: ThesisSection?           # Optional
    data_analysis: AnalysisSection[] # Required (1+)
    valuation: ValuationSection?     # Optional
    risks: RiskSection?              # Optional
    recommendation: RecommendSection? # Optional
    appendix: AppendixSection?       # Optional
```

## Section Definitions

### CoverSection
```yaml
CoverSection:
  headline: string           # Main title
  subheadline: string?       # Subtitle
  hero_metrics: Metric[]     # 1-4 key numbers
  hero_image: string?        # Optional cover image
  rating: Rating?            # Buy/Hold/Sell or equivalent
```

### SummarySection
```yaml
SummarySection:
  key_points: string[]       # 3-5 bullet points
  highlights: Metric[]       # Key metrics with deltas
  primary_chart: ChartConfig? # One main visualization
```

### ThesisSection
```yaml
ThesisSection:
  headline: string           # Investment thesis in one line
  rationale: string          # 2-3 paragraph explanation
  catalysts: Catalyst[]      # What will drive change
  time_horizon: string       # "12 months", "Long-term", etc.
```

### AnalysisSection
```yaml
AnalysisSection:
  title: string
  narrative: string          # AI-generated analysis text
  data: StructuredData       # Tables, time series, etc.
  visualizations: ChartConfig[]
  insights: Insight[]        # Key observations
```

### ValuationSection
```yaml
ValuationSection:
  method: enum[DCF, Multiples, NetworkValue, Relative, Custom]
  fair_value: ValueEstimate
  scenarios: Scenario[]      # Bull/Base/Bear cases
  sensitivity: SensitivityTable?
```

### RiskSection
```yaml
RiskSection:
  risks: Risk[]
  risk_matrix: RiskMatrix?   # Probability x Impact
  mitigants: string[]
```

### RecommendSection
```yaml
RecommendSection:
  action: enum[StrongBuy, Buy, Hold, Sell, StrongSell, Custom]
  target: ValueEstimate?
  rationale: string
  disclaimers: string[]      # Required legal text
```

## Data Types

### Metric
```yaml
Metric:
  label: string
  value: number | string
  unit: string?              # "$", "%", "KRW", etc.
  delta: number?             # Change percentage
  delta_period: string?      # "QoQ", "YoY", "vs prev"
  status: enum[positive, negative, neutral]?
  format: enum[number, currency, percentage, text]?
```

### ChartConfig
```yaml
ChartConfig:
  type: enum[line, bar, area, scatter, heatmap, waterfall, donut, sankey]
  title: string?
  data: ChartData
  options: ChartOptions?
  height: number?            # In pixels, default 300
```

### ChartData
```yaml
ChartData:
  labels: string[]           # X-axis labels
  datasets: Dataset[]

Dataset:
  label: string
  data: number[]
  color: string?
  is_forecast: boolean?      # For forecast styling
```

### Risk
```yaml
Risk:
  title: string
  description: string
  probability: enum[low, medium, high]
  impact: enum[low, medium, high]
  category: string?          # "Market", "Operational", etc.
```

### Insight
```yaml
Insight:
  headline: string
  body: string
  supporting_metric: Metric?
  source: string?
  priority: enum[high, medium, low]?
```

## Domain-Specific Extensions

### Stock Report Extensions
```yaml
StockExtensions:
  ticker: string
  exchange: string
  sector: string
  market_cap: Metric
  financials:
    income_statement: FinancialTable
    balance_sheet: FinancialTable
    cash_flow: FinancialTable
  multiples:
    pe_ratio: Metric
    pb_ratio: Metric
    ev_ebitda: Metric
  peers: PeerComparison[]
```

### Crypto Report Extensions
```yaml
CryptoExtensions:
  token: string
  chain: string
  protocol_type: string
  tokenomics:
    total_supply: Metric
    circulating_supply: Metric
    inflation_rate: Metric
    vesting_schedule: VestingEvent[]
  on_chain:
    tvl: Metric
    dau: Metric
    transaction_volume: Metric
    whale_holdings: Metric
```

### Macro Report Extensions
```yaml
MacroExtensions:
  region: string
  countries: string[]
  indicators:
    gdp: Metric
    inflation: Metric
    unemployment: Metric
    interest_rate: Metric
  forecasts: Forecast[]
  policy_outlook: string
```

## Component Mapping

| Data Type | Recommended Component | Fallback |
|-----------|----------------------|----------|
| Single Metric | HeroMetric | TrendIndicator |
| Metric Array | MetricGrid | DataTable |
| Time Series | LineChart | AreaChart |
| Categories | BarChart | DataTable |
| Distribution | DonutChart | BarChart |
| Comparison | ComparisonGrid | DataTable |
| Correlation | ScatterPlot | DataTable |
| Flow | Sankey | WaterfallChart |
| Intensity | Heatmap | DataTable |
| Risk Matrix | ScatterPlot | DataTable |
| Long Text | InsightCard | QuoteBlock |

## Rendering Rules

### Page Structure
```
Cover (1 page) → Executive Summary (1 page) → Content (N pages) → Appendix (optional)
```

### Auto Layout Rules
1. **Hero metrics**: Always at top, max 4 per row
2. **Charts**: Full width or 2-column, never more than 2 per row
3. **Tables**: Full width, scrollable if > 10 rows
4. **Insights**: 2-column grid, max 4 per section
5. **Page breaks**: Before new major section

### Responsive Breakpoints
- Desktop: max-width 1200px
- Tablet: max-width 768px
- Print/PDF: A4 fixed width

## Example: Minimal Valid Report

```json
{
  "metadata": {
    "type": "stock",
    "title": "Samsung Electronics Analysis",
    "date": "2026-01-19"
  },
  "sections": {
    "cover": {
      "headline": "Samsung Electronics",
      "hero_metrics": [
        {"label": "Target Price", "value": 85000, "unit": "KRW", "delta": 12}
      ]
    },
    "executive_summary": {
      "key_points": [
        "Memory chip cycle recovery expected in H2",
        "Foundry business gaining market share"
      ],
      "highlights": [
        {"label": "Revenue", "value": 280, "unit": "T KRW", "delta": 15}
      ]
    },
    "data_analysis": [
      {
        "title": "Financial Performance",
        "narrative": "Revenue grew 15% YoY driven by...",
        "visualizations": [
          {
            "type": "line",
            "title": "Quarterly Revenue",
            "data": {
              "labels": ["Q1", "Q2", "Q3", "Q4"],
              "datasets": [{"label": "2025", "data": [65, 70, 72, 73]}]
            }
          }
        ]
      }
    ]
  }
}
```
