import os
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QCursor, QAction, QFont, QColor, QGuiApplication
from PyQt6.QtWidgets import QWidget, QMenu

from pet_state import PetState
from effects import PixelParticleSystem, PixelSpeechBubble

class PixelDesktopPet(QWidget):
    # Fixed 300x300 pixel target size
    FIXED_SPRITE_SIZE = 300
    
    SCALES = {
        'Fixed 300px': 300,
        'Small (48px)': 48,
        'Normal (96px)': 96,
        'Big (160px)': 160,
        'Giant (300px)': 300
    }

    def __init__(self, assets_dir):
        super().__init__()
        self.assets_dir = assets_dir
        
        # Core Systems
        self.state = PetState(pet_type='cat')
        self.particles = PixelParticleSystem()
        self.speech_bubble = PixelSpeechBubble()
        
        # Pixmap cache for crisp pixel rendering
        self.pixmap_cache = {}
        self.load_assets()
        
        # Fixed 300px Scale & Window Properties
        self.scale_name = 'Giant (300px)'
        self.sprite_size = self.FIXED_SPRITE_SIZE
        
        # Window setup for frameless, stays-on-top, translucent desktop pet
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # Dragging variables
        self.dragging = False
        self.drag_offset = QPoint()
        
        # Position initial pet at center of primary screen so it is immediately visible
        screen = QGuiApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        win_dim = int(self.sprite_size * 1.35)
        init_x = (self.screen_width // 2) - (win_dim // 2)
        init_y = (self.screen_height // 2) - (win_dim // 2)
        self.setGeometry(init_x, init_y, win_dim, win_dim)
        
        # Animation loop (60 FPS timer)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)  # ~60 FPS update
        
        # Show cute greeting
        self.speech_bubble.show_message(self.state.pet_type, "hello 👀")

    def load_assets(self):
        """Loads all generated sprite PNGs into memory pixmaps."""
        self.pixmap_cache.clear()
        if not os.path.exists(self.assets_dir):
            print(f"Error: assets directory {self.assets_dir} does not exist.")
            return
            
        for file in os.listdir(self.assets_dir):
            if file.endswith('.png'):
                path = os.path.join(self.assets_dir, file)
                pm = QPixmap(path)
                self.pixmap_cache[file] = pm

    def game_loop(self):
        # Update particles & speech bubble
        self.particles.update()
        self.speech_bubble.update()
        
        # Global cursor position for pet look-at logic
        cursor_pos = QCursor.pos()
        
        # Autonomous pet movement & state tick
        curr_x = self.x()
        curr_y = self.y()
        
        new_x = self.state.update(
            window_x=curr_x,
            window_y=curr_y,
            screen_width=self.screen_width,
            window_width=self.sprite_size,
            cursor_global_pos=cursor_pos,
            particle_sys=self.particles,
            speech_bubble=self.speech_bubble
        )
        
        # Move window horizontal position if walking/rolling
        if new_x != curr_x and not self.dragging:
            self.move(new_x, curr_y)
            
        # Trigger redraw
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # --- CRITICAL FOR Crisp Pixel Art ---
        # Disable smooth scaling / anti-aliasing so nearest-neighbor integer pixel edges are preserved!
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        
        # Get current sprite frame
        frame_name = self.state.get_current_frame_name()
        pm = self.pixmap_cache.get(frame_name)
        
        # Sprite canvas offset within window (centered at bottom of window)
        sprite_w = self.sprite_size
        sprite_h = self.sprite_size
        
        # Calculate padding to allow speech bubbles & particles above pet
        padding_top = self.height() - sprite_h - 10
        padding_left = (self.width() - sprite_w) // 2
        
        pet_rect = QRectF(padding_left, padding_top, sprite_w, sprite_h)
        
        # Draw cozy dark pixel glass backdrop card behind pet for 100% clear visibility on any wallpaper
        backdrop = QRectF(padding_left - 12, padding_top - 12, sprite_w + 24, sprite_h + 24)
        painter.setBrush(QColor(24, 28, 38, 175))  # Cozy dark pixel card
        painter.setPen(QPen(QColor(247, 160, 70, 220), 2))  # Warm orange border
        painter.drawRoundedRect(backdrop, 16, 16)
        
        if pm and not pm.isNull():
            painter.drawPixmap(pet_rect.toRect(), pm)
        else:
            # Fallback placeholder if missing
            painter.setBrush(QColor(255, 160, 50))
            painter.drawRect(pet_rect)
            
        # Draw Speech Bubble above pet
        self.speech_bubble.draw(painter, int(padding_left), int(padding_top), sprite_w)
        
        # Draw Particles
        font = QFont("Courier New", 9)
        self.particles.draw(painter, font)
        
        painter.end()

    # --- Mouse Interaction & Dragging ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.dragging:
                self.dragging = False
                event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Double click -> Play action / Excited reaction
            action = 'ROLL' if (self.state.pet_type == 'panda' and self.state.current_state != 'ROLL') else 'EXCITED'
            self.state.set_state(action, duration_ticks=150)
            self.particles.spawn('sparkle', self.width() // 2, self.height() // 2, count=5)
            self.speech_bubble.show_message(self.state.pet_type, "play? ✨")

    def pet_character(self):
        """Action when user pets the character."""
        self.state.set_state('HAPPY', duration_ticks=180)
        self.particles.spawn('heart', self.width() // 2, self.height() // 2 - 10, count=4)
        msg = "purrrr... ❤️" if self.state.pet_type == 'cat' else "so cozy! ❤️"
        self.speech_bubble.show_message(self.state.pet_type, msg)

    def feed_character(self):
        """Action when user feeds the pet."""
        self.state.set_state('EAT', duration_ticks=180)
        self.particles.spawn('sparkle', self.width() // 2, self.height() // 2, count=3)
        msg = "munch munch 🎋" if self.state.pet_type == 'panda' else "yum yum! 🐟"
        self.speech_bubble.show_message(self.state.pet_type, msg)

    def toggle_pet_type(self, pet_type):
        self.state.pet_type = pet_type
        self.state.set_random_state()
        self.speech_bubble.show_message(self.state.pet_type, f"hello, I'm a {pet_type}!")

    def set_scale(self, scale_name):
        if scale_name in self.SCALES:
            self.scale_name = scale_name
            self.sprite_size = self.SCALES[scale_name]
            # Resize window bounding box appropriately
            win_dim = int(self.sprite_size * 1.35)
            self.resize(win_dim, win_dim)
            self.update()

    def set_day_night(self, mode):
        self.state.day_night_mode = mode
        self.state.set_random_state()

    def show_context_menu(self, global_pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #24292E;
                color: #F0F6FC;
                border: 1px solid #444C56;
                font-family: 'Segoe UI', Arial;
                font-size: 12px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 20px 6px 12px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #0366D6;
                color: #FFFFFF;
            }
        """)

        # Pet Actions Submenu
        act_pet = QAction("❤️ Pet Companion", self)
        act_pet.triggered.connect(self.pet_character)
        menu.addAction(act_pet)

        act_feed = QAction("🍱 Feed Treat", self)
        act_feed.triggered.connect(self.feed_character)
        menu.addAction(act_feed)

        act_play = QAction("🎾 Play / Dance", self)
        act_play.triggered.connect(lambda: self.mouseDoubleClickEvent(type('Event', (), {'button': lambda: Qt.MouseButton.LeftButton})()))
        menu.addAction(act_play)

        act_sleep = QAction("💤 Force Sleep", self)
        act_sleep.triggered.connect(lambda: self.state.set_state('SLEEP', 300))
        menu.addAction(act_sleep)

        menu.addSeparator()

        # Pet Character Selection Submenu
        char_menu = menu.addMenu("🐱 Switch Character")
        act_cat = QAction("Cat 🐱", self, checkable=True)
        act_cat.setChecked(self.state.pet_type == 'cat')
        act_cat.triggered.connect(lambda: self.toggle_pet_type('cat'))
        char_menu.addAction(act_cat)

        act_panda = QAction("Panda 🐼", self, checkable=True)
        act_panda.setChecked(self.state.pet_type == 'panda')
        act_panda.triggered.connect(lambda: self.toggle_pet_type('panda'))
        char_menu.addAction(act_panda)

        # Scale Selection Submenu
        scale_menu = menu.addMenu("🔍 Pixel Scale Size")
        for s_name in ['Tiny', 'Small', 'Normal', 'Big', 'Huge', 'Giant']:
            act_s = QAction(f"{s_name} ({self.SCALES[s_name]}px)", self, checkable=True)
            act_s.setChecked(self.scale_name == s_name)
            act_s.triggered.connect(lambda checked, s=s_name: self.set_scale(s))
            scale_menu.addAction(act_s)

        # Day/Night Submenu
        dn_menu = menu.addMenu("🌙 Day / Night Mode")
        for mode in ['auto', 'day', 'night']:
            label = f"Auto (System Time)" if mode == 'auto' else (f"Force Day ☀️" if mode == 'day' else f"Force Night 🌙")
            act_dn = QAction(label, self, checkable=True)
            act_dn.setChecked(self.state.day_night_mode == mode)
            act_dn.triggered.connect(lambda checked, m=mode: self.set_day_night(m))
            dn_menu.addAction(act_dn)

        menu.addSeparator()

        act_quit = QAction("❌ Exit Desktop Pet", self)
        act_quit.triggered.connect(QGuiApplication.quit)
        menu.addAction(act_quit)

        menu.exec(global_pos)
