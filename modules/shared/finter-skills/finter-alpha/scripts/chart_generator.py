#!/usr/bin/env python3
"""
Chart Generator for Finter Alpha Strategies

Generates visually appealing PNG charts for alpha backtest results.
Designed for thumbnail/preview usage with dark theme styling.

Usage:
    python chart_generator.py --summary backtest_summary.csv --stats backtest_stats.csv
    python chart_generator.py --summary backtest_summary.csv --stats backtest_stats.csv --output chart.png
    python chart_generator.py --summary backtest_summary.csv --stats backtest_stats.csv --size thumbnail
"""

import argparse
import sys
from pathlib import Path

try:
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from matplotlib.patches import FancyBboxPatch
except ImportError as e:
    print(f"Error: Required package not found - {e}")
    print("Please install: pip install matplotlib pandas numpy")
    sys.exit(1)


# ============================================================
# STYLE CONFIGURATION (chat-agent2 inspired dark theme)
# ============================================================

COLORS = {
    "background": "#1a1a2e",  # Deep dark blue-gray
    "card": "#16213e",  # Slightly lighter card bg
    "primary": "#e94560",  # Vibrant red-pink (main line)
    "primary_light": "#ff6b6b",  # Lighter variant
    "secondary": "#0f3460",  # Dark blue
    "text": "#eaeaea",  # Light text
    "text_muted": "#8b8b8b",  # Muted text
    "positive": "#00d26a",  # Green for positive
    "negative": "#ff4757",  # Red for negative
    "grid": "#2a2a4a",  # Subtle grid
}

SIZES = {
    "thumbnail": (6, 4),  # 600x400 at 100 dpi
    "full": (12, 8),  # 1200x800 at 100 dpi
}


# ============================================================
# CHART GENERATION
# ============================================================


def create_performance_chart(
    nav_series: pd.Series,
    stats: dict,
    output_path: Path,
    size: str = "thumbnail",
    title: str = "Alpha Performance",
) -> Path:
    """
    Create a visually appealing performance chart.

    Parameters
    ----------
    nav_series : pd.Series
        NAV time series with datetime index
    stats : dict
        Performance statistics dict with keys like 'Total Return (%)', 'Sharpe Ratio', etc.
    output_path : Path
        Output file path for PNG
    size : str
        Chart size: 'thumbnail' (600x400) or 'full' (1200x800)
    title : str
        Chart title

    Returns
    -------
    Path
        Path to generated PNG file
    """
    figsize = SIZES.get(size, SIZES["thumbnail"])

    # Create figure with dark background
    fig, ax = plt.subplots(figsize=figsize, facecolor=COLORS["background"])
    ax.set_facecolor(COLORS["background"])

    # Prepare data
    dates = nav_series.index
    values = nav_series.values

    # Normalize to percentage return from start
    start_value = values[0]
    returns_pct = (values / start_value - 1) * 100

    # Create gradient fill under the line
    ax.fill_between(
        dates,
        returns_pct,
        alpha=0.3,
        color=COLORS["primary"],
        linewidth=0,
    )

    # Plot main line
    ax.plot(
        dates,
        returns_pct,
        color=COLORS["primary"],
        linewidth=2.5,
        solid_capstyle="round",
    )

    # Add zero line
    ax.axhline(
        y=0, color=COLORS["text_muted"], linewidth=0.5, linestyle="--", alpha=0.5
    )

    # Style axes
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["grid"])
    ax.spines["bottom"].set_color(COLORS["grid"])

    ax.tick_params(colors=COLORS["text_muted"], labelsize=8)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:+.0f}%"))

    # Date formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator())

    # Grid
    ax.grid(True, alpha=0.2, color=COLORS["grid"], linestyle="-", linewidth=0.5)
    ax.set_axisbelow(True)

    # Title
    ax.set_title(
        title,
        color=COLORS["text"],
        fontsize=14 if size == "full" else 11,
        fontweight="bold",
        loc="left",
        pad=10,
    )

    # Add performance metrics box
    _add_metrics_overlay(fig, ax, stats, size)

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2 if size == "thumbnail" else 0.15)

    # Save with transparent background option
    output_path = Path(output_path)
    fig.savefig(
        output_path,
        dpi=100,
        facecolor=COLORS["background"],
        edgecolor="none",
        bbox_inches="tight",
        pad_inches=0.1,
    )
    plt.close(fig)

    return output_path


