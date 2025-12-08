# 📝 Where to Write Commands - Step by Step Guide

## 🖥️ Where to Run Commands

You need to use **Command Prompt** (Windows) or **Terminal** (Mac/Linux).

---

## 🪟 Windows: Open Command Prompt

### Method 1: Quick Access
1. Press `Windows Key + R`
2. Type: `cmd`
3. Press `Enter`
4. Command Prompt window opens!

### Method 2: Start Menu
1. Click **Start** button
2. Type: `cmd` or `Command Prompt`
3. Click on **Command Prompt**

### Method 3: File Explorer
1. Open File Explorer
2. Navigate to your project folder: `C:\Users\omar6\OneDrive\SWE Project`
3. Click in the address bar
4. Type: `cmd` and press `Enter`
5. Command Prompt opens in that folder!

---

## 📂 Navigate to Your Project

Once Command Prompt is open, you'll see something like:
```
C:\Users\omar6>
```

**Type this to go to your project:**
```bash
cd "C:\Users\omar6\OneDrive\SWE Project"
```

Press `Enter`. Now you're in the project folder!

You should see:
```
C:\Users\omar6\OneDrive\SWE Project>
```

---

## 🚀 EASIEST WAY: Use the Batch Files!

**You DON'T need to type commands if you use these files:**

### Option 1: Complete Automatic Setup
1. Open File Explorer
2. Go to: `C:\Users\omar6\OneDrive\SWE Project`
3. **Double-click:** `COMPLETE_FIX.bat`
4. Wait for it to finish
5. Done! ✅

### Option 2: Just Start Servers
1. Open File Explorer
2. Go to: `C:\Users\omar6\OneDrive\SWE Project`
3. **Double-click:** `RUN_PROJECT.bat`
4. Servers start automatically!

---

## 📋 If You Need to Type Commands Manually

### Step 1: Open Command Prompt
- Press `Win + R`, type `cmd`, press Enter

### Step 2: Navigate to Project
```bash
cd "C:\Users\omar6\OneDrive\SWE Project"
```

### Step 3: Start Backend (Terminal 1)

**Type these commands one by one:**
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
```

**✅ Keep this window open!**

### Step 4: Start Frontend (NEW Command Prompt Window)

**Open a NEW Command Prompt window:**
- Press `Win + R`, type `cmd`, press Enter (again!)

**Type these commands:**
```bash
cd "C:\Users\omar6\OneDrive\SWE Project\frontend"
npm run dev
```

**You should see:**
```
○ Local:        http://localhost:3000
```

**✅ Keep this window open too!**

### Step 5: Open Browser
- Go to: http://localhost:3000

---

## 🎯 Visual Guide

```
┌─────────────────────────────────────┐
│  Command Prompt Window 1 (Backend) │
├─────────────────────────────────────┤
│ C:\Users\omar6>                     │
│ cd "C:\Users\omar6\OneDrive\SWE... │
│ cd backend                          │
│ venv\Scripts\activate               │
│ python manage.py runserver          │
│ Starting server at 8000...          │
│                                     │
│ ✅ KEEP THIS OPEN                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Command Prompt Window 2 (Frontend)│
├─────────────────────────────────────┤
│ C:\Users\omar6>                     │
│ cd "C:\Users\omar6\OneDrive\SWE... │
│ cd frontend                         │
│ npm run dev                         │
│ Ready at http://localhost:3000     │
│                                     │
│ ✅ KEEP THIS OPEN                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Browser Window                     │
├─────────────────────────────────────┤
│  http://localhost:3000              │
│                                     │
│  [Funder Dashboard]                 │
│                                     │
└─────────────────────────────────────┘
```

---

## 💡 Pro Tips

### Tip 1: Use File Explorer Address Bar
- Open File Explorer
- Go to project folder
- Click address bar
- Type `cmd` and press Enter
- Command Prompt opens in that folder!

### Tip 2: Right-Click in File Explorer
- Navigate to project folder
- Hold `Shift` and **Right-click** in empty space
- Click **"Open PowerShell window here"** or **"Open command window here"**

### Tip 3: Use Batch Files (Easiest!)
- Just double-click `COMPLETE_FIX.bat`
- No typing needed!

---

## ❓ Common Questions

### Q: "Where do I type the commands?"
**A:** In Command Prompt (cmd) window

### Q: "How do I open Command Prompt?"
**A:** Press `Win + R`, type `cmd`, press Enter

### Q: "Do I need to type everything?"
**A:** No! Just double-click `COMPLETE_FIX.bat` instead

### Q: "What if I make a typo?"
**A:** Just type the command again. You can use arrow keys to edit.

### Q: "How do I stop the servers?"
**A:** Press `Ctrl + C` in each Command Prompt window

---

## 🎬 Quick Start (3 Steps)

1. **Double-click:** `COMPLETE_FIX.bat` in File Explorer
2. **Wait** 10-15 seconds
3. **Open browser:** http://localhost:3000

**That's it!** 🎉

---

## 📍 Exact File Locations

Your project is here:
```
C:\Users\omar6\OneDrive\SWE Project\
```

Files you can double-click:
- `COMPLETE_FIX.bat` ← Start everything
- `RUN_PROJECT.bat` ← Just start servers
- `CHECK_STATUS.bat` ← Check what's running
- `TEST_CONNECTION.bat` ← Test connections

---

**Remember: You can double-click the .bat files instead of typing commands!** 🚀




