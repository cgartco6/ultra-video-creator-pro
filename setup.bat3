@echo off
echo ================================================
echo Ultra Video Creator Pro - Setup
echo ================================================

cd /d "%\~dp0"

echo Current folder: %CD%

if not exist "ultra-builder.py" (
    echo ERROR: Cannot find ultra-builder.py
    echo Make sure you are in the main project folder.
    pause
    exit /b
)

echo Running builder...
python ultra-builder.py

echo Starting services...
docker-compose up --build -d

echo.
echo ================================================
echo SUCCESS! Project should be ready.
echo Open browser -> http://localhost:3000
echo ================================================
pause
