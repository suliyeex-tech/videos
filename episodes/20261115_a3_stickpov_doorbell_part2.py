import math, random
import numpy as np, cv2
from kit import *
from stickpov import *
import stickpov as S

FORMAT = 'stickpov'
SLUG = '2026-11-15-pov-doorbell-part2'
VOICE = 'storyuk'; SPEED = 1.25; CAPTION = 'karaoke'; MOOD = {'style': 'tension', 'root': 46.25}; ZOOM = 1.2; PROGRESS_COL = RED
VOICE_SPEED = {'girl': 1.22}
S.HUD.update({'clock': (3, 9), 'tag': 'SATURDAY', 'place': 'YOUR PORCH'})
LINES = [
 ("Nobody voted. So you chose A. You open the front door.", 0.3),
 ("3:09 AM. Cold air. The porch is empty.", 0.2),
 ("No footprints. No hoodie. Just one thing on the doormat.", 0.2),
 ("Your phone. Same crack. Same case. Still warm.", 0.25),
 ("But your phone is in your hand.", 0.35),
 ("The phone on the mat is recording. Live.", 0.2),
 ("You pick it up. On the screen: your bedroom. Filmed from inside.", 0.2),
 ("Your bed. Your lamp. And your bedroom door, slowly opening.", 0.3),
 ("But nobody is home. You're on the porch.", 0.35),
 ("Then the stream title changes. Live: my neighbor has a twin.", 0.2),
 ("It's not your stream. It's Nina's.", 0.3),
 ("Don't freak out. I've been filming your window all week.", 0.2, 'girl'),
 ("There are two of you. One sleeps. One waits by the door.", 0.3, 'girl'),
 ("You look up at Nina's house. Every window is dark.", 0.25),
 ("On the stream, the other you sits on your bed. And looks right into the lens.", 0.3),
 ("Behind you, your front door clicks shut. Locked. From the inside.", 0.4),
 ("Your lock screen turns into a countdown. Twenty-three hours, fifty-eight minutes. Until Sunday, 3:07.", 0.3),
 ("Ring the doorbell of your own house, or call Nina? Comment A or B. Part three decides.", 1.2),
]
CAPS = [
 ["NOBODY VOTED.", "SO YOU CHOSE [A.]", "YOU {OPEN THE DOOR.}"], ["[3:09 AM.]", "COLD AIR.", "THE PORCH IS {EMPTY.}"],
 ["NO FOOTPRINTS.", "NO HOODIE.", "JUST [ONE THING]", "ON THE {DOORMAT.}"], ["YOUR PHONE.", "SAME CRACK.", "SAME CASE.", "{STILL WARM.}"],
 ["BUT YOUR PHONE", "IS {IN YOUR HAND.}"], ["THE PHONE", "ON THE MAT", "IS RECORDING.", "{LIVE.}"],
 ["YOU PICK IT UP.", "ON THE SCREEN:", "[YOUR BEDROOM.]", "{FILMED FROM INSIDE.}"], ["YOUR BED.", "YOUR LAMP.", "YOUR BEDROOM DOOR,", "{SLOWLY OPENING.}"],
 ["BUT {NOBODY}", "IS HOME.", "YOU'RE [ON THE PORCH.]"], ["THE STREAM TITLE", "CHANGES.", "LIVE: MY NEIGHBOR", "HAS A {TWIN.}"],
 ["IT'S NOT", "YOUR STREAM.", "IT'S [NINA'S.]"], ["DON'T FREAK OUT.", "I'VE BEEN FILMING", "YOUR WINDOW", "{ALL WEEK.}"],
 ["THERE ARE", "{TWO OF YOU.}", "ONE SLEEPS.", "ONE [WAITS BY THE DOOR.]"], ["YOU LOOK UP", "AT NINA'S HOUSE.", "EVERY WINDOW", "IS {DARK.}"],
 ["THE OTHER YOU", "SITS ON YOUR BED.", "AND LOOKS", "{INTO THE LENS.}"], ["BEHIND YOU,", "THE FRONT DOOR", "CLICKS SHUT.", "{LOCKED.}", "FROM THE {INSIDE.}"],
 ["YOUR LOCK SCREEN:", "A [COUNTDOWN.]", "[23:58]", "UNTIL", "{SUNDAY, 3:07.}"], []]
