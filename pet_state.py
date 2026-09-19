import random
import datetime
from PyQt6.QtCore import QPoint

class PetState:
    STATES = ['IDLE', 'WALK', 'SIT', 'SLEEP', 'HAPPY', 'ANGRY', 'CURIOUS', 'EXCITED', 'EAT', 'ROLL', 'PLAY']

    def __init__(self, pet_type='cat'):
        self.pet_type = pet_type  # 'cat' or 'panda'
        self.current_state = 'IDLE'
        self.direction = 1  # 1 = Facing Right, -1 = Facing Left
        self.state_timer = 0
        self.frame_index = 0
        self.frame_ticks = 0
        self.speed = 1.2  # Deliberately slow, cute movement speed
        
        # Day / Night settings ('auto', 'day', 'night')
        self.day_night_mode = 'auto'
        
        # Cursor tracking
        self.cursor_pos = QPoint(0, 0)
        self.looking_at_cursor = False
        
        self.set_random_state()

    def is_night(self):
        if self.day_night_mode == 'day':
            return False
        elif self.day_night_mode == 'night':
            return True
        else: # 'auto'
            hour = datetime.datetime.now().hour
            return hour >= 20 or hour < 6

    def set_state(self, new_state, duration_ticks=120):
        self.current_state = new_state
        self.state_timer = duration_ticks
        self.frame_index = 0
        self.frame_ticks = 0

    def set_random_state(self):
        night = self.is_night()
        
        if night:
            # Sleepy nighttime weights
            weights = {
                'SLEEP': 50,
                'SIT': 25,
                'IDLE': 15,
                'WALK': 10
            }
        else:
            # Energetic daytime weights
            weights = {
                'IDLE': 25,
                'WALK': 35,
                'SIT': 15,
                'SLEEP': 5,
                'CURIOUS': 10,
                'EXCITED': 5,
                'ROLL': 10 if self.pet_type == 'panda' else 0,
                'PLAY': 5
            }
            
        states = list(weights.keys())
        probs = list(weights.values())
        chosen_state = random.choices(states, weights=probs, k=1)[0]
        
        # Determine random walk direction if walking or rolling
        if chosen_state in ('WALK', 'ROLL'):
            self.direction = random.choice([1, -1])

        # Random duration between 2 to 6 seconds
        duration = random.randint(100, 300)
        self.set_state(chosen_state, duration)

    def update(self, window_x, window_y, screen_width, window_width, cursor_global_pos, particle_sys, speech_bubble):
        self.state_timer -= 1
        self.frame_ticks += 1
        
        # Cursor proximity check
        dx = cursor_global_pos.x() - (window_x + window_width // 2)
        dy = cursor_global_pos.y() - (window_y + 24)
        dist_sq = dx*dx + dy*dy
        
        # If cursor is very close, occasionally look at it
        if dist_sq < 140*140 and self.current_state in ('IDLE', 'SIT') and random.random() < 0.01:
            self.looking_at_cursor = True
            if dx > 0:
                self.direction = 1
            else:
                self.direction = -1
        else:
            self.looking_at_cursor = False

        # Periodic particle emissions
        if self.current_state == 'SLEEP' and self.frame_ticks % 60 == 0:
            particle_sys.spawn('zzz', window_width // 2, 10, count=1)
        elif self.current_state == 'HAPPY' and self.frame_ticks % 30 == 0:
            particle_sys.spawn('heart', window_width // 2, 15, count=1)
        elif self.current_state == 'EXCITED' and self.frame_ticks % 25 == 0:
            particle_sys.spawn('sparkle', window_width // 2, 15, count=1)
        elif self.current_state == 'PLAY' and self.frame_ticks % 40 == 0:
            particle_sys.spawn('music', window_width // 2, 15, count=1)
        elif self.is_night() and random.random() < 0.005:
            particle_sys.spawn('star', random.randint(5, window_width - 5), 5, count=1)

        # Movement updates
        new_x = window_x
        if self.current_state in ('WALK', 'ROLL'):
            move_speed = self.speed * (1.5 if self.current_state == 'ROLL' else 1.0)
            new_x += int(self.direction * move_speed)
            
            # Keep pet safely within screen bounds
            min_x = 0
            max_x = screen_width - window_width
            if new_x <= min_x:
                new_x = min_x
                self.direction = 1  # Turn right
            elif new_x >= max_x:
                new_x = max_x
                self.direction = -1  # Turn left

        # Random speech bubble trigger during idle/walk
        if self.current_state in ('IDLE', 'WALK', 'SIT') and not speech_bubble.visible:
            if random.random() < 0.001:  # Occasional dialogue
                speech_bubble.show_message(self.pet_type)

        # Switch states when timer expires
        if self.state_timer <= 0:
            self.set_random_state()
            
        return new_x

    def get_current_frame_name(self):
        """Returns the sprite frame name based on current state and animation ticker."""
        prefix = f"{self.pet_type}_"
        suffix = "_left.png" if self.direction == -1 else ".png"
        
        # Frame animation ticker (cycle every 12 ticks ~ 5 fps)
        anim_step = (self.frame_ticks // 12)
        
        if self.current_state == 'IDLE':
            if self.looking_at_cursor:
                frame_id = 'curious'
            else:
                cycle = anim_step % 6
                if cycle == 3:
                    frame_id = 'blink'
                elif cycle in (1, 2):
                    frame_id = 'idle_2'
                elif cycle == 4:
                    frame_id = 'idle_3'
                else:
                    frame_id = 'idle_1'
                    
        elif self.current_state == 'WALK':
            frame_id = f"walk_{1 + (anim_step % 4)}"
            
        elif self.current_state == 'SIT':
            frame_id = 'sit'
            
        elif self.current_state == 'SLEEP':
            frame_id = f"sleep_{1 + (anim_step % 2)}"
            
        elif self.current_state == 'HAPPY':
            frame_id = f"happy_{1 + (anim_step % 2)}"
            
        elif self.current_state == 'ANGRY':
            frame_id = 'angry' if self.pet_type == 'cat' else 'surprised'
            
        elif self.current_state == 'CURIOUS':
            frame_id = 'curious'
            
        elif self.current_state == 'EXCITED':
            frame_id = 'excited' if self.pet_type == 'cat' else 'happy_1'
            
        elif self.current_state == 'EAT':
            if self.pet_type == 'panda':
                frame_id = f"eat_{1 + (anim_step % 2)}"
            else:
                frame_id = f"happy_{1 + (anim_step % 2)}"
                
        elif self.current_state == 'ROLL':
            if self.pet_type == 'panda':
                frame_id = f"roll_{1 + (anim_step % 4)}"
            else:
                frame_id = f"walk_{1 + (anim_step % 4)}"
                
        elif self.current_state == 'PLAY':
            if self.pet_type == 'panda':
                frame_id = f"play_{1 + (anim_step % 2)}"
            else:
                frame_id = f"happy_{1 + (anim_step % 2)}"
        else:
            frame_id = 'idle_1'
            
        return prefix + frame_id + suffix
