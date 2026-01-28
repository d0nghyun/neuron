"""
Signal Smoothing Pattern

Smooth signals with rolling mean to reduce noise and turnover.

Use this pattern when:
- Raw signals are noisy
- You want smoother position changes
- Reducing turnover is important

Strategy Logic:
1. Calculate raw signal (e.g., momentum)
2. Apply rolling mean to smooth signal
3. Normalize smoothed signals to create weights
4. This creates more stable positions

Typical Parameters:
- signal_period: [10, 20, 40]
- smoothing_window: [3, 5, 10] days
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
    """Smooth signals with rolling mean to create stable positions."""

    def get(
        self,
        start: int,
        end: int,
        signal_period: int = 20,
        smoothing_window: int = 5,
    ) -> pd.DataFrame:
        """
        Generate positions with smoothed signals.

        Parameters
        ----------
        start : int
            Start date in YYYYMMDD format
        end : int
            End date in YYYYMMDD format
        signal_period : int
            Period for signal calculation (default: 20)
        smoothing_window : int
            Rolling window for signal smoothing (default: 5)

        Returns
        -------
        pd.DataFrame
            Position DataFrame with smoothed weights
        """
        # Load data with buffer
        buffer = max(signal_period, smoothing_window) * 2 + 250
        cf = ContentFactory("kr_stock", get_start_date(start, buffer), end)
        close = cf.get_df("price_close")

        # Calculate raw signal (always use fill_method=None!)
        signal = close.pct_change(signal_period, fill_method=None)

        # Apply rolling mean to smooth signal
        signal_smoothed = signal.rolling(smoothing_window).mean()

        # Normalize to create weights, 1e8 == 100% of AUM
        weights = signal_smoothed.div(signal_smoothed.sum(axis=1), axis=0) * 1e8

        # CRITICAL: Always shift positions to avoid look-ahead bias
        return weights.shift(1).loc[str(start) : str(end)]
