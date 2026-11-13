"""CHAT format: a funny text-message story on a phone UI. Each LINE is one message read aloud
(voice per line: e.g. 'bro' for one side, 'old'/'girl'/'mom' for the other). Use CAPTION='none', MOOD={'style': 'funny'}.
Episode builds MSGS = [dict(side='l'|'r', text=..., emoji='', punch=False)] aligned 1:1 with LINES (narrator lines: side='n')."""
import math, random
import numpy as np, cv2
from kit import *

UI_BG = (12, 10, 10); BL = (70, 64, 62); BR = (255, 132, 10); TXT = (245, 245, 245); SUB = (150, 150, 155)
TOP = 300; BOTTOM = 1560; FS = 52; PAD = 34; MAXW = 800
CHAT = {'name': 'Contact', 'avatar': '🙂', 'status': 'online', 'me': 'Me'}

def wrap_text(s, size=None, maxw=None):
    size = size or FS; maxw = maxw or (MAXW - 2 * PAD - 80)
    words = s.split(' '); lines = ['']
    for w in words:
        trial = (lines[-1] + ' ' + w).strip()
        if twidth(trial, size, INTER_M) > maxw and lines[-1]: lines.append(w)
        else: lines[-1] = trial
    return lines

def layout(msgs):
    """returns per-message (x, y, w, h, lines) in an infinite column starting at 0"""
    out = []; y = 0
    for m in msgs:
        if m['side'] == 'n': out.append(None); continue
        ls = wrap_text(m['text']); w = max(twidth(l_, FS, INTER_M) for l_ in ls) + 2 * PAD + (80 if m.get('emoji') else 0)
        h = len(ls) * 66 + 2 * 24; x = 40 if m['side'] == 'l' else W - 40 - w
        out.append((x, y, w, h, ls)); y += h + 22 + (26 if m.get('react') else 0)
    return out

def header(img):
    rrect(img, 0, 0, W, 250, 0, (28, 26, 26))
    poly(img, [(70, 170), (100, 140), (100, 200)], BR)
    circ(img, (W / 2, 120), 58, (90, 80, 78)); emoji(img, CHAT['avatar'], W / 2, 120, 70)
    text(img, CHAT['name'], W / 2, 205, 38, TXT, INTER_B)
    text(img, CHAT['status'], W / 2, 238, 24, (110, 200, 110), INTER_M)

def draw(img, t, msgs, starts, punch_scale=True):
    """t = absolute time; starts[i] = time message i appears"""
    img[:] = UI_BG
    L = layout(msgs); vis = [i for i, s in enumerate(starts) if s <= t and L[i]]
    nxt = next((i for i, s in enumerate(starts) if s > t), None)
    typing = nxt is not None and msgs[nxt]['side'] == 'l' and starts[nxt] - t < 0.9 and L[nxt]
    # scroll so that the newest bubble (or typing dots) sits above BOTTOM
    last_bottom = 0
    if vis: x, y, w, h, _ = L[vis[-1]]; last_bottom = y + h
    if typing: last_bottom = (L[vis[-1]][1] + L[vis[-1]][3] + 22 if vis else 0) + 90
    # smooth scroll
    target = max(0, last_bottom - (BOTTOM - TOP))
    if vis:
        prev = vis[:-1]; pb = (L[prev[-1]][1] + L[prev[-1]][3]) if prev else 0
        prev_target = max(0, pb - (BOTTOM - TOP)); k = eout(ramp(t, starts[vis[-1]], starts[vis[-1]] + 0.25))
        scroll = prev_target + (target - prev_target) * k
    else: scroll = 0
    for i in vis:
        x, y, w, h, ls = L[i]; m = msgs[i]; yy = TOP + y - scroll
        if yy + h < 260 or yy > BOTTOM + 40: continue
        k = back(ramp(t, starts[i], starts[i] + 0.22)); col = BL if m['side'] == 'l' else BR
        cx = x + w / 2; sc = 0.5 + 0.5 * k
        bw, bh = w * sc, h * sc; bx = (x if m['side'] == 'l' else x + w - bw)
        rrect(img, bx, yy + h - bh, bw, bh, 34 * sc, col)
        if k > 0.7:
            for j, l_ in enumerate(ls): text(img, l_, x + PAD + twidth(l_, FS, INTER_M) / 2, yy + 24 + 33 + j * 66, FS, TXT, INTER_M)
            if m.get('emoji'): emoji(img, m['emoji'], x + w - PAD - 34, yy + h / 2, 64)
        if m.get('react') and t > starts[i] + 0.5:
            q = back(ramp(t, starts[i] + 0.5, starts[i] + 0.7)); rx = x + w - 20 if m['side'] == 'l' else x + 20
            circ(img, (rx, yy + h + 4), 32 * q, (40, 38, 38)); emoji(img, m['react'], rx, yy + h + 4, 42 * q)
    if typing:
        yy = TOP + (L[vis[-1]][1] + L[vis[-1]][3] + 22 if vis else 0) - scroll
        rrect(img, 40, yy, 150, 76, 38, BL)
        for j in range(3): circ(img, (82 + j * 34, yy + 38 - 10 * max(0, math.sin(t * 9 - j * 0.8))), 10, SUB)
    header(img)
    rrect(img, 0, BOTTOM + 70, W, H - BOTTOM - 70, 0, (28, 26, 26)); rrect(img, 40, BOTTOM + 100, W - 180, 80, 40, (50, 48, 48), 2)
    text(img, 'iMessage', 170, BOTTOM + 140, 30, SUB, INTER_M); circ(img, (W - 80, BOTTOM + 140), 36, BR)

def burst(img, t, at, ch, cx=W / 2, cy=900, n=14):
    """emoji explosion for punchlines"""
    if not (at <= t < at + 1.2): return
    rb = random.Random(int(at * 100)); u = t - at
    for i in range(n):
        a = rb.uniform(-math.pi, 0); sp = rb.uniform(500, 1200)
        x = cx + math.cos(a) * sp * u; y = cy + math.sin(a) * sp * u + 900 * u * u
        emoji(img, ch, x, y, rb.uniform(60, 110), alpha=1 - ramp(u, 0.8, 1.2), rot=rb.uniform(-30, 30))

def punch(img, t, at, cx=W / 2, cy=900, amt=0.12):
    """quick zoom punch around a point"""
    k = ramp(t, at, at + 0.08) * (1 - ramp(t, at + 0.25, at + 0.6))
    if k <= 0: return
    z = 1 + amt * k; M = cv2.getRotationMatrix2D((cx, cy), random.uniform(-1.5, 1.5) * k, z)
    img[:] = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REPLICATE)

def title_card(img, t, top, big_txt, sub, ch='💸'):
    img[:] = grad((40, 20, 60), (10, 6, 20))
    for i in range(14):
        a = i / 14 * 6.283 + t * 0.6; line(img, (W / 2, 900), (W / 2 + 1500 * math.cos(a), 900 + 1500 * math.sin(a)), (60, 30, 80), 60)
    k = back(ramp(t, 0, 0.3)); emoji(img, ch, W / 2, 700, 260 * k, rot=8 * math.sin(t * 5))
    text(img, top, W / 2, 1000, 60, WHITE, INTER_B, alpha=ramp(t, 0.15, 0.4))
    text(img, big_txt, W / 2, 1110, 120, YEL, ANT, scale=0.6 + 0.4 * back(ramp(t, 0.25, 0.55)), stroke=8, scol=INK)
    text(img, sub, W / 2, 1230, 46, WHITE, INTER_B, alpha=ramp(t, 0.5, 0.8))
