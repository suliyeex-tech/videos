import math, random, os, importlib.util
import cv2
from kit import *

# reuse Omar + the Morecambe Bay flats from Part 1
_sp = importlib.util.spec_from_file_location('qs1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'e05_quicksand.py'))
_q = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_q)
flats, sunk, OMAR, SAND, WET, carshape = _q.flats, _q.sunk, _q.OMAR, _q.SAND, _q.WET, _q.carshape

FORMAT = 'cartoon'
SLUG = '2026-11-14-quicksand-part2-tide'
TITLE = 'STUCK IN QUICKSAND'; INFO = 'MORECAMBE BAY · 16:41'
VOICE = 'guy'; SPEED = 1.22; CAPTION = 'karaoke'; TICKS = True; ZOOM = 1.2
MOOD = {'style': 'tension', 'root': 58.27, 'bpm': 108}
LINES = [
 ("Part two. Omar is stuck in quicksand, and the tide is coming in.", 0.15),
 ("Last time he learned the rule: lean back and spread out. But he's still waist deep.", 0.15),
 ("And in Morecambe Bay, the tide can come in faster than you can run.", 0.2),
 ("Then he hears a voice. It's his best friend, Sienna Sunscreen. Beach influencer.", 0.1),
 ("She sprints across the sand to save him.", 0.25),
 ("Stupid mistake.", 0.35),
 ("Rescuers say it again and again: never walk out to someone who's stuck. Now there are two people stuck.", 0.15),
 ("And Sienna does the second worst thing. She grabs Omar's arms, and pulls.", 0.15),
 ("Remember: freeing one foot can take the force needed to lift a car. Yanking can hurt him long before the sand lets go.", 0.2),
 ("Rule number two: call nine nine nine, and ask for the Coastguard. Phone up high, not in the sand.", 0.15),
 ("Then lie back, stay calm, and move slowly.", 0.2),
 ("Here's how the pros get you out. They don't pull. They add water.", 0.15),
 ("A rescuer pushes a water lance into the sand around your legs. The packed sand turns back into liquid, and your leg slides free.", 0.15),
 ("And in Morecambe, the lifeboat crew has a hovercraft, because boats can't cross the mud.", 0.15),
 ("Meanwhile, Sienna's livestream hits forty thousand viewers. Her best stream ever.", 0.15),
 ("Both of them get out with minutes to spare.", 0.25),
 ("So who would you call first: the Coastguard, or your followers?", 1.0),
]
CAPS = [
 ["[PART TWO.]", "OMAR IS STUCK", "IN {QUICKSAND,}", "AND THE {TIDE}", "IS COMING IN."],
 ["THE RULE:", "[LEAN BACK]", "AND [SPREAD OUT.]", "BUT HE'S STILL", "{WAIST DEEP.}"],
 ["IN [MORECAMBE BAY,]", "THE TIDE CAN COME IN", "{FASTER THAN}", "{YOU CAN RUN.}"],
 ["THEN HE HEARS", "A VOICE.", "BEST FRIEND", "[SIENNA SUNSCREEN.]", "BEACH INFLUENCER."],
 ["SHE {SPRINTS}", "ACROSS THE SAND", "TO SAVE HIM."], ["!STUPID MISTAKE."],
 ["RESCUERS SAY:", "{NEVER WALK OUT}", "TO SOMEONE", "WHO'S STUCK.", "NOW THERE ARE", "[TWO PEOPLE STUCK.]"],
 ["THE SECOND", "{WORST THING:}", "SHE GRABS", "OMAR'S ARMS", "AND {PULLS.}"],
 ["FREEING ONE FOOT", "CAN TAKE THE FORCE", "TO [LIFT A CAR.]", "{YANKING} CAN", "{HURT HIM}", "FIRST."],
 ["RULE #2:", "CALL [999]", "ASK FOR THE", "[COASTGUARD.]", "PHONE {UP HIGH,}", "NOT IN THE SAND."],
 ["[LIE BACK,]", "STAY CALM,", "MOVE [SLOWLY.]"],
 ["THE PROS", "{DON'T PULL.}", "THEY [ADD WATER.]"],
 ["A [WATER LANCE]", "GOES INTO", "THE SAND.", "PACKED SAND TURNS", "BACK INTO [LIQUID,]", "AND THE LEG", "[SLIDES FREE.]"],
 ["THE LIFEBOAT CREW", "HAS A [HOVERCRAFT,]", "BECAUSE BOATS", "{CAN'T CROSS}", "THE MUD."],
 ["SIENNA'S LIVESTREAM:", "[40,000 VIEWERS.]", "HER {BEST STREAM EVER.}"],
 ["BOTH GET OUT", "WITH [MINUTES]", "TO SPARE."],
 ["WHO WOULD YOU", "CALL FIRST?", "[COASTGUARD]", "OR {FOLLOWERS?}"]]
