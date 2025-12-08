@echo off
echo ========================================
echo Installing Backend Dependencies
echo ========================================
echo.

cd /d "%~dp0\backend"

echo Step 1: Checking virtual environment...
if not exist venv (
    echo Virtual environment not found. Creating it...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

echo.
echo Step 2: Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Cannot activate virtual environment
    pause
    exit /b 1
)

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 4: Installing dependencies from requirements.txt...
echo This may take 2-3 minutes...
echo.

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo.
    echo Try manually:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now start the backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
pause

