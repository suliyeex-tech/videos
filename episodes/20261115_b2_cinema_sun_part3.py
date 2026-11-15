import math, random
import numpy as np, cv2
from kit import *
from cinema import *
import cinema as Cn

FORMAT = 'cinema'
SLUG = '2026-11-15-the-sun-came-back-part-3'
VOICE = 'guy'; SPEED = 1.22; CAPTION = 'karaoke'; MOOD = {'style': 'cinematic', 'root': 52.0, 'bpm': 96}
PROGRESS = True; PROGRESS_COL = (60, 170, 255); VIGNETTE = 0.3; ZOOM = 1.1
LINES = [
 ("Golden Hour Greg has waited three hundred sixty-five days for one sunset. Today, the Sun comes back.", 0.25),
 ("A year ago, it vanished. Earth froze to minus one hundred Fahrenheit. Greg kept his ring light on.", 0.25),
 ("Now the Sun is back. Same place, same size. Greg sets up his tripod.", 0.2),
 ("Eight minutes, twenty seconds. That's how long sunlight used to take. Nothing.", 0.3),
 ("Because Earth didn't wait. With no Sun to orbit, it flew off in a straight line. Thirty kilometers every second.", 0.2),
 ("In one year, that's almost a billion kilometers. Farther out than Jupiter's orbit.", 0.25),
 ("So now the light needs fifty-three minutes to reach us.", 0.3),
 ("Minute fifty-three. A dot appears. Not a sunrise. A star. A really bright star.", 0.25),
 ("About forty times dimmer than a normal day. Like a gloomy, cloudy afternoon.", 0.25),
 ("Greg takes the photo anyway. Caption: golden hour, kind of.", 0.3),
 ("Then he checks the thermometer. Still minus one hundred. Way too weak to thaw anything.", 0.3),
 ("But wait. The Sun's gravity is back too. Can it pull us home?", 0.35),
 ("Out here, escaping the Sun takes about seventeen kilometers per second. Earth is doing thirty.", 0.25),
 ("So the Sun pulls, and pulls... and Earth slows down, but never turns around.", 0.3),
 ("We're leaving the solar system. Forever. With Greg's tripod still pointed at the Sun.", 0.3),
 ("And every night, his sunset gets a little smaller.", 0.35),
 ("A Sun that comes back like this, or no Sun at all? Comment A or B.", 1.0),
]
CAPS = [
 ["[GOLDEN HOUR GREG]", "WAITED", "{365 DAYS.}", "TODAY", "THE SUN", "[COMES BACK.]"],
 ["A YEAR AGO", "IT {VANISHED.}", "[−100 °F.]", "RING LIGHT", "STILL ON."], ["NOW", "[IT'S BACK.]", "SAME PLACE.", "TRIPOD", "SET UP."],
 ["[8 MIN 20 S.]", "THE OLD", "DELAY.", "{NOTHING.}"], ["EARTH", "{DIDN'T WAIT.}", "NO SUN", "TO ORBIT.", "STRAIGHT LINE.", "[30 KM]", "EVERY SECOND."],
 ["ONE YEAR =", "[~1 BILLION KM.]", "PAST", "{JUPITER'S ORBIT.}"], ["LIGHT NOW", "NEEDS", "[53 MINUTES.]"],
 ["[MINUTE 53.]", "A DOT.", "NOT A SUNRISE.", "{A STAR.}"], ["[40x DIMMER.]", "A GLOOMY,", "CLOUDY", "AFTERNOON."],
 ["PHOTO", "ANYWAY.", "[GOLDEN HOUR,]", "{KIND OF.}"], ["THERMOMETER:", "[−100 °F.]", "{TOO WEAK}", "TO THAW."],
 ["BUT WAIT.", "[GRAVITY]", "IS BACK TOO.", "{PULL US HOME?}"], ["ESCAPE SPEED", "OUT HERE:", "[17 KM/S.]", "EARTH:", "{30 KM/S.}"],
 ["THE SUN", "PULLS...", "EARTH", "SLOWS DOWN,", "{NEVER TURNS}", "{AROUND.}"], ["WE'RE", "{LEAVING}", "THE SOLAR", "SYSTEM.", "[FOREVER.]"],
 ["EVERY NIGHT", "HIS SUNSET", "GETS", "[SMALLER.]"], ["[A] THIS SUN", "OR [B] NO SUN?", "{COMMENT.}"]]
