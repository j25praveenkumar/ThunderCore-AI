@echo off
title Thunder AI - Backend
color 0B
echo.
echo  ========================================
echo    THUNDER AI - Backend Server
echo  ========================================
echo.
cd /d "%~dp0"

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Install Python 3.12+
    pause
    exit /b 1
)

:: Kill anything already on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " 2^>nul') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo  Installing / verifying dependencies...
pip install -r requirements.txt -q

echo  Starting FastAPI backend on http://127.0.0.1:8000
echo  API Docs: http://127.0.0.1:8000/docs
echo.
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

pause
