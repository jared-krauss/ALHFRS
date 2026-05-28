#!/usr/bin/env python3
"""
extract-pdf.py — Gemini Cloud extractor for Met Police LFR deployment grid PDFs.

Companion to parse-met-pdf.py (deterministic regex). Run both on the same PDF,
then use diff-pdf-vs-dataset.py to compare the three extractions before merging.

Two prompt variants differ in their row-anchoring heuristic:
  --variant a  date-anchored  (misses rows where dates are on continuation lines)
  --variant b  location-anchored (catches rows with blank/N/A outcome columns)

Usage:
  python scripts/extract-pdf.py \\
      --pdf data/source-pdfs/met-lfr-grid-2023-to-2024.pdf \\
      --out data/staging/extract-gemini-a-2023-2024.json \\
      --variant a

  python scripts/extract-pdf.py \\
      --pdf data/source-pdfs/met-lfr-grid-2020-2022.pdf \\
      --out data/staging/extract-gemini-b-2020-2022.json \\
      --variant b

Requirements:
  pip install google-generativeai --break-system-packages
  GOOGLE_API_KEY must be set in the environment.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path


GEMINI_MODEL = "gemini-2.0-flash"

# Variant A: anchor extraction from date column.
# Best for dense, well-formatted rows; misses rows where a location wraps
# across lines and the date appears on the second physical line.
PROMPT_A = """\
You are extracting structured data from a Metropolitan Police Live Facial \
Recognition (LFR) deployment grid PDF.

Each row in the table represents one deployment operation. \
ANCHOR FROM THE DATE COLUMN: for every row that contains a date in DD/MM/YY \
or DD/MM/YYYY format, extract all values on that row plus any continuation \
lines that belong to the same deployment (location text sometimes wraps).

For each deployment row extract the following fields exactly as printed:

  location_name                  — deployment location (join continuation lines)
  date_start                     — ISO 8601 YYYY-MM-DD
  date_end                       — ISO 8601 YYYY-MM-DD (same as date_start if single day)
  duration_raw                   — duration string as printed, e.g. "6h 21m"
  stated_purpose                 — stated purpose, e.g. "Crime Hotspot"
  watchlist_size                 — integer
  threshold                      — decimal, e.g. 0.64
  outcome_alerts                 — total alerts integer
  outcome_true_alerts_confirmed  — integer
  outcome_true_alerts_unconfirmed — integer
  outcome_false_alerts_confirmed  — integer
  outcome_false_alerts_unconfirmed — integer
  outcome_false_alert_rate_pct   — decimal percentage
  outcome_arrests                — integer
  outcome_other_action           — integer
  outcome_no_action              — integer
  outcome_faces_scanned          — integer

Rules:
- Set any missing or unavailable field to null.
- Do NOT invent, estimate, or infer numbers — only extract values printed on the page.
- Do NOT include header rows, summary totals, or metadata rows.
- Output ONLY a valid JSON array, no markdown fences, no prose.

Example element (field order does not matter):
{"location_name":"Stratford Broadway","date_start":"2024-01-15","date_end":"2024-01-15",\
"duration_raw":"6h 21m","stated_purpose":"Crime Hotspot","watchlist_size":10500,\
"threshold":0.64,"outcome_alerts":18,"outcome_true_alerts_confirmed":2,\
"outcome_true_alerts_unconfirmed":0,"outcome_false_alerts_confirmed":16,\
"outcome_false_alerts_unconfirmed":0,"outcome_false_alert_rate_pct":88.89,\
"outcome_arrests":3,"outcome_other_action":0,"outcome_no_action":15,\
"outcome_faces_scanned":22415}
"""

# Variant B: anchor extraction from location names.
# Catches rows where outcome columns are blank or show N/A, and rows where
# the location text spans multiple physical lines before the date appears.
PROMPT_B = """\
You are extracting structured data from a Metropolitan Police Live Facial \
Recognition (LFR) deployment grid PDF.

Each row in the table represents one deployment operation. \
ANCHOR FROM LOCATION NAMES: identify every named street, area, or location \
that appears as a table row entry, then extract the date and all numeric/text \
columns on the same row. This approach catches rows where outcome columns are \
blank, show N/A, or where a date appears after the location text wraps to the \
next physical line.

