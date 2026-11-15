import math, random
from kit import *
from mapzoom import *

FORMAT = 'map'
SLUG = '2026-11-15-weird-borders-part2'
VOICE = 'bro'; SPEED = 1.3; CAPTION = 'karaoke'; TICKS = False; ZOOM = 0.8; VIGNETTE = 0.3
MOOD = {'style': 'funny', 'root': 55.0}
LINES = [
 ("This is Parcel Pete. He has twenty-four hours to deliver five packages to the weirdest borders on Earth.", 0.3),
 ("Miss one, and he's fired. Weird borders, part two.", 0.35),
 ("Package one: Pheasant Island, Spain. A tiny island in a river between Spain and France.", 0.25),
 ("Since 1659, it switches country every six months. February to July, it's Spanish. August to January, French.", 0.3),
 ("It's November. Wrong country on the label.", 0.3),
 ("Also, nobody lives there, and visiting is forbidden. Package one: returned.", 0.4),
 ("Package two: Baarle. Twenty-two bits of Belgium inside the Netherlands. And seven Dutch bits inside those.", 0.25),
 ("One house has its living room in the Netherlands and its kitchen in Belgium. Two doorbells. Two house numbers.", 0.3),
 ("Pete rings both. Package two: delivered. Probably.", 0.4),
 ("Package three: Point Roberts, USA. About twelve hundred Americans, cut off by Canada.", 0.25),
 ("Driving there from the rest of America? Two borders. Older kids cross four a day, just for school.", 0.4),
 ("Package four: Märket, a rock between Sweden and Finland. In 1885, Finland built a lighthouse there. On the Swedish side.", 0.3),
 ("So in 1985, they bent the border into a crazy S-shape around the lighthouse, so nobody lost a single meter.", 0.25),
 ("Pete's package? A light bulb. Of course.", 0.4),
 ("Package five: Bir Tawil, between Egypt and Sudan. Two thousand square kilometers that no country on Earth claims.", 0.25),
 ("Both want the land next door instead. The label says: to the King of Bir Tawil.", 0.3),
 ("There is no king. One hour left. Should Pete crown himself? Comment A for King Pete, or B for go home.", 0.6),
]
CAPS = [
 ["THIS IS", "[PARCEL PETE.]", "{24 HOURS,}", "5 PACKAGES,", "THE [WEIRDEST]", "BORDERS ON EARTH."],
 ["MISS ONE,", "HE'S {FIRED.}", "WEIRD BORDERS,", "[PART TWO.]"],
 ["#1:", "[PHEASANT ISLAND,]", "SPAIN.", "A TINY ISLAND", "BETWEEN", "{SPAIN} AND [FRANCE.]"],
 ["SINCE [1659]", "IT {SWITCHES COUNTRY}", "EVERY 6 MONTHS.", "FEB–JULY:", "{SPANISH.}", "AUG–JAN:", "[FRENCH.]"],
 ["IT'S [NOVEMBER.]", "{WRONG COUNTRY}", "ON THE LABEL."],
 ["NOBODY", "LIVES THERE.", "VISITING:", "{FORBIDDEN.}", "PACKAGE ONE:", "[RETURNED.]"],
 ["#2: [BAARLE.]", "[22] PIECES", "OF {BELGIUM}", "INSIDE THE", "[NETHERLANDS.]", "AND [7] DUTCH", "PIECES", "{INSIDE THOSE.}"],
 ["ONE HOUSE:", "LIVING ROOM", "[NETHERLANDS,]", "KITCHEN", "{BELGIUM.}", "TWO DOORBELLS.", "TWO NUMBERS."],
 ["PETE RINGS", "[BOTH.]", "DELIVERED.", "{PROBABLY.}"],
 ["#3:", "[POINT ROBERTS,]", "USA.", "[1,200]", "AMERICANS", "CUT OFF", "BY {CANADA.}"],
 ["TO DRIVE THERE:", "[2 BORDERS.]", "OLDER KIDS:", "{4 BORDERS}", "A DAY", "FOR SCHOOL."],
 ["#4: [MÄRKET,]", "SWEDEN–FINLAND.", "IN [1885]", "FINLAND BUILT", "A LIGHTHOUSE.", "ON THE", "{SWEDISH SIDE.}"],
 ["IN [1985]", "THEY BENT", "THE BORDER", "INTO AN {S-SHAPE}", "SO NOBODY", "LOST", "[A METER.]"],
 ["PETE'S PACKAGE?", "A [LIGHT BULB.]", "{OF COURSE.}"],
 ["#5: [BIR TAWIL,]", "EGYPT–SUDAN.", "[2,000 KM²]", "THAT {NO COUNTRY}", "CLAIMS."],
 ["BOTH WANT", "THE LAND", "[NEXT DOOR.]", "THE LABEL:", "TO THE", "{KING}", "OF BIR TAWIL."],
 ["THERE IS", "{NO KING.}", "1 HOUR LEFT.", "CROWN HIMSELF?", "[A] KING PETE", "[B] GO HOME"]]

