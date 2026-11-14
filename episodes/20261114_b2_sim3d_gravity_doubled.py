import math, random
from kit import *
from sim3d import *

FORMAT = 'sim3d'
SLUG = '2026-11-14-gravity-doubled-5-seconds'
VOICE = 'hype'; SPEED = 1.25; CAPTION = 'serif'; TICKS = True; ZOOM = 0.6; VIGNETTE = 0.25
MOOD = {'style': 'cinematic', 'root': 55.0, 'bpm': 84}
LINES = [
 ("What if gravity doubled for five seconds?", 0.25),
 ("You're in Times Square at noon. Thousands of people, hundreds of cars.", 0.3),
 ("Gravity is nine point eight. And then... nineteen point six.", 0.35),
 ("Instantly, you feel twice as heavy. Like someone just jumped on your back.", 0.3),
 ("Knees buckle. Half the crowd sits down. Hard.", 0.35),
 ("Every bathroom scale on Earth now reads double.", 0.3),
 ("Drop your phone, and it hits the ground in under four tenths of a second, instead of more than half a second.", 0.3),
 ("Your heart is pumping blood that suddenly weighs double. But two g is roller coaster level. You stay awake.", 0.3),
 ("Above you, every airliner feels two g. Good news: they're built to take two and a half.", 0.3),
 ("Pigeons drop like stones, then flap like crazy.", 0.3),
 ("The fountains only shoot half as high.", 0.3),
 ("Four hundred kilometers up, the space station gets pulled about a hundred meters lower.", 0.3),
 ("Even the Moon falls three centimeters closer to us.", 0.35),
 ("Three... two... one.", 0.35),
 ("Gravity snaps back. And everyone who was pushing to stay standing... launches into a tiny jump.", 0.3),
 ("Thousands of people in Times Square hop at the exact same moment.", 0.35),
 ("And the space station is now on a slightly wonky orbit. Mission control has questions.", 0.35),
 ("What would you do with five heavy seconds? Comment below.", 1.0),
]
CAPS = [[], ["You're in Times Square at noon.", "[Thousands] of people."], ["9.8 ... then [19.6.]"],
        ["You feel [twice as heavy.]"], ["Knees buckle. [Half the crowd] sits down."], ["Every scale reads [double.]"],
        ["Your phone hits the ground in [0.39 s]", "instead of 0.55 s."], ["Blood weighs double.", "But 2 g = [roller coaster.] You stay awake."],
        ["Airliners feel 2 g.", "They're built for [2.5 g.]"], ["Pigeons drop like stones."], ["Fountains shoot [half as high.]"],
        ["The space station drops [~100 m.]"], ["The Moon falls [3 cm] closer."], ["Three... two... one."],
        ["Gravity snaps back.", "Everyone [launches] into a tiny jump."], ["[Thousands] hop at the same moment."],
        ["The station's orbit is now [wonky.]"], []]

C_HIGH = Cam((60, 230, 40), -25, -55, 62); C_WIDE = Cam((0, 140, -260), 0, -24, 62); C_LOW = Cam((-30, 12, -40), 18, -4, 66)
C_UP = Cam((0, 8, -60), 0, 28, 72)
SKY = ((200, 150, 90), (240, 210, 170)); FOG = (235, 215, 190)
G = {'t0': 9e9, 't1': 9e9}

def crowd(polys, n, x0, x1, z0, z1, seed=5, squash=0.0, lift=0.0, t=0.0):
    rb = random.Random(seed)
    for i in range(n):
        x = rb.uniform(x0, x1); z = rb.uniform(z0, z1); c = rb.choice(CLOTHES); sp = rb.uniform(-6, 6)
        x += sp * t * (1 - squash); sq = squash * (1.0 if i % 2 == 0 else 0.35); y = lift * rb.uniform(0.6, 1.4)
        h = 3.2 * (1 - 0.5 * sq)
        box(polys, x, y, z, 1.6 + 0.5 * sq, h, 1.0, c); box(polys, x, y + h, z, 1.1, 1.1, 1.1, (120, 160, 210))
def world(img, t, cam, squash=0.0, lift=0.0, cars_stop=0.0, extra=None):
    p = []; city_scene(p, t, {'crowd': 0, 'cars_stop': cars_stop})
    crowd(p, 110, -55, 55, -100, 260, squash=squash, lift=lift, t=t)
    if extra: extra(p)
    render(img, cam, p, sky=SKY, fog=FOG, t=t)
