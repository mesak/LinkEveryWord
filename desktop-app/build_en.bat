@echo off
chcp 65001 >nul
echo ===============================================
echo Everything Flask Search Application - Packager
echo ===============================================
echo.

echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found, please install Python first
    pause
    exit /b 1
)

echo Checking PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo Error: PyInstaller installation failed
        pause
        exit /b 1
    )
)

echo Checking required packages...
python -c "import flask, flask_cors" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install flask flask-cors
    if errorlevel 1 (
        echo Error: Package installation failed
        pause
        exit /b 1
    )
)

echo.
echo Cleaning old build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"

echo.
echo Starting to package the application...
echo This may take a few minutes, please wait...
echo.

python -m PyInstaller --clean D:\Work\LinkEveryWord\desktop-app\app_standalone.spec

if errorlevel 1 (
    echo.
    echo Build failed!
    echo Please check the error message and try again
    pause
    exit /b 1
)

echo.
echo Build successful!
echo.
echo Executable location: dist\EverythingFlaskSearch.exe
echo.
echo Usage:
echo 1. Double-click dist\EverythingFlaskSearch.exe to start the application
echo 2. The application will automatically open the browser
echo 3. Search for files in the web interface
echo.
echo Notes:
echo - The executable file is about 20-50MB
echo - The first launch may be slow (3-5 seconds)
echo - To use the full function, please ensure that the Everything search engine is installed and running
echo - When Everything is not available, it will run in demo mode
echo.

set /p choice="Test the executable now? (y/N): "
if /i "!choice!"=="y" (
    echo Starting test...
    cd dist
    EverythingFlaskSearch.exe
)

echo.
echo Packaging complete!
pause
