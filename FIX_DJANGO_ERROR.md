# 🔧 Fix: "No module named 'django'"

## ❌ Error:
```
ModuleNotFoundError: No module named 'django'
ImportError: Couldn't import Django. Are you sure it's installed?
```

## ✅ Solution: Install Dependencies

The error means Django (and other packages) are not installed in your virtual environment.

---

## 🚀 Quick Fix - Automatic

**Double-click:** `INSTALL_DEPENDENCIES.bat`

This will:
- ✅ Create venv if needed
- ✅ Activate virtual environment
- ✅ Install all dependencies from `requirements.txt`
- ✅ Takes 2-3 minutes

---

## 📝 Manual Fix

### Step 1: Navigate to Backend

```bash
cd "C:\Users\omar6\OneDrive\SWE Project\backend"
```

### Step 2: Activate Virtual Environment

```bash
venv\Scripts\activate
```

**You should see `(venv)` at the start of your command line!**

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Wait 2-3 minutes** for installation to complete.

You should see:
```
Successfully installed Django-4.2.7 djangorestframework-3.14.0 ...
```

### Step 4: Verify Installation

```bash
python -c "import django; print(django.get_version())"
```

Should show: `4.2.7` (or similar)

### Step 5: Start Backend

```bash
python manage.py runserver
```

---

## ✅ What Gets Installed

From `requirements.txt`:
- Django 4.2.7
- Django REST Framework
- MySQL client
- bcrypt (password hashing)
- PyJWT (tokens)
- cryptography
- pyotp (MFA)
- qrcode (MFA QR codes)
- Pillow (image processing)
- pytest (testing)

**Total: ~15 packages**

---

## 🔍 Verify It Worked

After installation, you should be able to run:

```bash
python manage.py runserver
```

And see:
```
Starting development server at http://127.0.0.1:8000/
```

---

## ❓ Common Issues

### "pip: command not found"
- Make sure virtual environment is activated
- Try: `python -m pip install -r requirements.txt`

### "Permission denied"
- Run Command Prompt as Administrator
- Or check if files are locked

### "Failed to build mysqlclient"
- Install MySQL development libraries
- Or use: `pip install mysqlclient --no-cache-dir`

---

## 🎯 Quick Steps

1. **Double-click:** `INSTALL_DEPENDENCIES.bat`
2. **Wait 2-3 minutes**
3. **Then start backend:** `python manage.py runserver`

**That's it!** 🚀

