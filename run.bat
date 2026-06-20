@echo off
echo ======================================
echo   StreamVault - Starting Server
echo ======================================
if not exist "downloads" mkdir downloads
if not exist "temp" mkdir temp
pip install -r requirements.txt
echo.
echo Server starting...
echo Open: http://localhost:5000
echo.
python main.py
pause