YOU = (150, 150, 150); NINA = (200, 60, 160)
ST = {}
def T(f, t): return ST.get(f, 0) + t

def hand_phone(img, t, draw_screen, rise=1.0, x=W / 2, y=900):
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


NIGHT = (60, 30, 20)
def porch(img, t, mat_phone=0.0, door_open=1.0):
    """POV standing in the doorway looking out at the porch + street at night"""
    img[:] = grad((70, 36, 22), (40, 20, 14)); stars(img, t, 0.4, 900, (70, 36, 22))
    # houses across the street (Nina's in the middle)
    for i, (x, w, h) in enumerate(((-60, 360, 420), (330, 420, 520), (780, 360, 400))):
        y = 1000 - h; rrect(img, x, y, w, h, 4, (40, 26, 22)); poly(img, [(x - 20, y), (x + w / 2, y - 140), (x + w + 20, y)], (30, 20, 18))
        for wx in (x + 60, x + w - 130): rrect(img, wx, y + 100, 70, 90, 4, (25, 18, 16))
    rrect(img, 0, 1000, W, 120, 0, (50, 50, 55))   # street
    poly(img, [(0, 1120), (W, 1120), (W, H), (0, H)], (60, 70, 80))   # porch floor
    glow(img, 540, 1300, 520, (60, 90, 110), 0.8)
    # door frame edges (we stand in the doorway)
    rrect(img, 0, 0, 120, H, 0, (30, 40, 60)); rrect(img, W - 120, 0, 120, H, 0, (30, 40, 60)); rrect(img, 0, 0, W, 90, 0, (30, 40, 60))
    rrect(img, 380, 1500, 320, 120, 14, (50, 70, 100))   # doormat
    if mat_phone > 0:
        rrect(img, 490, 1510, 100, 90, 10, (30, 30, 34)); glow(img, 540, 1555, 140, (120, 90, 60), 0.8 * mat_phone)
        if int(t * 2) % 2 == 0: circ(img, (575, 1525), 7, RED)
def stream_screen(img, cx, cy, w, h, t, door=0.0, other=0.0, title='LIVE', who='Me'):
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    img[max(0, y0):min(H, y0 + int(h)), x0:x0 + int(w)] = (16, 14, 14)
    fx0, fy0, fw, fh = x0 + 10, y0 + 170, int(w) - 20, 470
    sub = np.zeros((fh, fw, 3), np.uint8); sub[:] = (36, 30, 34); sub[330:] = (30, 24, 28)
    cv2.rectangle(sub, (20, 250), (220, 340), (60, 50, 80), -1); cv2.rectangle(sub, (20, 230), (80, 270), (170, 160, 150), -1)   # bed + pillow
    cv2.rectangle(sub, (250, 200), (270, 330), (60, 60, 60), -1); cv2.circle(sub, (260, 190), 22, (120, 200, 240), -1)              # lamp
    dw = int(90 * (1 - door)); cv2.rectangle(sub, (290, 90), (370, 330), (8, 8, 8), -1); cv2.rectangle(sub, (290, 90), (290 + max(4, dw), 330), (70, 80, 100), -1)
    if other > 0:
        S2 = np.zeros_like(sub); hx, hy = 120, 170
        cv2.rectangle(S2, (hx - 30, hy + 30), (hx + 30, hy + 110), (150, 150, 150), -1); cv2.circle(S2, (hx, hy), 34, (20, 18, 18), -1)
        for sx in (-1, 1): cv2.ellipse(S2, (hx + sx * 11, hy - 2), (5, 8), 0, 0, 360, (255, 255, 255), -1)
        m = S2.any(2); sub[m] = (sub[m] * (1 - other) + S2[m] * other).astype(np.uint8)
    g = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY); rng = np.random.default_rng(int(t * 30)); g = np.clip(g + rng.normal(0, 7, g.shape), 0, 255).astype(np.uint8)
    sub = cv2.merge([g, (g * 1.1).clip(0, 255).astype(np.uint8), g])
    ya, yb = max(0, fy0), min(H, fy0 + fh)
    if yb > ya: img[ya:yb, fx0:fx0 + fw] = sub[ya - fy0:yb - fy0]
    rrect(img, x0 + 20, y0 + 40, 100, 44, 10, RED); text(img, 'LIVE', x0 + 70, y0 + 62, 30, WHITE, INTER_B)
    text(img, who, cx + 60, y0 + 62, 28, WHITE, INTER_B)
    text(img, title, cx, y0 + 125, 26 if twidth(title, 26, INTER_B) < w - 30 else 22, YEL, INTER_B)
    text(img, f'{int(1 + t * 3) % 9 + 1} watching', cx, y0 + 700, 26, (170, 170, 175), INTER_M)

