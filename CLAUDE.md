# CLAUDE.md — A London History of Facial Recognition Systems (ALHFRS)
> Claude Code context for this project. For the full human-readable overview see [README.md](README.md).

## What this project is
**ALHFRS** is a multi-year documentary art and data visualisation project by Jared Krauss. It documents facial recognition system deployments across London — by the Metropolitan Police, British Transport Police, and private retail operators — and critically examines their legal basis, demographic impact, and accountability gaps.

**Primary output:** An interactive website with a Leaflet deployment map, Gaussian splat embeds of physical deployment locations, and a community submission workflow.

**Current state (May 2026):**
- Deployment data: **371 records** in `met-police-lfr.json` (schema v1.2); 2020–2026 coverage with gaps in 2024
- The 2024 cohort is the largest gap — Garbett Excel is the right source but not yet migrated
- Legal data: 4 court cases / ICO enforcement actions
- News archive: 21 research articles
- Map: Live Leaflet map with marker clustering (`leaflet.markercluster`), year-filter timeline strip, 4 layers
- Splats: `splats/index.json` manifest in place; no splat files captured yet
- Website, community workflow: architecture planned, not yet built

## Directory map
```
ALHFRS/
├── CLAUDE.md                    this file
├── README.md                    human-readable project overview (data sources, schema, pipeline)
├── agents/
│   └── README.md                three agent persona definitions for subagent dispatch
├── data/
│   ├── deployments/             structured JSON deployment records (schema v1.2)
│   │   ├── met-police-lfr.json      8 Met Police LFR deployments (2020–2026)
│   │   ├── btp-lfr.json             2 British Transport Police LFR trials (Feb 2026)
│   │   ├── private-operators.json   5 Facewatch/Sainsbury's retail FRS records
│   │   └── retrospective-fr.json    4 RFR false-positive incidents (schema v1.0)
│   ├── legal/
│   │   └── enforcement-actions.json 4 court cases and ICO regulatory actions
│   ├── news/
│   │   └── gmail-research-threads.json 21 archived research articles (2024–2026)
│   ├── interactions/            placeholder — MOPAC stop-and-search demographics (TBD)
│   └── community/               placeholder — community submissions workflow (TBD)
├── map/
│   ├── index.html               Leaflet map entry point (serve via HTTP, not file://)
│   ├── js/                      6 ES6 modules: config, borough-layer, deployment-layer,
│   │                                layer-controls, legend, main
│   ├── london-boroughs.js       dead code — not imported anywhere (see map/README.md)
│   └── data/
│       ├── london-boroughs.geojson  borough boundaries (used by map)
│       └── london-wards.geojson     ward boundaries (loaded in config, not yet surfaced)
├── scripts/
│   ├── validate-dataset.py          schema + data quality validator (stdlib only)
│   ├── pdf-extract-deployments.py   pdfplumber + Hermes3:8b PDF → staging JSON extractor
│   ├── extract-pdf.py             new script for local LLM PDF extraction pipeline
│   └── geocode-batch.py           batch geocoding script for null lat/lon records
├── data/
│   └── staging/
│       ├── extract-2020-2022.json      9 records (merged into main ✓)
│       ├── extract-2023-2024.json      30 records (POOR QUALITY — hallucinated, do not merge)
│       └── gemini-2021-extraction.json 5 records from Gemini 3.5 Flash (2026-05-26, needs verification before merge — see Known Issues)
├── serve.ps1                        Start HTTP server on port 8741 (PowerShell, coloured output)
├── serve.bat                        Start HTTP server on port 8741 (batch, minimal)
├── tasks/
│   ├── map-future-goals.md          Backlog for map-embed.html (Wayback Machine enrichment, etc.)
│   ├── gemini-prompt-lfr-extraction.md  Full extraction prompt for LFR deployment data
│   ├── gemini-prompt-geocoding.md   Geocoding prompt for 169 null lat/lon records
│   └── gemini-output-merge-instructions.md  Instructions for merging staging JSON into main dataset
├── site/                        placeholder — website scaffold (TBD)
├── splats/
│   ├── README.md                index-only approach, hosting options, map integration plan
│   └── index.json               manifest (empty — no splats captured yet)
└── .claude/
    └── commands/
        └── data-review.md       /data-review slash command definition
```

## Running the map
**The map auto-starts on login** via Windows Task Scheduler ("ALHFRS Map Server"). Just open:

```
http://localhost:8741/map-embed.html
```

To start manually:
```powershell
Start-Process -FilePath "http://localhost:8741/map-embed.html"
```

