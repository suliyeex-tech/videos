"""QUIZ format (game-show trivia): bright gradient stage, 'QUESTION n/5' chip, progress dots, white question card,
three answer buttons A/B/C, a 3-second ring timer with ticks (silent LINES beat), reveal (correct = green + check,
wrong = dimmed), a big emoji pop and a fun-fact pill. Host name chip top-left.
Use with VOICE='girl' or 'guy', CAPTION='karaoke' (CAPS only on reveal lines), MOOD={'style': 'hype'}."""
import math, random
import numpy as np, cv2
from kit import *

QZ = {'host': 'Host', 'host_emoji': '🎤', 'total': 5}
BG1 = (120, 40, 90); BG2 = (60, 20, 40); BTN = (255, 255, 255); OK = (90, 200, 60); BAD = (70, 60, 200)

def stage(img, t):
    img[:] = grad(BG1, BG2)
    for i in range(16):
        a = i / 16 * 6.283 + t * 0.25
        line(img, (W / 2, 820), (W / 2 + 1600 * math.cos(a), 820 + 1600 * math.sin(a)), mix(BG1, (255, 255, 255), 0.05), 70)
    rb = random.Random(4)
    for i in range(30):
        x = rb.uniform(0, W); y = (rb.uniform(0, H) - t * rb.uniform(30, 90)) % H
        circ(img, (x, y), rb.uniform(3, 8), mix(BG1, (255, 255, 255), 0.25))

def top_bar(img, qn, done, t=0):
    """qn: current question number (1-based); done: list of booleans for revealed questions"""
    hw = twidth(QZ['host'], 26, INTER_B) + 120; rrect(img, 50, 120, hw, 80, 40, (255, 255, 255)); emoji(img, QZ['host_emoji'], 95, 160, 48)
    text(img, QZ['host'], 135 + twidth(QZ['host'], 26, INTER_B) / 2, 160, 26, INK, INTER_B)
    if qn:
        lab = f'QUESTION {qn}/{QZ["total"]}'; rrect(img, W - 50 - 330, 120, 330, 80, 40, YEL)
        text(img, lab, W - 50 - 165, 160, 36, INK, ANT)
    for i in range(QZ['total']):
        x = W / 2 - (QZ['total'] - 1) * 40 + i * 80; y = 270
        col = OK if i < len(done) and done[i] else ((255, 255, 255) if i == qn - 1 else mix(BG1, (255, 255, 255), 0.3))
        circ(img, (x, y), 20 if i != qn - 1 else 26, col)

def question_card(img, t, q, at=0.0):
    k = back(ramp(t, at, at + 0.3))
    if k <= 0: return
    words = q.split(' '); lines = ['']
    for w in words:
        tr = (lines[-1] + ' ' + w).strip()
        if twidth(tr, 64, INTER_B) > 820 and lines[-1]: lines.append(w)
        else: lines[-1] = tr
    h = 120 + 80 * len(lines); y0 = 360
    rrect(img, 70, y0 + (1 - k) * 60, 940, h, 40, (255, 255, 255))
    for i, l_ in enumerate(lines): text(img, l_, W / 2, y0 + 100 + i * 80 + (1 - k) * 60, 64, INK, INTER_B, alpha=min(1, k))
    return y0 + h

def answers(img, t, opts, at=0.3, reveal=None, correct=0, y0=760):
    for i, o in enumerate(opts):
        k = back(ramp(t, at + i * 0.15, at + i * 0.15 + 0.25))
        if k <= 0: continue
        y = y0 + i * 150; x = 110 + (1 - k) * 600
        col = BTN; fg = INK
        if reveal is not None and t >= reveal:
            if i == correct: col = OK; fg = WHITE
            else: col = mix(BTN, BG2, 0.55); fg = mix(INK, BG2, 0.3)
        sc = 1.0 + (0.06 * math.sin(min(1, (t - reveal) / 0.3) * math.pi) if (reveal is not None and t >= reveal and i == correct) else 0)
        rrect(img, x - 10 * (sc - 1) * 50, y - 5 * (sc - 1) * 50, 860 * sc, 120 * sc, 60, col)
        circ(img, (x + 62, y + 60), 42, INK if col == BTN else WHITE)
        text(img, 'ABC'[i], x + 62, y + 60, 50, WHITE if col == BTN else col, ANT)
        text(img, o, x + 150 + twidth(o, 54, INTER_B) / 2, y + 60, 54, fg, INTER_B)
        if reveal is not None and t >= reveal and i == correct: text(img, 'CORRECT', x + 760, y + 60, 34, WHITE, ANT, alpha=ramp(t, reveal + 0.1, reveal + 0.3))

def timer(img, t, t0, dur=3.0, cx=W / 2, cy=1330):
    if t < t0 - 0.2: return
    u = clamp((t - t0) / dur); left = max(0, math.ceil(dur - (t - t0)))
    k = back(ramp(t, t0 - 0.2, t0 + 0.1))
    circ(img, (cx, cy), 120 * k, INK); cv2.ellipse(img, P(cx, cy), (int(105 * k * 8), int(105 * k * 8)), -90, 0, 360 * (1 - u), YEL if left > 1 else RED, 18, cv2.LINE_AA, 3)
    if t < t0 + dur: text(img, str(left), cx, cy, 120, WHITE, ANT, scale=k * (1 + 0.15 * (1 - ((t - t0) % 1))))

def big_emoji(img, t, ch, at, cx=W / 2, cy=1330, size=260):
    if t < at: return
    k = back(ramp(t, at, at + 0.3)); emoji(img, ch, cx, cy, size * k, rot=6 * math.sin(t * 6))
    rb = random.Random(int(at * 10)); u = t - at
    if u < 1.0:
        for i in range(14):
            a = rb.uniform(0, 6.283); r = 500 * eout(u); circ(img, (cx + math.cos(a) * r, cy + math.sin(a) * r), 12 * (1 - u), rb.choice([YEL, OK, (255, 255, 255), RED]))
