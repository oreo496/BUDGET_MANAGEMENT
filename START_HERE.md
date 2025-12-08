# 🚀 START HERE - Clear Steps to Run Funder

Follow these steps **in order**. Don't skip any step!

---

## ✅ STEP 1: Check Prerequisites (2 minutes)

Make sure you have these installed:

1. **Python 3.8+**
   - Open Command Prompt (Windows) or Terminal (Mac/Linux)
   - Type: `python --version`
   - Should show: `Python 3.x.x`
   - If not installed: https://www.python.org/downloads/

2. **Node.js 18+**
   - Type: `node --version`
   - Should show: `v18.x.x` or higher
   - If not installed: https://nodejs.org/

3. **MySQL 8.0+**
   - Type: `mysql --version`
   - Should show MySQL version
   - If not installed: https://dev.mysql.com/downloads/mysql/

**✅ If all three show versions, proceed to Step 2.**

---

## ✅ STEP 2: Start MySQL (1 minute)

**Windows:**
1. Press `Win + R`
2. Type: `services.msc` and press Enter
3. Find "MySQL80" (or "MySQL")
4. Right-click → Start
5. Close the window

**Mac/Linux:**
```bash
sudo systemctl start mysql
```

**✅ MySQL is now running. Proceed to Step 3.**

---

## ✅ STEP 3: Create Database (2 minutes)

1. Open Command Prompt/Terminal
2. Type:
   ```bash
   mysql -u root -p
   ```
3. Enter your MySQL password (press Enter if no password)
4. Copy and paste these commands one by one:
   ```sql
   CREATE DATABASE IF NOT EXISTS funder;
   USE funder;
   EXIT;
   ```
5. Now run the schema:
   ```bash
   mysql -u root -p funder < schema.sql
   ```
   (Enter password when prompted)

**✅ Database created! Proceed to Step 4.**

---

## ✅ STEP 4: Setup Backend (5 minutes)

1. **Open Command Prompt/Terminal**

2. **Navigate to backend folder:**
   ```bash
   cd "C:\Users\omar6\OneDrive\SWE Project\backend"
   ```
   (Or navigate to wherever your project is)

3. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```
   Wait for it to finish.

4. **Activate virtual environment:**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   You should see `(venv)` at the start of your command line.

5. **Install all dependencies (including Django):**
   ```bash
   pip install -r requirements.txt
   ```
   This will take 2-3 minutes. Wait for it to finish.

6. **Create .env file:**
   
   **Windows:**
   ```bash
   copy .env.example .env
   ```
   
   **Mac/Linux:**
   ```bash
   cp .env.example .env
   ```

7. **Edit .env file:**
   - Open `backend\.env` in Notepad or any text editor
   - Find this line: `DB_PASSWORD=`
   - Add your MySQL password: `DB_PASSWORD=your_mysql_password`
   - Save the file

8. **Generate encryption key:**
   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
   Copy the output (long string of characters)

9. **Add encryption key to .env:**
   - Open `backend\.env` again
   - Find: `ENCRYPTION_KEY=`
   - Paste the key you copied: `ENCRYPTION_KEY=paste_key_here`
   - Save the file

10. **Run migrations:**
    ```bash
    python manage.py migrate --fake-initial
    ```

**✅ Backend setup complete! Proceed to Step 5.**

---

## ✅ STEP 5: Start Backend Server (1 minute)

**Make sure you're still in the backend folder and virtual environment is activated.**

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **You should see:**
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.
   ```

3. **✅ Backend is running!**
   - **DON'T CLOSE THIS WINDOW**
   - Keep it running
   - Open a **NEW** Command Prompt/Terminal window for frontend

**✅ Backend running at http://localhost:8000**

---

## ✅ STEP 6: Setup Frontend (3 minutes)

1. **Open a NEW Command Prompt/Terminal window**
   (Keep the backend window running!)

2. **Navigate to frontend folder:**
   ```bash
   cd "C:\Users\omar6\OneDrive\SWE Project\frontend"
   ```

