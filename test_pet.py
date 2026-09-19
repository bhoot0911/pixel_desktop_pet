import sys
import os
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPixmap, QColor, QFont
from PyQt6.QtWidgets import QApplication, QWidget

class SimplePetTest(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pixel Pet Test Window")
        
        # Asset path
        asset_path = os.path.join(os.path.dirname(__file__), "assets", "cat_idle_1.png")
        print("Loading test sprite from:", asset_path)
        print("File exists:", os.path.exists(asset_path))
        
        self.pixmap = QPixmap(asset_path)
        print("Pixmap loaded. Is Null?", self.pixmap.isNull(), "Width:", self.pixmap.width(), "Height:", self.pixmap.height())

        # Set window size
        self.sprite_size = 300
        self.resize(360, 360)
        
        # Window flags
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # Position in center of screen
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - 360) // 2, (screen.height() - 360) // 2)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)
        
        # Draw semi-transparent background bubble to guarantee visibility on any wallpaper
        painter.setBrush(QColor(20, 24, 33, 180))  # Cozy dark semi-transparent glass
        painter.setPen(QColor(255, 160, 70, 220))
        painter.drawRoundedRect(10, 10, self.width() - 20, self.height() - 20, 16, 16)
        
        # Draw Pet Sprite
        if not self.pixmap.isNull():
            px_x = (self.width() - self.sprite_size) // 2
            px_y = (self.height() - self.sprite_size) // 2
            painter.drawPixmap(px_x, px_y, self.sprite_size, self.sprite_size, self.pixmap)
            
        # Draw label
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        painter.drawText(30, 45, "🐱 Pixel Pet Test Window")
        painter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SimplePetTest()
    w.show()
    w.raise_()
    w.activateWindow()
    sys.exit(app.exec())
