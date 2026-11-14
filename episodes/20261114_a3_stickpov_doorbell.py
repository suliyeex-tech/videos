import math, random
import numpy as np, cv2
from kit import *
from stickpov import *
import stickpov as S

FORMAT = 'stickpov'
SLUG = '2026-11-14-pov-your-doorbell-camera-shows-you'
VOICE = 'suspense'; SPEED = 1.17; CAPTION = 'karaoke'; MOOD = {'style': 'tension', 'root': 46.25}; ZOOM = 1.2; PROGRESS_COL = RED
VOICE_SPEED = {'girl': 1.2}
S.HUD.update({'clock': (3, 7), 'tag': 'SATURDAY', 'place': 'YOUR HOUSE'})
LINES = [
 ("3:07 AM. Your phone buzzes. Doorbell camera. Motion at your front door.", 0.15),
 ("You live alone. You open the app.", 0.2),
 ("Someone is standing on your porch. Grey hoodie. Just like yours.", 0.2),
 ("Then they turn to the camera. And it's you.", 0.3),
 ("Same face. Same hoodie. Same cracked phone in their hand.", 0.15),
 ("It looks straight into the lens. And it smiles. You are not smiling.", 0.25),
 ("You look down. You're in bed. Wearing that exact hoodie.", 0.2),
 ("A text from your neighbor, Nightcam Nina. True crime streamer. Never sleeps.", 0.15),
 ("Why are you outside? I can see you from my window.", 0.15, 'girl'),
 ("You type: I'm in bed.", 0.2),
 ("She replies: Then who is waving at me?", 0.3, 'girl'),
 ("You check the camera. It is waving. Not at Nina. At you.", 0.25),
 ("On the camera, the other you is holding up its phone. The lock screen says three oh seven. Sunday.", 0.2),
 ("But today is Saturday.", 0.3),
 ("Whatever is on your porch... is from tomorrow.", 0.3),
 ("The doorbell rings.", 0.3),
 ("Then a text. From your own number. Don't open it. I'm the real one.", 0.2),
 ("And one more from Nina: It's not on the porch anymore.", 0.2),
 ("Down the hallway, something is breathing.", 0.25),
 ("Then the hallway light switches on. By itself.", 0.3),
 ("Open the front door, or check the hallway? Comment A or B. Part two decides.", 1.8),
]
CAPS = [
 ["[3:07 AM.]", "YOUR PHONE BUZZES.", "{DOORBELL CAMERA.}", "MOTION AT", "YOUR FRONT DOOR."], ["YOU LIVE", "{ALONE.}", "YOU OPEN THE APP."],
 ["SOMEONE IS", "ON YOUR PORCH.", "[GREY HOODIE.]", "{JUST LIKE YOURS.}"], ["THEY TURN", "TO THE CAMERA.", "AND IT'S", "{YOU.}"],
 ["SAME FACE.", "SAME HOODIE.", "SAME [CRACKED PHONE.]"], ["IT LOOKS", "INTO THE LENS.", "AND IT {SMILES.}", "YOU'RE [NOT.]"], ["YOU LOOK DOWN.", "YOU'RE [IN BED.]", "WEARING THAT", "{EXACT HOODIE.}"],
 ["A TEXT FROM", "[NIGHTCAM NINA.]", "TRUE CRIME STREAMER.", "{NEVER SLEEPS.}"], ["WHY ARE YOU", "{OUTSIDE?}", "I CAN SEE YOU."],
 ["YOU TYPE:", "[I'M IN BED.]"], ["THEN WHO", "IS {WAVING}", "AT ME?"],
 ["IT IS {WAVING.}", "NOT AT NINA.", "{AT YOU.}"], ["THE OTHER YOU", "HOLDS UP", "ITS PHONE.", "[3:07.]", "{SUNDAY.}"], ["BUT TODAY", "IS {SATURDAY.}"], ["WHATEVER IS", "ON YOUR PORCH...", "IS FROM {TOMORROW.}"], ["!DING DONG."],
 ["A TEXT", "FROM [YOUR OWN NUMBER.]", "{DON'T OPEN IT.}", "I'M THE REAL ONE."], ["NINA:", "IT'S {NOT ON THE PORCH}", "ANYMORE."],
 ["DOWN THE HALLWAY,", "SOMETHING IS", "{BREATHING.}"], ["THE HALLWAY LIGHT", "SWITCHES ON.", "{BY ITSELF.}"], []]
YOU = (150, 150, 150); NINA = (200, 60, 160)
ST = {}
def T(f, t): return ST.get(f, 0) + t

