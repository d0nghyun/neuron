# Preprocessing Methods (SSOT)

Single source of truth for data preprocessing methods.

## Overview

Data preprocessing transforms raw data into clean, usable features. Three main categories:

1. **Missing Value Handling**: Deal with NaN values
2. **Outlier Handling**: Remove or clip extreme values
3. **Normalization**: Scale data for cross-sectional comparability

**Key principle: Check data quality BEFORE preprocessing!**

---

## Missing Value Handling

### Strategy Selection

| Method | When to Use | Pros | Cons |
|--------|-------------|------|------|
| Forward fill | Time series (price, volume) | Preserves last known value | Can propagate stale data |
| Forward + Backward fill | Most cases | Handles start/end missing | May create look-ahead bias at start |
| Interpolation | Smooth continuous data | Creates reasonable estimates | Assumes linearity |
| Drop | Too much missing (>20%) | Clean dataset | Lose data |

### Method 1: Forward Fill + Backward Fill (Most Common)

**When to use:** Price, volume, most time series data

**Code:**
```python
def fill_missing(df):
    """Forward fill then backward fill"""
    return df.ffill().bfill()

# Usage
close = cf.get_df('price_close')
close_clean = fill_missing(close)
```

**Why forward + backward?**
- Forward fill: Uses last known value (realistic for trading)
- Backward fill: Handles missing values at the start (when no history yet)

### Method 2: Forward Fill Only

**When to use:** When backward fill may create look-ahead bias

**Code:**
```python
def ffill_only(df):
    """Forward fill only"""
    return df.ffill()

# Usage
close = cf.get_df('price_close')
close_clean = ffill_only(close)
```

**Trade-off:** Some NaN may remain at the start

### Method 3: Interpolation

**When to use:** Smooth continuous data where linearity is reasonable

**Code:**
```python
def interpolate_missing(df, method='linear'):
    """Interpolate missing values

    Args:
        method: 'linear', 'polynomial', 'spline'
    """
    return df.interpolate(method=method)

# Usage
close = cf.get_df('price_close')
close_clean = interpolate_missing(close, method='linear')
```

**Warning:** Can create unrealistic values for volatile data

### Method 4: Drop

**When to use:** Column has too much missing data (>20%)

**Code:**
```python
def drop_missing_columns(df, threshold=0.8):
    """Drop columns with too much missing data

    Args:
        threshold: Keep column if valid_ratio > threshold
    """
    return df.dropna(axis=1, thresh=int(len(df) * threshold))

# Usage
close = cf.get_df('price_close')
close_clean = drop_missing_columns(close, threshold=0.8)  # Keep if >80% valid
```

**When to drop rows:**
```python
def drop_missing_rows(df):
    """Drop rows with any NaN"""
    return df.dropna(axis=0)
```

---

## Outlier Handling

### Strategy Selection

| Method | When to Use | Pros | Cons |
|--------|-------------|------|------|
| Winsorization | Price-based, ratio-based factors | Preserves distribution shape | May distort tail information |
| Z-score clipping | Normally distributed data | Simple, interpretable | Assumes normality |
| Robust statistics | Heavy-tailed distributions | Robust to outliers | More computation |

### Method 1: Winsorization (Recommended)

**When to use:** Most factors (price-based, ratio-based)

**Code:**
```python
def winsorize(df, lower=0.01, upper=0.99):
    """Clip extreme values to percentiles (cross-sectional)

    Args:
        lower: Lower percentile (0.01 = 1%)
        upper: Upper percentile (0.99 = 99%)

    Returns:
        DataFrame with extreme values clipped per timestamp
    """
    return df.clip(
        lower=df.quantile(lower, axis=1),  # Per timestamp
        upper=df.quantile(upper, axis=1),
        axis=0
    )

# Usage
factor = cf.get_df('some_ratio')
factor_clean = winsorize(factor, lower=0.01, upper=0.99)
```

**Percentile guidelines:**
- Price-based factors: 1%/99%
- Ratio-based factors: 5%/95%
- Conservative: 2%/98%

**Why cross-sectional (axis=1)?**
- Clips per timestamp (across stocks)
- Handles market regime changes
- Prevents one bad day from affecting all dates

### Method 2: Z-score Clipping

**When to use:** Normally distributed factors

