#!/usr/bin/env python3
"""
Flexible Report Generator - Core Engine

Workflow: Data → Analyze → Select Components → Plan Layout → Render HTML
"""

import csv
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import jinja2
except ImportError:
    jinja2 = None

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
TEMPLATES_DIR = SKILL_DIR / "templates"


@dataclass
class DataProfile:
    """Analysis results of input data."""
    has_metrics: bool = False
    has_time_series: bool = False
    has_table: bool = False
    has_insights: bool = False
    metric_count: int = 0
    row_count: int = 0
    dataset_count: int = 0
    suggested_components: list = field(default_factory=list)


@dataclass
class Component:
    """A report component with data and styling."""
    type: str
    template: str
    data: dict
    weight: int = 1
    priority: int = 5
    grid_span: str = ""


@dataclass
class Layout:
    """Layout configuration for the report."""
    pattern: str
    grid_classes: str
    sections: list = field(default_factory=list)


@dataclass
class Design:
    """Visual design configuration."""
    colors: dict
    typography: dict
    style_name: str


class DataAnalyzer:
    """Analyze input data characteristics."""

    def analyze(self, data: dict) -> DataProfile:
        profile = DataProfile()

        # Check for metrics
        if "metrics" in data and data["metrics"]:
            profile.has_metrics = True
            profile.metric_count = len(data["metrics"])
            profile.suggested_components.append("HeroMetric")
            if profile.metric_count > 1:
                profile.suggested_components.append("TrendIndicator")

        # Check for time series
        if "time_series" in data and data["time_series"]:
            profile.has_time_series = True
            ts = data["time_series"]
            profile.dataset_count = len(ts.get("datasets", []))
            profile.suggested_components.append("LineChart")

        # Check for table data
        if "table" in data and data["table"]:
            profile.has_table = True
            profile.row_count = len(data["table"].get("rows", []))
            if profile.row_count > 0:
                profile.suggested_components.append("DataTable")

        # Check for insights
        if "insights" in data and data["insights"]:
            profile.has_insights = True
            profile.suggested_components.append("InsightCard")

        # Check for comparison data
        if "comparison" in data:
            profile.suggested_components.append("ComparisonGrid")

        return profile


