import math, random
from kit import *

FORMAT = 'cartoon'
SLUG = '2026-11-15-internet-vanished-part2'
VOICE = 'mom'; SPEED = 1.25; CAPTION = 'karaoke'; ZOOM = 1.0; VIGNETTE = 0.3
MOOD = {'style': 'tension', 'root': 52.0}
PROGRESS_COL = (220, 120, 255)
LINES = [
 ("This is Wendy Wifi. Three days ago, the internet vanished. She has refreshed a dead page four hundred and twelve times.", 0.3),
 ("She has until midnight to get back online, or her one thousand and ninety-five day streak dies.", 0.35),
 ("Day one, she streamed to her goldfish. He left after four seconds.", 0.35),
 ("Day two, she bought a paper map. She held it upside down for an hour.", 0.3),
 ("Day three, she talked to her neighbor Gary. Out loud. With her mouth.", 0.45),
 ("Then, at 3 AM, a screen turns on.", 0.4),
 ("Not her phone. Not her laptop. Grandma's old TV, up in the attic.", 0.35),
 ("And that part is real. An antenna TV doesn't need the internet.", 0.25),
 ("The picture flies from a broadcast tower, straight through the air, at the speed of light.", 0.35),
 ("Radio too. That's why emergency kits list a battery or hand-crank radio.", 0.35),
 ("On the screen, a man in a tie reads a list. Water at the school. Cash at the bank. Bread at nine.", 0.35),
 ("Wendy's first thought: should I go live?", 0.25),
 ("Her second thought: there is no live.", 0.45),
 ("Then the man stops reading. He looks straight into the camera.", 0.4),
 ("And says: Wendy. Your chat misses you.", 0.6),
 ("How does he know her name? Part three: who's behind the screen.", 0.3),
 ("Would you climb into that attic? Comment yes or no.", 0.8),
]
CAPS = [
 ["THIS IS", "[WENDY WIFI.]", "THE INTERNET", "{VANISHED.}", "SHE REFRESHED", "A DEAD PAGE", "[412 TIMES.]"],
 ["UNTIL", "{MIDNIGHT}", "OR HER", "[1,095-DAY]", "STREAK", "{DIES.}"],
 ["DAY 1:", "SHE STREAMED", "TO HER [GOLDFISH.]", "HE LEFT", "AFTER {4 SECONDS.}"],
 ["DAY 2:", "A [PAPER MAP.]", "HELD IT", "{UPSIDE DOWN}", "FOR AN HOUR."],
 ["DAY 3:", "SHE TALKED", "TO [GARY.]", "OUT LOUD.", "{WITH HER MOUTH.}"],
 ["THEN, AT", "[3 AM,]", "A SCREEN", "{TURNS ON.}"],
 ["NOT HER PHONE.", "NOT HER LAPTOP.", "[GRANDMA'S OLD TV,]", "IN THE {ATTIC.}"],
 ["THAT PART", "IS [REAL.]", "AN ANTENNA TV", "{DOESN'T NEED}", "THE INTERNET."],
 ["THE PICTURE", "FLIES FROM", "A [BROADCAST TOWER]", "THROUGH THE AIR", "AT {LIGHT SPEED.}"],
 ["[RADIO] TOO.", "EMERGENCY KITS", "LIST A", "{BATTERY OR}", "{HAND-CRANK RADIO.}"],
 ["A MAN IN A TIE", "READS A LIST.", "[WATER:] SCHOOL.", "[CASH:] BANK.", "[BREAD:] 9 AM."],
 ["FIRST THOUGHT:", "SHOULD I", "{GO LIVE?}"],
 ["SECOND THOUGHT:", "THERE IS", "{NO LIVE.}"],
 ["THE MAN", "{STOPS READING.}", "HE LOOKS", "INTO [THE CAMERA.]"],
 ["!WENDY.", "!{YOUR CHAT}", "!{MISSES YOU.}"],
 ["HOW DOES HE", "{KNOW HER NAME?}", "[PART THREE:]", "WHO'S BEHIND", "THE SCREEN."],
 ["WOULD YOU", "CLIMB INTO", "THAT {ATTIC?}", "COMMENT", "[YES] OR [NO.]"]]