**Code:**
```python
def clip_zscore(df, threshold=3):
    """Clip values beyond N standard deviations (cross-sectional)

    Args:
        threshold: Number of standard deviations (typically 3)

    Returns:
        DataFrame with extreme z-scores clipped per timestamp
    """
    mean = df.mean(axis=1)
    std = df.std(axis=1)
    return df.clip(
        lower=mean - threshold * std,
        upper=mean + threshold * std,
        axis=0
    )

# Usage
factor = cf.get_df('some_ratio')
factor_clean = clip_zscore(factor, threshold=3)
```

**Threshold guidelines:**
- Conservative: 2.5 std
- Standard: 3 std
- Liberal: 4 std

### Method 3: Robust Statistics (IQR)

**When to use:** Heavy-tailed distributions

**Code:**
```python
def clip_iqr(df, iqr_multiplier=1.5):
    """Clip using Interquartile Range (cross-sectional)

    Args:
        iqr_multiplier: IQR multiplier (1.5 = standard outlier detection)

    Returns:
        DataFrame with outliers clipped per timestamp
    """
    q1 = df.quantile(0.25, axis=1)
    q3 = df.quantile(0.75, axis=1)
    iqr = q3 - q1

    return df.clip(
        lower=q1 - iqr_multiplier * iqr,
        upper=q3 + iqr_multiplier * iqr,
        axis=0
    )

# Usage
factor = cf.get_df('some_ratio')
factor_clean = clip_iqr(factor, iqr_multiplier=1.5)
```

**IQR multiplier guidelines:**
- Conservative: 1.5 (standard)
- Liberal: 2.0
- Very liberal: 3.0

---

## Normalization

### Strategy Selection

| Method | When to Use | Pros | Cons |
|--------|-------------|------|------|
| Z-score | Most factors | Interpretable (std units) | Sensitive to outliers |
| Rank | Robust factors | Robust to outliers, uniform | Loses magnitude information |
| Min-max | Bounded range needed | Clear [0,1] range | Sensitive to outliers |

### Method 1: Cross-sectional Z-score (Most Common)

**When to use:** Most factors for cross-sectional strategies

**Code:**
```python
def zscore(df):
    """Normalize to z-scores (cross-sectional)

    Returns:
        DataFrame with mean=0, std=1 per timestamp
    """
    mean = df.mean(axis=1)
    std = df.std(axis=1)
    return df.sub(mean, axis=0).div(std, axis=0)

# Usage
factor = cf.get_df('some_ratio')
factor_normalized = zscore(factor)

# Check
print(factor_normalized.mean(axis=1).mean())  # ~0
print(factor_normalized.std(axis=1).mean())   # ~1
```

**Benefits:**
- Mean=0, Std=1 per timestamp
- Interpretable (z-score units)
- Comparable across different factors

**Limitations:**
- Sensitive to outliers (apply winsorization first!)
- Assumes enough stocks per timestamp

### Method 2: Cross-sectional Rank (Robust)

**When to use:** Factors with heavy tails or extreme outliers

**Code:**
```python
def rank_normalize(df, pct=True):
    """Rank normalize (cross-sectional)

    Args:
        pct: If True, return percentiles [0, 1], else ranks [1, N]

    Returns:
        DataFrame with ranks per timestamp
    """
    return df.rank(axis=1, pct=pct)

# Usage
factor = cf.get_df('some_ratio')
factor_ranked = rank_normalize(factor, pct=True)  # [0, 1]

# Check
print(factor_ranked.min().min())  # ~0
print(factor_ranked.max().max())  # ~1
```

**Benefits:**
- Robust to outliers
- Uniform distribution [0, 1]
- No need for winsorization

**Limitations:**
- Loses magnitude information
- Treats gaps equally (rank 100 vs 101 same as 1 vs 2)

### Method 3: Min-Max Scaling

**When to use:** Need specific [0, 1] range

**Code:**
```python
def minmax_scale(df):
    """Scale to [0, 1] range (cross-sectional)

    Returns:
        DataFrame scaled to [0, 1] per timestamp
    """
    min_val = df.min(axis=1)
    max_val = df.max(axis=1)
    return df.sub(min_val, axis=0).div(max_val - min_val, axis=0)

# Usage
factor = cf.get_df('some_ratio')
factor_scaled = minmax_scale(factor)

# Check
print(factor_scaled.min(axis=1).mean())  # 0
print(factor_scaled.max(axis=1).mean())  # 1
```

**Benefits:**
- Clear [0, 1] range
- Preserves distribution shape

**Limitations:**
- Very sensitive to outliers!
- Min/max may be extreme values