SIENNA = Look(skin=SKINS[3], hair=(60, 160, 230), style='long', shirt=(150, 90, 230), pants=(200, 160, 60), shoes=(240, 240, 240), extra='vest')
SURF = 1250

def head2(img, a=1.0):
    if a <= 0.02: return
    w = twidth(TITLE, 54) + 70
    rrect(img, W / 2 - w / 2, 150 - (1 - a) * 200, w, 78, 10, RED); text(img, TITLE, W / 2, 191 - (1 - a) * 200, 54)
    w1 = twidth('PART 2', 50) + 55; w2 = twidth(INFO, 40) + 44 + 28; gap = 24; x0 = W / 2 - (w1 + gap + w2) / 2
    pill(img, x0 + w1 / 2, 280, 'PART 2', 50, RED, WHITE, border=INK, alpha=a); pill(img, x0 + w1 + gap + w2 / 2, 280, INFO, 40, INK, WHITE, dot=YEL, alpha=a)
def tidebar(img, k, y=420):
    rrect(img, 140, y, 800, 44, 22, INK); rrect(img, 146, y + 6, 788 * clamp(k), 32, 16, (200, 140, 60))
    text(img, f'TIDE {int(100 * clamp(k))}%', W / 2, y + 23, 34, WHITE)
def phone_live(img, x, y, s, viewers, t):
    rrect(img, x - 90 * s, y - 160 * s, 180 * s, 320 * s, 24 * s, INK); rrect(img, x - 80 * s, y - 145 * s, 160 * s, 290 * s, 16 * s, (90, 60, 50))
    rrect(img, x - 70 * s, y - 135 * s, 70 * s, 34 * s, 8 * s, RED); text(img, 'LIVE', x - 35 * s, y - 118 * s, 26 * s, WHITE)
    text(img, f'{viewers:,}', x + 30 * s, y + 100 * s, 36 * s, YEL, ANT)
    for k in range(3):
        u = (t * 0.9 + k / 3) % 1; emoji(img, '❤️', x + 60 * s, y + 60 * s - 200 * u * s, 40 * s, alpha=1 - u)

def s1(img, t, d):   # hook: waist deep + tide racing in
    flats(img, t, tide=0.12 + 0.12 * ramp(t, 0, d), dark=0.2)
    sunk(img, OMAR, W / 2, 860, 1.05, 170, 'scream', al=150 + 15 * math.sin(t * 9), ar=150 - 15 * math.sin(t * 9), top=SURF)
    flash(img, t, 0, 0.15, WHITE, 0.7); head2(img, eout(ramp(t, 0.05, 0.35)))
    k = back(ramp(t, 1.2, 1.45)); text(img, 'WAIST DEEP', W / 2, 600, 120, RED, ANT, scale=k, stroke=10, scol=INK)
def s2(img, t, d):
    rule_card(img, t, d, 'LEAN BACK', 'SPREAD OUT.', bg=lambda im, tt: flats(im, tt, tide=0.25, dark=0.2))
    rotated(img, lambda c: person(c, OMAR, W / 2, 1150, 0.8, 'worry' if False else 'shock', al=100, ar=100), (W / 2, 1320), 60)
    pill(img, W / 2, 1640, 'STILL: WAIST DEEP', 46, INK, RED, alpha=eout(ramp(t, 1.6, 1.9)))
def s3(img, t, d):   # tide vs runner race
    img[:] = grad((230, 238, 245), (205, 215, 225))
    img[1100:] = grad(SAND, WET, 1100, H)
    wx = 1000 - 900 * ease(ramp(t, 0.2, d)); img[1100:, int(max(0, wx)):] = (150, 105, 50)
    for y in range(1110, H, 70): circ(img, (wx, y + 20 * math.sin(t * 8 + y)), 30, (235, 230, 220))
    rx = 900 - 500 * ease(ramp(t, 0.2, d))
    person(img, OMAR, rx, 720 + 8 * abs(math.sin(t * 14)), 0.8, 'scream', al=60 + 50 * math.sin(t * 14), ar=60 - 50 * math.sin(t * 14))
    statbox(img, t, 'TIDE vs YOU', 'TIDE WINS', RED, y=300, at=0.4)
    fact(img, t, 'RNLI: TIDE FASTER THAN YOU CAN RUN', 1.4, y=1640, size=34)
