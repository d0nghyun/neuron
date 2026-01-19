#!/usr/bin/env python3
"""
Schema Adapter - Convert new report schema to internal format

Supports both:
1. New schema (report-schema.md compliant)
2. Legacy schema (original flexible-report-generator format)

[P5 Modularity] - Adapter pattern for backwards compatibility
"""

from dataclasses import dataclass, field
from typing import Any, Optional
import json


@dataclass
class Metric:
    """Standardized metric representation."""
    label: str
    value: Any
    unit: str = ""
    delta: Optional[float] = None
    delta_period: str = "vs prev"
    status: str = "neutral"  # positive, negative, neutral
    format: str = "number"   # number, currency, percentage, text

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "value": self.value,
            "unit": self.unit,
            "delta": self.delta,
            "delta_period": self.delta_period,
            "status": self.status,
            "format": self.format
        }


@dataclass
class ChartData:
    """Standardized chart data."""
    type: str  # line, bar, area, scatter, etc.
    title: str
    labels: list
    datasets: list
    height: int = 300
    options: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "title": self.title,
            "labels": self.labels,
            "datasets": self.datasets,
            "height": self.height,
            "options": self.options
        }


@dataclass
class Insight:
    """Standardized insight."""
    headline: str
    body: str
    source: str = ""
    priority: str = "medium"