def hand_phone(img, t, draw_screen, rise=1.0, x=W / 2, y=1020):
    oy = (1 - eout(rise)) * 900
    line(img, (x + 160, y + 380 + oy), (x + 420, y + 900 + oy), YOU, 120)
    rrect(img, x - 230, y - 470 + oy, 460, 940, 70, (30, 30, 34)); rrect(img, x - 214, y - 454 + oy, 428, 908, 58, (18, 14, 14))
    rrect(img, x - 60, y - 440 + oy, 120, 30, 15, (30, 30, 34)); circ(img, (x + 170, y + 380 + oy), 70, (150, 185, 232))
    draw_screen(img, x, y + oy, 400, 860)
def bedroom(img, t, dark=0.0, glowk=1.0):
    img[:] = mix((60, 45, 40), (14, 10, 10), dark); img[1350:] = mix((50, 40, 45), (12, 10, 10), dark)
    rrect(img, 700, 380, 260, 330, 10, (30, 22, 20)); cv2.rectangle(img, P(712, 392), P(948, 698), (90, 60, 40), 3, cv2.LINE_AA, 3)
    circ(img, (840, 470), 40, (200, 210, 220))   # moon in the window
    for k in range(2): line(img, (830, 392), (830, 698), (40, 30, 30), 6)
def bed_front(img):
    rrect(img, 120, 1150, 840, 260, 30, (120, 70, 50)); rrect(img, 100, 1100, 880, 120, 40, (180, 160, 150))
    rrect(img, 80, 1000, 60, 420, 20, (60, 40, 30))
