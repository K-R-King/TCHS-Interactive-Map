# TCHS Interactive Map

An interactive campus map of Temple City High School. Click any room or area on the map to see a photo of it — handy for new students, visitors and Back to School Night.

![The interactive map](docs/map.png)

## Features

- **The 2025 campus map** (as of 8/22/25), with every room and area clickable.
- **Color-coded buildings** — each part of campus has its own color, and rooms highlight as you hover over them.
- **Photos of each location**, shown full-window with the room's name.
- **Resizable and fullscreen** — maximize the window or press F11.

![A room's photo](docs/room.jpg)

## Running it

You need [Python 3](https://www.python.org/downloads/) (3.9 or newer).

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Action | How |
| --- | --- |
| Open a room's photo | Click anywhere inside its box on the map |
| Go back to the map | Click **← Back to Map** |
| Fullscreen on / off | **F11** (or maximize the window) |
| Leave fullscreen | **Esc** |

## Project layout

```
main.py              The app
assets/              Campus map and location photos (sized for the app)
TCHS Map 2025.pdf    The original campus map
docs/                Screenshots for this README
```

## Adding or replacing a photo

Some locations still show a stand-in photo. To give a location its own photo:

1. Put the photo in `assets/` (JPEG or PNG).
2. In `main.py`, find the line that loads that location's image (for example `rm_212_image = pygame.image.load('assets/601.jpg')`) and change the file name.

Photos are fitted to the window automatically, so any size or shape works.
