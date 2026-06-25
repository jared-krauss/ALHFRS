# Progress Log

This run works in an isolated copy of the project. Nothing here touches the live project
until Jared reviews and approves.

> Note: an earlier aborted run left a note here about missing files and a "169 vs 64"
> discrepancy. Those were stale-copy issues and are now resolved (both staging files are
> present in this copy; the 64-new-records figure is confirmed correct). This log supersedes it.

## Workstream A — Data cleanup & verification — DONE
- Confirmed both staging files (garbett-2024.json, gemini-2021-extraction.json) are present.
- Found the handed-over garbett-2024.json (169 records) was an already-merged copy — all 169 IDs
  already in the dataset. Went back to the source Excel and computed the 64 genuinely-new 2024
  records (matches the corrected brief). Built, geocoded, sanity-checked, merged. Met file: 580 -> 644.
- Verified all 5 Gemini 2021 records one by one: merged 0 (2 aggregates, 1 statistical
  misattribution, 2 already-present duplicates). All rejections explained in DATA-CHANGES.md.
- Mapped 221 internal source-type labels to the official `FOI_disclosure` enum (kept originals in
  a new source_subtype field). Cleared 221 warnings.
- Tagged 110 legitimate repeat-deployment records into 10 location clusters (no deletions).
- Backfilled 10 boroughs + 16 wards where unambiguous; left 38 ambiguous wards blank.
- Resolved news redirects: 8 of 9 already done; news-015 unresolvable (broken stub) — annotated honestly.
- Validator (Met file): warnings 940 -> 887, errors 0 -> 0. Other files clean.
- Deliverable: _review/DATA-CHANGES.md. COMMITTED.

## Workstream B — Map accessibility & UI fixes — DONE (verified in browser)
Applied to map-embed.html (active build) and map/index.html (older modular build):
- Keyboard focus: added a visible amber :focus-visible outline to every interactive control
  (buttons, chips, links, timeline columns, borough select) — none existed before.
- ARIA: layer-panel toggle now has aria-expanded (syncs open/closed) + aria-controls;
  filter rows have role="group" + aria-label; each year/month/operator chip has a descriptive
  per-chip aria-label so screen readers announce what it does.
- Non-colour cue: added a shape glyph (circle = Met, triangle = BTP, square = Private) next to the
  colour coding in both the legend and the operator chips/layer buttons — colour-blind safe.
- Text size: bumped all 9px labels (filter labels, section labels, legend intro, timeline labels,
  news tags, title subtitle) up to 12px.
- Timeline: added a visible "Click a year to filter" hint next to the year strip.
- Community button: added a tooltip explaining it is not yet available (also News button on the
  older build).
- Verification: served the worktree on a local port and loaded both files in a real browser.
  Confirmed map renders (651 deployments / 684 markers on the active build), year filter works
  (684 -> 280 markers for 2024, reset restores 684), aria-pressed toggles, glyphs render, tooltips
  present, focus-visible rule resolves, and NO console errors on either build. JS also passed a
  node --check syntax pass. (Screenshot tool timed out on the WebGL splat iframe, but DOM/behaviour
  checks all passed.)
- Note: could not create .claude/launch.json for the preview tool (Write denied), so verification
  ran against a manually-started python http.server on port 8742 — verified the same files.
- Deliverable: changes in map-embed.html + map/index.html; details here. COMMITTED.

## Workstream C — Data visualization research — DONE
- Web-researched geographic+temporal viz techniques from epidemiology (space-time cube, STKDE),
  criminology (hotspot KDE, near-repeat victimization), and ecology (home-range/utilization
  distribution, origin-destination flow maps).
- Wrote 8 ideas, each with a plain-English description, the data question it answers, and pros/cons,
  plus a suggested priority order and framing cautions (the surveillance subject means the
  disease/wildlife metaphors need care). Recommendations only — nothing implemented.
- Deliverable: _review/DATAVIZ-IDEAS.md. COMMITTED.

## Workstream D — Photo shot list — DONE
- Ranked physical locations by deployment frequency across all 3 deployment files, grouping by
  coordinate + location_cluster_id + name (≈200m agglomeration to merge the many spelling variants
  of the same spot).
- Wrote the top 20 with most-specific real-world detail from the data (street/landmark/junction),
  frequency count and date range. Flagged borough-only/vague spots as "needs Jared's local knowledge
  to pinpoint." No composition/framing advice (Jared's creative call). Sorted most-deployed first.
- Deliverable: _review/PHOTO-SHOT-LIST.md. COMMITTED.

## Final status
- A — Data cleanup & verification: DONE  -> _review/DATA-CHANGES.md
- B — Map accessibility & UI fixes:  DONE (verified in browser) -> map-embed.html, map/index.html
- C — Data visualization research:   DONE  -> _review/DATAVIZ-IDEAS.md
- D — Photo shot list:               DONE  -> _review/PHOTO-SHOT-LIST.md
All four workstreams complete. Worktree branch NOT merged to main — that is Jared's decision
after review. Met dataset: 580 -> 644 records; validator warnings 940 -> 887, 0 errors.
