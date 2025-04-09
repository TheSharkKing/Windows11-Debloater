@echo off
:: Check for administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires administrator privileges.
    pause
    exit /b
)

:: Change directory to the script's location
cd /d "%~dp0windows-debloater\src"

:: Run the Python script
python main.py
pause