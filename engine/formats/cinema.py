"""CINEMA COUNTER format (meanwhile-style): no narration, cinematic 2.5D scenes with soft-shaded 'mannequin' people,
a big serif counter at the top-left, serif italic subtitles, piano/pad music, reveal question at the end.
Use with LINES of (None, seconds), CAPTION='serif', MOOD={'style': 'cinematic'}, PROGRESS=False."""
import math, random
import numpy as np, cv2
from kit import *

SKIN_T = [(120, 160, 210), (90, 130, 185), (70, 100, 150), (150, 185, 225), (60, 85, 125)]
CLOTH = [(60, 60, 180), (180, 120, 50), (60, 150, 70), (40, 170, 220), (150, 80, 140), (200, 200, 205), (50, 50, 60), (90, 130, 200)]

def sky(img, top, bot, y1=H): img[:y1] = grad(top, bot, 0, y1)
def ground(img, y, near, far): img[y:] = grad(far, near, y, H)

def person(img, x, y, s, cloth, skin, jump=0.0, shadow=True, arms_up=0.0):
    """2.5D mannequin: (x, y) = feet position on the ground. jump in px (lifts body, shadow stays)."""
    if shadow:
        k = max(0.35, 1 - jump / (300 * s + 1)); gc = tuple(int(c) for c in img[min(H - 1, int(y)), min(W - 1, max(0, int(x)))])
        ell(img, (x, y), 46 * s * k, 12 * s * k, mix(gc, (0, 0, 0), 0.45))
    yb = y - jump
    for dx in (-14, 14): rrect(img, x + dx * s - 10 * s, yb - 120 * s, 20 * s, 120 * s, 10 * s, mix(cloth, (20, 20, 20), 0.55))
    rrect(img, x - 34 * s, yb - 250 * s, 68 * s, 140 * s, 28 * s, cloth)
    rrect(img, x - 34 * s, yb - 250 * s, 26 * s, 140 * s, 20 * s, mix(cloth, (255, 255, 255), 0.18))
    for sx in (-1, 1):
        a = math.radians(170 * arms_up + 10); px, py = x + sx * 38 * s, yb - 235 * s
        line(img, (px, py), (px + sx * math.sin(a) * 105 * s, py + math.cos(a) * 105 * s), cloth, 22 * s)
    circ(img, (x, yb - 292 * s), 38 * s, skin); circ(img, (x - 12 * s, yb - 304 * s), 16 * s, mix(skin, (255, 255, 255), 0.25))

def crowd(img, t, y0, y1, n=120, seed=1, jump=0.0, arms=0.0, s0=0.35, s1=1.1, xspread=1.0):
    rb = random.Random(seed); ppl = []
    for i in range(n):
        u = rb.random(); y = y0 + (y1 - y0) * u ** 0.8; s = s0 + (s1 - s0) * (y - y0) / max(1, y1 - y0)
        x = W / 2 + rb.uniform(-0.75, 0.75) * W * xspread * (0.6 + 0.4 * s / s1)
        ppl.append((y, x, s, rb.choice(CLOTH), rb.choice(SKIN_T), rb.uniform(0.85, 1.15), rb.uniform(0, 0.12)))
    for y, x, s, c, sk, jv, dl in sorted(ppl):
        j = max(0.0, jump - dl) * jv
        person(img, x, y, s, c, sk, jump=j * 260 * s, arms_up=arms)

def stadium(img, t, glowk=1.0):
    sky(img, (40, 20, 15), (90, 50, 30), 900)
    poly(img, [(0, 420), (W, 420), (W, 1100), (0, 1100)], (50, 35, 30))
    rb = random.Random(3)
    for i in range(900):
        x = rb.uniform(0, W); y = rb.uniform(440, 1080); circ(img, (x, y), rb.uniform(3, 6), rb.choice(CLOTH))
    for lx in (120, 960):
        glow(img, lx, 330, 260, (180, 220, 255), 1.2 * glowk); circ(img, (lx, 330), 40, (240, 250, 255))
    img[1100:] = grad((70, 120, 160), (40, 80, 120), 1100, H)
    for x in range(0, W, 160): line(img, (x, 1100), (x - 300, H), (220, 220, 220), 4)

def field(img, t):
    sky(img, (230, 190, 140), (200, 220, 245), 900)
    glow(img, 820, 420, 300, (120, 200, 255), 1.0); circ(img, (820, 420), 70, (180, 240, 255))
    img[900:] = grad((60, 140, 160), (40, 100, 120), 900, H)
    for k in range(14): line(img, (W / 2, 900), (W / 2 + (k - 7) * 260, H), (40, 110, 130), 10)
    x = 300; rrect(img, x, 1080, 260, 120, 18, (40, 60, 200)); rrect(img, x + 120, 980, 120, 110, 10, (40, 60, 200)); rrect(img, x + 135, 995, 90, 70, 6, (200, 220, 230))
    circ(img, (x + 200, 1220), 80, (30, 30, 35)); circ(img, (x + 50, 1235), 50, (30, 30, 35)); line(img, (x + 30, 1080), (x + 30, 1020), (60, 60, 60), 12)
    person(img, 760, 1260, 0.9, (60, 90, 140), SKIN_T[1])

