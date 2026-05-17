# scripts/

Utility scripts for data collection, validation, and processing. New scripts should land here.

---

## validate-dataset.py

Schema compliance and data quality validator for ALHFRS deployment JSON files. Run this before merging any changes to `data/deployments/`.

### Usage

```powershell
# From D:\Dev\ALHFRS\ (project root)
python scripts/validate-dataset.py data/deployments/met-police-lfr.json
python scripts/validate-dataset.py data/deployments/btp-lfr.json
python scripts/validate-dataset.py data/deployments/private-operators.json
python scripts/validate-dataset.py data/deployments/retrospective-fr.json
```

### Exit codes

| Code | Meaning |
|---|---|
| `0` | No errors (warnings may be present) |
| `1` | One or more errors found |

Warnings are printed but do not set exit code 1. Errors must be resolved before merging.

### Output format

```
ALHFRS Dataset Validator — data/deployments/met-police-lfr.json
Schema version : 1.1
Records found  : 8
Last updated   : 2026-05-14

[XX]  [lfr-006] Missing required field: ward          ← error (red)
[!!]  [lfr-007] data_quality=unverified — needs follow-up  ← warning (amber)
[OK]  All 8 records passed — no issues found          ← clean (green)
```

### What it validates

**Per-record checks:**

| Check | Severity |
|---|---|
| Required fields present (`id`, `operator`, `lat`, `lon`, `date_start`, `data_quality`, `source_url`, `source_type`) | Error |
| `data_quality` value is one of `confirmed` / `approximate` / `unverified` | Error |
| `source_type` is a known enum value | Warning |
| Coordinates within Greater London bounding box (lat 51.28–51.69, lon -0.51–0.34) | Warning |
| `confirmed` record has a specific (non-generic) `source_url` | Error |
| `approximate` record with no `source_url` and no `notes` | Warning |
| `unverified` record (any) | Warning |
| `date_start` / `date_end` in valid ISO 8601 format (YYYY-MM-DD) | Error |
| `date_end` before `date_start` | Error |
| `date_start` before 2011-01-01 (pre-dates UK FRS deployments) | Warning |

**Cross-record checks:**

| Check | Severity |
|---|---|
| Near-duplicate detection: two records within 300m AND 90 days of each other | Warning |
| Cluster consistency: two records share a `location_cluster_id` but have different `borough` values | Warning |

### Retrospective FR handling

`retrospective-fr.json` uses `incidents[]` instead of `deployments[]` and has a different coordinate model (`footage_lat/lon`, `arrest_lat/lon`). The validator auto-detects this and applies a looser required-field set (`id`, `police_force`, `outcome`, `data_quality`, `source_url`, `source_type`). Coordinate bounds checks use `footage_lat/lon` with fallback to `arrest_lat/lon`.

### Dependencies

**None beyond Python stdlib.** No `pip install` required.

Uses: `json`, `math`, `datetime`, `sys`, `io`

### ANSI color on Windows

The script enables ANSI escape codes via `ctypes.windll.kernel32.SetConsoleMode` before printing. This works in Windows Terminal and PowerShell 7+. If color codes appear as raw characters in an older terminal, they don't affect functionality.

---

## Planned scripts

Scripts to be added here as the project develops:

| Script | Purpose |
|---|---|
| `splat-publish.py` | Parse splat location metadata, identify relevant records, write `annotations.json` |
| `news-canonicalize.py` | Resolve `share.google` redirects in the news archive to permanent article URLs |
| `interactions-fetch.py` | Download and normalise MOPAC stop-and-search data for `data/interactions/` |
