# CLAUDE.md — A London History of Facial Recognition Systems (ALHFRS)

> Claude Code context for this project. For the full human-readable overview see [README.md](README.md).

---

## What this project is

**ALHFRS** is a multi-year documentary art and data visualisation project by Jared Krauss. It documents facial recognition system deployments across London — by the Metropolitan Police, British Transport Police, and private retail operators — and critically examines their legal basis, demographic impact, and accountability gaps.

**Primary output:** An interactive website with a Leaflet deployment map, Gaussian splat embeds of physical deployment locations, and a community submission workflow.

**Current state (May 2026):**
- Deployment data: 15 active records across 4 JSON files (Met Police, BTP, private operators, retrospective FR)
- Legal data: 4 court cases / ICO enforcement actions
- News archive: 21 research articles
- Map: Live Leaflet prototype with 4 layers (Met, BTP, private, borough boundaries)
- Website, splats, community workflow: architecture planned, not yet built

---

## Directory map

```
ALHFRS/
├── CLAUDE.md                    this file
├── README.md                    human-readable project overview (data sources, schema, pipeline)
├── agents/
│   └── README.md                three agent persona definitions for subagent dispatch
├── data/
│   ├── deployments/             structured JSON deployment records (schema v1.1)
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
│   └── validate-dataset.py      schema + data quality validator (stdlib only)
├── site/                        placeholder — website scaffold (TBD)
├── splats/                      placeholder — Gaussian splat directories (TBD)
└── .claude/
    └── commands/
        └── data-review.md       /data-review slash command definition
```

---

## Running the map

```powershell
# From D:\Dev\ALHFRS\
python -m http.server 8000
# Open: http://localhost:8000/map/index.html
```

**Must use HTTP, not file://.** `fetch()` calls in the map JS are blocked by the browser under `file://` origins. If the map shows a load error banner, check you're on `http://localhost:8000`.

---

## Data schema overview

All deployment files use **schema v1.1**. Required fields per record:

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

---

## Data quality levels

These three values are the project's core accuracy signal. Treat them as a contract:

- **`confirmed`** — primary source (Met FOI disclosure, ICO enforcement notice, court judgment, official police statement). Requires a specific `source_url` (not a generic homepage).
- **`approximate`** — location or date inferred from adjacent evidence; not directly stated in a primary source. Must have `notes` explaining what was approximated and why.
- **`unverified`** — single secondary source; cannot yet be cross-referenced. Flags for follow-up; never publish without upgrading.

Do not upgrade a record's `data_quality` without adding a primary-source `source_url`.

---

## Source hierarchy

When evaluating or adding sources, highest to lowest confidence:

1. Met Police FOI disclosure or official published deployment log
2. ICO enforcement notice or court judgment
3. Official police press release or statement
4. NGO report (Big Brother Watch, Liberty) citing specific detail
5. Journalism citing a named source
6. Journalism without named source / general claims

---

## Key invariants

- **No speculative records.** Every deployment must trace to a verifiable source.
- **No code changes without running the validator.** Run `python scripts/validate-dataset.py <file>` before modifying any deployment JSON.
- **`retrospective-fr.json` uses a different schema.** RFR incidents (post-event FR applied to footage) use `incidents[]` not `deployments[]`, and have different coordinate fields (`footage_lat/lon`, `arrest_lat/lon`). The validator handles both.
- **Three FR technology types exist** — distinguish them clearly:
  1. **LFR (Live Facial Recognition)** — real-time camera scanning against watchlist (`met-police-lfr.json`, `btp-lfr.json`)
  2. **RFR (Retrospective FR)** — FR applied to existing footage after an incident (`retrospective-fr.json`)
  3. **OIFR (Operator-Initiated FR)** — handheld on-demand matching (not yet documented in data files)
- **Private operator records (`priv-*`) all use `approximate` dating.** Facewatch go-live dates were never publicly disclosed; 2022-01-01 is inferred from press coverage of the rollout.

---

## Agent persona dispatch

Three subagent personas are defined in `agents/README.md`. Route work accordingly:

| Persona | When to invoke |
|---|---|
| **Project Development Lead** | Schema changes, backlog items, PR review, splat pipeline coordination |
| **Data Cleanup & Verification** | Adding or reviewing records, sourcing, data_quality auditing, validator output triage |
| **Marketing & Public Rollout** | Artist statements, exhibition copy, press releases, community outreach, social media |

**Current orchestration stack:** Claude Code plan mode (manual invocation). LiteLLM + Qwen3 8B / Hermes-3 8B intended for automated dispatch — not yet wired up.

---

## /data-review command

Run a combined automated + LLM review of any deployment file:

```
/data-review
```

Defined in `.claude/commands/data-review.md`. It runs the validator then applies a structured review checklist (duplicates, coordinate bounds, data_quality assignment, source quality, temporal anomalies, missing annotations, schema consistency). Output is a structured severity table.

---

## Deferred features (placeholder directories)

These are explicitly unbuilt — their directories are `.gitkeep` placeholders:

| Directory | What goes here | Current state |
|---|---|---|
| `site/` | Published website (static or SSG) | Schema planned, no code |
| `splats/` | Per-location Gaussian splat directories (`scene.splat`, `annotations.json`) | Architecture in README, no splats |
| `data/interactions/` | MOPAC stop-and-search demographic data by borough/ward | Schema not yet designed |
| `data/community/` | Community-submitted photos/videos of active deployments | Moderation workflow TBD |

Do not create files in these directories without a plan for the accompanying schema.

---

## Known issues (from May 2026 audit)

1. **`map/data/london-wards.geojson` (1.05 MB) is available but has no layer toggle yet.** Ward-level boundaries are present; the toggle is planned — see `map/README.md`.

2. **Some news archive URLs are share.google redirects.** `data/news/gmail-research-threads.json` contains entries where `url` is a Gmail share redirect rather than a canonical article URL. `url_canonical` fields are partially filled; remainder need resolving.

3. **`lfr-006` (Liverpool Street) has null `ward`.** City of London ward data needs to be populated.

4. **Outcome data sparse.** Only `lfr-008` (Croydon static) has a populated `outcome_arrests` field (173). All other deployment records have null outcomes — intentional where data isn't public.

## Archive

`_archive/` is gitignored and holds dead code preserved for reference:

- `map-london-boroughs.js` — hardcoded 23-borough GeoJSON that was once in `map/`. Superseded by the full-resolution `map/data/london-boroughs.geojson`. Do not import or restore.
