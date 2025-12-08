@echo off
echo ========================================
echo Fix Database Password Issue
echo ========================================
echo.

cd backend

if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env >nul 2>&1
    echo [OK] .env file created
) else (
    echo [OK] .env file exists
)

echo.
echo ========================================
echo IMPORTANT: Database Password Setup
echo ========================================
echo.
echo The error shows: "Access denied (using password: NO)"
echo This means your MySQL password is not set in .env file
echo.
echo Please follow these steps:
echo.
echo 1. Open: backend\.env
echo 2. Find the line: DB_PASSWORD=
echo 3. Add your MySQL password: DB_PASSWORD=your_actual_password
echo 4. Save the file
echo.
echo Example:
echo   DB_PASSWORD=mypassword123
echo.
echo If you don't have a MySQL password, leave it empty:
echo   DB_PASSWORD=
echo.
echo ========================================
echo.

echo Opening .env file for editing...
timeout /t 2 /nobreak >nul
notepad backend\.env

echo.
echo ========================================
echo After saving .env file:
echo ========================================
echo.
echo 1. Make sure MySQL is running
echo 2. Try starting backend again:
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
pause




