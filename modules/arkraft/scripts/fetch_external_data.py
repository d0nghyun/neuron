"""Fetch external financial data sources → CSV for DW validation.

Sources: Fama-French, yfinance, FRED
Output: modules/arkraft/data/external/{source}/{name}.csv
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "external"
START = "2000-01-01"
END = datetime.now().strftime("%Y-%m-%d")


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ─── Fama-French ───────────────────────────────────────────────
def fetch_fama_french():
    """Download FF 3-factor, 5-factor, momentum from Ken French's site."""
    import pandas_datareader.data as web

    dst = OUT_DIR / "fama_french"
    datasets = {
        "ff3_daily": "F-F_Research_Data_Factors_daily",
        "ff5_daily": "F-F_Research_Data_5_Factors_2x3_daily",
        "momentum_daily": "F-F_Momentum_Factor_daily",
    }

    for name, ds_name in datasets.items():
        log(f"FF: {name} ...")
        try:
            df = web.DataReader(ds_name, "famafrench", start=START)[0]
            df.index = pd.to_datetime(df.index.astype(str))
            df = df[df.index >= START]
            # Values are in percent, keep as-is for now (user can decide)
            out_path = dst / f"{name}.csv"
            df.to_csv(out_path)
            log(f"  → {out_path.name}: {df.shape} ({df.index.min().date()} ~ {df.index.max().date()})")
        except Exception as e:
            log(f"  ✗ {name} failed: {e}")


# ─── yfinance ──────────────────────────────────────────────────
def fetch_yfinance():
    """Download major benchmarks, ETFs, Korea indices via yfinance."""
    import yfinance as yf

    dst = OUT_DIR / "yfinance"

    # Real-world quant benchmark universe
    tickers = {
        # US Equity
        "SPY": "S&P 500 ETF",
        "QQQ": "NASDAQ 100 ETF",
        "IWM": "Russell 2000 ETF",
        # International
        "EFA": "MSCI EAFE ETF",
        "EEM": "MSCI EM ETF",
        "EWY": "Korea ETF",
        # Fixed Income
        "TLT": "20+ Year Treasury ETF",
        "IEF": "7-10 Year Treasury ETF",
        "HYG": "High Yield Corp Bond ETF",
        # Commodities
        "GLD": "Gold ETF",
        "USO": "Oil ETF",
        # Volatility
        "^VIX": "VIX Index",
        # Korea
        "^KS11": "KOSPI",
        "^KQ11": "KOSDAQ",
    }

    # Batch download OHLCV
    ticker_list = list(tickers.keys())
    log(f"yfinance: downloading {len(ticker_list)} tickers ...")
    raw = yf.download(ticker_list, start=START, end=END, auto_adjust=True, progress=False)

    # Save per-field CSVs (CM format: datetime × ticker)
    for field in ["Close", "Volume", "High", "Low", "Open"]:
        if field in raw.columns.get_level_values(0):
            df = raw[field]
            if isinstance(df, pd.Series):
                df = df.to_frame()
            # Clean column names (remove ^ prefix)
            df.columns = [c.replace("^", "") for c in df.columns]
            out_path = dst / f"benchmarks_{field.lower()}.csv"
            df.to_csv(out_path)
            log(f"  → {out_path.name}: {df.shape}")

    # Also save individual ticker metadata
    meta = pd.DataFrame([
        {"ticker": k, "name": v} for k, v in tickers.items()
    ])
    meta.to_csv(dst / "ticker_meta.csv", index=False)
    log(f"  → ticker_meta.csv: {len(meta)} tickers")


# ─── FRED ──────────────────────────────────────────────────────
def fetch_fred():
    """Download key macro indicators from FRED via direct CSV URL."""
    import time
    import requests

    dst = OUT_DIR / "fred"

    series = {
        "DFF": "Fed Funds Rate",
        "DGS10": "10-Year Treasury Yield",
        "DGS2": "2-Year Treasury Yield",
        "T10Y2Y": "10Y-2Y Yield Spread",
        "CPIAUCSL": "CPI (All Urban)",
        "UNRATE": "Unemployment Rate",
        "DEXKOUS": "KRW/USD Exchange Rate",
        "VIXCLS": "VIX (CBOE)",
        "BAMLH0A0HYM2": "HY OAS Spread",
        "DCOILWTICO": "WTI Crude Oil",
        "GOLDPMGBD228NLBM": "Gold Price London PM Fix",
        "M2SL": "M2 Money Supply",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept": "text/csv",
    }

    results = []
    for series_id, desc in series.items():
        log(f"FRED: {series_id} ({desc}) ...")
        url = (
            f"https://fred.stlouisfed.org/graph/fredgraph.csv"
            f"?id={series_id}&cosd={START}&coed={END}"
        )
        try:
            resp = requests.get(url, timeout=60, headers=headers)
            resp.raise_for_status()
            out_path = dst / f"{series_id}.csv"
            out_path.write_text(resp.text)

            # FRED uses observation_date as column name
            df = pd.read_csv(out_path)
            date_col = [c for c in df.columns if "date" in c.lower()][0]
            val_col = [c for c in df.columns if c != date_col][0]
            df = df.rename(columns={date_col: "date", val_col: "value"})
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date")
            df = df[df["value"] != "."]
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna()
            df.to_csv(out_path)
            results.append({
                "series": series_id,
                "desc": desc,
                "rows": len(df),
                "start": str(df.index.min().date()) if len(df) > 0 else "N/A",
                "end": str(df.index.max().date()) if len(df) > 0 else "N/A",
            })
            log(f"  → {series_id}.csv: {len(df)} rows ({results[-1]['start']} ~ {results[-1]['end']})")
        except Exception as e:
            log(f"  ✗ {series_id} failed: {e}")
            results.append({"series": series_id, "desc": desc, "rows": 0, "start": "FAILED", "end": ""})
        time.sleep(1)  # rate limit courtesy

    pd.DataFrame(results).to_csv(dst / "series_meta.csv", index=False)


# ─── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    log(f"Output: {OUT_DIR}")
    log(f"Period: {START} ~ {END}")
    print("=" * 60)

    fetch_fama_french()
    print("-" * 60)
    fetch_yfinance()
    print("-" * 60)
    fetch_fred()

    print("=" * 60)
    # Summary
    csv_files = list(OUT_DIR.rglob("*.csv"))
    total_size = sum(f.stat().st_size for f in csv_files)
    log(f"Done! {len(csv_files)} CSV files, {total_size / 1024 / 1024:.1f} MB total")
    for f in sorted(csv_files):
        rel = f.relative_to(OUT_DIR)
        size_kb = f.stat().st_size / 1024
        log(f"  {rel} ({size_kb:.0f} KB)")
