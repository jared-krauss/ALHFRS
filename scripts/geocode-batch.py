#!/usr/bin/env python3
"""
geocode-batch.py — Nominatim geocoder for ALHFRS null lat/lon records.

Scans met-police-lfr.json for records with null lat or lon, geocodes each
via Nominatim (OpenStreetMap, free, no API key), validates the result against
the stated borough using a point-in-polygon check, then writes results to a
staging file.

Optionally applies results directly to the dataset with --apply.

Usage:
  python scripts/geocode-batch.py [options]

  --dataset   Path to deployment JSON (default: data/deployments/met-police-lfr.json)
  --geojson   Path to london-boroughs.geojson (default: map/data/london-boroughs.geojson)
  --out       Staging output (default: data/staging/geocoding-results.json)
  --state     State file for resumability (default: data/staging/.geocode-state.json)
  --apply     After geocoding, apply results to --dataset in place
  --limit N   Only process N records (for testing)
  --dry-run   Print queue without making network requests

Accuracy levels (set in geo_accuracy field):
  street_level  — Nominatim place_rank <= 22 (road or specific point)
  borough_level — Nominatim place_rank > 22 (suburb, district, city)
"""

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


DATASET = Path("data/deployments/met-police-lfr.json")
GEOJSON = Path("map/data/london-boroughs.geojson")
OUT     = Path("data/staging/geocoding-results.json")
STATE   = Path("data/staging/.geocode-state.json")

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT    = "ALHFRS-geocoder/1.0 (alhfrs-research; jaredkrauss@gmail.com)"
RATE_LIMIT    = 1.1  # seconds between requests (Nominatim policy: max 1/s)


# ── Point-in-polygon (ray casting, no external deps) ──────────────────────────

def _point_in_ring(px: float, py: float, ring: list) -> bool:
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def point_in_polygon(lat: float, lon: float, geometry: dict) -> bool:
    """Return True if (lat, lon) is inside a GeoJSON Polygon or MultiPolygon."""
    gtype = geometry["type"]
    if gtype == "Polygon":
        rings = geometry["coordinates"]
        if _point_in_ring(lon, lat, rings[0]):
            # Check holes (counter-winding rings)
            for hole in rings[1:]:
                if _point_in_ring(lon, lat, hole):
                    return False
            return True
        return False
    elif gtype == "MultiPolygon":
        for poly in geometry["coordinates"]:
            if _point_in_ring(lon, lat, poly[0]):
                for hole in poly[1:]:
                    if _point_in_ring(lon, lat, hole):
                        break
                else:
                    return True
        return False
    return False


def load_boroughs(geojson_path: Path) -> dict[str, dict]:
    """Return {normalized_name: geometry} mapping."""
    gj = json.loads(geojson_path.read_text(encoding="utf-8"))
    return {
        f["properties"]["name"].lower(): f["geometry"]
        for f in gj["features"]
        if f.get("properties", {}).get("name")
    }


def borough_contains(boroughs: dict, borough_name: str, lat: float, lon: float) -> bool | None:
    """Return True/False/None (None = borough not found in GeoJSON)."""
    key = (borough_name or "").lower().strip()
    geom = boroughs.get(key)
    if geom is None:
        # Try partial match (e.g. "City of Westminster" → "westminster")
        for bname, geom2 in boroughs.items():
            if key in bname or bname in key:
                return point_in_polygon(lat, lon, geom2)
        return None
    return point_in_polygon(lat, lon, geom)


# ── Nominatim ─────────────────────────────────────────────────────────────────

def nominatim_search(query: str) -> list[dict]:
    """Query Nominatim, return raw result list."""
    params = urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "countrycodes": "gb",
        "limit": 3,
        "addressdetails": 0,
    })
    url = f"{NOMINATIM_URL}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def place_rank_to_accuracy(place_rank: int) -> str:
    """Nominatim place_rank → geo_accuracy label."""
    # rank <=22 covers house numbers and roads (specific)
    # rank > 22 covers suburbs, boroughs, cities (coarse)
    return "street_level" if place_rank <= 22 else "borough_level"


