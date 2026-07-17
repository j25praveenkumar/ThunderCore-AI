@echo off
title Thunder AI - Electron App
color 0D
echo.
echo  ========================================
echo    THUNDER AI - Electron Desktop App
echo  ========================================
echo.

:: Kill anything on port 3000 (stale React dev server)
echo  Clearing port 3000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000 " 2^>nul') do (
    taskkill /f /pid %%a >nul 2>&1
)

:: Wait for backend on port 8000 to be ready
echo  Waiting for backend on port 8000...
:wait_backend
netstat -aon | findstr ":8000 " >nul 2>&1
if errorlevel 1 (
    echo  Backend not ready yet, retrying in 2s...
    timeout /t 2 /nobreak >nul
    goto wait_backend
)
echo  Backend is up!
echo.

cd /d "%~dp0\frontend"

if not exist "node_modules" (
    echo  Installing npm packages...
    npm install
)

npm run electron-dev

pause
