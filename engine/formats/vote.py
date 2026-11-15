"""VOTE format — "YOU DECIDE" interactive daily character series (reference E in REFERENCES.md, owner 2026-11-14).
Polished flat vector look: one big centred character, cosy detailed night rooms (fairy lights, posters, a sleeping pet),
ONE stat card at the top that changes every 3-5 s, DAY N stamp, chance meter, YOU DECIDE card and A/B option cards.
Use with CAPTION='sub', VOICE='story', MOOD {'style': 'funny'}. NEVER fake vote counts or viewer comments.

    stat_card(img, t, label, value, col, at)        top card; call with a new value at a new `at` to make it pop
    day_stamp(img, t, n, at)                         big DAY N stamp
    meter(img, t, label, v0, v1, at, y)              chance-of-success bar that fills from v0 % to v1 %
    decide(img, t)                                   full-screen YOU DECIDE! card
    ab_cards(img, t, a_txt, a_icon, b_txt, b_icon, at)
    flies(img, t, cx, cy, n) / stink(img, t, cx, cy)  running visual gags
    bedroom(img, t, ...) / street(img, t, ...) / office(img, t, ...) / kitchen(img, t)   backgrounds
    car(img, x, y, s, col)                           side-view car
    pet_cat(img, t, x, y, s, awake=False)            the sleeping cat gag
Colours BGR."""
import math, random
import numpy as np, cv2
from kit import *

NAVY = (70, 30, 28); PURPLE = (110, 40, 70); DEEP = (45, 18, 22)
VORANGE = (40, 140, 245); VBLUE = (235, 150, 50); VGREEN = (120, 210, 90); VPINK = (180, 120, 245); VYEL = (80, 210, 255)
CARD = (40, 26, 24)

# ---------- UI ----------
def stat_card(img, t, label, value, col=VYEL, at=0.0, y=170, w=640, x=W / 2, icon=None):
    """rounded dark card with a coloured border at the top; pops in at `at`."""
    k = back(ramp(t, at, at + 0.28))
    if k <= 0: return
    ww = w * (0.85 + 0.15 * k); h = 200
    rrect(img, x - ww / 2 + 6, y + 10, ww, h, 34, (10, 6, 6))
    rrect(img, x - ww / 2, y, ww, h, 34, col); rrect(img, x - ww / 2 + 7, y + 7, ww - 14, h - 14, 28, CARD)
    if k > 0.6:
        al = ramp(k, 0.6, 1.0)
        dx = 40 if icon else 0
        text(img, label, x + dx, y + 58, 40, mix(col, WHITE, 0.35), POP, alpha=al)
        text(img, value, x + dx, y + 132, 86, WHITE, POP, alpha=al, scale=0.9 + 0.1 * k)
        if icon: emoji(img, icon, x - ww / 2 + 80, y + h / 2, 86, alpha=al)
def day_stamp(img, t, n, at=0.0, sub=None):
    k = back(ramp(t, at, at + 0.3))
    if k <= 0: return
    tint(img, (20, 8, 10), 0.45 * min(1, k))
    rotated(img, lambda c: (rrect(c, 240, 700, 600, 300, 40, VYEL), rrect(c, 254, 714, 572, 272, 32, CARD),
                            text(c, f'DAY {n}', 540, 850, 190, VYEL, ANT)), (540, 850), -6, 0.6 + 0.4 * k)
    if sub: text(img, sub, 540, 1080, 56, WHITE, POP, alpha=ramp(t, at + 0.3, at + 0.5))
def meter(img, t, label, v0, v1, at=0.0, y=1450, col=VGREEN):
    k = eout(ramp(t, at, at + 0.3))
    if k <= 0: return
    x0, w = 140, 800
    rrect(img, x0 - 10, y - 90, w + 20, 220, 30, CARD); rrect(img, x0 - 10, y - 90, w + 20, 220, 30, col, th=4)
    text(img, label, W / 2, y - 40, 44, WHITE, POP, alpha=k)
    v = v0 + (v1 - v0) * ease(ramp(t, at + 0.6, at + 1.6))
    rrect(img, x0 + 20, y + 20, w - 40, 60, 30, (60, 50, 50)); rrect(img, x0 + 20, y + 20, max(60, (w - 40) * v / 100), 60, 30, col)
    text(img, f'{v:.0f}%', W / 2, y + 50, 56, WHITE, POP, stroke=5, scol=CARD)
