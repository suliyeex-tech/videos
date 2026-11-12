import math, random
import cv2
from kit import *

SLUG = '2026-11-12-car-sinking-60-seconds'
TITLE = 'IF YOUR CAR FELL INTO A LAKE'
INFO = 'ICY ROAD · 18:40'
LINES = [
 ("If your car plunged into a lake...", 0.10),
 ("you'd have about sixty seconds to get out alive.", 0.30),
 ("This is Ana. She's twenty-two. Her car just slid off an icy road, straight into the water.", 0.25),
 ("For the first thirty to sixty seconds, the car floats.", 0.30),
 ("Ana grabs her phone to call for help.", 0.15),
 ("Stupid mistake.", 0.40),
 ("Rescuers can't get there in sixty seconds. One expert puts it bluntly: touch your phone, and you're probably going to die.", 0.30),
 ("Within seconds, water presses against the doors. They won't open.", 0.30),
 ("The rule: seatbelt, window, out.", 0.25),
 ("Not the door. The window. Power windows usually keep working for the first thirty to sixty seconds.", 0.30),
 ("Ana unbuckles, and hits the switch...", 0.30),
 ("but her window is stuck.", 0.50),
 ("Follow for part two.", 1.0),
]
CAPS = [
 ["IF YOUR {CAR}", "PLUNGED INTO", "A [LAKE...]"], ["YOU'D HAVE", "ABOUT {60 SECONDS}", "TO GET OUT {ALIVE.}"],
 ["THIS IS [ANA.]", "SHE'S [22.]", "HER CAR JUST SLID", "OFF AN [ICY ROAD,]", "STRAIGHT INTO", "THE {WATER.}"],
 ["FOR THE FIRST", "[30 TO 60 SECONDS,]", "THE CAR [FLOATS.]"], ["ANA GRABS", "HER {PHONE}", "TO CALL FOR HELP."], ["!STUPID MISTAKE."],
 ["RESCUERS CAN'T", "GET THERE IN", "[60 SECONDS.]", "ONE EXPERT SAYS:", "TOUCH YOUR PHONE...", "{AND YOU'RE PROBABLY}", "{GOING TO DIE.}"],
 ["WITHIN SECONDS,", "[WATER PRESSES]", "ON THE DOORS.", "{THEY WON'T OPEN.}"], ["THE RULE:", "[SEATBELT. WINDOW. OUT.]"],
 ["{NOT} THE DOOR.", "[THE WINDOW.]", "POWER WINDOWS", "USUALLY WORK", "FOR THE FIRST", "[30 TO 60 SECONDS.]"],
 ["ANA [UNBUCKLES,]", "AND HITS", "THE [SWITCH...]"], ["BUT HER WINDOW", "{IS STUCK.}"], ["[FOLLOW]", "FOR PART TWO."]]
MOOD = {'root': 46.25, 'bpm': 116}
ANA = Look(skin=SKINS[2], hair=(25, 25, 35), style='curly', shirt=(90, 160, 60), pants=(110, 70, 40), shoes=(40, 40, 60))
CARC = (60, 60, 190); WATER = (140, 90, 30); WATER2 = (110, 65, 20)
START = {}; SPLASH = [0.0]
def T(f, t): return START.get(f, 0) + t
def timer(img, f, t):
    left = max(0, 60 - (T(f, t) - SPLASH[0]))
    col = RED if left < 30 else YEL
    rrect(img, W - 300, 120, 230, 100, 24, INK); circ(img, (W - 250, 170), 30, col, 6)
    line(img, (W - 250, 170), (W - 250 + 22 * math.sin(left / 60 * 6.283), 170 - 22 * math.cos(left / 60 * 6.283)), col, 5)
    text(img, f'0:{int(left):02d}', W - 145, 172, 70, col, ANT)

def carside(img, x, y, s=1.0, ang=0, lights=True, face=None):
    def dr(c):
        rrect(c, x - 260 * s, y - 80 * s, 520 * s, 130 * s, 40 * s, CARC); poly(c, [(x - 150 * s, y - 80 * s), (x - 90 * s, y - 175 * s), (x + 110 * s, y - 175 * s), (x + 180 * s, y - 80 * s)], CARC)
        poly(c, [(x - 130 * s, y - 86 * s), (x - 80 * s, y - 160 * s), (x + 5 * s, y - 160 * s), (x + 5 * s, y - 86 * s)], (230, 210, 170))
        poly(c, [(x + 20 * s, y - 86 * s), (x + 20 * s, y - 160 * s), (x + 100 * s, y - 160 * s), (x + 160 * s, y - 86 * s)], (230, 210, 170))
        if face: face(c)
        for dx in (-160, 160): circ(c, (x + dx * s, y + 50 * s), 52 * s, INK); circ(c, (x + dx * s, y + 50 * s), 22 * s, GREY)
        if lights: circ(c, (x + 250 * s, y - 40 * s), 16 * s, (150, 240, 255))
    if ang: rotated(img, dr, (x, y), ang)
    else: dr(img)
