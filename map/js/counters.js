/* =====================================================================
   counters.js — running counters for the ALHFRS map
   ---------------------------------------------------------------------
   Pure aggregation logic. No DOM, no MapLibre, no fetch — so it can be
   verified directly by `node --test` without a browser (see tests/).

   Spec:  _review/INTRO-COPY-SPEC.md  (Jared's answers, 2026-07-03)
   Plan:  _review/INTRO-COUNTERS-BUILD-PLAN.md  (decisions, 2026-07-29)

   NOTHING here is a hard-coded total. Every figure is derived from the
   records passed in, so the map updates itself as the dataset grows.
   tests/counters.test.js has an explicit test that proves this.

   ── Dependency note (SOP #6) ─────────────────────────────────────────
   Consumed by: index.html (the MapLibre map) only.
   Depends on: the deployment JSON *schema* — `operator`, `lat`/`lon`,
     `outcome_*`, and an optional `country` field that does not exist yet
     (REGION-ASSIGNMENT-SPEC.md adds it; this module already prefers it,
     so that spec upgrades the counters with no change here).
     Renaming any of those fields breaks this file.
     Schema contract holders: scripts/validate-dataset.py, data/README.md.
     scripts/verify-counters.py re-implements these sums independently as
     a cross-check — keep the two in step.

   Loaded as a classic script (sets window.ALHFRSCounters) rather than an
   ES module on purpose: index.html has inline onclick handlers calling
   script-scoped functions (toggleList, openPanel), which type="module"
   would break. The UMD wrapper keeps it require()-able for tests.
   ===================================================================== */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.ALHFRSCounters = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ---------- config: everything tunable lives here ----------
     Change the threshold, add a force, reorder countries or drop a
     metric without touching any logic below. */
  const CONFIG = {
    // A single operator needs this many deployments in a country before it
    // gets its own line; below this it pools into "Rest of <country>".
    promotionThreshold: 6,

    // Shown in this order, always — including at zero. An empty Scotland
    // line is a deliberate statement, not a gap.
    countries: ['England', 'Wales', 'Scotland', 'Northern Ireland'],

    // Operators whose jurisdiction is a single country. `null` = UK-wide or
    // location-dependent (private operators), so country comes from
    // coordinates instead. Unlisted operators fall through the same way.
    operatorCountry: {
      'Metropolitan Police': 'England',
      'South Wales Police': 'Wales',
      'British Transport Police': null,
      'Facewatch / Sainsbury\'s': null,
      // ready for data that does not exist yet:
      'Police Scotland': 'Scotland',
      'Police Service of Northern Ireland': 'Northern Ireland',
    },

    // Reused from scripts/validate-dataset.py — one source of truth.
    londonBBox: { latMin: 51.28, latMax: 51.69, lonMin: -0.51, lonMax: 0.34 },

    metrics: [
      { key: 'outcome_faces_scanned', label: 'Faces scanned' },
      { key: 'outcome_alerts', label: 'Alerts' },
      { key: 'outcome_true_alerts', label: 'Confirmed matches' },
      { key: 'outcome_false_alerts', label: 'False positives' },
      { key: 'outcome_arrests', label: 'Arrests' },
    ],

    unassignedLabel: 'Unassigned',
    restLabel: (country) => 'Rest of ' + country,
  };

  /* ---------- country derivation ----------
     Priority order. Guessing wrong is worse than admitting we do not
     know, so anything undecidable returns Unassigned and is shown. */
  function deriveCountry(rec, cfg) {
    cfg = cfg || CONFIG;

    // 1. An explicit field wins — nothing has one yet, but this means the
    //    region spec's backfill upgrades the counters automatically.
    if (rec && typeof rec.country === 'string' && rec.country.trim()) {
      return rec.country.trim();
    }

    // 2. Single-jurisdiction operator.
    const mapped = rec && cfg.operatorCountry[rec.operator];
    if (mapped) return mapped;

    // 3. Coordinates. Only London is claimed here — it is the one boundary
    //    this project already defines. Everything else stays honest.
    const b = cfg.londonBBox;
    const lat = rec && typeof rec.lat === 'number' ? rec.lat : null;
    const lon = rec && typeof rec.lon === 'number' ? rec.lon : null;
    if (lat !== null && lon !== null &&
        lat >= b.latMin && lat <= b.latMax && lon >= b.lonMin && lon <= b.lonMax) {
      return 'England';
    }

    // 4. Not known.
    return cfg.unassignedLabel;
  }

  /* ---------- LFR filter ----------
     Retrospective FR is a different technology with a different schema and
     no numeric outcomes (CLAUDE.md invariant: keep LFR/RFR/OIFR distinct).
     Counting it here would be a category error. */
  function isLFR(rec) {
    if (!rec) return false;
    // Explicit wins. Map feature properties are flattened, so the shape-sniffing
    // below cannot see footage_* — index.html sets `tech` for exactly this reason.
    if (rec.tech) return String(rec.tech).toUpperCase() === 'LFR';
    if (rec.footage_lat !== undefined || rec.footage_lon !== undefined) return false;
    if (rec.police_force !== undefined && rec.operator === undefined) return false;
    return true;
  }

  /* ---------- metric aggregation ----------
     A recorded 0 is data, not a gap — it means "this deployment genuinely
     had none". Only null/undefined counts as unknown. That distinction is
     the whole honesty story for false positives (386 real zeros vs 228
     genuinely unpublished). */
  function aggregate(records, cfg) {
    cfg = cfg || CONFIG;
    const out = { deployments: 0, metrics: {} };
    for (const m of cfg.metrics) {
      out.metrics[m.key] = { label: m.label, total: 0, reported: 0, zero: 0, unknown: 0 };
    }
    for (const rec of records || []) {
      if (!isLFR(rec)) continue;
      out.deployments++;
      for (const m of cfg.metrics) {
        const slot = out.metrics[m.key];
        const v = rec[m.key];
        if (v === null || v === undefined || v === '') { slot.unknown++; continue; }
        const n = Number(v);
        if (!Number.isFinite(n)) { slot.unknown++; continue; }
        slot.reported++;
        if (n === 0) slot.zero++;
        slot.total += n;
      }
    }
    return out;
  }

  /* ---------- geography grouping ----------
     Every country in CONFIG.countries always appears, even at zero.
     Unassigned only appears if it is non-empty. */
  function groupByCountry(records, cfg) {
    cfg = cfg || CONFIG;
    const lfr = (records || []).filter(isLFR);

    const buckets = new Map();
    const ensure = (name) => {
      if (!buckets.has(name)) buckets.set(name, new Map());
      return buckets.get(name);
    };
    for (const c of cfg.countries) ensure(c);

    for (const rec of lfr) {
      const country = deriveCountry(rec, cfg);
      const byOp = ensure(country);
      const op = (rec && rec.operator) || 'Unknown operator';
      if (!byOp.has(op)) byOp.set(op, []);
      byOp.get(op).push(rec);
    }

    const countries = [];
    const order = cfg.countries.slice();
    for (const name of buckets.keys()) if (!order.includes(name)) order.push(name);

    for (const name of order) {
      const byOp = buckets.get(name);
      if (!byOp) continue;
      if (name === cfg.unassignedLabel && byOp.size === 0) continue;

      const promoted = [];
      const pooled = [];
      for (const [op, recs] of byOp.entries()) {
        (recs.length >= cfg.promotionThreshold ? promoted : pooled).push({ operator: op, records: recs });
      }
      promoted.sort((a, b) => b.records.length - a.records.length || a.operator.localeCompare(b.operator));

      const pooledRecords = pooled.reduce((acc, p) => acc.concat(p.records), []);
      const all = [].concat(...Array.from(byOp.values()));

      const lines = promoted.map((p) => ({
        label: p.operator,
        deployments: p.records.length,
        promoted: true,
        summary: aggregate(p.records, cfg),
      }));
      if (pooledRecords.length) {
        lines.push({
          label: cfg.restLabel(name),
          deployments: pooledRecords.length,
          promoted: false,
          operators: pooled.map((p) => p.operator).sort(),
          summary: aggregate(pooledRecords, cfg),
        });
      }

      countries.push({
        country: name,
        deployments: all.length,
        summary: aggregate(all, cfg),
        lines,
      });
    }
    return countries;
  }

  /* ---------- top-level ---------- */
  function summarise(records, cfg) {
    cfg = cfg || CONFIG;
    const lfr = (records || []).filter(isLFR);
    return {
      uk: aggregate(lfr, cfg),
      countries: groupByCountry(lfr, cfg),
      threshold: cfg.promotionThreshold,
    };
  }

  /* ---------- presentation helpers ---------- */
  function formatNumber(n) {
    return Number(n || 0).toLocaleString('en-GB');
  }

  /* What to actually print for a metric.
     If NOTHING was reported, printing "0" asserts a fact we do not have —
     it reads as "zero faces were scanned" when the truth is "nobody published
     a figure". South Wales is the live example: 14 deployments, no
     faces-scanned figure anywhere. Accuracy over polish.

     "N/A" not an em dash — Jared, 2026-08-02: "that's more immediately
     recognizable as meaning not available". */
  const NOT_AVAILABLE = 'N/A';

  function displayValue(slot) {
    if (!slot || slot.reported === 0) return NOT_AVAILABLE;
    return formatNumber(slot.total);
  }

  /* Plain-English note about what is missing, built from the real counts.
     Never asserts precision the data cannot support. */
  function coverageNote(slot, deployments) {
    if (!slot) return '';
    if (deployments > 0 && slot.reported === 0) {
      return 'No figure published by any of these ' + formatNumber(deployments) +
             ' deployments, so no total can be shown.';
    }
    if (slot.reported === deployments && deployments > 0) {
      return 'Reported by all ' + formatNumber(deployments) + ' deployments.';
    }
    const parts = [
      'Reported by ' + formatNumber(slot.reported) + ' of ' + formatNumber(deployments) + ' deployments',
    ];
    if (slot.zero > 0) {
      parts.push(formatNumber(slot.zero) + ' of those recorded zero — a real figure, not a gap');
    }
    if (slot.unknown > 0) {
      parts.push(formatNumber(slot.unknown) + ' published nothing, so the true total is higher');
    }
    return parts.join('. ') + '.';
  }

  return {
    CONFIG,
    deriveCountry,
    isLFR,
    aggregate,
    groupByCountry,
    summarise,
    formatNumber,
    displayValue,
    coverageNote,
  };
});
