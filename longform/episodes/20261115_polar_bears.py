# Example long-form episode (published 2026-11-15): "What If Polar Bears Vanished? (Remember November 2026)"
# Write new episodes like this one. SCRIPT is spoken in order; consecutive lines with the same scene name form one scene.
SLUG = "2026-11-15-what-if-polar-bears-vanished"
TITLE = "What If Polar Bears Vanished? (Remember November 2026)"
SCRIPT = [
[
"hook",
"If you lost every polar bear tonight, eleven species would lose dinner, and almost nobody knows which one gets hit first."
],
[
"hook",
"Back in twenty twenty three, the internet posted a creepy A I polar bear with a caption that said: this is a November twenty twenty six meme. You won't understand it yet."
],
[
"hook",
"Well. It is November twenty twenty six. And I think I finally understand. The polar bear was trying to tell us something."
],
[
"turn",
"So today, every polar bear on Earth simply vanishes. No drama. No goodbye. They just log off."
],
[
"turn",
"We'll go in order. The first hour. The first year. The weird hybrid plot twist. And finally, the part that isn't hypothetical at all."
],
[
"meet",
"First, let's meet the bear we're about to lose. Because you've been lied to."
],
[
"meet",
"Polar bears are not white. Their fur is transparent and hollow, and the skin underneath is black."
],
[
"meet",
"So a polar bear is basically a black bear wearing a see through puffer jacket. Fashion icon. No notes."
],
[
"meet",
"A polar bear can smell a seal about a kilometre away, even through a metre of snow. You can't smell your own fridge from the sofa."
],
[
"meet",
"One tagged female swam six hundred and eighty seven kilometres without stopping. You can't reply to an email in that time."
],
[
"meet",
"And there are only about twenty six thousand of them left in the whole world. That's fewer people than fit in a mid sized football stadium."
],
[
"buffet",
"Hour one. The Arctic's biggest restaurant closes."
],
[
"buffet",
"Here is the thing nobody tells you. A polar bear is a terrible eater. Gloriously wasteful."
],
[
"buffet",
"It catches a seal, eats mostly the fat and the skin, and walks away from the rest. Like a toddler who only eats the frosting."
],
[
"buffet",
"Scientists estimate an average polar bear kills about a thousand kilograms of marine mammals a year, and roughly thirty percent is left behind."
],
[
"buffet",
"Across the Arctic, that adds up to around seven million kilograms of free food a year. The polar bear isn't just a predator. It's a catering company."
],
[
"buffet",
"At least eleven species eat the leftovers. Arctic foxes. Ravens. Gulls. Even young polar bears."
],
[
"buffet",
"And then there's the ivory gull, which follows polar bears around waiting for them to drop something. Imagine following your coworker all day hoping they drop a sandwich. That is the ivory gull's entire career."
],
[
"buffet",
"So who gets hit first? Probably the ivory gull and the Arctic fox. Their free buffet just vanished, and leftovers matter most exactly when other food is scarce."
],
[
"seals",
"Year one. Meanwhile, on the ice, the ringed seals are having the best day of their lives."
],
[
"seals",
"Ringed seals are the polar bear's main food. In some coastal ice areas, bears can take up to forty four percent of the year's seal pups."
],
[
"seals",
"Now, for the first time in their evolutionary history, ringed seals can nap on the ice without one eye open. Absolute spa weekend."
],
[
"seals",
"But more seals means more mouths eating Arctic fish. Ecologists would expect ripple effects down the food chain. How big? Honestly, nobody can say for sure. The Arctic doesn't come with a manual."
],
[
"hybrid",
"Now, the plot twist. Some polar bears have been dating outside the family."
],
[
"hybrid",
"Grizzly bears have been wandering north, and in the wild, scientists have confirmed eight polar grizzly hybrids."
],
[
"hybrid",
"The name depends on who the dad is. A grolar if dad is a grizzly. A pizzly if dad is a polar bear. Scientists named a bear like it's on a menu."
],
[
"hybrid",
"And here's the funny part. All eight confirmed wild hybrids trace back to the same female polar bear. One mom. Eight descendants. That's not a new species. That's a family group chat."
],
[
"hybrid",
"If the polar bears vanish, that chat goes quiet too. No more pizzlies. The menu loses an item."
],
[
"humans",
"What about us? For Inuit communities across the Arctic, the polar bear, nanuq, is woven into culture, stories and hunting traditions passed down for generations."
],
[
"humans",
"There is even a town in Canada, Churchill, that calls itself the polar bear capital of the world. Without bears, it's just the capital of the world. Which is a lot of pressure for a small town."
],
[
"humans",
"And the internet? It loses its favourite prophet. Every November meme from now on would just be a calendar."
],
[
"real",
"Okay. Here's the part that isn't funny. This isn't entirely hypothetical."
],
[
"real",
"Polar bears need sea ice to hunt seals. When the ice melts in summer, they're stuck on land, fasting, living off their fat."
],
[
"real",
"As the Arctic warms, that fasting season gets longer. In twenty twenty, a study in Nature Climate Change found that if emissions stay high, all but a few high Arctic populations could be in serious trouble by twenty one hundred."
],
[
"real",
"But the same study found that cutting emissions would keep more populations going for longer. So the ending isn't written yet."
],
[
"real",
"Polar bears are officially listed as vulnerable. Not extinct. Not doomed. Vulnerable. Which is exactly the moment when what we do still matters."
],
[
"close",
"So maybe that's what the November polar bear was trying to say all along. Remember the sea ice."
],
[
"close",
"Which Arctic animal would you miss the most? Tell me in the comments. And if a polar bear shows up on your feed this month, now you know what it's trying to tell you."
]
]
SUBS = [("six hundred and eighty seven kilometres", "687 km"), ("twenty twenty three", "2023"), ("twenty twenty six", "2026"), ("twenty twenty", "2020"), ("twenty one hundred", "2100"), ("twenty six thousand", "26,000"), ("forty four percent", "44%"), ("thirty percent", "30%"), ("a thousand kilograms", "1,000 kg"), ("seven million kilograms", "7 million kg"), ("A I ", "AI "), ("eleven species", "11 species"), ("confirmed eight", "confirmed 8"), ("All eight", "All 8"), ("Eight descendants", "8 descendants"), ("see through", "see-through")]

