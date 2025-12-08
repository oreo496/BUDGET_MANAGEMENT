@echo off
echo ========================================
echo Easy Start - Funder Application
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Creating virtual environment (if needed)...
cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create venv
        echo Make sure Python is installed
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

echo.
echo Step 2: Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Cannot find activation script!
    echo Recreating venv...
    rmdir /s /q venv
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo [OK] Virtual environment activated
echo.

echo Step 3: Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.

echo Step 4: Checking .env file...
if not exist .env (
    echo Creating .env file...
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
    echo [IMPORTANT] Edit backend\.env and add your MySQL password!
    echo Find: DB_PASSWORD=
    echo Add: DB_PASSWORD=your_password
    timeout /t 3 /nobreak >nul
)

echo.
echo Step 5: Starting backend server...
echo.
echo Backend will start in a new window.
echo Keep that window open!
echo.
start "Funder Backend" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate.bat && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo.
echo Step 6: Starting frontend server...
cd ..\frontend

if not exist node_modules (
    echo Installing frontend dependencies...
    call npm install
)

echo.
echo Frontend will start in a new window.
echo Keep that window open too!
echo.
start "Funder Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo Application Starting!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:3000
echo.
echo If you see errors:
echo 1. Check backend window for database errors
echo 2. Make sure MySQL is running
echo 3. Check backend\.env has correct password
echo.
pause

