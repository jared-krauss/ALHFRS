# A London History of Facial Recognition Systems (ALHFRS)

A multi-year documentary art and data visualisation project documenting the deployment of facial recognition systems across London — by the Metropolitan Police, private operators, and other actors — and critically examining their legal basis, demographic impact, and accountability gaps.

**Primary output:** An interactive website with a London deployment map, Gaussian splat embeds of physical locations, and a community submission workflow for photos and videos of active deployments.

---

## Project structure

```
ALHFRS/
├── data/
│   ├── deployments/        FRS deployment records
│   │   ├── met-police-lfr.json         654 Met Police LFR records (2016–2026, schema v1.2)
│   │   ├── south-wales-police-lfr.json 14 South Wales Police AFR trial records (2017–2018)
│   │   ├── retrospective-fr.json       5 retrospective FR incidents
│   │   └── private-operators.json      Facewatch, retail FRS
│   ├── staging/            Extracted records pending review/merge
│   │   ├── extract-2020-2022.json      (merged ✓)
│   │   └── extract-2023-2024.json      (poor quality — do not merge)
│   ├── interactions/       Met Police stop-and-search / interaction data (TBD)
│   ├── news/               Geolocated news articles (TBD)
│   ├── legal/
│   │   └── enforcement-actions.json    Court cases, ICO notices
│   └── community/          Community submissions, pending moderation
├── map/                    Leaflet map — marker clustering + year-filter timeline strip
│   ├── index.html          Map shell
│   ├── js/                 Modular JS (config, layers, controls, legend, main)
│   └── data/               Borough and ward GeoJSON
├── splats/
│   ├── README.md           Hosting approach, field schema, map integration plan
│   └── index.json          Splat manifest (empty — no captures yet)
├── scripts/
│   ├── validate-dataset.py         Data quality validator (stdlib only)
│   └── pdf-extract-deployments.py  PDF → staging JSON via pdfplumber + Hermes3:8b
├── map-embed.html          Self-contained embeddable map (single file)
└── site/                   Website scaffold (TBD)
```

---

## Data sources