def s4(img, t, d):
    flats(img, t, tide=0.3, dark=0.2)
    person(img, SIENNA, 300 + 30 * math.sin(t * 3), 980, 1.05, 'smile', al=20, ar=150); phone_live(img, 470, 900, 0.6, 312, t)
    namecard(img, t, 'SIENNA', 'SUNSCREEN · BEACH INFLUENCER', 720, 560, at=0.6)
    sunk(img, OMAR, 860, 1000, 0.55, 110, 'shock', al=150, ar=150, top=1230)
def s5(img, t, d):
    flats(img, t, tide=0.32, dark=0.2); streaks(img, t, 0.6, (220, 220, 220))
    x = 150 + 520 * ease(ramp(t, 0, d))
    person(img, SIENNA, x, 960 + 10 * abs(math.sin(t * 14)), 1.0, 'shock', al=120 + 50 * math.sin(t * 14), ar=120 - 50 * math.sin(t * 14))
    sunk(img, OMAR, 900, 1000, 0.55, 110, 'shock', al=150, ar=150, top=1230)
    text(img, 'I GOT YOU!!', W / 2, 520, 110, YEL, ANT, scale=back(ramp(t, 0.2, 0.45)), stroke=8, scol=INK)
def s6(img, t, d):
    img[:] = grad((40, 30, 180), (20, 10, 70)); vignette(img, 0.5)
    person(img, SIENNA, W / 2, 620, 1.5, 'scream', al=160, ar=160); flash(img, t, 0, 0.12, WHITE, 0.8)
def s7(img, t, d):
    flats(img, t, tide=0.35, dark=0.25)
    sunk(img, OMAR, 330, 900, 0.9, 150, 'shock', al=150, ar=150, top=1270)
    dep = 120 * eout(ramp(t, 0.2, 1.6)); sunk(img, SIENNA, 760, 900 - 40, 0.9, dep, 'scream', al=150, ar=150, top=1270)
    k = back(ramp(t, 2.2, 2.5)); rrect(img, W / 2 - 300 * k, 430, 600 * k, 130, 24, RED)
    if k > 0.8: text(img, 'STUCK x2', W / 2, 495, 90, WHITE, ANT)
    fact(img, t, 'COASTGUARD: NEVER GO OUT TO THEM', 1.0, y=1640, size=36)
def s8(img, t, d):
    flats(img, t, tide=0.38, dark=0.25); jx, jy = shake(t, 0.3, 2.0, 8)
    sunk(img, OMAR, 420 + jx, 860 + jy - 20 * ramp(t, 0.3, 1), 1.0, 160, 'scream', al=60, ar=40, top=1280)
    sunk(img, SIENNA, 760, 860, 1.0, 140, 'angry', al=150, ar=150, top=1280)
    line(img, (560, 920), (660, 920), SIENNA.skin, 28)
    pill(img, W / 2, 470, 'PULL!!', 100, RED, WHITE, alpha=eout(ramp(t, 0.2, 0.35)))
