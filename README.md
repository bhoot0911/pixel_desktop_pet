# 🐱 Cosmos & 🐼 Burrito - 2D Pixel Art Desktop Pet

An adorable, polished **2D Pixel-Art Desktop Companion** featuring **Cosmos the Cat** and **Burrito the Panda** for Windows!

![2D Pixel Desktop Pet](https://img.shields.org/badge/Style-2D%20Pixel%20Art-orange?style=for-the-badge)
![Python](https://img.shields.org/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![License](https://img.shields.org/badge/License-MIT-green?style=for-the-badge)

---

## 🌟 Features

### 🎨 Polished 2D Pixel-Art Style
- **Cosmos 🐱 (Cat)**: Ginger coat, cream chest/paws, pink inner ears, and expressive anime eyes with dual white sparkle highlights (`✨`).
- **Burrito 🐼 (Panda)**: Fluffy black & white body, dark eye patches, pink cheeks, and 360-degree rolling animation across the desktop!
- **Defined Limbs & Paws**: Clear front paws with pink toe-bean pads for Cosmos, and distinct black arms/legs with paw pads for Burrito.

### ⏱️ Integrated Productivity Suite & Timers
Right-click on your companion to access built-in focus tools & reminders:
- **⏱️ Pomodoro Focus Timer (25m)**: "🎉 Focus complete! Take a 5m break! ☕"
- **☕ Short Break Timer (5m)**: "💪 Break over! Back to work! 🚀"
- **💧 Drink Water Reminder (30m)**: "💧 Drink water time! Stay hydrated! 🥤"
- **🧘 Stretch & Posture Check (45m)**: "🧘 Stretch time! Sit up straight! ✨"
- **👁️ Eye Rest (20m - 20-20-20 Rule)**: "👁️ Look at something 20ft away! 👀"
- **📝 Custom Reminders**: Enter custom reminder text and delay in minutes!

### 🎮 Add-On Reactions & Controls
- **⌨️ Keyboard Typing Reaction**: Typing on your keyboard triggers a rapid typing paws animation ("Cosmos is typing! ⌨️").
- **🌀 Mouse Scroll Reaction**: Scrolling the mouse wheel triggers a spin/wave reaction ("Burrito: wheeee! 🌀").
- **❤️ Tap / Single Click**: Dedicated to petting your companion (❤️ hearts + purring).
- **Double Click**: Play/jump or panda roll (`✨` sparkles).
- **Drag & Drop**: Left-click drag to position your companion anywhere on screen.

### 🌙 Day & Night Cycle
- **Daytime (6 AM - 8 PM)**: Active, energetic walking, rolling, and playing.
- **Nighttime (8 PM - 6 AM)**: Sleepy behavior, frequent napping, and floating star particles.

### 🖼️ Nearest-Neighbor Crisp 300px Scaling
- **300×300 pixels** target size rendered using point-sampling nearest-neighbor scaling (`Image.NEAREST`) so pixel edges remain crisp and unmissable.
- **Transparent Desktop Floating Window**: Native Windows color-key transparency (`-transparentcolor`) sits directly on top of your desktop wallpaper and apps.

---

## 🚀 Quick Start

### 1. Requirements
- Windows 10 / 11
- Python 3.x
- Dependencies: `Pillow`

### 2. Installation & Running
```bash
# Clone the repository
git clone https://github.com/your-username/pixel-desktop-pet.git
cd pixel-desktop-pet

# Install required dependencies
pip install Pillow

# Launch Desktop Pet
python desktop_pet_app.py
```

### 3. Auto-Start on PC Turn-On
- Run `Enable_Startup.bat` to automatically launch Cosmos & Burrito whenever your PC turns on!
- Run `Disable_Startup.bat` to disable auto-start anytime.

---

## 📂 Project Structure

```
pixel_desktop_pet/
├── assets/                          # 94 generated pixel art PNG frames
├── sprites.py                       # Procedural 2D pixel-art generator engine
├── desktop_pet_app.py               # Native Tkinter transparent desktop pet app
├── main.py                          # PyQt6 desktop launcher
├── index.html                       # HTML5 standalone web canvas app fallback
├── Enable_Startup.bat               # 1-Click script to enable PC boot auto-start
├── Disable_Startup.bat              # 1-Click script to disable PC boot auto-start
├── Cosmos_and_Burrito_Startup.vbs  # Windows Startup folder VBS script
└── README.md                        # Project documentation
```

---

## 📜 License
This project is licensed under the **MIT License**.