| Source | Type | URL | Status |
|--------|------|-----|--------|
| Met Police FOI disclosures | LFR deployment logs by borough (2021–2023) | [met.police.uk/foi-ai](https://www.met.police.uk/foi-ai/metropolitan-police/disclosure-2024/april-2024/locations-facial-recognition-cameras-arrests-london-boroughs-2021-2023/) | Seeded |
| Met Police LFR page | Operational safeguards, general deployment info | [met.police.uk/lfr](https://www.met.police.uk/advice/advice-and-information/facial-recognition/live-facial-recognition/) | Seeded |
| Big Brother Watch | LFR campaign, deployment tracking | [bigbrotherwatch.org.uk](https://bigbrotherwatch.org.uk/campaigns/stop-facial-recognition/) | Seeded |
| Facewatch / Sainsbury's | Private retail FRS rollout (London stores) | [facewatch.co.uk](https://www.facewatch.co.uk/) | Seeded |
| ICO enforcement notices | Regulatory actions (Clearview, Serco) | [ico.org.uk](https://ico.org.uk/about-the-ico/media-centre/) | Seeded |
| UK judiciary / Hansard | Court cases, parliamentary questions | [judiciary.uk](https://www.judiciary.uk), [hansard.parliament.uk](https://hansard.parliament.uk) | Partially seeded |
| Zoë Garbett GLA report (Feb 2026) | Accountability critique | [london.gov.uk](https://www.london.gov.uk) | Referenced |
| MOPAC stop-and-search data | Borough-level interaction demographics | TBD | Not started |
| Surveillance Camera Commissioner | Annual reports | TBD | Not started |

---

## Map layers

| # | Layer | Data file | Status |
|---|-------|-----------|--------|
| 1 | Borough boundaries | `map/data/london-boroughs.geojson` | Live |
| 2 | Met Police LFR deployments | `data/deployments/met-police-lfr.json` | Live (654 records, 2016–2026) |
| 2a | BTP LFR deployments | `data/deployments/btp-lfr.json` | 2 records — not yet wired into live map |
| 3 | Private operator deployments | `data/deployments/private-operators.json` | Wired, not toggled separately yet |
| 3a | South Wales Police AFR deployments | `data/deployments/south-wales-police-lfr.json` | 14 records (2017–2018) — not yet wired into live map |
| 4 | News & events overlay | `data/news/gmail-research-threads.json` | 21 archived articles (not yet on map) |
| 5 | Community submissions | `data/community/` | Placeholder |
| 6 | Gaussian splat embeds | `splats/` | Architecture planned |
| 7 | Stop-and-search by borough/ward | `data/interactions/` | Not started |

---

## Data schema

All deployment files share a unified schema (v1.2):

```json
{
  "schema_version": "1.2",
  "deployments": [
    {
      "id": "lfr-001",
      "operator": "Metropolitan Police",
      "operator_type": "law_enforcement",
      "deployment_type": "mobile | static",
      "location_name": "...",
      "borough": "...",
      "ward": "...",
      "lat": 51.5,
      "lon": -0.1,
      "location_cluster_id": "...",
      "date_start": "YYYY-MM-DD",
      "date_end": null,
      "stated_purpose": "...",
      "outcome_arrests": null,
      "outcome_alerts": null,
      "data_quality": "confirmed | approximate | unverified",
      "source_url": "...",
      "source_type": "FOI_disclosure | news_report | court_record | police_statement | operator_statement | ngo_report",
      "notes": null
    }
  ]
}
```

**Data quality levels:**
- `confirmed` — primary source (FOI disclosure, official police statement, court record, ICO notice)
- `approximate` — derived from adjacent evidence; location or date not exact
- `unverified` — single secondary source; needs cross-referencing before publishing

---

## Running the validator

```powershell
python scripts/validate-dataset.py data/deployments/met-police-lfr.json
python scripts/validate-dataset.py data/deployments/south-wales-police-lfr.json
python scripts/validate-dataset.py data/deployments/retrospective-fr.json
python scripts/validate-dataset.py data/deployments/private-operators.json
python scripts/validate-dataset.py data/deployments/btp-lfr.json
```

The validator handles all three schema variants: `deployments[]` (LFR/private), `actions[]` (legal), and `incidents[]` (RFR). Exit 0 = no errors; exit 1 = errors found.

---

## Pipeline architecture

```
Raw sources (Met FOI, Hansard, news, community)
    ↓
scripts/  ← collection and conversion scripts (TBD)
    ↓
data/     ← structured JSON/CSV, validated by validate-dataset.py
    ↓
map/      ← Leaflet prototype renders deployment data
    ↓
site/     ← published website (static or SSG, TBD)
    ↓
splats/   ← per-location Gaussian splat directories
             SuperSplat annotation files reference data/ records
```

---

## Gaussian splat integration (planned)

Each location in `splats/` will contain:
```
splats/
└── croydon-high-street/
    ├── scene.splat           trained splat file
    ├── annotations.json      SuperSplat data points (linked to deployment records)
    ├── deployments.json      symlink/copy of relevant data/deployments/ records
    └── news.json             relevant news articles for this location
```

When a splat is approved, a pipeline script (`scripts/splat-publish.py`, TBD) will:
1. Parse the splat's location metadata
2. Identify relevant news, deployment, and legal records
3. Write `annotations.json` with embedded data point payloads
4. Register the splat in the map layer

---

## Dev setup

Serve locally from the project root (required — `fetch()` calls block on `file://`):

```powershell
python -m http.server 8741
# or: .\serve.ps1
```

Then open: `http://localhost:8741/map-embed.html`

The map auto-starts on login via Windows Task Scheduler ("ALHFRS Map Server") — just open the URL. Must use HTTP not `file://`; `fetch()` calls for GeoJSON and data files fail under `file://`.

---

## Key legal references

| Case / Action | Date | Outcome |
|---------------|------|---------|
| R (Bridges) v Chief Constable of South Wales Police [2020] EWCA Civ 1058 | Aug 2020 | AFR use held unlawful — landmark privacy ruling |
| Liberty v Metropolitan Police Commissioner | Apr 2026 | Met LFR policy held lawful — appeal indicated |
| ICO v Clearview AI | May 2022 / Oct 2025 | Fined £7.5m; Upper Tribunal upheld ICO on appeal |
| ICO v Serco Leisure | Feb 2024 | Enforcement notice — biometric employee monitoring unlawful |

---

*Project by Jared Krauss. Data sourced from public records. All deployment records are independently verifiable — see `source_url` fields.*
