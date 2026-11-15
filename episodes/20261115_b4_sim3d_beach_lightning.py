import math, random
from kit import *
from sim3d import *

FORMAT = 'sim3d'
SLUG = '2026-11-15-beach-lightning-30-seconds'
VOICE = 'story'; SPEED = 1.3; CAPTION = 'serif'; ZOOM = 0.6; VIGNETTE = 0.3
MOOD = {'style': 'tension', 'root': 52.0, 'bpm': 100}
LINES = [
 ("Tanline Trevor has thirty seconds to get off this beach. And everything he's about to do is wrong.", 0.3),
 ("Beach influencer. One sponsor. One sunset photo. One very dark cloud.", 0.3),
 ("Flash. He counts. One, two, three... ten seconds to the thunder.", 0.25),
 ("Sound travels about a mile every five seconds. That storm is two miles away.", 0.3),
 ("Trevor thinks: it's not even raining. I'm fine.", 0.3),
 ("Wrong. Lightning can strike up to ten miles from a storm. If you can hear thunder, you're in range.", 0.35),
 ("Stupid mistake number one: he hides under his beach umbrella.", 0.25),
 ("An umbrella, a pavilion, a lifeguard tower. None of them protect you. No place outside is safe.", 0.35),
 ("Mistake number two: the tallest palm tree. If it gets hit, the current can jump sideways into you.", 0.35),
 ("Mistake number three: he wades into the sea to film the storm. Get out of the water. Now.", 0.35),
 ("The right move? A real building, or a hard-topped car with the windows up.", 0.25),
 ("And it's not the rubber tires. It's the metal shell. The current flows around you, into the ground.", 0.35),
 ("Trevor sprints to his car. Door shut. Flash. Boom. Right on his umbrella.", 0.4),
 ("Ten minutes later, the rain stops. The sun comes out. Golden hour. He grabs the door handle.", 0.3),
 ("Nope. Wait thirty minutes after the last thunder. Lightning can still strike as the storm leaves.", 0.35),
 ("So Trevor waits thirty minutes, and shoots his sunset from the driver's seat.", 0.3),
 ("The sponsor loved it. The umbrella did not survive.", 0.4),
 ("Where would you have run first? A, the lifeguard tower, or B, the car? Comment A or B.", 1.0),
]
CAPS = [["Tanline Trevor has [30 seconds]", "to get off this beach."], ["One sponsor. One sunset photo.", "One [very dark cloud.]"],
        ["Flash. He counts...", "[10 seconds] to the thunder."], ["Sound: about [1 mile every 5 s.]", "The storm is [2 miles] away."],
        ["\"It's not even raining.", "I'm fine.\""], ["Lightning can strike up to [10 miles]", "from a storm. Hear thunder = [in range.]"],
        ["Stupid mistake #1:", "the [beach umbrella.]"], ["Umbrella. Pavilion. Lifeguard tower.", "[No place outside is safe.]"],
        ["Mistake #2: the tallest [palm tree.]", "The current can [jump sideways.]"], ["Mistake #3: [the sea.]", "Get out of the water. Now."],
        ["The right move: a [building,]", "or a [hard-topped car,] windows up."], ["Not the tires. The [metal shell.]", "The current flows [around you.]"],
        ["Door shut. Flash. Boom.", "Right on his [umbrella.]"], ["The rain stops. [Golden hour.]", "He grabs the door handle..."],
        ["Nope. Wait [30 minutes]", "after the last thunder."], ["He waits. And shoots his sunset", "from the [driver's seat.]"],
        ["The sponsor loved it.", "The umbrella [did not survive.]"], []]

STORM_SKY = ((70, 55, 50), (120, 110, 105)); STORM_FOG = (120, 112, 108)
SUNSET_SKY = ((150, 90, 120), (90, 170, 250)); SUNSET_FOG = (120, 170, 230)
C_WIDE = Cam((0, 60, -70), 0, -16, 62); C_LOW = Cam((-20, 6, -40), 15, -2, 64); C_SEA = Cam((10, 10, 60), 0, -4, 64)
C_CAR = Cam((-52, 9, -10), 10, -8, 60)
TREV = (40, 140, 250)   # orange shirt (BGR)
G = {}

