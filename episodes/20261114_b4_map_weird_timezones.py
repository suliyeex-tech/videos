import math, random
from kit import *
from mapzoom import *

FORMAT = 'map'
SLUG = '2026-11-14-weird-time-zones-part1'
VOICE = 'bro'; SPEED = 1.25; CAPTION = 'karaoke'; TICKS = True; ZOOM = 0.8; VIGNETTE = 0.3
MOOD = {'style': 'hype', 'root': 55.0}
LINES = [
 ("These two islands are four kilometers apart. And twenty-one hours apart.", 0.3),
 ("Weird time zones of the world, part one. Number six is the one nobody believes.", 0.3),
 ("Number one: the Diomede Islands. Big Diomede is Russia. Little Diomede is Alaska.", 0.25),
 ("The International Date Line runs right between them. So in winter, you can literally look across at tomorrow.", 0.25),
 ("That's why people call them Tomorrow Island and Yesterday Island.", 0.35),
 ("Number two: Nepal. Its clocks are five hours and forty-five minutes ahead of world time. Not five. Not six. Forty-five.", 0.35),
 ("Number three: China. It's about as wide as the mainland United States, but it runs on one single time zone.", 0.25),
 ("So out west in Kashgar, the January sun rises after ten in the morning.", 0.35),
 ("Number four: Samoa. In 2011, the whole country skipped a day. Friday, December thirtieth, just never happened.", 0.25),
 ("They hopped across the date line to line up with Australia and New Zealand.", 0.35),
 ("Number five: Kiribati. Its Line Islands are at UTC plus fourteen, the earliest clocks on Earth. They see every new year first.", 0.35),
 ("Number six: the country with the most time zones. Not Russia. Not the US. France.", 0.25),
 ("Twelve time zones, from the Pacific to the Indian Ocean, thanks to islands all over the planet.", 0.35),
 ("Bonus: at the South Pole, every time zone meets in one point. The research station just uses New Zealand time, because that's where its flights come from.", 0.35),
 ("Part two: the weirdest borders on Earth. Like an island that changes country every six months.", 0.3),
 ("Which one broke your brain? Comment the number.", 1.0),
]
CAPS = [
 ["[4 KM] APART.", "{21 HOURS}", "APART."], ["WEIRD", "[TIME ZONES,]", "PART ONE.", "NUMBER SIX", "NOBODY {BELIEVES.}"],
 ["#1:", "[DIOMEDE ISLANDS.]", "BIG DIOMEDE:", "{RUSSIA.}", "LITTLE DIOMEDE:", "[ALASKA.]"],
 ["THE [DATE LINE]", "RUNS BETWEEN THEM.", "IN WINTER", "YOU CAN", "LOOK AT", "{TOMORROW.}"],
 ["[TOMORROW ISLAND]", "AND", "{YESTERDAY ISLAND.}"],
 ["#2: [NEPAL.]", "[+5:45]", "AHEAD OF", "WORLD TIME.", "NOT 5.", "NOT 6.", "{FORTY-FIVE.}"],
 ["#3: [CHINA.]", "AS WIDE AS", "THE MAINLAND US.", "{ONE}", "TIME ZONE."],
 ["IN [KASHGAR,]", "THE JANUARY SUN", "RISES AFTER", "{10 AM.}"],
 ["#4: [SAMOA.]", "IN 2011", "IT {SKIPPED A DAY.}", "FRIDAY", "DEC 30", "{NEVER HAPPENED.}"],
 ["THEY HOPPED", "THE DATE LINE", "TO MATCH", "[AUSTRALIA]", "AND [NEW ZEALAND.]"],
 ["#5: [KIRIBATI.]", "[UTC +14,]", "THE EARLIEST", "CLOCKS ON EARTH.", "{NEW YEAR}", "{FIRST.}"],
 ["#6: MOST", "TIME ZONES.", "NOT RUSSIA.", "NOT THE US.", "{FRANCE.}"],
 ["[12] TIME ZONES,", "THANKS TO", "{ISLANDS}", "ALL OVER", "THE PLANET."],
 ["BONUS:", "[SOUTH POLE.]", "EVERY TIME ZONE", "MEETS.", "THEY USE", "{NEW ZEALAND}", "TIME,", "FLIGHTS COME", "FROM THERE."],
 ["PART TWO:", "{WEIRDEST BORDERS.}", "AN ISLAND THAT", "[CHANGES COUNTRY]", "EVERY 6 MONTHS."],
 ["WHICH ONE", "{BROKE YOUR BRAIN?}", "COMMENT", "[THE NUMBER.]"]]