def cabin(img, t):
    img[:] = grad((70, 60, 55), (40, 34, 30))
    for k in range(5):
        y = 760 + k * 170; s = 0.6 + k * 0.18
        for sx in (-1, 1):
            for j in range(3):
                x = W / 2 + sx * (120 + j * 120) * s
                rrect(img, x - 50 * s, y - 120 * s, 100 * s, 160 * s, 20 * s, (120, 80, 60))
                circ(img, (x, y - 150 * s), 30 * s, SKIN_T[(k + j) % 5])
    for k in range(3): rrect(img, 60 + k * 340, 300, 140, 200, 60, (230, 210, 180))

def city(img, t, night=1.0):
    sky(img, mix((240, 200, 150), (40, 15, 10), night), mix((250, 225, 200), (90, 45, 30), night), 1100)
    rb = random.Random(7)
    for i in range(26):
        x = i * 46 - 40; h = rb.randint(250, 650); c = mix((150, 140, 130), (40, 30, 30), night)
        rrect(img, x, 1100 - h, 50, h, 2, c)
        for wy in range(int(1100 - h + 20), 1090, 34):
            if rb.random() < 0.5: rrect(img, x + 10, wy, 12, 16, 2, mix((200, 200, 200), (120, 220, 255), night))
    img[1100:] = grad((60, 55, 55), (30, 28, 28), 1100, H)

def earth(img, cx, cy, r, t=0):
    glow(img, cx, cy, int(r * 1.5), (120, 90, 40), 0.8)
    circ(img, (cx, cy), r, (150, 90, 30))
    rb = random.Random(11)
    for i in range(16):
        a = rb.uniform(0, 6.28); d = rb.uniform(0, 0.75) * r; x = cx + math.cos(a + t * 0.1) * d
        if abs(x - cx) < r * 0.85: ell(img, (x, cy + math.sin(a) * d), rb.uniform(0.1, 0.25) * r, rb.uniform(0.08, 0.18) * r, (70, 150, 80))
    cv2.ellipse(img, P(cx, cy), (int(r * 8), int(r * 8)), 0, 0, 360, (230, 200, 160), 6, cv2.LINE_AA, 3)

def atom(img, cx, cy, t, s=1.0):
    glow(img, cx, cy, int(220 * s), (180, 120, 60), 0.9); circ(img, (cx, cy), 26 * s, (100, 140, 255))
    for k in range(3):
        cv2.ellipse(img, P(cx, cy), (int(240 * s * 8), int(80 * s * 8)), k * 60, 0, 360, (230, 210, 190), 3, cv2.LINE_AA, 3)
        a = t * 3 + k * 2.1; ex = 240 * s * math.cos(a); ey = 80 * s * math.sin(a); r = math.radians(k * 60)
        circ(img, (cx + ex * math.cos(r) - ey * math.sin(r), cy + ex * math.sin(r) + ey * math.cos(r)), 12 * s, (255, 220, 120))

def counter_overlay(img, label, value, sub=None, a=1.0, y=1080):
    """meanwhile-style counter on the left, above the subtitles"""
    if a <= 0.02: return
    lower_third(img, y - 60)
    text(img, label, 80 + twidth(label, 26, INTER_B) / 2, y, 26, (235, 235, 235), INTER_B, alpha=a)
    s = f'{int(value):,}'; text(img, s + 3 * ' ', 80 + twidth(s, 84, SERIF_I) / 2, y + 66, 84, (0, 0, 0), SERIF_I, alpha=0.5 * a)
    text(img, s, 80 + twidth(s, 84, SERIF_I) / 2, y + 62, 84, WHITE, SERIF_I, alpha=a)
    if sub: text(img, sub, 80 + twidth(sub, 24, INTER_B) / 2, y + 128, 24, (220, 220, 220), INTER_B, alpha=a)

def bars(img, k=0.10):
    h = int(H * k); img[:h] = (img[:h] * 0.0).astype(np.uint8); img[H - h:] = (img[H - h:] * 0.0).astype(np.uint8)

def grade(img, warm=0.0, cool=0.0):
    if warm: tint(img, (60, 140, 255), warm)
    if cool: tint(img, (255, 150, 60), cool)

def lower_third(img, y0=1000, y1=1480):
    """soft dark band so the counter and subtitles stay readable over busy scenes"""
    g = np.ones((y1 - y0, 1, 1), np.float32)
    n = y1 - y0; r = np.arange(n, dtype=np.float32)
    g[:, 0, 0] = 1 - 0.62 * np.clip(np.minimum(r / 120, (n - r) / 120), 0, 1)
    img[y0:y1] = (img[y0:y1] * g).astype(np.uint8)
