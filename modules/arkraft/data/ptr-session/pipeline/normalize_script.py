"""
normalize_script.py  --  Congressional Trading Disclosures (STOCK Act)
Orientation : Long / Event-log
  - Each row = one trade-disclosure record filed by a US House or Senate member
  - date   = transaction_date (when the trade was executed)
  - entity = composite member-id + global row-index  (guarantees no (date,entity) dups
             while preserving the semantic member_id for Step 3 entity override)
  - values = amount_low, amount_high, amount_mid  (parsed from the range string)
"""

import os
import re
import json
import pandas as pd
from pathlib import Path

ARTIFACTS_DIR = Path(os.environ["ARTIFACTS_DIR"])
PIPELINE_DIR  = Path(os.environ["PIPELINE_DIR"])
INPUT_FILE    = ARTIFACTS_DIR / "input" / "history.csv"

# ── 1. Read ──────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")
raw_shape = list(df.shape)
print(f"Read {raw_shape[0]} rows x {raw_shape[1]} cols from {INPUT_FILE.name}")

# ── 2. Parse date columns ─────────────────────────────────────────────────────
df["transaction_date"]   = pd.to_datetime(df["transaction_date"],   format="%m/%d/%Y", errors="coerce")
df["notification_date"]  = pd.to_datetime(df["notification_date"],  format="%m/%d/%Y", errors="coerce")
# year_filed (Senate) looks like MM/DD/YYYY too
df["year_filed"]         = pd.to_datetime(df["year_filed"],         format="%m/%d/%Y", errors="coerce")

# ── 3. Parse amount range string → numeric columns ───────────────────────────
_amt_re = re.compile(r"[\$,]")

def parse_amount(val: str):
    """
    '1,001 - $15,000'  -> (1001.0, 15000.0, 8000.5)
    '$15,001 - $50,000' -> (15001.0, 50000.0, 32500.5)
    Returns (low, high, mid) as float or (None, None, None) on failure.
    """
    if pd.isna(val):
        return None, None, None
    parts = str(val).split(" - ")
    try:
        low  = float(_amt_re.sub("", parts[0]))
        high = float(_amt_re.sub("", parts[1])) if len(parts) > 1 else low
        mid  = (low + high) / 2.0
        return low, high, mid
    except Exception:
        return None, None, None

parsed = df["amount"].apply(parse_amount)
df["amount_low"]  = [p[0] for p in parsed]
df["amount_high"] = [p[1] for p in parsed]
df["amount_mid"]  = [p[2] for p in parsed]

# ── 4. Build member_id (semantic entity) ─────────────────────────────────────
def make_member_id(row):
    if row["chamber"] == "House":
        ln = str(row["last_name"]).strip()
        fn = str(row["first_name"]).strip()
        sd = str(row["state_district"]).strip()
        return f"H_{ln}_{fn}_{sd}"
    else:
        m = re.search(r"/ptr/([^/]+)/", str(row["pdf_url"]))
        uuid = m.group(1) if m else "unknown"
        return f"S_{uuid}"

df["member_id"] = df.apply(make_member_id, axis=1)

# ── 5. Build unique entity: member_id + global row index ─────────────────────
#   Guarantees (date, entity) uniqueness while embedding semantic member_id.
#   Step 3 (spec-generation) can override entity to use member_id directly
#   and handle collisions with dtype=dict.
df["entity"] = df["member_id"] + "__r" + df.index.astype(str)

# ── 6. Set date column ────────────────────────────────────────────────────────
df["date"] = df["transaction_date"]

# ── 7. Drop rows with null date (would make the record unindexable) ───────────
n_before = len(df)
df = df.dropna(subset=["date"])
n_dropped = n_before - len(df)
if n_dropped:
    print(f"WARNING: dropped {n_dropped} rows with null transaction_date")

# ── 8. Confirm no (date, entity) duplicates ───────────────────────────────────
n_dup = df.duplicated(subset=["date", "entity"]).sum()
assert n_dup == 0, f"(date, entity) still has {n_dup} duplicates — adjust entity key"

# ── 9. Cast numeric columns to float64 ───────────────────────────────────────
for col in ["amount_low", "amount_high", "amount_mid"]:
    df[col] = df[col].astype("float64")

# ── 10. Assemble preserved columns (everything useful beyond date/entity/values)
preserved_cols = [
    "member_id",        # coarser semantic entity candidate
    "chamber",          # House | Senate
    "asset_name",       # full asset description
    "ticker",           # exchange ticker (nullable)
    "asset_type",       # ST, GS, Stock, etc.
    "transaction_type", # Purchase, Sale, Sale (Full), etc.
    "transaction_date", # original event date
    "notification_date",# PIT for House: when disclosure was filed
    "year_filed",       # PIT for Senate: disclosure filing date
    "amount",           # original range string
    "cap_gains",        # bool flag
    "year",             # calendar year of the trade
    "last_name",        # House member last name (null for Senate)
    "first_name",       # House member first name (null for Senate)
    "state_district",   # House district code  (null for Senate)
    "doc_id",           # House filing document ID (null for Senate)
    "pdf_url",          # disclosure PDF URL (available for both)
    "filing_type",      # Senate filing type code
    "owner",            # Self | Spouse | Joint | Child (Senate)
]

