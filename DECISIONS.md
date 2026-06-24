# Decisions — ALHFRS

> Single home for this repo's decisions. **Do not put decisions in CLAUDE.md** — it is
> auto-loaded context and must stay stable instructions, not an append-only ledger. CLAUDE.md
> carries only a pointer to here.
>
> **Entry format:** `- **<slug>** [tags] (YYYY-MM-DD): chose X over Y because <root cause>.`
> Append newest at the top. Supersede with strikethrough + a new entry; never rewrite history.
> Read on demand — not auto-loaded.

## 2026-06

- **map-engine-maplibre** [ALHFRS] (2026-06-23): chose a from-scratch MapLibre GL JS rebuild over upgrading the existing Leaflet map, because Jared prioritised a long-term GPU/3D foundation over the lower-risk Leaflet path (informed override — the assistant's evidence-based recommendation was to stay on Leaflet).
- **data-quality-into-detail-panel** [ALHFRS] (2026-06-23): chose to show a record's data-quality only inside the click-details panel over keeping it in the always-on legend, because the legend treatment (and the "ring brightness = recency" cue) was confusing and ineffective.

## 2026-05

- **2023-24-pdf-extract** [ALHFRS] (2026-05-30): abandoned Hermes3:8b extraction in favour of Gemini, because Hermes3 hallucinates regular-interval records on pages containing watchlist-criteria sections.
- **data-quality-enum** [ALHFRS] (2026-05-30): three values (confirmed/approximate/unverified) over two, because "approximate" captures inferred-but-sourced data that is neither fully verified nor fabricated.