def trevor(p, x, z, y=0.0, arms=0.0):
    box(p, x, y, z, 1.8, 3.4, 1.1, TREV); box(p, x, y + 3.4, z, 1.2, 1.2, 1.2, (120, 160, 210))
    box(p, x, y + 4.6, z, 1.3, 0.3, 1.3, (40, 40, 40))   # cap
def umbrella(p, x, z, burnt=0.0):
    c = mix((60, 60, 220), (30, 30, 30), burnt)
    box(p, x, 0, z, 0.3, 7, 0.3, (220, 220, 225))
    for a in range(0, 360, 45):
        r0, r1 = math.radians(a), math.radians(a + 45)
        quad(p, [(x, 8, z), (x + 7 * math.cos(r0), 6, z + 7 * math.sin(r0)), (x + 7 * math.cos(r1), 6, z + 7 * math.sin(r1))], c if (a // 45) % 2 else mix((240, 240, 245), (30, 30, 30), burnt))
def tower(p, x, z):
    for sx in (-3, 3):
        for sz in (-3, 3): box(p, x + sx, 0, z + sz, 0.5, 8, 0.5, (220, 220, 225))
    box(p, x, 8, z, 8, 5, 8, (60, 60, 220), top=(240, 240, 240))
def car(p, x, z):
    box(p, x, 0.8, z, 9, 3.4, 18, (200, 120, 50), top=(170, 100, 40)); box(p, x, 4.2, z - 1, 8, 3, 9, (90, 70, 60))
    for sx in (-4.6, 4.6):
        for sz in (-6, 6): box(p, x + sx, 0, z + sz, 1, 2.2, 3, (30, 30, 30))
def world(img, t, cam, sky=STORM_SKY, fog=STORM_FOG, extra=None, crowd=8, rainy=0.0, sea=0.0):
    p = []; beach_scene(p, t, {'crowd': crowd, 'sway': 6, 'dark': 0.6 if sky is STORM_SKY else 0.0, 'sea': sea})
    if extra: extra(p)
    render(img, cam, p, sky=sky, fog=fog, t=t)
    if rainy: rain(img, t, rainy)
def bolt(img, t, at, x=540, y1=1100, dur=0.35, seed=1):
    if not (at <= t < at + dur): return
    rb = random.Random(seed); pts = [(x, -20)]; y = -20
    while y < y1:
        y += rb.uniform(60, 130); pts.append((pts[-1][0] + rb.uniform(-70, 70), min(y, y1)))
    a = 1 - (t - at) / dur
    for q, r in zip(pts, pts[1:]): glow(img, (q[0] + r[0]) / 2, (q[1] + r[1]) / 2, 120, (200, 160, 140), 0.6 * a); line(img, q, r, (255, 245, 240), 9)
    tint(img, (255, 240, 230), 0.35 * a)
def tag(img, label, val, sub=None, a=1.0, y=1560): hud(img, label, val, None, a=a, x=110, y=y, sub=sub)
def mistake(img, t, n, at=0.0):
    k = back(ramp(t, at, at + 0.25))
    if k > 0: rrect(img, W / 2 - 330 * k, 250, 660 * k, 130, 24, (40, 40, 220))
    if k > 0.8: text(img, f'STUPID MISTAKE #{n}', W / 2, 315, 64, WHITE, ANT)

def s1(img, t, d):
    def ex(p): trevor(p, -14, -25); umbrella(p, -6, -18)
    world(img, t, lerp_cam(Cam((-16, 5, -36), 10, -2, 50), C_LOW, t / d), extra=ex)
    title(img, '30 seconds', 'to get off this beach.', a=ramp(t, 0.0, 0.25), y=480)
    tag(img, 'Storm distance', f'{counter(t, 0, d, 3.0, 2.0):.1f} mi', 'Tanline Trevor · beach influencer')
def s2(img, t, d):
    def ex(p): trevor(p, -14, -25)
    world(img, t, lerp_cam(C_LOW, C_WIDE, t / d), extra=ex)
    k = back(ramp(t, 0.3, 0.6)); pill(img, W / 2, 330, 'SPONSOR: 1 SUNSET PHOTO', 46, INK, YEL, dot=YEL, alpha=min(1, k))
    if t > 2.6: emoji(img, '⛈️', 820, 620, 160 * back(ramp(t, 2.6, 2.9)))
def s3(img, t, d):
    world(img, t, C_WIDE); bolt(img, t, 0.1, 820, 900)
    n = int(counter(t, 0.6, d - 0.3, 0, 10)); text(img, str(n), W / 2, 760, 300, WHITE, SERIF_I, stroke=3, scol=(40, 30, 30))
    tag(img, 'Flash to thunder', f'{n} s')
def s4(img, t, d):
    img[:] = grad((60, 45, 40), (30, 22, 20))
    line(img, (140, 900), (940, 900), (200, 200, 205), 4)
    for i in range(3):
        x = 140 + i * 400; circ(img, (x, 900), 14, WHITE); text(img, f'{i} mi', x, 970, 44, WHITE, INTER_B); text(img, f'{i * 5} s', x, 830, 40, YEL, INTER_B)
    k = ease(ramp(t, 0.3, d - 0.4)); emoji(img, '🔊', 140 + 800 * k, 760, 90)
    emoji(img, '⛈️', 940, 640, 140); emoji(img, '🧍', 140, 1080, 110)
    title(img, '~1 mile every 5 s', None, a=ramp(t, 0.2, 0.5), y=440)
def s5(img, t, d):
    def ex(p): trevor(p, -14, -25)
    world(img, t, C_LOW, extra=ex)
    emoji(img, '😎', 540, 640, 150 * back(ramp(t, 0.2, 0.5)))
    tag(img, 'Rain', '0 drops')
def s6(img, t, d):
    img[:] = grad((50, 40, 36), (22, 18, 16))
    for i in range(10):
        r = 70 * (i + 1) * ease(ramp(t, 0.2 + i * 0.08, 0.6 + i * 0.08)); cv2.circle(img, P(W / 2, 900), int(r * 8), (90, 90, 230) if i < 10 else WHITE, 3, cv2.LINE_AA, 3)
    emoji(img, '⛈️', W / 2, 900, 120); emoji(img, '🧍', W / 2 + 280, 900, 80)
    title(img, 'up to 10 miles', None, a=ramp(t, 0.6, 0.9), y=420)
    if t > 3.0: pill(img, W / 2, 1640, 'HEAR THUNDER = IN RANGE', 50, INK, WHITE, dot=RED, alpha=ramp(t, 3.0, 3.3))
def s7(img, t, d):
    def ex(p): trevor(p, -6, -20); umbrella(p, -6, -20)
    world(img, t, lerp_cam(C_LOW, Cam((-14, 7, -36), 12, -6, 56), t / d), extra=ex, rainy=0.4); mistake(img, t, 1, 0.2)
def s8(img, t, d):
    def ex(p): umbrella(p, -30, -20); tower(p, 10, 10); box(p, 50, 0, -60, 16, 8, 14, (120, 160, 200))
    world(img, t, C_LOW if t < d / 2 else Cam((-20, 18, -60), 15, -10, 64), extra=ex, rainy=0.6)
    for i, ch in enumerate(('☂️', '⛱️', '🛟')):
        k = back(ramp(t, 0.3 + i * 0.4, 0.6 + i * 0.4))
        if k > 0: emoji(img, ch, 280 + i * 260, 420, 110 * k); line(img, (220 + i * 260, 360), (340 + i * 260, 480), (60, 60, 255), 10) if k > 0.9 else None
    if t > 3.4: title(img, 'No place outside is safe.', None, a=ramp(t, 3.4, 3.7), y=1580)
def s9(img, t, d):
    def ex(p): trevor(p, 12, -10); palm(p, 10, -14, h=38)
    world(img, t, Cam((-10, 8, -50), 18, 8, 62), extra=ex, rainy=0.7); mistake(img, t, 2, 0.1)
    bolt(img, t, 2.6, 640, 760, 0.5, seed=3)
    if t > 2.7: line(img, (640, 900), (600, 1180), (255, 240, 200), 6) if t < 3.2 else None
def s10(img, t, d):
    def ex(p): trevor(p, 0, 150 + 10 * ramp(t, 0, d), y=-1.5)
    world(img, t, C_SEA, extra=ex, rainy=0.8); mistake(img, t, 3, 0.1)
    if t > 3.4: pill(img, W / 2, 1600, 'GET OUT OF THE WATER', 54, INK, WHITE, dot=RED, alpha=ramp(t, 3.4, 3.7))
def s11(img, t, d):
    def ex(p): car(p, -40, 30)
    world(img, t, lerp_cam(C_CAR, Cam((-46, 7, 5), 4, -6, 54), t / d), extra=ex, rainy=0.6)
    k = back(ramp(t, 0.3, 0.6)); pill(img, W / 2, 330, 'SAFE: BUILDING OR HARD-TOPPED CAR', 46, INK, (90, 200, 90), dot=(90, 200, 90), alpha=min(1, k))
def s12(img, t, d):
    img[:] = grad((60, 45, 40), (25, 20, 18)); y0 = 1150
    rrect(img, 200, y0 - 160, 680, 160, 40, (50, 110, 200)); rrect(img, 330, y0 - 300, 420, 160, 50, (50, 110, 200), 8)
    for x in (320, 760): circ(img, (x, y0 + 10), 70, (30, 30, 30))
    k = ramp(t, 0.6, 3.0); pts = [(540, 300), (540, y0 - 300), (330, y0 - 230), (230, y0 - 80), (330, y0 + 10), (540, 1600)]
    n = int(len(pts) * k) + 1
    for q, r in zip(pts[:n], pts[1:n]): line(img, q, r, (90, 240, 255), 10); glow(img, (q[0] + r[0]) / 2, (q[1] + r[1]) / 2, 80, (40, 160, 200), 0.5)
    emoji(img, '🙂', 540, y0 - 220, 90)
    if t > 0.5: text(img, 'TIRES?', 320, y0 + 140, 44, (150, 150, 155), INTER_B); line(img, (240, y0 + 140), (400, y0 + 140), (60, 60, 230), 6)
    title(img, 'The metal shell.', None, a=ramp(t, 1.6, 1.9), y=440)
def s13(img, t, d):
    def ex(p): car(p, -40, 30); umbrella(p, -20, 60, burnt=ramp(t, 2.2, 2.4))
    jx, jy = shake(t, 2.2, 0.5, 20)
    world(img, t, Cam((-52 + jx * 0.1, 12 + jy * 0.1, -25), 14, -8, 62), extra=ex, rainy=0.9)
    bolt(img, t, 2.2, 560, 1080, 0.45, seed=7)
    if t > 2.5: emoji(img, '🔥', 560, 1060, 110 * back(ramp(t, 2.5, 2.8)))
def s14(img, t, d):
    k = ramp(t, 0.3, 2.0)
    def ex(p): car(p, -40, 30)
    sky = SUNSET_SKY if k > 0.5 else STORM_SKY
    world(img, t, C_CAR, sky=sky, fog=SUNSET_FOG if k > 0.5 else STORM_FOG, extra=ex, rainy=0.7 * (1 - k))
    tag(img, 'Last thunder', f'{int(counter(t, 0, 1.0, 0, 10))} min ago')
    if t > 3.2: emoji(img, '✋', 640, 1000, 120 * back(ramp(t, 3.2, 3.5)))
def s15(img, t, d):
    def ex(p): car(p, -40, 30)
    world(img, t, C_CAR, sky=SUNSET_SKY, fog=SUNSET_FOG, extra=ex)
    k = back(ramp(t, 0.0, 0.25)); rrect(img, W / 2 - 220 * k, 330, 440 * k, 130, 24, (40, 40, 220))
    if k > 0.8: text(img, 'NOPE.', W / 2, 395, 80, WHITE, ANT)
    tag(img, 'Wait', '30 min', 'after the last thunder')
def s16(img, t, d):
    def ex(p): car(p, -40, 30)
    world(img, t, lerp_cam(C_CAR, Cam((-42, 6, 8), 2, 0, 50), t / d), sky=SUNSET_SKY, fog=SUNSET_FOG, extra=ex)
    tag(img, 'Waited', f'{int(counter(t, 0.2, 2.0, 10, 30))} min')
    if t > 2.6:
        k = back(ramp(t, 2.6, 2.9)); rrect(img, W / 2 - 230 * k, 560, 460 * k, 300, 20, WHITE)
        if k > 0.8: rrect(img, W / 2 - 210, 580, 420, 220, 10, (90, 160, 250)); circ(img, (W / 2, 720), 50, (120, 220, 255)); text(img, '#ad', W / 2, 830, 30, INK, INTER_B)
def s17(img, t, d):
    def ex(p): umbrella(p, -6, -20, burnt=1.0)
    world(img, t, Cam((-14, 6, -40), 12, -4, 56), sky=SUNSET_SKY, fog=SUNSET_FOG, extra=ex)
    emoji(img, '👍', 300, 520, 130 * back(ramp(t, 0.2, 0.5))); emoji(img, '🪦', 780, 520, 130 * back(ramp(t, 1.6, 1.9)))
def s18(img, t, d):
    def ex(p): tower(p, -30, 30); car(p, 40, 30)
    world(img, t, C_WIDE, extra=ex, rainy=0.4)
    for i, (lab, ch, col) in enumerate((('A · LIFEGUARD TOWER', '🛟', (40, 140, 245)), ('B · THE CAR', '🚗', (235, 150, 50)))):
        k = back(ramp(t, 0.3 + i * 0.3, 0.6 + i * 0.3)); y = 760 + i * 300
        if k > 0: rrect(img, W / 2 - 400 * k, y - 110, 800 * k, 220, 40, col)
        if k > 0.8: emoji(img, ch, W / 2 - 280, y, 110); text(img, lab, W / 2 + 90, y, 50, WHITE, INTER_B)
    pill(img, W / 2, 1420, 'COMMENT A OR B', 54, INK, WHITE, alpha=eout(ramp(t, 1.4, 1.7)))

def OVERLAY(img, t, total):
    if G.get('t0', 9e9) <= t < G.get('t1', 9e9):
        rem = max(0.0, 30 - 30 * (t - G['t0']) / (G['t1'] - G['t0']))
        text(img, f'0:{int(rem):02d}', W - 150, 150, 70, (90, 90, 255), SERIF_I, stroke=2, scol=(30, 20, 20))

NOZOOM = (s4, s6, s12)
def timeline(ls, dur):
    G['t0'] = 0.3; G['t1'] = ls(12) + 1.0
    fs = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18]
    return [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'boom': [ls(2) + 0.1, ls(2) + dur(2), ls(8) + 2.6, ls(12) + 2.2], 'mistake': ls(6) + 0.2,
            'whoosh': [ls(3), ls(10), ls(13)], 'pop': [ls(7) + 0.3, ls(7) + 0.7, ls(7) + 1.1, ls(9) + 0.1, ls(16) + 0.2],
            'ding': [ls(11) + 1.6, ls(15) + 2.6], 'heart': [(ls(12), ls(12) + 2.2)], 'end': ls(17) - 0.05}

POST = {
 'title': "Lightning At The Beach: You Have 30 Seconds ⚡ #shorts",
 'caption': "Tanline Trevor hears thunder at the beach and makes 3 stupid mistakes in 30 seconds: the umbrella, the palm tree, the sea ⚡ Then the one move that actually saves him (and why it's NOT the rubber tires). Where would you have run first: A) the lifeguard tower or B) the car? 👇",
 'tags': '#lightning #survival #beach #storm #safety #3danimation',
 'source': "Sources: NOAA National Weather Service Lightning Safety (weather.gov/safety/lightning): 'When thunder roars, go indoors'; lightning can strike up to 10 miles from the storm; no place outside is safe; safe shelter = enclosed building or hard-topped vehicle with windows up (not pavilions, sheds, under trees); get out of the water; wait 30 minutes after the last thunder; the metal shell, not rubber tires, protects you in a car; side flash from struck trees. Sound travels ~1 mile per 5 s. Trevor is fictional.",
}
