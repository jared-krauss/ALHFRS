import { QUALITY_COLORS, QUALITY_LABELS } from './config.js';

export function createLegend(map) {
  const legend = L.control({ position: 'bottomleft' });

  legend.onAdd = () => {
    const div = L.DomUtil.create('div', 'map-legend');
    div.innerHTML = `
      <div class="legend-title">Data confidence</div>
      ${Object.entries(QUALITY_COLORS).map(([key, color]) => `
        <div class="legend-item">
          <span class="legend-dot" style="background:${color}"></span>
          <span class="legend-label">${key}</span>
        </div>
      `).join('')}
      <div class="legend-note">ALHFRS · v0 prototype</div>
    `;
    return div;
  };

  legend.addTo(map);
  return legend;
}
