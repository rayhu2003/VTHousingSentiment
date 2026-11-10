# Runs the offline data pipeline end to end: scrape Reddit into MongoDB,
# score the scraped text with Gemini, then update the sentiments.json that
# the Flask API serves. Requires a filled-in .env (see .env.example).
$root = $PSScriptRoot
Set-Location $root

python DataScraper.py
if ($LASTEXITCODE -ne 0) { Write-Error "DataScraper.py failed"; exit 1 }

python SentimentFromDB.py
if ($LASTEXITCODE -ne 0) { Write-Error "SentimentFromDB.py failed"; exit 1 }

Copy-Item "$root\apartment_sentiments.json" "$root\my-app\backend\sentiments.json" -Force
Write-Host "Pipeline complete. my-app\backend\sentiments.json updated."
