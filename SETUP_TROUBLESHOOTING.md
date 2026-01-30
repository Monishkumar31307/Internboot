# Setup & Troubleshooting Guide

## 🎯 Complete Step-by-Step Instructions

### STEP 1: Open Terminal
1. Press `Windows + R`
2. Type `powershell` and press Enter
3. You now have a terminal open

### STEP 2: Navigate to Project Folder
Copy and paste this command:
```powershell
cd "C:\Users\monis\Downloads\internboot\Online Examination Portal"
```

**Verify correct location:**
```powershell
pwd
```
Should show: `C:\Users\monis\Downloads\internboot\Online Examination Portal`

### STEP 3: Check Python
```powershell
python --version
```

**Expected:** `Python 3.10.x` or higher

**If this fails:**
- Python is not installed or not in PATH
- Download from: https://www.python.org/downloads/
- During installation, CHECK "Add Python to PATH"
- Restart terminal after installing

### STEP 4: Fix pip (CRITICAL!)
```powershell
python -m pip install --upgrade pip setuptools wheel
```

**This solves most Windows installation issues.** Wait for completion.

### STEP 5: Run Setup (Everything Automatic)
```powershell
setup.bat
```

**This script will:**
1. Verify Python version
2. Install all dependencies (Django, Pillow, etc.)
3. Create database
4. Apply migrations
5. Load sample data
6. Collect static files

**Expected final message:** `Setup Complete!`

**If setup fails:**
- See troubleshooting section below
- Run `setup.bat` again

### STEP 6: Start Server
```powershell
python manage.py runserver
```

**Expected output:**
```
Django version 4.2.9
...
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### STEP 7: Open Website
Open your browser and go to:
```
http://127.0.0.1:8000
```

You should see the login page! ✓

### STEP 8: Login
**Admin Access:**
- Username: `admin`
- Password: `admin123`

**Student Access:**
- Username: `student1` (or student2, student3)
- Password: `student123`

---

## 🔧 Troubleshooting Problems

### Problem 1: "pip install fails" or "Python packages won't install"

**Error symptoms:**
- Messages about "building wheel"
- Errors mentioning Pillow, setuptools, etc.
- Exit code 1

**Solution:**
```powershell
# Step 1: Upgrade pip tools FIRST
python -m pip install --upgrade pip setuptools wheel

# Step 2: Install dependencies manually
python -m pip install Django==4.2.9
python -m pip install Pillow==10.1.0
python -m pip install django-crispy-forms==2.1
python -m pip install crispy-bootstrap4==2.0

# Step 3: Run setup again
setup.bat
```

---

### Problem 2: "Python command not found"

**Error message:**
```
'python' is not recognized as an internal or external command
```

**Cause:** Python not installed or not in PATH

**Solution:**
1. Download Python 3.10 or 3.11 from https://www.python.org/downloads/
2. During installation, **CHECK** "Add Python to PATH" ✓
3. Click "Install Now"
4. Restart your terminal
5. Try again: `python --version`

---

### Problem 3: "Django not found" or "No module named django"

**Error message:**
```
ModuleNotFoundError: No module named 'django'
```

**Cause:** Django not installed

**Solution:**
```powershell
python -m pip install -r requirements.txt
# OR
python -m pip install Django==4.2.9
```

---

### Problem 4: Database errors or "database is locked"

**Error messages:**
- "database is locked"
- "no such table"
- "migration conflicts"

**Solution:**
```powershell
# Step 1: Delete old database
del db.sqlite3

# Step 2: Run setup again (creates fresh database)
setup.bat

# Step 3: Start server
python manage.py runserver
```

---

### Problem 5: Port 8000 already in use

**Error message:**
```
OSError: [Errno 48] Address already in use
```

**Cause:** Another program using port 8000

**Solution:**
```powershell
# Option 1: Use different port
python manage.py runserver 8001

# Then open: http://127.0.0.1:8001

# Option 2: Close other programs using port 8000
# Or restart your computer
```

---

### Problem 6: Static files not loading (images/CSS broken)

**Symptoms:** Website looks broken, no styling

**Solution:**
```powershell
python manage.py collectstatic --noinput
python manage.py runserver
```

---

### Problem 7: "setup.bat doesn't exist" or "can't find setup.bat"

**Solution:**
```powershell
# Make sure you're in the correct folder
cd "C:\Users\monis\Downloads\internboot\Online Examination Portal"

# Verify setup.bat exists
dir setup.bat  # Should show the file

# Run it
setup.bat
```

---

### Problem 8: "file not found" or "no such file or directory"

**Error message:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'db.sqlite3'
```

**Solution:** Database doesn't exist, create it:
```powershell
python manage.py migrate
python sample_data.py
```

---

## ✅ Verification Checklist

After following all steps, verify everything works:

```powershell
# 1. Check Python
python --version
# Expected: Python 3.10 or higher

# 2. Check Django installed
python -m django --version
# Expected: 4.2.9

# 3. Check database exists
dir db.sqlite3
# Expected: file shown

# 4. Check server starts
python manage.py runserver
# Expected: "Starting development server at http://127.0.0.1:8000/"
# Press CTRL+C to stop
```

---

## 🆘 If Nothing Works

Follow this nuclear option:

```powershell
# 1. Delete database
del db.sqlite3

# 2. Delete Python cache
rmdir __pycache__ /s /q
rmdir src\__pycache__ /s /q

# 3. Uninstall and reinstall Django
python -m pip uninstall django -y
python -m pip uninstall pillow -y
python -m pip uninstall django-crispy-forms -y

# 4. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 5. Install everything fresh
python -m pip install -r requirements.txt

# 6. Run setup
setup.bat

# 7. Start server
python manage.py runserver
```

---

## 📋 Final Quick Reference

| Task | Command |
|------|---------|
| Navigate to folder | `cd "C:\Users\monis\Downloads\internboot\Online Examination Portal"` |
| Check Python | `python --version` |
| Upgrade pip | `python -m pip install --upgrade pip setuptools wheel` |
| Install dependencies | `python -m pip install -r requirements.txt` |
| Setup database | `setup.bat` |
| Start server | `python manage.py runserver` |
| Open website | http://127.0.0.1:8000 |
| Admin login | admin / admin123 |
| Student login | student1 / student123 |
| Stop server | CTRL+C |
| Reset everything | `del db.sqlite3` then `setup.bat` |

---

## 🎉 Success Indicators

You'll know it's working when:

✓ Browser shows login page at http://127.0.0.1:8000  
✓ Login credentials work (admin/admin123)  
✓ Dashboard loads after login  
✓ Can see exam list  
✓ Can take sample exams  

---

**Still stuck? Check README.md or QUICK_START.md for more detailed information.**
