#!/usr/bin/env python3
"""
Backtest Runner for Finter Alpha Strategies

Automates backtesting of alpha strategies with comprehensive result reporting.
Generates CSV results and performance chart PNG.

Usage:
    python backtest_runner.py --code alpha.py --universe kr_stock
    python backtest_runner.py --code alpha.py --universe kr_stock --no-validate
    python backtest_runner.py --code alpha.py --universe us_stock --start 20200101

Output files:
    backtest_summary.csv  - NAV time series
    backtest_stats.csv    - Performance metrics
    chart.png             - Performance chart (unless --no-chart)
"""

import argparse
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
    from finter.backtest import Simulator
except ImportError as e:
    print(f"Error: Required package not found - {e}")
    print("Please install: pip install finter pandas numpy")
    sys.exit(1)


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def load_alpha_from_file(filepath):
    """
    Load Alpha class from Python file.

    Parameters
    ----------
    filepath : str or Path
        Path to Python file containing Alpha class

    Returns
    -------
    class
        Alpha class from the file
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Alpha file not found: {filepath}")

    # Load module from file
    spec = importlib.util.spec_from_file_location("alpha_module", filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules["alpha_module"] = module
    spec.loader.exec_module(module)

    # Get Alpha class
    if not hasattr(module, "Alpha"):
        raise ValueError(f"File must contain a class named 'Alpha': {filepath}")

    return module.Alpha


def print_section(title):
    """Print formatted section header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print("=" * 70)


def print_metrics(stats, title="Performance Metrics"):
    """Print formatted performance metrics"""
    print_section(title)

    # Key metrics
    key_metrics = [
        "Total Return (%)",
        "Sharpe Ratio",
        "Max Drawdown (%)",
        "Hit Ratio (%)",
    ]

    for metric in key_metrics:
        if metric in stats:
            value = stats[metric]
            print(f"  {metric:.<50} {value:>12.2f}")

    # Additional metrics
    print("\n  Additional Metrics:")
    other_metrics = [k for k in stats.index if k not in key_metrics]
    for metric in sorted(other_metrics):
        value = stats[metric]
        if isinstance(value, (int, float, np.number)):
            print(f"    {metric:.<48} {value:>12.2f}")


def print_turnover_analysis(summary, title="Turnover & Cost Analysis"):
    """Print turnover and cost analysis from backtest summary"""
    print_section(title)

    # Calculate turnover metrics
    # target_turnover is already a ratio (1.0 = 100% of AUM)
    avg_daily_turnover = summary['target_turnover'].mean()
    annual_turnover = avg_daily_turnover * 252  # Annualized turnover ratio

    # Calculate cost metrics
    avg_aum = summary['aum'].mean()
    total_cost = summary['cost'].sum()
    total_slippage = summary['slippage'].sum()
    total_trading_cost = total_cost + total_slippage
    cost_drag = (total_trading_cost / avg_aum) * 100 if avg_aum > 0 else 0

    print(f"  {'Annual Turnover':.<50} {annual_turnover:>12.1%}")
    print(f"  {'Total Trading Cost':.<50} {total_trading_cost:>12,.0f}")
    print(f"    {'- Fee & Tax':.<48} {total_cost:>12,.0f}")
    print(f"    {'- Slippage':.<48} {total_slippage:>12,.0f}")
    print(f"  {'Cost Drag (% of AUM)':.<50} {cost_drag:>12.2f}%")

    # Return for saving to CSV
    return {
        'Annual Turnover (%)': annual_turnover * 100,  # Store as percentage
        'Total Trading Cost': total_trading_cost,
        'Fee & Tax': total_cost,
        'Slippage': total_slippage,
        'Cost Drag (%)': cost_drag,
    }