PETE = Look(skin=SKINS[1], hair=(30, 40, 70), style='cap', shirt=(40, 95, 150), pants=(60, 50, 45), shoes=(30, 30, 40))
BOX = (70, 140, 200); TAPE = (120, 190, 230)
C_WORLD = (10, 30, 3.2); C_EU = (2, 47, 26); C_PHE = (-1.77, 43.34, 120)
C_BAARLE = (4.93, 51.44, 110); C_PR = (-123.06, 48.99, 110); C_NA = (-100, 45, 12); C_MAR = (19.13, 60.3, 60); C_BIR = (33.75, 21.87, 60)

def parcel(img, x, y, s=1.0, lab=None):
    rrect(img, x - 90 * s, y - 70 * s, 180 * s, 140 * s, 10 * s, BOX); rrect(img, x - 12 * s, y - 70 * s, 24 * s, 140 * s, 2, TAPE)
    rrect(img, x - 90 * s, y - 70 * s, 180 * s, 140 * s, 10 * s, mix(BOX, INK, 0.5), th=3)
    if lab: rrect(img, x + 18 * s, y + 6 * s, 64 * s, 44 * s, 4, WHITE)
def stat(img, t, label, value, col=MGOLD, at=0.0, y=300, w=560, x=W / 2):
    k = back(ramp(t, at, at + 0.25))
    if k <= 0: return
    rrect(img, x - w / 2 * k, y, w * k, 150, 26, col); rrect(img, x - w / 2 * k + 5, y + 5, w * k - 10, 140, 22, INK)
    if k > 0.85: text(img, label, x, y + 40, 38, col, INTER_B); text(img, value, x, y + 102, 84, WHITE, ANT)
def pete(img, t, x=540, y=1050, s=1.6, expr='smile', ar=-160, al=20, sweat=False):
    bob = 8 * math.sin(t * 5)
    person(img, PETE, x, y + bob, s, expr, al=al, ar=ar, sweat=sweat, blink=(t % 3.1) < 0.12)
def hud(img, t, left, hours, at=0.0):
    stat(img, t, 'PACKAGES LEFT', str(left), MGOLD, at, 150, 400, 290); stat(img, t, 'HOURS LEFT', str(hours), MRED, at + 0.1, 150, 400, 790)

# ---- shots ----
def s1(img, t, d):   # hook: Pete buried under parcels, sweating
    img[:] = grad((60, 30, 40), (30, 14, 20)); glow(img, 540, 900, 600, (40, 60, 120), 0.8)
    rrect(img, 0, 1400, W, 520, 0, (40, 30, 35))
    pete(img, t, 540, 860, 2.2, 'worry', ar=-170, al=170, sweat=True)
    for i, (px, py, s) in enumerate(((330, 1450, 1.4), (750, 1450, 1.4), (540, 1330, 1.3), (420, 1210, 1.1), (660, 1210, 1.1))):
        k = back(ramp(t, 0.15 * i, 0.15 * i + 0.25)); parcel(img, px, py - (1 - k) * 500, s, True)
    hud(img, t, 5, 24, 0.3)
    if t > 3.5: emoji(img, '💀', 860, 620, 120 * back(ramp(t, 3.5, 3.8)))
    flash(img, t, 0, 0.12, WHITE, 0.6)
