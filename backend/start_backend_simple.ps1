# 简单的后端启动脚本

Write-Host "=== ImageGen 后端启动脚本 ===" -ForegroundColor Cyan
Write-Host ""

# 进入后端目录
$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $backendDir

Write-Host "当前目录: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# 检查虚拟环境
Write-Host "1️⃣  检查虚拟环境..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "✅ 虚拟环境存在" -ForegroundColor Green
    
    # 激活虚拟环境
    Write-Host "2️⃣  激活虚拟环境..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ 虚拟环境已激活" -ForegroundColor Green
} else {
    Write-Host "❌ 虚拟环境不存在，请先创建虚拟环境" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 检查依赖
Write-Host "3️⃣  检查依赖..." -ForegroundColor Yellow
$pipList = pip list 2>$null
if ($pipList -match "fastapi") {
    Write-Host "✅ 依赖已安装" -ForegroundColor Green
} else {
    Write-Host "⚠️  安装依赖..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✅ 依赖安装完成" -ForegroundColor Green
}

Write-Host ""

# 初始化数据库
Write-Host "4️⃣  初始化数据库..." -ForegroundColor Yellow
if (Test-Path "image_gen.db") {
    Write-Host "ℹ️  数据库文件已存在，跳过初始化" -ForegroundColor Cyan
} else {
    Write-Host "创建新数据库..." -ForegroundColor Yellow
    python init_db.py
    Write-Host "✅ 数据库初始化完成" -ForegroundColor Green
}

Write-Host ""

# 启动服务
Write-Host "5️⃣  启动后端服务..." -ForegroundColor Yellow
Write-Host ""
Write-Host "服务将运行在: http://0.0.0.0:8000" -ForegroundColor Cyan
Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

