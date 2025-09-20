<#
start-dev.ps1

Opens two PowerShell windows (backend + frontend) for local development.
Usage: right-click and "Run with PowerShell" or from an elevated PowerShell:
    .\start-dev.ps1

This script assumes the repo root is the current working directory and the venv is at E:/ne/Django/.venv
#>

$ErrorActionPreference = 'Stop'

Write-Host "Starting Cato-Store development servers..."

# Start backend in a new PowerShell window
$backendCmd = "E:/ne/Django/.venv/Scripts/python.exe E:/ne/Django/cato-store/manage.py runserver 0.0.0.0:8000"
Write-Host "Launching backend: $backendCmd"
Start-Process -FilePath powershell -ArgumentList "-NoExit", "-Command`,\"$backendCmd`\"" | Out-Null

# Wait for backend to become reachable before starting frontend
$backendUrl = 'http://127.0.0.1:8000/'
$maxWaitSeconds = 60
$intervalSeconds = 1
$elapsed = 0
Write-Host "Waiting for backend to respond at $backendUrl (timeout ${maxWaitSeconds}s) ..."
while ($true) {
    try {
        $resp = Invoke-WebRequest -Uri $backendUrl -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
        if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 400) {
            Write-Host "Backend is up (HTTP $($resp.StatusCode))."
            break
        }
    } catch {
        # ignore and retry
    }
    Start-Sleep -Seconds $intervalSeconds
    $elapsed += $intervalSeconds
    if ($elapsed -ge $maxWaitSeconds) {
        Write-Warning "Timed out waiting for backend after ${maxWaitSeconds}s. Launching frontend anyway."
        break
    }
}

# Start frontend in a new PowerShell window
Push-Location "E:/ne/Django/cato-store/frontend"
$frontendCmd = "npm run dev"
Write-Host "Launching frontend in E:/ne/Django/cato-store/frontend: $frontendCmd"
Start-Process -FilePath powershell -ArgumentList "-NoExit", "-Command`,\"cd 'E:/ne/Django/cato-store/frontend'; $frontendCmd`\"" | Out-Null
Pop-Location

Write-Host "Both processes launched (frontend started after backend ready or timeout). Check the two new PowerShell windows for logs." 
