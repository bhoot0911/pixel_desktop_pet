import os
from PIL import Image, ImageDraw

# Create sprites output directory
SPRITES_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(SPRITES_DIR, exist_ok=True)

GRID_SIZE = 48  # 48x48 pixel base canvas size

def create_canvas():
    """Creates a blank transparent 48x48 RGBA image."""
    return Image.new("RGBA", (GRID_SIZE, GRID_SIZE), (0, 0, 0, 0))

def hex_to_rgba(hex_str, alpha=255):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)

# Color Palettes
CAT_PALETTE = {
    'O': hex_to_rgba('2B1E1A'),  # Outline chocolate dark
    'B': hex_to_rgba('F7A046'),  # Body warm ginger orange
    'S': hex_to_rgba('D87B26'),  # Body shade
    'W': hex_to_rgba('FFF6E5'),  # White chest/muzzle/paws
    'P': hex_to_rgba('FF85A1'),  # Soft pink ears/nose/blush/toe-beans
    'E': hex_to_rgba('1B2A4A'),  # Eye navy
    'H': hex_to_rgba('FFFFFF'),  # Eye highlight sparkle
    'R': hex_to_rgba('FF99A8'),  # Cheerful blush
    'T': hex_to_rgba('BF5C14'),  # Stripes
    'K': hex_to_rgba('6B493B'),  # Soft whiskers
    '.': (0, 0, 0, 0)             # Transparent
}

PANDA_PALETTE = {
    'O': hex_to_rgba('161B22'),  # Dark outline
    'W': hex_to_rgba('F5F6F8'),  # White fluffy body
    'S': hex_to_rgba('D0D7DE'),  # White shade
    'B': hex_to_rgba('24292F'),  # Charcoal black patches/limbs
    'L': hex_to_rgba('38414A'),  # Black highlight / paw pad
    'P': hex_to_rgba('FF85A1'),  # Pink cheeks & mouth
    'E': hex_to_rgba('0D1117'),  # Deep eye pupil
    'H': hex_to_rgba('FFFFFF'),  # Eye glint
    'G': hex_to_rgba('38B000'),  # Bamboo leaf green
    '.': (0, 0, 0, 0)             # Transparent
}

def draw_pixels(img, pixel_matrix, palette, offset_x=0, offset_y=0):
    """Draws pixel matrix onto PIL Image."""
    pixels = img.load()
    for y, row in enumerate(pixel_matrix):
        for x, char in enumerate(row):
            if char in palette and char != '.':
                px = x + offset_x
                py = y + offset_y
                if 0 <= px < GRID_SIZE and 0 <= py < GRID_SIZE:
                    pixels[px, py] = palette[char]

