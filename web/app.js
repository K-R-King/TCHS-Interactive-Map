// TCHS Campus Map: the web version of main.py.
// Reads the same data files: data/places.json, data/photos.json and data/rooms.csv.
'use strict';

const MAP_W = 1240, MAP_H = 930;
const KIOSK = new URLSearchParams(location.search).has('kiosk');
const KIOSK_RESET_MS = 60_000;

const $ = (selector) => document.querySelector(selector);
const viewport = $('#viewport'), stage = $('#stage'), search = $('#search'), results = $('#results');
const viewer = $('#viewer'), photoEl = $('#photo'), tooltip = $('#tooltip');

let places = [], extras = [], byId = new Map();
let view = { scale: 1, x: 0, y: 0, min: 1 };
let kind = null;                // quick-find filter
let open = null, index = 0;     // the place being viewed and which photo
let openedInApp = false;        // so Back can return to the map with history.back()

// ------------------------------------------------------------------ Data

function parseCSV(text) {
  const rows = [];
  let row = [], field = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(field); rows.push(row); row = []; field = '';
    } else field += c;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  const [head, ...body] = rows.filter((r) => r.some((f) => f.trim()));
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h.trim().replace(/^﻿/, ''), (r[i] || '').trim()])));
}

function makePlace(info, data, photos, rooms) {
  const label = info.label || info.title;
  let title = info.title || (/^\d/.test(label) ? `Room ${label}` : label);
  if (info.note) title += ` – ${info.note}`;
  const room = rooms.get(info.id) || {};
  const details = [room.teacher, room.subject, room.notes].filter(Boolean).join(' · ');
  const own = photos[info.id] || [];
  return {
    ...info, label, title, details,
    color: data.zones[info.zone] || data.zones.teal,
    photos: own.length ? own : [data.stand_in],
    standIn: !own.length,
    search: [info.id, label, title, details].join(' ').toLowerCase(),
  };
}

const matches = (place, query) => query.split(/\s+/).every((word) => place.search.includes(word));

// ------------------------------------------------------------------ Map buttons

function buildPlaces() {
  for (const place of places) {
    const [x, y, w, h] = place.box;
    const el = document.createElement('button');
    el.type = 'button';
    el.className = `place ${place.shape || 'box'}`;
    el.style.cssText = `left:${x}px;top:${y}px;width:${w}px;height:${h}px;--c:${place.color}`;
    el.setAttribute('aria-label', place.details ? `${place.title}, ${place.details}` : place.title);
    el.dataset.id = place.id;
    el.innerHTML = '<span class="label"></span>';
    el.firstChild.textContent = place.label;
    if (place.note) {
      const note = document.createElement('span');
      note.className = 'note';
      note.textContent = place.note;
      el.append(note);
    }
    // Tall, narrow boxes get sideways text, like the printed map
    if (h > 2 * w && place.label.includes(' ')) el.classList.add('sideways');
    stage.append(el);
    place.el = el;
  }
}

// Make each label as large as fits its box; one size for regular rooms so rows match
function fitLabels() {
  for (const place of places) {
    const el = place.el, label = el.querySelector('.label'), note = el.querySelector('.note');
    const [, , w, h] = place.box;
    const big = Math.min(w, h) >= 56 && place.shape !== 'tag';
    let size = big ? 24 : 19;
    // Fits when no word spills out of the label and the label (plus note) fits inside the box
    const fits = () => label.scrollWidth <= label.clientWidth + 0.5
      && label.offsetWidth <= el.clientWidth - 2
      && label.offsetHeight + (note ? note.offsetHeight + 1 : 0) <= el.clientHeight - 1;
    const set = () => {
      label.style.fontSize = `${size}px`;
      if (note) note.style.fontSize = `${Math.max(6, Math.min(9, size / 2))}px`;
    };
    set();
    while (!fits() && size > 5) { size -= 0.5; set(); }
  }
}

// ------------------------------------------------------------------ Zoom and pan

function apply() {
  stage.style.transform = `translate(${view.x}px, ${view.y}px) scale(${view.scale})`;
}

function clamp() {
  const vw = viewport.clientWidth, vh = viewport.clientHeight;
  const w = MAP_W * view.scale, h = MAP_H * view.scale;
  view.x = w <= vw ? (vw - w) / 2 : Math.min(0, Math.max(vw - w, view.x));
  view.y = h <= vh ? (vh - h) / 2 : Math.min(0, Math.max(vh - h, view.y));
}

function fit() {
  view.min = Math.min(viewport.clientWidth / MAP_W, viewport.clientHeight / MAP_H);
  view.scale = view.min;
  clamp(); apply();
}

