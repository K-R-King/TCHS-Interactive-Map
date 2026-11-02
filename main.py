import os
import pygame
import sys

# Load assets relative to this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Keep Windows display scaling from enlarging the window past the screen edges
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()

# Create a Pygame window
# SCALED stretches the map to fill the window when it is resized, maximized or fullscreen
os.environ['SDL_RENDER_SCALE_QUALITY'] = 'best'
screen = pygame.display.set_mode((1240, 930), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('TCHS Interactive Map')

# Colours
TEXT_COLOR = (30, 41, 59)
SUBTITLE_COLOR = (71, 85, 105)
LETTERBOX_COLOR = (15, 23, 42)
RED = (220, 38, 38)
PURPLE = (147, 51, 234)
GREEN = (22, 163, 74)
YELLOW = (202, 138, 4)
BLUE = (37, 99, 235)
ORANGE = (234, 88, 12)
BROWN = (146, 64, 14)
BACK = (51, 65, 85)


# Scale a photo to fit the window without stretching it, centred on a dark background
def fit_to_window(image):
    scale = min(1240 / image.get_width(), 930 / image.get_height())
    size = (round(image.get_width() * scale), round(image.get_height() * scale))
    scaled = pygame.transform.smoothscale(image.convert(), size)
    canvas = pygame.Surface((1240, 930))
    canvas.fill(LETTERBOX_COLOR)
    canvas.blit(scaled, scaled.get_rect(center=(620, 465)))
    return canvas


# Mix a colour with white; amount 0 = white, 1 = the full colour
def tint(color, amount):
    return tuple(round(255 + (c - 255) * amount) for c in color)


# Load the label font at a given size, falling back to pygame's built-in font
label_font_path = pygame.font.match_font('segoeuisemibold,segoeui,helveticaneue,arial')
label_fonts = {}
def label_font(size):
    if size not in label_fonts:
        label_fonts[size] = pygame.font.Font(label_font_path, size)
    return label_fonts[size]


# Render text trimmed to its visible pixels, so it centres exactly
def render_tight(text, size, color):
    rendered = label_font(size).render(text, True, color)
    bounds = rendered.get_bounding_rect()
    return rendered.subsurface(bounds).copy() if bounds.width else rendered


# Split text into lines no wider than max_w at this font size
def wrap(text, size, max_w):
    lines = []
    for word in text.split(' '):
        if lines and label_font(size).size(lines[-1] + ' ' + word)[0] <= max_w:
            lines[-1] += ' ' + word
        else:
            lines.append(word)
    return lines


# Stack rendered lines on top of each other, centred
def stack(parts, gap):
    w = max(p.get_width() for p in parts)
    h = sum(p.get_height() for p in parts) + gap * (len(parts) - 1)
    stacked = pygame.Surface((w, h), pygame.SRCALPHA)
    y = 0
    for p in parts:
        stacked.blit(p, ((w - p.get_width()) // 2, y))
        y += p.get_height() + gap
    return stacked


# Render a button label as large as fits inside the button, wrapping if needed.
# An optional subtitle is drawn small underneath, like the printed map's notes.
labels = {}
def render_label(text, surface, color=TEXT_COLOR, max_size=None, subtitle=None):
    labels[surface] = text + (' – ' + subtitle if subtitle else '')
    pad = 6 if surface.get_width() > 40 else 3
    max_w, max_h = surface.get_width() - pad, surface.get_height() - 3
    note = None
    if subtitle:
        for size in (9, 8, 7):
            note = stack([render_tight(line, size, SUBTITLE_COLOR) for line in wrap(subtitle, size, max_w)], 1)
            if note.get_width() <= max_w:
                break
        max_h -= note.get_height() + 3
    # Tall, narrow boxes get sideways text, like the printed map
    sideways = max_h > 2 * max_w and ' ' in text
    if sideways:
        max_w, max_h = max_h, max_w
    # One size for regular rooms so rows match; larger only for big areas
    max_size = max_size or (24 if min(max_w, max_h) >= 56 else 19)
    for size in range(max_size, 6, -1):
        parts = [render_tight(line, size, color) for line in wrap(text, size, max_w)]
        label = stack(parts, round(size * 0.3))
        if label.get_width() <= max_w and label.get_height() <= max_h:
            if sideways:
                return pygame.transform.rotate(label, 90)
            return stack([label, note], 3) if note else label
    # Very small boxes: shrink the smallest text until it fits
    label = stack([render_tight(line, 7, color) for line in wrap(text, 7, max_w)], 1)
    scale = min(max_w / label.get_width(), max_h / label.get_height(), 1)
    return pygame.transform.smoothscale(label, (max(1, int(label.get_width() * scale)), max(1, int(label.get_height() * scale))))


# Full names shown in the caption when a room's photo is open
TITLES = {'RR': 'Restroom', 'Sr. Circle': 'Senior Circle', 'Conf Room': 'Conference Room',
          'Locker': 'Locker Rooms', 'Lunch': 'Lunch Shelter', 'Weight Room & Dance Studio 701': 'Weight Room & Dance Studio (701)',
          'Counseling College & Career': 'Counseling / College & Career'}
def full_title(text):
    return 'Room ' + text if text[:1].isdigit() else TITLES.get(text, text)


# Load map
map = pygame.image.load('assets/map_2025.png').convert()

# Load images of school
# Red
rm_601_image = pygame.image.load('assets/601.jpg')
rm_601_image = fit_to_window(rm_601_image)
staff_lounge_image = pygame.image.load('assets/staff_lounge.jpg')
staff_lounge_image = fit_to_window(staff_lounge_image)
rm_216_image = pygame.image.load('assets/214.jpg')
rm_216_image = fit_to_window(rm_216_image)
rm_215_image = pygame.image.load('assets/214.jpg')
rm_215_image = fit_to_window(rm_215_image)
rm_214_image = pygame.image.load('assets/214.jpg')
rm_214_image = fit_to_window(rm_214_image)
RR_1_image = pygame.image.load('assets/214.jpg')
RR_1_image = fit_to_window(RR_1_image)
rm_116_image = pygame.image.load('assets/116.jpg')
rm_116_image = fit_to_window(rm_116_image)
rm_115_image = pygame.image.load('assets/115.jpg')
rm_115_image = fit_to_window(rm_115_image)
rm_114_image = pygame.image.load('assets/114.jpg')
rm_114_image = fit_to_window(rm_114_image)
RR_2_image = pygame.image.load('assets/601.jpg')
RR_2_image = fit_to_window(RR_2_image)
rm_213_image = pygame.image.load('assets/213.jpg')
rm_213_image = fit_to_window(rm_213_image)
rm_113_image = pygame.image.load('assets/113.jpg')
rm_113_image = fit_to_window(rm_113_image)
rm_108_image = pygame.image.load('assets/108.jpg')
rm_108_image = fit_to_window(rm_108_image)
rm_208_image = pygame.image.load('assets/208.jpg')
rm_208_image = fit_to_window(rm_208_image)
rm_212_image = pygame.image.load('assets/601.jpg')
rm_212_image = fit_to_window(rm_212_image)
rm_211_image = pygame.image.load('assets/601.jpg')
rm_211_image = fit_to_window(rm_211_image)
rm_210_image = pygame.image.load('assets/601.jpg')
rm_210_image = fit_to_window(rm_210_image)
rm_209_image = pygame.image.load('assets/601.jpg')
rm_209_image = fit_to_window(rm_209_image)
RR_3_image = pygame.image.load('assets/601.jpg')
RR_3_image = fit_to_window(RR_3_image)
rm_112_image = pygame.image.load('assets/601.jpg')
rm_112_image = fit_to_window(rm_112_image)
rm_111_image = pygame.image.load('assets/601.jpg')
rm_111_image = fit_to_window(rm_111_image)
rm_110_image = pygame.image.load('assets/110.jpg')
rm_110_image = fit_to_window(rm_110_image)
rm_109_image = pygame.image.load('assets/601.jpg')
rm_109_image = fit_to_window(rm_109_image)
RR_4_image = pygame.image.load('assets/601.jpg')
RR_4_image = fit_to_window(RR_4_image)
# Red
# Purple
RR_400_image = pygame.image.load('assets/boys_ bathroom_200s.jpg')
RR_400_image = fit_to_window(RR_400_image)
rm_401_image = pygame.image.load('assets/ROOM 401-1.jpg')
rm_401_image = fit_to_window(rm_401_image)
rm_402_image = pygame.image.load('assets/ROOM 402-2.jpg')
rm_402_image = fit_to_window(rm_402_image)
rm_403_image = pygame.image.load('assets/ROOM 403-1.jpg')
rm_403_image = fit_to_window(rm_403_image)
rm_404_image = pygame.image.load('assets/ROOM 404-1.jpg')
rm_404_image = fit_to_window(rm_404_image)
rm_405_image = pygame.image.load('assets/ROOM 405-1.jpg')
rm_405_image = fit_to_window(rm_405_image)
rm_406_image = pygame.image.load('assets/ROOM 406-1.jpg')
rm_406_image = fit_to_window(rm_406_image)
rm_407_image = pygame.image.load('assets/ROOM 407-1.jpg')
rm_407_image = fit_to_window(rm_407_image)
rm_408_image = pygame.image.load('assets/ROOM 408-1.jpg')
rm_408_image = fit_to_window(rm_408_image)
rm_409_image = pygame.image.load('assets/ROOM 409-1.jpg')
rm_409_image = fit_to_window(rm_409_image)
# Purple
# Green
gym_image = pygame.image.load('assets/Front Entrance to Gym.jpg')
gym_image = fit_to_window(gym_image)
tennis_image = pygame.image.load('assets/Tennis Courts.jpg')
tennis_image = fit_to_window(tennis_image)
rm_702_image = pygame.image.load('assets/Room 702 and Tennis Court Entrance.jpg')
rm_702_image = fit_to_window(rm_702_image)
circle_image = pygame.image.load('assets/Senior Circle_1.jpg')
circle_image = fit_to_window(circle_image)
rm_703_image = pygame.image.load('assets/601.jpg')
rm_703_image = fit_to_window(rm_703_image)
rm_704_image = pygame.image.load('assets/700s side and gym stairs.jpg')
rm_704_image = fit_to_window(rm_704_image)
rm_705_image = pygame.image.load('assets/room 705 (edt) and 704.jpg')
rm_705_image = fit_to_window(rm_705_image)
rm_706_image = pygame.image.load('assets/room 706 and 707.jpg')
rm_706_image = fit_to_window(rm_706_image)
rm_707_image = pygame.image.load('assets/room 707.jpg')
rm_707_image = fit_to_window(rm_707_image)
rm_708_image = pygame.image.load('assets/601.jpg')
rm_708_image = fit_to_window(rm_708_image)
rm_709_image = pygame.image.load('assets/Boys restroom and art room.jpg')
rm_709_image = fit_to_window(rm_709_image)
rm_801_image = pygame.image.load('assets/601.jpg')
rm_801_image = fit_to_window(rm_801_image)
rm_802_image = pygame.image.load('assets/601.jpg')
rm_802_image = fit_to_window(rm_802_image)
rr_1_image = pygame.image.load('assets/room 707 windows and girls restroom.jpg')
rr_1_image = fit_to_window(rr_1_image)
weight_image = pygame.image.load('assets/Weight Room.jpg')
weight_image = fit_to_window(weight_image)
# Green
# Yellow
rm_501_image = pygame.image.load('assets/rm_501.jpg')
rm_501_image = fit_to_window(rm_501_image)
rm_502_image = pygame.image.load('assets/rm_502.jpg')
rm_502_image = fit_to_window(rm_502_image)
rm_503_image = pygame.image.load('assets/rm_503.jpg')
rm_503_image = fit_to_window(rm_503_image)
rm_504_image = pygame.image.load('assets/rm_504.jpg')
rm_504_image = fit_to_window(rm_504_image)
rm_505_image = pygame.image.load('assets/rm_505.jpg')
rm_505_image = fit_to_window(rm_505_image)
rm_506_image = pygame.image.load('assets/rm_506.jpg')
rm_506_image = fit_to_window(rm_506_image)
rm_507_image = pygame.image.load('assets/rm_507.jpg')
rm_507_image = fit_to_window(rm_507_image)
rm_508_image = pygame.image.load('assets/rm_508.jpg')
rm_508_image = fit_to_window(rm_508_image)
rm_509_image = pygame.image.load('assets/rm_509.jpg')
rm_509_image = fit_to_window(rm_509_image)
rm_510_image = pygame.image.load('assets/rm_510.jpg')
rm_510_image = fit_to_window(rm_510_image)
rm_511_image = pygame.image.load('assets/rm_511.jpg')
rm_511_image = fit_to_window(rm_511_image)
rm_512_image = pygame.image.load('assets/rm_512.jpg')
rm_512_image = fit_to_window(rm_512_image)
rm_514_image = pygame.image.load('assets/rm_514.jpg')
rm_514_image = fit_to_window(rm_514_image)
rm_515_image = pygame.image.load('assets/rm_515.jpg')
rm_515_image = fit_to_window(rm_515_image)
rm_516_image = pygame.image.load('assets/rm_516.jpg')
rm_516_image = fit_to_window(rm_516_image)
rm_517_image = pygame.image.load('assets/rm_517.jpg')
rm_517_image = fit_to_window(rm_517_image)
RR_yellow_image = pygame.image.load('assets/601.jpg')
RR_yellow_image = fit_to_window(RR_yellow_image)
# Yellow
# Blue
rm_905_image = pygame.image.load('assets/601 Entrance.jpg')
rm_905_image = fit_to_window(rm_905_image)
rm_904_image = pygame.image.load('assets/601 Entrance.jpg')
rm_904_image = fit_to_window(rm_904_image)
tennis_courts_image = pygame.image.load('assets/601 Entrance.jpg')
tennis_courts_image = fit_to_window(tennis_courts_image)
lemon_parking_lot_image = pygame.image.load('assets/601 Entrance.jpg')
lemon_parking_lot_image = fit_to_window(lemon_parking_lot_image)
lawn_image = pygame.image.load('assets/601 Entrance.jpg')
lawn_image = fit_to_window(lawn_image)
media_center_image = pygame.image.load('assets/601 Entrance.jpg')
media_center_image = fit_to_window(media_center_image)
senate_room_image = pygame.image.load('assets/601 Entrance.jpg')
senate_room_image = fit_to_window(senate_room_image)
mc4_image = pygame.image.load('assets/601 Entrance.jpg')
mc4_image = fit_to_window(mc4_image)
mc3_image = pygame.image.load('assets/601 Entrance.jpg')
mc3_image = fit_to_window(mc3_image)
mc2_image = pygame.image.load('assets/601 Entrance.jpg')
mc2_image = fit_to_window(mc2_image)
mc1_image = pygame.image.load('assets/601 Entrance.jpg')
mc1_image = fit_to_window(mc1_image)
conf_rm_2_image = pygame.image.load('assets/601.jpg')
conf_rm_2_image = fit_to_window(conf_rm_2_image)
# Blue
# Orange
principal_office = pygame.image.load('assets/principal_s_office.jpg')
principal_office = fit_to_window(principal_office)
nurse = pygame.image.load('assets/nurse_s_office.jpg')
nurse = fit_to_window(nurse)
registrar = pygame.image.load('assets/601.jpg')
registrar = fit_to_window(registrar)
conference_room = pygame.image.load('assets/conference_room.jpg')
conference_room = fit_to_window(conference_room)
rm_311 = pygame.image.load('assets/311_staff_entrance.jpg')
rm_311 = fit_to_window(rm_311)
attendance_office = pygame.image.load('assets/attendance_office_inner_entrance.jpg')
attendance_office = fit_to_window(attendance_office)
rm_310 = pygame.image.load('assets/rm_310.jpg')
rm_310 = fit_to_window(rm_310)
ccc = pygame.image.load('assets/counseling_office.jpg')
ccc = fit_to_window(ccc)
rm_304 = pygame.image.load('assets/rm_304.jpg')
rm_304 = fit_to_window(rm_304)
rr_orange = pygame.image.load('assets/601.jpg')
rr_orange = fit_to_window(rr_orange)
rm_309 = pygame.image.load('assets/601.jpg')
rm_309 = fit_to_window(rm_309)
rm_308 = pygame.image.load('assets/601.jpg')
rm_308 = fit_to_window(rm_308)
rm_305 = pygame.image.load('assets/rm_305.jpg')
rm_305 = fit_to_window(rm_305)
rm_306 = pygame.image.load('assets/rm_306.jpg')
rm_306 = fit_to_window(rm_306)
rm_307 = pygame.image.load('assets/rm_307.jpg')
rm_307 = fit_to_window(rm_307)
ad_office_image = pygame.image.load('assets/601.jpg')
ad_office_image = fit_to_window(ad_office_image)
admin_offices_image = pygame.image.load('assets/601.jpg')
admin_offices_image = fit_to_window(admin_offices_image)
school_psych_image = pygame.image.load('assets/601.jpg')
school_psych_image = fit_to_window(school_psych_image)
storage_image = pygame.image.load('assets/601.jpg')
storage_image = fit_to_window(storage_image)
lunch = pygame.image.load('assets/601.jpg')
lunch = fit_to_window(lunch)
# Orange
# Brown
rm_101_image = pygame.image.load('assets/rm_101.jpg')
rm_101_image = fit_to_window(rm_101_image)
rm_102_image = pygame.image.load('assets/rm_102.jpg')
rm_102_image = fit_to_window(rm_102_image)
rm_103_image = pygame.image.load('assets/rm_103.jpg')
rm_103_image = fit_to_window(rm_103_image)
rm_104_image = pygame.image.load('assets/rm_104.jpg')
rm_104_image = fit_to_window(rm_104_image)
rm_105_image = pygame.image.load('assets/rm_105.jpg')
rm_105_image = fit_to_window(rm_105_image)
rm_106_image = pygame.image.load('assets/rm_106.jpg')
rm_106_image = fit_to_window(rm_106_image)
rm_107_image = pygame.image.load('assets/rm_107.jpg')
rm_107_image = fit_to_window(rm_107_image)
rm_201_image = pygame.image.load('assets/rm_201.jpg')
rm_201_image = fit_to_window(rm_201_image)
rm_202_image = pygame.image.load('assets/rm_202.jpg')
rm_202_image = fit_to_window(rm_202_image)
rm_203_image = pygame.image.load('assets/rm_203.jpg')
rm_203_image = fit_to_window(rm_203_image)
rm_204_image = pygame.image.load('assets/rm_204.jpg')
rm_204_image = fit_to_window(rm_204_image)
rm_205_image = pygame.image.load('assets/rm_205.jpg')
rm_205_image = fit_to_window(rm_205_image)
rm_206_image = pygame.image.load('assets/rm_206.jpg')
rm_206_image = fit_to_window(rm_206_image)
rm_207_image = pygame.image.load('assets/rm_207.jpg')
rm_207_image = fit_to_window(rm_207_image)
rm_804_image = pygame.image.load('assets/rm_804.jpg')
rm_804_image = fit_to_window(rm_804_image)
rm_803_image = pygame.image.load('assets/601.jpg')
rm_803_image = fit_to_window(rm_803_image)
locker_image = pygame.image.load('assets/locker.jpg')
locker_image = fit_to_window(locker_image)
pool_image = pygame.image.load('assets/OutsidePool2.jpg')
pool_image = fit_to_window(pool_image)
# Brown

# Create current screen variable
current_screen = map

# Create a surface for the button
# Red
rm_601_button_surface = pygame.Surface((117, 154), pygame.SRCALPHA)
staff_lounge_button_surface = pygame.Surface((117, 101), pygame.SRCALPHA)
rm_216_button_surface = pygame.Surface((58, 34), pygame.SRCALPHA)
rm_215_button_surface = pygame.Surface((53, 34), pygame.SRCALPHA)
rm_214_button_surface = pygame.Surface((54, 34), pygame.SRCALPHA)
RR_1_button_surface = pygame.Surface((54, 34), pygame.SRCALPHA)
rm_116_button_surface = pygame.Surface((58, 34), pygame.SRCALPHA)
rm_115_button_surface = pygame.Surface((53, 34), pygame.SRCALPHA)
rm_114_button_surface = pygame.Surface((54, 34), pygame.SRCALPHA)
RR_2_button_surface = pygame.Surface((54, 34), pygame.SRCALPHA)
rm_213_button_surface = pygame.Surface((58, 34), pygame.SRCALPHA)
rm_113_button_surface = pygame.Surface((58, 33), pygame.SRCALPHA)
rm_108_button_surface = pygame.Surface((58, 34), pygame.SRCALPHA)
rm_208_button_surface = pygame.Surface((58, 33), pygame.SRCALPHA)
rm_212_button_surface = pygame.Surface((59, 34), pygame.SRCALPHA)
rm_211_button_surface = pygame.Surface((54, 34), pygame.SRCALPHA)
rm_210_button_surface = pygame.Surface((55, 34), pygame.SRCALPHA)
rm_209_button_surface = pygame.Surface((57, 34), pygame.SRCALPHA)
RR_3_button_surface = pygame.Surface((49, 34), pygame.SRCALPHA)
rm_112_button_surface = pygame.Surface((59, 34), pygame.SRCALPHA)
rm_111_button_surface = pygame.Surface((54, 34), pygame.SRCALPHA)
rm_110_button_surface = pygame.Surface((55, 34), pygame.SRCALPHA)
rm_109_button_surface = pygame.Surface((57, 34), pygame.SRCALPHA)
RR_4_button_surface = pygame.Surface((49, 34), pygame.SRCALPHA)
# Red
# Purple
RR_400_button_surface = pygame.Surface((39, 16), pygame.SRCALPHA)
rm_401_button_surface = pygame.Surface((39, 47), pygame.SRCALPHA)
rm_402_button_surface = pygame.Surface((39, 55), pygame.SRCALPHA)
rm_403_button_surface = pygame.Surface((39, 53), pygame.SRCALPHA)
rm_404_button_surface = pygame.Surface((39, 56), pygame.SRCALPHA)
rm_405_button_surface = pygame.Surface((38, 56), pygame.SRCALPHA)
rm_406_button_surface = pygame.Surface((38, 53), pygame.SRCALPHA)
rm_407_button_surface = pygame.Surface((38, 55), pygame.SRCALPHA)
rm_408_button_surface = pygame.Surface((38, 47), pygame.SRCALPHA)
rm_409_button_surface = pygame.Surface((38, 47), pygame.SRCALPHA)
# Purple
# Green
gym_button_surface = pygame.Surface((115, 94), pygame.SRCALPHA)
tennis_button_surface = pygame.Surface((39, 85), pygame.SRCALPHA)
circle_button_surface = pygame.Surface((50, 37), pygame.SRCALPHA)
rm_702_button_surface = pygame.Surface((65, 85), pygame.SRCALPHA)
rm_703_button_surface = pygame.Surface((49, 85), pygame.SRCALPHA)
rm_705_button_surface = pygame.Surface((26, 85), pygame.SRCALPHA)
rm_704_button_surface = pygame.Surface((27, 85), pygame.SRCALPHA)
rm_706_button_surface = pygame.Surface((22, 29), pygame.SRCALPHA)
rm_707_button_surface = pygame.Surface((22, 28), pygame.SRCALPHA)
rm_708_button_surface = pygame.Surface((22, 28), pygame.SRCALPHA)
rm_709_button_surface = pygame.Surface((26, 23), pygame.SRCALPHA)
rm_801_button_surface = pygame.Surface((22, 24), pygame.SRCALPHA)
rm_802_button_surface = pygame.Surface((22, 24), pygame.SRCALPHA)
rr_1_button_surface = pygame.Surface((22, 36), pygame.SRCALPHA)
weight_button_surface = pygame.Surface((62, 100), pygame.SRCALPHA)
# Green
# Yellow
rm_501_button_surface = pygame.Surface((37, 30), pygame.SRCALPHA)
rm_502_button_surface = pygame.Surface((38, 33), pygame.SRCALPHA)
rm_503_button_surface = pygame.Surface((38, 26), pygame.SRCALPHA)
rm_504_button_surface = pygame.Surface((38, 27), pygame.SRCALPHA)
rm_505_button_surface = pygame.Surface((38, 35), pygame.SRCALPHA)
rm_506_button_surface = pygame.Surface((38, 35), pygame.SRCALPHA)
rm_507_button_surface = pygame.Surface((37, 38), pygame.SRCALPHA)
rm_508_button_surface = pygame.Surface((40, 38), pygame.SRCALPHA)
rm_509_button_surface = pygame.Surface((39, 35), pygame.SRCALPHA)
rm_510_button_surface = pygame.Surface((39, 35), pygame.SRCALPHA)
rm_511_button_surface = pygame.Surface((39, 27), pygame.SRCALPHA)
rm_512_button_surface = pygame.Surface((39, 26), pygame.SRCALPHA)
rm_514_button_surface = pygame.Surface((39, 33), pygame.SRCALPHA)
rm_515_button_surface = pygame.Surface((39, 30), pygame.SRCALPHA)
rm_516_button_surface = pygame.Surface((39, 47), pygame.SRCALPHA)
rm_517_button_surface = pygame.Surface((37, 47), pygame.SRCALPHA)
RR_yellow_button_surface = pygame.Surface((38, 12), pygame.SRCALPHA)
# Yellow
# Blue
rm_905_button_surface = pygame.Surface((75, 85), pygame.SRCALPHA)
rm_904_button_surface = pygame.Surface((76, 85), pygame.SRCALPHA)
tennis_courts_button_surface = pygame.Surface((127, 231), pygame.SRCALPHA)
lemon_parking_lot_button_surface = pygame.Surface((126, 231), pygame.SRCALPHA)
lawn_button_surface = pygame.Surface((151, 210), pygame.SRCALPHA)
media_center_button_surface = pygame.Surface((123, 74), pygame.SRCALPHA)
senate_room_button_surface = pygame.Surface((41, 34), pygame.SRCALPHA)
mc1_button_surface = pygame.Surface((30, 14), pygame.SRCALPHA)
conf_rm_2_button_surface = pygame.Surface((58, 27), pygame.SRCALPHA)
mc2_button_surface = pygame.Surface((30, 14), pygame.SRCALPHA)
mc3_button_surface = pygame.Surface((30, 14), pygame.SRCALPHA)
mc4_button_surface = pygame.Surface((30, 14), pygame.SRCALPHA)
# Blue
# Orange
PO_button_surface = pygame.Surface((35, 28), pygame.SRCALPHA)
nurse_button_surface = pygame.Surface((31, 18), pygame.SRCALPHA)
rgr_button_surface = pygame.Surface((38, 40), pygame.SRCALPHA)
conf_button_surface = pygame.Surface((36, 49), pygame.SRCALPHA)
rm_311_button_surface = pygame.Surface((81, 37), pygame.SRCALPHA)
attendance_button_surface = pygame.Surface((68, 48), pygame.SRCALPHA)
rm_310_button_surface = pygame.Surface((143, 38), pygame.SRCALPHA)
ccc_button_surface = pygame.Surface((119, 40), pygame.SRCALPHA)
rm_304_button_surface = pygame.Surface((26, 39), pygame.SRCALPHA)
rr_orange_button_surface = pygame.Surface((32, 38), pygame.SRCALPHA)
rm_309_button_surface = pygame.Surface((57, 38), pygame.SRCALPHA)
rm_308_button_surface = pygame.Surface((77, 39), pygame.SRCALPHA)
rm_305_button_surface = pygame.Surface((41, 38), pygame.SRCALPHA)
rm_306_button_surface = pygame.Surface((42, 38), pygame.SRCALPHA)
rm_307_button_surface = pygame.Surface((49, 38), pygame.SRCALPHA)
ad_office_button_surface = pygame.Surface((18, 17), pygame.SRCALPHA)
admin_offices_button_surface = pygame.Surface((60, 24), pygame.SRCALPHA)
school_psych_button_surface = pygame.Surface((18, 16), pygame.SRCALPHA)
storage_button_surface = pygame.Surface((32, 38), pygame.SRCALPHA)
lunch_button_surface = pygame.Surface((74, 50), pygame.SRCALPHA)
# Orange
# Brown
pool_button_surface = pygame.Surface((62, 68), pygame.SRCALPHA)
rm_804_button_surface = pygame.Surface((19, 55), pygame.SRCALPHA)
rm_803_button_surface = pygame.Surface((19, 55), pygame.SRCALPHA)
locker_rooms_button_surface = pygame.Surface((20, 110), pygame.SRCALPHA)
rm_207_button_surface = pygame.Surface((59, 34), pygame.SRCALPHA)
rm_206_button_surface = pygame.Surface((54, 34), pygame.SRCALPHA)
rm_205_button_surface = pygame.Surface((55, 34), pygame.SRCALPHA)
rm_204_button_surface = pygame.Surface((53, 34), pygame.SRCALPHA)
rm_203_button_surface = pygame.Surface((52, 34), pygame.SRCALPHA)
rm_202_button_surface = pygame.Surface((55, 34), pygame.SRCALPHA)
rm_201_button_surface = pygame.Surface((60, 34), pygame.SRCALPHA)
rm_107_button_surface = pygame.Surface((59, 34), pygame.SRCALPHA)
rm_106_button_surface = pygame.Surface((54, 34), pygame.SRCALPHA)
rm_105_button_surface = pygame.Surface((55, 34), pygame.SRCALPHA)
rm_104_button_surface = pygame.Surface((53, 34), pygame.SRCALPHA)
rm_103_button_surface = pygame.Surface((52, 34), pygame.SRCALPHA)
rm_102_button_surface = pygame.Surface((55, 34), pygame.SRCALPHA)
rm_101_button_surface = pygame.Surface((60, 34), pygame.SRCALPHA)
# Brown
# Back
back_button_surface = pygame.Surface((170, 46), pygame.SRCALPHA)
# Back

# Render text on the button

# Red
rm_601_text = render_label("601", rm_601_button_surface)
rm_601_text_rect = rm_601_text.get_rect(
 center=(rm_601_button_surface.get_width() / 2, rm_601_button_surface.get_height() / 2))

staff_lounge_text = render_label("Cafeteria & Staff Lounge", staff_lounge_button_surface)
staff_lounge_text_rect = staff_lounge_text.get_rect(
 center=(staff_lounge_button_surface.get_width() / 2, staff_lounge_button_surface.get_height() / 2))

rm_216_text = render_label("216", rm_216_button_surface)
rm_216_text_rect = rm_216_text.get_rect(
 center=(rm_216_button_surface.get_width() / 2, rm_216_button_surface.get_height() / 2))

rm_215_text = render_label("215", rm_215_button_surface)
rm_215_text_rect = rm_215_text.get_rect(
 center=(rm_215_button_surface.get_width() / 2, rm_215_button_surface.get_height() / 2))

rm_214_text = render_label("214", rm_214_button_surface)
rm_214_text_rect = rm_214_text.get_rect(
 center=(rm_214_button_surface.get_width() / 2, rm_214_button_surface.get_height() / 2))

RR_1_text = render_label("RR", RR_1_button_surface)
RR_1_text_rect = RR_1_text.get_rect(
 center=(RR_1_button_surface.get_width() / 2, RR_1_button_surface.get_height() / 2))

rm_116_text = render_label("116", rm_116_button_surface)
rm_116_text_rect = rm_116_text.get_rect(
 center=(rm_116_button_surface.get_width() / 2, rm_116_button_surface.get_height() / 2))

rm_115_text = render_label("115", rm_115_button_surface)
rm_115_text_rect = rm_115_text.get_rect(
 center=(rm_115_button_surface.get_width() / 2, rm_115_button_surface.get_height() / 2))

rm_114_text = render_label("114", rm_114_button_surface)
rm_114_text_rect = rm_114_text.get_rect(
 center=(rm_114_button_surface.get_width() / 2, rm_114_button_surface.get_height() / 2))

RR_2_text = render_label("RR", RR_2_button_surface)
RR_2_text_rect = RR_2_text.get_rect(
 center=(RR_2_button_surface.get_width() / 2, RR_2_button_surface.get_height() / 2))

rm_213_text = render_label("213", rm_213_button_surface)
rm_213_text_rect = rm_213_text.get_rect(
 center=(rm_213_button_surface.get_width() / 2, rm_213_button_surface.get_height() / 2))

rm_113_text = render_label("113", rm_113_button_surface)
rm_113_text_rect = rm_113_text.get_rect(
 center=(rm_113_button_surface.get_width() / 2, rm_113_button_surface.get_height() / 2))

rm_108_text = render_label("108", rm_108_button_surface)
rm_108_text_rect = rm_108_text.get_rect(
 center=(rm_108_button_surface.get_width() / 2, rm_108_button_surface.get_height() / 2))

rm_208_text = render_label("208", rm_208_button_surface)
rm_208_text_rect = rm_208_text.get_rect(
 center=(rm_208_button_surface.get_width() / 2, rm_208_button_surface.get_height() / 2))

rm_212_text = render_label("212", rm_212_button_surface)
rm_212_text_rect = rm_212_text.get_rect(
 center=(rm_212_button_surface.get_width() / 2, rm_212_button_surface.get_height() / 2))

rm_211_text = render_label("211", rm_211_button_surface)
rm_211_text_rect = rm_211_text.get_rect(
 center=(rm_211_button_surface.get_width() / 2, rm_211_button_surface.get_height() / 2))

rm_210_text = render_label("210", rm_210_button_surface)
rm_210_text_rect = rm_210_text.get_rect(
 center=(rm_210_button_surface.get_width() / 2, rm_210_button_surface.get_height() / 2))

rm_209_text = render_label("209", rm_209_button_surface)
rm_209_text_rect = rm_209_text.get_rect(
 center=(rm_209_button_surface.get_width() / 2, rm_209_button_surface.get_height() / 2))

RR_3_text = render_label("RR", RR_3_button_surface)
RR_3_text_rect = RR_3_text.get_rect(
 center=(RR_3_button_surface.get_width() / 2, RR_3_button_surface.get_height() / 2))

rm_112_text = render_label("112", rm_112_button_surface)
rm_112_text_rect = rm_112_text.get_rect(
 center=(rm_112_button_surface.get_width() / 2, rm_112_button_surface.get_height() / 2))

rm_111_text = render_label("111", rm_111_button_surface)
rm_111_text_rect = rm_111_text.get_rect(
 center=(rm_111_button_surface.get_width() / 2, rm_111_button_surface.get_height() / 2))

rm_110_text = render_label("110", rm_110_button_surface)
rm_110_text_rect = rm_110_text.get_rect(
 center=(rm_110_button_surface.get_width() / 2, rm_110_button_surface.get_height() / 2))

rm_109_text = render_label("109", rm_109_button_surface)
rm_109_text_rect = rm_109_text.get_rect(
 center=(rm_109_button_surface.get_width() / 2, rm_109_button_surface.get_height() / 2))

RR_4_text = render_label("RR", RR_4_button_surface)
RR_4_text_rect = RR_4_text.get_rect(
 center=(RR_4_button_surface.get_width() / 2, RR_4_button_surface.get_height() / 2))
# Red

# Purple
RR_400_text = render_label("RR", RR_400_button_surface)
RR_400_text_rect = RR_400_text.get_rect(
 center=(RR_400_button_surface.get_width() / 2, RR_400_button_surface.get_height() / 2))

rm_401_text = render_label("401", rm_401_button_surface)
rm_401_text_rect = rm_401_text.get_rect(
 center=(rm_401_button_surface.get_width() / 2, rm_401_button_surface.get_height() / 2))

rm_402_text = render_label("402", rm_402_button_surface)
rm_402_text_rect = rm_402_text.get_rect(
 center=(rm_402_button_surface.get_width() / 2, rm_402_button_surface.get_height() / 2))

rm_403_text = render_label("403", rm_403_button_surface)
rm_403_text_rect = rm_403_text.get_rect(
 center=(rm_403_button_surface.get_width() / 2, rm_403_button_surface.get_height() / 2))

rm_404_text = render_label("404", rm_404_button_surface)
rm_404_text_rect = rm_404_text.get_rect(
 center=(rm_404_button_surface.get_width() / 2, rm_404_button_surface.get_height() / 2))

rm_405_text = render_label("405", rm_405_button_surface)
rm_405_text_rect = rm_405_text.get_rect(
 center=(rm_405_button_surface.get_width() / 2, rm_405_button_surface.get_height() / 2))

rm_406_text = render_label("406", rm_406_button_surface)
rm_406_text_rect = rm_406_text.get_rect(
 center=(rm_406_button_surface.get_width() / 2, rm_406_button_surface.get_height() / 2))

rm_407_text = render_label("407", rm_407_button_surface)
rm_407_text_rect = rm_407_text.get_rect(
 center=(rm_407_button_surface.get_width() / 2, rm_407_button_surface.get_height() / 2))

rm_408_text = render_label("408", rm_408_button_surface)
rm_408_text_rect = rm_408_text.get_rect(
 center=(rm_408_button_surface.get_width() / 2, rm_408_button_surface.get_height() / 2))

rm_409_text = render_label("409", rm_409_button_surface)
rm_409_text_rect = rm_409_text.get_rect(
 center=(rm_409_button_surface.get_width() / 2, rm_409_button_surface.get_height() / 2))

# Purple

# Green
gym_text = render_label("Beckner Gym", gym_button_surface)
gym_text_rect = gym_text.get_rect(
 center=(gym_button_surface.get_width() / 2, gym_button_surface.get_height() / 2))

tennis_text = render_label("Tennis Courts", tennis_button_surface)
tennis_text_rect = tennis_text.get_rect(
 center=(tennis_button_surface.get_width() / 2, tennis_button_surface.get_height() / 2))

rm_702_text = render_label("702", rm_702_button_surface)
rm_702_text_rect = rm_702_text.get_rect(
 center=(rm_702_button_surface.get_width() / 2, rm_702_button_surface.get_height() / 2))

circle_text = render_label("Senior Circle", circle_button_surface)
circle_text_rect = circle_text.get_rect(
 center=(circle_button_surface.get_width() / 2, circle_button_surface.get_height() / 2))

rm_703_text = render_label("703", rm_703_button_surface)
rm_703_text_rect = rm_703_text.get_rect(
 center=(rm_703_button_surface.get_width() / 2, rm_703_button_surface.get_height() / 2))

rm_705_text = render_label("705", rm_705_button_surface)
rm_705_text_rect = rm_705_text.get_rect(
 center=(rm_705_button_surface.get_width() / 2, rm_705_button_surface.get_height() / 2))

rm_704_text = render_label("704", rm_704_button_surface)
rm_704_text_rect = rm_704_text.get_rect(
 center=(rm_704_button_surface.get_width() / 2, rm_704_button_surface.get_height() / 2))

rm_706_text = render_label("706", rm_706_button_surface)
rm_706_text_rect = rm_706_text.get_rect(
 center=(rm_706_button_surface.get_width() / 2, rm_706_button_surface.get_height() / 2))

rm_707_text = render_label("707", rm_707_button_surface)
rm_707_text_rect = rm_707_text.get_rect(
 center=(rm_707_button_surface.get_width() / 2, rm_707_button_surface.get_height() / 2))

rm_708_text = render_label("708", rm_708_button_surface)
rm_708_text_rect = rm_708_text.get_rect(
 center=(rm_708_button_surface.get_width() / 2, rm_708_button_surface.get_height() / 2))

rm_709_text = render_label("709", rm_709_button_surface)
rm_709_text_rect = rm_709_text.get_rect(
 center=(rm_709_button_surface.get_width() / 2, rm_709_button_surface.get_height() / 2))

rm_801_text = render_label("801", rm_801_button_surface)
rm_801_text_rect = rm_801_text.get_rect(
 center=(rm_801_button_surface.get_width() / 2, rm_801_button_surface.get_height() / 2))

rm_802_text = render_label("802", rm_802_button_surface)
rm_802_text_rect = rm_802_text.get_rect(
 center=(rm_802_button_surface.get_width() / 2, rm_802_button_surface.get_height() / 2))

rr_1_text = render_label("RR", rr_1_button_surface)
rr_1_text_rect = rr_1_text.get_rect(
 center=(rr_1_button_surface.get_width() / 2, rr_1_button_surface.get_height() / 2))

weight_text = render_label("Weight Room & Dance Studio 701", weight_button_surface)
weight_text_rect = weight_text.get_rect(
 center=(weight_button_surface.get_width() / 2, weight_button_surface.get_height() / 2))
# Green

# Yellow
rm_501_text = render_label("501", rm_501_button_surface)
rm_501_text_rect = rm_501_text.get_rect(
 center=(rm_501_button_surface.get_width() / 2, rm_501_button_surface.get_height() / 2))

rm_502_text = render_label("502", rm_502_button_surface)
rm_502_text_rect = rm_502_text.get_rect(
 center=(rm_502_button_surface.get_width() / 2, rm_502_button_surface.get_height() / 2))

rm_503_text = render_label("503", rm_503_button_surface)
rm_503_text_rect = rm_503_text.get_rect(
 center=(rm_503_button_surface.get_width() / 2, rm_503_button_surface.get_height() / 2))

rm_504_text = render_label("504", rm_504_button_surface)
rm_504_text_rect = rm_504_text.get_rect(
 center=(rm_504_button_surface.get_width() / 2, rm_504_button_surface.get_height() / 2))

rm_505_text = render_label("505", rm_505_button_surface)
rm_505_text_rect = rm_505_text.get_rect(
 center=(rm_505_button_surface.get_width() / 2, rm_505_button_surface.get_height() / 2))

rm_506_text = render_label("506", rm_506_button_surface)
rm_506_text_rect = rm_506_text.get_rect(
 center=(rm_506_button_surface.get_width() / 2, rm_506_button_surface.get_height() / 2))

rm_507_text = render_label("507", rm_507_button_surface)
rm_507_text_rect = rm_507_text.get_rect(
 center=(rm_507_button_surface.get_width() / 2, rm_507_button_surface.get_height() / 2))

rm_508_text = render_label("508", rm_508_button_surface)
rm_508_text_rect = rm_508_text.get_rect(
 center=(rm_508_button_surface.get_width() / 2, rm_508_button_surface.get_height() / 2))

rm_509_text = render_label("509", rm_509_button_surface)
rm_509_text_rect = rm_509_text.get_rect(
 center=(rm_509_button_surface.get_width() / 2, rm_509_button_surface.get_height() / 2))

rm_510_text = render_label("510", rm_510_button_surface)
rm_510_text_rect = rm_510_text.get_rect(
 center=(rm_510_button_surface.get_width() / 2, rm_510_button_surface.get_height() / 2))

rm_511_text = render_label("511", rm_511_button_surface)
rm_511_text_rect = rm_511_text.get_rect(
 center=(rm_511_button_surface.get_width() / 2, rm_511_button_surface.get_height() / 2))

rm_512_text = render_label("512", rm_512_button_surface)
rm_512_text_rect = rm_512_text.get_rect(
 center=(rm_512_button_surface.get_width() / 2, rm_512_button_surface.get_height() / 2))

rm_514_text = render_label("514", rm_514_button_surface)
rm_514_text_rect = rm_514_text.get_rect(
 center=(rm_514_button_surface.get_width() / 2, rm_514_button_surface.get_height() / 2))

rm_515_text = render_label("515", rm_515_button_surface)
rm_515_text_rect = rm_515_text.get_rect(
 center=(rm_515_button_surface.get_width() / 2, rm_515_button_surface.get_height() / 2))

rm_516_text = render_label("516", rm_516_button_surface)
rm_516_text_rect = rm_516_text.get_rect(
 center=(rm_516_button_surface.get_width() / 2, rm_516_button_surface.get_height() / 2))

rm_517_text = render_label("517", rm_517_button_surface)
rm_517_text_rect = rm_517_text.get_rect(
 center=(rm_517_button_surface.get_width() / 2, rm_517_button_surface.get_height() / 2))

RR_yellow_text = render_label("RR", RR_yellow_button_surface)
RR_yellow_text_rect = RR_yellow_text.get_rect(
 center=(RR_yellow_button_surface.get_width() / 2, RR_yellow_button_surface.get_height() / 2))
# Yellow

# Blue
rm_905_text = render_label("905", rm_905_button_surface)
rm_905_text_rect = rm_905_text.get_rect(
 center=(rm_905_button_surface.get_width() / 2, rm_905_button_surface.get_height() / 2))

rm_904_text = render_label("904", rm_904_button_surface)
rm_904_text_rect = rm_904_text.get_rect(
 center=(rm_904_button_surface.get_width() / 2, rm_904_button_surface.get_height() / 2))

tennis_courts_text = render_label("Tennis Courts", tennis_courts_button_surface)
tennis_courts_text_rect = tennis_courts_text.get_rect(
 center=(tennis_courts_button_surface.get_width() / 2, tennis_courts_button_surface.get_height() / 2))

lemon_parking_lot_text = render_label("Lemon Parking Lot", lemon_parking_lot_button_surface)
lemon_parking_lot_text_rect = lemon_parking_lot_text.get_rect(
 center=(lemon_parking_lot_button_surface.get_width() / 2, lemon_parking_lot_button_surface.get_height() / 2))

lawn_text = render_label("Lawn", lawn_button_surface)
lawn_text_rect = lawn_text.get_rect(
 center=(lawn_button_surface.get_width() / 2, lawn_button_surface.get_height() / 2))

media_center_text = render_label("Media Center", media_center_button_surface)
media_center_text_rect = media_center_text.get_rect(
 center=(media_center_button_surface.get_width() / 2, media_center_button_surface.get_height() / 2))

senate_room_text = render_label("Senate Room", senate_room_button_surface)
senate_room_text_rect = senate_room_text.get_rect(
 center=(senate_room_button_surface.get_width() / 2, senate_room_button_surface.get_height() / 2))

mc1_text = render_label("MC1", mc1_button_surface)
mc1_text_rect = mc1_text.get_rect(
 center=(mc1_button_surface.get_width() / 2, mc1_button_surface.get_height() / 2))
conf_rm_2_text = render_label("Conference Rm 2", conf_rm_2_button_surface)
conf_rm_2_text_rect = conf_rm_2_text.get_rect(
 center=(conf_rm_2_button_surface.get_width() / 2, conf_rm_2_button_surface.get_height() / 2))

mc2_text = render_label("MC2", mc2_button_surface)
mc2_text_rect = mc2_text.get_rect(
 center=(mc2_button_surface.get_width() / 2, mc2_button_surface.get_height() / 2))

mc3_text = render_label("MC3", mc3_button_surface)
mc3_text_rect = mc3_text.get_rect(
 center=(mc3_button_surface.get_width() / 2, mc3_button_surface.get_height() / 2))

mc4_text = render_label("MC4", mc4_button_surface)
mc4_text_rect = mc4_text.get_rect(
 center=(mc4_button_surface.get_width() / 2, mc4_button_surface.get_height() / 2))
# Blue

# Orange
PO_text = render_label("Principal's Office", PO_button_surface)
PO_text_rect = PO_text.get_rect(
 center=(PO_button_surface.get_width() / 2, PO_button_surface.get_height() / 2))

conf_text = render_label("Conf Room", conf_button_surface)
conf_text_rect = conf_text.get_rect(
 center=(conf_button_surface.get_width() / 2, conf_button_surface.get_height() / 2))

nurse_text = render_label("Nurse", nurse_button_surface)
nurse_text_rect = nurse_text.get_rect(
 center=(nurse_button_surface.get_width() / 2, nurse_button_surface.get_height() / 2))

rgr_text = render_label("Registrar", rgr_button_surface)
rgr_text_rect = rgr_text.get_rect(
 center=(rgr_button_surface.get_width() / 2, rgr_button_surface.get_height() / 2))

attendance_text = render_label("Main Office & Attendance", attendance_button_surface)
attendance_text_rect = attendance_text.get_rect(
 center=(attendance_button_surface.get_width() / 2, attendance_button_surface.get_height() / 2))

rm_311_text = render_label("311", rm_311_button_surface)
rm_311_text_rect = rm_311_text.get_rect(
 center=(rm_311_button_surface.get_width() / 2, rm_311_button_surface.get_height() / 2))

rm_310_text = render_label("310", rm_310_button_surface)
rm_310_text_rect = rm_310_text.get_rect(
 center=(rm_310_button_surface.get_width() / 2, rm_310_button_surface.get_height() / 2))

ccc_text = render_label("Counseling College & Career", ccc_button_surface)
ccc_text_rect = ccc_text.get_rect(
 center=(ccc_button_surface.get_width() / 2, ccc_button_surface.get_height() / 2))

rm_304_text = render_label("304", rm_304_button_surface, subtitle="Mental Fitness Ctr")
rm_304_text_rect = rm_304_text.get_rect(
 center=(rm_304_button_surface.get_width() / 2, rm_304_button_surface.get_height() / 2))

rr_orange_text = render_label("RR", rr_orange_button_surface)
rr_orange_text_rect = rr_orange_text.get_rect(
 center=(rr_orange_button_surface.get_width() / 2, rr_orange_button_surface.get_height() / 2))

rm_309_text = render_label("309", rm_309_button_surface)
rm_309_text_rect = rm_309_text.get_rect(
 center=(rm_309_button_surface.get_width() / 2, rm_309_button_surface.get_height() / 2))

rm_308_text = render_label("308", rm_308_button_surface)
rm_308_text_rect = rm_308_text.get_rect(
 center=(rm_308_button_surface.get_width() / 2, rm_308_button_surface.get_height() / 2))

rm_305_text = render_label("305", rm_305_button_surface, subtitle="DIS Counselor")
rm_305_text_rect = rm_305_text.get_rect(
 center=(rm_305_button_surface.get_width() / 2, rm_305_button_surface.get_height() / 2))

rm_306_text = render_label("306", rm_306_button_surface)
rm_306_text_rect = rm_306_text.get_rect(
 center=(rm_306_button_surface.get_width() / 2, rm_306_button_surface.get_height() / 2))

rm_307_text = render_label("307", rm_307_button_surface, subtitle="School Psych")
rm_307_text_rect = rm_307_text.get_rect(
 center=(rm_307_button_surface.get_width() / 2, rm_307_button_surface.get_height() / 2))
ad_office_text = render_label("AD Office", ad_office_button_surface)
ad_office_text_rect = ad_office_text.get_rect(
 center=(ad_office_button_surface.get_width() / 2, ad_office_button_surface.get_height() / 2))
admin_offices_text = render_label("Administrative Offices", admin_offices_button_surface)
admin_offices_text_rect = admin_offices_text.get_rect(
 center=(admin_offices_button_surface.get_width() / 2, admin_offices_button_surface.get_height() / 2))
school_psych_text = render_label("School Psych", school_psych_button_surface)
school_psych_text_rect = school_psych_text.get_rect(
 center=(school_psych_button_surface.get_width() / 2, school_psych_button_surface.get_height() / 2))
storage_text = render_label("Storage", storage_button_surface)
storage_text_rect = storage_text.get_rect(
 center=(storage_button_surface.get_width() / 2, storage_button_surface.get_height() / 2))

lunch_text = render_label("Lunch Shelter", lunch_button_surface)
lunch_text_rect = lunch_text.get_rect(
 center=(lunch_button_surface.get_width() / 2, lunch_button_surface.get_height() / 2))
# Orange

# Brown
pool_button_text = render_label("Pool", pool_button_surface)
pool_button_text_rect = pool_button_text.get_rect(
 center=(pool_button_surface.get_width() / 2, pool_button_surface.get_height() / 2))

rm_804_button_text = render_label("804", rm_804_button_surface)
rm_804_button_text_rect = rm_804_button_text.get_rect(
 center=(rm_804_button_surface.get_width() / 2, rm_804_button_surface.get_height() / 2))

rm_803_button_text = render_label("803", rm_803_button_surface)
rm_803_button_text_rect = rm_803_button_text.get_rect(
 center=(rm_803_button_surface.get_width() / 2, rm_803_button_surface.get_height() / 2))

locker_rooms_button_text = render_label("Locker Rooms", locker_rooms_button_surface)
locker_rooms_button_text_rect = locker_rooms_button_text.get_rect(
 center=(locker_rooms_button_surface.get_width() / 2, locker_rooms_button_surface.get_height() / 2))

rm_207_button_text = render_label("207", rm_207_button_surface)
rm_207_button_text_rect = rm_207_button_text.get_rect(
 center=(rm_207_button_surface.get_width() / 2, rm_207_button_surface.get_height() / 2))

rm_206_button_text = render_label("206", rm_206_button_surface)
rm_206_button_text_rect = rm_206_button_text.get_rect(
 center=(rm_206_button_surface.get_width() / 2, rm_206_button_surface.get_height() / 2))

rm_205_button_text = render_label("205", rm_205_button_surface)
rm_205_button_text_rect = rm_205_button_text.get_rect(
 center=(rm_205_button_surface.get_width() / 2, rm_205_button_surface.get_height() / 2))

rm_204_button_text = render_label("204", rm_204_button_surface)
rm_204_button_text_rect = rm_204_button_text.get_rect(
 center=(rm_204_button_surface.get_width() / 2, rm_204_button_surface.get_height() / 2))

rm_203_button_text = render_label("203", rm_203_button_surface)
rm_203_button_text_rect = rm_203_button_text.get_rect(
 center=(rm_203_button_surface.get_width() / 2, rm_203_button_surface.get_height() / 2))

rm_202_button_text = render_label("202", rm_202_button_surface)
rm_202_button_text_rect = rm_202_button_text.get_rect(
 center=(rm_202_button_surface.get_width() / 2, rm_202_button_surface.get_height() / 2))

rm_201_button_text = render_label("201", rm_201_button_surface)
rm_201_button_text_rect = rm_201_button_text.get_rect(
 center=(rm_201_button_surface.get_width() / 2, rm_201_button_surface.get_height() / 2))

rm_107_button_text = render_label("107", rm_107_button_surface)
rm_107_button_text_rect = rm_107_button_text.get_rect(
 center=(rm_107_button_surface.get_width() / 2, rm_107_button_surface.get_height() / 2))

rm_106_button_text = render_label("106", rm_106_button_surface)
rm_106_button_text_rect = rm_106_button_text.get_rect(
 center=(rm_106_button_surface.get_width() / 2, rm_106_button_surface.get_height() / 2))

rm_105_button_text = render_label("105", rm_105_button_surface)
rm_105_button_text_rect = rm_105_button_text.get_rect(
 center=(rm_105_button_surface.get_width() / 2, rm_105_button_surface.get_height() / 2))

rm_104_button_text = render_label("104", rm_104_button_surface)
rm_104_button_text_rect = rm_104_button_text.get_rect(
 center=(rm_104_button_surface.get_width() / 2, rm_104_button_surface.get_height() / 2))

rm_103_button_text = render_label("103", rm_103_button_surface)
rm_103_button_text_rect = rm_103_button_text.get_rect(
 center=(rm_103_button_surface.get_width() / 2, rm_103_button_surface.get_height() / 2))

rm_102_button_text = render_label("102", rm_102_button_surface)
rm_102_button_text_rect = rm_102_button_text.get_rect(
 center=(rm_102_button_surface.get_width() / 2, rm_102_button_surface.get_height() / 2))

rm_101_button_text = render_label("101", rm_101_button_surface)
rm_101_button_text_rect = rm_101_button_text.get_rect(
 center=(rm_101_button_surface.get_width() / 2, rm_101_button_surface.get_height() / 2))
# Brown
#Back
back_button_text = render_label("←  Back to Map", back_button_surface, max_size=18)
back_button_text_rect = back_button_text.get_rect(
 center=(back_button_surface.get_width() / 2, back_button_surface.get_height() / 2))
#Back

# Create a pygame.Rect object that represents the button's boundaries
# Red
rm_601_button_rect = pygame.Rect(755, 338, 117, 154)
staff_lounge_button_rect = pygame.Rect(755, 235, 117, 101)
rm_216_button_rect = pygame.Rect(837, 646, 58, 34)
rm_215_button_rect = pygame.Rect(897, 646, 53, 34)
rm_214_button_rect = pygame.Rect(952, 646, 54, 34)
RR_1_button_rect = pygame.Rect(1007, 646, 54, 34)
rm_116_button_rect = pygame.Rect(837, 681, 58, 34)
rm_115_button_rect = pygame.Rect(897, 681, 53, 34)
rm_114_button_rect = pygame.Rect(952, 681, 54, 34)
RR_2_button_rect = pygame.Rect(1007, 681, 54, 34)
rm_213_button_rect = pygame.Rect(1121, 647, 58, 34)
rm_113_button_rect = pygame.Rect(1121, 683, 58, 33)
rm_108_button_rect = pygame.Rect(1121, 764, 58, 34)
rm_208_button_rect = pygame.Rect(1121, 729, 58, 33)
rm_212_button_rect = pygame.Rect(784, 728, 59, 34)
rm_211_button_rect = pygame.Rect(844, 728, 54, 34)
rm_210_button_rect = pygame.Rect(899, 728, 55, 34)
rm_209_button_rect = pygame.Rect(955, 728, 57, 34)
RR_3_button_rect = pygame.Rect(1013, 728, 49, 34)
rm_112_button_rect = pygame.Rect(784, 764, 59, 34)
rm_111_button_rect = pygame.Rect(844, 764, 54, 34)
rm_110_button_rect = pygame.Rect(899, 764, 55, 34)
rm_109_button_rect = pygame.Rect(955, 764, 57, 34)
RR_4_button_rect = pygame.Rect(1013, 764, 49, 34)
# Red
# Purple
RR_400_button_rect = pygame.Rect(1010, 389, 39, 16)
rm_401_button_rect = pygame.Rect(1010, 406, 39, 47)
rm_402_button_rect = pygame.Rect(1010, 313, 39, 55)
rm_403_button_rect = pygame.Rect(1010, 258, 39, 53)
rm_404_button_rect = pygame.Rect(1010, 201, 39, 56)
rm_405_button_rect = pygame.Rect(1050, 201, 38, 56)
rm_406_button_rect = pygame.Rect(1050, 258, 38, 53)
rm_407_button_rect = pygame.Rect(1050, 313, 38, 55)
rm_408_button_rect = pygame.Rect(1050, 406, 38, 47)
rm_409_button_rect = pygame.Rect(1050, 463, 38, 47)
# Purple
# Green
gym_button_rect = pygame.Rect(451, 385, 115, 94)
tennis_button_rect = pygame.Rect(438, 271, 39, 85)
rm_702_button_rect = pygame.Rect(490, 271, 65, 85)
circle_button_rect = pygame.Rect(632, 415, 59, 57)
rm_703_button_rect = pygame.Rect(556, 271, 49, 85)
rm_705_button_rect = pygame.Rect(634, 271, 26, 85)
rm_704_button_rect = pygame.Rect(606, 271, 27, 85)
rm_706_button_rect = pygame.Rect(661, 327, 22, 29)
rm_707_button_rect = pygame.Rect(661, 299, 22, 28)
rm_708_button_rect = pygame.Rect(661, 271, 22, 28)
rm_801_button_rect = pygame.Rect(569, 427, 22, 24)
rm_802_button_rect = pygame.Rect(569, 402, 22, 24)
rm_709_button_rect = pygame.Rect(634, 246, 26, 23)
rr_1_button_rect = pygame.Rect(661, 233, 22, 36)
weight_button_rect = pygame.Rect(489, 169, 62, 100)
# Green
# Yellow
rm_501_button_rect = pygame.Rect(1090, 423, 37, 30)
rm_502_button_rect = pygame.Rect(1090, 388, 38, 33)
rm_503_button_rect = pygame.Rect(1090, 342, 38, 26)
rm_504_button_rect = pygame.Rect(1090, 313, 38, 27)
rm_505_button_rect = pygame.Rect(1090, 276, 38, 35)
rm_506_button_rect = pygame.Rect(1090, 240, 38, 35)
rm_507_button_rect = pygame.Rect(1090, 201, 37, 38)
rm_508_button_rect = pygame.Rect(1128, 201, 40, 38)
rm_509_button_rect = pygame.Rect(1129, 240, 39, 35)
rm_510_button_rect = pygame.Rect(1129, 276, 39, 35)
rm_511_button_rect = pygame.Rect(1129, 313, 39, 27)
rm_512_button_rect = pygame.Rect(1129, 342, 39, 26)
rm_514_button_rect = pygame.Rect(1129, 388, 39, 33)
rm_515_button_rect = pygame.Rect(1129, 423, 39, 30)
rm_516_button_rect = pygame.Rect(1129, 463, 39, 47)
rm_517_button_rect = pygame.Rect(1090, 463, 37, 47)
RR_yellow_button_rect = pygame.Rect(1090, 369, 38, 12)
# Yellow
# Blue
rm_905_button_rect = pygame.Rect(408, 552, 75, 85)
rm_904_button_rect = pygame.Rect(483, 552, 76, 85)
tennis_courts_button_rect = pygame.Rect(158, 655, 127, 231)
lemon_parking_lot_button_rect = pygame.Rect(287, 655, 126, 231)
lawn_button_rect = pygame.Rect(427, 655, 151, 210)
media_center_button_rect = pygame.Rect(594, 810, 123, 74)
senate_room_button_rect = pygame.Rect(676, 658, 41, 34)
mc1_button_rect = pygame.Rect(594, 700, 30, 14)
conf_rm_2_button_rect = pygame.Rect(619, 713, 58, 27)
mc2_button_rect = pygame.Rect(594, 686, 30, 14)
mc3_button_rect = pygame.Rect(594, 672, 30, 14)
mc4_button_rect = pygame.Rect(594, 658, 30, 14)
# Blue
# Orange
PO_button_rect = pygame.Rect(615, 536, 35, 28)
nurse_button_rect = pygame.Rect(678, 537, 31, 18)
rgr_button_rect = pygame.Rect(754, 574, 38, 40)
conf_button_rect = pygame.Rect(615, 565, 36, 49)
attendance_button_rect = pygame.Rect(594, 760, 68, 48)
rm_311_button_rect = pygame.Rect(754, 536, 81, 37)
rm_310_button_rect = pygame.Rect(836, 536, 143, 38)
ccc_button_rect = pygame.Rect(833, 574, 119, 40)
rm_304_button_rect = pygame.Rect(953, 575, 26, 39)
rr_orange_button_rect = pygame.Rect(980, 536, 32, 38)
rm_309_button_rect = pygame.Rect(1034, 536, 57, 38)
rm_308_button_rect = pygame.Rect(1092, 536, 77, 39)
rm_305_button_rect = pygame.Rect(1034, 576, 41, 38)
rm_306_button_rect = pygame.Rect(1076, 576, 42, 38)
rm_307_button_rect = pygame.Rect(1120, 576, 49, 38)
ad_office_button_rect = pygame.Rect(710, 537, 18, 17)
admin_offices_button_rect = pygame.Rect(669, 590, 60, 24)
school_psych_button_rect = pygame.Rect(793, 598, 18, 16)
storage_button_rect = pygame.Rect(980, 575, 32, 38)
lunch_button_rect = pygame.Rect(899, 302, 74, 50)
# Orange
# Brown
pool_button_rect = pygame.Rect(292, 425, 62, 68)
rm_804_button_rect = pygame.Rect(404, 412, 19, 55)
rm_803_button_rect = pygame.Rect(404, 467, 19, 55)
locker_rooms_button_rect = pygame.Rect(383, 412, 20, 110)
rm_207_button_rect = pygame.Rect(784, 810, 59, 34)
rm_206_button_rect = pygame.Rect(844, 810, 54, 34)
rm_205_button_rect = pygame.Rect(899, 810, 55, 34)
rm_204_button_rect = pygame.Rect(955, 810, 53, 34)
rm_203_button_rect = pygame.Rect(1010, 810, 52, 34)
rm_202_button_rect = pygame.Rect(1063, 810, 55, 34)
rm_201_button_rect = pygame.Rect(1120, 810, 60, 34)
rm_107_button_rect = pygame.Rect(784, 846, 59, 34)
rm_106_button_rect = pygame.Rect(844, 846, 54, 34)
rm_105_button_rect = pygame.Rect(899, 846, 55, 34)
rm_104_button_rect = pygame.Rect(955, 846, 53, 34)
rm_103_button_rect = pygame.Rect(1010, 846, 52, 34)
rm_102_button_rect = pygame.Rect(1063, 846, 55, 34)
rm_101_button_rect = pygame.Rect(1120, 846, 60, 34)
# Brown
#Back
back_button_rect = pygame.Rect(24, 20, 170, 46)
#Back

# Create button hover effect function (to be called for each button)
hovered_label = None
def button_hover_effect(rect1, surface, color):
 global hovered_label
 hovered = rect1.collidepoint(pygame.mouse.get_pos())
 if hovered:
     hovered_label = labels.get(surface)
 box = surface.get_rect().inflate(-2, -2)
 radius = max(2, min(8, box.width // 4, box.height // 4))
 surface.fill((0, 0, 0, 0))
 pygame.draw.rect(surface, tint(color, 0.38 if hovered else 0.12), box, border_radius=radius)
 pygame.draw.rect(surface, color, box, 2 if hovered else 1, border_radius=radius)


# Caption shown over a room's photo, and the fade between screens
current_title = ''
shown_screen = None
fade_alpha = 0
fade_overlay = pygame.Surface((1240, 930))
fade_overlay.fill(LETTERBOX_COLOR)


# Start the main loop
while True:
 # Set the frame rate
 clock.tick(60)


 # Fill the display with color
 screen.fill((155, 255, 155))


 # Get events from the event queue
 for event in pygame.event.get():
     # Check for the quit event
     if event.type == pygame.QUIT:
         # Quit the game
         pygame.quit()
         sys.exit()

     # F11 switches fullscreen on and off; Esc leaves fullscreen
     if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_F11 or (event.key == pygame.K_ESCAPE and pygame.display.is_fullscreen()):
             pygame.display.toggle_fullscreen()

     # Check for the mouse button down event
     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
         if current_screen != map:
             if back_button_rect.collidepoint(event.pos):
                 current_screen = map
         # Red
         elif rm_601_button_rect.collidepoint(event.pos):
             current_screen = rm_601_image
         elif staff_lounge_button_rect.collidepoint(event.pos):
             current_screen = staff_lounge_image
         elif rm_216_button_rect.collidepoint(event.pos):
             current_screen = rm_216_image
         elif rm_215_button_rect.collidepoint(event.pos):
             current_screen = rm_215_image
         elif rm_214_button_rect.collidepoint(event.pos):
             current_screen = rm_214_image
         elif RR_1_button_rect.collidepoint(event.pos):
             current_screen = RR_1_image
         elif rm_116_button_rect.collidepoint(event.pos):
             current_screen = rm_116_image
         elif rm_115_button_rect.collidepoint(event.pos):
             current_screen = rm_115_image
         elif rm_114_button_rect.collidepoint(event.pos):
             current_screen = rm_114_image
         elif RR_2_button_rect.collidepoint(event.pos):
             current_screen = RR_2_image
         elif rm_213_button_rect.collidepoint(event.pos):
             current_screen = rm_213_image
         elif rm_113_button_rect.collidepoint(event.pos):
             current_screen = rm_113_image
         elif rm_108_button_rect.collidepoint(event.pos):
             current_screen = rm_108_image
         elif rm_208_button_rect.collidepoint(event.pos):
             current_screen = rm_208_image
         elif rm_212_button_rect.collidepoint(event.pos):
             current_screen = rm_212_image
         elif rm_211_button_rect.collidepoint(event.pos):
             current_screen = rm_211_image
         elif rm_210_button_rect.collidepoint(event.pos):
             current_screen = rm_210_image
         elif rm_209_button_rect.collidepoint(event.pos):
             current_screen = rm_209_image
         elif RR_3_button_rect.collidepoint(event.pos):
             current_screen = RR_3_image
         elif rm_112_button_rect.collidepoint(event.pos):
             current_screen = rm_112_image
         elif rm_111_button_rect.collidepoint(event.pos):
             current_screen = rm_111_image
         elif rm_110_button_rect.collidepoint(event.pos):
             current_screen = rm_110_image
         elif rm_109_button_rect.collidepoint(event.pos):
             current_screen = rm_109_image
         elif RR_4_button_rect.collidepoint(event.pos):
             current_screen = RR_4_image
         # Red
         # Purple
         elif RR_400_button_rect.collidepoint(event.pos):
             current_screen = RR_400_image
         elif rm_401_button_rect.collidepoint(event.pos):
             current_screen = rm_401_image
         elif rm_402_button_rect.collidepoint(event.pos):
             current_screen = rm_402_image
         elif rm_403_button_rect.collidepoint(event.pos):
             current_screen = rm_403_image
         elif rm_404_button_rect.collidepoint(event.pos):
             current_screen = rm_404_image
         elif rm_405_button_rect.collidepoint(event.pos):
             current_screen = rm_405_image
         elif rm_406_button_rect.collidepoint(event.pos):
             current_screen = rm_406_image
         elif rm_407_button_rect.collidepoint(event.pos):
             current_screen = rm_407_image
         elif rm_408_button_rect.collidepoint(event.pos):
             current_screen = rm_408_image
         elif rm_409_button_rect.collidepoint(event.pos):
             current_screen = rm_409_image
         # Purple
         # Green
         elif gym_button_rect.collidepoint(event.pos):
             current_screen = gym_image
         elif tennis_button_rect.collidepoint(event.pos):
             current_screen = tennis_image
         elif rm_702_button_rect.collidepoint(event.pos):
             current_screen = rm_702_image
         elif circle_button_rect.collidepoint(event.pos):
             current_screen = circle_image
         elif rm_703_button_rect.collidepoint(event.pos):
             current_screen = rm_703_image
         elif rm_705_button_rect.collidepoint(event.pos):
             current_screen = rm_705_image
         elif rm_704_button_rect.collidepoint(event.pos):
             current_screen = rm_704_image
         elif rm_706_button_rect.collidepoint(event.pos):
             current_screen = rm_706_image
         elif rm_707_button_rect.collidepoint(event.pos):
             current_screen = rm_707_image
         elif rm_708_button_rect.collidepoint(event.pos):
             current_screen = rm_708_image
         elif rm_709_button_rect.collidepoint(event.pos):
             current_screen = rm_709_image
         elif rm_801_button_rect.collidepoint(event.pos):
             current_screen = rm_801_image
         elif rm_802_button_rect.collidepoint(event.pos):
             current_screen = rm_802_image
         elif rr_1_button_rect.collidepoint(event.pos):
             current_screen = rr_1_image
         elif weight_button_rect.collidepoint(event.pos):
             current_screen = weight_image
         # Green
         # Yellow
         elif rm_501_button_rect.collidepoint(event.pos):
             current_screen = rm_501_image
         elif rm_502_button_rect.collidepoint(event.pos):
             current_screen = rm_502_image
         elif rm_503_button_rect.collidepoint(event.pos):
             current_screen = rm_503_image
         elif rm_504_button_rect.collidepoint(event.pos):
             current_screen = rm_504_image
         elif rm_505_button_rect.collidepoint(event.pos):
             current_screen = rm_505_image
         elif rm_506_button_rect.collidepoint(event.pos):
             current_screen = rm_506_image
         elif rm_507_button_rect.collidepoint(event.pos):
             current_screen = rm_507_image
         elif rm_508_button_rect.collidepoint(event.pos):
             current_screen = rm_508_image
         elif rm_509_button_rect.collidepoint(event.pos):
             current_screen = rm_509_image
         elif rm_510_button_rect.collidepoint(event.pos):
             current_screen = rm_510_image
         elif rm_511_button_rect.collidepoint(event.pos):
             current_screen = rm_511_image
         elif rm_512_button_rect.collidepoint(event.pos):
             current_screen = rm_512_image
         elif rm_514_button_rect.collidepoint(event.pos):
             current_screen = rm_514_image
         elif rm_515_button_rect.collidepoint(event.pos):
             current_screen = rm_515_image
         elif rm_516_button_rect.collidepoint(event.pos):
             current_screen = rm_516_image
         elif rm_517_button_rect.collidepoint(event.pos):
             current_screen = rm_517_image
         elif RR_yellow_button_rect.collidepoint(event.pos):
             current_screen = RR_yellow_image
         # Yellow
         # Blue
         elif rm_905_button_rect.collidepoint(event.pos):
             current_screen = rm_905_image
         elif rm_904_button_rect.collidepoint(event.pos):
             current_screen = rm_904_image
         elif tennis_courts_button_rect.collidepoint(event.pos):
             current_screen = tennis_courts_image
         elif lemon_parking_lot_button_rect.collidepoint(event.pos):
             current_screen = lemon_parking_lot_image
         elif lawn_button_rect.collidepoint(event.pos):
             current_screen = lawn_image
         elif media_center_button_rect.collidepoint(event.pos):
             current_screen = media_center_image
         elif senate_room_button_rect.collidepoint(event.pos):
             current_screen = senate_room_image
         elif mc1_button_rect.collidepoint(event.pos):
             current_screen = mc1_image
         elif conf_rm_2_button_rect.collidepoint(event.pos):
             current_screen = conf_rm_2_image
         elif mc2_button_rect.collidepoint(event.pos):
             current_screen = mc2_image
         elif mc3_button_rect.collidepoint(event.pos):
             current_screen = mc3_image
         elif mc4_button_rect.collidepoint(event.pos):
             current_screen = mc4_image
         # Blue
         # Orange
         elif PO_button_rect.collidepoint(event.pos):
             current_screen = principal_office
         elif nurse_button_rect.collidepoint(event.pos):
             current_screen = nurse
         elif rgr_button_rect.collidepoint(event.pos):
             current_screen = registrar
         elif conf_button_rect.collidepoint(event.pos):
             current_screen = conference_room
         elif rm_311_button_rect.collidepoint(event.pos):
             current_screen = rm_311
         elif attendance_button_rect.collidepoint(event.pos):
             current_screen = attendance_office
         elif rm_310_button_rect.collidepoint(event.pos):
             current_screen = rm_310
         elif ccc_button_rect.collidepoint(event.pos):
             current_screen = ccc
         elif rm_304_button_rect.collidepoint(event.pos):
             current_screen = rm_304
         elif rr_orange_button_rect.collidepoint(event.pos):
             current_screen = rr_orange
         elif rm_309_button_rect.collidepoint(event.pos):
             current_screen = rm_309
         elif rm_308_button_rect.collidepoint(event.pos):
             current_screen = rm_308
         elif rm_305_button_rect.collidepoint(event.pos):
             current_screen = rm_305
         elif rm_306_button_rect.collidepoint(event.pos):
             current_screen = rm_306
         elif rm_307_button_rect.collidepoint(event.pos):
             current_screen = rm_307
         elif ad_office_button_rect.collidepoint(event.pos):
             current_screen = ad_office_image
         elif admin_offices_button_rect.collidepoint(event.pos):
             current_screen = admin_offices_image
         elif school_psych_button_rect.collidepoint(event.pos):
             current_screen = school_psych_image
         elif storage_button_rect.collidepoint(event.pos):
             current_screen = storage_image
         elif lunch_button_rect.collidepoint(event.pos):
             current_screen = lunch
         # Orange
         # Brown
         elif pool_button_rect.collidepoint(event.pos):
             current_screen = pool_image
         elif rm_804_button_rect.collidepoint(event.pos):
             current_screen = rm_804_image
         elif rm_803_button_rect.collidepoint(event.pos):
             current_screen = rm_803_image
         elif locker_rooms_button_rect.collidepoint(event.pos):
             current_screen = locker_image
         elif rm_207_button_rect.collidepoint(event.pos):
             current_screen = rm_207_image
         elif rm_206_button_rect.collidepoint(event.pos):
             current_screen = rm_206_image
         elif rm_205_button_rect.collidepoint(event.pos):
             current_screen = rm_205_image
         elif rm_204_button_rect.collidepoint(event.pos):
             current_screen = rm_204_image
         elif rm_203_button_rect.collidepoint(event.pos):
             current_screen = rm_203_image
         elif rm_202_button_rect.collidepoint(event.pos):
             current_screen = rm_202_image
         elif rm_201_button_rect.collidepoint(event.pos):
             current_screen = rm_201_image
         elif rm_107_button_rect.collidepoint(event.pos):
             current_screen = rm_107_image
         elif rm_106_button_rect.collidepoint(event.pos):
             current_screen = rm_106_image
         elif rm_105_button_rect.collidepoint(event.pos):
             current_screen = rm_105_image
         elif rm_104_button_rect.collidepoint(event.pos):
             current_screen = rm_104_image
         elif rm_103_button_rect.collidepoint(event.pos):
             current_screen = rm_103_image
         elif rm_102_button_rect.collidepoint(event.pos):
             current_screen = rm_102_image
         elif rm_101_button_rect.collidepoint(event.pos):
             current_screen = rm_101_image
         # Brown
         if current_screen != map and current_screen != shown_screen:
             current_title = full_title(hovered_label or '')

 # Check if the mouse is over the button. This will create the button hover effect
 hovered_label = None
 if current_screen == map:
  # Red
  button_hover_effect(rm_601_button_rect, rm_601_button_surface, RED)
  button_hover_effect(staff_lounge_button_rect, staff_lounge_button_surface, RED)
  button_hover_effect(rm_216_button_rect, rm_216_button_surface, RED)
  button_hover_effect(rm_215_button_rect, rm_215_button_surface, RED)
  button_hover_effect(rm_214_button_rect, rm_214_button_surface, RED)
  button_hover_effect(RR_1_button_rect, RR_1_button_surface, RED)
  button_hover_effect(rm_116_button_rect, rm_116_button_surface, RED)
  button_hover_effect(rm_115_button_rect, rm_115_button_surface, RED)
  button_hover_effect(rm_114_button_rect, rm_114_button_surface, RED)
  button_hover_effect(RR_2_button_rect, RR_2_button_surface, RED)
  button_hover_effect(rm_213_button_rect, rm_213_button_surface, RED)
  button_hover_effect(rm_113_button_rect, rm_113_button_surface, RED)
  button_hover_effect(rm_108_button_rect, rm_108_button_surface, RED)
  button_hover_effect(rm_208_button_rect, rm_208_button_surface, RED)
  button_hover_effect(rm_212_button_rect, rm_212_button_surface, RED)
  button_hover_effect(rm_211_button_rect, rm_211_button_surface, RED)
  button_hover_effect(rm_210_button_rect, rm_210_button_surface, RED)
  button_hover_effect(rm_209_button_rect, rm_209_button_surface, RED)
  button_hover_effect(RR_3_button_rect, RR_3_button_surface, RED)
  button_hover_effect(rm_112_button_rect, rm_112_button_surface, RED)
  button_hover_effect(rm_111_button_rect, rm_111_button_surface, RED)
  button_hover_effect(rm_110_button_rect, rm_110_button_surface, RED)
  button_hover_effect(rm_109_button_rect, rm_109_button_surface, RED)
  button_hover_effect(RR_4_button_rect, RR_4_button_surface, RED)
  # Red
  # Purple
  button_hover_effect(RR_400_button_rect, RR_400_button_surface, PURPLE)
  button_hover_effect(rm_401_button_rect, rm_401_button_surface, PURPLE)
  button_hover_effect(rm_402_button_rect, rm_402_button_surface, PURPLE)
  button_hover_effect(rm_403_button_rect, rm_403_button_surface, PURPLE)
  button_hover_effect(rm_404_button_rect, rm_404_button_surface, PURPLE)
  button_hover_effect(rm_405_button_rect, rm_405_button_surface, PURPLE)
  button_hover_effect(rm_406_button_rect, rm_406_button_surface, PURPLE)
  button_hover_effect(rm_407_button_rect, rm_407_button_surface, PURPLE)
  button_hover_effect(rm_408_button_rect, rm_408_button_surface, PURPLE)
  button_hover_effect(rm_409_button_rect, rm_409_button_surface, PURPLE)
  # Purple
  # Green
  button_hover_effect(gym_button_rect, gym_button_surface, GREEN)
  button_hover_effect(tennis_button_rect, tennis_button_surface, GREEN)
  button_hover_effect(rm_702_button_rect, rm_702_button_surface, GREEN)
  button_hover_effect(circle_button_rect, circle_button_surface, GREEN)
  button_hover_effect(rm_703_button_rect, rm_703_button_surface, GREEN)
  button_hover_effect(rm_705_button_rect, rm_705_button_surface, GREEN)
  button_hover_effect(rm_704_button_rect, rm_704_button_surface, GREEN)
  button_hover_effect(rm_706_button_rect, rm_706_button_surface, GREEN)
  button_hover_effect(rm_707_button_rect, rm_707_button_surface, GREEN)
  button_hover_effect(rm_708_button_rect, rm_708_button_surface, GREEN)
  button_hover_effect(rm_709_button_rect, rm_709_button_surface, GREEN)
  button_hover_effect(rm_801_button_rect, rm_801_button_surface, GREEN)
  button_hover_effect(rm_802_button_rect, rm_802_button_surface, GREEN)
  button_hover_effect(rr_1_button_rect, rr_1_button_surface, GREEN)
  button_hover_effect(weight_button_rect, weight_button_surface, GREEN)
  # Green
  # Yellow
  button_hover_effect(rm_501_button_rect, rm_501_button_surface, YELLOW)
  button_hover_effect(rm_502_button_rect, rm_502_button_surface, YELLOW)
  button_hover_effect(rm_503_button_rect, rm_503_button_surface, YELLOW)
  button_hover_effect(rm_504_button_rect, rm_504_button_surface, YELLOW)
  button_hover_effect(rm_505_button_rect, rm_505_button_surface, YELLOW)
  button_hover_effect(rm_506_button_rect, rm_506_button_surface, YELLOW)
  button_hover_effect(rm_507_button_rect, rm_507_button_surface, YELLOW)
  button_hover_effect(rm_508_button_rect, rm_508_button_surface, YELLOW)
  button_hover_effect(rm_509_button_rect, rm_509_button_surface, YELLOW)
  button_hover_effect(rm_510_button_rect, rm_510_button_surface, YELLOW)
  button_hover_effect(rm_511_button_rect, rm_511_button_surface, YELLOW)
  button_hover_effect(rm_512_button_rect, rm_512_button_surface, YELLOW)
  button_hover_effect(rm_514_button_rect, rm_514_button_surface, YELLOW)
  button_hover_effect(rm_515_button_rect, rm_515_button_surface, YELLOW)
  button_hover_effect(rm_516_button_rect, rm_516_button_surface, YELLOW)
  button_hover_effect(rm_517_button_rect, rm_517_button_surface, YELLOW)
  button_hover_effect(RR_yellow_button_rect, RR_yellow_button_surface, YELLOW)
  # Yellow
  # Blue
  button_hover_effect(rm_905_button_rect, rm_905_button_surface, BLUE)
  button_hover_effect(rm_904_button_rect, rm_904_button_surface, BLUE)
  button_hover_effect(tennis_courts_button_rect, tennis_courts_button_surface, BLUE)
  button_hover_effect(lemon_parking_lot_button_rect, lemon_parking_lot_button_surface, BLUE)
  button_hover_effect(lawn_button_rect, lawn_button_surface, BLUE)
  button_hover_effect(media_center_button_rect, media_center_button_surface, BLUE)
  button_hover_effect(senate_room_button_rect, senate_room_button_surface, BLUE)
  button_hover_effect(mc1_button_rect, mc1_button_surface, BLUE)
  button_hover_effect(conf_rm_2_button_rect, conf_rm_2_button_surface, BLUE)
  button_hover_effect(mc2_button_rect, mc2_button_surface, BLUE)
  button_hover_effect(mc3_button_rect, mc3_button_surface, BLUE)
  button_hover_effect(mc4_button_rect, mc4_button_surface, BLUE)
  # Blue
  # Orange
  button_hover_effect(PO_button_rect, PO_button_surface, ORANGE)
  button_hover_effect(nurse_button_rect, nurse_button_surface, ORANGE)
  button_hover_effect(rgr_button_rect, rgr_button_surface, ORANGE)
  button_hover_effect(conf_button_rect, conf_button_surface, ORANGE)
  button_hover_effect(rm_311_button_rect, rm_311_button_surface, ORANGE)
  button_hover_effect(attendance_button_rect, attendance_button_surface, ORANGE)
  button_hover_effect(rm_310_button_rect, rm_310_button_surface, ORANGE)
  button_hover_effect(ccc_button_rect, ccc_button_surface, ORANGE)
  button_hover_effect(rm_304_button_rect, rm_304_button_surface, ORANGE)
  button_hover_effect(rr_orange_button_rect, rr_orange_button_surface, ORANGE)
  button_hover_effect(rm_309_button_rect, rm_309_button_surface, ORANGE)
  button_hover_effect(rm_308_button_rect, rm_308_button_surface, ORANGE)
  button_hover_effect(rm_305_button_rect, rm_305_button_surface, ORANGE)
  button_hover_effect(rm_306_button_rect, rm_306_button_surface, ORANGE)
  button_hover_effect(rm_307_button_rect, rm_307_button_surface, ORANGE)
  button_hover_effect(ad_office_button_rect, ad_office_button_surface, ORANGE)
  button_hover_effect(admin_offices_button_rect, admin_offices_button_surface, ORANGE)
  button_hover_effect(school_psych_button_rect, school_psych_button_surface, ORANGE)
  button_hover_effect(storage_button_rect, storage_button_surface, ORANGE)
  button_hover_effect(lunch_button_rect, lunch_button_surface, ORANGE)
  # Orange
  # Brown
  button_hover_effect(pool_button_rect, pool_button_surface, BROWN)
  button_hover_effect(rm_804_button_rect, rm_804_button_surface, BROWN)
  button_hover_effect(rm_803_button_rect, rm_803_button_surface, BROWN)
  button_hover_effect(locker_rooms_button_rect, locker_rooms_button_surface, BROWN)
  button_hover_effect(rm_207_button_rect, rm_207_button_surface, BROWN)
  button_hover_effect(rm_206_button_rect, rm_206_button_surface, BROWN)
  button_hover_effect(rm_205_button_rect, rm_205_button_surface, BROWN)
  button_hover_effect(rm_204_button_rect, rm_204_button_surface, BROWN)
  button_hover_effect(rm_203_button_rect, rm_203_button_surface, BROWN)
  button_hover_effect(rm_202_button_rect, rm_202_button_surface, BROWN)
  button_hover_effect(rm_201_button_rect, rm_201_button_surface, BROWN)
  button_hover_effect(rm_107_button_rect, rm_107_button_surface, BROWN)
  button_hover_effect(rm_106_button_rect, rm_106_button_surface, BROWN)
  button_hover_effect(rm_105_button_rect, rm_105_button_surface, BROWN)
  button_hover_effect(rm_104_button_rect, rm_104_button_surface, BROWN)
  button_hover_effect(rm_103_button_rect, rm_103_button_surface, BROWN)
  button_hover_effect(rm_102_button_rect, rm_102_button_surface, BROWN)
  button_hover_effect(rm_101_button_rect, rm_101_button_surface, BROWN)
  # Brown
 else:
  button_hover_effect(back_button_rect, back_button_surface, BACK)
 pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hovered_label else pygame.SYSTEM_CURSOR_ARROW)


 # Show the button text
 # Red
 rm_601_button_surface.blit(rm_601_text, rm_601_text_rect)
 staff_lounge_button_surface.blit(staff_lounge_text, staff_lounge_text_rect)
 rm_216_button_surface.blit(rm_216_text, rm_216_text_rect)
 rm_215_button_surface.blit(rm_215_text, rm_215_text_rect)
 rm_214_button_surface.blit(rm_214_text, rm_214_text_rect)
 RR_1_button_surface.blit(RR_1_text, RR_1_text_rect)
 rm_116_button_surface.blit(rm_116_text, rm_116_text_rect)
 rm_115_button_surface.blit(rm_115_text, rm_115_text_rect)
 rm_114_button_surface.blit(rm_114_text, rm_114_text_rect)
 RR_2_button_surface.blit(RR_2_text, RR_2_text_rect)
 rm_213_button_surface.blit(rm_213_text, rm_213_text_rect)
 rm_113_button_surface.blit(rm_113_text, rm_113_text_rect)
 rm_108_button_surface.blit(rm_108_text, rm_108_text_rect)
 rm_208_button_surface.blit(rm_208_text, rm_208_text_rect)
 rm_212_button_surface.blit(rm_212_text, rm_212_text_rect)
 rm_211_button_surface.blit(rm_211_text, rm_211_text_rect)
 rm_210_button_surface.blit(rm_210_text, rm_210_text_rect)
 rm_209_button_surface.blit(rm_209_text, rm_209_text_rect)
 RR_3_button_surface.blit(RR_3_text, RR_3_text_rect)
 rm_112_button_surface.blit(rm_112_text, rm_112_text_rect)
 rm_111_button_surface.blit(rm_111_text, rm_111_text_rect)
 rm_110_button_surface.blit(rm_110_text, rm_110_text_rect)
 rm_109_button_surface.blit(rm_109_text, rm_109_text_rect)
 RR_4_button_surface.blit(RR_4_text, RR_4_text_rect)
 # Red
 # Purple
 RR_400_button_surface.blit(RR_400_text, RR_400_text_rect)
 rm_401_button_surface.blit(rm_401_text, rm_401_text_rect)
 rm_402_button_surface.blit(rm_402_text, rm_402_text_rect)
 rm_403_button_surface.blit(rm_403_text, rm_403_text_rect)
 rm_404_button_surface.blit(rm_404_text, rm_404_text_rect)
 rm_405_button_surface.blit(rm_405_text, rm_405_text_rect)
 rm_406_button_surface.blit(rm_406_text, rm_406_text_rect)
 rm_407_button_surface.blit(rm_407_text, rm_407_text_rect)
 rm_408_button_surface.blit(rm_408_text, rm_408_text_rect)
 rm_409_button_surface.blit(rm_409_text, rm_409_text_rect)
 # Purple
 # Green
 gym_button_surface.blit(gym_text, gym_text_rect)
 tennis_button_surface.blit(tennis_text, tennis_text_rect)
 rm_702_button_surface.blit(rm_702_text, rm_702_text_rect)
 circle_button_surface.blit(circle_text, circle_text_rect)
 rm_703_button_surface.blit(rm_703_text, rm_703_text_rect)
 rm_705_button_surface.blit(rm_705_text, rm_705_text_rect)
 rm_704_button_surface.blit(rm_704_text, rm_704_text_rect)
 rm_706_button_surface.blit(rm_706_text, rm_706_text_rect)
 rm_707_button_surface.blit(rm_707_text, rm_707_text_rect)
 rm_708_button_surface.blit(rm_708_text, rm_708_text_rect)
 rm_709_button_surface.blit(rm_709_text, rm_709_text_rect)
 rm_801_button_surface.blit(rm_801_text, rm_801_text_rect)
 rm_802_button_surface.blit(rm_802_text, rm_802_text_rect)
 rr_1_button_surface.blit(rr_1_text, rr_1_text_rect)
 weight_button_surface.blit(weight_text, weight_text_rect)
 # Green
 # Yellow
 rm_501_button_surface.blit(rm_501_text, rm_501_text_rect)
 rm_502_button_surface.blit(rm_502_text, rm_502_text_rect)
 rm_503_button_surface.blit(rm_503_text, rm_503_text_rect)
 rm_504_button_surface.blit(rm_504_text, rm_504_text_rect)
 rm_505_button_surface.blit(rm_505_text, rm_505_text_rect)
 rm_506_button_surface.blit(rm_506_text, rm_506_text_rect)
 rm_507_button_surface.blit(rm_507_text, rm_507_text_rect)
 rm_508_button_surface.blit(rm_508_text, rm_508_text_rect)
 rm_509_button_surface.blit(rm_509_text, rm_509_text_rect)
 rm_510_button_surface.blit(rm_510_text, rm_510_text_rect)
 rm_511_button_surface.blit(rm_511_text, rm_511_text_rect)
 rm_512_button_surface.blit(rm_512_text, rm_512_text_rect)
 rm_514_button_surface.blit(rm_514_text, rm_514_text_rect)
 rm_515_button_surface.blit(rm_515_text, rm_515_text_rect)
 rm_516_button_surface.blit(rm_516_text, rm_516_text_rect)
 rm_517_button_surface.blit(rm_517_text, rm_517_text_rect)
 RR_yellow_button_surface.blit(RR_yellow_text, RR_yellow_text_rect)
 # Yellow
 # Blue
 rm_905_button_surface.blit(rm_905_text, rm_905_text_rect)
 rm_904_button_surface.blit(rm_904_text, rm_904_text_rect)
 tennis_courts_button_surface.blit(tennis_courts_text, tennis_courts_text_rect)
 lemon_parking_lot_button_surface.blit(lemon_parking_lot_text, lemon_parking_lot_text_rect)
 lawn_button_surface.blit(lawn_text, lawn_text_rect)
 media_center_button_surface.blit(media_center_text, media_center_text_rect)
 senate_room_button_surface.blit(senate_room_text, senate_room_text_rect)
 mc1_button_surface.blit(mc1_text, mc1_text_rect)
 conf_rm_2_button_surface.blit(conf_rm_2_text, conf_rm_2_text_rect)
 mc2_button_surface.blit(mc2_text, mc2_text_rect)
 mc3_button_surface.blit(mc3_text, mc3_text_rect)
 mc4_button_surface.blit(mc4_text, mc4_text_rect)
 # Blue
 # Orange
 PO_button_surface.blit(PO_text, PO_text_rect)
 nurse_button_surface.blit(nurse_text, nurse_text_rect)
 rgr_button_surface.blit(rgr_text, rgr_text_rect)
 rm_311_button_surface.blit(rm_311_text, rm_311_text_rect)
 conf_button_surface.blit(conf_text, conf_text_rect)
 rm_310_button_surface.blit(rm_310_text, rm_310_text_rect)
 ccc_button_surface.blit(ccc_text, ccc_text_rect)
 rm_304_button_surface.blit(rm_304_text, rm_304_text_rect)
 rr_orange_button_surface.blit(rr_orange_text, rr_orange_text_rect)
 rm_309_button_surface.blit(rm_309_text, rm_309_text_rect)
 rm_308_button_surface.blit(rm_308_text, rm_308_text_rect)
 rm_305_button_surface.blit(rm_305_text, rm_305_text_rect)
 rm_306_button_surface.blit(rm_306_text, rm_306_text_rect)
 rm_307_button_surface.blit(rm_307_text, rm_307_text_rect)
 ad_office_button_surface.blit(ad_office_text, ad_office_text_rect)
 admin_offices_button_surface.blit(admin_offices_text, admin_offices_text_rect)
 school_psych_button_surface.blit(school_psych_text, school_psych_text_rect)
 storage_button_surface.blit(storage_text, storage_text_rect)
 lunch_button_surface.blit(lunch_text, lunch_text_rect)
 attendance_button_surface.blit(attendance_text, attendance_text_rect)
 # Orange
 # Brown
 pool_button_surface.blit(pool_button_text, pool_button_text_rect)
 rm_804_button_surface.blit(rm_804_button_text, rm_804_button_text_rect)
 rm_803_button_surface.blit(rm_803_button_text, rm_803_button_text_rect)
 locker_rooms_button_surface.blit(locker_rooms_button_text, locker_rooms_button_text_rect)
 rm_207_button_surface.blit(rm_207_button_text, rm_207_button_text_rect)
 rm_206_button_surface.blit(rm_206_button_text, rm_206_button_text_rect)
 rm_205_button_surface.blit(rm_205_button_text, rm_205_button_text_rect)
 rm_204_button_surface.blit(rm_204_button_text, rm_204_button_text_rect)
 rm_203_button_surface.blit(rm_203_button_text, rm_203_button_text_rect)
 rm_202_button_surface.blit(rm_202_button_text, rm_202_button_text_rect)
 rm_201_button_surface.blit(rm_201_button_text, rm_201_button_text_rect)
 rm_107_button_surface.blit(rm_107_button_text, rm_107_button_text_rect)
 rm_106_button_surface.blit(rm_106_button_text, rm_106_button_text_rect)
 rm_105_button_surface.blit(rm_105_button_text, rm_105_button_text_rect)
 rm_104_button_surface.blit(rm_104_button_text, rm_104_button_text_rect)
 rm_103_button_surface.blit(rm_103_button_text, rm_103_button_text_rect)
 rm_102_button_surface.blit(rm_102_button_text, rm_102_button_text_rect)
 rm_101_button_surface.blit(rm_101_button_text, rm_101_button_text_rect)
 # Brown
 # Back
 back_button_surface.blit(back_button_text, back_button_text_rect)
 # Back


 # Draw the map and button on the screen
 if current_screen == map:
     screen.blit(current_screen, (0, 0))  # controls test_surface location
     # Red
     screen.blit(rm_601_button_surface, (rm_601_button_rect.x, rm_601_button_rect.y))
     screen.blit(staff_lounge_button_surface, (staff_lounge_button_rect.x, staff_lounge_button_rect.y))
     screen.blit(rm_216_button_surface, (rm_216_button_rect.x, rm_216_button_rect.y))
     screen.blit(rm_215_button_surface, (rm_215_button_rect.x, rm_215_button_rect.y))
     screen.blit(rm_214_button_surface, (rm_214_button_rect.x, rm_214_button_rect.y))
     screen.blit(RR_1_button_surface, (RR_1_button_rect.x, RR_1_button_rect.y))
     screen.blit(rm_116_button_surface, (rm_116_button_rect.x, rm_116_button_rect.y))
     screen.blit(rm_115_button_surface, (rm_115_button_rect.x, rm_115_button_rect.y))
     screen.blit(rm_114_button_surface, (rm_114_button_rect.x, rm_114_button_rect.y))
     screen.blit(RR_2_button_surface, (RR_2_button_rect.x, RR_2_button_rect.y))
     screen.blit(rm_213_button_surface, (rm_213_button_rect.x, rm_213_button_rect.y))
     screen.blit(rm_113_button_surface, (rm_113_button_rect.x, rm_113_button_rect.y))
     screen.blit(rm_108_button_surface, (rm_108_button_rect.x, rm_108_button_rect.y))
     screen.blit(rm_208_button_surface, (rm_208_button_rect.x, rm_208_button_rect.y))
     screen.blit(rm_212_button_surface, (rm_212_button_rect.x, rm_212_button_rect.y))
     screen.blit(rm_211_button_surface, (rm_211_button_rect.x, rm_211_button_rect.y))
     screen.blit(rm_210_button_surface, (rm_210_button_rect.x, rm_210_button_rect.y))
     screen.blit(rm_209_button_surface, (rm_209_button_rect.x, rm_209_button_rect.y))
     screen.blit(RR_3_button_surface, (RR_3_button_rect.x, RR_3_button_rect.y))
     screen.blit(rm_112_button_surface, (rm_112_button_rect.x, rm_112_button_rect.y))
     screen.blit(rm_111_button_surface, (rm_111_button_rect.x, rm_111_button_rect.y))
     screen.blit(rm_110_button_surface, (rm_110_button_rect.x, rm_110_button_rect.y))
     screen.blit(rm_109_button_surface, (rm_109_button_rect.x, rm_109_button_rect.y))
     screen.blit(RR_4_button_surface, (RR_4_button_rect.x, RR_4_button_rect.y))
     # Red
     # Purple
     screen.blit(RR_400_button_surface, (RR_400_button_rect.x, RR_400_button_rect.y))
     screen.blit(rm_401_button_surface, (rm_401_button_rect.x, rm_401_button_rect.y))
     screen.blit(rm_402_button_surface, (rm_402_button_rect.x, rm_402_button_rect.y))
     screen.blit(rm_403_button_surface, (rm_403_button_rect.x, rm_403_button_rect.y))
     screen.blit(rm_404_button_surface, (rm_404_button_rect.x, rm_404_button_rect.y))
     screen.blit(rm_405_button_surface, (rm_405_button_rect.x, rm_405_button_rect.y))
     screen.blit(rm_406_button_surface, (rm_406_button_rect.x, rm_406_button_rect.y))
     screen.blit(rm_407_button_surface, (rm_407_button_rect.x, rm_407_button_rect.y))
     screen.blit(rm_408_button_surface, (rm_408_button_rect.x, rm_408_button_rect.y))
     screen.blit(rm_409_button_surface, (rm_409_button_rect.x, rm_409_button_rect.y))
     # Purple
     # Green
     screen.blit(gym_button_surface, (gym_button_rect.x, gym_button_rect.y))
     screen.blit(tennis_button_surface, (tennis_button_rect.x, tennis_button_rect.y))
     screen.blit(rm_702_button_surface, (rm_702_button_rect.x, rm_702_button_rect.y))
     screen.blit(circle_button_surface, circle_button_surface.get_rect(center=circle_button_rect.center))
     screen.blit(rm_703_button_surface, (rm_703_button_rect.x, rm_703_button_rect.y))
     screen.blit(rm_705_button_surface, (rm_705_button_rect.x, rm_705_button_rect.y))
     screen.blit(rm_704_button_surface, (rm_704_button_rect.x, rm_704_button_rect.y))
     screen.blit(rm_706_button_surface, (rm_706_button_rect.x, rm_706_button_rect.y))
     screen.blit(rm_707_button_surface, (rm_707_button_rect.x, rm_707_button_rect.y))
     screen.blit(rm_708_button_surface, (rm_708_button_rect.x, rm_708_button_rect.y))
     screen.blit(rm_709_button_surface, (rm_709_button_rect.x, rm_709_button_rect.y))
     screen.blit(rm_801_button_surface, (rm_801_button_rect.x, rm_801_button_rect.y))
     screen.blit(rm_802_button_surface, (rm_802_button_rect.x, rm_802_button_rect.y))
     screen.blit(rr_1_button_surface, (rr_1_button_rect.x, rr_1_button_rect.y))
     screen.blit(weight_button_surface, (weight_button_rect.x, weight_button_rect.y))
     # Green
     # Yellow
     screen.blit(rm_501_button_surface, (rm_501_button_rect.x, rm_501_button_rect.y))
     screen.blit(rm_502_button_surface, (rm_502_button_rect.x, rm_502_button_rect.y))
     screen.blit(rm_503_button_surface, (rm_503_button_rect.x, rm_503_button_rect.y))
     screen.blit(rm_504_button_surface, (rm_504_button_rect.x, rm_504_button_rect.y))
     screen.blit(rm_505_button_surface, (rm_505_button_rect.x, rm_505_button_rect.y))
     screen.blit(rm_506_button_surface, (rm_506_button_rect.x, rm_506_button_rect.y))
     screen.blit(rm_507_button_surface, (rm_507_button_rect.x, rm_507_button_rect.y))
     screen.blit(rm_508_button_surface, (rm_508_button_rect.x, rm_508_button_rect.y))
     screen.blit(rm_509_button_surface, (rm_509_button_rect.x, rm_509_button_rect.y))
     screen.blit(rm_510_button_surface, (rm_510_button_rect.x, rm_510_button_rect.y))
     screen.blit(rm_511_button_surface, (rm_511_button_rect.x, rm_511_button_rect.y))
     screen.blit(rm_512_button_surface, (rm_512_button_rect.x, rm_512_button_rect.y))
     screen.blit(rm_514_button_surface, (rm_514_button_rect.x, rm_514_button_rect.y))
     screen.blit(rm_515_button_surface, (rm_515_button_rect.x, rm_515_button_rect.y))
     screen.blit(rm_516_button_surface, (rm_516_button_rect.x, rm_516_button_rect.y))
     screen.blit(rm_517_button_surface, (rm_517_button_rect.x, rm_517_button_rect.y))
     screen.blit(RR_yellow_button_surface, (RR_yellow_button_rect.x, RR_yellow_button_rect.y))
     # Yellow
     # Blue
     screen.blit(rm_905_button_surface, (rm_905_button_rect.x, rm_905_button_rect.y))
     screen.blit(rm_904_button_surface, (rm_904_button_rect.x, rm_904_button_rect.y))
     screen.blit(tennis_courts_button_surface, (tennis_courts_button_rect.x, tennis_courts_button_rect.y))
     screen.blit(lemon_parking_lot_button_surface,
                 (lemon_parking_lot_button_rect.x, lemon_parking_lot_button_rect.y))
     screen.blit(lawn_button_surface, (lawn_button_rect.x, lawn_button_rect.y))
     screen.blit(media_center_button_surface, (media_center_button_rect.x, media_center_button_rect.y))
     screen.blit(senate_room_button_surface, (senate_room_button_rect.x, senate_room_button_rect.y))
     screen.blit(mc1_button_surface, (mc1_button_rect.x, mc1_button_rect.y))
     screen.blit(conf_rm_2_button_surface, (conf_rm_2_button_rect.x, conf_rm_2_button_rect.y))
     screen.blit(mc2_button_surface, (mc2_button_rect.x, mc2_button_rect.y))
     screen.blit(mc3_button_surface, (mc3_button_rect.x, mc3_button_rect.y))
     screen.blit(mc4_button_surface, (mc4_button_rect.x, mc4_button_rect.y))
     # Blue
     # Orange
     screen.blit(PO_button_surface, (PO_button_rect.x, PO_button_rect.y))
     screen.blit(nurse_button_surface, (nurse_button_rect.x, nurse_button_rect.y))
     screen.blit(rgr_button_surface, (rgr_button_rect.x, rgr_button_rect.y))
     screen.blit(rm_311_button_surface, (rm_311_button_rect.x, rm_311_button_rect.y))
     screen.blit(conf_button_surface, (conf_button_rect.x, conf_button_rect.y))
     screen.blit(rm_310_button_surface, (rm_310_button_rect.x, rm_310_button_rect.y))
     screen.blit(ccc_button_surface, (ccc_button_rect.x, ccc_button_rect.y))
     screen.blit(rm_304_button_surface, (rm_304_button_rect.x, rm_304_button_rect.y))
     screen.blit(rr_orange_button_surface, (rr_orange_button_rect.x, rr_orange_button_rect.y))
     screen.blit(rm_309_button_surface, (rm_309_button_rect.x, rm_309_button_rect.y))
     screen.blit(rm_308_button_surface, (rm_308_button_rect.x, rm_308_button_rect.y))
     screen.blit(rm_305_button_surface, (rm_305_button_rect.x, rm_305_button_rect.y))
     screen.blit(rm_306_button_surface, (rm_306_button_rect.x, rm_306_button_rect.y))
     screen.blit(rm_307_button_surface, (rm_307_button_rect.x, rm_307_button_rect.y))
     screen.blit(ad_office_button_surface, (ad_office_button_rect.x, ad_office_button_rect.y))
     screen.blit(admin_offices_button_surface, (admin_offices_button_rect.x, admin_offices_button_rect.y))
     screen.blit(school_psych_button_surface, (school_psych_button_rect.x, school_psych_button_rect.y))
     screen.blit(storage_button_surface, (storage_button_rect.x, storage_button_rect.y))
     screen.blit(lunch_button_surface, (lunch_button_rect.x, lunch_button_rect.y))
     screen.blit(attendance_button_surface, (attendance_button_rect.x, attendance_button_rect.y))
     # Orange
     # Brown
     screen.blit(pool_button_surface, (pool_button_rect.x, pool_button_rect.y))
     screen.blit(rm_804_button_surface, (rm_804_button_rect.x, rm_804_button_rect.y))
     screen.blit(rm_803_button_surface, (rm_803_button_rect.x, rm_803_button_rect.y))
     screen.blit(locker_rooms_button_surface, (locker_rooms_button_rect.x, locker_rooms_button_rect.y))
     screen.blit(rm_207_button_surface, (rm_207_button_rect.x, rm_207_button_rect.y))
     screen.blit(rm_206_button_surface, (rm_206_button_rect.x, rm_206_button_rect.y))
     screen.blit(rm_205_button_surface, (rm_205_button_rect.x, rm_205_button_rect.y))
     screen.blit(rm_204_button_surface, (rm_204_button_rect.x, rm_204_button_rect.y))
     screen.blit(rm_203_button_surface, (rm_203_button_rect.x, rm_203_button_rect.y))
     screen.blit(rm_202_button_surface, (rm_202_button_rect.x, rm_202_button_rect.y))
     screen.blit(rm_201_button_surface, (rm_201_button_rect.x, rm_201_button_rect.y))
     screen.blit(rm_107_button_surface, (rm_107_button_rect.x, rm_107_button_rect.y))
     screen.blit(rm_106_button_surface, (rm_106_button_rect.x, rm_106_button_rect.y))
     screen.blit(rm_105_button_surface, (rm_105_button_rect.x, rm_105_button_rect.y))
     screen.blit(rm_104_button_surface, (rm_104_button_rect.x, rm_104_button_rect.y))
     screen.blit(rm_103_button_surface, (rm_103_button_rect.x, rm_103_button_rect.y))
     screen.blit(rm_102_button_surface, (rm_102_button_rect.x, rm_102_button_rect.y))
     screen.blit(rm_101_button_surface, (rm_101_button_rect.x, rm_101_button_rect.y))
     # Brown

 else:
     screen.blit(current_screen, (0, 0))
     # Back
     screen.blit(back_button_surface, (back_button_rect.x, back_button_rect.y))
     # Back
     # Caption
     if current_title:
         caption_text = render_tight(current_title, 26, (255, 255, 255))
         caption = pygame.Surface((caption_text.get_width() + 48, caption_text.get_height() + 28), pygame.SRCALPHA)
         pygame.draw.rect(caption, (15, 23, 42, 200), caption.get_rect(), border_radius=caption.get_height() // 2)
         caption.blit(caption_text, caption_text.get_rect(center=caption.get_rect().center))
         screen.blit(caption, caption.get_rect(midbottom=(620, 900)))
     # Caption

 # Fade in whenever the screen changes
 if current_screen is not shown_screen:
     shown_screen = current_screen
     fade_alpha = 255
 if fade_alpha > 0:
     fade_overlay.set_alpha(fade_alpha)
     screen.blit(fade_overlay, (0, 0))
     fade_alpha -= 30

 # Update the game state
 pygame.display.update()

