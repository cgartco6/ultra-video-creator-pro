@echo off
echo ================================================
echo Ultra Video Creator Pro - FIXED Setup
echo ================================================

cd /d "%\~dp0"

echo Current folder: %CD%

if not exist "ultra-builder.py" (
    echo ERROR: ultra-builder.py not found in this folder.
    pause
    exit /b
)

echo Running builder...
python ultra-builder.py

echo Creating docker-compose.yml...
echo version: '3.9' > docker-compose.yml
echo services: >> docker-compose.yml
echo   orchestrator: >> docker-compose.yml
echo     build: ./orchestrator >> docker-compose.yml
echo     ports: >> docker-compose.yml
echo       - "8000:8000" >> docker-compose.yml

echo Starting services...
docker-compose up --build -d

echo.
echo ================================================
echo SUCCESS - Project should be running.
echo Open browser: http://localhost:3000
echo ================================================
pause