def s1(img, t, d):
    img[:] = (12, 10, 10)
    k = back(ramp(t, 0.1, 0.35)); text(img, 'YOUR VOTES', W / 2, 600, 60, (170, 170, 175), INTER_B, alpha=min(1, k))
    text(img, '0', W / 2, 780, 260, RED, ANT, scale=k)
    if t > 1.4:
        q = back(ramp(t, 1.4, 1.7)); rrect(img, 150, 1000, 780, 130, 22, YEL); rrect(img, 156, 1006, 768, 118, 18, INK2)
        rrect(img, 180, 1029, 72, 72, 14, YEL); text(img, 'A', 216, 1065, 52, INK2, INTER_B); text(img, 'OPEN THE DOOR', 590, 1065, 52, WHITE, INTER_B, alpha=min(1, q))
    hud(img, ST[s1] + t)
def s2(img, t, d):
    porch(img, t, door_open=1.0); flash(img, t, 0, 0.2, WHITE, 0.5)
    for i in range(3): line(img, (300 + i * 200 + 40 * math.sin(t * 2 + i), 700 + 30 * i), (420 + i * 200 + 40 * math.sin(t * 2 + i), 690 + 30 * i), (200, 200, 210), 3)
    hud(img, ST[s2] + t)
def s3(img, t, d):
    porch(img, t, mat_phone=ramp(t, 1.6, 2.0))
    if t > 0.4: pill(img, W / 2, 360, 'FOOTPRINTS: 0', 44, INK2, WHITE, alpha=ramp(t, 0.4, 0.7))
    hud(img, ST[s3] + t)
def s4(img, t, d):   # close up phone on the mat
    porch(img, t, mat_phone=1.0)
    k = eout(ramp(t, 0, 0.5)); z = 0.4 + 0.6 * k
    rotated(img, lambda c: (rrect(c, 540 - 220 * z, 1050 - 440 * z, 440 * z, 880 * z, 60 * z, (30, 30, 34)),
                            rrect(c, 540 - 205 * z, 1050 - 425 * z, 410 * z, 850 * z, 50 * z, (110, 40, 60)),
                            line(c, (540 - 150 * z, 1050 - 300 * z), (540 + 120 * z, 1050 + 200 * z), (230, 230, 230), 4),
                            line(c, (540 - 40 * z, 1050 - 100 * z), (540 + 180 * z, 1050 - 260 * z), (230, 230, 230), 3)), (540, 1050), -8)
    for i, lab in enumerate(('SAME CRACK', 'SAME CASE', 'STILL WARM')):
        if t > 0.9 + i * 0.6: pill(img, W / 2, 330 + i * 100, lab, 40, INK2, YEL if i < 2 else RED, alpha=ramp(t, 0.9 + i * 0.6, 1.1 + i * 0.6))