WENDY = Look(skin=SKINS[0], hair=(170, 110, 240), style='long', shirt=(150, 60, 120), pants=(70, 50, 50), shoes=(40, 40, 50), extra='hoodie')
GARY = Look(skin=SKINS[2], hair=(60, 60, 60), style='cap', shirt=(60, 130, 90), pants=(90, 70, 50))
VIO = (220, 120, 255); NAVY = (60, 28, 24)

def chip(img, t, label, value, col=YEL, at=0.0, x=W / 2, y=330, w=520):
    k = back(ramp(t, at, at + 0.25))
    if k <= 0: return
    rrect(img, x - w / 2 * k, y, w * k, 140, 24, INK); rrect(img, x - w / 2 * k, y, w * k, 140, 24, col, th=4)
    if k > 0.85: text(img, label, x, y + 38, 36, col, INTER_B); text(img, value, x, y + 98, 76, WHITE, ANT)
def dark_circles(img, hx, hy, s):
    for sx in (-1, 1): ell(img, (hx + sx * 32 * s, hy + 22 * s), 20 * s, 8 * s, (120, 90, 140), 0, 180, int(5 * s))
def wendy(img, t, x, y, s=1.0, expr='flat', tired=True, **kw):
    bob = 5 * s * math.sin(t * 3)
    person(img, WENDY, x, y + bob, s, expr, blink=(t % 2.7) < 0.15, **kw)
def flies(img, t, cx, cy, n=2, r=140):
    for i in range(n):
        a = t * (2.4 + 0.5 * i) + i * 2.5; x = cx + r * math.cos(a); y = cy + 0.6 * r * math.sin(a * 1.3)
        ell(img, (x - 6, y - 7), 8, 5, (230, 230, 230), rot=30); ell(img, (x + 6, y - 7), 8, 5, (230, 230, 230), rot=-30); circ(img, (x, y), 7, (20, 20, 20))
def room(img, t, dark=0.0):
    img[:] = grad(mix((110, 50, 70), (20, 10, 14), dark), mix((60, 28, 40), (10, 6, 8), dark))
    rrect(img, 0, 1420, W, 500, 0, mix((70, 50, 60), (14, 10, 12), dark))
    # ring light + monitor with "no connection"
    cv2.circle(img, P(880, 640), 8 * 130, mix((230, 230, 255), (40, 40, 50), dark), 8 * 18, cv2.LINE_AA, 3)
    rrect(img, 60, 900, 360, 230, 14, (30, 30, 36)); rrect(img, 72, 912, 336, 206, 8, mix((120, 60, 50), (30, 20, 20), dark))
    for r_ in (70, 45, 20): ell(img, (240, 1040), r_, r_, (200, 200, 210), 225, 315, 6)
    line(img, (170, 960), (310, 1080), RED, 9); line(img, (310, 960), (170, 1080), RED, 9)
    rrect(img, 40, 1130, 420, 26, 6, (50, 60, 90))
    for i in range(3): rrect(img, 620 + i * 18, 1470 - i * 34, 300, 30, 6, (60, 130, 200))   # pizza boxes
def goldfish(img, t, x, y, gone=0.0):
    circ(img, (x, y), 150, (230, 200, 160)); circ(img, (x, y), 150, WHITE, 4); rrect(img, x - 150, y - 160, 300, 40, 0, (0, 0, 0)) if False else None
    if gone < 1:
        fx = x - 30 + 400 * ease(gone); ell(img, (fx, y + 10), 50, 30, (60, 140, 250)); poly(img, [(fx + 40, y + 10), (fx + 90, y - 20), (fx + 90, y + 40)], (60, 140, 250))
        circ(img, (fx - 25, y), 7, INK)
