/**
 * Wires layer toggle buttons to their Leaflet layers.
 * Each button toggles its layer on/off and flips its own .active CSS class.
 *
 * layers: { boroughs, met, btp, private } — null values are safely skipped
 * map: L.map instance
 */
export function initControls(map, layers) {
  function wire(btnId, layer) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    // If layer failed to load, mark button as unavailable
    if (!layer) {
      btn.disabled = true;
      btn.title = 'Data not loaded';
      return;
    }

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
  wire('btn-met',      layers.met);
  wire('btn-btp',      layers.btp);
  wire('btn-private',  layers.private);
  // btn-news and btn-community are disabled in HTML — no handlers needed
}
