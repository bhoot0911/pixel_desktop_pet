@echo off
title Push 2D Pixel Desktop Pet to GitHub (bhoot0911/pixel-desktop-pet)
echo ========================================================
echo   Pushing Cosmos & Burrito Desktop Pet to GitHub
echo   Repository: https://github.com/bhoot0911/pixel-desktop-pet
echo ========================================================
cd /d "%~dp0"

echo.
echo Checking for Git...
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Git is not yet installed on this PC.
    echo.
    echo Easy Option 1: Open VS Code, open this folder, press Ctrl+Shift+G and click "Publish to GitHub".
    echo Easy Option 2: Install Git from https://git-scm.com/download/win and re-run this script!
    echo.
    pause
    exit /b
)

echo Initializing local Git repository...
git init
git add .
git commit -m "Initial commit: Cosmos (Cat) & Burrito (Panda) 2D Pixel Desktop Pet with Productivity Suite"

git branch -M main
git remote remove origin >nul 2>nul
git remote add origin https://github.com/bhoot0911/pixel-desktop-pet.git
echo.
echo Pushing code to https://github.com/bhoot0911/pixel-desktop-pet ...
git push -u origin main

echo.
echo ========================================================
echo   SUCCESS! Repository published to GitHub:
echo   https://github.com/bhoot0911/pixel-desktop-pet
echo ========================================================
pause
