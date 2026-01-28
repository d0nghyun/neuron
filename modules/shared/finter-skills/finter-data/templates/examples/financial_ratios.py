"""
Financial Ratio Calculation Example

Demonstrates how to:
1. Discover financial items using search
2. Load financial data with get_fc()
3. Apply rolling operations (TTM, averages)
4. Calculate common financial ratios
5. Convert to wide format for Alpha usage

Key concepts:
- TTM (Trailing Twelve Months): Sum of last 4 quarters
- Average: Mean of last 4 quarters for balance sheet items
- get_fc() returns FinancialCalculator (fluent API)
- to_wide() converts to pandas DataFrame

Usage:
    from finter.data import ContentFactory
    cf = ContentFactory('kr_stock', 20150101, 20250101)

    # Calculate ROE
    roe_df = calculate_roe(cf)

    # Use in Alpha
    positions = roe_df.rank(axis=1, pct=True) * 1e8
"""

from finter.data import ContentFactory, Symbol
import polars as pl


def calculate_roe(cf: ContentFactory):
    """
    Calculate Return on Equity (ROE).

    Formula: ROE = Net Income (TTM) / Average Equity

    Returns:
        pd.DataFrame: ROE values (dates × stocks)
    """
    fc = cf.get_fc({
        'income': 'krx-spot-owners_of_parent_net_income',
        'equity': 'krx-spot-owners_of_parent_equity'
    })

    roe = (fc
        .apply_rolling(4, 'sum', variables=['income'])
        .apply_rolling(4, 'mean', variables=['equity'])
        .apply_expression('income / equity')
    )

    return roe.to_wide()


def calculate_operating_margin(cf: ContentFactory):
    """
    Calculate Operating Margin (TTM).

    Formula: Operating Margin = Operating Income (TTM) / Sales (TTM)

    Returns:
        pd.DataFrame: Operating margin values (dates × stocks)
    """
    fc = cf.get_fc({
        'oi': 'krx-spot-operating_income',
        'sales': 'krx-spot-sales'
    })

    margin = (fc
        .apply_rolling(4, 'sum', variables=['oi', 'sales'])
        .apply_expression('oi / sales')
    )

    return margin.to_wide()


def calculate_current_ratio(cf: ContentFactory):
    """
    Calculate Current Ratio (snapshot, no rolling).

    Formula: Current Ratio = Current Assets / Current Liabilities

    Returns:
        pd.DataFrame: Current ratio values (dates × stocks)
    """
    fc = cf.get_fc({
        'ca': 'krx-spot-current_assets',
        'cl': 'krx-spot-current_liabilities'
    })

    current_ratio = fc.apply_expression('ca / cl')

    return current_ratio.to_wide()


def calculate_debt_to_equity(cf: ContentFactory):
    """
    Calculate Debt-to-Equity ratio (snapshot, no rolling).

    Formula: D/E = Total Liabilities / Owners Equity

    Returns:
        pd.DataFrame: D/E values (dates × stocks)
    """
    fc = cf.get_fc({
        'debt': 'krx-spot-total_liabilities',
        'equity': 'krx-spot-owners_of_parent_equity'
    })

    debt_equity = fc.apply_expression('debt / equity')

    return debt_equity.to_wide()


def calculate_asset_turnover(cf: ContentFactory):
    """
    Calculate Asset Turnover.

    Formula: Asset Turnover = Sales (TTM) / Average Assets

    Returns:
        pd.DataFrame: Asset turnover values (dates × stocks)
    """
    fc = cf.get_fc({
        'sales': 'krx-spot-sales',
        'assets': 'krx-spot-total_assets'
    })

    turnover = (fc
        .apply_rolling(4, 'sum', variables=['sales'])
        .apply_rolling(4, 'mean', variables=['assets'])
        .apply_expression('sales / assets')
    )

    return turnover.to_wide()


