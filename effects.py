import random
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush

class Particle:
    def __init__(self, ptype, x, y):
        self.ptype = ptype  # 'heart', 'sparkle', 'zzz', 'exclamation', 'music', 'star'
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.8, -0.3)  # Float upward
        self.life = 1.0  # 1.0 down to 0.0
        self.decay = random.uniform(0.015, 0.03)
        self.size = random.choice([3, 4, 5])
        self.text = {
            'heart': '❤️',
            'sparkle': '✨',
            'zzz': 'Z',
            'exclamation': '!',
            'music': '♪',
            'star': '★'
        }.get(ptype, '✨')
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        return self.life > 0

class PixelParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn(self, ptype, x, y, count=3):
        for _ in range(count):
            offset_x = random.uniform(-10, 10)
            offset_y = random.uniform(-5, 5)
            self.particles.append(Particle(ptype, x + offset_x, y + offset_y))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, painter: QPainter, font: QFont):
        for p in self.particles:
            painter.save()
            alpha = int(max(0, min(255, p.life * 255)))
            
            if p.ptype == 'zzz':
                painter.setFont(QFont("Courier New", 9, QFont.Weight.Bold))
                painter.setPen(QColor(100, 150, 255, alpha))
                painter.drawText(int(p.x), int(p.y), "Z")
            elif p.ptype == 'heart':
                painter.setFont(QFont("Segoe UI Emoji", 8))
                painter.setPen(QColor(255, 80, 120, alpha))
                painter.drawText(int(p.x), int(p.y), "♥")
            elif p.ptype == 'exclamation':
                painter.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
                painter.setPen(QColor(255, 200, 50, alpha))
                painter.drawText(int(p.x), int(p.y), "!")
            elif p.ptype == 'music':
                painter.setFont(QFont("Segoe UI Symbol", 9))
                painter.setPen(QColor(180, 100, 255, alpha))
                painter.drawText(int(p.x), int(p.y), "♪")
            elif p.ptype == 'star':
                painter.setFont(QFont("Segoe UI Symbol", 8))
                painter.setPen(QColor(255, 220, 80, alpha))
                painter.drawText(int(p.x), int(p.y), "★")
            else: # sparkle
                painter.setFont(QFont("Segoe UI Symbol", 8))
                painter.setPen(QColor(255, 230, 100, alpha))
                painter.drawText(int(p.x), int(p.y), "✦")
                
            painter.restore()


class PixelSpeechBubble:
    CAT_MESSAGES = [
        "pspsps...",
        "feed me",
        "hello 👀",
        "play?",
        "zzz...",
        "hehe",
        "why are we working",
        "purrrr... ❤️",
        "miau!",
        "so cozy!"
    ]
    
    PANDA_MESSAGES = [
        "munch munch 🎋",
        "hello 👀",
        "roll time!",
        "play?",
        "zzz...",
        "hehe",
        "bamboo break!",
        "why are we working",
        "nap time...",
        "so cozy!"
    ]

    def __init__(self):
        self.text = ""
        self.visible = False
        self.timer = 0
        self.opacity = 1.0

    def show_message(self, pet_type='cat', custom_msg=None):
        if custom_msg:
            self.text = custom_msg
        else:
            options = self.CAT_MESSAGES if pet_type == 'cat' else self.PANDA_MESSAGES
            self.text = random.choice(options)
        self.visible = True
        self.timer = 150  # ~2.5 seconds at 60fps
        self.opacity = 1.0

    def update(self):
        if self.visible:
            self.timer -= 1
            if self.timer < 30:
                self.opacity = max(0.0, self.timer / 30.0)
            if self.timer <= 0:
                self.visible = False

    def draw(self, painter: QPainter, pet_x: int, pet_y: int, pet_width: int):
        if not self.visible or not self.text:
            return

        painter.save()
        
        # Crisp pixel font setup scaled dynamically to pet size
        font_size = 15 if pet_width >= 240 else (12 if pet_width >= 120 else 9)
        font = QFont("Courier New", font_size, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Calculate bubble size
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(self.text)
        text_height = metrics.height()
        
        padding_x = 8
        padding_y = 4
        bubble_width = text_width + (padding_x * 2)
        bubble_height = text_height + (padding_y * 2)
        
        # Position bubble above pet
        bx = int(pet_x + (pet_width / 2) - (bubble_width / 2))
        by = int(pet_y - bubble_height - 8)
        
        alpha = int(self.opacity * 255)
        
        # Outer 1px Dark Border
        border_pen = QPen(QColor(27, 30, 36, alpha))
        border_pen.setWidth(2)
        painter.setPen(border_pen)
        
        # Cream Pixel Fill
        bg_brush = QBrush(QColor(255, 253, 245, alpha))
        painter.setBrush(bg_brush)
        
        # Draw Speech Box (Rounded pixel rect)
        painter.drawRoundedRect(bx, by, bubble_width, bubble_height, 4, 4)
        
        # Tail pointing down to pet
        tail_x = int(pet_x + (pet_width / 2))
        tail_y = by + bubble_height
        
        tail_poly = [
            QPointF(tail_x - 4, tail_y),
            QPointF(tail_x + 4, tail_y),
            QPointF(tail_x, tail_y + 6)
        ]
        painter.drawPolygon(tail_poly)
        
        # Draw Text inside bubble
        painter.setPen(QColor(27, 30, 36, alpha))
        painter.drawText(bx + padding_x, by + padding_y + metrics.ascent(), self.text)
        
        painter.restore()
