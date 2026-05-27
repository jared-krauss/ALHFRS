#!/usr/bin/env python
"""
pdf-extract-deployments.py — Extract LFR deployment records from Met Police PDFs
using pdfplumber for text extraction and Hermes3:8b (local) for JSON structuring.

Usage:
  python pdf-extract-deployments.py --pdf <path> --out <json-output> [--start-id <N>]
                                    [--source-label <str>] [--skip-last-pages <N>]
                                    [--chunk-pages <N>] [--compare <met-police-lfr.json>]

This script:
1. Extracts text from the PDF using pdfplumber
2. Chunks it into manageable sections (by table/page), skipping criteria/policy pages
3. Calls hermes3:8b via Ollama for each chunk to extract structured records
4. Merges and deduplicates results
5. Optionally corroborates against existing dataset (--compare)
6. Writes validated JSON output

Does NOT modify met-police-lfr.json directly — outputs a staging file.
Run validate-dataset.py afterward, then manually merge.

Threshold rules (hardcoded):
  Before 11 Jul 2024 → 0.60
  11–24 Jul 2024     → 0.62
  25 Jul 2024+       → 0.64

Criteria-page skipping:
  Pages whose first 200 chars contain "watchlist", "criteria", or "threshold"
  are skipped entirely as policy/justification pages (logged to stderr).
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

PYTHON        = r"D:\Dev\tools\.venv\Scripts\python.exe"
LLM_TASK      = r"D:\Dev\tools\llm-task.py"
OLLAMA_HOST        = "http://127.0.0.1:11434"
LITELLM_HOST       = "http://127.0.0.1:4000"     # LiteLLM proxy — OpenAI-compatible
LITELLM_MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "")
MODEL_LOCAL        = "hermes3:8b"                 # local fallback
MODEL_FRONTIER     = "frontier-smart"             # DeepSeek V4 Flash via LiteLLM (default for PDFs)

FIELD_SCHEMA = """
CRITICAL EXTRACTION RULES — READ BEFORE PROCESSING:

1. IGNORE any sections about watchlist criteria, crime hotspot justifications,
   threshold justifications, or background/policy documents. These are NOT deployments.

2. ONLY extract rows/entries that represent an actual deployment event.
   A real deployment entry will have ALL THREE of:
   - A specific date (day/month/year)
   - A named location (street, area, or venue)
   - Outcome numbers (faces scanned, alerts, arrests) — even if some are zero or unknown

3. If a section is describing policy or criteria rather than events, output an empty array [].

4. HALLUCINATION GUARD: If you find yourself producing records with suspiciously regular
   date intervals (every 2 weeks, every month, every quarter), you are almost certainly
   hallucinating — output [] instead. Real deployment dates are irregular.

5. If a field value is genuinely not present in the text, use null — do not invent values.

