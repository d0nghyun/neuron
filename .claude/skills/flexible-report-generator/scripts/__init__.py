"""
Report Generator Package

Flexible report generation with AI-driven layout planning.
Supports stock, crypto, macro, and custom report types.

Usage:
    from report_generator import ReportGenerator, SchemaAdapter

    # Adapt any data format
    adapter = SchemaAdapter()
    data = adapter.adapt(raw_data)

    # Generate report
    generator = ReportGenerator()
    html = generator.generate(data, title="My Report")

For MCP integration:
    from report_generator.mcp_interface import (
        FinanceDataSource,
        CryptoDataSource,
        MacroDataSource,
        get_data_source,
    )
"""

from .report_generator import (
    ReportGenerator,
    DataAnalyzer,
    ComponentSelector,
    LayoutPlanner,
    DesignSelector,
)
from .schema_adapter import SchemaAdapter, adapt_schema

__version__ = "0.2.0"
__all__ = [
    "ReportGenerator",
    "SchemaAdapter",
    "adapt_schema",
    "DataAnalyzer",
    "ComponentSelector",
    "LayoutPlanner",
    "DesignSelector",
]
