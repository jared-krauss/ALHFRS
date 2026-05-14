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

  // Fetch borough GeoJSON and deployment data in parallel
  let boroughsGeoJSON, metData;
  try {
    [boroughsGeoJSON, metData] = await Promise.all([
      fetch(DATA_PATHS.boroughs).then(r => {
        if (!r.ok) throw new Error(`Borough GeoJSON fetch failed: ${r.status}`);
        return r.json();
      }),
      fetch(DATA_PATHS.metDeployments).then(r => {
        if (!r.ok) throw new Error(`Deployment data fetch failed: ${r.status}`);
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

  // Layers
  const boroughLayer = createBoroughLayer(map, boroughsGeoJSON);
  const deploymentLayer = createDeploymentLayer(metData.deployments);
  deploymentLayer.addTo(map);

  // Controls and legend
  initControls(map, { boroughs: boroughLayer, deployments: deploymentLayer });
  createLegend(map);
}

init();