function zoomAt(clientX, clientY, factor) {
  const rect = viewport.getBoundingClientRect();
  const px = clientX - rect.left, py = clientY - rect.top;
  const scale = Math.min(Math.max(view.scale * factor, view.min), Math.max(view.min * 6, 3));
  const k = scale / view.scale;
  view.x = px - (px - view.x) * k;
  view.y = py - (py - view.y) * k;
  view.scale = scale;
  clamp(); apply();
}

function zoomCenter(factor) {
  const rect = viewport.getBoundingClientRect();
  stage.style.transition = 'transform .2s ease';
  zoomAt(rect.left + rect.width / 2, rect.top + rect.height / 2, factor);
  setTimeout(() => { stage.style.transition = ''; }, 220);
}

// Drag to pan, pinch or scroll to zoom, tap to open
const pointers = new Map();
let gesture = null;

viewport.addEventListener('pointerdown', (e) => {
  if (e.target.closest('.zoom')) return;
  viewport.setPointerCapture(e.pointerId);
  pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  if (pointers.size === 1) gesture = { startX: e.clientX, startY: e.clientY, moved: false };
  else if (gesture) gesture.moved = true;   // a second finger means pinch, not tap
  hideTooltip();
});

viewport.addEventListener('pointermove', (e) => {
  if (!pointers.has(e.pointerId)) {
    if (e.pointerType === 'mouse') showTooltip(e);
    return;
  }
  const prev = pointers.get(e.pointerId);
  if (pointers.size === 1) {
    if (Math.hypot(e.clientX - gesture.startX, e.clientY - gesture.startY) > 6) gesture.moved = true;
    if (gesture.moved) {
      viewport.classList.add('dragging');
      view.x += e.clientX - prev.x;
      view.y += e.clientY - prev.y;
      clamp(); apply();
    }
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  } else if (pointers.size === 2) {
    const [a, b] = [...pointers.values()];
    const before = Math.hypot(a.x - b.x, a.y - b.y);
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    const [c, d] = [...pointers.values()];
    const after = Math.hypot(c.x - d.x, c.y - d.y);
    const mid = { x: (c.x + d.x) / 2, y: (c.y + d.y) / 2 };
    view.x += mid.x - (a.x + b.x) / 2;
    view.y += mid.y - (a.y + b.y) / 2;
    if (before > 0) zoomAt(mid.x, mid.y, after / before);
  }
});

function endPointer(e) {
  if (!pointers.has(e.pointerId)) return;
  pointers.delete(e.pointerId);
  if (pointers.size === 0) {
    viewport.classList.remove('dragging');
    if (gesture && !gesture.moved && e.type === 'pointerup') {
      const el = document.elementFromPoint(e.clientX, e.clientY)?.closest('.place');
      if (el) openPlace(byId.get(el.dataset.id));
    }
    gesture = null;
  }
}
viewport.addEventListener('pointerup', endPointer);
viewport.addEventListener('pointercancel', endPointer);
viewport.addEventListener('wheel', (e) => {
  e.preventDefault();
  zoomAt(e.clientX, e.clientY, Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0018)));
}, { passive: false });
viewport.addEventListener('dblclick', (e) => {
  if (!e.target.closest('.place, .zoom')) zoomAt(e.clientX, e.clientY, 1.8);
});
viewport.addEventListener('pointerleave', hideTooltip);

$('#zoom-in').addEventListener('click', () => zoomCenter(1.5));
$('#zoom-out').addEventListener('click', () => zoomCenter(1 / 1.5));
$('#zoom-fit').addEventListener('click', () => { stage.style.transition = 'transform .25s ease'; fit(); setTimeout(() => { stage.style.transition = ''; }, 260); });
window.addEventListener('resize', () => { const old = view.min; fit(); if (old) clamp(); });

// Hover tooltips with the full name and teacher
function showTooltip(e) {
  const el = e.target.closest?.('.place');
  if (!el) return hideTooltip();
  const place = byId.get(el.dataset.id);
  const rect = viewport.getBoundingClientRect();
  tooltip.innerHTML = '';
  tooltip.append(place.title);
  if (place.details) {
    const small = document.createElement('small');
    small.textContent = place.details;
    tooltip.append(small);
  }
  tooltip.style.left = `${Math.min(Math.max(e.clientX - rect.left, 140), rect.width - 140)}px`;
  tooltip.style.top = `${Math.max(e.clientY - rect.top, 60)}px`;
  tooltip.hidden = false;
}
function hideTooltip() { tooltip.hidden = true; }

