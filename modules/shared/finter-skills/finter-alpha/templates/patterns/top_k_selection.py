"""
Top-K Selection Pattern

Select fixed number of top-ranked stocks based on a signal.

Use this pattern when:
- You want to hold a fixed number of positions
- Portfolio concentration is desired
- Signal ranking is reliable

Strategy Logic:
1. Calculate signal (e.g., momentum)
2. Rank all stocks by signal
3. Select top K stocks
4. Equal weight selected stocks

Typical Parameters:
- signal_period: [10, 20, 40, 60]
- top_k: [10, 20, 30, 50]
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
    """Select and equal weight top K stocks by signal."""

    def get(
        self, start: int, end: int, signal_period: int = 20, top_k: int = 20
    ) -> pd.DataFrame:
        """
        Generate top-K positions.

        Parameters
        ----------
        start : int
            Start date in YYYYMMDD format
        end : int
            End date in YYYYMMDD format
        signal_period : int
            Period for signal calculation (default: 20)
        top_k : int
            Number of top stocks to select (default: 20)

        Returns
        -------
        pd.DataFrame
            Position DataFrame with top-K selection
        """
        # Load data with buffer
        cf = ContentFactory(
            "kr_stock", get_start_date(start, signal_period * 2 + 250), end
        )
        close = cf.get_df("price_close")

        # Calculate signal (example: momentum) - always use fill_method=None!
        signal = close.pct_change(signal_period, fill_method=None)

        # Select top K stocks per day
        top_k_mask = signal.rank(axis=1, ascending=False) <= top_k

        # Equal weight selected stocks, 1e8 == 100% of AUM
        positions = top_k_mask.astype(float) * (1e8 / top_k)

        # CRITICAL: Always shift positions to avoid look-ahead bias
        return positions.shift(1).loc[str(start) : str(end)]
