import math, random
import cv2
from kit import *

SLUG = '2026-11-12-elevator-cable-snapped'
TITLE = 'IF YOUR ELEVATOR FELL 40 FLOORS'
INFO = 'FLOOR 39 · 08:58'
LINES = [
 ("If your elevator cable snapped on the fortieth floor...", 0.10),
 ("jumping at the last second would not save you.", 0.30),
 ("This is Nina. She's thirty, and she's riding up to her office on the fortieth floor.", 0.25),
 ("Then she hears a loud snap.", 0.35),
 ("Good news first. Elevators hang on four to eight steel cables, and each one can hold the car on its own.", 0.25),
 ("And if the car falls too fast, safety brakes clamp onto the rails.", 0.35),
 ("But let's say everything fails.", 0.35),
 ("Nina's plan? Jump right before impact.", 0.15),
 ("Stupid mistake.", 0.40),
 ("From forty floors, she'd be falling at over a hundred and fifty kilometers an hour. Her jump? About ten.", 0.30),
 ("She'd still hit the floor at almost full speed.", 0.30),
 ("The rule: lie flat on the floor.", 0.25),
 ("It spreads the impact across her whole body.", 0.35),
 ("Then the brakes kick in... and Nina is stuck between two floors.", 0.50),
 ("Follow for part two.", 1.0),
]
CAPS = [
 ["IF YOUR {ELEVATOR}", "{CABLE SNAPPED}", "ON THE [40TH FLOOR...]"], ["{JUMPING}", "AT THE LAST SECOND", "WOULD {NOT SAVE YOU.}"],
 ["THIS IS [NINA.]", "SHE'S [30,]", "RIDING UP", "TO HER OFFICE", "ON THE [40TH FLOOR.]"], ["THEN SHE HEARS", "A LOUD {SNAP.}"],
 ["[GOOD NEWS] FIRST.", "ELEVATORS HANG ON", "[4 TO 8] STEEL CABLES,", "AND [EACH ONE]", "CAN HOLD THE CAR", "[ON ITS OWN.]"],
 ["AND IF IT FALLS", "TOO FAST,", "[SAFETY BRAKES]", "CLAMP THE RAILS."], ["BUT LET'S SAY", "{EVERYTHING FAILS.}"],
 ["NINA'S PLAN?", "{JUMP} RIGHT", "BEFORE {IMPACT.}"], ["!STUPID MISTAKE."],
 ["FROM [40 FLOORS,]", "SHE'D BE FALLING", "AT {150+ KM/H.}", "HER JUMP?", "ABOUT [10.]"], ["SHE'D STILL", "HIT THE FLOOR", "AT {ALMOST FULL SPEED.}"],
 ["THE RULE:", "[LIE FLAT]", "ON THE FLOOR."], ["IT [SPREADS]", "THE IMPACT", "ACROSS HER [WHOLE BODY.]"],
 ["THEN THE [BRAKES]", "KICK IN...", "AND NINA IS", "{STUCK BETWEEN}", "{TWO FLOORS.}"], ["[FOLLOW]", "FOR PART TWO."]]
MOOD = {'root': 49.0, 'bpm': 112}
NINA = Look(skin=SKINS[0], hair=(40, 40, 90), style='long', shirt=(170, 120, 60), pants=(60, 50, 48), shoes=(40, 40, 120))
STEEL = (175, 170, 165); WALL = (95, 88, 80)

def car(img, cx, cy, s=1.0, inner=None, cables=6, snapped=0, sparks=False):
    w, h = 420 * s, 560 * s
    for k in range(cables):
        x = cx - 90 * s + k * 180 * s / max(1, cables - 1)
        if k < snapped:
            line(img, (x, cy - h / 2 - 40 * s), (x + 30 * s * math.sin(k + 1), cy - h / 2 - 240 * s), STEEL, 6 * s)
        else: line(img, (x, cy - h / 2), (x, cy - h / 2 - 2000), STEEL, 7 * s)
    rrect(img, cx - w / 2, cy - h / 2, w, h, 14 * s, (120, 120, 130)); rrect(img, cx - w / 2 + 14 * s, cy - h / 2 + 14 * s, w - 28 * s, h - 28 * s, 10 * s, (200, 215, 225))
    if inner: inner(img)
    line(img, (cx, cy - h / 2 + 14 * s), (cx, cy + h / 2 - 14 * s), (150, 160, 170), 4 * s)
    if sparks:
        for k in range(10):
            a = random.uniform(0, 6.28); r = random.uniform(20, 90) * s
            line(img, (cx - w / 2, cy + h / 2), (cx - w / 2 + r * math.cos(a), cy + h / 2 + r * math.sin(a)), (120, 230, 255), 4); line(img, (cx + w / 2, cy + h / 2), (cx + w / 2 - r * math.cos(a), cy + h / 2 + r * math.sin(a)), (120, 230, 255), 4)
