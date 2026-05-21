import { TILE_URL, TILE_OPTIONS, MAP_CENTER, MAP_ZOOM, DATA_PATHS } from './config.js';
import { createBoroughLayer } from './borough-layer.js';
import { createDeploymentLayer } from './deployment-layer.js';
import { initControls } from './layer-controls.js';
import { createLegend } from './legend.js';

async function init() {
  // Map
  const map = L.map('map', { zoomControl: false, attributionControl: false })
    .setView(MAP_CENTER, MAP_ZOOM);

  L.control.zoom({ position: 'topright' }).addTo(map);
  L.tileLayer(TILE_URL, TILE_OPTIONS).addTo(map);

  // Fetch all data sources in parallel; non-critical sources degrade gracefully
  let boroughsGeoJSON, metData, btpData, privateData;
  try {
    [boroughsGeoJSON, metData] = await Promise.all([
      fetch(DATA_PATHS.boroughs).then(r => {
        if (!r.ok) throw new Error(`Borough GeoJSON fetch failed: ${r.status}`);
        return r.json();
      }),
      fetch(DATA_PATHS.metDeployments).then(r => {
        if (!r.ok) throw new Error(`Met deployment data fetch failed: ${r.status}`);
        return r.json();
      }),
    ]);
  } catch (err) {
    console.error('ALHFRS data load error:', err);
    document.getElementById('load-error').textContent =
      'Failed to load map data. Make sure you are serving from D:\\Dev\\ALHFRS\\ (not file://).';
    document.getElementById('load-error').style.display = 'block';
    return;
  }

  // Optional layers — fail silently if files missing
  [btpData, privateData] = await Promise.all([
    fetch(DATA_PATHS.btpDeployments).then(r => r.ok ? r.json() : null).catch(() => null),
    fetch(DATA_PATHS.privateDeployments).then(r => r.ok ? r.json() : null).catch(() => null),
  ]);

  // Layers
  const boroughLayer = createBoroughLayer(map, boroughsGeoJSON);
  const metLayer     = createDeploymentLayer(metData.deployments);
  const btpLayer     = btpData     ? createDeploymentLayer(btpData.deployments)     : null;
  const privateLayer = privateData ? createDeploymentLayer(privateData.deployments) : null;

  metLayer.addTo(map);
  if (btpLayer)     btpLayer.addTo(map);
  if (privateLayer) privateLayer.addTo(map);

  // Controls and legend
  initControls(map, {
    boroughs: boroughLayer,
    met:      metLayer,
    btp:      btpLayer,
    private:  privateLayer,
  });
  createLegend(map);

  // ── Timeline strip ────────────────────────────────────────────────────────

  const allDeployments = [
    ...metData.deployments,
    ...(btpData     ? btpData.deployments     : []),
    ...(privateData ? privateData.deployments : []),
  ];

  // All cluster layers that support year-filtering
  const clusterLayers = [metLayer, btpLayer, privateLayer].filter(Boolean);

  let activeYear    = null;
  let activeBorough = null;

  function countVisible() {
    let n = 0;
    for (const cluster of clusterLayers) {
      const allMarkers = cluster._alhfrsMarkers;
      if (!allMarkers) continue;
      for (const marker of allMarkers) {
        const yearOk    = !activeYear    || marker.options.year    === activeYear;
        const boroughOk = !activeBorough || marker.options.borough === activeBorough;
        if (yearOk && boroughOk) n++;
      }
    }
    return n;
  }

  function applyFilters() {
    for (const cluster of clusterLayers) {
      const allMarkers = cluster._alhfrsMarkers;
      if (!allMarkers) continue;
      cluster.clearLayers();
      for (const marker of allMarkers) {
        const yearOk    = !activeYear    || marker.options.year    === activeYear;
        const boroughOk = !activeBorough || marker.options.borough === activeBorough;
        if (yearOk && boroughOk) cluster.addLayer(marker);
      }
    }
    const countEl = document.getElementById('tl-total-count');
    if (countEl) countEl.textContent = `${countVisible().toLocaleString()} deployments`;
  }

  function buildTimeline() {
    const strip = document.getElementById('timeline-strip');
    if (!strip) return;

    const years = ['2020', '2021', '2022', '2023', '2024', '2025', '2026'];

    // Count deployments per year (total, ignoring borough filter for bar heights)
    const counts = {};
    for (const d of allDeployments) {
      const y = d.date_start?.slice(0, 4);
      if (y) counts[y] = (counts[y] || 0) + 1;
    }
    const maxCount = Math.max(...Object.values(counts), 1);

    // Borough list (sorted by frequency)
    const boroughCounts = {};
    for (const d of allDeployments) {
      if (d.borough) boroughCounts[d.borough] = (boroughCounts[d.borough] || 0) + 1;
    }
    const boroughs = Object.entries(boroughCounts)
      .sort((a, b) => b[1] - a[1])
      .map(([b]) => b);

    strip.innerHTML = '';

    // Left: total count
    const totalCount = document.createElement('div');
    totalCount.id = 'tl-total-count';
    totalCount.className = 'tl-label';
    totalCount.style.cssText = 'min-width:110px; color:#6b7fa8; font-size:10px; font-weight:600; letter-spacing:0.04em; align-self:center;';
    totalCount.textContent = `${allDeployments.length.toLocaleString()} deployments`;
    strip.appendChild(totalCount);

    // Borough select
    const boroughWrap = document.createElement('div');
    boroughWrap.style.cssText = 'align-self:center; margin-right:16px; flex-shrink:0;';
    const boroughSel = document.createElement('select');
    boroughSel.id = 'borough-select';
    boroughSel.innerHTML = `<option value="">All boroughs</option>` +
      boroughs.map(b => `<option value="${b}">${b} (${boroughCounts[b]})</option>`).join('');
    boroughSel.addEventListener('change', () => {
      activeBorough = boroughSel.value || null;
      applyFilters();
    });
    boroughWrap.appendChild(boroughSel);
    strip.appendChild(boroughWrap);

    // Divider
    const div = document.createElement('div');
    div.className = 'tl-label';
    div.style.cssText = 'margin-right:8px;';
    div.textContent = 'YEAR';
    strip.appendChild(div);

    for (const year of years) {
      const count = counts[year] || 0;
      const pct   = count > 0 ? Math.max(0.2, count / maxCount) : 0;
      const barH  = count > 0 ? Math.round(pct * 36) : 2;

      const col = document.createElement('div');
      col.className = 'tl-col';
      col.dataset.year = year;
      col.setAttribute('title', `${year}: ${count} deployment${count !== 1 ? 's' : ''}`);
      if (count === 0) col.style.cursor = 'default';

      col.innerHTML = `
        <div class="tl-count">${count > 0 ? count : ''}</div>
        <div class="tl-bar" style="height:${barH}px"></div>
        <div class="tl-year">${year}</div>
      `;

      col.addEventListener('click', () => {
        if (count === 0) return;
        activeYear = activeYear === year ? null : year;
        applyFilters();
        strip.querySelectorAll('.tl-col').forEach(el => {
          el.classList.toggle('tl-active', el.dataset.year === activeYear);
        });
      });

      strip.appendChild(col);
    }
  }

  buildTimeline();
}

init();
