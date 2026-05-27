# Gemini Prompt — Met Police LFR Deployment Extraction

**Use in:** Google AI Studio (aistudio.google.com)  
**Model:** Gemini 2.5 Pro (with URL/tool access enabled — use the "Run with tools" toggle)  
**Purpose:** Extract all Met Police Live Facial Recognition deployment events from public sources.  
**Primary gap:** 2021 is entirely missing from our dataset. Secondary goal: corroborate 2020 and 2022–2026 records.

---

## COPY THIS PROMPT INTO AI STUDIO

---

You are a research assistant extracting structured data about Metropolitan Police Service (MPS) Live Facial Recognition (LFR) deployments in London from public sources.

**Your task:** Visit the URLs listed below, follow links to relevant PDFs or disclosure documents, and extract every LFR deployment event you can find. Focus especially on **2021**, which is our primary data gap, but extract all years you encounter so we can corroborate existing records.

---

### START WITH THESE URLS (visit each one)

1. **Primary FOI release — covers 2021–2023:**  
   https://www.met.police.uk/foi-ai/metropolitan-police/disclosure-2024/april-2024/locations-facial-recognition-cameras-arrests-london-boroughs-2021-2023/

2. **MPS FOI disclosure index — search for "facial recognition":**  
   https://www.met.police.uk/foi-ai/metropolitan-police/  
   Search or browse for any FOI releases mentioning: facial recognition, LFR, live facial recognition

3. **Big Brother Watch — LFR tracker and reports:**  
   https://bigbrotherwatch.org.uk/campaigns/face-off/  
   https://bigbrotherwatch.org.uk/2021/  
   Download any PDFs about Met Police LFR deployments

4. **HMICFRS — inspection reports mentioning Met LFR:**  
   https://hmicfrs.justiceinspectorates.gov.uk/  
   Search: "facial recognition Metropolitan Police"

5. **MPS annual statistics / data:**  
   https://www.met.police.uk/police-data/

6. **Liberty — facial recognition reports 2020–2022:**  
   https://www.libertyhumanrights.org.uk/  
   Search: "facial recognition" + "Metropolitan Police"

For each source, follow links to the actual documents (PDFs, spreadsheets, disclosure tables) — don't just read the summary page.

---

### WHAT TO EXTRACT

For every **deployment event** you find, extract the following fields:

| Field | Description | Example |
|-------|-------------|---------|
| `location_name` | Street address or named location | "Romford Market, South Street" |
| `borough` | London borough | "Havering" |
| `ward` | Electoral ward if stated | "Romford Town" |
| `date_start` | ISO 8601 date YYYY-MM-DD | "2021-03-15" |
| `date_end` | End date if multi-day, else same as start | "2021-03-15" |
| `deployment_type` | One of: `mobile`, `fixed`, `event`, `pilot` | "mobile" |
| `stated_purpose` | Stated reason for deployment | "Wanted persons, crime prevention" |
| `outcome_arrests` | Number of arrests if stated | 2 |
| `outcome_alerts` | Number of alerts/matches if stated | 47 |
| `data_quality` | Your confidence: `confirmed` / `approximate` / `unverified` | "confirmed" |
| `source_url` | Direct URL to the document you extracted this from | "https://..." |
| `source_type` | One of: `FOI_disclosure`, `annual_report`, `press_release`, `NGO_report`, `HMICFRS_report` | "FOI_disclosure" |
| `notes` | Anything notable: ambiguities, conflicting info, partial data | "" |

**Do not invent or estimate values.** If a field is not stated in the source, set it to `null`. Only use `approximate` for date or location when the source gives a range or implies a period without a specific date.

---

### OUTPUT FORMAT

Return a single valid JSON array. Each element is one deployment. Use this exact structure:

```json
[
  {
    "location_name": "Romford Market, South Street",
    "borough": "Havering",
    "ward": "Romford Town",
    "date_start": "2021-03-15",
    "date_end": "2021-03-15",
    "deployment_type": "mobile",
    "stated_purpose": "Wanted persons, crime prevention",
    "outcome_arrests": null,
    "outcome_alerts": null,
    "data_quality": "confirmed",
    "source_url": "https://www.met.police.uk/foi-ai/.../",
    "source_type": "FOI_disclosure",
    "notes": ""
  }
]
```

**After the JSON array**, include a brief **Source Summary** section listing:
- Which URLs you successfully accessed
- Which PDFs you read
- Which years each source covered
- Any sources that returned errors or were inaccessible
- Any notable discrepancies between sources (e.g., two sources give different arrest counts for the same deployment)

---

### IMPORTANT NOTES

- The Metropolitan Police began regular LFR deployments in 2020. Prior to that were pilots (2016–2019) — include those if found, but note them as `deployment_type: "pilot"`.
- "LFR" and "live facial recognition" and "facial recognition van" all refer to the same system — include all.
- Some FOI responses give aggregate counts (e.g., "47 deployments in 2021") without individual records — if so, note the aggregate in your Source Summary but don't fabricate individual records.
- If a document gives a table of deployments with dates and locations, extract each row as a separate record.
- Flag any 2021 records especially clearly in your notes (add `"notes": "2021 record — primary data gap"`)

---

### AFTER EXTRACTION

Once you have your JSON array, cross-check: do any of your extracted records clearly match the same deployment event from two different sources? If so, merge them into one record and note both source URLs in `notes`.

---
