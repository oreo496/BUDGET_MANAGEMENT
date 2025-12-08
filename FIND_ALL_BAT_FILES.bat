@echo off
echo ========================================
echo Finding All .bat Files in Project
echo ========================================
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Looking for .bat files...
echo.

dir /b *.bat

echo.
echo ========================================
echo Files Found Above
echo ========================================
echo.
echo To run any file, just double-click it!
echo.
echo Most useful files:
echo   - CREATE_VENV_FIX.bat (Create virtual environment)
echo   - EASY_START.bat (Start everything automatically)
echo   - START_BACKEND.bat (Just start backend)
echo.
pause

