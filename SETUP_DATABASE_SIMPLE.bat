@echo off
echo ========================================
echo Simple Database Setup
echo ========================================
echo.

echo Step 1: Testing MySQL connection...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] MySQL command not found!
    echo.
    echo Please use MySQL Workbench instead:
    echo 1. Open MySQL Workbench
    echo 2. Connect to your server
    echo 3. Run: CREATE DATABASE funder;
    echo 4. Then run: USE funder;
    echo 5. Then run: SOURCE schema.sql;
    echo.
    pause
    exit /b 1
)

echo [OK] MySQL found
echo.

echo Step 2: Creating database...
echo.
echo You will be asked for your MySQL password.
echo If you don't have a password, just press Enter.
echo.

mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS funder;"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to create database!
    echo.
    echo Try this instead:
    echo 1. Open MySQL Workbench
    echo 2. Connect to server
    echo 3. Run: CREATE DATABASE funder;
    echo 4. Then run the schema.sql file
    echo.
    pause
    exit /b 1
)

echo [OK] Database created!
echo.

echo Step 3: Running schema.sql...
echo You will be asked for password again.
echo.

cd /d "%~dp0"
mysql -u root -p funder < schema.sql

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to run schema!
    echo.
    echo Try manually in MySQL Workbench:
    echo 1. Open schema.sql file
    echo 2. Copy all content
    echo 3. Paste in MySQL Workbench
    echo 4. Make sure 'funder' database is selected
    echo 5. Execute
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Schema applied!
echo.

echo Step 4: Verifying...
mysql -u root -p funder -e "SHOW TABLES;" 2>nul

echo.
echo ========================================
echo Database Setup Complete!
echo ========================================
echo.
echo You should see 10 tables listed above.
echo.
echo Now start the backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
pause




