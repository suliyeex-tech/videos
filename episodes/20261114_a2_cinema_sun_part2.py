import math, random
import numpy as np, cv2
from kit import *
from cinema import *
import cinema as Cn

FORMAT = 'cinema'
SLUG = '2026-11-14-the-sun-vanished-part-2'
VOICE = 'guy'; SPEED = 1.22; CAPTION = 'karaoke'; TICKS = True; MOOD = {'style': 'cinematic', 'root': 52.0, 'bpm': 96}
PROGRESS = True; PROGRESS_COL = (60, 170, 255); VIGNETTE = 0.3; ZOOM = 1.1
LINES = [
 ("Part two. The Sun just vanished. Here's what happens to you, day by day.", 0.15),
 ("For eight minutes and twenty seconds... nothing. Its last light is still on the way.", 0.15),
 ("Then, total darkness. Even the Moon goes black. It only ever reflected the Sun.", 0.2),
 ("And with nothing to orbit, Earth flies off into space in a straight line.", 0.2),
 ("Day one. The temperature drops about thirty-six degrees Fahrenheit.", 0.15),
 ("Meet your neighbor, Golden Hour Greg. Sunset influencer. He's waiting for golden hour.", 0.2),
 ("Week one. The average temperature falls below zero. Ponds freeze solid.", 0.15),
 ("Photosynthesis stops instantly. Most plants are dead within weeks.", 0.15),
 ("But the giant trees? Some could hang on for decades.", 0.2),
 ("Day nine. Greg posts a black screen. Caption: still waiting. Zero views.", 0.25),
 ("His ring light is now the brightest thing on the planet.", 0.2),
 ("Year one. Minus one hundred degrees Fahrenheit.", 0.15),
 ("And yet, the oceans don't freeze solid. The ice on top works like a blanket.", 0.1),
 ("The deep water stays liquid for hundreds of thousands of years.", 0.2),
 ("So where do you survive? Iceland. Volcanic heat already warms about nine in ten homes there.", 0.15),
 ("Or a submarine, deep in the warmest part of the ocean.", 0.15),
 ("And the microbes around deep-sea vents? They don't even notice the Sun is gone.", 0.2),
 ("Iceland or submarine? Comment your pick.", 1.0),
]
CAPS = [
 ["[PART TWO.]", "THE SUN", "{JUST VANISHED.}", "DAY BY DAY."], ["FOR [8 MIN 20 S...]", "NOTHING.", "ITS LAST LIGHT", "IS {STILL ON THE WAY.}"],
 ["THEN,", "{TOTAL DARKNESS.}", "EVEN THE [MOON]", "GOES BLACK."], ["NOTHING TO ORBIT.", "EARTH FLIES OFF", "IN A [STRAIGHT LINE.]"],
 ["[DAY ONE.]", "THE TEMPERATURE", "DROPS ABOUT", "{36 °F.}"], ["MEET", "[GOLDEN HOUR GREG.]", "SUNSET INFLUENCER.", "{STILL WAITING.}"],
 ["[WEEK ONE.]", "AVERAGE TEMP", "{BELOW ZERO.}", "PONDS", "FREEZE SOLID."], ["PHOTOSYNTHESIS", "{STOPS.}", "MOST PLANTS", "DEAD IN [WEEKS.]"],
 ["BUT GIANT TREES?", "SOME HANG ON", "FOR [DECADES.]"], ["[DAY NINE.]", "GREG POSTS", "A BLACK SCREEN.", "{ZERO VIEWS.}"],
 ["HIS [RING LIGHT]", "IS NOW THE", "{BRIGHTEST THING}", "ON THE PLANET."], ["[YEAR ONE.]", "{MINUS 100 °F.}"], ["YET THE OCEANS", "{DON'T FREEZE SOLID.}", "THE ICE ON TOP", "IS A [BLANKET.]"],
 ["THE DEEP WATER", "STAYS LIQUID", "FOR [100,000s]", "OF YEARS."], ["WHERE DO", "YOU SURVIVE?", "[ICELAND.]", "VOLCANIC HEAT", "WARMS [9 IN 10]", "HOMES."],
 ["OR A [SUBMARINE,]", "DEEP IN THE", "WARMEST OCEAN."], ["DEEP-SEA VENT", "MICROBES?", "THEY {DON'T EVEN}", "[NOTICE.]"], ["[ICELAND]", "OR {SUBMARINE?}"]]
