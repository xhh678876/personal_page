@echo off
chcp 65001 >nul
echo ========================================
echo  学术主页生成器 - 桌面版打包工具
echo ========================================
echo.

REM 检查 Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误：未检测到 Node.js
    echo.
    echo 请先安装 Node.js：https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo ✓ Node.js 已安装
echo.

REM 检查依赖
if not exist "node_modules" (
    echo [1/4] 安装项目依赖...
    echo.
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ❌ 依赖安装失败！
        pause
        exit /b 1
    )
    echo.
    echo ✓ 依赖安装完成
) else (
    echo [1/4] ✓ 依赖已存在
)
echo.

echo [2/4] 构建 Next.js 生产版本...
echo.
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Next.js 构建失败！
    pause
    exit /b 1
)
echo.
echo ✓ Next.js 构建完成
echo.

echo [3/4] 打包 Electron 桌面应用...
echo 这可能需要几分钟时间，请耐心等待...
echo.
call npm run dist
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Electron 打包失败！
    pause
    exit /b 1
)
echo.
echo ✓ Electron 打包完成
echo.

echo [4/4] 完成！
echo.
echo ========================================
echo  🎉 打包成功！
echo ========================================
echo.
echo 安装程序位置：
echo dist\学术主页生成器 Setup.exe
echo.
echo 您可以：
echo 1. 直接运行安装程序
echo 2. 分享给他人使用（无需安装 Node.js）
echo.
echo 按任意键打开 dist 文件夹...
pause >nul
explorer dist
