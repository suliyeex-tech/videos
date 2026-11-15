"""GAMEUI format (new 2026-11-15, shorts B): a story told as a retro strategy/RTS video game.
Top resource bar (icon + value chips that pop when they change), mission/objective panel, unit selection boxes and a
mouse cursor, "ACHIEVEMENT UNLOCKED" toasts, big LEVEL / MISSION FAILED / RESPAWN banners, a player character
(the gamer) in a small facecam bubble, subtle scanlines. Use with CAPTION='sub', a lively narrator, MOOD 'funny'.
Example: episodes/20261115_b3_gameui_emu_war.py"""
import math, random
import numpy as np, cv2
from kit import *

UI = (34, 24, 22); UI2 = (60, 44, 40); UIB = (120, 200, 250)    # panel, panel light, border (warm yellow, BGR)
GGREEN = (90, 210, 110); GRED = (70, 70, 240); GGOLD = (60, 200, 255); GBLUE = (230, 160, 60)
WHEAT = (90, 190, 235); WHEAT_D = (60, 150, 200); DIRT = (70, 110, 150)
KHAKI = (110, 160, 170)
rg = random.Random(4)
STALKS = [(rg.uniform(0, W), rg.uniform(0, 1), rg.uniform(0, 6.28)) for _ in range(260)]

def field(img, t, horizon=820, wheat=1.0, sky=((200, 160, 110), (230, 215, 190)), eaten=0.0):
    img[:horizon] = grad(sky[0], sky[1], 0, horizon)
    ell(img, (W / 2, horizon + 10), 900, 60, (120, 150, 140))
    img[horizon:] = grad(mix(WHEAT, DIRT, eaten), mix(WHEAT_D, DIRT, eaten * 0.8), horizon, H)
    for x, v, ph in STALKS:
        y = horizon + 20 + v ** 1.6 * (H - horizon - 40); s = 0.4 + 1.2 * v
        if rg.random() < eaten * 0.0: continue
        hgt = 40 * s * wheat * (1 - eaten * (0.5 + 0.5 * math.sin(ph * 7)))
        sw = 4 * s * math.sin(t * 2 + ph)
        line(img, (x, y), (x + sw, y - hgt), mix(WHEAT_D, (40, 110, 170), v), max(1, 2 * s))
        if hgt > 6: ell(img, (x + sw, y - hgt), 4 * s, 9 * s, mix(WHEAT, (120, 220, 255), 0.3))
    for i in range(9):   # fence
        x = 40 + i * 125; line(img, (x, horizon + 30), (x, horizon - 20), (60, 90, 120), 6)
    line(img, (0, horizon - 5), (W, horizon - 5), (60, 90, 120), 3); line(img, (0, horizon + 15), (W, horizon + 15), (60, 90, 120), 3)

def emu(img, x, y, s=1.0, t=0.0, run=0.0, d=1, col=(70, 80, 95), boss=False):
    """emu standing on (x, y); run 0..1 animates legs; d = facing (+1 right)"""
    if boss: col = (35, 35, 40)
    ph = t * 14 * run
    for k, off in ((0, 0), (1, math.pi)):
        a = 0.5 * math.sin(ph + off) * run
        kx = x + d * 10 * s + 30 * s * math.sin(a); ky = y - 40 * s
        line(img, (x, y - 80 * s), (kx, ky), (80, 120, 160), 6 * s); line(img, (kx, ky), (kx + d * 20 * s * math.sin(a + 0.4), y), (80, 120, 160), 6 * s)
    ell(img, (x, y - 105 * s), 62 * s, 46 * s, col)
    for i in range(5): ell(img, (x - d * (30 - i * 12) * s, y - (120 - 6 * (i % 2)) * s), 18 * s, 26 * s, mix(col, (20, 20, 20), 0.25))
    bob = 6 * s * math.sin(ph * 2) * run
    nx, ny = x + d * 45 * s, y - 130 * s; hx, hy = x + d * 62 * s, y - 210 * s + bob
    line(img, (nx, ny), (hx, hy), mix(col, (150, 150, 170), 0.3), 14 * s)
    circ(img, (hx, hy), 16 * s, mix(col, (150, 150, 170), 0.3)); circ(img, (hx + d * 5 * s, hy - 3 * s), 4.5 * s, (240, 240, 240)); circ(img, (hx + d * 6 * s, hy - 3 * s), 2.5 * s, (10, 10, 10))
    poly(img, [(hx + d * 12 * s, hy - 5 * s), (hx + d * 34 * s, hy + 2 * s), (hx + d * 12 * s, hy + 7 * s)], (60, 110, 160))