def s5(img, t, d):   # but your phone is in your hand
    porch(img, t, mat_phone=1.0)
    hand_phone(img, t, lambda im, cx, cy, w, h: lock_screen(im, cx, cy, w, h, '3:09', 'Saturday'), rise=ramp(t, 0, 0.35), x=740, y=1060)
    if t > 1.0: text(img, '2 PHONES', 330, 560, 120, RED, ANT, scale=back(ramp(t, 1.0, 1.25)), stroke=8, scol=INK2)
def s6(img, t, d):   # recording live
    porch(img, t, mat_phone=1.0); sx, sy = (0, 0)
    k = back(ramp(t, 0.1, 0.4)); rrect(img, 380, 1330 - 60 * k, 320 * k, 90, 20, RED)
    if k > 0.8: circ(img, (420, 1315), 12, WHITE); text(img, 'REC · LIVE', 560, 1315, 44, WHITE, INTER_B)
    hud(img, ST[s6] + t, red=True)
def s7(img, t, d):   # the stream of your bedroom (lines 6-7)
    porch(img, t); tint(img, (0, 0, 0), 0.5)
    rel = ST[s7] + t
    door = ease(ramp(rel, ST.get('l7', 99) + 1.8, ST.get('l7', 99) + 3.6))
    hand_phone(img, t, lambda im, cx, cy, w, h: stream_screen(im, cx, cy, w, h, rel, door, 0, 'LIVE · front door cam', 'unknown'), rise=ramp(t, 0, 0.35))
    hud(img, rel, red=door > 0.1)
def s8(img, t, d):   # you alone on the porch (3rd person)
    porch(img, t); tint(img, (0, 0, 0), 0.2)
    stick(img, 540, 1560, 0.95, YOU, 'shock', 0, arm='phone')
    if t > 0.8: pill(img, W / 2, 360, 'HOME: NOBODY', 48, INK2, RED, alpha=ramp(t, 0.8, 1.1))
    hud(img, ST[s8] + t, red=True)
def s9(img, t, d):   # title changes
    porch(img, t); tint(img, (0, 0, 0), 0.5); rel = ST[s9] + t
    ch = t > ST.get('l9d', 1.5)
    hand_phone(img, t, lambda im, cx, cy, w, h: stream_screen(im, cx, cy, w, h, rel, 1.0, 0, 'LIVE: my neighbor has a twin??' if ch else 'LIVE · front door cam', 'Nightcam Nina' if t > ST.get('l10', 99) - ST[s9] else 'unknown'), rise=1.0)
    hud(img, rel, red=True)
def s10(img, t, d):   # Nina's chat
    porch(img, t); tint(img, (0, 0, 0), 0.6); rel = ST[s10] + t
    hand_phone(img, t, lambda im, cx, cy, w, h: chat_screen(im, cx, cy, w, h, 'Nightcam Nina', NINA_MSGS, rel), rise=1.0)
    hud(img, rel, red=True)
def s11(img, t, d):   # Nina's house, dark
    porch(img, t); k = eout(ramp(t, 0, 1.6)); M = cv2.getRotationMatrix2D((540, 760), 0, 1 + 0.9 * k); img[:] = cv2.warpAffine(img, M, (W, H))
    if t > 1.6: pill(img, W / 2, 360, "NINA'S HOUSE · ALL DARK", 44, INK2, WHITE, alpha=ramp(t, 1.6, 1.9))
    hud(img, ST[s11] + t, red=True)
def s12(img, t, d):   # other you on your bed
    porch(img, t); tint(img, (0, 0, 0), 0.6); rel = ST[s12] + t
    hand_phone(img, t, lambda im, cx, cy, w, h: stream_screen(im, cx, cy, w, h, rel, 1.0, ramp(t, 0.6, 1.4), 'LIVE: my neighbor has a twin??', 'Nightcam Nina'), rise=1.0)
    if t > 2.6: text(img, 'IT SEES YOU', W / 2, 470, 120, RED, ANT, scale=back(ramp(t, 2.6, 2.85)), stroke=8, scol=INK2)
    hud(img, rel, red=True)