# From D:\Dev\ALHFRS\  — two options:
.\serve.ps1          # PowerShell with coloured output
serve.bat            # minimal batch file

# Or directly:
python -m http.server 8741

**Must use HTTP, not file://.** `fetch()` calls fail under `file://` (Chrome CORS). If the map shows a load error banner, verify you're on `http://localhost:8741`.

**Two map builds exist:**
- `map-embed.html` — single-file self-contained build (the active build). Includes operator filter, year timeline, news panel, splat panel.
- `map/index.html` — modular ES6 build (older; maintained separately in `map/js/`).

**Recent changes:**
- Added semantic operator-type colors and halation aesthetics.
- Merged 35 new records from Met PDF (2023, 2025, 2020).
- Merged 20 orphan/duplicate pairs from 2024 reverification.
- Reverified 2024 records against Met PDF — fixed 53 date swaps and added 32 records.
- Added lfr-536 Walworth Rd 2024-11-01 (missed by Garbett extraction).
- Updated README with 366 records, schema v1.2, staging dir, splats index, map features.
- Updated CLAUDE.md with 366 records, v1.2 schema, LLM pipeline, open issues.
- Added Walworth 2024 Gaussian splat panel to `map-embed.html`.
- Added scripts/README.md with validate-dataset.py reference.
- Added 2026-05-18 project audit + mempalace note in CLAUDE.md.
- Updated map-embed.html for resilient fetch, news panel, and PDF script enhancements.
- Added multi-select filters, year/month filter strip, mobile layout, null-coord fix to `map-embed.html`.
- Added 169 Garbett 2024 LFR records (lfr-367 to lfr-535).
- Updated map to load deployments from JSON files instead of stale inline data.
- Added borough filter + live count in timeline strip; fixed stated_purpose on 2020-22 records.
- Updated README with 366 records, schema v1.2, staging dir, splats index, and map features.
- Updated CLAUDE.md with 366 records, v1.2 schema, LLM pipeline, open issues.
- Merged 2020-2022 staging records (9 new deployments, lfr-358 to lfr-366).
- Added local LLM PDF extraction pipeline + 2020-22 staging data.

## Local LLM extraction pipeline
PDF extraction uses `scripts/extract-pdf.py` (requires `D:\Dev\tools\.venv`):

```powershell
python scripts/extract-pdf.py --input D:\Data\met-pdfs --output D:\Output\deployments.json
```

This script extracts deployment data from PDFs and saves it in JSON format. Ensure the virtual environment is activated before running the script.

For more details, refer to `scripts/README.md`.

