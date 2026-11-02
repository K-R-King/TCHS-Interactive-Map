"""TCHS Interactive Map: click a place on the campus map to see photos of it.

    python main.py            normal window
    python main.py --kiosk    fullscreen, resets itself after a minute without use
"""
import csv
import json
import os
import sys

import pygame

# Load files relative to this script (or the packaged app), wherever it is run from
os.chdir(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))

# Keep Windows display scaling from enlarging the window past the screen edges
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_RENDER_SCALE_QUALITY'] = 'best'

KIOSK = '--kiosk' in sys.argv
KIOSK_RESET_MS = 60_000

pygame.init()
WIDTH, HEIGHT = 1240, 930
# SCALED stretches everything to fill the window when it is resized, maximized or fullscreen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('TCHS Interactive Map')
if KIOSK:
    pygame.display.toggle_fullscreen()
clock = pygame.time.Clock()


# ------------------------------------------------------------------ Colours

TEXT = (30, 41, 59)
SUBTEXT = (71, 85, 105)
MUTED = (100, 116, 139)
DARK = (15, 23, 42)
WHITE = (255, 255, 255)
BLUE = (37, 99, 235)
RED = (220, 38, 38)


# Mix a colour with white; amount 0 = white, 1 = the full colour
def tint(color, amount):
    return tuple(round(255 + (c - 255) * amount) for c in color)


def hex_color(text):
    return tuple(int(text[i:i + 2], 16) for i in (1, 3, 5))


# ------------------------------------------------------------------ Places

with open('data/places.json', encoding='utf-8') as f:
    DATA = json.load(f)
ZONES = {name: hex_color(value) for name, value in DATA['zones'].items()}

# Teachers and subjects, kept in a spreadsheet so anyone can edit them.
# The packaged app also checks for a rooms.csv next to the .exe, so it can be updated without rebuilding.
ROOM_INFO = {}
rooms_csv = os.path.join(os.path.dirname(sys.executable), 'rooms.csv') if getattr(sys, 'frozen', False) else ''
for path in (rooms_csv, 'data/rooms.csv'):
    if path and os.path.exists(path):
        with open(path, encoding='utf-8-sig', newline='') as f:
            ROOM_INFO = {row['id']: row for row in csv.DictReader(f)}
        break


class Place:
    """A spot on campus and its photos. Places on the map have a box; extras don't."""

    def __init__(self, info):
        self.id = info['id']
        self.label = info.get('label', info.get('title', ''))
        self.kind = info['kind']
        self.color = ZONES.get(info.get('zone'), ZONES['teal'])
        self.box = pygame.Rect(info['box']) if 'box' in info else None
        self.shape = info.get('shape', 'box')
        self.note = info.get('note')
        title = info.get('title') or (f'Room {self.label}' if self.label[:1].isdigit() else self.label)
        self.title = f'{title} – {self.note}' if self.note else title
        extra = ROOM_INFO.get(self.id, {})
        self.teacher = (extra.get('teacher') or '').strip()
        self.subject = (extra.get('subject') or '').strip()
        self.details = ' · '.join(x for x in (self.teacher, self.subject, (extra.get('notes') or '').strip()) if x)
        folder = f'assets/photos/{self.id}'
        files = sorted(f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))) \
            if os.path.isdir(folder) else []
        self.photos = [f'{folder}/{f}' for f in files] or [DATA['stand_in']]
        self.stand_in = not files
        self.search_text = ' '.join([self.id, self.label, self.title, self.details]).lower()
        self.glow = 0.0          # hover highlight, eased in and out
        self.labels = {}         # rendered label for each zoom level

    def matches(self, query):
        return all(word in self.search_text for word in query.split())


