@echo off
echo ========================================
echo Creating Virtual Environment
echo ========================================
echo.

cd /d "%~dp0\backend"

echo Current directory: %CD%
echo.

if exist venv (
    echo Virtual environment already exists at:
    echo %CD%\venv
    echo.
    echo Testing activation...
    if exist venv\Scripts\activate.bat (
        echo [OK] Activation script found!
        echo.
        echo To activate, type:
        echo   venv\Scripts\activate
        echo.
    ) else (
        echo [ERROR] venv exists but activation script missing!
        echo Recreating virtual environment...
        rmdir /s /q venv
        goto :create
    )
) else (
    :create
    echo Virtual environment does NOT exist.
    echo Creating it now...
    echo.
    python -m venv venv
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to create virtual environment!
        echo.
        echo Possible issues:
        echo 1. Python not installed
        echo 2. Python not in PATH
        echo 3. Try: python3 -m venv venv
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created!
    echo Location: %CD%\venv
    echo.
)

echo Testing activation...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [SUCCESS] Virtual environment activated!
    echo.
    echo You should see (venv) at the start of your command prompt.
    echo.
    echo Next step: Install dependencies
    echo   pip install -r requirements.txt
) else if exist venv\Scripts\activate (
    call venv\Scripts\activate
    echo [SUCCESS] Virtual environment activated!
) else (
    echo [ERROR] Activation script still not found!
    echo Virtual environment might be corrupted.
    echo.
    echo Try deleting venv folder and running this script again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Virtual Environment Ready!
echo ========================================
echo.
pause

