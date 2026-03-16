import os
import json
from pathlib import Path

import numpy as np
import pandas as pd

ARTIFACTS_DIR = Path(os.environ["ARTIFACTS_DIR"])
PIPELINE_DIR = Path(os.environ["PIPELINE_DIR"])


class NumpySafeEncoder(json.JSONEncoder):
    """JSON encoder that handles numpy types (int64, float64, bool_, etc.)."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (pd.Timestamp,)):
            return obj.isoformat()
        if obj is pd.NaT:
            return None
        return super().default(obj)


# ── 1. Load inputs ──────────────────────────────────────────────────────────
print("Loading spec.json …")
with open(PIPELINE_DIR / "spec.json") as f:
    spec = json.load(f)

print("Loading normalized.parquet …")
df = pd.read_parquet(PIPELINE_DIR / "normalized.parquet")
print(f"  Input shape: {df.shape}")

# ── 2. Parse spec axes ───────────────────────────────────────────────────────
time_col_src   = spec["axes"]["time"]["source_column"]   # "pit_date" (derived)
entity_col_src = spec["axes"]["entity"]["source_column"] # "ticker"
value_entries  = spec["axes"]["value"]                   # list of value defs

print(f"  Time source column : {time_col_src}")
print(f"  Entity source column: {entity_col_src}")
print(f"  Value entries: {[v['cm_name'] for v in value_entries]}")

# ── 3. Derive pit_date = COALESCE(notification_date, year_filed) ─────────────
# House filings: notification_date is set, year_filed is NaT
# Senate filings: year_filed is set, notification_date is NaT
print("Deriving pit_date …")
df["pit_date"] = df["notification_date"].fillna(df["year_filed"])
n_null_pit = df["pit_date"].isna().sum()
print(f"  pit_date nulls after COALESCE: {n_null_pit}")
if n_null_pit > 0:
    print(f"  WARNING: {n_null_pit} rows have no pit_date — dropping.")
    df = df[df["pit_date"].notna()].copy()

# Normalise to date-only (no time component)
df["pit_date"] = pd.to_datetime(df["pit_date"]).dt.normalize()

# ── 4. Drop rows with null ticker ────────────────────────────────────────────
n_before = len(df)
df = df[df[entity_col_src].notna() & (df[entity_col_src] != "")].copy()
n_dropped_ticker = n_before - len(df)
print(f"  Dropped {n_dropped_ticker} rows with null/empty ticker")

# Ensure ticker is string (preserve leading zeros if any)
df[entity_col_src] = df[entity_col_src].astype(str)

# ── 5. Process each value entry ─────────────────────────────────────────────
output_files   = []
value_col_names = []
total_null_filled = 0
total_dups_removed = 0

for val_entry in value_entries:
    cm_name      = val_entry["cm_name"]
    dtype        = val_entry.get("dtype", "float64")
    dict_columns = val_entry.get("dict_columns", [])

    print(f"\nProcessing value '{cm_name}' (dtype={dtype}) …")

    if dtype == "dict":
        # ── 5a. Aggregate dict_columns into JSON array per (pit_date, ticker) ─
        # Only keep columns that actually exist in the DataFrame
        available_dict_cols = [c for c in dict_columns if c in df.columns]
        missing_cols = set(dict_columns) - set(available_dict_cols)
        if missing_cols:
            print(f"  WARNING: dict_columns missing from data: {missing_cols}")

        def aggregate_to_json(group_df):
            """Convert each row in the group to a dict, collect into JSON array."""
            records = []
            for _, row in group_df[available_dict_cols].iterrows():
                rec = {}
                for col in available_dict_cols:
                    val = row[col]
                    # Sanitise: NaN/NaT → None
                    if val is pd.NaT or (isinstance(val, float) and np.isnan(val)):
                        rec[col] = None
                    elif isinstance(val, (np.integer,)):
                        rec[col] = int(val)
                    elif isinstance(val, (np.floating,)):
                        rec[col] = float(val)
                    else:
                        rec[col] = val
                records.append(rec)
            return json.dumps(records, ensure_ascii=False)

        print(f"  Aggregating {len(available_dict_cols)} dict columns into JSON arrays …")
        grouped = (
            df.groupby(["pit_date", entity_col_src], sort=False)
            .apply(aggregate_to_json, include_groups=False)
            .reset_index()
        )
        grouped.columns = ["pit_date", "ticker", "trade_details"]

        print(f"  Grouped rows: {len(grouped)}")

        # ── 5b. Pivot to 2D ────────────────────────────────────────────────
        pivot_df = grouped.pivot_table(
            index="pit_date",
            columns="ticker",
            values="trade_details",
            aggfunc="last",  # duplicate (date, ticker) → keep last
        )

        # Reset column axis name (remove 'ticker' label from column axis)
        pivot_df.columns.name = None

        # Ensure DatetimeIndex
        pivot_df.index = pd.to_datetime(pivot_df.index)
        pivot_df = pivot_df.sort_index()

        # String columns (object dtype) — no float casting needed for dict
        print(f"  Pivot shape: {pivot_df.shape}")

    else:
        # ── 5c. Numeric pivot ──────────────────────────────────────────────
        src_col = val_entry.get("source_column", cm_name)
        if src_col not in df.columns:
            print(f"  ERROR: source_column '{src_col}' not found in data. Skipping.")
            continue

        pivot_df = df.pivot_table(
            index="pit_date",
            columns=entity_col_src,
            values=src_col,
            aggfunc="last",
        )
        pivot_df.columns.name = None
        pivot_df.index = pd.to_datetime(pivot_df.index)
        pivot_df = pivot_df.sort_index()
        pivot_df = pivot_df.astype("float64")
        print(f"  Pivot shape: {pivot_df.shape}")

    # ── 6. Validation ────────────────────────────────────────────────────────
    assert not pivot_df.empty, f"[{cm_name}] Empty DataFrame after pivot"
    assert isinstance(pivot_df.index, pd.DatetimeIndex), \
        f"[{cm_name}] Index is not DatetimeIndex"
    assert not isinstance(pivot_df.columns, pd.MultiIndex), \
        f"[{cm_name}] Columns are MultiIndex — forbidden"
    assert pivot_df.index.is_monotonic_increasing, \
        f"[{cm_name}] Index is not sorted"
    assert pivot_df.index.is_unique, \
        f"[{cm_name}] Duplicate dates in index"

    # Column-name cleanliness (no tuple strings, no metric prefixes)
    bad_cols = [
        c for c in pivot_df.columns
        if str(c).startswith("(") or "/" in str(c) or " - " in str(c)
    ]
    assert not bad_cols, f"[{cm_name}] Bad column names: {bad_cols[:5]}"

    # ── 7. Save parquet ──────────────────────────────────────────────────────
    out_path = ARTIFACTS_DIR / f"{cm_name}.parquet"
    pivot_df.to_parquet(out_path, index=True)
    print(f"  ✓ Saved → {out_path}")
    print(f"    Dates: {pivot_df.index[0].date()} → {pivot_df.index[-1].date()}")
    print(f"    Entities: {pivot_df.shape[1]}  |  Dates: {pivot_df.shape[0]}")

    output_files.append(f"{cm_name}.parquet")
    value_col_names.append(cm_name)

    # Count NaN cells for report
    total_null_filled += int(pivot_df.isna().sum().sum())

# ── 8. Write transform.json ──────────────────────────────────────────────────
# Reload last pivot for summary stats (single value here)
last_pivot = pd.read_parquet(ARTIFACTS_DIR / output_files[-1])

transform_meta = {
    "status": "success",
    "input_rows": int(len(pd.read_parquet(PIPELINE_DIR / "normalized.parquet"))),
    "output_rows": int(last_pivot.shape[0]),
    "output_columns": int(last_pivot.shape[1]),
    "value_columns": value_col_names,
    "output_files": output_files,
    "entity_count": int(last_pivot.shape[1]),
    "date_range": [
        last_pivot.index[0].strftime("%Y-%m-%d"),
        last_pivot.index[-1].strftime("%Y-%m-%d"),
    ],
    "dropped_rows": int(n_dropped_ticker + (n_null_pit if n_null_pit > 0 else 0)),
    "null_filled": total_null_filled,
    "duplicates_removed": total_dups_removed,
}

with open(PIPELINE_DIR / "transform.json", "w") as f:
    json.dump(transform_meta, f, indent=2, ensure_ascii=False, cls=NumpySafeEncoder)

print(f"\n✓ transform.json written → {PIPELINE_DIR / 'transform.json'}")
print(json.dumps(transform_meta, indent=2, cls=NumpySafeEncoder))
print("\n✅ Transform complete.")
