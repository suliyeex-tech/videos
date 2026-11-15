import math, random
from kit import *
from vote import *

FORMAT = 'vote'
SLUG = '2026-11-15-you-decide-doug-day1'
VOICE = 'story'; SPEED = 1.3; CAPTION = 'sub'; ZOOM = 0.6; VIGNETTE = 0.25; SUB_Y = 1700
MOOD = {'style': 'funny', 'root': 60.0}
PROGRESS_COL = VYEL
LINES = [
 ("This is Doug Dashboard. He has failed his driving test six times.", 0.3),
 ("He has thirty days to pass. Or he rides his little sister's pink scooter to work. Forever.", 0.35),
 ("And you decide everything he does. Day one.", 0.45),
 ("Doug's room. Four energy drinks. One driving manual. Never opened.", 0.3),
 ("The cat has read more of it than Doug.", 0.3),
 ("Doug says he learns by doing. He has done nothing.", 0.45),
 ("Test one: he drove onto the sidewalk. Test two: he reversed into the examiner's car.", 0.3),
 ("Test three: he honked at a pigeon for four minutes. Tests four to six? We don't talk about those.", 0.45),
 ("Today, Mom lends him her car. He adjusts the mirrors for twenty minutes.", 0.3),
 ("Perfect. Now he can see himself.", 0.45),
 ("Engine on. Seat belt on. Hands at ten and two. He is ready.", 0.3),
 ("He takes a deep breath. Slams the gas. The engine roars.", 0.3),
 ("The car is still in park.", 0.45),
 ("Then Pickles the cat walks behind the car. Doug screams. Pickles yawns.", 0.35),
 ("Distance driven today: zero meters. But the mirrors look amazing.", 0.35),
 ("Mom takes her keys back. Slowly. Like you take scissors from a toddler.", 0.4),
 ("Chance Doug passes: one percent. Okay, two. For effort.", 0.35),
 ("Twenty-nine days left. You decide!", 0.3),
 ("A: Grandma Gertrude teaches him. She drove a school bus for forty years. B: He watches driving videos all night, and takes the test tomorrow.", 0.3),
 ("Comment A or B. Tomorrow, on day two, we'll see what happens.", 0.8),
]
CAPS = [[ln[0]] for ln in LINES]

DOUG = Look(skin=SKINS[0], hair=(40, 70, 120), style='short', shirt=(90, 140, 60), pants=(110, 70, 40), shoes=(40, 40, 50), extra='hoodie')
PINK = (180, 110, 245); GLS = (40, 30, 30)
MOM_CAR = (70, 70, 210)

def doug(img, t, x=540, y=760, s=1.5, expr='smile', gross=0.0, helmet=None, **kw):
    return hero(img, t, DOUG, x, y, s, expr, gross=gross, helmet=helmet, glasses=GLS, **kw)
def scooter(img, x, y, s=1.0):
    line(img, (x - 260 * s, y), (x + 200 * s, y), PINK, 34 * s); line(img, (x + 200 * s, y), (x + 240 * s, y - 380 * s), PINK, 20 * s)
    line(img, (x + 170 * s, y - 380 * s), (x + 310 * s, y - 380 * s), (60, 60, 60), 18 * s)
    for wx in (-230, 210): circ(img, (x + wx * s, y + 40 * s), 46 * s, (60, 60, 70)); circ(img, (x + wx * s, y + 40 * s), 20 * s, WHITE)
    for i, c in enumerate(((255, 255, 255), (120, 240, 255), PINK)): line(img, (x + 300 * s, y - 380 * s), (x + 360 * s + 20 * i, y - 330 * s + 30 * i), c, 6 * s)   # streamers
    emoji(img, '🦄', x - 20 * s, y - 40 * s, 70 * s)

# ---- shots ----
def s0(img, t, d):   # HOOK: worst state, close-up, helmet, flies, scooter
    street(img, t)
    z = 1.0 + 0.1 * (1 - eout(ramp(t, 0, 0.6)))
    scooter(img, 540, 1560, 1.25 * z)
    doug(img, t, 520, 820, 2.0 * z, 'worry', gross=0.7, helmet=PINK, al=40, ar=-40, sweat=True)
    if t < ls1: stat_card(img, t, 'DRIVING TESTS FAILED', '6', VORANGE, 0.15, icon='🚗')
    else: stat_card(img, t, 'DAYS LEFT', '30', VYEL, ls1 + 0.05, icon='📅')
    if t > ls1 + 3.0: emoji(img, '😭', 820, 560, 110 * back(ramp(t, ls1 + 3.0, ls1 + 3.3)))