def shaft(img, t, off=0.0, floor0=40):
    img[:] = grad((70, 60, 55), (45, 40, 36))
    for sx in (250, 830): rrect(img, sx - 12, 0, 24, H, 4, (130, 125, 120))
    sp = 420; y0 = -(off % sp)
    for k in range(0, 7):
        y = y0 + k * sp; f = floor0 - int(off // sp) + 2 - k
        rrect(img, 0, y, 220, 26, 0, (80, 74, 68)); rrect(img, W - 220, y, 220, 26, 0, (80, 74, 68))
        text(img, str(f), 110, y + 70, 64, (150, 170, 200), ANT)
def shotA(img, t, d):
    SNAP = 1.75
    u = max(0.0, t - SNAP); off = 0 if u == 0 else u * u * 2600
    shaft(img, t, off)
    jx, jy = shake(t, SNAP, 0.3, 14)
    car(img, W / 2 + jx, 980 + jy, 1.0, inner=lambda im: person(im, NINA, W / 2 + jx, 880 + jy - 60 * min(1, u), 0.55, 'shock' if u > 0 else 'smile', al=20 if u == 0 else 150, ar=20 if u == 0 else 150), snapped=6 if u > 0 else 0)
    if u > 0: streaks(img, t, 0.6, (200, 200, 200), vertical=True); flash(img, t, SNAP, 0.15, WHITE, 0.6)
    pill(img, W / 2, 1560, 'CABLES: 0' if u > 0 else 'FLOOR 40', 54, INK, RED if u > 0 else YEL)
    header(img, eout(ramp(t, 0.05, 0.4)))
def interior(img, t, floor, light=1.0, down=False):
    img[:] = grad((185, 195, 205), (150, 160, 170))
    rrect(img, 0, 1500, W, 420, 0, (110, 110, 115))
    for x in (80, 1000): line(img, (x, 300), (x, 1500), (200, 210, 220), 6)
    rrect(img, 380, 160, 320, 150, 18, INK); text(img, str(floor), 470, 238, 110, (80, 120, 255), ANT); poly(img, [(600, 200), (640, 260), (680, 200)] if down else [(600, 260), (640, 200), (680, 260)], (80, 120, 255))
    rrect(img, 880, 700, 120, 360, 16, (160, 165, 170))
    for k in range(6): circ(img, (920 + (k % 2) * 40, 760 + (k // 2) * 80), 16, (230, 225, 220) if k != 5 else (80, 200, 255))
def shotB(img, t, d):
    fl = 36 + min(3, int(t * 1.1)); interior(img, t, fl)
    person(img, NINA, 470, 1000, 1.25, 'smile', al=20, ar=110)
    rrect(img, 610, 1060, 50, 70, 8, (235, 190, 120)); rrect(img, 606, 1050, 58, 16, 6, INK)   # coffee
    namecard(img, t, 'NINA · 30', 'LATE FOR A MEETING', 760, 520)
def shotC(img, t, d):
    img[:] = grad((60, 50, 45), (35, 30, 28))
    S = 0.5; snapped = 1 if t > S else 0
    car(img, W / 2, 1450, 1.6, snapped=snapped)
    if t > S:
        for k in range(14):
            a = random.uniform(-3.0, -0.1); r = random.uniform(40, 220)
            line(img, (W / 2 - 145, 1000), (W / 2 - 145 + r * math.cos(a), 1000 + r * math.sin(a)), (120, 230, 255), 5)
        flash(img, t, S, 0.15, WHITE, 0.7)
        pill(img, W / 2, 330, 'SNAP!', 110, RED, WHITE, alpha=eout(ramp(t, S, S + 0.1)))
def shotD(img, t, d):
    img[:] = grad((215, 228, 238), (190, 205, 220))
    for y in range(0, H, 90): cv2.line(img, (0, y), (W, y), (205, 218, 230), 2)
    car(img, W / 2, 1150, 0.95, cables=6)
    for k in range(6):
        x = W / 2 - 86 + k * 34.4; a = back(ramp(t, 0.6 + k * 0.15, 0.8 + k * 0.15))
        if a > 0: circ(img, (x, 760), 18 * a, GREEN); text(img, '✓' if False else str(k + 1), x, 760, int(26 * a), WHITE)
    statbox(img, t, 'STEEL CABLES', '4 - 8', YEL)
    fact(img, t, 'EACH CABLE ALONE CAN HOLD THE CAR', 2.6, y=1650)
def shotE(img, t, d):
    img[:] = grad((215, 228, 238), (190, 205, 220))
    for x in (300, 780): rrect(img, x - 16, 0, 32, H, 4, (140, 140, 150))
    fall = 260 * eout(ramp(t, 0, 0.9)); cy = 700 + fall
    car(img, W / 2, cy, 0.95, cables=0, snapped=0)
    clamp_ = eout(ramp(t, 0.8, 1.0))
    for sx in (-1, 1):
        x = W / 2 + sx * 230; rrect(img, x - 30 + sx * (1 - clamp_) * 30, cy + 220, 60, 90, 8, RED)
    if t > 0.8:
        for k in range(8):
            a = random.uniform(0, 6.28); r = random.uniform(20, 80)
            for sx in (-1, 1): line(img, (W / 2 + sx * 250, cy + 270), (W / 2 + sx * 250 + r * math.cos(a), cy + 270 + r * math.sin(a)), (120, 230, 255), 4)
    pill(img, W / 2, 330, 'SAFETY BRAKES: ON', 54, INK, GREEN, alpha=eout(ramp(t, 0.9, 1.1)))
    fact(img, t, 'OTIS SHOWED THE SAFETY BRAKE IN 1853', 1.6, y=1640, size=38)
def shotF(img, t, d):
    off = 600 + t * 2600; shaft(img, t, off, 40)
    streaks(img, t, 0.8, (210, 210, 210), vertical=True)
    car(img, W / 2 + random.uniform(-5, 5), 980, 1.0, cables=6, snapped=6, inner=lambda im: person(im, NINA, W / 2, 840, 0.55, 'scream', al=160, ar=160))
    pill(img, W / 2, 330, 'BRAKES: FAILED', 54, INK, RED)
def shotG(img, t, d):
    interior(img, t, 22 - int(t * 6) % 20, down=True)
    crouch = 0.5 + 0.5 * math.sin(t * 5)
    person(img, NINA, W / 2, 980 + 60 * crouch, 1.25, 'determined', al=40, ar=40)
    q = back(ramp(t, 0.4, 0.65))
    if q > 0:
        ell(img, (800, 520), 200 * q, 110 * q, WHITE); circ(img, (680, 650), 24 * q, WHITE); circ(img, (640, 700), 14 * q, WHITE)
        text(img, 'JUMP!', 800, 520, int(110 * q), RED, ANT)
def shotGM(img, t, d):
    img[:] = grad((40, 30, 180), (20, 10, 70)); vignette(img, 0.5)
    person(img, NINA, W / 2, 560 - 120 * math.sin(min(t * 4, 3.14)), 1.5, 'shock', al=170, ar=170)
    flash(img, t, 0, 0.12, WHITE, 0.8)
def bar(img, t, y, label, val, vmax, col, at):
    k = eout(ramp(t, at, at + 0.8)); w = 820 * val / vmax * k
    text(img, label, 130 + twidth(label, 52) / 2, y - 60, 52, INK)
    rrect(img, 120, y, 840, 120, 20, (205, 210, 215)); rrect(img, 120, y, max(40, w), 120, 20, col)
    lab = f'{int(val * k)} KM/H'; tw = twidth(lab, 70, ANT)
    text(img, lab, 120 + max(40, w) - tw / 2 - 30 if w > 300 else 120 + max(40, w) + tw / 2 + 30, y + 62, 70, WHITE if w > 300 else INK, ANT)
def shotH(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    bar(img, t, 620, 'ELEVATOR FALL SPEED (40 FLOORS)', 175, 180, RED, 0.3)
    bar(img, t, 960, "NINA'S BEST JUMP", 10, 180, GREEN, 2.6)
    if t > 4.2:
        q = back(ramp(t, 4.2, 4.5)); text(img, '165 KM/H', W / 2, 1560, int(150 * q), RED, ANT, stroke=8, scol=INK)
        text(img, 'STILL LEFT', W / 2, 1680, int(60 * q), INK)
    fact(img, t, '~120 M FALL · IGNORING AIR DRAG', 1.4, y=360, size=36)
def shotJ(img, t, d):
    rule_card(img, t, d, 'LIE FLAT', 'ON THE FLOOR.', bg=lambda im, tt: interior(im, tt, 12, 1.0))
    rotated(img, lambda c: person(c, NINA, W / 2, 1000, 0.9, 'determined', al=170, ar=170), (W / 2, 1200), 90)
def shotK(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    # left: standing -> force in legs ; right: lying -> spread
    rrect(img, 60, 1450, 440, 20, 6, INK); rrect(img, 580, 1450, 440, 20, 6, INK)
    person(img, NINA, 280, 1020, 0.85, 'shock', al=20, ar=20)
    for sx in (-1, 1): poly(img, [(280 + sx * 32 - 20, 1460), (280 + sx * 32 + 20, 1460), (280 + sx * 32, 1560)], RED)
    rotated(img, lambda c: person(c, NINA, 800, 1180, 0.72, 'flat', al=170, ar=170), (800, 1410), 90)
    for k in range(7):
        x = 640 + k * 55; a = eout(ramp(t, 0.5 + k * 0.05, 0.8 + k * 0.05)); line(img, (x, 1480), (x, 1480 + 50 * a), GREEN, 10)
    text(img, 'ONE SPOT', 280, 600, 70, RED, ANT); text(img, 'SPREAD OUT', 800, 600, 70, GREEN, ANT)
    text(img, 'X', 280, 700, 110, RED, ANT); text(img, 'OK', 800, 700, 110, GREEN, ANT)
def shotL(img, t, d):
    img[:] = grad((70, 60, 55), (45, 40, 36))
    stop = eout(ramp(t, 0, 1.0)); cy = 500 + 520 * stop
    for y, f in ((620, 12), (1500, 11)):
        rrect(img, 0, y, W, 30, 0, (80, 74, 68)); rrect(img, 60, y - 360, 300, 360, 6, (150, 145, 140)); rrect(img, 720, y - 360, 300, 360, 6, (150, 145, 140))
        text(img, f'FLOOR {f}', 210, y - 400, 52, (150, 170, 200))
    for sx in (250, 830): rrect(img, sx - 12, 0, 24, H, 4, (130, 125, 120))
    car(img, W / 2, cy, 0.95, cables=6, snapped=6, sparks=t < 1.1, inner=lambda im: person(im, NINA, W / 2, cy - 140, 0.5, 'worry' if t > 1.2 else 'scream', al=20, ar=20))
    pill(img, W / 2, 330, 'STOPPED · FLOOR 11 ½', 54, INK, YEL, alpha=eout(ramp(t, 1.2, 1.5)))
def end_char(img, t):
    rrect(img, W / 2 - 160, 1260, 320, 440, 10, (120, 120, 130)); rrect(img, W / 2 - 146, 1274, 292, 412, 8, (200, 215, 225))
    person(img, NINA, W / 2, 1400, 0.45, 'worry', al=150 + 15 * math.sin(t * 8), ar=20)
def shotM(img, t, d): end_card(img, t, d, 'STUCK BETWEEN FLOORS', end_char)

NOZOOM = (shotGM, shotM, shotH)
def timeline(ls, dur):
    return [(0, shotA), (ls(2) - 0.1, shotB), (ls(3) - 0.1, shotC), (ls(4) - 0.1, shotD), (ls(5) - 0.1, shotE), (ls(6) - 0.1, shotF),
            (ls(7) - 0.1, shotG), (ls(8) - 0.05, shotGM), (ls(9) - 0.1, shotH), (ls(11) - 0.1, shotJ), (ls(12) - 0.1, shotK), (ls(13) - 0.1, shotL), (ls(14) - 0.1, shotM)]
def SFX(ls, dur):
    return {'hook_end': ls(2) - 0.1, 'snap': [1.75, ls(3) + 0.4], 'boom': [1.75, ls(6) + 0.2], 'mistake': ls(8), 'ding': [ls(2) + 2.5],
            'heart': [(ls(9), ls(11))], 'end': ls(14) - 0.1}

POST = {
 'title': "If Your Elevator Fell 40 Floors, Don't Jump 🛗 Part 1 #shorts",
 'caption': "Your elevator cable snaps on the 40th floor. Most people think jumping at the last second will save them. It won't. What would YOU do? Follow for Part 2. 🛗",
 'tags': '#whatif #elevator #survival #science #animation #storytime',
}
