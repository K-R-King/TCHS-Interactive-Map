"""TCHS Interactive Map: click a place on the campus map to see photos of it."""
import os
import sys

import pygame

# Load files relative to this script, wherever it is run from
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Keep Windows display scaling from enlarging the window past the screen edges
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_RENDER_SCALE_QUALITY'] = 'best'

pygame.init()
WIDTH, HEIGHT = 1240, 930
# SCALED stretches everything to fill the window when it is resized, maximized or fullscreen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('TCHS Interactive Map')
clock = pygame.time.Clock()


# ------------------------------------------------------------------ Colours

TEXT = (30, 41, 59)
SUBTEXT = (71, 85, 105)
DARK = (15, 23, 42)
WHITE = (255, 255, 255)
RED = (220, 38, 38)
PURPLE = (147, 51, 234)
GREEN = (22, 163, 74)
YELLOW = (202, 138, 4)
BLUE = (37, 99, 235)
ORANGE = (234, 88, 12)
BROWN = (146, 64, 14)


# Mix a colour with white; amount 0 = white, 1 = the full colour
def tint(color, amount):
    return tuple(round(255 + (c - 255) * amount) for c in color)


# ------------------------------------------------------------------ Places

STAND_IN = '601.jpg'  # shown for places that don't have their own photo yet


class Place:
    """A clickable spot on the map and the photos shown when it is clicked."""

    def __init__(self, label, color, box, photos=(), title=None, note=None, shape='box'):
        self.label = label                      # text on the map
        self.color = color
        self.rect = pygame.Rect(box)            # x, y, width, height on the map
        self.photos = list(photos) or [STAND_IN]
        self.stand_in = not photos
        self.note = note                        # small second line, e.g. what a room is used for
        self.shape = shape                      # 'box' or 'circle'
        if title is None:
            title = 'Restroom' if label == 'RR' else f'Room {label}' if label[0].isdigit() else label
        self.title = f'{title} – {note}' if note else title
        self.glow = 0.0                         # hover highlight, eased in and out
        self.label_image = None                 # rendered once the fonts are ready


