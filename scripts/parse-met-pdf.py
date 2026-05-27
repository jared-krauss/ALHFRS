#!/usr/bin/env python
"""
parse-met-pdf.py — Deterministic regex parser for the Met LFR deployment grid PDFs.

The Met publishes its deployment grid as a tabular PDF. Each row has a strict
column structure:

  <location-prefix>  DD/MM/YY  Hh MMm  <purpose>  <watchlist>  <threshold>
  <total_alerts> <true_conf> <true_uncon> <false_conf> <false_uncon> <rate>%
  <arrests> <other> <no_action> <faces_seen>

Location text often wraps to subsequent lines (continuation lines), which we
stitch back to the parent row.

Two grid formats:
- 2023-2024 PDF: 16 columns (with "true_confirmed/unconfirmed" split)
- 2025 PDF: same 16 columns
- 2020-2022 PDF: simpler 11 columns; handled with a separate regex

Usage:
  python parse-met-pdf.py --pdf <path> --out <json-output> [--format 2024|2025|2020]

Output is a staging file — does NOT modify met-police-lfr.json directly.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ── Regex patterns ─────────────────────────────────────────────────────────

DATE_RE = re.compile(r'\b(\d{2}/\d{2}/\d{2,4})\b')

# Main row pattern for 2023-2024 + 2025 formats:
#   <location-prefix> <DD/MM/YY> <Hh MMm> <purpose> <watchlist> <threshold>
#   <alerts> <true_c> <true_u> <false_c> <false_u> <rate>% <arrests> <other> <no_action> <faces>
ROW_2024_RE = re.compile(
    r'^(?P<loc>.+?)\s+'
    r'(?P<date>\d{2}/\d{2}/\d{2,4})\s+'
    r'(?P<dur>\d+h?r?\s*\d+m?\s*r?)\s+'        # "5h 48m" or "5hr 48m"
    r'(?P<purpose>(?:Crime Hotspot|.+?))\s+'
    r'(?P<watchlist>\d+)\s+'
    r'(?P<threshold>0\.\d+)\s+'
    r'(?P<alerts>\d+)\s+'
    r'(?P<true_c>\d+)\s+'
    r'(?P<true_u>\d+)\s+'
    r'(?P<false_c>\d+)\s+'
    r'(?P<false_u>\d+)\s+'
    r'(?P<rate>[\d.]+)%?\s+'
    r'(?P<arrests>\d+)\s+'
    r'(?P<other>\d+)\s+'
    r'(?P<noact>\d+)\s+'
    r'(?P<faces>\d+)\s*$'
)

# Pattern for 2020-2022 format (different column layout):
#   <location> <DD/MM/YY> <purpose-codes> <watchlist> <alerts> <true_c> <true_uc> <false_c> <false_uc> <engagements> <arrests> <faces> <rate>
# Has "N/A" values too.
ROW_2020_RE = re.compile(
    r'^(?P<loc>.+?)\s+'
    r'(?P<date>\d{2}/\d{2}/\d{2,4})\s+'
    r'(?P<purpose>[\d,\s]+)\s+'
    r'(?P<watchlist>\d+)\s+'
    r'(?P<alerts>\d+|N/A)\s+'
    r'(?P<true_c>\d+|N/A)\s+'
    r'(?P<true_u>\d+|N/A)\s+'
    r'(?P<false_c>\d+|N/A)\s+'
    r'(?P<false_u>\d+|N/A)\s+'
    r'(?P<engagements>\d+|N/A)\s+'
    r'(?P<arrests>\d+|N/A)\s+'
    r'(?P<faces>\d+|N/A)\s+'
    r'(?P<rate>[\d.%]+|N/A)\s*$'
)

# A line that's almost-certainly a continuation (no date, short, no big numbers)
CONTINUATION_RE = re.compile(r'^[A-Za-z0-9,.\'’\s\-\(\)/&]+$')


# ── Helpers ────────────────────────────────────────────────────────────────

def normalize_date(date_str: str) -> str:
    """DD/MM/YY → YYYY-MM-DD."""
    parts = date_str.split('/')
    if len(parts) != 3:
        return date_str
    d, m, y = parts
    if len(y) == 2:
        y = '20' + y
    return f"{y}-{int(m):02d}-{int(d):02d}"


def parse_duration(dur_str: str) -> int | None:
    """'6h 21m' or '4hr 47m' → total minutes."""
    if not dur_str:
        return None
    m = re.search(r'(\d+)\s*h(?:r)?\s*(\d+)\s*m', dur_str)
    if not m:
        return None
    h, mins = int(m.group(1)), int(m.group(2))
    return h * 60 + mins


def parse_int_or_none(s: str | None) -> int | None:
    if s is None or s.upper() == 'N/A':
        return None
    try:
        return int(s)
    except ValueError:
        return None


def extract_pdf_text(pdf_path: str) -> str:
    """Concatenate all pages' text (preserving line breaks)."""
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber not installed", file=sys.stderr)
        sys.exit(1)

    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF: {pdf_path} — {len(pdf.pages)} pages", file=sys.stderr)
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ''
            chunks.append(f'\n=== Page {i+1} ===\n' + text)
    return '\n'.join(chunks)


