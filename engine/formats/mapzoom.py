"""MAPZOOM format (geography list, reference D in REFERENCES.md): a flat satellite-style world map that flies and zooms
between places, glowing highlighted countries, flag pins with labels, big "#N" rank badges, clock chips.
Map data: engine/data/world110m.json (Natural Earth 1:110m countries, public domain).
    cam = (lon, lat, px_per_degree);   cam_lerp(a, b, k) for fly-overs (zooms out in the middle like a real map app)
    world(img, cam, hi={'FRA': GOLD}); pin(img, cam, lon, lat, '🇫🇷', 'FRANCE'); rank(img, t, 3); clock(img, x, y, 'SAT', '13:00')
Colours BGR."""
import math, json, os
import numpy as np, cv2
from kit import *

_D = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'world110m.json')))
_RINGS = [(c['iso'], [np.array(r, float) for r in c['r']]) for c in _D]
OCEAN = (70, 38, 14); OCEAN2 = (110, 62, 24); LAND = (88, 128, 96); LAND_D = (60, 92, 70); BORDER = (40, 60, 45)
MGOLD = (60, 200, 255); MRED = (70, 60, 240); MBLUE = (255, 190, 90)

def proj(cam, lon, lat):
    clon, clat, s = cam; k = math.cos(math.radians(clat)) * 0.35 + 0.65
    dl = (lon - clon + 540) % 360 - 180
    return W / 2 + dl * s * k, H * 0.46 - (lat - clat) * s
def cam_lerp(a, b, k, hop=True):
    k = ease(k); dl = (b[0] - a[0] + 540) % 360 - 180
    lon = (a[0] + dl * k + 540) % 360 - 180; lat = a[1] + (b[1] - a[1]) * k
    s = math.exp(math.log(a[2]) * (1 - k) + math.log(b[2]) * k)
    if hop:   # zoom out in the middle of long flights
        far = min(1.0, (abs(dl) + abs(b[1] - a[1])) / 120); s = s / (1 + 3.0 * far * math.sin(math.pi * k))
    return (lon, lat, s)
def world(img, cam, hi=None, t=0.0, grid=True, dim=None):
    hi = hi or {}
    img[:] = grad(OCEAN2, OCEAN)
    clon, clat, s = cam
    if grid:
        for lo in range(-180, 181, 15):
            x, _ = proj(cam, lo, 0)
            if -10 < x < W + 10: line(img, (x, 0), (x, H), mix(OCEAN, (255, 255, 255), 0.07), 1)
        for la in range(-75, 76, 15):
            _, y = proj(cam, clon, la)
            if -10 < y < H + 10: line(img, (0, y), (W, y), mix(OCEAN, (255, 255, 255), 0.07), 1)
    k = math.cos(math.radians(clat)) * 0.35 + 0.65
    for iso, rings in (_RINGS if s < 150 else []):
        col = hi.get(iso, LAND if not dim or iso in hi else LAND_D)
        for r in rings:
            for shift in (-360, 0, 360):
                dl = r[:, 0] - clon
                if shift == 0: dl = (dl + 540) % 360 - 180 if s < 8 else dl
                else: dl = dl + shift
                if s >= 8 and shift != 0: continue
                xs = W / 2 + dl * s * k; ys = H * 0.46 - (r[:, 1] - clat) * s
                if xs.max() < -50 or xs.min() > W + 50 or ys.max() < -50 or ys.min() > H + 50: continue
                if s < 8 and (xs.max() - xs.min()) > W * 0.8 and shift == 0: continue   # ring wrapped across the seam
                pts = np.stack([xs, ys], 1); p8 = np.round(pts * 8).astype(np.int32)
                cv2.fillPoly(img, [p8], col, cv2.LINE_AA, 3)
                cv2.polylines(img, [p8], True, BORDER if iso not in hi else mix(col, (255, 255, 255), 0.5), 2, cv2.LINE_AA, 3)
                if s < 8: break
    for iso, col in (hi.items() if s < 150 else []):   # glow over highlighted countries
        for _, rings in [(i, r) for i, r in _RINGS if i == iso]:
            r = max(rings, key=len); cx, cy = proj(cam, float(r[:, 0].mean()), float(r[:, 1].mean()))
            glow(img, cx, cy, int(min(500, 40 + s * 6)), mix(col, (0, 0, 0), 0.4), 0.35 + 0.15 * math.sin(t * 4))
def pin(img, cam, lon, lat, flag=None, lab=None, a=1.0, col=MRED, size=1.0):
    if a <= 0.02: return
    x, y = proj(cam, lon, lat); s = size * (0.6 + 0.4 * a)
    circ(img, (x, y), 16 * s, WHITE); circ(img, (x, y), 10 * s, col)
    poly(img, [(x - 34 * s, y - 70 * s), (x + 34 * s, y - 70 * s), (x, y - 14 * s)], WHITE)
    circ(img, (x, y - 100 * s), 54 * s, WHITE)
    if flag: emoji(img, flag, x, y - 100 * s, 66 * s, alpha=a)
    if lab:
        w = twidth(lab, int(46 * size)) + 40
        rrect(img, x - w / 2, y + 26 * s, w, 62 * size, 14, INK); text(img, lab, x, y + 26 * s + 31 * size, int(46 * size), WHITE, alpha=a)
def dot(img, cam, lon, lat, col=MGOLD, r=12, a=1.0):
    if a <= 0.02: return
    x, y = proj(cam, lon, lat); glow(img, x, y, int(r * 4), col, 0.6 * a); circ(img, (x, y), r * a, col); circ(img, (x, y), r * a, WHITE, 2)
def rank(img, t, n, at=0.0, x=150, y=400):
    k = back(ramp(t, at, at + 0.25))
    if k <= 0: return
    circ(img, (x, y), 92 * k, INK); circ(img, (x, y), 84 * k, MGOLD)
    text(img, f'#{n}', x, y + 4, 110, INK, ANT, scale=k)
def series_chip(img, title, part='PART 1', a=1.0):
    if a <= 0.02: return
    w = twidth(title, 50) + 60
    rrect(img, W / 2 - w / 2, 140 - (1 - a) * 150, w, 76, 12, MRED); text(img, title, W / 2, 178 - (1 - a) * 150, 50, WHITE)
    pill(img, W / 2, 268, part, 44, CREAM, INK, border=INK, alpha=a)
def clock(img, x, y, day, hhmm, col=WHITE, a=1.0, w=330):
    if a <= 0.02: return
    rrect(img, x - w / 2, y - 70, w, 140, 26, INK); rrect(img, x - w / 2 + 6, y - 64, w - 12, 128, 22, mix(INK, col, 0.12))
    text(img, day, x, y - 34, 36, col, INTER_B, alpha=a); text(img, hhmm, x, y + 22, 76, col, ANT, alpha=a)
def dateline(img, cam, a=1.0, lab='DATE LINE'):
    x, _ = proj(cam, 180.0 if cam[0] > 0 else -180.0, 0) if False else proj(cam, -168.98, 0)
    for y in range(0, H, 40): line(img, (x, y), (x, y + 22), mix(INK, MGOLD, a), 6)
    if lab: pill(img, x, 560, lab, 40, INK, MGOLD, alpha=a)
