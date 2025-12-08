@echo off
echo ========================================
echo Opening .env File for You
echo ========================================
echo.

cd /d "%~dp0\backend"

if exist ".env" (
    echo [OK] Found .env file
    echo Opening it now...
    notepad .env
) else (
    echo [ERROR] .env file not found!
    echo Creating it now...
    (
        echo # Django Configuration
        echo SECRET_KEY=django-insecure-change-this-in-production
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo.
        echo # Database Configuration
        echo DB_NAME=funder
        echo DB_USER=root
        echo DB_PASSWORD=
        echo DB_HOST=localhost
        echo DB_PORT=3306
        echo.
        echo # JWT Configuration
        echo JWT_SECRET_KEY=django-insecure-change-this-in-production
        echo JWT_ALGORITHM=HS256
        echo.
        echo # Encryption Key
        echo ENCRYPTION_KEY=default-key-32-chars-long-change-this!!
    ) > .env
    echo [OK] Created .env file
    echo Opening it now...
    notepad .env
)

echo.
echo ========================================
echo IMPORTANT: Add Your MySQL Password
echo ========================================
echo.
echo In the Notepad window that just opened:
echo.
echo 1. Find the line: DB_PASSWORD=
echo 2. Add your MySQL password after the = sign
echo    Example: DB_PASSWORD=mypassword123
echo.
echo 3. If you don't have a MySQL password, leave it empty:
echo    DB_PASSWORD=
echo.
echo 4. Save the file (Ctrl+S)
echo 5. Close Notepad
echo.
echo Then try starting the backend again!
echo.
pause