C_WORLD = (10, 15, 3.2)
C_BERING = (-169.0, 65.8, 40); C_DIO = (-169.0, 65.77, 420)
C_NEPAL = (84.0, 28.3, 45); C_CHINA = (104.0, 35.0, 13); C_KASH = (76.0, 39.5, 30); C_SAMOA = (-172.0, -13.8, 30); C_PACIFIC = (175.0, -25.0, 7)
C_KIRI = (-157.4, 1.9, 22); C_FRANCE = (2.5, 46.5, 22); C_FRWORLD = (20, 0, 3.2)
FR_DOTS = [(-149.4, -17.6), (165.6, -21.3), (55.5, -21.1), (-61.5, 16.2), (-53.0, 4.0), (-56.3, 46.9), (45.1, -12.8), (-176.2, -13.3),
           (-61.0, 14.6), (69.3, -49.3), (-109.2, 10.3), (-140.0, -9.0), (2.5, 46.5)]

def dio(img, t, labels=0.0, zoom=1.0):
    """schematic close-up of the Diomede Islands (not to scale for the map, but true to the 3.8 km gap)"""
    img[:] = grad(OCEAN2, OCEAN)
    for k in range(14): line(img, (0, 300 + k * 110 + 20 * math.sin(t + k)), (W, 300 + k * 110 + 20 * math.sin(t + k + 1)), mix(OCEAN, WHITE, 0.05), 2)
    z = zoom
    poly(img, [(540 - 520 * z, 900 - 260 * z), (540 - 260 * z, 900 - 330 * z), (540 - 90 * z, 900 - 200 * z), (540 - 70 * z, 900 + 60 * z), (540 - 210 * z, 900 + 240 * z), (540 - 470 * z, 900 + 200 * z), (540 - 560 * z, 900)], LAND)
    poly(img, [(540 + 110 * z, 900 - 40 * z), (540 + 230 * z, 900 - 120 * z), (540 + 330 * z, 900 - 40 * z), (540 + 300 * z, 900 + 90 * z), (540 + 160 * z, 900 + 110 * z)], LAND)
    for y in range(0, H, 40): line(img, (540, y), (540, y + 22), MGOLD, 6)
    pill(img, 540, 480, 'DATE LINE', 40, INK, MGOLD)
    if labels > 0:
        pill(img, 540 - 300 * z, 900 - 400 * z, 'BIG DIOMEDE 🇷🇺' if False else 'BIG DIOMEDE · RUSSIA', 34, INK, (120, 120, 255), alpha=labels)
        pill(img, 540 + 220 * z, 900 + 200 * z, 'LITTLE DIOMEDE · USA', 34, INK, MBLUE, alpha=labels)
    line(img, (540 - 70 * z, 1080), (540 + 110 * z, 1080), WHITE, 4); pill(img, 540 + 20 * z, 1130, '3.8 KM', 36, INK, WHITE, alpha=labels)
def island(img, cam, lon, lat, rx, ry, col):
    x, y = proj(cam, lon, lat); s = cam[2] / 420
    ell(img, (x, y), rx * s, ry * s, col); ell(img, (x, y), rx * s, ry * s, WHITE, th=3)
def s1(img, t, d):
    dio(img, t, labels=ramp(t, 0.6, 0.9), zoom=0.8 + 0.2 * ease(ramp(t, 0, 2)))
    if t > 1.2:
        clock(img, 290, 1500, 'SUNDAY', '10:00', MGOLD, ramp(t, 1.2, 1.5), 300); clock(img, 790, 1500, 'SATURDAY', '13:00', MBLUE, ramp(t, 1.3, 1.6), 300)
    flash(img, t, 0, 0.12, WHITE, 0.6)
