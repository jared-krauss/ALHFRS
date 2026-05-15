"""
validate-dataset.py — ALHFRS deployment data validator

Checks any ALHFRS JSON deployment file against schema rules and data quality
expectations. Designed to run on new datasets before they are merged.

Usage:
    python scripts/validate-dataset.py data/deployments/met-police-lfr.json
    python scripts/validate-dataset.py data/deployments/private-operators.json

Exit codes:
    0  — no errors (warnings may be present)
    1  — one or more errors found
"""

import io
import json
import sys
import math
from datetime import date, datetime

# Force UTF-8 output on Windows (avoids CP1252 UnicodeEncodeError)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ── Colours (ANSI, suppressed on Windows if unsupported) ──────────────────────
try:
    import ctypes
    ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
    _colour = True
except Exception:
    _colour = True  # try anyway; worst case is extra chars in output

def _c(code, text):
    return f'\033[{code}m{text}\033[0m' if _colour else text

OK   = lambda t: _c('32', f'[OK]  {t}')
WARN = lambda t: _c('33', f'[!!]  {t}')
ERR  = lambda t: _c('31', f'[XX]  {t}')
HDR  = lambda t: _c('1;36', t)

# ── Greater London bounding box ────────────────────────────────────────────────
LONDON_LAT = (51.28, 51.69)
LONDON_LON = (-0.51, 0.34)

REQUIRED_FIELDS = ['id', 'operator', 'lat', 'lon', 'date_start',
                   'data_quality', 'source_url', 'source_type']

VALID_QUALITY = {'confirmed', 'approximate', 'unverified'}
VALID_SOURCE_TYPE = {'FOI_disclosure', 'news_report', 'court_record',
                     'police_statement', 'operator_statement', 'ngo_report'}

GENERIC_URLS = {
    'https://www.met.police.uk/',
    'https://bigbrotherwatch.org.uk/',
    'https://www.facewatch.co.uk/',
    'https://ico.org.uk/',
}

# Near-duplicate thresholds
NEAR_DIST_M  = 300   # metres
NEAR_DAYS    = 90    # days

# ── Helpers ────────────────────────────────────────────────────────────────────
def haversine_m(lat1, lon1, lat2, lon2):
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def parse_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return None

# ── Validators ─────────────────────────────────────────────────────────────────
def check_record(rec, errors, warnings):
    rid = rec.get('id', '<no-id>')

    # Required fields
    for field in REQUIRED_FIELDS:
        if rec.get(field) is None:
            errors.append(ERR(f'[{rid}] Missing required field: {field}'))

    # data_quality value
    dq = rec.get('data_quality')
    if dq and dq not in VALID_QUALITY:
        errors.append(ERR(f'[{rid}] Invalid data_quality "{dq}" — must be one of {VALID_QUALITY}'))

    # source_type value
    st = rec.get('source_type')
    if st and st not in VALID_SOURCE_TYPE:
        warnings.append(WARN(f'[{rid}] Unknown source_type "{st}"'))

    # Coordinate sanity
    lat, lon = rec.get('lat'), rec.get('lon')
    if lat is not None and lon is not None:
        if not (LONDON_LAT[0] <= lat <= LONDON_LAT[1]):
            warnings.append(WARN(f'[{rid}] lat={lat} is outside Greater London bounds ({LONDON_LAT}) — intentional?'))
        if not (LONDON_LON[0] <= lon <= LONDON_LON[1]):
            warnings.append(WARN(f'[{rid}] lon={lon} is outside Greater London bounds ({LONDON_LON}) — intentional?'))

    # Source quality vs data_quality
    url = rec.get('source_url') or ''
    if dq == 'confirmed' and (not url or url.rstrip('/') + '/' in GENERIC_URLS or url in GENERIC_URLS):
        errors.append(ERR(f'[{rid}] data_quality=confirmed but source_url is missing or generic: "{url}"'))
    if dq == 'approximate' and not url and not rec.get('notes'):
        warnings.append(WARN(f'[{rid}] data_quality=approximate with no source_url or notes'))
    if dq == 'unverified':
        warnings.append(WARN(f'[{rid}] data_quality=unverified — needs follow-up'))

    # Date validity
    d_start = parse_date(rec.get('date_start'))
    d_end   = parse_date(rec.get('date_end'))
    if rec.get('date_start') and not d_start:
        errors.append(ERR(f'[{rid}] date_start "{rec.get("date_start")}" is not valid ISO 8601'))
    if rec.get('date_end') and not d_end:
        errors.append(ERR(f'[{rid}] date_end "{rec.get("date_end")}" is not valid ISO 8601'))
    if d_start and d_end and d_end < d_start:
        errors.append(ERR(f'[{rid}] date_end {d_end} is before date_start {d_start}'))
    if d_start and d_start < date(2011, 1, 1):
        warnings.append(WARN(f'[{rid}] date_start {d_start} predates UK facial recognition deployments — verify'))

    # Cluster consistency (deferred to cross-record check)