def flock(img, t, n, x0, x1, y0, y1, s=0.6, run=0.0, seed=2, vx=0.0, scatter=0.0):
    rb = random.Random(seed); items = []
    for i in range(n):
        x = rb.uniform(x0, x1); y = rb.uniform(y0, y1); d = rb.choice((-1, 1)); sc = s * (0.6 + 0.6 * (y - y0) / max(1, y1 - y0))
        ang = rb.uniform(0, 6.28); x += vx * t + scatter * math.cos(ang) * 900 * t; y += scatter * math.sin(ang) * 120 * t
        if scatter: d = 1 if math.cos(ang) > 0 else -1
        items.append((y, x, sc, d, rb.random()))
    for y, x, sc, d, ph in sorted(items): emu(img, x, y, sc, t + ph, run, d)

def soldier(img, x, y, s=1.0, sel=False, t=0.0):
    if sel:
        rrect(img, x - 60 * s, y - 230 * s, 120 * s, 250 * s, 10, GGREEN, 3)
        rrect(img, x - 50 * s, y - 250 * s, 100 * s, 10 * s, 4, (40, 40, 40)); rrect(img, x - 50 * s, y - 250 * s, 100 * s, 10 * s, 4, GGREEN)
    for sx in (-1, 1): line(img, (x + sx * 10 * s, y - 70 * s), (x + sx * 14 * s, y), (60, 90, 100), 12 * s)
    rrect(img, x - 30 * s, y - 150 * s, 60 * s, 85 * s, 14, KHAKI)
    circ(img, (x, y - 175 * s), 22 * s, (140, 185, 232))
    ell(img, (x, y - 192 * s), 44 * s, 10 * s, (80, 120, 130)); ell(img, (x - 6 * s, y - 198 * s), 26 * s, 14 * s, (80, 120, 130), 180, 360)

def lewis(img, x, y, s=1.0, jam=0.0, t=0.0):
    rrect(img, x - 90 * s, y - 20 * s, 180 * s, 26 * s, 8, (50, 50, 55)); circ(img, (x - 20 * s, y - 34 * s), 30 * s, (60, 60, 65))
    for sx in (-1, 1): line(img, (x + 50 * s, y), (x + 50 * s + sx * 30 * s, y + 60 * s), (50, 50, 55), 6 * s)
    if jam: text(img, 'JAMMED', x, y - 90 * s, 44 * s, GRED, INTER_B, scale=1 + 0.08 * math.sin(t * 20))

def truck(img, x, y, s=1.0, t=0.0, bump=0.0):
    by = -abs(math.sin(t * 9)) * 26 * s * bump
    rrect(img, x - 160 * s, y - 120 * s + by, 230 * s, 80 * s, 10, (70, 110, 90)); rrect(img, x + 60 * s, y - 150 * s + by, 110 * s, 110 * s, 14, (70, 110, 90))
    rrect(img, x + 80 * s, y - 135 * s + by, 70 * s, 45 * s, 6, (200, 220, 230))
    for wx in (-110, 110): circ(img, (x + wx * s, y - 30 * s), 32 * s, (35, 35, 35)); circ(img, (x + wx * s, y - 30 * s), 12 * s, (120, 120, 120))
    lewis(img, x - 60 * s, y - 140 * s + by, 0.6 * s)

def chip(img, x, y, icon, label, value, col=WHITE, pulse=0.0, w=240):
    rrect(img, x, y, w, 76, 16, UI2); rrect(img, x, y, w, 76, 16, mix(UIB, col, 0.5), 2)
    emoji(img, icon, x + 38, y + 38, 40)
    text(img, label, x + 72 + twidth(label, 18, INTER_B) / 2, y + 20, 18, (200, 200, 205), INTER_B)
    sc = 1 + 0.25 * pulse
    text(img, value, x + 72 + twidth(value, 38, INTER_B) / 2, y + 52, 38, col, INTER_B, scale=sc)

