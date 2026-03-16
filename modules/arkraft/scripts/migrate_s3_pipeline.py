#!/usr/bin/env python3
"""S3 migration: pipeline/ → subdirectories (logs/, scripts/, spec/, reports/, analysis/, data/)

Migrates existing session artifacts from flat pipeline/ structure to the new
subdirectory structure. Dry-run by default; pass --execute to apply changes.

Usage:
    python migrate_s3_pipeline.py                  # dry-run, all sessions
    python migrate_s3_pipeline.py --execute         # apply migration
    python migrate_s3_pipeline.py --session <id>    # single session
"""
import argparse
import fnmatch
import re
import sys
from collections import defaultdict

import boto3

BUCKET = "arkraft-production"
TEAM_ID = "9c8a1efb-633b-464e-9fff-ab99f0c84e3c"
DATASETS_PREFIX = f"teams/{TEAM_ID}/datasets/"

# Exact filename → new subdirectory mapping
FILE_MAP: dict[str, str] = {
    # scripts/
    "normalize_script.py": "scripts/normalize_script.py",
    "transform_script.py": "scripts/transform_script.py",
    # reports/
    "detection_report.json": "reports/detection_report.json",
    "readiness.json": "reports/readiness.json",
    "transform.json": "reports/transform.json",
    "register.json": "reports/register.json",
    "incremental_recipe.json": "reports/incremental_recipe.json",
    # spec/
    "spec.json": "spec/spec.json",
    "input_request.json": "spec/input_request.json",
    "user_answers.json": "spec/user_answers.json",
    "answer_history.json": "spec/answer_history.json",
    "matching_result.json": "spec/matching_result.json",
    "domain_analysis.json": "spec/domain_analysis.json",
    "domain_context.json": "spec/domain_context.json",
    # data/
    "normalized.parquet": "data/normalized.parquet",
    # logs/
    "active_log.json": "logs/active_log.json",
    "run_metrics.json": "logs/run_metrics.json",
    "script_profiles.json": "logs/script_profiles.json",
    # analysis/
    "analysis_report.json": "analysis/analysis_report.json",
    "review_notes.json": "analysis/review_notes.json",
    "data_profile.json": "analysis/data_profile.json",
    "catalog_data.parquet": "analysis/catalog_data.parquet",
}

# Pattern-based mappings (checked in order)
PATTERN_MAP: list[tuple[str, str]] = [
    ("section_*.json", "analysis/"),
]


def resolve_destination(filename: str) -> str:
    """Map a pipeline/ filename to its new subdirectory path."""
    # 1. Exact match
    if filename in FILE_MAP:
        return FILE_MAP[filename]

    # 2. Pattern match (e.g. section_*.json → analysis/)
    for pattern, dest_dir in PATTERN_MAP:
        if fnmatch.fnmatch(filename, pattern):
            return f"{dest_dir}{filename}"

    # 3. Fallback: unknown files go to scripts/ (most are agent-generated scripts)
    return f"scripts/{filename}"


def list_sessions(s3) -> list[str]:
    """List all session IDs under the datasets prefix."""
    paginator = s3.get_paginator("list_objects_v2")
    sessions: set[str] = set()

    for page in paginator.paginate(
        Bucket=BUCKET, Prefix=DATASETS_PREFIX, Delimiter="/"
    ):
        for prefix_obj in page.get("CommonPrefixes", []):
            # e.g. teams/{team_id}/datasets/{session_id}/
            session_id = prefix_obj["Prefix"].rstrip("/").rsplit("/", 1)[-1]
            sessions.add(session_id)

    return sorted(sessions)


def list_pipeline_objects(s3, session_id: str) -> list[dict]:
    """List all objects under pipeline/ for a given session."""
    prefix = f"{DATASETS_PREFIX}{session_id}/pipeline/"
    paginator = s3.get_paginator("list_objects_v2")
    objects = []

    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            objects.append(obj)

    return objects