GREG = ((40, 120, 240), SKIN_T[0])

def hud(img, label, value, sub=None, col=WHITE, a=1.0):
    rrect(img, 60, 150, 600, 210, 26, (20, 16, 14)); rrect(img, 60, 150, 10, 210, 4, (60, 170, 255))
    text(img, label, 90 + twidth(label, 28, INTER_B) / 2, 190, 28, (200, 200, 205), INTER_B, alpha=a)
    text(img, value, 90 + twidth(value, 96, SERIF_I) / 2, 268, 96, col, SERIF_I, alpha=a)
    if sub: text(img, sub, 90 + twidth(sub, 24, INTER_B) / 2, 338, 24, (60, 170, 255), INTER_B, alpha=a)
def frozen_ground(img, y=1450):
    img[y:] = grad((200, 195, 190), (240, 236, 232), y, H)
def ringlight(img, x, y, s=1.0, on=1.0):
    line(img, (x, y), (x, y - 520 * s), (60, 60, 60), 10 * s)
    if on: glow(img, x, y - 600 * s, int(240 * s), (180, 200, 220), 0.9 * on)
    cv2.circle(img, P(x, y - 600 * s), int(90 * s * 8), mix((80, 80, 80), (250, 250, 255), on), int(18 * s), cv2.LINE_AA, 3)
def tripod(img, x, y, s=1.0, ang=0.0):
    for dx in (-60, 0, 60): line(img, (x, y - 260 * s), (x + dx * s, y), (50, 50, 55), 8 * s)
    cx, cy = x, y - 280 * s
    rrect(img, cx - 60 * s, cy - 40 * s, 120 * s, 80 * s, 12, (40, 40, 45)); circ(img, (cx + 70 * s, cy - 10 * s), 34 * s, (70, 70, 80)); circ(img, (cx + 70 * s, cy - 10 * s), 20 * s, (160, 120, 90))
def sundot(img, x, y, r, k=1.0):
    glow(img, x, y, int(r * 9), (130, 220, 255), 0.9 * k); circ(img, (x, y), r, mix((40, 40, 40), (210, 250, 255), k))
def night(img, t, k=1.0):
    img[:] = (8, 5, 4); stars(img, t, k)
def greg(img, x, y, s=1.4, arms=0.1): Cn.person(img, x, y, s, GREG[0], GREG[1], arms_up=arms)

def c1(img, t, d):
    night(img, t); frozen_ground(img)
    z = 1.25 - 0.25 * eout(ramp(t, 0, 0.8)); greg(img, 420, 1470, 1.5 * z); tripod(img, 720, 1470, 1.1)
    k = back(ramp(t, 0.15, 0.4))
    if k > 0: text(img, 'GOLDEN HOUR GREG', W / 2, 560, 96, YEL, ANT, scale=k, stroke=6, scol=INK)
    text(img, 'DAY 365 OF WAITING FOR A SUNSET', W / 2, 650, 36, WHITE, INTER_B, alpha=ramp(t, 0.5, 0.8))
    k = back(ramp(t, 3.4, 3.7)); pill(img, W / 2, 330, 'PART 3 · THE SUN COMES BACK', 44, INK, YEL, dot=RED, alpha=min(1, max(0, k)))
def c2(img, t, d):
    city(img, t, night=1.0); tint(img, (0, 0, 0), 0.45); snow(img, t, 0.7)
    ringlight(img, 760, 1500, 1.0, 1.0); greg(img, 470, 1500, 1.4)
    hud(img, 'ONE YEAR AGO', '−100 °F', 'THE SUN VANISHED', (255, 220, 190))
