@echo off
title Disable Auto-Start on PC Turn-On
echo Disabling Auto-Start...
del /f /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Cosmos_and_Burrito_Startup.vbs" 2>nul
echo.
echo Auto-start disabled. Cosmos & Burrito will no longer open automatically on boot.
echo.
pause
