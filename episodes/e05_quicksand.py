import math, random
import cv2
from kit import *

SLUG = '2026-11-12-quicksand-movies-lied'
TITLE = 'IF YOU STEPPED INTO QUICKSAND'
INFO = 'MORECAMBE BAY · 16:05'
LINES = [
 ("If you stepped into quicksand...", 0.10),
 ("the movies got it completely wrong.", 0.30),
 ("This is Omar. He's twenty-nine, and he's walking across the sands of Morecambe Bay, in England.", 0.25),
 ("One wrong step, and he's in up to his knees.", 0.30),
 ("Good news: you can't sink all the way. Quicksand is about twice as dense as your body.", 0.25),
 ("Most people only go in to around their waist.", 0.35),
 ("But Omar panics, and yanks one leg straight up.", 0.15),
 ("Stupid mistake.", 0.40),
 ("Struggling packs the sand even tighter. Pulling one foot out, even at one centimeter a second, takes the force needed to lift a car.", 0.30),
 ("The rule: lean back, and spread out.", 0.25),
 ("Wiggle your legs slowly, let water seep in, and you'll float up.", 0.35),
 ("But Omar has a bigger problem...", 0.25),
 ("the tide is coming in.", 0.50),
 ("Follow for part two.", 1.0),
]
CAPS = [
 ["IF YOU STEPPED", "INTO {QUICKSAND...}"], ["THE [MOVIES]", "GOT IT", "{COMPLETELY WRONG.}"],
 ["THIS IS [OMAR.]", "HE'S [29,]", "WALKING ACROSS", "THE SANDS OF", "[MORECAMBE BAY,]", "IN ENGLAND."], ["ONE {WRONG STEP,}", "AND HE'S IN", "UP TO HIS [KNEES.]"],
 ["[GOOD NEWS:]", "YOU {CAN'T SINK}", "ALL THE WAY.", "QUICKSAND IS ABOUT", "[TWICE AS DENSE]", "AS YOUR BODY."], ["MOST PEOPLE", "ONLY GO IN", "TO AROUND", "THEIR [WAIST.]"],
 ["BUT OMAR {PANICS,}", "AND {YANKS} ONE LEG", "STRAIGHT UP."], ["!STUPID MISTAKE."],
 ["STRUGGLING", "[PACKS THE SAND]", "EVEN TIGHTER.", "PULLING ONE FOOT OUT,", "EVEN AT [1 CM A SECOND,]", "TAKES THE FORCE", "TO {LIFT A CAR.}"],
 ["THE RULE:", "[LEAN BACK]", "AND [SPREAD OUT.]"], ["[WIGGLE] YOUR LEGS", "SLOWLY,", "LET [WATER] SEEP IN,", "AND YOU'LL", "[FLOAT UP.]"],
 ["BUT OMAR HAS", "A {BIGGER PROBLEM...}"], ["THE {TIDE}", "{IS COMING IN.}"], ["[FOLLOW]", "FOR PART TWO."]]
MOOD = {'root': 58.27, 'bpm': 104}
OMAR = Look(skin=SKINS[1], hair=(30, 30, 40), style='short', shirt=(60, 140, 220), pants=(80, 110, 130), shoes=(40, 60, 90), extra='backpack')
SAND = (130, 195, 225); WET = (95, 155, 190); SKYT, SKYB = (225, 200, 160), (240, 230, 210)
def flats(img, t, horizon=820, tide=0.0, dark=0.0):
    img[:horizon] = grad(mix(SKYT, (120, 110, 110), dark), mix(SKYB, (170, 160, 150), dark), 0, horizon)
    poly(img, [(0, horizon), (200, horizon - 80), (420, horizon - 30), (700, horizon - 110), (1080, horizon - 40), (1080, horizon), (0, horizon)], (120, 130, 110))
    img[horizon:] = grad(SAND, WET, horizon, H)
    for k in range(9):
        y = horizon + 40 + k * k * 9
        for x in range(-100, W + 100, 180): line(img, (x + (k * 53) % 180, y), (x + (k * 53) % 180 + 70, y + 4), mix(SAND, WET, 0.6), 3)
    if tide > 0:
        top = horizon + (H - horizon) * tide
        img[horizon:int(top)] = (140, 95, 40)
        for x in range(0, W, 60): circ(img, (x + (t * 120) % 60, top), 22, (235, 230, 220))