def snow(img, t, k=1.0):
    rb = random.Random(9)
    for i in range(int(120 * k)):
        x = (rb.uniform(0, W) + 40 * math.sin(t + i)) % W; y = (rb.uniform(0, H) + t * rb.uniform(80, 200)) % H
        circ(img, (x, y), rb.uniform(3, 7), (250, 250, 255))
def c3(img, t, d):
    night(img, t); frozen_ground(img)
    flash(img, t, 0.2, 0.3, WHITE, 0.6)
    k = back(ramp(t, 0.3, 0.7)); pill(img, W / 2, 330, 'SUN: BACK', 56, INK, YEL, dot=YEL, alpha=min(1, k))
    tripod(img, 700, 1470, 1.2); greg(img, 380, 1470, 1.3, arms=0.6 * ramp(t, 1.5, 2.0))
def c4(img, t, d):
    night(img, t); frozen_ground(img); tripod(img, 700, 1470, 1.2); greg(img, 380, 1470, 1.3)
    s = max(0, 500 - 500 * ramp(t, 0, d * 0.7)); hud(img, 'SUNLIGHT ARRIVES IN', f'{int(s // 60)}:{int(s % 60):02d}', 'THE OLD DELAY', YEL)
    if t > d * 0.75: text(img, 'NOTHING.', W / 2, 800, 120, RED, ANT, scale=back(ramp(t, d * 0.75, d * 0.75 + 0.3)))
def c5(img, t, d):
    night(img, t); cx, cy = 300, 1100
    text(img, 'X', cx, cy, 80, (120, 120, 130), INTER_B); text(img, 'WHERE THE SUN WAS', cx, cy + 80, 26, (150, 150, 160), INTER_B)
    k = ease(ramp(t, 0.2, d)); ex, ey = cx + 120 + 640 * k, cy - 900 * k
    for j in range(0, 40):
        u = j / 40 * k; circ(img, (cx + 120 + 640 * u, cy - 900 * u), 5, (60, 170, 255))
    earth(img, ex, ey, 60, t)
    hud(img, 'EARTH SPEED', '30 KM/S', 'STRAIGHT LINE, NO ORBIT', WHITE)
def c6(img, t, d):
    night(img, t); y = 1000
    line(img, (80, y), (1000, y), (90, 90, 100), 3)
    for lab, au, col in (('SUN', 0, YEL), ('EARTH WAS', 1, (60, 170, 255)), ('JUPITER\'S ORBIT', 5.2, (120, 170, 220)), ('EARTH NOW', 6.4, (60, 170, 255))):
        x = 120 + au * 135; circ(img, (x, y), 14 if au else 22, col)
        if au in (0, 5.2) or ramp(t, 0.6, 0.9) > 0: text(img, lab, x, y + (60 if au not in (1, 6.4) else -60), 28, col, INTER_B)
    kx = 120 + 135 * (1 + 5.4 * ease(ramp(t, 0.6, 2.4))); earth(img, kx, y, 30, t)
    hud(img, 'DISTANCE FLOWN', f'{int(counter(t, 0.6, 2.4, 0, 950))}M KM', 'IN ONE YEAR', WHITE)
def c7(img, t, d):
    night(img, t); frozen_ground(img); tripod(img, 700, 1470, 1.2); greg(img, 380, 1470, 1.3)
    hud(img, 'SUNLIGHT ARRIVES IN', f'{53 - int(counter(t, 0.3, d, 0, 2))} MIN', 'NOT 8 MIN 20 S', YEL)
    emoji(img, '⏳', 800, 760, 140 * back(ramp(t, 0.6, 0.9)))
def c8(img, t, d):
    night(img, t, 0.8); frozen_ground(img, 1500)
    k = ramp(t, 0.8, 1.6); sundot(img, 760, 520, 10 + 4 * k, k)
    flash(img, t, 0.8, 0.2, WHITE, 0.3)
    tripod(img, 560, 1500, 1.3); greg(img, 300, 1500, 1.3, arms=0.3)
    if t > 2.2: pill(img, 760, 660, 'THE SUN?!', 40, INK, YEL, alpha=ramp(t, 2.2, 2.5))
