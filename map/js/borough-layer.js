import { BOROUGH_STYLE } from './config.js';

export function createBoroughLayer(map, geojsonData) {
  const layer = L.geoJSON(geojsonData, {
    style: BOROUGH_STYLE,
    onEachFeature(feature, featureLayer) {
      featureLayer.bindTooltip(feature.properties.name, {
        sticky: true,
        className: 'borough-tooltip',
      });
    },
  });
  layer.addTo(map);
  return layer;
}