def s2(img, t, d):
    cam = cam_lerp(C_BERING, C_WORLD, ramp(t, 0, 1.4), hop=False); world(img, cam, t=t)
    series_chip(img, 'WEIRD TIME ZONES', 'PART 1', eout(ramp(t, 0.2, 0.5)))
    for i in range(6): dot(img, cam, *[(-169, 65.8), (84, 28.3), (104, 35), (-172, -13.8), (-157.4, 1.9), (2.5, 46.5)][i], a=ramp(t, 1.4 + 0.25 * i, 1.6 + 0.25 * i))
def s3(img, t, d):
    cam = cam_lerp(C_WORLD, C_BERING, ramp(t, 0, 1.4), hop=False); world(img, cam, hi={'RUS': (60, 60, 200), 'USA': (200, 120, 60)}, t=t)
    rank(img, t, 1, 0.2)
    pin(img, cam, -169.06, 65.78, '🇷🇺', 'BIG DIOMEDE', ramp(t, 1.6, 1.9), size=0.9)
    pin(img, cam, -168.93, 65.4, '🇺🇸', 'LITTLE DIOMEDE', ramp(t, 3.0, 3.3), size=0.9, col=MBLUE)
def s4(img, t, d):
    dio(img, t, labels=1.0, zoom=1.0)
    if t > 2.5: clock(img, 290, 1500, 'TOMORROW', 'SUN', MGOLD, ramp(t, 2.5, 2.8), 300); clock(img, 790, 1500, 'TODAY', 'SAT', MBLUE, ramp(t, 2.6, 2.9), 300)
def s5(img, t, d):
    dio(img, t, labels=0.0, zoom=1.0); x1, y1 = 240, 760; x2, y2 = 770, 900
    pill(img, x1, y1 - 140, 'TOMORROW ISLAND', 40, INK, MGOLD, alpha=ramp(t, 0.1, 0.4)); pill(img, x2, y2 + 110, 'YESTERDAY ISLAND', 40, INK, MBLUE, alpha=ramp(t, 1.0, 1.3))
def s6(img, t, d):
    cam = cam_lerp(C_BERING, C_NEPAL, ramp(t, 0, 1.6)); world(img, cam, hi={'NPL': MGOLD} if t > 1.4 else {}, t=t, dim=t > 1.4)
    rank(img, t, 2, 1.0); pin(img, cam, 84.0, 28.3, '🇳🇵', 'NEPAL', ramp(t, 1.6, 1.9))
    if t > 2.6:
        v = int(counter(t, 2.6, 4.2, 0, 45)); clock(img, W / 2, 1530, 'UTC', f'+5:{v:02d}', MGOLD, ramp(t, 2.6, 2.9), 380)
def s7(img, t, d):
    cam = cam_lerp(C_NEPAL, C_CHINA, ramp(t, 0, 1.2), hop=False); world(img, cam, hi={'CHN': MRED}, t=t, dim=True)
    rank(img, t, 3, 0.3); pin(img, cam, 116.4, 39.9, '🇨🇳', 'BEIJING TIME', ramp(t, 1.0, 1.3), size=0.9)
    if t > 2.5:
        for k in range(5):
            x, _ = proj(cam, 75 + k * 15, 0); a = ramp(t, 2.5 + k * 0.15, 2.7 + k * 0.15)
            for y in range(560, 1380, 40): line(img, (x, y), (x, y + 20), mix(INK, WHITE, 0.8 * a), 4)
        pill(img, W / 2, 1500, '5 ZONES WIDE → 1 CLOCK', 46, INK, MGOLD, alpha=ramp(t, 3.4, 3.7))
def s8(img, t, d):
    cam = cam_lerp(C_CHINA, C_KASH, ramp(t, 0, 1.0), hop=False); world(img, cam, hi={'CHN': MRED}, t=t, dim=True)
    pin(img, cam, 75.99, 39.47, '🌅', 'KASHGAR', ramp(t, 0.8, 1.1))
    if t > 1.6: clock(img, W / 2, 1520, 'JANUARY SUNRISE', '10:16', MGOLD, ramp(t, 1.6, 1.9), 460)
