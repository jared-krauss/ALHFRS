# Gemini Prompt — Geocode ALHFRS Null Lat/Lon Records

**Use in:** Google AI Studio (aistudio.google.com)  
**Model:** Gemini 2.5 Flash or Pro (tools NOT required — this is pure inference)  
**Purpose:** Fill lat/lon for 169 ALHFRS deployment records where coordinates are null.  
**Accuracy target:** Street-centroid level (±100m is fine — these are police van deployments, not point-precision forensics)

**How to use:**  
1. Open `D:\Dev\ALHFRS\data\staging\geocoding-needed.json`  
2. Copy its contents  
3. Paste into the prompt below where indicated  
4. Run. Gemini will return a JSON array with coordinates filled in.  
5. Save output to `D:\Dev\ALHFRS\data\staging\geocoding-results.json`

---

## COPY THIS PROMPT INTO AI STUDIO

---

You are a geocoding assistant with expert knowledge of London geography.

I have 169 Metropolitan Police LFR deployment records that are missing latitude/longitude coordinates. Each record has an `id`, `location_name`, `borough`, and `ward`. Your task is to provide best-estimate WGS84 decimal degree coordinates for each record.

**Accuracy standard:** Street-centroid level. These are police mobile surveillance deployments — a point that falls on or very near the named street or location is sufficient. You do not need sub-10m precision.

**Confidence flag:** For each record, add a `geo_confidence` field:
- `"high"` — you are confident in the specific street location (e.g., "Romford Market, South Street" → precise)
- `"medium"` — you know the general area but not the exact street (e.g., "Westminster" with ward info → borough centroid-ish)
- `"low"` — the location is vague and you are using a borough or ward centroid only

**If you genuinely cannot determine coordinates** for a record (location name is too ambiguous and you have no ward info), set `lat` and `lon` to `null` and `geo_confidence` to `"failed"`.

---

### INPUT DATA

Paste the contents of geocoding-needed.json here:

```json
[PASTE CONTENTS OF D:\Dev\ALHFRS\data\staging\geocoding-needed.json HERE]
```

---

### OUTPUT FORMAT

Return a single JSON array. Each element must include:

```json
[
  {
    "id": "lfr-376",
    "lat": 51.3727,
    "lon": -0.1007,
    "geo_confidence": "high",
    "geo_note": "Church St, Croydon town centre — centroid of pedestrianised shopping street"
  }
]
```

Fields:
- `id` — copy from input, do not change
- `lat` — decimal degrees, 4–6 decimal places
- `lon` — decimal degrees, 4–6 decimal places (negative = west of Greenwich)
- `geo_confidence` — `"high"` / `"medium"` / `"low"` / `"failed"`
- `geo_note` — one sentence explaining your reasoning or the reference point used

**Only return the JSON array.** No prose before or after. This output will be parsed programmatically.

---

### LONDON GEOGRAPHY NOTES

- All deployments are within Greater London (roughly 51.28°N–51.69°N, -0.51°W–0.34°E)
- The Met Police area covers 32 boroughs + City of London
- Common deployment locations: high streets, markets, transport hubs, shopping centres
- If a location says "High St, [Borough]" and you're not certain which High St, use the main town centre high street for that borough
- Ward boundaries are a useful fallback — use ward centroid if street is ambiguous

---