def tv(img, x, y, s=1.0, on=0.0, draw=None):
    rrect(img, x - 260 * s, y - 200 * s, 520 * s, 400 * s, 40 * s, (60, 90, 120)); rrect(img, x - 220 * s, y - 165 * s, 380 * s, 330 * s, 40 * s, (30, 30, 30))
    for k in range(2): circ(img, (x + 200 * s, y - 100 * s + k * 90 * s), 24 * s, (180, 180, 190))
    line(img, (x - 40 * s, y - 200 * s), (x - 160 * s, y - 380 * s), (200, 200, 210), 6 * s); line(img, (x + 40 * s, y - 200 * s), (x + 150 * s, y - 380 * s), (200, 200, 210), 6 * s)
    rrect(img, x - 200 * s, y + 200 * s, 30 * s, 60 * s, 4, (50, 70, 90)); rrect(img, x + 170 * s, y + 200 * s, 30 * s, 60 * s, 4, (50, 70, 90))
    if on > 0:
        x0, y0, w, h = int(x - 210 * s), int(y - 155 * s), int(360 * s), int(310 * s)
        sub = img[y0:y0 + h, x0:x0 + w]
        sub[:] = (sub * (1 - on) + np.array((200, 190, 170)) * on).astype(np.uint8)
        if draw: draw(img, x0, y0, w, h)
        rng = np.random.default_rng(int(on * 1000 + x)); n = rng.integers(0, 30, (h, w, 1), dtype=np.uint8); sub[:] = np.clip(sub.astype(int) - n, 0, 255).astype(np.uint8)
        glow(img, x - 30 * s, y, int(420 * s), (120, 110, 90), 0.6 * on)
def anchor(img, x0, y0, w, h, look=0.0, mouth=0.0):
    cx = x0 + w // 2; k = min(w / 360, h / 310)
    rrect(img, x0, y0 + int(h * 0.72), w, int(h * 0.28), 0, (120, 90, 70))   # desk
    rrect(img, cx - 70 * k, y0 + int(h * 0.42), 140 * k, int(h * 0.34), 30 * k, (60, 50, 50))
    poly(img, [(cx - 10 * k, y0 + h * 0.44), (cx + 10 * k, y0 + h * 0.44), (cx + 14 * k, y0 + h * 0.66), (cx, y0 + h * 0.72), (cx - 14 * k, y0 + h * 0.66)], RED)
    hy = y0 + h * 0.3; circ(img, (cx, hy), 52 * k, (140, 185, 232)); ell(img, (cx, hy - 30 * k), 52 * k, 28 * k, (50, 50, 60), 180, 360)
    ex = 0 if look > 0.5 else -10 * k
    for sx in (-1, 1): circ(img, (cx + sx * 18 * k + ex, hy), (6 if look < 0.5 else 8) * k, INK)
    ell(img, (cx, hy + 26 * k), 14 * k, (3 + 8 * mouth) * k, INK)
def attic(img, t, light=0.0):
    img[:] = (14, 10, 12)
    poly(img, [(0, 300), (540, 60), (W, 300), (W, H), (0, H)], mix((30, 30, 40), (60, 70, 90), light))
    for x in range(-200, W + 200, 180): line(img, (540, 60), (x, H), mix((24, 22, 30), (40, 50, 60), light), 10)
    rrect(img, 0, 1500, W, 420, 0, mix((30, 26, 30), (60, 70, 90), light))
    for (x, y) in ((140, 1440), (930, 1420)): rrect(img, x - 90, y - 140, 180, 160, 8, mix((40, 60, 80), (80, 120, 160), light))

# ---- shots ----
def s1(img, t, d):   # hook: Wendy in the dark, refreshing
    room(img, t, 0.3); wendy(img, t, 560, 760, 1.6, 'worry', al=10, ar=-140, sweat=True); flies(img, t, 560, 700, 3, 220)
    rrect(img, 700, 820, 90, 160, 14, INK); glow(img, 745, 880, 120, (90, 80, 60), 0.8)
    if t > 0.1: chip(img, t, 'PAGE REFRESHES', f'{int(counter(t, 0.1, 5.0, 380, 412))}', VIO, 0.05, y=150)
    flash(img, t, 0, 0.12, WHITE, 0.6)
def s2(img, t, d):
    room(img, t, 0.3); wendy(img, t, 540, 820, 1.3, 'worry')
    chip(img, t, 'STREAK', '1,095 DAYS', YEL, 0.1, x=290, y=150, w=460); chip(img, t, 'DEADLINE', 'MIDNIGHT', RED, 0.6, x=790, y=150, w=420)
    if t > 3.0: emoji(img, '🔥', 540, 520, 130 * back(ramp(t, 3.0, 3.3)) * (1 - 0.6 * ramp(t, 4.0, 5.0)))
