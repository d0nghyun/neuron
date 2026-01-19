#!/usr/bin/env python3
"""
MCP Data Source Interface Definitions

These are abstract interfaces that should be implemented when
connecting to actual MCP data sources in Claude Agent SDK environment.

[P5 Modularity] - Clean interfaces for external data sources
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Protocol
from enum import Enum


class DataSourceType(Enum):
    """Supported data source types."""
    FINANCE = "finance"
    CRYPTO = "crypto"
    MACRO = "macro"
    CUSTOM = "custom"


@dataclass
class Metric:
    """Standard metric format returned by data sources."""
    label: str
    value: Any
    unit: str = ""
    delta: Optional[float] = None
    delta_period: str = "vs prev"
    timestamp: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "value": self.value,
            "unit": self.unit,
            "delta": self.delta,
            "delta_period": self.delta_period,
        }


@dataclass
class TimeSeries:
    """Standard time series format."""
    name: str
    labels: list[str]
    data: list[float]
    is_forecast: bool = False

    def to_dict(self) -> dict:
        return {
            "label": self.name,
            "data": self.data,
            "is_forecast": self.is_forecast,
        }


@dataclass
class DataSourceResult:
    """Standard result format from any data source."""
    source_type: DataSourceType
    subject: str  # ticker, token, region, etc.
    metrics: dict[str, Metric] = field(default_factory=dict)
    time_series: dict[str, TimeSeries] = field(default_factory=dict)
    tables: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def to_report_data(self) -> dict:
        """Convert to report generator input format."""
        return {
            "metadata": {
                "type": self.source_type.value,
                "subject": self.subject,
                **self.metadata,
            },
            "metrics": {k: v.to_dict() for k, v in self.metrics.items()},
            "time_series": {
                "datasets": [ts.to_dict() for ts in self.time_series.values()],
                "labels": next(iter(self.time_series.values())).labels if self.time_series else [],
            } if self.time_series else None,
            "table": self.tables[0] if self.tables else None,
        }


class MCPDataSource(Protocol):
    """Protocol for MCP data sources."""

    async def fetch(
        self,
        subject: str,
        metrics: list[str],
        period: str = "1Y",
        **kwargs
    ) -> DataSourceResult:
        """Fetch data from the source."""
        ...


class FinanceDataSource(ABC):
    """
    Abstract interface for financial data sources.

    Implementations should connect to:
    - Yahoo Finance API
    - Bloomberg API
    - Company filings (SEC EDGAR, DART)
    """

    @abstractmethod
    async def get_stock_data(
        self,
        ticker: str,
        metrics: list[str] = None,
        period: str = "1Y"
    ) -> DataSourceResult:
        """
        Fetch stock financial data.

        Args:
            ticker: Stock ticker (e.g., "005930.KS", "AAPL")
            metrics: Specific metrics to fetch, or None for all
            period: Time period for historical data

        Returns:
            DataSourceResult with:
            - metrics: price, market_cap, pe_ratio, revenue, profit, etc.
            - time_series: revenue_quarterly, price_daily, etc.
            - tables: financials, peer_comparison
        """
        pass

    @abstractmethod
    async def get_financials(
        self,
        ticker: str,
        statement: str = "income",  # income, balance, cashflow
        period: str = "annual"  # annual, quarterly
    ) -> DataSourceResult:
        """Fetch detailed financial statements."""
        pass

    @abstractmethod
    async def get_peers(
        self,
        ticker: str,
        metrics: list[str] = None
    ) -> DataSourceResult:
        """Fetch peer comparison data."""
        pass


class CryptoDataSource(ABC):
    """
    Abstract interface for crypto data sources.

    Implementations should connect to:
    - CoinGecko / CoinMarketCap
    - Glassnode / CryptoQuant (on-chain)
    - DefiLlama (DeFi protocols)
    - Dune Analytics (custom queries)
    """

    @abstractmethod
    async def get_token_data(
        self,
        token: str,
        metrics: list[str] = None,
        chain: str = "ethereum"
    ) -> DataSourceResult:
        """
        Fetch token/protocol data.

        Args:
            token: Token symbol or protocol name
            metrics: Specific metrics to fetch
            chain: Blockchain network

        Returns:
            DataSourceResult with:
            - metrics: price, market_cap, volume, tvl, etc.
            - time_series: price_history, tvl_history, etc.
        """
        pass

    @abstractmethod
    async def get_on_chain_metrics(
        self,
        address: str,
        chain: str = "ethereum",
        metrics: list[str] = None
    ) -> DataSourceResult:
        """Fetch on-chain metrics for address/protocol."""
        pass

    @abstractmethod
    async def get_tokenomics(
        self,
        token: str
    ) -> DataSourceResult:
        """Fetch tokenomics data (supply, vesting, etc.)."""
        pass


class MacroDataSource(ABC):
    """
    Abstract interface for macroeconomic data sources.

    Implementations should connect to:
    - FRED (Federal Reserve Economic Data)
    - BLS (Bureau of Labor Statistics)
    - IMF / World Bank
    - Central bank APIs
    """

    @abstractmethod
    async def get_economic_data(
        self,
        region: str,
        indicators: list[str] = None,
        period: str = "5Y"
    ) -> DataSourceResult:
        """
        Fetch macroeconomic data.

        Args:
            region: Country/region code ("US", "KR", "EU", "GLOBAL")
            indicators: Economic indicators to fetch
            period: Time period

        Returns:
            DataSourceResult with:
            - metrics: gdp_growth, inflation, unemployment, etc.
            - time_series: historical indicator data
        """
        pass

    @abstractmethod
    async def get_rates(
        self,
        region: str,
        rate_types: list[str] = None  # policy, 10y, 2y, etc.
    ) -> DataSourceResult:
        """Fetch interest rate data."""
        pass

    @abstractmethod
    async def get_forecast(
        self,
        region: str,
        indicators: list[str] = None
    ) -> DataSourceResult:
        """Fetch economic forecasts."""
        pass


# ============================================================
# Mock implementations for testing
# ============================================================

class MockFinanceDataSource(FinanceDataSource):
    """Mock implementation for testing without real API."""

    async def get_stock_data(
        self,
        ticker: str,
        metrics: list[str] = None,
        period: str = "1Y"
    ) -> DataSourceResult:
        return DataSourceResult(
            source_type=DataSourceType.FINANCE,
            subject=ticker,
            metrics={
                "price": Metric("Price", 85000, "KRW", 12.5),
                "market_cap": Metric("Market Cap", 500000000000000, "KRW"),
                "pe_ratio": Metric("P/E Ratio", 15.2),
                "revenue": Metric("Revenue", 280000000000000, "KRW", 15.3, "YoY"),
            },
            time_series={
                "revenue": TimeSeries(
                    "Revenue",
                    ["2023Q1", "2023Q2", "2023Q3", "2023Q4", "2024Q1"],
                    [65, 68, 70, 73, 74]
                ),
                "profit": TimeSeries(
                    "Net Profit",
                    ["2023Q1", "2023Q2", "2023Q3", "2023Q4", "2024Q1"],
                    [6.5, 7.0, 7.2, 8.0, 8.5]
                ),
            },
            metadata={
                "name": "Samsung Electronics",
                "sector": "Technology",
                "exchange": "KRX",
            }
        )

    async def get_financials(self, ticker, statement="income", period="annual"):
        return DataSourceResult(
            source_type=DataSourceType.FINANCE,
            subject=ticker,
            tables=[{
                "title": f"{statement.title()} Statement",
                "columns": ["Item", "2022", "2023", "2024E"],
                "rows": [
                    ["Revenue", "280T", "300T", "320T"],
                    ["Operating Profit", "43T", "50T", "55T"],
                    ["Net Profit", "30T", "35T", "40T"],
                ]
            }]
        )

    async def get_peers(self, ticker, metrics=None):
        return DataSourceResult(
            source_type=DataSourceType.FINANCE,
            subject=ticker,
            tables=[{
                "title": "Peer Comparison",
                "columns": ["Company", "P/E", "ROE", "Market Cap"],
                "rows": [
                    ["Samsung", "15.2", "12%", "500T"],
                    ["SK Hynix", "18.5", "10%", "120T"],
                    ["TSMC", "22.1", "25%", "600T"],
                ]
            }]
        )


class MockCryptoDataSource(CryptoDataSource):
    """Mock implementation for testing."""

    async def get_token_data(self, token, metrics=None, chain="ethereum"):
        return DataSourceResult(
            source_type=DataSourceType.CRYPTO,
            subject=token,
            metrics={
                "price": Metric("Price", 3500, "USD", 5.2),
                "market_cap": Metric("Market Cap", 420000000000, "USD"),
                "volume_24h": Metric("24h Volume", 15000000000, "USD"),
                "tvl": Metric("TVL", 50000000000, "USD", -2.1),
            },
            time_series={
                "price": TimeSeries(
                    "Price",
                    ["Jan", "Feb", "Mar", "Apr", "May"],
                    [2800, 3000, 3200, 3400, 3500]
                ),
            },
            metadata={
                "chain": chain,
                "type": "Layer 1",
            }
        )

    async def get_on_chain_metrics(self, address, chain="ethereum", metrics=None):
        return DataSourceResult(
            source_type=DataSourceType.CRYPTO,
            subject=address,
            metrics={
                "active_addresses": Metric("Daily Active", 500000),
                "transactions": Metric("Daily Txns", 1200000),
            }
        )

    async def get_tokenomics(self, token):
        return DataSourceResult(
            source_type=DataSourceType.CRYPTO,
            subject=token,
            tables=[{
                "title": "Token Distribution",
                "columns": ["Category", "Amount", "Percentage"],
                "rows": [
                    ["Foundation", "10M", "10%"],
                    ["Team", "15M", "15%"],
                    ["Public", "75M", "75%"],
                ]
            }]
        )


class MockMacroDataSource(MacroDataSource):
    """Mock implementation for testing."""

    async def get_economic_data(self, region, indicators=None, period="5Y"):
        return DataSourceResult(
            source_type=DataSourceType.MACRO,
            subject=region,
            metrics={
                "gdp_growth": Metric("GDP Growth", 2.5, "%", 0.3),
                "inflation": Metric("Inflation (CPI)", 2.8, "%", -0.5),
                "unemployment": Metric("Unemployment", 4.0, "%", -0.2),
            },
            time_series={
                "gdp": TimeSeries(
                    "GDP Growth",
                    ["2020", "2021", "2022", "2023", "2024"],
                    [-2.8, 5.9, 2.1, 2.5, 2.3]
                ),
            },
            metadata={
                "region_name": "United States",
                "data_source": "FRED",
            }
        )

    async def get_rates(self, region, rate_types=None):
        return DataSourceResult(
            source_type=DataSourceType.MACRO,
            subject=region,
            metrics={
                "policy_rate": Metric("Fed Funds Rate", 4.5, "%"),
                "10y_yield": Metric("10Y Treasury", 4.2, "%"),
                "2y_yield": Metric("2Y Treasury", 4.0, "%"),
            }
        )

    async def get_forecast(self, region, indicators=None):
        return DataSourceResult(
            source_type=DataSourceType.MACRO,
            subject=region,
            time_series={
                "gdp_forecast": TimeSeries(
                    "GDP Growth Forecast",
                    ["2024", "2025", "2026"],
                    [2.3, 2.0, 2.2],
                    is_forecast=True
                ),
            }
        )


# ============================================================
# Factory for getting data sources
# ============================================================

def get_data_source(
    source_type: DataSourceType,
    use_mock: bool = True
) -> MCPDataSource:
    """
    Get appropriate data source.

    Args:
        source_type: Type of data source
        use_mock: If True, return mock implementation

    Returns:
        Data source instance
    """
    if use_mock:
        if source_type == DataSourceType.FINANCE:
            return MockFinanceDataSource()
        elif source_type == DataSourceType.CRYPTO:
            return MockCryptoDataSource()
        elif source_type == DataSourceType.MACRO:
            return MockMacroDataSource()

    # Real implementations would be imported and returned here
    raise NotImplementedError(f"Real data source for {source_type} not implemented")


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":
    import asyncio

    async def test():
        # Test finance
        finance = MockFinanceDataSource()
        result = await finance.get_stock_data("005930.KS")
        print("Finance:", result.subject, result.metrics.keys())

        # Test crypto
        crypto = MockCryptoDataSource()
        result = await crypto.get_token_data("ETH")
        print("Crypto:", result.subject, result.metrics.keys())

        # Test macro
        macro = MockMacroDataSource()
        result = await macro.get_economic_data("US")
        print("Macro:", result.subject, result.metrics.keys())

        # Convert to report data
        report_data = result.to_report_data()
        print("Report data keys:", report_data.keys())

    asyncio.run(test())
