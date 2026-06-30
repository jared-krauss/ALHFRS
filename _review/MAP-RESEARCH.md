# Map Upgrade Research — Free / Open-Source Tools

> **Purpose:** Find proven, genuinely free/open-source tools to solve specific problems with
> the ALHFRS documentary-art web map (currently a single self-contained `map-embed.html` built
> on **Leaflet**, plotting ~644 facial-recognition deployment points across London).
>
> **Audience:** Non-technical. Everything below is in plain English.
> **Status:** PRELIMINARY — more feedback themes will be appended later. Sections are self-contained.
>
> **Two sizes of change** (this distinction matters more than anything else):
> - **ADD-ON** = a small plugin or snippet bolted onto the existing Leaflet map. Low risk, reversible, keeps everything you have.
> - **REPLACE** = swap Leaflet out for a different map engine. Big rebuild, higher risk, touches everything.

---

## Theme A — Fast, mobile-friendly rendering of many map points

**The problem:** With ~644 points, text labels overlap and the map adapts badly to mobile (portrait and landscape). Jared half-remembers "a new TypeScript technique that uses the browser's front engine to reduce the cost of computing text and graphic layouts."

**What that memory most likely refers to:** the shift from drawing maps with **HTML/CSS elements** (which the browser has to lay out and paint one by one — slow once there are hundreds of them) to drawing them on the **GPU via WebGL** (the browser's graphics chip draws thousands of shapes per frame almost for free). "The browser's front engine" = the GPU / WebGL rendering path. This is the core idea behind MapLibre, deck.gl, Leaflet.glify and PixiOverlay below. It is a *rendering technique*, not specifically a TypeScript feature — though MapLibre and deck.gl are written in TypeScript.

Important nuance: **WebGL rendering does not by itself fix overlapping text.** Overlapping labels are a *label-collision* problem. MapLibre solves it natively (it hides colliding labels automatically); the Leaflet add-ons mostly solve the *speed* problem and still need clustering (which you already have) to manage overlap.

### Option A1 — CSS `content-visibility` (the simplest possible thing) — ADD-ON
- **What it is:** a one-line CSS property (`content-visibility: auto`, paired with `contain-intrinsic-size`) that tells the browser to skip the layout/paint work for anything currently off-screen. Documented at [web.dev](https://web.dev/articles/content-visibility) and [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/content-visibility).
- **Licence:** N/A — it's a built-in browser feature, free forever.
- **Problem it solves:** cuts the cost of laying out large blocks of HTML (e.g. long side panels, the news list, legend) that aren't visible. web.dev reports up to a 7x rendering speedup on heavy pages. It does **not** speed up map markers themselves (Leaflet manages those), but it's the cheapest win for the surrounding panels.
- **Size of change:** tiny add-on — a few CSS lines, no library, fully reversible.
- **Caveat:** helps the *page chrome*, not the 644 markers. Best treated as a free bonus, not the main fix.

### Option A2 — Leaflet.markercluster (you already have this) — keep it
- The current clustering plugin already collapses nearby markers into one, which is the standard, cheapest way to stop 644 markers from overlapping. Any rendering upgrade should keep clustering on. No change recommended here beyond confirming it stays.

### Option A3 — supercluster — ADD-ON (clustering engine)
- **What it is:** Mapbox's standalone clustering maths library ([github.com/mapbox/supercluster](https://github.com/mapbox/supercluster)). It only computes clusters extremely fast; it doesn't draw anything. Often paired with a WebGL renderer.
- **Licence:** ISC (a permissive, genuinely free licence, like MIT).
- **Problem it solves:** faster, smoother clustering than Leaflet.markercluster at large scale. At 644 points this is overkill — markercluster is fine. Only relevant if point counts grow into the tens of thousands.
- **Size of change:** add-on, but only worth it alongside a WebGL renderer. **Not recommended at current scale.**

### Option A4 — Leaflet.glify — ADD-ON (WebGL on top of Leaflet)
- **What it is:** [Leaflet.glify](https://github.com/robertleeplummerjr/Leaflet.glify) — "a ridiculously fast WebGL renderer plugin for Leaflet." Draws points/lines/polygons on the GPU while keeping your existing Leaflet map.
- **Licence:** MIT (genuinely free). ~539 stars, last release 3.3.1 on 2024-12-05 — maintained but not hugely active.
- **Problem it solves:** lets Leaflet draw thousands of points smoothly without replacing it.
- **Size of change:** add-on — keeps Leaflet. But it draws plain dots, not your styled markers/popups, so re-creating the current look (operator colours, click popups) is real work. **Bigger than it sounds at 644 points.**

### Option A5 — Leaflet.PixiOverlay — ADD-ON (WebGL via Pixi.js)
- **What it is:** [Leaflet.PixiOverlay](https://github.com/manubb/Leaflet.PixiOverlay) — renders a Pixi.js (WebGL game-graphics) layer on top of Leaflet.
- **Licence:** ISC (free). Listed on the official Leaflet plugins page, widely used.
- **Problem it solves:** very smooth zoom/pan with many custom-drawn markers, still inside Leaflet.
- **Size of change:** add-on, but you draw markers yourself in Pixi — more coding than glify for styled markers. Overkill at 644 points.

### Option A6 — deck.gl (+ deck.gl-leaflet) — ADD-ON *or* REPLACE depending on use
- **What it is:** [deck.gl](https://deck.gl) is Uber's heavyweight GPU data-visualisation framework. The [deck.gl-leaflet](https://github.com/zakjan/deck.gl-leaflet) bridge (now `@deck.gl-community/leaflet`) lets it overlay on a Leaflet map.
- **Licence:** MIT (free).
- **Problem it solves:** stunning large-scale data viz (heatmaps, arcs, animated trips) and built-in collision-hiding for dense points (`CollisionFilterExtension`). Also powers the time animation in Theme B.
- **Size of change:** can be added over Leaflet, but it's a large, complex dependency (~hundreds of KB) and a steep learning curve. Realistically a partial-rebuild. **Justified only if you want rich animation/3D, not just to draw 644 dots.**

### Option A7 — MapLibre GL JS — REPLACE Leaflet (the big lift)
- **What it is:** [MapLibre GL JS](https://maplibre.org/projects/gl-js/) — the fully open-source fork of Mapbox GL JS v1. Renders the **entire map on the GPU/WebGL**, including automatic label-collision handling (overlapping text is hidden for you) and smooth vector zoom.
- **Licence:** BSD-2-Clause (genuinely free, no API key required for the library itself — though you'd want a free/open map-tile style).
- **Problem it solves:** this is the textbook answer to "draw many points fast and stop text overlapping," and it's the closest match to Jared's "browser graphics engine" memory. Handles 100,000+ points at 60fps.
- **Size of change:** **REPLACE — the biggest change on this list.** It is a different map engine, so the whole `map-embed.html` (markers, popups, filters, legend wiring) would be rebuilt against MapLibre's API. Bundle is ~290KB gzipped vs Leaflet's ~42KB. High payoff for label overlap + mobile smoothness, but a genuine rebuild, not a weekend add-on.

### Theme A — simplest-first recommendation
1. **First, the free wins (do these regardless):** add `content-visibility:auto` to the heavy side panels (A1), and confirm marker clustering stays on (A2). These cost almost nothing and may resolve much of the mobile sluggishness.
2. **If text-overlap on mobile is still the pain point** and you're willing to do a real rebuild, **MapLibre GL JS (A7)** is the proper long-term answer because it fixes label collision *and* rendering speed at once — but be clear-eyed that it **replaces Leaflet** (big job).
3. **Avoid** glify/PixiOverlay/deck.gl/supercluster *purely for speed* at 644 points — they're built for tens of thousands of points and would add complexity without solving the overlap problem. deck.gl earns its place only if you also want the Theme B time animation.

> **Big-rebuild flag:** MapLibre (A7) = replace Leaflet. Everything else in Theme A is an add-on or a free CSS tweak.

---

## Theme B — Time animation / looping playback (deployments appearing over 2020→2026)

**The problem:** you want a play/stop button that animates the map through time, so points appear as their deployment dates arrive (2020 → 2026), and ideally loops. You already have a year/month *filter* strip; this adds automated *playback*.

### Option B1 — Leaflet.timeline (skeate) — ADD-ON ✅ best fit
- **What it is:** [Leaflet.timeline](https://github.com/skeate/Leaflet.timeline) — "Display arbitrary GeoJSON on a map with a timeline slider and play button." It's a Leaflet layer that reads `start`/`end` dates from each point and reveals them over time, with a built-in slider and play button.
- **Licence:** MIT (genuinely free). Actively maintained (recent bugfix releases).
- **Problem it solves:** exactly your use case — time-series points appearing on a play-through. Built specifically for GeoJSON points with date properties.
- **Size of change:** **ADD-ON** — drops onto your existing Leaflet map. You'd feed it your deployment dates (you already have `date_start`). The lightest path to the feature.

### Option B2 — Leaflet.TimeDimension (socib) — ADD-ON
- **What it is:** [Leaflet.TimeDimension](https://github.com/socib/Leaflet.TimeDimension) — a richer time-control plugin: play/pause, next/back, time slider, **speed slider, and a loop option** for automatic repeat.
- **Licence:** MIT (free). ~451 stars — but **last release was Nov 2019**, so it's mature but effectively unmaintained. Works with modern Leaflet in practice, but no one's fixing bugs.
- **Problem it solves:** same as B1, with more playback controls (speed, explicit loop) out of the box.
- **Size of change:** **ADD-ON** to Leaflet. More features than B1 but staler codebase. Choose this only if you specifically want the speed slider / loop toggle and are OK with an unmaintained dependency.

### Option B3 — deck.gl TripsLayer / kepler.gl — REPLACE (overkill here)
- **What it is:** [deck.gl TripsLayer](https://deck.gl/docs/api-reference/geo-layers/trips-layer) animates a moving "playhead" along paths over time; [kepler.gl](https://github.com/keplergl/kepler.gl) is a full GPU mapping app built on it with time playback.
- **Licence:** both MIT (free).
- **Problem it solves:** beautiful large-scale *movement* animation (vehicles travelling routes). Your data is **static points appearing on dates**, not things moving along paths — TripsLayer is the wrong shape for it.
- **Size of change:** **REPLACE / major rebuild** (deck.gl is a separate GPU engine; kepler.gl is a whole app). Not warranted for "points appear over time."

### Theme B — simplest-first recommendation
- **Use Leaflet.timeline (B1).** It is the closest match to what you described, is an add-on to your current Leaflet map, MIT-licensed, and actively maintained.
- If you find you want a **speed control or explicit loop button** that B1 lacks, look at **Leaflet.TimeDimension (B2)** — but note it's unmaintained since 2019.
- **Skip** deck.gl/kepler.gl (B3) for this — it's a moving-vehicle tool and would mean replacing Leaflet.

> **Big-rebuild flag:** only B3 is a rebuild. B1 and B2 are both add-ons. Recommended option (B1) is a safe add-on.

---

## Theme C — Collapsible / minimizable legend and control panels (hide to save space on mobile)

**The problem:** the legend and control panels eat screen space on mobile; you want to collapse/hide them. Prefer an existing Leaflet plugin over hand-rolled UI. Everything here is an **ADD-ON** to Leaflet — none replaces it.

### Option C1 — Built-in `collapsed: true` on Leaflet's layer control — ADD-ON (free, already in Leaflet)
- **What it is:** Leaflet's own `L.control.layers` has a `collapsed` option (default `true`): the control shrinks to a small icon and expands on tap/hover. No plugin needed. (See [Leaflet docs / issue #5210](https://github.com/Leaflet/Leaflet/issues/5210).)
- **Licence:** BSD-2-Clause (Leaflet itself — free).
- **Problem it solves:** the *layer toggles* can already collapse to an icon for free. Doesn't cover a custom legend, but it's zero-cost for the layer switcher.
- **Size of change:** trivial — flip one option. **Always worth doing first.**
- **Note:** there are long-standing minor bugs when forcing `collapsed:false` to stay open; the default collapsing behaviour is solid.

### Option C2 — leaflet-sidebar-v2 — ADD-ON ✅ best fit for panels
- **What it is:** [leaflet-sidebar-v2](https://github.com/Turbo87/sidebar-v2) (and the maintained fork [norwin/leaflet-sidebar-v2](https://git.nroo.de/norwin/leaflet-sidebar-v2)) — a responsive, collapsible **tabbed sidebar** for Leaflet. Tap a tab icon to slide the panel open/closed. Designed mobile-first.
- **Licence:** MIT (free).
- **Problem it solves:** moves your legend / news / 3D panels into a single tidy sidebar that collapses to a strip of icons on mobile — the standard, polished answer to "panels eat the screen."
- **Size of change:** **ADD-ON**, but a moderate one: you'd move your existing panel HTML into the sidebar's tab structure. Bigger than a one-liner, smaller than a rebuild. The original repo's last release is 2020, but it's widely used and a maintained fork exists.

### Option C3 — L.Control.AccordionLegend — ADD-ON (legend-specific)
- **What it is:** [L.Control.AccordionLegend](https://github.com/GreenInfo-Network/L.Control.AccordionLegend) — an accordion-style legend with explicit `collapseUI()` / `expandUI()` / `toggleUI()` methods to hide and show the panel.
- **Licence:** MIT (free). Last release Dec 2020 — mature, not actively maintained.
- **Problem it solves:** specifically a collapsible **legend** with layer/opacity controls. Narrower than the sidebar but purpose-built for legends.
- **Size of change:** **ADD-ON.** Good if you only want the *legend* to collapse and don't want to restructure all panels into a sidebar.

### Option C4 — Plain HTML `<details>` / a CSS toggle — ADD-ON (no library at all)
- **What it is:** the browser's native `<details>`/`<summary>` element makes any block collapsible with zero JavaScript and zero dependencies. Wrap the legend in it and it gets a click-to-expand arrow for free.
- **Licence:** N/A — built-in browser feature.
- **Problem it solves:** the *simplest possible* collapsible legend, no plugin, fully reversible.
- **Size of change:** tiny add-on — a couple of HTML tags plus a little CSS.

### Theme C — simplest-first recommendation
1. **Start free:** set `collapsed: true` on the layer control (C1) and wrap the legend in a native `<details>` element (C4). That likely solves the mobile space problem with no new dependency.
2. **If you want a single polished, tabbed panel** that slides away on mobile, adopt **leaflet-sidebar-v2 (C2)** — the standard choice, MIT-licensed, add-on (moderate effort to migrate panels in).
3. C3 is a fine middle ground if you only care about the legend and prefer a ready-made accordion over hand-rolling `<details>`.

> **Big-rebuild flag:** none. Every Theme C option is an add-on or a built-in browser/Leaflet feature. No tool here touches the map engine.

---

## Theme D — In-map onboarding / intro overlay (welcome panel or guided intro)

**The problem:** new visitors need a short welcome / guided intro explaining what the map shows. All options here are **ADD-ONs** — none touches the map engine.

⚠️ **Licence warning up front (important for a public art project):** the two libraries you named — **intro.js and Shepherd.js** — both have their *core* library under **AGPL-3.0**, not MIT. AGPL is a "copyleft" licence: if you publish a website that uses it, AGPL can require you to release *your whole site's source code* under the same terms (or buy a paid commercial licence). For a public-facing documentary project, that's a real consideration. There is a cleaner MIT-licensed alternative (Driver.js, D1) that does the same job without the strings.

### Option D1 — Driver.js — ADD-ON ✅ recommended
- **What it is:** [Driver.js](https://driverjs.com/) ([github.com/kamranahmedse/driver.js](https://github.com/kamranahmedse/driver.js)) — a lightweight, zero-dependency library for guided tours and feature highlights. It dims the page and spotlights elements one at a time with a "next/back/done" popover.
- **Licence:** **MIT (genuinely free, no strings)** — the key advantage over intro.js/Shepherd.js.
- **Problem it solves:** a guided walkthrough ("this is the filter, this is the timeline, click a dot to see details") with no licensing risk.
- **Size of change:** **ADD-ON** — small. One script, written in TypeScript, no dependencies, framework-agnostic, works fine alongside Leaflet.

### Option D2 — Shepherd.js — ADD-ON (capable, but AGPL)
- **What it is:** [Shepherd.js](https://docs.shepherdjs.dev/) — a polished, highly flexible guided-tour library (modal overlays, keyboard nav, good positioning). Widely regarded as the strongest of the tour libraries feature-wise.
- **Licence:** **AGPL-3.0** for the core (the MIT bit is only the React wrapper, which you don't need). Paid commercial licence available. **The AGPL copyleft applies to a public site** — flag for review before adopting.
- **Problem it solves:** the richest guided-tour experience.
- **Size of change:** add-on. Only choose over Driver.js if you specifically need a feature Driver.js lacks *and* you accept the AGPL terms (or pay).

### Option D3 — intro.js — ADD-ON (not recommended)
- **What it is:** [intro.js](https://introjs.com/) — the original step-by-step tour library.
- **Licence:** **AGPL-3.0** (free only for open-source/personal/non-commercial; commercial licence otherwise). Same copyleft caveat as D2.
- **Problem it solves:** same as the others. But a 2026 accessibility benchmark flagged it as the *worst* of the libraries tested (missing ARIA labels, no focus trap), and development has slowed to maintenance-only.
- **Size of change:** add-on, but **avoid** — worse licence + worse accessibility than Driver.js for the same job.

### Option D4 — A plain Leaflet modal / `<dialog>` welcome panel — ADD-ON (simplest)
- **What it is:** instead of a guided *tour*, just show a one-time welcome card explaining the map, using the browser's native `<dialog>` element or a tiny Leaflet popup/control. No library at all. (Leaflet plugins like `leaflet-control-window` exist, but the native `<dialog>` needs nothing.)
- **Licence:** N/A — built-in browser feature.
- **Problem it solves:** if you only need a *welcome message* (not a step-by-step tour), this is the zero-dependency answer. Pair it with a "don't show again" checkbox via a cookie/localStorage.
- **Size of change:** tiny add-on — a bit of HTML/CSS/JS, no dependency, no licence concern.

### Theme D — simplest-first recommendation
1. **If you just want a welcome panel:** use a native `<dialog>` modal (D4). No library, no licence issue, minimal code. This is likely all an art map needs.
2. **If you want a proper step-by-step guided tour:** use **Driver.js (D1)** — MIT-licensed, tiny, dependency-free. It is the clear pick over intro.js/Shepherd.js *specifically because of the AGPL licensing* on those two.
3. **Avoid intro.js and Shepherd.js** unless you've reviewed and accepted AGPL (or budget for their commercial licence). For a public website this is a genuine flag, not a formality.

> **Big-rebuild flag:** none — all add-ons. The real flag here is **licensing**, not size of change: intro.js/Shepherd.js are AGPL; Driver.js and a native modal are not.

---

## Theme E — The "stuck highlight" toggle-button bug and the z-index / layering bug

**These are not library jobs.** Both are standard, tiny CSS fixes. No tool needed. Confirmed below so the upgrade plan can simply note "small CSS fix."

### E1 — "Stuck highlight" on a toggle button (it stays highlighted after tapping)
- **What's happening:** on touch screens, a `:hover` (and sometimes `:focus`) style "sticks" after you tap — the button keeps its highlighted look until you tap somewhere else. This is the well-known **"sticky hover"** problem on mobile. ([CSS-Tricks](https://css-tricks.com/solving-sticky-hover-states-with-media-hover-hover/))
- **Standard fix (CSS only, no JavaScript):** wrap hover styling in a media query so it only applies on devices that actually have a hovering pointer (a mouse):
  ```css
  @media (hover: hover) {
    .toggle-button:hover { /* highlight styles here */ }
  }
  ```
  Touch devices fail this test, so the highlight never sticks. If the button is a genuine on/off toggle, drive its "on" look from an explicit **active-state class** (e.g. `.is-active`) that your JavaScript adds/removes — **do not** rely on `:focus` for the lit state, because `:focus` also sticks on mobile until another control is tapped.
- **Plain-English takeaway:** separate "the user is pointing at it" (`:hover`, gate behind `@media (hover:hover)`) from "this toggle is switched on" (a class you control). That removes the stuck highlight. **No tool needed — a few CSS lines plus a class toggle.**

### E2 — The z-index / layering bug (something appears under/over the wrong thing)
- **What's happening:** an element shows through, or hides behind, another when it shouldn't. This is almost always a **stacking-context** issue: `z-index` only works on elements that are *positioned* (`position: relative/absolute/fixed/sticky`), and a `z-index` value only competes **within the same stacking context** — a high `z-index` inside a parent that sits low in the stack can't escape its parent.
- **Standard fix:**
  1. Make sure the element you want on top has both `position` set (e.g. `position: relative`) **and** a `z-index`.
  2. Check parent elements — properties like `transform`, `opacity` below 1, `filter`, or `will-change` silently create a new stacking context that traps children. If a panel won't rise above the map, the culprit is usually a parent like that.
  3. For Leaflet specifically, Leaflet uses its own pane z-index scale (map tiles, overlays, markers, popups, controls each have set layers). Custom panels layered over the map should sit **above** Leaflet's control pane; give your overlay a `z-index` higher than Leaflet's controls (Leaflet's top panes are in the hundreds to ~1000), and make sure it isn't nested inside a Leaflet pane that caps it.
- **Plain-English takeaway:** "give it `position` + a high enough `z-index`, and check no parent is trapping it." **No tool needed — a CSS fix.**

> **Big-rebuild flag:** none. Both E1 and E2 are small CSS edits. The plan should record: *"no library required — confirmed standard CSS fixes."*

---

## Bottom line — one simplest recommendation per theme

| Theme | Simplest recommended option | Type | Rebuild risk |
|---|---|---|---|
| **A. Fast mobile rendering of many points** | First do the **free wins**: `content-visibility:auto` on heavy panels + keep marker clustering. The *proper* fix for overlapping text is **MapLibre GL JS**, but that **replaces Leaflet**. | CSS tweak now / MapLibre later | ⚠️ **MapLibre = full rebuild.** All other Theme-A options are add-ons but are overkill at 644 points. |
| **B. Time animation / play button** | **Leaflet.timeline** (skeate) — MIT, maintained, reads your dates, has a play button. | Add-on | ✅ Safe add-on. (deck.gl/kepler.gl would be a rebuild — skip.) |
| **C. Collapsible legend / panels** | Free first: set `collapsed:true` on the layer control + wrap the legend in a native `<details>`. For a polished tabbed panel, **leaflet-sidebar-v2** (MIT). | Built-in / add-on | ✅ No rebuild anywhere in Theme C. |
| **D. Onboarding / intro overlay** | A native `<dialog>` **welcome card** if you just want a message; **Driver.js** (MIT) if you want a guided tour. | Add-on | ✅ No rebuild. ⚠️ **Avoid intro.js & Shepherd.js — they are AGPL-licensed** (copyleft risk for a public site). |
| **E. Stuck-highlight & z-index bugs** | **No tool.** Gate hover behind `@media (hover:hover)` + use an explicit active-state class; fix layering with `position` + `z-index` and check for trapping parents. | CSS fix | ✅ Tiny CSS edits, no library. |

**The one thing to flag loudest:** only **Theme A's MapLibre option is a true "replace Leaflet" rebuild.** Everything else across all five themes is either a small safe add-on, a built-in browser feature, or a CSS fix. If the overlapping-text-on-mobile problem is the top priority and the free CSS/clustering wins don't fully solve it, that's the one place where a bigger investment (swapping the map engine to MapLibre) is genuinely justified — and it should be a deliberate, separate decision, not bundled in with the small fixes.

> *End of preliminary research. Sections above are self-contained; further feedback themes can be appended below this line.*

---
---

# Round 2

> **What changed since Round 1:** the user has **lifted the "free / open-source only" rule.** Round 2 includes **paid and commercial** options too, wherever they're meaningfully better. Everything is still written in plain English for a non-technical reader.
>
> **Same two sizes of change as before:**
> - **ADD-ON** = a small plugin or snippet bolted onto the existing Leaflet map. Low risk, reversible.
> - **REPLACE** = swap Leaflet for a different map engine (MapLibre). Big rebuild, touches everything.
>
> **Cost labels used below:** *Free* (no cost ever) · *Freemium* (free tier, pay to unlock more) · *Paid* (costs money).

---

## R1 — "Pretext Library" + GPU text/graphics rendering in the browser

**What Jared asked:** he named a "Pretext Library" as the thing he meant for "dynamically reloading text using the web browser's front engine to reduce the cost of computing text and graphic layouts." I was asked to find out what this actually is.

### CONFIRMED: Pretext is a real, specific library — and Jared remembered it accurately.

- **Name + link:** **Pretext** (a.k.a. Pretext.js) — [github.com/chenglou/pretext](https://github.com/chenglou/pretext), site [pretextjs.dev](https://pretextjs.dev/), npm `@chenglou/pretext`.
- **Who made it:** Cheng Lou (senior engineer at Midjourney, creator of React Motion). It's recent (covered by InfoQ in **April 2026**) and already very popular (~48k GitHub stars).
- **Cost / licence:** **Free — MIT licence** (no strings, safe for a public project).
- **What it actually is, in plain English:** a tiny (~15KB) JavaScript/TypeScript library that **measures and lays out multi-line text using pure arithmetic**, instead of asking the browser to do it. Normally, when code needs to know "how tall is this paragraph?" it asks the browser via calls like `getBoundingClientRect()` / `offsetHeight`. Each such question forces the browser to stop and re-do a full layout pass ("forced synchronous reflow") — one of the most expensive things a browser does. Pretext measures the font **once** (using the browser's own font engine as the source of truth, via the Canvas `measureText` API) and then does all further layout maths itself, with **no reflow ever**. Its own benchmarks claim ~300–600x faster text measurement, fast enough to run every animation frame (it markets "120 FPS text layout").
- **Crucial clarification — what it does NOT do:** Pretext is a **measurement / layout calculator, not a renderer**. It does **not** draw text on the GPU. It tells you *where* text should go and *how big* it is; you still draw it (to DOM, Canvas or SVG) yourself. So Jared's phrase "the browser's front engine" maps to "it uses the browser's font engine to measure once, then avoids the browser's layout engine thereafter" — it's about **avoiding expensive layout recalculation**, not GPU graphics.

### Is Pretext relevant to the ALHFRS map?

**Honest answer: marginally, and not as the headline fix.** Here's the nuance:

- The map's heavy cost isn't measuring text — it's **drawing ~644 markers and avoiding overlapping labels** (a *collision* problem, covered in Round 1 Theme A and below). Pretext doesn't place markers or hide colliding labels.
- Where Pretext *could* help: if the new **detail panel** (R4 below) or the news list renders a lot of text and re-flows it on every interaction (resize, animation, typing), Pretext can make that text layout buttery-smooth. That's a "nice polish on the side panels" use, the same category as Round 1's `content-visibility` tip — **not** the thing that fixes the map itself.
- **Recommendation:** file Pretext as a *known, legit, free tool to keep in the back pocket* for text-heavy panels — **but it is not the tool that solves the map's overlapping-labels-on-mobile problem.** Don't reach for it first. (If the real goal is "stop labels overlapping," see the collision plugins immediately below and MapLibre in Round 1 Theme A.)

### The category Jared was really pointing at: GPU/WebGL text & graphics in the browser

This is a *different* family of tools from Pretext (these actually **draw** on the GPU). Relevant only if you go down the "draw thousands of custom things fast" road:

| Tool | Cost / licence | What it does | Relevance to this map |
|---|---|---|---|
| **PixiJS** ([pixijs.com](https://pixijs.com)) | Free, MIT | A fast 2D GPU graphics engine (WebGL/WebGPU). Draws huge numbers of shapes/sprites/text smoothly. | Only via the Leaflet.PixiOverlay bridge (Round 1 A5). Overkill at 644 points. |
| **troika-three-text** ([protectwise.github.io/troika](https://protectwise.github.io/troika/troika-three-text/)) | Free, MIT | Crisp GPU text rendering for 3D (Three.js) scenes, using "signed distance field" glyphs generated in a background worker. Handles kerning, right-to-left, Arabic. | Relevant **only if you embed a 3D/Three.js scene** (e.g. some Gaussian-splat viewers are Three.js based — see R4). Not for the 2D map. |
| **HarfBuzz (JS/WASM builds)** | Free, open | Industrial-grade text *shaping* (turning characters into correctly-positioned glyphs for complex scripts). | Far more than this project needs. Mentioned only for completeness. |

### Map label-collision plugins (the actual fix for "overlapping labels")

Since "overlapping labels on mobile" is the real pain, these are the on-point, **free** Leaflet add-ons (all ADD-ONs, no rebuild):

- **Leaflet.LabelTextCollision** ([github.com/yakitoritabetai/Leaflet.LabelTextCollision](https://github.com/yakitoritabetai/Leaflet.LabelTextCollision)) — shows labels on the map but **hides ones that would overlap**, preferring whichever you list first (so you can prioritise important deployments). Free (open source).
- **Leaflet.LayerGroup.Collision** ([github.com/MazeMap/Leaflet.LayerGroup.Collision](https://github.com/MazeMap/Leaflet.LayerGroup.Collision)) — declutters overlapping **markers** by hiding ones whose boxes collide (uses the fast `rbush` library under the hood). Free, MIT.
- **leaflet-inflatable-markers-group** ([github.com/Meteo-Concept/leaflet-inflatable-markers-group](https://github.com/Meteo-Concept/leaflet-inflatable-markers-group)) — gives markers a small "deflated" state when crowded and a full state when there's room. Free.

### R1 bottom line
- **Pretext is real, free (MIT), and Jared described it correctly** — but it's a *text-measurement* tool, not a map fix and not a GPU renderer. Keep it for smooth text in the new detail/news panels; don't expect it to fix the map.
- **For overlapping labels specifically**, the simplest path is a free Leaflet **collision plugin** (e.g. Leaflet.LabelTextCollision) as an add-on; the heavyweight "does it automatically" answer remains **MapLibre** (a full rebuild — Round 1 Theme A).
- **GPU text libraries (PixiJS, troika) only matter if you add a 3D scene** (relevant to the splat viewer in R4), not for the flat map.

> **Big-rebuild flag:** none here. Pretext and the collision plugins are all add-ons. (MapLibre, mentioned for context, remains the only rebuild.)

---

## R2 — Cross-browser + responsive map loading (phone portrait/landscape, tablet, desktop)

**The problem:** make the map size itself correctly across browsers and screen shapes — phone in portrait, phone rotated to landscape, tablet, desktop — without the classic bugs (map renders at zero height, or only fills half the screen until you rotate, or the mobile browser's address bar covers part of it).

Good news: this is **almost entirely free, built-in technique — not a library purchase.** The robust modern approach has three parts, all ADD-ONs / CSS tweaks.

### R2a — Size the map with modern viewport units (free, CSS only) — ADD-ON
- **What it is:** newer CSS height units **`dvh` / `svh` / `lvh`** ("dynamic / small / large viewport height") that finally fix the long-standing mobile bug where `100vh` was taller than the actual visible area because the phone's address bar wasn't accounted for. Plain English: `svh` = height with the address bar showing, `lvh` = with it hidden, `dvh` = adjusts live as the bar slides away. ([web reference: dev.to guide](https://dev.to/softheartengineer/mastering-modern-viewport-units-svh-lvh-and-dvh-for-responsive-web-design-5de9))
- **Cost / licence:** free, built into all current browsers.
- **What it solves:** the map filling exactly the visible screen on phones, not spilling under the address bar.
- **Best-practice recipe (from 2026 guidance):** use `svh` for a fixed full-screen map so it's always fully visible regardless of the address bar; provide a plain `100vh` line *first* as a fallback for very old browsers, then the `100svh`/`100dvh` line after it. Add a specific media query for **landscape** because the rules that look right in portrait often break when the viewport is very short and wide.
- **Size of change:** tiny — a few CSS lines on the map container.

### R2b — Tell Leaflet to recalculate when the screen changes (`invalidateSize`) — ADD-ON
- **What it is:** Leaflet's own `map.invalidateSize()` method. When the map's container changes size (rotate the phone, open/close a panel, address bar slides away), Leaflet must be *told* to re-measure — otherwise you get the classic "map only fills part of the box / grey tiles down one side" bug. ([Leaflet docs](https://leafletjs.com/examples/mobile/), [resize issue thread](https://github.com/Leaflet/Leaflet/issues/1544))
- **Cost / licence:** free — it's part of Leaflet, already in the project.
- **What it solves:** the #1 responsive-map bug. The robust pattern: listen for the browser's `resize` and `orientationchange` events and call `map.invalidateSize()` after the container has resized. Call it only *after* the map is fully created, never before.
- **Size of change:** tiny — a few lines of JavaScript wiring up an event listener. **This is the single most important fix for "looks wrong until I rotate."**

### R2c — Leaflet's mobile/touch handling (free, built-in) — keep on
- Leaflet already includes mobile-tuned touch handling, pinch-zoom, and a documented full-screen mobile example. The main extra step is the standard responsive `<meta name="viewport">` tag in the page head so phones don't render it zoomed-out. Confirm that tag is present; otherwise nothing to add.

### R2d — A responsive UI helper (optional, only if the panels get complex) — ADD-ON
- If the new detail panel / legend / timeline UI grows complicated across screen sizes, a lightweight CSS approach (CSS Grid + container queries, or a minimal utility CSS framework) keeps it tidy — but for a single map page this is usually **not worth a framework**. The Round 1 recommendation of **leaflet-sidebar-v2** (mobile-first collapsible panel, MIT, free) already covers most of the responsive-panel need. No new tool recommended here.

### R2e — Actually testing it across real browsers/devices — free first, paid if needed
You can't trust a desktop emulator for mobile map behaviour (the address-bar/reflow behaviour differs on real phones). Options:
- **Free:** test on Jared's real iPhone + Mac (already on Tailscale) and in the desktop browsers' built-in device-emulation — good enough for a solo project.
- **Paid, only if you need wide device coverage:**
  - **LambdaTest / TestMu AI** ([lambdatest.com](https://www.lambdatest.com)) — has a genuine **free tier** (limited monthly minutes, ~10 responsive tests, accessibility checks) and paid live plans from about **$15/month**. Best value for occasional cross-device checking.
  - **BrowserStack** ([browserstack.com](https://www.browserstack.com)) — broadest device coverage (thousands of real browsers/devices) but **no permanent free tier** (free trial only); plans roughly **$19–$449/month**.
- **Recommendation:** for a solo art project, **real-device testing on your own phone is enough** — don't pay for a testing service unless you later need to prove it works on dozens of devices.

### R2 bottom line
- **No purchase needed.** The robust responsive approach is: size the map with **`svh`/`dvh`** units (R2a), and call Leaflet's **`invalidateSize()`** on resize/rotate (R2b). Those two fixes solve almost all "wrong size until I rotate / address bar covers it" problems.
- Keep Leaflet's built-in mobile touch handling and ensure the viewport meta tag is present (R2c).
- For testing, **use your own iPhone/Mac**; only consider **LambdaTest (free tier / ~$15/mo)** if you ever need broad device coverage. **BrowserStack** is the enterprise option (no free tier).

> **Big-rebuild flag:** none. All of R2 is CSS tweaks + a few lines of Leaflet wiring. No engine change.

---

## R3 — "Spotlight on London" effect (grey out / dim everywhere outside Greater London)

**The goal:** the moment the map loads, everything outside Greater London is greyed-out / dimmed / blurred, so the eye is immediately drawn to London and the viewer instantly understands the map is *about* London. This is a well-known cartographic technique often called a **mask** or **inverted polygon** (you cut a London-shaped hole in a dark overlay that covers the rest of the world).

You already have the raw material: **`map/data/london-boroughs.geojson`** — the outline of Greater London. The mask is built from that exact shape.

### In Leaflet (your current engine) — all ADD-ONs, all free

**Option R3a — Leaflet.Mask plugin (easiest, purpose-built)** ✅ recommended
- **Name + link:** **Leaflet.Mask** ([github.com/ptma/Leaflet.Mask](https://github.com/ptma/Leaflet.Mask), [demo](https://ptma.github.io/Leaflet.Mask/)).
- **Cost / licence:** free, open source.
- **What it does:** you point it at a GeoJSON polygon and it masks (dims/covers) the entire rest of the map, leaving only that shape visible. Literally `L.mask('london-boroughs.geojson').addTo(map)`. It has handy options: `interactive: false` (so clicks pass through the grey area to the map) and `fitBounds: true` (auto-zoom to the shape).
- **Size of change:** small ADD-ON — one plugin + a couple of lines, reusing the borough GeoJSON you already have.
- **Look:** gives a solid dimmed overlay outside London. You control the colour/opacity (e.g. a soft dark or a desaturated grey).

**Option R3b — Turf.js inverted-polygon mask (no plugin, more control)** — ADD-ON
- **Name + link:** **Turf.js** `mask` ([turfjs.org/docs/api/mask](https://turfjs.org/docs/api/mask)) — a free geospatial-maths toolkit.
- **Cost / licence:** free, MIT.
- **What it does:** `turf.mask()` takes the London polygon and returns a new polygon that is "the whole world with a London-shaped hole." You then add that as a normal Leaflet GeoJSON layer filled with a semi-transparent dark colour — instant spotlight. (Historically you did this by hand with a world-rectangle + `turf.difference`; `mask()` now does it in one call.)
- **Size of change:** small ADD-ON. Slightly more code than R3a but no extra map plugin and total control over styling (you can even animate the opacity on load).
- **Note:** for a clean edge, feed it the dissolved outer boundary of London rather than all 33 separate boroughs.

**Option R3c — leaflet-boundary-canvas (clip the *tiles* to London)** — ADD-ON
- **What it does:** instead of dimming the outside, this clips the actual map *tiles* so they only render **inside** London — outside is blank/transparent (you'd put a colour or texture behind). A stronger, more graphic look ("London floating on a flat background"). Free, open source.
- **Size of change:** small-to-moderate ADD-ON. Best when you want London to look *cut out* rather than *dimmed*. Slightly more finicky than R3a.

**Blur, specifically:** a true *blur* (not just dim) of the outside is harder — Leaflet doesn't blur map tiles directly. The practical route is the mask overlay (R3a/R3b) with a semi-opaque colour, optionally plus a CSS `backdrop-filter: blur()` on the mask layer in browsers that support it. A full crisp blur of the underlying tiles is fiddly; **dimming is the reliable, good-looking choice.** Recommend dim, not blur.

### In MapLibre (only relevant if you ever switch engines)
- MapLibre has **no built-in mask feature** — it's a long-standing community request, not shipped. You'd either draw the same Turf.js inverted polygon as a fill layer (same idea as R3b, works fine) or hand-write a low-level custom WebGL "stencil" layer (advanced). So switching to MapLibre gives you **no advantage** for this effect; if anything it's marginally more work. ([MapLibre discussion #3237](https://github.com/maplibre/maplibre-gl-js/discussions/3237))

### Difficulty / R3 bottom line
- **Easy and free.** The spotlight effect is one of the cheaper wins here. **Use Leaflet.Mask (R3a)** with the borough GeoJSON you already have — a few lines, dimmed-outside look, clicks pass through.
- If you want finer styling control or to animate the dim-in on load, use the **Turf.js mask (R3b)** instead — still small, no map-engine change.
- Choose **leaflet-boundary-canvas (R3c)** only if you want London visually *cut out* rather than dimmed.
- **Recommend dim, not blur** — blur of the live tiles is fiddly for little gain.
- **No reason to switch to MapLibre for this** — it actually has less built-in support than Leaflet here.

> **Big-rebuild flag:** none. Every recommended R3 option is a small Leaflet add-on reusing your existing London outline.

---

## R4 — Rich "click a deployment" detail panel (facts + sources + news + social + photos + Gaussian splat)

**The goal:** clicking a deployment opens a rich view that can mix: the deployment facts + source link, related news articles, social-media embeds, user-submitted photos/videos, Jared's own photos, and an embedded **Gaussian splat** (3D capture) of the location.

This splits into two questions: **(a)** where does all that content live — popup or side panel? and **(b)** how do you embed a Gaussian splat in a web page?

### Part (a) — Popup vs side detail-panel

**Verdict up front: use a side panel, not a popup, for rich mixed content.** A Leaflet popup is a small bubble pinned to the marker — fine for a sentence or two, but it gets cramped and clumsy once you add news, embeds, photos and a 3D viewer, and it obscures the map. The standard, best-practice pattern is: **small popup teaser → "More" button → opens a side panel** with the full rich content. ([pattern discussion](https://github.com/Turbo87/leaflet-sidebar/issues/46))

| Option | Cost / licence | What it is | Change size |
|---|---|---|---|
| **leaflet-sidebar-v2** (already recommended in Round 1 Theme C) ✅ | Free, MIT | Responsive, tabbed, collapsible side panel. Put deployment detail in it; collapses to icons on mobile. The natural home for the rich panel. | ADD-ON (moderate — move panel HTML in) |
| **leaflet-popup-sidebar** ([github.com/boldtrn/leaflet-popup-sidebar](https://github.com/boldtrn/leaflet-popup-sidebar)) | Free, open source | A panel that behaves like a popup but renders in a sidebar; JS-API driven, no HTML markup needed. | ADD-ON |
| **Plain rich Leaflet popup** | Free (built-in) | Leaflet popups can hold arbitrary HTML (images, embeds). Use `openOn` so opening one closes the last. OK for a teaser, cramped for the full mix. | Built-in |
| **Your own HTML `<dialog>` / panel** | Free (built-in browser) | Full control over layout; bind "marker click → open panel and fill it." No dependency. | ADD-ON (more hand-coding) |

**Recommendation for (a):** marker click shows a **small popup teaser** (name, date, operator, "View details" button); the button opens **leaflet-sidebar-v2** holding the full rich content (facts, source link, news list, any social embed, photos, and the splat viewer). This keeps the map uncluttered and works on mobile. Mostly an ADD-ON, but assembling the rich panel itself is the real work in this whole upgrade.

**On social-media embeds & user photos:** these are just HTML inside the panel — an X/Instagram embed is a snippet of code you paste; photos are `<img>`/`<video>` tags. No special map tooling needed. (Note for later: user-submitted media ties into the deferred `data/community/` workflow and will need moderation — out of scope for the map itself.)

### Part (b) — Embedding a Gaussian splat (the 3D capture) in the page

This is the genuinely new capability. There are two routes: **(1) the dead-simple paid/hosted iframe**, and **(2) the free self-hosted JS viewer.** Both embed fine *inside* the detail panel from part (a).

#### Easiest possible: hosted iframe embeds (paste one line)
| Service | Cost | What it gives you | Embed effort |
|---|---|---|---|
| **Luma AI** ([lumalabs.ai/interactive-scenes](https://lumalabs.ai/interactive-scenes)) | **Free** for capture + hosting + iframe embed; paid enterprise tier for commercial licensing/API | You capture with the phone app, Luma processes it free in the cloud, and gives you an **iframe** to paste. Very high visual quality. | Trivial — paste an `<iframe>`. **Downside:** Luma-branded, hosted on their servers (not white-labelled), you depend on their platform. |
| **SplatHost** ([splat.host](https://splat.host/)) | **Freemium** (free tier; pay for more) | Upload a `.ply`/`.splat` from *any* tool (Luma, Polycam, your own COLMAP pipeline) and it gives you a **copy-paste iframe**. Tool-agnostic. | Trivial — paste an `<iframe>`. Good middle ground: you own the splat file, they handle the viewer/hosting. |
| **Polycam** ([poly.cam](https://poly.cam)) | Freemium (free = watermark + limited export; Plus **$20/mo** removes watermark) | Capture + share/embed. | Easy, but platform-locked and watermarked on free tier. |

#### Most control / no platform lock-in: free self-hosted JS viewers
These run on *your* page and load a splat file *you* host. More setup, but no branding, no third-party dependency — a good fit for an archival documentary project that wants to own its assets. **This pairs naturally with Jared's existing Gaussian-splat / COLMAP pipeline on the GTX 1080.**

| Library | Cost / licence | Best for | Embed effort |
|---|---|---|---|
| **SuperSplat Viewer** (PlayCanvas) ([playcanvas.com/products/supersplat](https://playcanvas.com/products/supersplat), npm `@playcanvas/supersplat-viewer`) ✅ | **Free, MIT** | General-purpose desktop + mobile. SuperSplat is also the free editor for cleaning up your splats. Can **export a single self-contained HTML file** of a splat, or embed via the viewer package. | **Easy-moderate** — the single-file HTML export is nearly as simple as an iframe, and you host it yourself. **Best balance of easy + self-owned.** |
| **Spark** (World Labs / Stoichast) | Free, open source | Production websites, mobile-first, smallest files (`.spz` format). Integrates with Three.js / React. Called a current leader for web splats. | Moderate — it's a JS library you wire into a Three.js scene (more dev work; needs the troika/Three.js world from R1). |
| **mkkellogg GaussianSplats3D** ([github.com/mkkellogg/GaussianSplats3D]) | Free, open source | If you already use Three.js. Invented the streaming-friendly `.ksplat` format (faster load, less memory). | Moderate — Three.js library. |
| **Babylon.js 8** | Free, open source (Apache) | Splats as a first-class feature inside the Babylon 3D engine. | Moderate — only if you're already using Babylon. |

#### Plain-English recommendation for (b)
- **Fastest to see something working:** **Luma AI** free iframe — capture on phone, paste one line. Accept the Luma branding/hosting for a quick prototype.
- **Best long-term for an archival art project that wants to own its files:** **SuperSplat (free, MIT)** — use its free editor to tidy the capture, then its **single-file HTML export** that you self-host and drop into the detail panel. No branding, no platform dependency, and it dovetails with Jared's own splat/COLMAP pipeline.
- **Tool-agnostic hosted middle ground:** **SplatHost** (freemium) — you keep the `.splat` file, they give you an iframe. Good if self-hosting the viewer feels like too much but you don't want to be locked to Luma.
- **Avoid** the heavier Three.js viewers (Spark, mkkellogg, Babylon) **unless** you're already building a Three.js scene — they're more developer work for the same visible result here.

### R4 bottom line
- **Panel:** marker → small popup teaser → **"View details" opens leaflet-sidebar-v2** holding the rich content. Mostly add-on plumbing; building the rich panel layout is the main effort of the whole upgrade. **No rebuild.**
- **Splat embed:** start with **Luma AI's free iframe** to prototype; settle on **SuperSplat's free self-hosted single-file export** for the real, self-owned version. Both just drop into the panel.
- Social embeds and photos are ordinary HTML inside the panel — no special map tooling.

> **Big-rebuild flag:** none for the *map*. The Three.js-based splat viewers (Spark/mkkellogg/Babylon) imply a bigger 3D-dev effort, but the recommended Luma-iframe / SuperSplat-export paths avoid that.

---

## R5 — Custom shape markers, with slight variants per sub-type

**The goal:** instead of telling operators apart only by *colour*, give each operator a distinct **shape** (e.g. Met Police = circle, BTP = triangle, private retail = square), and use **small shape variants** to signal sub-types (e.g. permanent vs mobile camera; live FR vs retrospective FR). Shape is a second visual channel on top of colour — and it's more accessible (colour-blind-friendly) and reads better in print, which matters for a documentary-art piece.

### In Leaflet (your current engine) — all free ADD-ONs

The core mechanism: Leaflet lets a marker be **any SVG/HTML you supply**, via either `L.divIcon` (HTML/inline SVG) or `L.icon` (an image/SVG file). So you can draw literally any shape. The helper libraries below just save you from hand-drawing each one.

| Option | Cost / licence | What it gives you | Effort |
|---|---|---|---|
| **Leaflet.SvgShapeMarkers** ([github.com/rowanwins/Leaflet.SvgShapeMarkers](https://github.com/rowanwins/Leaflet.SvgShapeMarkers), npm `leaflet-svg-shape-markers`) ✅ | Free, open source | Ready-made shape markers: **triangle, diamond, square, circle** etc. via `L.shapeMarker(latlng, { shape: 'triangle', radius, color, fillOpacity })`. Because it extends Leaflet's Path class, the same colour/size/opacity options work — so **one shape per operator + a colour/size tweak per sub-type** is exactly its sweet spot. | **Low** — closest fit to the requirement |
| **Esri Leaflet.shapeMarkers** ([github.com/Esri/Leaflet.shapeMarkers](https://github.com/Esri/Leaflet.shapeMarkers)) | Free, open source | Fixed-size shape symbols (`xMarker`, etc.). Similar idea, fixed sizes. | Low |
| **leaflet-svgicon** ([github.com/iatkin/leaflet-svgicon](https://github.com/iatkin/leaflet-svgicon)) | Free, open source | A customisable SVG `divIcon` with **no dependencies**; includes a rhombus example; change the shape by swapping the SVG path. | Low-moderate |
| **Leaflet.ExtraMarkers** ([github.com/coryasilva/Leaflet.ExtraMarkers](https://github.com/coryasilva/Leaflet.ExtraMarkers)) | Free, open source | Polished pin-style SVG markers with an **icon inside** (e.g. a little camera glyph) + colour presets. Good if you want "pin with symbol" rather than pure geometric shapes. | Low |
| **Hand-rolled `L.divIcon` with inline SVG** | Free (built-in) | Full artistic control — draw your own bespoke shapes/variants as SVG, travels with your code, no external request, no dependency. Best for a distinctive *art* look. | Moderate (you draw them) |
| **MapMarker Studio** ([wpgeodirectory.com/mapmarkerstudio/leaflet](https://wpgeodirectory.com/mapmarkerstudio/leaflet/)) | Free web tool | Visual designer that spits out ready `L.icon`/`L.divIcon` snippets with the anchor pre-calculated — handy for generating the SVGs without maths. | N/A (a helper tool) |

**How to express sub-types as "slight variants":** pick *one* visual dimension to mean sub-type so it stays legible — e.g. **solid fill = permanent, hollow/outline = mobile**; or a small notch/dot added to the base shape for retrospective FR. With `L.divIcon` + inline SVG you control this precisely; with Leaflet.SvgShapeMarkers you'd lean on fill/outline/size options.

**Accessibility note:** shape-plus-colour (not colour alone) is the recommended approach for colour-blind readers and for print/exhibition reproduction — a genuine plus for this project, not just decoration.

### In MapLibre (only relevant if you ever switch engines)
- MapLibre handles this through its **symbol layer**: you register SVG/PNG images with `map.addImage()` and then **data-drive** which image each point uses from a property in your data (e.g. `operator`). This is powerful and fast for thousands of points, and the "different shape per category from a data field" pattern is idiomatic in MapLibre. ([MapTiler SVG icon example](https://docs.maptiler.com/sdk-js/examples/custom-points-icon-svg/))
- **But** it's only worth it if you're *already* moving to MapLibre for the Round 1 Theme A label-overlap reasons — it is **not** a reason to switch on its own. Leaflet does custom shapes perfectly well at 644 points.

### R5 bottom line
- **Easiest fit:** **Leaflet.SvgShapeMarkers** (free) — gives you triangle/diamond/square/circle out of the box, one shape per operator, with colour/fill/size tweaks for sub-types. Small add-on.
- **For a bespoke art look:** hand-draw shapes as inline SVG in **`L.divIcon`** (free, built-in, no dependency) — more effort but total control, and the variants (solid vs outline, added notch) are easy to encode.
- Keep sub-type signalling to **one** visual dimension (fill or a small added mark) so the map stays readable.
- **No engine switch needed** — MapLibre's data-driven symbol layer is nice but only relevant if you're already rebuilding on MapLibre for other reasons.

> **Big-rebuild flag:** none. Custom shapes are a free Leaflet add-on (or built-in `divIcon`). MapLibre's approach is mentioned only as a "if you've already switched" note.

---

## Round 2 — bottom line (one simplest recommendation per theme)

| Theme | Simplest recommended option | Cost | Type | Rebuild risk |
|---|---|---|---|---|
| **R1. "Pretext Library" / GPU text** | **Pretext is real & free (MIT)** — but it's a *text-measurement* tool for smooth text in panels, **not** a map fix. For the actual "overlapping labels" pain, add a free Leaflet **collision plugin** (e.g. Leaflet.LabelTextCollision). | Free | Add-on | ✅ No rebuild. (Automatic label-hiding "for free" only comes with MapLibre = rebuild, per Round 1.) |
| **R2. Cross-browser / responsive loading** | Size the map with **`svh`/`dvh`** CSS units + call Leaflet's **`invalidateSize()`** on resize/rotate. Test on your own iPhone/Mac. | Free (paid LambdaTest ~$15/mo only if you need wide device coverage) | CSS + few JS lines | ✅ No rebuild. |
| **R3. "Spotlight on London"** | **Leaflet.Mask** plugin pointed at your existing borough GeoJSON — dims everything outside London; clicks pass through. (Turf.js `mask` if you want more styling control.) | Free | Add-on | ✅ No rebuild. (Recommend *dim*, not blur. MapLibre has *less* built-in support here.) |
| **R4. Rich click-a-deployment panel + splat** | Marker → small popup teaser → **"View details" opens leaflet-sidebar-v2** with the rich content. For the 3D splat: **Luma AI free iframe** to prototype, then **SuperSplat's free self-hosted single-file export** for the owned version. | Free (SplatHost / Polycam / Luma-enterprise are paid upgrades if wanted) | Add-on (building the panel is the main effort) | ✅ No map rebuild. ⚠️ Three.js splat viewers (Spark/mkkellogg/Babylon) = more 3D dev — avoid unless already doing Three.js. |
| **R5. Custom shape markers + sub-type variants** | **Leaflet.SvgShapeMarkers** (triangle/diamond/square/circle per operator) + fill/outline/size tweaks for sub-types; or hand-drawn inline SVG in `L.divIcon` for a bespoke art look. | Free | Add-on | ✅ No rebuild. |

### The loudest flags for Round 2
1. **Almost nothing here requires a rebuild.** R2, R3, R4 (panel), and R5 are all **add-ons or CSS** on top of your current Leaflet map. Lifting the "free only" rule barely changes the recommendations — **the best options for these five themes are still free**; paid choices (LambdaTest, SplatHost, Polycam, Luma enterprise) are *conveniences*, not necessities.
2. **The one place a paid/hosted option is genuinely tempting is the Gaussian splat (R4b):** Luma's free iframe is the fastest way to see a splat live, and SplatHost (freemium) is the easiest tool-agnostic hosted embed. But the **free, self-owned** path (SuperSplat single-file export) is the right long-term answer for an archive that should own its assets — and it fits Jared's existing splat/COLMAP pipeline.
3. **Pretext was correctly remembered but is the wrong tool for the headline problem.** It's a legitimate, free, smooth-text library worth keeping for the new text-heavy detail panel — but it does **not** fix overlapping map labels. That remains either a free collision plugin (add-on) or, for the automatic-everything version, **MapLibre — still the only true "replace Leaflet" rebuild on the table** (carried over from Round 1 Theme A).
4. **The single biggest *effort* in Round 2 is not a tool choice at all — it's building the rich R4 detail panel** (laying out facts + news + embeds + photos + splot viewer). That's design/assembly work, not a risky dependency. Plan time for it; it's the centrepiece of the upgrade.

> *End of Round 2.*

