"""Shared drawing kit for the daily 'what if' survival shorts (1080x1920, 30 fps). Colours are BGR."""
import os, math, random
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
BEB = f'{HERE}/fonts/bebas-neue-latin-400-normal.woff'
ANT = f'{HERE}/fonts/anton-latin-400-normal.woff'
INTER_B = f'{HERE}/fonts/inter-bold.otf'; INTER_M = f'{HERE}/fonts/inter-medium.otf'
SERIF_I = f'{HERE}/fonts/lora-italic.ttf'; POP = f'{HERE}/fonts/poppins-bold.ttf'
WHITE = (248, 246, 244); RED = (58, 48, 235); YEL = (70, 200, 255); INK = (30, 22, 20); CREAM = (215, 235, 245)
GREEN = (110, 200, 80); ORANGE = (40, 140, 240); BLUE = (200, 120, 40); SKY = (235, 190, 120); GREY = (150, 150, 155)
SKINS = [(140, 185, 232), (100, 150, 205), (70, 110, 160), (160, 200, 240)]

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x):
    x = clamp(x); c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def ramp(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def mix(c1, c2, k): return tuple(int(c1[i] * (1 - k) + c2[i] * k) for i in range(3))

# ---------- text ----------
_fc, _tc = {}, {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]
def tsprite(s, size, col, path=BEB, stroke=0, scol=(0, 0, 0)):
    k = (s, size, col, path, stroke, scol)
    if k not in _tc:
        f = font(path, size); l, t, r, b = f.getbbox(s, stroke_width=stroke); pad = 6
        im = Image.new('RGBA', (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((pad - l, pad - t), s, font=f, fill=(col[2], col[1], col[0], 255), stroke_width=stroke, stroke_fill=(scol[2], scol[1], scol[0], 255))
        a = np.array(im); _tc[k] = (a[:, :, 2::-1].astype(np.float32), a[:, :, 3:4].astype(np.float32) / 255)
    return _tc[k]
def blit(img, rgb, al, cx, cy, alpha=1.0, scale=1.0):
    if alpha <= 0.003: return
    if abs(scale - 1) > 0.01:
        nw, nh = max(1, int(rgb.shape[1] * scale)), max(1, int(rgb.shape[0] * scale))
        rgb = cv2.resize(rgb, (nw, nh)); al = cv2.resize(al, (nw, nh))[:, :, None]
    h, w = rgb.shape[:2]; x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb: return
    r = rgb[ya - y0:yb - y0, xa - x0:xb - x0]; a = al[ya - y0:yb - y0, xa - x0:xb - x0] * alpha
    reg = img[ya:yb, xa:xb]; reg[:] = (reg * (1 - a) + r * a).astype(np.uint8)
def text(img, s, cx, cy, size, col=WHITE, path=BEB, alpha=1.0, scale=1.0, stroke=0, scol=(0, 0, 0)):
    size = int(size)
    if size < 6 or alpha <= 0.003 or scale <= 0.02 or not s: return
    rgb, al = tsprite(s, size, col, path, stroke, scol); blit(img, rgb, al, cx, cy, alpha, scale)
def twidth(s, size, path=BEB, stroke=0): return tsprite(s, size, WHITE, path, stroke)[0].shape[1] - 12

# ---------- shapes ----------
def P(x, y): return (int(round(x * 8)), int(round(y * 8)))
def line(img, a, b, col, th): cv2.line(img, P(*a), P(*b), col, max(1, int(th)), cv2.LINE_AA, 3)
def circ(img, c, r, col, th=-1): cv2.circle(img, P(*c), max(1, int(r * 8)), col, int(th), cv2.LINE_AA, 3)
def ell(img, c, ax, ay, col, a0=0, a1=360, th=-1, rot=0): cv2.ellipse(img, P(*c), (max(1, int(ax * 8)), max(1, int(ay * 8))), rot, a0, a1, col, int(th), cv2.LINE_AA, 3)
def poly(img, pts, col): cv2.fillPoly(img, [np.array([P(*p) for p in pts], np.int32)], col, cv2.LINE_AA, 3)
def rrect(img, x, y, w, h, r, col, th=-1):
    x, y, w, h = int(x), int(y), int(w), int(h); r = int(max(0, min(r, w / 2, h / 2)))
    if w <= 0 or h <= 0: return
    if th < 0:
        cv2.rectangle(img, (x + r, y), (x + w - r, y + h), col, -1, cv2.LINE_AA); cv2.rectangle(img, (x, y + r), (x + w, y + h - r), col, -1, cv2.LINE_AA)
        if r > 0:
            for cx, cy in ((x + r, y + r), (x + w - r, y + r), (x + r, y + h - r), (x + w - r, y + h - r)): cv2.circle(img, (cx, cy), r, col, -1, cv2.LINE_AA)
    else:
        cv2.rectangle(img, (x, y), (x + w, y + h), col, int(th), cv2.LINE_AA)
def glow(img, cx, cy, rad, col, strength=1.0):
    rad = int(rad); k = ('g', rad)
    if k not in _tc:
        yy, xx = np.mgrid[-rad:rad + 1, -rad:rad + 1].astype(np.float32)
        _tc[k] = (np.clip(1 - np.sqrt(xx * xx + yy * yy) / rad, 0, 1) ** 2.2)[:, :, None]
    g = _tc[k]; x0, y0 = int(cx - rad), int(cy - rad)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + 2 * rad + 1), min(H, y0 + 2 * rad + 1)
    if xa >= xb or ya >= yb: return
    reg = img[ya:yb, xa:xb].astype(np.float32) + g[ya - y0:yb - y0, xa - x0:xb - x0] * strength * np.array(col, np.float32)
    img[ya:yb, xa:xb] = np.clip(reg, 0, 255).astype(np.uint8)
_g = {}
def grad(top, bot, y0=0, y1=H):
    k = (top, bot, y0, y1)
    if k not in _g:
        g = np.linspace(0, 1, y1 - y0, dtype=np.float32)[:, None, None]
        _g[k] = ((np.array(top, np.float32) * (1 - g) + np.array(bot, np.float32) * g) * np.ones((1, W, 1), np.float32)).astype(np.uint8)
    return _g[k]
def tint(img, col, k):
    if k > 0.003: img[:] = np.clip(img.astype(np.float32) * (1 - k) + np.array(col, np.float32) * k, 0, 255).astype(np.uint8)
def vignette(img, k=0.35):
    key = ('vig', round(k, 2))
    if key not in _tc:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); d = np.sqrt(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
        _tc[key] = (1 - k * np.clip(d, 0, 1.4) ** 2)[:, :, None]
    img[:] = (img * _tc[key]).astype(np.uint8)

rs = random.Random(5)
STARS = [(rs.uniform(0, W), rs.uniform(0, H), rs.uniform(1, 3.6), rs.uniform(0, 6.28)) for _ in range(260)]
def stars(img, t, k=1.0, ymax=H, base=(0, 0, 0)):
    for (x, y, r, ph) in STARS:
        if y > ymax: continue
        a = k * (0.6 + 0.4 * math.sin(t * 3 + ph))
        if a > 0.03: circ(img, (x, y), r, tuple(int(base[i] + (250 - base[i]) * a) for i in range(3)))
RAIN = [(rs.uniform(0, W), rs.uniform(0, H), rs.uniform(900, 1500)) for _ in range(140)]
def rain(img, t, k=1.0, col=(230, 220, 210)):
    for i, (x, y, sp) in enumerate(RAIN):
        if i > len(RAIN) * k: break
        yy = (y + sp * t) % H; xx = (x - 0.25 * sp * t) % W; line(img, (xx, yy), (xx - 14, yy + 56), col, 3)
STREAK = [(rs.uniform(0, W), rs.uniform(250, 1750), rs.uniform(120, 420), rs.uniform(2200, 4200)) for _ in range(46)]
def streaks(img, t, k=1.0, col=WHITE, vertical=False):
    for i, (x, y, ln, sp) in enumerate(STREAK):
        if i > len(STREAK) * k: break
        if vertical:
            yy = (y - sp * t) % (H + 600) - 300; xx = x; line(img, (xx, yy), (xx, yy + ln), col, 5)
        else:
            xx = (x + sp * t) % (W + 600) - 300; line(img, (xx, y), (xx + ln, y), col, 5)

# ---------- UI ----------
def pill(img, cx, cy, txt, size=44, bg=INK, fg=WHITE, dot=None, border=WHITE, alpha=1.0):
    if alpha <= 0.02: return
    w = twidth(txt, size) + size * 1.1 + (size * 0.7 if dot else 0); h = size * 1.45; y = cy + (1 - alpha) * -30
    rrect(img, cx - w / 2, y - h / 2, w, h, h / 2, border); rrect(img, cx - w / 2 + 4, y - h / 2 + 4, w - 8, h - 8, h / 2 - 4, bg)
    if dot: circ(img, (cx - w / 2 + size * 0.75, y), size * 0.24, dot)
    text(img, txt, cx + (size * 0.35 if dot else 0), y + 2, size, fg)
def fact(img, t, txt, at, y=650, size=40):
    """green-dot 'REAL ·' fact badge"""
    pill(img, W / 2, y, 'REAL · ' + txt, size, INK, WHITE, dot=GREEN, alpha=eout(ramp(t, at, at + 0.3)))
def statbox(img, t, label, value, col=YEL, y=330, at=0.1, w=680):
    k = back(ramp(t, at, at + 0.25))
    if k <= 0: return
    rrect(img, W / 2 - w / 2 * k, y, w * k, 250, 28, INK)
    if k > 0.9: text(img, label, W / 2, y + 52, 52); text(img, value, W / 2, y + 160, 140, col, ANT)
def counter(t, a, b, v0, v1): return v0 + (v1 - v0) * ease(ramp(t, a, b))

HEADER = {'title': '', 'info': ''}
def header(img, a=1.0):
    if a <= 0.02: return
    ttl = HEADER['title']; w = twidth(ttl, 54) + 70
    rrect(img, W / 2 - w / 2, 150 - (1 - a) * 200, w, 78, 10, RED); text(img, ttl, W / 2, 191 - (1 - a) * 200, 54)
    w1 = twidth('PART 1', 50) + 55; w2 = twidth(HEADER['info'], 40) + 44 + 28; gap = 24; x0 = W / 2 - (w1 + gap + w2) / 2
    pill(img, x0 + w1 / 2, 280, 'PART 1', 50, CREAM, INK, border=INK, alpha=a); pill(img, x0 + w1 + gap + w2 / 2, 280, HEADER['info'], 40, INK, WHITE, dot=YEL, alpha=a)

def namecard(img, t, name, sub, x=800, y=520, at=0.3):
    a = back(ramp(t, at, at + 0.25))
    if a <= 0: return
    w = max(400, twidth(sub, 34) + 60)
    rrect(img, x - w / 2, y - 60 * a, w * a, 150 * a, 14, INK); rrect(img, x - w / 2 + 8, y + 8 - 60 * a, w * a - 16, 150 * a - 16, 10, CREAM)
    text(img, name, x, y - 2, 92, INK, scale=a); text(img, sub, x, y + 52, 34, RED, scale=a)

def rule_card(img, t, d, l1, l2, bg=None, y=330):
    if bg: bg(img, t)
    else: img[:] = grad((40, 16, 12), (14, 6, 8))
    tint(img, (10, 6, 6), 0.35)
    k = back(ramp(t, 0.05, 0.3)); yy = y - (1 - k) * 500
    rrect(img, 110, yy, 860, 420, 26, INK); rrect(img, 122, yy + 12, 836, 396, 18, CREAM); rrect(img, 110, yy, 860, 22, 10, RED)
    rrect(img, W / 2 - 110, yy + 36, 220, 56, 10, RED); text(img, 'THE RULE', W / 2, yy + 66, 44)
    s1 = 104 if twidth(l1, 104, ANT) < 780 else 80; s2 = 104 if twidth(l2, 104, ANT) < 780 else 80
    text(img, l1, W / 2, yy + 180, s1, INK, ANT); text(img, l2, W / 2, yy + 310, s2, RED, ANT)

def end_card(img, t, d, sub, draw_char=None):
    img[:] = grad((30, 12, 8), (70, 40, 28)); stars(img, t, 0.8, ymax=1200, base=(30, 12, 8)); img[1720:] = (245, 240, 235)
    glow(img, W / 2, 800, 620, (30, 50, 150), 0.9)
    k = back(ramp(t, 0, 0.3))
    text(img, 'PART 2', W / 2, 560, 300, RED, ANT, scale=0.6 + 0.4 * k, stroke=12, scol=INK)
    s = 84 if twidth(sub, 84) < 950 else 64
    text(img, sub, W / 2, 770, s, WHITE, alpha=ramp(t, 0.25, 0.5))
    q = back(ramp(t, 0.4, 0.7)); pul = 1 + 0.04 * math.sin(t * 9)
    if q > 0: rrect(img, W / 2 - 250 * q * pul, 900, 500 * q * pul, 120 * q, 60 * q, WHITE); text(img, 'FOLLOW', W / 2, 962, 84, INK, scale=q * pul)
    if draw_char: draw_char(img, t)

def flash(img, t, at, dur=0.15, col=WHITE, k=0.7): tint(img, col, k * (1 - ramp(t, at, at + dur)) if t >= at else 0)
def shake(t, at, dur=0.35, amp=16): return (random.uniform(-amp, amp), random.uniform(-amp, amp)) if at <= t < at + dur else (0, 0)

def rotated(img, draw, centre, ang, scale=1.0):
    """draw something on a transparent layer, rotate it about centre (degrees, + = counter-clockwise), composite."""
    c = np.zeros_like(img); draw(c)
    R = cv2.getRotationMatrix2D((float(centre[0]), float(centre[1])), ang, scale)
    rc = cv2.warpAffine(c, R, (W, H)); m = rc.any(2)
    img[m] = rc[m]

# ---------- character ----------
class Look:
    def __init__(self, skin=SKINS[0], hair=(38, 52, 86), style='short', shirt=(160, 170, 30), pants=(120, 70, 40), shoes=(40, 40, 60), extra=None):
        self.skin, self.hair, self.style, self.shirt, self.pants, self.shoes, self.extra = skin, hair, style, shirt, pants, shoes, extra
def person(img, L, hx, hy, s=1.0, expr='smile', look=(0, 0), al=15, ar=-15, body=True, blink=False, windy=0.0, legs=True, sweat=False, cheeks=False, wet=False):
    """hx,hy = head centre. arms: al/ar degrees (0 = straight down, +-90 = sideways, 180 = up)."""
    skin = L.skin; hands = []
    if L.style == 'long':
        if windy > 0:
            for i in range(5): line(img, (hx - 60 * s, hy - 60 * s + i * 30 * s), (hx - (190 + 40 * math.sin(i * 2 + windy * 20)) * s, hy - 80 * s + i * 34 * s), L.hair, 34 * s)
        else: rrect(img, hx - 100 * s, hy - 50 * s, 200 * s, 215 * s, 70 * s, L.hair)
    if body:
        if legs:
            for dx in (-38, 38):
                rrect(img, hx + (dx - 28) * s, hy + 270 * s, 56 * s, 140 * s, 16 * s, L.pants)
                rrect(img, hx + (dx - 34) * s, hy + 395 * s, 72 * s, 32 * s, 14 * s, L.shoes)
        for a, sx in ((al, -1), (ar, 1)):
            r = math.radians(a); p0 = (hx + sx * 70 * s, hy + 118 * s); Lr = 135 * s
            p1 = (p0[0] + sx * math.sin(r) * Lr, p0[1] + math.cos(r) * Lr)
            line(img, p0, p1, L.shirt, 46 * s); circ(img, p1, 25 * s, skin); hands.append(p1)
        rrect(img, hx - 88 * s, hy + 78 * s, 176 * s, 215 * s, 46 * s, L.shirt)
        if L.extra == 'tie': poly(img, [(hx - 14 * s, hy + 92 * s), (hx + 14 * s, hy + 92 * s), (hx + 18 * s, hy + 210 * s), (hx, hy + 236 * s), (hx - 18 * s, hy + 210 * s)], RED)
        if L.extra == 'vest': rrect(img, hx - 88 * s, hy + 100 * s, 176 * s, 120 * s, 30 * s, ORANGE); line(img, (hx - 80 * s, hy + 150 * s), (hx + 80 * s, hy + 150 * s), (230, 230, 230), 10 * s)
        if L.extra == 'hoodie': circ(img, (hx, hy + 92 * s), 40 * s, mix(L.shirt, INK, 0.25)); line(img, (hx - 20 * s, hy + 110 * s), (hx - 24 * s, hy + 170 * s), WHITE, 5 * s); line(img, (hx + 20 * s, hy + 110 * s), (hx + 24 * s, hy + 170 * s), WHITE, 5 * s)
        if L.extra == 'backpack':
            line(img, (hx - 50 * s, hy + 90 * s), (hx - 56 * s, hy + 230 * s), (40, 60, 90), 14 * s); line(img, (hx + 50 * s, hy + 90 * s), (hx + 56 * s, hy + 230 * s), (40, 60, 90), 14 * s)
    # head
    if L.style in ('short', 'bun', 'curly'):
        circ(img, (hx, hy - 20 * s), 94 * s, L.hair)
        if L.style == 'short':
            for dx in (-55, -20, 20, 55): circ(img, (hx + dx * s, hy - 92 * s), 32 * s, L.hair)
        if L.style == 'curly':
            for i in range(9): a = math.pi * (1.0 + i / 8); circ(img, (hx + 96 * s * math.cos(a), hy - 20 * s + 96 * s * math.sin(a)), 30 * s, L.hair)
        if L.style == 'bun': circ(img, (hx, hy - 120 * s), 46 * s, L.hair)
    if L.style == 'long': circ(img, (hx, hy - 20 * s), 96 * s, L.hair)
    circ(img, (hx - 88 * s, hy + 8 * s), 17 * s, skin); circ(img, (hx + 88 * s, hy + 8 * s), 17 * s, skin)
    circ(img, (hx, hy), 88 * s, skin)
    if L.style in ('short', 'bun', 'curly', 'long'): ell(img, (hx, hy - 34 * s), 86 * s, 56 * s, L.hair, 180, 360)
    if L.style == 'cap':
        ell(img, (hx, hy - 30 * s), 92 * s, 64 * s, RED, 180, 360); rrect(img, hx - 10 * s, hy - 46 * s, 140 * s, 22 * s, 10 * s, RED)
    ex, ey = look[0] * 8 * s, look[1] * 6 * s; big = expr in ('shock', 'scream')
    for sx in (-1, 1):
        c = (hx + sx * 32 * s + ex, hy - 2 * s + ey)
        if blink or expr == 'closed': line(img, (c[0] - 11 * s, c[1]), (c[0] + 11 * s, c[1]), INK, 6 * s)
        else:
            if big: circ(img, c, 19 * s, WHITE)
            circ(img, c, (10 if not big else 9) * s, INK)
        tilt = {'worry': 9, 'cold': 9, 'scream': 6, 'angry': -10, 'determined': -7}.get(expr, 0) * s
        by = hy - (36 if not big else 46) * s
        line(img, (c[0] - 15 * s, by - sx * tilt), (c[0] + 15 * s, by + sx * tilt), L.hair if L.style != 'cap' else INK, 7 * s)
    my = hy + 42 * s
    if expr == 'smile': ell(img, (hx, my - 10 * s), 26 * s, 20 * s, INK, 20, 160, int(7 * s))
    elif expr in ('flat', 'determined', 'closed'): line(img, (hx - 20 * s, my), (hx + 20 * s, my), INK, 7 * s)
    elif expr == 'shock': ell(img, (hx, my + 4 * s), 15 * s, 21 * s, INK)
    elif expr == 'scream': ell(img, (hx, my + 8 * s), 24 * s, 30 * s, INK); ell(img, (hx, my + 22 * s), 14 * s, 10 * s, (90, 90, 200))
    elif expr == 'cheeks': circ(img, (hx, my), 14 * s, INK); circ(img, (hx - 46 * s, my - 6 * s), 26 * s, mix(skin, (120, 120, 240), 0.4)); circ(img, (hx + 46 * s, my - 6 * s), 26 * s, mix(skin, (120, 120, 240), 0.4))
    elif expr in ('worry', 'cold'):
        pts = [(hx + (i - 4) * 7 * s, my + math.sin(i * 1.5) * 5 * s) for i in range(9)]
        for a, b in zip(pts, pts[1:]): line(img, a, b, INK, 6 * s)
    elif expr == 'angry': ell(img, (hx, my + 8 * s), 22 * s, 12 * s, INK, 200, 340, int(7 * s))
    if sweat:
        for (dx, dy) in ((-96, -40), (98, -20)): circ(img, (hx + dx * s, hy + dy * s), 12 * s, (250, 220, 170))
    if wet:
        for (dx, dy) in ((-60, -70), (40, -90), (70, -40)): circ(img, (hx + dx * s, hy + dy * s), 8 * s, (250, 215, 160))
    return hands

# ---------- emoji (Noto Color Emoji, bitmap at 109 px, scaled) ----------
EMOJI = f'{HERE}/fonts/emoji.ttf'
_ec = {}
def emoji(img, ch, cx, cy, size=80, alpha=1.0, rot=0):
    if alpha <= 0.02 or size < 4: return
    if ch not in _ec:
        f = ImageFont.truetype(EMOJI, 109); im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        bb = im.getbbox() or (0, 0, 1, 1); im = im.crop(bb); a = np.array(im)
        _ec[ch] = (a[:, :, 2::-1].astype(np.float32), a[:, :, 3:4].astype(np.float32) / 255)
    rgb, al = _ec[ch]; sc = size / max(rgb.shape[:2])
    if rot:
        h, w = rgb.shape[:2]; M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, 1.0)
        rgb = cv2.warpAffine(rgb, M, (w, h)); al = cv2.warpAffine(al, M, (w, h))[:, :, None]
    blit(img, rgb, al, cx, cy, alpha, sc)
