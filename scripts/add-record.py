#!/usr/bin/env python3
"""
add-record.py — Interactive single-record add for ALHFRS deployment files.

Prompts for required and common fields, validates inline, auto-assigns ID,
then appends to the target file and runs the validator.

Usage:
  python scripts/add-record.py --file met   [--dry-run]
  python scripts/add-record.py --file btp   [--dry-run]
  python scripts/add-record.py --file private [--dry-run]

Fields prompted:
  Required: location_name, date_start, lat, lon, data_quality, source_url, source_type
  Common:   date_end, borough, ward, stated_purpose, operator (non-met files),
            outcome_alerts, outcome_arrests, notes
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


FILES = {
    'met':     Path('data/deployments/met-police-lfr.json'),
    'btp':     Path('data/deployments/btp-lfr.json'),
    'private': Path('data/deployments/private-operators.json'),
}

OPERATORS = {
    'met':     'Metropolitan Police',
    'btp':     'British Transport Police',
    'private': None,  # prompted
}

OPERATOR_TYPES = {
    'met':     'law_enforcement',
    'btp':     'law_enforcement',
    'private': 'private',
}

ID_PREFIXES = {
    'met':     'lfr',
    'btp':     'btp',
    'private': 'priv',
}

VALID_QUALITY = ['confirmed', 'approximate', 'unverified']
VALID_SOURCE_TYPES = [
    'FOI_disclosure', 'news_report', 'court_record', 'police_statement',
    'operator_statement', 'ngo_report', 'met-lfr-deployment-grid',
    'garbett-gla-2024-deployment-grid',
]


def prompt(label: str, default=None, required=True, choices=None, cast=None) -> str | None:
    hint = f" [{default}]" if default is not None else ""
    if choices:
        hint = f" ({'/'.join(choices)}){hint}"
    while True:
        val = input(f"  {label}{hint}: ").strip()
        if not val:
            if default is not None:
                return default
            if not required:
                return None
            print(f"    Required — enter a value for '{label}'")
            continue
        if choices and val not in choices:
            print(f"    Must be one of: {', '.join(choices)}")
            continue
        if cast:
            try:
                return cast(val)
            except (ValueError, TypeError):
                print(f"    Invalid {cast.__name__} — try again")
                continue
        return val


def find_next_id(data: dict, prefix: str) -> str:
    """Return next available ID string."""
    records = data.get('deployments', data) if isinstance(data, dict) else data
    nums = []
    for r in records:
        rid = str(r.get('id', ''))
        if rid.startswith(prefix + '-'):
            try:
                nums.append(int(rid[len(prefix)+1:]))
            except ValueError:
                pass
    n = max(nums) + 1 if nums else 1
    return f"{prefix}-{n:03d}"


def main():
    ap = argparse.ArgumentParser(description="Interactively add one LFR deployment record.")
    ap.add_argument('--file', choices=['met', 'btp', 'private'], required=True,
                    help='Target dataset (met=Metropolitan Police, btp=BTP, private=Private operators)')
    ap.add_argument('--dry-run', action='store_true',
                    help='Print the record without writing to disk')
    args = ap.parse_args()

    target = FILES[args.file]
    if not target.exists():
        print(f"ERROR: Dataset not found: {target}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(target.read_text(encoding='utf-8'))
    prefix = ID_PREFIXES[args.file]
    new_id = find_next_id(data, prefix)

    print(f"\nAdding record to: {target}")
    print(f"Auto-assigned ID: {new_id}")
    print(f"(Press Enter to accept [default], type 'skip' for optional fields)\n")

    rec = {'id': new_id}

    # Operator
    if OPERATORS[args.file]:
        rec['operator'] = OPERATORS[args.file]
    else:
        rec['operator'] = prompt('operator', required=True)

    rec['operator_type']   = OPERATOR_TYPES[args.file]
    rec['deployment_type'] = 'mobile'

    # Location
    rec['location_name'] = prompt('location_name', required=True)
    rec['borough']       = prompt('borough', required=False) or None
    rec['ward']          = prompt('ward', required=False) or None

    # Coordinates
    lat_str = prompt('lat (decimal, e.g. 51.5154)', required=True)
    lon_str = prompt('lon (decimal, e.g. -0.1408)', required=True)
    try:
        rec['lat'] = float(lat_str)
        rec['lon'] = float(lon_str)
    except ValueError:
        print("ERROR: lat/lon must be decimal numbers", file=sys.stderr)
        sys.exit(1)

    if not (51.28 <= rec['lat'] <= 51.69 and -0.51 <= rec['lon'] <= 0.34):
        print(f"WARNING: coordinates {rec['lat']}, {rec['lon']} are outside Greater London bounds")

    # Dates
    rec['date_start'] = prompt('date_start (YYYY-MM-DD)', required=True)
    rec['date_end']   = prompt('date_end (YYYY-MM-DD)', default=rec['date_start'], required=False)

    # Purpose / outcomes
    rec['stated_purpose'] = prompt('stated_purpose', required=False) or None

    alerts_str  = prompt('outcome_alerts (int)', required=False)
    arrests_str = prompt('outcome_arrests (int)', required=False)
    def to_int(s):
        return int(s) if s and s.lower() not in ('skip', 'none', 'null', 'n/a') else None
    rec['outcome_alerts']  = to_int(alerts_str)
    rec['outcome_arrests'] = to_int(arrests_str)

    # Data quality + source
    rec['data_quality'] = prompt(
        'data_quality', required=True, choices=VALID_QUALITY
    )
    rec['source_url']  = prompt('source_url (specific document URL)', required=True)
    rec['source_type'] = prompt('source_type', required=True)

    rec['notes'] = prompt('notes (optional)', required=False) or ''

    # Fill remaining schema keys with None
    for key in ['location_cluster_id', 'vendor', 'threshold', 'watchlist_size']:
        rec.setdefault(key, None)

    print(f"\nRecord preview:")
    print(json.dumps(rec, indent=2, ensure_ascii=False))

    if args.dry_run:
        print("\n(dry run — nothing written)")
        return

    confirm = input("\nWrite this record? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("Aborted.")
        return

    # Append to deployments list
    deployments = data.get('deployments', data)
    if isinstance(data, dict) and 'deployments' in data:
        data['deployments'].append(rec)
    else:
        data.append(rec)

    target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Written: {target}")

    # Validate
    print("\nRunning validator...")
    result = subprocess.run(
        [sys.executable, 'scripts/validate-dataset.py', str(target)],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        if any(k in line for k in ('error', 'warning', 'clean', 'PASS', 'FAIL', '==')):
            print(' ', line)


if __name__ == '__main__':
    main()
