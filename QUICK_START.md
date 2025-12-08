# Quick Start Guide - Get Funder Running

This guide will help you set up and run the Funder application step by step.

## Prerequisites

Before starting, make sure you have:

1. **Python 3.8+** installed
   - Check: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Node.js 18+** installed
   - Check: `node --version`
   - Download: https://nodejs.org/

3. **MySQL 8.0+** installed and running
   - Check: `mysql --version`
   - Download: https://dev.mysql.com/downloads/mysql/

4. **Git** (optional, for version control)

---

## Step 1: Database Setup

### 1.1 Start MySQL Service

**Windows:**
- Open Services (Win + R, type `services.msc`)
- Find "MySQL80" and start it

**Mac/Linux:**
```bash
sudo systemctl start mysql
# or
sudo service mysql start
```

### 1.2 Create Database

Open MySQL command line or MySQL Workbench:

```bash
mysql -u root -p
```

Then run:

```sql
CREATE DATABASE IF NOT EXISTS funder;
EXIT;
```

### 1.3 Run Schema Script

From the project root directory:

```bash
mysql -u root -p funder < schema.sql
```

Or if you're already in MySQL:

```sql
USE funder;
SOURCE schema.sql;
```

**Verify tables were created:**
```sql
SHOW TABLES;
-- Should show: users, admins, categories, bank_accounts, transactions, budgets, goals, ai_alerts, system_logs, admin_actions
```

---

## Step 2: Backend Setup (Django)

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 2.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

If you get errors, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4 Configure Environment Variables

**Windows:**
```bash
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

**Edit `.env` file** with your database credentials:

```env
# Django Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=funder
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_HOST=localhost
DB_PORT=3306

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-this
JWT_ALGORITHM=HS256

# Encryption Key (generate with command below)
ENCRYPTION_KEY=your-encryption-key-32-chars-long
```

### 2.5 Generate Encryption Key

Run this command to generate a secure encryption key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the output and paste it as `ENCRYPTION_KEY` in your `.env` file.

### 2.6 Run Database Migrations

Since we're using existing tables, we'll fake the initial migrations:

```bash
python manage.py migrate --fake-initial
```

If that doesn't work, try:
```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

### 2.7 Create Django Superuser (Optional)

For admin panel access:

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### 2.8 Test Backend Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

**Test it:**
- Open browser: http://localhost:8000/admin
- Or test API: http://localhost:8000/api/auth/register

**If you see errors:**
- Check database connection in `.env`
- Make sure MySQL is running
- Verify database name is correct

**Stop the server:** Press `Ctrl+C`

---

## Step 3: Frontend Setup (Next.js)

### 3.1 Open New Terminal Window

Keep backend running in first terminal, open a new terminal for frontend.

### 3.2 Navigate to Frontend Directory

```bash
cd frontend
```

### 3.3 Install Node Dependencies

```bash
npm install
```

This may take a few minutes. If you get errors:
```bash
npm cache clean --force
npm install
```

### 3.4 Configure Environment Variables

**Windows:**
```bash
copy .env.example .env.local
```

**Mac/Linux:**
```bash
cp .env.example .env.local
```

**Edit `.env.local` file:**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Funder
```

### 3.5 Test Frontend Server

```bash
npm run dev
```

You should see:
```
✓ Ready in 2.5s
○ Local:        http://localhost:3000
```

**Open browser:** http://localhost:3000

You should see the Funder dashboard!

**Stop the server:** Press `Ctrl+C`

---

## Step 4: Verify Everything Works

### 4.1 Backend API Test

With backend running (`python manage.py runserver`):

**Test Registration:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**Or use Postman/Thunder Client** to test the API endpoints.

### 4.2 Frontend Test

With frontend running (`npm run dev`):

1. Open http://localhost:3000
2. You should see the Dashboard
3. Try navigating to different pages:
   - Transactions
   - Accounts
   - Investments
   - Cards
   - Settings

### 4.3 Check Console for Errors

- **Backend:** Check terminal for Django errors
- **Frontend:** Open browser DevTools (F12) → Console tab

---

## Step 5: Seed Database (Optional)

To add sample data for testing:

```bash
cd backend
python database/seeders/seed_data.py
```

This creates sample users, transactions, budgets, and goals.

---

## Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError: No module named 'django'"**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Error: "Access denied for user 'root'@'localhost'"**
- Check MySQL password in `.env` file
- Reset MySQL password if needed

**Error: "Table doesn't exist"**
```bash
# Re-run schema
mysql -u root -p funder < ../schema.sql
python manage.py migrate --fake-initial
```

**Error: "Port 8000 already in use"**
```bash
# Use different port
python manage.py runserver 8001
```

### Frontend Issues

**Error: "Cannot find module"**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 3000 already in use"**
```bash
# Use different port
npm run dev -- -p 3001
```

**Error: "API connection failed"**
- Make sure backend is running
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend `settings.py`

### Database Issues

**MySQL not starting:**
- Check MySQL service is running
- Check MySQL logs for errors
- Verify MySQL installation

**Connection refused:**
- Check MySQL is running
- Verify host/port in `.env`
- Check firewall settings

---

## Running Both Servers

### Option 1: Two Terminal Windows

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
python manage.py runserver
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Option 2: Use a Process Manager

**Windows (PowerShell):**
```powershell
# Terminal 1
cd backend; venv\Scripts\activate; python manage.py runserver

# Terminal 2
cd frontend; npm run dev
```

---

## Next Steps

1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:3000
3. ✅ Database connected and working
4. ✅ Test the application

**Now you can:**
- Register a new user
- Add transactions
- Create budgets
- Set goals
- Explore all features!

---

## Quick Commands Reference

### Backend
```bash
cd backend
venv\Scripts\activate  # Activate venv
python manage.py runserver  # Start server
python manage.py createsuperuser  # Create admin
python manage.py migrate  # Run migrations
```

### Frontend
```bash
cd frontend
npm install  # Install dependencies
npm run dev  # Start dev server
npm run build  # Build for production
npm test  # Run tests
```

---

## Need Help?

If you encounter issues:
1. Check error messages carefully
2. Verify all prerequisites are installed
3. Check database connection
4. Review `.env` and `.env.local` files
5. Check that ports 3000 and 8000 are available

Good luck! 🚀

