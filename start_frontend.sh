#!/bin/bash

# 🚀 前端项目快速启动脚本 (macOS/Linux)

echo "================================"
echo "  极简MVP - 前端项目启动脚本"
echo "================================"
echo ""

# 检查 Flutter 是否安装
echo "📋 检查 Flutter 环境..."
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter 未安装或不在 PATH 中"
    echo ""
    echo "请按照以下步骤安装 Flutter:"
    echo "1. 访问 https://flutter.dev/docs/get-started/install/macos"
    echo "2. 下载并解压 Flutter SDK"
    echo "3. 将 Flutter/bin 添加到 ~/.bash_profile 或 ~/.zshrc"
    echo "4. 重启终端"
    echo ""
    exit 1
fi

echo "✅ Flutter 已安装"
flutter --version
echo ""

# 检查 Android 模拟器或 iOS 模拟器
echo "📱 检查可用设备..."
flutter devices
echo ""

# 进入前端目录
echo "📂 进入前端项目目录..."
cd "$(dirname "$0")/frontend" || exit 1
echo "✅ 当前目录: $(pwd)"
echo ""

# 获取依赖
echo "📦 获取项目依赖..."
flutter pub get
if [ $? -ne 0 ]; then
    echo "❌ 获取依赖失败"
    exit 1
fi
echo "✅ 依赖获取成功"
echo ""

# 检查后端服务
echo "🔍 检查后端服务..."
if curl -s http://localhost:8000/docs > /dev/null; then
    echo "✅ 后端服务正在运行"
else
    echo "⚠️  后端服务未运行"
    echo ""
    echo "请在另一个终端运行以下命令启动后端服务:"
    echo "cd backend"
    echo "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    read -p "继续运行前端? (Y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi
echo ""

# 启动应用
echo "🚀 启动应用..."
echo ""
echo "提示:"
echo "- 按 'r' 进行热重载"
echo "- 按 'R' 进行完整重启"
echo "- 按 'q' 退出应用"
echo ""

flutter run

echo ""
echo "================================"
echo "  应用已关闭"
echo "================================"

