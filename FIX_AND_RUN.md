# 🔧 FIX: Site Cannot Be Reached - Complete Solution

## Quick Fix - Run This First

**Windows Users:**
1. Double-click `RUN_PROJECT.bat` in the project root
2. It will start both servers automatically
3. Browser will open automatically

**OR manually:**

## Step-by-Step Fix

### 1. Check What's Running

Run this to see what's working:
```bash
CHECK_STATUS.bat
```

### 2. Start Backend (Terminal 1)

```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

**You MUST see:**
```
Starting development server at http://127.0.0.1:8000/
```

**If you see errors:**
- "Module not found" → Run: `pip install -r requirements.txt`
- "Can't connect to database" → Check `.env` file has correct MySQL password
- "Port 8000 in use" → Stop other apps or use port 8001

### 3. Test Backend is Working

Open browser: http://localhost:8000

**You should see:**
```json
{"status": "ok", "message": "Funder API is running"}
```

**If you see this, backend is working! ✅**

### 4. Start Frontend (Terminal 2 - NEW WINDOW)

```bash
cd frontend
npm run dev
```

**You MUST see:**
```
✓ Ready in 2.5s
○ Local:        http://localhost:3000
```

**If you see errors:**
- "Cannot find module" → Run: `npm install`
- "Port 3000 in use" → Stop other apps or use port 3001

### 5. Open Browser

Go to: **http://localhost:3000**

**You should see the Funder dashboard!**

---

## Common Issues & Fixes

### Issue 1: "This site can't be reached"

**Cause:** Server not running

**Fix:**
1. Check if backend is running: http://localhost:8000
2. Check if frontend is running: http://localhost:3000
3. Both must be running!

### Issue 2: Backend won't start

**Error: "ModuleNotFoundError: No module named 'django'"**

**Fix:**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue 3: Frontend won't start

**Error: "Cannot find module"**

**Fix:**
```bash
cd frontend
npm install
```

### Issue 4: Database connection error

**Error: "Access denied for user"**

**Fix:**
1. Open `backend\.env`
2. Check `DB_PASSWORD=your_actual_mysql_password`
3. Make sure MySQL is running

### Issue 5: Port already in use

**Error: "Port 8000/3000 already in use"**

**Fix Backend:**
```bash
python manage.py runserver 8001
```

**Fix Frontend:**
```bash
npm run dev -- -p 3001
```

Then update `frontend\.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8001/api
```

---

## Verification Checklist

Before opening browser, verify:

- [ ] MySQL is running (check Services)
- [ ] Backend terminal shows: "Starting development server at http://127.0.0.1:8000/"
- [ ] Frontend terminal shows: "○ Local: http://localhost:3000"
- [ ] http://localhost:8000 shows: `{"status": "ok", ...}`
- [ ] http://localhost:3000 shows the Funder dashboard

---

## Quick Test Commands

**Test Backend:**
```bash
curl http://localhost:8000/health
```
Should return: `{"status":"ok","message":"Funder API is running"}`

**Test Frontend:**
Just open: http://localhost:3000

---

## Still Not Working?

1. **Check both terminals are open and running**
2. **Check no firewall blocking ports 3000/8000**
3. **Try different browser** (Chrome, Firefox, Edge)
4. **Clear browser cache** (Ctrl+Shift+Delete)
5. **Check Windows Firewall** isn't blocking

---

## Emergency: Start Everything Fresh

If nothing works, start completely fresh:

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver

# Terminal 2 - Frontend (NEW WINDOW)
cd frontend
npm install
npm run dev
```

Then open: http://localhost:3000

---

**The site WILL work if both servers are running!** 🚀

