# ALHFRS Map — Upgrade Plan (draft for Jared's approval)

Built from Jared's feedback (`MAP-FEEDBACK.md`) + tool research (`MAP-RESEARCH.md`).
Scope = **the core map only.** Data-viz ideas are a separate later track (Jared's steer).
Status: **awaiting Jared's go-ahead**, especially on the foundation decision below.

## Foundation decision — FINAL (Jared's call, 2026-06-23): rebuild on MapLibre GL JS

**Decision: build the new map from scratch on MapLibre GL JS, not on the current Leaflet engine.**

This section is written to be honest about how that decision was reached, because the recommendation
and the decision differ — and that's deliberate, not a mistake.

**What I (the assistant) actually recommended:** *stay on Leaflet.* The round-2 research found that
lifting the "free only" rule barely mattered, and that **every single thing Jared asked for is
achievable on the current Leaflet engine with free add-ons or CSS** — at far lower risk and effort
than a from-scratch rebuild. For one of Jared's key wants (the "spotlight on London"), MapLibre
actually has *less* built-in support than Leaflet. On the evidence, upgrading the existing Leaflet
map was the lower-risk, faster, cheaper path.

What each want maps to on the current Leaflet engine (all free, for the record):
- overlapping labels → `Leaflet.LabelTextCollision`; responsive → CSS `svh/dvh` + `invalidateSize()`;
  London spotlight → `Leaflet.Mask` (uses the borough GeoJSON we already have); detail panel →
  `leaflet-sidebar-v2`; operator shapes → `Leaflet.SvgShapeMarkers`; animation → `Leaflet.timeline`;
  splat embed → engine-independent (Luma iframe to prototype, SuperSplat free self-host to own).

**What Jared decided, and why:** Jared chose **MapLibre anyway** — an informed override, not a
mistaken premise. His reasoning is long-term: MapLibre renders the whole map on the GPU, which gives
a smoother, more polished, more "modern" feel for a design-forward documentary-art piece, and lays a
foundation for future 3D / "space-time cube" data-visualisation work that Leaflet cannot do natively.
He is knowingly trading **higher upfront cost and risk** (a full rebuild) for that **long-term GPU/3D
foundation**. That is a legitimate priority call: he values where the project is going over getting
everything working in the cheapest way today.

**Honest framing for whoever builds this:** several features below would have been *cheaper and
lower-risk* as free Leaflet plugins. We are doing them on MapLibre by choice. Where that's true, the
handoff doc flags it, so nobody mistakes the harder path for a necessary one. The two genuinely
expensive things — the **data** and the **design system** (layout, hierarchy, shapes, colour, copy) —
are engine-independent and carry straight over, so choosing MapLibre does **not** waste that work.

> Full detail for a builder: see [`MAP-UPGRADE-HANDOFF.md`](MAP-UPGRADE-HANDOFF.md).

## Phase 0 — Design foundations (engine-independent; do first)
- Lock the **visual system**: operator = distinct **shape** scheme (circle/triangle/square or
  better), with reserved future *variants* for permanent cameras + retrospective FR; colour palette;
  typography. Markers will use the shapes (fixes the legend-vs-map mismatch, feedback #8/#17).
- Redesign the **legend**: collapsible; **data-quality removed** from it (moves to click-details);
  drop the "ring brightness = recency" idea entirely (#9, #10).
- Establish real **UX hierarchy + grid** (#12, #13) — I propose, Jared's eye refines.
- Finalise specific tools from research (splat viewer, mask method) once round-2 research lands.

## Phase 1 — Rebuild core map on MapLibre (parity + the basics fixed)
- London base map; load the same deployment data + clustering.
- **Operator shapes on the actual markers** + colour.
- **Responsive + cross-browser** (#1, #15): proper portrait/landscape/tablet/desktop; panels reflow;
  no text overlap (MapLibre auto-manages label collisions).
- **Spotlight on London** (#20): grey/blur/defocus outside Greater London + a better default zoom (#5).
- **Prominent intro** that draws the eye to what the dots mean (#5, #19).
- Crowded **bottom strip** re-spaced (#7); **legend** collapsible (#3); **filter buttons** with a
  stark on-state that clears instantly (#2 — rebuilt fresh, so the old "stuck highlight" can't recur);
  **menu/news layering** correct (#4).

## Phase 2 — Click-to-reveal detail panel (build the frame, fill over time) (#18)
- Click a deployment → panel showing what exists now: deployment **facts + source link + related
  news**, with clearly-marked empty slots ready for **Jared's photos, community submissions, and a
  Gaussian-splat embed** (wired but dormant until content exists).

## Phase 3 — Time animation (play/stop, off by default) (#6)
- A play button animates dots **accumulating over time**, ending on the full picture; loops.
- NOTE: data currently starts **2020** (earliest records Feb 2020), not 2016. The animation begins
  where the data begins; if Jared has/plans pre-2020 records we extend the timeline back.

## Future track (noted, NOT this round)
- Shape variants (permanent cameras, RFR); community-submission workflow; splat capture; and the
  separate data-viz "other windows/maps" track.

## How we work / verification
- Build in the sandbox; current map stays live; nothing merges until Jared approves; commit
  checkpoints as we go (crash-safe). Verify on Jared's phone over Tailscale (portrait + landscape),
  plus desktop, before any swap.

## Open item
- **"Pretext Library"** (Jared's text-rendering reference) — research identifying it; but MapLibre
  already solves the label/layout-cost problem natively, so this may be moot. Will confirm.
