@echo off
title Hair Rain Predictor - Useless Project Launcher
echo ===============================================================
echo 💇🌧️ HAIR RAIN PREDICTOR - COLLEGE USELESS PROJECT
echo ===============================================================
echo.

cd /d "%~dp0"

IF EXIST ".venv\Scripts\python.exe" (
    echo [OK] Virtual environment found. Launching application...
    echo.
    ".venv\Scripts\python.exe" -m streamlit run app.py
) ELSE (
    echo [INFO] Virtual environment not found. Using system Python...
    echo.
    python -m streamlit run app.py
)

pause
