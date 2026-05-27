# ALHFRS Project Audit — 2026-05-18

> Read-only audit of D:\Dev\ALHFRS\ and D:\Dev\jaredkrauss-art\ (ALHFRS content only). No files modified.

---

## 1 — Canonical File Tree

### D:\Dev\ALHFRS\ (main repo)

The repo has **4 live git worktrees** (claude/musing-maxwell, naughty-mccarthy, nice-dijkstra, suspicious-brown) in `.claude/worktrees/`. These are stale Claude Code agent branches — the canonical files are in the root. All analysis below refers to root-branch files only.

```
ALHFRS/
├── CLAUDE.md                         AI session context (comprehensive, up to date)
├── README.md                         Human-readable overview + schema + pipeline diagram
├── .gitignore
├── map-embed.html                    Self-contained embeddable single-file map
│
├── agents/
│   └── README.md                     3 agent persona definitions (Dev Lead / Data / Marketing)
│
├── data/
│   ├── README.md                     Full 19-field schema reference + known gap list
│   ├── deployments/
│   │   ├── met-police-lfr.json       8 records, schema v1.1 — 7.9 KB (last updated 2026-05-14)
│   │   ├── btp-lfr.json              2 records, schema v1.1 — 2.2 KB (last updated 2026-05-15)
│   │   ├── private-operators.json    5 records, schema v1.1 — 5.2 KB (last updated 2026-05-14)
│   │   └── retrospective-fr.json     4 incidents, schema v1.0 — 8.5 KB (last updated 2026-05-15)
│   ├── legal/
│   │   └── enforcement-actions.json  4 actions, schema v1.0 — 4.8 KB (last updated 2026-05-14)
│   ├── news/
│   │   └── gmail-research-threads.json  21 articles — 17 KB (last updated 2026-05-17)
│   ├── interactions/                 PLACEHOLDER (.gitkeep only)
│   └── community/                    PLACEHOLDER (.gitkeep only)
│
├── map/
│   ├── README.md                     Architecture, ward layer plan, GeoJSON notes
│   ├── index.html                    Leaflet map shell
│   ├── js/
│   │   ├── config.js                 Constants: tile URL, colors, data paths
│   │   ├── main.js                   Async init, data fetching, layer wiring
│   │   ├── borough-layer.js          GeoJSON borough layer
│   │   ├── deployment-layer.js       Circle markers + popups
│   │   ├── layer-controls.js         Panel toggle buttons
│   │   └── legend.js                 Bottom-left quality legend
│   └── data/
│       ├── london-boroughs.geojson   244 KB — 32 borough polygons (live, in use)
│       └── london-wards.geojson      1.05 MB — ward-level polygons (present, NOT wired yet)
│
├── scripts/
│   ├── README.md                     Validator documentation
│   └── validate-dataset.py           Schema + data quality validator (stdlib only)
│
├── site/                             PLACEHOLDER (.gitkeep)
├── splats/                           PLACEHOLDER (.gitkeep) — splat files live in jaredkrauss-art
│
└── .claude/
    ├── commands/
    │   └── data-review.md            /data-review slash command (runs validator + LLM review)
    └── launch.json
```

