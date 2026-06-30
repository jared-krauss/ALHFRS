# Map Upgrade — Jared's Feedback Log

> Running collection of Jared's feedback on the ALHFRS map, gathered across several messages.
> **Status: COLLECTING** — do not generate the upgrade plan until Jared says "I'm done."
> When he does: ask clarifying / vision-refining questions FIRST, then plan. Prefer existing
> free/open-source tools over custom code. Keep all explanations non-technical.

---

## Batch 1 — 2026-06-23 ("quick off top of my mind")

1. **Mobile responsiveness is broken.** The map doesn't dynamically adapt on mobile in either
   portrait or landscape; text overlaps and eats up screen real estate.
   - Jared's suggested fix (needs interpreting): *"the new typescript technique that uses the web
     browser front engine to reduce cost of computing text and graphic layouts."* → likely means
     GPU/WebGL-style rendering done by the browser (e.g. MapLibre GL / deck.gl) rather than the
     current Leaflet DOM rendering. CONFIRM with Jared / research existing options.
   - Category: responsive layout + possible rendering-engine change.

2. **Year-filter button "stuck highlight" bug.** Clicking a year greys it (selected). Clicking it
   again turns the data filter OFF, but the grey highlight stays — you have to click another button
   or a non-interactive area to clear it. Wants: a **starker colour when a filter is ON**, and the
   highlight should **disappear immediately when OFF**. (Classic focus-vs-active-state bug.)
   - Category: bug + filter UX.

3. **Legend takes too much space; no way to minimize it.** Useful, but needs a collapse/minimize.
   - Category: UX / controls.

4. **Layering bug:** open the hamburger menu (top-right) → click News → the news panel loads
   *behind* the menu dropdown. Should appear in front (or the menu should close first).
   - Category: bug (stacking / z-index).

5. **Default view too zoomed out + no in-map introduction.** London view is too far out, and there
   isn't enough explanation *within the map itself* of what's being shown.
   - Category: content / onboarding + default zoom.

6. **Looping animation, off by default.** Wants an optional looping time animation with a play/stop
   button — not running until someone presses play.
   - Category: feature (time playback).

### Screenshots
- (none yet — Jared said screenshots are coming in later messages)

### Open questions to resolve before planning
- Q1 (item 1): what exactly is the "typescript / browser front engine" technique? Does Jared have a
  link or name, or is it a half-remembered idea? My read: GPU/WebGL map rendering.
- Q2 (item 6): what should the animation *show*? Most likely deployments appearing over time
  (2020→2026) as a time-lapse of surveillance spreading across London — confirm.

---

## Batch 2 — 2026-06-23 (screenshot IMG_8500 + design critique)

**Screenshot (IMG_8500, phone portrait):** pink dots over London; a large legend panel covering
the centre-left; hamburger top-right; the year row (2020–2026), month row, and the bottom
title/intro block ("A London History of Facial Recognition Systems… 651 deployments… data to May
2026") all crowded together at the bottom. Jared's annotations: **yellow circle** = the whole
too-zoomed-out / crowded London view; **blue circle** = the legend; **cyan circle** = the crowded
bottom strip.

7. **Bottom strip too crowded (cyan).** Year filter + month filter + the bottom title/intro block
   are jammed together and too close. Needs breathing room / spacing / separation.
8. **Legend shape glyphs are confusing (blue).** The legend shows different shapes (●▲■) for the
   operator types, but every marker on the map is just a circle — so the shapes mean nothing and
   confuse. NOTE: those shape glyphs were *added in the earlier accessibility pass* (so colour
   wouldn't be the only cue). Must reconcile: either make the map markers actually use the shapes,
   or drop the shapes from the legend. Pick one.
9. **Data-quality text & how it's conveyed = not useful (blue).** "confirmed · approx · unverified"
   and the current visual treatment are very hard to grasp. Data quality *might* have a place
   (Jared says debatable) — but definitely not this way. Rethink whether/how to show it at all.
10. **"Ring brightness = recency" is faff (blue).** Conveying recency via ring brightness is
    ineffective. Wrong approach — needs a different idea or dropping.
11. **(reconfirms Batch 1)** general text crowding, legend size, too-zoomed-out London view.

### SCOPE CLARIFICATION — important for the plan
- **Fix the BASIC map FIRST** — make it functional and good. The data-viz ideas are "almost for
  different windows / different maps," NOT all crammed into this one map. *Some* data-viz ideas
  could later be folded into the main map, but the basic working map comes first. Jared will give
  feedback on the data-viz ideas separately, later. → The upgrade plan should scope to **core map
  fixes/quality**, and treat the data-viz ideas as a separate later track.

### General / strategic design notes
12. **Weak UX hierarchy** — not enough visual hierarchy to guide and inform the user about what
    they're looking at and how to use it.
13. **Graphic-design grid** — the grid (and deliberate "breaking the grid") design principles
    could be applied much better across the layout.

---

## Batch 3 — 2026-06-23 ("that's all my feedback for now" → DONE; ask questions, then plan)

14. **"Pretext Library"** is what Jared meant earlier re: dynamic text reloading / "browser front
    engine to reduce text & graphic layout cost." IDENTIFY IT (research + ask for a link) — likely a
    text-layout / GPU rendering library; unconfirmed.
15. **Map must load dynamically across different browsers AND screen shapes/orientations**
    (cross-browser + truly responsive). Reinforces the mobile point.
16. **Constraint lifted:** do NOT limit to free/OSS — include ALL tools that could work (paid /
    commercial too). Job = explain the options clearly so Jared can choose well.
17. **Operator shapes: Jared LIKES them.** → Resolve Batch-2 #8 by making the actual MAP markers
    use distinct shapes per operator (not only the legend). **Future scope:** shape *variants* — a
    slightly adjusted Met Police shape for semi-/permanent cameras, and a variant for retrospective
    FR (RFR). So: shape = operator, variant = sub-type.
18. **Click a deployment → rich detail panel** surfacing related data/links:
    - the specific deployment's data + link to its **source**;
    - related **news articles**;
    - **social-media posts / user-submitted photos or videos** (people submit separately; Jared
      curates them into the database);
    - **Jared's own photos** of the area/deployment, and/or a **Gaussian splat** of the area.
19. **Intro text (bottom) should be prominent** — draw the eye to the explanation of the dots/data.
20. **"This is London" framing (yellow circle):** make the background read clearly as London — e.g.
    zoom out a bit and **grey out / blur / defocus everywhere except London** (a spotlight/mask on
    the city) so the viewer instantly knows the area shown.

**STATUS: collection complete.** Next step = ask refining questions, get answers, THEN write the
plan. Plan scope = core map first; data-viz ideas are a separate later track (per Batch 2).