def s3(img, t, d):
    room(img, t, 0.2); wendy(img, t, 330, 800, 1.1, 'smile', ar=-150); goldfish(img, t, 760, 1160, ramp(t, 2.5, 3.2))
    chip(img, t, 'DAY 1 · VIEWERS', '1' if t < 2.6 else '0', VIO, 0.1, y=150)
def s4(img, t, d):
    img[:] = grad((230, 200, 160), (200, 180, 150)); rrect(img, 0, 1350, W, 570, 0, (110, 160, 120))
    wendy(img, t, 540, 820, 1.3, 'determined', tired=True, al=150, ar=-150)
    rotated(img, lambda c: (rrect(c, 290, 960, 500, 330, 10, (200, 230, 240)), line(c, (330, 1000), (750, 1250), (60, 140, 60), 8),
                            line(c, (360, 1200), (700, 1020), (200, 100, 60), 8), text(c, 'MAP', 540, 1130, 90, (40, 40, 160), ANT)), (540, 1125), 180)
    chip(img, t, 'DAY 2 · MAP', 'UPSIDE DOWN', YEL, 0.2, y=150, w=560)
def s5(img, t, d):
    img[:] = grad((230, 200, 160), (200, 180, 150)); rrect(img, 0, 1350, W, 570, 0, (110, 160, 120))
    for x in range(0, W, 70): rrect(img, x, 1150, 50, 220, 8, (200, 220, 235))
    wendy(img, t, 330, 820, 1.1, 'shock' if t < 2.5 else 'worry'); person(img, GARY, 780, 860, 1.0, 'smile', ar=-160)
    chip(img, t, 'DAY 3 · HUMANS TALKED TO', '1', YEL, 0.2, y=150, w=640)
    if t > 3.0: emoji(img, '😬', 330, 560, 100 * back(ramp(t, 3.0, 3.3)))
def s6(img, t, d):   # 3 AM, a screen turns on
    room(img, t, 0.9); wendy(img, t, 540, 900, 1.2, 'closed', tired=False)
    k = ramp(t, 1.2, 1.4); glow(img, 540, 300, 600, (120, 110, 90), 1.2 * k)
    pill(img, W / 2, 200, '3:00 AM', 60, INK, WHITE)
    if t > 1.3: wendy(img, t, 540, 900, 1.2, 'shock', tired=True)
def s7(img, t, d):
    k = ramp(t, 0.0, 1.0)
    if t < 1.8:
        room(img, t, 0.9)
        for i, (ic, x) in enumerate((('📱', 330), ('💻', 750))):
            if t > 0.2 + 0.7 * i: emoji(img, ic, x, 800, 150); line(img, (x - 90, 710), (x + 90, 890), RED, 14); line(img, (x + 90, 710), (x - 90, 890), RED, 14)
    else:
        attic(img, t, 0.4); tv(img, 540, 1050, 1.2, on=1.0, draw=lambda im, x0, y0, w, h: None)
        pill(img, W / 2, 330, "GRANDMA'S TV", 54, INK, YEL, alpha=ramp(t, 2.0, 2.3))
def s8(img, t, d):   # antenna TV needs no internet
    attic(img, t, 0.4); tv(img, 540, 1050, 1.2, on=1.0)
    k = back(ramp(t, 0.6, 0.9))
    if k > 0: rrect(img, 120, 330, 840 * k, 120, 22, INK)
    if k > 0.8: text(img, 'INTERNET NEEDED: NO', 540, 392, 66, GREEN, ANT)
