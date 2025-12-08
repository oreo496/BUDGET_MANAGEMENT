@echo off
echo ========================================
echo COMPLETE FIX - Funder Application
echo ========================================
echo.

echo Step 1: Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo [OK] Python found

echo.
echo Step 2: Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found! Please install Node.js 18+
    pause
    exit /b 1
)
echo [OK] Node.js found

echo.
echo Step 3: Setting up Backend...
cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        echo Make sure Python is installed correctly
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo [ERROR] Cannot find virtual environment activation script
    echo Recreating virtual environment...
    rmdir /s /q venv
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo Installing/updating Python dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install backend dependencies
    pause
    exit /b 1
)
echo [OK] Backend dependencies installed

if not exist .env (
    echo Creating .env file...
    copy .env.example .env >nul 2>&1
    echo.
    echo [IMPORTANT] Please edit backend\.env and add your MySQL password!
    echo Set: DB_PASSWORD=your_mysql_password
    echo.
    timeout /t 3 /nobreak >nul
)

echo.
echo Step 4: Setting up Frontend...
cd ..\frontend

if not exist node_modules (
    echo Installing Node dependencies (this may take a few minutes)...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install frontend dependencies
        pause
        exit /b 1
    )
) else (
    echo [OK] Frontend dependencies already installed
)

if not exist .env.local (
    echo Creating .env.local file...
    copy .env.example .env.local >nul 2>&1
    echo [OK] Created .env.local
)

echo.
echo Step 5: Starting servers...
echo.

cd ..\backend
start "Funder Backend" cmd /k "venv\Scripts\activate && python manage.py runserver"
echo [OK] Backend server starting...

timeout /t 3 /nobreak >nul

cd ..\frontend
start "Funder Frontend" cmd /k "npm run dev"
echo [OK] Frontend server starting...

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:3000
echo.
echo If the site doesn't load:
echo 1. Wait 10-15 seconds for servers to fully start
echo 2. Check backend terminal for errors
echo 3. Check frontend terminal for errors
echo 4. Make sure MySQL is running
echo 5. Check backend\.env has correct database password
echo.
pause

