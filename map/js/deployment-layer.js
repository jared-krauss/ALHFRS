import { QUALITY_COLORS } from './config.js';

function buildPopupHTML(d) {
  const dateStr = d.date_end && d.date_end !== d.date_start
    ? `${d.date_start} – ${d.date_end}`
    : d.date_start;

  const operatorLine = d.operator
    ? `<div class="popup-stat"><span class="popup-label">Operator</span>${d.operator}</div>`
    : '';

  const vendorLine = d.vendor
    ? `<div class="popup-stat"><span class="popup-label">Vendor</span>${d.vendor}</div>`
    : '';

  const facesLine = d.faces_scanned != null
    ? `<div class="popup-stat"><span class="popup-label">Faces scanned</span>${Number(d.faces_scanned).toLocaleString()}</div>`
    : '';

  const arrestsLine = d.outcome_arrests != null
    ? `<div class="popup-stat"><span class="popup-label">Arrests</span>${d.outcome_arrests}</div>`
    : '';

  const alertsLine = d.outcome_alerts != null
    ? `<div class="popup-stat"><span class="popup-label">Alerts</span>${d.outcome_alerts}</div>`
    : '';

  const sourceLine = d.source_url
    ? `<a class="popup-source" href="${d.source_url}" target="_blank" rel="noopener">Source ↗</a>`
    : `<span></span>`;

  const qualityColor = QUALITY_COLORS[d.data_quality] ?? QUALITY_COLORS.unverified;
  const deployType = d.deployment_type ? ` · ${d.deployment_type}` : '';

  return `
    <div class="lfr-popup">
      <div class="popup-title">${d.location_name}</div>
      <div class="popup-meta">${d.borough} · ${dateStr}${deployType}</div>
      <div class="popup-purpose">${d.stated_purpose}</div>
      ${operatorLine}${vendorLine}${facesLine}${arrestsLine}${alertsLine}
      ${d.notes ? `<div class="popup-notes">${d.notes}</div>` : ''}
      <div class="popup-footer">
        <span class="popup-quality" style="color:${qualityColor}">● ${d.data_quality}</span>
        ${sourceLine}
      </div>
    </div>
  `;
}

export function createDeploymentLayer(deployments) {
  const cluster = L.markerClusterGroup({
    iconCreateFunction(c) {
      const count = c.getChildCount();
      const size = count < 10 ? 34 : count < 50 ? 40 : 46;
      return L.divIcon({
        html: `<div class="alhfrs-cluster-inner">${count}</div>`,
        className: 'alhfrs-cluster',
        iconSize: L.point(size, size),
        iconAnchor: L.point(size / 2, size / 2),
      });
    },
    maxClusterRadius: 50,
    spiderfyOnMaxZoom: true,
    showCoverageOnHover: false,
    animate: true,
  });

  const markers = [];

  for (const d of deployments) {
    if (!d.lat || !d.lon) continue;
    const color = QUALITY_COLORS[d.data_quality] ?? QUALITY_COLORS.unverified;
    const year = d.date_start ? d.date_start.slice(0, 4) : null;

    const marker = L.circleMarker([d.lat, d.lon], {
      radius: 8,
      fillColor: color,
      color: '#1a1a2e',
      weight: 1.5,
      fillOpacity: 0.9,
      year,
      deploymentId: d.id,
    }).bindPopup(buildPopupHTML(d), { maxWidth: 320 });

    markers.push(marker);
    cluster.addLayer(marker);
  }

  // Expose for year-filter access in main.js
  cluster._alhfrsMarkers = markers;

  return cluster;
}
