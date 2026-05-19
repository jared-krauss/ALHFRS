# Visualization Brainstorm — ALHFRS
## A London History of Facial Recognition Systems

> **Status:** Working document, May 2026  
> **Audience:** Jared (project lead) + future collaborators  
> **Note:** `map-embed.html` referenced in brief does not exist — the current map entry point is `map/index.html`. This document treats the Leaflet map as the primary existing UI and discusses all visualizations in relation to it.

---

## Data Audit Summary

Before the viz concepts, a grounding inventory of what is and isn't available now:

| Dataset | Records | Date range | Key gaps |
|---|---|---|---|
| Met Police LFR | 8 | 2020–2026 | Outcome data sparse (only lfr-008 has arrest count); watchlist sizes unknown |
| BTP LFR | 2 | Feb 2026 | Vendor not named; outcome data absent |
| Private operators | 5 | ~2022–ongoing | All Facewatch/Sainsbury's; dates approximate; ~200+ additional UK Facewatch clients undocumented |
| Retrospective FR | 4 | 2024–2026 | Mixed forces; 3 are false-positive case studies; mass RFR (rfr-004, Aug 2024 riots) unquantified |
| Legal/enforcement | 4 | 2020–2026 | Appeal outcomes pending (legal-002 appeal; legal-003 Court of Appeal) |
| News archive | 21 | 2024–2026 | ~12 URLs unresolved (share.google redirects) |

**Scale stats available for annotation:**
- lfr-008 (Croydon static): 470,000 faces scanned, 173 arrests, Oct 2025–Mar 2026
- Met RFR: 3,030 → 24,677 searches in 2024 alone (+700%)
- UK total RFR 2024: 252,798 searches
- London 2026 YTD: ~1.7M faces scanned (Security Today / news-001)
- NEC Neoface confirmed as Met LFR + OIFR vendor

---

## 1 — Deployment Timeline

### Chart type
**Annotated step chart** (cumulative active deployments over time) with a secondary axis showing **RFR search volume** (bar chart underneath). Two series: police operators and private operators. Key legal/policy events as vertical annotation lines.

### Why not a smooth curve
Deployments are point-in-time events, not continuous measurements. A step function that holds a level until the next deployment is more honest about how surveillance infrastructure actually accumulates.

### The story it tells
Surveillance doesn't arrive all at once — it *accretes*. The chart shows:  
- 2020: A scattering of Met mobile operations, legally ambiguous after Bridges  
- 2022: The private sector quietly enters at scale (5 Facewatch stores, no public announcement)  
- 2024–2025: Pace accelerates — Wembley, Croydon static, RFR volume spikes 700%  
- 2026: The ceiling cracks open — BTP expands to rail, OIFR handheld pilot, Mayor confirms identity checks, Liberty challenge dismissed. National rollout announced.

The legal annotation lines show that Bridges (2020) and the EHRC intervention (Oct 2025) produced no visible inflection in the deployment curve. The challenge line (Liberty v Met, Apr 2026) is followed *immediately* by a national rollout announcement.

### Data fields needed
```
date_start        (all deployment records)
date_end          (null = still active)
operator_type     (law_enforcement vs retail — for series split)
id                (for hover/tooltip)
— supplementary —
legal events from enforcement-actions.json: date field
news events for annotation: date + title (news-001, news-004, news-014, news-017)
RFR volume: rfr_volume_2024 context block + quarterly estimates if researchable
```

### Annotation candidates (vertical lines)
| Date | Label | Colour |
|---|---|---|
| 2020-08-11 | Bridges ruling | amber |
| 2022-05-23 | Clearview AI £7.5M fine | amber |
| 2024-08 | August riots — mass RFR | red |
| 2025-10-13 | EHRC intervention | amber |
| 2026-04-21 | Liberty v Met dismissed | red |
| 2026-04-21 | National rollout announced | red |

