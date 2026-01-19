# Report Generator - Migration Guide for Claude Agent SDK

## Overview

This package is designed to be portable to Claude Agent SDK environments with MCP integration.

## Package Structure (Target)

```
report-generator/
├── pyproject.toml           # Package definition
├── requirements.txt         # Dependencies
├── README.md               # Usage guide
│
├── src/
│   └── report_generator/
│       ├── __init__.py
│       ├── generator.py     # Main ReportGenerator class
│       ├── schema_adapter.py
│       ├── components/
│       │   ├── __init__.py
│       │   ├── metrics.py
│       │   ├── charts.py
│       │   └── content.py
│       └── templates/       # Jinja2 templates
│
├── agents/                  # Agent SDK definitions
│   ├── report_orchestrator.py
│   ├── stock_analyst.py
│   ├── crypto_analyst.py
│   └── macro_analyst.py
│
├── mcp/                     # MCP tool definitions
│   ├── finance_data.py
│   ├── crypto_data.py
│   └── macro_data.py
│
└── knowledge/               # Static knowledge base
    ├── report_schema.md
    └── report_constraints.yaml
```

## Migration Steps

### 1. Copy Core Files

```bash
# From neuron repo
cp -r .claude/skills/flexible-report-generator/scripts/* report-generator/src/report_generator/
cp -r .claude/skills/flexible-report-generator/templates/* report-generator/src/report_generator/templates/
cp -r .claude/skills/flexible-report-generator/data/* report-generator/src/report_generator/data/
cp knowledge/report-schema.md report-generator/knowledge/
cp knowledge/report-constraints.yaml report-generator/knowledge/
```

### 2. Install in Agent SDK Environment

```bash
cd report-generator
pip install -e .
```

### 3. Register MCP Tools

```python
# In your Agent SDK setup
from report_generator.mcp import finance_data, crypto_data, macro_data

# Register as MCP tools
mcp.register_tool("finance-data", finance_data.get_stock_data)
mcp.register_tool("crypto-data", crypto_data.get_token_data)
mcp.register_tool("macro-data", macro_data.get_economic_data)
```

### 4. Create Agent

```python
from claude_agent_sdk import Agent
from report_generator import ReportGenerator
from report_generator.agents import ReportOrchestrator

# Create the report orchestrator agent
orchestrator = ReportOrchestrator(
    generator=ReportGenerator(),
    mcp_client=mcp_client,
)

# Run
result = await orchestrator.generate_report(
    query="삼성전자 분석 리포트",
    output_format="html"
)
```

## MCP Tool Interface

### finance-data

```python
@mcp_tool
def get_stock_data(
    ticker: str,
    metrics: list[str],
    period: str = "1Y"
) -> dict:
    """
    Fetch stock financial data.

    Args:
        ticker: Stock ticker (e.g., "005930.KS", "AAPL")
        metrics: List of metrics to fetch
        period: Time period ("1Y", "5Y", "MAX")

    Returns:
        {
            "ticker": "005930.KS",
            "name": "Samsung Electronics",
            "metrics": {
                "price": {"value": 85000, "delta": 12},
                "pe_ratio": {"value": 15.2},
                ...
            },
            "time_series": {
                "revenue": {"labels": [...], "data": [...]},
                ...
            }
        }
    """
```

### crypto-data

```python
@mcp_tool
def get_token_data(
    token: str,
    metrics: list[str],
    chain: str = "ethereum"
) -> dict:
    """
    Fetch crypto token/protocol data.

    Args:
        token: Token symbol or protocol name
        metrics: List of metrics (tvl, price, volume, etc.)
        chain: Blockchain network

    Returns:
        {
            "token": "ETH",
            "chain": "ethereum",
            "metrics": {
                "price": {"value": 3500, "delta": 5.2},
                "tvl": {"value": 50000000000},
                ...
            },
            "on_chain": {
                "active_addresses": {"labels": [...], "data": [...]},
                ...
            }
        }
    """
```

### macro-data

```python
@mcp_tool
def get_economic_data(
    region: str,
    indicators: list[str],
    period: str = "5Y"
) -> dict:
    """
    Fetch macroeconomic data.

    Args:
        region: Country/region code ("US", "KR", "EU")
        indicators: Economic indicators (gdp, inflation, etc.)
        period: Time period

    Returns:
        {
            "region": "US",
            "indicators": {
                "gdp_growth": {"value": 2.5, "delta": 0.3},
                "inflation": {"value": 2.8},
                ...
            },
            "time_series": {
                "gdp": {"labels": [...], "data": [...]},
                ...
            }
        }
    """
```

## Agent SDK Integration

### ReportOrchestrator Agent

```python
class ReportOrchestrator:
    """
    Main orchestrator agent for report generation.

    Workflow:
    1. Parse user query → determine report type
    2. Call appropriate MCP data tools
    3. Route to domain analyst subagent
    4. Generate final report
    """

    def __init__(self, generator, mcp_client):
        self.generator = generator
        self.mcp = mcp_client
        self.analysts = {
            "stock": StockAnalyst(),
            "crypto": CryptoAnalyst(),
            "macro": MacroAnalyst(),
        }

    async def generate_report(
        self,
        query: str,
        output_format: str = "html"
    ) -> str:
        # 1. Parse query
        report_type, subject = self._parse_query(query)

        # 2. Collect data via MCP
        data = await self._collect_data(report_type, subject)

        # 3. Analyze with domain agent
        analyst = self.analysts.get(report_type)
        analysis = await analyst.analyze(data)

        # 4. Generate report
        report = self.generator.generate(
            data=analysis,
            title=f"{subject} Analysis",
            purpose=report_type,
        )

        return report
```

## Environment Variables

```bash
# Required for MCP data sources
YAHOO_FINANCE_API_KEY=xxx
COINGECKO_API_KEY=xxx
FRED_API_KEY=xxx

# Optional
OPENAI_API_KEY=xxx  # For embeddings if needed
```

## Testing After Migration

```python
# Test basic generation
from report_generator import ReportGenerator

gen = ReportGenerator()
html = gen.generate(
    data={"metrics": {"test": {"value": 100}}},
    title="Test Report"
)
assert len(html) > 0

# Test MCP integration
from report_generator.mcp import finance_data
data = await finance_data.get_stock_data("AAPL", ["price", "pe_ratio"])
assert "metrics" in data

# Test full pipeline
from report_generator.agents import ReportOrchestrator
orchestrator = ReportOrchestrator(gen, mcp_client)
report = await orchestrator.generate_report("Apple 분석")
assert len(report) > 0
```