def check_near_duplicates(records, warnings):
    for i, a in enumerate(records):
        for b in records[i+1:]:
            lat_a, lon_a = a.get('lat'), a.get('lon')
            lat_b, lon_b = b.get('lat'), b.get('lon')
            if None in (lat_a, lon_a, lat_b, lon_b):
                continue
            dist = haversine_m(lat_a, lon_a, lat_b, lon_b)
            if dist > NEAR_DIST_M:
                continue
            d_a = parse_date(a.get('date_start'))
            d_b = parse_date(b.get('date_start'))
            if d_a and d_b and abs((d_a - d_b).days) <= NEAR_DAYS:
                warnings.append(WARN(
                    f'Near-duplicate? [{a["id"]}] and [{b["id"]}] are {dist:.0f}m apart '
                    f'and {abs((d_a-d_b).days)} days apart — check location_cluster_id'
                ))

def check_cluster_consistency(records, warnings):
    """Cross-borough clusters are unusual but not necessarily wrong — warn, not error."""
    clusters = {}
    for r in records:
        cid = r.get('location_cluster_id')
        if not cid:
            continue
        borough = r.get('borough')
        if cid not in clusters:
            clusters[cid] = borough
        elif clusters[cid] != borough:
            warnings.append(WARN(
                f'[{r["id"]}] Cluster "{cid}" spans boroughs: '
                f'"{clusters[cid]}" vs "{borough}" — intentional? Consider splitting cluster or using notes.'
            ))

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/validate-dataset.py <path/to/dataset.json>')
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(ERR(f'File not found: {path}'))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(ERR(f'Invalid JSON: {e}'))
        sys.exit(1)

    # Accept either "deployments" or "actions" as the record array key
    records = data.get('deployments') or data.get('actions') or []
    if not records:
        print(WARN('No deployments/actions array found in file — nothing to validate'))
        sys.exit(0)

    print(HDR(f'\nALHFRS Dataset Validator — {path}'))
    print(f'Schema version : {data.get("schema_version", "unknown")}')
    print(f'Records found  : {len(records)}')
    print(f'Last updated   : {data.get("last_updated", "unknown")}\n')

    errors, warnings = [], []

    for rec in records:
        check_record(rec, errors, warnings)

    check_near_duplicates(records, warnings)
    check_cluster_consistency(records, warnings)

    # Print results per record (group by id for readability)
    seen_ids = []
    for line in errors + warnings:
        print(line)

    # Summary
    print()
    total = len(records)
    err_count  = len(errors)
    warn_count = len(warnings)

    if err_count == 0 and warn_count == 0:
        print(OK(f'All {total} records passed — no issues found'))
    else:
        if err_count:
            print(_c('31', f'{err_count} error(s) found'))
        if warn_count:
            print(_c('33', f'{warn_count} warning(s) found'))
        print(f'{total - err_count} of {total} records clean')

    print()
    sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