def topbar(img, t, res):
    """res: list of (icon, label, value, col, changed_at or None) up to 4"""
    rrect(img, 14, 14, W - 28, 108, 22, UI); rrect(img, 14, 14, W - 28, 108, 22, UIB, 2)
    n = len(res); w = (W - 60 - 12 * (n - 1)) / n
    for i, (ic, lab, val, col, at) in enumerate(res):
        p = 0.0 if at is None else max(0.0, 1 - abs(t - at) / 0.25) if t >= at - 0.05 else 0.0
        chip(img, 30 + i * (w + 12), 30, ic, lab, val, col, p, w)

def objective(img, txt, a=1.0, done=None, y=150):
    if a <= 0.02: return
    w = twidth(txt, 30, INTER_B) + 120
    rrect(img, 30, y, w, 70, 14, mix((0, 0, 0), UI, a)); rrect(img, 30, y, w, 70, 14, mix((0, 0, 0), UIB, a), 2)
    col = GGREEN if done is True else GRED if done is False else GGOLD
    rrect(img, 50, y + 20, 30, 30, 6, mix((0, 0, 0), col, a), 3)
    if done is True: line(img, (56, y + 36), (64, y + 44), col, 5); line(img, (64, y + 44), (76, y + 26), col, 5)
    if done is False: line(img, (56, y + 26), (74, y + 44), col, 5); line(img, (74, y + 26), (56, y + 44), col, 5)
    text(img, txt, 95 + twidth(txt, 30, INTER_B) / 2, y + 35, 30, mix((0, 0, 0), WHITE, a), INTER_B)

def achievement(img, t, at, title, icon='🏆', dur=2.6, y=260):
    if not (at <= t < at + dur): return
    k = eout(ramp(t, at, at + 0.3)) * (1 - ramp(t, at + dur - 0.3, at + dur))
    x = W / 2; w = max(640, twidth(title, 40, INTER_B) + 200); yy = y - 200 * (1 - k)
    rrect(img, x - w / 2, yy, w, 130, 26, UI); rrect(img, x - w / 2, yy, w, 130, 26, GGOLD, 3)
    emoji(img, icon, x - w / 2 + 70, yy + 65, 64)
    text(img, 'ACHIEVEMENT UNLOCKED', x + 40, yy + 38, 24, GGOLD, INTER_B)
    text(img, title, x + 40, yy + 86, 40, WHITE, INTER_B)

def banner(img, t, txt, col=GRED, at=0.0, y=700, size=130, sub=None):
    k = back(ramp(t, at, at + 0.3))
    if k <= 0: return
    tint(img, (0, 0, 0), 0.35 * min(1, k))
    rrect(img, 0, y - size * 0.75, W, size * 1.5 + (60 if sub else 0), 0, mix((0, 0, 0), col, 0.35))
    text(img, txt, W / 2, y, size, col, ANT, scale=k, stroke=8, scol=(10, 10, 10))
    if sub: text(img, sub, W / 2, y + size * 0.75, 36, WHITE, INTER_B, alpha=ramp(t, at + 0.3, at + 0.6))

def cursor(img, x, y, click=0.0):
    pts = [(x, y), (x, y + 60), (x + 16, y + 46), (x + 28, y + 72), (x + 38, y + 67), (x + 26, y + 42), (x + 46, y + 42)]
    poly(img, [(px + 3, py + 3) for px, py in pts], (10, 10, 10)); poly(img, pts, WHITE)
    if click > 0: cv2.circle(img, P(x, y), int((20 + 50 * click) * 8), mix(WHITE, (0, 0, 0), click), 3, cv2.LINE_AA, 3)

def facecam(img, t, mood='🙂', x=930, y=300, r=105, name='PIXEL PAM'):
    circ(img, (x, y), r + 8, GGOLD); circ(img, (x, y), r, (90, 50, 60))
    emoji(img, mood, x, y + 4, r * 1.2)
    rrect(img, x - 95, y + r - 6, 190, 40, 12, GRED); text(img, name, x, y + r + 14, 24, WHITE, INTER_B)
    if int(t * 2) % 2 == 0: circ(img, (x - r + 18, y - r + 18), 9, GRED)

def health(img, x, y, w, v, col=GGREEN, label=None):
    rrect(img, x, y, w, 26, 8, (30, 30, 30)); rrect(img, x + 3, y + 3, max(4, (w - 6) * clamp(v)), 20, 6, col)
    if label: text(img, label, x + w / 2, y - 22, 24, WHITE, INTER_B)

def scanlines(img, k=0.88):
    img[::5] = (img[::5] * k).astype(np.uint8)
