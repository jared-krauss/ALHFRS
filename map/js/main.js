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

  let activeYear = null;

  function applyYearFilter(year) {
    for (const cluster of clusterLayers) {
      const allMarkers = cluster._alhfrsMarkers;
      if (!allMarkers) continue;
      cluster.clearLayers();
      for (const marker of allMarkers) {
        if (!year || marker.options.year === year) {
          cluster.addLayer(marker);
        }
      }
    }
  }

  function buildTimeline() {
    const strip = document.getElementById('timeline-strip');
    if (!strip) return;

    const years = ['2020', '2021', '2022', '2023', '2024', '2025', '2026'];

    // Count deployments per year
    const counts = {};
    for (const d of allDeployments) {
      const y = d.date_start?.slice(0, 4);
      if (y) counts[y] = (counts[y] || 0) + 1;
    }
    const maxCount = Math.max(...Object.values(counts), 1);

    strip.innerHTML = '<div class="tl-label">YEAR</div>';

    for (const year of years) {
      const count = counts[year] || 0;
      // Scale bar height: non-zero years get at least 20% of max height
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
        applyYearFilter(activeYear);
        // Update active state styling
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
