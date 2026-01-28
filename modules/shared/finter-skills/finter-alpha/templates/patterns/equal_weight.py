"""
Equal Weight Portfolio Pattern

Simplest portfolio construction: Equal weight across all available stocks.

Use this pattern when:
- You want a benchmark portfolio
- Testing basic infrastructure
- Building a baseline for comparison

Strategy Logic:
1. Load stock data
2. Assign equal weight to all stocks with available data
3. Rebalance daily
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
    """Equal weight portfolio across all available stocks."""

    def get(self, start: int, end: int) -> pd.DataFrame:
        """
        Generate equal weight positions.

        Parameters
        ----------
        start : int
            Start date in YYYYMMDD format
        end : int
            End date in YYYYMMDD format

        Returns
        -------
        pd.DataFrame
            Position DataFrame with equal weights
        """
        # Load data with buffer
        cf = ContentFactory("kr_stock", get_start_date(start), end)
        close = cf.get_df("price_close")

        # Equal weight all stocks, 1e8 == 100% of AUM
        n_stocks = close.shape[1]
        positions = close.notna().astype(float) * (1e8 / n_stocks)

        # CRITICAL: Always shift positions to avoid look-ahead bias
        return positions.shift(1).loc[str(start) : str(end)]