def geocode_record(rec: dict, boroughs: dict) -> dict:
    """Geocode one record. Returns result dict."""
    rid       = rec["id"]
    loc_name  = (rec.get("location_name") or "").strip()
    borough   = (rec.get("borough") or "").strip()

    # Build progressive queries: most specific first
    queries = []
    if loc_name and borough:
        queries.append(f"{loc_name}, {borough}, London, UK")
    if loc_name:
        queries.append(f"{loc_name}, London, UK")
    if borough:
        queries.append(f"{borough}, London, UK")

    for query in queries:
        try:
            results = nominatim_search(query)
        except Exception as e:
            return {
                "id": rid, "lat": None, "lon": None,
                "geo_source": "nominatim", "geo_status": f"error: {e}",
                "geo_accuracy": None, "geo_validated": False,
                "geo_importance": None, "query_used": query,
            }

        if not results:
            time.sleep(RATE_LIMIT)
            continue

        best = results[0]
        lat  = float(best["lat"])
        lon  = float(best["lon"])
        rank = int(best.get("place_rank", 30))
        importance = float(best.get("importance", 0))

        # Borough boundary validation
        validated = None
        geo_status = "success"
        if borough:
            inside = borough_contains(boroughs, borough, lat, lon)
            if inside is True:
                validated = True
            elif inside is False:
                validated = False
                geo_status = "boundary_mismatch"
            # None = borough not found in GeoJSON, can't validate

        time.sleep(RATE_LIMIT)
        return {
            "id": rid,
            "lat": lat,
            "lon": lon,
            "geo_source": "nominatim",
            "geo_accuracy": place_rank_to_accuracy(rank),
            "geo_validated": validated,
            "geo_status": geo_status,
            "geo_importance": round(importance, 4),
            "query_used": query,
            "nominatim_display_name": best.get("display_name", "")[:80],
        }

        time.sleep(RATE_LIMIT)

    return {
        "id": rid, "lat": None, "lon": None,
        "geo_source": "nominatim", "geo_status": "no_result",
        "geo_accuracy": None, "geo_validated": False,
        "geo_importance": None, "query_used": queries[0] if queries else "",
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Geocode null lat/lon records using Nominatim."
    )
    ap.add_argument("--dataset", default=str(DATASET))
    ap.add_argument("--geojson", default=str(GEOJSON))
    ap.add_argument("--out",     default=str(OUT))
    ap.add_argument("--state",   default=str(STATE))
    ap.add_argument("--apply",   action="store_true",
                    help="Apply results to --dataset after geocoding")
    ap.add_argument("--limit",   type=int, default=None,
                    help="Only geocode this many records (testing)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print queue without making requests")
    args = ap.parse_args()

    dataset_path = Path(args.dataset)
    out_path     = Path(args.out)
    state_path   = Path(args.state)

    # Load dataset
    data        = json.loads(dataset_path.read_text(encoding="utf-8"))
    deployments = data["deployments"]

    # Load borough boundaries
    boroughs = load_boroughs(Path(args.geojson))
    print(f"Loaded {len(boroughs)} borough boundaries")

    # Load state (completed IDs)
    completed = set()
    if state_path.exists():
        completed = set(json.loads(state_path.read_text(encoding="utf-8")).get("completed", []))
        print(f"Resuming: {len(completed)} already geocoded")

    # Load existing results (to merge with new ones)
    existing_results = {}
    if out_path.exists():
        prev = json.loads(out_path.read_text(encoding="utf-8"))
        for r in prev.get("results", []):
            existing_results[r["id"]] = r

    # Build queue: null lat or lon, not already done
    queue = [
        r for r in deployments
        if (r.get("lat") is None or r.get("lon") is None)
        and r["id"] not in completed
    ]
    if args.limit:
        queue = queue[:args.limit]

    print(f"Queue: {len(queue)} records to geocode")

    if args.dry_run:
        for rec in queue[:20]:
            loc = rec.get("location_name","?")
            bor = rec.get("borough","?")
            print(f"  {rec['id']}  {loc[:35]:<35}  {bor}")
        if len(queue) > 20:
            print(f"  ... and {len(queue)-20} more")
        return

    # Geocode
    new_results = []
    success = boundary_miss = no_result = errors = 0

    for i, rec in enumerate(queue):
        rid = rec["id"]
        loc = rec.get("location_name","?")
        bor = rec.get("borough","?")
        print(f"  [{i+1}/{len(queue)}] {rid}  {loc[:35]:<35}  {bor}", end="  ", flush=True)

        result = geocode_record(rec, boroughs)
        new_results.append(result)
        existing_results[rid] = result

        status = result["geo_status"]
        if status == "success":
            success += 1
            print(f"OK  lat={result['lat']:.4f} lon={result['lon']:.4f}  acc={result['geo_accuracy']}")
        elif status == "boundary_mismatch":
            boundary_miss += 1
            print(f"BOUNDARY_MISMATCH  lat={result['lat']:.4f} lon={result['lon']:.4f}")
        elif status == "no_result":
            no_result += 1
            print("NO_RESULT")
        else:
            errors += 1
            print(f"ERROR: {status}")

        # Update state after each record
        completed.add(rid)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            json.dumps({"completed": sorted(completed)}, indent=2),
            encoding="utf-8"
        )

    # Write results
    all_results = sorted(existing_results.values(), key=lambda r: r["id"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps({
            "record_count": len(all_results),
            "results": all_results,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"\nResults: {success} success, {boundary_miss} boundary_mismatch, "
          f"{no_result} no_result, {errors} errors")
    print(f"Written: {out_path}")

    if not args.apply:
        print(f"\nTo apply results to dataset:")
        print(f"  python scripts/geocode-batch.py --apply")
        return

    # Apply: merge lat/lon + geo fields into dataset
    results_by_id = {r["id"]: r for r in all_results}
    applied = skipped = 0
    for rec in deployments:
        res = results_by_id.get(rec["id"])
        if res and res.get("lat") is not None:
            rec["lat"]          = res["lat"]
            rec["lon"]          = res["lon"]
            rec["geo_source"]   = res.get("geo_source")
            rec["geo_accuracy"] = res.get("geo_accuracy")
            rec["geo_validated"] = res.get("geo_validated")
            applied += 1
        else:
            skipped += 1

    dataset_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"Applied: {applied} records updated, {skipped} unchanged")
    print(f"Written: {dataset_path}")


if __name__ == "__main__":
    main()
