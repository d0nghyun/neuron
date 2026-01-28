"""
Helper functions for Finter alpha strategy development.

NOTE: These functions are already included in all template files.
This file serves as a reference - you don't need to import from it.

All examples and patterns include these functions inline for portability.
Copy any additional functions below into your strategy file if needed.
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def get_start_date(start: int, buffer: int = 365) -> int:
    """
    Get start date with buffer days for data loading.

    Because we need to load data with buffer for calculations.
    Rule of thumb: buffer = 2x longest lookback + 250 days

    Parameters
    ----------
    start : int
        Start date in YYYYMMDD format (e.g., 20240101)
    buffer : int
        Number of buffer days to add before start date (default: 365)

    Returns
    -------
    int
        Adjusted start date in YYYYMMDD format

    Examples
    --------
    >>> get_start_date(20240101, buffer=60)
    20231102

    >>> # For 60-day momentum with safety margin
    >>> get_start_date(20240101, buffer=60*2 + 250)
    20230403
    """
    return int(
        (datetime.strptime(str(start), "%Y%m%d") - timedelta(days=buffer)).strftime(
            "%Y%m%d"
        )
    )


def validate_positions(positions: pd.DataFrame, max_total: float = 1e8) -> None:
    """
    Validate position DataFrame meets all constraints.

    Parameters
    ----------
    positions : pd.DataFrame
        Position DataFrame to validate
    max_total : float
        Maximum allowed row sum (default: 1e8)

    Raises
    ------
    AssertionError
        If validation fails

    Examples
    --------
    >>> validate_positions(positions)
    ✓ Position validation passed
    - Shape: (252, 100)
    - Row sum range: [0.00, 100000000.00]
    - NaN count: 0
    - Inf count: 0
    """
    print("\n=== Position Validation ===")
    print(f"Shape: {positions.shape}")

    # Check for NaN/Inf
    nan_count = positions.isnull().sum().sum()
    inf_count = np.isinf(positions).sum().sum()
    print(f"NaN count: {nan_count}")
    print(f"Inf count: {inf_count}")

    assert nan_count == 0, f"Contains {nan_count} NaN values"
    assert inf_count == 0, f"Contains {inf_count} Inf values"

    # Check row sums
    row_sums = positions.sum(axis=1)
    print(f"Row sum range: [{row_sums.min():.2f}, {row_sums.max():.2f}]")

    assert (
        row_sums.max() <= max_total + 1
    ), f"Row sums exceed {max_total}: max={row_sums.max():.0f}"

    print("✓ Position validation passed")


def get_finter_ids(stock_names: list, universe: str = "kr_stock") -> list:
    """
    Convert list of stock names to FINTER IDs.

    IMPORTANT: Run this BEFORE writing your Alpha class, then hardcode the IDs.
    Do NOT call this function inside your Alpha.get() method.

    Parameters
    ----------
    stock_names : list
        List of company names or ticker codes
    universe : str
        Market universe ("kr_stock", "us_stock", etc.)

    Returns
    -------
    list
        List of FINTER IDs to hardcode in your strategy

    Examples
    --------
    >>> # Step 1: Find IDs (run this first)
    >>> target_ids = get_finter_ids(["삼성전자", "SK하이닉스", "NAVER"])
    삼성전자: 12948
    SK하이닉스: 34521
    NAVER: 78932

    >>> # Step 2: Hardcode these IDs in your Alpha class
    >>> class Alpha(BaseAlpha):
    ...     def get(self, start, end):
    ...         target_ids = ["12948", "34521", "78932"]  # Hardcoded from above
    ...         close = cf.get_df("price_close")[target_ids]
    """
    from finter.data import Symbol

    symbol = Symbol(universe)
    ids = []

    for name in stock_names:
        results = symbol.search(name)
        if not results.empty:
            finter_id = results.index[0]
            ids.append(finter_id)
            print(f"{name}: {finter_id}")
        else:
            print(f"Warning: '{name}' not found")

    return ids
