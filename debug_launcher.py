import sys
import os
import traceback

log_file = os.path.join(os.path.dirname(__file__), "debug.txt")

with open(log_file, "w", encoding="utf-8") as f:
    f.write("Starting debug launcher...\n")
    try:
        f.write("Importing PyQt6...\n")
        from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, QRectF
        from PyQt6.QtGui import QPainter, QPixmap, QCursor, QAction, QFont, QColor, QGuiApplication
        from PyQt6.QtWidgets import QApplication, QWidget, QMenu, QSystemTrayIcon
        f.write("PyQt6 imported successfully.\n")

        f.write("Initializing QApplication...\n")
        app = QApplication(sys.argv)
        f.write("QApplication initialized.\n")

        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        f.write(f"Assets dir: {assets_dir}, exists: {os.path.exists(assets_dir)}\n")

        from pet_widget import PixelDesktopPet
        f.write("Creating PixelDesktopPet widget...\n")
        pet = PixelDesktopPet(assets_dir)
        f.write("PixelDesktopPet widget created.\n")
        
        pet.show()
        pet.raise_()
        pet.activateWindow()
        f.write("Pet widget shown successfully.\n")

    except Exception as e:
        f.write("ERROR TRACEBACK:\n")
        f.write(traceback.format_exc() + "\n")
