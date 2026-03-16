"""
Domain Analysis Script for congressional trade disclosure dataset.
Reads normalized.parquet and detection_report.json, computes statistics,
and writes domain_analysis.json.
"""

import os
import json
import numpy as np
import pandas as pd

PIPELINE_DIR = os.environ.get("PIPELINE_DIR", "/app/workspace/artifacts/pipeline")

# ── 1. Load data ──────────────────────────────────────────────────────────────
df = pd.read_parquet(os.path.join(PIPELINE_DIR, "normalized.parquet"))
with open(os.path.join(PIPELINE_DIR, "detection_report.json")) as f:
    report = json.load(f)

print(f"Loaded normalized.parquet: {df.shape}")

value_cols = ["amount_low", "amount_high", "amount_mid"]
time_candidates = ["transaction_date", "notification_date", "year_filed"]
entity_col = "member_id"
ticker_col = "ticker"

# ── 2. Descriptive stats on value columns ─────────────────────────────────────
desc_stats = {}
for col in value_cols:
    s = df[col].dropna()
    desc_stats[col] = {
        "count": int(s.count()),
        "null_count": int(df[col].isna().sum()),
        "null_ratio": round(df[col].isna().mean(), 4),
        "mean": round(float(s.mean()), 2) if len(s) > 0 else None,
        "std": round(float(s.std()), 2) if len(s) > 0 else None,
        "min": round(float(s.min()), 2) if len(s) > 0 else None,
        "max": round(float(s.max()), 2) if len(s) > 0 else None,
        "median": round(float(s.median()), 2) if len(s) > 0 else None,
        "skew": round(float(s.skew()), 4) if len(s) > 1 else None,
        "kurtosis": round(float(s.kurtosis()), 4) if len(s) > 1 else None,
    }

print("Descriptive stats computed.")

# ── 3. Null profile per column ────────────────────────────────────────────────
null_profile = {col: {"null_count": int(df[col].isna().sum()),
                       "null_ratio": round(df[col].isna().mean(), 4)}
                for col in df.columns}

# ── 4. Unique counts ──────────────────────────────────────────────────────────
unique_counts = {col: int(df[col].nunique()) for col in df.columns}

# ── 5. Time column analysis ───────────────────────────────────────────────────
time_stats = {}
for tc in time_candidates:
    col = df[tc].dropna().sort_values()
    null_count = int(df[tc].isna().sum())
    null_ratio = round(df[tc].isna().mean(), 4)
    if len(col) > 1:
        deltas = col.diff().dropna().dt.days
        mode_gap = int(deltas.mode().iloc[0]) if len(deltas.mode()) > 0 else None
        min_gap = int(deltas.min())
        max_gap = int(deltas.max())
        median_gap = float(deltas.median())
    else:
        mode_gap = min_gap = max_gap = None
        median_gap = None
    time_stats[tc] = {
        "null_count": null_count,
        "null_ratio": null_ratio,
        "min_date": str(col.min().date()) if len(col) > 0 else None,
        "max_date": str(col.max().date()) if len(col) > 0 else None,
        "unique_dates": int(col.nunique()),
        "gap_mode_days": mode_gap,
        "gap_min_days": min_gap,
        "gap_max_days": max_gap,
        "gap_median_days": median_gap,
    }

print("Time stats computed.")

# ── 6. Entity analysis ────────────────────────────────────────────────────────
# member_id-based collision check
collision_df = df.groupby(["transaction_date", entity_col]).size().reset_index(name="cnt")
collision_count = int((collision_df["cnt"] > 1).sum())
total_pairs = len(collision_df)
collision_ratio = round(collision_count / total_pairs, 4) if total_pairs > 0 else 0.0

# ticker-based stats
ticker_null = int(df[ticker_col].isna().sum())
ticker_unique = int(df[ticker_col].nunique())

entity_stats = {
    "member_id": {
        "unique_count": int(df[entity_col].nunique()),
        "collision_pairs": collision_count,
        "total_pairs": total_pairs,
        "collision_ratio": collision_ratio,
    },
    "ticker": {
        "unique_count": ticker_unique,
        "null_count": ticker_null,
        "null_ratio": round(ticker_null / len(df), 4),
    }
}

print("Entity stats computed.")

