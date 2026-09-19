import sys
import os
import traceback

# Setup error log file
LOG_FILE = os.path.join(os.path.dirname(__file__), "error.log")

def log_error(err_msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(err_msg + "\n")
    print(err_msg)

try:
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon, QPixmap, QAction, QPainter, QColor
    from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
    from pet_widget import PixelDesktopPet
    from sprites import generate_all_sprites
except Exception as e:
    log_error(f"Import Error: {traceback.format_exc()}")

def create_tray_icon():
    try:
        pix = QPixmap(32, 32)
        pix.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pix)
        painter.setBrush(QColor(247, 160, 70))
        painter.setPen(QColor(43, 30, 26))
        painter.drawRect(4, 4, 24, 24)
        painter.setBrush(QColor(255, 246, 229))
        painter.drawRect(8, 12, 16, 12)
        painter.end()
        return QIcon(pix)
    except Exception:
        return QIcon()

def main():
    try:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
        
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        # Assets location
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        if not os.path.exists(assets_dir) or len(os.listdir(assets_dir)) == 0:
            generate_all_sprites()

        # Create Pet Widget
        pet = PixelDesktopPet(assets_dir)
        pet.show()
        pet.raise_()
        pet.activateWindow()

        # System Tray Icon Setup (Safe initialization)
        try:
            if QSystemTrayIcon.isSystemTrayAvailable():
                tray_icon = QSystemTrayIcon(create_tray_icon(), app)
                tray_menu = QMenu()
                tray_menu.setStyleSheet("""
                    QMenu {
                        background-color: #24292E;
                        color: #F0F6FC;
                        border: 1px solid #444C56;
                        font-family: 'Segoe UI', Arial;
                        font-size: 12px;
                        padding: 4px;
                    }
                    QMenu::item:selected {
                        background-color: #0366D6;
                        color: #FFFFFF;
                    }
                """)

                act_show = QAction("🐾 Bring Pet to Front", app)
                act_show.triggered.connect(lambda: (pet.raise_(), pet.activateWindow()))
                tray_menu.addAction(act_show)

                act_pet = QAction("❤️ Pet Companion", app)
                act_pet.triggered.connect(pet.pet_character)
                tray_menu.addAction(act_pet)

                act_feed = QAction("🍱 Feed Treat", app)
                act_feed.triggered.connect(pet.feed_character)
                tray_menu.addAction(act_feed)

                tray_menu.addSeparator()

                act_cat = QAction("🐱 Switch to Cat", app)
                act_cat.triggered.connect(lambda: pet.toggle_pet_type('cat'))
                tray_menu.addAction(act_cat)

                act_panda = QAction("🐼 Switch to Panda", app)
                act_panda.triggered.connect(lambda: pet.toggle_pet_type('panda'))
                tray_menu.addAction(act_panda)

                tray_menu.addSeparator()

                act_quit = QAction("❌ Exit Desktop Pet", app)
                act_quit.triggered.connect(app.quit)
                tray_menu.addAction(act_quit)

                tray_icon.setContextMenu(tray_menu)
                tray_icon.setToolTip("2D Pixel Desktop Pet")
                tray_icon.show()
        except Exception as e_tray:
            log_error(f"Tray error (non-fatal): {e_tray}")

        sys.exit(app.exec())

    except Exception as e:
        log_error(f"Main execution crash: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