ST = {}
def T(f, t): return ST.get(f, 0) + t
GREG = ((40, 120, 240), SKIN_T[0])

def hud(img, label, value, sub=None, col=WHITE, a=1.0):
    rrect(img, 60, 150, 560, 210, 26, (20, 16, 14)); rrect(img, 60, 150, 10, 210, 4, (60, 170, 255))
    text(img, label, 90 + twidth(label, 28, INTER_B) / 2, 190, 28, (200, 200, 205), INTER_B, alpha=a)
    text(img, value, 90 + twidth(value, 96, SERIF_I) / 2, 268, 96, col, SERIF_I, alpha=a)
    if sub: text(img, sub, 90 + twidth(sub, 24, INTER_B) / 2, 338, 24, (60, 170, 255), INTER_B, alpha=a)
def tempf(v): return f'{int(round(v))} °F'
def frost(img, k):
    if k <= 0: return
    tint(img, (255, 235, 210), 0.35 * k); rb = random.Random(3)
    for i in range(int(160 * k)):
        x = rb.uniform(0, W); y = rb.uniform(0, H)
        if rb.random() < 0.5 or y < 200 or y > H - 200: circ(img, (x, y), rb.uniform(2, 5), (255, 250, 245))
def snow(img, t, k=1.0):
    rb = random.Random(9)
    for i in range(int(120 * k)):
        x = (rb.uniform(0, W) + 40 * math.sin(t + i)) % W; y = (rb.uniform(0, H) + t * rb.uniform(80, 200)) % H
        circ(img, (x, y), rb.uniform(3, 7), (250, 250, 255))
def ringlight(img, x, y, s=1.0, on=1.0):
    line(img, (x, y), (x, y - 520 * s), (60, 60, 60), 10 * s)
    if on: glow(img, x, y - 600 * s, int(240 * s), (180, 200, 220), 0.9 * on)
    cv2.circle(img, P(x, y - 600 * s), int(90 * s * 8), mix((80, 80, 80), (250, 250, 255), on), int(18 * s), cv2.LINE_AA, 3)

def c1(img, t, d):
    city(img, t, night=0.25); crowd(img, t, 1250, 1700, 40, seed=3)
    glow(img, 820, 520, 380, (120, 210, 255), 1.0 * (1 - ramp(t, 0.6, 1.2))); circ(img, (820, 520), 110 * (1 - eout(ramp(t, 0.6, 1.2))), (190, 245, 255))
    k = back(ramp(t, 0.05, 0.3)); rrect(img, W / 2 - 160 * k, 220, 320 * k, 110, 18, RED)
    if k > 0.8: text(img, 'PART 2', W / 2, 275, 72, WHITE, ANT)
    text(img, 'THE SUN VANISHED', W / 2, 430, 110, YEL, ANT, scale=0.7 + 0.3 * back(ramp(t, 0.2, 0.5)), stroke=8, scol=INK)
def c2(img, t, d):
    city(img, t, night=0.1); crowd(img, t, 1250, 1700, 50, seed=4)
    glow(img, 820, 420, 360, (120, 210, 255), 1.0); circ(img, (820, 420), 100, (190, 245, 255))
    s = max(0, 500 - 500 * ramp(t, 0, d)); hud(img, 'LAST SUNLIGHT ARRIVES IN', f'{int(s // 60)}:{int(s % 60):02d}', 'LIGHT NEEDS 8 MIN 20 S', YEL)
def c3(img, t, d):
    city(img, t, night=1.0); k = ramp(t, 0.3, 0.5)
    tint(img, (0, 0, 0), 0.75 * k)
    mk = 1 - ramp(t, 1.4, 2.4); glow(img, 800, 420, 200, (200, 200, 200), 0.6 * mk); circ(img, (800, 420), 80, mix((25, 25, 25), (230, 235, 240), mk))
    flash(img, t, 0.3, 0.12, WHITE, 0.8)
    if t > 2.4: text(img, 'MOON: GONE TOO', W / 2, 300, 60, RED, INTER_B, scale=back(ramp(t, 2.4, 2.6)))
