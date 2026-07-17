@echo off
title Thunder AI - Frontend
color 0A
echo.
echo  ========================================
echo    THUNDER AI - React Frontend
echo  ========================================
echo.
cd /d "%~dp0\frontend"

:: Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Node.js not found. Install from https://nodejs.org
    pause
    exit /b 1
)

:: Install npm packages if needed
if not exist "node_modules" (
    echo  Installing npm packages...
    npm install
)

echo  Starting React app on http://localhost:3000
echo.
npm start

pause
