@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo Online Examination Portal - Setup
echo ========================================
echo.

echo Checking Python installation...
python --version
echo Python OK
echo.

echo [1/4] Installing dependencies from requirements.txt...
python -m pip install -r requirements.txt
echo Dependencies installed
echo.

echo [2/4] Applying database migrations...
python manage.py makemigrations
python manage.py migrate
echo Database ready
echo.

echo [3/4] Creating sample data...
python sample_data.py
echo Sample data created
echo.

echo [4/4] Collecting static files...
python manage.py collectstatic --noinput
echo Static files collected
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo System is ready to use!
echo.
echo Next: Run this command to start the server
echo        python manage.py runserver
echo.
echo Then open your browser to: http://127.0.0.1:8000
echo Login with: admin / admin123
echo.
pause