import kit16 as _k; _k.SUBS = SUBS
# Scenes for "What If Polar Bears Vanished?"
from kit16 import *
import kit16
import cairo, math, random

ICE_TOP, ICE_BOT = "#0d1b33", "#2a4a7a"

def sky(c, t, top="#0a1428", bot="#24406e", star_a=0.6):
    bg(c, top, bot); stars(c, t, star_a, 620)

def ice(c, y=760, color="#e8f2ff", shade="#b9d3f0"):
    c.set_source_rgba(*hexc(shade)[:3], 1)
    c.move_to(0, H); c.line_to(0, y + 10)
    for i in range(0, W + 1, 40): c.line_to(i, y + 10 + 8 * math.sin(i / 90))
    c.line_to(W, H); c.close_path(); c.fill()
    c.set_source_rgba(*hexc(color)[:3], 1)
    c.move_to(0, H); c.line_to(0, y)
    for i in range(0, W + 1, 40): c.line_to(i, y + 6 * math.sin(i / 70 + 1))
    c.line_to(W, H); c.close_path(); c.fill()

def ell(c, x, y, rx, ry, col, a=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(rx, ry); c.arc(0, 0, 1, 0, 6.2832); c.restore()
    c.set_source_rgba(*hexc(col)[:3], a); c.fill()

def bear(c, x, y, s=1.0, a=1.0, face=1, t=0.0, fur="#f4f1e8", fur_a=1.0, skin_show=0.0, glasses=False, patches=None):
    """Stylised cartoon polar bear standing on all fours, feet at y."""
    if a <= 0.001: return
    c.save(); c.translate(x, y); c.scale(s * face, s)
    bob = 3 * math.sin(t * 3)
    legs = [(-95, 0), (-55, 0), (55, 0), (90, 0)]
    # black skin silhouette (revealed when fur is see-through)
    def body_shapes(col, al):
        for lx, _ in legs: ell(c, lx, -40, 26, 46, col, al)
        ell(c, 0, -110 + bob, 150, 85, col, al)
        ell(c, 150, -150 + bob, 62, 56, col, al)
        ell(c, 135, -198 + bob, 17, 17, col, al); ell(c, 172, -195 + bob, 15, 15, col, al)
        ell(c, 205, -135 + bob, 34, 24, col, al)
        ell(c, -150, -125 + bob, 18, 16, col, al)
    if skin_show > 0: body_shapes("#111111", a * skin_show)
    body_shapes(fur, a * fur_a)
    if fur_a < 1:  # outline of the "puffer jacket"
        c.set_source_rgba(0.85, 0.95, 1, a * (1 - fur_a) * 0.9); c.set_line_width(4)
        c.save(); c.translate(0, -110 + bob); c.scale(150, 85); c.arc(0, 0, 1, 0, 6.2832); c.restore(); c.stroke()
        c.save(); c.translate(150, -150 + bob); c.scale(62, 56); c.arc(0, 0, 1, 0, 6.2832); c.restore(); c.stroke()
    if patches:
        for px, py, pr in patches: ell(c, px, py + bob, pr, pr * 0.7, "#8a5a32", a * 0.9)
    # face
    ell(c, 135, -198 + bob, 8, 8, "#d9cfc0", a * fur_a)
    ell(c, 228, -140 + bob, 11, 8, "#141414", a)  # nose
    ell(c, 172, -165 + bob, 7, 8, "#141414", a)   # eye
    if glasses:
        c.set_source_rgba(0.05, 0.05, 0.08, a); rrect(c, 150, -178 + bob, 52, 24, 8); c.fill()
    c.set_source_rgba(0.1, 0.1, 0.1, a); c.set_line_width(3)
    c.move_to(205, -122 + bob); c.curve_to(212, -116 + bob, 222, -118 + bob, 228, -126 + bob); c.stroke()
    c.restore()

def seal(c, x, y, s=1.0, a=1.0, t=0.0, glasses=False, face=1):
    if a <= 0.001: return
    c.save(); c.translate(x, y); c.scale(s * face, s)
    ell(c, 0, -32, 95, 34, "#8d97a6", a)
    ell(c, 85, -48, 38, 32, "#9aa4b3", a)
    ell(c, -95, -22, 26, 12, "#7c8696", a, 0.4)
    for sx, sy in ((-30, -45), (10, -38), (-55, -30), (30, -52)):
        ell(c, sx, sy, 6, 4, "#6d7686", a * 0.8)
    ell(c, 102, -55, 6, 7, "#141414", a); ell(c, 120, -44, 6, 4, "#141414", a)
    if glasses:
        c.set_source_rgba(0.05, 0.05, 0.08, a); rrect(c, 84, -66, 46, 20, 7); c.fill()
        c.set_source_rgba(1, 0.3, 0.5, a); c.set_line_width(3); c.move_to(84, -58); c.line_to(60, -62); c.stroke()
    c.restore()

def fox(c, x, y, s=1.0, a=1.0, face=1):
    c.save(); c.translate(x, y); c.scale(s * face, s)
    ell(c, -60, -40, 45, 18, "#f5f7fb", a, -0.4)
    ell(c, 0, -38, 52, 26, "#f5f7fb", a)
    for lx in (-30, -10, 22, 38): ell(c, lx, -12, 7, 16, "#e8edf5", a)
    ell(c, 55, -60, 26, 22, "#f5f7fb", a)
    c.set_source_rgba(0.96, 0.97, 0.98, a)
    c.move_to(42, -76); c.line_to(48, -100); c.line_to(58, -78); c.close_path(); c.fill()
    c.move_to(58, -78); c.line_to(68, -98); c.line_to(72, -74); c.close_path(); c.fill()
    ell(c, 80, -56, 7, 5, "#141414", a); ell(c, 62, -64, 4, 4, "#141414", a)
    c.restore()

def gull(c, x, y, s=1.0, a=1.0, t=0.0, face=1):
    c.save(); c.translate(x, y); c.scale(s * face, s)
    flap = 18 * math.sin(t * 8)
    c.set_source_rgba(0.97, 0.98, 1, a); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(-60, -10 - flap); c.curve_to(-30, -30 - flap, -10, -10, 0, 0); c.curve_to(10, -10, 30, -30 - flap, 60, -10 - flap); c.stroke()
    ell(c, 0, 2, 22, 11, "#fbfcff", a); ell(c, 22, -4, 9, 8, "#fbfcff", a)
    ell(c, 25, -6, 2.5, 2.5, "#141414", a)
    c.set_source_rgba(0.95, 0.75, 0.2, a); c.move_to(30, -4); c.line_to(42, -2); c.line_to(30, 0); c.close_path(); c.fill()
    c.restore()

def raven(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ell(c, 0, -30, 30, 18, "#1c1f2a", a); ell(c, 28, -44, 13, 12, "#1c1f2a", a)
    c.set_source_rgba(0.1, 0.1, 0.13, a); c.move_to(38, -46); c.line_to(54, -42); c.line_to(38, -38); c.close_path(); c.fill()
    c.move_to(-26, -30); c.line_to(-52, -22); c.line_to(-24, -20); c.close_path(); c.fill()
    ell(c, 31, -47, 2.5, 2.5, "#eeeeee", a)
    c.restore()

def chat_bubble(c, s, x, y, a, size=34, color="#2b3550", text_color="#ffffff"):
    if a <= 0: return
    setfont(c, "semibold", size); w = c.text_extents(s).x_advance + 50
    c.set_source_rgba(*hexc(color)[:3], 0.95 * a); rrect(c, x - w / 2, y - size - 10, w, size + 34, 22); c.fill()
    c.move_to(x - w / 2 + 40, y + 24); c.line_to(x - w / 2 + 30, y + 46); c.line_to(x - w / 2 + 70, y + 24); c.close_path(); c.fill()
    text(c, s, x, y + 6, size, "semibold", text_color, a)

def calendar(c, x, y, a, month="NOVEMBER", year="2026", check=0.0):
    if a <= 0: return
    c.set_source_rgba(1, 1, 1, a); rrect(c, x - 170, y - 150, 340, 300, 22); c.fill()
    c.set_source_rgba(0.85, 0.2, 0.25, a); rrect(c, x - 170, y - 150, 340, 90, 22); c.fill(); c.rectangle(x - 170, y - 90, 340, 30); c.fill()
    text(c, month, x, y - 95, 40, "black", "#ffffff", a)
    text(c, year, x, y + 70, 110, "black", "#1a1a2a", a)
    if check > 0:
        c.set_source_rgba(0.2, 0.75, 0.35, a * check); c.set_line_width(22); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(x + 90, y + 40); c.line_to(x + 140, y + 95); c.line_to(x + 240, y - 40); c.stroke()

def counter(c, value, x, y, size, color="#ffd27a", a=1.0, suffix=""):
    text(c, f"{int(value):,}{suffix}", x, y, size, "black", color, a)

# ---------------- scenes ----------------
def sc_hook(c, t, sc):
    sky(c, t); ice(c)
    s1 = S(sc, 1); s2 = S(sc, 2)
    meme = ramp(t, s1, 0.5)
    bx = lerp(760, 520, meme)
    bear(c, bx, 800, 1.25, 1.0, 1, t)
    text(c, "WHAT IF POLAR BEARS", 960, 130, 84, "black", "#ffffff", ramp(t, 0.2, 0.5))
    text(c, "VANISHED?", 960, 230, 92, "black", "#7fd4ff", ramp(t, 0.45, 0.5))
    label_chip(c, "11 species lose dinner", 1450, 420, ramp(t, 3.0, 0.4) * (1 - meme), "#ffd27a", 40)
    if meme > 0:
        c.set_source_rgba(0, 0, 0, 0.55 * meme); c.paint()
        calendar(c, 1260, 520, meme, check=ramp(t, s2 + 1.2, 0.5))
        bear(c, 560, 800, 1.1, meme, 1, t * 0.3, glasses=False)
        chat_bubble(c, "this is a November 2026 meme", 640, 360, ramp(t, s1 + 2.0, 0.4) * (1 - ramp(t, s2, 0.3)))
        chat_bubble(c, "you won't understand it yet", 640, 450, ramp(t, s1 + 4.0, 0.4) * (1 - ramp(t, s2, 0.3)))
        chat_bubble(c, "...it's November 2026", 640, 400, ramp(t, s2 + 0.5, 0.4), color="#3a2b55")
        text(c, "a 2023 AI meme, revisited", 1260, 760, 30, "medium", "#cfd8ff", meme * 0.9)

def sc_turn(c, t, sc):
    sky(c, t); ice(c)
    gone = ramp(t, 2.8, 0.8)
    bear(c, 760, 800, 1.2, 1 - gone, 1, t)
    if t > 2.8:
        k = clamp((t - 2.8) / 0.9)
        for i in range(30):
            ang = i * 2.4; r = 40 + 400 * k
            c.set_source_rgba(1, 1, 1, 0.8 * (1 - k)); c.arc(960 + r * math.cos(ang), 600 + 0.5 * r * math.sin(ang), 6, 0, 6.2832); c.fill()
    label_chip(c, "polar_bear has left the chat", 960, 300, ramp(t, 3.4, 0.4) * (1 - ramp(t, S(sc, 1) - 0.2, 0.3)), "#9fb4ff", 40)
    st, d, _ = sc["sents"][1]
    items = ["1  HOUR ONE", "2  YEAR ONE", "3  PLOT TWIST", "4  NOT HYPOTHETICAL"]
    for i, it in enumerate(items):
        a = ramp(t, st + 0.6 + i * (d - 1) / 4, 0.4)
        label_chip(c, it, 960, 230 + i * 120, a, ["#7fd4ff", "#9dff8a", "#ffb6c1", "#ffd27a"][i], 44)

def sc_meet(c, t, sc):
    sky(c, t, "#0b1730", "#1d3560", 0.4); ice(c, 820)
    S1, S2, S3, S4, S5 = (S(sc, i) for i in range(1, 6))
    text(c, "MEET THE BEAR", 960, 120, 60, "black", "#ffffff", ramp(t, 0.1) * (1 - ramp(t, S1, 0.3)))
    # fur reveal
    see = ramp(t, S1 + 1.2, 1.0) * (1 - ramp(t, S3 - 0.3, 0.4))
    show_bear = 1 - ramp(t, S3 - 0.3, 0.4)
    if show_bear > 0:
        bear(c, 820, 860, 1.6, show_bear, 1, t, fur="#f4f1e8", fur_a=1 - 0.8 * see, skin_show=see)
        label_chip(c, "fur: transparent + hollow", 1450, 300, ramp(t, S1 + 1.5) * show_bear, "#7fd4ff", 34)
        label_chip(c, "skin: black", 1450, 400, ramp(t, S1 + 3.2) * show_bear, "#ffffff", 34)
        label_chip(c, "see-through puffer jacket", 1450, 520, ramp(t, S2 + 0.3) * show_bear, "#ffd27a", 34)
    # smell
    sm = ramp(t, S3 - 0.1, 0.4) * (1 - ramp(t, S4 - 0.3, 0.3))
    if sm > 0:
        bear(c, 420, 860, 0.9, sm, 1, t)
        p = clamp((t - S3) / 2.0)
        c.set_source_rgba(1, 0.85, 0.5, sm); c.set_line_width(5); c.set_dash([14, 14], -t * 60)
        c.move_to(650, 700); c.line_to(650 + 950 * p, 700); c.stroke(); c.set_dash([])
        c.set_source_rgba(0.85, 0.92, 1, sm); c.rectangle(1460, 640, 300, 80); c.fill()
        seal(c, 1600, 830, 0.8, sm * ramp(t, S3 + 1.8, 0.3), t)
        text(c, "~1 km", 1100, 660, 64, "black", "#ffd27a", sm)
        text(c, "through ~1 m of snow", 1610, 620, 30, "semibold", "#ffffff", sm * ramp(t, S3 + 2.2, 0.3))
    # swim
    sw = ramp(t, S4 - 0.1, 0.4) * (1 - ramp(t, S5 - 0.3, 0.3))
    if sw > 0:
        g = cairo.LinearGradient(0, 300, 0, H); g.add_color_stop_rgba(0, 0.05, 0.25, 0.5, sw); g.add_color_stop_rgba(1, 0.02, 0.1, 0.25, sw)
        c.set_source(g); c.rectangle(0, 300, W, H); c.fill()
        p = clamp((t - S4) / 4.5)
        c.set_source_rgba(1, 1, 1, 0.6 * sw); c.set_line_width(4); c.set_dash([10, 12])
        c.move_to(200, 600); c.curve_to(700, 450, 1100, 750, 1720, 560); c.stroke(); c.set_dash([])
        hx = lerp(200, 1720, p); hy = 600 + math.sin(p * 3.1) * -40
        ell(c, hx, hy, 40, 30, "#f4f1e8", sw); ell(c, hx + 30, hy - 10, 6, 6, "#141414", sw)
        text(c, "687 km", 960, 230, 120, "black", "#ffd27a", sw)
        text(c, "without stopping", 960, 300, 40, "semibold", "#ffffff", sw)
        chat_bubble(c, "Re: your email from 9 days ago", 1300, 420, ramp(t, S4 + 3.5, 0.4) * sw, color="#3a2b55")
    # count
    ct = ramp(t, S5 - 0.1, 0.4)
    if ct > 0:
        c.set_source_rgba(0.03, 0.05, 0.1, 0.85 * ct); c.paint()
        v = 26000 * ease(clamp((t - S5) / 1.8))
        counter(c, v, 960, 470, 200, "#ffd27a", ct)
        text(c, "polar bears left (estimate: 22,000 to 31,000)", 960, 560, 36, "semibold", "#ffffff", ct)
        label_chip(c, "< one mid-sized football stadium", 960, 700, ramp(t, S5 + 3.5, 0.4), "#7fd4ff", 36)

def sc_buffet(c, t, sc):
    sky(c, t, "#0a1730", "#1f3b66", 0.5); ice(c, 780)
    S = [s[0] for s in sc["sents"]]
    # restaurant sign
    closed = ramp(t, 1.0, 0.3)
    sign = 1 - ramp(t, S[2] - 0.2, 0.3)
    if sign > 0:
        c.set_source_rgba(0.12, 0.08, 0.05, sign); rrect(c, 610, 200, 700, 300, 26); c.fill()
        text(c, "ARCTIC BUFFET", 960, 300, 64, "black", "#ffd27a", sign)
        text(c, "OPEN" if closed < 0.5 else "CLOSED", 960, 440, 110, "black", "#7dffb0" if closed < 0.5 else "#ff6b6b", sign)
    # bear eats seal, leaves leftovers
    eat = ramp(t, S[2], 0.4) * (1 - ramp(t, S[4] - 0.3, 0.3))
    if eat > 0:
        bear(c, 700, 860, 1.2, eat, 1, t)
        seal(c, 1250, 860, 1.1, eat * (1 - 0.5 * ramp(t, S[3] - 1.5, 1.0)), t, face=-1)
        label_chip(c, "eats: fat + skin", 960, 220, ramp(t, S[3] - 2.5, 0.3) * eat, "#ffd27a", 36)
        label_chip(c, "leaves: the rest", 960, 320, ramp(t, S[3] - 1.2, 0.3) * eat, "#ffb6c1", 36)
        chat_bubble(c, "only eats the frosting", 1350, 560, ramp(t, S[3] - 0.6, 0.3) * eat * (1 - ramp(t, S[3], 0.2)))
    # numbers
    nb = ramp(t, S[3], 0.4) * (1 - ramp(t, S[5] - 0.3, 0.3))
    if nb > 0:
        c.set_source_rgba(0.03, 0.05, 0.1, 0.97 * nb); c.paint()
        text(c, "per bear, per year", 960, 200, 40, "semibold", "#9fb4ff", nb)
        counter(c, 1000 * ease(clamp((t - S[3]) / 1.5)), 620, 400, 130, "#ffffff", nb, " kg")
        text(c, "killed", 620, 470, 36, "semibold", "#cfd8ff", nb)
        a2 = ramp(t, S[3] + 4.0, 0.4) * nb
        text(c, "~30%", 1320, 400, 130, "black", "#ffd27a", a2)
        text(c, "left behind", 1320, 470, 36, "semibold", "#ffd27a", a2)
        a3 = ramp(t, S[4], 0.4) * nb
        text(c, "≈ 7,000,000 kg of free food / year", 960, 660, 60, "black", "#7dffb0", a3)
        label_chip(c, "polar bear = Arctic catering company", 960, 800, ramp(t, S[4] + 4.5, 0.4) * nb, "#ffd27a", 36)
    # scavengers
    sv = ramp(t, S[5], 0.4) * (1 - ramp(t, S[6] - 0.3, 0.3))
    if sv > 0:
        text(c, "11+ species eat the leftovers", 960, 180, 60, "black", "#ffffff", sv)
        fox(c, 420, 760, 1.5, sv * ramp(t, S[5] + 1.6, 0.3))
        raven(c, 830, 740, 2.0, sv * ramp(t, S[5] + 2.4, 0.3))
        gull(c, 1180, 600, 1.6, sv * ramp(t, S[5] + 3.0, 0.3), t)
        bear(c, 1560, 800, 0.6, sv * ramp(t, S[5] + 3.6, 0.3), -1, t)
        for x, lab, k in ((420, "arctic fox", 1.6), (830, "raven", 2.4), (1180, "gull", 3.0), (1560, "young bears", 3.6)):
            text(c, lab, x, 860, 34, "semibold", "#10203a", sv * ramp(t, S[5] + k, 0.3))
    # ivory gull follows bear
    ig = ramp(t, S[6], 0.4) * (1 - ramp(t, S[7] - 0.3, 0.3))
    if ig > 0:
        walk = (t - S[6]) * 120
        bx = 300 + walk % 1500
        bear(c, bx, 840, 0.9, ig, 1, t * 2)
        gull(c, bx - 260, 560 + 20 * math.sin(t * 2), 1.2, ig, t)
        text(c, "ivory gull", bx - 260, 640, 30, "semibold", "#ffffff", ig)
        chat_bubble(c, "drop the sandwich. drop the sandwich.", 960, 260, ramp(t, S[6] + 3.5, 0.3) * ig, color="#3a2b55")
    # who gets hit first
    hf = ramp(t, S[7], 0.4)
    if hf > 0:
        c.set_source_rgba(0.03, 0.05, 0.1, 0.8 * hf); c.paint()
        text(c, "WHO GETS HIT FIRST?", 960, 200, 64, "black", "#ffffff", hf)
        gull(c, 700, 520, 2.2, hf, t); fox(c, 1250, 640, 2.0, hf)
        text(c, "ivory gull", 700, 720, 40, "bold", "#ffd27a", hf); text(c, "arctic fox", 1250, 720, 40, "bold", "#ffd27a", hf)
        text(c, "(probably)", 960, 800, 34, "medium", "#9fb4ff", ramp(t, S[7] + 1.5, 0.3))

def sc_seals(c, t, sc):
    sky(c, t, "#0f2140", "#3b6aa0", 0.3); ice(c, 700)
    S = [s[0] for s in sc["sents"]]
    text(c, "YEAR ONE", 960, 130, 64, "black", "#ffffff", ramp(t, 0.1) * (1 - ramp(t, S[1], 0.3)))
    for i, (x, sc_) in enumerate(((500, 1.0), (980, 1.2), (1420, 0.9))):
        seal(c, x, 780, sc_, 1.0, t, glasses=t > S[2] + 0.6, face=1 if i % 2 else -1)
    pct = ramp(t, S[1], 0.4) * (1 - ramp(t, S[2] - 0.2, 0.3))
    if pct > 0:
        text(c, "up to 44%", 960, 330, 140, "black", "#ffd27a", pct)
        text(c, "of a year's seal pups taken by bears", 960, 400, 38, "semibold", "#ffffff", pct)
        text(c, "(in some coastal ice areas)", 960, 450, 30, "medium", "#cfd8ff", pct)
    spa = ramp(t, S[2], 0.4) * (1 - ramp(t, S[3] - 0.2, 0.3))
    if spa > 0:
        c.set_source_rgba(0.95, 0.5, 0.65, spa); rrect(c, 760, 220, 400, 140, 26); c.fill()
        text(c, "SEAL SPA", 960, 310, 70, "black", "#ffffff", spa)
        text(c, "now open • no bears", 960, 420, 34, "semibold", "#ffffff", spa)
    rp = ramp(t, S[3], 0.4)
    if rp > 0:
        xs = [300, 760, 1200, 1600]
        labs = ["more seals", "more fish eaten", "?", "?"]
        for i, (x, l) in enumerate(zip(xs, labs)):
            a = ramp(t, S[3] + 0.5 + i * 1.0, 0.3)
            label_chip(c, l, x, 300, a, ["#cfd8ff", "#7fd4ff", "#ffd27a", "#ffd27a"][i], 36)
            if i:
                c.set_source_rgba(1, 1, 1, a * 0.8); c.set_line_width(4)
                mx = (xs[i - 1] + x) / 2 + (35 if i == 1 else 0)
                c.move_to(mx - 25, 285); c.line_to(mx + 25, 285); c.line_to(mx + 12, 275); c.move_to(mx + 25, 285); c.line_to(mx + 12, 295); c.stroke()
        label_chip(c, "the Arctic doesn't come with a manual", 960, 470, ramp(t, S[3] + 6.0, 0.4), "#ff8a8a", 34)

def sc_hybrid(c, t, sc):
    sky(c, t, "#1a1430", "#3a2b55", 0.4); ice(c, 800, "#f0ecf7", "#cfc7e0")
    S = [s[0] for s in sc["sents"]]
    text(c, "PLOT TWIST", 960, 130, 70, "black", "#ffb6c1", ramp(t, 0.1))
    a1 = ramp(t, S[1], 0.4) * (1 - ramp(t, S[2] - 0.2, 0.3))
    if a1 > 0 or t < S[1]:
        a0 = max(a1, 1 - ramp(t, S[1] - 0.2, 0.2)) if t < S[2] else a1
        bear(c, 520, 860, 0.9, a0, 1, t)
        bear(c, 1400, 860, 0.9, a0, -1, t, fur="#7a4a26")
        text(c, "♥", 960, 600, 120, "black", "#ff6b8a", a0 * (0.6 + 0.4 * math.sin(t * 5)))
        label_chip(c, "8 confirmed wild hybrids", 960, 330, a1, "#ffd27a", 40)
    menu = ramp(t, S[2], 0.4) * (1 - ramp(t, S[3] - 0.2, 0.3))
    if menu > 0:
        c.set_source_rgba(0.98, 0.95, 0.88, menu); rrect(c, 560, 230, 800, 520, 24); c.fill()
        text(c, "~ MENU ~", 960, 320, 54, "black", "#5a3a1a", menu)
        text(c, "GROLAR ............ grizzly dad", 960, 450, 44, "bold", "#3a2a1a", ramp(t, S[2] + 1.0, 0.3) * menu)
        text(c, "PIZZLY ............. polar dad", 960, 560, 44, "bold", "#3a2a1a", ramp(t, S[2] + 2.5, 0.3) * menu)
        text(c, "(chef's special)", 960, 660, 32, "medium", "#8a6a4a", ramp(t, S[2] + 4.0, 0.3) * menu)
    fam = ramp(t, S[3], 0.4) * (1 - ramp(t, S[4] - 0.2, 0.3))
    if fam > 0:
        bear(c, 960, 470, 0.7, fam, 1, t)
        text(c, "one polar bear mom", 960, 520, 34, "semibold", "#ffffff", fam)
        for i in range(8):
            a = ramp(t, S[3] + 2.5 + i * 0.25, 0.25) * fam
            x = 330 + i * 180
            c.set_source_rgba(1, 1, 1, a * 0.5); c.set_line_width(2); c.move_to(960, 540); c.line_to(x, 680); c.stroke()
            bear(c, x - 40, 790, 0.38, a, 1, t + i, fur=["#d9c3a5", "#c9a882", "#e2d3bb", "#b8936a"][i % 4])
        chat_bubble(c, "Family Group Chat (8 members)", 1350, 300, ramp(t, S[3] + 6.0, 0.4) * fam, color="#2b5a3a")
    q = ramp(t, S[4], 0.4)
    if q > 0:
        chat_bubble(c, "Family Group Chat (0 members)", 960, 420, q, color="#3a3a46")
        label_chip(c, "the menu loses an item", 960, 640, ramp(t, S[4] + 2.5, 0.4), "#ff8a8a", 38)

def sc_humans(c, t, sc):
    sky(c, t, "#0b1730", "#26406a", 0.6); ice(c, 800)
    S = [s[0] for s in sc["sents"]]
    a0 = 1 - ramp(t, S[1] - 0.2, 0.3)
    if a0 > 0:
        text(c, "nanuq", 960, 420, 160, "black", "#ffffff", a0 * ramp(t, 1.5, 0.6))
        text(c, "the polar bear, in Inuktitut", 960, 500, 38, "semibold", "#9fb4ff", a0 * ramp(t, 2.3, 0.4))
        text(c, "culture • stories • hunting traditions", 960, 600, 36, "semibold", "#cfd8ff", a0 * ramp(t, 4.0, 0.4))
    a1 = ramp(t, S[1], 0.4) * (1 - ramp(t, S[2] - 0.2, 0.3))
    if a1 > 0:
        c.set_source_rgba(0.5, 0.35, 0.2, a1); c.rectangle(950, 520, 22, 290); c.fill()
        c.set_source_rgba(0.1, 0.45, 0.25, a1); rrect(c, 560, 260, 800, 260, 20); c.fill()
        c.set_source_rgba(1, 1, 1, a1); c.set_line_width(5); rrect(c, 575, 275, 770, 230, 14); c.stroke()
        text(c, "CHURCHILL", 960, 360, 70, "black", "#ffffff", a1)
        cross = ramp(t, S[1] + 5.0, 0.4)
        text(c, "POLAR BEAR CAPITAL OF THE WORLD", 960, 450, 38, "bold", "#ffffff", a1)
        if cross > 0:
            c.set_source_rgba(1, 0.3, 0.3, a1 * cross); c.set_line_width(8)
            c.move_to(620, 438); c.line_to(620 + 260 * cross, 438); c.stroke()
        chat_bubble(c, "...no pressure", 1450, 640, ramp(t, S[1] + 7.5, 0.4) * a1, color="#3a2b55")
    a2 = ramp(t, S[2], 0.4)
    if a2 > 0:
        calendar(c, 960, 480, a2)
        label_chip(c, "the internet loses its favourite prophet", 960, 760, ramp(t, S[2] + 0.6, 0.4), "#ffd27a", 36)

def sc_real(c, t, sc):
    S = [s[0] for s in sc["sents"]]
    bg(c, "#061020", "#0d2240"); stars(c, t, 0.4)
    text(c, "THE PART THAT ISN'T HYPOTHETICAL", 960, 120, 54, "black", "#ffffff", ramp(t, 0.3))
    # sea-ice disc shrinking
    cx, cy = 620, 540
    shrink = ramp(t, S[2], 4.0)
    c.set_source_rgba(0.08, 0.2, 0.4, 1); c.arc(cx, cy, 300, 0, 6.2832); c.fill()
    r = lerp(250, 150, shrink) + 8 * math.sin(t)
    c.set_source_rgba(0.92, 0.96, 1, 0.95); c.move_to(cx + r, cy)
    for i in range(1, 61):
        a = i / 60 * 6.2832; rr = r * (1 + 0.08 * math.sin(a * 5 + 1) + 0.05 * math.sin(a * 9))
        c.line_to(cx + rr * math.cos(a), cy + rr * math.sin(a))
    c.close_path(); c.fill()
    text(c, "summer sea ice", cx, cy + 360, 32, "semibold", "#9fb4ff", ramp(t, S[1], 0.4))
    bear(c, cx - 60, cy + 60, 0.45, ramp(t, S[1], 0.4), 1, t)
    # right panel
    px = 1380
    a1 = ramp(t, S[1] + 2.5, 0.4) * (1 - ramp(t, S[2] - 0.2, 0.3))
    label_chip(c, "no ice = no seal hunting", px, 360, a1, "#7fd4ff", 34)
    label_chip(c, "stuck on land, fasting", px, 470, ramp(t, S[1] + 4.5, 0.4) * (1 - ramp(t, S[2] - 0.2, 0.3)), "#ffd27a", 34)
    a2 = ramp(t, S[2], 0.4) * (1 - ramp(t, S[3] - 0.2, 0.3))
    if a2 > 0:
        text(c, "FASTING SEASON", px, 300, 40, "bold", "#9fb4ff", a2)
        bw = lerp(200, 520, ramp(t, S[2] + 1.0, 4.0))
        c.set_source_rgba(1, 0.55, 0.4, a2); rrect(c, px - 260, 340, bw, 60, 12); c.fill()
        text(c, "Nature Climate Change, 2020", px, 470, 32, "semibold", "#ffffff", ramp(t, S[2] + 4.0, 0.4) * a2)
        text(c, "high emissions: most populations", px, 540, 32, "semibold", "#ff8a8a", ramp(t, S[2] + 6.0, 0.4) * a2)
        text(c, "in serious trouble by 2100", px, 585, 32, "semibold", "#ff8a8a", ramp(t, S[2] + 6.0, 0.4) * a2)
    a3 = ramp(t, S[3], 0.4) * (1 - ramp(t, S[4] - 0.2, 0.3))
    if a3 > 0:
        label_chip(c, "cut emissions → more populations last", px, 420, a3, "#7dffb0", 32)
        text(c, "the ending isn't written yet", px, 540, 36, "bold", "#ffffff", ramp(t, S[3] + 3.0, 0.4) * a3)
    a4 = ramp(t, S[4], 0.4)
    if a4 > 0:
        c.set_source_rgba(1, 0.75, 0.2, 0.15 * a4); rrect(c, px - 250, 320, 500, 200, 20); c.fill()
        c.set_source_rgba(1, 0.75, 0.2, a4); c.set_line_width(4); rrect(c, px - 250, 320, 500, 200, 20); c.stroke()
        text(c, "IUCN STATUS", px, 390, 36, "bold", "#ffd27a", a4)
        text(c, "VULNERABLE", px, 470, 64, "black", "#ffffff", a4)
        text(c, "not extinct • not doomed", px, 590, 32, "semibold", "#cfd8ff", ramp(t, S[4] + 2.5, 0.4))

def sc_close(c, t, sc):
    sky(c, t); ice(c)
    bear(c, 700, 860, 1.1, 1.0, 1, t)
    text(c, "REMEMBER", 1300, 380, 96, "black", "#ffffff", ramp(t, 1.0, 0.4))
    text(c, "THE SEA ICE", 1300, 490, 96, "black", "#7fd4ff", ramp(t, 1.6, 0.4))
    a = ramp(t, S(sc, 1), 0.4)
    text(c, "Which Arctic animal would you miss most?", 960, 160, 52, "bold", "#ffffff", a)
    text(c, "↓  comments  ↓", 960, 230, 38, "semibold", "#ffd27a", ramp(t, S(sc, 1) + 1.0, 0.4))
    text(c, "WHAT IF IT VANISHED?", 1300, 600, 36, "bold", "#9fb4ff", ramp(t, 2.4, 0.4))

DRAW = {"hook": sc_hook, "turn": sc_turn, "meet": sc_meet, "buffet": sc_buffet, "seals": sc_seals,
        "hybrid": sc_hybrid, "humans": sc_humans, "real": sc_real, "close": sc_close}


def THUMB(c):
    """Draw the 1920x1080 thumbnail (lf.py scales it to 1280x720)."""
    sky(c, 1.0, "#08142a", "#2a4f86", 0.9); ice(c, 820)
    bear(c, 1640, 960, 1.3, 1.0, -1, 0.0)
    calendar(c, 1580, 300, 1.0)
    text(c, "WHAT IF", 100, 330, 150, "black", "#ffffff", align="l")
    text(c, "POLAR BEARS", 100, 500, 150, "black", "#7fd4ff", align="l")
    text(c, "VANISHED?", 100, 670, 150, "black", "#ffd27a", align="l")