### Implementation complexity
**Medium.** D3.js or Observable Plot. The step chart logic is standard; the dual-axis with annotation lines adds complexity but is well-trodden. Tooltip on each step node showing deployment details. Biggest challenge: constructing the RFR volume secondary series requires additional research to get quarterly figures.

### Embed location
**Separate page section** (scrollable narrative / longform page). Too information-dense for the map sidebar. Could also work as a full-bleed hero element at the top of the site's main page before the map.

---

## 2 — Operator Breakdown

### Chart type
**Horizontal stacked bar chart** — one bar per operator category (Met Police / BTP / Private Retail), broken down by deployment type (mobile / static / ongoing). Below it, a secondary panel showing the only outcome stat we have: **faces scanned vs arrests** as a proportional graphic for lfr-008.

Alternative framing: a **Sankey diagram** flowing from operator → deployment_type → location_cluster. More editorial but harder to build.

### The story it tells
Private retail has more permanent static installations (5, all Facewatch, all ongoing since 2022) than either police force. BTP went from zero to two major termini in three days in February 2026. The Met's operational tempo is episodic — mobile deployments — until Croydon becomes permanent. "Permanent" is the meaningful threshold: once cameras are bolted to a wall, the question shifts from *when will they leave* to *who decides they stay*.

The outcome panel is a visual gut-punch: Croydon scanned **470,000 faces** to produce **173 arrests** — a 0.037% match rate. Whether that justifies the surveillance of 470,000 people is the question the chart asks and declines to answer.

### Data fields needed
```
operator          (for grouping)
operator_type     (law_enforcement / retail)
deployment_type   (mobile / static)
date_end          (null = still active → "ongoing" category)
outcome_arrests   (lfr-008 only — for proportional graphic)
— calculated —
"faces scanned" stat: 470,000 (from lfr-008 notes, needs field in schema)
```

### Schema gap
`outcome_faces_scanned` is not a field in schema v1.1. The 470,000 figure is buried in `notes`. Worth adding a formal field.

### Implementation complexity
**Simple.** Standard charting library (Chart.js, Recharts, or plain D3). The proportional faces/arrests graphic could be a simple dot matrix or icon array — 470,000 dots for scanned faces, 173 highlighted — which is visually arresting and requires minimal code if the dot count is stylised (e.g., at 1:100 scale: 4,700 dots, 1.73 highlighted).

### Embed location
**Map UI panel** (right-hand sidebar or bottom sheet on mobile). Brief version — just the bar chart without the secondary panel — works as a compact overview when a user first opens the map.

---

## 3 — Vendor Ecosystem

### Chart type
**Force-directed network graph** (D3 force simulation). Three node types:

