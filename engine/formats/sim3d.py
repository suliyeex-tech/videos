"""SIM3D format (whatif.sim style): a small 3D world rendered in code (flat-shaded polygons, perspective camera,
fog, shadows-as-blobs), a real famous PLACE, a HUD with data (TEMPERATURE 72 °F · PLACE), a serif title,
serif italic subtitles, and a countdown "X RETURNS IN 1.77 S · SHOWN 6x SLOWER". Typical hook:
"What if X disappeared for 5 seconds?" told in 2nd person ("You're on the pier...").

Scene = list of polygons built each frame from parameters (sea level, freeze, darkness, fall offsets...).
    cam = Cam(pos=(0, 30, -120), yaw=0, pitch=-12, fov=62)
    polys = []; beach_scene(polys, t, P)   # P = dict of effect parameters
    render(img, cam, polys, sky=(...), fog=(...))
Colours BGR."""
import math, random
import numpy as np, cv2
from kit import *

class Cam:
    def __init__(self, pos=(0, 30, -120), yaw=0.0, pitch=-12.0, fov=62.0):
        self.pos = np.array(pos, float); self.yaw = yaw; self.pitch = pitch; self.fov = fov
    def mats(self):
        cy, sy = math.cos(math.radians(self.yaw)), math.sin(math.radians(self.yaw))
        cp, sp = math.cos(math.radians(self.pitch)), math.sin(math.radians(self.pitch))
        Ry = np.array([[cy, 0, -sy], [0, 1, 0], [sy, 0, cy]]); Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
        return Rx @ Ry
def lerp_cam(a, b, k):
    k = ease(k); return Cam(tuple(np.array(a.pos) * (1 - k) + np.array(b.pos) * k), a.yaw + (b.yaw - a.yaw) * k,
                            a.pitch + (b.pitch - a.pitch) * k, a.fov + (b.fov - a.fov) * k)

LIGHT = np.array([-0.45, 0.8, -0.35]); LIGHT = LIGHT / np.linalg.norm(LIGHT)

def quad(polys, pts, col, shade=True, emissive=False):
    polys.append((np.array(pts, float), col, shade, emissive))
