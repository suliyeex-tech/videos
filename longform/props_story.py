"""Shared props for 2nd-person story episodes (dark rooms, round-head character, phone + message chips, city, news)."""
from kit16 import *
import cairo, math

# ---------- props ----------
def chat_bubble(c, s, x, y, a, size=34, color="#2b3550", text_color="#ffffff"):
    if a <= 0: return
    setfont(c, "semibold", size); w = c.text_extents(s).x_advance + 50
    c.set_source_rgba(*hexc(color)[:3], 0.95 * a); rrect(c, x - w / 2, y - size - 10, w, size + 34, 22); c.fill()
    c.move_to(x - w / 2 + 40, y + 24); c.line_to(x - w / 2 + 30, y + 46); c.line_to(x - w / 2 + 70, y + 24); c.close_path(); c.fill()
    text(c, s, x, y + 6, size, "semibold", text_color, a)


def dark(c, top="#0b0f1c", bot="#161d33"):
    bg(c, top, bot)

def vignette(c):
    g = cairo.RadialGradient(960, 540, 300, 960, 540, 1150)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.75)
    c.set_source(g); c.paint()

def room(c, t, lamp=0.0, clock="3:12", glow_phone=1.0):
    dark(c)
    c.set_source_rgba(0.13, 0.16, 0.26, 1); c.rectangle(0, 760, W, 320); c.fill()          # floor
    c.set_source_rgba(0.10, 0.13, 0.22, 1); rrect(c, 1320, 240, 360, 300, 10); c.fill()   # window
    for i in range(7):
        c.set_source_rgba(0.16, 0.2, 0.32, 1); c.rectangle(1330, 255 + i * 40, 340, 16); c.fill()
    c.set_source_rgba(0.2, 0.24, 0.4, 1); rrect(c, 300, 620, 760, 170, 26); c.fill()      # bed
    c.set_source_rgba(0.28, 0.33, 0.52, 1); rrect(c, 320, 590, 180, 70, 30); c.fill()     # pillow
    c.set_source_rgba(0.14, 0.12, 0.12, 1); rrect(c, 120, 640, 150, 140, 8); c.fill()     # nightstand
    c.set_source_rgba(0.05, 0.05, 0.06, 1); rrect(c, 140, 600, 110, 50, 8); c.fill()      # clock
    text(c, clock, 195, 638, 34, "bold", "#ff3b3b", 1)
    if glow_phone > 0: glow(c, 470, 600, 220, "#9fc3ff", 0.25 * glow_phone)
    if lamp: c.set_source_rgba(1, 0.85, 0.5, 0.08 * lamp); c.paint()

def person(c, x, y, s=1.0, a=1.0, mood="neutral", phone=False, t=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.3, 0.33, 0.4, a); rrect(c, -45, -150, 90, 150, 30); c.fill()       # body
    c.set_source_rgba(0.85, 0.85, 0.85, a); c.arc(0, -205, 62, 0, 6.2832); c.fill()        # head
    c.set_source_rgba(0.35, 0.22, 0.14, a)                                                   # hair
    c.arc(0, -215, 62, math.pi * 1.05, math.pi * 1.95); c.fill()
    c.set_source_rgba(0.1, 0.1, 0.12, a)
    blink = 1 if (t % 4) > 0.15 else 0.2
    for ex in (-22, 22):
        c.save(); c.translate(ex, -205); c.scale(1, blink); c.arc(0, 0, 7, 0, 6.2832); c.restore(); c.fill()
    c.set_line_width(5)
    if mood == "shock":
        c.arc(0, -168, 12, 0, 6.2832); c.fill()
    elif mood == "smile":
        c.arc(0, -185, 20, 0.2, math.pi - 0.2); c.stroke()
    else:
        c.move_to(-16, -172); c.line_to(16, -172); c.stroke()
    if phone:
        c.set_source_rgba(0.06, 0.06, 0.08, a); rrect(c, 40, -120, 40, 70, 8); c.fill()
        glow(c, 60, -90, 70, "#9fc3ff", 0.4 * a)
    c.restore()

