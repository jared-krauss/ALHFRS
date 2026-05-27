# After Gemini — How to Merge Results Back

## Extraction output → met-police-lfr.json

1. Save Gemini's JSON array to `D:\Dev\ALHFRS\data\staging\gemini-2021-extraction.json`
2. Open it and manually verify a few records look sane
3. The records won't have `id` fields yet — run this to assign IDs starting at lfr-536:

```powershell
$existing = (Get-Content "D:\Dev\ALHFRS\data\deployments\met-police-lfr.json" -Raw | ConvertFrom-Json).deployments
$new = Get-Content "D:\Dev\ALHFRS\data\staging\gemini-2021-extraction.json" -Raw | ConvertFrom-Json
$nextId = 536
foreach ($rec in $new) {
    $rec | Add-Member -NotePropertyName "id" -NotePropertyValue "lfr-$nextId" -Force
    $rec | Add-Member -NotePropertyName "operator" -NotePropertyValue "Metropolitan Police" -Force
    $rec | Add-Member -NotePropertyName "operator_type" -NotePropertyValue "law_enforcement" -Force
    $nextId++
}
# Merge and write back
$combined = $existing + $new
$root = Get-Content "D:\Dev\ALHFRS\data\deployments\met-police-lfr.json" -Raw | ConvertFrom-Json
$root.deployments = $combined
$root.last_updated = (Get-Date -Format "yyyy-MM-dd")
$root | ConvertTo-Json -Depth 10 | Set-Content "D:\Dev\ALHFRS\data\deployments\met-police-lfr.json" -Encoding UTF8
Write-Host "Merged $($new.Count) new records. Total: $($combined.Count)"
```

4. Verify: `$data.deployments | Group-Object { ($_.date_start -split "-")[0] } | Sort Name`  
   Should now show 2021 alongside other years.

---

## Geocoding output → met-police-lfr.json

1. Save Gemini's JSON array to `D:\Dev\ALHFRS\data\staging\geocoding-results.json`
2. Run this to patch lat/lon back in:

```powershell
$dataFile = "D:\Dev\ALHFRS\data\deployments\met-police-lfr.json"
$root = Get-Content $dataFile -Raw | ConvertFrom-Json
$geoResults = Get-Content "D:\Dev\ALHFRS\data\staging\geocoding-results.json" -Raw | ConvertFrom-Json

# Build lookup by id
$geoMap = @{}
foreach ($g in $geoResults) { $geoMap[$g.id] = $g }

$patched = 0
foreach ($dep in $root.deployments) {
    if ($geoMap.ContainsKey($dep.id) -and $null -eq $dep.lat) {
        $geo = $geoMap[$dep.id]
        $dep.lat = $geo.lat
        $dep.lon = $geo.lon
        $dep | Add-Member -NotePropertyName "geo_confidence" -NotePropertyValue $geo.geo_confidence -Force
        $patched++
    }
}

$root.last_updated = (Get-Date -Format "yyyy-MM-dd")
$root | ConvertTo-Json -Depth 10 | Set-Content $dataFile -Encoding UTF8
Write-Host "Patched $patched records with coordinates."
```

3. Verify: 
```powershell
$root = Get-Content $dataFile -Raw | ConvertFrom-Json
($root.deployments | Where-Object { $null -eq $_.lat }).Count
# Should be lower than 169 (failed geocodes will remain null)
```

---

## Corroboration check

If Gemini also extracted 2022–2026 records, compare against existing data:

```powershell
# Find potential duplicates by date + borough
$new = Get-Content "D:\Dev\ALHFRS\data\staging\gemini-2021-extraction.json" -Raw | ConvertFrom-Json
$existing = (Get-Content "D:\Dev\ALHFRS\data\deployments\met-police-lfr.json" -Raw | ConvertFrom-Json).deployments

foreach ($n in $new) {
    $match = $existing | Where-Object { $_.date_start -eq $n.date_start -and $_.borough -eq $n.borough }
    if ($match) {
        Write-Host "POSSIBLE DUPLICATE: $($n.date_start) $($n.borough) — existing: $($match.id)"
    }
}
```
