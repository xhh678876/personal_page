#!/bin/bash

echo "========================================"
echo "  学术主页生成器 - Linux 版启动"
echo "========================================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未检测到 Node.js"
    echo ""
    echo "请先安装 Node.js："
    echo "Ubuntu/Debian: sudo apt install nodejs npm"
    echo "Fedora: sudo dnf install nodejs npm"
    echo "Arch: sudo pacman -S nodejs npm"
    echo ""
    echo "或访问：https://nodejs.org/"
    exit 1
fi

echo "✓ Node.js 已安装: $(node -v)"
echo ""

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "[1/2] 首次运行，正在安装依赖..."
    echo ""
    npm install
    echo ""
    echo "✓ 依赖安装完成"
    echo ""
else
    echo "[1/2] ✓ 依赖检查完成"
    echo ""
fi

echo "[2/2] 正在启动开发服务器..."
echo ""
echo "========================================"
echo "  服务器即将启动在:"
echo "  http://localhost:3000"
echo "========================================"
echo ""
echo "提示："
echo "- 使用 Gemini API（推荐）：免费获取 https://aistudio.google.com/app/apikey"
echo "- 使用 OpenAI API：https://platform.openai.com/api-keys"
echo ""
echo "按 Ctrl+C 可停止服务器"
echo ""

npm run dev