def phone(c, x, y, a=1.0, lines=(), tlist=(), t=0.0, header="Unknown", clock="3:12", typing=False):
    if a <= 0: return
    c.set_source_rgba(0.05, 0.06, 0.09, a); rrect(c, x - 230, y - 400, 460, 800, 60); c.fill()
    c.set_source_rgba(0.25, 0.28, 0.36, a); c.set_line_width(6); rrect(c, x - 230, y - 400, 460, 800, 60); c.stroke()
    c.set_source_rgba(0.12, 0.14, 0.2, a); rrect(c, x - 205, y - 375, 410, 750, 44); c.fill()
    text(c, clock, x - 150, y - 330, 26, "semibold", "#cfd8ff", a)
    c.set_source_rgba(0.4, 0.44, 0.55, a); c.arc(x, y - 270, 34, 0, 6.2832); c.fill()
    text(c, "?", x, y - 257, 40, "bold", "#ffffff", a)
    text(c, header, x, y - 205, 26, "semibold", "#cfd8ff", a)
    for i in range(5):
        c.set_source_rgba(0.24, 0.27, 0.36, a * 0.9); rrect(c, x - 170, y - 160 + i * 90, 300 - (i % 2) * 70, 60, 20); c.fill()
    if typing:
        for i in range(3):
            k = 0.5 + 0.5 * math.sin(t * 6 - i)
            c.set_source_rgba(1, 1, 1, a * (0.3 + 0.7 * k)); c.arc(x - 120 + i * 30, y + 300, 9, 0, 6.2832); c.fill()

def chips(c, items, x, y, t, size=38):
    """items: list of (start_time, text, color)."""
    yy = y
    for st, s, col in items:
        a = ramp(t, st, 0.3)
        if a <= 0: continue
        setfont(c, "semibold", size); w = c.text_extents(s).x_advance + 40
        c.set_source_rgba(0.08, 0.1, 0.16, 0.9 * a); rrect(c, x - 20, yy - size - 8, w, size + 26, 10); c.fill()
        text(c, s, x, yy, size, "semibold", col, a, align="l")
        yy += size + 34

def city(c, t, cars=True, people=True, label=None):
    bg(c, "#2b3a5c", "#9db4d6")
    for i, (x, h) in enumerate([(80, 360), (300, 480), (520, 300), (760, 540), (1000, 380), (1240, 470), (1480, 330), (1700, 420)]):
        c.set_source_rgba(0.18, 0.22, 0.32, 1); c.rectangle(x, 780 - h, 190, h); c.fill()
        for r in range(int(h / 70)):
            for q in range(3):
                c.set_source_rgba(1, 0.86, 0.5, 0.5 if (r + q + i) % 3 else 0.15); c.rectangle(x + 25 + q * 55, 800 - h + r * 70, 30, 34); c.fill()
    c.set_source_rgba(0.2, 0.2, 0.24, 1); c.rectangle(0, 780, W, 300); c.fill()
    c.set_source_rgba(1, 1, 1, 0.6)
    for i in range(0, W, 160): c.rectangle(i + (t * 0 % 160), 920, 90, 10); c.fill()
    if cars:
        for i in range(9):
            x = (i * 230 + t * 40) % (W + 200) - 100
            c.set_source_rgba(*[(0.85, 0.3, 0.3), (0.3, 0.55, 0.9), (0.95, 0.8, 0.3)][i % 3], 1); rrect(c, x, 840, 160, 60, 16); c.fill()
    if label: label_chip(c, label, 960, 150, 1, "#ffd27a", 44)

def news(c, t, headline, sub, a=1.0):
    c.set_source_rgba(0.75, 0.1, 0.12, a); c.rectangle(0, 700, W, 90); c.fill()
    text(c, "BREAKING", 60, 760, 46, "black", "#ffffff", a, align="l")
    c.set_source_rgba(0.05, 0.05, 0.08, 0.92 * a); c.rectangle(0, 790, W, 90); c.fill()
    text(c, headline, 60, 850, 40, "bold", "#ffffff", a, align="l")
    label_chip(c, sub, 960, 150, a, "#ffd27a", 44)

def sc(sc_, i): return sc_["sents"][i][0]