# Build final long-format DataFrame
value_cols = ["amount_low", "amount_high", "amount_mid"]
output_cols = ["date", "entity"] + preserved_cols + value_cols

# Keep only columns that exist
output_cols = [c for c in output_cols if c in df.columns]
out_df = df[output_cols].copy()

# ── 11. Validate output ───────────────────────────────────────────────────────
assert "date"   in out_df.columns, "Missing 'date' column"
assert "entity" in out_df.columns, "Missing 'entity' column"
assert all(out_df[c].dtype == "float64" for c in value_cols), "Value columns must be float64"
assert out_df["date"].notna().all(), "date column has nulls"
print(f"Output shape: {out_df.shape}")
print(f"date range  : {out_df['date'].min().date()} to {out_df['date'].max().date()}")
print(f"unique members (member_id): {out_df['member_id'].nunique()}")
print(f"unique tickers: {out_df['ticker'].nunique()}")
print(f"value stats:\n{out_df[value_cols].describe()}")

# ── 12. Write normalized.parquet ─────────────────────────────────────────────
out_path = PIPELINE_DIR / "normalized.parquet"
out_df.to_parquet(out_path, index=False)
print(f"\nWrote normalized.parquet -> {out_path}  ({len(out_df)} rows)")

# ── 13. Build and write detection_report.json ────────────────────────────────
# Sample entities & dates for the report
sample_entities = sorted(out_df["member_id"].dropna().unique()[:10].tolist())
date_min = str(out_df["date"].min().date())
date_max = str(out_df["date"].max().date())
date_count = int(out_df["date"].nunique())

report = {
    "orientation": "long_event_log",
    "header_type": "single",
    "column_mapping": {
        "time":   "transaction_date",
        "entity": "entity (composite: member_id__r{row_idx})",
        "values": ["amount_low", "amount_high", "amount_mid"]
    },
    "normalization": {
        "method": "event_log_with_amount_parsing",
        "input_shape":  raw_shape,
        "output_shape": list(out_df.shape)
    },
    "detected_entities": sample_entities,
    "detected_dates": {
        "min":   date_min,
        "max":   date_max,
        "count": date_count
    },
    "preserved_columns": preserved_cols,
    "time_candidates": [
        {
            "column": "transaction_date",
            "role": "event_date",
            "pit_reasoning": (
                "The date the congressional member actually executed the trade. "
                "This is NOT publicly actionable on this date — disclosure happens later. "
                "Do not use as the PIT index."
            )
        },
        {
            "column": "notification_date",
            "role": "index",
            "pit_reasoning": (
                "House records only. The date the trade disclosure was filed with the Clerk "
                "of the House — first moment the trade is publicly observable. "
                "This is the true PIT date for House data."
            )
        },
        {
            "column": "year_filed",
            "role": "index",
            "pit_reasoning": (
                "Senate records only. The date the periodic transaction report (PTR) was "
                "filed with the Senate EFD system — first moment the trade is publicly "
                "observable. This is the true PIT date for Senate data."
            )
        }
    ],
    "entity_candidates": [
        {
            "column": "member_id",
            "unique_count": int(out_df["member_id"].nunique()),
            "id_pattern": "composite_key",
            "is_composite": True,
            "source_columns": ["chamber", "last_name", "first_name", "state_district", "pdf_url"],
            "notes": (
                "Semantic legislator/filing identifier. "
                "House: 'H_{last_name}_{first_name}_{district}' (6 unique members). "
                "Senate: 'S_{filing_uuid}' (89 unique filings; senator name unavailable). "
                "Collision rate >50% at (transaction_date, member_id) — "
                "multiple trades per member per day is expected. "
                "Spec step should use dtype='dict'."
            )
        },
        {
            "column": "ticker",
            "unique_count": int(out_df["ticker"].dropna().nunique()),
            "id_pattern": "ticker",
            "is_composite": False,
            "source_columns": ["ticker"],
            "notes": "Exchange ticker symbol. 97 nulls (bonds, funds, non-public assets)."
        },
        {
            "column": "state_district",
            "unique_count": int(out_df["state_district"].dropna().nunique()),
            "id_pattern": "custom",
            "is_composite": False,
            "source_columns": ["state_district"],
            "notes": "House congressional district code (AL04, GA12, …). Null for all Senate rows."
        }
    ],
    "event_log_notes": (
        "This is a STOCK Act congressional trade disclosure dataset. "
        "Each row is an independent trade event. "
        "There is no traditional time-series entity — (date, member) collisions are "
        "inherent (>50% collision rate). "
        "The composite entity key 'member_id__r{row_idx}' ensures (date,entity) uniqueness "
        "for the normalized parquet while preserving member_id for Step 3 override. "
        "Step 3 should override entity to member_id and set dtype='dict' on value columns."
    )
}

report_path = PIPELINE_DIR / "detection_report.json"
with open(report_path, "w") as f:
    json.dump(report, f, indent=2)
print(f"Wrote detection_report.json -> {report_path}")
print("\nDone.")
