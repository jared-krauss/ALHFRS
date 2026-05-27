#!/usr/bin/env python
"""
apply-fingerprint-fixes.py — Apply DATE_SWAP and LOCATION_DRIFT corrections to
the dataset, then append NEW_IN_PDF records as new entries.

Inputs:
  --dataset       Path to met-police-lfr.json (will be modified in-place)
  --report        Path to fingerprint-report-YYYY.json
  --start-id      First ID to use for NEW_IN_PDF appended records
  --dry-run       Show planned changes without writing

The Walworth lfr-536 duplicate (added by hand for visible-value first step) is
deleted as a special case because lfr-506 will be date-corrected to occupy the
same canonical slot.

Outputs:
  - Modified dataset
  - Backup of dataset before changes at <dataset>.pre-fix-YYYYMMDD.json
"""

import argparse
import json
import re
import shutil
from datetime import date as _d
from pathlib import Path


def swap_date(iso_date):
    try:
        y, m, d = iso_date.split('-')
        new_iso = f"{y}-{d.zfill(2)}-{m.zfill(2)}"
        _d(int(y), int(d), int(m))  # validate
        return new_iso
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', required=True)
    ap.add_argument('--report', required=True)
    ap.add_argument('--start-id', type=int, required=True)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    with open(args.dataset, encoding='utf-8') as f:
        dataset = json.load(f)
    with open(args.report, encoding='utf-8') as f:
        report = json.load(f)

    by_id = {r['id']: r for r in dataset['deployments']}

    changes = {'date_swap': [], 'location_drift': [], 'new_records': [], 'deletions': []}

    # ── 1. DATE_SWAP fixes ────────────────────────────────────────────────────
    for item in report['date_swap']:
        rid = item['ds_id']
        ds_date_old = item['ds_date']
        pdf_date_new = item['pdf_date']
        if rid not in by_id:
            continue
        rec = by_id[rid]
        if rec.get('date_start') != ds_date_old:
            continue  # already fixed or differs
        changes['date_swap'].append((rid, ds_date_old, pdf_date_new))
        if not args.dry_run:
            rec['date_start'] = pdf_date_new
            rec['date_end'] = pdf_date_new
            # Add note about correction
            existing_notes = rec.get('notes') or ''
            correction_note = f' [DATE CORRECTED 2026-05-27: was {ds_date_old}, fixed to {pdf_date_new} after DD/MM-swap detected via Met PDF re-extraction.]'
            if 'DATE CORRECTED' not in existing_notes:
                rec['notes'] = existing_notes + correction_note

    # ── 2. LOCATION_DRIFT fixes (typo / spelling) ────────────────────────────
    for item in report['location_drift']:
        rid = item['ds_id']
        if rid not in by_id:
            continue
        rec = by_id[rid]
        # Only fix if dates match (high confidence same record)
        if rec.get('date_start') != item['pdf_date']:
            continue
        old_loc = rec.get('location_name')
        new_loc = item['pdf_location']
        if old_loc == new_loc:
            continue
        changes['location_drift'].append((rid, old_loc, new_loc))
        if not args.dry_run:
            rec['location_name'] = new_loc
            existing_notes = rec.get('notes') or ''
            note = f' [LOCATION CORRECTED 2026-05-27: was "{old_loc}", fixed to "{new_loc}" via Met PDF.]'
            if 'LOCATION CORRECTED' not in existing_notes:
                rec['notes'] = existing_notes + note

    # ── 3. NEW_IN_PDF additions ──────────────────────────────────────────────
    # Get a reference NEC/Met record for default fields
    template = next((r for r in dataset['deployments']
                     if r.get('source_type') == 'garbett-gla-2024-deployment-grid'
                     and r.get('vendor') == 'NEC'), {})

    next_id = args.start_id
    for pdf_rec in report['new_in_pdf']:
        new_rec = {
            'id': f'lfr-{next_id}',
            'operator': 'Metropolitan Police',
            'operator_type': 'law_enforcement',
            'date_start': pdf_rec['date_start'],
            'date_end': pdf_rec['date_start'],
            'location_name': pdf_rec['location_name'],
            'borough': None,
            'ward': None,
            'ward_code': None,
            'lat': None,
            'lon': None,
            'location_cluster_id': None,
            'deployment_type': 'mobile',
            'stated_purpose': pdf_rec.get('stated_purpose') or 'Crime Hotspot',
            'watchlist_size': pdf_rec.get('watchlist_size'),
            'threshold': pdf_rec.get('threshold'),
            'outcome_alerts': pdf_rec.get('outcome_alerts'),
            'outcome_true_alerts': (
                (pdf_rec.get('outcome_true_alerts_confirmed') or 0)
                + (pdf_rec.get('outcome_true_alerts_unconfirmed') or 0)
                if (pdf_rec.get('outcome_true_alerts_confirmed') is not None
                    or pdf_rec.get('outcome_true_alerts_unconfirmed') is not None)
                else None
            ),
            'outcome_false_alerts': (
                (pdf_rec.get('outcome_false_alerts_confirmed') or 0)
                + (pdf_rec.get('outcome_false_alerts_unconfirmed') or 0)
                if (pdf_rec.get('outcome_false_alerts_confirmed') is not None
                    or pdf_rec.get('outcome_false_alerts_unconfirmed') is not None)
                else None
            ),
            'outcome_arrests': pdf_rec.get('outcome_arrests'),
            'outcome_faces_scanned': pdf_rec.get('outcome_faces_scanned'),
            'vendor': 'NEC',
            'data_quality': 'confirmed',
            'source_type': 'met-lfr-deployment-grid',
            'source_url': 'https://www.met.police.uk/SysSiteAssets/media/downloads/force-content/met/advice/lfr/deployment-records/lfr-deployment-grid.pdf',
            'notes': (
                f"Page-extracted from Met LFR deployment grid PDF 2023-2024. "
                f"Duration: {pdf_rec.get('duration_raw') or 'unknown'}. "
                f"Added 2026-05-27 during full re-extraction; "
                f"originally missed by Garbett-GLA extraction."
            ),
        }
        changes['new_records'].append(new_rec)
        next_id += 1
        if not args.dry_run:
            dataset['deployments'].append(new_rec)

    # ── 4. Delete the lfr-536 duplicate (Walworth Nov 1) ─────────────────────
    # lfr-536 was added by hand earlier; lfr-506 will be the correct record after
    # date-swap correction. So we delete lfr-536.
    if 'lfr-536' in by_id:
        changes['deletions'].append('lfr-536')
        if not args.dry_run:
            dataset['deployments'] = [r for r in dataset['deployments'] if r['id'] != 'lfr-536']

    # ── Report ────────────────────────────────────────────────────────────────
    print(f'== PLANNED CHANGES (dry-run={args.dry_run}) ==')
    print(f'DATE_SWAP fixes:     {len(changes["date_swap"])}')
    print(f'LOCATION fixes:      {len(changes["location_drift"])}')
    print(f'NEW records added:   {len(changes["new_records"])}')
    print(f'Records deleted:     {len(changes["deletions"])}')
    print(f'Final dataset size:  {len(dataset["deployments"])}')

    if changes['new_records']:
        print(f'\n-- NEW records being added --')
        for r in changes['new_records'][:5]:
            print(f'  {r["id"]:10} {r["date_start"]} {r["location_name"]:35} alerts={r["outcome_alerts"]} arrests={r["outcome_arrests"]}')
        if len(changes['new_records']) > 5:
            print(f'  ... and {len(changes["new_records"])-5} more')

    if not args.dry_run:
        # Backup
        backup = Path(args.dataset).parent / (Path(args.dataset).stem + '.pre-fix-20260527.json')
        # Already created above? Make idempotent
        if not backup.exists():
            shutil.copy(args.dataset, backup)
            print(f'Backup: {backup}')
        # Update metadata
        dataset['last_updated'] = '2026-05-27'
        # Write
        with open(args.dataset, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print(f'Wrote {args.dataset}')


if __name__ == '__main__':
    main()
