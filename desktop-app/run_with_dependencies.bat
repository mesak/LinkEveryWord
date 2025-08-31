@echo off
echo 正在检查并安装 Windows Search API 依赖...

:: 检查 Python 是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 找不到 Python，请确保 Python 已安装并在 PATH 中
    pause
    exit /b 1
)

:: 尝试安装 pywin32
echo 正在安装 pywin32...
python -m pip install pywin32
if errorlevel 1 (
    echo 警告: pywin32 安装失败，将使用简化的搜索模式
) else (
    echo 成功安装 pywin32
)

:: 运行应用程序
echo 启动应用程序...
python app_standalone.py

pause
