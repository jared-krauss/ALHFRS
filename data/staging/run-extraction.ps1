$python = "D:\Dev\tools\.venv\Scripts\python.exe"
$script = "D:\Dev\ALHFRS\scripts\pdf-extract-deployments.py"
$base = "D:\Dev\jaredkrauss-art\Content & Assets\Featured Projects\A London History of Facial Recognition Systems (ALHFRS)\Assets\Research Material\Deployment Data"

& $python $script --pdf "$base\lfr-deployment-grid-2020-2022.pdf" --out "D:\Dev\ALHFRS\data\staging\extract-2020-2022.json" --start-id 358 --source-label lfr-deployment-grid-2020-2022 --chunk-pages 4 2>"D:\Dev\ALHFRS\data\staging\log-2020-2022.txt"
"DONE-2020-2022" | Out-File "D:\Dev\ALHFRS\data\staging\log-2020-2022.txt" -Append

& $python $script --pdf "$base\lfr-deployment-grid-2023-to-2024.pdf" --out "D:\Dev\ALHFRS\data\staging\extract-2023-2024.json" --start-id 450 --source-label lfr-deployment-grid-2023-to-2024 --skip-last 1 --chunk-pages 4 2>"D:\Dev\ALHFRS\data\staging\log-2023-2024.txt"
"DONE-2023-2024" | Out-File "D:\Dev\ALHFRS\data\staging\log-2023-2024.txt" -Append
