@echo off
echo ========================================
echo Setup .env File for Backend
echo ========================================
echo.

cd backend

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo [OK] .env file created
) else (
    echo [OK] .env file already exists
)

echo.
echo ========================================
echo Database Configuration
echo ========================================
echo.

set /p DB_PASS="Enter your MySQL password (press Enter if no password): "

echo.
echo Updating .env file...

REM Create a temporary file with updated password
(
    echo # Django Configuration
    echo SECRET_KEY=django-insecure-change-this-in-production
    echo DEBUG=True
    echo ALLOWED_HOSTS=localhost,127.0.0.1
    echo.
    echo # Database Configuration
    echo DB_NAME=funder
    echo DB_USER=root
    echo DB_PASSWORD=%DB_PASS%
    echo DB_HOST=localhost
    echo DB_PORT=3306
    echo.
    echo # JWT Configuration
    echo JWT_SECRET_KEY=django-insecure-change-this-in-production
    echo JWT_ALGORITHM=HS256
    echo.
    echo # Encryption Key
    echo ENCRYPTION_KEY=default-key-32-chars-long-change-this!!
) > .env.tmp

move /y .env.tmp .env >nul 2>&1

echo [OK] .env file updated with your MySQL password
echo.
echo Generating encryption key...
python -c "from cryptography.fernet import Fernet; key = Fernet.generate_key().decode(); print('ENCRYPTION_KEY=' + key)" >> .env 2>nul

if %errorlevel% == 0 (
    echo [OK] Encryption key generated
) else (
    echo [WARNING] Could not generate encryption key (cryptography not installed)
    echo You can add it manually later
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Your .env file is configured.
echo You can now start the backend server:
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
pause




