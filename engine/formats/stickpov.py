"""STICK POV format (Stick-Motion style): flat 2D rooms, stick people with round black heads and hoodies,
HUD clock (top-left) + countdown (top-right), phone close-ups held by a hand, A/B choice end card.
Use with VOICE='suspense', CAPTION='karaoke', MOOD={'style': 'tension'}."""
import math, random
import numpy as np, cv2
from kit import *

INK2 = (18, 16, 16); LINEC = (200, 220, 230)
HUD = {'clock': (3, 12), 'pm': False, 'tag': 'DAY 1', 'place': 'TRAIN', 'cd_label': 'NEXT STOP IN', 'cd_end': None, 'cd_from': 60}

def hud(img, T, cd=None, a=1.0, red=False):
    """T = absolute video time (for the ticking clock)"""
    if a <= 0.02: return
    h, m = HUD['clock']; mm = m + int(T // 12); hh = h + mm // 60; mm %= 60
    text(img, ('• ' + HUD['tag']), 120, 128, 30, RED, INTER_B, alpha=a)
    text(img, f'{hh}:{mm:02d}', 150, 182, 80, WHITE, INTER_B, alpha=a); text(img, 'PM' if HUD['pm'] else 'AM', 262, 196, 30, WHITE, INTER_B, alpha=a)
    text(img, HUD['place'], 120, 236, 24, (170, 170, 175), INTER_B, alpha=a)
    if cd is not None:
        text(img, HUD['cd_label'], W - 170, 128, 24, (170, 170, 175), INTER_B, alpha=a)
        s = max(0, cd); col = RED if (red or s < 10) else YEL
        text(img, f'{int(s // 60)}:{int(s % 60):02d}', W - 170, 180, 76, col, INTER_B, alpha=a)

def train(img, t, speed=1.0, outside=None, dark=0.0, light_flicker=False):
    """train interior. outside(img, t, x0, y0, w, h) draws what is seen through the windows."""
    wall = mix((70, 78, 66), (20, 22, 20), dark); img[:] = wall
    img[1350:] = mix((40, 44, 40), (10, 10, 10), dark)
    for wx in (60, 410, 760):
        rrect(img, wx - 8, 520, 276, 336, 26, mix((40, 40, 40), INK2, dark))
        sub = img[528:848, wx:wx + 260]
        sub[:] = (20, 16, 14)
        if outside: outside(sub, t, wx)
        else:
            for k in range(6):   # tunnel lights rushing by
                x = int((k * 140 - t * 2400 * speed + wx * 3) % 520) - 130
                cv2.rectangle(sub, (x, 150), (x + 60, 162), (150, 210, 240), -1)
        cv2.rectangle(sub, (0, 0), (259, 319), (90, 90, 90), 3)
    for px in (330, 690): rrect(img, px - 9, 380, 18, 1000, 9, (150, 160, 165))
    line(img, (0, 470), (W, 470), (150, 160, 165), 8)
    for sx in range(40, W, 240): rrect(img, sx, 1130, 200, 70, 18, mix((60, 80, 150), (20, 20, 30), dark)); rrect(img, sx, 1195, 200, 150, 10, mix((40, 55, 110), (15, 15, 25), dark))
    if light_flicker and int(t * 13) % 7 == 0: tint(img, (0, 0, 0), 0.5)
    glow(img, W / 2, 380, 500, (40, 50, 50), 0.4 * (1 - dark))

def stick(img, x, y, s=1.0, hood=(200, 120, 40), face='flat', look=0, arm=None, lamp=False, phone=False, a=1.0):
    """stick person; (x, y) = feet. face: flat|shock|o|happy|closed"""
    hx, hy = x, y - 560 * s
    for dx in (-22, 22): line(img, (x + dx * s * 0.6, y - 200 * s), (x + dx * s, y), INK2, 12 * s); line(img, (x + dx * s, y), (x + dx * s + 26 * s, y), INK2, 12 * s)
    rrect(img, x - 70 * s, hy + 100 * s, 140 * s, 270 * s, 50 * s, hood)
    rrect(img, x - 52 * s, hy + 80 * s, 104 * s, 60 * s, 30 * s, mix(hood, INK2, 0.25))
    if arm == 'up': line(img, (x + 60 * s, hy + 150 * s), (x + 120 * s, hy + 20 * s), hood, 34 * s)
    elif arm == 'phone':
        line(img, (x + 50 * s, hy + 160 * s), (x + 110 * s, hy + 220 * s), hood, 34 * s); rrect(img, x + 95 * s, hy + 150 * s, 40 * s, 70 * s, 8 * s, INK2)
        glow(img, x + 115 * s, hy + 170 * s, int(120 * s), (120, 90, 60), 0.8)
    circ(img, (hx, hy), 86 * s, INK2); cv2.circle(img, P(hx, hy), int(86 * s * 8), LINEC, 2, cv2.LINE_AA, 3)
    ex = look * 18 * s
    for sx in (-1, 1):
        c = (hx + sx * 28 * s + ex, hy - 6 * s)
        if face == 'closed': line(img, (c[0] - 12 * s, c[1]), (c[0] + 12 * s, c[1]), WHITE, 5 * s)
        else: ell(img, c, (13 if face in ('shock', 'o') else 10) * s, (20 if face in ('shock', 'o') else 16) * s, WHITE)
    if face == 'o': ell(img, (hx + ex, hy + 46 * s), 10 * s, 14 * s, WHITE)
    elif face == 'happy': ell(img, (hx + ex, hy + 36 * s), 22 * s, 14 * s, WHITE, 20, 160, int(5 * s))
    elif face == 'shock': ell(img, (hx + ex, hy + 46 * s), 14 * s, 20 * s, WHITE)
    if lamp:
        rrect(img, hx - 70 * s, hy - 92 * s, 140 * s, 50 * s, 25 * s, (40, 120, 240))
        glow(img, hx + 120 * s, hy - 50 * s, int(260 * s), (120, 200, 230), 1.0)

def hand_phone(img, t, draw_screen, rise=1.0, x=W / 2, y=1020):
    """a hand holding a phone from the bottom-right, like a POV close-up"""
    oy = (1 - eout(rise)) * 900
    line(img, (x + 160, y + 380 + oy), (x + 420, y + 900 + oy), (200, 120, 40), 120)
    rrect(img, x - 230, y - 470 + oy, 460, 940, 70, (30, 30, 34)); rrect(img, x - 214, y - 454 + oy, 428, 908, 58, (18, 14, 14))
    rrect(img, x - 60, y - 440 + oy, 120, 30, 15, (30, 30, 34))
    circ(img, (x + 170, y + 380 + oy), 70, (150, 185, 232))
    draw_screen(img, x, y + oy, 400, 860)

def lock_screen(img, cx, cy, w, h, time_txt, sub='Tuesday, November 3', note=None):
    y0, y1 = int(cy - h / 2), int(cy + h / 2); x0 = int(cx - w / 2); g = grad((120, 40, 60), (60, 20, 30), 0, int(h))[:, :int(w)]
    ya, yb = max(0, y0), min(H, y1)
    if yb > ya: img[ya:yb, x0:x0 + int(w)] = g[ya - y0:yb - y0]
    text(img, sub, cx, cy - h / 2 + 150, 30, WHITE, INTER_M); text(img, time_txt, cx, cy - h / 2 + 240, 130, WHITE, INTER_B)
    if note:
        rrect(img, cx - w / 2 + 20, cy - 40, w - 40, 110, 24, (90, 70, 70)); text(img, note, cx, cy + 15, 32, WHITE, INTER_B)

def chat_screen(img, cx, cy, w, h, title, msgs, t, per=0.6):
    """msgs: list of (side 'l'/'r', text, appear_time)"""
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    img[max(0, y0):max(0, min(H, y0 + int(h))), x0:x0 + int(w)] = (20, 18, 18)
    circ(img, (cx, y0 + 80), 36, (200, 80, 220)); text(img, title[0], cx, y0 + 80, 40, WHITE, INTER_B); text(img, title, cx, y0 + 140, 26, WHITE, INTER_B)
    y = y0 + 200
    for side, txt, at in msgs:
        if t < at: break
        k = back(ramp(t, at, at + 0.2)); tw = min(w - 90, twidth(txt, 28, INTER_M) + 40)
        bx = x0 + 24 if side == 'l' else x0 + w - 24 - tw; col = (60, 58, 58) if side == 'l' else (230, 130, 40)
        rrect(img, bx, y, tw * k, 64, 22, col); text(img, txt, bx + tw / 2, y + 32, 28, WHITE, INTER_M, alpha=k); y += 84

def choice_end(img, t, a_txt, b_txt, part='PART 2', bg=None):
    if bg: bg(img, t)
    tint(img, (0, 0, 0), 0.55)
    for i, (L_, txt, col) in enumerate((('A', a_txt, YEL), ('B', b_txt, RED))):
        k = back(ramp(t, 0.15 + i * 0.2, 0.45 + i * 0.2)); y = 860 + i * 170
        rrect(img, 150 + (1 - k) * 400, y - 60, 780, 120, 22, col); rrect(img, 156 + (1 - k) * 400, y - 54, 768, 108, 18, INK2)
        rrect(img, 180 + (1 - k) * 400, y - 36, 72, 72, 14, col); text(img, L_, 216 + (1 - k) * 400, y, 52, INK2, INTER_B)
        text(img, txt, 590 + (1 - k) * 400, y, 46, WHITE, INTER_B)
    q = ramp(t, 0.8, 1.1); pul = 1 + 0.05 * math.sin(t * 8)
    text(img, 'FOLLOW FOR', W / 2, 1290, 54, WHITE, INTER_B, alpha=q); text(img, part, W / 2, 1380, 110, YEL, ANT, alpha=q, scale=pul)
    text(img, 'COMMENT  A  OR  B', W / 2, 1490, 40, (190, 190, 195), INTER_B, alpha=q)
