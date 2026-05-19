# Extraction Notes — 2025 & 2026 LFR Deployment Records

**Extracted:** 2026-05-19  
**Extractor:** Claude (Cowork session)  
**Source extraction file:** `data/extraction-2026-05-18.md`  
**Target file:** `data/deployments/met-police-lfr.json`  
**Records appended:** lfr-032 → lfr-357 (326 new records)

---

## Source PDFs

| File | URL | Records |
|---|---|---|
| `live-facial-recognition-deployment-record-2025.pdf` | https://www.met.police.uk/SysSiteAssets/media/downloads/met/advice/facial-recognition/live-facial-recognition-deployment-record-2025.pdf | 231 (Jan–Dec 2025) |
| `live-facial-recognition-deployment-record-2026.pdf` | https://www.met.police.uk/SysSiteAssets/media/downloads/met/advice/facial-recognition/live-facial-recognition-deployment-record-2026.pdf | 95 (Jan–17 Apr 2026) |

PDFs were pre-parsed into markdown tables in `data/extraction-2026-05-18.md`. The extraction script (`outputs/generate_lfr_records.py`) read those tables; no direct PDF parsing was performed in this session.

---

## Threshold Applied

All 2025 and 2026 records use `threshold: 0.64`. Per the project's threshold rules:

| Date range | Threshold |
|---|---|
| Before 11 Jul 2024 | 0.60 |
| 11–24 Jul 2024 | 0.62 |
| 25 Jul 2024 onward | **0.64** |

---

## Schema and Data Quality

- `data_quality: "confirmed"` — records are drawn from official MPS deployment logs (primary source)
- `source_type: "police_statement"` — operational deployment records published by MPS
- `operator_type: "law_enforcement"`, `vendor: "NEC"`, `deployment_type: "mobile"` applied uniformly
- All dates in range: 2025-01-08 to 2026-04-17

---

## Skipped Records

| ID placeholder | Date | Location | Reason |
|---|---|---|---|
| (would have been lfr-258) | 2025-12-18 | North End, Croydon | `outcome_faces_scanned = 4` — partial/metadata row; threshold < 10 faces triggers skip |

The valid record for the same date and location (faces = 6,282) was retained as lfr-258.

---

## Coordinate Resolution

Coordinates were resolved from a lookup table keyed by `(normalised_location, normalised_borough)` built into the extraction script. No coordinates are provided in the source PDFs.

**36 records initially fell back to London centroid (51.5074, -0.1278).** These were patched by `outputs/patch_coords.py` immediately after initial extraction. All 36 were resolved; zero centroid records remain in the final dataset.

### Coord misses resolved

| IDs | Location (raw) | Borough | Coordinates assigned |
|---|---|---|---|
| lfr-040 | Town Sq, Walthamstow | Waltham Forest | 51.5835, -0.0196 (Walthamstow Town Square) |
| lfr-051, 059, 104, 108, 263, 332 | High St / High Street, Ilford | Redbridge | 51.5588, 0.0740 (Ilford High Street) |
| lfr-052 | High St, Sutton | Sutton | 51.3594, -0.1891 (Sutton High Street) |
| lfr-057, 132, 163, 228 | Clarence St, Kingston | Kingston | 51.4117, -0.3004 (Clarence Street, Kingston) |
| lfr-058 | Westfield, Shepherds Bush | H&F | 51.5077, -0.2248 (Westfield London, White City) |
| lfr-239 | Westfield, White City | H&F | 51.5077, -0.2248 (same) |
| lfr-067, 236, 352 | High St / High Street, Hounslow | Hounslow | 51.4672, -0.3655 (Hounslow High Street) |
| lfr-074, 084, 162, 297 | Stratford Westfield / Stratford, Westfields / Westfields, Stratford | Newham | 51.5429, -0.0021 (Westfield Stratford City) |
| lfr-080 | High St, Bromley | Bromley | 51.4037, 0.0147 (Bromley High Street) |
| lfr-081 | High St, Camden | Camden | 51.5392, -0.1425 (Camden High Street) |
| lfr-103 | Station Lane, Hornchurch | Havering | 51.5567, 0.2155 (Station Lane) |
| lfr-107, 265 | High St, Harlesden | Brent | 51.5360, -0.2564 (Harlesden High Street) |
| lfr-116 | High St, Bexleyheath | Bexley | 51.4596, 0.1396 (Bexleyheath High Street) |
| lfr-131 | Station Rd, Hayes | Hillingdon | 51.5063, -0.4194 (Station Road, Hayes) |
| lfr-144, 183 | High St, Lewisham | Lewisham | 51.4553, -0.0140 (Lewisham High Street) |
| lfr-149 | Praed St, Paddington | Westminster | 51.5168, -0.1769 (Praed Street, Paddington) |
| lfr-218 | London Rd, Morden | Merton | 51.4016, -0.1959 (London Road, Morden) |
| lfr-264 | St Ann's, Harrow | Harrow | 51.5806, -0.3337 (St Ann's Road, Harrow) |
| lfr-273 | High Road, Kilburn | Brent | 51.5457, -0.1986 (Kilburn High Road) |
| lfr-284 | High Street, Acton | Ealing | 51.5030, -0.2683 (Acton High Street) |
| lfr-325 | Broadway, Bexley | Bexley | 51.4596, 0.1396 (Bexleyheath Broadway) |

