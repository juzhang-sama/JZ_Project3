# 以管理员身份运行 Flutter
# 这个脚本会修复权限问题并运行 Flutter

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Flutter Android 应用部署脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "需要以管理员身份运行此脚本" -ForegroundColor Red
    Write-Host "请右键点击 PowerShell 并选择 '以管理员身份运行'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ 以管理员身份运行" -ForegroundColor Green
Write-Host ""

# 步骤 1: 清理 Gradle 缓存
Write-Host "步骤 1: 清理 Gradle 缓存..." -ForegroundColor Yellow
$gradleDir = "$env:USERPROFILE\.gradle"
if (Test-Path $gradleDir) {
    Write-Host "删除 $gradleDir"
    Remove-Item -Path $gradleDir -Recurse -Force -ErrorAction SilentlyContinue
}
Write-Host "✅ Gradle 缓存已清理" -ForegroundColor Green
Write-Host ""

# 步骤 2: 清理 Android 缓存
Write-Host "步骤 2: 清理 Android 缓存..." -ForegroundColor Yellow
$androidDir = "$env:USERPROFILE\.android"
if (Test-Path $androidDir) {
    Write-Host "删除 $androidDir"
    Remove-Item -Path $androidDir -Recurse -Force -ErrorAction SilentlyContinue
}
Write-Host "✅ Android 缓存已清理" -ForegroundColor Green
Write-Host ""

# 步骤 3: 创建新的目录并设置权限
Write-Host "步骤 3: 创建目录并设置权限..." -ForegroundColor Yellow
$nativeDir = "$env:USERPROFILE\.gradle\native"
New-Item -ItemType Directory -Path $nativeDir -Force | Out-Null
icacls $nativeDir /grant:r "$env:USERNAME`:F" /T /C | Out-Null
Write-Host "✅ 目录权限已设置" -ForegroundColor Green
Write-Host ""

# 步骤 4: 配置 Flutter 使用 Java 17
Write-Host "步骤 4: 配置 Flutter 使用 Java 17..." -ForegroundColor Yellow
cd d:\JZ_Project3\frontend
$env:Path = "D:\flutter\flutter\bin;" + $env:Path
D:\flutter\flutter\bin\flutter.bat config --jdk-dir="C:\Program Files\Microsoft\jdk-17.0.15.6-hotspot"
Write-Host "✅ Java 17 已配置" -ForegroundColor Green
Write-Host ""

# 步骤 5: 清理 Flutter 项目
Write-Host "步骤 5: 清理 Flutter 项目..." -ForegroundColor Yellow
D:\flutter\flutter\bin\flutter.bat clean
Write-Host "✅ Flutter 项目已清理" -ForegroundColor Green
Write-Host ""

# 步骤 6: 运行 Flutter
Write-Host "步骤 6: 编译并部署应用..." -ForegroundColor Cyan
Write-Host "这可能需要 5-15 分钟，请耐心等待..." -ForegroundColor Yellow
Write-Host ""

D:\flutter\flutter\bin\flutter.bat run

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