def decide(img, t, at=0.0):
    img[:] = grad(PURPLE, DEEP); k = back(ramp(t, at, at + 0.3))
    for i in range(14):
        a = i / 14 * 2 * math.pi + t * 0.4
        poly(img, [(540, 900), (540 + 1400 * math.cos(a), 900 + 1400 * math.sin(a)), (540 + 1400 * math.cos(a + 0.18), 900 + 1400 * math.sin(a + 0.18))], mix(PURPLE, DEEP, 0.5))
    text(img, 'YOU', 540, 760, 200, WHITE, ANT, scale=k, stroke=12, scol=CARD)
    text(img, 'DECIDE!', 540, 960, 240, VYEL, ANT, scale=k * (1 + 0.04 * math.sin(t * 8)), stroke=12, scol=CARD)
    emoji(img, '👇', 540, 1180, 130 * back(ramp(t, at + 0.4, at + 0.7)))
def ab_cards(img, t, a_txt, a_icon, b_txt, b_icon, at=0.0, y0=760):
    for i, (L, txt, ic, col) in enumerate((('A', a_txt, a_icon, VORANGE), ('B', b_txt, b_icon, VBLUE))):
        k = back(ramp(t, at + 0.5 * i, at + 0.5 * i + 0.3)); y = y0 + i * 330
        if k <= 0: continue
        x0 = 80 + (1 - k) * (-900 if i == 0 else 900)
        rrect(img, x0 + 8, y + 12, 920, 270, 40, (10, 6, 6)); rrect(img, x0, y, 920, 270, 40, col)
        circ(img, (x0 + 110, y + 135), 74, WHITE); text(img, L, x0 + 110, y + 140, 110, col, ANT)
        lines = txt.split('|')
        for j, ln in enumerate(lines): text(img, ln, x0 + 470, y + 135 + (j - (len(lines) - 1) / 2) * 70, 58, WHITE, POP)
        emoji(img, ic, x0 + 830, y + 135, 110)

# ---------- gags ----------
def flies(img, t, cx, cy, n=3, r=150):
    for i in range(n):
        a = t * (2.2 + 0.4 * i) + i * 2.1; x = cx + r * math.cos(a) * (1 + 0.2 * i); y = cy + 0.6 * r * math.sin(a * 1.3)
        ww = 10 * abs(math.sin(t * 40 + i))
        ell(img, (x - 7, y - 8), 9, 5 + ww * 0.4, (230, 230, 230), rot=30); ell(img, (x + 7, y - 8), 9, 5 + ww * 0.4, (230, 230, 230), rot=-30)
        circ(img, (x, y), 8, (20, 20, 20))
def stink(img, t, cx, cy, n=3, col=(90, 200, 120)):
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * 70; ph = t * 3 + i
        pts = [(x + 14 * math.sin(ph + j * 0.6), cy - j * 16 - 20 * ((t * 0.8 + i * 0.3) % 1)) for j in range(9)]
        for a, b in zip(pts, pts[1:]): line(img, a, b, col, 7)
def sweat_drops(img, t, cx, cy):
    for i in range(3):
        k = (t * 1.2 + i * 0.33) % 1; circ(img, (cx + (i - 1) * 90, cy + k * 120), 10, (250, 220, 170))

# ---------- props ----------
def pet_cat(img, t, x, y, s=1.0, awake=False, col=(70, 120, 200)):
    ell(img, (x, y), 90 * s, 46 * s, col); circ(img, (x + 70 * s, y - 20 * s), 40 * s, col)
    poly(img, [(x + 44 * s, y - 50 * s), (x + 54 * s, y - 86 * s), (x + 72 * s, y - 56 * s)], col); poly(img, [(x + 80 * s, y - 56 * s), (x + 98 * s, y - 86 * s), (x + 106 * s, y - 46 * s)], col)
    ell(img, (x - 90 * s, y + 10 * s), 50 * s, 16 * s, col, rot=-20)
    if awake:
        circ(img, (x + 58 * s, y - 24 * s), 7 * s, INK); circ(img, (x + 84 * s, y - 24 * s), 7 * s, INK)
    else:
        line(img, (x + 50 * s, y - 22 * s), (x + 64 * s, y - 22 * s), INK, 4 * s); line(img, (x + 78 * s, y - 22 * s), (x + 92 * s, y - 22 * s), INK, 4 * s)
        k = (t * 0.7) % 1; text(img, 'z', x + 120 * s + 30 * k * s, y - 80 * s - 60 * k * s, int(40 * s * (0.6 + 0.6 * k)), WHITE, POP, alpha=1 - k)
