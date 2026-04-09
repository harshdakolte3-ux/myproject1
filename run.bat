@echo off
REM FoodHub - Online Food Ordering System
REM Setup and run script

echo.
echo ============================================
echo   FoodHub - Online Food Ordering System
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
python -m pip install --user -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Initializing database...
REM The database will be created automatically on first run

echo.
echo [3/3] Starting FoodHub server...
echo.
echo ============================================
echo   Server is running at http://localhost:5000
echo   Open your browser and navigate to the URL above
echo ============================================
echo.

python app.py

pause
