#!/bin/bash

echo "========================================"
echo "  学术主页生成器 - Linux 桌面版"
echo "========================================"
echo ""

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "[1/3] 首次运行，正在安装依赖..."
    echo ""
    npm install
    echo ""
    echo "✓ 依赖安装完成"
    echo ""
else
    echo "[1/3] ✓ 依赖检查完成"
    echo ""
fi

# 构建 Next.js
if [ ! -d ".next" ]; then
    echo "[2/3] 构建应用程序..."
    echo ""
    npm run build
    echo ""
    echo "✓ 构建完成"
    echo ""
else
    echo "[2/3] ✓ 应用已构建"
    echo ""
fi

echo "[3/3] 正在启动桌面应用..."
echo ""
echo "========================================"
echo "  应用即将在新窗口中打开"
echo "========================================"
echo ""
echo "按 Ctrl+C 可关闭应用"
echo ""

npm run electron
