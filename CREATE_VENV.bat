@echo off
echo ========================================
echo Creating Virtual Environment
echo ========================================
echo.

cd /d "%~dp0\backend"

echo Current directory: %CD%
echo.

if exist venv (
    echo Virtual environment already exists!
    echo.
    echo Do you want to recreate it? (This will delete the old one)
    echo Press Y to recreate, N to keep existing
    choice /C YN /N /M "Recreate venv"
    if errorlevel 2 goto :keep_existing
    if errorlevel 1 goto :recreate
)

:create_new
echo Creating new virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to create virtual environment!
    echo.
    echo Possible issues:
    echo 1. Python is not installed
    echo 2. Python is not in PATH
    echo 3. Try using: python3 -m venv venv
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment created successfully!
goto :activate

:recreate
echo Deleting old virtual environment...
rmdir /s /q venv
echo Creating new virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment recreated!
goto :activate

:keep_existing
echo Keeping existing virtual environment.
goto :activate

:activate
echo.
echo Testing activation...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated!
    echo.
    echo You should see (venv) at the start of your command prompt
) else if exist venv\Scripts\activate (
    call venv\Scripts\activate
    echo [OK] Virtual environment activated!
) else (
    echo [ERROR] Activation script not found!
    echo Virtual environment might be corrupted.
    echo Try deleting the venv folder and running this script again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Install dependencies:
echo    pip install -r requirements.txt
echo.
echo 2. Start the server:
echo    python manage.py runserver
echo.
pause