def c9(img, t, d):
    img[:] = grad((60, 55, 55), (110, 105, 100)); frozen_ground(img, 1450)
    sundot(img, 760, 460, 14, 1)
    for i, (lab, v, col) in enumerate((('NORMAL DAY', 1.0, YEL), ('NOW', 1 / 40, (150, 150, 160)))):
        x = 330 + i * 420; hh = 700 * max(v, 0.02) * eout(ramp(t, 0.2 + i * 0.4, 1.0 + i * 0.4))
        rrect(img, x - 90, 1350 - hh, 180, max(4, hh), 10, col); text(img, lab, x, 1400, 34, WHITE, INTER_B)
    title_ = '40x DIMMER'; text(img, title_, W / 2, 400, 90, WHITE, ANT, alpha=ramp(t, 1.4, 1.7))
def c10(img, t, d):
    img[:] = (14, 12, 12)
    rrect(img, 290, 300, 500, 1000, 50, (40, 40, 44)); rrect(img, 306, 316, 468, 968, 40, (60, 55, 55))
    rrect(img, 306, 1060, 468, 224, 0, (220, 216, 212)); sundot(img, 600, 560, 10, 1)
    text(img, 'golden hour, kind of', W / 2, 1150, 36, INK, INTER_M); text(img, '#goldenhour', W / 2, 1200, 30, (200, 160, 80), INTER_M)
    emoji(img, '❤️', W / 2 - 60, 1360, 50); text(img, str(int(counter(t, 0.6, 2.4, 0, 3))), W / 2 + 20, 1360, 60, WHITE, INTER_B)
    flash(img, t, 0.3, 0.15, WHITE, 0.9)
def c11(img, t, d):
    img[:] = grad((50, 45, 45), (20, 18, 18))
    rrect(img, W / 2 - 60, 420, 120, 800, 60, (230, 230, 235)); circ(img, (W / 2, 1260), 110, (230, 230, 235))
    lv = 0.12 + 0.02 * math.sin(t * 2); rrect(img, W / 2 - 30, 1200 - 740 * lv, 60, 740 * lv, 30, (60, 60, 220)); circ(img, (W / 2, 1260), 80, (60, 60, 220))
    text(img, '−100 °F', W / 2 + 250, 1100, 70, WHITE, SERIF_I)
    if t > 2.0: text(img, 'TOO WEAK', W / 2, 330, 110, RED, ANT, scale=back(ramp(t, 2.0, 2.3)))
def c12(img, t, d):
    night(img, t); sundot(img, 260, 700, 16, 1); earth(img, 820, 1000, 70, t)
    k = ramp(t, 0.6, 2.4)
    for i in range(5):
        u = (t * 0.5 + i / 5) % 1; x = 820 - 520 * u; y = 1000 - 300 * u; circ(img, (x, y), 6, mix((60, 60, 60), YEL, k))
    text(img, '?', 820, 820, 140, WHITE, INTER_B, alpha=ramp(t, 2.6, 2.9))
def c13(img, t, d):
    img[:] = grad((40, 25, 20), (15, 10, 8))
    for i, (lab, v, col) in enumerate((('ESCAPE SPEED', 17, (120, 120, 130)), ('EARTH', 30, (60, 170, 255)))):
        y = 700 + i * 320; w = 760 * v / 30 * eout(ramp(t, 0.2 + i * 1.4, 1.2 + i * 1.4))
        rrect(img, 160, y, max(4, w), 120, 20, col); text(img, lab, 160 + twidth(lab, 40, INTER_B) / 2, y - 40, 40, WHITE, INTER_B)
        if w > 300: text(img, f'{v} KM/S', 160 + w - 130, y + 60, 56, WHITE, ANT)
    if t > 3.4: text(img, 'TOO FAST', W / 2, 1450, 120, RED, ANT, scale=back(ramp(t, 3.4, 3.7)))