def lake(img, t, level=1180, night=True):
    img[:] = grad((80, 50, 40), (150, 110, 90)) if night else grad((235, 190, 140), (250, 230, 200))
    stars(img, t, 0.4, ymax=600, base=(80, 50, 40)) if night else None
    poly(img, [(0, 700), (300, 560), (600, 680), (900, 540), (1080, 620), (1080, level), (0, level)], (95, 75, 70))
    for x in range(0, W, 140): poly(img, [(x + 20, level), (x + 70, level - 160), (x + 120, level)], (70, 95, 60))
    img[level:] = WATER
    for k in range(10):
        y = level + 60 + k * 70; xo = (t * 60 + k * 90) % 200
        for x in range(-200, W + 200, 200): line(img, (x + xo, y), (x + xo + 90, y), (170, 120, 60), 5)
def shotA(img, t, d):
    lake(img, t)
    P_ = 1.3; u = ramp(t, 0, P_)
    x = 180 + 520 * u; y = 900 + 340 * u * u
    if t < P_: carside(img, x, y, 0.8, ang=-35 * u)
    else:
        carside(img, 700, 1240 + 30 * math.sin(t * 3), 0.8, ang=-25)
        img[1270:] = WATER
        q = ramp(t, P_, P_ + 0.7)
        if q < 1:
            for k in range(14): a = math.pi * (0.1 + 0.8 * k / 13); r = 260 * eout(q); circ(img, (700 + r * math.cos(a) * 1.4, 1250 - r * math.sin(a)), 22 * (1 - q) + 4, WHITE)
        flash(img, t, P_, 0.15, WHITE, 0.5)
    rrect(img, 0, 1180, 240, 40, 0, (60, 60, 70)); poly(img, [(0, 1180), (240, 1180), (300, 1300), (0, 1300)], (100, 110, 120))
    pill(img, W / 2, 1560, 'TIME TO ESCAPE · 60 S', 54, INK, RED)
    header(img, eout(ramp(t, 0.05, 0.4)))
def shotB(img, t, d):
    img[:] = grad((90, 60, 50), (190, 160, 140)); stars(img, t, 0.4, ymax=500, base=(90, 60, 50))
    img[1250:] = (225, 225, 230)
    for x in range(0, W, 180): rrect(img, (x - t * 400) % (W + 180) - 90, 1420, 110, 14, 4, (250, 250, 250))
    spin = 25 * math.sin(t * 2.2) * ramp(t, 0.8, 1.6)
    carside(img, 480, 1250, 1.0, ang=spin, face=lambda c: person(c, ANA, 450, 1135, 0.32, 'smile' if t < 1.6 else 'shock', body=False))
    for k in range(6): circ(img, (180 - k * 30 - (t * 200) % 40, 1300 + 10 * math.sin(k)), 14 + k * 3, (245, 245, 250))
    namecard(img, t, 'ANA · 22', 'DRIVING HOME', 760, 560)
    pill(img, W / 2, 330, 'ROAD: BLACK ICE', 50, INK, (255, 200, 140), dot=(255, 200, 140), alpha=eout(ramp(t, 1.4, 1.7)))
def shotC(img, t, d):
    lake(img, t, 1100)
    bob = 12 * math.sin(t * 2.5)
    carside(img, W / 2, 1110 + bob + 30 * t, 1.0, ang=-12, face=lambda c: person(c, ANA, W / 2 - 40, 990 + bob + 30 * t, 0.32, 'shock', body=False))
    img[1150:] = np.clip(img[1150:].astype(np.int16) * 0 + np.array(WATER), 0, 255).astype(np.uint8)
    for k in range(10):
        y = 1210 + k * 70; xo = (t * 60 + k * 90) % 200
        for x in range(-200, W + 200, 200): line(img, (x + xo, y), (x + xo + 90, y), (170, 120, 60), 5)
    statbox(img, t, 'FLOATING PHASE', '30 - 60 S', YEL)
    fact(img, t, 'GIESBRECHT, 100+ TEST SINKINGS', 1.6, y=1650, size=38)
    timer(img, shotC, t)
