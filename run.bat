@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
)
call ".venv\Scripts\activate.bat"
echo Installing Flask...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Flask installation failed. Check your internet connection and Python installation.
    pause
    exit /b 1
)
echo.
echo Starting MoodLens AI...
echo Open http://127.0.0.1:5000 in your browser.
python app.py
pause