def s9(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    surf = 1150; img[surf:] = grad(SAND, WET, surf, H)
    for k in range(80): circ(img, ((k * 131) % W, surf + 30 + (k * 211) % 700), 6, mix(WET, INK, 0.25 + 0.2 * (k % 2)))
    rrect(img, 380, surf - 40, 70, 260, 20, OMAR.pants); rrect(img, 360, surf + 200, 110, 50, 20, OMAR.shoes)
    line(img, (415, surf - 40), (415, 700), (90, 120, 160), 8); circ(img, (600, 640), 60, GREY); line(img, (415, 640), (600, 580), (90, 120, 160), 8)
    line(img, (660, 640), (760, 900), (90, 120, 160), 8); carshape(img, 760, 990, 1.2); text(img, '=', 600, 820, 100, INK, ANT)
    statbox(img, t, 'FORCE TO FREE 1 FOOT', '~1 CAR', RED, y=300, at=0.3)
    if t > 2.6: k = back(ramp(t, 2.6, 2.9)); text(img, 'OUCH', 300, 860, 120, RED, ANT, scale=k, stroke=8, scol=INK)
def s10(img, t, d):
    rule_card(img, t, d, 'CALL 999', 'ASK: COASTGUARD', bg=lambda im, tt: flats(im, tt, tide=0.4, dark=0.25))
    up = eout(ramp(t, 0.6, 1.2)); x, y = W / 2 + 160, 1250 - 300 * up
    rrect(img, x - 50, y - 90, 100, 180, 16, INK); rrect(img, x - 42, y - 78, 84, 150, 10, (240, 200, 120)); text(img, '999', x, y, 40, INK, ANT)
    line(img, (x, y + 90), (x - 40, 1500), OMAR.skin, 30)
    if t > 1.4: emoji(img, '📞', 300, 1200, 120 * back(ramp(t, 1.4, 1.7)))
def s11(img, t, d):
    flats(img, t, tide=0.42, dark=0.25)
    rotated(img, lambda c: person(c, OMAR, 360, 1050, 0.8, 'closed', al=100, ar=100), (360, 1250), 65 + 3 * math.sin(t * 2))
    rotated(img, lambda c: person(c, SIENNA, 740, 1050, 0.8, 'closed', al=100, ar=100), (740, 1250), -65 - 3 * math.sin(t * 2))
    pill(img, W / 2, 460, 'SLOW = SAFE', 64, INK, GREEN, alpha=eout(ramp(t, 0.3, 0.6)))
def s12(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    k = back(ramp(t, 0.1, 0.35)); text(img, 'PULL', 320, 800, 140, INK, ANT, scale=k)
    if t > 0.8: line(img, (200, 720), (440, 880), RED, 30); line(img, (440, 720), (200, 880), RED, 30)
    k2 = back(ramp(t, 1.4, 1.7)); text(img, 'WATER', 760, 800, 140, (200, 140, 40), ANT, scale=k2)
    if k2 > 0.5: emoji(img, '💧', 760, 1050, 160 * k2)
def s13(img, t, d):   # water lance cross-section
    img[:] = grad((230, 238, 245), (205, 215, 225))
    surf = 760; img[surf:] = grad(SAND, WET, surf, H)
    for k in range(120): circ(img, ((k * 131) % W, surf + 30 + (k * 211) % 1100), 7, mix(WET, INK, 0.3 + 0.2 * (k % 2)))
    liq = ease(ramp(t, 1.2, 3.2))
    if liq > 0: ell(img, (540, 1180), 260 * liq, 420 * liq, (190, 160, 100))
    for k in range(int(30 * liq)):
        a = k * 2.4; r = 200 * liq * ((k * 37) % 10) / 10; circ(img, (540 + r * math.cos(a + t), 1180 + 1.6 * r * math.sin(a + t)), 8, (240, 220, 170))
    lift = 160 * ease(ramp(t, 3.4, d))
    rrect(img, 490, 820 - lift, 100, 520, 30, OMAR.pants); rrect(img, 470, 1320 - lift, 150, 70, 26, OMAR.shoes)
    lx = 760; ly = 560 + 500 * eout(ramp(t, 0.2, 1.0)); line(img, (lx + 120, 560), (lx, ly), (50, 60, 70), 18)
    line(img, (lx + 120, 560), (lx + 300, 420), (60, 60, 200), 22)
    if t > 1.0:
        for k in range(10): circ(img, (lx - 30 * k, ly + 20 * math.sin(t * 20 + k)), 10, (230, 200, 120))
    statbox(img, t, 'RESCUE TOOL', 'WATER LANCE', YEL, y=300, at=0.3)
    if lift > 60: pill(img, W / 2, 1700, 'SLIDES FREE', 60, INK, GREEN)
def hover(img, x, y, s):
    ell(img, (x, y + 40 * s), 260 * s, 50 * s, (40, 40, 40)); rrect(img, x - 220 * s, y - 70 * s, 440 * s, 110 * s, 30 * s, (40, 110, 240))
    rrect(img, x - 120 * s, y - 150 * s, 240 * s, 90 * s, 20 * s, (230, 230, 235)); text(img, 'RESCUE', x, y - 15 * s, 60 * s, WHITE, ANT)
    circ(img, (x + 180 * s, y - 150 * s), 70 * s, (90, 90, 95), 6)
def s14(img, t, d):
    flats(img, t, tide=0.45, dark=0.25)
    x = 1300 - 700 * eout(ramp(t, 0, 2.0)); hover(img, x, 1100 + 6 * math.sin(t * 9), 1.0)
    for k in range(6): circ(img, (x + 240 + k * 50, 1150 + 10 * math.sin(t * 10 + k)), 20 - k * 2, (235, 230, 220))
    statbox(img, t, 'BOATS?', "CAN'T REACH", RED, y=300, at=0.3)
    fact(img, t, 'RNLI MORECAMBE RUNS A HOVERCRAFT', 1.8, y=1640, size=36)
def s15(img, t, d):
    img[:] = grad((40, 30, 30), (20, 15, 15))
    v = int(counter(t, 0.2, d - 0.5, 312, 40000)); phone_live(img, W / 2, 900, 2.2, v, t)
    text(img, 'BEST STREAM EVER', W / 2, 360, 90, YEL, ANT, scale=back(ramp(t, 1.5, 1.8)), stroke=8, scol=INK)
def s16(img, t, d):
    flats(img, t, tide=0.55, dark=0.2); hover(img, 760, 1150, 0.8)
    person(img, OMAR, 300, 930, 0.9, 'smile', al=150, ar=20, wet=True); person(img, SIENNA, 480, 930, 0.9, 'smile', al=20, ar=150, wet=True)
    pill(img, W / 2, 460, 'BOTH SAFE', 70, INK, GREEN, alpha=eout(ramp(t, 0.3, 0.6)))
    if t > 0.6: emoji(img, '🎉', 860, 700, 140 * back(ramp(t, 0.6, 0.9)))
def s17(img, t, d):
    img[:] = grad((30, 12, 8), (70, 40, 28)); stars(img, t, 0.8, ymax=1200, base=(30, 12, 8))
    k = back(ramp(t, 0, 0.3))
    text(img, 'WHO DO YOU CALL?', W / 2, 420, 110, WHITE, ANT, scale=0.6 + 0.4 * k, stroke=8, scol=INK)
    for i, (lab, col) in enumerate((('A  COASTGUARD', GREEN), ('B  FOLLOWERS', RED))):
        q = back(ramp(t, 0.4 + i * 0.3, 0.7 + i * 0.3)); y = 640 + i * 190
        if q > 0: rrect(img, W / 2 - 380 * q, y, 760 * q, 140, 30, col); text(img, lab, W / 2, y + 70, 80, WHITE, ANT, scale=q)
    pill(img, W / 2, 1060, 'COMMENT A OR B', 54, INK, YEL, alpha=eout(ramp(t, 1.2, 1.5)))
    person(img, OMAR, 380, 1540, 0.45, 'smile', al=150, ar=20); person(img, SIENNA, 700, 1540, 0.45, 'smile', al=20, ar=150)

NOZOOM = (s6, s9, s13, s17, s15)
def timeline(ls, dur):
    fs = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17]
    return [(0 if i == 0 else ls(i) - 0.08, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'boom': [ls(0) + 0.05, ls(6) + 2.2], 'whoosh': [ls(2), ls(4), ls(13)], 'mistake': ls(5),
            'heart': [(ls(7), ls(9))], 'ding': [ls(9) + 1.4, ls(15)], 'splash': [ls(12) + 1.2], 'notif': [ls(14) + k * 0.4 for k in range(8)],
            'pop': [ls(11) + 0.1, ls(11) + 1.4], 'end': ls(16) - 0.05}

POST = {
 'title': "Stuck In Quicksand As The Tide Comes In 🌊 Part 2 #shorts",
 'caption': "Part 2: Omar is waist deep in Morecambe Bay quicksand, the tide is racing in, and his influencer best friend Sienna Sunscreen makes it so much worse 😭 Who would you call first: A) the Coastguard or B) your followers? 👇",
 'tags': '#quicksand #survival #part2 #storytime #animation #whatwouldyoudo',
 'source': "Sources: RNLI / HM Coastguard Morecambe Bay safety advice (tide faster than you can run; call 999 and ask for the Coastguard; don't go out to someone stuck); fire & rescue mud rescue (water lances); Khaldoun et al., Nature 2005 (force to free a foot). Original fiction.",
}