def validate_positions(positions):
    """
    Validate position DataFrame for common issues.

    Parameters
    ----------
    positions : pd.DataFrame
        Position DataFrame to validate

    Returns
    -------
    dict
        Validation results with warnings and errors
    """
    issues = {"errors": [], "warnings": []}

    # Check for empty DataFrame
    if positions.empty:
        issues["errors"].append("Position DataFrame is empty")
        return issues

    # Check row sums
    row_sums = positions.sum(axis=1)
    max_sum = row_sums.max()

    if max_sum > 1e8 + 1000:  # Allow small rounding error
        issues["errors"].append(f"Row sums exceed 1e8 (total AUM). Max: {max_sum:.0f}")

    # Check for NaN values
    nan_count = positions.isnull().sum().sum()
    if nan_count > 0:
        nan_pct = nan_count / positions.size * 100
        issues["warnings"].append(
            f"Contains {nan_count} NaN values ({nan_pct:.2f}% of total)"
        )

    # Check for all-NaN rows (will cause "All NaN detected" error on Finter submit)
    all_nan_rows = positions.isna().all(axis=1)
    if all_nan_rows.any():
        nan_row_count = all_nan_rows.sum()
        first_dates = positions.index[all_nan_rows].tolist()[:3]
        issues["errors"].append(
            f"Found {nan_row_count} rows where ALL values are NaN. "
            f"Use fillna(0) for cash positions. First dates: {first_dates}"
        )

    # Check for zero positions
    zero_positions = (row_sums == 0).sum()
    if zero_positions > 0:
        zero_pct = zero_positions / len(positions) * 100
        issues["warnings"].append(
            f"{zero_positions} days with zero positions ({zero_pct:.1f}% of days)"
        )

    # Check for negative values
    if (positions < 0).any().any():
        issues["warnings"].append("Contains negative positions (short positions)")

    return issues


# ============================================================
# MAIN BACKTEST WORKFLOW
# ============================================================