def c4(img, t, d):
    img[:] = (6, 4, 4); stars(img, t, 0.9)
    cv2.circle(img, P(W / 2, 1100), 380 * 8, (90, 90, 100), 3, cv2.LINE_AA, 3)
    k = ease(ramp(t, 0.2, d)); ex = W / 2 + 380 + 0 * k; ey = 1100 - 900 * k
    for j in range(0, int(900 * k), 40): circ(img, (W / 2 + 380, 1100 - j), 5, (60, 170, 255))
    earth(img, ex, ey, 70, t); text(img, 'X', W / 2, 1100, 80, (120, 120, 130), INTER_B)
    text(img, 'WHERE THE SUN WAS', W / 2, 1180, 26, (150, 150, 160), INTER_B)
def c5(img, t, d):
    city(img, t, night=1.0); crowd(img, t, 1250, 1700, 50, seed=6); frost(img, ramp(t, 0, d) * 0.6)
    hud(img, 'AVERAGE TEMPERATURE', tempf(counter(t, 0.3, d - 0.3, 59, 23)), 'DAY 1 · −36 °F', (255, 230, 200))
def c6(img, t, d):
    city(img, t, night=1.0); tint(img, (0, 0, 0), 0.3); frost(img, 0.5)
    ringlight(img, 760, 1500, 1.0, 1.0); Cn.person(img, 470, 1500, 1.5, GREG[0], GREG[1], arms_up=0.15)
    rrect(img, 520, 1080, 30, 54, 6, INK)
    namecard(img, t, 'GOLDEN HOUR GREG', 'SUNSET INFLUENCER · 41 FOLLOWERS · WAITING', W / 2, 560, at=0.3)
    k = back(ramp(t, 1.4, 1.7)); pill(img, W / 2, 330, 'NEXT GOLDEN HOUR: NEVER', 46, INK, YEL, dot=RED, alpha=k)
def c7(img, t, d):
    img[:900] = grad((40, 20, 15), (80, 60, 50), 0, 900); img[900:] = grad((200, 190, 180), (240, 235, 230), 900, H)
    ell(img, (W / 2, 1300), 420, 140, mix((120, 80, 40), (250, 230, 200), ramp(t, 0.5, 2.0)))
    for i in range(8):
        a = i / 8 * 6.28; line(img, (W / 2, 1300), (W / 2 + 380 * math.cos(a) * ramp(t, 1, 2), 1300 + 120 * math.sin(a) * ramp(t, 1, 2)), (255, 255, 255), 4)
    snow(img, t, 0.7); hud(img, 'AVERAGE TEMPERATURE', tempf(counter(t, 0.2, d - 0.3, 23, -2)), 'WEEK 1', (255, 230, 200))
def plant(img, x, y, s, droop, dead):
    c = mix((60, 160, 70), (40, 80, 110), dead)
    line(img, (x, y), (x + 60 * droop * s, y - 200 * s + 80 * droop * s), c, 12 * s)
    for sx in (-1, 1): ell(img, (x + sx * 50 * s + 50 * droop * s, y - 140 * s + 70 * droop * s), 46 * s, 18 * s, c, rot=sx * (30 + 60 * droop))
def c8(img, t, d):
    img[:] = grad((30, 20, 15), (60, 45, 40)); img[1300:] = (40, 50, 60)
    k = ramp(t, 0.4, d)
    for i in range(7): plant(img, 120 + i * 140, 1300, 1.2, k, k)
    v = int(100 * (1 - ramp(t, 0.2, 0.6))); hud(img, 'PHOTOSYNTHESIS', f'{v}%', 'NO LIGHT = NO FOOD', RED if v < 50 else GREEN)
def c9(img, t, d):
    img[:] = grad((30, 20, 15), (70, 55, 50)); img[1400:] = (230, 230, 235); snow(img, t, 0.6)
    rrect(img, W / 2 - 70, 700, 140, 720, 30, (40, 60, 90))
    for (dx, dy, r) in ((0, 560, 300), (-220, 720, 220), (220, 720, 220), (0, 420, 220)): circ(img, (W / 2 + dx, dy), r * back(ramp(t, 0.1, 0.5)), (50, 90, 50))
    k = back(ramp(t, 1.0, 1.3)); pill(img, W / 2, 1560, 'STILL ALIVE: DECADES', 50, INK, GREEN, dot=GREEN, alpha=min(1, k))