P = Place
PLACES = [
    # 600s building and the 100s / 200s wings
    P('601', RED, (755, 338, 117, 154), ['601.jpg', '601 Entrance.jpg', '601 Left Door.jpg', 'Rm601 Side.jpg',
       '600s_building.jpg', '600s_building_pt2.jpg']),
    P('Cafeteria & Staff Lounge', RED, (755, 235, 117, 101), ['staff_lounge.jpg', 'Staff Lounge.jpg',
       'Staff Lounge Left Door.jpg', 'Staff Lounge Right Door.jpg']),
    P('216', RED, (837, 646, 58, 34)),
    P('215', RED, (897, 646, 53, 34)),
    P('214', RED, (952, 646, 54, 34), ['214.jpg']),
    P('RR', RED, (1007, 646, 54, 34), ['girls_bathroom_200s.jpg', '200s_girl_s restroom.jpg',
       'boys_ bathroom_200s.jpg']),
    P('116', RED, (837, 681, 58, 34), ['116.jpg']),
    P('115', RED, (897, 681, 53, 34), ['115.jpg']),
    P('114', RED, (952, 681, 54, 34), ['114.jpg']),
    P('RR', RED, (1007, 681, 54, 34), ['100s_boys_ bathroom.jpg', '100s_girls_bathroom.jpg']),
    P('213', RED, (1121, 647, 58, 34), ['213.jpg']),
    P('113', RED, (1121, 683, 58, 33), ['113.jpg']),
    P('108', RED, (1121, 764, 58, 34), ['108.jpg']),
    P('208', RED, (1121, 729, 58, 33), ['208.jpg']),
    P('212', RED, (784, 728, 59, 34)),
    P('211', RED, (844, 728, 54, 34)),
    P('210', RED, (899, 728, 55, 34)),
    P('209', RED, (955, 728, 57, 34)),
    P('RR', RED, (1013, 728, 49, 34), ['girls_bathroom_200s.jpg', '200s_girl_s restroom.jpg',
       'boys_ bathroom_200s.jpg']),
    P('112', RED, (784, 764, 59, 34)),
    P('111', RED, (844, 764, 54, 34)),
    P('110', RED, (899, 764, 55, 34), ['110.jpg']),
    P('109', RED, (955, 764, 57, 34)),
    P('RR', RED, (1013, 764, 49, 34), ['100s_boys_ bathroom.jpg', '100s_girls_bathroom.jpg']),

    # 400s
    P('RR', PURPLE, (1010, 389, 39, 16), ['boys_ bathroom_200s.jpg']),
    P('401', PURPLE, (1010, 406, 39, 47), ['ROOM 401-1.jpg']),
    P('402', PURPLE, (1010, 313, 39, 55), ['ROOM 402-2.jpg']),
    P('403', PURPLE, (1010, 258, 39, 53), ['ROOM 403-1.jpg']),
    P('404', PURPLE, (1010, 201, 39, 56), ['ROOM 404-1.jpg']),
    P('405', PURPLE, (1050, 201, 38, 56), ['ROOM 405-1.jpg']),
    P('406', PURPLE, (1050, 258, 38, 53), ['ROOM 406-1.jpg']),
    P('407', PURPLE, (1050, 313, 38, 55), ['ROOM 407-1.jpg']),
    P('408', PURPLE, (1050, 406, 38, 47), ['ROOM 408-1.jpg']),
    P('409', PURPLE, (1050, 463, 38, 47), ['ROOM 409-1.jpg']),

    # 700s, 800s, gym and Senior Circle
    P('Beckner Gym', GREEN, (451, 385, 115, 94), ['Front Entrance to Gym.jpg', 'Outside Gym.jpg', 'Gym Door.jpg',
       'Side of Gym.jpg', 'Side Staircase of Gym.jpg', 'Gym Door and Basketball Courts.jpg']),
    P('Tennis Courts', GREEN, (438, 271, 39, 85), ['Tennis Courts.jpg', 'Tennis Courts Side.jpg',
       'Tennis Courts and Bicycle Racks.jpg', 'Tennis Courts and Team Room 2.jpg']),
    P('702', GREEN, (490, 271, 65, 85), ['Room 702 and Tennis Court Entrance.jpg']),
    P('Senior Circle', GREEN, (632, 415, 59, 57), ['Senior Circle_1.jpg', 'Senior Circle.jpg',
       'Senior Circle_2.jpg', 'Senior Circle_3.jpg', 'Senior Circle_4.jpg', 'Senior Circle Benches.jpg',
       'senior_circle_side.jpg'], shape='circle'),
    P('703', GREEN, (556, 271, 49, 85)),
    P('705', GREEN, (634, 271, 26, 85), ['room 705 (edt) and 704.jpg']),
    P('704', GREEN, (606, 271, 27, 85), ['700s side and gym stairs.jpg']),
    P('706', GREEN, (661, 327, 22, 29), ['room 706 and 707.jpg', 'room 706 windows.jpg']),
    P('707', GREEN, (661, 299, 22, 28), ['room 707.jpg']),
    P('708', GREEN, (661, 271, 22, 28)),
    P('709', GREEN, (634, 246, 26, 23), ['Boys restroom and art room.jpg']),
    P('801', GREEN, (569, 427, 22, 24)),
    P('802', GREEN, (569, 402, 22, 24)),
    P('RR', GREEN, (661, 233, 22, 36), ['room 707 windows and girls restroom.jpg']),
    P('Weight Room & Dance Studio 701', GREEN, (489, 169, 62, 100), ['Weight Room.jpg'], title='Weight Room & Dance Studio (701)'),

    # 500s
    P('501', YELLOW, (1090, 423, 37, 30), ['rm_501.jpg']),
    P('502', YELLOW, (1090, 388, 38, 33), ['rm_502.jpg']),
    P('503', YELLOW, (1090, 342, 38, 26), ['rm_503.jpg']),
    P('504', YELLOW, (1090, 313, 38, 27), ['rm_504.jpg']),
    P('505', YELLOW, (1090, 276, 38, 35), ['rm_505.jpg']),
    P('506', YELLOW, (1090, 240, 38, 35), ['rm_506.jpg']),
    P('507', YELLOW, (1090, 201, 37, 38), ['rm_507.jpg']),
    P('508', YELLOW, (1128, 201, 40, 38), ['rm_508.jpg']),
    P('509', YELLOW, (1129, 240, 39, 35), ['rm_509.jpg']),
    P('510', YELLOW, (1129, 276, 39, 35), ['rm_510.jpg']),
    P('511', YELLOW, (1129, 313, 39, 27), ['rm_511.jpg']),
    P('512', YELLOW, (1129, 342, 39, 26), ['rm_512.jpg']),
    P('514', YELLOW, (1129, 388, 39, 33), ['rm_514.jpg']),
    P('515', YELLOW, (1129, 423, 39, 30), ['rm_515.jpg']),
    P('516', YELLOW, (1129, 463, 39, 47), ['rm_516.jpg']),
    P('517', YELLOW, (1090, 463, 37, 47), ['rm_517.jpg']),
    P('RR', YELLOW, (1090, 369, 38, 12)),

    # Performing Arts, fields and Media Center
    P('905', BLUE, (408, 552, 75, 85), ['Performing Arts Building.jpg']),
    P('904', BLUE, (483, 552, 76, 85), ['Performing Arts Building.jpg']),
    P('Tennis Courts', BLUE, (158, 655, 127, 231)),
    P('Lemon Parking Lot', BLUE, (287, 655, 126, 231)),
    P('Lawn', BLUE, (427, 655, 151, 210)),
    P('Media Center', BLUE, (594, 810, 123, 74)),
    P('Senate Room', BLUE, (676, 658, 41, 34)),
    P('MC1', BLUE, (594, 700, 30, 14)),
    P('Conference Rm 2', BLUE, (619, 713, 58, 27), title='Conference Room 2'),
    P('MC2', BLUE, (594, 686, 30, 14)),
    P('MC3', BLUE, (594, 672, 30, 14)),
    P('MC4', BLUE, (594, 658, 30, 14)),

    # Offices and the 300s
    P("Principal's Office", ORANGE, (615, 536, 35, 28), ['principal_s_office.jpg']),
    P('Nurse', ORANGE, (678, 537, 31, 18), ['nurse_s_office.jpg']),
    P('Registrar', ORANGE, (754, 574, 38, 40), ['records_office.jpg']),
    P('Conf Room', ORANGE, (615, 565, 36, 49), ['conference_room.jpg'], title='Conference Room'),
    P('311', ORANGE, (754, 536, 81, 37), ['311_staff_entrance.jpg']),
    P('Main Office & Attendance', ORANGE, (594, 760, 68, 48), ['attendance_office_inner_entrance.jpg'], title='Main Office & Attendance Office'),
    P('310', ORANGE, (836, 536, 143, 38), ['rm_310.jpg']),
    P('Counseling College & Career', ORANGE, (833, 574, 119, 40), ['counseling_office.jpg'], title='Counseling / College & Career'),
    P('304', ORANGE, (953, 575, 26, 39), ['rm_304.jpg'], note='Mental Fitness Ctr'),
    P('RR', ORANGE, (980, 536, 32, 38), ['300s_boys_bathroom.jpg', 'girls_bathroom_311.jpg',
       'staff_women_s_restroom_311.jpg']),
    P('309', ORANGE, (1034, 536, 57, 38)),
    P('308', ORANGE, (1092, 536, 77, 39)),
    P('305', ORANGE, (1034, 576, 41, 38), ['rm_305.jpg'], note='DIS Counselor'),
    P('306', ORANGE, (1076, 576, 42, 38), ['rm_306.jpg']),
    P('307', ORANGE, (1120, 576, 49, 38), ['rm_307.jpg'], note='School Psych'),
    P('AD Office', ORANGE, (710, 537, 18, 17)),
    P('Administrative Offices', ORANGE, (669, 590, 60, 24), ['admin_office.jpg', 'admin_office(1).jpg',
       'admin_office_entrance.jpg', 'assistant_principal_office.jpg', 'assistant_principal_s_office.jpg']),
    P('School Psych', ORANGE, (793, 598, 18, 16)),
    P('Storage', ORANGE, (980, 575, 32, 38)),
    P('Lunch Shelter', ORANGE, (899, 302, 74, 50)),

    # Pool, locker rooms and the south 100s / 200s rows
    P('Pool', BROWN, (292, 425, 62, 68), ['OutsidePool2.jpg', 'pool.jpg']),
    P('804', BROWN, (404, 412, 19, 55), ['rm_804.jpg']),
    P('803', BROWN, (404, 467, 19, 55)),
    P('Locker Rooms', BROWN, (383, 412, 20, 110), ['locker.jpg', 'Girls Lockeroom.jpg',
       'Trainers Room and Gym Door.jpg']),
    P('207', BROWN, (784, 810, 59, 34), ['rm_207.jpg']),
    P('206', BROWN, (844, 810, 54, 34), ['rm_206.jpg']),
    P('205', BROWN, (899, 810, 55, 34), ['rm_205.jpg']),
    P('204', BROWN, (955, 810, 53, 34), ['rm_204.jpg']),
    P('203', BROWN, (1010, 810, 52, 34), ['rm_203.jpg']),
    P('202', BROWN, (1063, 810, 55, 34), ['rm_202.jpg']),
    P('201', BROWN, (1120, 810, 60, 34), ['rm_201.jpg']),
    P('107', BROWN, (784, 846, 59, 34), ['rm_107.jpg']),
    P('106', BROWN, (844, 846, 54, 34), ['rm_106.jpg', 'rm_106_pt2.jpg']),
    P('105', BROWN, (899, 846, 55, 34), ['rm_105.jpg']),
    P('104', BROWN, (955, 846, 53, 34), ['rm_104.jpg']),
    P('103', BROWN, (1010, 846, 52, 34), ['rm_103.jpg']),
    P('102', BROWN, (1063, 846, 55, 34), ['rm_102.jpg']),
    P('101', BROWN, (1120, 846, 60, 34), ['rm_101.jpg']),
]