def s2(img, t, d):
    cam = cam_lerp(C_PHE, C_WORLD, 0.0 if t < 0 else 1 - ramp(t, 0, 2.2), hop=False); cam = cam_lerp(C_WORLD, C_EU, ramp(t, 0, 2.4), hop=False)
    world(img, cam, t=t)
    series_chip(img, 'WEIRD BORDERS', 'PART 2', eout(ramp(t, 0.2, 0.5)))
    for i, (lo, la) in enumerate(((-1.77, 43.34), (4.93, 51.44), (-123.06, 48.99), (19.13, 60.3), (33.75, 21.87))):
        dot(img, cam, lo, la, a=ramp(t, 0.8 + 0.2 * i, 1.0 + 0.2 * i))
    if t > 1.0: text(img, 'FIRED?', W / 2, 1550, 150, MRED, ANT, scale=back(ramp(t, 1.0, 1.3)), stroke=10, scol=INK)
def s3(img, t, d):
    cam = cam_lerp(C_EU, (-1.77, 43.34, 70), ramp(t, 0, 1.6), hop=False); world(img, cam, hi={'ESP': MRED, 'FRA': MBLUE}, t=t)
    rank(img, t, 1, 0.2); pin(img, cam, -1.77, 43.34, '🏝️', 'PHEASANT ISLAND', ramp(t, 1.4, 1.7), size=0.9)
    stat(img, t, 'PACKAGES LEFT', '5', MGOLD, 0.1, 1450, 420)
def river(img, t, flag, lab=1.0):
    img[:] = grad((90, 120, 90), (60, 90, 60))
    poly(img, [(0, 760), (W, 640), (W, 1180), (0, 1300)], (150, 100, 40))
    for k in range(8): line(img, (0, 820 + k * 55 + 10 * math.sin(t * 2 + k)), (W, 700 + k * 55 + 10 * math.sin(t * 2 + k + 1)), (175, 125, 60), 3)
    ell(img, (540, 970), 330, 90, (70, 150, 90)); ell(img, (540, 960), 300, 70, (80, 170, 100))
    for x in (380, 470, 610, 700): circ(img, (x, 930), 34, (50, 120, 60))
    rrect(img, 520, 820, 40, 120, 6, (200, 200, 205))   # the monument
    pill(img, 540, 580, 'SPAIN', 46, INK, (120, 120, 255), alpha=lab); pill(img, 540, 1400, 'FRANCE', 46, INK, MBLUE, alpha=lab)
    emoji(img, flag, 540, 760, 120)
def s4(img, t, d):
    k = (t * 1.5) % 2 < 1; river(img, t, '🇪🇸' if k else '🇫🇷')
    if t > 0.3: stat(img, t, 'SINCE', '1659', MGOLD, 0.3, 160, 360)
    if t > 3.0:
        for i, (lab, col) in enumerate((('FEB–JUL 🇪🇸', MRED), ('AUG–JAN 🇫🇷', MBLUE))):
            pill(img, 540, 1560 + i * 110, lab.split(' ')[0] + (' · SPAIN' if i == 0 else ' · FRANCE'), 52, INK, col, alpha=ramp(t, 3.0 + 1.4 * i, 3.3 + 1.4 * i))
def s5(img, t, d):
    img[:] = grad((50, 40, 60), (25, 18, 30))
    parcel(img, 540, 900, 3.0, True); text(img, 'SPAIN', 600, 940, 60, INK, ANT)
    pill(img, 540, 400, 'TODAY: NOV 15', 56, INK, MGOLD, alpha=ramp(t, 0.1, 0.4))
    emoji(img, '🇫🇷', 540, 560, 130 * back(ramp(t, 0.4, 0.7)))
    if t > 0.9:
        k = back(ramp(t, 0.9, 1.15)); rotated(img, lambda c: (rrect(c, 160, 1480, 760, 170, 20, MRED), text(c, 'WRONG COUNTRY', 540, 1565, 110, WHITE, ANT)), (540, 1565), 8, k)
