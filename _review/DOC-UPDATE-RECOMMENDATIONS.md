# Doc-update recommendations (for Jared to approve — NOT yet applied)

> **What this is:** proposed, ready-to-paste edits to the three root project docs —
> `DECISIONS.md`, `CLAUDE.md`, `README.md` — to reflect the map-upgrade direction and the data work.
> **Nothing here has been applied.** All three files exist and were left untouched on purpose. Approve,
> tweak, or reject each item.
>
> **The big timing rule:** the MapLibre rebuild and most of the recent data work **live in the
> sandbox / worktree and are NOT merged into `main` yet.** Docs on `main` must not describe unmerged
> work as if it's done. So most edits below are marked **"after the sandbox merge."** Only the
> decision-log entries are safe to add **now**, because a *decision* is true the moment it's made,
> regardless of whether the code has shipped.
>
> **Convention being followed** (from the D:\Dev docs protocol): **lean CLAUDE.md = operating manual;
> details live in README; decisions live in DECISIONS.md.** Decisions never go in CLAUDE.md (only a
> pointer). DECISIONS.md entries use the exact format in that file's header, newest-at-top of the
> current month.

---

## 1. `DECISIONS.md` — APPLY NOW (two new entries)

These record decisions already made, so they're true now and safe to add before any merge.

**Where:** the file currently has a `## 2026-05` section. Add a **new `## 2026-06` section ABOVE it**
(newest month on top), containing both entries below. The format matches the file's header exactly:
`- **<slug>** [tags] (YYYY-MM-DD): chose X over Y because <root cause>.`