class SchemaAdapter:
    """
    Adapts various input schemas to internal report format.

    Supports:
    - New schema (from report-schema.md)
    - Legacy schema (original format)
    - Auto-detection of arbitrary JSON structures
    """

    def adapt(self, data: dict) -> dict:
        """
        Main entry point. Auto-detects schema and adapts.

        Returns internal format:
        {
            "metadata": {...},
            "metrics": {...},
            "time_series": {...},
            "insights": [...],
            "table": {...},
            "sections": [...],  # For multi-page
        }
        """
        # Detect schema version
        if self._is_new_schema(data):
            return self._adapt_new_schema(data)
        elif self._is_legacy_schema(data):
            return self._adapt_legacy_schema(data)
        else:
            return self._adapt_arbitrary(data)

    def _is_new_schema(self, data: dict) -> bool:
        """Check if data follows new report-schema.md format."""
        return "metadata" in data and "sections" in data

    def _is_legacy_schema(self, data: dict) -> bool:
        """Check if data follows original flexible-report-generator format."""
        return "metrics" in data or "time_series" in data or "table" in data

    def _adapt_new_schema(self, data: dict) -> dict:
        """Convert new schema to internal format."""
        result = {
            "metadata": data.get("metadata", {}),
            "metrics": {},
            "time_series": None,
            "insights": [],
            "table": None,
            "sections": [],
            "cover": None,
            "executive_summary": None,
        }

        sections = data.get("sections", {})

        # Extract cover
        if "cover" in sections:
            cover = sections["cover"]
            result["cover"] = {
                "headline": cover.get("headline", ""),
                "subheadline": cover.get("subheadline", ""),
                "rating": cover.get("rating"),
            }
            # Convert hero_metrics to metrics
            for i, m in enumerate(cover.get("hero_metrics", [])):
                key = m.get("label", f"metric_{i}").lower().replace(" ", "_")
                result["metrics"][key] = self._normalize_metric(m)

        # Extract executive summary
        if "executive_summary" in sections:
            summary = sections["executive_summary"]
            result["executive_summary"] = {
                "key_points": summary.get("key_points", []),
            }
            # Convert highlights to additional metrics
            for m in summary.get("highlights", []):
                key = m.get("label", "").lower().replace(" ", "_")
                if key and key not in result["metrics"]:
                    result["metrics"][key] = self._normalize_metric(m)
            # Extract primary chart
            if "primary_chart" in summary:
                result["time_series"] = self._normalize_chart(summary["primary_chart"])

        # Extract data_analysis sections
        for section in sections.get("data_analysis", []):
            adapted_section = {
                "title": section.get("title", "Analysis"),
                "narrative": section.get("narrative", ""),
                "insights": [],
                "charts": [],
                "tables": [],
            }

            # Insights
            for insight in section.get("insights", []):
                result["insights"].append({
                    "headline": insight.get("headline", ""),
                    "body": insight.get("body", ""),
                    "source": insight.get("source", ""),
                })

            # Visualizations
            for viz in section.get("visualizations", []):
                chart = self._normalize_chart(viz)
                adapted_section["charts"].append(chart)
                # First chart becomes primary if not set
                if result["time_series"] is None:
                    result["time_series"] = chart

            # Data/Tables
            if "data" in section:
                table = self._extract_table(section["data"])
                if table:
                    adapted_section["tables"].append(table)
                    if result["table"] is None:
                        result["table"] = table

            result["sections"].append(adapted_section)

        # Extract risks
        if "risks" in sections:
            risk_section = sections["risks"]
            for risk in risk_section.get("risks", []):
                result["insights"].append({
                    "headline": f"Risk: {risk.get('title', '')}",
                    "body": risk.get("description", ""),
                    "source": f"Probability: {risk.get('probability', 'N/A')}, Impact: {risk.get('impact', 'N/A')}",
                })

        # Extract recommendation
        if "recommendation" in sections:
            rec = sections["recommendation"]
            result["recommendation"] = {
                "action": rec.get("action", ""),
                "target": rec.get("target"),
                "rationale": rec.get("rationale", ""),
            }

        return result

    def _adapt_legacy_schema(self, data: dict) -> dict:
        """Pass through legacy schema with minimal normalization."""
        result = {
            "metadata": data.get("metadata", {"type": "custom", "title": "Report"}),
            "metrics": {},
            "time_series": data.get("time_series"),
            "insights": data.get("insights", []),
            "table": data.get("table"),
            "sections": [],
        }

        # Normalize metrics
        if "metrics" in data:
            for key, value in data["metrics"].items():
                result["metrics"][key] = self._normalize_metric(value)

        return result

    def _adapt_arbitrary(self, data: dict) -> dict:
        """
        Auto-detect structure from arbitrary JSON.
        [P16] AI judgment layer - infer data types.
        """
        result = {
            "metadata": {"type": "custom", "title": "Auto-Generated Report"},
            "metrics": {},
            "time_series": None,
            "insights": [],
            "table": None,
            "sections": [],
        }

        for key, value in data.items():
            if isinstance(value, (int, float)):
                # Single number → metric
                result["metrics"][key] = {
                    "label": self._key_to_label(key),
                    "value": value,
                    "unit": self._infer_unit(key),
                }
            elif isinstance(value, dict):
                if "value" in value:
                    # Looks like a metric
                    result["metrics"][key] = self._normalize_metric(value)
                elif "labels" in value and "datasets" in value:
                    # Looks like chart data
                    result["time_series"] = self._normalize_chart(value)
                elif "columns" in value and "rows" in value:
                    # Looks like table
                    result["table"] = value
            elif isinstance(value, list):
                if len(value) > 0:
                    first = value[0]
                    if isinstance(first, dict):
                        if "headline" in first or "body" in first:
                            # Looks like insights
                            result["insights"] = value
                        elif all(isinstance(v, dict) for v in value):
                            # List of objects → table
                            result["table"] = self._list_to_table(value)
                    elif isinstance(first, (int, float)):
                        # Numeric array → time series
                        result["time_series"] = {
                            "title": self._key_to_label(key),
                            "labels": [str(i) for i in range(len(value))],
                            "datasets": [{"label": key, "data": value}]
                        }
            elif isinstance(value, str) and len(value) > 50:
                # Long text → insight
                result["insights"].append({
                    "headline": self._key_to_label(key),
                    "body": value,
                })

        return result

    def _normalize_metric(self, m: dict) -> dict:
        """Normalize a metric to standard format."""
        if not isinstance(m, dict):
            return {"label": str(m), "value": m}

        return {
            "label": m.get("label", ""),
            "value": m.get("value", 0),
            "unit": m.get("unit", ""),
            "delta": m.get("delta"),
            "delta_period": m.get("delta_period", "vs prev"),
            "status": self._infer_status(m.get("delta")),
        }

    def _normalize_chart(self, chart: dict) -> dict:
        """Normalize chart config."""
        if not isinstance(chart, dict):
            return None

        return {
            "type": chart.get("type", "line"),
            "title": chart.get("title", ""),
            "labels": chart.get("labels", chart.get("data", {}).get("labels", [])),
            "datasets": chart.get("datasets", chart.get("data", {}).get("datasets", [])),
            "height": chart.get("height", 300),
        }

    def _extract_table(self, data: Any) -> Optional[dict]:
        """Extract table from various formats."""
        if isinstance(data, dict):
            if "columns" in data and "rows" in data:
                return data
        elif isinstance(data, list) and len(data) > 0:
            return self._list_to_table(data)
        return None

    def _list_to_table(self, items: list) -> dict:
        """Convert list of dicts to table format."""
        if not items or not isinstance(items[0], dict):
            return None

        columns = list(items[0].keys())
        rows = [[item.get(col, "") for col in columns] for item in items]

        return {
            "columns": columns,
            "rows": rows,
        }

    def _key_to_label(self, key: str) -> str:
        """Convert snake_case key to Title Case label."""
        return key.replace("_", " ").replace("-", " ").title()

    def _infer_unit(self, key: str) -> str:
        """Infer unit from key name."""
        key_lower = key.lower()
        if any(x in key_lower for x in ["price", "revenue", "cost", "value"]):
            return "$"
        if any(x in key_lower for x in ["rate", "ratio", "percent", "growth"]):
            return "%"
        return ""

    def _infer_status(self, delta: Optional[float]) -> str:
        """Infer status from delta."""
        if delta is None:
            return "neutral"
        if delta > 0:
            return "positive"
        if delta < 0:
            return "negative"
        return "neutral"


