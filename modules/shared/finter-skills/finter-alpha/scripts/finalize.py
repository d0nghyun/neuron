#!/usr/bin/env python3
"""
Finalize Alpha Strategy - All-in-One Script

Run validation, backtest, generate chart, and create info.json in one command.

Usage:
    python finalize.py --code alpha.py --universe kr_stock --title "My Strategy" --category momentum

    # With custom summary
    python finalize.py --code alpha.py --universe kr_stock --title "RSI Reversal" \
        --category technical --summary "Buy oversold RSI, monthly rebalance"

Output files (all in same directory as alpha.py):
    - backtest_summary.csv
    - backtest_stats.csv
    - chart.png
    - info.json
"""

import argparse
import importlib.util
import json
import random
import re
import string
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONSTANTS
# ============================================================

VALID_CATEGORIES = [
    "momentum", "value", "quality", "growth", "size", "low_vol",
    "technical", "macro", "stat_arb", "event", "ml", "composite",
]

VALID_UNIVERSES = [
    "kr_stock", "us_stock", "us_etf", "vn_stock", "id_stock", "btcusdt_spot_binance",
]


# ============================================================
# ALPHA LOADING & VALIDATION
# ============================================================

def load_alpha_class(filepath: Path):
    """Load Alpha class from Python file."""
    if not filepath.exists():
        raise FileNotFoundError(f"Alpha file not found: {filepath}")

    spec = importlib.util.spec_from_file_location("alpha_module", filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules["alpha_module"] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "Alpha"):
        raise ValueError(f"File must contain a class named 'Alpha': {filepath}")

    return module.Alpha


def check_class_name(filepath: Path) -> tuple[bool, str]:
    """Check if Alpha class is named correctly."""
    import ast

    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return False, f"Syntax error: {e}"

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                base_name = None
                if isinstance(base, ast.Name):
                    base_name = base.id
                elif isinstance(base, ast.Attribute):
                    base_name = base.attr

                if base_name == 'BaseAlpha' and node.name != 'Alpha':
                    return False, f"Class must be named 'Alpha', not '{node.name}'"

    return True, "OK"


def validate_positions(positions: pd.DataFrame) -> dict:
    """Validate position DataFrame."""
    issues = {"errors": [], "warnings": []}

    if positions.empty:
        issues["errors"].append("Position DataFrame is empty")
        return issues

    # Check row sums
    row_sums = positions.sum(axis=1)
    if row_sums.max() > 1e8 + 1000:
        issues["errors"].append(f"Row sums exceed 1e8. Max: {row_sums.max():.0f}")

    # Check for all-NaN rows
    all_nan_rows = positions.isna().all(axis=1)
    if all_nan_rows.any():
        dates = positions.index[all_nan_rows].tolist()[:3]
        issues["errors"].append(
            f"Found {all_nan_rows.sum()} all-NaN rows. Use fillna(0). First: {dates}"
        )

    # Warnings
    nan_count = positions.isnull().sum().sum()
    if nan_count > 0:
        issues["warnings"].append(f"{nan_count} NaN values ({nan_count/positions.size*100:.1f}%)")

    zero_days = (row_sums == 0).sum()
    if zero_days > 0:
        issues["warnings"].append(f"{zero_days} days with zero positions")

    return issues


def check_path_independence(AlphaClass, verbose=False) -> tuple[bool, str]:
    """Check if alpha is path-independent."""
    try:
        alpha = AlphaClass()

        # Two overlapping periods
        pos1 = alpha.get(20200101, 20211231)
        pos2 = alpha.get(20210101, 20221231)

        # Find overlap
        overlap_start = max(pos1.index.min(), pos2.index.min())
        overlap_end = min(pos1.index.max(), pos2.index.max())

        p1 = pos1.loc[overlap_start:overlap_end]
        p2 = pos2.loc[overlap_start:overlap_end]

        # Align
        common_idx = p1.index.intersection(p2.index)
        common_cols = p1.columns.intersection(p2.columns)

        if len(common_idx) == 0:
            return True, "No overlap to check"

        p1 = p1.loc[common_idx, common_cols]
        p2 = p2.loc[common_idx, common_cols]

        # Compare
        diff = (p1.fillna(0) - p2.fillna(0)).abs()
        max_diff = diff.max().max()

        if max_diff > 1e-6:
            return False, f"max_diff={max_diff:.2e}"
        return True, "OK"

    except Exception as e:
        return False, f"Error: {e}"


