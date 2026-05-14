export const TILE_URL = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
export const TILE_OPTIONS = { maxZoom: 19, subdomains: 'abcd' };

export const MAP_CENTER = [51.509, -0.118];
export const MAP_ZOOM = 11;

export const QUALITY_COLORS = {
  confirmed: '#e94560',
  approximate: '#f6a623',
  unverified: '#8899aa',
};

export const QUALITY_LABELS = {
  confirmed: 'Confirmed (primary source)',
  approximate: 'Approximate (derived from evidence)',
  unverified: 'Unverified (single secondary source)',
};

// Paths are relative to map/index.html
export const DATA_PATHS = {
  boroughs: './data/london-boroughs.geojson',
  metDeployments: '../data/deployments/met-police-lfr.json',
  privateDeployments: '../data/deployments/private-operators.json',
};

export const BOROUGH_STYLE = {
  color: '#2a3a5e',
  weight: 1,
  fillColor: 'transparent',
  fillOpacity: 0,
};
