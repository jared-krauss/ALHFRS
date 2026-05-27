#!/usr/bin/env python3
"""
fix-source-urls.py — One-shot migration: fix empty source_url on 178 records.

Three operations:

1. Remove lfr-358, lfr-359, lfr-360 — duplicates of lfr-600/601/602 (same
   date + location, lfr-600+ already confirmed with source_url set).

2. For lfr-361 to lfr-366 (source_type=lfr-deployment-grid-2020-2022): set
   source_url to the Met Police deployment grid PDF URL. Data from primary
   Met source — keep data_quality=confirmed.

3. For 169 garbett-gla-2024-deployment-grid records:
   - If notes field contains a Met PDF URL (Source ref: ...): extract and
     promote to source_url, keep data_quality=confirmed.
   - Otherwise: change data_quality from confirmed → approximate. Garbett
     Excel is a secondary source compilation, not a primary FOI disclosure.

Usage:
  python scripts/fix-source-urls.py [--dry-run]

Reads/writes:
  data/deployments/met-police-lfr.json
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


DATASET = Path("data/deployments/met-police-lfr.json")

# URL shared by all met-lfr-deployment-grid records (lfr-600/601/602 already use this)
MET_GRID_URL = (
    "https://www.met.police.uk/SysSiteAssets/media/downloads/force-content/"
    "met/advice/lfr/deployment-records/lfr-deployment-grid.pdf"
)

# 2023-2024 specific PDF — used for garbett 2024 records without an explicit source ref
MET_GRID_2024_URL = (
    "https://www.met.police.uk/SysSiteAssets/media/downloads/force-content/"
    "met/advice/lfr/deployment-records/lfr-deployment-grid-2023-to-2024.pdf"
)

# Records that are exact duplicates of lfr-600 / lfr-601 / lfr-602
DUPLICATE_IDS = {"lfr-358", "lfr-359", "lfr-360"}

# Records whose source_url to set directly (not duplicates, same source PDF)
GRID_2022_URL_FIX = {"lfr-361", "lfr-362", "lfr-363", "lfr-364", "lfr-365", "lfr-366"}

URL_RE = re.compile(r'https?://\S+')


def extract_url_from_notes(notes: str) -> str | None:
    """Return the first URL found in a notes string, or None."""
    if not notes:
        return None
    m = URL_RE.search(notes)
    if m:
        return m.group(0).rstrip('.,')
    return None


def main():
    ap = argparse.ArgumentParser(
        description="Fix empty source_url on lfr-deployment-grid-2020-2022 and garbett records."
    )
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would change without writing")
    args = ap.parse_args()

    data = json.loads(DATASET.read_text(encoding="utf-8"))
    deployments = data["deployments"]
    original_count = len(deployments)

    removed = []
    url_promoted = []
    downgraded = []
    url_set_grid = []

    new_deployments = []
    for rec in deployments:
        rid = rec["id"]
        st  = rec.get("source_type", "")

        # ── 1. Remove exact duplicates ─────────────────────────────────────────
        if rid in DUPLICATE_IDS:
            removed.append(rid)
            continue

        # ── 2. Fix 2020-2022 grid records ─────────────────────────────────────
        if rid in GRID_2022_URL_FIX:
            if not args.dry_run:
                rec["source_url"] = MET_GRID_URL
            url_set_grid.append(rid)
            new_deployments.append(rec)
            continue

        # ── 3. Fix garbett records ─────────────────────────────────────────────
        if st == "garbett-gla-2024-deployment-grid":
            url_in_notes = extract_url_from_notes(rec.get("notes") or "")
            if url_in_notes:
                # Has an explicit source ref URL — promote it, keep confirmed
                if not args.dry_run:
                    rec["source_url"] = url_in_notes
                url_promoted.append((rid, url_in_notes[:70]))
            else:
                # No direct source ref — downgrade to approximate, assign the
                # 2023-2024 deployment grid PDF as the closest verifiable source
                if not args.dry_run:
                    rec["data_quality"] = "approximate"
                    rec["source_url"] = MET_GRID_2024_URL
                downgraded.append(rid)
            new_deployments.append(rec)
            continue

        new_deployments.append(rec)

    # ── Summary ─────────────────────────────────────────────────────────────────
    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}fix-source-urls.py summary")
    print(f"  Records before:          {original_count}")
    print(f"  Duplicates removed:      {len(removed)}  ({', '.join(removed)})")
    print(f"  2020-2022 grid URL set:  {len(url_set_grid)}")
    print(f"  Garbett URL promoted:    {len(url_promoted)}")
    print(f"  Garbett to approximate:  {len(downgraded)}")
    print(f"  Records after:           {original_count - len(removed)}")

    if url_set_grid:
        print(f"\n  Grid URL set ({len(url_set_grid)}):")
        for rid in url_set_grid:
            print(f"    {rid}  {MET_GRID_URL[:65]}...")

    if url_promoted:
        print(f"\n  URL promoted from notes ({len(url_promoted)}):")
        for rid, url in url_promoted[:5]:
            print(f"    {rid}  {url}")
        if len(url_promoted) > 5:
            print(f"    ... and {len(url_promoted) - 5} more")

    if downgraded:
        print(f"\n  Downgraded to approximate ({len(downgraded)}):")
        for rid in downgraded[:5]:
            print(f"    {rid}")
        if len(downgraded) > 5:
            print(f"    ... and {len(downgraded) - 5} more")

    if args.dry_run:
        print("\n(no files written — dry run)")
        return

    # ── Write ────────────────────────────────────────────────────────────────────
    data["deployments"] = new_deployments
    DATASET.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten: {DATASET}")

    # ── Validate ─────────────────────────────────────────────────────────────────
    print("\nRunning validator...")
    result = subprocess.run(
        [sys.executable, "scripts/validate-dataset.py", str(DATASET)],
        capture_output=True, text=True
    )
    # Print just the summary line(s)
    for line in result.stdout.splitlines():
        if any(k in line for k in ("errors", "warnings", "clean", "PASS", "FAIL", "Total", "==")):
            print(" ", line)
    if result.returncode != 0 and not result.stdout:
        print(result.stderr[:500])


if __name__ == "__main__":
    main()