# ------------------------------------------------------------------ Text

font_path = pygame.font.match_font('segoeuisemibold,segoeui,helveticaneue,arial')
fonts = {}


def font(size):
    if size not in fonts:
        fonts[size] = pygame.font.Font(font_path, size)
    return fonts[size]


# Render text trimmed to its visible pixels, so it centres exactly
def render_tight(text, size, color):
    rendered = font(size).render(text, True, color)
    bounds = rendered.get_bounding_rect()
    return rendered.subsurface(bounds).copy() if bounds.width else rendered


# Split text into lines no wider than max_w at this font size
def wrap(text, size, max_w):
    lines = []
    for word in text.split(' '):
        if lines and font(size).size(lines[-1] + ' ' + word)[0] <= max_w:
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


# Render a label as large as fits in a w x h space, wrapping if needed.
# An optional note is drawn small underneath, like the printed map's notes.
def render_label(text, w, h, note=None):
    max_w, max_h = w - (6 if w > 40 else 3), h - 3
    note_image = None
    if note:
        for size in (9, 8, 7):
            note_image = stack([render_tight(line, size, SUBTEXT) for line in wrap(note, size, max_w)], 1)
            if note_image.get_width() <= max_w:
                break
        max_h -= note_image.get_height() + 3
    # Tall, narrow boxes get sideways text, like the printed map
    sideways = max_h > 2 * max_w and ' ' in text
    if sideways:
        max_w, max_h = max_h, max_w
    # One size for regular rooms so rows match; larger only for big areas
    for size in range(24 if min(max_w, max_h) >= 56 else 19, 6, -1):
        label = stack([render_tight(line, size, TEXT) for line in wrap(text, size, max_w)], round(size * 0.3))
        if label.get_width() <= max_w and label.get_height() <= max_h:
            if sideways:
                return pygame.transform.rotate(label, 90)
            return stack([label, note_image], 3) if note_image else label
    # Very small boxes: shrink the smallest text until it fits
    label = stack([render_tight(line, 7, TEXT) for line in wrap(text, 7, max_w)], 1)
    scale = min(max_w / label.get_width(), max_h / label.get_height(), 1)
    return pygame.transform.smoothscale(label, (max(1, int(label.get_width() * scale)),
                                                max(1, int(label.get_height() * scale))))