def c14(img, t, d):
    night(img, t); sundot(img, 180, 1300, 12, 1)
    k = ease(ramp(t, 0, d)); ex = 300 + 600 * k; ey = 1150 - 700 * k
    for j in range(30):
        u = j / 30 * k; circ(img, (300 + 600 * u, 1150 - 700 * u + 60 * math.sin(u * 3)), 4, (60, 170, 255))
    earth(img, ex, ey, 60, t)
    hud(img, 'EARTH SPEED', f'{counter(t, 0.2, d, 30, 25):.0f} KM/S', 'SLOWING, NOT STOPPING', WHITE)
def c15(img, t, d):
    night(img, t); frozen_ground(img, 1500); sundot(img, 820, 480, 9 * (1 - 0.3 * ramp(t, 0, d)), 1)
    tripod(img, 560, 1500, 1.3); greg(img, 300, 1500, 1.3)
    k = back(ramp(t, 1.4, 1.7)); pill(img, W / 2, 330, 'LEAVING THE SOLAR SYSTEM', 46, INK, RED, dot=RED, alpha=min(1, max(0, k)))
def c16(img, t, d):
    night(img, t); r = 12 * (1 - 0.6 * ease(ramp(t, 0.2, d))); sundot(img, W / 2, 760, r, 1)
    for i, x in enumerate((240, 540, 840)):
        if t > 0.6 + i * 0.5: text(img, f'NIGHT {[1, 100, 1000][i]}', x, 1200, 40, (200, 200, 205), INTER_B)
def c17(img, t, d):
    night(img, t)
    for i, (lab, ch, col) in enumerate((('A · THIS SUN', '⭐', YEL), ('B · NO SUN', '🌑', (255, 170, 60)))):
        k = back(ramp(t, 0.1 + i * 0.25, 0.4 + i * 0.25)); x = 270 + i * 540
        if k > 0: rrect(img, x - 220 * k, 520, 440 * k, 560, 40, col)
        if k > 0.8: rrect(img, x - 210, 530, 420, 540, 34, INK); emoji(img, ch, x, 720, 200); text(img, lab, x, 950, 56, col, ANT)
    text(img, 'COMMENT A OR B', W / 2, 1180, 56, WHITE, INTER_B, alpha=ramp(t, 0.8, 1.1))

NOZOOM = (c6, c9, c13, c17)
def timeline(ls, dur):
    fs = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17]
    return [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'boom': [ls(2) + 0.2, ls(7) + 0.8, ls(12) + 3.4], 'whoosh': [ls(4), ls(5), ls(13)], 'pop': [ls(0) + 3.4, ls(9) + 0.6, ls(9) + 1.2, ls(14) + 1.4],
            'heart': [(ls(6), ls(7) + 0.8)], 'ding': [ls(2) + 0.4, ls(7) + 2.2], 'riser': [ls(11) + 1.0], 'end': ls(16) - 0.05}

POST = {
 'title': "The Sun Came Back After 1 Year... Too Late ☀️ Part 3 #shorts",
 'caption': "The Sun comes back after a year of darkness. Golden Hour Greg waits for his sunset... 53 minutes. Because Earth kept flying for a year, ~1 billion km out, and now it's going too fast for the Sun to ever pull it back 🌍💨 A Sun that comes back like this, or no Sun at all? Comment A or B 👇",
 'tags': '#whatif #space #science #sun #physics #animation #part3',
 'source': "Thought experiment, physics: Earth's orbital speed ≈ 29.8 km/s; with no Sun it moves in a straight line, ≈ 9.4×10⁸ km in one year, ≈ 6.4 AU from the Sun (Jupiter orbits at 5.2 AU); light travel time ≈ 53 min; sunlight ∝ 1/r² ≈ 1/40; solar escape speed at 6.4 AU ≈ 42.1/√6.4 ≈ 16.7 km/s < 29.8 km/s, so Earth is not recaptured. Earlier parts: Live Science / Popular Science (−100 °F after a year). Greg is fictional.",
}
