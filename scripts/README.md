# scripts/

Utility scripts for data quality, validation, and maintenance. All scripts run from the project root (`D:\Dev\ALHFRS\`).

---

## validate-dataset.py

Schema compliance and data quality checker. Run this before committing any changes to deployment JSON files.

### Usage

```powershell
# Validate a single file
python scripts/validate-dataset.py data/deployments/met-police-lfr.json

# Validate all files in a directory
python scripts/validate-dataset.py data/deployments/

# Validate legal actions
python scripts/validate-dataset.py data/legal/enforcement-actions.json
```

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | No errors (warnings may still be present) |
| `1` | One or more errors found — do not commit |

### What it checks

**Required fields — deployment schema v1.1**

`id`, `operator`, `lat`, `lon`, `date_start`, `data_quality`, `source_url`, `source_type`

**Required fields — retrospective FR incident schema v1.0**

Different schema branch: uses `police_force`, `footage_lat`/`footage_lon`, `incident_date`, `outcome`. Detected automatically via the `is_incident` flag on each record.

**Coordinate bounds — Greater London**

| Field | Min | Max |
|-------|-----|-----|
| lat | 51.28 | 51.69 |
| lon | -0.51 | 0.34 |

**Enum validation**

- `data_quality`: `confirmed` / `approximate` / `unverified`
- `source_type`: `FOI_disclosure` / `news_report` / `court_record` / `police_statement` / `operator_statement` / `ngo_report`

**Date validation**

- ISO 8601 format (`YYYY-MM-DD`) required
- No dates before 2011
- `date_end` must not precede `date_start`

**Near-duplicate detection**

Warns when two records are within **300 metres** and **90 days** of each other. Legitimate cluster records (e.g. the two Stratford deployments) use `location_cluster_id` to signal intent and suppress false positives.

**Cluster consistency**

Warns if records sharing a `location_cluster_id` span more than one borough.

**Source URL vs data_quality**

Records marked `confirmed` must have a specific, non-generic source URL. A homepage or campaign index page cannot support `confirmed`.

### Output format

ANSI-coloured on Windows terminals that support it; plain text fallback otherwise.

```
[OK]  lfr-001 — all required fields present
[OK]  lfr-001 — coordinates within Greater London bounds
[!!]  lfr-005 — ward is null (consider populating)
[XX]  lfr-009 — missing required field: source_url

Summary: 2 errors, 1 warning across 9 records
```

### Dependencies

Standard library only: `json`, `math`, `datetime`, `sys`, `os`, `collections`. No `pip install` needed.

---

## Adding new scripts

- **One script, one purpose** — keep them small and chainable
- **Exit code discipline** — `0` = success, non-zero = failure
- **Run from project root** — paths relative to `D:\Dev\ALHFRS\`, not to `scripts/`
- **Document here** — add a section to this README when you add a script
