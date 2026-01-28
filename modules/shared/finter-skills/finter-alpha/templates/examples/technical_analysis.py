"""
Simple Momentum Strategy

Classic momentum: Buy recent winners, sell recent losers.

Strategy Logic:
1. Calculate price momentum over specified period
2. Rank all stocks by momentum
3. Select top performers above threshold
4. Equal weight selected stocks

Typical Parameters:
- momentum_period: [10, 21, 42, 63]
- top_percent: [0.8, 0.9, 0.95]
"""

from finter import BaseAlpha
from finter.data import ContentFactory
import pandas as pd
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
    """Classic momentum strategy: Buy recent winners, sell recent losers."""

    def get(
        self,
        start: int,
        end: int,
        momentum_period: int = 21,
        top_percent: float = 0.9,
    ) -> pd.DataFrame:
        """
        Generate alpha positions for date range.

        Parameters
        ----------
        start : int
            Start date in YYYYMMDD format (e.g., 20240101)
        end : int
            End date in YYYYMMDD format (e.g., 20241231)
        momentum_period : int
            Lookback period for momentum calculation (default: 21 days)
        top_percent : float
            Percentile threshold for selection (0.9 = top 10% stocks)

        Returns
        -------
        pd.DataFrame
            Position DataFrame with:
            - Index: Trading dates
            - Columns: Stock tickers (FINTER IDs)
            - Values: Position sizes (money allocated, row sum ≤ 1e8)
        """
        # Load data with buffer for calculations
        # Rule of thumb: buffer = 2x longest lookback + 250 days
        cf = ContentFactory(
            "kr_stock", get_start_date(start, momentum_period * 2 + 250), end
        )
        close = cf.get_df("price_close")

        # Calculate momentum (always use fill_method=None for path independence!)
        momentum = close.pct_change(momentum_period, fill_method=None)

        # Rank stocks by momentum
        rank = momentum.rank(pct=True, axis=1)

        # Select top stocks
        selected = rank >= top_percent

        # Create positions (equal weight), 1e8 == 100% of AUM
        weights = selected.div(selected.sum(axis=1), axis=0) * 1e8

        # CRITICAL: Always shift positions to avoid look-ahead bias
        return weights.shift(1).loc[str(start) : str(end)]