if __name__ == '__main__':
    # Example usage
    cf = ContentFactory('kr_stock', 20150101, 20250101)

    print('=== Financial Ratio Calculation Example ===\n')

    # Discover financial items
    print('Step 1: Discover financial items')
    print('Using cf.search() to find available items...')

    # TIP: Search with prefix for financial data
    income_items = cf.search('krx-spot-owners_of_parent_net_income')
    print(f'Found {len(income_items)} items')
    print(f'Using: {income_items[0] if income_items else "none"}\n')

    # Calculate ROE
    print('Step 2: Calculate ROE')
    roe_df = calculate_roe(cf)
    print(f'Shape: {roe_df.shape} (dates × stocks)')
    print(f'Date range: {roe_df.index[0]} to {roe_df.index[-1]}')
    print(f'Latest mean ROE: {roe_df.iloc[-1].mean():.4f}\n')

    # Calculate Operating Margin
    print('Step 3: Calculate Operating Margin')
    margin_df = calculate_operating_margin(cf)
    print(f'Shape: {margin_df.shape}')
    print(f'Latest mean margin: {margin_df.iloc[-1].mean():.4f}\n')

    # Calculate Current Ratio
    print('Step 4: Calculate Current Ratio')
    current_ratio_df = calculate_current_ratio(cf)
    print(f'Shape: {current_ratio_df.shape}')
    print(f'Latest mean current ratio: {current_ratio_df.iloc[-1].mean():.4f}\n')

    # Inspect Samsung Electronics
    print('Step 5: Inspect Samsung Electronics (ID: 12170)')
    symbol = Symbol('kr_stock')
    samsung = symbol.search('삼성전자')
    samsung_id = samsung.index[0]

    if samsung_id in roe_df.columns:
        samsung_roe = roe_df[samsung_id].dropna()
        print(f'\nSamsung ROE:')
        print(f'  Latest: {samsung_roe.iloc[-1]:.4f}')
        print(f'  Mean: {samsung_roe.mean():.4f}')
        print(f'  Latest 5 values:')
        print(samsung_roe.tail())

    print('\n=== Summary ===')
    print('✓ Financial data loaded with get_fc()')
    print('✓ Rolling operations applied (TTM, averages)')
    print('✓ Ratios calculated with apply_expression()')
    print('✓ Converted to wide format with to_wide()')
    print('\nReady for Alpha strategy usage!')

    # Example: Use in Alpha strategy
    print('\n=== Example Alpha Usage ===')
    print('# Rank-based positions from ROE')
    print('positions = roe_df.rank(axis=1, pct=True) * 1e8')
    positions = roe_df.rank(axis=1, pct=True) * 1e8
    print(f'Positions shape: {positions.shape}')
    print(f'Positions range: [{positions.min().min():.0f}, {positions.max().max():.0f}]')

    print('\n=== MultiIndex Example (Without Expression) ===')
    # When you don't apply expression, to_wide() returns MultiIndex columns
    fc = cf.get_fc({
        'income': 'krx-spot-owners_of_parent_net_income',
        'sales': 'krx-spot-sales'
    })

    ttm = fc.apply_rolling(4, 'sum', variables=['income', 'sales'])
    ttm_df = ttm.to_wide()

    print(f'Shape: {ttm_df.shape}')
    print(f'Column type: {type(ttm_df.columns)}')
    print(f'First 3 columns: {ttm_df.columns[:3].tolist()}')

    # Access specific stock using .xs()
    if samsung_id in [col[1] for col in ttm_df.columns]:
        samsung_id_int = int(samsung_id)
        samsung_ttm = ttm_df.xs(samsung_id_int, level=1, axis=1)
        print(f'\nSamsung TTM data:')
        print(f'  Columns: {samsung_ttm.columns.tolist()}')
        print(f'  Latest income: {samsung_ttm["income"].iloc[-1]:,.0f}')
        print(f'  Latest sales: {samsung_ttm["sales"].iloc[-1]:,.0f}')
