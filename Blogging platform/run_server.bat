@echo off
echo ===================================
echo Blogging Platform - Development Server
echo ===================================
echo.
echo Starting Django development server...
echo.
echo Open your browser and go to:
echo   http://localhost:8000
echo.
echo Admin panel:
echo   http://localhost:8000/admin
echo.
echo Press CTRL+C to stop the server
echo.

python manage.py runserver
