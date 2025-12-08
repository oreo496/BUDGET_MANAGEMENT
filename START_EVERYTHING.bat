@echo off
echo ========================================
echo Starting Funder Application
echo ========================================
echo.

echo Step 1: Starting Backend Server...
cd /d "%~dp0\backend"

REM Check if venv exists and activate
if exist venv\Scripts\activate.bat (
    start "Funder Backend" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate.bat && python manage.py runserver"
    echo [OK] Backend server starting in new window...
) else (
    echo [ERROR] Virtual environment not found!
    echo Please create it first: python -m venv venv
    pause
    exit /b 1
)

timeout /t 3 /nobreak >nul

echo.
echo Step 2: Starting Frontend Server...
cd /d "%~dp0\frontend"

if exist node_modules (
    start "Funder Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
    echo [OK] Frontend server starting in new window...
) else (
    echo [WARNING] node_modules not found!
    echo Installing dependencies first...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install frontend dependencies
        pause
        exit /b 1
    )
    start "Funder Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
    echo [OK] Frontend server starting...
)

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo Application Starting!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Two windows will open:
echo   - Backend server (keep it running)
echo   - Frontend server (keep it running)
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo If you see errors:
echo 1. Check backend window - make sure it shows "Starting server"
echo 2. Check frontend window - make sure it shows "Ready"
echo 3. Wait 10-15 seconds for both to fully start
echo 4. Refresh browser if needed
echo.
pause