def sunk(img, L, hx, hy, s, depth, expr='shock', al=20, ar=20, top=None):
    """draw person with everything below the sand line y=top hidden; depth in px of how far the feet are below the surface"""
    c = img.copy(); person(c, L, hx, hy + depth, s, expr, al=al, ar=ar)
    surf = int(top if top is not None else hy + 410 * s)
    img[:surf] = c[:surf]
    ell(img, (hx, surf + 4), 150 * s, 26 * s, mix(WET, INK, 0.25)); ell(img, (hx, surf), 130 * s, 18 * s, WET)
def shotA(img, t, d):
    img[:] = grad((60, 70, 80), (30, 35, 45)); tint(img, (60, 120, 160), 0.15)
    for y in range(0, H, 6): img[y] = (img[y] * 0.85).astype(np.uint8)   # old-film scanlines
    img[1150:] = (70, 120, 150)
    hand = 1150 - 160 + 140 * ramp(t, 0, 1.4)
    rrect(img, W / 2 - 20, hand, 40, 200, 14, OMAR.skin); circ(img, (W / 2, hand), 34, OMAR.skin)
    for k in range(4): line(img, (W / 2 - 30 + k * 20, hand - 20), (W / 2 - 34 + k * 22, hand - 60), OMAR.skin, 16)
    img[1150:] = (70, 120, 150); ell(img, (W / 2, 1150), 160, 22, (55, 95, 125))
    text(img, 'THE MOVIES', W / 2, 560, 120, (200, 200, 205), ANT, alpha=ramp(t, 0.2, 0.5))
    W_ = 2.0
    if t > W_:
        k = back(ramp(t, W_, W_ + 0.25)); line(img, (W / 2 - 300 * k, 760 - 300 * k), (W / 2 + 300 * k, 760 + 300 * k), RED, 46); line(img, (W / 2 + 300 * k, 760 - 300 * k), (W / 2 - 300 * k, 760 + 300 * k), RED, 46)
    header(img, eout(ramp(t, 0.05, 0.4)))
def shotB(img, t, d):
    flats(img, t)
    x = 300 + 70 * t
    person(img, OMAR, x, 980 + 6 * abs(math.sin(t * 6)), 1.05, 'smile', al=20 + 15 * math.sin(t * 6), ar=20 - 15 * math.sin(t * 6))
    namecard(img, t, 'OMAR · 29', 'HIKING THE BAY', 780, 520)
    pill(img, W / 2, 330, 'MORECAMBE BAY, ENGLAND', 46, INK, WHITE, dot=YEL, alpha=eout(ramp(t, 1.2, 1.5)))
def shotC(img, t, d):
    flats(img, t)
    dep = 110 * eout(ramp(t, 0.3, 1.4)); jx, jy = shake(t, 0.3, 0.3, 10)
    sunk(img, OMAR, W / 2 + jx, 820 + jy, 1.2, dep, 'shock' if t > 0.4 else 'smile', al=60, ar=60, top=820 + 410 * 1.2)
    pill(img, W / 2, 330, 'DEPTH: KNEES', 54, INK, YEL, alpha=eout(ramp(t, 1.2, 1.5)))
def beaker(img, x, y, fill, label, val, col, k):
    rrect(img, x - 140, y - 260, 280, 400, 26, (215, 220, 225)); rrect(img, x - 126, y - 246 + 372 * (1 - fill * k), 252, 372 * fill * k, 18, col)
    text(img, label, x, y + 210, 60, INK, ANT); text(img, val, x, y + 290, 54, mix(col, INK, 0.3))
