# MAP-REDESIGN-RECOMMENDATIONS.md
> Visual design analysis and encoding rationale for `map-embed.html`
> Prepared 2026-05-28 · Code audit, data verification, and multi-perspective design review

---

## Summary of findings

The map's visual design had accumulated four compounding problems:

1. **Borough button mis-cued** — `.layer-btn.active` coloured the "Borough boundaries" toggle `#ff6eb4` (Met Police pink), making a spatial-layer control look like an operator filter.
2. **Boundary strokes washed out** — CSS `body::before` halation blob at `rgba(255,110,180,0.13)` / `blur(80px)` spread pink across the canvas, obscuring dark navy `#2a3a5e` boundary strokes. Root cause: opacity too high, not a colour clash.
3. **Dot size encoded nothing** — `RADII = { met:9, btp:8, private:7 }` was arbitrary. A free visual channel (radius) was wasted on uniform decoration.
4. **Map silent about itself** — no visible text without clicking told a new visitor what physically happens at a dot. "LFR" appeared in the legend but was never decoded.

All four were confirmed from code inspection and data analysis. P0 fixes address all of them.

---

## Colour system

### Operator hue palette (unchanged — correct)

| Operator | Hex | Rationale |
|---|---|---|
| Met Police LFR | `#ff6eb4` pink | High-chroma distinctive; Met deployments are the majority |
| BTP LFR | `#7ed4fd` blue | Cold, institutional, contrasts with Met |
| Private (Facewatch) | `#a78bfa` purple | Distinct from both; softer than Met |
| Retrospective FR | `#fb923c` orange | Categorically different technology — warm anchor |

The neon-pastel palette on CartoDB Dark reads well at low zoom. Operator hue is the primary categorical channel and must not be reused for anything else (which is why the borough button active state needed its own override: `#6a9aba` steel blue).

### Borough boundary (unchanged — `#2a3a5e`)

Navy-dark boundary strokes deliberately sit below the dot layer visually. The root fix (halation reduction) restores legibility without introducing a competing data colour. A teal or high-chroma border colour would read as a 5th operator type.

---

## Visual encoding rationale

Full encoding table — all channels accounted for:

| Channel | Value | What it encodes |
|---|---|---|
| **Hue** | `#ff6eb4` / `#7ed4fd` / `#a78bfa` / `#fb923c` | Operator type (categorical) |
| **Fill opacity** | 1.0 / 0.72 / 0.48 | Data quality: confirmed / approximate / unverified |
| **Radius** | 3–12px (sqrt scale) | `outcome_arrests` count (quantitative) |
| **Stroke opacity** | 0.25 / 0.5 / 0.7 / 0.9 | Year recency: 2020-22 / 2023 / 2024 / 2025-26 |
| **Dash pattern** | `5, 3` dashed ring | Null `outcome_arrests` (data not disclosed) |

### Why radius = arrests

Arrests is the accountability metric at the civil liberties heart of this project. Radius is the most preattentive size channel — viewers read "bigger = more of something" without instruction. The distribution makes this legible: Croydon (173 arrests, 6-month deployment), Brixton, Woolwich, and Kilburn produce visibly larger dots against a field of small ones. A viewer can identify high-accountability clusters without opening a popup.

Arrests data completeness (verified from `met-police-lfr.json`, 580 records): null=11, zero=48, 1–5=358, 6–15=159, 16–50=3, 51+=1. 98% of records are populated. The CLAUDE.md note "outcome data sparse" was stale after the Garbett merge.

Sqrt scale formula: `Math.min(12, Math.max(4, Math.round(3 + Math.sqrt(a) * 1.5)))` — linear scale would make Croydon (~40px) dwarf everything. Sqrt compresses the tail while preserving order.

BTP (2 records) and private operators (5 records) have no arrests data — structurally absent, not sparse. Fixed radius 5px is appropriate.

### Why stroke opacity = year

Fill opacity is doing critical work (quality). Stroke opacity in Leaflet's `circleMarker` is orthogonal — it controls only the SVG stroke, not the fill. It was previously wasted at uniform 0.9 on all records.

Year encoding direction: newer = brighter ring. The program is growing (2020=6, 2021=0, 2022=7, 2023=47, 2024=183, 2025=240, 2026=97). Brighter rings on recent records signals program expansion without tooltip interaction.

The faded stroke on 2020–22 records also has correct semantic weight: historical records should feel more archival/background. This encoding direction was independently confirmed by data viz review.

**Why not year → dot size**: Size conventionally means "more of something quantitative." Year is ordinal, not quantitative. Mixing year into the size channel would corrupt the arrests signal and make the accountability pattern unreadable.

