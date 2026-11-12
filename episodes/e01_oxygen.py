import math, random
import cv2
from kit import *

SLUG = '2026-11-12-oxygen-vanished-5-seconds'
TITLE = 'IF OXYGEN VANISHED FOR 5 SEC'
INFO = 'NEW YORK · 11:59'
LINES = [
 ("If all the oxygen in the air vanished for five seconds...", 0.10),
 ("most people would make one deadly mistake.", 0.30),
 ("This is Sam. He's twenty-three, and he's crossing a street in New York.", 0.25),
 ("At exactly noon, every oxygen molecule in the air disappears.", 0.30),
 ("The air gets twenty-one percent thinner. Sam's ears pop, like he just jumped two kilometers up.", 0.30),
 ("Every fire on Earth goes out. Car engines choke and die.", 0.35),
 ("The rule: hold your breath.", 0.25),
 ("But Sam panics, and gasps for air.", 0.15),
 ("Stupid mistake.", 0.40),
 ("That air has no oxygen left. Just one or two breaths of it can knock you out.", 0.25),
 ("His lungs actually pull oxygen out of his blood.", 0.35),
 ("Five seconds later, the oxygen comes back.", 0.25),
 ("But Sam is already falling... in the middle of the street.", 0.50),
 ("Follow for part two.", 1.0),
]
CAPS = [
 ["IF ALL THE {OXYGEN}", "IN THE AIR", "{VANISHED}", "FOR [5 SECONDS...]"], ["MOST PEOPLE", "WOULD MAKE", "ONE {DEADLY}", "{MISTAKE.}"],
 ["THIS IS [SAM.]", "HE'S [23,]", "CROSSING A STREET", "IN [NEW YORK.]"], ["AT EXACTLY [NOON,]", "EVERY {OXYGEN}", "{MOLECULE}", "{DISAPPEARS.}"],
 ["THE AIR GETS", "{21% THINNER.}", "SAM'S [EARS POP,]", "LIKE HE JUST", "JUMPED [2 KM UP.]"],
 ["EVERY {FIRE}", "ON EARTH {GOES OUT.}", "CAR ENGINES", "{CHOKE AND DIE.}"], ["THE RULE:", "[HOLD YOUR BREATH.]"],
 ["BUT SAM {PANICS,}", "AND {GASPS FOR AIR.}"], ["!STUPID MISTAKE."],
 ["THAT AIR HAS", "{NO OXYGEN LEFT.}", "JUST [1 OR 2 BREATHS]", "CAN {KNOCK YOU OUT.}"], ["HIS LUNGS", "PULL OXYGEN", "{OUT OF HIS BLOOD.}"],
 ["[5 SECONDS] LATER,", "THE OXYGEN", "[COMES BACK.]"], ["BUT SAM IS", "{ALREADY FALLING...}", "IN THE MIDDLE", "OF THE {STREET.}"], ["[FOLLOW]", "FOR PART TWO."]]
MOOD = {'root': 55.0, 'bpm': 108}
SAM = Look(skin=SKINS[1], hair=(30, 30, 40), style='short', shirt=(60, 60, 200), pants=(110, 70, 40), shoes=(40, 40, 50), extra='hoodie')

