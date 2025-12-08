@echo off
echo ========================================
echo Finding .env File Location
echo ========================================
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Looking for .env file in backend folder...
if exist "backend\.env" (
    echo [FOUND] .env file is here:
    echo %CD%\backend\.env
    echo.
    echo Opening it now...
    timeout /t 2 /nobreak >nul
    notepad "backend\.env"
) else (
    echo [NOT FOUND] .env file does not exist!
    echo.
    echo Creating it now...
    if exist "backend\.env.example" (
        copy "backend\.env.example" "backend\.env" >nul 2>&1
        echo [OK] Created .env file from .env.example
        echo.
        echo Opening it for you to edit...
        timeout /t 2 /nobreak >nul
        notepad "backend\.env"
    ) else (
        echo [ERROR] .env.example not found either!
        echo Creating new .env file...
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
        ) > "backend\.env"
        echo [OK] Created new .env file
        echo.
        echo Opening it for you to edit...
        timeout /t 2 /nobreak >nul
        notepad "backend\.env"
    )
)

echo.
echo ========================================
echo IMPORTANT: Add Your MySQL Password
echo ========================================
echo.
echo In the file that just opened, find this line:
echo   DB_PASSWORD=
echo.
echo Add your MySQL password:
echo   DB_PASSWORD=your_password_here
echo.
echo If you don't have a password, leave it empty:
echo   DB_PASSWORD=
echo.
echo Save the file (Ctrl+S) and close Notepad
echo.
pause




