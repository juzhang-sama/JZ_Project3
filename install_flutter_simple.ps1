Write-Host "Installing Flutter SDK..." -ForegroundColor Cyan
Write-Host ""

$flutterDir = "D:\flutter"
$zipPath = "$flutterDir\flutter.zip"
$flutterBin = "$flutterDir\flutter\bin"

Write-Host "Step 1: Creating directory..." -ForegroundColor Yellow
if (-not (Test-Path $flutterDir)) {
    New-Item -ItemType Directory -Path $flutterDir -Force | Out-Null
    Write-Host "OK: Directory created" -ForegroundColor Green
}
Write-Host ""

Write-Host "Step 2: Downloading Flutter SDK (this may take 2-5 minutes)..." -ForegroundColor Yellow
$url = "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.24.0-stable.zip"

try {
    $client = New-Object System.Net.WebClient
    $client.DownloadFile($url, $zipPath)
    Write-Host "OK: Download complete" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Download failed: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "Step 3: Extracting files (this may take 1-2 minutes)..." -ForegroundColor Yellow
try {
    Expand-Archive -Path $zipPath -DestinationPath $flutterDir -Force
    Write-Host "OK: Extraction complete" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Extraction failed: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "Step 4: Cleaning up..." -ForegroundColor Yellow
Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
Write-Host "OK: Cleanup complete" -ForegroundColor Green
Write-Host ""

Write-Host "Step 5: Adding to PATH..." -ForegroundColor Yellow
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$flutterBin*") {
    $newPath = $currentPath + ";" + $flutterBin
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "OK: Flutter added to PATH" -ForegroundColor Green
    Write-Host "NOTE: Restart PowerShell for changes to take effect" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "Step 6: Verifying installation..." -ForegroundColor Yellow
$flutterExe = "$flutterBin\flutter.bat"
if (Test-Path $flutterExe) {
    Write-Host "OK: Flutter executable found" -ForegroundColor Green
} else {
    Write-Host "ERROR: Flutter executable not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "Installation complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart PowerShell" -ForegroundColor White
Write-Host "2. Run: flutter devices" -ForegroundColor White
Write-Host "3. Start Android emulator" -ForegroundColor White
Write-Host "4. Run: .\start_frontend.ps1" -ForegroundColor White