**Root cause:** The lookup key was the comma-stripped location name (e.g. "High St, Ilford" → "high st"), but the COORDS dict stored the full form ("high st ilford"). The prefix-shortening fallback doesn't cross comma boundaries. Patched via `patch_coords.py`; the COORDS dict in the generation script should be updated if re-run.

---

## Notable Records

### Notting Hill Carnival 2025 — lfr-167, lfr-168

| ID | Date | Location | Borough |
|---|---|---|---|
| lfr-167 | 2025-08-24 | Kilburn Lane / Brent | Brent |
| lfr-168 | 2025-08-25 | Kilburn Lane / Brent | Brent |

Two-day carnival deployment. `stated_purpose: "Crowd safety, wanted persons, major sporting/public event"`. Assigned `location_cluster_id: "notting-hill-carnival"` (already established in the COORDS dict). Note: the carnival straddles the Brent/Kensington and Chelsea boundary — the validator flags this as a cross-borough cluster, which is intentional and documented in the source.

### Arsenal Match — lfr-225

| ID | Date | Location | Borough |
|---|---|---|---|
| lfr-225 | 2025-11-23 | Arsenal, Highbury | Islington |

Event PSO deployment for an Arsenal home fixture. Consistent with lfr-031 from 2023.

### T2 Heathrow Airport — lfr-230

| ID | Date | Location | Borough |
|---|---|---|---|
| lfr-230 | 2025-11-27 | T2 Heathrow Airport, Hillingdon | Hillingdon |

**First airport deployment in the dataset.** `use_case: "CNI PSO"` (Critical National Infrastructure). `stated_purpose: "Critical national infrastructure protection"`. Coordinates: 51.4717, -0.4540 (Terminal 2).

### Tottenham Hotspur Match — lfr-280

| ID | Date | Location | Borough |
|---|---|---|---|
| lfr-280 | 2026-02-22 | Love Lane / High Rd, Haringey | Haringey |

Event PSO for a Spurs home fixture at Tottenham Hotspur Stadium. Consistent with the established `love-lane` entry in COORDS for Haringey.

---

## Validator Output Summary

Run: `python3 scripts/validate-dataset.py data/deployments/met-police-lfr.json`

```
357 of 357 records clean
470 warning(s) found
```

All 470 warnings are non-blocking:

- **Near-duplicate location warnings** (~468): the validator flags records within 200m and 90 days of each other without a shared `location_cluster_id`. Expected behaviour for a dataset of repeat hotspot deployments — the Met Police revisits the same high streets many times per year. The 2025/2026 records do not have `location_cluster_id` values assigned (only the earlier cohort does); this is a known gap for future enrichment.

- **Cross-borough cluster warning** (2 records): `lfr-167` and `lfr-168` in the `notting-hill-carnival` cluster span Brent and Kensington and Chelsea. Intentional — the carnival route crosses the boundary.

**No errors.**

---

## Known Gaps / Future Work

| Gap | Notes |
|---|---|
| `location_cluster_id` not set for 2025/2026 records | Only the 2023–2024 cohort has cluster IDs. Requires a separate clustering pass over the new records. |
| `ward` null for some records | Where lookup found a borough-level match but no ward-level data (e.g. Acton, Harlesden). |
| `outcome_false_alerts` heuristic | Where the source shows a non-zero FA rate but no explicit "N false alerts confirmed" text, the extractor defaults to 1. This may undercount where multiple false alerts occurred but were not individually noted. |
| 2026 dataset is partial | Covers only through 17 April 2026. The MPS typically publishes updated records quarterly; a refresh pull is recommended after Q2 2026. |
| Coordinate precision | All coordinates are landmark-level (centre of named street/building) rather than exact camera positions, which are not disclosed in the source documents. `data_quality: "confirmed"` applies to the operational record, not the coordinate. |