def s6(img, t, d):
    river(img, t, '🚫', lab=0.6)
    if t > 0.2: stat(img, t, 'POPULATION', '0', MGOLD, 0.2, 160, 380)
    if t > 2.6:
        pete(img, t, 860, 1520, 0.9, 'flat', ar=-60)
        k = back(ramp(t, 2.6, 2.9)); rotated(img, lambda c: (rrect(c, 120, 1180, 520, 140, 18, MRED), text(c, 'RETURNED', 380, 1250, 100, WHITE, ANT)), (380, 1250), -6, k)
    stat(img, t, 'PACKAGES LEFT', '5', MGOLD, 0.0, 1690, 380, 300) if t < 3.2 else stat(img, t, 'PACKAGES LEFT', '4', MGOLD, 3.2, 1690, 380, 300)
def s7(img, t, d):
    cam = cam_lerp((-1.77, 43.34, 70), C_BAARLE, ramp(t, 0, 1.5), hop=False); hi = {'NLD': (60, 140, 240), 'BEL': (70, 200, 240)}
    world(img, cam, hi=hi, t=t); rank(img, t, 2, 0.2)
    rnd = random.Random(3)
    nb = int(counter(t, 2.0, 4.6, 0, 22)); nd = int(counter(t, 5.2, 6.6, 0, 7))
    pts = [(4.93 + rnd.uniform(-0.6, 0.6) * 1.0, 51.44 + rnd.uniform(-0.35, 0.35)) for _ in range(29)]
    for i in range(nb): dot(img, cam, *pts[i], (70, 200, 240), 10)
    for i in range(nd): dot(img, cam, pts[i][0] + 0.03, pts[i][1] + 0.02, (60, 140, 240), 6)
    if t > 2.0: stat(img, t, 'BELGIAN BITS', str(nb), (70, 200, 240), 2.0, 1450, 420, 290)
    if t > 5.2: stat(img, t, 'DUTCH BITS IN THOSE', str(nd), (60, 140, 240), 5.2, 1450, 460, 790)
    pin(img, cam, 4.93, 51.44, '🇧🇪', 'BAARLE', ramp(t, 1.3, 1.6), size=0.8)
def house(img, t, rings=0):
    img[:] = grad((90, 60, 50), (50, 30, 25)); stars(img, t, 0.4, 700, (90, 60, 50))
    rrect(img, 0, 1450, W, 470, 0, (60, 60, 60))
    rrect(img, 190, 820, 700, 630, 10, (170, 190, 215)); poly(img, [(150, 830), (540, 520), (930, 830)], (60, 70, 130))
    for y in range(820, 1460, 40): line(img, (540, y), (540, y + 22), WHITE, 6)   # the border line through the house
    for x in (300, 780): rrect(img, x - 80, 920, 160, 140, 8, (120, 200, 240))
    for x, num, col in ((380, '19', (60, 140, 240)), (700, '2', (70, 200, 240))):
        rrect(img, x - 60, 1190, 120, 260, 10, (60, 80, 120)); rrect(img, x - 40, 1120, 80, 54, 8, WHITE); text(img, num, x, 1148, 44, INK, ANT)
        circ(img, (x + 80, 1300), 14, col)
    pill(img, 330, 760, 'NETHERLANDS 🇳🇱'.split(' ')[0], 40, INK, (60, 140, 240)); pill(img, 750, 760, 'BELGIUM', 40, INK, (70, 200, 240))
def s8(img, t, d):
    house(img, t)
    if t > 1.2: emoji(img, '🛋️', 300, 990, 100 * back(ramp(t, 1.2, 1.5)))
    if t > 2.6: emoji(img, '🍳', 780, 990, 100 * back(ramp(t, 2.6, 2.9)))
    if t > 3.8: stat(img, t, 'DOORBELLS', '2', MGOLD, 3.8, 1530, 360, 290);
    if t > 4.6: stat(img, t, 'HOUSE NUMBERS', '2', MRED, 4.6, 1530, 400, 790)
