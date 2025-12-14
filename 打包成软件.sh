#!/bin/bash

echo "========================================"
echo "  学术主页生成器 - Linux 打包工具"
echo "========================================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未检测到 Node.js"
    echo ""
    echo "请先安装 Node.js"
    exit 1
fi

echo "✓ Node.js 已安装"
echo ""

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "[1/4] 安装项目依赖..."
    echo ""
    npm install
    echo ""
    echo "✓ 依赖安装完成"
else
    echo "[1/4] ✓ 依赖已存在"
fi
echo ""

echo "[2/4] 构建 Next.js 生产版本..."
echo ""
npm run build
echo ""
echo "✓ Next.js 构建完成"
echo ""

echo "[3/4] 打包 Electron 桌面应用..."
echo "这可能需要几分钟时间，请耐心等待..."
echo ""
npm run dist
echo ""
echo "✓ Electron 打包完成"
echo ""

echo "[4/4] 完成！"
echo ""
echo "========================================"
echo "  🎉 打包成功！"
echo "========================================"
echo ""
echo "安装包位置："
echo "dist/学术主页生成器-*.AppImage    (Linux 通用)"
echo "dist/学术主页生成器-*.deb         (Debian/Ubuntu)"
echo "dist/学术主页生成器-*.rpm         (Fedora/RedHat)"
echo ""
echo "您可以："
echo "1. 直接运行 AppImage (chmod +x *.AppImage && ./学术主页生成器-*.AppImage)"
echo "2. 安装 deb/rpm 包"
echo "3. 分享给他人使用"
echo ""
echo "按任意键打开 dist 文件夹..."
read -n 1
xdg-open dist 2>/dev/null || nautilus dist 2>/dev/null || dolphin dist 2>/dev/null || echo "请手动打开 dist 文件夹"