def fairy_lights(img, t, y=150, sag=60):
    pts = [(x, y + sag * math.sin(math.pi * ((x % 360) / 360))) for x in range(0, W + 1, 12)]
    for a, b in zip(pts, pts[1:]): line(img, a, b, (40, 40, 50), 3)
    cols = [VYEL, VPINK, VGREEN, VBLUE]
    for i, x in enumerate(range(30, W, 60)):
        yy = y + sag * math.sin(math.pi * ((x % 360) / 360)) + 14; c = cols[i % 4]; b = 0.6 + 0.4 * math.sin(t * 3 + i)
        glow(img, x, yy, 34, mix((0, 0, 0), c, 0.6), b * 0.8); circ(img, (x, yy), 9, mix(c, WHITE, 0.3))
def poster(img, x, y, w, h, col, icon):
    rrect(img, x, y, w, h, 6, col); rrect(img, x + 10, y + 10, w - 20, h - 20, 4, mix(col, WHITE, 0.25)); emoji(img, icon, x + w / 2, y + h / 2, min(w, h) * 0.55)
def bedroom(img, t, cat=True, lamp=True, posters=(('🏎️', VBLUE), ('🏆', VPINK))):
    img[:] = grad(PURPLE, NAVY)
    # back wall + floor
    rrect(img, 0, 1380, W, 540, 0, (60, 45, 60)); rrect(img, 0, 1380, W, 14, 0, (40, 28, 40))
    # window with moon
    rrect(img, 640, 330, 340, 380, 18, (30, 22, 30)); rrect(img, 656, 346, 308, 348, 12, (90, 40, 30))
    circ(img, (880, 430), 46, (200, 235, 250)); stars(img, t, 0.3, 700, (90, 40, 30))
    line(img, (810, 346), (810, 694), (30, 22, 30), 10); line(img, (656, 520), (964, 520), (30, 22, 30), 10)
    fairy_lights(img, t, 120, 70)
    for i, (ic, c) in enumerate(posters): poster(img, 90 + i * 250, 330 + i * 40, 200, 260, c, ic)
    # desk + monitor
    rrect(img, 40, 1120, 460, 30, 8, (50, 70, 110)); rrect(img, 70, 1150, 26, 230, 4, (40, 55, 85)); rrect(img, 444, 1150, 26, 230, 4, (40, 55, 85))
    rrect(img, 150, 900, 260, 180, 12, (30, 30, 40)); rrect(img, 162, 912, 236, 156, 6, (190, 140, 60)); rrect(img, 260, 1080, 40, 40, 4, (30, 30, 40))
    glow(img, 280, 990, 200, (120, 80, 30), 0.4)
    if lamp: glow(img, 460, 1000, 260, (40, 120, 160), 0.35)
    if cat: pet_cat(img, t, 300, 1080, 0.8)
    # bed
    rrect(img, 640, 1240, 420, 200, 26, (150, 80, 70)); rrect(img, 660, 1210, 140, 70, 24, (230, 220, 220))
def street(img, t, night=False):
    top, bot = ((110, 50, 40), (60, 30, 30)) if night else ((240, 200, 150), (225, 215, 200))
    img[:] = grad(top, bot)
    if night: stars(img, t, 0.5, 900, top)
    else: circ(img, (860, 300), 80, (170, 240, 255)); glow(img, 860, 300, 260, (60, 110, 140), 0.5)
    # houses
    for i, (x, w, h, col) in enumerate(((-40, 360, 520, (150, 170, 210)), (360, 380, 600, (120, 150, 190)), (780, 360, 480, (170, 190, 220)))):
        y = 1300 - h; rrect(img, x, y, w, h, 6, col if not night else mix(col, NAVY, 0.6)); poly(img, [(x - 20, y), (x + w / 2, y - 160), (x + w + 20, y)], (70, 80, 150) if not night else (50, 40, 80))
        for wx in (x + 70, x + w - 130):
            rrect(img, wx, y + 120, 70, 90, 6, (120, 200, 240) if night else (230, 210, 170))
    rrect(img, 0, 1300, W, 620, 0, (90, 90, 95)); rrect(img, 0, 1300, W, 40, 0, (170, 170, 175))
    for x in range(0, W, 220): rrect(img, x + 40, 1640, 120, 18, 6, (220, 230, 240))
