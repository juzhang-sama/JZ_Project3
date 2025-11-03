@echo off
setlocal enabledelayedexpansion

echo.
echo ================================
echo  Flutter Frontend Application
echo ================================
echo.

REM Set Flutter path
set PATH=D:\flutter\flutter\bin;%PATH%

REM Change to frontend directory
cd /d d:\JZ_Project3\frontend

echo Step 1: Getting dependencies...
echo.
call flutter pub get
if errorlevel 1 (
    echo ERROR: Failed to get dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Checking for devices...
echo.
call flutter devices

echo.
echo Step 3: Running application...
echo.
echo Tips:
echo - Press 'r' to hot reload
echo - Press 'R' to restart
echo - Press 'q' to quit
echo.

call flutter run

pause