def gtag(img, val, a=1.0, sub='Times Square, New York'):
    hud(img, 'Gravity', val, sub, a=a, x=110, y=1530)

def s1(img, t, d):
    world(img, t, lerp_cam(C_HIGH, C_WIDE, t / d))
    title(img, 'What if gravity', 'doubled for 5 seconds?', a=ramp(t, 0.05, 0.4), y=560)
def s2(img, t, d):
    world(img, t, lerp_cam(C_WIDE, C_LOW, t / d)); gtag(img, '9.8 m/s²', ramp(t, 0.1, 0.4))
def s3(img, t, d):
    k = ramp(t, 1.4, 1.6); jx, jy = shake(t, 1.45, 0.5, 18)
    world(img, t, Cam((-30 + jx * 0.1, 12 + jy * 0.1, -40), 18, -4, 66), squash=0.4 * k)
    if t > 1.45: flash(img, t, 1.45, 0.25, WHITE, 0.8)
    gtag(img, f'{9.8 + 9.8 * k:.1f} m/s²')
    if t > 1.5: text(img, '2 G', W / 2, 640, 220, (60, 60, 255), SERIF_I, scale=back(ramp(t, 1.5, 1.8)), stroke=3, scol=(30, 20, 20))
def s4(img, t, d):
    world(img, t, lerp_cam(C_LOW, Cam((-10, 9, -20), 10, -8, 70), t / d), squash=0.5)
    hud(img, 'You feel like', f'{int(counter(t, 0.2, 1.6, 70, 140))} kg', 'normally 70 kg', x=110, y=1530)
def s5(img, t, d):
    jx, jy = shake(t, 0.2, 0.4, 14)
    world(img, t, lerp_cam(C_LOW, C_WIDE, t / d * 0.6), squash=0.6 + 0.4 * ramp(t, 0.1, 0.6), cars_stop=0.6)
    gtag(img, '19.6 m/s²')
def s6(img, t, d):   # bathroom scale close-up
    img[:] = grad((210, 215, 220), (160, 165, 170))
    rrect(img, 240, 600, 600, 700, 80, (245, 245, 248)); rrect(img, 380, 700, 320, 150, 20, (40, 40, 45))
    v = counter(t, 0.2, 1.2, 70, 140); text(img, f'{v:.1f}', 540, 775, 110, (80, 240, 120), SERIF_I)
    text(img, 'KG', 540, 900, 44, (80, 80, 85), INTER_B)
    for sx in (-1, 1): rrect(img, 540 + sx * 140 - 70, 980, 140, 220, 40, (225, 225, 230))
    title(img, '×2', None, a=ramp(t, 1.2, 1.4), y=480)
def drop_col(img, x, t, g, lab, col):
    fall = 1.5; T = math.sqrt(2 * fall / g); u = min(1, (t % 2.2) / 1.2 / T * 0.55)
    y = 560 + 800 * min(1, (0.5 * g * ((t % 2.2) * 0.45) ** 2) / fall)
    pass
    rrect(img, x - 40, y - 75, 80, 150, 14, INK); rrect(img, x - 32, y - 65, 64, 120, 8, col)
    text(img, lab, x, 1530, 54, WHITE, INTER_B); text(img, f'{T:.2f} s', x, 1610, 70, col, SERIF_I)
def s7(img, t, d):
    img[:] = grad((70, 50, 40), (25, 20, 18))
    drop_col(img, 300, t, 9.8, 'NORMAL', (240, 200, 120)); drop_col(img, 780, t, 19.6, 'DOUBLE G', (80, 80, 255))
    text(img, 'phone dropped from 1.5 m', W / 2, 420, 50, (220, 220, 225), SERIF_I)
def s8(img, t, d):
    img[:] = grad((60, 30, 120), (20, 10, 50)); vignette(img, 0.4)
    s = 1 + 0.12 * abs(math.sin(t * 7)); emoji(img, '❤️', W / 2, 820, 360 * s)
    k = back(ramp(t, 2.8, 3.1)); rrect(img, W / 2 - 360 * k, 1080, 720 * k, 150, 30, (40, 170, 70))
    if k > 0.8: text(img, '2 G = ROLLER COASTER', W / 2, 1155, 62, WHITE, INTER_B)