def s9(img, t, d):
    house(img, t); pete(img, t, 540, 1240, 0.8, 'smile' if t < 2 else 'flat', ar=-120, al=120)
    for i, x in enumerate((460, 780)):
        if t > 0.3 + i * 0.5: emoji(img, '🔔', x, 1240, 80 * back(ramp(t, 0.3 + i * 0.5, 0.55 + i * 0.5)), rot=15 * math.sin(t * 30))
    if t > 1.5: stat(img, t, 'PACKAGES LEFT', '3', MGOLD, 1.5, 300, 420)
    if t > 2.4: text(img, 'PROBABLY', 540, 560, 120, MGOLD, ANT, scale=back(ramp(t, 2.4, 2.7)), stroke=8, scol=INK)
def s10(img, t, d):
    cam = cam_lerp(C_BAARLE, C_PR, ramp(t, 0, 1.8)); world(img, cam, hi={'USA': MBLUE, 'CAN': MRED} if t > 1.5 else {}, t=t)
    rank(img, t, 3, 1.2); pin(img, cam, -123.06, 48.99, '🇺🇸', 'POINT ROBERTS', ramp(t, 1.7, 2.0), size=0.9)
    if t > 2.6: stat(img, t, 'POPULATION', str(int(counter(t, 2.6, 3.6, 0, 1191))), MGOLD, 2.6, 1450, 420)
def peninsula(img, t):
    img[:] = grad(OCEAN2, OCEAN)
    poly(img, [(0, 0), (W, 0), (W, 900), (700, 900), (640, 860), (380, 880), (0, 950)], (88, 128, 96))   # Canada
    poly(img, [(380, 880), (640, 860), (700, 1000), (600, 1150), (430, 1120)], (100, 150, 110))     # Point Roberts
    for x in range(0, W, 40): line(img, (x, 900), (x + 22, 900), WHITE, 6)
    poly(img, [(0, 1500), (W, 1420), (W, H), (0, H)], (100, 150, 110))   # mainland USA
    for x in range(0, W, 40): line(img, (x, 1460 - x * 0.07), (x + 22, 1460 - (x + 22) * 0.07), WHITE, 6)
    pill(img, 540, 400, 'CANADA', 50, INK, MRED); pill(img, 540, 1030, 'POINT ROBERTS 🇺🇸'.split(' 🇺')[0], 40, INK, MBLUE); pill(img, 540, 1650, 'REST OF THE USA', 44, INK, MBLUE)
def s11(img, t, d):
    peninsula(img, t)
    k = ramp(t, 0.3, 3.0); path = [(540, 1700), (900, 1420), (980, 900), (650, 950)]
    seg = min(2.999, k * 3); i = int(seg); f = seg - i; x = path[i][0] + (path[i + 1][0] - path[i][0]) * f; y = path[i][1] + (path[i + 1][1] - path[i][1]) * f
    for a, b in zip(path[:i + 1], path[1:i + 2]): line(img, a, b if path.index(b) <= i else (x, y), MGOLD, 10)
    emoji(img, '🚚', x, y, 90)
    nb = 0 + (k > 0.36) + (k > 0.93); stat(img, t, 'BORDERS CROSSED', str(nb), MGOLD, 0.2, 150, 440)
    if t > 3.6: emoji(img, '🚌', 300, 1250, 100 * back(ramp(t, 3.6, 3.9))); stat(img, t, 'KIDS · BORDERS A DAY', '4', MRED, 3.8, 1150, 480, 330)
def s12(img, t, d):
    cam = cam_lerp(C_PR, C_MAR, ramp(t, 0, 1.8)); world(img, cam, hi={'SWE': MGOLD, 'FIN': MBLUE} if t > 1.5 else {}, t=t)
    rank(img, t, 4, 1.2); pin(img, cam, 19.13, 60.3, '🗼', 'MÄRKET', ramp(t, 1.7, 2.0), size=0.9)
    if t > 3.4: stat(img, t, 'LIGHTHOUSE BUILT', '1885', MGOLD, 3.4, 1450, 440)
    if t > 5.6: text(img, 'OOPS', 540, 1300, 170, MRED, ANT, scale=back(ramp(t, 5.6, 5.9)), stroke=10, scol=INK)
