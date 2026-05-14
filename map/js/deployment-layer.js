import { QUALITY_COLORS } from './config.js';

function buildPopupHTML(d) {
  const dateStr = d.date_end && d.date_end !== d.date_start
    ? `${d.date_start} – ${d.date_end}`
    : d.date_start;

  const arrestsLine = d.outcome_arrests !== null
    ? `<div class="popup-stat">Arrests recorded: <strong>${d.outcome_arrests}</strong></div>`
    : '';

  const claimedLine = d.claimed_reduction
    ? `<div class="popup-stat">Claimed reduction: ${d.claimed_reduction}</div>`
    : '';

  const sourceLine = d.source_url
    ? `<a class="popup-source" href="${d.source_url}" target="_blank" rel="noopener">Source ↗</a>`
    : '';

  const qualityColor = QUALITY_COLORS[d.data_quality] ?? QUALITY_COLORS.unverified;
  const deployType = d.deployment_type ? `· ${d.deployment_type}` : '';

  return `
    <div class="lfr-popup">
      <div class="popup-title">${d.location_name}</div>
      <div class="popup-meta">${d.borough} · ${dateStr} ${deployType}</div>
      <div class="popup-purpose">${d.stated_purpose}</div>
      ${arrestsLine}${claimedLine}
      ${d.notes ? `<div class="popup-notes">${d.notes}</div>` : ''}
      <div class="popup-footer">
        <span class="popup-quality" style="color:${qualityColor}">● ${d.data_quality}</span>
        ${sourceLine}
      </div>
    </div>
  `;
}

export function createDeploymentLayer(deployments) {
  const group = L.layerGroup();

  for (const d of deployments) {
    if (!d.lat || !d.lon) continue;
    const color = QUALITY_COLORS[d.data_quality] ?? QUALITY_COLORS.unverified;

    L.circleMarker([d.lat, d.lon], {
      radius: 8,
      fillColor: color,
      color: '#fff',
      weight: 1.5,
      fillOpacity: 0.85,
      // store id so the cluster field can be used later
      deploymentId: d.id,
    })
      .bindPopup(buildPopupHTML(d), { maxWidth: 320 })
      .addTo(group);
  }

  return group;
}
