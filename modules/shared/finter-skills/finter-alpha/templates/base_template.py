"""
BaseAlpha Template

Simple framework for quick alpha prototyping.
Copy this template and implement your strategy logic in the get() method.
"""

import pandas as pd
from finter import BaseAlpha
from finter.data import ContentFactory
from datetime import datetime, timedelta


def get_start_date(start: int, buffer: int = 365) -> int:
    """
    Get start date with buffer days for data loading.
    Rule of thumb: buffer = 2x longest lookback + 250 days
    """
    return int(
        (datetime.strptime(str(start), "%Y%m%d") - timedelta(days=buffer)).strftime("%Y%m%d")
    )


class Alpha(BaseAlpha):
    """
    [REPLACE] Your strategy description here.

    Strategy Logic:
    1. [REPLACE] Step 1
    2. [REPLACE] Step 2
    3. [REPLACE] Step 3

    Parameters:
    - param1: [REPLACE] Description
    - param2: [REPLACE] Description
    """

    def get(self, start: int, end: int, **kwargs) -> pd.DataFrame:
        """
        Generate alpha positions for date range.

        Parameters
        ----------
        start : int
            Start date in YYYYMMDD format (e.g., 20240101)
        end : int
            End date in YYYYMMDD format (e.g., 20241231)
        **kwargs : dict
            Strategy parameters:
            - param1: (type) description (default: value)
            - param2: (type) description (default: value)

        Returns
        -------
        pd.DataFrame
            Position DataFrame with:
            - Index: Trading dates
            - Columns: Stock tickers (FINTER IDs)
            - Values: Position sizes (money allocated, row sum ≤ 1e8)
        """
        # Extract parameters with defaults
        param1 = kwargs.get("param1", 20)
        param2 = kwargs.get("param2", 0.9)

        # Load data with buffer for calculations
        # Rule of thumb: buffer = 2x longest lookback + 250 days
        cf = ContentFactory("kr_stock", get_start_date(start), end)

        # Load necessary data
        # Note: Always use cf.search() to find exact item names
        # Example: cf.search('volume'), cf.search('market')
        close_price = cf.get_df("price_close")
        # volume = cf.get_df("volume_sum")  # Use cf.search('volume') to find
        # book_to_market = cf.get_df("book-to-market")  # Value factor

        # ==========================================
        # IMPLEMENT YOUR STRATEGY LOGIC HERE
        # ==========================================

        # Example: Simple momentum strategy (always use fill_method=None!)
        momentum = close_price.pct_change(param1, fill_method=None)

        # Rank stocks
        rank = momentum.rank(pct=True, axis=1)

        # Select stocks
        selected = rank >= param2

        # Create positions (equal weight), 1e8 == 100% of AUM
        positions = selected.div(selected.sum(axis=1), axis=0) * 1e8

        # ==========================================
        # END OF STRATEGY LOGIC
        # ==========================================

        # CRITICAL: Always shift positions to avoid look-ahead bias
        positions_shifted = positions.shift(1)

        # Filter to requested date range
        return positions_shifted.loc[str(start) : str(end)]


# ============================================================
# TESTING CODE (optional - for development/debugging)
# ============================================================

if __name__ == "__main__":
    # Quick test
    print("Testing Alpha strategy...")

    alpha = Alpha()

    # Test on small date range
    test_start = 20200101
    test_end = 20240131

    positions = alpha.get(test_start, test_end)

    print(f"\nPosition DataFrame shape: {positions.shape}")
    print(f"Date range: {positions.index[0]} to {positions.index[-1]}")
    print(f"Number of trading days: {len(positions)}")
    print(f"Number of stocks: {positions.shape[1]}")

    # Validate positions
    row_sums = positions.sum(axis=1)
    print("\nPosition validation:")
    print(f"  Min row sum: {row_sums.min():.0f}")
    print(f"  Max row sum: {row_sums.max():.0f}")
    print(f"  Mean row sum: {row_sums.mean():.0f}")

    if row_sums.max() > 1e8 + 1:
        print("  ⚠️ WARNING: Row sums exceed 1e8!")
    else:
        print("  ✓ Row sum constraints satisfied")

    nan_count = positions.isnull().sum().sum()
    print(f"  NaN count: {nan_count}")

    if nan_count > 0:
        print("  ⚠️ WARNING: Positions contain NaN values!")
    else:
        print("  ✓ No NaN values")

    # Show sample positions
    print("\nSample positions (first 3 days):")
    print(positions.head(3))

    print("\n✓ Template test complete!")
