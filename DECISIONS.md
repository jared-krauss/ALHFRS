# Decisions — ALHFRS

> Single home for this repo's decisions. **Do not put decisions in CLAUDE.md** — it is
> auto-loaded context and must stay stable instructions, not an append-only ledger. CLAUDE.md
> carries only a pointer to here.
>
> **Entry format:** `- **<slug>** [tags] (YYYY-MM-DD): chose X over Y because <root cause>.`
> Append newest at the top. Supersede with strikethrough + a new entry; never rewrite history.
> Read on demand — not auto-loaded.

## 2026-06

- **validator-incidents-schema-fix** [ALHFRS] (2026-06-30): confirmed the `b480cc8` fix is live and correct — `validate-dataset.py` now detects `incidents[]` files, passes `is_incident=True` through to `check_record()`, and skips near-duplicate/cluster checks for them. Verified against the live `retrospective-fr.json` (5 records, 0 errors, 6 expected warnings all legitimate). No further changes needed.
- **met-btp-shapes-via-external-design** [ALHFRS] (2026-06-29): superseded the phone mockup's Met/BTP shape picks (including checker-band-shield) — chose to derive both shapes from their real badge silhouettes via a separate Claude design session (Jared supplies the Brandfetch reference images), because Jared judged the mockup's hand-drawn options oversimplified and not actually tracing the two forces' real, visually distinct badges. RFR ring colour (neon red `#FF1744`) is unaffected and stays confirmed.
- **scope-widened-beyond-london** [ALHFRS] (2026-06-28): chose to show nationally-significant out-of-London deployments (Wales, Sunderland) with regions ungreying themselves once historically relevant and staying lit, over keeping the spotlight static to Greater London only, because Jared wants London's story situated in its national context. Confirmed by Jared, no longer draft.
~~- **met-shape-checker-band-shield, rfr-ring-neon-red** [ALHFRS] (2026-06-28): chose a shield with a small chequered band (echoing the Sillitoe tartan) over a plain shield for Met, and neon red `#FF1744` over electric magenta for the RFR outline ring, per Jared's picks on the phone mockup.~~ *(Met-shape half superseded 2026-06-29 — see `met-btp-shapes-via-external-design` above. RFR-ring half still stands.)*
- **merged-wales-and-sunderland-records** [ALHFRS] (2026-06-28): added South Wales Police as a new operator (`data/deployments/south-wales-police-lfr.json`, 14 records, swp-001..015 minus the unverified swp-010) and one Northumbria RFR record (`rfr-005`) over leaving them in staging, because Jared confirmed both — well-sourced, validator-clean, and the Wales batch fills in the deployment data behind the existing `legal-001` Bridges case record.
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