def s1(img, t, d):
    bedroom(img, t); doug(img, t, 540, 820, 1.6, 'smile', gross=0.4, ar=-150)
    for i, ic in enumerate(('💬', '🅰️', '🅱️')):
        emoji(img, ic, 260 + i * 280, 470, 110 * back(ramp(t, 0.3 + 0.25 * i, 0.55 + 0.25 * i)))
    day_stamp(img, t, 1, d - 1.1)
def s2(img, t, d):
    bedroom(img, t); doug(img, t, 600, 800, 1.4, 'flat', gross=0.4)
    for i in range(4): emoji(img, '🥤', 120 + i * 70, 1050, 70 * back(ramp(t, 0.6 + 0.15 * i, 0.8 + 0.15 * i)))
    if t < 2.3: stat_card(img, t, 'ENERGY DRINKS', str(min(4, max(0, int((t - 0.6) / 0.15) + 1))), VGREEN, 0.5, icon='🥤')
    else:
        stat_card(img, t, 'MANUAL PAGES READ', '0', VORANGE, 2.3, icon='📕')
        k = back(ramp(t, 2.4, 2.7)); rrect(img, 380 - 70 * k, 1180, 140 * k, 100, 8, (40, 40, 200))
        if k > 0.8: text(img, 'NEW', 380, 1230, 40, WHITE, ANT)
def s3(img, t, d):
    bedroom(img, t, cat=False); doug(img, t, 720, 800, 1.3, 'shock')
    rrect(img, 190, 1050, 200, 40, 6, (40, 40, 200)); pet_cat(img, t, 300, 1020, 0.9)
    emoji(img, '👓', 360, 975, 60)
    stat_card(img, t, 'PAGES READ · CAT', '212', VPINK, 0.3, icon='🐈')
def flash_back(img, k=0.25): tint(img, (90, 150, 190), k)
def s4(img, t, d):   # tests 1 and 2
    street(img, t); flash_back(img)
    if t < 2.4:
        stat_card(img, t, 'TEST #1', 'FAIL', VORANGE, 0.1, icon='❌')
        car(img, 520, 1330, 1.0, (160, 160, 165))
        x = 520 + 0 * t
        rotated(img, lambda c: car(c, 560, 1290, 1.0, (60, 160, 230)), (560, 1290), 8 * ease(ramp(t, 0.6, 1.2)))
        if t > 1.2: emoji(img, '🚶', 900, 1150, 140); emoji(img, '😱', 900, 1000, 80)
    else:
        stat_card(img, t, 'TEST #2', 'FAIL', VORANGE, 2.4, icon='❌')
        car(img, 760, 1520, 0.9, (150, 150, 150)); text(img, 'EXAMINER', 760, 1380, 44, INK, ANT)
        xx = 200 + 300 * ease(ramp(t, 2.6, 3.4)); car(img, xx, 1500, 0.9, (60, 160, 230))
        if t > 3.4: emoji(img, '💥', 560, 1380, 200 * back(ramp(t, 3.4, 3.6)))
def s5(img, t, d):   # test 3 pigeon + classified
    street(img, t); flash_back(img)
    car(img, 380, 1500, 1.0, (60, 160, 230)); emoji(img, '🐦', 860, 1420, 120)
    for i in range(int(min(6, max(0, t - 0.4) * 4))):
        text(img, 'HONK', 700 + 30 * math.sin(i), 1220 - i * 70, 60, VYEL, ANT, alpha=0.9)
    if t < 2.6: stat_card(img, t, 'HONKING AT PIGEON', f'{int(counter(t, 0.6, 2.4, 0, 4))} MIN', VYEL, 0.2, icon='📯')
    else:
        stat_card(img, t, 'TESTS #4 – #6', '???', VORANGE, 2.6, icon='🤐')
        k = back(ramp(t, 3.0, 3.3)); rotated(img, lambda c: (rrect(c, 170, 760, 740, 170, 18, (40, 40, 200)), text(c, 'CLASSIFIED', 540, 845, 120, WHITE, ANT)), (540, 845), -10, k)
def driveway(img, t, lights=False, gear='P'):
    street(img, t)
    car(img, 540, 1520, 1.25, MOM_CAR, lights)
def doug_in_car(img, t, expr='smile', x=470, y=1215, s=0.55):
    person(img, DOUG, x, y + 3 * math.sin(t * 4), s, expr, body=False, blink=(t % 3.1) < 0.1)
    for sx in (-1, 1): circ(img, (x + sx * 34 * s, y - 2 * s), 27 * s, GLS, 3)