def s9(img, t, d):   # tower -> waves -> house
    img[:] = grad((90, 40, 30), (40, 20, 14)); stars(img, t, 0.6, 1200, (90, 40, 30)); rrect(img, 0, 1500, W, 420, 0, (40, 50, 40))
    tx = 180
    for a, b in (((tx - 80, 1500), (tx, 700)), ((tx + 80, 1500), (tx, 700))): line(img, a, b, (180, 180, 200), 10)
    for y in range(800, 1500, 100): line(img, (tx - 80 * (y - 700) / 800, y), (tx + 80 * (y - 700) / 800, y), (180, 180, 200), 6)
    circ(img, (tx, 690), 16, RED)
    for i in range(6):
        r = ((t * 380 + i * 160) % 960)
        ell(img, (tx, 690), r, r, mix(YEL, (40, 20, 14), r / 960), -60, 60, 6)
    rrect(img, 760, 1160, 240, 340, 6, (90, 110, 150)); poly(img, [(730, 1160), (880, 1010), (1030, 1160)], (60, 70, 110))
    line(img, (880, 1010), (880, 920), (200, 200, 210), 6); line(img, (850, 900), (910, 940), (200, 200, 210), 6)
    if t > 2.0: pill(img, W / 2, 330, 'SPEED OF LIGHT · 300,000 KM/S', 46, INK, YEL, alpha=ramp(t, 2.0, 2.3))
def s10(img, t, d):
    img[:] = grad((60, 70, 90), (30, 34, 44))
    emoji(img, '📻', 540, 820, 340 * back(ramp(t, 0.1, 0.4)))
    for i, lab in enumerate(('BATTERY RADIO', 'HAND-CRANK RADIO')):
        if t > 1.8 + 0.6 * i: rrect(img, 190, 1010 + i * 115, 700, 100, 22, INK); text(img, lab, 540, 1060 + i * 115, 54, WHITE, ANT)
    chip(img, t, 'EMERGENCY KIT', 'ITEM: RADIO', GREEN, 0.3, y=330, w=560)
def news(img, x0, y0, w, h, look=0.0, mouth=0.0):
    anchor(img, x0, y0, w, h, look, mouth)
def s11(img, t, d):   # the list
    attic(img, t, 0.5)
    m = abs(math.sin(t * 9)) if t < d - 0.3 else 0
    tv(img, 540, 800, 1.5, on=1.0, draw=lambda im, x0, y0, w, h: news(im, x0, y0, w, h, 0, m))
    for i, (ic, lab, at) in enumerate((('💧', 'WATER · SCHOOL', 2.2), ('💵', 'CASH · BANK', 3.5), ('🍞', 'BREAD · 9 AM', 4.6))):
        if t > at: rrect(img, 190, 1400 + i * 115, 700, 100, 22, INK); emoji(img, ic, 260, 1450 + i * 115, 70); text(img, lab, 580, 1450 + i * 115, 54, WHITE, ANT)
def s12(img, t, d):   # go live?
    attic(img, t, 0.5); wendy(img, t, 360, 860, 1.1, 'smile' if t < ST_12 else 'worry', ar=-150)
    k = back(ramp(t, 0.3, 0.6)); x, y = 800, 900
    rrect(img, x - 140 * k, y - 260 * k, 280 * k, 520 * k, 30, INK)
    if k > 0.8:
        live = t < ST_12; col = RED if live else (90, 90, 95)
        rrect(img, x - 100, y + 120, 200, 80, 20, col); text(img, 'GO LIVE', x, y + 160, 48, WHITE, ANT)
        if not live: text(img, 'NO SIGNAL', x, y - 40, 44, (170, 170, 175), INTER_B); line(img, (x - 110, y + 110), (x + 110, y + 210), RED, 10)
ST_12 = 2.5
def s13(img, t, d):   # stops reading, looks into camera
    attic(img, t, 0.5); z = 1.5 + 0.6 * ease(ramp(t, 0.6, d))
    tv(img, 540, 900, z, on=1.0, draw=lambda im, x0, y0, w, h: news(im, x0, y0, w, h, ramp(t, 1.4, 1.6), 0))
def s14(img, t, d):   # Wendy. Your chat misses you.
    img[:] = (200, 190, 170); x0, y0, w, h = 0, 200, W, 930
    anchor(img, x0, y0, w, h, 1.0, abs(math.sin(t * 8)) if t < d - 0.6 else 0)
    rng = np.random.default_rng(int(t * 30)); n = rng.integers(0, 40, (H, W, 1), dtype=np.uint8); img[:] = np.clip(img.astype(int) - n, 0, 255).astype(np.uint8)
    img[::4] = (img[::4] * 0.85).astype(np.uint8)
    if int(t * 7) % 9 == 0: tint(img, (0, 0, 0), 0.4)
