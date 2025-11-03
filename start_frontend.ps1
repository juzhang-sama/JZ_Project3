# 🚀 前端项目快速启动脚本

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  极简MVP - 前端项目启动脚本" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Flutter 是否安装
Write-Host "📋 检查 Flutter 环境..." -ForegroundColor Yellow
$flutterPath = Get-Command flutter -ErrorAction SilentlyContinue
if ($null -eq $flutterPath) {
    Write-Host "❌ Flutter 未安装或不在 PATH 中" -ForegroundColor Red
    Write-Host ""
    Write-Host "请按照以下步骤安装 Flutter:" -ForegroundColor Yellow
    Write-Host "1. 访问 https://flutter.dev/docs/get-started/install/windows" -ForegroundColor White
    Write-Host "2. 下载并解压 Flutter SDK" -ForegroundColor White
    Write-Host "3. 将 Flutter\bin 添加到系统 PATH" -ForegroundColor White
    Write-Host "4. 重启 PowerShell" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ Flutter 已安装" -ForegroundColor Green
flutter --version
Write-Host ""

# 检查 Android 模拟器
Write-Host "📱 检查可用设备..." -ForegroundColor Yellow
$devices = flutter devices 2>&1
Write-Host $devices
Write-Host ""

# 检查是否有可用设备
if ($devices -match "No devices detected") {
    Write-Host "⚠️  未检测到设备" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请选择以下选项之一:" -ForegroundColor Yellow
    Write-Host "1. 启动 Android 模拟器" -ForegroundColor White
    Write-Host "2. 连接 Android 真实设备 (启用 USB 调试)" -ForegroundColor White
    Write-Host "3. 启动 iOS 模拟器 (仅 macOS)" -ForegroundColor White
    Write-Host ""
    Write-Host "启动 Android 模拟器的命令:" -ForegroundColor Cyan
    Write-Host "emulator -avd <device_name>" -ForegroundColor White
    Write-Host ""
    exit 1
}

# 进入前端目录
Write-Host "📂 进入前端项目目录..." -ForegroundColor Yellow
Set-Location "d:\JZ_Project3\frontend"
Write-Host "✅ 当前目录: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# 获取依赖
Write-Host "📦 获取项目依赖..." -ForegroundColor Yellow
flutter pub get
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 获取依赖失败" -ForegroundColor Red
    exit 1
}
Write-Host "✅ 依赖获取成功" -ForegroundColor Green
Write-Host ""

# 检查后端服务
Write-Host "🔍 检查后端服务..." -ForegroundColor Yellow
$backendCheck = Invoke-WebRequest -Uri "http://localhost:8000/docs" -ErrorAction SilentlyContinue
if ($null -eq $backendCheck) {
    Write-Host "⚠️  后端服务未运行" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请在另一个终端运行以下命令启动后端服务:" -ForegroundColor Cyan
    Write-Host "cd d:\JZ_Project3\backend" -ForegroundColor White
    Write-Host ".\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
    Write-Host ""
    Write-Host "继续运行前端? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -ne "Y" -and $response -ne "y") {
        exit 0
    }
} else {
    Write-Host "✅ 后端服务正在运行" -ForegroundColor Green
}
Write-Host ""

# 启动应用
Write-Host "🚀 启动应用..." -ForegroundColor Cyan
Write-Host ""
Write-Host "提示:" -ForegroundColor Yellow
Write-Host "- 按 'r' 进行热重载" -ForegroundColor White
Write-Host "- 按 'R' 进行完整重启" -ForegroundColor White
Write-Host "- 按 'q' 退出应用" -ForegroundColor White
Write-Host ""

flutter run

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  应用已关闭" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