# ============================================================
# BACKTEST
# ============================================================

def run_backtest(positions: pd.DataFrame, universe: str):
    """Run backtest and return result."""
    from finter.backtest import Simulator

    simulator = Simulator(market_type=universe)
    return simulator.run(position=positions)


def calculate_turnover_stats(summary: pd.DataFrame) -> dict:
    """Calculate turnover and cost statistics."""
    avg_daily_turnover = summary['target_turnover'].mean()
    annual_turnover = avg_daily_turnover * 252

    avg_aum = summary['aum'].mean()
    total_cost = summary['cost'].sum() + summary['slippage'].sum()
    cost_drag = (total_cost / avg_aum) * 100 if avg_aum > 0 else 0

    return {
        'Annual Turnover (%)': annual_turnover * 100,
        'Total Trading Cost': total_cost,
        'Cost Drag (%)': cost_drag,
    }


# ============================================================
# CHART GENERATION
# ============================================================

def create_chart(nav_series: pd.Series, stats: dict, output_path: Path, title: str):
    """Create performance chart PNG."""
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    COLORS = {
        "background": "#1a1a2e",
        "primary": "#e94560",
        "text": "#eaeaea",
        "text_muted": "#8b8b8b",
        "positive": "#00d26a",
        "negative": "#ff4757",
        "grid": "#2a2a4a",
    }

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=COLORS["background"])
    ax.set_facecolor(COLORS["background"])

    # Normalize to percentage return
    returns_pct = (nav_series.values / nav_series.values[0] - 1) * 100

    ax.fill_between(nav_series.index, returns_pct, alpha=0.3, color=COLORS["primary"])
    ax.plot(nav_series.index, returns_pct, color=COLORS["primary"], linewidth=2.5)
    ax.axhline(y=0, color=COLORS["text_muted"], linewidth=0.5, linestyle="--", alpha=0.5)

    # Style
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["grid"])
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.tick_params(colors=COLORS["text_muted"], labelsize=8)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:+.0f}%"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.grid(True, alpha=0.2, color=COLORS["grid"])
    ax.set_title(title, color=COLORS["text"], fontsize=11, fontweight="bold", loc="left", pad=10)

    # Metrics overlay
    total_return = stats.get("Total Return (%)", 0)
    sharpe = stats.get("Sharpe Ratio", 0)
    max_dd = stats.get("Max Drawdown (%)", 0)

    metrics = [
        (0.2, f"{total_return:+.1f}%", "Return", COLORS["positive"] if total_return >= 0 else COLORS["negative"]),
        (0.5, f"{sharpe:.2f}", "Sharpe", COLORS["positive"] if sharpe >= 1 else COLORS["text"]),
        (0.8, f"{max_dd:.1f}%", "MaxDD", COLORS["negative"] if max_dd < -20 else COLORS["text"]),
    ]

    for x, value, label, color in metrics:
        fig.text(x, 0.12, value, ha="center", fontsize=14, fontweight="bold", color=color)
        fig.text(x, 0.04, label, ha="center", fontsize=7, color=COLORS["text_muted"])

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)
    fig.savefig(output_path, dpi=100, facecolor=COLORS["background"], bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


# ============================================================
# INFO GENERATION
# ============================================================

def generate_info(title: str, summary: str, category: str, universe: str) -> dict:
    """Generate info.json content."""
    # Convert title to snake_case
    if not title.isascii():
        raise ValueError(f"Title must be English only: '{title}'")

    base_name = re.sub(r"[-\s]+", "_", title)
    base_name = re.sub(r"[^a-zA-Z0-9_]", "", base_name).lower()
    if len(base_name) > 34:
        base_name = base_name[:34]

    datetime_suffix = datetime.now(timezone.utc).strftime("%y%m%d%H")
    random_suffix = "".join(random.choices(string.ascii_lowercase, k=2))
    model_title = f"{base_name}_{datetime_suffix}{random_suffix}"

    return {
        "model_type": "alpha",
        "model_title": model_title,
        "model_summary": summary,
        "model_category": category,
        "tags": [],
        "universe": universe,
        "investable": False,
        "evaluation": "Backtest completed",
        "lessons": "Implementation completed",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================
# MAIN
# ============================================================

def print_header(title: str):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print("─" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Finalize alpha: validate + backtest + chart + info",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--code", required=True, help="Path to alpha.py")
    parser.add_argument("--universe", required=True, choices=VALID_UNIVERSES)
    parser.add_argument("--title", required=True, help="Strategy title (English, max 34 chars)")
    parser.add_argument("--category", required=True, choices=VALID_CATEGORIES)
    parser.add_argument("--summary", default=None, help="Strategy summary")
    parser.add_argument("--start", type=int, default=20200101)
    parser.add_argument("--end", type=int, default=int(datetime.now(timezone.utc).strftime("%Y%m%d")))
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--no-chart", action="store_true")

    args = parser.parse_args()

    alpha_path = Path(args.code)
    output_dir = Path(args.output_dir) if args.output_dir else alpha_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  FINALIZE ALPHA")
    print("=" * 60)
    print(f"  Code: {alpha_path}")
    print(f"  Universe: {args.universe}")
    print(f"  Period: {args.start} - {args.end}")

    # ─────────────────────────────────────────────────────────
    # STEP 1: Validation
    # ─────────────────────────────────────────────────────────
    print_header("1. Validation")

    # Class name
    passed, msg = check_class_name(alpha_path)
    print(f"  Class name: {'✓' if passed else '✗'} {msg}")
    if not passed:
        sys.exit(1)

    # Load and generate positions
    try:
        AlphaClass = load_alpha_class(alpha_path)
        alpha = AlphaClass()
        positions = alpha.get(args.start, args.end)
        print(f"  Positions: ✓ {positions.shape[0]} days, {positions.shape[1]} stocks")
    except Exception as e:
        print(f"  Positions: ✗ {e}")
        sys.exit(1)

    # Position validation
    validation = validate_positions(positions)
    if validation["errors"]:
        for err in validation["errors"]:
            print(f"  ✗ {err}")
        sys.exit(1)
    for warn in validation["warnings"]:
        print(f"  ⚠ {warn}")

    # Path independence
    passed, msg = check_path_independence(AlphaClass)
    print(f"  Path independence: {'✓' if passed else '✗'} {msg}")
    if not passed:
        print("  Fix: Use pct_change(N, fill_method=None)")
        sys.exit(1)

    # ─────────────────────────────────────────────────────────
    # STEP 2: Backtest
    # ─────────────────────────────────────────────────────────
    print_header("2. Backtest")

    try:
        result = run_backtest(positions, args.universe)
        stats = result.statistics
        turnover_stats = calculate_turnover_stats(result.summary)

        print(f"  Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
        print(f"  Total Return: {stats['Total Return (%)']:.1f}%")
        print(f"  Max Drawdown: {stats['Max Drawdown (%)']:.1f}%")
        print(f"  Annual Turnover: {turnover_stats['Annual Turnover (%)']:.0f}%")
    except Exception as e:
        print(f"  ✗ Backtest failed: {e}")
        sys.exit(1)

    # Save backtest results
    summary_path = output_dir / "backtest_summary.csv"
    stats_path = output_dir / "backtest_stats.csv"

    result.summary.to_csv(summary_path)
    all_stats = stats.copy()
    for k, v in turnover_stats.items():
        all_stats[k] = v
    all_stats.to_csv(stats_path)

    print(f"  Saved: {summary_path.name}, {stats_path.name}")

    # ─────────────────────────────────────────────────────────
    # STEP 3: Chart
    # ─────────────────────────────────────────────────────────
    if not args.no_chart:
        print_header("3. Chart")
        try:
            chart_path = output_dir / "chart.png"
            create_chart(result.summary['nav'], dict(stats), chart_path, args.title)
            print(f"  Saved: {chart_path.name}")
        except Exception as e:
            print(f"  ⚠ Chart failed: {e}")

    # ─────────────────────────────────────────────────────────
    # STEP 4: Info
    # ─────────────────────────────────────────────────────────
    print_header("4. Info")

    summary_text = args.summary or f"{args.title} strategy for {args.universe}"
    try:
        info = generate_info(args.title, summary_text, args.category, args.universe)
        info_path = output_dir / "info.json"
        info_path.write_text(json.dumps(info, ensure_ascii=False, indent=2))
        print(f"  model_title: {info['model_title']}")
        print(f"  Saved: {info_path.name}")
    except Exception as e:
        print(f"  ✗ Info failed: {e}")
        sys.exit(1)

    # ─────────────────────────────────────────────────────────
    # Done
    # ─────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("  ✅ FINALIZE COMPLETE")
    print("=" * 60)
    print(f"  Output: {output_dir}")
    print()


if __name__ == "__main__":
    main()
