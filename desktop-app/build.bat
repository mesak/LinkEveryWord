@echo off
chcp 65001 >nul
echo ===============================================
echo Everything Flask 搜尋應用程式 - 打包工具
echo ===============================================
echo.

echo 檢查 Python 環境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤: 找不到 Python，請先安裝 Python
    pause
    exit /b 1
)

echo 檢查 PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 安裝 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo 錯誤: PyInstaller 安裝失敗
        pause
        exit /b 1
    )
)

echo 檢查必要套件...
python -c "import flask, flask_cors" >nul 2>&1
if errorlevel 1 (
    echo 安裝必要套件...
    pip install flask flask-cors
    if errorlevel 1 (
        echo 錯誤: 套件安裝失敗
        pause
        exit /b 1
    )
)

echo.
echo 清理舊的建置檔案...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"

echo.
echo 開始打包應用程式...
echo 這可能需要幾分鐘時間，請耐心等待...
echo.

pyinstaller --clean app_standalone.spec

if errorlevel 1 (
    echo.
    echo ❌ 打包失敗！
    echo 請檢查錯誤訊息並重試
    pause
    exit /b 1
)

echo.
echo ✅ 打包成功！
echo.
echo 📁 執行檔位置: dist\EverythingFlaskSearch.exe
echo.
echo 💡 使用方法:
echo 1. 雙擊 dist\EverythingFlaskSearch.exe 啟動應用程式
echo 2. 應用程式會自動開啟瀏覽器
echo 3. 在 Web 介面中搜尋檔案
echo.
echo 📋 注意事項:
echo - 執行檔大約 20-50MB
echo - 首次啟動可能較慢 (3-5秒)
echo - 如果要使用完整功能，請確保 Everything 搜尋引擎已安裝並運行
echo - 沒有 Everything 時，會以示範模式運行
echo.

set /p choice="是否現在測試執行檔? (y/N): "
if /i "!choice!"=="y" (
    echo 啟動測試...
    cd dist
    EverythingFlaskSearch.exe
)

echo.
echo 打包完成！
pause