def plane(polys, x, y, z):
    box(polys, x, y, z, 6, 6, 60, (235, 235, 240)); box(polys, x, y + 2, z + 4, 70, 1.5, 12, (210, 210, 220)); box(polys, x, y + 6, z - 26, 2, 10, 8, (60, 60, 200))
    box(polys, x, y + 2, z - 26, 24, 1.2, 6, (210, 210, 220))
def plane2(polys, x, y, z):
    box(polys, x, y, z, 14, 14, 130, (235, 235, 240)); box(polys, x, y + 4, z + 8, 150, 3, 26, (210, 210, 220)); box(polys, x, y + 14, z - 56, 4, 22, 18, (60, 60, 200))
    box(polys, x, y + 4, z - 56, 50, 2.5, 12, (210, 210, 220))
    for sx in (-40, 40): box(polys, x + sx, y - 6, z + 12, 9, 9, 22, (150, 150, 160))
def s9(img, t, d):
    def ex(p): plane2(p, 0, 120 - 12 * t, 160 + 20 * t)
    world(img, t, lerp_cam(C_UP, Cam((0, 8, -60), 0, 34, 66), t / d), squash=0.6, extra=ex)
    hud(img, 'Wing load', f'{2.0:.1f} g', 'built for 2.5 g', x=110, y=1530)
def s10(img, t, d):
    def ex(p):
        rb = random.Random(4)
        for i in range(14):
            x = rb.uniform(-40, 40); z = rb.uniform(-10, 80); y0 = rb.uniform(40, 80); fall = 0.5 * 19.6 * min(t, 1.3) ** 2 * 3
            y = max(1, y0 - fall + (6 * math.sin(t * 30 + i) if t > 1.3 else 0)); box(p, x, y, z, 2, 1.2, 1.4, (120, 120, 130)); box(p, x, y + 0.6, z, 4 + 2 * math.sin(t * 40 + i), 0.3, 1, (150, 150, 160))
    world(img, t, Cam((0, 20, -70), 0, 4, 64), squash=0.6, extra=ex)
def s11(img, t, d):  # fountain arcs
    img[:] = grad((200, 150, 90), (240, 210, 170)); img[1300:] = (150, 155, 160)
    for i, (x, g, lab) in enumerate(((320, 1.0, 'NORMAL'), (760, 2.0, 'DOUBLE G'))):
        hgt = 700 / g; rrect(img, x - 120, 1260, 240, 60, 20, (120, 120, 125))
        for k in range(40):
            u = ((t * 0.9 + k / 40) % 1); sx = (k % 2) * 2 - 1
            px = x + sx * 160 * u; py = 1260 - 4 * hgt * u * (1 - u)
            circ(img, (px, py), 9, (240, 200, 140))
        text(img, lab, x, 1530, 54, INK, INTER_B); text(img, f'{int(hgt * 2 / 70) / 10:.0f}' if False else ('100%' if g == 1 else '50%'), x, 1610, 70, (60, 60, 230) if g > 1 else INK, SERIF_I)
def earth_arc(img, y0=1500):
    circ(img, (W / 2, y0 + 1700), 1800, (180, 120, 50)); circ(img, (W / 2, y0 + 1700), 1800, (230, 200, 160), 6)
def s12(img, t, d):
    img[:] = (12, 8, 6); stars(img, t, 1.0)
    earth_arc(img); drop = 140 * ease(ramp(t, 0.4, d - 0.5))
    x = 200 + 120 * t; y = 700 + drop
    rrect(img, x - 70, y - 8, 140, 16, 4, (220, 220, 225)); rrect(img, x - 12, y - 30, 24, 60, 4, (200, 200, 205))
    for sx in (-1, 1): rrect(img, x + sx * 90 - 30, y - 50, 60, 100, 4, (140, 90, 40))
    hud(img, 'Space station', f'-{int(counter(t, 0.4, d - 0.5, 0, 109))} m', '400 km up', x=110, y=420)
def s13(img, t, d):
    img[:] = (12, 8, 6); stars(img, t, 1.0)
    x = W / 2; y = 860 + 30 * ease(ramp(t, 0.3, d))
    circ(img, (x, y), 280, (200, 205, 210))
    for a, r, rr in ((0.5, 120, 50), (2.2, 160, 40), (4.0, 90, 60), (5.2, 190, 30)): circ(img, (x + r * math.cos(a), y + r * math.sin(a)), rr, (170, 175, 180))
    hud(img, 'The Moon', f'-{counter(t, 0.3, d - 0.3, 0, 3.4):.1f} cm', 'closer to Earth', x=110, y=420)