def s9(img, t, d):
    cam = cam_lerp(C_KASH, C_SAMOA, ramp(t, 0, 1.6)); world(img, cam, t=t)
    rank(img, t, 4, 1.0); pin(img, cam, -172.0, -13.8, '🇼🇸', 'SAMOA', ramp(t, 1.6, 1.9))
    if t > 3.2:
        for i, (dd, col) in enumerate((('29', WHITE), ('30', MRED), ('31', WHITE))):
            x = 260 + i * 280; k = back(ramp(t, 3.2 + 0.2 * i, 3.45 + 0.2 * i))
            rrect(img, x - 110 * k, 1380, 220 * k, 240, 20, WHITE); rrect(img, x - 110 * k, 1380, 220 * k, 60, 16, MRED)
            if k > 0.8: text(img, dd, x, 1520, 120, INK, ANT)
        if t > 4.6:
            a = back(ramp(t, 4.6, 4.85)); line(img, (430, 1400), (630, 1600), MRED, int(24 * a) + 1); line(img, (630, 1400), (430, 1600), MRED, int(24 * a) + 1)
def s10(img, t, d):
    cam = cam_lerp(C_SAMOA, C_PACIFIC, ramp(t, 0, 1.2), hop=False); world(img, cam, hi={'AUS': (80, 160, 220), 'NZL': (80, 160, 220)}, t=t)
    x0, y0 = proj(cam, -172.0, -13.8); x1, y1 = proj(cam, 172.0, -13.8)
    k = ease(ramp(t, 0.8, 2.2)); dot(img, cam, -172.0 + (-16 + 360) * 0 if False else -172.0, -13.8, MGOLD, 14, 1 - k)
    xx = x0 + (x1 - x0) * k; yy = y0 - 160 * math.sin(math.pi * k); circ(img, (xx, yy), 18, MGOLD); glow(img, xx, yy, 80, MGOLD, 0.6)
    dl, _ = proj(cam, 180.0, 0)
    for y in range(0, H, 40): line(img, (dl, y), (dl, y + 22), MGOLD, 5)
    pill(img, dl, 560, 'DATE LINE', 40, INK, MGOLD)
def s11(img, t, d):
    cam = cam_lerp(C_PACIFIC, C_KIRI, ramp(t, 0, 1.4)); world(img, cam, t=t)
    rank(img, t, 5, 1.0); pin(img, cam, -157.4, 1.9, '🇰🇮', 'LINE ISLANDS', ramp(t, 1.4, 1.7), size=0.9)
    if t > 2.6: clock(img, W / 2, 1520, 'UTC', '+14', MGOLD, ramp(t, 2.6, 2.9), 300)
    if t > 5.0: emoji(img, '🎆', 860, 820, 150 * back(ramp(t, 5.0, 5.3)))
def s12(img, t, d):
    cam = cam_lerp(C_KIRI, C_WORLD, ramp(t, 0, 1.2), hop=False)
    hi = {}
    if t > 1.6: hi['RUS'] = (90, 90, 120)
    if t > 2.4: hi['USA'] = (120, 100, 90)
    if t > 3.4: hi = {'FRA': MBLUE}
    world(img, cam, hi=hi, t=t, dim=True); rank(img, t, 6, 0.3)
    for i, (lab, at) in enumerate((('RUSSIA? 11', 1.6), ('USA? 11', 2.4))):
        if at < t < 3.4: pill(img, W / 2, 1450 + i * 100, lab, 50, INK, (150, 150, 155))
    if t > 3.4: text(img, 'FRANCE', W / 2, 1470, 170, MBLUE, ANT, scale=back(ramp(t, 3.4, 3.7)), stroke=10, scol=INK); emoji(img, '🇫🇷', W / 2, 1650, 110)
def s13(img, t, d):
    world(img, C_FRWORLD, hi={'FRA': MBLUE}, t=t, dim=True)
    n = int(ramp(t, 0.2, 3.0) * len(FR_DOTS))
    for i, (lo, la) in enumerate(FR_DOTS[:n]): dot(img, C_FRWORLD, lo, la, MBLUE, 13)
    k = back(ramp(t, 3.0, 3.3)); text(img, '12 TIME ZONES', W / 2, 1480, 110, WHITE, ANT, scale=k, stroke=8, scol=INK)
