#!/usr/bin/env python3
"""Migrate S3 flat files to folder-based structure.

Migrations:
  teams/{tid}/alphas/{id}.parquet       → teams/{tid}/alphas/{id}/data.parquet
  teams/{tid}/alphas/{id}.nav.parquet   → teams/{tid}/alphas/{id}/nav.parquet
  teams/{tid}/catalogs/{cm_id}.parquet  → teams/{tid}/catalogs/{cm_id}/data.parquet
  teams/{tid}/portfolios/{pid}.parquet  → teams/{tid}/portfolios/{pid}/data.parquet
"""

import argparse
import logging
import re
import sys

import boto3

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Counters
# ---------------------------------------------------------------------------

class Stats:
    def __init__(self):
        self.migrated = 0
        self.skipped = 0
        self.errors = 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def list_objects(s3, bucket: str, prefix: str):
    """Yield all object keys under a prefix."""
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            yield obj["Key"]


def copy_and_delete(s3, bucket: str, src: str, dst: str, dry_run: bool, stats: Stats):
    """Copy src to dst then delete src. Handles errors per-file."""
    if dry_run:
        log.info("[DRY-RUN] %s → %s", src, dst)
        stats.migrated += 1
        return
    try:
        s3.copy_object(
            Bucket=bucket,
            CopySource={"Bucket": bucket, "Key": src},
            Key=dst,
        )
        s3.delete_object(Bucket=bucket, Key=src)
        log.info("Migrated  %s → %s", src, dst)
        stats.migrated += 1
    except Exception:
        log.exception("Error migrating %s → %s", src, dst)
        stats.errors += 1


# ---------------------------------------------------------------------------
# Migration functions
# ---------------------------------------------------------------------------

# Match flat alpha files:
#   teams/{tid}/alphas/{id}.parquet          → data.parquet
#   teams/{tid}/alphas/{id}.nav.parquet      → nav.parquet
# Skip anything already in folder structure (contains /data.parquet or /nav.parquet).
_ALPHA_DATA_RE = re.compile(
    r"^(teams/[^/]+/alphas/)([^/]+)\.parquet$"
)
_ALPHA_NAV_RE = re.compile(
    r"^(teams/[^/]+/alphas/)([^/]+)\.nav\.parquet$"
)


def migrate_alphas(s3, bucket: str, team_prefix: str, dry_run: bool, stats: Stats):
    """Migrate flat alpha parquet files to folder structure."""
    prefix = f"{team_prefix}alphas/"
    for key in list_objects(s3, bucket, prefix):
        # Already in folder structure
        if "/data.parquet" in key or key.endswith("/nav.parquet"):
            parts = key.split("/")
            # Folder structure has at least: teams/tid/alphas/id/file.parquet
            if len(parts) >= 5:
                stats.skipped += 1
                continue

        # Nav files first (more specific pattern)
        m = _ALPHA_NAV_RE.match(key)
        if m:
            alpha_prefix, alpha_id = m.group(1), m.group(2)
            dst = f"{alpha_prefix}{alpha_id}/nav.parquet"
            copy_and_delete(s3, bucket, key, dst, dry_run, stats)
            continue

        # Data files
        m = _ALPHA_DATA_RE.match(key)
        if m:
            alpha_prefix, alpha_id = m.group(1), m.group(2)
            dst = f"{alpha_prefix}{alpha_id}/data.parquet"
            copy_and_delete(s3, bucket, key, dst, dry_run, stats)
            continue

        # Unknown pattern — skip
        stats.skipped += 1


_CATALOG_RE = re.compile(
    r"^(teams/[^/]+/catalogs/)([^/]+)\.parquet$"
)


def migrate_catalogs(s3, bucket: str, team_prefix: str, dry_run: bool, stats: Stats):
    """Migrate flat catalog parquet files to folder structure."""
    prefix = f"{team_prefix}catalogs/"
    for key in list_objects(s3, bucket, prefix):
        if "/data.parquet" in key:
            parts = key.split("/")
            if len(parts) >= 5:
                stats.skipped += 1
                continue

        m = _CATALOG_RE.match(key)
        if m:
            cat_prefix, cm_id = m.group(1), m.group(2)
            dst = f"{cat_prefix}{cm_id}/data.parquet"
            copy_and_delete(s3, bucket, key, dst, dry_run, stats)
            continue

        stats.skipped += 1


_PORTFOLIO_RE = re.compile(
    r"^(teams/[^/]+/portfolios/)([^/]+)\.parquet$"
)


def migrate_portfolios(s3, bucket: str, team_prefix: str, dry_run: bool, stats: Stats):
    """Migrate flat portfolio parquet files to folder structure."""
    prefix = f"{team_prefix}portfolios/"
    for key in list_objects(s3, bucket, prefix):
        if "/data.parquet" in key:
            parts = key.split("/")
            if len(parts) >= 5:
                stats.skipped += 1
                continue

        m = _PORTFOLIO_RE.match(key)
        if m:
            port_prefix, pid = m.group(1), m.group(2)
            dst = f"{port_prefix}{pid}/data.parquet"
            copy_and_delete(s3, bucket, key, dst, dry_run, stats)
            continue

        stats.skipped += 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Migrate S3 flat files to folder-based structure."
    )
    parser.add_argument(
        "--bucket", default="arkraft-production", help="S3 bucket name"
    )
    parser.add_argument(
        "--endpoint", default=None,
        help="S3 endpoint URL (e.g., http://localhost:9000 for MinIO)"
    )
    parser.add_argument(
        "--team-id", default=None,
        help="Scope migration to a specific team ID (default: all teams)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be done without making changes"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable debug logging"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)-8s %(message)s",
    )

    # Build S3 client
    client_kwargs = {}
    if args.endpoint:
        client_kwargs["endpoint_url"] = args.endpoint
    s3 = boto3.client("s3", **client_kwargs)

    if args.dry_run:
        log.info("=== DRY RUN — no changes will be made ===")

    stats = Stats()

    # Determine team prefixes to process
    if args.team_id:
        team_prefixes = [f"teams/{args.team_id}/"]
    else:
        # Discover all team prefixes
        team_prefixes = []
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(
            Bucket=args.bucket, Prefix="teams/", Delimiter="/"
        ):
            for cp in page.get("CommonPrefixes", []):
                team_prefixes.append(cp["Prefix"])
        if not team_prefixes:
            log.warning("No teams found under teams/ prefix.")
            sys.exit(0)

    log.info("Teams to process: %d", len(team_prefixes))

    for tp in sorted(team_prefixes):
        log.info("--- Processing %s ---", tp.rstrip("/"))
        migrate_alphas(s3, args.bucket, tp, args.dry_run, stats)
        migrate_catalogs(s3, args.bucket, tp, args.dry_run, stats)
        migrate_portfolios(s3, args.bucket, tp, args.dry_run, stats)

    # Summary
    log.info("=== Summary ===")
    log.info("  Migrated: %d", stats.migrated)
    log.info("  Skipped:  %d", stats.skipped)
    log.info("  Errors:   %d", stats.errors)

    if stats.errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