def box(polys, x, y, z, w, h, d, col, top=None, emissive=False):
    """axis-aligned box: (x, z) = centre on the ground, y = base height."""
    x0, x1, z0, z1, y0, y1 = x - w / 2, x + w / 2, z - d / 2, z + d / 2, y, y + h
    quad(polys, [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], top or col, emissive=emissive)
    quad(polys, [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], col, emissive=emissive)
    quad(polys, [(x1, y0, z1), (x0, y0, z1), (x0, y1, z1), (x1, y1, z1)], col, emissive=emissive)
    quad(polys, [(x0, y0, z1), (x0, y0, z0), (x0, y1, z0), (x0, y1, z1)], col, emissive=emissive)
    quad(polys, [(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], col, emissive=emissive)

def render(img, cam, polys, sky=((235, 190, 120), (250, 225, 190)), fog=(245, 225, 200), fog_d=(250, 1400), horizon_glow=None, stars_k=0.0, t=0.0):
    img[:] = grad(sky[0], sky[1])
    if stars_k > 0: stars(img, t, stars_k, ymax=H, base=sky[0])
    R = cam.mats(); f = (W / 2) / math.tan(math.radians(cam.fov / 2)); cx, cy = W / 2, H * 0.5
    items = []
    for pts, col, shade, em in polys:
        c = (pts - cam.pos) @ R.T            # camera space: x right, y up, z forward
        if np.all(c[:, 2] < 1): continue
        if np.any(c[:, 2] < 1):              # clip against the near plane (simple: push points forward)
            c = c.copy(); c[:, 2] = np.maximum(c[:, 2], 1)
        d = c[:, 2].mean()
        n = np.cross(pts[1] - pts[0], pts[2] - pts[0]); nn = np.linalg.norm(n)
        k = 1.0
        if shade and nn > 0: k = 0.55 + 0.45 * abs(float(np.dot(n / nn, LIGHT)))
        col2 = col if em else tuple(int(min(255, ch * k)) for ch in col)
        fk = 0.0 if em else clamp((d - fog_d[0]) / (fog_d[1] - fog_d[0])) * 0.85
        col2 = mix(col2, fog, fk)
        p2 = np.stack([cx + f * c[:, 0] / c[:, 2], cy - f * c[:, 1] / c[:, 2]], 1)
        items.append((d, p2, col2))
    items.sort(key=lambda q: -q[0])
    for d, p2, col in items:
        cv2.fillPoly(img, [np.round(p2 * 4).astype(np.int32)], col, cv2.LINE_AA, shift=2)
    if horizon_glow: glow(img, W / 2, H * 0.42, 700, horizon_glow, 0.5)

# ---------------- scene builders ----------------
SAND = (150, 200, 225); SEA = (150, 110, 40); SEA_L = (175, 140, 70); WALK = (175, 180, 185); ROAD = (70, 70, 75)
PALM_T = (60, 95, 130); PALM_L = (60, 140, 70)
CLOTHES = [(60, 60, 200), (200, 120, 50), (60, 160, 70), (40, 180, 230), (160, 80, 150), (230, 230, 235), (50, 50, 60)]

def people(polys, n, x0, x1, z0, z1, seed=3, lift=0.0, frozen=0.0, t=0.0, walk=True):
    rb = random.Random(seed)
    for i in range(n):
        x = rb.uniform(x0, x1); z = rb.uniform(z0, z1); c = rb.choice(CLOTHES); sp = rb.uniform(-6, 6) if walk else 0
        x += sp * t * (1 - frozen); y = lift * rb.uniform(0.5, 1.5)
        if frozen: c = mix(c, (250, 245, 240), frozen * 0.8)
        box(polys, x, y, z, 1.6, 3.2, 1.0, c); box(polys, x, y + 3.2, z, 1.1, 1.1, 1.1, mix((120, 160, 210), (250, 245, 240), frozen * 0.8))
def palm(polys, x, z, h=26, frozen=0.0, sway=0.0):
    tc = mix(PALM_T, (240, 240, 240), frozen * 0.7); lc = mix(PALM_L, (245, 245, 240), frozen * 0.85)
    box(polys, x, 0, z, 1.4, h, 1.4, tc)
    for a in range(0, 360, 60):
        r = math.radians(a + sway); ex, ez = x + math.cos(r) * 11, z + math.sin(r) * 11
        quad(polys, [(x, h, z), (ex - math.sin(r) * 2, h - 5, ez + math.cos(r) * 2), (ex, h - 7, ez), (ex + math.sin(r) * 2, h - 5, ez - math.cos(r) * 2)], lc)
def wheel(polys, x, z, r=34, y0=12, ang=0.0, col=(80, 80, 230), frozen=0.0):
    col = mix(col, (245, 245, 245), frozen * 0.7)
    for i in range(16):
        a0 = math.radians(i * 22.5 + ang); a1 = math.radians((i + 1) * 22.5 + ang); cy = y0 + r
        p0 = (x, cy + r * math.sin(a0), z + r * math.cos(a0)); p1 = (x, cy + r * math.sin(a1), z + r * math.cos(a1))
        quad(polys, [p0, p1, (p1[0] + 1, p1[1] - 1, p1[2]), (p0[0] + 1, p0[1] - 1, p0[2])], col, shade=False)
        gc = [(60, 60, 220), (40, 200, 240), (200, 120, 50), (60, 170, 70)][i % 4]
        box(polys, x, p0[1] - 3, p0[2], 3, 3, 3, mix(gc, (245, 245, 245), frozen * 0.7))
    for sx in (-6, 6): quad(polys, [(x, 0, z + sx), (x, y0 + r, z), (x + 1, y0 + r, z), (x + 1, 0, z + sx)], mix((90, 90, 95), (240, 240, 240), frozen * 0.6))

def beach_scene(polys, t, P):
    """A generic beach + pier + boardwalk town. P keys (all optional, 0..1 unless noted):
    sea (sea level offset, units), water (0 = no water at all), frozen, dark, crowd, wheel_ang, sway."""
    fr = P.get('frozen', 0.0); water = P.get('water', 1.0); sea_y = P.get('sea', 0.0)
    sand = mix(SAND, (250, 248, 245), fr * 0.9)
    quad(polys, [(-900, 0, -200), (900, 0, -200), (900, 0, 140), (-900, 0, 140)], sand)
    quad(polys, [(-900, 0.1, -40), (900, 0.1, -40), (900, 0.1, -20), (-900, 0.1, -20)], mix(WALK, (250, 250, 250), fr * 0.8))
    quad(polys, [(-900, 0.1, -200), (900, 0.1, -200), (900, 0.1, -160), (-900, 0.1, -160)], ROAD)
    # seabed (visible when water is gone)
    quad(polys, [(-1500, -60, 140), (1500, -60, 140), (1500, -260, 1600), (-1500, -260, 1600)], mix((70, 110, 140), (240, 240, 240), fr * 0.5))
    if water > 0.02:
        sc = mix(mix(SEA, (240, 235, 225), fr * 0.85), (40, 30, 20), P.get('dark', 0) * 0.5)
        y = sea_y - 60 * (1 - water)
        quad(polys, [(-1500, y, 130), (1500, y, 130), (1500, y, 1600), (-1500, y, 1600)], sc, shade=False)
        if fr < 0.5:
            for k in range(6):
                zz = 160 + ((k * 40 + t * 20) % 240)
                quad(polys, [(-1500, y + 0.3, zz), (1500, y + 0.3, zz), (1500, y + 0.3, zz + 3), (-1500, y + 0.3, zz + 3)], mix(SEA_L, (255, 255, 255), 0.3), shade=False)
    # pier
    box(polys, 60, 8, 330, 26, 3, 420, mix((90, 120, 150), (245, 245, 245), fr * 0.6))
    for zz in range(140, 540, 40):
        for xx in (49, 71): box(polys, xx, -60, zz, 2, 68, 2, (60, 80, 100))
    wheel(polys, 60, 420, ang=P.get('wheel_ang', t * 6), y0=11, frozen=fr)
    # boardwalk buildings
    rb = random.Random(7)
    for i in range(-8, 9):
        x = i * 34 + rb.uniform(-4, 4); h = rb.uniform(14, 40); c = rb.choice([(170, 200, 230), (200, 210, 225), (150, 170, 200), (190, 160, 140), (210, 225, 235)])
        box(polys, x, 0, -110 + rb.uniform(-10, 10), 28, h, 30, mix(c, (245, 245, 245), fr * 0.7), top=mix((110, 120, 130), (250, 250, 250), fr))
    for i in range(-6, 7): palm(polys, i * 44 + 10, -12, frozen=fr, sway=P.get('sway', 0) * math.sin(t * 2 + i))
    people(polys, int(P.get('crowd', 60)), -160, 200, -30, 120, lift=P.get('lift', 0), frozen=fr, t=t)

def city_scene(polys, t, P):
    """A generic city intersection with towers, cars and people. P: frozen, lift, cars_stop, crowd."""
    fr = P.get('frozen', 0.0)
    quad(polys, [(-900, 0, -400), (900, 0, -400), (900, 0, 1600), (-900, 0, 1600)], mix((150, 155, 160), (250, 250, 250), fr))
    quad(polys, [(-24, 0.1, -400), (24, 0.1, -400), (24, 0.1, 1600), (-24, 0.1, 1600)], ROAD)
    quad(polys, [(-900, 0.1, 280), (900, 0.1, 280), (900, 0.1, 328), (-900, 0.1, 328)], ROAD)
    for zz in range(-300, 1600, 30): quad(polys, [(-0.6, 0.2, zz), (0.6, 0.2, zz), (0.6, 0.2, zz + 14), (-0.6, 0.2, zz + 14)], (60, 200, 240))
    rb = random.Random(11)
    for side in (-1, 1):
        for i in range(14):
            z = -250 + i * 120 + rb.uniform(-10, 10)
            if 240 < z < 370: continue
            h = rb.uniform(60, 260); w = rb.uniform(50, 80); c = rb.choice([(120, 110, 100), (160, 150, 140), (90, 100, 120), (180, 180, 175), (100, 120, 150)])
            bx = side * (60 + w / 2 + rb.uniform(0, 30)); fx = bx - side * (w / 2 + 0.4)
            box(polys, bx, 0, z, w, h, rb.uniform(60, 100), mix(c, (245, 245, 245), fr * 0.6))
            for k in range(int(h / 18)):   # glowing window bands on the street-facing wall
                quad(polys, [(fx, 8 + k * 18, z - 25), (fx, 8 + k * 18, z + 25), (fx, 12 + k * 18, z + 25), (fx, 12 + k * 18, z - 25)], (130, 220, 250), shade=False, emissive=P.get('lights', 0) > 0.5)
    for i in range(22):
        lane = rb.choice((-12, 12)); z = rb.uniform(-200, 1400); v = 30 * (1 - P.get('cars_stop', 0))
        z += (v * t if lane > 0 else -v * t); c = rb.choice([(40, 200, 250), (60, 60, 200), (230, 230, 235), (50, 50, 55), (200, 120, 50)])
        box(polys, lane, P.get('lift', 0) * rb.uniform(0.5, 2), z, 8, 6, 16, c, top=mix(c, (0, 0, 0), 0.2))
    people(polys, int(P.get('crowd', 80)), -55, 55, -100, 260, seed=5, lift=P.get('lift', 0), frozen=fr, t=t)

# ---------------- overlays ----------------
def hud(img, label, value, place, a=1.0, x=110, y=210, sub=None):
    def lt(s, xx, yy, size, col, path):
        w = twidth(s, size, path); text(img, s, xx + w / 2, yy, size, col, path, alpha=a)
    lt(label.upper(), x, y, 30, (235, 235, 235), INTER_M)
    lt(value, x, y + 62, 84, WHITE, SERIF_I)
    if place: lt(place.upper(), x, y + 130, 30, (225, 225, 225), INTER_M)
    if sub: lt(sub.upper(), x, y + 130, 26, (200, 200, 200), INTER_M)
def title(img, l1, l2=None, a=1.0, y=520):
    text(img, l1, W / 2, y, 82, WHITE, SERIF_I, alpha=a, stroke=2, scol=(60, 50, 40))
    if l2: text(img, l2, W / 2, y + 100, 82, WHITE, SERIF_I, alpha=a, stroke=2, scol=(60, 50, 40))
def countdown(img, t, t0, total, label, slow=6, x=110, y=210):
    rem = max(0.0, total - (t - t0) / slow)
    hud(img, label, f'{rem:.2f} S', None, sub=f'shown {slow}x slower')
