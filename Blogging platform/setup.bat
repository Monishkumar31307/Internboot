@echo off
echo ===================================
echo Blogging Platform - Setup Script
echo ===================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies!
    exit /b 1
)

echo Step 2: Running migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error running migrations!
    exit /b 1
)

echo Step 3: Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo Error collecting static files!
    exit /b 1
)

echo Step 4: Creating superuser...
echo Please create a superuser account:
python manage.py createsuperuser

echo Step 5: Creating sample data...
python sample_data.py

echo.
echo ===================================
echo Setup Complete!
echo ===================================
echo.
echo Next steps:
echo 1. Run: run_server.bat
echo 2. Visit: http://localhost:8000
echo 3. Admin: http://localhost:8000/admin
echo.
pause
