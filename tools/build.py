"""Rebuild the generated files after adding photos or editing data/places.json.

    python tools/build.py

Writes:
  data/photos.json      the photos in each place's folder (the website reads this)
  PHOTO-CHECKLIST.md    every place that still needs a photo, to take around campus
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_TYPES = ('.jpg', '.jpeg', '.png')
KIND_NAMES = {'room': 'Classrooms', 'restroom': 'Restrooms', 'office': 'Offices', 'athletics': 'Athletics',
              'outdoor': 'Outdoor areas', 'entrance': 'Entrances', 'other': 'Other'}


def place_name(place):
    label = place.get('label', '')
    return place.get('title') or (f'Room {label}' if label[:1].isdigit() else label)


def main():
    os.chdir(ROOT)
    with open('data/places.json', encoding='utf-8') as f:
        data = json.load(f)
    everything = data['places'] + data['extras']

    photos = {}
    for place in everything:
        folder = f'assets/photos/{place["id"]}'
        os.makedirs(folder, exist_ok=True)
        files = sorted(f for f in os.listdir(folder) if f.lower().endswith(PHOTO_TYPES))
        photos[place['id']] = [f'{folder}/{f}' for f in files]
    with open('data/photos.json', 'w', encoding='utf-8') as f:
        json.dump(photos, f, indent=1, ensure_ascii=False)

    missing = [p for p in data['places'] if not photos[p['id']]]
    lines = ['# Photo checklist', '',
             f'{len(missing)} places on the map still show a stand-in photo. Take a photo of each '
             '(the doorway or entrance works best), put it in that place\'s folder, then run '
             '`python tools/build.py`.', '']
    for kind, heading in KIND_NAMES.items():
        group = [p for p in missing if p['kind'] == kind]
        if not group:
            continue
        lines += [f'## {heading}', '']
        lines += [f'- [ ] **{place_name(p)}** — `assets/photos/{p["id"]}/`' for p in group]
        lines.append('')
    with open('PHOTO-CHECKLIST.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    total = sum(len(v) for v in photos.values())
    print(f'{total} photos in {len(photos)} places; {len(missing)} places still need a photo')


if __name__ == '__main__':
    main()
