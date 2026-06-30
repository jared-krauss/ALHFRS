# Task: Fill 2021 ALHFRS Data Gap

**Status:** TODO  
**Priority:** Medium  
**Created:** 2026-05-26  
**Updated:** 2026-06-30

## Context

The met-police-lfr.json dataset (654 records as of June 2026) has no 2021 entries. Years present: 2016–2020, 2022–2026. The 2020–2024 PDF extraction session hit a rate limit and likely missed 2021 records entirely.

## Sources to check

- **MPS Annual Reports 2021** — [met.police.uk/foi/](https://www.met.police.uk/foi/) — annual statistics on LFR deployments
- **Garbett 2021 data** — check if there is an Excel/CSV equivalent to the 2024 Garbett file for 2021
- **HMICFRS inspection reports** — Her Majesty's Inspectorate covers LFR use; 2021 inspection may cite specific deployments
- **Big Brother Watch / Liberty reports** — both published LFR reports covering 2020–2022 period
- **FOI requests** — existing FOI releases on met.police.uk may cover 2021

## Approach — use Gemini (free tier) for extraction

Since this is document extraction from PDFs/public sources, route to Gemini 1.5 Flash via Google AI Studio (free) rather than running locally.

**Option A — Manual (Jared does it):**
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Upload the relevant 2021 PDFs (MPS annual report, HMICFRS, BBW reports)
3. Prompt: *"Extract all Live Facial Recognition deployment events from this document. For each: operator, location name, date (start and end if available), deployment type (enforcement/pilot/event), outcome if stated. Return as JSON array."*
4. Paste output into `data/staging/garbett-2021-staging.json` following existing schema
5. Run `python scripts/merge-staging.py` to merge into met-police-lfr.json

**Option B — Automated via Gemini API directly (LiteLLM is decommissioned 2026-06-15):**
- Set `GOOGLE_API_KEY` in Windows environment variables
- Run `pdf-extract-deployments.py` against 2021 PDFs pointing directly at the Google AI Studio endpoint

## Schema reminder

```json
{
  "id": "lfr-NNN",
  "operator": "Metropolitan Police Service",
  "deployment_type": "enforcement|pilot|event",
  "location_name": "...",
  "location_area": "...",
  "lat": null,
  "lon": null,
  "date_start": "2021-MM-DD",
  "date_end": "2021-MM-DD",
  "outcome": "...",
  "source": "...",
  "notes": "..."
}
```

Next available ID after merge: `lfr-679` (max ID in met-police-lfr.json is `lfr-678` as of 2026-06-30).

## After extraction

- Run geocoding pass on new records (lat/lon currently null on 2024 batch too)
- Update map — year chips will auto-populate from data
