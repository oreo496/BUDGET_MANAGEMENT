@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.

cd /d "%~dp0\backend"

echo Current directory: %CD%
echo.

REM Check if venv exists
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Creating virtual environment now...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        echo Make sure Python is installed
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
)

REM Activate virtual environment
echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo [ERROR] Cannot find activation script!
    echo Virtual environment might be corrupted.
    echo.
    echo Try running: CREATE_VENV.bat
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found!
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
    echo [OK] .env file created
    echo.
    echo [IMPORTANT] Please edit backend\.env and add your MySQL password!
    echo Find: DB_PASSWORD=
    echo Add: DB_PASSWORD=your_password
    echo.
    timeout /t 3 /nobreak >nul
)

echo.
echo Starting Django server...
echo.
python manage.py runserver

pause




