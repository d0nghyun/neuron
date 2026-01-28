"""
Multi-Crypto Momentum Strategy

Cross-sectional momentum strategy for Binance perpetual futures using 10-minute candles.

⚠️ CRITICAL MEMORY CONSTRAINT:
   USE ONLY 2024 DATA (20240101 - 20241231).
   10-min candles with 378 coins = ~20M rows per year.
   Loading >1 year WILL CRASH the Jupyter server!

Strategy Logic:
1. Calculate price momentum over specified period (in 10-min candles)
2. Rank assets by momentum
3. Go long top-K assets with equal weight in USD

Important Notes:
- Universe: 'crypto_test' (same for ContentFactory and Simulator)
- Data: 10-minute candles, ~378 coins
- Position: USD amounts (NOT ratios) - e.g., $50,000 per asset
- Time conversion: 144 periods = 1 day, 1008 periods = 1 week
- DATE RANGE: Always start from 20240101, never earlier!

Typical Parameters:
- momentum_period: [144, 288, 432, 1008] (1 day, 2 days, 3 days, 1 week)
- top_k: [3, 5, 10] (number of assets to hold)
"""

from finter import BaseAlpha
from finter.data import ContentFactory
import pandas as pd


class Alpha(BaseAlpha):
    """Multi-crypto momentum strategy using 10-minute candles."""

    def get(
        self,
        start: int,
        end: int,
        momentum_period: int = 144,  # 1 day = 144 * 10min
        top_k: int = 5,
        position_size_usd: float = 50_000,  # USD per asset
    ) -> pd.DataFrame:
        """
        Generate alpha positions for multiple cryptocurrencies.

        Parameters
        ----------
        start : int
            Start date in YYYYMMDD format (e.g., 20241201)
        end : int
            End date in YYYYMMDD format (e.g., 20241231)
        momentum_period : int
            Lookback period in 10-min candles (default: 144 = 1 day)
            Common values: 144 (1d), 288 (2d), 432 (3d), 1008 (1w)
        top_k : int
            Number of top assets to hold (default: 5)
        position_size_usd : float
            USD amount per asset (default: $50,000)

        Returns
        -------
        pd.DataFrame
            Position DataFrame with:
            - Index: Trading dates (10-min resolution)
            - Columns: Asset codes (BTCUSDT, ETHUSDT, ...)
            - Values: Position size in USD (e.g., 50000 = $50k)
        """
        # Load data with buffer for lookback
        # ⚠️ NEVER use start < 20240101 (memory constraint)
        cf = ContentFactory('crypto_test', 20240101, end)

        # Load closing prices (10-min candles)
        close = cf.get_df('close')

        # Calculate momentum (percent change over period)
        # Always use fill_method=None to avoid forward-fill issues
        momentum = close.pct_change(periods=momentum_period, fill_method=None)

        # Rank assets by momentum (higher momentum = lower rank)
        ranks = momentum.rank(axis=1, ascending=False)

        # Select top-K assets
        selected = ranks <= top_k

        # Calculate positions in USD
        # Each selected asset gets position_size_usd
        positions = selected.astype(float) * position_size_usd

        # CRITICAL: Always shift positions to avoid look-ahead bias
        return positions.shift(1).loc[str(start):str(end)]


# Example usage in Jupyter:
"""
from finter.backtest import Simulator

# ⚠️ CRITICAL: Always use 20240101 as start for crypto_test (memory constraint)

# Generate positions
alpha = Alpha()
positions = alpha.get(
    20240101,  # ⚠️ Never earlier than 20240101!
    20241231,
    momentum_period=144,  # 1 day
    top_k=5,
    position_size_usd=50_000
)

# Run backtest
sim = Simulator("crypto_test", 20240101, 20241231)  # ⚠️ Same constraint
result = sim.run(position=positions)

# Check results
stats = result.statistics
print(f"Total Return: {stats['Total Return (%)']:.2f}%")
print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"Max Drawdown: {stats['Max Drawdown (%)']:.2f}%")
print(f"Hit Ratio: {stats['Hit Ratio (%)']:.2f}%")

# Plot NAV curve
result.summary['nav'].plot(title='Multi-Crypto Momentum Strategy NAV', figsize=(12, 6))
"""