for place in PLACES:
    w, h = place.rect.size
    if place.shape == 'circle':
        w, h = int(w * 0.85), int(h * 0.65)   # keep the text inside the curve
    place.label_image = render_label(place.label, w, h, place.note)


# ------------------------------------------------------------------ Images

campus_map = pygame.image.load('assets/map_2025.png').convert()
photos = {}


# Load a photo the first time it is shown, fitted to the window without stretching
def photo(name):
    if name not in photos:
        image = pygame.image.load('assets/' + name).convert()
        scale = min(WIDTH / image.get_width(), HEIGHT / image.get_height())
        size = (round(image.get_width() * scale), round(image.get_height() * scale))
        canvas = pygame.Surface((WIDTH, HEIGHT))
        canvas.fill(DARK)
        scaled = pygame.transform.smoothscale(image, size)
        canvas.blit(scaled, scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        photos[name] = canvas
    return photos[name]


# ------------------------------------------------------------------ Controls

SEARCH_RECT = pygame.Rect(566, 128, 176, 32)
BACK_RECT = pygame.Rect(24, 20, 170, 46)
PREV_CENTER = (60, HEIGHT // 2)
NEXT_CENTER = (WIDTH - 60, HEIGHT // 2)
ARROW_RADIUS = 28


def pill(rect, fill, border=None, width=1):
    """Draw a rounded, possibly translucent, rectangle."""
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(surface, fill, surface.get_rect(), border_radius=rect.height // 2)
    if border:
        pygame.draw.rect(surface, border, surface.get_rect(), width, border_radius=rect.height // 2)
    screen.blit(surface, rect)


def draw_arrow(center, direction, hovered):
    """Draw a round next/previous button; direction is -1 for left, 1 for right."""
    size = ARROW_RADIUS * 2
    button = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(button, (*DARK, 220 if hovered else 150), (ARROW_RADIUS, ARROW_RADIUS), ARROW_RADIUS)
    tip, back = ARROW_RADIUS + 6 * direction, ARROW_RADIUS - 5 * direction
    pygame.draw.lines(button, WHITE, False, [(back, ARROW_RADIUS - 10), (tip, ARROW_RADIUS), (back, ARROW_RADIUS + 10)], 4)
    screen.blit(button, button.get_rect(center=center))


def in_circle(pos, center):
    return (pos[0] - center[0]) ** 2 + (pos[1] - center[1]) ** 2 <= ARROW_RADIUS ** 2


def matches(place, query):
    return query in place.label.lower() or query in place.title.lower()


# ------------------------------------------------------------------ Drawing

def draw_place(place, hovered, query):
    place.glow += ((1 if hovered else 0) - place.glow) * 0.3
    matched = query and matches(place, query)
    dimmed = query and not matched
    if dimmed:
        fill, border, width = (241, 245, 249), (203, 213, 225), 1
    else:
        strength = 0.45 if matched else 0.12 + 0.3 * place.glow
        fill, border = tint(place.color, strength), place.color
        width = 2 if hovered or matched else 1
    box = place.rect.inflate(-2, -2)
    if place.shape == 'circle':
        pygame.draw.ellipse(screen, fill, box)
        pygame.draw.ellipse(screen, border, box, width)
    else:
        radius = max(2, min(8, box.width // 4, box.height // 4))
        pygame.draw.rect(screen, fill, box, border_radius=radius)
        pygame.draw.rect(screen, border, box, width, border_radius=radius)
    place.label_image.set_alpha(70 if dimmed else 255)
    screen.blit(place.label_image, place.label_image.get_rect(center=place.rect.center))
    # A pulsing ring makes search results easy to spot, even tiny ones
    if matched:
        pulse = 3 + 3 * abs((pygame.time.get_ticks() % 1000) / 500 - 1)
        ring = place.rect.inflate(2 * pulse, 2 * pulse)
        if place.shape == 'circle':
            pygame.draw.ellipse(screen, place.color, ring, 2)
        else:
            pygame.draw.rect(screen, place.color, ring, 2, border_radius=8)


def draw_search(query, count):
    active = bool(query)
    pill(SEARCH_RECT, (*WHITE, 240), BLUE if active else (148, 163, 184), 2 if active else 1)
    # Magnifying glass
    cx, cy = SEARCH_RECT.x + 17, SEARCH_RECT.centery - 2
    pygame.draw.circle(screen, SUBTEXT, (cx, cy), 6, 2)
    pygame.draw.line(screen, SUBTEXT, (cx + 4, cy + 4), (cx + 9, cy + 9), 3)
    if query:
        text = render_tight(query, 15, TEXT)
        hint = render_tight(f'{count} found' if count else 'no match', 11, SUBTEXT if count else RED)
        screen.blit(hint, hint.get_rect(midright=(SEARCH_RECT.right - 12, SEARCH_RECT.centery)))
        # Blinking cursor after the text
        x = SEARCH_RECT.x + 32
        screen.blit(text, text.get_rect(midleft=(x, SEARCH_RECT.centery)))
        if pygame.time.get_ticks() // 500 % 2:
            caret_x = x + text.get_width() + 2
            pygame.draw.line(screen, TEXT, (caret_x, SEARCH_RECT.centery - 8), (caret_x, SEARCH_RECT.centery + 8), 1)
    else:
        hint = render_tight('Type to find a room', 13, (100, 116, 139))
        screen.blit(hint, hint.get_rect(midleft=(SEARCH_RECT.x + 32, SEARCH_RECT.centery)))


def draw_tooltip(text, pos):
    label = render_tight(text, 14, WHITE)
    rect = label.get_rect().inflate(20, 14)
    rect.midbottom = (pos[0], pos[1] - 14)
    rect.clamp_ip(screen.get_rect().inflate(-8, -8))
    pill(rect, (*DARK, 230))
    screen.blit(label, label.get_rect(center=rect.center))


def draw_map(mouse, query):
    screen.blit(campus_map, (0, 0))
    hovered = next((p for p in PLACES if p.rect.collidepoint(mouse)), None)
    for place in PLACES:
        draw_place(place, place is hovered, query)
    draw_search(query, sum(matches(p, query) for p in PLACES) if query else 0)
    if hovered:
        draw_tooltip(hovered.title, mouse)
    return hovered


def draw_photo(place, index, mouse):
    screen.blit(photo(place.photos[index]), (0, 0))
    hovering = BACK_RECT.collidepoint(mouse)

    # Back button
    pill(BACK_RECT, (*tint(place.color, 0.25 if hovering else 0.06), 245), (51, 65, 85))
    back = render_tight('←  Back to Map', 18, TEXT)
    screen.blit(back, back.get_rect(center=BACK_RECT.center))

    # Previous / next buttons when there is more than one photo
    many = len(place.photos) > 1
    if many:
        for center, direction in ((PREV_CENTER, -1), (NEXT_CENTER, 1)):
            over = in_circle(mouse, center)
            hovering = hovering or over
            draw_arrow(center, direction, over)

    # Caption: name, photo count, and a note on stand-in photos
    lines = [render_tight(place.title, 26, WHITE)]
    if many:
        count =render_tight(f'{index + 1} / {len(place.photos)}', 16, (203, 213, 225))
        row = pygame.Surface((lines[0].get_width() + 18 + count.get_width(), lines[0].get_height()), pygame.SRCALPHA)
        row.blit(lines[0], (0, 0))
        row.blit(count, count.get_rect(bottomright=row.get_rect().bottomright))
        lines[0] = row
    if place.stand_in:
        lines.append(render_tight('Stand-in photo – real photo coming soon', 13, (203, 213, 225)))
    caption = stack(lines, 8)
    rect = caption.get_rect().inflate(48, 28)
    rect.midbottom = (WIDTH // 2, HEIGHT - 30)
    pygame.draw.rect(screen, DARK, rect, border_radius=min(rect.height // 2, 28))
    screen.blit(caption, caption.get_rect(center=rect.center))
    return hovering


# ------------------------------------------------------------------ Main loop

current = None          # the place whose photos are open, or None for the map
index = 0               # which of its photos is showing
query = ''              # search text typed on the map
fade = 0                # fade-in strength after the screen changes
fade_overlay = pygame.Surface((WIDTH, HEIGHT))
fade_overlay.fill(DARK)


def show(place, photo_index=0):
    global current, index, fade
    current, index, fade = place, photo_index, 255


while True:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                if current:
                    show(None)
                elif query:
                    query = ''
                elif pygame.display.is_fullscreen():
                    pygame.display.toggle_fullscreen()
            elif current:
                count = len(current.photos)
                if event.key == pygame.K_BACKSPACE:
                    show(None)
                elif event.key == pygame.K_LEFT and count > 1:
                    show(current, (index - 1) % count)
                elif event.key == pygame.K_RIGHT and count > 1:
                    show(current, (index + 1) % count)
            elif event.key == pygame.K_BACKSPACE:
                query = query[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and query:
                found = [p for p in PLACES if matches(p, query.strip().lower())]
                if found:
                    show(found[0])
                    query = ''

        elif event.type == pygame.TEXTINPUT and not current and len(query) < 18:
            query += event.text

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current:
                count = len(current.photos)
                if BACK_RECT.collidepoint(event.pos):
                    show(None)
                elif count > 1 and in_circle(event.pos, PREV_CENTER):
                    show(current, (index - 1) % count)
                elif count > 1 and in_circle(event.pos, NEXT_CENTER):
                    show(current, (index + 1) % count)
            else:
                clicked = next((p for p in PLACES if p.rect.collidepoint(event.pos)), None)
                if clicked:
                    show(clicked)
                    query = ''

    if current:
        clickable = draw_photo(current, index, mouse)
    else:
        clickable = draw_map(mouse, query.strip().lower())
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if clickable else pygame.SYSTEM_CURSOR_ARROW)

    # Fade in whenever the screen changes
    if fade > 0:
        fade_overlay.set_alpha(fade)
        screen.blit(fade_overlay, (0, 0))
        fade -= 30

    pygame.display.update()
