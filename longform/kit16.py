"""16:9 drawing kit for long-form videos (pycairo). Episodes do `from kit16 import *`."""
#!/usr/bin/env python3
"""Render scenes for 'What if the Moon vanished?'.
usage: render.py scene NAME          -> scenes/NAME.mp4
       render.py frame NAME T OUT    -> PNG still at local time T
"""
import cairo, json, math, os, random, subprocess, sys

W, H, FPS = 1920, 1080, 30
LEAD, TAIL = 0.35, 0.55
GAP = float(os.environ.get("LF_GAP", "0.18"))  # pause between lines; an episode can set GAP = ... (read by lf.py)
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Inter"
FACES = {"bold": "Inter Bold", "semibold": "Inter SemiBold", "medium": "Inter Medium", "black": "Inter Black"}
def setfont(c, weight, size):
    c.select_font_face(FACES.get(weight, "Inter Bold"), cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)

# ---------- timeline ----------
timing = json.load(open(os.environ.get("LF_TIMING", os.path.join(HERE, "timing.json"))))
ORDER = []
for sc, _, _ in timing:
    if sc not in ORDER:
        ORDER.append(sc)

def build_timeline():
    scenes, g = {}, 0.0
    for name in ORDER:
        sents = [(t, d) for s, t, d in timing if s == name]
        local, starts = LEAD, []
        for t, d in sents:
            starts.append((local, d, t))
            local += d + GAP
        dur = local - GAP + TAIL
        dur = math.ceil(dur * FPS) / FPS
        scenes[name] = {"start": g, "dur": dur, "sents": starts}
        g += dur
    return scenes, g

SCENES, TOTAL = build_timeline()

# ---------- helpers ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x):
    x = clamp(x); return x * x * (3 - 2 * x)
def ramp(t, t0, d=0.6): return ease((t - t0) / d)
def lerp(a, b, k): return a + (b - a) * k
def hexc(h, a=1.0):
    h = h.lstrip("#"); return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)

random.seed(7)
STARS = [(random.random() * W, random.random() * H, random.random() * 1.6 + 0.4,
          random.random() * 6.28, random.random() * 0.5 + 0.3) for _ in range(360)]

def bg(c, top="#060914", bot="#101a38"):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc(top)[:3]); g.add_color_stop_rgb(1, *hexc(bot)[:3])
    c.set_source(g); c.paint()

def stars(c, t, alpha=1.0, ymax=H):
    for x, y, r, ph, sp in STARS:
        if y > ymax: continue
        a = alpha * (0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * sp * 2 + ph)))
        c.set_source_rgba(1, 1, 1, a * 0.85)
        c.arc(x, y, r, 0, 6.2832); c.fill()

def text(c, s, x, y, size, weight='bold', color="#ffffff", alpha=1.0, align="c", face=FONT):
    if alpha <= 0.001: return
    setfont(c, weight, size)
    e = c.text_extents(s)
    if align == "c": px = x - e.x_advance / 2
    elif align == "r": px = x - e.x_advance
    else: px = x
    c.move_to(px, y)
    c.set_source_rgba(*hexc(color)[:3], alpha)
    c.show_text(s)
    return e.x_advance

def wrap(c, s, size, maxw, weight='bold'):
    setfont(c, weight, size)
    lines, cur = [], ""
    for w in s.split():
        trial = (cur + " " + w).strip()
        if c.text_extents(trial).x_advance > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = trial
    if cur: lines.append(cur)
    return lines

def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()

SUBS = []  # (spoken, shown) pairs; the episode sets kit16.SUBS
def caption(c, sc, t):
    for st, d, s in sc["sents"]:
        for a_, b_ in globals()["SUBS"]: s = s.replace(a_, b_)
        if st - 0.05 <= t <= st + d + GAP * 0.5:
            a = ramp(t, st - 0.05, 0.15) * (1 - ramp(t, st + d + GAP * 0.5 - 0.12, 0.12))
            size = 40
            lines = wrap(c, s, size, 1500, 'semibold')
            lh = size * 1.3
            bh = lh * len(lines) + 30
            y0 = H - 70 - bh
            c.set_source_rgba(0, 0, 0, 0.55 * a); rrect(c, 960 - 800, y0, 1600, bh, 18); c.fill()
            for i, ln in enumerate(lines):
                text(c, ln, 960, y0 + 15 + size + i * lh - 4, size, 'semibold', "#ffffff", a)
            return