def s13(img, t, d):   # door clicks shut behind you
    img[:] = (14, 12, 12); sx, sy = shake(t, 0.9, 0.4, 24)
    rrect(img, 240 + sx, 260 + sy, 600, 1300, 8, (50, 60, 80)); rrect(img, 270 + sx, 290 + sy, 540, 1270, 6, (40, 48, 66))
    circ(img, (740 + sx, 960 + sy), 22, (160, 170, 180))
    if t > 0.9: text(img, 'CLICK', W / 2, 760, 180, YEL, ANT, scale=back(ramp(t, 0.9, 1.1)), stroke=10, scol=INK2)
    if t > 2.2: emoji(img, '🔒', W / 2, 1100, 200 * back(ramp(t, 2.2, 2.5)))
    flash(img, t, 0.9, 0.12, WHITE, 0.5)
    hud(img, ST[s13] + t, red=True)
def s14(img, t, d):   # countdown
    porch(img, t); tint(img, (0, 0, 0), 0.6); rel = ST[s14] + t
    secs = 23 * 3600 + 58 * 60 - int(max(0, t - 1.2) * 1)
    def scr(im, cx, cy, w, h):
        lock_screen(im, cx, cy, w, h, '3:10', 'Saturday')
        if t > 1.0:
            rrect(im, cx - w / 2 + 20, cy - 20, w - 40, 260, 24, (20, 20, 40))
            text(im, 'UNTIL SUNDAY 3:07', cx, cy + 30, 30, RED, INTER_B)
            text(im, f'{secs // 3600}:{secs % 3600 // 60:02d}:{secs % 60:02d}', cx, cy + 130, 90, WHITE, INTER_B)
    hand_phone(img, t, scr, rise=1.0)
    hud(img, rel, red=True)
def bg_end(img, t): porch(img, t)
def s15(img, t, d): choice_end(img, t, 'RING YOUR DOORBELL', 'CALL NINA', 'PART 3', bg=bg_end)

NOZOOM = (s15, s1)
NINA_MSGS = []
def timeline(ls, dur):
    fs = [s1, s2, s3, s4, s5, s6, s7, None, s8, s9, None, s10, None, s11, s12, s13, s14, s15]
    tl = [((0 if i == 0 else ls(i) - 0.05), f) for i, f in enumerate(fs) if f is not None]
    for a, f in tl: ST[f] = round(a * 30) / 30
    ST['l7'] = ls(7) - ST[s7]; ST['l9d'] = dur(9) * 0.45; ST['l10'] = ls(10)
    NINA_MSGS[:] = [('l', "don't freak out", ls(11)), ('l', 'been filming ur window', ls(11) + 1.2), ('l', 'all week', ls(11) + 2.0), ('l', 'there are 2 of you', ls(12)),
                    ('l', 'one sleeps', ls(12) + 1.6), ('l', 'one waits by the door', ls(12) + 2.4)]
    return tl
def SFX(ls, dur):
    return {'hook_end': ls(1), 'notif': [ls(11), ls(11) + 1.2, ls(11) + 2.0, ls(12), ls(12) + 1.6, ls(12) + 2.4], 'whoosh': [ls(1), ls(6), ls(13)],
            'boom': [ls(4) + 0.3, ls(9) + dur(9) * 0.45, ls(14) + 2.6, ls(15) + 0.9], 'heart': [(ls(6), ls(9)), (ls(14), ls(16))], 'riser': [ls(15) + 0.8],
            'pop': [ls(0) + 1.4, ls(3) + 0.9, ls(3) + 1.5, ls(3) + 2.1, ls(5) + 0.1], 'end': ls(17) - 0.05}

POST = {
 'title': "POV: Your Doorbell Camera Shows... YOU 🚪 Part 2 #shorts",
 'caption': "Part 2: nobody voted, so you opened the front door. The porch is empty... except for YOUR phone, live-streaming your bedroom from inside 😨 And your neighbor Nightcam Nina knows why. Ring your own doorbell or call Nina? Comment A or B, Part 3 decides 👇",
 'tags': '#pov #creepy #horrorstory #storytime #animation #choices #part2',
 'source': 'Original fiction. All characters are fictional.',
}
