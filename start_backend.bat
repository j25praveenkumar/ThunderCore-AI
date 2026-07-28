@echo off
title Thunder AI - Backend
color 0B
echo.
echo  ========================================
echo    THUNDER AI - Backend Server
echo  ========================================
echo.
cd /d "%~dp0"

:: Use Python 3.14 explicitly (where all packages are installed)
py -3.14 --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python 3.14 not found.
    echo  Install from https://python.org/downloads
    pause
    exit /b 1
)

:: Kill anything already on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " 2^>nul') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo  Installing / verifying dependencies...
py -3.14 -m pip install -r requirements.txt -q

echo  Starting FastAPI backend on http://127.0.0.1:8000
echo  API Docs: http://127.0.0.1:8000/docs
echo.
py -3.14 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

pause
