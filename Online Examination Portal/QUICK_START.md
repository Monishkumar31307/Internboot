# Quick Start Guide - Online Examination Portal

## ⚡ Get Started - Step by Step

### STEP 1: Open Terminal in Project Folder
Open PowerShell or Command Prompt and navigate to the project:
```powershell
cd "C:\Users\monis\Downloads\internboot\Online Examination Portal"
```

**Verify you're in the correct folder:**
```powershell
pwd   # Should show: ...Online Examination Portal
dir   # Should show: manage.py, setup.bat, requirements.txt, etc.
```

---

### STEP 2: Check Python Installation
Verify Python 3.10+ is installed:
```powershell
python --version
```

**Expected output:** `Python 3.10.x` or higher  
**Not installed?** Download from https://www.python.org/

---

### STEP 3: Upgrade pip Tools (IMPORTANT!)
Run this BEFORE setup.bat to fix install issues:
```powershell
python -m pip install --upgrade pip setuptools wheel
```

This fixes the Pillow installation issue on Windows.

---

### STEP 4: Run Setup (All-in-One)
Now run the improved setup script:
```powershell
setup.bat
```

**This does automatically:**
- ✓ Installs all dependencies (Django, Pillow, crispy-forms)
- ✓ Creates database
- ✓ Applies migrations
- ✓ Creates sample data
- ✓ Collects static files

**Wait for:** "Setup Complete!" message

---

### STEP 5: Start the Server
After setup finishes, start the server:

**Option A - Using batch file:**
```powershell
run_server.bat
```

**Option B - Manual:**
```powershell
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

### STEP 6: Open in Browser
Click or copy this link to your browser:
**http://127.0.0.1:8000**

---

## 🔑 Login Credentials

### Admin Dashboard
```
Username: admin
Password: admin123
```
**Access:** http://127.0.0.1:8000/login/

### Student Portal
```
Username: student1  (or student2, student3)
Password: student123
```

---

## ✅ What You Get After Setup

- ✓ Working Django application
- ✓ SQLite database with sample data
- ✓ 3 Sample exams (29 questions total)
- ✓ 1 Admin account
- ✓ 3 Student accounts
- ✓ Ready-to-use examination system

---

## 🎯 What to Do First

### As a Student:
1. Login to http://127.0.0.1:8000
2. Click "View Exams"
3. Select an exam
4. Click "Start Exam"
5. Answer questions
6. Submit and see results

### As an Admin:
1. Login to http://127.0.0.1:8000
2. Click "Admin Dashboard"
3. View student attempts
4. Check rankings
5. Create new exams (optional)

---

## 🆘 Troubleshooting

### Problem: pip install fails during setup
**Solution:**
```powershell
python -m pip install --upgrade pip setuptools wheel
setup.bat
```

### Problem: "python command not found"
**Solution:** 
- Python not in PATH
- Install Python 3.10+: https://www.python.org/
- Make sure "Add to PATH" is checked during installation

### Problem: Port 8000 already in use
**Solution:**
```powershell
python manage.py runserver 8001
```
Then open: http://127.0.0.1:8001

### Problem: Database errors after first run
**Solution:**
```powershell
# Delete old database
del db.sqlite3

# Run setup again
setup.bat
```

### Problem: "No module named 'django'"
**Solution:**
```powershell
python -m pip install -r requirements.txt
```

---

## 📞 Getting Help

1. **Check Python version:** `python --version` (must be 3.8+)
2. **Check Django installed:** `python -m django --version`
3. **See logs:** Run `setup.bat` and read all messages
4. **Reset everything:** Delete db.sqlite3 and run setup.bat again
5. **Read full docs:** Open `README.md` for comprehensive guide

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management tool |
| `setup.bat` | Run ALL setup automatically |
| `run_server.bat` | Start the server |
| `requirements.txt` | Python dependencies |
| `sample_data.py` | Generate test data |
| `db.sqlite3` | SQLite database (created by setup) |
| `README.md` | Full documentation |

---

## 🚀 You're Done!

**The website is now running at: http://127.0.0.1:8000**

**Remember:**
- Login with `admin/admin123` for admin access
- Login with `student1/student123` for student access
- Press `CTRL+C` in terminal to stop the server
- Run `python manage.py runserver` to restart
