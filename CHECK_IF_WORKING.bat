@echo off
echo ========================================
echo Checking Funder Application Status
echo ========================================
echo.

echo [1] Checking Backend (http://localhost:8000)...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Backend is running and responding!
    curl -s http://localhost:8000/health
    echo.
    echo.
) else (
    echo [ERROR] Backend is NOT running
    echo Start it with: START_BACKEND.bat
    echo.
)

echo [2] Checking Frontend (http://localhost:3000)...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Frontend is running and responding!
    echo Open: http://localhost:3000
    echo.
) else (
    echo [ERROR] Frontend is NOT running
    echo Start it with:
    echo   cd frontend
    echo   npm run dev
    echo.
)

echo ========================================
echo Summary
echo ========================================
echo.

curl -s http://localhost:8000/health >nul 2>&1
set BACKEND_OK=%errorlevel%

curl -s http://localhost:3000 >nul 2>&1
set FRONTEND_OK=%errorlevel%

if %BACKEND_OK% == 0 (
    if %FRONTEND_OK% == 0 (
        echo [SUCCESS] Both servers are running!
        echo.
        echo Backend: http://localhost:8000
        echo Frontend: http://localhost:3000
        echo.
        echo Open http://localhost:3000 in your browser
        echo You should see the Funder dashboard!
        echo.
        echo Opening browser now...
        timeout /t 2 /nobreak >nul
        start http://localhost:3000
    ) else (
        echo [PARTIAL] Backend is running, but Frontend is NOT
        echo.
        echo To start frontend:
        echo 1. Open a NEW Command Prompt
        echo 2. Type: cd frontend
        echo 3. Type: npm run dev
        echo 4. Wait for it to start
        echo 5. Open http://localhost:3000
    )
) else (
    if %FRONTEND_OK% == 0 (
        echo [PARTIAL] Frontend is running, but Backend is NOT
        echo.
        echo To start backend:
        echo 1. Double-click: START_BACKEND.bat
        echo 2. Or manually: cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
    ) else (
        echo [ERROR] Neither server is running!
        echo.
        echo Start backend: START_BACKEND.bat
        echo Start frontend: cd frontend ^&^& npm run dev
    )
)

echo.
pause




