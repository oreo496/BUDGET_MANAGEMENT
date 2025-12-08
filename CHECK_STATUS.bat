@echo off
echo ========================================
echo Funder Application Status Check
echo ========================================
echo.

echo Checking Backend (port 8000)...
netstat -ano | findstr :8000 >nul
if %errorlevel% == 0 (
    echo [OK] Backend is running on http://localhost:8000
    curl -s http://localhost:8000/health >nul 2>&1
    if %errorlevel% == 0 (
        echo [OK] Backend health check passed
    ) else (
        echo [WARNING] Backend is running but health check failed
    )
) else (
    echo [ERROR] Backend is NOT running
    echo Start it with: cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
)

echo.
echo Checking Frontend (port 3000)...
netstat -ano | findstr :3000 >nul
if %errorlevel% == 0 (
    echo [OK] Frontend is running on http://localhost:3000
) else (
    echo [ERROR] Frontend is NOT running
    echo Start it with: cd frontend ^&^& npm run dev
)

echo.
echo Checking MySQL...
sc query MySQL80 >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] MySQL service found
) else (
    echo [WARNING] MySQL service not found or not running
)

echo.
echo ========================================
echo Status Check Complete
echo ========================================
echo.
pause