def glow(c, x, y, r, color, a):
    g = cairo.RadialGradient(x, y, r * 0.2, x, y, r)
    g.add_color_stop_rgba(0, *hexc(color)[:3], a); g.add_color_stop_rgba(1, *hexc(color)[:3], 0)
    c.set_source(g); c.arc(x, y, r, 0, 6.2832); c.fill()

random.seed(3)
LAND = [(random.uniform(-1.2, 2.2), random.uniform(-0.8, 0.8), random.uniform(0.15, 0.45), random.uniform(0.1, 0.3)) for _ in range(14)]
def earth(c, x, y, r, t, spin=0.04):
    glow(c, x, y, r * 1.35, "#4aa3ff", 0.35)
    g = cairo.RadialGradient(x - r * 0.35, y - r * 0.35, r * 0.1, x, y, r)
    g.add_color_stop_rgb(0, *hexc("#3d8bff")[:3]); g.add_color_stop_rgb(1, *hexc("#0b2a6b")[:3])
    c.save(); c.arc(x, y, r, 0, 6.2832); c.clip()
    c.set_source(g); c.paint()
    off = (t * spin) % 2.0
    for lx, ly, rw, rh in LAND:
        for k in (0, -2.0):
            cx = x + (lx - off + k) * r
            c.save(); c.translate(cx, y + ly * r); c.scale(rw * r, rh * r)
            c.arc(0, 0, 1, 0, 6.2832); c.restore()
            c.set_source_rgba(0.24, 0.62, 0.36, 0.85); c.fill()
    # night-side shade
    s = cairo.LinearGradient(x - r, y, x + r, y)
    s.add_color_stop_rgba(0, 0, 0, 0, 0); s.add_color_stop_rgba(0.55, 0, 0, 0, 0.05); s.add_color_stop_rgba(1, 0, 0, 0.05, 0.6)
    c.set_source(s); c.paint()
    c.restore()

random.seed(11)
CRATERS = [(random.uniform(-0.6, 0.6), random.uniform(-0.6, 0.6), random.uniform(0.06, 0.2)) for _ in range(9)]
def moon(c, x, y, r, a=1.0, halo=True):
    if a <= 0.001: return
    if halo: glow(c, x, y, r * 2.4, "#cfd8ff", 0.22 * a)
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, 0.96, 0.96, 0.93, a); g.add_color_stop_rgba(1, 0.62, 0.63, 0.66, a)
    c.set_source(g); c.arc(x, y, r, 0, 6.2832); c.fill()
    for cx, cy, cr in CRATERS:
        if cx * cx + cy * cy < 0.55:
            c.set_source_rgba(0.45, 0.46, 0.5, 0.35 * a); c.arc(x + cx * r, y + cy * r, cr * r, 0, 6.2832); c.fill()

def label_chip(c, s, x, y, a, color="#ffd27a", size=34):
    if a <= 0: return
    setfont(c, "bold", size)
    w = c.text_extents(s).x_advance + 44
    c.set_source_rgba(*hexc(color)[:3], 0.16 * a); rrect(c, x - w / 2, y - size - 6, w, size + 30, 14); c.fill()
    c.set_source_rgba(*hexc(color)[:3], 0.9 * a); c.set_line_width(2.5); rrect(c, x - w / 2, y - size - 6, w, size + 30, 14); c.stroke()
    text(c, s, x, y + 6, size, 'bold', color, a)

def S(sc, i): return sc["sents"][i][0]
def SE(sc, i): st, d, _ = sc["sents"][i]; return st + d

# ---------- scenes ----------