// ------------------------------------------------------------------ Search and quick find

function highlight() {
  const query = search.value.trim().toLowerCase();
  const found = query ? [...places, ...extras].filter((p) => matches(p, query)) : [];
  for (const place of places) {
    const on = query ? found.includes(place) : kind ? place.kind === kind : null;
    place.el.classList.toggle('match', on === true);
    place.el.classList.toggle('dim', on === false);
  }
  document.querySelectorAll('.chips [data-kind]').forEach((b) => b.classList.toggle('on', b.dataset.kind === kind));

  const count = $('#count');
  count.textContent = query ? (found.length ? `${found.length} found` : 'no match') : '';
  count.classList.toggle('none', !!query && !found.length);

  results.innerHTML = '';
  results.hidden = !query || !found.length || document.activeElement !== search;
  found.slice(0, 8).forEach((place, i) => {
    const li = document.createElement('li');
    li.setAttribute('role', 'option');
    li.style.setProperty('--c', place.color);
    if (i === 0) li.classList.add('active');
    li.innerHTML = '<span class="dot"></span><span><span class="name"></span><span class="info"></span></span>';
    li.querySelector('.name').textContent = place.title;
    li.querySelector('.info').textContent = place.details || (place.box ? '' : 'More places');
    li.addEventListener('pointerdown', (e) => { e.preventDefault(); openPlace(place); });
    results.append(li);
  });
  return found;
}

search.addEventListener('input', () => { kind = null; highlight(); });
search.addEventListener('focus', highlight);
search.addEventListener('blur', () => { results.hidden = true; });
search.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    const found = highlight();
    if (found.length) openPlace(found[0]);
  } else if (e.key === 'Escape') {
    search.value = ''; highlight(); search.blur();
  }
});

document.querySelectorAll('.chips [data-kind]').forEach((button) => {
  button.addEventListener('click', () => {
    kind = kind === button.dataset.kind ? null : button.dataset.kind;
    search.value = '';
    highlight();
  });
});

// ------------------------------------------------------------------ Photo viewer

function openPlace(place, photoIndex = 0) {
  results.hidden = true;
  search.blur();
  if (location.hash.slice(1) !== place.id) {
    openedInApp = true;
    location.hash = place.id;
  }
  show(place, photoIndex);
}

function show(place, photoIndex = 0) {
  open = place;
  index = photoIndex;
  const many = place.photos.length > 1;
  $('#viewer-title').textContent = place.title;
  $('#viewer-count').textContent = many ? `${index + 1} / ${place.photos.length}` : '';
  $('#viewer-details').textContent = place.details;
  $('#viewer-details').hidden = !place.details;
  $('#viewer-note').hidden = !place.standIn;
  $('#viewer-prev').hidden = $('#viewer-next').hidden = !many;
  photoEl.src = encodeURI(place.photos[index]);
  photoEl.alt = place.title;
  photoEl.classList.remove('swap'); void photoEl.offsetWidth; photoEl.classList.add('swap');
  viewer.hidden = false;
  document.title = `${place.title} – TCHS Campus Map`;
  // Load the neighbouring photos so swiping feels instant
  for (const i of [index + 1, index - 1]) {
    const path = place.photos[(i + place.photos.length) % place.photos.length];
    new Image().src = encodeURI(path);
  }
}

function step(direction) {
  if (open && open.photos.length > 1) show(open, (index + direction + open.photos.length) % open.photos.length);
}

function closeViewer() {
  if (!open) return;
  if (openedInApp) history.back();
  else { history.replaceState(null, '', location.pathname + location.search); route(); }
}

function route() {
  const place = byId.get(decodeURIComponent(location.hash.slice(1)));
  if (place) show(place, 0);
  else {
    open = null;
    viewer.hidden = true;
    document.title = 'TCHS Campus Map';
  }
}
window.addEventListener('hashchange', route);

$('#viewer-back').addEventListener('click', closeViewer);
$('#viewer-prev').addEventListener('click', () => step(-1));
$('#viewer-next').addEventListener('click', () => step(1));
$('#viewer-share').addEventListener('click', async () => {
  const url = location.href;
  try {
    if (navigator.share) await navigator.share({ title: open.title, url });
    else { await navigator.clipboard.writeText(url); toast('Link copied'); }
  } catch { /* share sheet closed */ }
});

// Swipe between photos
let swipe = null;
viewer.addEventListener('pointerdown', (e) => { if (e.target === photoEl) swipe = { x: e.clientX, y: e.clientY }; });
viewer.addEventListener('pointerup', (e) => {
  if (!swipe) return;
  const dx = e.clientX - swipe.x, dy = e.clientY - swipe.y;
  if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) step(dx < 0 ? 1 : -1);
  swipe = null;
});

