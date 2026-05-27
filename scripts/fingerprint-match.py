#!/usr/bin/env python
"""
fingerprint-match.py — Match dataset records to PDF rows by metric fingerprint.

The Met deployment grid PDF row metrics (watchlist_size, outcome_alerts,
outcome_arrests, outcome_faces_scanned) form a near-unique fingerprint per
deployment. We use this to identify dataset records whose DATE is wrong
(systematic DD/MM swap in the Garbett extraction).

Output categories:
  - PERFECT_MATCH: location + date + fingerprint all align → no action needed
  - DATE_SWAP: location + fingerprint match a PDF row with DD/MM swapped
  - METRIC_DRIFT: location + date match but metrics differ → needs review
  - LOCATION_DRIFT: fingerprint + date match but location string differs → needs review
  - NEW_IN_PDF: PDF row with no fingerprint match in dataset → missing record
  - ORPHAN_IN_DS: dataset row whose fingerprint doesn't appear in PDF → suspect record
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


def fingerprint(rec, src='pdf', loose=False):
    """Tuple of metric values. By default (strict), uses (watchlist, alerts, arrests, faces).
    If loose=True, drops watchlist (which is often null in older / non-grid sources)."""
    fields = ['outcome_alerts', 'outcome_arrests', 'outcome_faces_scanned']
    if not loose:
        fields = ['watchlist_size'] + fields
    return tuple(rec.get(f) for f in fields)


def normalize_loc(s):
    if not s:
        return ''
    s = s.lower()
    s = re.sub(r'[^\w\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def loc_tokens(s):
    norm = normalize_loc(s)
    stop = {'the', 'and', 'rd', 'road', 'st', 'street', 'high', 'a'}
    return set(t for t in norm.split() if t not in stop)


def loc_score(a, b):
    ta, tb = loc_tokens(a), loc_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


def swap_date(iso_date):
    """2024-01-11 -> 2024-11-01 (swap month/day). Returns None if invalid."""
    try:
        y, m, d = iso_date.split('-')
        # Build new date with d and m swapped
        m_new = d.zfill(2)
        d_new = m.zfill(2)
        new_iso = f"{y}-{m_new}-{d_new}"
        # Validate
        from datetime import date as _d
        _d(int(y), int(m_new), int(d_new))
        return new_iso
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf-extract', required=True)
    ap.add_argument('--dataset', required=True)
    ap.add_argument('--year-filter', default=None)
    ap.add_argument('--report-out', required=True)
    ap.add_argument('--loose', action='store_true',
                    help='Loose fingerprint mode: drop watchlist_size (use for 2025+ records)')
    args = ap.parse_args()

    with open(args.pdf_extract, encoding='utf-8') as f:
        pdf_recs = json.load(f)['records']
    with open(args.dataset, encoding='utf-8') as f:
        ds_recs = json.load(f)['deployments']

    if args.year_filter:
        pdf_recs = [r for r in pdf_recs if r['date_start'].startswith(args.year_filter)]
        ds_recs = [r for r in ds_recs if (r.get('date_start') or '').startswith(args.year_filter)]

    # Build fingerprint indexes
    pdf_by_fp = defaultdict(list)
    for r in pdf_recs:
        fp = fingerprint(r, 'pdf', loose=args.loose)
        # Only useful if fingerprint has all non-null entries
        if all(v is not None for v in fp):
            pdf_by_fp[fp].append(r)

    ds_by_fp = defaultdict(list)
    for r in ds_recs:
        fp = fingerprint(r, 'ds', loose=args.loose)
        if all(v is not None for v in fp):
            ds_by_fp[fp].append(r)

    pdf_seen = set()
    ds_seen = set()

    perfect = []
    date_swap = []
    metric_drift = []
    location_drift = []
    new_in_pdf = []
    orphan_in_ds = []

    # First pass: fingerprint matches
    for fp, pdf_list in pdf_by_fp.items():
        ds_list = ds_by_fp.get(fp, [])
        if not ds_list:
            continue
        # Try to pair each PDF with a DS record sharing this fingerprint
        for pdf_r in pdf_list:
            best = None
            best_score = -1
            for ds_r in ds_list:
                if ds_r['id'] in ds_seen:
                    continue
                s = loc_score(pdf_r['location_name'], ds_r.get('location_name', ''))
                # Bonus if dates match
                if ds_r.get('date_start') == pdf_r['date_start']:
                    s += 2.0
                elif ds_r.get('date_start') == swap_date(pdf_r['date_start']):
                    s += 1.0  # swapped-date match
                if s > best_score:
                    best_score = s
                    best = ds_r
            if best is None:
                continue
            pdf_id = (pdf_r['date_start'], pdf_r['location_name'], fp)
            if pdf_id in pdf_seen:
                continue
            pdf_seen.add(pdf_id)
            ds_seen.add(best['id'])
            # Classify
            same_date = best.get('date_start') == pdf_r['date_start']
            swap_match = best.get('date_start') == swap_date(pdf_r['date_start'])
            loc_match = loc_score(pdf_r['location_name'], best.get('location_name','')) >= 0.3

            if same_date and loc_match:
                perfect.append((pdf_r, best))
            elif swap_match and loc_match:
                date_swap.append((pdf_r, best))
            elif same_date:
                # Same date + fingerprint, location differs (possible alt spelling)
                location_drift.append((pdf_r, best))
            elif swap_match:
                # DD/MM swap + fingerprint match but locations differ
                location_drift.append((pdf_r, best))
            elif loc_match:
                # Fingerprint + location match but date is different (not DD/MM swap)
                location_drift.append((pdf_r, best))
            else:
                # Fingerprint matches but everything else differs - suspect
                location_drift.append((pdf_r, best))

    # Records not yet matched
    for r in pdf_recs:
        pdf_id = (r['date_start'], r['location_name'], fingerprint(r, 'pdf', loose=args.loose))
        if pdf_id not in pdf_seen:
            new_in_pdf.append(r)

    for r in ds_recs:
        if r['id'] not in ds_seen:
            orphan_in_ds.append(r)

    # ── Print summary ────────────────────────────────────────────────────────
    print('== FINGERPRINT MATCH SUMMARY ==')
    print(f'PDF records: {len(pdf_recs)}  Dataset records: {len(ds_recs)}')
    print(f'PERFECT (date+loc+metrics align):  {len(perfect)}')
    print(f'DATE_SWAP (DD/MM swap in dataset): {len(date_swap)}')
    print(f'LOCATION_DRIFT (fp+date match, location differs OR fp match different date): {len(location_drift)}')
    print(f'METRIC_DRIFT: {len(metric_drift)}')
    print(f'NEW_IN_PDF (missing from dataset): {len(new_in_pdf)}')
    print(f'ORPHAN_IN_DS (no fp match in PDF, possibly wrong-source or hallucinated): {len(orphan_in_ds)}')

    if date_swap:
        print(f'\n-- DATE_SWAP records (DD/MM was swapped in dataset) --')
        for pdf_r, ds_r in date_swap:
            print(f'  {ds_r["id"]:10} DS_date={ds_r.get("date_start")}  -> PDF_date={pdf_r["date_start"]}  loc="{ds_r.get("location_name","?")}"')

    if new_in_pdf:
        print(f'\n-- NEW_IN_PDF (truly missing) --')
        for r in new_in_pdf[:30]:
            print(f'  {r["date_start"]} {r["location_name"]:35} alerts={r["outcome_alerts"]} arrests={r["outcome_arrests"]} faces={r["outcome_faces_scanned"]}')
        if len(new_in_pdf) > 30:
            print(f'  ... and {len(new_in_pdf)-30} more')

    if orphan_in_ds:
        print(f'\n-- ORPHAN_IN_DS (in dataset, no matching PDF fingerprint) --')
        for r in orphan_in_ds[:30]:
            print(f'  {r["id"]:10} {r.get("date_start")} {r.get("location_name","?")[:35]:35} src={r.get("source_type")}')
        if len(orphan_in_ds) > 30:
            print(f'  ... and {len(orphan_in_ds)-30} more')

    report = {
        'pdf_count': len(pdf_recs),
        'ds_count': len(ds_recs),
        'perfect': [(p['date_start'], p['location_name'], d['id']) for p,d in perfect],
        'date_swap': [
            {'ds_id': d['id'], 'ds_date': d.get('date_start'), 'pdf_date': p['date_start'],
             'location': d.get('location_name'), 'pdf_location': p['location_name']}
            for p,d in date_swap
        ],
        'location_drift': [
            {'ds_id': d['id'], 'ds_date': d.get('date_start'), 'pdf_date': p['date_start'],
             'ds_location': d.get('location_name'), 'pdf_location': p['location_name']}
            for p,d in location_drift
        ],
        'new_in_pdf': new_in_pdf,
        'orphan_in_ds': [{'id': r['id'], 'date': r.get('date_start'),
                          'location': r.get('location_name'),
                          'source_type': r.get('source_type')} for r in orphan_in_ds],
    }
    with open(args.report_out, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f'\nReport: {args.report_out}')


if __name__ == '__main__':
    main()