def s6(img, t, d):   # mirrors
    driveway(img, t); doug_in_car(img, t, 'determined')
    emoji(img, '👩', 880, 1100, 140); text(img, 'MOM', 880, 1210, 44, INK, ANT)
    stat_card(img, t, 'MIRROR TIME', f'{int(counter(t, 0.8, 3.5, 0, 20))} MIN', VBLUE, 0.3, icon='🪞')
def s7(img, t, d):   # sees himself
    img[:] = grad((60, 40, 40), (30, 20, 20))
    k = back(ramp(t, 0.05, 0.35))
    rrect(img, 540 - 420 * k, 520, 840 * k, 420, 120, (30, 30, 30)); rrect(img, 540 - 400 * k, 540, 800 * k, 380, 110, (200, 190, 170))
    if k > 0.8: person(img, DOUG, 540, 760, 1.4, 'smile', body=False); [circ(img, (540 + sx * 48, 757), 38, GLS, 6) for sx in (-1, 1)]
    if t > 0.9: emoji(img, '✨', 820, 600, 100 * back(ramp(t, 0.9, 1.2))); emoji(img, '✨', 280, 860, 80 * back(ramp(t, 1.1, 1.4)))
    stat_card(img, t, 'CAN SEE THE ROAD', 'NO', VORANGE, 0.9, icon='🛣️')
def s8(img, t, d):   # checklist
    driveway(img, t, lights=t > 0.4); doug_in_car(img, t, 'determined')
    for i, (lab, at) in enumerate((('ENGINE ON', 0.2), ('SEAT BELT', 0.9), ('10 & 2', 1.7))):
        k = back(ramp(t, at, at + 0.25))
        if k > 0: rrect(img, 120, 520 + i * 120, 560 * k, 100, 24, CARD); text(img, lab, 120 + 280 * k, 570 + i * 120, 56, WHITE, POP, alpha=min(1, k)); emoji(img, '✅', 740, 570 + i * 120, 80 * k)
    stat_card(img, t, 'READY', f'{int(counter(t, 0.2, 2.6, 0, 100))}%', VGREEN, 0.1, icon='🏁')
def s9(img, t, d):   # still in park
    driveway(img, t, lights=True); doug_in_car(img, t, 'smile')
    k = back(ramp(t, 0.15, 0.4)); circ(img, (540, 820), 170 * k, (40, 40, 220)); circ(img, (540, 820), 150 * k, WHITE)
    if k > 0.8: text(img, 'P', 540, 830, 220, (40, 40, 220), ANT)
    stat_card(img, t, 'GEAR', 'PARK', VORANGE, 0.1, icon='🅿️')
def s10(img, t, d):   # cat behind the car
    driveway(img, t, lights=True)
    cx = 1250 - 500 * ease(ramp(t, 0.0, 1.6)); pet_cat(img, t, cx, 1560, 0.9, awake=True)
    scream = t > 1.6
    doug_in_car(img, t, 'scream' if scream else 'smile', s=0.55 if not scream else 0.62)
    if scream:
        stat_card(img, t, 'HEART RATE', f'{int(counter(t, 1.6, 2.4, 80, 180))} BPM', VORANGE, 1.6, icon='💓')
        for i in range(3): text(img, 'AAAA', 300 + 20 * math.sin(t * 30 + i), 1000 - i * 80, 70 - i * 10, WHITE, ANT, stroke=6, scol=INK)
    else: stat_card(img, t, 'PICKLES', 'INCOMING', VPINK, 0.2, icon='🐈')
    if t > 3.3: emoji(img, '🥱', cx + 90, 1440, 80 * back(ramp(t, 3.3, 3.6)))
def s11(img, t, d):
    driveway(img, t); doug(img, t, 540, 820, 1.3, 'smile', ar=-160)
    if t > 0.1: stat_card(img, t, 'DISTANCE DRIVEN', '0 M', VORANGE, 0.1, icon='📏')
    if t > 2.0: emoji(img, '✨', 830, 1250, 100 * back(ramp(t, 2.0, 2.3))); emoji(img, '🪞', 830, 1250, 70)
def s12(img, t, d):
    bedroom(img, t); doug(img, t, 540, 760, 1.2, 'worry', gross=0.4)
    meter(img, t, 'CHANCE DOUG PASSES', 0, 1, 0.1, 1480, VORANGE) if t < 1.9 else meter(img, t, 'CHANCE DOUG PASSES', 1, 2, 1.3, 1480, VGREEN)
    stat_card(img, t, 'DAYS LEFT', '30', VYEL, 0.0, icon='📅')