def c10(img, t, d):
    img[:] = (14, 12, 12)
    rrect(img, 290, 300, 500, 1000, 50, (40, 40, 44)); rrect(img, 306, 316, 468, 968, 40, (2, 2, 2))
    text(img, 'still waiting', W / 2, 1180, 40, WHITE, INTER_M); text(img, '#goldenhour', W / 2, 1230, 34, (200, 160, 80), INTER_M)
    emoji(img, '👁️', W / 2 - 60, 1360, 60); text(img, '0', W / 2 + 30, 1360, 64, RED, INTER_B)
    emoji(img, '🥶', 820, 340, 120 * back(ramp(t, 1.2, 1.5)))
    pill(img, W / 2, 230, 'DAY 9', 50, INK, WHITE, dot=RED)
def c10b(img, t, d):
    img[:] = (4, 3, 3); stars(img, t, 0.5); img[1500:] = (30, 30, 34)
    z = 1 + 0.6 * ease(ramp(t, 0, d)); ringlight(img, W / 2, 1500, 1.4 * z, 1.0 + 0.3 * math.sin(t * 6))
    glow(img, W / 2, 1500 - 840 * z, int(600 * z), (160, 190, 220), 1.2)
    Cn.person(img, 300, 1520, 1.3, GREG[0], GREG[1], arms_up=0.9)
    k = back(ramp(t, 1.0, 1.3)); pill(img, W / 2, 300, 'BRIGHTEST LIGHT ON EARTH', 44, INK, YEL, dot=YEL, alpha=min(1, k))
def c11(img, t, d):
    img[:] = (6, 4, 4); stars(img, t, 0.9)
    r = 330; earth(img, W / 2, 800, r, t); k = ramp(t, 0.2, 1.6)
    ov = img.copy(); circ(ov, (W / 2, 800), r, (245, 240, 235)); img[:] = cv2.addWeighted(img, 1 - 0.85 * k, ov, 0.85 * k, 0)
    hud(img, 'AVERAGE TEMPERATURE', tempf(counter(t, 0.1, 1.6, -2, -100)), 'YEAR 1', (255, 200, 150))
def c12(img, t, d):
    img[:600] = grad((20, 10, 5), (40, 30, 25), 0, 600)
    img[600:] = grad((120, 60, 20), (40, 15, 5), 600, H)
    ih = int(160 * ease(ramp(t, 0.2, 1.4))); img[600:600 + ih] = (250, 240, 230)
    for i in range(10):
        x = (i * 130 + t * 60) % W; circ(img, (x, 1200 + 200 * math.sin(i + t)), 8, (200, 140, 60))
    if t > 1.4: text(img, 'ICE BLANKET', W / 2, 600 + ih / 2, 54, INK, INTER_B)
    if dsub(t, 1.6): text(img, 'LIQUID WATER', W / 2, 1050, 70, (230, 200, 120), INTER_B, alpha=ramp(t, 1.6, 2.0))
def dsub(t, a): return t > a
def c13(img, t, d):
    img[:] = grad((40, 15, 10), (20, 8, 5)); img[1250:] = (40, 30, 30)
    poly(img, [(200, 1250), (540, 650), (880, 1250)], (60, 60, 70)); glow(img, 540, 660, 300, (40, 120, 255), 1.0 + 0.3 * math.sin(t * 4))
    for i in range(6):
        x = 150 + i * 160; rrect(img, x, 1150, 110, 100, 6, (90, 80, 70)); poly(img, [(x - 10, 1150), (x + 55, 1090), (x + 120, 1150)], (60, 50, 50))
        rrect(img, x + 35, 1180, 40, 40, 4, (120, 220, 255) if i < 6 * ramp(t, 0.5, 1.5) else (30, 30, 30))
    snow(img, t, 0.6); hud(img, 'HOMES WITH VOLCANIC HEAT', '~9 IN 10', 'ICELAND', YEL)