---

## Composite Preprocessing Pipeline

Combine multiple steps for robust preprocessing:

```python
def preprocess_factor(df, method='robust'):
    """Complete preprocessing pipeline

    Args:
        df: Raw factor data
        method: 'robust' (default) or 'standard'

    Returns:
        Preprocessed DataFrame
    """
    # Step 1: Handle missing values
    df_clean = df.ffill().bfill()

    if method == 'robust':
        # Step 2: Remove outliers (robust)
        df_clean = winsorize(df_clean, lower=0.01, upper=0.99)

        # Step 3: Normalize (robust)
        df_final = rank_normalize(df_clean, pct=True)

    elif method == 'standard':
        # Step 2: Remove outliers (standard)
        df_clean = clip_zscore(df_clean, threshold=3)

        # Step 3: Normalize (standard)
        df_final = zscore(df_clean)

    return df_final

# Usage
factor = cf.get_df('some_ratio')
factor_processed = preprocess_factor(factor, method='robust')
```

**Recommended pipeline:**
1. Handle missing → 2. Remove outliers → 3. Normalize

**Why this order?**
- Missing values break outlier detection
- Outliers distort normalization
- Each step assumes previous steps are done

---

## Validation

Always validate preprocessing results:

```python
def validate_preprocessing(df_before, df_after):
    """Validate preprocessing results

    Args:
        df_before: Raw data
        df_after: Preprocessed data
    """
    print("=== Validation ===")

    # Check shape
    print(f"Shape before: {df_before.shape}")
    print(f"Shape after: {df_after.shape}")
    assert df_before.shape == df_after.shape, "Shape mismatch!"

    # Check NaN
    print(f"\nNaN before: {df_before.isna().sum().sum()}")
    print(f"NaN after: {df_after.isna().sum().sum()}")

    # Check distribution
    print(f"\nBefore - Min: {df_before.min().min():.2f}, Max: {df_before.max().max():.2f}")
    print(f"After  - Min: {df_after.min().min():.2f}, Max: {df_after.max().max():.2f}")

    # Check correlation (should be high!)
    corr = df_before.corrwith(df_after, axis=0).mean()
    print(f"\nMean correlation: {corr:.4f}")
    if corr < 0.8:
        print("⚠️ WARNING: Low correlation! Check preprocessing.")

    print("\n✓ Validation complete")

# Usage
factor = cf.get_df('some_ratio')
factor_processed = preprocess_factor(factor, method='robust')
validate_preprocessing(factor, factor_processed)
```

---

## Common Patterns by Data Type

### Market Data (price, volume)

```python
# Price
close = cf.get_df('price_close')
close_clean = close.ffill().bfill()  # Missing values
close_final = winsorize(close_clean, 0.01, 0.99)  # Outliers

# Volume (log transform often helps)
# Use cf.search('volume') to find exact name for your universe
# kr_stock/id_stock: 'volume_sum'  |  us_stock/us_etf: 'trading_volume'
volume = cf.get_df('volume_sum')  # kr_stock example
volume_clean = volume.ffill().bfill()
log_volume = np.log1p(volume_clean)  # log(1 + x) handles 0
volume_final = zscore(log_volume)  # Normalize
```

### Ratio Factors (P/E, P/B, etc.)

```python
# Ratios often have extreme outliers
ratio = cf.get_df('some_ratio')
ratio_clean = ratio.ffill().bfill()
ratio_winsorized = winsorize(ratio_clean, 0.05, 0.95)  # 5%/95% for ratios
ratio_final = rank_normalize(ratio_winsorized)  # Rank is robust
```

### Financial Statement Factors

```python
# ROE, margins, etc. from get_fc()
roe = (cf.get_fc({
    'income': 'krx-spot-owners_of_parent_net_income',
    'equity': 'krx-spot-owners_of_parent_equity'
})
    .apply_rolling(4, 'sum', variables=['income'])
    .apply_rolling(4, 'mean', variables=['equity'])
    .apply_expression('income / equity')
    .to_wide())

# Already have NaN from financial reporting lag
roe_filled = roe.ffill()  # Forward fill (don't bfill - look-ahead!)
roe_clean = winsorize(roe_filled, 0.01, 0.99)
roe_final = zscore(roe_clean)
```

---

## See Also

- `framework.md` - Data quality principles
- `financial_calculator.md` - Financial data preprocessing
- `templates/examples/` - Complete examples