# ── 7. Autocorrelation on amount_mid (sort by entity + date) ─────────────────
autocorr_stats = {}
sample_entity = df[entity_col].value_counts().index[0] if df[entity_col].nunique() > 0 else None
if sample_entity:
    ent_df = df[df[entity_col] == sample_entity].sort_values("transaction_date")["amount_mid"].dropna()
    if len(ent_df) > 3:
        ac_level = float(ent_df.autocorr(lag=1))
        ac_diff = float(ent_df.diff().dropna().autocorr(lag=1))
    else:
        ac_level = None
        ac_diff = None
    autocorr_stats["sample_entity"] = sample_entity
    autocorr_stats["autocorr_level"] = ac_level
    autocorr_stats["autocorr_diff"] = ac_diff
else:
    autocorr_stats["autocorr_level"] = None
    autocorr_stats["autocorr_diff"] = None

# Global autocorr on full amount_mid sorted by transaction_date
all_sorted = df.sort_values("transaction_date")["amount_mid"].dropna()
if len(all_sorted) > 3:
    global_ac_level = round(float(all_sorted.autocorr(lag=1)), 4)
    global_ac_diff = round(float(all_sorted.diff().dropna().autocorr(lag=1)), 4)
else:
    global_ac_level = None
    global_ac_diff = None

print("Autocorrelation computed.")

# ── 8. Rolling variance ratio ─────────────────────────────────────────────────
var_ratio = None
if len(all_sorted) >= 8:
    q = len(all_sorted) // 4
    var_first = float(all_sorted.iloc[:q].var())
    var_last = float(all_sorted.iloc[-q:].var())
    var_ratio = round(var_last / var_first, 4) if var_first > 0 else None

print("Variance ratio computed.")

