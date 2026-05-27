#!/usr/bin/env python
"""
merge-orphan-duplicates.py — Merge dataset orphans that duplicate newly-added
PDF records.

When apply-fingerprint-fixes.py added NEW_IN_PDF records, some duplicated
existing orphans (because the orphans had NULL arrests, so the fingerprint
matcher couldn't match them). This script:

  1. Finds orphan/new-record pairs by (date_or_swap, faces_scanned)
  2. Updates the orphan with PDF date + missing metrics
  3. Deletes the duplicate new record

Inputs:
  --dataset   met-police-lfr.json
  --pdf       reverify-deterministic-2023-2024.json
  --report    fingerprint-report-2024-loose.json
  --new-id-min  IDs >= this threshold are candidates for deletion (default 537)
"""

import argparse
import json
import shutil
from datetime import date as _d
from pathlib import Path


def swap_date(iso_date):
    try:
        y, m, d = iso_date.split('-')
        _d(int(y), int(d), int(m))
        return f"{y}-{d.zfill(2)}-{m.zfill(2)}"
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', required=True)
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--report', required=True)
    ap.add_argument('--new-id-min', type=int, default=537)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    with open(args.dataset, encoding='utf-8') as f:
        dataset = json.load(f)
    with open(args.pdf, encoding='utf-8') as f:
        pdf_recs = json.load(f)['records']
    with open(args.report, encoding='utf-8') as f:
        report = json.load(f)

    by_id = {r['id']: r for r in dataset['deployments']}

    merges = []  # (orphan_id, deleted_new_id, pdf_record)

    for o in report['orphan_in_ds']:
        orphan = by_id.get(o['id'])
        if not orphan:
            continue
        faces = orphan.get('outcome_faces_scanned')
        date = orphan.get('date_start')
        if faces is None or date is None:
            continue
        sw = swap_date(date)
        # Find matching PDF row
        pdf_match = next(
            (p for p in pdf_recs
             if p.get('outcome_faces_scanned') == faces
             and (p['date_start'] == date or p['date_start'] == sw)),
            None
        )
        if not pdf_match:
            continue
        # Find the duplicate new record
        new_recs = [
            r for r in dataset['deployments']
            if r['id'].startswith('lfr-')
            and r['id'].split('-')[1].isdigit()
            and int(r['id'].split('-')[1]) >= args.new_id_min
            and r.get('date_start') == pdf_match['date_start']
            and r.get('outcome_faces_scanned') == faces
        ]
        if not new_recs:
            continue
        merges.append((orphan, new_recs[0], pdf_match))

    print(f'== MERGE PLAN (dry-run={args.dry_run}) ==')
    print(f'Pairs to merge: {len(merges)}')
    for orphan, new_rec, pdf in merges:
        print(f'  Update {orphan["id"]:10} (was: {orphan["date_start"]} {orphan["location_name"]})')
        print(f'    -> date={pdf["date_start"]}, location={pdf["location_name"]}, alerts={pdf["outcome_alerts"]}, arrests={pdf["outcome_arrests"]}')
        print(f'  Delete {new_rec["id"]} (duplicate)')

    if args.dry_run:
        return

    for orphan, new_rec, pdf in merges:
        # Update orphan with PDF data
        old_date = orphan['date_start']
        old_loc = orphan.get('location_name')

        orphan['date_start'] = pdf['date_start']
        orphan['date_end'] = pdf['date_start']
        orphan['location_name'] = pdf['location_name']
        if orphan.get('outcome_alerts') is None:
            orphan['outcome_alerts'] = pdf.get('outcome_alerts')
        if orphan.get('outcome_arrests') is None:
            orphan['outcome_arrests'] = pdf.get('outcome_arrests')
        if orphan.get('outcome_true_alerts') is None and pdf.get('outcome_true_alerts_confirmed') is not None:
            orphan['outcome_true_alerts'] = (pdf['outcome_true_alerts_confirmed'] or 0) + (pdf['outcome_true_alerts_unconfirmed'] or 0)
        if orphan.get('outcome_false_alerts') is None and pdf.get('outcome_false_alerts_confirmed') is not None:
            orphan['outcome_false_alerts'] = (pdf['outcome_false_alerts_confirmed'] or 0) + (pdf['outcome_false_alerts_unconfirmed'] or 0)
        if orphan.get('threshold') is None:
            orphan['threshold'] = pdf.get('threshold')

        existing_notes = orphan.get('notes') or ''
        note = f' [MERGED 2026-05-27: was {old_date} "{old_loc}"; corrected to PDF row {pdf["date_start"]} "{pdf["location_name"]}"; merged from duplicate {new_rec["id"]}.]'
        if 'MERGED 2026-05-27' not in existing_notes:
            orphan['notes'] = existing_notes + note

    # Delete the duplicate new records
    delete_ids = {new_rec['id'] for _, new_rec, _ in merges}
    dataset['deployments'] = [r for r in dataset['deployments'] if r['id'] not in delete_ids]
    dataset['last_updated'] = '2026-05-27'

    with open(args.dataset, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'\nWrote {args.dataset}')
    print(f'Final record count: {len(dataset["deployments"])}')


if __name__ == '__main__':
    main()
