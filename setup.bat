@echo off
echo ========================================
echo Funder Project Setup Script (Windows)
echo ========================================
echo.

echo Step 1: Setting up Backend...
echo.

cd backend

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python is installed and in PATH
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit backend\.env file with your database credentials!
    echo.
)

echo.
echo Step 2: Setting up Frontend...
echo.

cd ..\frontend

echo Installing Node dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node dependencies
    echo Make sure Node.js is installed
    pause
    exit /b 1
)

echo.
echo Creating .env.local file...
if not exist .env.local (
    copy .env.example .env.local
    echo.
    echo IMPORTANT: Please edit frontend\.env.local file with your API URL!
    echo.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create MySQL database: mysql -u root -p ^< schema.sql
echo 2. Edit backend\.env with database credentials
echo 3. Edit frontend\.env.local with API URL
echo 4. Run backend: cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
echo 5. Run frontend: cd frontend ^&^& npm run dev
echo.
pause