def s13(img, t, d):
    if t < 1.4:
        bedroom(img, t); doug(img, t, 540, 760, 1.2, 'worry', gross=0.4)
        stat_card(img, t, 'DAYS LEFT', '29', VYEL, 0.1, icon='📅')
    else: decide(img, t, 1.4)
def s14(img, t, d):
    img[:] = grad(PURPLE, DEEP); fairy_lights(img, t, 100, 50)
    text(img, 'DAY 2 — YOU DECIDE', 540, 560, 70, VYEL, ANT)
    ab_cards(img, t, 'Grandma Gertrude|teaches him', '👵', 'Videos all night,|test tomorrow', '📱', 0.1, 680)
    k = ramp(t, 0.2, 0.6); doug(img, t, 540, 1500 + 200 * (1 - k), 0.7, 'worry')
def s15(img, t, d):
    img[:] = grad(PURPLE, DEEP); fairy_lights(img, t, 100, 50)
    ab_cards(img, t, 'Grandma Gertrude|teaches him', '👵', 'Videos all night,|test tomorrow', '📱', -1, 680)
    p = 1 + 0.05 * math.sin(t * 8)
    text(img, 'COMMENT A or B', 540, 520, 96, WHITE, ANT, scale=p * back(ramp(t, 0.1, 0.4)), stroke=8, scol=CARD)
    doug(img, t, 540, 1500, 0.7, 'smile', ar=-160); emoji(img, '👇', 820, 1500, 110 * back(ramp(t, 0.3, 0.6)))

ls1 = 4.0   # set in timeline
NOZOOM = (s7, s13, s14, s15)
def s9a(img, t, d):   # revving in park
    driveway(img, t, lights=True); dx, dy = shake(t, 1.2, 2.0, 10); doug_in_car(img, t, 'determined' if t < 1.2 else 'scream', x=470 + dx, y=1215 + dy)
    stat_card(img, t, 'ENGINE', f'{int(counter(t, 1.2, 2.4, 800, 6000)):,} RPM', VORANGE, 0.2, icon='🔥')
    if t > 1.3:
        for i in range(4): circ(img, (100 - 30 * i - 60 * ((t * 2 + i * 0.25) % 1), 1460 - 20 * i), 30 + 20 * i, (200, 200, 205))
def s11a(img, t, d):   # mom takes keys
    driveway(img, t); doug(img, t, 420, 820, 1.2, 'worry')
    emoji(img, '👩', 820, 900, 200); k = ease(ramp(t, 0.6, 2.2)); emoji(img, '🔑', 560 + 220 * k, 1050 - 60 * k, 90)
    stat_card(img, t, 'CAR KEYS', '0', VORANGE, 0.2, icon='🔑')
def timeline(ls, dur):
    global ls1
    ls1 = ls(1) - ls(0)
    sh = [s0, None, s1, s2, s3, None, s4, s5, s6, s7, s8, s9a, s9, s10, s11, s11a, s12, s13, s14, s15]
    return [((0 if i == 0 else ls(i) - 0.05), f) for i, f in enumerate(sh) if f is not None]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'boom': [ls(2) + dur(2) - 0.9, ls(11) + 1.2], 'whoosh': [ls(i) for i in (2, 3, 6, 8, 13, 16, 17, 18)],
            'pop': [ls(0) + 0.2, ls(1), ls(3) + 0.6, ls(3) + 0.75, ls(3) + 0.9, ls(3) + 1.05, ls(3) + 2.3, ls(4) + 0.3, ls(7) + 2.6, ls(8) + 0.3,
                    ls(10) + 0.2, ls(10) + 0.9, ls(10) + 1.7, ls(12) + 0.15, ls(14) + 0.1, ls(15) + 0.2, ls(18) + 0.1, ls(18) + 0.6],
            'mistake': ls(12) + 0.2, 'ding': [ls(9) + 0.9, ls(16) + 2.8, ls(19) + 0.2],
            'snap': [ls(6) + 3.0, ls(6) + 3.4], 'notif': [ls(19) + 0.4, ls(19) + 0.6], 'end': ls(19) - 0.05}

POST = {
 'title': "He Failed His Driving Test 6 Times. YOU Decide Day 2 🚗 Part 1 #shorts",
 'caption': "Doug Dashboard failed his driving test 6 times. He has 30 days to pass... or ride his little sister's pink scooter to work forever 🛴💀 YOU decide what he does next: A) Grandma Gertrude teaches him or B) driving videos all night and the test tomorrow. Comment A or B, the most-voted happens on Day 2 👇",
 'tags': '#youdecide #storytime #funny #animation #drivingtest #comedy #part1',
}
