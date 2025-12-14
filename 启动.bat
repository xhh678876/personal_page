@echo off
echo ========================================
echo  学术主页生成器 - Academic Homepage Generator
echo  Version 2.0 Pro
echo ========================================
echo.

REM 检查 node_modules 是否存在
if not exist "node_modules" (
    echo [1/2] 首次运行，正在安装依赖...
    echo 这可能需要几分钟时间，请耐心等待...
    echo.
    call npm install
    echo.
    echo ✓ 依赖安装完成！
    echo.
) else (
    echo [1/2] 依赖检查完成
    echo.
)

echo [2/2] 正在启动开发服务器...
echo.
echo ========================================
echo  服务器即将启动在:
echo  http://localhost:3000
echo ========================================
echo.
echo 提示：
echo - 使用 Gemini API（推荐）：免费获取 https://aistudio.google.com/app/apikey
echo - 使用 OpenAI API：https://platform.openai.com/api-keys
echo.
echo 按 Ctrl+C 可停止服务器
echo.

call npm run dev
