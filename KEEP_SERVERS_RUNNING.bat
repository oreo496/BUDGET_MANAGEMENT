@echo off
title Funder App - Keep Servers Running
color 0A
echo ================================================
echo   FUNDER BUDGET MANAGEMENT - SERVER MONITOR
echo ================================================
echo.
echo This script will keep both servers running
echo Backend: http://127.0.0.1:8000/
echo Frontend: http://localhost:3000/
echo.
echo Press Ctrl+C to stop all servers
echo ================================================
echo.

:START
echo [%TIME%] Starting backend server...
start "Backend Server" /MIN cmd /k "cd /d %~dp0backend && ..\.venv\Scripts\python.exe manage.py runserver"

timeout /t 5 /nobreak >nul

echo [%TIME%] Starting frontend server...
start "Frontend Server" /MIN cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ================================================
echo Both servers are now running!
echo.
echo Backend: http://127.0.0.1:8000/
echo Frontend: http://localhost:3000/
echo Admin Panel: http://localhost:3000/admin/login
echo.
echo To stop servers: Close the "Backend Server" and "Frontend Server" windows
echo ================================================
echo.

:MONITOR
timeout /t 30 /nobreak >nul
tasklist /FI "WINDOWTITLE eq Backend Server*" 2>NUL | find /I /N "cmd.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo [%TIME%] Backend server stopped! Restarting...
    start "Backend Server" /MIN cmd /k "cd /d %~dp0backend && ..\.venv\Scripts\python.exe manage.py runserver"
)

tasklist /FI "WINDOWTITLE eq Frontend Server*" 2>NUL | find /I /N "cmd.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo [%TIME%] Frontend server stopped! Restarting...
    start "Frontend Server" /MIN cmd /k "cd /d %~dp0frontend && npm run dev"
)

goto MONITOR