- **Technology vendors** (NEC/Neoface, Facewatch, Clearview AI, Police National Database, unknown BTP vendor)
- **Operators / deployers** (Metropolitan Police, BTP, Sainsbury's/Facewatch clients, Serco Leisure)
- **Oversight / accountability bodies** (ICO, EHRC, High Court, Court of Appeal, Parliament)

Edge types:
- **Supply relationship** (vendor → operator) — solid line
- **Enforcement action** (oversight body → vendor/operator) — dashed red line
- **Legal challenge** (oversight body → operator) — dashed amber line

Node size: scaled to number of deployment records or people affected (where known).

### The story it tells
The supply chain for mass surveillance in London is extraordinarily thin. Two vendors — NEC and Facewatch — supply virtually all documented deployments. The oversight apparatus (ICO, EHRC, courts) fires enforcement actions that create noise but not blockage: Clearview was fined in 2022, is still litigating in 2026. Serco was ordered to stop and did. The Met was challenged in court and won. The graph makes visible what prose tends to obscure: the *structural* relationships between commercial interests, state power, and the institutions supposedly constraining them.

### Data fields needed
This viz requires editorial synthesis, not direct JSON fields. The graph is assembled from:
```
— vendors (manual, from notes fields across all JSON files) —
NEC Neoface: Met LFR (all 8 records) + OIFR (retrospective-fr.json context)
Facewatch: priv-001 through priv-005
Clearview AI: legal-003
PND (Police National Database): RFR context block (252,798 searches 2024)
BTP vendor: unknown — research needed

— operators —
All operator fields across deployment files

— oversight bodies —
From enforcement-actions.json: enforcement_body, court fields
```

### Implementation complexity
**Complex.** D3 force simulation with custom node rendering, collision detection, drag interaction, and tooltip panels. Roughly 2–3 days of front-end work. The visual payoff is high but it needs careful layout tuning — force graphs are chaotic by default. Consider static layout as a fallback (manually positioned nodes, no physics) if implementation time is constrained.

### Embed location
**Separate page section** — the graph needs space to breathe and cannot function in a map sidebar. Could live in a "System" or "Who Profits" section of the site.

---

## 4 — Geographic Density

### Chart type
**Choropleth map** — London boroughs shaded by deployment density — overlaid on the existing Leaflet base. This would be a new *statistical layer* toggled alongside the current pin markers, not a replacement for them.

Two variants worth building:

**Variant A — Raw deployment count by borough**  
Simple: count of records per borough. Boroughs: Croydon (2 Met), Newham (2 Met), Southwark (1 BTP + 1 private), and so on.

**Variant B — Deprivation × deployment overlay**  
More powerful: cross-reference deployment count against Index of Multiple Deprivation (IMD) decile data (publicly available from MHCLG). Shows whether surveillance concentrates in London's most economically deprived areas. This is the Croydon and Newham story — not just high-deprivation boroughs happen to have deployments, but that deprivation is the *shared characteristic* of the places being watched.

### The story it tells
Variant A: Surveillance isn't evenly spread across London. It concentrates in specific zones — East London shopping complexes, South London town centres, major rail termini.  

Variant B (the more powerful version): Add a deprivation fill and you see that Croydon (LFR permanent), Newham (LFR twice, 2020 and 2023), Tower Hamlets (Facewatch), Hackney (Facewatch) are all in or near the most deprived quintile of London boroughs. Westminster, where lfr-002 was deployed, is an outlier — a commercial/tourist zone. The pattern is: surveillance follows deprivation, with a carve-out for major commercial infrastructure.

Key annotation for the map: the lfr-008 note from CLAUDE.md — *"Croydon is also one of London's most deprived boroughs — demographic implications documented by Zoë Garbett GLA Feb 2026."*

### Data fields needed
```
— from deployment records —
borough           (all 15 deployment records)
operator_type     (for colour coding within choropleth)

— external data needed —
London Borough IMD 2019/2023 scores (from MHCLG — free, GeoJSON available)
Borough-level ethnic composition from 2021 Census (ONS)

— computed —
deployments_per_borough (aggregate count)
implication: needs a borough → IMD lookup table
```

### Implementation complexity
**Medium.** The Leaflet choropleth layer itself is simple — `london-boroughs.geojson` is already loaded in the map, just needs fill logic added. The IMD data join requires a lookup table (~33 rows). Variant B adds complexity if you want a bivariate choropleth (two dimensions — deprivation × deployment density — encoded simultaneously), which requires a custom colour scheme (e.g., 3×3 or 4×4 grid). A bivariate choropleth is genuinely complex but visually extraordinary. Rough time estimate: simple choropleth 1 day, bivariate 3–4 days.

### Embed location
**Inside map UI** — a new layer toggle "Deployment density" in the existing panel. Toggles the borough fill on/off without removing the point markers.

---

## 5 — Legal/Policy Timeline

### Chart type
**Vertical annotated timeline** (newspaper-style) with two tracks running in parallel:

- **Left track:** Deployment escalation events (each deployment or policy change as a labelled node)
- **Right track:** Legal/accountability responses (court cases, ICO enforcement, parliamentary interventions, NGO reports)

The tracks run simultaneously so you can read across: what legal action was happening *at the same time* as each deployment expansion.

Alternative: **Deployment growth curve** (cumulative deployments, same as Viz 1) with legal events as annotated pins *on* the curve, sized by outcome significance. This is the more editorial approach — the curve is a protagonist, the legal events are the antagonists, and the curve never bends.

### The story it tells
Legal challenge and deployment expansion are happening simultaneously, not sequentially. The Bridges ruling (2020) found SWP's use unlawful — the Met immediately pressed on regardless, operating under a different legal rationale. The Liberty challenge (filed ~2024, decided Apr 2026) was dismissed. One month later, national rollout was announced.

The timeline makes the pattern unmissable: accountability mechanisms are *reactive by design*, perpetually chasing a deployment programme that moves faster than litigation. Each legal event creates a brief pause in public discourse, then deployment accelerates again.

Key pairing to highlight: **Bridges ruling (Aug 2020) → lfr-003 Stratford (Jun 2020, during BLM protests)**. The deployment at Stratford predates Bridges and occurred during the largest civil rights protests in a generation. The legal system's response arrived after the surveillance had already happened.

### Data fields needed
```
— from enforcement-actions.json —
date, case_name, outcome, significance (all 4 records)

— from deployment records —
date_start, location_name, operator (all 15 records)

— from news archive —
date, title, tags (selected records: news-001, news-004, news-005, news-006,
news-010, news-013, news-014, news-017, news-018)

— manually compiled key policy events —
2025-08: +10 mobile LFR vans nationally (news-014)
2026-02: Mayor confirms identity checks pilot (news-006)
2026-03: Croydon made permanent (news-017)
2026-04: National rollout announced (news-004)
```

### Implementation complexity
**Simple to Medium.** A vertical timeline is CSS-heavy but technically simple — mostly layout, not complex data logic. The annotated line chart variant requires D3. Both are achievable in 1–2 days. The editorial challenge is harder than the technical one: choosing which ~15–20 events to include and writing the annotation copy.

### Embed location
**Separate page section** — a standalone "History" or "The Record" section. Too long for a map sidebar. This is the spine of the longform site narrative. Should probably come *before* the map, as contextual framing.

---

## 6 — Demographic Bias

### Current data state
This is the most important visualization and the one with the least data. The existing records contain:

- Qualitative notes on demographic context (Croydon deprivation, Whitechapel's Bangladeshi community, Dalston's Black Caribbean population)
- Four false-positive case studies (rfr-001 to rfr-003 and priv-002) — three involve named individuals with documented racial dimensions
- News-010: Home Office admitted bias with Black and Asian subjects
- News-005: Essex Police "tweaked" biased FR software
- rfr-002: Liberty Investigates documented racial bias ("generic racial similarities... 97% error cited")

What's missing: systematic false-positive rate disaggregated by ethnicity, MOPAC stop-and-search outcome data by borough, watchlist demographic composition.

### Chart type (what's buildable now)
**Case study matrix** — a table-as-infographic showing documented false-positive incidents. Each row is a case. Columns: location / operator / victim demographics / custody duration / legal outcome / source quality. Styled as a redacted-document aesthetic (monospace, horizontal rules, faint redaction bars over unknown fields).

This is small-data journalism, not statistics. Five documented cases (rfr-001, rfr-002, rfr-003, priv-002, lfr-006 / Thompson) with named or partially named individuals. The story is told through specifics, not distributions.

**Future chart type (when data exists)**  
**Diverging bar chart** — false-positive rate by ethnicity, compared against London population proportions (2021 Census baseline). One bar for each ethnic group: positive = over-representation in false alerts, negative = under-representation. Referenced directly against NIST FRVT demographic bias testing data and the Home Office admission in news-010.

### The story it tells (case study version)
These are not edge cases. In three months of documented 2026 incidents: a man held 24 hours on an RFR false positive in Harlesden (Black British, Colin McMahon); a man wrongly arrested on "generic Asian" racial similarity reasoning in Milton Keynes (Alvi Choudhury); a man ejected from Sainsbury's on a Facewatch false positive (Warren Rajah, described as Black in Guardian reporting). All cleared. All in communities of colour. The Met claimed in December 2025 that "no one has been arrested from a false positive." Three documented cases say otherwise within four months of that claim.

### Data fields needed
```
— currently available —
rfr-001 to rfr-004 (incidents[] array)
priv-002 notes (Rajah incident, Guardian ref)
lfr-006 notes (Thompson incident)
legal-002 (Thompson / Liberty v Met)

— external data for future version —
MOPAC stop-and-search demographics by borough (data/interactions/ — placeholder)
2021 Census ethnic composition by borough (ONS)
NIST FRVT demographic bias data (frvt.nist.gov)
Home Office FR accuracy testing by ethnicity (news-010)
```

### Implementation complexity
**Simple** (case study matrix) — this is mostly CSS layout and careful copywriting. The matrix itself could be an HTML table with editorial styling, no D3 required.  
**Complex** (future diverging bar) — requires acquiring and cleaning external demographic datasets before the chart can be built.

### Embed location
**Separate page section** — "Who Gets Watched" or "False Positives." The case study matrix should stand alone on the page, given the gravity of the subject. Not appropriate for the map sidebar. Could link *from* individual map markers (e.g., clicking lfr-006 at Liverpool Street surfaces the Thompson case with a link to the full section).

---

## Hero Picks: Standalone Documentary Art Pieces

Three visualizations most suitable as primary exhibition/publication pieces — designed to work as images, not just interactive tools:

---

### ★ Hero 1 — The Deployment Curve with Legal Annotations *(Viz 5 / Viz 1 combined)*

**Why it's the hero:** It contains the entire argument of the project in a single image. A rising step curve that never reverses, with every legal challenge marked on it, and the curve visibly indifferent to those challenges. The fact that the Liberty v Met dismissal (Apr 2026) is followed immediately by the national rollout announcement creates a visual moment — the curve steepens *after* the court ruling.

**Standalone format:** Dark background, portrait orientation. The curve in red (#e94560). Legal challenge annotations in amber. National rollout annotation in a different red, slightly brighter. Minimal axis labels — the years as faint guides, not prominent data. A single pull-quote annotation: *"The deployment programme moves faster than litigation."*

**Publication contexts:** Print-ready for investigative journalism (The Guardian, The Intercept). Exhibition print at A1. Hero image for the site's landing page.

---

### ★ Hero 2 — Deprivation × Surveillance Bivariate Choropleth *(Viz 4, Variant B)*

**Why it's the hero:** The geographic argument about who gets watched, made without words. A bivariate choropleth encoding both deprivation rank and deployment count simultaneously. Dark grey for low-deprivation/no-deployment boroughs (most of London). Deep red for high-deprivation/high-deployment (Croydon, Newham, Tower Hamlets, Hackney). The visual weight of the map lands in East and South London — historically working-class, disproportionately Black, Asian and Mixed communities.

**Standalone format:** Full London borough map, portrait orientation. No base map tiles (pure GeoJSON fill — more graphic, less cartographic). A legend key explaining the bivariate encoding. Minimal labelling — borough names only on the high-combined-score boroughs. Single annotation: *"Croydon. London's first permanent facial recognition cameras. 10th most deprived borough."*

**Publication contexts:** Exhibition print. Campaign material for Big Brother Watch, Liberty. Booklet/zine production.

---

### ★ Hero 3 — False Positive Case Study Matrix *(Viz 6)*

**Why it's the hero:** The statistical argument is abstract; the names are not. A matrix of documented false positives — styled as a partially-redacted evidence document — with each row carrying the weight of a specific life disrupted. Five cases, five rows, running from the Thompson misidentification (Liverpool Street, 2024) through to the Harlesden arrest (April 2026). The most powerful element: the final column is *outcome* — every row reads "Charges dropped," "Acquitted," "Wrongful arrest." The Met's claim that "no one has been arrested from a false positive" is footnoted at the bottom.

**Standalone format:** Monospace typeface (Courier or JetBrains Mono). Off-white text on near-black (#0d1117). Horizontal rules between rows. "REDACTED" bars over fields that are genuinely unknown (victim names in rfr-003, rfr-004). The document aesthetic suggests suppressed evidence, partially revealed. A footer: *"Metropolitan Police, December 2025: 'No arrests have been made as a result of a false positive alert.'"*

**Publication contexts:** Print. Web. Could be produced as a physical document for exhibition — A4 pages that visitors can handle.

---

## Aesthetic Brief & Design System

### Reference points
- **NYT Graphics / The Pudding** — chart-first storytelling, dark mode, editorial annotation on the chart itself not just in surrounding copy
- **The Intercept** — document aesthetics, redaction as visual language, legal/surveillance subject matter
- **Forensic Architecture** — evidence-building aesthetic, precision over polish, the chart as argument
- **Big Brother Watch campaign materials** — accessible but urgent; not academic

### Colour palette (consistent with map/index.html)
```css
--bg-primary:     #0d1117;   /* background */
--bg-elevated:    #131b2e;   /* card / panel surfaces */
--border:         #2a3a5e;   /* borders, dividers */
--text-primary:   #e2e8f8;   /* headlines */
--text-secondary: #9ba8c0;   /* body */
--text-muted:     #6b7fa8;   /* metadata, footnotes */
--accent-red:     #e94560;   /* alerts, active states, primary data series */
--accent-amber:   #c97f2c;   /* warnings, legal annotations */
--accent-blue:    #4a7fa8;   /* links, neutral data */
--confirmed:      #2e7d52;   /* data quality confirmed */
--approximate:    #c97f2c;   /* data quality approximate */
--unverified:     #7a3535;   /* data quality unverified */
```

### Typography
- **Headlines/labels:** `ui-monospace` stack (SF Mono / Consolas / Courier New) — the surveillance-document aesthetic
- **Body/annotations:** `-apple-system` stack (matches existing map)
- **Data values:** Monospace, slightly larger weight than labels

### Chart rules
1. Dark background always — these are not corporate dashboards
2. Grid lines at 15–20% opacity, never prominent
3. Annotation text *on* the chart, not just in captions — the editorial reading should be embedded in the data space
4. No rounded corners on chart elements (rectangles stay rectangular)
5. Axis labels: minimal, left-aligned, no box or border
6. Source citations in the chart footer, same size as axis labels

---

## Data Gaps & Research Needs

Before Viz 6 (demographic bias) can be built beyond the case study version:

| Gap | Where to get it | Priority |
|---|---|---|
| Ethnicity of false-positive victims (lfr-006 Thompson, priv-002 Rajah — partially confirmed; rfr-003 unnamed) | News reporting; Liberty Investigates | High |
| MOPAC stop-and-search data by borough and ethnicity | met.police.uk / MOPAC data dashboard | High |
| BTP LFR vendor name | BTP FOI request | Medium |
| Watchlist size and demographic composition for any Met LFR deployment | Met FOI request — likely refused initially | High |
| Quarterly RFR volume for secondary axis in Viz 1 | Parliamentary Research Briefings; Met annual reports | Medium |
| `outcome_faces_scanned` as a formal schema field | Add to schema v1.2 | Low (internal) |
| Resolve 12 share.google redirects in news archive | Browser resolution and canonical URL update | Medium |

---

*Generated from live data audit of ALHFRS deployment files. Last updated 2026-05-18.*
