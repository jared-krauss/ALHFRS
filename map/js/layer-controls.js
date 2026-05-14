/**
 * Wires the layer toggle buttons in #layer-panel to their respective Leaflet layers.
 * Each button toggles its layer and its own .active CSS class.
 *
 * layers: { boroughs: L.layer, deployments: L.layerGroup }
 * map: L.map instance
 */
export function initControls(map, layers) {
  function wire(btnId, layer) {
    const btn = document.getElementById(btnId);
    if (!btn || !layer) return;

    let visible = true;
    btn.addEventListener('click', () => {
      visible = !visible;
      btn.classList.toggle('active', visible);
      if (visible) {
        layer.addTo(map);
      } else {
        map.removeLayer(layer);
      }
    });
  }

  wire('btn-boroughs', layers.boroughs);
  wire('btn-deployments', layers.deployments);
  // btn-news and btn-community are disabled in HTML — no handlers needed
}