def rock(img, t, bent):
    img[:] = grad(OCEAN2, OCEAN)
    for k in range(12): line(img, (0, 400 + k * 120 + 15 * math.sin(t + k)), (W, 400 + k * 120 + 15 * math.sin(t + k + 1)), mix(OCEAN, WHITE, 0.05), 2)
    poly(img, [(200, 760), (480, 640), (820, 700), (900, 980), (760, 1250), (380, 1270), (170, 1050)], (150, 150, 160))
    x0 = 540
    if bent <= 0: pts = [(x0, 600), (x0, 1320)]
    else:
        pts = []
        for i in range(41):
            y = 600 + i * 18; u = (y - 600) / 720; dx = bent * 260 * math.sin(u * 2 * math.pi) * (1 if u < 1 else 0)
            pts.append((x0 + dx, y))
    for a, b in zip(pts, pts[1:]): line(img, a, b, MGOLD, 8)
    lx, ly = 620, 900
    rrect(img, lx - 40, ly - 180, 80, 200, 8, WHITE); rrect(img, lx - 40, ly - 120, 80, 40, 0, MRED); rrect(img, lx - 50, ly - 220, 100, 50, 10, (60, 60, 60))
    glow(img, lx, ly - 195, 140, (120, 220, 255), 0.6 + 0.3 * math.sin(t * 6))
    pill(img, 300, 560, 'FINLAND', 40, INK, MBLUE); pill(img, 800, 560, 'SWEDEN', 40, INK, MGOLD)
def s13(img, t, d):
    b = ease(ramp(t, 1.4, 3.4)); rock(img, t, b)
    stat(img, t, 'BORDER REDRAWN', '1985', MGOLD, 0.2, 150, 440)
    if t > 4.6: stat(img, t, 'LAND LOST', '0 M²', MRED, 4.6, 1450, 380)
def s14(img, t, d):
    rock(img, t, 1.0); pete(img, t, 330, 1150, 0.9, 'flat', ar=-150)
    emoji(img, '💡', 540, 700, 200 * back(ramp(t, 0.6, 0.9)))
    if t > 0.6: stat(img, t, 'PACKAGES LEFT', '1', MGOLD, 1.4, 1450, 420)
def s15(img, t, d):
    cam = cam_lerp(C_MAR, C_BIR, ramp(t, 0, 1.8)); world(img, cam, hi={'EGY': MGOLD, 'SDN': MRED} if t > 1.5 else {}, t=t, dim=t > 1.5)
    rank(img, t, 5, 1.2); pin(img, cam, 33.75, 21.87, '🏳️', 'BIR TAWIL', ramp(t, 1.7, 2.0), size=0.9)
    if t > 3.6: stat(img, t, 'CLAIMED BY', '0 COUNTRIES', MRED, 3.6, 1450, 520)
def desert(img, t, pills=1.0):
    img[:] = grad((200, 210, 240), (90, 160, 220)); rrect(img, 0, 1000, W, 920, 0, (100, 170, 215))
    for k in range(6): ell(img, (k * 220, 1040), 260, 60, (90, 160, 205))
    circ(img, (850, 380), 110, (150, 230, 255)); glow(img, 850, 380, 300, (60, 120, 160), 0.5)
    for (x, y, l) in ((330, 1480, 'EGYPT WANTS IT'), (330, 1580, 'SUDAN WANTS IT')): pill(img, x, y, l, 40, INK, WHITE, alpha=pills)
    pill(img, 800, 1530, 'HALAIB', 56, INK, MGOLD, alpha=pills)
def s16(img, t, d):
    desert(img, t, 1 - ramp(t, 2.7, 3.0)); pete(img, t, 540, 820, 1.1, 'worry', ar=-150, sweat=True)
    parcel(img, 700, 1000, 0.9, True)
    if t > 3.0:
        k = back(ramp(t, 3.0, 3.3)); rrect(img, W / 2 - 420 * k, 1560, 840 * k, 170, 20, WHITE)
        if k > 0.8: text(img, 'TO: THE KING', W / 2, 1610, 70, INK, ANT); text(img, 'OF BIR TAWIL', W / 2, 1680, 56, MRED, ANT)