For each deployment row extract the following fields exactly as printed:

  location_name                  — deployment location (join continuation lines)
  date_start                     — ISO 8601 YYYY-MM-DD
  date_end                       — ISO 8601 YYYY-MM-DD (same as date_start if single day)
  duration_raw                   — duration string as printed, e.g. "6h 21m"
  stated_purpose                 — stated purpose, e.g. "Crime Hotspot"
  watchlist_size                 — integer
  threshold                      — decimal, e.g. 0.64
  outcome_alerts                 — total alerts integer
  outcome_true_alerts_confirmed  — integer
  outcome_true_alerts_unconfirmed — integer
  outcome_false_alerts_confirmed  — integer
  outcome_false_alerts_unconfirmed — integer
  outcome_false_alert_rate_pct   — decimal percentage
  outcome_arrests                — integer
  outcome_other_action           — integer
  outcome_no_action              — integer
  outcome_faces_scanned          — integer

Rules:
- Set any missing or unavailable field to null.
- Do NOT invent, estimate, or infer numbers — only extract values printed on the page.
- Do NOT include header rows, summary totals, or metadata rows.
- Output ONLY a valid JSON array, no markdown fences, no prose.
"""

PROMPTS = {'a': PROMPT_A, 'b': PROMPT_B}


def upload_and_wait(genai, pdf_path: str, timeout: int = 120):
    """Upload PDF to Gemini File API and wait until ACTIVE."""
    print(f"  Uploading {Path(pdf_path).name}...", file=sys.stderr)
    uploaded = genai.upload_file(
        path=pdf_path,
        mime_type="application/pdf",
        display_name=Path(pdf_path).stem,
    )

    deadline = time.time() + timeout
    while time.time() < deadline:
        f = genai.get_file(uploaded.name)
        if f.state.name == "ACTIVE":
            return f
        if f.state.name == "FAILED":
            print(f"ERROR: File processing failed: {uploaded.name}", file=sys.stderr)
            sys.exit(1)
        time.sleep(2)

    print("ERROR: Timed out waiting for file to become ACTIVE", file=sys.stderr)
    sys.exit(1)


def extract(pdf_path: str, variant: str, api_key: str) -> list[dict]:
    try:
        import google.generativeai as genai
    except ImportError:
        print("ERROR: google-generativeai not installed. Run:", file=sys.stderr)
        print("  pip install google-generativeai --break-system-packages", file=sys.stderr)
        sys.exit(1)

    genai.configure(api_key=api_key)
    file_ref = upload_and_wait(genai, pdf_path)

    model = genai.GenerativeModel(GEMINI_MODEL)
    print(f"  Extracting (variant {variant})...", file=sys.stderr)
    response = model.generate_content(
        [file_ref, PROMPTS[variant]],
        generation_config={"response_mime_type": "application/json"},
    )

    try:
        genai.delete_file(file_ref.name)
    except Exception:
        pass

    text = response.text.strip()
    # Strip markdown fences if the model adds them despite instructions
    if text.startswith("```"):
        lines = text.split('\n')
        text = '\n'.join(lines[1:])
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]

    try:
        records = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"ERROR: Gemini response is not valid JSON: {e}", file=sys.stderr)
        print(f"First 500 chars of response:\n{text[:500]}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(records, list):
        print(f"ERROR: Expected JSON array, got {type(records).__name__}", file=sys.stderr)
        sys.exit(1)

    return records


def main():
    ap = argparse.ArgumentParser(
        description='Extract Met LFR deployment data from a PDF using Gemini Cloud API.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument('--pdf', required=True,
                    help='Path to source PDF (e.g. data/source-pdfs/met-lfr-grid-2023-to-2024.pdf)')
    ap.add_argument('--out', required=True,
                    help='Output staging JSON file path')
    ap.add_argument('--variant', choices=['a', 'b'], default='a',
                    help='a=date-anchored (default), b=location-anchored')
    args = ap.parse_args()

    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("ERROR: GOOGLE_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    print(f"PDF:     {pdf_path}", file=sys.stderr)
    print(f"Variant: {args.variant}", file=sys.stderr)
    print(f"Model:   {GEMINI_MODEL}", file=sys.stderr)

    records = extract(str(pdf_path), args.variant, api_key)

    out = {
        'source_pdf': pdf_path.name,
        'model': GEMINI_MODEL,
        'prompt_variant': args.variant,
        'extractor': 'gemini-file-api',
        'record_count': len(records),
        'records': records,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(records)} records → {args.out}", file=sys.stderr)


if __name__ == '__main__':
    main()
