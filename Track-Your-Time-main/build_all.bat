@echo off
echo ========================================
echo  Time Tracker Pro - Build Script
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo Step 1/5: Installing dependencies...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2/5: Cleaning old builds...
echo.
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist gui_tracker.spec del gui_tracker.spec

echo.
echo Step 3/5: Building executable...
echo This may take 2-5 minutes...
echo.
python installer\build_exe.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo Step 4/5: Testing executable...
echo.
if not exist dist\TimeTrackerPro.exe (
    echo ERROR: Executable not found!
    pause
    exit /b 1
)

for %%I in (dist\TimeTrackerPro.exe) do set size=%%~zI
set /a size_mb=%size% / 1048576
echo SUCCESS: TimeTrackerPro.exe created (%size_mb% MB)

echo.
echo Step 5/5: Creating installer...
echo.

:: Check if Inno Setup is installed
set INNO_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_PATH% (
    echo WARNING: Inno Setup not found!
    echo Download from: https://jrsoftware.org/isdl.php
    echo.
    echo You can still use: dist\TimeTrackerPro.exe
    echo.
    goto :skip_installer
)

%INNO_PATH% installer\setup.iss
if errorlevel 1 (
    echo ERROR: Failed to create installer
    pause
    exit /b 1
)

echo.
echo ========================================
echo  BUILD COMPLETE!
echo ========================================
echo.
echo Created files:
echo   1. Executable: dist\TimeTrackerPro.exe
echo   2. Installer:  dist\installer\TimeTrackerProSetup.exe
echo.
echo Test the executable before distributing!
echo.
goto :end

:skip_installer
echo ========================================
echo  BUILD COMPLETE (No Installer)
echo ========================================
echo.
echo Created file:
echo   - Executable: dist\TimeTrackerPro.exe
echo.
echo To create installer:
echo   1. Install Inno Setup from https://jrsoftware.org/isdl.php
echo   2. Run this script again
echo.

:end
pause