PLACES = [Place(p) for p in DATA['places']]
EXTRAS = [Place(p) for p in DATA['extras']]


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
def render_label(text, w, h, note=None, max_size=19, big_size=24):
    max_w, max_h = w - (6 if w > 40 else 3), h - 3
    note_image = None
    if note:
        for size in range(max(9, max_size // 2), 6, -1):
            note_image = stack([render_tight(line, size, SUBTEXT) for line in wrap(note, size, max_w)], 1)
            if note_image.get_width() <= max_w:
                break
        max_h -= note_image.get_height() + 3
    # Tall, narrow boxes get sideways text, like the printed map
    sideways = max_h > 2 * max_w and ' ' in text
    if sideways:
        max_w, max_h = max_h, max_w
    # One size for regular rooms so rows match; larger only for big areas
    top = big_size if min(max_w, max_h) >= 56 * big_size / 24 else max_size
    for size in range(top, 6, -1):
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


def place_label(place, zoom):
    """The place's label, rendered sharp for the current zoom level."""
    if zoom not in place.labels:
        w, h = place.box.width * zoom, place.box.height * zoom
        if place.shape == 'circle':
            w, h = w * 0.85, h * 0.65   # keep the text inside the curve
        place.labels[zoom] = render_label(place.label, int(w), int(h), place.note,
                                          max_size=round(19 * zoom), big_size=round(24 * zoom))
    return place.labels[zoom]


# ------------------------------------------------------------------ Map view (zoom and pan)

ZOOMS = [1, 1.5, 2, 3]
map_hd = pygame.image.load(DATA['map']).convert()
map_scaled = {}


def map_at(zoom):
    if zoom not in map_scaled:
        size = (round(WIDTH * zoom), round(HEIGHT * zoom))
        map_scaled[zoom] = pygame.transform.smoothscale(map_hd, size)
    return map_scaled[zoom]


class View:
    zoom = 1
    x = y = 0       # top-left corner of the screen, in zoomed map pixels

    @classmethod
    def clamp(cls):
        cls.x = max(0, min(cls.x, WIDTH * cls.zoom - WIDTH))
        cls.y = max(0, min(cls.y, HEIGHT * cls.zoom - HEIGHT))

    @classmethod
    def zoom_to(cls, zoom, around=(WIDTH / 2, HEIGHT / 2)):
        """Change zoom, keeping the map point under `around` in place."""
        scale = zoom / cls.zoom
        cls.x = (around[0] + cls.x) * scale - around[0]
        cls.y = (around[1] + cls.y) * scale - around[1]
        cls.zoom = zoom
        cls.clamp()

    @classmethod
    def step(cls, direction, around=(WIDTH / 2, HEIGHT / 2)):
        i = max(0, min(len(ZOOMS) - 1, ZOOMS.index(cls.zoom) + direction))
        cls.zoom_to(ZOOMS[i], around)

    @classmethod
    def to_screen(cls, rect):
        z = cls.zoom
        return pygame.Rect(round(rect.x * z - cls.x), round(rect.y * z - cls.y), round(rect.w * z), round(rect.h * z))

    @classmethod
    def to_map(cls, pos):
        return ((pos[0] + cls.x) / cls.zoom, (pos[1] + cls.y) / cls.zoom)


# ------------------------------------------------------------------ Photos

photo_cache = {}


# Load a photo the first time it is shown, fitted to the window without stretching
def photo(path):
    if path not in photo_cache:
        image = pygame.image.load(path).convert()
        scale = min(WIDTH / image.get_width(), HEIGHT / image.get_height())
        size = (round(image.get_width() * scale), round(image.get_height() * scale))
        canvas = pygame.Surface((WIDTH, HEIGHT))
        canvas.fill(DARK)
        scaled = pygame.transform.smoothscale(image, size)
        canvas.blit(scaled, scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        photo_cache[path] = canvas
    return photo_cache[path]


# ------------------------------------------------------------------ Controls

SEARCH_RECT = pygame.Rect(24, 126, 220, 36)
CHIPS = [('restroom', 'Restrooms'), ('office', 'Offices'), ('athletics', 'Athletics'), ('entrance', 'Entrances'),
         ('more', 'More places')]
CHIP_RECTS = {}
x = SEARCH_RECT.right + 10
for key, text in CHIPS:
    w = font(14).size(text)[0] + 28
    CHIP_RECTS[key] = pygame.Rect(x, SEARCH_RECT.y + 2, w, SEARCH_RECT.h - 4)
    x += w + 8
ZOOM_IN = pygame.Rect(24, 760, 40, 40)
ZOOM_OUT = pygame.Rect(24, 806, 40, 40)
ZOOM_RESET = pygame.Rect(72, 806, 84, 40)
BACK_RECT = pygame.Rect(24, 20, 170, 46)
PREV_CENTER = (60, HEIGHT // 2)
NEXT_CENTER = (WIDTH - 60, HEIGHT // 2)
ARROW_RADIUS = 28
PANEL = pygame.Rect(0, 0, 520, 140 + 52 * len(EXTRAS))
PANEL.center = (WIDTH // 2, HEIGHT // 2)
PANEL_CLOSE = pygame.Rect(PANEL.right - 52, PANEL.y + 16, 36, 36)
EXTRA_ROWS = [pygame.Rect(PANEL.x + 20, PANEL.y + 96 + 52 * i, PANEL.w - 40, 46) for i in range(len(EXTRAS))]


def pill(rect, fill, border=None, width=1, radius=None):
    """Draw a rounded, possibly translucent, rectangle."""
    radius = rect.height // 2 if radius is None else radius
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(surface, fill, surface.get_rect(), border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, surface.get_rect(), width, border_radius=radius)
    screen.blit(surface, rect)


def shadow(rect, radius, strength=60):
    for i in range(6, 0, -2):
        pill(rect.inflate(i * 2, i * 2).move(0, 3), (0, 0, 0, strength // i), radius=radius + i)


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


def round_button(rect, hovered, symbol):
    shadow(rect, 10, 40)
    pill(rect, (*WHITE, 250), (148, 163, 184), radius=10)
    if hovered:
        pill(rect, (*tint(BLUE, 0.12), 255), BLUE, radius=10)
    cx, cy = rect.center
    if symbol in '+-':
        pygame.draw.line(screen, TEXT, (cx - 9, cy), (cx + 9, cy), 3)
        if symbol == '+':
            pygame.draw.line(screen, TEXT, (cx, cy - 9), (cx, cy + 9), 3)
    else:
        text = render_tight(symbol, 14, TEXT)
        screen.blit(text, text.get_rect(center=rect.center))


# ------------------------------------------------------------------ Drawing the map

def highlighted(place, query, chip):
    if query:
        return place.matches(query)
    if chip:
        return place.kind == chip
    return None     # nothing being searched for


def draw_place(place, hovered, query, chip):
    rect = View.to_screen(place.box)
    if not rect.colliderect(screen.get_rect()):
        return
    place.glow += ((1 if hovered else 0) - place.glow) * 0.3
    found = highlighted(place, query, chip)
    dimmed = found is False
    if dimmed:
        fill, border, width = (241, 245, 249), (203, 213, 225), 1
    else:
        strength = 0.45 if found else 0.12 + 0.3 * place.glow
        fill, border = tint(place.color, strength), place.color
        width = 2 if hovered or found else 1
    box = rect.inflate(-2, -2)
    if place.shape == 'circle':
        pygame.draw.ellipse(screen, fill, box)
        pygame.draw.ellipse(screen, border, box, width)
    else:
        radius = box.height // 2 if place.shape == 'tag' else max(2, min(round(8 * View.zoom), box.width // 4, box.height // 4))
        pygame.draw.rect(screen, fill, box, border_radius=radius)
        pygame.draw.rect(screen, border, box, width, border_radius=radius)
    label = place_label(place, View.zoom)
    label.set_alpha(70 if dimmed else 255)
    screen.blit(label, label.get_rect(center=rect.center))
    # A pulsing ring makes search results easy to spot, even tiny ones
    if found:
        pulse = 3 + 3 * abs((pygame.time.get_ticks() % 1000) / 500 - 1)
        ring = rect.inflate(2 * pulse, 2 * pulse)
        if place.shape == 'circle':
            pygame.draw.ellipse(screen, place.color, ring, 2)
        else:
            pygame.draw.rect(screen, place.color, ring, 2, border_radius=8)


def draw_toolbar(query, chip, mouse, count):
    # Search box
    active = bool(query)
    shadow(SEARCH_RECT, SEARCH_RECT.h // 2, 40)
    pill(SEARCH_RECT, (*WHITE, 250), BLUE if active else (148, 163, 184), 2 if active else 1)
    cx, cy = SEARCH_RECT.x + 18, SEARCH_RECT.centery - 2
    pygame.draw.circle(screen, SUBTEXT, (cx, cy), 6, 2)
    pygame.draw.line(screen, SUBTEXT, (cx + 4, cy + 4), (cx + 9, cy + 9), 3)
    if query:
        text = render_tight(query[-22:], 15, TEXT)
        x = SEARCH_RECT.x + 34
        screen.blit(text, text.get_rect(midleft=(x, SEARCH_RECT.centery)))
        if pygame.time.get_ticks() // 500 % 2:
            caret_x = x + text.get_width() + 2
            pygame.draw.line(screen, TEXT, (caret_x, SEARCH_RECT.centery - 9), (caret_x, SEARCH_RECT.centery + 9), 1)
        hint = render_tight(f'{count} found' if count else 'no match', 11, SUBTEXT if count else RED)
        screen.blit(hint, hint.get_rect(midright=(SEARCH_RECT.right - 14, SEARCH_RECT.centery)))
    else:
        hint = render_tight('Room, place or teacher', 13, MUTED)
        screen.blit(hint, hint.get_rect(midleft=(SEARCH_RECT.x + 34, SEARCH_RECT.centery)))

    # Quick-find chips
    for key, text in CHIPS:
        rect = CHIP_RECTS[key]
        on = chip == key
        over = rect.collidepoint(mouse)
        shadow(rect, rect.h // 2, 30)
        pill(rect, (*(BLUE if on else tint(BLUE, 0.1) if over else WHITE), 250), BLUE if on or over else (148, 163, 184))
        label = render_tight(text, 14, WHITE if on else TEXT)
        screen.blit(label, label.get_rect(center=rect.center))

    # Zoom
    round_button(ZOOM_IN, ZOOM_IN.collidepoint(mouse), '+')
    round_button(ZOOM_OUT, ZOOM_OUT.collidepoint(mouse), '-')
    if View.zoom != 1:
        round_button(ZOOM_RESET, ZOOM_RESET.collidepoint(mouse), 'Reset')


def draw_tooltip(place, pos):
    lines = [render_tight(place.title, 14, WHITE)]
    if place.details:
        lines.append(render_tight(place.details, 12, (203, 213, 225)))
    label = stack(lines, 5)
    rect = label.get_rect().inflate(22, 16)
    rect.midbottom = (pos[0], pos[1] - 14)
    rect.clamp_ip(screen.get_rect().inflate(-8, -8))
    pill(rect, (*DARK, 235), radius=min(rect.h // 2, 14))
    screen.blit(label, label.get_rect(center=rect.center))


def draw_kiosk_banner():
    rect = pygame.Rect(0, 0, 560, 52)
    rect.midbottom = (WIDTH // 2, HEIGHT - 24)
    glow = 200 + 55 * abs((pygame.time.get_ticks() % 2000) / 1000 - 1)
    shadow(rect, 26)
    pill(rect, (*DARK, int(glow)))
    text = render_tight('Tap a room – or type a room number or teacher', 20, WHITE)
    screen.blit(text, text.get_rect(center=rect.center))


def draw_more_panel(mouse):
    dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim.fill((*DARK, 140))
    screen.blit(dim, (0, 0))
    shadow(PANEL, 18, 80)
    pill(PANEL, (*WHITE, 255), radius=18)
    title = render_tight('More places', 26, TEXT)
    screen.blit(title, (PANEL.x + 24, PANEL.y + 26))
    sub = render_tight('Photos of places that aren’t outlined on the map', 13, MUTED)
    screen.blit(sub, (PANEL.x + 24, PANEL.y + 64))
    over_close = PANEL_CLOSE.collidepoint(mouse)
    pill(PANEL_CLOSE, (*tint(TEXT, 0.12 if over_close else 0.05), 255))
    c = PANEL_CLOSE.center
    pygame.draw.line(screen, TEXT, (c[0] - 7, c[1] - 7), (c[0] + 7, c[1] + 7), 3)
    pygame.draw.line(screen, TEXT, (c[0] - 7, c[1] + 7), (c[0] + 7, c[1] - 7), 3)
    for place, rect in zip(EXTRAS, EXTRA_ROWS):
        over = rect.collidepoint(mouse)
        pill(rect, (*tint(BLUE, 0.1 if over else 0.03), 255), BLUE if over else (226, 232, 240), radius=10)
        name = render_tight(place.title, 17, TEXT)
        screen.blit(name, name.get_rect(midleft=(rect.x + 16, rect.centery)))
        n = len(place.photos)
        count = render_tight(f'{n} photo{"s" if n != 1 else ""}  ›', 13, MUTED)
        screen.blit(count, count.get_rect(midright=(rect.right - 16, rect.centery)))
    return over_close or any(r.collidepoint(mouse) for r in EXTRA_ROWS)


def draw_map(mouse, query, chip, panel_open):
    screen.blit(map_at(View.zoom), (-round(View.x), -round(View.y)))
    over_ui = not panel_open and (SEARCH_RECT.collidepoint(mouse) or ZOOM_IN.collidepoint(mouse)
                                  or ZOOM_OUT.collidepoint(mouse) or (View.zoom != 1 and ZOOM_RESET.collidepoint(mouse))
                                  or any(r.collidepoint(mouse) for r in CHIP_RECTS.values()))
    map_pos = View.to_map(mouse)
    hovered = None
    if not panel_open and not over_ui:
        hovered = next((p for p in PLACES if p.box.collidepoint(map_pos)), None)
    for place in PLACES:
        draw_place(place, place is hovered, query, chip)
    count = sum(p.matches(query) for p in PLACES + EXTRAS) if query else 0
    draw_toolbar(query, chip, mouse, count)
    if KIOSK and not query and not chip and not panel_open:
        draw_kiosk_banner()
    if hovered:
        draw_tooltip(hovered, mouse)
    if panel_open:
        return draw_more_panel(mouse)
    return hovered is not None or (over_ui and not SEARCH_RECT.collidepoint(mouse))


def draw_photo(place, index, mouse):
    screen.blit(photo(place.photos[index]), (0, 0))
    hovering = BACK_RECT.collidepoint(mouse)

    # Back button
    shadow(BACK_RECT, BACK_RECT.h // 2)
    pill(BACK_RECT, (*tint(place.color, 0.25 if hovering else 0.06), 250), (51, 65, 85))
    back = render_tight('←  Back to Map', 18, TEXT)
    screen.blit(back, back.get_rect(center=BACK_RECT.center))

    # Previous / next buttons when there is more than one photo
    many = len(place.photos) > 1
    if many:
        for center, direction in ((PREV_CENTER, -1), (NEXT_CENTER, 1)):
            over = in_circle(mouse, center)
            hovering = hovering or over
            draw_arrow(center, direction, over)

    # Caption: name, photo count, teacher and subject, and a note on stand-in photos
    lines = [render_tight(place.title, 26, WHITE)]
    if many:
        count = render_tight(f'{index + 1} / {len(place.photos)}', 16, (203, 213, 225))
        row = pygame.Surface((lines[0].get_width() + 18 + count.get_width(), lines[0].get_height()), pygame.SRCALPHA)
        row.blit(lines[0], (0, 0))
        row.blit(count, count.get_rect(bottomright=row.get_rect().bottomright))
        lines[0] = row
    if place.details:
        lines.append(render_tight(place.details, 17, (226, 232, 240)))
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
chip = None             # quick-find filter: 'restroom', 'office', 'athletics' or 'entrance'
panel_open = False      # the "More places" list
press = None            # where the mouse went down on the map, to tell clicks from drags
dragging = False
fade = 0                # fade-in strength after the screen changes
fade_overlay = pygame.Surface((WIDTH, HEIGHT))
fade_overlay.fill(DARK)
last_input = 0
cursor = None


def show(place, photo_index=0):
    global current, index, fade
    current, index, fade = place, photo_index, 255


def reset():
    """Back to a fresh map, as a new visitor would want it."""
    global query, chip, panel_open
    show(None)
    query, chip, panel_open = '', None, False
    View.zoom, View.x, View.y = 1, 0, 0


def click_map(pos):
    """Handle a click (not a drag) on the map screen."""
    global query, chip, panel_open
    if panel_open:
        if PANEL_CLOSE.collidepoint(pos) or not PANEL.collidepoint(pos):
            panel_open = False
        for place, rect in zip(EXTRAS, EXTRA_ROWS):
            if rect.collidepoint(pos):
                panel_open = False
                show(place)
        return
    for key, rect in CHIP_RECTS.items():
        if rect.collidepoint(pos):
            if key == 'more':
                panel_open = True
            else:
                chip = None if chip == key else key
                query = ''
            return
    if ZOOM_IN.collidepoint(pos):
        View.step(1)
    elif ZOOM_OUT.collidepoint(pos):
        View.step(-1)
    elif View.zoom != 1 and ZOOM_RESET.collidepoint(pos):
        View.zoom_to(1)
    elif not SEARCH_RECT.collidepoint(pos):
        map_pos = View.to_map(pos)
        clicked = next((p for p in PLACES if p.box.collidepoint(map_pos)), None)
        if clicked:
            show(clicked)


while True:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type in (pygame.KEYDOWN, pygame.TEXTINPUT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.MOUSEMOTION):
            last_input = now

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                if current:
                    show(None)
                elif panel_open:
                    panel_open = False
                elif query or chip:
                    query, chip = '', None
                elif View.zoom != 1:
                    View.zoom_to(1)
                elif pygame.display.is_fullscreen() and not KIOSK:
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
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and query.strip():
                found = [p for p in PLACES + EXTRAS if p.matches(query.strip().lower())]
                if found:
                    show(found[0])
                    query = ''
            elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS) and not query:
                View.step(1)
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS) and not query:
                View.step(-1)

        elif event.type == pygame.TEXTINPUT and not current and not panel_open:
            if event.text in '+=-' and not query:
                continue    # handled as zoom keys
            if len(query) < 30:
                query += event.text
                chip = None

        elif event.type == pygame.MOUSEWHEEL and not current and not panel_open:
            View.step(1 if event.y > 0 else -1, mouse)

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
                press, dragging = event.pos, False

        elif event.type == pygame.MOUSEMOTION and press and not current:
            if not dragging and abs(event.pos[0] - press[0]) + abs(event.pos[1] - press[1]) > 6 and View.zoom != 1:
                dragging = True
            if dragging:
                View.x -= event.rel[0]
                View.y -= event.rel[1]
                View.clamp()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and press:
            if not dragging and not current:
                click_map(event.pos)
            press, dragging = None, False

    if KIOSK and now - last_input > KIOSK_RESET_MS and (current or query or chip or panel_open or View.zoom != 1):
        reset()

    if current:
        clickable = draw_photo(current, index, mouse)
    else:
        clickable = draw_map(mouse, query.strip().lower(), chip, panel_open)
    wanted = pygame.SYSTEM_CURSOR_SIZEALL if dragging else pygame.SYSTEM_CURSOR_HAND if clickable else pygame.SYSTEM_CURSOR_ARROW
    if wanted != cursor:
        pygame.mouse.set_cursor(wanted)
        cursor = wanted

    # Fade in whenever the screen changes
    if fade > 0:
        fade_overlay.set_alpha(fade)
        screen.blit(fade_overlay, (0, 0))
        fade -= 30

    pygame.display.update()
