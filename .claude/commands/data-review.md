# /data-review — ALHFRS Dataset Review

Reviews a policing or FRS dataset for data quality issues before it is merged into the ALHFRS project. Accepts a file path as argument (JSON or CSV). If no argument is given, reviews all files in `data/deployments/`.

## Usage

```
/data-review data/deployments/new-file.json
/data-review data/deployments/
/data-review                         # reviews all deployment files
```

---

## What this command does

When invoked, run the automated validator first, then perform a structured LLM review:

### Step 1 — Automated validation

```bash
python scripts/validate-dataset.py $ARGUMENTS
```

Report the full output verbatim. Note any errors (exit code 1) vs warnings only (exit code 0).

### Step 2 — LLM quality review

Read the file(s) in full and apply the following checklist. For each issue found, report:
- **Severity**: HIGH / MEDIUM / LOW
- **Record ID(s)** affected
- **Finding**: what the problem is
- **Recommended fix**: exact change to make

---

## Review checklist

### A. Duplicates and near-duplicates
- Are any two records within 300m of each other? If so, check whether they share a `location_cluster_id`. If not, flag.
- Are any two records at the same location within 90 days of each other with no explanation in `notes`?
- Are any two records describing the same incident from different sources (e.g. a Met statement and a Big Brother Watch report)?

### B. Coordinate validity
- Does the lat/lon place the marker in the stated borough? (Use your knowledge of London geography.)
- Any coordinates at 0.0 / 0.0 or suspiciously round numbers (e.g. lon exactly 0.0000)?
- Any coordinates obviously wrong (e.g. a Westminster record with an East London lat/lon)?

### C. Data quality assignment
- Is `data_quality: confirmed` justified? Confirmed requires a primary source: Met Police FOI disclosure, ICO notice, court record, or official police statement. News reports alone are `approximate`.
- Is `data_quality: approximate` appropriate? Use when location/date is derived from adjacent evidence (e.g. court record places incident nearby but not exact address).
- Flag any `unverified` records for immediate follow-up — these should not stay unverified indefinitely.

### D. Source quality
- Does the `source_url` point to a specific document or page? Generic domain roots (met.police.uk/, bigbrotherwatch.org.uk/) are insufficient for `confirmed` records.
- Is the `source_type` accurate? Options: `FOI_disclosure`, `news_report`, `court_record`, `police_statement`, `operator_statement`, `ngo_report`.

### E. Categorical fit
- Does this record belong in `data/deployments/`? Or should it be in:
  - `data/legal/enforcement-actions.json` (regulatory action, not a deployment location)
  - `data/legal/` (court case, parliamentary question)
  - `data/news/` (news article without a specific deployment)
- Private operator records (Facewatch, Clearview, etc.) belong in `private-operators.json`, not `met-police-lfr.json`.

### F. Temporal anomalies
- Any dates before 2011 (UK police FR trials didn't begin until ~2015)?
- Any `date_end` before `date_start`?
- Any deployment lasting implausibly long (>6 months) without a note explaining it's a permanent installation?

### G. Missing annotations
- Is the `notes` field blank when the incident is known to have documentary significance (court case, parliamentary question, false positive incident)?
- Is `ward` null when the location is specific enough to determine it?
- Is `outcome_arrests` null for a deployment where Met published statistics?

### H. Schema consistency
- Do all records use the same field names and value conventions as the rest of the file?
- Are `null` values used consistently (not empty strings `""` or the string `"null"`)?

---

## Output format

After the automated validator output, produce a structured report:

```
## Data Review Report — [filename] — [date]

### Automated validator: [PASSED / X errors / Y warnings]

### Issues found

| # | Severity | Record(s) | Finding | Recommended fix |
|---|----------|-----------|---------|-----------------|
| 1 | HIGH     | lfr-003   | ...     | ...             |

### Records approved as-is
[List IDs that passed all checks with no issues]

### Suggested next steps
[Max 3 bullets]
```

If no issues are found, say so clearly and confirm the file is ready to merge.

---

## Context for the reviewer

This project documents facial recognition deployments across London. Accuracy is critical — errors propagate into a public-facing map. When in doubt, **downgrade** data_quality rather than assert confidence we don't have. The `notes` field is the place to document uncertainty in plain language.

Key source hierarchy (highest to lowest confidence):
1. Met Police FOI disclosure or official published log
2. ICO enforcement notice or court judgment
3. Official police press release or statement
4. NGO report (Big Brother Watch, Liberty) with specific deployment detail
5. Journalism citing a named source
6. Journalism without named source / general claims

The Bridges and Thompson cases establish that erroneous LFR identifications have real consequences for real people. Treat every record as if it will be scrutinised in court.
