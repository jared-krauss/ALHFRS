#!/usr/bin/env python
"""
diff-pdf-vs-dataset.py — Compare deterministic PDF extraction against current dataset.

Identifies:
  - Records in PDF but not in dataset (gaps — need adding)
  - Records in dataset but not in PDF (potentially hallucinated or different source)
  - Value disagreements on records present in both (alert counts, arrests, etc.)

Matches records using a fuzzy (date, location-token) key.

Usage:
  python diff-pdf-vs-dataset.py --pdf-extract <staging.json> --dataset <met-police-lfr.json>
                                [--year-filter 2024] [--report-out <report.md>]
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


def normalize_location(loc: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace. Used for matching."""
    if not loc:
        return ''
    loc = loc.lower()
    # Common abbreviations to canonical
    loc = loc.replace("'", "'").replace("'", "'")
    loc = loc.replace("rd,", "road").replace(" rd ", " road ").replace(" rd", " road")
    loc = loc.replace("st,", "street").replace(" st ", " street ")
    loc = loc.replace("b'way", "broadway").replace("bway", "broadway").replace("b�way", "broadway")
    loc = loc.replace("'", "")
    loc = re.sub(r'[^\w\s]', ' ', loc)
    loc = re.sub(r'\s+', ' ', loc).strip()
    return loc


def location_tokens(loc: str) -> set[str]:
    """Set of meaningful tokens (drop common stopwords)."""
    norm = normalize_location(loc)
    tokens = set(norm.split())
    stop = {'the', 'of', 'and', '&', 'a', 'rd', 'road', 'st', 'street'}
    return tokens - stop


