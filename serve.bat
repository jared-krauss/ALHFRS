@echo off
echo.
echo   ALHFRS Map Server
echo   Open: http://localhost:8741/map-embed.html
echo   Press Ctrl+C to stop.
echo.
cd /d "%~dp0"
python -m http.server 8741
pause