class PixelArtBuilder:
    @staticmethod
    def draw_cat_frame(frame_name, eye_state='open', mouth_state='normal', pose='idle', frame_num=0, flipped=False):
        img = create_canvas()
        
        y_off = 1 if (pose == 'idle' and frame_num == 1) else (2 if (pose == 'idle' and frame_num == 2) else 0)
        if pose == 'sleep':
            y_off = 2

        # 1. Ears (Fluffy, Pink Inner Padding)
        cat_ears = [
            "  OOO        OOO  ",
            " OPOOO      OPOOO ",
            "OPPPOOO    OPPPOOO",
            "OPPPPOO    OPPPPOO",
            "OBBBBBBOOOOBBBBBBO"
        ]
        draw_pixels(img, cat_ears, CAT_PALETTE, offset_x=15, offset_y=8 + y_off)

        # 2. Head Base (Defined Rounded Shape)
        cat_head = [
            "   OOOOOOOOOOOOOO   ",
            "  OBBBBBBBBBBBBBBO  ",
            " OBBBBBTBBBBTBBBBBO ",
            "OBBBBBBBBBBBBBBBBBBO",
            "OBBBBBBBBBBBBBBBBBBO",
            "OBBBWWWWWWWWWWWWBBBO",
            "OBBBWWWWWWWWWWWWBBBO",
            " OBBBWWWWWWWWWWBBBO ",
            "  OOOOOOOOOOOOOOOO  "
        ]
        head_x = 14
        head_y = 12 + y_off
        draw_pixels(img, cat_head, CAT_PALETTE, offset_x=head_x, offset_y=head_y)

        # 3. Whiskers
        whiskers_l = ["K K ", " K  "]
        whiskers_r = [" K K", "  K "]
        draw_pixels(img, whiskers_l, CAT_PALETTE, offset_x=head_x - 3, offset_y=head_y + 4)
        draw_pixels(img, whiskers_r, CAT_PALETTE, offset_x=head_x + 19, offset_y=head_y + 4)

        # 4. Clear Defined Eyes
        if eye_state == 'open':
            eyes = [
                " OOOO    OOOO ",
                "OHEEEO  OHEEEO",
                "OEEEEO  OEEEEO",
                " OOOO    OOOO "
            ]
            draw_pixels(img, eyes, CAT_PALETTE, offset_x=head_x + 3, offset_y=head_y + 2)
            draw_pixels(img, ["RR", "RR"], CAT_PALETTE, offset_x=head_x + 2, offset_y=head_y + 5)
            draw_pixels(img, ["RR", "RR"], CAT_PALETTE, offset_x=head_x + 16, offset_y=head_y + 5)
            
        elif eye_state == 'blink' or eye_state == 'closed':
            eyes = [
                " OOOO    OOOO ",
                "              "
            ]
            draw_pixels(img, eyes, CAT_PALETTE, offset_x=head_x + 3, offset_y=head_y + 3)
            
        elif eye_state == 'happy':
            eyes = [
                "  OO      OO  ",
                " O  O    O  O "
            ]
            draw_pixels(img, eyes, CAT_PALETTE, offset_x=head_x + 4, offset_y=head_y + 2)
            draw_pixels(img, ["RR", "RR"], CAT_PALETTE, offset_x=head_x + 2, offset_y=head_y + 5)
            draw_pixels(img, ["RR", "RR"], CAT_PALETTE, offset_x=head_x + 16, offset_y=head_y + 5)

        # 5. Nose & Mouth
        draw_pixels(img, [" P "], CAT_PALETTE, offset_x=head_x + 8, offset_y=head_y + 4)
        draw_pixels(img, ["OPO" if mouth_state == 'open' else "O O"], CAT_PALETTE, offset_x=head_x + 8, offset_y=head_y + 5)

        # 6. Body & Highly Defined Paws/Legs
        if pose in ('idle', 'excited', 'curious', 'type', 'scroll'):
            body = [
                "   OOOOOOOOOO   ",
                "  OWWBBBBBBWWO  ",
                " OWWWWBBBBWWWO ",
                " OWWWWBBBBWWWO ",
                "  OWWWWWWWWWWO  ",
                "   OOOOOOOOOO   "
            ]
            draw_pixels(img, body, CAT_PALETTE, offset_x=17, offset_y=20 + y_off)

            # CLEAR DEFINED PAWS (Left & Right Paws with Pink Toe Beans)
            if pose == 'type':
                if frame_num % 2 == 0:
                    paws = [
                        "  OO    OO  ",
                        " OWPO   OO  ",
                        "  OO   OWPO ",
                        "        OO  "
                    ]
                else:
                    paws = [
                        "  OO    OO  ",
                        "  OO   OWPO ",
                        " OWPO   OO  ",
                        "  OO        "
                    ]
            elif pose == 'scroll':
                paws = [
                    " OWPO  OWPO ",
                    "  OO    OO  ",
                    " OWW    WW  ",
                    "  OO    OO  "
                ]
            else:
                paws = [
                    "  OO    OO  ",
                    " OWPO  OWPO ",
                    " OWW    WW  ",
                    "  OO    OO  "
                ]
            draw_pixels(img, paws, CAT_PALETTE, offset_x=18, offset_y=24 + y_off)

            # Tail sway
            tail_frames = [
                ["     OO", "    OB ", "   OB  ", "  OBO  ", " OO    "],
                ["      OO", "     OB ", "    OB  ", "   OBO  ", "  OO    "],
                ["    OO  ", "   OB   ", "   OB   ", "  OBO   ", " OO     "]
            ]
            tf = tail_frames[frame_num % len(tail_frames)]
            draw_pixels(img, tf, CAT_PALETTE, offset_x=28, offset_y=19 + y_off)

        elif pose == 'walk':
            body = [
                "   OOOOOOOOOO   ",
                "  OWWBBBBBBWWO  ",
                " OWWWWBBBBWWWO ",
                " OWWWWBBBBWWWO ",
                "  OWWWWWWWWWWO  ",
                "   OOOOOOOOOO   "
            ]
            draw_pixels(img, body, CAT_PALETTE, offset_x=17, offset_y=20)
            if frame_num % 2 == 0:
                paws = [
                    " OWPO   OO  ",
                    "OWWO   OWPO ",
                    " OO     OO  "
                ]
            else:
                paws = [
                    "  OO   OWPO ",
                    " OWPO  OWWO ",
                    "  OO    OO  "
                ]
            draw_pixels(img, paws, CAT_PALETTE, offset_x=18, offset_y=24)
            draw_pixels(img, ["   OO", "  OB ", " OBO ", "OO   "], CAT_PALETTE, offset_x=28, offset_y=19)

        elif pose == 'sit':
            body = [
                "   OOOOOOOOOO   ",
                "  OWWBBBBBBWWO  ",
                " OWWWWBBBBWWWO ",
                " OWWWWBBBBWWWO ",
                " OWWWWWWWWWWWO ",
                "  OOOOOOOOOOO  "
            ]
            draw_pixels(img, body, CAT_PALETTE, offset_x=17, offset_y=20)
            paws = [
                "  OOOOOOOO  ",
                " OWPO  OWPO ",
                " OWWWWWWWO  "
            ]
            draw_pixels(img, paws, CAT_PALETTE, offset_x=18, offset_y=24)

        elif pose == 'sleep':
            body_sleep = [
                "    OOOOOOOOOOOO    ",
                "   OBBBBBBBBBBBBO   ",
                "  OBBWWWWWWBBBBBBO  ",
                " OBBWWWWWWWWBBBBBBO ",
                "  OOOOOOOOOOOOOOOO  "
            ]
            draw_pixels(img, body_sleep, CAT_PALETTE, offset_x=14, offset_y=22 + y_off)

        if flipped:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

        return img

    @staticmethod
    def draw_panda_frame(frame_name, eye_state='open', mouth_state='normal', pose='idle', frame_num=0, flipped=False):
        img = create_canvas()
        
        y_off = 1 if (pose == 'idle' and frame_num == 1) else (2 if (pose == 'idle' and frame_num == 2) else 0)
        if pose == 'sleep':
            y_off = 2

        # 1. Round Black Ears
        ears = [
            "  OOOO     OOOO  ",
            " OBBBBO   OBBBBO ",
            "OBBBBBBO OBBBBBBO",
            " OOOOOOO  OOOOOOO "
        ]
        draw_pixels(img, ears, PANDA_PALETTE, offset_x=15, offset_y=7 + y_off)

        # 2. Head Base (White Fluffy Face)
        head_base = [
            "   OOOOOOOOOOOOOO   ",
            "  OWWWWWWWWWWWWWWO  ",
            " OWWWWWWWWWWWWWWWWO ",
            "OWWWWWWWWWWWWWWWWWWO",
            "OWWWWWWWWWWWWWWWWWWO",
            "OWWWWWWWWWWWWWWWWWWO",
            " OWWWWWWWWWWWWWWWWO ",
            "  OOOOOOOOOOOOOOOO  "
        ]
        head_x = 14
        head_y = 11 + y_off
        draw_pixels(img, head_base, PANDA_PALETTE, offset_x=head_x, offset_y=head_y)

        # 3. Eye Patches & Big Shiny Eyes
        if eye_state == 'open':
            patches = [
                " OBBBO    OBBBO ",
                "OBHEBBO  OBHEBBO",
                "OBHEBBO  OBHEBBO",
                " OBBBO    OBBBO "
            ]
            draw_pixels(img, patches, PANDA_PALETTE, offset_x=head_x + 2, offset_y=head_y + 2)
            draw_pixels(img, ["PP", "PP"], PANDA_PALETTE, offset_x=head_x + 1, offset_y=head_y + 5)
            draw_pixels(img, ["PP", "PP"], PANDA_PALETTE, offset_x=head_x + 15, offset_y=head_y + 5)
        elif eye_state == 'happy':
            patches = [
                " OBBBO    OBBBO ",
                "OB O BBO OBO BBO",
                " OBBBO    OBBBO "
            ]
            draw_pixels(img, patches, PANDA_PALETTE, offset_x=head_x + 2, offset_y=head_y + 3)
            draw_pixels(img, ["PP", "PP"], PANDA_PALETTE, offset_x=head_x + 1, offset_y=head_y + 5)
            draw_pixels(img, ["PP", "PP"], PANDA_PALETTE, offset_x=head_x + 15, offset_y=head_y + 5)

        # 4. Nose & Mouth
        draw_pixels(img, [" B "], PANDA_PALETTE, offset_x=head_x + 8, offset_y=head_y + 4)
        draw_pixels(img, ["OPO" if mouth_state in ('open', 'eat') else "OBO"], PANDA_PALETTE, offset_x=head_x + 8, offset_y=head_y + 5)

        # 5. Body & Highly Defined Black Arms & Legs
        if pose in ('idle', 'surprised', 'curious', 'type', 'scroll'):
            body = [
                "   OOOOOOOOOO   ",
                "  OBBWWWWWWBBO  ",
                " OBBBWWWWWWBBBO ",
                " OBBBWWWWWWBBBO ",
                "  OWWWWWWWWWWO  ",
                "   OOOOOOOOOO   "
            ]
            draw_pixels(img, body, PANDA_PALETTE, offset_x=17, offset_y=19 + y_off)

            # CLEAR DEFINED PANDA ARMS & LEGS WITH WHITE PAW PADS
            if pose == 'type':
                if frame_num % 2 == 0:
                    limbs = [
                        "  OOOO    OOOO  ",
                        " OBBLBO   OBBBO ",
                        "  OBBBO  OBBLBO ",
                        "   OO      OO   "
                    ]
                else:
                    limbs = [
                        "  OOOO    OOOO  ",
                        "  OBBBO  OBBLBO ",
                        " OBBLBO   OBBBO ",
                        "   OO      OO   "
                    ]
            elif pose == 'scroll':
                limbs = [
                    " OBBLBO  OBBLBO ",
                    "  OBBBO   OBBBO ",
                    "   OOOO   OOOO  "
                ]
            else:
                limbs = [
                    "  OOOO    OOOO  ",
                    " OBBLBO  OBBLBO ",
                    "  OBBBO   OBBBO ",
                    "   OO      OO   "
                ]
            draw_pixels(img, limbs, PANDA_PALETTE, offset_x=17, offset_y=23 + y_off)

        elif pose == 'walk':
            body = [
                "   OOOOOOOOOO   ",
                "  OBBWWWWWWBBO  ",
                " OBBBWWWWWWBBBO ",
                " OBBBWWWWWWBBBO ",
                "  OWWWWWWWWWWO  ",
                "   OOOOOOOOOO   "
            ]
            draw_pixels(img, body, PANDA_PALETTE, offset_x=17, offset_y=19)
            if frame_num % 2 == 0:
                limbs = [" OBBLBO  OOOO ", "  OBBBO OBBLBO", "   OO    OOOO "]
            else:
                limbs = [" OOOO   OBBLBO", "OBBLBO   OBBBO", " OOOO     OO  "]
            draw_pixels(img, limbs, PANDA_PALETTE, offset_x=17, offset_y=23)

        elif pose in ('sit', 'eat'):
            body = [
                "   OOOOOOOOOO   ",
                "  OBBWWWWWWBBO  ",
                " OBBBWWWWWWBBBO ",
                " OBBBWWWWWWBBBO ",
                "  OBBBBBBBBBBO  ",
                "   OOOOOOOOOO   "
            ]
            draw_pixels(img, body, PANDA_PALETTE, offset_x=17, offset_y=19)
            limbs = [
                "  OOOOOOOOOO  ",
                " OBBLBBBBBLBO ",
                "  OOOOOOOOOO  "
            ]
            draw_pixels(img, limbs, PANDA_PALETTE, offset_x=17, offset_y=24)

        elif pose == 'roll':
            angle = (frame_num % 4) * 90
            base_roll = create_canvas()
            ball = [
                "    OOOOOOOO    ",
                "   OBBBBBBBBO   ",
                "  OBBWWWWWWBBO  ",
                " OBBWWWWWWWWBBO ",
                " OBBWWWWWWWWBBO ",
                "  OBBWWWWWWBBO  ",
                "   OBBBBBBBBO   ",
                "    OOOOOOOO    "
            ]
            draw_pixels(base_roll, ball, PANDA_PALETTE, offset_x=16, offset_y=19)
            img = base_roll.rotate(angle)

        if flipped:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

        return img