def c14(img, t, d):
    img[:] = grad((70, 30, 10), (20, 6, 2))
    x = W / 2 + 40 * math.sin(t); y = 900
    ell(img, (x, y), 330, 110, (60, 150, 200)); rrect(img, x - 60, y - 190, 150, 110, 30, (60, 150, 200))
    for i in range(3): circ(img, (x - 160 + i * 110, y), 30, (200, 240, 255))
    glow(img, x + 360, y, 260, (150, 220, 255), 0.7); poly(img, [(x + 320, y), (x + 900, y - 220), (x + 900, y + 220)], (90, 70, 40))
    hud(img, 'DEPTH', f'{int(counter(t, 0, d, 200, 1500))} M', 'WARMEST WATER', (230, 230, 255))
def c15(img, t, d):
    img[:] = grad((40, 15, 5), (10, 4, 2)); img[1400:] = (20, 20, 25)
    poly(img, [(420, 1400), (500, 1000), (580, 1000), (660, 1400)], (40, 40, 45))
    rb = random.Random(5)
    for i in range(40):
        u = (rb.random() + t * 0.3) % 1; circ(img, (540 + rb.uniform(-80, 80) * (1 + u * 2), 1000 - u * 700), 30 + 60 * u, (60, 60, 70))
    for i in range(30):
        x = rb.uniform(300, 780); y = rb.uniform(1100, 1450); circ(img, (x, y), 7, (180, 255, 140)); glow(img, x, y, 30, (60, 160, 60), 0.5 + 0.5 * math.sin(t * 5 + i))
    k = back(ramp(t, 1.5, 1.8)); emoji(img, '😎', 760, 1000, 110 * k)
    hud(img, 'SUN NEEDED', '0%', 'CHEMOSYNTHESIS', GREEN)
def c16(img, t, d):
    img[:] = grad((40, 15, 10), (10, 5, 3)); stars(img, t, 0.6)
    for i, (lab, ch, col) in enumerate((('ICELAND', '🌋', YEL), ('SUBMARINE', '🌊', (255, 170, 60)))):
        k = back(ramp(t, 0.1 + i * 0.25, 0.4 + i * 0.25)); x = 270 + i * 540
        rrect(img, x - 200 * k, 520, 400 * k, 560, 40, col)
        if k > 0.8: rrect(img, x - 190, 530, 380, 540, 34, INK); emoji(img, ch, x, 720, 200); text(img, lab, x, 950, 64, col, ANT)
    text(img, 'VS', W / 2, 800, 90, WHITE, ANT, alpha=ramp(t, 0.5, 0.7))
    text(img, 'COMMENT YOUR PICK 👇'.replace(' 👇', ''), W / 2, 1150, 56, WHITE, INTER_B, alpha=ramp(t, 0.8, 1.1), scale=1 + 0.04 * math.sin(t * 8))

NOZOOM = (c16,)
def timeline(ls, dur):
    fs = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c10b, c11, c12, c12, c13, c14, c15, c16]
    tl = [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
    tl = [x for i, x in enumerate(tl) if i != 13]   # c12 spans lines 12-13
    for a, f in tl: ST[f] = a
    return tl
def SFX(ls, dur):
    return {'hook_end': ls(1), 'boom': [ls(2) + 0.3, ls(11) + 0.1], 'whoosh': [ls(3) + 0.2, ls(14)], 'pop': [ls(5) + 0.3, ls(9) + 1.2, ls(10) + 1.0, ls(16) + 1.5],
            'heart': [(ls(11), ls(13))], 'ding': [ls(8) + 1.0, ls(14) + 0.6], 'riser': [ls(16)], 'end': ls(17) - 0.05}

POST = {
 'title': "The Sun Vanished: Day 1 To Year 1 ☀️ Part 2 #shorts",
 'caption': "Part 2: the Sun is gone. Day 1: −36 °F. Week 1: below zero. Year 1: −100 °F... but the oceans never freeze solid. And Golden Hour Greg is still waiting 🥶 Where would you survive: Iceland or a submarine? 👇",
 'tags': '#whatif #space #science #sun #survival #animation #part2',
 'source': 'Sources: Live Science "What would happen to Earth if the sun suddenly vanished?" (8 min 20 s light delay, ~20 °C/36 °F drop on day 1, chemosynthetic vent microbes); Popular Science "If the Sun went out, how long could life on Earth survive?" (below 0 °F in a week, −100 °F after a year, oceans insulated by ice, trees for decades, Iceland geothermal, submarines); Iceland geothermal space heating ~90% of homes (Orkustofnun / Wikipedia "Geothermal power in Iceland").',
}