def run_backtest(
    alpha_file, start_date, end_date, universe, output_dir=None, generate_chart=True
):
    """
    Run complete backtest workflow.

    Validation runs BEFORE backtest - files are only generated if validation passes.

    Parameters
    ----------
    alpha_file : str
        Path to alpha strategy file
    start_date : int
        Start date in YYYYMMDD format
    end_date : int
        End date in YYYYMMDD format
    universe : str
        Market universe ("kr_stock", "us_stock", etc.)
    output_dir : str or Path, optional
        Output directory for results (default: current working directory)
    generate_chart : bool
        Whether to generate chart PNG (default: True)

    Returns
    -------
    bool
        True if backtest completed successfully, False otherwise
    """
    print_section("Backtest Configuration")
    print(f"  Alpha file: {alpha_file}")
    print(f"  Date range: {start_date} - {end_date}")
    print(f"  Universe: {universe}")

    # Load Alpha class
    print_section("Loading Alpha Strategy")
    try:
        AlphaClass = load_alpha_from_file(alpha_file)
        print("  ✓ Successfully loaded Alpha class")

        if AlphaClass.__doc__:
            print("\n  Strategy Description:")
            for line in AlphaClass.__doc__.strip().split("\n"):
                print(f"    {line}")
    except Exception as e:
        print(f"  ✗ Error loading Alpha class: {e}")
        return False

    # Generate positions
    print_section("Generating Positions")
    try:
        alpha = AlphaClass()
        positions = alpha.get(start_date, end_date)

        print("  ✓ Positions generated successfully")
        print(f"  Shape: {positions.shape}")
        print(f"  Date range: {positions.index[0]} to {positions.index[-1]}")
        print(f"  Trading days: {len(positions)}")
        print(f"  Number of stocks: {positions.shape[1]}")
    except Exception as e:
        print(f"  ✗ Error generating positions: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Validate positions
    print_section("Position Validation")
    validation = validate_positions(positions)

    if validation["errors"]:
        print("  ✗ ERRORS FOUND:")
        for error in validation["errors"]:
            print(f"    - {error}")
        return False
    else:
        print("  ✓ No errors found")

    if validation["warnings"]:
        print("\n  ⚠️  WARNINGS:")
        for warning in validation["warnings"]:
            print(f"    - {warning}")

    # Show position statistics
    row_sums = positions.sum(axis=1)
    print("\n  Position Statistics:")
    print(
        f"    Row sum - Min: {row_sums.min():.0f}, "
        f"Max: {row_sums.max():.0f}, "
        f"Mean: {row_sums.mean():.0f}"
    )

    avg_stocks_per_day = (positions > 0).sum(axis=1).mean()
    print(f"    Average stocks per day: {avg_stocks_per_day:.1f}")

    # Run alpha validation (class name, path independence, trading days) BEFORE backtest
    print_section("Alpha Validation")
    try:
        from alpha_validator import (
            check_class_name,
            check_path_independence,
            check_trading_days,
            load_alpha_from_file as load_alpha_validator,
        )

        val_universe = universe

        # Check 0: Class Name
        print("\n  0. Class Name")
        passed0, msg0, details0 = check_class_name(alpha_file)
        status0 = "✓ PASS" if passed0 else "✗ FAIL"
        print(f"     {status0} - {msg0}")
        if not passed0 and "wrong_names" in details0:
            print(f"     Fix: rename 'class {details0['wrong_names'][0]}' to 'class Alpha'")

        AlphaClassForValidation = load_alpha_validator(alpha_file)

        # Check 1: Path Independence
        print("\n  1. Path Independence")
        passed1, msg1, _ = check_path_independence(AlphaClassForValidation)
        status1 = "✓ PASS" if passed1 else "✗ FAIL"
        print(f"     {status1} - {msg1}")

        # Check 2: Trading Days
        print("\n  2. Trading Days Index")
        passed2, msg2, _ = check_trading_days(AlphaClassForValidation, val_universe)
        status2 = "✓ PASS" if passed2 else "✗ FAIL"
        print(f"     {status2} - {msg2}")

        if not (passed0 and passed1 and passed2):
            print("\n  ✗ Validation FAILED - fix alpha.py before backtest!")
            print("    No output files generated.")
            return False
        else:
            print("\n  ✓ All validations passed!")

    except ImportError:
        print("  ⚠️  alpha_validator.py not found, skipping validation")
    except Exception as e:
        print(f"  ⚠️  Validation error: {e}")
        print("    Continuing with backtest...")

    # Run backtest
    print_section("Running Backtest")
    try:
        simulator = Simulator(
            market_type=universe,
        )

        result = simulator.run(position=positions)
        print("  ✓ Backtest completed successfully")

    except Exception as e:
        print(f"  ✗ Error running backtest: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Print results
    print_metrics(result.statistics)

    # Print turnover & cost analysis
    turnover_stats = print_turnover_analysis(result.summary)

    # Save results
    print_section("Saving Results")

    # Determine output directory
    out_dir = Path(output_dir) if output_dir else Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save summary (fixed filename, no timestamp)
    summary_file = out_dir / "backtest_summary.csv"
    result.summary.to_csv(summary_file)
    print(f"  ✓ Summary saved: {summary_file}")
    print("    Note: NAV starts at 1000 (initial portfolio value)")

    # Save statistics (including turnover analysis)
    stats_file = out_dir / "backtest_stats.csv"
    # Combine performance stats with turnover stats
    all_stats = result.statistics.copy()
    for key, value in turnover_stats.items():
        all_stats[key] = value
    all_stats.to_csv(stats_file)
    print(f"  ✓ Statistics saved: {stats_file}")

    # Generate chart
    if generate_chart:
        print_section("Generating Chart")
        try:
            from chart_generator import create_performance_chart, load_backtest_data

            nav_series, stats_dict = load_backtest_data(summary_file, stats_file)
            chart_file = out_dir / "chart.png"
            create_performance_chart(
                nav_series=nav_series,
                stats=stats_dict,
                output_path=chart_file,
                size="thumbnail",
                title="Alpha Performance",
            )
            print(f"  ✓ Chart saved: {chart_file}")
        except ImportError:
            print("  ⚠️  chart_generator not found, skipping chart generation")
        except Exception as e:
            print(f"  ⚠️  Chart generation failed: {e}")

    print_section("Backtest Complete")
    print(f"  All results saved to: {out_dir}")

    return True


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description="Backtest Finter alpha strategies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backtest_runner.py --code alpha.py --universe kr_stock
  python backtest_runner.py --code alpha.py --universe kr_stock --no-validate
  python backtest_runner.py --code alpha.py --universe us_stock --start 20200101
  python backtest_runner.py --code alpha.py --universe kr_stock --no-chart
        """,
    )

    parser.add_argument(
        "--code", required=True, help="Path to Python file containing Alpha class"
    )

    parser.add_argument(
        "--start",
        type=int,
        default=20200101,
        help="Start date in YYYYMMDD format (default: 20200101)",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=int(datetime.now(timezone.utc).strftime("%Y%m%d")),
        help="End date in YYYYMMDD format (default: today)",
    )

    parser.add_argument(
        "--universe",
        required=True,
        choices=[
            "kr_stock",
            "us_stock",
            "vn_stock",
            "id_stock",
            "us_etf",
            "crypto_test",
        ],
        help="Market universe (required)",
    )

    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for results (default: current directory)",
    )

    parser.add_argument(
        "--no-chart",
        action="store_true",
        help="Skip chart PNG generation",
    )

    args = parser.parse_args()

    # Run backtest (validation runs BEFORE backtest, files only generated on success)
    success = run_backtest(
        alpha_file=args.code,
        start_date=args.start,
        end_date=args.end,
        universe=args.universe,
        output_dir=args.output_dir,
        generate_chart=not args.no_chart,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