def s17(img, t, d):
    desert(img, t, 0.0)
    if t > 1.2: emoji(img, '👑', 540, 590 + 20 * math.sin(t * 4), 150 * back(ramp(t, 1.2, 1.5)))
    pete(img, t, 540, 820, 1.1, 'shock' if t < 2.5 else 'smile', ar=-170)
    stat(img, t, 'HOURS LEFT', '1', MRED, 0.6, 150, 380)
    for i, (L_, txt, col) in enumerate((('A', 'KING PETE 👑'.split(' 👑')[0], ORANGE), ('B', 'GO HOME', BLUE))):
        k = back(ramp(t, 3.4 + 0.3 * i, 3.7 + 0.3 * i)); y = 1440 + i * 190
        if k > 0:
            rrect(img, W / 2 - 400 * k, y, 800 * k, 160, 30, col)
            if k > 0.8: circ(img, (W / 2 - 300, y + 80), 56, WHITE); text(img, L_, W / 2 - 300, y + 84, 80, col, ANT); text(img, txt, W / 2 + 60, y + 84, 90, WHITE, ANT)

NOZOOM = (s17,)
def timeline(ls, dur):
    return [(0, s1), (ls(1) - 0.05, s2), (ls(2) - 0.05, s3), (ls(3) - 0.05, s4), (ls(4) - 0.05, s5), (ls(5) - 0.05, s6), (ls(6) - 0.05, s7), (ls(7) - 0.05, s8),
            (ls(8) - 0.05, s9), (ls(9) - 0.05, s10), (ls(10) - 0.05, s11), (ls(11) - 0.05, s12), (ls(12) - 0.05, s13), (ls(13) - 0.05, s14), (ls(14) - 0.05, s15),
            (ls(15) - 0.05, s16), (ls(16) - 0.05, s17)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'whoosh': [ls(i) for i in (1, 2, 6, 9, 11, 14)], 'boom': [ls(0) + 0.05],
            'pop': [ls(0) + 0.15 * k for k in range(5)] + [ls(0) + 1.2, ls(0) + 1.3, ls(5) + 3.2, ls(8) + 1.5, ls(13) + 1.4, ls(12) + 4.6],
            'ding': [ls(2) + 1.4, ls(6) + 1.3, ls(8) + 0.3, ls(8) + 0.8, ls(9) + 1.7, ls(11) + 1.7, ls(13) + 0.6, ls(14) + 1.7],
            'mistake': ls(4) + 0.9, 'notif': [ls(16) + 3.4, ls(16) + 3.7], 'end': ls(16) - 0.05}

POST = {
 'title': "An Island That Changes Country Every 6 Months 🌍 Weird Borders Part 2 #shorts",
 'caption': "Parcel Pete has 24 hours to deliver 5 packages to the weirdest borders on Earth: an island that switches country every 6 months, a house in 2 countries, a US town you reach through Canada, a bent border and land NO country wants 📦🌍 Should Pete crown himself? Comment A (King Pete) or B (go home) 👇",
 'tags': '#geography #borders #maps #facts #didyouknow #part2',
 'source': "Sources: Pheasant Island condominium (Treaty of the Pyrenees 1659; Spain 1 Feb–31 Jul, France 1 Aug–31 Jan; uninhabited, access forbidden) – Wikipedia; Baarle-Hertog: 22 Belgian enclaves, 7 Dutch exclaves inside them; house Loveren 2 / Loveren 19 with two doorbells – Brussels Times; Point Roberts, WA: 1,191 people (2020 census), students cross the border 4 times per school day – Wikipedia; Märket lighthouse 1885 on the Swedish side, border redrawn 1985 in an inverted S with no net land change – Wikipedia; Bir Tawil ~2,060 km², unclaimed because Egypt and Sudan both claim the Halaib Triangle. Map: Natural Earth. Parcel Pete is fictional.",
}
