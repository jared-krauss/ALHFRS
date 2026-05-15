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
  const boroughLayer   = createBoroughLayer(map, boroughsGeoJSON);
  const metLayer       = createDeploymentLayer(metData.deployments);
  const btpLayer       = btpData     ? createDeploymentLayer(btpData.deployments)     : null;
  const privateLayer   = privateData ? createDeploymentLayer(privateData.deployments) : null;

  metLayer.addTo(map);
  if (btpLayer)     btpLayer.addTo(map);
  if (privateLayer) privateLayer.addTo(map);

  // Controls and legend
  initControls(map, {
    boroughs:  boroughLayer,
    met:       metLayer,
    btp:       btpLayer,
    private:   privateLayer,
  });
  createLegend(map);
}

init();
