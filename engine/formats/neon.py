"""NEON format (darkset-style): black stage, glowing blue figure, thin white line icons, sentence captions on top.
Use with CAPTION='top', VOICE='hype', MOOD={'style': 'hype'}, TICKS=True."""
import math, random
import numpy as np, cv2
from kit import *

BG = (12, 9, 8); NB = (255, 185, 70)      # neon blue (BGR)
NW = (235, 235, 240); DIM = (90, 90, 95); GOLD = (60, 200, 255); NRED = (80, 70, 255)
FLOOR = 1240
rp = random.Random(9)
DUST = [(rp.uniform(0, W), rp.uniform(380, 1500), rp.uniform(1.5, 4), rp.uniform(0, 6.28)) for _ in range(70)]

def stage(img, t, floor=True, dust=True):
    img[:] = BG
    glow(img, W / 2, 900, 700, (30, 20, 10), 0.8)
    if dust:
        for x, y, r, ph in DUST:
            a = 0.25 + 0.25 * math.sin(t * 1.5 + ph); circ(img, (x + 8 * math.sin(t * 0.3 + ph), y - 6 * t % 40), r, mix(BG, NB, a))
    if floor:
        for x in range(40, W - 40, 22): line(img, (x, FLOOR), (x + 10, FLOOR), (70, 70, 75), 2)

def neon_glow(img, cx, cy, r, col=NB, k=1.0): glow(img, cx, cy, int(r), tuple(int(c * 0.55) for c in col), k)

def fig(img, x, y, s=1.0, col=NB, a=1.0, g=True, grad=False, sad=False):
    """glowing person icon standing on y (feet)."""
    if a <= 0.02: return
    c = mix(BG, col, a)
    if g: neon_glow(img, x, y - 90 * s, 130 * s, col, 0.9 * a)
    circ(img, (x, y - 150 * s), 30 * s, c)
    poly(img, [(x - 52 * s, y), (x - 45 * s, y - 75 * s), (x - 20 * s, y - 108 * s), (x + 20 * s, y - 108 * s), (x + 45 * s, y - 75 * s), (x + 52 * s, y)], c)
    if grad: rrect(img, x - 34 * s, y - 192 * s, 68 * s, 14 * s, 3, NW); poly(img, [(x - 40 * s, y - 186 * s), (x, y - 204 * s), (x + 40 * s, y - 186 * s)], NW)
    if sad: line(img, (x - 10 * s, y - 136 * s), (x + 10 * s, y - 136 * s), BG, 4 * s)

def label(img, x, y, txt, col=NW, a=1.0, size=30):
    if a <= 0.02: return
    w = twidth(txt, size, INTER_B) + 34
    rrect(img, x - w / 2, y - size * 0.75, w, size * 1.5, size * 0.75, mix(BG, col, 0.9 * a), 2)
    text(img, txt, x, y + 1, size, mix(BG, col, a), INTER_B)

def big(img, txt, x, y, size=120, col=NW, a=1.0, sc=1.0, font=None):
    if col != NW: neon_glow(img, x, y, size * 1.6, col, 0.5 * a)
    text(img, txt, x, y, size, mix(BG, col, a), font or INTER_B, scale=sc)

def window(img, cx, cy, w, h, title='', a=1.0, col=NW):
    if a <= 0.02: return
    c = mix(BG, col, a)
    rrect(img, cx - w / 2, cy - h / 2, w, h, 10, c, 3); line(img, (cx - w / 2, cy - h / 2 + 44), (cx + w / 2, cy - h / 2 + 44), c, 2)
    for i in range(3): circ(img, (cx - w / 2 + 22 + i * 22, cy - h / 2 + 22), 6, c)
    if title: text(img, title, cx, cy - h / 2 + 22, 24, c, INTER_B)

def phone(img, cx, cy, s=1.0, a=1.0, col=NW, screen=None):
    if a <= 0.02: return
    c = mix(BG, col, a); w, h = 260 * s, 520 * s
    rrect(img, cx - w / 2, cy - h / 2, w, h, 36 * s, c, max(2, int(4 * s)))
    rrect(img, cx - 40 * s, cy - h / 2 + 14 * s, 80 * s, 18 * s, 9 * s, c)
    if screen: screen(cx, cy, w - 30 * s, h - 70 * s)

def feed(img, cx, cy, w, h, off, a=1.0, hi=None):
    """scrolling feed cards inside a rect; off = scroll offset px; hi(i)-> colour for card i"""
    y0 = cy - h / 2; ch = 150
    sub = img[int(y0):int(y0 + h), int(cx - w / 2):int(cx + w / 2)]
    k0 = int(off // (ch + 16))
    for k in range(k0, k0 + int(h / (ch + 16)) + 2):
        y = k * (ch + 16) - off
        col = hi(k) if hi else DIM
        cv2.rectangle(sub, (8, int(y)), (int(w) - 8, int(y + ch)), mix(BG, col, a), 2, cv2.LINE_AA)
        cv2.rectangle(sub, (20, int(y + 14)), (int(w * 0.45), int(y + ch - 14)), mix(BG, col, a * 0.6), -1, cv2.LINE_AA)
        for j in range(3): cv2.rectangle(sub, (int(w * 0.5), int(y + 24 + j * 34)), (int(w * (0.9 - 0.12 * j)), int(y + 38 + j * 34)), mix(BG, col, a * 0.7), -1)

def slot(img, cx, cy, t, spin=True, a=1.0, win=False):
    c = mix(BG, NW, a)
    rrect(img, cx - 200, cy - 170, 400, 340, 30, c, 4); rrect(img, cx - 160, cy - 110, 320, 150, 12, c, 3)
    syms = ['7', '$', '?', '*', '7', '$']
    for i in range(3):
        x = cx - 107 + i * 107
        if spin and not win:
            v = int(t * 18 + i * 3) % len(syms); y = cy - 35 + ((t * 18 + i * 3) % 1) * 40 - 20
        else: v = 0; y = cy - 35
        text(img, syms[v], x, y, 90, GOLD if win else NW, INTER_B, alpha=a)
        if i < 2: line(img, (x + 53, cy - 105), (x + 53, cy + 35), c, 2)
    lev = -50 + 100 * (0.5 + 0.5 * math.sin(t * 4)) if spin else -50
    line(img, (cx + 200, cy), (cx + 260, cy - 20 + lev), c, 6); circ(img, (cx + 260, cy - 20 + lev), 22, NRED)

def curve(img, t, x0, y0, w, h, kind='vr', a=1.0, col=NB, lab=''):
    """response curves: 'vr' straight steep, 'fi' scallops, 'fr' steps"""
    k = eout(ramp(t, 0, 1.4)); pts = []
    for i in range(int(60 * k) + 1):
        u = i / 60
        if kind == 'vr': v = u
        elif kind == 'fr': v = u * 0.85 - 0.04 * ((u * 8) % 1)
        else: v = u * 0.55 * (0.4 + 0.6 * ((u * 5) % 1) ** 2)
        pts.append((x0 + u * w, y0 - v * h))
    for p, q in zip(pts, pts[1:]): line(img, p, q, mix(BG, col, a), 6 if kind == 'vr' else 3)
    if pts and lab: label(img, pts[-1][0] - 30, pts[-1][1] - 40, lab, col, a, 26)

def counter_text(v): return f'{int(v):,}'