def cam(img, t, draw, label='FRONT DOOR', stamp='SAT 3:07:12 AM', zoom=1.0, glitch=0.0):
    c = np.zeros_like(img); c[:] = (40, 40, 40)
    # porch: door, frame, mat, wall light
    rrect(c, 300, 300, 480, 1200, 6, (70, 70, 70)); rrect(c, 330, 330, 420, 1170, 4, (50, 50, 50))
    c[1500:] = (85, 85, 85); rrect(c, 380, 1500, 320, 60, 10, (60, 60, 60))
    glow(c, 880, 520, 260, (90, 90, 90), 1.0); rrect(c, 860, 470, 40, 80, 10, (200, 200, 200))
    draw(c)
    if zoom != 1.0:
        M = cv2.getRotationMatrix2D((W / 2, 900), 0, zoom); c = cv2.warpAffine(c, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
    g = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY).astype(np.float32)
    rng = np.random.default_rng(int(t * 30)); g = g + rng.normal(0, 9, g.shape)
    yy, xx = np.mgrid[0:H, 0:W]; v = 1 - 0.65 * (((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2)
    g = np.clip(g * v * 1.5, 0, 255)
    img[:, :, 0] = (g * 0.45).astype(np.uint8); img[:, :, 1] = g.astype(np.uint8); img[:, :, 2] = (g * 0.5).astype(np.uint8)
    img[::4] = (img[::4] * 0.8).astype(np.uint8)
    if glitch > 0:
        for k in range(6):
            y = random.randint(0, H - 60); sh = random.randint(-80, 80); img[y:y + 50] = np.roll(img[y:y + 50], sh, axis=1)
    circ(img, (80, 330), 14, RED if int(t * 2) % 2 == 0 else (60, 60, 60))
    text(img, 'REC', 145, 330, 34, WHITE, INTER_B); text(img, label, W - 60 - twidth(label, 34, INTER_B) / 2, 330, 34, WHITE, INTER_B)
    text(img, stamp, W - 60 - twidth(stamp, 34, INTER_B) / 2, 380, 34, WHITE, INTER_B)
def back_stick(c, x, y, s=1.0):
    stick(c, x, y, s, (150, 150, 150), 'closed', 0); circ(c, (x, y - 560 * s), 88 * s, (18, 16, 16))
    ell(c, (x, y - 600 * s), 96 * s, 60 * s, (150, 150, 150), 180, 360)

def s1(img, t, d):
    bedroom(img, t, 0.8)
    hand_phone(img, t, lambda im, cx, cy, w, h: lock_screen(im, cx, cy, w, h, '3:07', 'Saturday', note='Motion at Front Door' if t > 0.4 else None), rise=ramp(t, 0, 0.3))
    hud(img, T(s1, t))
def s2(img, t, d):
    bedroom(img, t, 0.7); stick(img, 540, 1450, 1.0, YOU, 'flat', look=1 if t > 1 else 0); bed_front(img)
    glow(img, 650, 900, 200, (120, 90, 60), 0.9)
    hud(img, T(s2, t))
def s3(img, t, d): cam(img, t, lambda c: back_stick(c, 540, 1520, 1.15 + 0.03 * t))
def s4(img, t, d):
    turned = t > 1.3
    def dr(c):
        if turned: stick(c, 540, 1520, 1.15, YOU, 'flat', 0)
        else: back_stick(c, 540, 1520, 1.15)
    cam(img, t, dr, zoom=1.0 + 0.5 * ease(ramp(t, 1.3, d)), glitch=1.0 if 1.3 < t < 1.6 else 0)
    if t > 1.9: text(img, "IT'S YOU", W / 2, 560, 150, RED, ANT, scale=back(ramp(t, 1.9, 2.1)), stroke=10, scol=INK2)
def s5(img, t, d):
    cam(img, t, lambda c: stick(c, 540, 1700, 1.6, YOU, 'flat', 0, arm='phone'), zoom=1.3)
    for i, lab in enumerate(('SAME FACE', 'SAME HOODIE', 'SAME CRACKED PHONE')):
        k = back(ramp(t, 0.2 + i * 0.9, 0.45 + i * 0.9))
        if k > 0: rrect(img, 120, 480 + i * 110, 560 * k, 90, 20, INK2); text(img, '✓ ' .replace('✓ ', '') + lab, 120 + 280 * k, 525 + i * 110, 42, YEL, INTER_B, alpha=min(1, k))
def s5b(img, t, d):
    def dr(c):
        stick(c, 540, 1900, 2.2, YOU, 'happy', 0)
        ell(c, (540, 1900 - 560 * 2.2 + 50 * 2.2), 60 * ramp(t, 0.6, 1.2), 30, WHITE, 0, 180)
    cam(img, t, dr, zoom=1.0 + 0.15 * t, glitch=1.0 if 2.2 < t < 2.4 else 0)
def s6(img, t, d):
    bedroom(img, t, 0.7); stick(img, 540, 1330, 1.0, YOU, 'shock', look=0); bed_front(img)
    k = ramp(t, 0.6, 1.0); cv2.circle(img, P(540, 1000), int(240 * 8), RED, 8, cv2.LINE_AA, 3) if k > 0 else None
    hud(img, T(s6, t), red=True)
NINA_MSGS = []
def phone_chat(img, t, a, upto):
    def scr(im, cx, cy, w, h): chat_screen(im, cx, cy, w, h, 'Nightcam Nina', [m for m in NINA_MSGS[:upto]], a + t)
    hand_phone(img, t, scr, rise=1.0)
def s7(img, t, d):
    bedroom(img, t, 0.85)
    stick(img, 760, 1000 + 20 * math.sin(t * 2), 0.55, NINA, 'happy', look=-1, arm='phone')
    rrect(img, 560, 360, 420, 110, 20, RED); circ(img, (600, 415), 12, WHITE); text(img, 'LIVE · TRUE CRIME', 790, 415, 34, WHITE, INTER_B)
    namecard(img, t, 'NIGHTCAM NINA', 'TRUE CRIME STREAMER · NEVER SLEEPS', W / 2, 1180, at=0.5)
    hud(img, T(s7, t))
def s8(img, t, d): bedroom(img, t, 0.9); phone_chat(img, t, ST[s8], 1); hud(img, T(s8, t))
def s9(img, t, d): bedroom(img, t, 0.9); phone_chat(img, t, ST[s9], 2); hud(img, T(s9, t))
def s10(img, t, d): bedroom(img, t, 0.9); phone_chat(img, t, ST[s10], 3); hud(img, T(s10, t), red=True)
def s10b(img, t, d):
    def dr(c):
        up = int(t * 3) % 2 == 0
        stick(c, 540, 1520, 1.15, YOU, 'happy', 0, arm='up' if up else None)
    cam(img, t, dr, zoom=1.0 + 0.4 * ease(ramp(t, 1.5, d)))
    if t > 1.6: text(img, 'AT YOU', W / 2, 560, 140, RED, ANT, scale=back(ramp(t, 1.6, 1.8)), stroke=10, scol=INK2)
def s11(img, t, d):
    def dr(c):
        stick(c, 540, 1520, 1.15, YOU, 'happy', 0, arm='up')
        rrect(c, 640, 760, 150, 260, 20, (230, 230, 230)); text(c, '3:07', 715, 860, 56, INK2, INTER_B); text(c, 'SUNDAY', 715, 940, 30, INK2, INTER_B)
    cam(img, t, dr, zoom=1.0 + 0.6 * ease(ramp(t, 1.0, d)))
def s12(img, t, d):
    img[:] = (10, 10, 12)
    for i, (lab, day, col) in enumerate((('TODAY', 'SATURDAY', WHITE), ('THE CLIP', 'SUNDAY', RED))):
        k = back(ramp(t, 0.1 + i * 0.5, 0.35 + i * 0.5)); y = 700 + i * 360
        text(img, lab, W / 2, y - 90, 44, (170, 170, 175), INTER_B, alpha=min(1, k)); text(img, day, W / 2, y + 20, 150, col, ANT, scale=k)
    hud(img, T(s12, t), red=True)
def s13(img, t, d):
    bedroom(img, t, 0.95); sx, sy = shake(t, 0.05, 1.0, 26)
    text(img, 'DING', W / 2 + sx, 640 + sy, 200, YEL, ANT, scale=back(ramp(t, 0.05, 0.25)), stroke=10, scol=INK2)
    text(img, 'DONG', W / 2 - sx, 860 - sy, 200, RED, ANT, scale=back(ramp(t, 0.5, 0.7)), stroke=10, scol=INK2)
    flash(img, t, 0.05, 0.12, WHITE, 0.6); flash(img, t, 0.5, 0.12, WHITE, 0.5)
    hud(img, T(s13, t), red=True)
def s14(img, t, d):
    bedroom(img, t, 0.95)
    def scr(im, cx, cy, w, h): chat_screen(im, cx, cy, w, h, 'Me', [('l', "Don't open it.", ST[s14] + 0.9), ('l', "I'm the real one.", ST[s14] + 2.3)], ST[s14] + t)
    hand_phone(img, t, scr, rise=ramp(t, 0, 0.3))
    if t > 0.5: pill(img, W / 2, 330, 'FROM: YOUR OWN NUMBER', 40, INK2, RED, dot=RED)
def s15(img, t, d): bedroom(img, t, 0.95); phone_chat(img, t, ST[s15], 4); hud(img, T(s15, t), red=True)
def hallway(img, t, k=1.0):
    img[:] = (10, 8, 8)
    poly(img, [(0, 0), (W, 0), (700, 700), (380, 700)], (24, 20, 20)); poly(img, [(0, H), (W, H), (700, 1200), (380, 1200)], (30, 26, 26))
    poly(img, [(0, 0), (380, 700), (380, 1200), (0, H)], (18, 15, 15)); poly(img, [(W, 0), (700, 700), (700, 1200), (W, H)], (18, 15, 15))
    rrect(img, 380, 700, 320, 500, 0, (6, 5, 5)); rrect(img, 470, 760, 150, 440, 4, (40, 34, 30))
def s16(img, t, d):
    hallway(img, t); b = 0.5 + 0.5 * math.sin(t * 3.2)
    for k in range(2): ell(img, (510 + k * 60, 940), 9, 5 + 4 * b, (230, 230, 240))
    glow(img, 540, 940, int(120 + 40 * b), (60, 60, 80), 0.6)
    hud(img, T(s16, t), red=True)
def s16b(img, t, d):
    hallway(img, t); on = t > 0.6 and not (0.9 < t < 1.0)
    if on:
        glow(img, 540, 600, 500, (120, 200, 230), 1.4); tint(img, (120, 200, 230), 0.12)
        circ(img, (540, 380), 30, (220, 245, 255))
        stick(img, 545, 1180, 0.55, YOU, 'happy', 0)
    flash(img, t, 0.6, 0.15, WHITE, 0.6)
    hud(img, T(s16b, t), red=True)
def bg_end(img, t): hallway(img, t)
def s17(img, t, d): choice_end(img, t, 'OPEN THE DOOR', 'CHECK THE HALLWAY', 'PART 2', bg=bg_end)

NOZOOM = (s17, s12)
def timeline(ls, dur):
    fs = [s1, s2, s3, s4, s5, s5b, s6, s7, s8, s9, s10, s10b, s11, s12, s12, s13, s14, s15, s16, s16b, s17]
    tl = [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
    tl = [x for i, x in enumerate(tl) if i != 14]
    for a, f in tl: ST[f] = round(a * 30) / 30
    NINA_MSGS[:] = [('l', 'why are you outside??', ls(8)), ('r', "i'm in bed", ls(9)), ('l', 'then who is waving at me', ls(10)), ('l', "it's not on the porch anymore", ls(17))]
    return tl
def SFX(ls, dur):
    return {'hook_end': ls(1), 'notif': [0.5, ls(8), ls(9), ls(10), ls(16) + 0.9, ls(16) + 2.3, ls(17)], 'boom': [ls(3) + 1.3, ls(5) + 2.2, ls(11) + 1.6, ls(13) + 0.2, ls(15) + 0.05, ls(15) + 0.5, ls(19) + 0.6],
            'whoosh': [ls(6)], 'heart': [(ls(10), ls(15)), (ls(18), ls(20))], 'riser': [ls(18)], 'pop': [ls(4) + 0.2, ls(4) + 1.1, ls(4) + 2.0], 'end': ls(20) - 0.05}

POST = {
 'title': "POV: Your Doorbell Camera Shows... YOU 🚪 Part 1 #shorts",
 'caption': "3:07 AM. Motion at your front door. It's you, in your hoodie, holding your phone. And its lock screen says Sunday 😨 Open the door or check the hallway? Comment A or B, Part 2 decides 👇",
 'tags': '#pov #creepy #horrorstory #storytime #animation #choices #part1',
 'source': 'Original fiction. All characters are fictional.',
}
