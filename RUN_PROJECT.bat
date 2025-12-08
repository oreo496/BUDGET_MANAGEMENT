@echo off
echo ========================================
echo Starting Funder Application
echo ========================================
echo.

echo Checking if backend is already running...
netstat -ano | findstr :8000 >nul
if %errorlevel% == 0 (
    echo Backend is already running on port 8000
) else (
    echo Starting backend server...
    cd backend
    if not exist venv (
        echo Creating virtual environment...
        python -m venv venv
    )
    if exist venv\Scripts\activate.bat (
        start "Funder Backend" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate.bat && python manage.py runserver"
    ) else (
        start "Funder Backend" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate && python manage.py runserver"
    )
    cd ..
    timeout /t 3 /nobreak >nul
)

echo.
echo Checking if frontend is already running...
netstat -ano | findstr :3000 >nul
if %errorlevel% == 0 (
    echo Frontend is already running on port 3000
) else (
    echo Starting frontend server...
    start "Funder Frontend" cmd /k "cd frontend && npm run dev"
    timeout /t 5 /nobreak >nul
)

echo.
echo ========================================
echo Application Starting!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:3000
echo.
echo Press any key to exit (servers will keep running)...
pause >nul