def shotD(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    beaker(img, 300, 900, 0.5, 'YOU', '~1 G/ML', (140, 185, 232), eout(ramp(t, 0.6, 1.2)))
    beaker(img, 780, 900, 1.0, 'QUICKSAND', '~2 G/ML', (90, 150, 190), eout(ramp(t, 1.4, 2.0)))
    statbox(img, t, 'DENSITY', '2X', YEL, y=330, at=2.4)
def shotE(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    surf = 900
    img[surf:] = grad(SAND, WET, surf, H)
    for k in range(60): circ(img, ((k * 131) % W, surf + 40 + (k * 211) % 900), 5, mix(WET, INK, 0.2))
    sunk(img, OMAR, W / 2, 634, 1.0, 0, 'worry', al=60, ar=60, top=surf + 4)
    c = np.zeros_like(img); person(c, OMAR, W / 2, 634, 1.0, 'worry', al=60, ar=60); m = c.any(2); m[:surf + 6] = False
    img[m] = (img[m] * 0.45 + c[m] * 0.55).astype(np.uint8)
    for x in range(80, W - 80, 60): line(img, (x, surf + 2), (x + 30, surf + 2), RED, 6)
    pill(img, W / 2, 1640, 'MAX DEPTH: ABOUT THE WAIST', 46, INK, RED, alpha=eout(ramp(t, 0.6, 0.9)))
    fact(img, t, 'NATURE, 2005: PEOPLE CAN\'T SINK ALL THE WAY', 1.0, y=360, size=36)
def shotF(img, t, d):
    flats(img, t)
    pull = ramp(t, 0.3, 1.0); jx, jy = random.uniform(-8, 8), random.uniform(-8, 8)
    sunk(img, OMAR, W / 2 + jx, 760 + jy - 30 * pull, 1.2, 170, 'scream', al=150, ar=150, top=1250)
    for k in range(8):
        a = k / 8 * 6.283; line(img, (W / 2 + 160 * math.cos(a), 1260 + 30 * math.sin(a)), (W / 2 + (200 + 80 * pull) * math.cos(a), 1260 + (40 + 20 * pull) * math.sin(a)), mix(WET, INK, 0.5), 6)
    pill(img, W / 2, 330, 'PULL!', 90, RED, WHITE, alpha=eout(ramp(t, 0.3, 0.4)))
def shotG(img, t, d):
    img[:] = grad((40, 30, 180), (20, 10, 70)); vignette(img, 0.5)
    person(img, OMAR, W / 2, 600, 1.6, 'scream', al=150, ar=150)
    flash(img, t, 0, 0.12, WHITE, 0.8)
def carshape(img, x, y, s):
    rrect(img, x - 150 * s, y - 50 * s, 300 * s, 80 * s, 24 * s, (60, 60, 190)); poly(img, [(x - 90 * s, y - 50 * s), (x - 50 * s, y - 110 * s), (x + 70 * s, y - 110 * s), (x + 110 * s, y - 50 * s)], (60, 60, 190))
    for dx in (-90, 90): circ(img, (x + dx * s, y + 30 * s), 32 * s, INK)
def shotH(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    surf = 1150; img[surf:] = grad(SAND, WET, surf, H)
    for k in range(80): circ(img, ((k * 131) % W, surf + 30 + (k * 211) % 700), 6, mix(WET, INK, 0.25 + 0.2 * (k % 2)))
    # foot pulled by a rope with a car on the other side (balance)
    lift = 30 * math.sin(t * 2) * 0.3
    rrect(img, 380, surf - 40, 70, 260, 20, OMAR.pants); rrect(img, 360, surf + 200, 110, 50, 20, OMAR.shoes)
    line(img, (415, surf - 40), (415, 700), (90, 120, 160), 8); circ(img, (600, 640), 60, GREY); line(img, (415, 640), (600, 580), (90, 120, 160), 8)
    line(img, (660, 640), (760, 900 + lift), (90, 120, 160), 8)
    carshape(img, 760, 990 + lift, 1.2)
    text(img, '=', 600, 820, 100, INK, ANT)
    statbox(img, t, 'FORCE TO FREE 1 FOOT', '≈ 1 CAR' if False else '~1 CAR', RED, y=300, at=2.6)
    fact(img, t, 'BONN ET AL., NATURE 2005', 3.4, y=1700)
def shotI(img, t, d):
    rule_card(img, t, d, 'LEAN BACK', 'SPREAD OUT.', bg=lambda im, tt: flats(im, tt))
    rotated(img, lambda c: person(c, OMAR, W / 2, 1120, 0.85, 'determined', al=100, ar=100), (W / 2, 1300), 75)
def shotJ(img, t, d):
    flats(img, t)
    up = ramp(t, 0.8, d)
    rotated(img, lambda c: person(c, OMAR, W / 2, 1060 - 40 * up, 1.0, 'flat', al=100, ar=100), (W / 2, 1290 - 40 * up), 78 + 4 * math.sin(t * 6))
    for k in range(8):
        u = (t * 0.8 + k / 8) % 1; circ(img, (W / 2 - 300 + k * 85, 1360 - 60 * u), 10 * (1 - u) + 2, (230, 200, 150))
    for k in range(3): poly(img, [(W / 2 - 200 + k * 200, 760 - 40 * ((t + k * 0.3) % 1)), (W / 2 - 230 + k * 200, 810 - 40 * ((t + k * 0.3) % 1)), (W / 2 - 170 + k * 200, 810 - 40 * ((t + k * 0.3) % 1))], GREEN)
    pill(img, W / 2, 330, 'FLOATING UP', 54, INK, GREEN, alpha=eout(ramp(t, 1.4, 1.7)))
def shotK(img, t, d):
    tide = 0.08 + 0.32 * ease(ramp(t, 0, d)); flats(img, t, tide=tide, dark=0.25)
    sunk(img, OMAR, W / 2, 880, 1.0, 150, 'shock', al=20, ar=20, top=880 + 410)
    pill(img, W / 2, 330, 'TIDE: INCOMING', 54, INK, RED, dot=RED, alpha=eout(ramp(t, 0.3, 0.6)))
def end_char(img, t):
    img[1500:1720] = (140, 95, 40)
    for x in range(0, W, 60): circ(img, (x + (t * 120) % 60, 1500), 18, (235, 230, 220))
    person(img, OMAR, W / 2, 1390, 0.45, 'shock', al=150, ar=150, legs=False)
    img[1500:1720] = (140, 95, 40)
def shotL(img, t, d): end_card(img, t, d, 'THE TIDE', end_char)

NOZOOM = (shotA, shotG, shotL, shotD, shotH)
def timeline(ls, dur):
    return [(0, shotA), (ls(2) - 0.1, shotB), (ls(3) - 0.1, shotC), (ls(4) - 0.1, shotD), (ls(5) - 0.1, shotE), (ls(6) - 0.1, shotF), (ls(7) - 0.05, shotG),
            (ls(8) - 0.1, shotH), (ls(9) - 0.1, shotI), (ls(10) - 0.1, shotJ), (ls(11) - 0.1, shotK), (ls(13) - 0.1, shotL)]
def SFX(ls, dur):
    return {'hook_end': ls(2) - 0.1, 'boom': [ls(1) + 0.4, ls(3) + 0.3], 'mistake': ls(7), 'heart': [(ls(11), ls(13))], 'splash': [ls(12)],
            'end': ls(13) - 0.1}

POST = {
 'title': "If You Stepped Into Quicksand, The Movies Lied 😳 Part 1 #shorts",
 'caption': "You step into quicksand. Hollywood says you sink and vanish. Science says you won't... but one move makes it way worse. Would you know what to do? Follow for Part 2. 😳",
 'tags': '#whatif #quicksand #survival #science #animation #storytime',
}