function toast(text) {
  const el = $('#toast');
  el.textContent = text;
  el.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => { el.hidden = true; }, 1800);
}

// ------------------------------------------------------------------ More places

function buildMore() {
  const list = $('#more-list');
  for (const place of extras) {
    const li = document.createElement('li');
    const button = document.createElement('button');
    button.type = 'button';
    button.append(place.title);
    const count = document.createElement('span');
    const n = place.photos.length;
    count.textContent = `${n} photo${n === 1 ? '' : 's'} ›`;
    button.append(count);
    button.addEventListener('click', () => { $('#more').hidden = true; openPlace(place); });
    li.append(button);
    list.append(li);
  }
}
$('#more-button').addEventListener('click', () => { $('#more').hidden = false; $('#more-close').focus(); });
$('#more-close').addEventListener('click', () => { $('#more').hidden = true; });
$('#more').addEventListener('click', (e) => { if (e.target.id === 'more') $('#more').hidden = true; });

// ------------------------------------------------------------------ Keyboard

document.addEventListener('keydown', (e) => {
  if (open) {
    if (e.key === 'Escape' || e.key === 'Backspace') { e.preventDefault(); closeViewer(); }
    else if (e.key === 'ArrowLeft') step(-1);
    else if (e.key === 'ArrowRight') step(1);
    return;
  }
  if (!$('#more').hidden && e.key === 'Escape') { $('#more').hidden = true; return; }
  if (document.activeElement === search) return;
  if (e.key === 'Escape') { kind = null; search.value = ''; highlight(); fit(); }
  else if (e.key === '+' || e.key === '=') zoomCenter(1.5);
  else if (e.key === '-') zoomCenter(1 / 1.5);
  else if (e.key.length === 1 && /[\w ]/.test(e.key) && !e.ctrlKey && !e.metaKey && !e.altKey) search.focus();
});

// ------------------------------------------------------------------ Kiosk mode

let idle;
function resetIdle() {
  clearTimeout(idle);
  $('#kiosk-banner').hidden = true;
  idle = setTimeout(() => {
    $('#more').hidden = true;
    if (open) { history.replaceState(null, '', location.pathname + location.search); route(); }
    kind = null; search.value = ''; search.blur(); highlight(); fit();
    $('#kiosk-banner').hidden = false;
  }, KIOSK_RESET_MS);
}

// ------------------------------------------------------------------ Start

async function start() {
  const get = (path) => fetch(path, { cache: 'no-cache' });
  const [data, photos, csv] = await Promise.all([
    get('data/places.json').then((r) => r.json()),
    get('data/photos.json').then((r) => r.json()),
    get('data/rooms.csv').then((r) => (r.ok ? r.text() : '')).catch(() => ''),
  ]);
  const rooms = new Map(parseCSV(csv).map((row) => [row.id, row]));
  places = data.places.map((p) => makePlace(p, data, photos, rooms));
  extras = data.extras.map((p) => makePlace(p, data, photos, rooms));
  byId = new Map([...places, ...extras].map((p) => [p.id, p]));

  const map = $('#map');
  map.src = data.map;
  // Wait for the map image and fonts, but never hang the page on them
  const atMost = (promise, ms) => Promise.race([promise.catch(() => {}), new Promise((done) => setTimeout(done, ms))]);
  await atMost(map.decode(), 3000);
  buildPlaces();
  buildMore();
  await atMost(document.fonts.ready, 1500);
  fitLabels();
  fit();
  // On phones the whole map is tiny, so start zoomed in on the main buildings
  if (viewport.clientWidth < 700) {
    view.scale = Math.min(viewport.clientHeight / MAP_H, view.min * 2.4);
    view.x = viewport.clientWidth / 2 - 830 * view.scale;
    view.y = viewport.clientHeight / 2 - 560 * view.scale;
    clamp(); apply();
  }
  $('#loading').remove();

  const q = new URLSearchParams(location.search).get('q');
  if (q) { search.value = q; highlight(); }
  route();

  if (KIOSK) {
    document.body.classList.add('kiosk');
    for (const type of ['pointerdown', 'keydown', 'wheel']) document.addEventListener(type, resetIdle, { passive: true });
    resetIdle();
    $('#kiosk-banner').hidden = false;
  }
}

start().catch((err) => {
  $('#loading').textContent = 'Sorry, the map could not load. Try refreshing the page.';
  console.error(err);
});
