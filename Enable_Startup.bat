@echo off
title Enable Auto-Start on PC Turn-On
echo Enabling Auto-Start for Cosmos & Burrito...
copy /y "%~dp0Cosmos_and_Burrito_Startup.vbs" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\" >nul
echo.
echo SUCCESS! Cosmos & Burrito will now automatically open on your screen every time your PC turns on.
echo.
pause
