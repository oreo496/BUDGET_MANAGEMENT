# 🚨 INSTANT FIX - Get Site Working NOW

## ⚡ FASTEST WAY (30 seconds)

**Double-click:** `COMPLETE_FIX.bat`

This will:
- ✅ Check all prerequisites
- ✅ Install all dependencies
- ✅ Start both servers
- ✅ Open browser automatically

**Wait 10-15 seconds after it finishes, then refresh browser!**

---

## 🔧 If COMPLETE_FIX.bat doesn't work:

### Option 1: Manual Quick Start

**Open 2 Command Prompt windows:**

**Window 1 (Backend):**
```bash
cd "C:\Users\omar6\OneDrive\SWE Project\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

**Window 2 (Frontend):**
```bash
cd "C:\Users\omar6\OneDrive\SWE Project\frontend"
npm install
npm run dev
```

**Then open:** http://localhost:3000

---

## ✅ Verify It's Working

**Test Backend:**
- Open: http://localhost:8000
- Should see: `{"status": "ok", "message": "Funder API is running"}`

**Test Frontend:**
- Open: http://localhost:3000
- Should see: Funder dashboard with sidebar

---

## 🐛 Common Fixes

### "Site can't be reached"
**Cause:** Servers not running

**Fix:**
1. Check Terminal 1 shows: `Starting development server at http://127.0.0.1:8000/`
2. Check Terminal 2 shows: `○ Local: http://localhost:3000`
3. Both MUST be running!

### "Module not found" (Backend)
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### "Cannot find module" (Frontend)
```bash
cd frontend
npm install
```

### "Port already in use"
**Backend:**
```bash
python manage.py runserver 8001
```

**Frontend:**
```bash
npm run dev -- -p 3001
```

Then update `frontend\.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8001/api
```

### Database Error
1. Make sure MySQL is running
2. Check `backend\.env` has: `DB_PASSWORD=your_actual_password`
3. Test: `mysql -u root -p`

---

## 📋 Quick Checklist

Before opening browser:
- [ ] MySQL running (check Services)
- [ ] Backend terminal shows server running
- [ ] Frontend terminal shows server running
- [ ] http://localhost:8000 works (shows JSON)
- [ ] http://localhost:3000 works (shows dashboard)

---

## 🎯 Still Not Working?

1. **Run:** `TEST_CONNECTION.bat` to see what's wrong
2. **Check:** Both terminals for error messages
3. **Try:** Different browser (Chrome, Firefox, Edge)
4. **Clear:** Browser cache (Ctrl+Shift+Delete)

---

**The site WILL work if both servers are running!** 🚀