Ready-to-paste block (drop it in directly under the file's intro block, above `## 2026-05`):

```markdown
## 2026-06

- **map-engine-maplibre** [ALHFRS] (2026-06-23): chose a from-scratch MapLibre GL JS rebuild over upgrading the existing Leaflet map, because Jared prioritised a long-term GPU/3D foundation (future 3D data-viz, smoother/polished rendering) over the lower-risk path — an informed override; the assistant's evidence-based recommendation was to stay on Leaflet, where every current want was achievable with free add-ons.
- **data-quality-into-detail-panel** [ALHFRS] (2026-06-23): chose to show a record's data-quality only inside the click-details panel over keeping it in the always-on legend, because the legend treatment (and the "ring brightness = recency" cue) was judged confusing and ineffective, and confidence reads better in context.
```

> **Note on the 40-word cap:** the `map-engine-maplibre` entry runs slightly long because the honest
> "recommendation vs decision" nuance matters here. If you'd rather keep strictly to the cap, the
> shorter form is: *"chose a from-scratch MapLibre GL JS rebuild over upgrading the existing Leaflet
> map, because Jared prioritised a long-term GPU/3D foundation over the lower-risk Leaflet path
> (informed override — the recommendation was to stay on Leaflet)."* — and the full rationale already
> lives in `_review/MAP-UPGRADE-PLAN.md` and `_review/MAP-UPGRADE-HANDOFF.md`.

---

## 2. `CLAUDE.md` — APPLY AFTER THE SANDBOX MERGE (with one small exception, below)

CLAUDE.md is auto-loaded into every Claude session, so it must describe the **live** state, not
sandbox plans. Today it describes the **live Leaflet build** — which is still accurate, because the
MapLibre map isn't merged. **Do not rewrite CLAUDE.md to say the map is MapLibre until the rebuild is
actually merged to `main`.** Below: what's already stale (independent of the rebuild), and what
changes only after merge.

### 2a. Optional small fix — could apply NOW (independent of the rebuild)

There's an existing **internal inconsistency** in CLAUDE.md unrelated to MapLibre: the **directory
map** still says `met-police-lfr.json … 8 Met Police LFR deployments`, while the **Current state**
block in the same file (and README) says **580 records**. That "8" is stale regardless of any map
work.

- **When:** now (it's just correcting an existing error, not describing unmerged work).
- **Change:** in the directory-map code block, update the `met-police-lfr.json` line from
  `8 Met Police LFR deployments (2020–2026)` to match the real count, e.g.
  `Met Police LFR deployments (2020–2026) — see Current state for live count`.
  (Pointing to the Current-state count avoids having two numbers to keep in sync.)
- **Caution:** confirm the true live-on-`main` count before editing — don't paste in the sandbox count
  if the sandbox data isn't merged. Use whatever `met-police-lfr.json` on `main` actually contains.

### 2b. Map sections — APPLY AFTER MERGE

When the MapLibre build is merged and becomes the live map, update these CLAUDE.md spots. Until then,
leave them describing Leaflet.

- **"What this project is" → Primary output line.** Currently: *"An interactive website with a Leaflet
  deployment map…"*. After merge, change "Leaflet deployment map" → **"MapLibre GL JS deployment map"**.
- **"Current state" → Map bullet.** Currently: *"Map: Live Leaflet map with marker clustering
  (`leaflet.markercluster`), year-filter timeline strip, 4 layers"*. After merge, replace with a lean
  one-liner pointing to README for detail, e.g.:
  > Map: live **MapLibre GL JS** build — operator-shape markers, native clustering, collapsible legend,
  > click-details panel, optional time animation. Full feature list in [README.md](README.md).
- **"Running the map" → "Two map builds exist".** After merge this note should describe the **new**
  build as active and the Leaflet files as superseded/archived. Keep it lean — exact wording depends on
  how the files are finally named/placed (e.g. whether `map-embed.html` is replaced or retired).
- **Keep it lean.** Per the convention, don't pile MapLibre implementation detail into CLAUDE.md.
  CLAUDE.md says *what's live and how to run it*; the feature detail and rebuild rationale belong in
  **README.md** and **DECISIONS.md** (the latter already covered in §1).
- **Decisions pointer stays as-is.** CLAUDE.md already points to `DECISIONS.md` and must **not** gain a
  decision entry — the two new decisions go only in DECISIONS.md (§1).

> **What NOT to do now:** do not edit CLAUDE.md's map sections to describe the MapLibre map while it's
> still in the sandbox. That would make the auto-loaded operating manual lie about the live system.

---

## 3. `README.md` — APPLY AFTER THE SANDBOX MERGE

README is the human-readable overview and is where map-feature detail belongs. After the rebuild
merges, update the map-related parts. Until then, README correctly describes the Leaflet map.

- **Top "Primary output" paragraph.** Currently: *"An interactive website with a London deployment
  map…"* — this is engine-neutral and **fine as-is**; no change needed (it doesn't name Leaflet).
- **Project-structure block.** The `map/` line currently reads
  `map/ … Leaflet map — marker clustering + year-filter timeline strip`. After merge, update to
  reflect the MapLibre build and the new features, e.g.:
  > `map/ … MapLibre GL JS map — operator-shape markers, native clustering, "spotlight on London"
  > mask, collapsible legend, click-details panel, optional time animation`
  and update the `map-embed.html` line to point at whatever the new active file is.
- **"Map layers" table.** Layer 2 row currently: *"Met Police LFR deployments … Live (580 records,
  2020–2026)"*. After merge, update the record count to the real merged count, and (if the rebuild
  changes how layers toggle) reconcile the table with the new build.
- **Consider a short "Map features" subsection** after merge, listing what the upgrade delivered
  (responsive/cross-browser, spotlight-on-London, operator shapes, click-details panel with source +
  news + reserved photo/community/splat slots, optional cumulative time animation from 2020). This is
  the natural home for the detail that should stay **out** of the lean CLAUDE.md.
- **Splat integration section.** Already says "planned" — fine. After the detail panel ships with a
  wired-but-dormant splat slot, you may add one line noting the panel has a splat embed slot
  (Luma iframe prototype → SuperSplat self-hosted long-term). Gate on merge.

---

## Summary table — what to apply when

| File | Change | When |
|---|---|---|
| `DECISIONS.md` | Add `## 2026-06` section with `map-engine-maplibre` + `data-quality-into-detail-panel` entries | **Now** |
| `CLAUDE.md` | Fix stale "8 Met Police LFR deployments" in directory map (existing error) | **Now** (verify live count first) |
| `CLAUDE.md` | Map sections: Leaflet → MapLibre, lean wording, point detail to README | **After merge** |
| `README.md` | Project-structure + Map-layers + optional "Map features" section reflecting the rebuild | **After merge** |
| `README.md` | Splat slot note in splat section | **After merge** |

**All three files exist** — so these are recommendations only and (per the task) none has been edited.
If any had been missing, the recommendation would have been to create it per the lean convention,
**after Jared's approval** — not pre-emptively.