# Utility function for direct use
def adapt_schema(data: dict) -> dict:
    """Convenience function to adapt any schema."""
    adapter = SchemaAdapter()
    return adapter.adapt(data)


if __name__ == "__main__":
    # Test with various inputs

    # New schema
    new_schema = {
        "metadata": {"type": "stock", "title": "Test Report"},
        "sections": {
            "cover": {
                "headline": "Company Analysis",
                "hero_metrics": [
                    {"label": "Revenue", "value": 1000000, "delta": 15}
                ]
            },
            "executive_summary": {
                "key_points": ["Point 1", "Point 2"]
            },
            "data_analysis": [
                {
                    "title": "Financial Analysis",
                    "visualizations": [
                        {"type": "line", "labels": ["Q1", "Q2"], "datasets": [{"data": [100, 120]}]}
                    ]
                }
            ]
        }
    }

    # Legacy schema
    legacy_schema = {
        "metrics": {"revenue": {"value": 1000000, "delta": 15, "label": "Revenue"}},
        "time_series": {"labels": ["Q1", "Q2"], "datasets": [{"data": [100, 120]}]}
    }

    # Arbitrary JSON
    arbitrary = {
        "revenue": 1000000,
        "growth_rate": 15.5,
        "quarterly_data": [100, 120, 140, 160],
        "products": [
            {"name": "A", "sales": 500},
            {"name": "B", "sales": 300}
        ]
    }

    adapter = SchemaAdapter()

    print("=== New Schema ===")
    print(json.dumps(adapter.adapt(new_schema), indent=2, default=str)[:500])

    print("\n=== Legacy Schema ===")
    print(json.dumps(adapter.adapt(legacy_schema), indent=2, default=str)[:500])

    print("\n=== Arbitrary JSON ===")
    print(json.dumps(adapter.adapt(arbitrary), indent=2, default=str)[:500])
