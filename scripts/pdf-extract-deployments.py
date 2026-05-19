#!/usr/bin/env python
"""
pdf-extract-deployments.py — Extract LFR deployment records from Met Police PDFs
using pdfplumber for text extraction and Hermes3:8b (local) for JSON structuring.

Usage:
  python pdf-extract-deployments.py --pdf <path> --out <json-output> [--start-id <N>]
                                    [--source-label <str>] [--skip-last-pages <N>]

This script:
1. Extracts text from the PDF using pdfplumber
2. Chunks it into manageable sections (by table/page)
3. Calls hermes3:8b via Ollama for each chunk to extract structured records
4. Merges and deduplicates results
5. Writes validated JSON output

Does NOT modify met-police-lfr.json directly — outputs a staging file.
Run validate-dataset.py afterward, then manually merge.

Threshold rules (hardcoded):
  Before 11 Jul 2024 → 0.60
  11–24 Jul 2024     → 0.62
  25 Jul 2024+       → 0.64
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

PYTHON     = r"D:\Dev\tools\.venv\Scripts\python.exe"
LLM_TASK   = r"D:\Dev\tools\llm-task.py"
OLLAMA_HOST = "http://127.0.0.1:11434"
MODEL      = "hermes3:8b"

FIELD_SCHEMA = """
Extract an array of LFR deployment records. Each record must have these fields:
{
  "id":                    "lfr-NNN",           // sequential, filled in later — use "TBD-N"
  "date":                  "YYYY-MM-DD",
  "operator":              "Metropolitan Police",
  "vendor":                "NEC",
  "type":                  "mobile",
  "location_name":         "...",               // exact location as given
  "borough":               "...",               // London borough
  "lat":                   0.0,                 // use your knowledge of London
  "lng":                   0.0,
  "status":                "completed",
  "outcome_faces_scanned": null,                // integer or null
  "outcome_alerts":        null,                // integer or null
  "outcome_arrests":       null,                // integer or null
  "threshold":             0.60,                // see rules below
  "event_name":            null,                // named event or null
  "event_type":            "routine",           // routine|sporting|carnival|state_event|public_order|cnit
  "camera_count":          null,
  "duration_hours":        null,
  "watchlist_size":        null,
  "notes":                 "",
  "sources":               ["<source-label>"]
}

Threshold rules:
- date before 2024-07-11 → 0.60
- date 2024-07-11 to 2024-07-24 → 0.62
- date 2024-07-25 or later → 0.64

Output: JSON array only. No markdown, no explanation.
"""


def threshold_for(date_str: str) -> float:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        if d >= date(2024, 7, 25):
            return 0.64
        if d >= date(2024, 7, 11):
            return 0.62
        return 0.60
    except Exception:
        return 0.60


def extract_pdf_text(pdf_path: str, skip_last: int = 0) -> list[str]:
    """Returns list of page texts."""
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber not installed. Run: uv pip install pdfplumber --python D:\\Dev\\tools\\.venv\\Scripts\\python.exe", file=sys.stderr)
        sys.exit(1)

    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        end = total - skip_last if skip_last > 0 else total
        print(f"  PDF has {total} pages, processing {end}", file=sys.stderr)
        for i, page in enumerate(pdf.pages[:end]):
            text = page.extract_text() or ""
            # Also try table extraction
            tables = page.extract_tables()
            if tables:
                for tbl in tables:
                    for row in tbl:
                        if row:
                            text += "\n" + " | ".join(str(c or "") for c in row)
            if text.strip():
                pages.append(f"[Page {i+1}]\n{text.strip()}")
    return pages


def call_hermes(chunk: str, source_label: str) -> list[dict]:
    """Call hermes3:8b to extract records from a text chunk."""
    schema = FIELD_SCHEMA.replace("<source-label>", source_label)
    prompt = f"{schema}\n\nText to extract from:\n{chunk}"

    import urllib.request, urllib.error
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.05},
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw = data.get("response", "").strip()
    except Exception as e:
        print(f"  WARNING: Ollama call failed: {e}", file=sys.stderr)
        return []

    # Strip markdown fences
    raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'\s*```\s*$', '', raw, flags=re.MULTILINE)

    try:
        records = json.loads(raw)
        if isinstance(records, dict):
            records = [records]
        return records if isinstance(records, list) else []
    except json.JSONDecodeError as e:
        print(f"  WARNING: JSON parse failed: {e}\n  Raw (first 300): {raw[:300]}", file=sys.stderr)
        return []


def assign_ids(records: list[dict], start_id: int) -> list[dict]:
    """Replace TBD-N IDs with real sequential IDs."""
    counter = start_id
    for r in records:
        r["id"] = f"lfr-{counter:03d}"
        # Recalculate threshold from date
        if r.get("date"):
            r["threshold"] = threshold_for(r["date"])
        counter += 1
    return records


def dedup_records(records: list[dict]) -> list[dict]:
    """Remove exact-date+location duplicates."""
    seen = set()
    out = []
    for r in records:
        key = (r.get("date", ""), r.get("location_name", "").lower()[:30])
        if key not in seen:
            seen.add(key)
            out.append(r)
        else:
            print(f"  DEDUP: skipped duplicate {key}", file=sys.stderr)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf",         required=True)
    parser.add_argument("--out",         required=True, help="Staging output JSON file")
    parser.add_argument("--start-id",    type=int, default=400, help="First ID to assign")
    parser.add_argument("--source-label",default="lfr-deployment-grid-pdf")
    parser.add_argument("--skip-last",   type=int, default=0, help="Skip last N pages (e.g. blank page)")
    parser.add_argument("--chunk-pages", type=int, default=5, help="Pages per Ollama call")
    args = parser.parse_args()

    pdf_path = args.pdf
    print(f"\n=== PDF Extraction: {Path(pdf_path).name} ===", file=sys.stderr)

    pages = extract_pdf_text(pdf_path, skip_last=args.skip_last)
    print(f"  Extracted {len(pages)} non-empty pages", file=sys.stderr)

    # Chunk pages for Ollama (context limit)
    chunks = []
    for i in range(0, len(pages), args.chunk_pages):
        chunks.append("\n\n".join(pages[i:i+args.chunk_pages]))
    print(f"  Processing {len(chunks)} chunks ({args.chunk_pages} pages each)", file=sys.stderr)

    all_records = []
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{len(chunks)}...", file=sys.stderr)
        t0 = time.time()
        records = call_hermes(chunk, args.source_label)
        elapsed = time.time() - t0
        print(f"    → {len(records)} records in {elapsed:.1f}s", file=sys.stderr)
        all_records.extend(records)

    print(f"\n  Total before dedup: {len(all_records)}", file=sys.stderr)
    all_records = dedup_records(all_records)
    print(f"  Total after dedup:  {len(all_records)}", file=sys.stderr)

    # Sort by date
    all_records.sort(key=lambda r: r.get("date", ""))

    # Assign real IDs
    all_records = assign_ids(all_records, args.start_id)

    # Write output
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(all_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✓ Written {len(all_records)} records to {out_path}", file=sys.stderr)
    print(f"  Next available ID: lfr-{args.start_id + len(all_records):03d}", file=sys.stderr)


if __name__ == "__main__":
    main()
