# Decisions — ALHFRS

> Single home for this repo's decisions. **Do not put decisions in CLAUDE.md** — it is
> auto-loaded context and must stay stable instructions, not an append-only ledger. CLAUDE.md
> carries only a pointer to here.
>
> **Entry format:** `- **<slug>** [tags] (YYYY-MM-DD): chose X over Y because <root cause>.`
> Append newest at the top. Supersede with strikethrough + a new entry; never rewrite history.
> Read on demand — not auto-loaded.

## 2026-06

- **operator-colours-and-private-shape-locked** [ALHFRS] (2026-06-28): chose real Brandfetch-sourced brand colours (Met International Klein Blue #0032A0; BTP Smalt #003399) over the earlier placeholder candidates, and locked Private to Sainsbury's official orange #F06C00 + square, because Jared wants markers tied to each operator's actual identity rather than an invented palette. Met/BTP fills are now nearly indistinguishable at marker size — shape carries the differentiation, not colour.
- **port-of-hull-included** [ALHFRS] (2026-06-28): chose to include the out-of-Greater-London Port of Hull trial (now `lfr-672`) in the merged 2016-2019 batch over excluding it as out-of-scope, because it's part of the Met's own officially documented 10-trial set and Jared confirmed wanting it included.
- **rfr-colour-operator-fill-plus-outline** [ALHFRS] (2026-06-28): chose RFR markers to keep the operator's own fill colour with a distinct standout outline ring (candidates: neon red #FF1744 / electric magenta #FF2DF5) over a fully separate RFR colour or a same-colour hollow ring, because it preserves "which operator" at a glance while still flagging "retrospective" unambiguously.
- **extend-timeline-to-2016** [ALHFRS] (2026-06-28): chose to extend the deployment dataset and time-animation start back to 2016-2019 (the Met's original LFR trial period) over keeping 2020 as the documented start, per Jared's request; sourcing/verification is in progress, not yet merged.
- **a11y-fixes-superseded-by-maplibre** [ALHFRS] (2026-06-27): chose to let the MapLibre rebuild supersede the unmerged Leaflet accessibility fixes (focus outlines, ARIA, shape glyphs) over porting them into the live map first, because Phase 0/1 of the rebuild reimplements the same markup from scratch anyway.
- **map-engine-maplibre** [ALHFRS] (2026-06-23): chose a from-scratch MapLibre GL JS rebuild over upgrading the existing Leaflet map, because Jared prioritised a long-term GPU/3D foundation over the lower-risk Leaflet path (informed override — the assistant's evidence-based recommendation was to stay on Leaflet).
- **data-quality-into-detail-panel** [ALHFRS] (2026-06-23): chose to show a record's data-quality only inside the click-details panel over keeping it in the always-on legend, because the legend treatment (and the "ring brightness = recency" cue) was confusing and ineffective.

## 2026-05

- **2023-24-pdf-extract** [ALHFRS] (2026-05-30): abandoned Hermes3:8b extraction in favour of Gemini, because Hermes3 hallucinates regular-interval records on pages containing watchlist-criteria sections.
- **data-quality-enum** [ALHFRS] (2026-05-30): three values (confirmed/approximate/unverified) over two, because "approximate" captures inferred-but-sourced data that is neither fully verified nor fabricated.
