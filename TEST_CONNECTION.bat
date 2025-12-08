@echo off
echo ========================================
echo Testing Funder Application Connection
echo ========================================
echo.

echo Testing Backend (http://localhost:8000)...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Backend is running and responding!
    curl -s http://localhost:8000/health
    echo.
) else (
    echo [FAILED] Backend is not responding
    echo Make sure backend is running: cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
    echo.
)

echo Testing Frontend (http://localhost:3000)...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Frontend is running and responding!
    echo Open http://localhost:3000 in your browser
    echo.
) else (
    echo [FAILED] Frontend is not responding
    echo Make sure frontend is running: cd frontend ^&^& npm run dev
    echo.
)

echo ========================================
echo Test Complete
echo ========================================
echo.
pause

