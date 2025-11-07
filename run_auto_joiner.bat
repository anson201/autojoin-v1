@echo off
title Roblox Auto-Joiner
color 0A
echo.
echo ================================================
echo     ROBLOX AUTO-JOINER - LAUNCHER
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if script exists
if not exist "roblox_auto_joiner_v2.py" (
    echo ERROR: roblox_auto_joiner_v2.py not found!
    echo.
    echo Please make sure the script is in the same folder as this batch file.
    echo.
    pause
    exit /b 1
)

echo Script found!
echo.
echo Starting Auto-Joiner...
echo.
echo ================================================
echo.

REM Run the script
python roblox_auto_joiner_v2.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ================================================
    echo     Script exited with an error
    echo ================================================
    pause
)

REM Window will stay open due to the script's input() at the end
