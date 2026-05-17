# map/

Leaflet-based interactive deployment map. Loads all deployment data from `../data/` and renders it as layered circle markers on a dark London basemap.

---

## How to run

```powershell
# From D:\Dev\ALHFRS\ (project root — not map/)
python -m http.server 8000
# Open: http://localhost:8000/map/index.html
```

**Must be served via HTTP.** The JS modules use `fetch()` to load GeoJSON and deployment JSON, which browsers block under `file://` origins. A `load-error` banner appears in the page if data loading fails.

---

## Architecture

- **Leaflet 1.9.4** (via CDN)
- **ES6 modules** — `index.html` imports `js/main.js` as `type="module"`; all other JS files are ES6 modules imported from there
- **CartoDB Dark Matter** basemap (`{s}.basemaps.cartocdn.com/dark_all/`)
- **Dark theme UI** — background `#0d1117`, accent red `#e94560`, amber `#f6a623`
- **No build step, no bundler** — plain browser ES6 modules

---

## File breakdown

| File | Owns |
|---|---|
| `index.html` | HTML shell, CSS, layer panel markup, load-error banner |
| `js/config.js` | All constants: `TILE_URL`, `MAP_CENTER` (51.509, -0.118), `MAP_ZOOM` (11), `QUALITY_COLORS`, `QUALITY_LABELS`, `DATA_PATHS`, `BOROUGH_STYLE` |
| `js/main.js` | Async `init()`: creates map, fetches data, wires layers and controls |
| `js/borough-layer.js` | Creates a Leaflet GeoJSON layer from borough boundaries; sticky tooltips on hover |
| `js/deployment-layer.js` | Creates `L.circleMarker` per deployment record; builds popup HTML |
| `js/layer-controls.js` | Wires the layer panel toggle buttons; disables buttons whose data failed to load |
| `js/legend.js` | `L.control` (bottom-left) showing `QUALITY_COLORS` / `QUALITY_LABELS` |

---

## Data loading pattern

Data paths are defined in `config.js` relative to `map/index.html`:

```js
export const DATA_PATHS = {
  boroughs:           './data/london-boroughs.geojson',
  metDeployments:     '../data/deployments/met-police-lfr.json',
  btpDeployments:     '../data/deployments/btp-lfr.json',
  privateDeployments: '../data/deployments/private-operators.json',
};
```

**Critical vs optional layers** (`main.js`):
- Borough GeoJSON + Met Police data are fetched together in a `Promise.all`. If either fails, a load-error banner is shown and `init()` returns early.
- BTP and private operator data are fetched in a second `Promise.all` with `.catch(() => null)`. If they fail, they return `null` and their layer-panel buttons are automatically disabled — the map still loads.

---

## Popup field rendering

`deployment-layer.js` builds popup HTML from these record fields:

```
location_name
borough · date_start[–date_end] · deployment_type

stated_purpose

[Arrests: outcome_arrests]            (if non-null)
[Claimed reduction: claimed_reduction] (if non-null)
[notes]                               (if non-null)

● data_quality label  |  [Source ↗]
```

Circle marker color is keyed to `data_quality` via `QUALITY_COLORS` from `config.js`:
- `confirmed` → `#e94560` (red)
- `approximate` → `#f6a623` (amber)
- `unverified` → `#8899aa` (grey)

---

## Adding a new deployment layer

1. Add the data file path to `DATA_PATHS` in `config.js`.
2. In `main.js`, fetch it (optional pattern: `fetch(...).then(r => r.ok ? r.json() : null).catch(() => null)`).
3. If the data file has a `deployments` array, pass `data.deployments` to `createDeploymentLayer()`.
4. Add the layer to the `initControls` call.
5. Add a button in the layer panel section in `index.html` with matching `data-layer` attribute.

---

## Known issues

**`london-boroughs.js` is dead code.** It exports a hardcoded GeoJSON FeatureCollection of 23 London boroughs but is not imported anywhere. The map uses `./data/london-boroughs.geojson` (full-resolution, 244 KB) instead. Do not import `london-boroughs.js` into new code.

**`london-wards.geojson` (1.05 MB) is present but not surfaced.** `config.js` doesn't reference it yet. Ward boundaries are planned as a future layer toggle — when wired up, add a path to `DATA_PATHS` and create a layer using `createBoroughLayer()` or a similar GeoJSON handler.

---

## GeoJSON files

| File | Size | Content |
|---|---|---|
| `data/london-boroughs.geojson` | 244 KB | 32 London borough boundary polygons |
| `data/london-wards.geojson` | 1.05 MB | Ward-level boundary polygons (finer granularity) |