def interior(img, t, f, water=0.0):
    img[:] = grad((90, 70, 60), (60, 45, 40))
    rrect(img, 60, 300, 960, 700, 50, (40, 34, 30))
    rrect(img, 100, 340, 880, 620, 40, mix((120, 80, 50), (150, 100, 40), water))   # windshield / outside
    lv = 960 - 620 * water
    if water > 0: rrect(img, 100, lv, 880, 960 - lv, 0, WATER)
    rrect(img, 0, 1000, W, 920, 0, (55, 45, 40))
def shotD(img, t, d):
    interior(img, t, shotD, 0.15)
    person(img, ANA, 520, 1150, 1.3, 'worry', al=20, ar=115)
    ph = (700, 1250)
    rrect(img, ph[0] - 70, ph[1] - 140, 140, 250, 20, INK); rrect(img, ph[0] - 58, ph[1] - 126, 116, 222, 12, (230, 190, 120))
    text(img, '911', ph[0], ph[1] - 50, 60, INK, ANT); text(img, 'CALLING...' if int(t * 3) % 2 else 'CALLING', ph[0], ph[1] + 20, 30, INK)
    timer(img, shotD, t)
def shotE(img, t, d):
    img[:] = grad((40, 30, 180), (20, 10, 70)); vignette(img, 0.5)
    person(img, ANA, W / 2, 600, 1.6, 'shock', al=20, ar=120)
    rrect(img, W / 2 + 150, 720, 110, 190, 16, INK); rrect(img, W / 2 + 160, 730, 90, 170, 10, (230, 190, 120))
    flash(img, t, 0, 0.12, WHITE, 0.8)
