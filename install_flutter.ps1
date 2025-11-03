# Flutter SDK 安装脚本

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Flutter SDK 安装脚本" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 设置变量
$flutterDir = "D:\flutter"
$zipPath = "$flutterDir\flutter.zip"
$flutterBin = "$flutterDir\flutter\bin"

# 步骤 1: 创建目录
Write-Host "📂 步骤 1: 创建 Flutter 目录..." -ForegroundColor Yellow
if (-not (Test-Path $flutterDir)) {
    New-Item -ItemType Directory -Path $flutterDir -Force | Out-Null
    Write-Host "✅ 目录已创建: $flutterDir" -ForegroundColor Green
} else {
    Write-Host "⚠️  目录已存在: $flutterDir" -ForegroundColor Yellow
}
Write-Host ""

# 步骤 2: 下载 Flutter SDK
Write-Host "📥 步骤 2: 下载 Flutter SDK..." -ForegroundColor Yellow
Write-Host "这可能需要 2-5 分钟，请耐心等待..." -ForegroundColor Gray

$url = "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.24.0-stable.zip"

try {
    $client = New-Object System.Net.WebClient
    $client.DownloadFile($url, $zipPath)
    Write-Host "✅ 下载完成" -ForegroundColor Green
    
    $size = (Get-Item $zipPath).Length / 1MB
    Write-Host "📦 文件大小: $([Math]::Round($size, 2)) MB" -ForegroundColor Green
} catch {
    Write-Host "❌ 下载失败: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 步骤 3: 解压文件
Write-Host "📂 步骤 3: 解压 Flutter SDK..." -ForegroundColor Yellow
Write-Host "这可能需要 1-2 分钟..." -ForegroundColor Gray

try {
    Expand-Archive -Path $zipPath -DestinationPath $flutterDir -Force
    Write-Host "✅ 解压完成" -ForegroundColor Green
} catch {
    Write-Host "❌ 解压失败: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 步骤 4: 删除 zip 文件
Write-Host "🗑️  步骤 4: 清理临时文件..." -ForegroundColor Yellow
Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
Write-Host "✅ 临时文件已删除" -ForegroundColor Green
Write-Host ""

# 步骤 5: 添加到 PATH
Write-Host "🔧 步骤 5: 配置系统 PATH..." -ForegroundColor Yellow

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$flutterBin*") {
    $newPath = $currentPath + ";" + $flutterBin
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✅ Flutter bin 已添加到 PATH" -ForegroundColor Green
    Write-Host "需要重启 PowerShell 以使更改生效" -ForegroundColor Yellow
} else {
    Write-Host "Flutter bin 已在 PATH 中" -ForegroundColor Yellow
}
Write-Host ""

# 步骤 6: 验证安装
Write-Host "✅ 步骤 6: 验证安装..." -ForegroundColor Yellow

$flutterExe = "$flutterBin\flutter.bat"
if (Test-Path $flutterExe) {
    Write-Host "✅ Flutter 可执行文件已找到" -ForegroundColor Green
    Write-Host "📍 位置: $flutterExe" -ForegroundColor Gray
} else {
    Write-Host "❌ Flutter 可执行文件未找到" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 步骤 7: 运行 flutter doctor
Write-Host "🏥 步骤 7: 运行 Flutter Doctor..." -ForegroundColor Yellow
Write-Host "检查 Flutter 环境..." -ForegroundColor Gray
Write-Host ""

& "$flutterExe" doctor

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  安装完成！" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 后续步骤:" -ForegroundColor Yellow
Write-Host "1. 重启 PowerShell 以使 PATH 更改生效" -ForegroundColor White
Write-Host "2. 运行 'flutter devices' 检查可用设备" -ForegroundColor White
Write-Host "3. 启动 Android 模拟器或连接真实设备" -ForegroundColor White
Write-Host "4. 运行 '.\start_frontend.ps1' 启动应用" -ForegroundColor White
Write-Host ""

