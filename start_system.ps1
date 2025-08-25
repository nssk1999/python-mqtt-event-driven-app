# MQTT Event-Driven Architecture Demo - Windows Startup Script (PowerShell)

Write-Host "🚀 Starting MQTT Event-Driven Architecture Demo System" -ForegroundColor Cyan

# Ensure venv exists
if (-not (Test-Path -Path "venv")) {
  Write-Host "❌ Virtual environment not found. Run setup first:" -ForegroundColor Red
  Write-Host "   python -m venv venv"
  Write-Host "   .\\venv\\Scripts\\Activate.ps1"
  Write-Host "   python -m pip install -r requirements.txt"
  exit 1
}

# Activate venv in each new PowerShell window
$projectPath = "$PSScriptRoot"

function Start-Component {
  param(
    [string]$Title,
    [string]$Script,
    [string]$Description
  )
  Write-Host "🔄 Starting $Title..."
  $command = "cd `"$projectPath`"; .\\venv\\Scripts\\Activate.ps1; Write-Host '🚀 $Description'; python $Script; Read-Host 'Press Enter to close'"
  Start-Process powershell -ArgumentList "-NoExit","-Command", $command -WindowStyle Normal
  Start-Sleep -Seconds 1
}

# Start components
Start-Component -Title "Web Dashboard" -Script "web_app.py" -Description "Web Dashboard - Real-time MQTT data visualization"
Start-Component -Title "MQTT Publisher" -Script "mqtt_publisher.py" -Description "MQTT Publisher - Simulating IoT sensor data"
Start-Component -Title "MQTT Subscriber" -Script "mqtt_subscriber.py" -Description "MQTT Subscriber - Processing incoming messages"

Write-Host "🎉 System startup complete!" -ForegroundColor Green
Write-Host "🌐 Open your browser and navigate to: http://localhost:5000"