3. **Install dependencies:**
   ```bash
   npm install
   ```
   This will take 2-3 minutes. Wait for it to finish.

4. **Create .env.local file:**
   
   **Windows:**
   ```bash
   copy .env.example .env.local
   ```
   
   **Mac/Linux:**
   ```bash
   cp .env.example .env.local
   ```

5. **Check .env.local file:**
   - Open `frontend\.env.local`
   - Should already have: `NEXT_PUBLIC_API_URL=http://localhost:8000/api`
   - If not, add it
   - Save the file

**✅ Frontend setup complete! Proceed to Step 7.**

---

## ✅ STEP 7: Start Frontend Server (1 minute)

**Make sure you're in the frontend folder.**

1. **Start the server:**
   ```bash
   npm run dev
   ```

2. **You should see:**
   ```
   ✓ Ready in 2.5s
   ○ Local:        http://localhost:3000
   ```

3. **✅ Frontend is running!**

**✅ Frontend running at http://localhost:3000**

---

## ✅ STEP 8: Open the Application (30 seconds)

1. **Open your web browser** (Chrome, Firefox, Edge, etc.)

2. **Go to:** http://localhost:3000

3. **You should see:**
   - Funder dashboard
   - Sidebar with navigation
   - Cards and charts

**🎉 SUCCESS! Your application is running!**

---

## 📋 Summary - What Should Be Running

You should have **2 terminal windows open**:

1. **Terminal 1 (Backend):**
   - Shows: `Starting development server at http://127.0.0.1:8000/`
   - **Keep this running!**

2. **Terminal 2 (Frontend):**
   - Shows: `○ Local: http://localhost:3000`
   - **Keep this running!**

3. **Browser:**
   - Open: http://localhost:3000
   - Should show the Funder application

---

## 🛑 How to Stop the Servers

When you're done:

1. **Stop Backend:**
   - Go to Terminal 1
   - Press `Ctrl + C`
   - Type `y` and press Enter

2. **Stop Frontend:**
   - Go to Terminal 2
   - Press `Ctrl + C`

---

## 🔄 How to Start Again Later

**Next time you want to run the project:**

1. **Start MySQL** (Step 2)

2. **Start Backend:**
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   # or: source venv/bin/activate  # Mac/Linux
   python manage.py runserver
   ```

3. **Start Frontend (in new terminal):**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Open browser:** http://localhost:3000

---

## ❌ Troubleshooting

### "python: command not found"
- Use `python3` instead of `python`
- Or install Python: https://www.python.org/downloads/

### "mysql: command not found"
- MySQL not in PATH, or not installed
- Install MySQL: https://dev.mysql.com/downloads/mysql/

### "npm: command not found"
- Node.js not installed
- Install: https://nodejs.org/

### "Port 8000 already in use"
- Something else is using port 8000
- Stop other applications or use: `python manage.py runserver 8001`

### "Port 3000 already in use"
- Something else is using port 3000
- Stop other applications or use: `npm run dev -- -p 3001`

### "Can't connect to database"
- Check MySQL is running (Step 2)
- Check password in `backend\.env` file
- Test: `mysql -u root -p`

### "Module not found"
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt` again

### Backend shows errors
- Check `backend\.env` file has correct database password
- Make sure MySQL is running
- Verify database exists: `mysql -u root -p` then `SHOW DATABASES;`

---

## ✅ Checklist

Before starting, make sure:
- [ ] Python installed (`python --version`)
- [ ] Node.js installed (`node --version`)
- [ ] MySQL installed and running (`mysql --version`)
- [ ] Database created (`funder` database exists)
- [ ] Schema.sql executed (tables created)
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] Backend .env file configured
- [ ] Frontend dependencies installed
- [ ] Frontend .env.local file configured
- [ ] Backend server running (Terminal 1)
- [ ] Frontend server running (Terminal 2)
- [ ] Browser open at http://localhost:3000

---

## 🎯 Quick Command Reference

**Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm run dev
```

**Stop servers:**
- Press `Ctrl + C` in each terminal

---

**That's it! Follow these steps and your project will be running! 🚀**

