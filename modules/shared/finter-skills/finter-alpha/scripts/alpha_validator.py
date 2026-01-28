#!/usr/bin/env python3
"""
Alpha Strategy Validator for Finter

Validates alpha strategies for common issues:
1. Path Independence - positions must be identical for overlapping dates
2. Trading Days Index - positions must align with universe trading days

Usage:
    python alpha_validator.py --code alpha.py --universe kr_stock
    python alpha_validator.py --code alpha.py --universe us_stock --verbose
"""

import argparse
import importlib.util
import sys
from pathlib import Path

import pandas as pd
from finter.data import ContentFactory


def load_alpha_from_file(filepath):
    """Load Alpha class from Python file."""
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Alpha file not found: {filepath}")

    spec = importlib.util.spec_from_file_location("alpha_module", filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules["alpha_module"] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "Alpha"):
        raise ValueError(f"File must contain a class named 'Alpha': {filepath}")

    return module.Alpha


# ============================================================
# CHECK 0: Class Name (run before loading)
# ============================================================

def check_class_name(filepath, verbose=False):
    """Check if the Alpha class is named correctly (must be 'Alpha', not 'MyAlpha', etc.)."""
    import ast

    filepath = Path(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return False, f"Syntax error: {e}", {}

    base_alpha_classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check if this class inherits from BaseAlpha
            for base in node.bases:
                base_name = None
                if isinstance(base, ast.Name):
                    base_name = base.id
                elif isinstance(base, ast.Attribute):
                    base_name = base.attr

                if base_name == 'BaseAlpha':
                    base_alpha_classes.append(node.name)

    if not base_alpha_classes:
        return True, "No BaseAlpha subclass found (skipped)", {}

    # Check if any BaseAlpha subclass is NOT named "Alpha"
    wrong_names = [name for name in base_alpha_classes if name != 'Alpha']

    if wrong_names:
        return False, f"Class must be named 'Alpha', not '{wrong_names[0]}'", {
            "wrong_names": wrong_names
        }

    return True, "OK", {"class_names": base_alpha_classes}


def print_header(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print("─" * 60)


# ============================================================
# CHECK 1: Path Independence
# ============================================================

def check_path_independence(AlphaClass, verbose=False):
    """Check if positions are identical for overlapping dates."""
    range1 = (20200101, 20211231)
    range2 = (20210101, 20221231)
    overlap_start, overlap_end = "20210101", "20211231"

    print(f"    Range 1: {range1[0]} - {range1[1]}")
    print(f"    Range 2: {range2[0]} - {range2[1]}")

    alpha = AlphaClass()
    pos1 = alpha.get(*range1)
    pos2 = alpha.get(*range2)

    # Align to overlap
    pos1_overlap = pos1.loc[overlap_start:overlap_end]
    pos2_overlap = pos2.loc[overlap_start:overlap_end]

    common_cols = pos1_overlap.columns.intersection(pos2_overlap.columns)
    common_idx = pos1_overlap.index.intersection(pos2_overlap.index)

    # Exclude last few rows (boundary effects from shift)
    if len(common_idx) > 5:
        common_idx = common_idx[:-3]

    pos1_aligned = pos1_overlap.loc[common_idx, common_cols]
    pos2_aligned = pos2_overlap.loc[common_idx, common_cols]

    if len(common_idx) == 0:
        return False, "No overlapping dates", {}

    diff = (pos1_aligned - pos2_aligned).abs()
    max_diff = diff.max().max()

    passed = max_diff < 1e-6
    details = {
        "overlap_days": len(common_idx),
        "max_diff": max_diff,
    }

    if not passed and verbose:
        diff_mask = diff > 1e-6
        details["affected_pct"] = diff_mask.sum().sum() / diff.size * 100

    return passed, f"max_diff={max_diff:.2e}", details


# ============================================================
# CHECK 2: Trading Days Index
# ============================================================

def check_trading_days(AlphaClass, universe, verbose=False):
    """Check if position index matches trading days."""
    # Skip for crypto universe - 8H candles, no trading_days
    if universe == "crypto_test":
        print("    Skipped for crypto_test (crypto uses 8H candles)")
        return True, "skipped (crypto)", {}

    start, end = 20230101, 20231231

    print(f"    Universe: {universe}, Range: {start} - {end}")

    cf = ContentFactory(universe, start, end)
    # Normalize trading_days to YYYYMMDD int
    trading_days = set(int(d.strftime('%Y%m%d')) for d in cf.trading_days)

    alpha = AlphaClass()
    positions = alpha.get(start, end)

    # Normalize position index to YYYYMMDD int
    pos_index = positions.index
    if hasattr(pos_index, 'strftime'):
        pos_dates = set(int(d) for d in pos_index.strftime('%Y%m%d'))
    else:
        pos_dates = set(int(str(d).replace('-', '')[:8]) for d in pos_index)

    extra_days = pos_dates - trading_days

    passed = len(extra_days) == 0
    details = {
        "trading_days": len(trading_days),
        "position_days": len(pos_dates),
        "invalid_days": len(extra_days),
    }

    if not passed and verbose:
        details["invalid_samples"] = sorted(extra_days)[:5]

    return passed, f"invalid={len(extra_days)}", details


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Validate alpha strategy for common issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Checks performed:
  0. Class Name - class must be named 'Alpha', not 'MyAlpha' etc.
  1. Path Independence - get() with different end dates must return
     identical values for overlapping periods
  2. Trading Days - position index must match universe trading days

Common fixes:
  - Class Name: rename class to 'Alpha'
  - Path Independence: use .expanding() instead of .mean()/.std()
  - Trading Days: use cf.trading_days to align index
        """,
    )

    parser.add_argument("--code", required=True, help="Path to alpha.py")
    parser.add_argument("--universe", required=True, help="Market universe")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show details")

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  Alpha Validator")
    print("=" * 60)
    print(f"  File: {args.code}")
    print(f"  Universe: {args.universe}")

    results = []

    # Check 0: Class Name (before loading module)
    print_header("0. Class Name")
    try:
        passed, msg, details = check_class_name(args.code, args.verbose)
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"\n    {status} - {msg}")
        if not passed and "wrong_names" in details:
            print(f"    Fix: rename 'class {details['wrong_names'][0]}' to 'class Alpha'")
        results.append(passed)
    except Exception as e:
        print(f"\n    ✗ ERROR - {e}")
        results.append(False)

    # Load Alpha
    try:
        AlphaClass = load_alpha_from_file(args.code)
    except Exception as e:
        print(f"\n  ✗ Failed to load Alpha: {e}")
        sys.exit(1)

    # Check 1: Path Independence
    print_header("1. Path Independence")
    try:
        passed, msg, details = check_path_independence(AlphaClass, args.verbose)
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"\n    {status} - {msg}")
        if args.verbose and not passed and "affected_pct" in details:
            print(f"    Affected: {details['affected_pct']:.1f}% of cells")
        results.append(passed)
    except Exception as e:
        print(f"\n    ✗ ERROR - {e}")
        results.append(False)

    # Check 2: Trading Days
    print_header("2. Trading Days Index")
    try:
        passed, msg, details = check_trading_days(AlphaClass, args.universe, args.verbose)
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"\n    {status} - {msg}")
        if args.verbose and not passed and "invalid_samples" in details:
            print(f"    Examples: {details['invalid_samples']}")
        results.append(passed)
    except Exception as e:
        print(f"\n    ✗ ERROR - {e}")
        results.append(False)

    # Summary
    print_header("Summary")
    all_passed = all(results)
    if all_passed:
        print("  ✓ All checks passed!")
    else:
        print(f"  ✗ {results.count(False)}/{len(results)} checks failed")

    print()
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
