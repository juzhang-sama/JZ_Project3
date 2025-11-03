Write-Host "Starting Flutter Frontend Application..." -ForegroundColor Cyan
Write-Host ""

# Set Flutter path
$env:Path = "D:\flutter\flutter\bin;" + $env:Path

# Change to frontend directory
cd d:\JZ_Project3\frontend

Write-Host "Step 1: Getting dependencies..." -ForegroundColor Yellow
D:\flutter\flutter\bin\flutter.bat pub get

Write-Host ""
Write-Host "Step 2: Checking for devices..." -ForegroundColor Yellow
D:\flutter\flutter\bin\flutter.bat devices

Write-Host ""
Write-Host "Step 3: Running application..." -ForegroundColor Yellow
Write-Host "Tips:" -ForegroundColor Gray
Write-Host "- Press 'r' to hot reload" -ForegroundColor Gray
Write-Host "- Press 'R' to restart" -ForegroundColor Gray
Write-Host "- Press 'q' to quit" -ForegroundColor Gray
Write-Host ""

D:\flutter\flutter\bin\flutter.bat run

