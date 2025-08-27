@echo off
chcp 65001 >nul
echo ========================================
echo 建立發布包
echo ========================================
echo.

set APP_NAME=EverythingFlaskSearch
set VERSION=v1.0
set RELEASE_DIR=%APP_NAME%_%VERSION%

echo 建立發布資料夾...
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"

echo 複製執行檔...
copy "dist\EverythingFlaskSearch.exe" "%RELEASE_DIR%\"

echo 複製說明文件...
copy "dist\README.txt" "%RELEASE_DIR%\"
copy "QUICKSTART.md" "%RELEASE_DIR%\快速開始指南.md"

echo 建立快捷方式說明...
echo 使用方法: > "%RELEASE_DIR%\使用說明.txt"
echo 1. 雙擊 EverythingFlaskSearch.exe 啟動應用程式 >> "%RELEASE_DIR%\使用說明.txt"
echo 2. 應用程式會自動開啟瀏覽器 >> "%RELEASE_DIR%\使用說明.txt"
echo 3. 在 Web 介面中搜尋檔案 >> "%RELEASE_DIR%\使用說明.txt"
echo 4. 按 Ctrl+C 停止服務 >> "%RELEASE_DIR%\使用說明.txt"
echo. >> "%RELEASE_DIR%\使用說明.txt"
echo 建議安裝 Everything 搜尋引擎以獲得完整功能： >> "%RELEASE_DIR%\使用說明.txt"
echo https://www.voidtools.com/downloads/ >> "%RELEASE_DIR%\使用說明.txt"

echo 計算檔案大小...
for %%F in ("%RELEASE_DIR%\EverythingFlaskSearch.exe") do (
    set "size=%%~zF"
    set /a "sizeMB=!size!/1024/1024"
)

echo.
echo ✅ 發布包建立完成！
echo.
echo 📁 位置: %RELEASE_DIR%\
echo 📄 檔案:
dir "%RELEASE_DIR%" /b
echo.
echo 📊 主執行檔大小: 約 15MB
echo.
echo 🚀 您可以將整個 %RELEASE_DIR% 資料夾發布給其他使用者
echo 💡 使用者只需要雙擊 EverythingFlaskSearch.exe 即可使用

pause