def s14(img, t, d):
    world(img, t, Cam((-30, 12, -40), 18, -4, 66), squash=0.8)
    n = 3 - int(min(2.99, t / max(0.5, d / 3))); text(img, str(n), W / 2, 760, 300, WHITE, SERIF_I, scale=0.8 + 0.2 * back(ramp(t % (d / 3), 0, 0.2)), stroke=3, scol=(30, 20, 20))
def s15(img, t, d):
    lift = 3.5 * math.sin(math.pi * clamp(t / 1.4)) if t < 1.4 else 0
    world(img, t, Cam((-30, 12, -40), 18, -4, 66), squash=0.8 * (1 - ramp(t, 0, 0.15)), lift=lift)
    flash(img, t, 0, 0.25, WHITE, 0.9); gtag(img, f'{19.6 - 9.8 * ramp(t, 0, 0.1):.1f} m/s²')
def s16(img, t, d):
    lift = 3.0 * abs(math.sin(math.pi * clamp(t / 1.2))) if t < 1.2 else 0
    world(img, t, lerp_cam(C_WIDE, C_HIGH, t / d), lift=lift)
    title(img, 'Hop.', None, a=ramp(t, 0.3, 0.6), y=560)
def s17(img, t, d):
    img[:] = (12, 8, 6); stars(img, t, 1.0)
    circ(img, (W / 2, 900), 200, (180, 120, 50))
    ell(img, (W / 2, 900), 420, 330, (200, 200, 205), th=3)
    ell(img, (W / 2 + 40, 920), 470 * (1 + 0.04 * math.sin(t * 3)), 300, (60, 60, 255), th=4)
    a = t * 1.6; px, py = W / 2 + 40 + 470 * math.cos(a), 920 + 300 * math.sin(a)
    rrect(img, px - 40, py - 6, 80, 12, 4, (230, 230, 235))
    title(img, 'Mission control', 'has questions.', a=ramp(t, 0.6, 0.9), y=1540)
def s18(img, t, d):
    world(img, t, C_HIGH)
    title(img, 'What would you do with', '5 heavy seconds?', a=ramp(t, 0.1, 0.4), y=640)
    pill(img, W / 2, 1000, 'COMMENT BELOW', 54, INK, WHITE, alpha=eout(ramp(t, 0.8, 1.1)))

def OVERLAY(img, t, total):
    if G['t0'] <= t < G['t1']:
        rem = max(0.0, 5 - 5 * (t - G['t0']) / (G['t1'] - G['t0'])); slow = (G['t1'] - G['t0']) / 5
        hud(img, 'Gravity returns in', f'{rem:.2f} s', None, x=110, y=210, sub=f'shown {slow:.0f}x slower')

NOZOOM = (s6, s7, s8, s11, s12, s13, s17)
def timeline(ls, dur):
    G['t0'] = ls(2) + 1.45; G['t1'] = ls(14)
    fs = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18]
    return [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'riser': ls(2) + 1.4, 'boom': [ls(2) + 1.45, ls(4) + 0.3, ls(14)], 'whoosh': [ls(6), ls(9), ls(11), ls(16)],
            'heart': [(ls(7), ls(8))], 'ding': [ls(5) + 1.0, ls(15) + 0.2], 'pop': [ls(13) + k * dur(13) / 3 for k in range(3)], 'end': ls(17) - 0.05}

POST = {
 'title': "What If Gravity Doubled For 5 Seconds? 🌍 #shorts",
 'caption': "Gravity doubles for 5 seconds in Times Square: everyone feels twice as heavy, pigeons drop, the space station sinks ~100 m... and when it snaps back, thousands of people hop at once 😅 What would you do with 5 heavy seconds? 👇",
 'tags': '#whatif #gravity #physics #science #space #3danimation',
 'source': "Physics: g = 9.8 m/s²; fall time t = √(2h/g) (1.5 m: 0.55 s → 0.39 s); airliner limit load factor +2.5 g (FAA 14 CFR 25.337); gravity at ISS altitude ≈ 8.7 m/s² (extra drop in 5 s ≈ ½·8.7·5² ≈ 109 m); Earth's pull at the Moon ≈ 0.0027 m/s² (≈ 3.4 cm in 5 s). A thought experiment, not a real event.",
}