rb = random.Random(3)
TOWERS = [(x, rb.randint(500, 1100), rb.choice([(120, 110, 100), (150, 135, 120), (95, 90, 85), (170, 160, 150)])) for x in range(-60, W + 100, 150)]
MOLS = [(rb.uniform(60, W - 60), rb.uniform(420, 1150), rb.uniform(26, 40), rb.uniform(0, 6.28)) for _ in range(26)]
def city(img, t, sky=((235, 180, 90), (250, 228, 190)), dim=0.0):
    img[:1200] = grad(sky[0], sky[1], 0, 1200)
    for i, (x, h, c) in enumerate(TOWERS):
        c2 = mix(c, (60, 50, 50), dim)
        rrect(img, x, 1200 - h, 140, h + 10, 4, c2)
        for wy in range(30, h - 40, 70):
            for wx in (20, 62, 104):
                if (i * 7 + wy // 70 + wx) % 3: rrect(img, x + wx, 1200 - h + wy, 22, 36, 3, mix((235, 225, 190), (90, 80, 70), dim))
    img[1200:] = (120, 120, 125); img[1200:1230] = (175, 175, 180)
    for k in range(9): rrect(img, 60 + k * 112, 1420, 70, 180, 4, (235, 235, 238))   # crosswalk
def taxi(img, x, y, s=1.0, lights=False):
    rrect(img, x - 190 * s, y - 70 * s, 380 * s, 110 * s, 30 * s, (40, 200, 255)); rrect(img, x - 110 * s, y - 140 * s, 220 * s, 90 * s, 30 * s, (40, 200, 255))
    rrect(img, x - 95 * s, y - 128 * s, 85 * s, 62 * s, 10 * s, (230, 200, 150)); rrect(img, x + 10 * s, y - 128 * s, 85 * s, 62 * s, 10 * s, (230, 200, 150))
    rrect(img, x - 40 * s, y - 170 * s, 80 * s, 30 * s, 6 * s, WHITE); text(img, 'TAXI', x, y - 155 * s, int(28 * s), INK)
    for dx in (-115, 115): circ(img, (x + dx * s, y + 40 * s), 44 * s, INK); circ(img, (x + dx * s, y + 40 * s), 20 * s, GREY)
    if lights: glow(img, x + 180 * s, y - 20 * s, int(200 * s), (120, 220, 255), 1.0)
def o2(img, x, y, r, a=1.0, col=(255, 200, 120)):
    if a <= 0.02: return
    circ(img, (x - r * 0.55, y), r * a, col); circ(img, (x + r * 0.55, y), r * a, col)
    text(img, 'O2', x, y + 2, int(r * 0.9), INK, ANT, alpha=a)

def shotA(img, t, d):
    city(img, t)
    V = 1.9   # 'vanished'
    for i, (x, y, r, ph) in enumerate(MOLS):
        yy = y + 18 * math.sin(t * 2 + ph)
        if t < V + i * 0.03: o2(img, x, yy, r)
        else:
            q = ramp(t, V + i * 0.03, V + i * 0.03 + 0.18)
            if q < 1: cv2.circle(img, P(x, yy), int(r * (1 + q) * 8), WHITE, 3, cv2.LINE_AA, 3)
    flash(img, t, V, 0.2, WHITE, 0.5)
    pill(img, W / 2, 1560, 'AIR · 21% OXYGEN' if t < V else 'AIR · 0% OXYGEN', 54, INK, YEL if t < V else RED)
    header(img, eout(ramp(t, 0.05, 0.4)))
def shotB(img, t, d):
    city(img, t)
    for i, (x, y, r, ph) in enumerate(MOLS[::2]): o2(img, x, y + 18 * math.sin(t * 2 + ph), r * 0.8)
    taxi(img, 870 - 30 * t, 1330, 0.9)
    person(img, SAM, 380 + 40 * t, 1000 + 6 * abs(math.sin(t * 6)), 1.15, 'smile', al=20 + 15 * math.sin(t * 6), ar=20 - 15 * math.sin(t * 6))
    namecard(img, t, 'SAM · 23', 'ON HIS LUNCH BREAK', 790, 560)
    pill(img, W / 2, 330, 'NEW YORK · 11:59:58', 46, INK, WHITE, dot=YEL, alpha=eout(ramp(t, 1.2, 1.5)))
def shotC(img, t, d):
    img[:] = grad((60, 30, 20), (25, 12, 10)); glow(img, W / 2, 820, 560, (40, 60, 160), 0.6 + 0.2 * math.sin(t * 8))
    sec = 58 + int(ramp(t, 0, 0.9) * 2); s_ = f'11:59:{sec:02d}' if sec < 60 else '12:00:00'
    rrect(img, 120, 620, 840, 300, 40, INK); rrect(img, 134, 634, 812, 272, 30, (40, 30, 30))
    text(img, s_, W / 2, 772, 190, RED if sec >= 60 else YEL, ANT)
    Z = 0.9
    for i, (x, y, r, ph) in enumerate(MOLS):
        yy = y * 0.6 + 900 + 10 * math.sin(t * 3 + ph)
        if not (220 < yy < 1240 and 120 < x < 960) or t < Z:
            if t < Z: o2(img, x, (yy + 300) % 1500 + 200, r * 0.8)
            else:
                q = ramp(t, Z + i * 0.04, Z + i * 0.04 + 0.2)
                if q < 1: o2(img, x, (yy + 300) % 1500 + 200, r * 0.8 * (1 - q))
    flash(img, t, Z, 0.25, WHITE, 0.6)
    pill(img, W / 2, 1060, 'O2 MOLECULES LEFT: 0' if t > Z + 0.6 else 'O2 MOLECULES: EVERYWHERE', 46, INK, RED if t > Z + 0.6 else WHITE)
def shotD(img, t, d):
    city(img, t)
    person(img, SAM, W / 2, 1050, 1.5, 'shock' if t > 0.9 else 'worry', al=150, ar=150)
    q = ramp(t, 1.9, 2.2)   # ears pop
    for sx in (-1, 1):
        for k in range(3):
            r = 60 + k * 40 + 60 * ((t * 2) % 1)
            if t > 1.9: cv2.ellipse(img, P(W / 2 + sx * 150, 1060), (int(r * 8), int(r * 8)), 0, -40 if sx > 0 else 140, 40 if sx > 0 else 220, YEL, 5, cv2.LINE_AA, 3)
    v = counter(t, 0.2, 1.2, 100, 79)
    statbox(img, t, 'AIR PRESSURE', f'{v:.0f}%', RED if v < 90 else YEL)
    fact(img, t, 'AIR IS ~21% OXYGEN', 1.4)
    if t > 1.9: pill(img, W / 2, 1640, 'POP!', 70, RED, WHITE, alpha=eout(ramp(t, 1.9, 2.0)))
def flame(img, x, y, s, k):
    if k <= 0.02: return
    poly(img, [(x - 40 * s * k, y), (x, y - 140 * s * k - 14 * math.sin(random.random() * 6)), (x + 40 * s * k, y)], (40, 120, 250)); poly(img, [(x - 20 * s * k, y), (x, y - 70 * s * k), (x + 20 * s * k, y)], (90, 220, 255))
def shotE(img, t, d):
    city(img, t, dim=0.15)
    OUT = 0.6
    # hot-dog cart
    rrect(img, 120, 1150, 340, 180, 16, (200, 200, 205)); rrect(img, 100, 980, 380, 40, 10, RED); line(img, (140, 1020), (140, 1150), INK, 8); line(img, (440, 1020), (440, 1150), INK, 8)
    for k in range(4): flame(img, 170 + k * 80, 1150, 0.8, 1 - ramp(t, OUT, OUT + 0.15))
    if t > OUT:
        for k in range(4): circ(img, (170 + k * 80 + 10 * math.sin(t * 3 + k), 1100 - 120 * ((t - OUT + k * 0.2) % 1)), 18, (200, 200, 205))
    taxi(img, 760, 1380, 0.95)
    if t > ramp(1, 0, 1) * 1.6:
        for k in range(3): circ(img, (560 - (t * 80) % 60 - k * 40, 1380 - k * 20), 22 + k * 8, (90, 90, 95))
        pill(img, 760, 1150, 'ENGINE: STALLED', 40, INK, RED, alpha=eout(ramp(t, 1.6, 1.9)))
    statbox(img, t, 'FIRES BURNING ON EARTH', '0', RED, at=0.4)
def bg_red(img, t):
    img[:] = grad((40, 30, 140), (20, 14, 60))
def shotF(img, t, d):
    rule_card(img, t, d, 'HOLD YOUR', 'BREATH.', bg=lambda im, tt: city(im, tt, dim=0.4))
    person(img, SAM, W / 2, 1050, 1.2, 'cheeks', al=10, ar=10)
def shotG(img, t, d):
    S = d - 0.0
    img[:] = grad((70, 60, 200), (30, 24, 90))
    for i in range(16):
        a = i / 16 * 6.283 + t * 0.4; line(img, (W / 2, 900), (W / 2 + 1400 * math.cos(a), 900 + 1400 * math.sin(a)), (60, 50, 170), 40)
    jx, jy = (random.uniform(-10, 10), random.uniform(-10, 10))
    person(img, SAM, W / 2 + jx, 820 + jy, 2.4, 'scream', al=160, ar=160, sweat=True)
    for k in range(5):
        u = (t * 1.6 + k / 5) % 1; o = W / 2 + (k - 2) * 120
        cv2.ellipse(img, P(o, 1080 + 300 * (1 - u)), (int(40 * 8 * (1 - u)), int(20 * 8 * (1 - u))), 0, 0, 360, WHITE, 4, cv2.LINE_AA, 3)
def shotGM(img, t, d):   # stupid mistake
    img[:] = grad((40, 30, 180), (20, 10, 70)); vignette(img, 0.5)
    person(img, SAM, W / 2, 620, 1.7, 'scream', al=170, ar=170)
    flash(img, t, 0, 0.12, WHITE, 0.8)
def lungs(img, cx, cy, s=1.0, col=(150, 150, 245)):
    for sx in (-1, 1):
        ell(img, (cx + sx * 130 * s, cy + 40 * s), 120 * s, 230 * s, col, rot=sx * 8)
    line(img, (cx, cy - 330 * s), (cx, cy - 150 * s), (210, 200, 240), 34 * s)
    for sx in (-1, 1): line(img, (cx, cy - 150 * s), (cx + sx * 90 * s, cy - 90 * s), (210, 200, 240), 26 * s)
def shotH(img, t, d):
    img[:] = grad((60, 30, 25), (25, 12, 10)); glow(img, W / 2, 900, 520, (50, 50, 170), 0.6)
    lungs(img, W / 2, 900, 1.25)
    for k in range(10):   # O2 leaving blood -> lungs -> out
        u = (t * 0.7 + k / 10) % 1; sx = -1 if k % 2 else 1
        x = W / 2 + sx * (330 - 200 * u); y = 1050 - 520 * u
        o2(img, x, y, 22, a=min(1, 3 * (1 - u)), col=(120, 120, 255))
    rrect(img, 120, 1490, 840, 0, 0, INK)
    pill(img, W / 2, 1560, 'BLOOD O2  ' + str(int(counter(t, 0.5, d, 98, 60))) + '%', 50, INK, RED)
    fact(img, t, "CSB: 1-2 BREATHS CAN CAUSE UNCONSCIOUSNESS", 0.8, y=380, size=34)
def shotI(img, t, d):
    city(img, t, dim=0.2 * (1 - ramp(t, 0.6, 1.2)))
    for i, (x, y, r, ph) in enumerate(MOLS):
        q = back(ramp(t, 0.6 + i * 0.03, 0.8 + i * 0.03)); o2(img, x, y + 18 * math.sin(t * 2 + ph), r * q)
    s = int(min(5, ramp(t, 0, 0.6) * 5))
    statbox(img, t, 'TIME WITHOUT OXYGEN', f'0:0{s}', YEL, at=0.0)
def shotJ(img, t, d):
    city(img, t, sky=((200, 150, 80), (240, 210, 170)))
    fall = eout(ramp(t, 0, 0.8))
    cx, cy = W / 2 - 60, 1040 + 260 * fall
    # Sam tipping over
    rotated(img, lambda c: person(c, SAM, cx, cy, 1.15, 'closed', al=40, ar=40), (cx, cy + 300), -78 * fall)
    tx = 1500 - 520 * ramp(t, 0.6, d)
    taxi(img, tx, 1500, 1.25, lights=True)
    if t > 1.0: pill(img, W / 2, 330, 'HONK!', 80, RED, WHITE, alpha=eout(ramp(t, 1.0, 1.15)))
def end_char(img, t):
    taxi(img, W / 2 + 120, 1640, 0.9, lights=True); person(img, SAM, W / 2 - 260, 1420, 0.7, 'closed', al=60, ar=60)
def shotK(img, t, d): end_card(img, t, d, 'THE TAXI', end_char)

NOZOOM = (shotC, shotGM, shotK)
def timeline(ls, dur):
    return [(0, shotA), (ls(2) - 0.1, shotB), (ls(3) - 0.1, shotC), (ls(4) - 0.1, shotD), (ls(5) - 0.1, shotE), (ls(6) - 0.1, shotF),
            (ls(7) - 0.1, shotG), (ls(8) - 0.05, shotGM), (ls(9) - 0.1, shotH), (ls(11) - 0.1, shotI), (ls(12) - 0.1, shotJ), (ls(13) - 0.1, shotK)]
def SFX(ls, dur):
    return {'hook_end': ls(2) - 0.1, 'boom': [1.9, ls(3) + 0.9], 'pop': [ls(4) + 1.9], 'mistake': ls(8), 'heart': [(ls(9), ls(11))],
            'ding': [ls(11) + 0.6], 'end': ls(13) - 0.1}

POST = {
 'title': 'If Oxygen Vanished for 5 Seconds, Don\'t Do This 😮‍💨 Part 1 #shorts',
 'caption': 'If all the oxygen in the air vanished for 5 seconds, most people would make ONE deadly mistake. Would you hold your breath in time? Follow for Part 2. 😮‍💨',
 'tags': '#whatif #oxygen #science #survival #animation #storytime',
}
