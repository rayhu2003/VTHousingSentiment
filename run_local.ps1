# Runs VTHousingSentiment fully locally for demos: Flask backend (reads the
# local sentiments.json, no API keys or internet needed) + React frontend
# pointed at it instead of the deployed Render API.
$root = $PSScriptRoot

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\my-app\backend'; python app.py"

Start-Sleep -Seconds 2

$env:REACT_APP_API_URL = "http://localhost:5000"
Set-Location "$root\my-app"
npm start
