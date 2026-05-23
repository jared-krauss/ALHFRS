#!/usr/bin/env python
"""
merge-staging.py — Merge a staging JSON file into met-police-lfr.json.

Usage:
  python merge-staging.py --staging data/staging/garbett-2024.json
  python merge-staging.py --staging data/staging/garbett-2024.json --dry-run

Makes a timestamped backup of met-police-lfr.json before writing.
Sorts the merged deployments by date_start.
"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

DATASET_PATH = Path(r"D:\Dev\ALHFRS\data\deployments\met-police-lfr.json")


def main():
    parser = argparse.ArgumentParser(description="Merge staging records into met-police-lfr.json")
    parser.add_argument("--staging", required=True, help="Path to staging JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change, no writes")
    args = parser.parse_args()

    staging_path = Path(args.staging)
    if not staging_path.exists():
        print(f"ERROR: staging file not found: {staging_path}")
        raise SystemExit(1)

    staging = json.loads(staging_path.read_text(encoding="utf-8"))
    new_records = staging.get("deployments", staging) if isinstance(staging, dict) else staging

    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    existing = dataset.get("deployments", [])

    existing_ids = {r["id"] for r in existing}
    to_add = [r for r in new_records if r["id"] not in existing_ids]
    already_present = len(new_records) - len(to_add)

    print(f"Staging: {len(new_records)} records")
    print(f"  Already in dataset: {already_present}")
    print(f"  To add:             {len(to_add)}")

    if not to_add:
        print("Nothing to merge.")
        return

    if args.dry_run:
        print("\n[DRY RUN] Would add:")
        for r in to_add[:5]:
            print(f"  {r['id']}  {r['date_start']}  {r['location_name'][:40]}")
        if len(to_add) > 5:
            print(f"  ... and {len(to_add)-5} more")
        return

    # Backup
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = DATASET_PATH.with_suffix(f".{ts}.bak.json")
    shutil.copy2(DATASET_PATH, backup)
    print(f"Backup: {backup.name}")

    # Merge and sort
    merged = existing + to_add
    merged.sort(key=lambda r: r.get("date_start") or "")

    dataset["deployments"] = merged
    dataset["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    DATASET_PATH.write_text(json.dumps(dataset, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK Merged {len(to_add)} records. Dataset now has {len(merged)} deployments.")
    print(f"  Updated: {DATASET_PATH}")


if __name__ == "__main__":
    main()
