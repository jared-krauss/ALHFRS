# ALHFRS Map Rebuild — Developer Handoff (MapLibre GL JS)

> **Purpose:** a single, self-contained brief from which a developer — or a future Claude Code
> session with **zero prior conversation context** — can execute the ALHFRS map rebuild on MapLibre
> GL JS. If you are picking this up cold, read this whole file first; you should not need any other
> document to start, though `_review/MAP-FEEDBACK.md` (Jared's raw feedback) and
> `_review/MAP-RESEARCH.md` (the full tool research) are the source material behind every choice here.
>
> **Tone note:** the project owner (Jared) is a non-technical creative. This handoff is written for a
> *builder* so it is more technical than other `_review/` docs — but explanations of *why* should
> stay plain when surfaced back to Jared.

---

## 0. What this project is (one paragraph)

**ALHFRS — "A London History of Facial Recognition Systems"** is a multi-year documentary-art and
data-visualisation project by Jared Krauss. It maps facial-recognition deployments across London
(Metropolitan Police live facial recognition, British Transport Police, private retail operators,
and retrospective FR incidents) and critically examines their legal basis and accountability gaps.
The current public-facing artefact is a **single self-contained web page, `map-embed.html`, built on
the Leaflet mapping library**, plotting ~640+ deployment points over a map of London. This handoff
covers **rebuilding that map on MapLibre GL JS** with a set of upgrades.

---

## 1. The goal

Replace the current Leaflet map with a **from-scratch MapLibre GL JS build** that:

1. Renders smoothly and responsively on phone (portrait **and** landscape), tablet, and desktop,
   across browsers — no overlapping text, no "half-height map until you rotate" bug.
2. Reads in **clearly as a map of London** the instant it loads (a "spotlight on London" effect that
   dims everything outside Greater London).
3. Tells operators apart by **shape** (not colour alone), with room for future sub-type variants.
4. Lets a visitor **click a deployment to open a rich detail panel** (deployment facts + source link
   + related news now; empty-but-wired slots for Jared's photos, community submissions, and a
   Gaussian-splat embed later).
5. Offers an **optional looping time animation** (off by default) where dots **accumulate** over time.
6. Fixes the accumulated UX problems from the current map (crowded bottom strip, oversized
   non-collapsible legend, confusing legend glyphs, "stuck highlight" filter buttons, news-panel
   layering bug, too-zoomed-out default, weak visual hierarchy, ineffective "data-quality" and
   "ring-brightness = recency" treatments).

This is the **core map** only. Broader data-visualisation ideas (`_review/DATAVIZ-IDEAS.md`) are a
**separate later track** and are explicitly out of scope here.

---

## 2. Locked decisions (from Jared, 2026-06-23) — do not relitigate

These are settled. Build to them.

1. **Engine: MapLibre GL JS — a from-scratch rebuild — NOT the current Leaflet engine.**
   - *Honest record:* the assistant's evidence-based recommendation was actually to **stay on
     Leaflet** — every current want is achievable there with free add-ons, at lower risk and cost.
     Jared deliberately chose MapLibre anyway, prioritising the **long-term GPU/3D foundation**
     (future 3D "space-time cube" data-viz, smooth GPU zoom, polish) over lower upfront cost. This is
     an **informed override, not a mistake.** Build MapLibre; don't re-pitch Leaflet.
2. **Data-quality** (`confirmed` / `approximate` / `unverified`): **REMOVE it from the always-on
   legend.** Show a record's confidence **only inside the click-details panel.**
3. **Click-details panel:** build the **frame now** — deployment facts + source link + related news —
   with **clearly-marked empty slots** for Jared's photos, community submissions, and a Gaussian-splat
   embed to fill later.
4. **Time animation:** dots **ACCUMULATE** over time (cumulative, not a moving window); **play/stop**;
   **off by default**; **loops**. Data currently starts **2020** (earliest records Feb 2020), so the
   animation **begins where the data begins** — note this; it is not 2016.
5. **Scope:** **CORE MAP first.** Data-viz ideas are a separate later track.
6. **Splat embed:** prototype via the **free Luma iframe**; own it long-term via **free self-hosted
   SuperSplat export** (fits Jared's existing COLMAP / Gaussian-splat pipeline on his GTX 1080).

---

## 3. De-risking approach (read before touching anything)

The rebuild is the highest-risk item on the list (a full engine swap). Contain the risk:

- **The data carries over unchanged.** The deployment JSON (`data/deployments/*.json`, schema v1.2)
  is engine-independent. MapLibre consumes GeoJSON / point data the same conceptual way Leaflet does.
  **Do not re-model or re-validate the data as part of this** — reuse it as-is. Run
  `python scripts/validate-dataset.py <file>` only if you *change* a data file (you shouldn't need to).
- **The design system carries over unchanged.** Layout, visual hierarchy, the operator-shape scheme,
  colour palette, typography, and copy are all engine-independent. They are the expensive part and are
  defined in Phase 0 **before** any MapLibre code, so the work is not wasted whatever happens.
- **The current Leaflet map stays live.** Do **not** delete or break `map-embed.html`. It remains the
  published map until the new MapLibre build is approved. The new build lives alongside it (e.g.
  `map-embed-maplibre.html` or a `map-next/` folder — builder's choice, but keep it separate).
- **Build in the sandbox / worktree.** All work happens in the git worktree branch. **Nothing merges
  to `main`** until Jared reviews and approves. Do not push, do not merge on his behalf.
- **Commit checkpoints as you go** (`git add -A && git commit`) so a crash never loses work.
- **Reversible by construction:** because the old map is untouched, "rolling back" is just "keep
  serving `map-embed.html`." There is no destructive step until Jared chooses to swap.

---

## 4. The phased plan

### Phase 0 — Design foundations (engine-independent; do this FIRST)

Nothing here is MapLibre-specific; it's the design contract the build implements. Doing it first means
the expensive thinking survives regardless of engine, and the MapLibre phases become mechanical.

- **Operator → shape scheme.** Each operator gets a distinct **shape** (e.g. Met Police = circle,
  BTP = triangle, private retail = square — final shapes are Jared's call). Reserve **future
  variants** for sub-types: a slightly adjusted shape for permanent/semi-permanent cameras, and a
  variant for retrospective FR (RFR). Rule: **shape = operator, variant = sub-type**, and keep the
  variant to **one** visual dimension (e.g. solid fill vs hollow outline) so it stays legible.
  *This resolves the current legend-vs-map mismatch:* the legend currently shows shapes but every map
  marker is a circle. Jared **likes** the shapes — so the fix is to make the **actual markers** use
  them (feedback #8 / #17), not to drop them.
- **Colour palette + typography.** Lock these (the current build uses a "poppy pastel halation"
  aesthetic — carry the intent forward, refine as Jared's eye dictates).
- **Legend redesign.** Collapsible; **data-quality removed** from it (moves into click-details, per
  locked decision 2); **drop the "ring brightness = recency" idea entirely** (feedback #9, #10 — it
  was judged ineffective).
- **UX hierarchy + grid.** Establish real visual hierarchy and a graphic-design grid (with deliberate
  grid-breaking) to guide the eye (feedback #12, #13). Assistant proposes; Jared's eye refines.
- **Prominent intro / onboarding copy.** Decide the wording and placement of the in-map explanation
  of what the dots mean (feedback #5, #19), and whether there's also a one-time welcome card.

### Phase 1 — Core map rebuilt on MapLibre (parity + the basics fixed)

- **Base map + data load.** Stand up MapLibre with a London base style (a free/open vector tile style
  is fine; no API key is required for the MapLibre library itself). Load the same deployment data.
- **Clustering.** MapLibre has **native clustering** on GeoJSON sources (`cluster: true` on the
  source) — no plugin needed. (On Leaflet this was the `leaflet.markercluster` plugin.)
- **Operator shapes on the actual markers.** In MapLibre this is a **symbol layer**: register each
  shape as an image via `map.addImage()` and **data-drive** which image each point uses from the
  `operator` property (`icon-image` expression). This is idiomatic, GPU-fast MapLibre. *(Leaflet
  equivalent would have been the free `Leaflet.SvgShapeMarkers` plugin or hand-rolled `L.divIcon`
  SVG — cheaper, but we're on MapLibre by choice.)*
- **Responsive + cross-browser** (feedback #1, #15): size the map container with modern CSS viewport
  units (**`svh`/`dvh`**, with a `100vh` fallback line first for old browsers) so it fills exactly the
  visible screen and doesn't hide under the mobile address bar; add a **landscape** media query.
  MapLibre re-renders on container resize but **call `map.resize()` on the browser `resize` and
  `orientationchange` events** to be safe — this is MapLibre's equivalent of Leaflet's
  `invalidateSize()` and is the single most important fix for "looks wrong until I rotate." Ensure the
  `<meta name="viewport">` tag is present.
- **Overlapping labels.** This is the one feature MapLibre genuinely does **better natively** than
  Leaflet: its symbol layer **automatically hides colliding labels** for you (control with
  `text-allow-overlap` / `icon-allow-overlap` left at their default `false`, plus `symbol-sort-key`
  to choose which labels win). *(On Leaflet this needed the free `Leaflet.LabelTextCollision` plugin.)*
- **Spotlight on London** (feedback #20) — see §5 below for the exact MapLibre method (this is where
  MapLibre is *weaker* than Leaflet, so it's spelled out separately).
- **Prominent intro** drawing the eye to what the dots mean (feedback #5, #19); **better default
  zoom/centre** so London fills the frame instead of sitting tiny (feedback #5).
- **Bottom strip re-spaced** (feedback #7); **legend collapsible** (feedback #3); **filter buttons
  with a stark ON state that clears instantly** (feedback #2 — rebuilt fresh so the old "stuck
  highlight" can't recur; see the CSS note in §6); **menu/news layering correct** (feedback #4).

### Phase 2 — Click-details panel (build the frame, fill over time) (feedback #18)

- **Pattern:** clicking a deployment shows a **small popup teaser** (name, date, operator + a "View
  details" affordance) → opens a **side detail panel** with the rich content. Don't cram rich content
  into the popup itself — it obscures the map and reads badly on mobile.
- **In MapLibre** the panel is **your own HTML/CSS element**, shown/hidden on the map's `click` event
  for the deployment layer (MapLibre's click gives you the clicked feature's properties directly).
  *(Leaflet equivalent would have been the free `leaflet-sidebar-v2` plugin; on MapLibre the sidebar
  is hand-built, which is a little more work but fully under your control.)*
- **Build now:** deployment **facts** (from the record), **source link** (`source_url`), and
  **related news** (match against `data/news/`). **Show the record's `data_quality` here** — this is
  the *only* place confidence appears now (locked decision 2).
- **Wire-but-dormant slots, clearly marked empty:** Jared's own photos; community submissions
  (ties into the deferred `data/community/` moderation workflow — out of scope to build here);
  and a **Gaussian-splat embed** (see §4 Phase-2 splat note below). Each slot should be visibly a
  placeholder ("photo coming", etc.), not hidden, so Jared can see where content will land.
- **Splat embed mechanics:** the embed is just HTML inside the panel, engine-independent.
  **Prototype** with a **Luma AI free `<iframe>`** (capture on phone → Luma hosts → paste one line).
  **Own it long-term** with **SuperSplat's free, MIT, self-hosted single-file HTML export**, which
  fits Jared's COLMAP pipeline and keeps the asset under his control. Social embeds and photos are
  ordinary `<img>`/`<video>`/embed HTML — no special map tooling.

### Phase 3 — Time animation (play/stop, off by default, cumulative, loops) (feedback #6)

- **Behaviour (locked decision 4):** a **play** button steps a playhead through time from the data's
  start to its end; dots **accumulate** (each deployment appears on its `date_start` and stays
  visible), ending on the full picture; then it **loops**. **Off by default** — nothing animates until
  the visitor presses play. A **stop** button halts and (builder's choice) resets or freezes.
- **In MapLibre** this is naturally a **filter expression on the symbol layer** driven by an animated
  "current date" variable: on each animation frame, advance the date and set a layer filter like
  "`date_start` <= currentDate". Because it's a GPU filter, it's smooth even with hundreds of points.
  *(On Leaflet this was the free `Leaflet.timeline` plugin, which reads per-point dates and has a
  built-in play button — cheaper out of the box; on MapLibre you wire the playhead yourself, but you
  get GPU-smooth transitions.)*
- **Data-start note:** the animation **starts at 2020** (earliest records are Feb 2020), **not 2016.**
  If Jared later adds pre-2020 records, extend the timeline start backwards — no code change beyond the
  date bounds.

### Future track (noted, NOT this round)

Out of scope here; listed so nobody scope-creeps into them:
- Shape **variants** for permanent cameras and RFR (the scheme reserves room; don't build the variant
  rendering yet).
- The **community-submission** capture + moderation workflow (`data/community/`).
- Actual **splat capture** (the embed slot is wired; captures come later).
- The separate **data-visualisation "other windows / maps"** track (`_review/DATAVIZ-IDEAS.md`),
  including any future **3D "space-time cube"** — this is the long-term payoff Jared chose MapLibre for,
  but it is explicitly **not** built in this round.

---

## 5. The "spotlight on London" effect on MapLibre — spell-out (IMPORTANT)

This is the one place where choosing MapLibre **costs us** built-in support, so it needs care.

- **The effect:** on load, everything **outside Greater London is dimmed** so the eye is drawn to the
  city and the viewer instantly understands the map is *about* London. Cartographers call this a
  **mask** / **inverted-polygon** overlay: you cut a London-shaped hole in a dark, semi-transparent
  layer that covers the rest of the world.
- **The raw material already exists:** `map/data/london-boroughs.geojson` is the outline of Greater
  London. Build the mask from that exact shape. For a clean edge, use the **dissolved outer boundary**
  of London rather than all 33 separate borough polygons.
- **The catch:** **Leaflet has a purpose-built plugin for this (`Leaflet.Mask`) — MapLibre does NOT.**
  A built-in mask is a long-standing, unshipped MapLibre community request. So on MapLibre you build
  the mask yourself. There is no advantage to MapLibre here; if anything it's marginally more work.
- **The MapLibre method (do this):**
  1. Use **Turf.js** (`turf.mask()`, free/MIT) to turn the London polygon into an **inverted polygon**
     = "the whole world with a London-shaped hole." (`turf.mask()` does this in one call; historically
     it was a world-rectangle minus London via `turf.difference`.)
  2. Add that inverted polygon to the map as a normal MapLibre **`fill` layer**, filled with a
     semi-transparent dark / desaturated colour. That instantly dims everything outside London. You
     control colour and opacity, and you can animate the opacity on load for a dim-in.
  3. Make sure the fill layer **doesn't intercept clicks** meant for the markers (place it below the
     symbol layer in the layer order, or leave it non-interactive) so deployment clicks still work.
- **Dim, not blur.** A true *blur* of the underlying tiles is fiddly on either engine for little gain.
  Use a semi-opaque **dim**; if you want a touch of blur, a CSS `backdrop-filter: blur()` on an overlay
  is the only easy route, and only in browsers that support it. **Recommend dim.**

---

## 6. Notes on specific bug fixes (no library needed)

- **"Stuck highlight" filter buttons** (feedback #2): the current bug is the classic mobile
  **"sticky hover/focus"** — a `:hover`/`:focus` style sticks after tapping until you tap elsewhere.
  Fix in CSS only: gate hover styling behind `@media (hover: hover)` so it only applies to real
  pointers, and drive the toggle's lit "ON" look from an **explicit active-state class** your JS adds
  and removes — **never** from `:focus`. Make the ON colour **starker** and have it clear **instantly**
  on toggle-off. Building fresh on MapLibre means the old stuck state can't carry over, but apply this
  rule from the start.
- **News-panel layering bug** (feedback #4): a z-index / stacking-context issue. Give the panel
  `position` + a high enough `z-index`, and check no parent (with `transform`, `opacity<1`, `filter`,
  or `will-change`) is trapping it in its own stacking context. Either render the news panel above the
  menu, or close the menu when News opens.

---

## 7. Feature → tool / approach map (MapLibre-native vs plugin vs "Leaflet would've sufficed")

| Feature (feedback #) | On MapLibre (the chosen path) | Native or extra? | Cheaper Leaflet alt we passed up |
|---|---|---|---|
| Many points, smooth render (#1) | GPU vector rendering | **Native** | (Leaflet was fine at this scale; CSS `content-visibility` on panels was the cheap win) |
| Overlapping labels hidden (#1, #15) | Symbol layer auto-collision (`*-allow-overlap: false`, `symbol-sort-key`) | **Native — genuine MapLibre win** | free `Leaflet.LabelTextCollision` plugin |
| Clustering | GeoJSON source `cluster: true` | **Native** | `leaflet.markercluster` (already in use) |
| Responsive sizing (#1, #15) | CSS `svh`/`dvh` + `map.resize()` on resize/rotate | CSS + a few JS lines | identical approach on Leaflet (`invalidateSize()`) |
| Operator **shapes** on markers (#8, #17) | Symbol layer, `addImage()` + data-driven `icon-image` | **Native (data-driven)** | free `Leaflet.SvgShapeMarkers` or `L.divIcon` SVG |
| **Spotlight on London** (#20) | Turf.js inverted polygon → MapLibre `fill` layer | **Plugin (Turf.js) + hand-wiring; MapLibre has NO built-in mask** | free `Leaflet.Mask` plugin — **would have been easier** |
| **Click-details panel** (#18) | Own HTML panel toggled on the layer `click` event | Hand-built | free `leaflet-sidebar-v2` plugin |
| **Time animation** (#6) | Animated date variable → symbol-layer filter expression | Hand-wired (GPU-smooth) | free `Leaflet.timeline` plugin (play button built in) |
| Gaussian-splat embed | Luma `<iframe>` → SuperSplat self-hosted HTML export | Engine-independent HTML | identical on Leaflet |
| Collapsible legend (#3) | Native `<details>` element or hand-rolled CSS toggle | Built-in browser feature | identical on Leaflet |
| Stuck-highlight + z-index bugs (#2, #4) | CSS only (`@media (hover:hover)` + active class; `position`+`z-index`) | CSS fix | identical on Leaflet |
| Onboarding / welcome (#5, #19) | Native `<dialog>` welcome card; Driver.js (MIT) if a guided tour is wanted | Built-in / small add-on | identical on Leaflet (avoid intro.js & Shepherd.js — AGPL) |

**Reading this table:** most rows say a free Leaflet plugin would have sufficed. That is the honest
cost of the MapLibre decision, and it's fine — Jared chose MapLibre for the long game, not because
these features demanded it. The **two real MapLibre wins** are (a) automatic label-collision hiding
and (b) the GPU foundation for future 3D. The **one real MapLibre cost** is the spotlight mask (§5).

---

## 8. Verification (before any swap to live)

- **Test on Jared's real phone over Tailscale** (the PC serves the map; the phone reaches it via
  Tailscale). Check **portrait AND landscape** — the landscape (short, wide viewport) case is where
  responsive layouts most often break. You cannot trust a desktop emulator for mobile map behaviour;
  real-device testing on Jared's iPhone is the standard here.
- **Test on desktop** (and ideally a second browser) for cross-browser sanity.
- **Specifically re-check every feedback item** that was a bug: no overlapping text at any size; map
  fills the screen correctly after rotation; filter ON-state is stark and clears instantly; news panel
  sits above the menu; default view reads as London; legend collapses; bottom strip has breathing room.
- For a solo art project, **own-device testing is enough** — don't pay for a cross-device testing
  service (LambdaTest/BrowserStack) unless wide device coverage ever becomes a real requirement.
- **Nothing merges to `main` until Jared has seen it and approved.** Keep `map-embed.html` live until
  then.

---

## 9. Open items / things needing Jared's judgement

1. **Is "Pretext" still relevant given MapLibre?** Jared named the **Pretext** library
   (github.com/chenglou/pretext, free/MIT) as the "browser front-engine" text technique he half-
   remembered. Research confirmed it's real and he remembered it correctly — **but it's a
   text-*measurement* tool, not a map renderer and not a GPU graphics engine.** It does **not** fix
   overlapping map labels (MapLibre's symbol layer does that natively). Pretext's only possible use
   here is making a very text-heavy panel re-flow smoothly. **Recommendation:** keep Pretext in the
   back pocket for the detail/news panels if they ever feel janky; do **not** treat it as a map
   dependency. Likely moot for the map itself. Flagged for Jared only because he asked about it.
2. **Data start: 2020, not 2016.** The animation and any "history" framing begin at **2020** (earliest
   records Feb 2020). If Jared has or plans **pre-2020** records, say so and the timeline extends back.
   Otherwise all "since 2020" copy is correct as-is.
3. **Shape-variant future scope.** The shape scheme **reserves** room for sub-type variants (permanent
   vs mobile cameras; RFR), but those variants are **not built this round.** Confirm Jared's happy that
   the first build ships with **one shape per operator** and variants come later.
4. **Final shapes/colours/copy** are Phase-0 design decisions that want Jared's eye before Phase-1
   coding locks them in.

If anything else blocks progress mid-build, stop that part and write the problem + simplest options
into `_review/HANDOFF-BLOCKERS.md` for Jared, rather than guessing.

---

## 10. Quick reference — where things live

- **Current live map:** `map-embed.html` (single-file Leaflet build) — **keep serving this until swap.**
- **Older modular Leaflet build:** `map/index.html` + `map/js/` — not the active build.
- **Deployment data (carries over unchanged):** `data/deployments/*.json` (schema v1.2).
- **London outline for the spotlight mask:** `map/data/london-boroughs.geojson`.
- **News for the detail panel:** `data/news/gmail-research-threads.json`.
- **Validator (only if you touch data):** `python scripts/validate-dataset.py <file>`.
- **Serve locally:** `python -m http.server 8741` (or `serve.ps1` / `serve.bat`) — must be **HTTP**,
  not `file://`, or `fetch()` calls fail. Map auto-starts on login via the "ALHFRS Map Server" task.
- **Source material behind this plan:** `_review/MAP-FEEDBACK.md`, `_review/MAP-RESEARCH.md`,
  `_review/MAP-UPGRADE-PLAN.md`.
