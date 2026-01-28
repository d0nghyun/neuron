"""
Long-Short Market-Neutral Strategy

Market-neutral strategy that goes long top performers and short bottom performers.

Strategy Logic:
1. Calculate momentum (price change)
2. Rank all stocks by momentum
3. Long top 20%, Short bottom 20%
4. Equal weight within each leg

Position Rules:
- Positive values = Long positions
- Negative values = Short positions
- abs_sum <= 1e8 (total notional exposure)
- Cash = 1e8 - abs_sum

Examples:
| Long    | Short   | abs_sum | Cash   | Description           |
|---------|---------|---------|--------|-----------------------|
| 0.5e8   | -0.5e8  | 1e8     | 0      | 1:1 L/S, fully invested |
| 0.4e8   | -0.4e8  | 0.8e8   | 0.2e8  | 20% cash              |

Typical Parameters:
- momentum_period: [10, 20, 40, 60]
- long_pct: [0.1, 0.2, 0.3] (top percentile to long)
- short_pct: [0.1, 0.2, 0.3] (bottom percentile to short)
"""

from datetime import datetime, timedelta

import pandas as pd
from finter import BaseAlpha
from finter.data import ContentFactory


def get_start_date(start: int, buffer: int = 365) -> int:
    """
    Get start date with buffer days for data loading.
    Rule of thumb: buffer = 2x longest lookback + 250 days
    """
    return int(
        (datetime.strptime(str(start), "%Y%m%d") - timedelta(days=buffer)).strftime("%Y%m%d")
    )


class Alpha(BaseAlpha):
    """Market-neutral long-short momentum strategy."""

    def get(
        self,
        start: int,
        end: int,
        momentum_period: int = 20,
        long_pct: float = 0.2,
        short_pct: float = 0.2,
    ) -> pd.DataFrame:
        """
        Generate market-neutral positions.

        Parameters
        ----------
        start : int
            Start date in YYYYMMDD format
        end : int
            End date in YYYYMMDD format
        momentum_period : int
            Momentum calculation period (default: 20)
        long_pct : float
            Top percentile to long (default: 0.2 = top 20%)
        short_pct : float
            Bottom percentile to short (default: 0.2 = bottom 20%)

        Returns
        -------
        pd.DataFrame
            Position DataFrame with positive (long) and negative (short) values.
            abs_sum <= 1e8 per row.
        """
        # Load data with buffer
        cf = ContentFactory(
            "kr_stock", get_start_date(start, momentum_period * 2 + 250), end
        )
        close = cf.get_df("price_close")

        # Calculate momentum (always use fill_method=None!)
        momentum = close.pct_change(momentum_period, fill_method=None)

        # Rank stocks by momentum (0 to 1)
        rank = momentum.rank(axis=1, pct=True)

        # Long top performers, Short bottom performers
        long_mask = rank >= (1 - long_pct)   # e.g., >= 0.8 for top 20%
        short_mask = rank <= short_pct        # e.g., <= 0.2 for bottom 20%

        # Equal weight each leg: 0.5e8 long + 0.5e8 short = 1e8 abs sum
        long_weight = long_mask.div(long_mask.sum(axis=1), axis=0) * 0.5e8
        short_weight = -short_mask.div(short_mask.sum(axis=1), axis=0) * 0.5e8

        positions = long_weight.fillna(0) + short_weight.fillna(0)

        # CRITICAL: Always shift positions to avoid look-ahead bias
        return positions.shift(1).fillna(0).loc[str(start):str(end)]