def migrate_session(s3, session_id: str, execute: bool) -> dict:
    """Migrate a single session. Returns stats dict."""
    session_prefix = f"{DATASETS_PREFIX}{session_id}/"
    pipeline_objects = list_pipeline_objects(s3, session_id)

    stats = {"moved": 0, "skipped": 0, "errors": 0, "files": []}

    if not pipeline_objects:
        return stats

    for obj in pipeline_objects:
        old_key = obj["Key"]
        # Extract filename relative to pipeline/
        rel_path = old_key[len(f"{session_prefix}pipeline/") :]

        # Skip subdirectories within pipeline/ (e.g. pipeline/some_dir/file)
        # These are unexpected; log and skip
        if "/" in rel_path:
            print(f"  SKIP (nested): {old_key}")
            stats["skipped"] += 1
            continue

        new_rel = resolve_destination(rel_path)
        new_key = f"{session_prefix}{new_rel}"

        label = "MOVE" if execute else "WOULD MOVE"
        print(f"  {label}: pipeline/{rel_path} → {new_rel}")
        stats["files"].append((old_key, new_key))

        if execute:
            try:
                s3.copy_object(
                    Bucket=BUCKET,
                    CopySource={"Bucket": BUCKET, "Key": old_key},
                    Key=new_key,
                )
                s3.delete_object(Bucket=BUCKET, Key=old_key)
                stats["moved"] += 1
            except Exception as e:
                print(f"  ERROR: {e}")
                stats["errors"] += 1
        else:
            stats["moved"] += 1

    return stats


def verify_session(s3, session_id: str) -> list[str]:
    """Check if any files remain in pipeline/ after migration."""
    remaining = list_pipeline_objects(s3, session_id)
    return [obj["Key"] for obj in remaining]


def main():
    parser = argparse.ArgumentParser(
        description="Migrate S3 pipeline/ artifacts to subdirectory structure"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually perform the migration (default: dry-run)",
    )
    parser.add_argument(
        "--session",
        type=str,
        default=None,
        help="Migrate a single session ID (default: all sessions)",
    )
    args = parser.parse_args()

    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"=== S3 Pipeline Migration ({mode}) ===")
    print(f"Bucket: {BUCKET}")
    print(f"Team:   {TEAM_ID}")
    print()

    s3 = boto3.client("s3")

    # Discover sessions
    if args.session:
        session_ids = [args.session]
        print(f"Target: 1 session ({args.session})")
    else:
        session_ids = list_sessions(s3)
        print(f"Found {len(session_ids)} sessions")
    print()

    # Migrate
    total = {"moved": 0, "skipped": 0, "errors": 0}
    for i, sid in enumerate(session_ids, 1):
        print(f"[{i}/{len(session_ids)}] Session: {sid}")
        stats = migrate_session(s3, sid, args.execute)

        if not stats["files"] and stats["skipped"] == 0:
            print("  (no pipeline/ objects)")

        total["moved"] += stats["moved"]
        total["skipped"] += stats["skipped"]
        total["errors"] += stats["errors"]
        print()

    # Verify (only in execute mode)
    if args.execute:
        print("=== Verification ===")
        all_clean = True
        for sid in session_ids:
            remaining = verify_session(s3, sid)
            if remaining:
                all_clean = False
                print(f"  WARN: {sid} still has {len(remaining)} file(s) in pipeline/:")
                for key in remaining:
                    print(f"    - {key}")
        if all_clean:
            print("  All sessions clean — no files remain in pipeline/")
        print()

    # Summary
    print("=== Summary ===")
    print(f"  Files {'moved' if args.execute else 'to move'}: {total['moved']}")
    print(f"  Skipped:  {total['skipped']}")
    print(f"  Errors:   {total['errors']}")

    if not args.execute and total["moved"] > 0:
        print()
        print("Run with --execute to apply changes.")

    if total["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
