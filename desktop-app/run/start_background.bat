@echo off
echo 正在啟動 EverythingFlaskSearch 後台服務...

:: 檢查可執行文件是否存在
if not exist "EverythingFlaskSearch.exe" (
    echo 錯誤: 找不到可執行文件 EverythingFlaskSearch.exe
    echo 請先重新下載最新版本的應用程序
    pause
    exit /b 1
)

:: 在後台啟動應用程序
echo 啟動後台服務...
start /B "EverythingFlaskSearch" "EverythingFlaskSearch.exe"

echo 服務已在後台啟動！
echo 您可以關閉此視窗，服務將繼續執行。
echo 要停止服務，請在工作管理員中結束 EverythingFlaskSearch.exe 程序。

:: 等待幾秒鐘讓使用者看到訊息
timeout /t 3 /nobreak >nul