def shotF(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    # quote card
    k = back(ramp(t, 3.2, 3.5))
    rrect(img, 90, 1450 - 40 * (1 - k), 900, 300, 30, INK)
    if k > 0.5:
        text(img, '"IF YOU TOUCH YOUR CELL PHONE,', W / 2, 1510, 50, WHITE, alpha=k); text(img, "YOU'RE PROBABLY GOING TO DIE.\"", W / 2, 1580, 50, (120, 140, 255), alpha=k)
        text(img, '- DR. GORDON GIESBRECHT, COLD-WATER EXPERT', W / 2, 1670, 34, (170, 170, 175), alpha=k)
    # ambulance far away vs timer
    rrect(img, 120, 520, 840, 16, 6, (180, 185, 190))
    amb = 150 + 120 * ramp(t, 0, 3)
    rrect(img, amb - 70, 440, 140, 80, 12, WHITE); rrect(img, amb - 30, 452, 22, 50, 0, RED); rrect(img, amb - 44, 466, 50, 22, 0, RED); circ(img, (amb - 40, 525), 18, INK); circ(img, (amb + 40, 525), 18, INK)
    circ(img, (amb, 430), 12, (255, 120, 60) if int(t * 6) % 2 else RED)
    circ(img, (920, 500), 40, RED); text(img, 'ANA', 920, 590, 50, INK)
    text(img, 'RESCUE', amb, 380, 50, INK)
    statbox(img, t, 'ANA HAS', f'0:{int(max(0, 60 - (T(shotF, t) - SPLASH[0]))):02d}', RED, y=760, at=0.2)
def shotG(img, t, d):
    img[:] = grad((150, 100, 40), (90, 55, 20))
    for k in range(12): circ(img, ((k * 97 + t * 30) % W, (1700 - (t * 120 + k * 150) % 1500)), 8 + k % 3 * 4, (200, 160, 110))
    carside(img, W / 2, 1100, 1.25, ang=0, lights=False, face=lambda c: person(c, ANA, W / 2 - 50, 960, 0.4, 'worry', body=False))
    for k in range(5):
        y = 950 + k * 60; a = eout(ramp(t, 0.3 + k * 0.08, 0.6 + k * 0.08))
        line(img, (60, y), (60 + 150 * a, y), WHITE, 10); poly(img, [(60 + 150 * a, y - 22), (60 + 150 * a + 40, y), (60 + 150 * a, y + 22)], WHITE)
    statbox(img, t, 'DOOR', 'WON\'T OPEN', RED, at=1.0, w=720)
    fact(img, t, 'WATER PRESSURE PINS THE DOORS', 1.6, y=1650)
    timer(img, shotG, t)
def shotH(img, t, d):
    rule_card(img, t, d, 'SEATBELT.', 'WINDOW. OUT.', bg=lambda im, tt: interior(im, tt, shotH, 0.3))
    person(img, ANA, W / 2, 1150, 1.1, 'determined', al=30, ar=30)
def shotI(img, t, d):
    interior(img, t, shotI, 0.35)
    # door with X, window with check
    Y = 1400
    rrect(img, 120, Y, 380, 420, 30, (70, 60, 55)); text(img, 'DOOR', 310, Y + 60, 60, WHITE); line(img, (180, Y + 120), (440, Y + 380), RED, 24); line(img, (440, Y + 120), (180, Y + 380), RED, 24)
    rrect(img, 580, Y, 380, 420, 30, (70, 60, 55)); text(img, 'WINDOW', 770, Y + 60, 60, WHITE)
    down = eout(ramp(t, 1.0, 2.5)); rrect(img, 620, Y + 110 + 270 * down, 300, 280 - 270 * down, 10, (200, 180, 140))
    pts = [(690, Y + 240), (750, Y + 310), (870, Y + 160)]
    if t > 2.0: line(img, pts[0], pts[1], GREEN, 26); line(img, pts[1], pts[2], GREEN, 26)
    fact(img, t, 'POWER WINDOWS: USUALLY 30-60 S', 2.8, y=360)
    timer(img, shotI, t)
def shotJ(img, t, d):
    interior(img, t, shotJ, 0.5)
    # buckle close up
    rrect(img, 160, 1480, 300, 120, 20, (40, 40, 45)); rrect(img, 460 - 160 * eout(ramp(t, 0.3, 0.6)), 1510, 140, 60, 10, (200, 200, 210))
    text(img, 'CLICK', 310, 1680, 70, YEL, ANT, alpha=ramp(t, 0.5, 0.6))
    # switch
    q = 40 * ramp(t, 1.3, 1.5)
    rrect(img, 620, 1440, 280, 220, 30, (40, 40, 45)); rrect(img, 700, 1480 + q, 120, 140, 20, (90, 90, 95))
    poly(img, [(760, 1500 + q), (730, 1550 + q), (790, 1550 + q)], WHITE)
    circ(img, (760, 1420 + q), 60, ANA.skin)
    timer(img, shotJ, t)
def shotK(img, t, d):
    interior(img, t, shotK, 0.55 + 0.25 * ramp(t, 0, d))
    person(img, ANA, 520, 1150, 1.3, 'scream', al=20, ar=120)
    jig = 8 * math.sin(t * 40) if t > 0.4 else 0
    rrect(img, 660 + jig, 560, 300, 260, 20, (200, 180, 140)); text(img, 'STUCK', 810 + jig, 690, 90, RED, ANT, alpha=ramp(t, 0.6, 0.7))
    timer(img, shotK, t)
def end_char(img, t):
    rrect(img, 0, 1500, W, 220, 0, WATER); carside(img, W / 2, 1520, 0.6, ang=-15, lights=False)
def shotL(img, t, d): end_card(img, t, d, 'THE STUCK WINDOW', end_char)

NOZOOM = (shotE, shotL, shotF)
def timeline(ls, dur):
    tl = [(0, shotA), (ls(2) - 0.1, shotB), (ls(3) - 0.1, shotC), (ls(4) - 0.1, shotD), (ls(5) - 0.05, shotE), (ls(6) - 0.1, shotF), (ls(7) - 0.1, shotG),
          (ls(8) - 0.1, shotH), (ls(9) - 0.1, shotI), (ls(10) - 0.1, shotJ), (ls(11) - 0.1, shotK), (ls(12) - 0.1, shotL)]
    for a, f in tl: START[f] = round(a * 30) / 30
    SPLASH[0] = ls(3) - 0.1
    return tl
def SFX(ls, dur):
    return {'hook_end': ls(2) - 0.1, 'splash': [1.3, ls(3)], 'boom': [1.3], 'mistake': ls(5), 'heart': [(ls(6), ls(8))], 'pop': [ls(10) + 0.5, ls(10) + 1.4],
            'end': ls(12) - 0.1}

POST = {
 'title': "If Your Car Fell Into a Lake, You'd Have 60 Seconds 🚗💦 Part 1 #shorts",
 'caption': "Your car slides into a lake. You have about 60 seconds. Most people grab their phone first, and that's the deadly mistake. Seatbelt. Window. Out. Follow for Part 2. 🚗💦",
 'tags': '#whatif #survival #carsafety #lifehack #animation #storytime',
}
