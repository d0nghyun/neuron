"""
Specific Stock Strategy

Strategy targeting specific stocks only.

IMPORTANT: Find FINTER IDs first using Symbol.search(), then hardcode them.

Example workflow:
1. Run the find_stock_ids() function below to get FINTER IDs
2. Copy the IDs and hardcode them in your Alpha class
3. Implement your strategy logic

Typical Parameters:
- momentum_period: [10, 20, 30, 60]
"""

import pandas as pd
from finter import BaseAlpha
from finter.data import ContentFactory, Symbol
from datetime import datetime, timedelta


def get_start_date(start: int, buffer: int = 365) -> int:
    """
    Get start date with buffer days for data loading.
    Rule of thumb: buffer = 2x longest lookback + 250 days
    """
    return int(
        (datetime.strptime(str(start), "%Y%m%d") - timedelta(days=buffer)).strftime("%Y%m%d")
    )


def get_finter_ids(stock_names: list, universe: str = "kr_stock") -> list:
    """
    Convert list of stock names to FINTER IDs.
    Run this BEFORE writing your Alpha class, then hardcode the IDs.

    IMPORTANT: Symbol must be instantiated first!
    ✓ Correct: symbol = Symbol(universe); symbol.search(name)
    ✗ Wrong:   Symbol.search(name, universe=universe)
    """
    # MUST create instance first
    symbol = Symbol(universe)

    ids = []
    for name in stock_names:
        # Then call search on instance
        results = symbol.search(name)
        if not results.empty:
            finter_id = results.index[0]
            ids.append(finter_id)
            print(f"{name}: {finter_id}")
        else:
            print(f"Warning: '{name}' not found")
    return ids

# ============================================================
# STEP 1: Find FINTER IDs (run this first, BEFORE creating Alpha class)
# ============================================================


def find_stock_ids():
    """
    Run this function first to find FINTER IDs for your target stocks.
    Copy the output IDs and hardcode them in the Alpha class below.
    """
    # Korean stock examples
    print("=== Korean Stocks ===")
    kr_ids = get_finter_ids(["삼성전자", "SK하이닉스", "NAVER"], universe="kr_stock")

    # US stock examples
    print("\n=== US Stocks ===")
    us_ids = get_finter_ids(
        ["AAPL", "MSFT", "GOOGL", "META", "AMZN"], universe="us_stock"
    )

    print("\n✓ Copy these IDs and hardcode them in your Alpha class")
    return kr_ids, us_ids


# ============================================================
# STEP 2: Create Alpha class with hardcoded IDs
# ============================================================


class Alpha(BaseAlpha):
    """
    Strategy targeting specific stocks only.
    Stock IDs were found using Symbol.search() and hardcoded here.

    Strategy Logic:
    1. Load data for specific stocks only
    2. Calculate momentum for each stock
    3. Rank and select stocks with positive momentum
    4. Equal weight selected stocks
    """

    def get(self, start: int, end: int, momentum_period: int = 20) -> pd.DataFrame:
        """
        Generate alpha positions for date range.

        Parameters
        ----------
        start : int
            Start date in YYYYMMDD format
        end : int
            End date in YYYYMMDD format
        momentum_period : int
            Momentum calculation period

        Returns
        -------
        pd.DataFrame
            Position DataFrame
        """
        # Load data with buffer
        cf = ContentFactory(
            "kr_stock", get_start_date(start, momentum_period * 2 + 250), end
        )

        # Hardcoded FINTER IDs (found using Symbol.search())
        # NOTE: These are example IDs - use actual IDs from find_stock_ids()
        target_ids = [
            "12948",  # Samsung Electronics (example)
            "34521",  # SK Hynix (example)
            "78932",  # NAVER (example)
        ]

        # Load data only for these stocks
        close = cf.get_df("price_close")[target_ids]

        # Calculate momentum (always use fill_method=None!)
        momentum = close.pct_change(momentum_period, fill_method=None)

        # Rank stocks by momentum
        rank = momentum.rank(axis=1, pct=True)

        # Allocate to stocks with positive momentum, 1e8 == 100% of AUM
        selected = rank > 0.5
        weights = selected.div(selected.sum(axis=1), axis=0) * 1e8

        # CRITICAL: Always shift positions to avoid look-ahead bias
        return weights.shift(1).loc[str(start) : str(end)]


# ============================================================
# US Stocks Example
# ============================================================


class Alpha(BaseAlpha):
    """
    FAANG momentum strategy.
    Stock IDs were found using Symbol.search() and hardcoded.

    Strategy Logic:
    1. Load data for FAANG stocks only
    2. Calculate 20-day returns
    3. Select top 3 performers
    4. Equal weight selected stocks
    """

    def get(self, start: int, end: int) -> pd.DataFrame:
        """Generate alpha positions for US stocks."""
        # Load data with buffer
        cf = ContentFactory("us_stock", get_start_date(start, 20 * 2 + 250), end)

        # Hardcoded FINTER IDs for FAANG stocks
        # NOTE: These are example IDs - use actual IDs from find_stock_ids()
        faang_ids = [
            "45123",  # Meta (Facebook) - example
            "67890",  # Apple - example
            "23456",  # Amazon - example
            "78901",  # Netflix - example
            "34567",  # Google - example
        ]

        # Load and analyze
        close = cf.get_df("price_close")[faang_ids]
        returns_20d = close.pct_change(20, fill_method=None)

        # Equal weight the top 3 performers
        rank = returns_20d.rank(axis=1, ascending=False)
        selected = rank <= 3

        # 1e8 == 100% of AUM
        weights = selected.div(selected.sum(axis=1), axis=0) * 1e8

        # CRITICAL: Always shift positions to avoid look-ahead bias
        return weights.shift(1).loc[str(start) : str(end)]


# ============================================================
# Run this to find your stock IDs
# ============================================================

if __name__ == "__main__":
    print("Finding FINTER IDs for target stocks...\n")
    kr_ids, us_ids = find_stock_ids()
