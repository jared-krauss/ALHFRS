# data/

Structured JSON records for all ALHFRS deployment, legal, and news data. The map and any future site build read directly from these files — they are the canonical source of truth for the project.

---

## Directory layout

```
data/
├── deployments/
│   ├── met-police-lfr.json         Met Police Live Facial Recognition (schema v1.1)
│   ├── btp-lfr.json                British Transport Police LFR trials (schema v1.1)
│   ├── private-operators.json      Facewatch/Sainsbury's retail FRS (schema v1.1)
│   └── retrospective-fr.json       Retrospective FR false-positive incidents (schema v1.0)
├── legal/
│   └── enforcement-actions.json    Court cases and ICO regulatory actions (schema v1.0)
├── news/
│   └── gmail-research-threads.json Research article archive from Gmail (schema v1.0)
├── interactions/                   MOPAC stop-and-search data (placeholder — TBD)
└── community/                      Community submissions (placeholder — TBD)
```

---

## Deployment schema v1.1

All files in `deployments/` (except `retrospective-fr.json`) use this schema. The top-level JSON object has metadata fields (`schema_version`, `source`, `last_updated`, `notes`) and a `deployments` array.

### Field reference

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | yes | string | Unique across all deployment files (e.g. `lfr-001`, `btp-002`, `priv-003`) |
| `operator` | yes | string | Full operator name |
| `operator_type` | yes | enum | `law_enforcement` / `retail` / `transport` |
| `deployment_type` | yes | enum | `mobile` / `static` |
| `location_name` | no | string | Human-readable location description |
| `borough` | no | string | London borough name |
| `ward` | no | string | London ward name (null if unknown — see lfr-006) |
| `lat` | yes | float | Latitude — must be 51.28–51.69 |
| `lon` | yes | float | Longitude — must be -0.51–0.34 |
| `location_cluster_id` | no | string | Groups records at same physical location (see below) |
| `date_start` | yes | ISO 8601 | YYYY-MM-DD format |
| `date_end` | no | ISO 8601 | null = ongoing or permanent |
| `stated_purpose` | no | string | Deployment purpose per operator |
| `outcome_arrests` | no | integer | Arrest count (populated for lfr-008 only) |
| `outcome_alerts` | no | integer | Alert count (unused; null for all current records) |
| `data_quality` | yes | enum | `confirmed` / `approximate` / `unverified` |
| `source_url` | yes | string | Specific document URL — must not be a generic homepage |
| `source_type` | yes | enum | `FOI_disclosure` / `news_report` / `court_record` / `police_statement` / `operator_statement` / `ngo_report` |
| `notes` | no | string | Free-text annotation for context, caveats, cross-references |

---

## Retrospective FR schema v1.0

`retrospective-fr.json` uses a distinct schema — RFR is a different technology (FR applied to existing footage after an incident, not real-time scanning). Its records are in an `incidents` array, not `deployments`.

Key differences from v1.1:
- `police_force` instead of `operator`
- Separate footage coordinates (`footage_lat/lon`) and arrest coordinates (`arrest_lat/lon`)
- `arrest_date_approx` instead of `date_start` (partial dates like `2026-04` are valid)
- `outcome` field (e.g. `false_positive`, `conviction`)
- No `deployment_type`, `operator_type`, or `location_cluster_id`

The validator (`scripts/validate-dataset.py`) auto-detects RFR files by the presence of `incidents` and applies a looser required-field set.

---

## Data quality levels

The `data_quality` field is the core accuracy signal. Treat it as a contract:

| Value | Meaning | Requirements |
|---|---|---|
| `confirmed` | Primary source directly states location, date, and operator | Must have a specific `source_url` — not a generic homepage like `met.police.uk/` |
| `approximate` | Location or date inferred from adjacent evidence, not directly stated | Must have `notes` explaining what was approximated and why |
| `unverified` | Single secondary source; not yet cross-referenced | Flags automatically in the validator; must be resolved before publishing |

**Do not upgrade a record's `data_quality` without supplying a primary-source `source_url`.**

---

## Source hierarchy

When choosing between competing sources, highest to lowest confidence:

1. Met Police FOI disclosure or official published deployment log
2. ICO enforcement notice or court judgment
3. Official police press release or statement
4. NGO report (Big Brother Watch, Liberty) with specific detail
5. Journalism citing a named source
6. Journalism without a named source

---

## location_cluster_id

Groups records that relate to the same physical location (e.g. repeated deployments at the same site over time). Current clusters:

| Cluster ID | Records | Location |
|---|---|---|
| `stratford-complex` | `lfr-003` (2020), `lfr-005` (2023) | Westfield Stratford City / Stratford Shopping Centre |
| `croydon-centre` | `lfr-004` (2022 mobile), `lfr-008` (2025 static) | Croydon High Street zone |

Records at the same physical location but different `location_cluster_id` values — or different boroughs within the same cluster — will trigger a validator warning.

---

## Three FR technology types

The project distinguishes three types of police FR that appear across the data files:

| Type | Description | Data files |
|---|---|---|
| **LFR** — Live Facial Recognition | Real-time camera scanning against a watchlist | `met-police-lfr.json`, `btp-lfr.json` |
| **RFR** — Retrospective FR | FR applied to existing footage or images after an incident | `retrospective-fr.json` |
| **OIFR** — Operator-Initiated FR | Handheld device, on-demand face capture and matching | Not yet in data files |

Do not mix LFR and RFR records into the same deployment file — their schemas and legal frameworks differ.

---

## Placeholder directories

| Directory | What will go here |
|---|---|
| `interactions/` | MOPAC stop-and-search data by borough and ward — demographic impact context; schema not yet designed |
| `community/` | Community-submitted photos and videos of active deployments; moderation workflow TBD |

Do not add data files to these directories until the schemas are designed.

---

## Running the validator

```powershell
# Validate a single file
python scripts/validate-dataset.py data/deployments/met-police-lfr.json

# Validate all files sequentially (PowerShell)
Get-ChildItem data\deployments\*.json | ForEach-Object {
    python scripts/validate-dataset.py $_.FullName
}
```

Exit code 0 = no errors. Exit code 1 = one or more errors found. Warnings are printed but do not affect exit code.

See `scripts/README.md` for full validator documentation.

---

## Known data gaps and issues

- **Private operator dates approximate.** `priv-001` through `priv-005` all use `2022-01-01` — the actual Facewatch go-live dates in each Sainsbury's store were never publicly disclosed. Do not change to `confirmed` without a primary source.
- **`lfr-006` has null `ward`.** Liverpool Street falls in the City of London; ward data needs to be populated.
- **Outcome fields mostly null.** Only `lfr-008` has `outcome_arrests` populated (173). Other operators do not publish outcome data.
- **Some news archive URLs are share.google redirects.** `gmail-research-threads.json` has entries where `url` is a Gmail share redirect. `url_canonical` is partially filled — remaining redirects need resolving to permanent article URLs.
