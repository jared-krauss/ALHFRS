# ALHFRS — Gaussian Splat Index

This directory is an **index only**. Binary splat files (`.ply`, `.splat`, `.glb`) are excluded by `.gitignore` and are never committed.

## Purpose

Gaussian splat captures of LFR deployment sites — streets, town centres, stadiums — are indexed here so they can be embedded in the map and site as iframe viewers.

## Adding a splat

1. Capture and process the splat externally (COLMAP → gaussian-splatting, or iPhone → Polycam)
2. Host the output file (SuperSplat cloud, Cloudflare R2, or another static host)
3. Add an entry to `index.json`:

```json
{
  "id": "splat-001",
  "deployment_id": "lfr-014",
  "location_name": "Westminster — King's Coronation route",
  "captured": "2024-MM-DD",
  "host": "supersplat",
  "viewer_url": "https://playcanvas.com/supersplat/viewer?url=...",
  "thumbnail": "https://...",
  "notes": ""
}
```

## Fields

| Field | Description |
|-------|-------------|
| `id` | Unique splat ID (`splat-NNN`) |
| `deployment_id` | Links to a record in `data/deployments/met-police-lfr.json` |
| `location_name` | Human-readable label |
| `captured` | Date of capture |
| `host` | `supersplat` \| `r2` \| `local` |
| `viewer_url` | Embeddable iframe URL |
| `thumbnail` | Preview image URL for map popup |
| `notes` | Any capture or processing notes |

## Map integration

The map reads `splats/index.json` at load time and adds a 📷 badge to any deployment marker that has an associated splat. Clicking opens the viewer in a modal iframe.