class ComponentSelector:
    """Select components based on data profile."""

    def __init__(self):
        self.component_defs = self._load_components()

    def _load_components(self) -> dict:
        components = {}
        csv_path = DATA_DIR / "components.csv"
        if csv_path.exists():
            with open(csv_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    components[row["Component"]] = row
        return components

    def select(self, profile: DataProfile, data: dict) -> list[Component]:
        components = []

        # Add hero metrics (first and most important)
        if profile.has_metrics:
            metrics = data.get("metrics", {})
            for i, (key, metric) in enumerate(metrics.items()):
                comp = Component(
                    type="HeroMetric" if i == 0 else "TrendIndicator",
                    template="hero_metric.html.j2" if i == 0 else "trend_indicator.html.j2",
                    data={**metric, "id": key},
                    weight=1,
                    priority=1 if i == 0 else 2,
                    grid_span="col-span-2" if i == 0 else ""
                )
                components.append(comp)

        # Add insights early for impact
        if profile.has_insights:
            for i, insight in enumerate(data.get("insights", [])[:2]):
                comp = Component(
                    type="InsightCard",
                    template="insight_card.html.j2",
                    data={**insight, "id": f"insight-{i}"},
                    weight=1,
                    priority=2
                )
                components.append(comp)

        # Add charts
        if profile.has_time_series:
            ts = data.get("time_series", {})
            comp = Component(
                type="LineChart",
                template="chart_section.html.j2",
                data={
                    "id": "main-chart",
                    "chart_type": "line",
                    "title": ts.get("title", "Trend Analysis"),
                    "labels": ts.get("labels", []),
                    "datasets": ts.get("datasets", []),
                    "height": 300
                },
                weight=2,
                priority=3,
                grid_span="col-span-2"
            )
            components.append(comp)

        # Add bar chart if categorical data exists
        if "categories" in data:
            cat = data["categories"]
            comp = Component(
                type="BarChart",
                template="chart_section.html.j2",
                data={
                    "id": "bar-chart",
                    "chart_type": "bar",
                    "title": cat.get("title", "Category Breakdown"),
                    "labels": cat.get("labels", []),
                    "datasets": cat.get("datasets", []),
                    "height": 250
                },
                weight=2,
                priority=4
            )
            components.append(comp)

        # Add table last
        if profile.has_table:
            table = data.get("table", {})
            comp = Component(
                type="DataTable",
                template="data_table.html.j2",
                data={
                    "id": "main-table",
                    "title": table.get("title", "Detailed Data"),
                    "columns": table.get("columns", []),
                    "rows": table.get("rows", [])
                },
                weight=3,
                priority=5,
                grid_span="col-span-full"
            )
            components.append(comp)

        # Sort by priority
        components.sort(key=lambda c: c.priority)

        return components


class LayoutPlanner:
    """Plan layout based on components and purpose."""

    def __init__(self):
        self.layouts = self._load_layouts()

    def _load_layouts(self) -> dict:
        layouts = {}
        csv_path = DATA_DIR / "layouts.csv"
        if csv_path.exists():
            with open(csv_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    layouts[row["Layout Pattern"]] = row
        return layouts

    def plan(self, components: list[Component], purpose: str) -> Layout:
        # Map purpose to layout pattern
        purpose_map = {
            "executive": "Executive Summary",
            "analyst": "Data Deep Dive",
            "dashboard": "Dashboard Grid",
            "storytelling": "Storytelling",
            "comparison": "Comparison Focus"
        }

        pattern_name = purpose_map.get(purpose, "Executive Summary")
        pattern = self.layouts.get(pattern_name, {})

        # Create sections based on component types
        sections = self._create_sections(components, pattern)

        return Layout(
            pattern=pattern_name,
            grid_classes=pattern.get("Grid Classes", "grid-cols-1 lg:grid-cols-2"),
            sections=sections
        )

    def _create_sections(self, components: list[Component], pattern: dict) -> list:
        sections = []
        current_section = {"title": None, "components": [], "grid_classes": pattern.get("Grid Classes", "")}

        # Group by type for cleaner layout
        type_groups = {"metric": [], "insight": [], "chart": [], "table": [], "other": []}

        for comp in components:
            if comp.type in ["HeroMetric", "TrendIndicator"]:
                type_groups["metric"].append(comp)
            elif comp.type in ["InsightCard", "QuoteBlock"]:
                type_groups["insight"].append(comp)
            elif comp.type in ["LineChart", "BarChart", "DonutChart"]:
                type_groups["chart"].append(comp)
            elif comp.type == "DataTable":
                type_groups["table"].append(comp)
            else:
                type_groups["other"].append(comp)

        # Build sections in order
        if type_groups["metric"]:
            sections.append({
                "title": None,  # Hero section, no title
                "components": type_groups["metric"],
                "grid_classes": "grid-cols-2 md:grid-cols-4"
            })

        if type_groups["insight"]:
            sections.append({
                "title": "Key Insights",
                "components": type_groups["insight"],
                "grid_classes": "grid-cols-1 md:grid-cols-2"
            })

        if type_groups["chart"]:
            sections.append({
                "title": "Analysis",
                "components": type_groups["chart"],
                "grid_classes": "grid-cols-1 lg:grid-cols-2"
            })

        if type_groups["table"]:
            sections.append({
                "title": "Detailed Data",
                "components": type_groups["table"],
                "grid_classes": "grid-cols-1"
            })

        return sections


class DesignSelector:
    """Select visual design based on purpose and style."""

    def __init__(self):
        self.color_schemes = self._load_colors()
        self.styles = self._load_styles()

    def _load_colors(self) -> dict:
        schemes = {}
        csv_path = DATA_DIR / "color-schemes.csv"
        if csv_path.exists():
            with open(csv_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    schemes[row["Scheme"]] = row
        return schemes

    def _load_styles(self) -> dict:
        styles = {}
        csv_path = DATA_DIR / "analyst-styles.csv"
        if csv_path.exists():
            with open(csv_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    styles[row["Style"]] = row
        return styles

    def select(self, purpose: str, style: str) -> Design:
        # Map purpose to color scheme
        purpose_colors = {
            "executive": "Executive Gray",
            "analyst": "Analyst Orange",
            "dashboard": "Tech Purple",
            "storytelling": "Growth Green",
            "comparison": "Finance Blue"
        }

        scheme_name = purpose_colors.get(purpose, "Finance Blue")
        scheme = self.color_schemes.get(scheme_name, list(self.color_schemes.values())[0] if self.color_schemes else {})

        colors = {
            "primary": scheme.get("Primary", "#1E40AF"),
            "secondary": scheme.get("Secondary", "#3B82F6"),
            "accent": scheme.get("Accent", "#F59E0B"),
            "background": scheme.get("Background", "#F8FAFC"),
            "text": scheme.get("Text", "#1E293B"),
            "border": scheme.get("Border", "#E2E8F0")
        }

        # Typography (could be extended with typography.csv)
        typography = {
            "heading": "Inter",
            "body": "Inter"
        }

        return Design(
            colors=colors,
            typography=typography,
            style_name=style
        )


class ReportGenerator:
    """Main report generation orchestrator."""

    def __init__(self):
        self.analyzer = DataAnalyzer()
        self.selector = ComponentSelector()
        self.planner = LayoutPlanner()
        self.design_selector = DesignSelector()

        if jinja2:
            self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
                autoescape=jinja2.select_autoescape(['html', 'xml'])
            )
            self._setup_filters()
        else:
            self.env = None

    def _setup_filters(self):
        """Add custom Jinja2 filters."""
        def format_number(value):
            if isinstance(value, (int, float)):
                if value >= 1_000_000:
                    return f"{value/1_000_000:.1f}M"
                elif value >= 1_000:
                    return f"{value/1_000:.1f}K"
                return f"{value:,.0f}"
            return value

        def to_json(value):
            return json.dumps(value)

        self.env.filters['format_number'] = format_number
        self.env.filters['tojson'] = to_json

    def generate(self,
                 data: dict,
                 title: str,
                 purpose: str = "executive",
                 style: str = "witty",
                 output_format: str = "html") -> str:
        """
        Main entry point for report generation.

        Args:
            data: Input data dictionary
            title: Report title
            purpose: Report purpose (executive, analyst, dashboard, storytelling)
            style: Writing style (witty, formal, storyteller, minimalist)
            output_format: Output format (html, pdf)

        Returns:
            Generated HTML string (or PDF bytes if format is pdf)
        """
        # Step 1: Analyze data
        profile = self.analyzer.analyze(data)

        # Step 2: Select components
        components = self.selector.select(profile, data)

        # Step 3: Plan layout
        layout = self.planner.plan(components, purpose)

        # Step 4: Get design
        design = self.design_selector.select(purpose, style)

        # Step 5: Render HTML
        if self.env:
            html = self._render_jinja(title, layout, design, data)
        else:
            html = self._render_fallback(title, layout, design, components, data)

        # Step 6: Optional PDF export
        if output_format == "pdf":
            return self._export_pdf(html)

        return html

    def _render_jinja(self, title: str, layout: Layout, design: Design, data: dict) -> str:
        """Render using Jinja2 templates."""
        try:
            template = self.env.get_template('base.html.j2')
            return template.render(
                title=title,
                layout=layout,
                colors=design.colors,
                typography=design.typography,
                style=design.style_name,
                data=data,
                chart_configs=self._generate_chart_configs(layout)
            )
        except jinja2.TemplateNotFound:
            return self._render_fallback(title, layout, design, [], data)

    def _render_fallback(self, title: str, layout: Layout, design: Design,
                         components: list[Component], data: dict) -> str:
        """Fallback HTML generation without Jinja2 templates."""
        colors = design.colors

        # Build chart scripts
        chart_scripts = self._generate_chart_scripts(layout, data)

        # Build component HTML
        sections_html = self._render_sections(layout, data, design)

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --color-primary: {colors["primary"]};
            --color-secondary: {colors["secondary"]};
            --color-accent: {colors["accent"]};
            --color-background: {colors["background"]};
            --color-text: {colors["text"]};
            --color-border: {colors["border"]};
        }}
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
</head>
<body class="bg-[var(--color-background)] text-[var(--color-text)] min-h-screen">
    <header class="bg-white border-b border-[var(--color-border)]">
        <div class="max-w-7xl mx-auto px-6 py-8">
            <h1 class="text-3xl font-bold text-[var(--color-primary)]">{title}</h1>
            <p class="text-sm text-gray-500 mt-2">Generated Report • {layout.pattern}</p>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
        {sections_html}
    </main>

    <footer class="bg-white border-t border-[var(--color-border)] mt-12">
        <div class="max-w-7xl mx-auto px-6 py-4 text-center text-sm text-gray-500">
            Generated by Flexible Report Generator
        </div>
    </footer>

    <script>
    {chart_scripts}
    </script>
</body>
</html>'''

        return html

    def _render_sections(self, layout: Layout, data: dict, design: Design) -> str:
        """Render all sections."""
        sections_html = []

        for section in layout.sections:
            section_title = f'<h2 class="text-xl font-semibold mb-6 text-[var(--color-text)]">{section["title"]}</h2>' if section.get("title") else ""

            components_html = []
            for comp in section.get("components", []):
                comp_html = self._render_component(comp, data, design)
                components_html.append(comp_html)

            grid_classes = section.get("grid_classes", "grid-cols-1")
            section_html = f'''
        <section class="mb-12">
            {section_title}
            <div class="grid {grid_classes} gap-6">
                {"".join(components_html)}
            </div>
        </section>'''
            sections_html.append(section_html)

        return "".join(sections_html)

    def _render_component(self, comp: Component, data: dict, design: Design) -> str:
        """Render a single component."""
        colors = design.colors
        comp_data = comp.data

        if comp.type == "HeroMetric":
            value = comp_data.get("value", 0)
            delta = comp_data.get("delta", 0)
            label = comp_data.get("label", "")
            unit = comp_data.get("unit", "")

            delta_color = "text-green-600" if delta >= 0 else "text-red-600"
            delta_sign = "+" if delta >= 0 else ""

            formatted_value = self._format_number(value)

            return f'''
                <div class="bg-white rounded-2xl p-6 shadow-lg {comp.grid_span}">
                    <div class="flex items-baseline gap-2 mb-2">
                        <span class="text-4xl font-bold text-[var(--color-primary)]">{unit}{formatted_value}</span>
                    </div>
                    <div class="text-lg text-gray-600 mb-3">{label}</div>
                    <div class="flex items-center gap-2 text-sm">
                        <span class="{delta_color} font-medium">{delta_sign}{delta}%</span>
                        <span class="text-gray-400">vs previous period</span>
                    </div>
                </div>'''

        elif comp.type == "TrendIndicator":
            value = comp_data.get("value", 0)
            delta = comp_data.get("delta", 0)
            label = comp_data.get("label", "")
            unit = comp_data.get("unit", "")

            delta_color = "text-green-600" if delta >= 0 else "text-red-600"
            delta_sign = "+" if delta >= 0 else ""
            arrow = "↑" if delta >= 0 else "↓"

            formatted_value = self._format_number(value)

            return f'''
                <div class="bg-white rounded-xl p-4 shadow">
                    <div class="text-2xl font-bold text-[var(--color-text)]">{unit}{formatted_value}</div>
                    <div class="text-sm text-gray-500">{label}</div>
                    <div class="{delta_color} text-sm font-medium mt-1">{arrow} {delta_sign}{delta}%</div>
                </div>'''

        elif comp.type == "InsightCard":
            headline = comp_data.get("headline", "")
            body = comp_data.get("body", "")
            source = comp_data.get("source", "")

            source_html = f'<p class="text-xs text-gray-400 mt-3">Source: {source}</p>' if source else ""

            return f'''
                <div class="bg-gradient-to-br from-[var(--color-primary)]/5 to-transparent rounded-2xl p-6 border border-[var(--color-primary)]/10">
                    <div class="flex items-start gap-4">
                        <div class="w-10 h-10 rounded-full bg-[var(--color-accent)]/20 flex items-center justify-center flex-shrink-0">
                            <svg class="w-5 h-5 text-[var(--color-accent)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                            </svg>
                        </div>
                        <div>
                            <h4 class="font-semibold text-lg mb-2">{headline}</h4>
                            <p class="text-gray-600">{body}</p>
                            {source_html}
                        </div>
                    </div>
                </div>'''

        elif comp.type in ["LineChart", "BarChart"]:
            chart_id = comp_data.get("id", "chart")
            title = comp_data.get("title", "")
            height = comp_data.get("height", 300)

            return f'''
                <div class="bg-white rounded-2xl p-6 shadow-lg {comp.grid_span}">
                    <h3 class="text-lg font-semibold mb-4">{title}</h3>
                    <div class="relative" style="height: {height}px;">
                        <canvas id="{chart_id}"></canvas>
                    </div>
                </div>'''

        elif comp.type == "DataTable":
            title = comp_data.get("title", "Data")
            columns = comp_data.get("columns", [])
            rows = comp_data.get("rows", [])

            header_html = "".join([f'<th class="px-4 py-3 text-left text-sm font-semibold text-gray-700 bg-gray-50">{col}</th>' for col in columns])

            rows_html = ""
            for row in rows:
                cells = "".join([f'<td class="px-4 py-3 text-sm text-gray-600">{cell}</td>' for cell in row])
                rows_html += f'<tr class="border-b border-gray-100 hover:bg-gray-50">{cells}</tr>'

            return f'''
                <div class="bg-white rounded-2xl shadow-lg overflow-hidden {comp.grid_span}">
                    <div class="px-6 py-4 border-b border-gray-100">
                        <h3 class="text-lg font-semibold">{title}</h3>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead><tr>{header_html}</tr></thead>
                            <tbody>{rows_html}</tbody>
                        </table>
                    </div>
                </div>'''

        return f'<!-- Unknown component: {comp.type} -->'

    def _generate_chart_scripts(self, layout: Layout, data: dict) -> str:
        """Generate Chart.js initialization scripts."""
        scripts = []

        for section in layout.sections:
            for comp in section.get("components", []):
                if comp.type in ["LineChart", "BarChart"]:
                    chart_id = comp.data.get("id", "chart")
                    chart_type = comp.data.get("chart_type", "line")
                    labels = json.dumps(comp.data.get("labels", []))

                    # Build datasets
                    datasets = comp.data.get("datasets", [])
                    datasets_config = []
                    colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]

                    for i, ds in enumerate(datasets):
                        color = colors[i % len(colors)]
                        ds_config = {
                            "label": ds.get("label", f"Dataset {i+1}"),
                            "data": ds.get("data", []),
                            "borderColor": color,
                            "backgroundColor": f"{color}20" if chart_type == "line" else color,
                            "tension": 0.3,
                            "fill": chart_type == "line"
                        }
                        datasets_config.append(ds_config)

                    script = f'''
new Chart(document.getElementById('{chart_id}'), {{
    type: '{chart_type}',
    data: {{
        labels: {labels},
        datasets: {json.dumps(datasets_config)}
    }},
    options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
            legend: {{ position: 'bottom' }}
        }},
        scales: {{
            y: {{ beginAtZero: true }}
        }}
    }}
}});'''
                    scripts.append(script)

        return "\n".join(scripts)

    def _generate_chart_configs(self, layout: Layout) -> dict:
        """Generate chart configurations for Jinja2 templates."""
        configs = {}
        for section in layout.sections:
            for comp in section.get("components", []):
                if comp.type in ["LineChart", "BarChart", "DonutChart"]:
                    configs[comp.data.get("id", "chart")] = {
                        "type": comp.data.get("chart_type", "line"),
                        "data": {
                            "labels": comp.data.get("labels", []),
                            "datasets": comp.data.get("datasets", [])
                        }
                    }
        return configs

    def _format_number(self, value: Any) -> str:
        """Format numbers with K/M suffixes."""
        if isinstance(value, (int, float)):
            if value >= 1_000_000:
                return f"{value/1_000_000:.1f}M"
            elif value >= 1_000:
                return f"{value/1_000:.1f}K"
            return f"{value:,.0f}"
        return str(value)

    def _export_pdf(self, html: str) -> bytes:
        """Export HTML to PDF using Playwright."""
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.set_content(html, wait_until='networkidle')
                pdf = page.pdf(format='A4', print_background=True)
                browser.close()

            return pdf
        except ImportError:
            raise RuntimeError("PDF export requires playwright. Install with: pip install playwright && playwright install chromium")


if __name__ == "__main__":
    # Simple test
    test_data = {
        "metrics": {
            "revenue": {"value": 1500000, "delta": 23, "label": "Total Revenue", "unit": "$"},
            "users": {"value": 50000, "delta": 15, "label": "Active Users"},
            "conversion": {"value": 3.2, "delta": -2, "label": "Conversion Rate", "unit": "%"}
        },
        "time_series": {
            "title": "Revenue Trend",
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "datasets": [
                {"label": "2024", "data": [100, 120, 140, 180, 200, 250]},
                {"label": "2023", "data": [80, 90, 100, 120, 140, 160]}
            ]
        },
        "insights": [
            {"headline": "Strong Q2 Growth", "body": "Revenue increased 23% compared to last quarter, driven by enterprise segment expansion."},
            {"headline": "User Retention Improved", "body": "Monthly active users grew 15% with improved onboarding flow."}
        ],
        "table": {
            "title": "Product Performance",
            "columns": ["Product", "Revenue", "Growth", "Status"],
            "rows": [
                ["Enterprise Plan", "$800K", "+32%", "Growing"],
                ["Pro Plan", "$500K", "+18%", "Stable"],
                ["Basic Plan", "$200K", "+5%", "Mature"]
            ]
        }
    }

    generator = ReportGenerator()
    html = generator.generate(
        data=test_data,
        title="Q2 2024 Performance Report",
        purpose="executive",
        style="witty"
    )

    print(f"Generated HTML: {len(html)} bytes")

    # Save to file
    output_path = SKILL_DIR / "demo_report.html"
    with open(output_path, "w") as f:
        f.write(html)
    print(f"Saved to: {output_path}")