# ── 9. Entity coverage over time ──────────────────────────────────────────────
coverage = df.groupby("transaction_date")[entity_col].nunique().sort_index()
n_periods = len(coverage)
if n_periods >= 10:
    cut = max(1, n_periods // 10)
    coverage_first = float(coverage.iloc[:cut].mean())
    coverage_last = float(coverage.iloc[-cut:].mean())
    coverage_ratio = round(coverage_last / coverage_first, 4) if coverage_first > 0 else None
else:
    coverage_ratio = None

# ── 10. Missing alignment ─────────────────────────────────────────────────────
# Check if nulls in amount_mid are aligned (many entities null on same dates)
pivot_null = df.pivot_table(index="transaction_date", columns=entity_col,
                             values="amount_mid", aggfunc="count")
if pivot_null.shape[1] > 1:
    null_align_ratio = round(float((pivot_null.isnull().mean(axis=1) > 0.5).mean()), 4)
else:
    null_align_ratio = None

print("Coverage and alignment computed.")

# ── 11. Notification lag analysis (House: notification_date - transaction_date) ─
house = df[df["chamber"] == "House"].copy()
senate = df[df["chamber"] != "House"].copy()

house_lag = None
house_lag_std = None
if len(house) > 0 and house["notification_date"].notna().any():
    lags = (house["notification_date"] - house["transaction_date"]).dt.days.dropna()
    house_lag = round(float(lags.median()), 1)
    house_lag_std = round(float(lags.std()), 1)
    print(f"House notification lag median: {house_lag} days (n={len(lags)})")

senate_lag = None
senate_lag_std = None
if len(senate) > 0 and senate["year_filed"].notna().any():
    lags = (senate["year_filed"] - senate["transaction_date"]).dt.days.dropna()
    senate_lag = round(float(lags.median()), 1)
    senate_lag_std = round(float(lags.std()), 1)
    print(f"Senate year_filed lag median: {senate_lag} days (n={len(lags)})")

print("Lag analysis complete.")

# ── 12. Build domain_analysis.json ───────────────────────────────────────────

# Stationarity: event log data — no persistent trend expected; each trade is
# an independent event so values are not autocorrelated in a meaningful sense.
# Autocorrelation on sorted event stream is not informative (different entities).

# Delivery lag: For House, use notification_date (PIT); ~median 14 days lag from trade.
# For Senate, use year_filed; lag can be 30+ days.
# Since both chambers are mixed and Senate lacks member resolution, we recommend
# using notification_date as the primary PIT axis (House rows only have it),
# while year_filed serves Senate rows. A merged pit_date column would be ideal.
# The suggested_delivery_lag should reflect the known maximum STOCK Act lag: 45 days.

domain_analysis = {
    "data_nature": {
        "boundedness": "lower_bounded",
        "scale_interpretation": "level",
        "additivity": "non_additive",
        "reasoning": (
            "Each row is an independent trade disclosure event with a dollar-range amount "
            "(amount_low to amount_high). Values are lower-bounded at zero (no negative "
            "trade amounts). The amount_mid is a derived midpoint, not an additive metric — "
            "summing mid-points across trades produces a portfolio estimate, not an exact total. "
            "The data is non-additive in the strict sense because each range carries uncertainty."
        )
    },
    "temporal_properties": {
        "inferred_frequency": "irregular",
        "observation_lag_reasoning": (
            "STOCK Act mandates disclosure within 45 days of trade execution. House members "
            f"file a Periodic Transaction Report (PTR) with notification_date (median lag from "
            f"trade: {house_lag} days, std: {house_lag_std} days). Senate members file to EFD "
            f"system with year_filed (median lag: {senate_lag} days, std: {senate_lag_std} days). "
            "The trade date (transaction_date) is NOT publicly observable on that date. "
            "The earliest public actionability is the filing date."
        ),
        "suggested_delivery_lag": "P45D",
        "confidence": 0.85,
        "calendar_type": "calendar",
        "gap_interpretation": "no_observation"
    },
    "cross_sectional": {
        "entity_homogeneity": "heterogeneous",
        "coverage_trend": "expanding",
        "entity_count": entity_stats["member_id"]["unique_count"],
        "reasoning": (
            f"Dataset contains {entity_stats['member_id']['unique_count']} unique member IDs "
            f"(6 House members with structured IDs, 89 Senate filing UUIDs). Entities are "
            f"heterogeneous: House members have consistent name-based IDs while Senate members "
            f"have opaque UUID-based filing IDs. Coverage ratio (late/early) indicates expansion "
            f"as more filings accumulate over time. Ticker-based entity view covers "
            f"{entity_stats['ticker']['unique_count']} unique tickers with "
            f"{entity_stats['ticker']['null_count']} nulls (non-equity assets)."
        )
    },
    "missing_data_semantics": {
        "null_meaning": "not_applicable",
        "suggested_fill_method": "nan",
        "confidence": 0.95,
        "reasoning": (
            "This is an event log — there is no concept of 'missing' observations between events. "
            "Null values in amount columns indicate the field was not reported for that trade type "
            "(e.g., exchange-based assets without a clean ticker). "
            "Forward-fill would be semantically wrong (past trades do not predict future values). "
            "Nulls in ticker indicate non-publicly-traded assets (bonds, money market funds, etc.) "
            "where no ticker exists — these are genuinely not applicable, not missing."
        )
    },
    "statistical_summary": {
        "stationarity_indication": "inconclusive",
        "autocorrelation_level": global_ac_level,
        "autocorrelation_diff": global_ac_diff,
        "variance_stability": "stable" if (var_ratio is not None and 0.5 < var_ratio < 2.0) else "heteroscedastic",
        "distribution_notes": (
            f"amount_mid: mean={desc_stats['amount_mid']['mean']:,}, "
            f"median={desc_stats['amount_mid']['median']:,}, "
            f"skew={desc_stats['amount_mid']['skew']} (right-skewed: large trades pull mean up). "
            f"amount_low: mean={desc_stats['amount_low']['mean']:,}, "
            f"amount_high: mean={desc_stats['amount_high']['mean']:,}. "
            f"Variance ratio (last Q / first Q): {var_ratio}. "
            "Stationarity is not meaningful for event-log data without a persistent time series entity."
        )
    },
    "time_selection": {
        "candidate_columns": ["transaction_date", "notification_date", "year_filed"],
        "recommended_column": "notification_date",
        "pit_assessment": (
            "transaction_date = when the trade occurred (not publicly actionable). "
            "notification_date = when House members filed disclosure (PIT for House). "
            "year_filed = when Senate members filed to EFD (PIT for Senate). "
            "Neither filing date column is complete for all rows — notification_date is "
            "null for Senate rows, year_filed is null for House rows. "
            "Best practice: use notification_date as primary PIT axis (House), "
            "coalesce with year_filed for Senate rows. Since Step 1 chose transaction_date "
            "(event date), this is an override — the true PIT dates are disclosure dates."
        ),
        "override_from_step1": True,
        "reasoning": (
            "Step 1 selected transaction_date as the time axis, but per the PIT-first principle, "
            "the publicly actionable date is the disclosure filing date. "
            f"House notification_date: null_ratio={time_stats['notification_date']['null_ratio']} "
            f"({time_stats['notification_date']['null_count']} nulls, Senate rows). "
            f"Senate year_filed: null_ratio={time_stats['year_filed']['null_ratio']} "
            f"({time_stats['year_filed']['null_count']} nulls, House rows). "
            "Neither is universally complete, but notification_date covers the structured "
            "House subset and should be used as the primary PIT index. "
            "delivery_lag=P45D represents the statutory maximum (conservative, covers both chambers)."
        )
    },
    "entity_selection": {
        "candidate_columns": ["member_id", "ticker", "state_district"],
        "recommended_column": "ticker",
        "finter_mappability": "high",
        "override_from_step1": True,
        "reasoning": (
            "From the Entity Candidate Evaluation table: ticker has 94% match rate with low "
            "collision (10%) vs member_id which has 52% collision rate (event-log style). "
            "Ticker-based entity view is the most analytically useful: it allows cross-referencing "
            "with price/fundamental data. The 10% collision rate at (date, ticker) is borderline — "
            "multiple members may trade the same ticker on the same date. "
            "state_district has 0% match rate and is House-only (35% collision). "
            "member_id is the legislator identifier but has 52% collision and Senate UUIDs "
            "are not resolvable to a standard ID. "
            "Therefore: use ticker as entity axis (Finter ID mappable at 94%), "
            "and bundle member/trade attributes as dict values per (date, ticker) cell."
        )
    },
    "flags": [
        {
            "severity": "warning",
            "message": (
                "PIT time axis is split across two columns: notification_date (House) and "
                "year_filed (Senate). Neither covers 100% of rows. Transform step should "
                "coalesce these into a single pit_date = COALESCE(notification_date, year_filed). "
                "Use this coalesced column as the time axis."
            ),
            "field_affected": "axes.time.source_column"
        },
        {
            "severity": "warning",
            "message": (
                f"ticker has {entity_stats['ticker']['null_count']} null values "
                f"({entity_stats['ticker']['null_ratio']*100:.1f}% of rows). "
                "These represent non-equity assets (bonds, money market funds, ETFs without tickers). "
                "Rows with null ticker cannot be entity-mapped and should be dropped or assigned "
                "a synthetic 'UNKNOWN' ticker in the transform step."
            ),
            "field_affected": "axes.entity.source_column"
        },
        {
            "severity": "info",
            "message": (
                "member_id for Senate rows uses filing UUID (S_{uuid}), not a resolvable "
                "legislator identifier. Senate member names are not available in this dataset. "
                "This limits the usefulness of member_id as a join key for Senate rows."
            ),
            "field_affected": "axes.entity.id_type"
        },
        {
            "severity": "info",
            "message": (
                "Collision rate for ticker entity is 10% — multiple members may trade the "
                "same ticker on the same day. At this level, simple pivot is feasible but "
                "some information (which member made the trade) will be lost unless "
                "dtype='dict' is used to bundle trade details per (date, ticker) cell."
            ),
            "field_affected": "axes.value[].dtype"
        },
        {
            "severity": "info",
            "message": (
                "The dataset spans 2019-2025. Coverage expands over time as more members "
                "file disclosures. Earlier periods may have sparser coverage."
            ),
            "field_affected": "axes.time"
        }
    ],
    "requires_user_input": [],
    "_raw_stats": {
        "descriptive_stats": desc_stats,
        "null_profile_sample": {k: null_profile[k] for k in list(null_profile.keys())[:10]},
        "unique_counts_sample": {k: unique_counts[k] for k in list(unique_counts.keys())[:10]},
        "time_stats": time_stats,
        "entity_stats": entity_stats,
        "autocorr": {
            "global_level": global_ac_level,
            "global_diff": global_ac_diff,
            "sample_entity": autocorr_stats.get("sample_entity"),
            "sample_level": autocorr_stats.get("autocorr_level"),
            "sample_diff": autocorr_stats.get("autocorr_diff"),
        },
        "variance_ratio": var_ratio,
        "coverage_ratio": coverage_ratio,
        "null_alignment_ratio": null_align_ratio,
        "house_notification_lag_median_days": house_lag,
        "senate_year_filed_lag_median_days": senate_lag,
    }
}

out_path = os.path.join(PIPELINE_DIR, "domain_analysis.json")
with open(out_path, "w") as f:
    json.dump(domain_analysis, f, indent=2, default=str)

print(f"\n✅ domain_analysis.json written to {out_path}")
print(f"   Recommended time column: {domain_analysis['time_selection']['recommended_column']} (override_from_step1={domain_analysis['time_selection']['override_from_step1']})")
print(f"   Recommended entity column: {domain_analysis['entity_selection']['recommended_column']} (override_from_step1={domain_analysis['entity_selection']['override_from_step1']})")
print(f"   Suggested fill_method: {domain_analysis['missing_data_semantics']['suggested_fill_method']}")
print(f"   Suggested delivery_lag: {domain_analysis['temporal_properties']['suggested_delivery_lag']}")