**_archive/** (gitignored): `map-london-boroughs.js` — dead code, superseded by full-resolution GeoJSON.

---

### D:\Dev\jaredkrauss-art\ (ALHFRS content only)

```
Content & Assets/Featured Projects/
└── A London History of Facial Recognition Systems (ALHFRS)/
    ├── README.md                     Project status card + GitHub URL + website embed code
    │
    ├── Assets/
    │   ├── Splats/
    │   │   └── Walworth 2024/
    │   │       ├── T18-30-1-Spatial-Vocab-New-Masks_8000iters.ply     110 MB  ⚠ large
    │   │       ├── T19-3-26-Exhaustive-Masks_4500iters_3000.ply        41 MB
    │   │       ├── T19-3-26-Exhaustive-Masks_4500iters_3000-cameras.json   5.4 KB
    │   │       ├── T19-x-1-Vocab-New-Masks_7000iters_2000.ply          37 MB
    │   │       └── T19-x-1-Vocab-New-Masks_7000iterscameras.json       5.4 KB
    │   │
    │   └── Research Material/
    │       ├── Deployment Data/
    │       │   ├── Copy of Live Facial Recognition Deployments.xlsx    229 KB  ← DATA ASSET
    │       │   ├── LFR-Numbers-with-arrests(1).ods                      49 KB  ← DATA ASSET
    │       │   ├── lfr-deployment-grid-2020-2022.pdf                   176 KB
    │       │   ├── lfr-deployment-grid-2023-to-2024.pdf                960 KB
    │       │   └── lfr-deployment-grid-2025-up-to-May20-.pdf           679 KB  ← newest grid
    │       │
    │       ├── FaceWatch - Gordons Wine Bar/
    │       │   └── Public expects facial recognition...Facewatch.pdf   189 KB
    │       │
    │       ├── Misc/
    │       │   ├── Intimate alienation -reduced.pdf                     1.9 MB  (photo essay ref?)
    │       │   └── Inbox to Process/                                    ← UNPROCESSED INBOX
    │       │       ├── Data Extraction on Facial Recognition...csv      18 KB  ← DATA ASSET
    │       │       └── The unchecked expansion...Zoë Garbet.pdf         1.4 MB
    │       │
    │       ├── NEC & Met Files/
    │       │   ├── NEC & Met FIles-20260513T162144Z-3-001.zip          110 MB  ⚠ NEEDS SESSION
    │       │   ├── NEC-FR_white-paper-It'sAllAboutTheFace.pdf            1.4 MB
    │       │   ├── LFR-Numbers-with-arrests BBW (Aug 2024).ods          49 KB  ← DATA ASSET
    │       │   ├── live-facial-recognition-deployment-record-2025.pdf    49 KB  ← PRIMARY SOURCE
    │       │   ├── live-facial-recognition-deployment-record-2026.pdf  (size not checked)
    │       │   ├── lfr-deployment-grid-2020-2022.pdf                   (duplicate of above)
    │       │   ├── lfr-deployment-grid-2023-to-2024.pdf                (duplicate)
    │       │   ├── lfr-policy-document2.pdf
    │       │   ├── mps-lfr-1-v.3.0-web.pdf                            (Met LFR policy v3)
    │       │   └── 20× Screen Shot 2019-07-19 .png                     (early deployment screenshots)
    │       │
    │       └── Official Governmet Documents/               [sic]
    │           ├── FRS_Consultation_FINAL-2026-new-legal-framework.pdf  ← IMPORTANT
    │           ├── ICO-guidance-on-video-surveillance-including-cctv.pdf
    │           ├── London-Met-Police-Trial-of-Facial-Recognition-Tech-Report-2.pdf
    │           ├── facial_recognition_delivering_more_precise_policing...met.pdf
    │           ├── frt-equitability-study_mar2023.pdf                   ← BIAS DATA
    │           ├── mayorsquestions-2016-boris-comissioner.pdf           ← HISTORICAL
    │           ├── npia--capture-and-interchange-standard... (×2 duplicate)
    │           └── scc_self_assessment_tool-23-web.pdf
```

---

## 2 — Deployment Data Inventory

**Total records:** 15 deployment records + 4 RFR incidents + 4 legal actions + 21 news articles.

### Met Police LFR — `met-police-lfr.json` (8 records)

| ID | Location | Borough | Date | Type | Quality | Outcomes |
|----|----------|---------|------|------|---------|----------|
| lfr-001 | Romford Market | Havering | 2020-02-11 | mobile | confirmed (FOI) | null |
| lfr-002 | Oxford Street (Bond St) | Westminster | 2020-02-27 | mobile | confirmed (news) | null |
| lfr-003 | Stratford / Westfield | Newham | 2020-06-15 | mobile | confirmed (FOI) | null |
| lfr-004 | Croydon Town Centre | Croydon | 2022-05-24 | mobile | confirmed (FOI) | null |
| lfr-005 | Westfield Stratford City | Newham | 2023-09-07 | mobile | confirmed (FOI) | null |
| lfr-006 | Liverpool Street area | City of London | 2024-02-07 | mobile | approximate (news) | null |
| lfr-007 | Wembley Stadium (NFL) | Brent | 2024-11-20 | mobile | approximate (police stmt) | null |
| lfr-008 | Croydon High St (static) | Croydon | 2025-10-01– | static | confirmed (police stmt) | **173 arrests** |

Coordinate range: lat 51.37–51.58, lon -0.28–0.18. All within Greater London bounds. Two clusters defined: `stratford-complex` (lfr-003/005), `croydon-centre` (lfr-004/008).

### BTP LFR — `btp-lfr.json` (2 records)

| ID | Location | Borough | Date | Quality |
|----|----------|---------|------|---------|
| btp-001 | London Bridge station | Southwark | 2026-02-11– | confirmed (BBC) |
| btp-002 | London Waterloo station | Lambeth | 2026-02-14– | confirmed (BBC) |

Both ongoing (six-month trial). No outcome data yet — trial too recent.

### Private Operators — `private-operators.json` (5 records)

| ID | Location | Borough | Date | Quality |
|----|----------|---------|------|---------|
| priv-001 | Sainsbury's Dalston | Hackney | ~2022-01-01 | approximate |
| priv-002 | Sainsbury's Elephant & Castle | Southwark | ~2022-01-01 | approximate |
| priv-003 | Sainsbury's Ladbroke Grove | K&C | ~2022-01-01 | approximate |
| priv-004 | Sainsbury's Camden | Camden | ~2022-01-01 | approximate |
| priv-005 | Sainsbury's Whitechapel | Tower Hamlets | ~2022-01-01 | approximate |

All operator: Facewatch / Sainsbury's. All `approximate` — go-live dates inferred from press coverage; never officially disclosed. Extra field `claimed_reduction` present (not in standard v1.1 schema — allowed for retail).

### Retrospective FR — `retrospective-fr.json` (4 incidents, schema v1.0)

| ID | Subject | Force | Date | Outcome | Quality |
|----|---------|-------|------|---------|---------|
| rfr-001 | Colin McMahon | Met | ~2026-04 | false positive | confirmed |
| rfr-002 | Alvi Choudhury | Thames Valley | 2026-01-08 | false positive | confirmed |
| rfr-003 | Anonymous | South Wales | ~2024-11 | false positive | approximate |
| rfr-004 | (mass, riots) | Met + others | 2024-08 | unknown | confirmed |

Note: rfr-002 and rfr-003 are not London/Met — included for comparative context on racial bias. `rfr-004` is a collective record; individual cases not yet documented.

### Legal / Regulatory — `enforcement-actions.json` (4 actions)

| ID | Case | Date | Outcome |
|----|------|------|---------|
| legal-001 | Bridges v South Wales Police | 2020-08-11 | Appeal allowed — AFR unlawful |
| legal-002 | Liberty v Met Commissioner | 2026-04-21 | Challenge dismissed (appeal pending) |
| legal-003 | ICO v Clearview AI | 2022-05-23 | £7.5m fine; CoA appeal Dec 2025 |
| legal-004 | ICO v Serco Leisure | 2024-02-01 | Stop processing + delete all biometric data |

### News archive — `gmail-research-threads.json` (21 articles)

Coverage: 2024-08 to 2026-05. Mix of canonical URLs and unresolved share.google redirects. Several articles tagged and cross-referenced to deployment records. Some have lat/lon; most don't.

---

## 3 — Schema / Format Reference (preserve exactly)

### Deployment v1.1 (met-police-lfr, btp-lfr, private-operators)

```json
{
  "schema_version": "1.1",
  "source": "...",
  "last_updated": "YYYY-MM-DD",
  "notes": "...",
  "deployments": [
    {
      "id": "lfr-001",              // string, unique across all files
      "operator": "...",
      "operator_type": "law_enforcement | retail | transport",
      "deployment_type": "mobile | static",
      "location_name": "...",
      "borough": "...",
      "ward": "... | null",
      "lat": 51.5,                  // float, 51.28–51.69
      "lon": -0.1,                  // float, -0.51–0.34
      "location_cluster_id": "... | null",
      "date_start": "YYYY-MM-DD",
      "date_end": "YYYY-MM-DD | null",
      "stated_purpose": "...",
      "outcome_arrests": null,      // integer or null
      "outcome_alerts": null,       // integer or null
      "data_quality": "confirmed | approximate | unverified",
      "source_url": "...",
      "source_type": "FOI_disclosure | news_report | court_record | police_statement | operator_statement | ngo_report",
      "notes": "... | null"
    }
  ]
}
```

Private operators add one extra non-standard field: `"claimed_reduction": "..."`.

### Retrospective FR v1.0 (retrospective-fr.json)

Uses `incidents[]` not `deployments[]`. Key field differences:
- `police_force` (not `operator`)
- `footage_lat/lon` + `arrest_lat/lon` (separate coordinate pairs)
- `arrest_date_approx` (partial dates like `"2026-04"` are valid)
- `outcome`: `false_positive | conviction | unknown`
- `custody_duration_hours`: integer
- `legal_outcome`: string
- No `deployment_type`, `operator_type`, `location_cluster_id`

Top-level also has `context{}` block with aggregate stats and OIFR note.

### Legal v1.0 (enforcement-actions.json)

Uses `actions[]`. Court cases have: `case_name`, `citation`, `claimant`, `respondent`, `court`, `date`, `outcome`, `key_findings[]`, `significance`, `source_url`. ICO enforcement has: `actor`, `enforcement_body`, `action_type`, `appeal_status`.

### News v1.0 (gmail-research-threads.json)

Uses `articles[]`. Fields: `id`, `date`, `title`, `publication`, `url`, `url_canonical`, `location_name`, `borough`, `lat`, `lon`, `tags[]`, `notes`.

---

## 4 — Gaps and Issues

### 🔴 Data gaps requiring research

**GAP: Deployment records missing for documented events in the CSV inbox**

The `Data Extraction...csv` (18 KB, "Inbox to Process") contains ~33 historical events not yet migrated into structured JSON. High-priority missing records:

| Event | CSV Date | Likely file |
|-------|----------|-------------|
| First LFR deployment in London | 2016 | met-police-lfr.json — need FOI source |
| Notting Hill Carnival | 2017 | met-police-lfr.json — 95 false positives documented |
| Jan 2019 test deployment (£90 fine incident) | Jan 2019 | met-police-lfr.json |
| King Charles Coronation deployment | May 2023 | met-police-lfr.json — Home Office blog cited |
| North London Derby (Arsenal v Spurs) | Sep 2023 | met-police-lfr.json — 3 arrests documented |
| Soho weekend deployments (×2) | Aug 2023 | met-police-lfr.json — Home Office blog cited |
| Bethnal Green deployment (BBC documented) | May 2024 | met-police-lfr.json — 6 arrests |
| Hounslow deployment | May 2024 | met-police-lfr.json — 6 arrests |
| Jan–Jun 2024 aggregate (79 deployments, 231 arrests) | 2024 | context block or separate aggregate record |

**GAP: Private operators beyond Sainsbury's**

CSV documents Facewatch in Budgens, Sports Direct, Costcutter, and Home Bargains (UK-wide). No London-specific location records for these yet. The "Sara misidentification" at Home Bargains (May 2024) is documented in CSV — no `priv-*` record exists.

**GAP: Gordon's Wine Bar (Facewatch)**

A dedicated research folder exists (`FaceWatch - Gordons Wine Bar/`) with a PDF. No corresponding `priv-*` record in `private-operators.json`. This appears to be a known Facewatch private deployment (London, Embankment area).

**GAP: OIFR (Operator-Initiated FR)**

Three references in the data note the Met's Feb 2026 OIFR trial (handheld devices, ~100 units, £763k, NEC Neoface). No data file exists yet. `data/README.md` notes it explicitly as undocumented.

**GAP: lfr-006 ward is null**

Liverpool Street falls in the City of London — its ward-level geography is unusual (City has its own ward system). Known issue flagged in CLAUDE.md.

**GAP: lfr-002 data_quality may be too high**

`lfr-002` (Oxford St) is marked `confirmed` but `source_type` is `news_report` (Big Brother Watch). Per the schema, `confirmed` requires a primary source. The data review command's checklist would flag this. *(Low urgency — not my call to change, flagging for awareness.)*

**GAP: lfr-004 and lfr-005 outcome_arrests potentially retrievable**

Both reference the Met FOI URL that explicitly covers "arrests, 2021–2023". The `data/README.md` already flags this as a research task. Fetch `https://www.met.police.uk/foi-ai/metropolitan-police/disclosure-2024/april-2024/locations-facial-recognition-cameras-arrests-london-boroughs-2021-2023/` to check.

**GAP: Ethnic breakdown data not yet in any file**

The CSV notes the Met promised to publish ethnic breakdown data of scans (promised early 2025). No such data appears in any current file. If published, would belong in `data/interactions/` or as a field addition.

**GAP: `live-facial-recognition-deployment-record-2025.pdf` and `...-2026.pdf` not processed**

These appear to be official Met deployment logs — exactly the kind of primary source needed to populate or confirm existing records and fill in dates/outcomes. They are in jaredkrauss-art/NEC & Met Files/ but nothing has been ingested from them into the JSON yet. **These are the single highest-value unread documents in the research pile.**

---

### 🟡 Known issues (already documented in CLAUDE.md / data/README.md)

| Issue | Where noted | Status |
|-------|-------------|--------|
| Ward layer toggle not wired | map/README.md | Implementation plan written, not built |
| Some news URLs are share.google redirects | CLAUDE.md §Known issues | Partially resolved (`url_canonical` present for some) |
| `lfr-006` null ward | CLAUDE.md | Open |
| Outcome data mostly null | data/README.md | Intentional except research gap on lfr-004/005 |
| Liberty v Met appeal outcome pending | enforcement-actions.json | As of 2026-05-14 |
| Clearview CoA appeal pending | enforcement-actions.json | As of 2026-05 |

---

### 🔵 Items requiring a dedicated session (don't open casually)

| File | Size | What it probably is | Why it needs its own session |
|------|------|---------------------|------------------------------|
| `NEC & Met Files-20260513T162144Z-3-001.zip` | 110 MB | Google Drive export of NEC/Met research materials | Unknown contents; likely contains duplicate PDFs + potentially new sources; needs systematic extraction and triage |
| `T18-30-1-Spatial-Vocab-New-Masks_8000iters.ply` | 110 MB | Gaussian splat (Walworth 2024, highest-quality variant) | Large binary; needs SuperSplat or viewer to assess quality; integration into `splats/` pipeline requires COLMAP pipeline review |
| `T19-3-26-Exhaustive-Masks_4500iters_3000.ply` | 41 MB | Gaussian splat (Walworth 2024, exhaustive-mask variant) | Same |
| `T19-x-1-Vocab-New-Masks_7000iters_2000.ply` | 37 MB | Gaussian splat (Walworth 2024, third variant) | Same |
| `london-wards.geojson` | 1.05 MB | Ward boundary polygons | Already present and valid; integration into map is a planned 4-file change (described in map/README.md) — not complex, just needs focused execution |

---

## 5 — Architecture State Summary

| Component | State |
|-----------|-------|
| Data layer (JSON) | Live, 15 deployment records + supporting data |
| Leaflet map (local dev) | Live — `python -m http.server 8000` + `http://localhost:8000/map/index.html` |
| map-embed.html | Live — markers work file://, borough outlines need HTTP |
| GitHub repo | Exists (`jared-krauss/ALHFRS`), GitHub Pages URL in jaredkrauss-art README |
| Ward layer toggle | Planned — spec written in map/README.md, 4 files to change |
| Splat integration | Walworth 2024 .ply files exist in jaredkrauss-art; `splats/` dir in ALHFRS is empty placeholder |
| Site | Placeholder only (`site/.gitkeep`) |
| Community submission workflow | Placeholder only |
| Demographic/stop-search data | Not started |
| OIFR data file | Not started |
| Smolagents/LiteLLM orchestration | Deferred — LiteLLM installed but not running |

---

## 6 — Recommended Next Actions (prioritised)

1. **Process `live-facial-recognition-deployment-record-2025.pdf` and `...-2026.pdf`** — these are official Met deployment logs and are the most direct path to confirming/extending existing records and filling outcome nulls. Read them; cross-reference against current JSON.

2. **Migrate the CSV inbox** (`Data Extraction...csv`) — 33 historical events, several clearly map to missing deployment records (2017 Notting Hill Carnival, 2023 Arsenal/Coronation/Soho, May 2024 Bethnal Green/Hounslow). Run `/data-review` on any new records before committing.

3. **Wire the ward layer toggle** — the spec is complete in `map/README.md`. Four-file change. Low risk.

4. **Resolve `share.google` redirect URLs** in `gmail-research-threads.json` — batch fetch `url_canonical` for the remaining unresolved ones.

5. **Create a Gordon's Wine Bar record** in `private-operators.json` — source PDF already in research material.

6. **Triage the 110 MB zip** in a dedicated session — extract, scan for novel sources.