def generate_all_sprites():
    """Generates all Cat and Panda animation frames including typing/scroll reactions and saves them as PNGs."""
    print("Generating enhanced pixel art sprites with clear paws and limbs...")
    
    # CAT ANIMATIONS
    cat_frames = {
        'idle_1': PixelArtBuilder.draw_cat_frame('idle_1', eye_state='open', pose='idle', frame_num=0),
        'idle_2': PixelArtBuilder.draw_cat_frame('idle_2', eye_state='open', pose='idle', frame_num=1),
        'idle_3': PixelArtBuilder.draw_cat_frame('idle_3', eye_state='open', pose='idle', frame_num=2),
        'blink': PixelArtBuilder.draw_cat_frame('blink', eye_state='blink', pose='idle', frame_num=0),
        'walk_1': PixelArtBuilder.draw_cat_frame('walk_1', eye_state='open', pose='walk', frame_num=0),
        'walk_2': PixelArtBuilder.draw_cat_frame('walk_2', eye_state='open', pose='walk', frame_num=1),
        'walk_3': PixelArtBuilder.draw_cat_frame('walk_3', eye_state='open', pose='walk', frame_num=2),
        'walk_4': PixelArtBuilder.draw_cat_frame('walk_4', eye_state='open', pose='walk', frame_num=3),
        'sit': PixelArtBuilder.draw_cat_frame('sit', eye_state='open', pose='sit', frame_num=0),
        'sleep_1': PixelArtBuilder.draw_cat_frame('sleep_1', eye_state='closed', pose='sleep', frame_num=0),
        'sleep_2': PixelArtBuilder.draw_cat_frame('sleep_2', eye_state='closed', pose='sleep', frame_num=1),
        'happy_1': PixelArtBuilder.draw_cat_frame('happy_1', eye_state='happy', mouth_state='open', pose='idle', frame_num=0),
        'happy_2': PixelArtBuilder.draw_cat_frame('happy_2', eye_state='happy', mouth_state='open', pose='idle', frame_num=1),
        'type_1': PixelArtBuilder.draw_cat_frame('type_1', eye_state='happy', mouth_state='open', pose='type', frame_num=0),
        'type_2': PixelArtBuilder.draw_cat_frame('type_2', eye_state='happy', mouth_state='open', pose='type', frame_num=1),
        'scroll_1': PixelArtBuilder.draw_cat_frame('scroll_1', eye_state='open', mouth_state='open', pose='scroll', frame_num=0),
        'scroll_2': PixelArtBuilder.draw_cat_frame('scroll_2', eye_state='happy', mouth_state='open', pose='scroll', frame_num=1),
        'angry': PixelArtBuilder.draw_cat_frame('angry', eye_state='angry', mouth_state='frown', pose='idle', frame_num=0),
        'curious': PixelArtBuilder.draw_cat_frame('curious', eye_state='open', pose='curious', frame_num=0),
        'excited': PixelArtBuilder.draw_cat_frame('excited', eye_state='happy', mouth_state='open', pose='excited', frame_num=1)
    }

    # Save Cat frames
    for name, img in cat_frames.items():
        img.save(os.path.join(SPRITES_DIR, f"cat_{name}.png"))
        img.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(SPRITES_DIR, f"cat_{name}_left.png"))

    # PANDA ANIMATIONS
    panda_frames = {
        'idle_1': PixelArtBuilder.draw_panda_frame('idle_1', eye_state='open', pose='idle', frame_num=0),
        'idle_2': PixelArtBuilder.draw_panda_frame('idle_2', eye_state='open', pose='idle', frame_num=1),
        'idle_3': PixelArtBuilder.draw_panda_frame('idle_3', eye_state='open', pose='idle', frame_num=2),
        'blink': PixelArtBuilder.draw_panda_frame('blink', eye_state='blink', pose='idle', frame_num=0),
        'walk_1': PixelArtBuilder.draw_panda_frame('walk_1', eye_state='open', pose='walk', frame_num=0),
        'walk_2': PixelArtBuilder.draw_panda_frame('walk_2', eye_state='open', pose='walk', frame_num=1),
        'walk_3': PixelArtBuilder.draw_panda_frame('walk_3', eye_state='open', pose='walk', frame_num=2),
        'walk_4': PixelArtBuilder.draw_panda_frame('walk_4', eye_state='open', pose='walk', frame_num=3),
        'sit': PixelArtBuilder.draw_panda_frame('sit', eye_state='open', pose='sit', frame_num=0),
        'sleep_1': PixelArtBuilder.draw_panda_frame('sleep_1', eye_state='closed', pose='sleep', frame_num=0),
        'sleep_2': PixelArtBuilder.draw_panda_frame('sleep_2', eye_state='closed', pose='sleep', frame_num=1),
        'eat_1': PixelArtBuilder.draw_panda_frame('eat_1', eye_state='open', mouth_state='eat', pose='eat', frame_num=0),
        'eat_2': PixelArtBuilder.draw_panda_frame('eat_2', eye_state='happy', mouth_state='eat', pose='eat', frame_num=1),
        'type_1': PixelArtBuilder.draw_panda_frame('type_1', eye_state='happy', mouth_state='open', pose='type', frame_num=0),
        'type_2': PixelArtBuilder.draw_panda_frame('type_2', eye_state='happy', mouth_state='open', pose='type', frame_num=1),
        'scroll_1': PixelArtBuilder.draw_panda_frame('scroll_1', eye_state='open', mouth_state='open', pose='scroll', frame_num=0),
        'scroll_2': PixelArtBuilder.draw_panda_frame('scroll_2', eye_state='happy', mouth_state='open', pose='scroll', frame_num=1),
        'roll_1': PixelArtBuilder.draw_panda_frame('roll_1', eye_state='happy', pose='roll', frame_num=0),
        'roll_2': PixelArtBuilder.draw_panda_frame('roll_2', eye_state='happy', pose='roll', frame_num=1),
        'roll_3': PixelArtBuilder.draw_panda_frame('roll_3', eye_state='happy', pose='roll', frame_num=2),
        'roll_4': PixelArtBuilder.draw_panda_frame('roll_4', eye_state='happy', pose='roll', frame_num=3),
        'happy_1': PixelArtBuilder.draw_panda_frame('happy_1', eye_state='happy', mouth_state='open', pose='idle', frame_num=0),
        'happy_2': PixelArtBuilder.draw_panda_frame('happy_2', eye_state='happy', mouth_state='open', pose='idle', frame_num=1),
        'curious': PixelArtBuilder.draw_panda_frame('curious', eye_state='open', pose='curious', frame_num=0),
        'surprised': PixelArtBuilder.draw_panda_frame('surprised', eye_state='surprised', mouth_state='open', pose='surprised', frame_num=0),
        'play_1': PixelArtBuilder.draw_panda_frame('play_1', eye_state='happy', pose='idle', frame_num=0),
        'play_2': PixelArtBuilder.draw_panda_frame('play_2', eye_state='happy', pose='idle', frame_num=1)
    }

    for name, img in panda_frames.items():
        img.save(os.path.join(SPRITES_DIR, f"panda_{name}.png"))
        img.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(SPRITES_DIR, f"panda_{name}_left.png"))

    print(f"Enhanced sprites with clear limbs generated ({len(cat_frames)*2 + len(panda_frames)*2} frames)!")

if __name__ == "__main__":
    generate_all_sprites()
