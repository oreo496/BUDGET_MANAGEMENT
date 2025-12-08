@echo off
echo ========================================
echo Creating Funder Database
echo ========================================
echo.

echo This script will:
echo 1. Create the 'funder' database
echo 2. Run the schema.sql to create all tables
echo.

set /p MYSQL_USER="Enter MySQL username (default: root): "
if "%MYSQL_USER%"=="" set MYSQL_USER=root

set /p MYSQL_PASS="Enter MySQL password (press Enter if no password): "

echo.
echo Creating database...
echo.

if "%MYSQL_PASS%"=="" (
    mysql -u %MYSQL_USER% -e "CREATE DATABASE IF NOT EXISTS funder;"
) else (
    mysql -u %MYSQL_USER% -p%MYSQL_PASS% -e "CREATE DATABASE IF NOT EXISTS funder;"
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to create database!
    echo.
    echo Possible issues:
    echo 1. MySQL is not running
    echo 2. Wrong username/password
    echo 3. MySQL not in PATH
    echo.
    echo Try manually:
    echo   mysql -u root -p
    echo   Then type: CREATE DATABASE funder;
    pause
    exit /b 1
)

echo [OK] Database 'funder' created!
echo.

echo Running schema.sql to create tables...
echo.

cd /d "%~dp0"

if "%MYSQL_PASS%"=="" (
    mysql -u %MYSQL_USER% funder < schema.sql
) else (
    mysql -u %MYSQL_USER% -p%MYSQL_PASS% funder < schema.sql
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to run schema.sql!
    echo.
    echo Try manually:
    echo   mysql -u root -p funder ^< schema.sql
    pause
    exit /b 1
)

echo [OK] Schema applied successfully!
echo.

echo Verifying tables were created...
if "%MYSQL_PASS%"=="" (
    mysql -u %MYSQL_USER% funder -e "SHOW TABLES;" 2>nul
) else (
    mysql -u %MYSQL_USER% -p%MYSQL_PASS% funder -e "SHOW TABLES;" 2>nul
)

echo.
echo ========================================
echo Database Setup Complete!
echo ========================================
echo.
echo You should see tables like: users, transactions, budgets, etc.
echo.
echo Now you can start the backend server!
echo.
pause