def location_overlap_score(a: str, b: str) -> float:
    """Jaccard-like overlap of tokens. 0.0–1.0."""
    ta, tb = location_tokens(a), location_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf-extract', required=True)
    ap.add_argument('--dataset', required=True)
    ap.add_argument('--year-filter', default=None,
                    help='Only compare records in this year (e.g. "2024")')
    ap.add_argument('--report-out', default=None)
    args = ap.parse_args()

    with open(args.pdf_extract, encoding='utf-8') as f:
        pdf_records = json.load(f)['records']
    with open(args.dataset, encoding='utf-8') as f:
        ds_records = json.load(f)['deployments']

    # Year filter
    if args.year_filter:
        pdf_records = [r for r in pdf_records if r['date_start'].startswith(args.year_filter)]
        ds_records = [r for r in ds_records if (r.get('date_start') or '').startswith(args.year_filter)]

    # Build date-indexed maps
    pdf_by_date = defaultdict(list)
    for r in pdf_records:
        pdf_by_date[r['date_start']].append(r)
    ds_by_date = defaultdict(list)
    for r in ds_records:
        ds_by_date[r.get('date_start','?')].append(r)

    matched_pairs = []          # (pdf_rec, ds_rec, score)
    pdf_unmatched = []          # PDF rows not found in dataset
    ds_unmatched = []           # Dataset rows not found in PDF
    pdf_seen_idx = set()
    ds_seen_id = set()

    all_dates = sorted(set(pdf_by_date) | set(ds_by_date))

    for date in all_dates:
        pdf_list = pdf_by_date.get(date, [])
        ds_list = ds_by_date.get(date, [])

        # Greedy match: for each PDF row, find best dataset row
        for i, pdf_rec in enumerate(pdf_list):
            best_score = 0.0
            best_ds = None
            for ds_rec in ds_list:
                if ds_rec['id'] in ds_seen_id:
                    continue
                score = location_overlap_score(
                    pdf_rec['location_name'],
                    ds_rec.get('location_name', '')
                )
                if score > best_score:
                    best_score = score
                    best_ds = ds_rec
            if best_ds and best_score >= 0.3:  # threshold for "same location"
                matched_pairs.append((pdf_rec, best_ds, best_score))
                pdf_seen_idx.add((date, i))
                ds_seen_id.add(best_ds['id'])
            else:
                pdf_unmatched.append((date, pdf_rec, best_score, best_ds))

        # Dataset rows for this date not matched
        for ds_rec in ds_list:
            if ds_rec['id'] not in ds_seen_id:
                ds_unmatched.append((date, ds_rec))
                ds_seen_id.add(ds_rec['id'])

    # ── Detect value disagreements among matched pairs ───────────────────────
    disagreements = []
    for pdf_rec, ds_rec, score in matched_pairs:
        diffs = []
        # Outcome fields
        for f_pdf, f_ds in [
            ('outcome_alerts', 'outcome_alerts'),
            ('outcome_arrests', 'outcome_arrests'),
            ('outcome_faces_scanned', 'outcome_faces_scanned'),
            ('watchlist_size', 'watchlist_size'),
        ]:
            pdf_val = pdf_rec.get(f_pdf)
            ds_val = ds_rec.get(f_ds)
            if pdf_val is not None and ds_val is not None and pdf_val != ds_val:
                diffs.append(f'{f_pdf}: PDF={pdf_val} DS={ds_val}')
        if diffs:
            disagreements.append((pdf_rec, ds_rec, score, diffs))

    # ── Print summary ────────────────────────────────────────────────────────
    print(f'\n== DIFF SUMMARY ==')
    print(f'PDF records: {len(pdf_records)}  |  Dataset records: {len(ds_records)}')
    print(f'Matched: {len(matched_pairs)}')
    print(f'In PDF but not in dataset: {len(pdf_unmatched)}  <- missing additions')
    print(f'In dataset but not in PDF: {len(ds_unmatched)}  <- potentially wrong source')
    print(f'Value disagreements on matched: {len(disagreements)}')

    if pdf_unmatched:
        print(f'\n-- MISSING FROM DATASET ({len(pdf_unmatched)}) --')
        for date, rec, score, near in pdf_unmatched:
            near_str = f' (near: {near["id"]} {near.get("location_name","?")} s={score:.2f})' if near else ''
            print(f'  {date} {rec["location_name"]:35} alerts={rec["outcome_alerts"]} arrests={rec["outcome_arrests"]}{near_str}')

    if ds_unmatched:
        print(f'\n-- IN DATASET BUT NOT IN PDF ({len(ds_unmatched)}) --')
        for date, rec in ds_unmatched[:30]:
            print(f'  {rec["id"]:10} {date} {rec.get("location_name","?")[:35]:35} arrests={rec.get("outcome_arrests")}  source={rec.get("source_type","?")}')
        if len(ds_unmatched) > 30:
            print(f'  ... and {len(ds_unmatched)-30} more')

    if disagreements:
        print(f'\n-- VALUE DISAGREEMENTS ({len(disagreements)}) --')
        for pdf_rec, ds_rec, score, diffs in disagreements[:20]:
            print(f'  {ds_rec["id"]:10} {ds_rec.get("date_start")} {ds_rec.get("location_name","?")[:30]:30}')
            for diff in diffs:
                print(f'    {diff}')
        if len(disagreements) > 20:
            print(f'  ... and {len(disagreements)-20} more')

    # Write detailed report
    if args.report_out:
        report = {
            'pdf_record_count': len(pdf_records),
            'dataset_record_count': len(ds_records),
            'matched_count': len(matched_pairs),
            'missing_from_dataset': [
                {'date': d, 'record': r, 'best_neighbor_id': (n['id'] if n else None), 'best_neighbor_score': s}
                for d, r, s, n in pdf_unmatched
            ],
            'in_dataset_not_in_pdf': [
                {'date': d, 'record': r} for d, r in ds_unmatched
            ],
            'value_disagreements': [
                {'matched_id': ds['id'], 'pdf_record': p, 'dataset_record': ds, 'diffs': diffs, 'match_score': s}
                for p, ds, s, diffs in disagreements
            ],
        }
        with open(args.report_out, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f'\nDetailed report: {args.report_out}', file=sys.stderr)


if __name__ == '__main__':
    main()