### Dashed ring for null-arrest records

11 Met records have null `outcome_arrests`. A dashed ring signals "data gap" without penalising these records with a zero-arrest radius — null ≠ zero. These 11 records get radius 3px (minimum) and `dashArray: '5, 3'`. Confirmed in legend.

---

## P0 fix specification

### P0.1 — Borough button active colour

**Problem:** `.layer-btn.active` sets `color: #ff6eb4` globally. When "Borough boundaries" is toggled on, the button turns Met Police pink — a spatial-layer control reads as an operator filter.

**Fix:** Added `#btn-boroughs.active` specific override after the generic rule:
```css
#btn-boroughs.active {
  background: rgba(106, 154, 186, 0.15);
  color: #6a9aba;
  border-color: #6a9aba;
}
```
Steel blue `#6a9aba` is visually neutral — distinguishable from all four operator hues. Does not modify the generic `.layer-btn.active` rule (other buttons unaffected).

### P0.2 — Halation opacity reduction

**Problem:** `body::before` `rgba(255,110,180,0.13)` at `blur(80px)` washed pink over the entire canvas. Borough boundary navy strokes (`#2a3a5e`) became indistinct — appeared to merge with Met dots despite being a different colour.

**Fix:** Reduced both halation blobs:
- Pink: `0.13` → `0.06`
- Blue: `0.10` → `0.05`

Halation is retained (separates dots from the dark tile background) but no longer overwhelms the boundary layer.

### P0.3 — Borough boundary weight

**Fix:** `weight: 1` → `weight: 0.75` — slight reduction to keep boundaries as spatial context rather than competing feature.

### P0.4 — Arrests radius + year stroke opacity

Added `arrestsRadius()` and `yearStrokeOpacity()` helpers. Replaced `RADII` constant with `LAYER_CONFIG` object. Rewrote `createDeploymentLayer(deployments, config)` to use per-record radius and stroke opacity rather than per-layer constants.

### P0.5 — Drop-shadow reduction

Marker `filter: drop-shadow` reduced from `5px / 0.75 opacity` to `3px / 0.40 opacity` on all four operator classes. Drop-shadow is retained (separates dots from dark tile) but reduced so it doesn't fight with the halation.

### P0.6 — Title bar self-description

**Problem:** No visible text explained what a dot represented. "LFR" in the legend was never decoded. New visitor had no mental model of "a police van on a London street scanning passing faces against a watchlist."

**Fix:** Title bar expanded from 36px to 52px. Permanent subtitle added:
> "Each dot marks a day police deployed live facial recognition cameras on a London street."

No click, no scroll, no tooltip — visible on load.

### P0.7 — Legend improvements

Three additions:
1. **Intro sentence** above operator list: "Each dot = one day of live facial recognition scanning."
2. **Arrests size key** (after quality section): three circles labelled 0 / 1–9 / 10+
3. **Encoding notes**: dashed-circle null note, "Ring brightness = recency · brighter = 2025–26"

---

## P1 backlog (document — do not implement yet)

### White ring for cluster members

102 records (18%) have a named `location_cluster_id`: croydon-centre (36), stratford-complex (19), oxford-circus (13), woolwich (10), wembley-area (7), brixton (7). A white outer ring would signal "recurring surveillance zone" — the same corner of a high street, year after year.

Implementation: `color: '#ffffff'`, `weight: 2.5` for records with non-null `location_cluster_id`. New legend item required.

Deferred: introduces a 5th stroke-colour variant; needs legend space and copy; low risk of misreading but adds visual complexity. Implement after confirming cluster names are accurate and complete.

### Borough choropleth

Aggregate records by borough, compute relative density, apply fill intensity to borough boundaries. Would show at-a-glance which boroughs are most surveilled without requiring per-dot inspection.

Deferred: requires aggregation logic, colour ramp design, potential conflict with dot layer at low zoom.

---

## External evaluation

> Gemini API evaluation was unavailable during this session (daily free-tier quota exhausted after earlier API calls). The analysis above is drawn from direct code inspection, data verification against `met-police-lfr.json`, and multi-perspective design review conducted prior to implementation.
>
> The three evaluation questions posed were: (Q1) artistic language and aesthetic coherence; (Q2) new-visitor UX and self-description gaps; (Q3) perceptual risks of the radius=arrests + stroke-opacity=year encoding. These questions are addressed substantively in the sections above under "Visual encoding rationale" and "P0.6 — Title bar self-description."

---

*Generated 2026-05-28 · ALHFRS project · `map-embed.html` P0 visual fixes*