def _add_metrics_overlay(fig, ax, stats: dict, size: str):
    """Add performance metrics overlay at the bottom of the chart."""

    # Get metrics
    total_return = stats.get("Total Return (%)", 0)
    sharpe = stats.get("Sharpe Ratio", 0)
    max_dd = stats.get("Max Drawdown (%)", 0)

    # Determine colors based on values
    return_color = COLORS["positive"] if total_return >= 0 else COLORS["negative"]
    sharpe_color = (
        COLORS["positive"]
        if sharpe >= 1.0
        else (COLORS["text"] if sharpe >= 0 else COLORS["negative"])
    )
    dd_color = (
        COLORS["negative"]
        if max_dd < -20
        else (COLORS["text"] if max_dd < -10 else COLORS["positive"])
    )

    # Font sizes based on chart size
    if size == "thumbnail":
        value_size, label_size = 14, 7
        y_pos = 0.08
    else:
        value_size, label_size = 18, 9
        y_pos = 0.06

    # Create metrics text
    metrics = [
        (0.2, f"{total_return:+.1f}%", "Return", return_color),
        (0.5, f"{sharpe:.2f}", "Sharpe", sharpe_color),
        (0.8, f"{max_dd:.1f}%", "MaxDD", dd_color),
    ]

    for x_pos, value, label, color in metrics:
        # Value
        fig.text(
            x_pos,
            y_pos + 0.04,
            value,
            ha="center",
            va="center",
            fontsize=value_size,
            fontweight="bold",
            color=color,
            transform=fig.transFigure,
        )
        # Label
        fig.text(
            x_pos,
            y_pos - 0.02,
            label,
            ha="center",
            va="center",
            fontsize=label_size,
            color=COLORS["text_muted"],
            transform=fig.transFigure,
        )


def load_backtest_data(summary_path: Path, stats_path: Path) -> tuple[pd.Series, dict]:
    """
    Load backtest results from CSV files.

    Parameters
    ----------
    summary_path : Path
        Path to backtest_summary CSV (contains 'nav' column)
    stats_path : Path
        Path to backtest_stats CSV (contains performance metrics)

    Returns
    -------
    tuple[pd.Series, dict]
        NAV series and stats dictionary
    """
    # Load summary
    summary_df = pd.read_csv(summary_path, index_col=0, parse_dates=True)

    if "nav" not in summary_df.columns:
        raise ValueError(
            f"Summary file must contain 'nav' column. Found: {summary_df.columns.tolist()}"
        )

    nav_series = summary_df["nav"]

    # Load stats
    stats_df = pd.read_csv(stats_path, index_col=0, header=None)
    stats = stats_df[1].to_dict()

    # Convert numeric strings to float
    for key in stats:
        try:
            stats[key] = float(stats[key])
        except (ValueError, TypeError):
            pass

    return nav_series, stats


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description="Generate performance chart PNG from backtest results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python chart_generator.py --summary backtest_summary.csv --stats backtest_stats.csv
  python chart_generator.py --summary summary.csv --stats stats.csv --output my_chart.png
  python chart_generator.py --summary summary.csv --stats stats.csv --size full
        """,
    )

    parser.add_argument(
        "--summary",
        required=True,
        help="Path to backtest_summary CSV file (must contain 'nav' column)",
    )

    parser.add_argument(
        "--stats",
        required=True,
        help="Path to backtest_stats CSV file",
    )

    parser.add_argument(
        "--output",
        default="chart.png",
        help="Output PNG file path (default: chart.png)",
    )

    parser.add_argument(
        "--size",
        choices=["thumbnail", "full"],
        default="thumbnail",
        help="Chart size: thumbnail (600x400) or full (1200x800)",
    )

    parser.add_argument(
        "--title",
        default="Alpha Performance",
        help="Chart title (default: 'Alpha Performance')",
    )

    args = parser.parse_args()

    # Validate paths
    summary_path = Path(args.summary)
    stats_path = Path(args.stats)

    if not summary_path.exists():
        print(f"Error: Summary file not found: {summary_path}")
        sys.exit(1)

    if not stats_path.exists():
        print(f"Error: Stats file not found: {stats_path}")
        sys.exit(1)

    # Load data
    print("Loading backtest data...")
    try:
        nav_series, stats = load_backtest_data(summary_path, stats_path)
        print(f"  NAV data: {len(nav_series)} days")
        print(f"  Stats: {len(stats)} metrics")
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    # Generate chart
    print(f"Generating {args.size} chart...")
    try:
        output_path = create_performance_chart(
            nav_series=nav_series,
            stats=stats,
            output_path=Path(args.output),
            size=args.size,
            title=args.title,
        )
        print(f"  Chart saved: {output_path}")
    except Exception as e:
        print(f"Error generating chart: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    print("Done!")


if __name__ == "__main__":
    main()