def s14(img, t, d):   # polar view
    img[:] = grad((110, 62, 24), (70, 38, 14)); cx, cy = W / 2, 900
    circ(img, (cx, cy), 300, (245, 240, 235))
    for k in range(24):
        a = k / 24 * 2 * math.pi + t * 0.15; kk = ramp(t, 0.2 + k * 0.03, 0.4 + k * 0.03)
        line(img, (cx, cy), (cx + 420 * kk * math.cos(a), cy + 420 * kk * math.sin(a)), mix((200, 160, 120), MGOLD if k == 0 else (200, 160, 120), 1), 3)
    circ(img, (cx, cy), 24, MRED); pill(img, cx, cy - 380, 'SOUTH POLE', 50, INK, WHITE)
    if t > 3.6: clock(img, W / 2, 1520, 'STATION CLOCK', 'NZ TIME', MGOLD, ramp(t, 3.6, 3.9), 460); emoji(img, '🇳🇿', 860, 1360, 110 * back(ramp(t, 3.8, 4.1)))
    if t > 6.0: emoji(img, '✈️', 200 + 120 * (t - 6), 1300, 100)
def s15(img, t, d):
    cam = (-1.77, 43.34, 30 + 15 * t); world(img, cam, hi={'FRA': MBLUE, 'ESP': MRED}, t=t)
    x, y = proj(cam, -1.77, 43.34); k = 0.5 + 0.5 * math.sin(t * 6)
    emoji(img, '🇫🇷' if k > 0.5 else '🇪🇸', x, y - 150, 130); circ(img, (x, y), 20, MGOLD); glow(img, x, y, 120, MGOLD, 0.7)
    series_chip(img, 'WEIRDEST BORDERS', 'PART 2', eout(ramp(t, 0.2, 0.5)))
    text(img, '?', x + 150, y - 150, 150, WHITE, ANT, alpha=ramp(t, 1.5, 1.8))
def s16(img, t, d):
    world(img, C_WORLD, t=t, dim=True)
    for i in range(6):
        y = 420 + i * 140; k = back(ramp(t, 0.1 + i * 0.12, 0.35 + i * 0.12))
        if k > 0:
            rrect(img, W / 2 - 330 * k, y - 55, 660 * k, 110, 26, INK)
            if k > 0.8: text(img, f'#{i + 1}  ' + ['DIOMEDE', 'NEPAL', 'CHINA', 'SAMOA', 'KIRIBATI', 'FRANCE'][i], W / 2, y, 64, MGOLD if i == 5 else WHITE, ANT)

NOZOOM = (s5, s14, s16)
def timeline(ls, dur):
    fs = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16]
    return [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'whoosh': [ls(i) for i in (2, 5, 6, 8, 10, 11)], 'boom': [ls(0) + 0.05, ls(11) + 3.4],
            'ding': [ls(2) + 0.2, ls(5) + 1.0, ls(6) + 0.3, ls(8) + 1.0, ls(10) + 1.0, ls(11) + 0.3], 'pop': [ls(8) + 3.2, ls(8) + 3.4, ls(8) + 3.6, ls(12) + 0.5, ls(12) + 1.5],
            'notif': [ls(15) + k * 0.12 for k in range(6)], 'end': ls(15) - 0.05}

POST = {
 'title': "Two Islands 4 km Apart But 21 Hours Apart 🌍 Weird Time Zones Part 1 #shorts",
 'caption': "Two islands 4 km apart but 21 hours apart, a country that deleted a whole day, and the nation with the most time zones (it's not Russia) 🌍⏰ Which one broke your brain? Comment the number 👇",
 'tags': '#geography #timezones #maps #facts #didyouknow #part1',
 'source': "Sources: Diomede Islands (~3.8 km apart, date line between them; Wikipedia/geographyrealm); Nepal Standard Time UTC+5:45; China uses one time zone (Beijing Time); Kashgar latest sunrise ≈10:16 Beijing time in early January (sunrise-sunset.org); Samoa skipped 30 Dec 2011; Kiribati Line Islands UTC+14; France has 12 time zones (13 with Adélie Land); Amundsen–Scott South Pole Station keeps New Zealand time. Map: Natural Earth.",
}