def s15(img, t, d):   # Part 3 card
    img[:] = grad((30, 12, 8), (70, 40, 28)); stars(img, t, 0.8, ymax=1200, base=(30, 12, 8)); glow(img, W / 2, 800, 620, (30, 50, 150), 0.9)
    text(img, "WHO'S BEHIND THE SCREEN?", W / 2, 770, 70, WHITE, alpha=ramp(t, 0.25, 0.5))
    q = back(ramp(t, 0.4, 0.7)); pul = 1 + 0.04 * math.sin(t * 9)
    if q > 0: rrect(img, W / 2 - 250 * q * pul, 880, 500 * q * pul, 120 * q, 60 * q, WHITE); text(img, 'FOLLOW', W / 2, 942, 84, INK, scale=q * pul)
    text(img, 'PART 3', W / 2, 560, 300, RED, ANT, scale=0.6 + 0.4 * back(ramp(t, 0, 0.3)), stroke=12, scol=INK)
    tv(img, 540, 1560, 0.8, on=1.0, draw=lambda im, x0, y0, w, h: news(im, x0, y0, w, h, 1.0, 0))
def s16(img, t, d):
    attic(img, t, 0.5); tv(img, 540, 1000, 1.1, on=1.0, draw=lambda im, x0, y0, w, h: news(im, x0, y0, w, h, 1.0, 0))
    for i, (L_, col) in enumerate((('YES', GREEN), ('NO', RED))):
        k = back(ramp(t, 0.3 + 0.3 * i, 0.6 + 0.3 * i)); x = 300 + i * 480
        if k > 0: rrect(img, x - 180 * k, 1500, 360 * k, 160, 30, col)
        if k > 0.8: text(img, L_, x, 1580, 110, WHITE, ANT)
    pill(img, W / 2, 330, 'COMMENT 👇'.replace(' 👇', ''), 70, INK, YEL, alpha=ramp(t, 0.1, 0.4))

NOZOOM = (s14, s15, s16)
def timeline(ls, dur):
    global ST_12
    fs = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, None, s13, s14, s15, s16]
    tl = [((0 if i == 0 else ls(i) - 0.05), f) for i, f in enumerate(fs) if f is not None]
    ST_12 = ls(12) - ls(11)
    return tl
def SFX(ls, dur):
    return {'hook_end': ls(1), 'whoosh': [ls(i) for i in (2, 3, 4, 6, 8, 10)], 'boom': [ls(5) + 1.2, ls(14) + 0.1],
            'pop': [ls(1) + 0.1, ls(1) + 0.6, ls(3) + 0.2, ls(4) + 0.2, ls(7) + 0.6, ls(9) + 0.3, ls(9) + 1.8, ls(9) + 2.4, ls(10) + 2.2, ls(10) + 3.5, ls(10) + 4.6],
            'mistake': ls(2) + 2.5, 'ding': [ls(7) + 0.7, ls(8) + 2.0], 'riser': [ls(13) + 1.0], 'heart': [(ls(13), ls(15))],
            'notif': [ls(16) + 0.3, ls(16) + 0.6], 'end': ls(15) - 0.05}

POST = {
 'title': "The Internet Vanished. At 3 AM, One Screen Turned On 📺 Part 2 #shorts",
 'caption': "Part 2: the internet has been gone for 3 days and streamer Wendy Wifi is NOT okay (412 refreshes). Then at 3 AM, grandma's old antenna TV turns on in the attic... and the man on screen says her name 📺😨 Would you climb into that attic? Comment YES or NO 👇",
 'tags': '#whatif #internet #storytime #animation #mystery #survival #part2',
 'source': "Over-the-air (antenna) TV and radio are broadcast from transmitter towers and don't need an internet connection; emergency kit lists (Ready.gov / FEMA and local emergency offices) recommend a battery-powered or hand-crank radio. Radio waves travel at the speed of light (~300,000 km/s). Wendy, Gary and the anchor are fictional.",
}
