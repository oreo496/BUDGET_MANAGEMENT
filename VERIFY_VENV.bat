@echo off
echo ========================================
echo Verifying Virtual Environment
echo ========================================
echo.

cd /d "%~dp0\backend"

echo Checking if venv exists...
if exist venv (
    echo [OK] venv folder exists
    echo Location: %CD%\venv
    echo.
    
    echo Checking activation script...
    if exist venv\Scripts\activate.bat (
        echo [OK] Activation script found!
        echo.
        echo Testing activation...
        call venv\Scripts\activate.bat
        echo [SUCCESS] Virtual environment activated!
        echo.
        echo You should see (venv) in your command prompt now.
        echo.
        
        echo Checking Python in venv...
        python --version
        echo.
        
        echo Checking if Django is installed...
        python -c "import django; print('Django version:', django.get_version())" 2>nul
        if %errorlevel% == 0 (
            echo [OK] Django is installed!
        ) else (
            echo [WARNING] Django not found - need to install dependencies
            echo Run: pip install -r requirements.txt
        )
    ) else (
        echo [ERROR] Activation script not found!
        echo The venv might be incomplete.
        echo Try recreating it.
    )
) else (
    echo [ERROR] venv folder does NOT exist!
    echo.
    echo You need to create it first:
    echo   python -m venv venv
)

echo.
echo ========================================
echo Verification Complete
echo ========================================
echo.
pause

