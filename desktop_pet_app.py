import os
import sys
import random
import datetime
import tkinter as tk
import tkinter.font as tkfont
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

class DesktopPetTk:
    # Scale presets (Base sprite = 48x48)
    SCALES = {
        'Small (48px)': 48,
        'Normal (96px)': 96,
        'Big (160px)': 160,
        'Giant (300px)': 300  # Default 300px fixed size
    }

    # Custom Pet Names
    PET_NAMES = {
        'cat': 'Cosmos',
        'panda': 'Burrito'
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cosmos & Burrito - 2D Pixel Desktop Pet")
        
        # Window setup for frameless, stays-on-top, transparent desktop pet
        self.root.overrideredirect(True)
        self.root.wm_attributes('-topmost', True)
        
        # Windows transparent color key (makes #000001 completely invisible!)
        self.bg_color = '#000001'
        self.root.config(bg=self.bg_color)
        try:
            self.root.wm_attributes('-transparentcolor', self.bg_color)
        except Exception:
            pass

        # Dimensions & Settings
        self.pet_type = 'cat'  # 'cat' = Cosmos, 'panda' = Burrito
        self.sprite_size = 300  # Fixed 300px target size
        self.win_w = int(self.sprite_size * 1.3)
        self.win_h = int(self.sprite_size * 1.5)  # 150px generous headroom for speech bubbles!
        
        # Position at center of screen
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        init_x = (screen_w - self.win_w) // 2
        init_y = (screen_h - self.win_h) // 2
        self.root.geometry(f"{self.win_w}x{self.win_h}+{init_x}+{init_y}")

        # Canvas for drawing pet & speech bubble
        self.canvas = tk.Canvas(
            self.root, 
            width=self.win_w, 
            height=self.win_h, 
            bg=self.bg_color, 
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)

        # Asset Image Cache
        self.raw_images = {}
        self.tk_images = {}
        self.load_assets()

        # State Machine Variables
        self.state = 'IDLE'
        self.direction = 1  # 1 = Right, -1 = Left
        self.frame_index = 0
        self.ticks = 0
        self.state_timer = 150
        
        # Initial greeting with custom name
        self.bubble_text = "hi, I'm Cosmos! 🐱"
        self.bubble_timer = 160
        
        # Dragging variables
        self.drag_x = 0
        self.drag_y = 0
        
        # --- PRODUCTIVITY TIMERS & REMINDERS ---
        self.active_timers = []  # [{ 'name': ..., 'remaining_sec': ..., 'msg': ... }]
        self.last_sec_tick = datetime.datetime.now()

        # Event Bindings
        self.canvas.bind('<Button-1>', self.on_left_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<Double-Button-1>', self.on_double_click)
        self.canvas.bind('<Button-3>', self.show_context_menu)

        # Keyboard & Scroll reactions
        self.root.bind_all('<Key>', self.on_typing_key)
        self.root.bind_all('<MouseWheel>', self.on_mouse_scroll)
        self.root.bind_all('<Button-4>', self.on_mouse_scroll)
        self.root.bind_all('<Button-5>', self.on_mouse_scroll)

        # Right Click Context Menu
        self.menu = tk.Menu(self.root, tearoff=0, bg='#24292E', fg='#FFFFFF', activebackground='#0366D6', activeforeground='#FFFFFF')
        
        # Actions Submenu
        self.menu.add_command(label="❤️ Pet Cosmos / Burrito", command=self.pet_character)
        self.menu.add_command(label="🍱 Feed Treat", command=self.feed_character)
        self.menu.add_command(label="⌨️ Type / Work", command=self.type_reaction)
        self.menu.add_command(label="🌀 Scroll / Spin", command=self.scroll_reaction)
        self.menu.add_command(label="💤 Force Sleep", command=lambda: self.set_state('SLEEP', 300))
        self.menu.add_separator()

        # --- PRODUCTIVITY SUBMENU ---
        prod_sub = tk.Menu(self.menu, tearoff=0, bg='#24292E', fg='#FFFFFF', activebackground='#0366D6')
        prod_sub.add_command(label="⏱️ 25m Pomodoro Focus Timer", command=lambda: self.start_timer("Pomodoro", 25*60, "🎉 Focus complete! Take a 5m break! ☕"))
        prod_sub.add_command(label="☕ 5m Short Break Timer", command=lambda: self.start_timer("Short Break", 5*60, "💪 Break over! Back to work! 🚀"))
        prod_sub.add_command(label="💧 30m Drink Water Reminder", command=lambda: self.start_timer("Drink Water", 30*60, "💧 Drink water time! Stay hydrated! 🥤"))
        prod_sub.add_command(label="🧘 45m Stretch & Posture Check", command=lambda: self.start_timer("Posture Check", 45*60, "🧘 Stretch time! Sit up straight! ✨"))
        prod_sub.add_command(label="👁️ 20m Eye Rest (20-20-20 Rule)", command=lambda: self.start_timer("Eye Rest", 20*60, "👁️ Look at something 20ft away! 👀"))
        prod_sub.add_separator()
        prod_sub.add_command(label="🔔 Quick 1m Test Timer", command=lambda: self.start_timer("Quick 1m", 1*60, "🔔 1 Minute Timer Done! 🎉"))
        prod_sub.add_command(label="📝 Custom Reminder...", command=self.set_custom_reminder)
        prod_sub.add_command(label="📋 Active Timers Status", command=self.show_timers_status)
        self.menu.add_cascade(label="⏱️ Productivity & Timers", menu=prod_sub)

        self.menu.add_separator()
        self.menu.add_command(label="🐱 Switch to Cosmos (Cat)", command=lambda: self.switch_pet('cat'))
        self.menu.add_command(label="🐼 Switch to Burrito (Panda)", command=lambda: self.switch_pet('panda'))
        self.menu.add_separator()
        
        # Scale menu
        scale_sub = tk.Menu(self.menu, tearoff=0, bg='#24292E', fg='#FFFFFF', activebackground='#0366D6')
        for name, sz in self.SCALES.items():
            scale_sub.add_command(label=name, command=lambda s=sz: self.change_size(s))
        self.menu.add_cascade(label="🔍 Resize Pet", menu=scale_sub)
        self.menu.add_separator()
        self.menu.add_command(label="❌ Exit Desktop Pet", command=self.root.destroy)

        # Animation Loop Timer (60 FPS ~ 16ms)
        self.animate()

    def load_assets(self):
        """Loads and caches all sprite PNG images."""
        if not os.path.exists(ASSETS_DIR):
            return
        for file in os.listdir(ASSETS_DIR):
            if file.endswith('.png'):
                path = os.path.join(ASSETS_DIR, file)
                try:
                    img = Image.open(path).convert("RGBA")
                    self.raw_images[file] = img
                except Exception as e:
                    print(f"Error loading {file}: {e}")

    def get_tk_image(self, frame_filename):
        """Returns scaled ImageTk.PhotoImage using nearest-neighbor crisp scaling."""
        key = (frame_filename, self.sprite_size)
        if key not in self.tk_images and frame_filename in self.raw_images:
            raw = self.raw_images[frame_filename]
            # CRISP NEAREST NEIGHBOR POINT SAMPLING
            scaled = raw.resize((self.sprite_size, self.sprite_size), Image.NEAREST)
            self.tk_images[key] = ImageTk.PhotoImage(scaled)
        return self.tk_images.get(key)

    def set_state(self, new_state, duration=150):
        self.state = new_state
        self.state_timer = duration
        self.frame_index = 0

    def pick_random_state(self):
        hour = datetime.datetime.now().hour
        is_night = (hour >= 20 or hour < 6)
        
        if is_night:
            options = ['SLEEP', 'SIT', 'IDLE', 'WALK']
            weights = [50, 25, 15, 10]
        else:
            options = ['IDLE', 'WALK', 'SIT', 'SLEEP', 'HAPPY', 'ROLL' if self.pet_type == 'panda' else 'EXCITED']
            weights = [30, 35, 15, 5, 10, 10]

        chosen = random.choices(options, weights=weights, k=1)[0]
        if chosen in ('WALK', 'ROLL'):
            self.direction = random.choice([1, -1])
        self.set_state(chosen, random.randint(120, 280))

    def get_current_frame_filename(self):
        prefix = f"{self.pet_type}_"
        suffix = "_left.png" if self.direction == -1 else ".png"
        anim_step = (self.ticks // 8)

        if self.state == 'IDLE':
            cycle = anim_step % 6
            frame_id = 'blink' if cycle == 3 else ('idle_2' if cycle in (1, 2) else 'idle_1')
        elif self.state == 'WALK':
            frame_id = f"walk_{1 + (anim_step % 4)}"
        elif self.state == 'SIT':
            frame_id = 'sit'
        elif self.state == 'SLEEP':
            frame_id = f"sleep_{1 + (anim_step % 2)}"
        elif self.state == 'HAPPY':
            frame_id = f"happy_{1 + (anim_step % 2)}"
        elif self.state == 'TYPE':
            frame_id = f"type_{1 + (anim_step % 2)}"
        elif self.state == 'SCROLL':
            frame_id = f"scroll_{1 + (anim_step % 2)}"
        elif self.state == 'EAT':
            frame_id = f"eat_{1 + (anim_step % 2)}" if self.pet_type == 'panda' else f"happy_{1 + (anim_step % 2)}"
        elif self.state == 'ROLL':
            frame_id = f"roll_{1 + (anim_step % 4)}" if self.pet_type == 'panda' else f"walk_{1 + (anim_step % 4)}"
        elif self.state == 'EXCITED':
            frame_id = 'excited' if self.pet_type == 'cat' else 'happy_1'
        else:
            frame_id = 'idle_1'

        filename = prefix + frame_id + suffix
        if filename not in self.raw_images:
            filename = prefix + 'idle_1.png'
        return filename

    def show_speech(self, text, duration=180):
        self.bubble_text = text
        self.bubble_timer = duration

    # --- PRODUCTIVITY METHODS ---
    def start_timer(self, name, duration_sec, alert_msg):
        self.active_timers.append({
            'name': name,
            'remaining_sec': duration_sec,
            'msg': alert_msg
        })
        mins = duration_sec // 60
        self.set_state('EXCITED', 120)
        pet_name = self.PET_NAMES[self.pet_type]
        self.show_speech(f"⏱️ {pet_name}: {name} ({mins}m)", duration=140)

    def set_custom_reminder(self):
        try:
            pet_name = self.PET_NAMES[self.pet_type]
            rem_text = simpledialog.askstring("Custom Reminder", f"What should {pet_name} remind you to do?", parent=self.root)
            if rem_text:
                mins_str = simpledialog.askstring("Reminder Delay", "In how many minutes?", parent=self.root)
                if mins_str and mins_str.isdigit():
                    mins = int(mins_str)
                    self.start_timer(rem_text[:12], mins * 60, f"🔔 {pet_name}: {rem_text}")
        except Exception:
            pass

    def show_timers_status(self):
        if not self.active_timers:
            pet_name = self.PET_NAMES[self.pet_type]
            self.show_speech(f"{pet_name}: no active timers! ⏱️")
        else:
            t = self.active_timers[0]
            m, s = divmod(t['remaining_sec'], 60)
            self.show_speech(f"⏱️ {t['name']}: {m}m {s}s left")

    def tick_productivity_timers(self):
        now = datetime.datetime.now()
        if (now - self.last_sec_tick).total_seconds() >= 1.0:
            self.last_sec_tick = now
            finished = []
            for t in self.active_timers:
                t['remaining_sec'] -= 1
                if t['remaining_sec'] <= 0:
                    finished.append(t)
            
            for f in finished:
                self.active_timers.remove(f)
                # ALERT TRIGGER!
                self.set_state('EXCITED', 240)
                self.show_speech(f['msg'], duration=300)

    def animate(self):
        self.ticks += 1
        self.state_timer -= 1
        if self.bubble_timer > 0:
            self.bubble_timer -= 1

        # Check productivity timers every second
        self.tick_productivity_timers()

        # Walk / Roll movement across desktop
        if self.state in ('WALK', 'ROLL'):
            speed = 2 if self.state == 'ROLL' else 1
            curr_x = self.root.winfo_x()
            curr_y = self.root.winfo_y()
            new_x = curr_x + (self.direction * speed)
            
            screen_w = self.root.winfo_screenwidth()
            if new_x <= 10:
                new_x = 10
                self.direction = 1
            elif new_x >= screen_w - self.win_w - 10:
                new_x = screen_w - self.win_w - 10
                self.direction = -1
            self.root.geometry(f"+{new_x}+{curr_y}")

        if self.state_timer <= 0:
            self.pick_random_state()

        # Render Canvas Elements
        self.canvas.delete('all')

        # Get Current Frame
        fname = self.get_current_frame_filename()
        tk_img = self.get_tk_image(fname)
        
        # Dynamic canvas size & sprite position
        ch = max(self.win_h, self.canvas.winfo_height())
        cw = max(self.win_w, self.canvas.winfo_width())

        img_x = (cw - self.sprite_size) // 2
        img_y = ch - self.sprite_size - 10
        
        if tk_img:
            self.canvas.create_image(img_x, img_y, anchor='nw', image=tk_img)

        # Draw Speech Bubble (Guaranteed NO Clipping with tkfont & bounds)
        if self.bubble_timer > 0 and self.bubble_text:
            bx = cw // 2
            
            # Font measurement
            font_spec = ('Segoe UI', 12, 'bold')
            font_obj = tkfont.Font(family='Segoe UI', size=12, weight='bold')
            text_w = font_obj.measure(self.bubble_text)
            
            padding_h = 24  # Horizontal padding
            tw = text_w + (padding_h * 2)
            th = 38
            
            # GUARANTEED SAFETY BOUNDS: top is ALWAYS >= 14px from top edge of canvas!
            top = max(14, img_y - 20 - th)
            bottom = top + th
            left = bx - (tw // 2)
            right = bx + (tw // 2)
            
            # Outer Rounded Pixel Bubble
            self.canvas.create_rectangle(
                left, top, right, bottom, 
                fill='#FFFDF5', outline='#1C1E24', width=2
            )
            # Pointer Tail
            self.canvas.create_polygon(
                bx - 6, bottom, bx + 6, bottom, bx, bottom + 8, 
                fill='#FFFDF5', outline='#1C1E24', width=2
            )
            # Centered Text
            self.canvas.create_text(
                bx, top + (th // 2), text=self.bubble_text, 
                font=font_spec, fill='#1C1E24'
            )

        self.root.after(16, self.animate)

    # --- EVENT HANDLERS ---
    def on_typing_key(self, event):
        """Action when user types on keyboard: Typing paws reaction!"""
        if self.state != 'TYPE':
            self.set_state('TYPE', 60)
            pet_name = self.PET_NAMES[self.pet_type]
            msg = random.choice([f"{pet_name} is typing! ⌨️", "working hard! 💻", "type fast! ⚡", "focus mode! 🎯"])
            self.show_speech(msg, duration=80)

    def on_mouse_scroll(self, event):
        """Action when user scrolls mouse wheel: Scroll spin reaction!"""
        if self.state != 'SCROLL':
            self.set_state('SCROLL', 60)
            pet_name = self.PET_NAMES[self.pet_type]
            msg = random.choice([f"{pet_name}: wheeee! 🌀", "scrolling! 📜", "spin spin! ✨", "keep scrolling! 🚀"])
            self.show_speech(msg, duration=80)

    def on_left_click(self, event):
        """Tap / Left Click dedicated to PETTING the companion."""
        self.drag_x = event.x
        self.drag_y = event.y
        self.pet_character()

    def on_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_x)
        y = self.root.winfo_y() + (event.y - self.drag_y)
        self.root.geometry(f"+{x}+{y}")

    def on_double_click(self, event):
        self.play_character()

    def pet_character(self):
        """Tap reaction: Petting the character."""
        self.set_state('HAPPY', 180)
        msg = "Cosmos purrrr... ❤️" if self.pet_type == 'cat' else "Burrito is so cozy! ❤️"
        self.show_speech(msg)

    def type_reaction(self):
        self.set_state('TYPE', 120)
        pet_name = self.PET_NAMES[self.pet_type]
        self.show_speech(f"{pet_name} is typing! ⌨️")

    def scroll_reaction(self):
        self.set_state('SCROLL', 120)
        pet_name = self.PET_NAMES[self.pet_type]
        self.show_speech(f"{pet_name}: wheeee! 🌀")

    def feed_character(self):
        self.set_state('EAT', 180)
        msg = "Cosmos: yum yum! 🐟" if self.pet_type == 'cat' else "Burrito: munch munch 🎋"
        self.show_speech(msg)

    def play_character(self):
        act = 'ROLL' if self.pet_type == 'panda' else 'EXCITED'
        self.set_state(act, 180)
        pet_name = self.PET_NAMES[self.pet_type]
        self.show_speech(f"play with {pet_name}? ✨")

    def switch_pet(self, ptype):
        self.pet_type = ptype
        pet_name = self.PET_NAMES[ptype]
        icon = '🐱' if ptype == 'cat' else '🐼'
        self.show_speech(f"hi, I'm {pet_name}! {icon}")
        self.pick_random_state()

    def change_size(self, size_px):
        self.sprite_size = size_px
        self.win_w = int(size_px * 1.3)
        self.win_h = int(size_px * 1.5)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.geometry(f"{self.win_w}x{self.win_h}+{x}+{y}")
        self.canvas.config(width=self.win_w, height=self.win_h)

    def show_context_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DesktopPetTk()
    app.run()
