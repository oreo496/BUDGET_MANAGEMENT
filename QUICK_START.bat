@echo off
REM QUICK START - For users who have already run setup.bat
echo.
echo ========================================
echo  QUICK START - BUDGET MANAGEMENT
echo ========================================
echo.
echo This assumes you have:
echo - Run setup.bat before
echo - PostgreSQL running
echo - Database 'funder' created
echo.
echo Press any key to continue...
pause

REM Start Backend
echo.
echo Starting Backend...
start "Backend - BUDGET_MANAGEMENT" cmd /k "cd /d "%~dp0backend" && call venv\Scripts\activate.bat && python manage.py migrate && python manage.py runserver"

timeout /t 5 /nobreak >nul

REM Start Frontend
echo Starting Frontend...
start "Frontend - BUDGET_MANAGEMENT" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo Services Starting!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Wait 10 seconds for servers to start, then open browser...
timeout /t 10 /nobreak >nul

REM Open browser
start http://localhost:3000

echo Done!
