@echo off
title Push 2D Pixel Desktop Pet to GitHub (bhoot0911/pixel-desktop-pet)
echo ========================================================
echo   Configuring Git User & Pushing to GitHub
echo ========================================================
cd /d "%~dp0"

echo Setting Git user name and email...
git config user.name "bhoot0911"
git config user.email "bhoot0911@users.noreply.github.com"

echo Initializing local Git repository...
git init
git config user.name "bhoot0911"
git config user.email "bhoot0911@users.noreply.github.com"

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
