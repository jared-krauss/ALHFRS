# serve.ps1 — Start a local HTTP server for the ALHFRS map
# Run this from the ALHFRS directory, then open http://localhost:8741/map-embed.html

$port = 8741
$dir  = $PSScriptRoot

Write-Host ""
Write-Host "  ALHFRS Map Server" -ForegroundColor Cyan
Write-Host "  -----------------" -ForegroundColor DarkGray
Write-Host "  Serving: $dir" -ForegroundColor Gray
Write-Host ""
Write-Host "  Open in browser:" -ForegroundColor White
Write-Host "  http://localhost:$port/map-embed.html" -ForegroundColor Green
Write-Host ""
Write-Host "  Press Ctrl+C to stop." -ForegroundColor DarkGray
Write-Host ""

Set-Location $dir
python -m http.server $port