def office(img, t, sign='DRIVING TEST'):
    img[:] = grad((200, 205, 200), (160, 170, 170))
    rrect(img, 0, 1380, W, 540, 0, (110, 120, 130))
    rrect(img, 240, 260, 600, 140, 14, (60, 120, 40)); text(img, sign, 540, 330, 80, WHITE, ANT)
    for i in range(3): rrect(img, 80 + i * 330, 520, 250, 300, 8, (225, 230, 230)); rrect(img, 80 + i * 330, 520, 250, 300, 8, (150, 150, 150), th=3)
    rrect(img, 130, 1150, 820, 60, 10, (60, 90, 140)); rrect(img, 160, 1210, 760, 170, 0, (50, 75, 120))
def car(img, x, y, s=1.0, col=(60, 60, 220), lights=False):
    """side view, x,y = centre bottom of the body"""
    rrect(img, x - 330 * s, y - 170 * s, 660 * s, 150 * s, 50 * s, col)
    poly(img, [(x - 200 * s, y - 165 * s), (x - 120 * s, y - 290 * s), (x + 140 * s, y - 290 * s), (x + 230 * s, y - 165 * s)], col)
    poly(img, [(x - 170 * s, y - 170 * s), (x - 105 * s, y - 268 * s), (x + 10 * s, y - 268 * s), (x + 10 * s, y - 170 * s)], (230, 210, 170))
    poly(img, [(x + 30 * s, y - 170 * s), (x + 30 * s, y - 268 * s), (x + 132 * s, y - 268 * s), (x + 200 * s, y - 170 * s)], (230, 210, 170))
    for wx in (-200, 200): circ(img, (x + wx * s, y - 20 * s), 70 * s, (40, 40, 45)); circ(img, (x + wx * s, y - 20 * s), 34 * s, (180, 180, 185))
    if lights: glow(img, x + 330 * s, y - 120 * s, int(140 * s), (80, 200, 255), 0.8)
    circ(img, (x + 315 * s, y - 120 * s), 16 * s, (120, 230, 255))

# ---------- character ----------
def hero(img, t, L, hx, hy, s=1.0, expr='smile', gross=0.0, helmet=None, glasses=None, **kw):
    """kit.person + reference-E gags. gross 0..1 adds flies + stink lines; helmet = colour of a bike helmet."""
    bob = 6 * s * math.sin(t * 4)
    if gross > 0: stink(img, t, hx, hy - 120 * s + bob, 3)
    hands = person(img, L, hx, hy + bob, s, expr, blink=(t % 3.3) < 0.12, **kw)
    if helmet:
        ell(img, (hx, hy - 40 * s + bob), 104 * s, 86 * s, helmet, 180, 360); rrect(img, hx - 104 * s, hy - 50 * s + bob, 208 * s, 22 * s, 10 * s, mix(helmet, INK, 0.3))
        for dx in (-40, 0, 40): rrect(img, hx + (dx - 8) * s, hy - 116 * s + bob, 16 * s, 50 * s, 6 * s, mix(helmet, WHITE, 0.4))
        line(img, (hx - 80 * s, hy - 30 * s + bob), (hx - 50 * s, hy + 70 * s + bob), INK, 5 * s); line(img, (hx + 80 * s, hy - 30 * s + bob), (hx + 50 * s, hy + 70 * s + bob), INK, 5 * s)
    if glasses:
        for sx in (-1, 1): circ(img, (hx + sx * 34 * s, hy - 2 * s + bob), 27 * s, glasses, int(max(2, 6 * s)))
        line(img, (hx - 8 * s, hy - 4 * s + bob), (hx + 8 * s, hy - 4 * s + bob), glasses, 5 * s)
    if gross > 0: flies(img, t, hx, hy - 40 * s, int(1 + 2 * gross), 160 * s)
    return hands