def parse_rows_2024(text: str) -> list[dict]:
    """Parse 2023-2024 / 2025 format. Stitches continuation lines."""
    lines = [l.rstrip() for l in text.split('\n')]
    rows = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        # Try to match a data row
        m = ROW_2024_RE.match(line)
        if m:
            row = m.groupdict()
            # Look ahead for continuation lines
            j = i + 1
            cont_parts = []
            while j < len(lines):
                next_line = lines[j].strip()
                if not next_line:
                    j += 1
                    continue
                # If next line has a date or looks like a header, stop
                if DATE_RE.search(next_line):
                    break
                if next_line.startswith('==='):
                    break
                if 'MPS LFR' in next_line or 'Deployment' in next_line:
                    break
                if 'Total' in next_line and 'False' in next_line:
                    break
                if 'Confirmed' in next_line and ('True' in next_line or 'False' in next_line):
                    break
                if 'More Trust' in next_line:
                    break
                # Looks like continuation
                if CONTINUATION_RE.match(next_line) and len(next_line) < 50:
                    cont_parts.append(next_line)
                    j += 1
                else:
                    break
            location = row['loc'].strip()
            if cont_parts:
                location = location + ' ' + ' '.join(cont_parts)
            location = re.sub(r'\s+', ' ', location).strip()

            rows.append({
                'location_name': location,
                'date_start': normalize_date(row['date']),
                'duration_minutes': parse_duration(row['dur']),
                'duration_raw': row['dur'].strip(),
                'stated_purpose': row['purpose'].strip(),
                'watchlist_size': parse_int_or_none(row['watchlist']),
                'threshold': float(row['threshold']),
                'outcome_alerts': parse_int_or_none(row['alerts']),
                'outcome_true_alerts_confirmed': parse_int_or_none(row['true_c']),
                'outcome_true_alerts_unconfirmed': parse_int_or_none(row['true_u']),
                'outcome_false_alerts_confirmed': parse_int_or_none(row['false_c']),
                'outcome_false_alerts_unconfirmed': parse_int_or_none(row['false_u']),
                'outcome_false_alert_rate_pct': float(row['rate']) if row['rate'].replace('.','').isdigit() else None,
                'outcome_arrests': parse_int_or_none(row['arrests']),
                'outcome_other_action': parse_int_or_none(row['other']),
                'outcome_no_action': parse_int_or_none(row['noact']),
                'outcome_faces_scanned': parse_int_or_none(row['faces']),
            })
            i = j
        else:
            i += 1
    return rows


def parse_rows_2020(text: str) -> list[dict]:
    """Parse 2020-2022 format (different column layout)."""
    lines = [l.rstrip() for l in text.split('\n')]
    rows = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        m = ROW_2020_RE.match(line)
        if m:
            row = m.groupdict()
            j = i + 1
            cont_parts = []
            while j < len(lines):
                next_line = lines[j].strip()
                if not next_line:
                    j += 1
                    continue
                if DATE_RE.search(next_line):
                    break
                if next_line.startswith('==='):
                    break
                if 'MPS LFR' in next_line or 'Deployment' in next_line:
                    break
                if CONTINUATION_RE.match(next_line) and len(next_line) < 60:
                    cont_parts.append(next_line)
                    j += 1
                else:
                    break
            location = row['loc'].strip()
            if cont_parts:
                location = location + ' ' + ' '.join(cont_parts)
            location = re.sub(r'\s+', ' ', location).strip()
            rows.append({
                'location_name': location,
                'date_start': normalize_date(row['date']),
                'duration_minutes': None,
                'duration_raw': None,
                'stated_purpose': row['purpose'].strip(),
                'watchlist_size': parse_int_or_none(row['watchlist']),
                'threshold': None,
                'outcome_alerts': parse_int_or_none(row['alerts']),
                'outcome_true_alerts_confirmed': parse_int_or_none(row['true_c']),
                'outcome_true_alerts_unconfirmed': parse_int_or_none(row['true_u']),
                'outcome_false_alerts_confirmed': parse_int_or_none(row['false_c']),
                'outcome_false_alerts_unconfirmed': parse_int_or_none(row['false_u']),
                'outcome_engagements': parse_int_or_none(row['engagements']),
                'outcome_arrests': parse_int_or_none(row['arrests']),
                'outcome_faces_scanned': parse_int_or_none(row['faces']),
                'outcome_false_alert_rate_pct': row['rate'],
            })
            i = j
        else:
            i += 1
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--format', choices=['2024', '2020'], default='2024',
                    help='Column layout: 2024 = 2023-2024+2025 PDFs, 2020 = 2020-2022 PDF')
    args = ap.parse_args()

    text = extract_pdf_text(args.pdf)

    if args.format == '2024':
        rows = parse_rows_2024(text)
    else:
        rows = parse_rows_2020(text)

    print(f"Parsed {len(rows)} rows", file=sys.stderr)

    out = {
        'source_pdf': str(Path(args.pdf).name),
        'format': args.format,
        'parser': 'deterministic-regex-v1',
        'record_count': len(rows),
        'records': rows,
    }
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {args.out}", file=sys.stderr)


if __name__ == '__main__':
    main()
