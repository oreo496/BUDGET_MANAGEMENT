# 🔧 FIX: "Unknown database 'funder'" Error

## ❌ Error You're Seeing:
```
OperationalError: (1049, "Unknown database 'funder'")
```

## ✅ Solution: Create the Database

The database doesn't exist yet. You need to create it first!

---

## 🚀 Quick Fix - Automatic

**Double-click:** `CREATE_DATABASE.bat`

It will:
- Ask for your MySQL username and password
- Create the 'funder' database
- Run schema.sql to create all tables
- Verify everything worked

---

## 📝 Manual Fix

### Step 1: Open MySQL

**Option A: Command Line**
```bash
mysql -u root -p
```
(Enter your password when prompted)

**Option B: MySQL Workbench**
- Open MySQL Workbench
- Connect to your MySQL server

### Step 2: Create Database

In MySQL, type:
```sql
CREATE DATABASE funder;
```

Press Enter.

### Step 3: Run Schema

**Option A: From Command Line (outside MySQL)**
```bash
mysql -u root -p funder < schema.sql
```

**Option B: From MySQL Command Line**
```sql
USE funder;
SOURCE C:/Users/omar6/OneDrive/SWE Project/schema.sql;
```
(Adjust the path to match your actual path)

**Option C: Copy-Paste Schema**
1. Open `schema.sql` in Notepad
2. Copy all the content
3. Paste into MySQL Workbench
4. Execute

### Step 4: Verify

Check if tables were created:
```sql
USE funder;
SHOW TABLES;
```

You should see:
- users
- admins
- categories
- bank_accounts
- transactions
- budgets
- goals
- ai_alerts
- system_logs
- admin_actions

---

## ✅ After Creating Database

1. **Start backend again:**
   ```bash
   cd backend
   venv\Scripts\activate
   python manage.py runserver
   ```

2. **Should work now!** ✅

---

## 🎯 Complete Setup Order

1. ✅ **Create Database** ← You are here!
   - Run: `CREATE_DATABASE.bat`
   - Or manually create it

2. ✅ **Setup .env file**
   - Add MySQL password to `backend\.env`

3. ✅ **Start Backend**
   - `python manage.py runserver`

4. ✅ **Start Frontend**
   - `npm run dev`

---

## ❓ Common Issues

### "mysql: command not found"
- MySQL not in PATH
- Use full path: `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`
- Or use MySQL Workbench instead

### "Access denied"
- Wrong password
- Check your MySQL password
- Update it in `backend\.env`

### "Can't connect to MySQL"
- MySQL service not running
- Start it: Services → MySQL80 → Start

---

## 📋 Quick Checklist

- [ ] MySQL is running
- [ ] Database 'funder' exists
- [ ] Tables created (run schema.sql)
- [ ] .env file has correct password
- [ ] Backend can connect

---

**The error means the database doesn't exist. Create it and it will work!** 🎯




