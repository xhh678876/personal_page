@echo off
chcp 65001 >nul
echo ========================================
echo  学术主页生成器 - 桌面版
echo ========================================
echo.

REM 检查依赖
if not exist "node_modules" (
    echo [1/3] 首次运行，正在安装依赖...
    echo.
    call npm install
    echo.
    echo ✓ 依赖安装完成
    echo.
) else (
    echo [1/3] ✓ 依赖检查完成
    echo.
)

REM 构建 Next.js
if not exist ".next" (
    echo [2/3] 构建应用程序...
    echo.
    call npm run build
    echo.
    echo ✓ 构建完成
    echo.
) else (
    echo [2/3] ✓ 应用已构建
    echo.
)

echo [3/3] 正在启动桌面应用...
echo.
echo ========================================
echo  应用即将在新窗口中打开
echo ========================================
echo.
echo 按 Ctrl+C 可关闭应用
echo.

call npm run electron