---
# From D:\Dev\ALHFRS\
& "D:\Dev\tools\.venv\Scripts\python.exe" scripts\pdf-extract-deployments.py `
    --pdf "path\to\file.pdf" `
    --out "data\staging\extract-YYYY.json" `
    --start-id 400 `
    --source-label "source-label-here" `
    --skip-last 1   # skip blank last page if needed

**Known issue:** Complex PDFs with watchlist-criteria sections confuse Hermes3 — it hallucinates regular-interval records. Skip criteria pages by checking first 200 chars of each page for "watchlist"/"criteria"/"threshold". The 2023-24 extract is unusable; needs Gemini or prompt refinement.

**Corroboration:** Cross-reference across sources — discrepancies (same date, different location name) are analytically valuable. `met-police-lfr.json` has a `corroboration_notes` array for flagged discrepancies.

General LLM task harness: `D:\Dev\tools\llm-task.py` — supports extract-json, summarize, update-md, tag, classify. Models: `hermes3:8b` (structured), `qwen3:8b` (writing), `qwen3:8b-lean` (fast).
---

## Data schema overview
All deployment files use **schema v1.2**. Required fields per record:

| Field | Type | Notes |
|---|---|---|
| `id` | string | Unique (e.g. `lfr-001`, `priv-003`, `btp-002`) |
| `operator` | string | Full operator name |
| `lat` / `lon` | float | Within Greater London bounds: lat 51.28–51.69, lon -0.51–0.34 |
| `date_start` | ISO 8601 | YYYY-MM-DD |
| `data_quality` | enum | `confirmed` / `approximate` / `unverified` |
| `source_url` | string | Specific document URL — not a generic homepage |
| `source_type` | enum | `FOI_disclosure` / `news_report` / `court_record` / `police_statement` / `operator_statement` / `ngo_report` |

See [data/README.md](data/README.md) for the full 19-field schema and schema variants for retrospective FR and legal files.

## Data quality levels
These three values are the project's core accuracy signal. Treat them as a contract:

- **`confirmed`** — primary source (Met FOI disclosure, ICO enforcement notice, court judgment, official police statement). Requires a specific `source_url` (not a generic homepage).
- **`approximate`** — location or date inferred from adjacent evidence; not directly stated in a primary source. Must have `notes` explaining what was approximated and why.
- **`unverified`** — single secondary source; cannot yet be cross-referenced. Flags for follow-up; never publish without upgrading.

Do not upgrade a record's `data_quality` without adding a primary-source `source_url`.

## Source hierarchy
When evaluating or adding sources, highest to lowest confidence:

1. Met Police FOI disclosure or official published deployment log
2. ICO enforcement notice or court judgment
3. Official police press release or statement
4. NGO report (Big Brother Watch, Liberty) citing specific detail
5. Journalism citing a named source
6. Journalism without named source / general claims

## Key invariants
- **No speculative records.** Every deployment must trace to a verifiable source.
- **No code changes without running the validator.** Run `python scripts/validate-dataset.py <file>` before modifying any deployment JSON.
- **`retrospective-fr.json` uses a different schema.** RFR incidents (post-event FR applied to footage) use `incidents[]` not `deployments[]`, and have different coordinate fields (`footage_lat/lon`, `arrest_lat/lon`). The validator handles both.
- **Three FR technology types exist** — distinguish them clearly:
  1. **LFR (Live Facial Recognition)** — real-time camera scanning against watchlist (`met-police-lfr.json`, `btp-lfr.json`)
  2. **RFR (Retrospective FR)** — FR applied to existing footage after an incident (`retrospective-fr.json`)
  3. **OIFR (Operator-Initiated FR)** — handheld on-demand matching (not yet documented in data files)
- **Private operator records (`priv-*`) all use `approximate` dating.** Facewatch go-live dates were never publicly disclosed; 2022-01-01 is inferred from press coverage of the rollout.
- **New records added:** 35 new records from Met PDF (2023, 2025, 2020), 169 Garbett 2024 LFR records (lfr-367 to lfr-535), and 2025-2026 LFR records (lfr-032 to lfr-357).
- **Schema updated:** v1.2 schema now includes semantic operator-type colors and poppy pastel halation aesthetic.
- **Data verification:** Reverified 2024 records against Met PDF, fixed 53 date swaps, added 32 records.
- **Tooling updates:** Added local LLM PDF extraction pipeline for 2020-22 staging data.

## Agent persona dispatch
Three subagent personas are defined in `agents/README.md`. Route work accordingly:

| Persona | When to invoke |
|---|---|
| **Project Development Lead** | Schema changes, backlog items, PR review, splat pipeline coordination |
| **Data Cleanup & Verification** | Adding or reviewing records, sourcing, data_quality auditing, validator output triage |
| **Marketing & Public Rollout** | Artist statements, exhibition copy, press releases, community outreach, social media |

**Current orchestration stack:** Claude Code + local LLM harness (`D:\Dev\tools\llm-task.py`). Ollama at `localhost:11434` with hermes3:8b and qwen3:8b available. LiteLLM proxy at port 4000 (registered in Task Scheduler, may not be running — check before use).

**MemPalace semantic memory** is available for this project. ChromaDB palace at `D:\MemPalace\palace` with 8,000+ indexed drawers. Access via the `mempalace-mcp.exe` MCP (29 tools) in Claude Code sessions. The `hermes` wing auto-indexes Layer-2 synthetic notes. Use semantic search over all project docs, prior research notes, and vault content before starting any new extraction or analysis work. Project files at `D:\Dev\MemPalace\`.

**Recent changes:**
- Merged semantic operator-type colors + halation aesthetic
- Added 35 new records from Met PDF (2023, 2025, 2020)
- Merged 20 orphan/duplicate pairs from 2024 reverification
- Reverified 2024 records against Met PDF — fixed 53 date swaps, added 32 records
- Added lfr-536 Walworth Rd 2024-11-01 (missed by Garbett extraction)
- Added 2026-05-18 project audit + mempalace note in CLAUDE.md
- Merged semantic operator-type colors + poppy pastel halation aesthetic
- Fixed resilient fetch, news panel, PDF script enhancements
- Added multi-select filters, year/month filter strip, mobile layout, null-coord fix
- Added 169 Garbett 2024 LFR records (lfr-367 to lfr-535)
- Loaded deployments from JSON files instead of stale inline data
- Added borough filter + live count in timeline strip; fixed stated_purpose on 2020-22 records
- Updated README — 366 records, schema v1.2, staging dir, splats index, map features
- Updated CLAUDE.md — 366 records, v1.2 schema, LLM pipeline, open issues
- Merged 2020-2022 staging records (9 new deployments, lfr-358 to lfr-366)
- Added local LLM PDF extraction pipeline + 2020-22 staging data
- Added 2025-2026 LFR records (lfr-032 to lfr-357) + splats index + docs
- Added 2023 deployment records (lfr-009â€“031) + marker clustering + year-filter timeline strip
- Added Walworth 2024 Gaussian splat panel to map embed
- Added scripts/README.md with validate-dataset.py reference

## /data-review command
Run a combined automated + LLM review of any deployment file:

```
/data-review
```

Defined in `.claude/commands/data-review.md`. It runs the validator then applies a structured review checklist (duplicates, coordinate bounds, data_quality assignment, source quality, temporal anomalies, missing annotations, schema consistency). Output is a structured severity table.

## Deferred features (placeholder directories)
These are explicitly unbuilt — their directories are `.gitkeep` placeholders:

| Directory | What goes here | Current state |
|---|---|---|
| `site/` | Published website (static or SSG) | Schema planned, no code |
| `splats/` | Gaussian splat captures indexed in `splats/index.json`; binary files excluded by `.gitignore` | `index.json` manifest live, no splats captured yet |
| `data/interactions/` | MOPAC stop-and-search demographic data by borough/ward | Schema not yet designed |
| `data/community/` | Community-submitted photos/videos of active deployments | Moderation workflow TBD |

Do not create files in these directories without a plan for the accompanying schema.

## Task Scheduler entries (auto-start on login)
| Task name | What it does |
|---|---|
| `ALHFRS Map Server` | `python -m http.server 8741` from `D:\Dev\ALHFRS\` |
| `Hermes Agent` | Watches Layer-1_Inbox, routes new notes through Ollama → Layer-2 |

Both registered 2026-05-26. If something isn't running: open Task Scheduler → find entry → right-click → Run.

## Known issues / open work (May 2026)
1. **2024 cohort missing** — records jump from 2023 (lfr-031) to 2025 (lfr-032). The Garbett Excel covers 2020–2025 with 254 records and contains 2024 data. Needs migration.

2. **2023-24 PDF extraction poor quality** — `data/staging/extract-2023-2024.json` has 30 hallucinated records with regular 2-week intervals. Do not merge. Needs Gemini API or revised prompt that skips watchlist-criteria sections.

3. **Corroboration discrepancies logged** — `corroboration_notes` in `met-police-lfr.json`: same-date records with different location names from different sources (2020-02-11, 2020-02-27). Analytically interesting — don't resolve blindly.

4. **`map/data/london-wards.geojson` (1.05 MB) has no layer toggle yet.** Ward-level boundaries loaded in config; toggle planned.

5. **Some news archive URLs are share.google redirects.** `data/news/gmail-research-threads.json` — `url_canonical` partially filled; remainder need resolving.

6. **`lfr-006` (Liverpool Street) has null `ward`.** City of London ward data needs populating.

7. **Outcome data sparse.** Most records have null outcomes — intentional where data isn't public. Only a few records have `outcome_arrests` populated.

8. **Gemini 2021 extraction unreliable.** `data/staging/gemini-2021-extraction.json` (5 records, 2026-05-26): The "zero deployments in 2021" claim likely contradicts our existing data. Croydon 173 arrest figure is probably an annual total misattributed to a single deployment. Victoria + Tottenham 2026-05-18 records (from itnews.com.au) are genuinely new and probably addable after de-duplication check. **Do not merge this file wholesale — validate record by record.**

9. **169 null lat/lon records** need geocoding. Prompt ready at `tasks/gemini-prompt-geocoding.md`; data at `data/staging/geocoding-needed.json`.

10. **News panel Wayback Machine enrichment** deferred. Logged in `tasks/map-future-goals.md`. Proposed: `scripts/enrich-news-wayback.py` checks `archive.org/wayback/available` for each article URL, stores `url_wayback` in news JSON.

11. **2024 records from Met PDF (2023, 2025, 2020)** — need verification and integration into existing data.

12. **Orphan/duplicate pairs from 2024 reverification** — need manual resolution to ensure accuracy.

13. **Date swaps fixed in 2024 records** — additional records added as part of reverification process.

14. **New deployment record for Walworth Rd (lfr-536)** — needs validation and integration.

15. **Wayback Machine enrichment script deferred** — plan to implement after current priorities are completed.

## Archive
`_archive/` is gitignored and holds dead code preserved for reference:

- `map-london-boroughs.js` — hardcoded 23-borough GeoJSON that was once in `map/`. Superseded by the full-resolution `map/data/london-boroughs.geojson`. Do not import or restore.
- Additional files may be added to this directory as part of project history and reference.