Extract an array of LFR deployment records. Each record must have these fields:
{
  "id":                    "lfr-NNN",           // sequential, filled in later — use "TBD-N"
  "date":                  "YYYY-MM-DD",
  "operator":              "Metropolitan Police",
  "vendor":                "NEC",
  "type":                  "mobile",
  "location_name":         "...",               // exact location as given in the text
  "borough":               "...",               // London borough
  "lat":                   0.0,                 // use your knowledge of London geography
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

Output: JSON array only. No markdown, no explanation. Empty array [] if no real deployments found.
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


# Keywords that indicate a criteria/policy page rather than a deployment record page.
CRITERIA_KEYWORDS = ("watchlist", "criteria", "threshold", "hotspot justification",
                     "background document", "eligibility", "authorisation criteria")


def is_criteria_page(text: str) -> bool:
    """Return True if the page appears to be a policy/criteria page, not a deployment page."""
    snippet = text[:200].lower()
    return any(kw in snippet for kw in CRITERIA_KEYWORDS)


def extract_pdf_text(pdf_path: str, skip_last: int = 0) -> list[str]:
    """Returns list of page texts, skipping criteria/policy pages."""
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber not installed. Run: uv pip install pdfplumber --python D:\\Dev\\tools\\.venv\\Scripts\\python.exe", file=sys.stderr)
        sys.exit(1)

    pages = []
    skipped_criteria = 0
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
            if not text.strip():
                continue
            if is_criteria_page(text):
                print(f"  SKIP page {i+1}: criteria/policy page (contains watchlist/criteria/threshold keywords)", file=sys.stderr)
                skipped_criteria += 1
                continue
            pages.append(f"[Page {i+1}]\n{text.strip()}")
    if skipped_criteria:
        print(f"  Skipped {skipped_criteria} criteria/policy pages total", file=sys.stderr)
    return pages


def _check_litellm_available() -> bool:
    """Check if LiteLLM proxy is reachable."""
    import urllib.request, urllib.error
    try:
        with urllib.request.urlopen(f"{LITELLM_HOST}/health", timeout=3):
            return True
    except Exception:
        return False


def call_llm(chunk: str, source_label: str, model: str = None) -> list[dict]:
    """
    Extract records from a text chunk using the best available model.

    Routing:
      - If model is "frontier-fast" (default) AND LiteLLM is reachable:
          → Gemini 1.5 Flash via LiteLLM at localhost:4000 (faster, more accurate)
      - Fallback: hermes3:8b via Ollama at localhost:11434

    ALHFRS data is public — frontier routing is safe here (no PII).
    """
    import urllib.request, urllib.error

    if model is None:
        model = MODEL_FRONTIER

    schema = FIELD_SCHEMA.replace("<source-label>", source_label)
    prompt = f"{schema}\n\nText to extract from:\n{chunk}"

    # Try LiteLLM / frontier first
    if model != MODEL_LOCAL and _check_litellm_available():
        try:
            payload = json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a precise data extraction assistant. Output only valid JSON arrays."},
                    {"role": "user",   "content": prompt},
                ],
                "temperature": 0.05,
                "max_tokens": 4096,
            }).encode("utf-8")
            _headers = {"Content-Type": "application/json"}
            if LITELLM_MASTER_KEY:
                _headers["Authorization"] = f"Bearer {LITELLM_MASTER_KEY}"
            req = urllib.request.Request(
                f"{LITELLM_HOST}/v1/chat/completions",
                data=payload,
                headers=_headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw = data["choices"][0]["message"]["content"].strip()
            print(f"  [LiteLLM/{model}] extraction complete", file=sys.stderr)
        except Exception as e:
            print(f"  WARNING: LiteLLM call failed ({e}), falling back to local hermes3:8b", file=sys.stderr)
            return call_llm(chunk, source_label, model=MODEL_LOCAL)
    else:
        # Ollama direct path
        if model != MODEL_LOCAL:
            print(f"  LiteLLM unavailable — using local {MODEL_LOCAL}", file=sys.stderr)
        payload = json.dumps({
            "model": MODEL_LOCAL,
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
            print(f"  [Ollama/{MODEL_LOCAL}] extraction complete", file=sys.stderr)
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


# Keep backward-compatible alias
def call_hermes(chunk: str, source_label: str) -> list[dict]:
    """Backward-compatible wrapper — now routes through call_llm()."""
    return call_llm(chunk, source_label, model=MODEL_LOCAL)


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


def load_existing_dataset(json_path: str) -> list[dict]:
    """Load met-police-lfr.json and return the deployments list."""
    try:
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        # Support both top-level array and {"deployments": [...]} shape
        if isinstance(data, list):
            return data
        return data.get("deployments", [])
    except Exception as e:
        print(f"  WARNING: Could not load existing dataset: {e}", file=sys.stderr)
        return []


def corroborate_records(records: list[dict], existing: list[dict]) -> list[dict]:
    """
    Cross-check extracted records against existing dataset.
    Adds a "corroboration_status" field to each record:
      MATCH       — same date + borough exists in existing dataset
      DISCREPANCY — same date exists but location/outcome differs
      NEW         — not found in existing dataset at all

    Prints a summary to stderr.
    """
    # Build lookup: date_start -> list of existing records
    by_date: dict[str, list[dict]] = {}
    for ex in existing:
        d = ex.get("date_start") or ex.get("date", "")
        by_date.setdefault(d, []).append(ex)

    counts = {"MATCH": 0, "DISCREPANCY": 0, "NEW": 0}

    for rec in records:
        rec_date = rec.get("date", "")
        rec_borough = (rec.get("borough") or "").lower().strip()
        rec_location = (rec.get("location_name") or "").lower().strip()

        candidates = by_date.get(rec_date, [])
        status = "NEW"
        if candidates:
            for ex in candidates:
                ex_borough = (ex.get("borough") or "").lower().strip()
                ex_location = (ex.get("location_name") or "").lower().strip()
                # Match on borough (most reliable) or first 20 chars of location
                borough_match = rec_borough and ex_borough and rec_borough == ex_borough
                location_match = rec_location[:20] == ex_location[:20]
                if borough_match or location_match:
                    status = "MATCH"
                    break
            if status == "NEW":
                # Same date exists but no matching location/borough
                status = "DISCREPANCY"

        rec["corroboration_status"] = status
        counts[status] += 1

    print(f"\n  Corroboration summary:", file=sys.stderr)
    print(f"    MATCH       : {counts['MATCH']}", file=sys.stderr)
    print(f"    DISCREPANCY : {counts['DISCREPANCY']}", file=sys.stderr)
    print(f"    NEW         : {counts['NEW']}", file=sys.stderr)

    # Print discrepancies for manual review
    discrepancies = [r for r in records if r.get("corroboration_status") == "DISCREPANCY"]
    if discrepancies:
        print(f"\n  Discrepant records (same date, different location):", file=sys.stderr)
        for r in discrepancies:
            print(f"    {r.get('date')} | extracted: {r.get('location_name')} ({r.get('borough')})", file=sys.stderr)

    return records


def main():
    parser = argparse.ArgumentParser(
        description="Extract LFR deployment records from Met Police PDFs via Hermes3:8b."
    )
    parser.add_argument("--pdf",         required=True)
    parser.add_argument("--out",         required=True, help="Staging output JSON file")
    parser.add_argument("--start-id",    type=int, default=400, help="First ID to assign")
    parser.add_argument("--source-label", default="lfr-deployment-grid-pdf")
    parser.add_argument("--skip-last",   type=int, default=0, help="Skip last N pages (e.g. blank page)")
    parser.add_argument("--chunk-pages", type=int, default=5, help="Pages per Ollama call")
    parser.add_argument("--compare",     metavar="MET_POLICE_LFR_JSON",
                        help="Path to met-police-lfr.json; corroborates extracted records against existing dataset")
    parser.add_argument("--model",       default=MODEL_FRONTIER,
                        help=f"LLM to use: frontier-fast (default, Gemini via LiteLLM), or local (hermes3:8b via Ollama). Use 'local' to force offline mode.")
    args = parser.parse_args()

    # Resolve 'local' shorthand
    if args.model == "local":
        args.model = MODEL_LOCAL

    pdf_path = args.pdf
    print(f"\n=== PDF Extraction: {Path(pdf_path).name} ===", file=sys.stderr)

    pages = extract_pdf_text(pdf_path, skip_last=args.skip_last)
    print(f"  Extracted {len(pages)} non-empty pages (after criteria-page filtering)", file=sys.stderr)

    # Chunk pages for Ollama (context limit)
    chunks = []
    for i in range(0, len(pages), args.chunk_pages):
        chunks.append("\n\n".join(pages[i:i + args.chunk_pages]))
    print(f"  Processing {len(chunks)} chunks ({args.chunk_pages} pages each)", file=sys.stderr)

    all_records = []
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{len(chunks)}...", file=sys.stderr)
        t0 = time.time()
        records = call_llm(chunk, args.source_label, model=args.model)
        elapsed = time.time() - t0
        print(f"    -> {len(records)} records in {elapsed:.1f}s", file=sys.stderr)
        all_records.extend(records)

    print(f"\n  Total before dedup: {len(all_records)}", file=sys.stderr)
    all_records = dedup_records(all_records)
    print(f"  Total after dedup:  {len(all_records)}", file=sys.stderr)

    # Sort by date
    all_records.sort(key=lambda r: r.get("date", ""))

    # Assign real IDs
    all_records = assign_ids(all_records, args.start_id)

    # Optional corroboration against existing dataset
    if args.compare:
        print(f"\n  Corroborating against: {args.compare}", file=sys.stderr)
        existing = load_existing_dataset(args.compare)
        print(f"  Existing dataset: {len(existing)} records", file=sys.stderr)
        all_records = corroborate_records(all_records, existing)

    # Write output
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(all_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Written {len(all_records)} records to {out_path}", file=sys.stderr)
    print(f"  Next available ID: lfr-{args.start_id + len(all_records):03d}", file=sys.stderr)


if __name__ == "__main__":
    main()
