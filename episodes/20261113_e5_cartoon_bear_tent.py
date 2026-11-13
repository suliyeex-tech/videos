import math, random
import cv2
from kit import *

FORMAT = 'cartoon'
SLUG = '2026-11-13-bear-in-your-tent'
TITLE = 'IF A BEAR OPENED YOUR TENT'; INFO = 'THE WOODS · 2:00 AM'
VOICE = 'hype'; CAPTION = 'karaoke'; TICKS = True; MOOD = {'style': 'funny', 'root': 58.27}; ZOOM = 1.3
LINES = [
 ("This is Tyler Trailmix. Outdoor influencer. Three hundred and twelve followers.", 0.15),
 ("Tonight's video: twenty-four hours alone in the woods.", 0.2),
 ("At 2 AM, something unzips his tent.", 0.25),
 ("It's a bear. And Tyler knows the rhyme. If it's brown, lie down.", 0.1),
 ("Stupid mistake.", 0.35),
 ("Fur color doesn't tell you the species. Black bears can be brown.", 0.15),
 ("And if a bear comes into your tent, park rangers say: don't play dead. Fight back.", 0.2),
 ("Run? Bad idea. Bears have been clocked at fifty-six kilometers an hour.", 0.15),
 ("Climb a tree? Also no. They climb better than you.", 0.2),
 ("So Tyler does the only logical thing...", 0.1),
 ("He goes live.", 0.25),
 ("Twelve viewers. Eleven type: fight back. One types: collab?", 0.3),
 ("Follow for part two.", 1.0),
]
CAPS = [
 ["THIS IS", "[TYLER TRAILMIX.]", "OUTDOOR INFLUENCER.", "[312] FOLLOWERS."], ["TONIGHT'S VIDEO:", "[24 HOURS]", "ALONE IN THE WOODS."],
 ["AT [2 AM,]", "SOMETHING", "{UNZIPS HIS TENT.}"], ["IT'S A {BEAR.}", "TYLER KNOWS", "THE RHYME:", "[IF IT'S BROWN,]", "[LIE DOWN.]"], ["!STUPID MISTAKE."],
 ["FUR COLOR", "{DOESN'T} TELL YOU", "THE SPECIES.", "BLACK BEARS", "CAN BE [BROWN.]"], ["IF A BEAR", "COMES [INTO YOUR TENT,]", "RANGERS SAY:", "{DON'T PLAY DEAD.}", "[FIGHT BACK.]"],
 ["RUN?", "{BAD IDEA.}", "BEARS HIT", "[56 KM/H.]"], ["CLIMB A TREE?", "{ALSO NO.}", "THEY CLIMB", "[BETTER THAN YOU.]"],
 ["SO TYLER DOES", "THE ONLY", "[LOGICAL THING...]"], ["HE GOES {LIVE.}"], ["[12 VIEWERS.]", "11 TYPE:", "[FIGHT BACK.]", "ONE TYPES:", "{COLLAB?}"], ["[FOLLOW]", "FOR PART TWO."]]
TY = Look(skin=SKINS[0], hair=(40, 90, 150), style='cap', shirt=(40, 150, 90), pants=(70, 90, 110), shoes=(40, 50, 70), extra='vest')
BEARC = (40, 75, 120); BEARD = (25, 50, 85)
rb = random.Random(2)
TREES = [(rb.uniform(-60, W + 60), rb.uniform(0.6, 1.3), rb.uniform(0, 6)) for _ in range(14)]

def forest(img, t, night=1.0):
    img[:] = grad(mix((200, 160, 110), (50, 25, 15), night), mix((220, 200, 160), (90, 50, 30), night))
    stars(img, t, 0.6 * night, ymax=700, base=mix((200, 160, 110), (50, 25, 15), night))
    circ(img, (850, 300), 60, mix((240, 250, 255), (220, 240, 250), night))
    for x, s, ph in sorted(TREES, key=lambda q: q[1]):
        c = mix((40, 90, 50), (20, 40, 25), night * (1.2 - s * 0.4))
        for k in range(3): poly(img, [(x - 120 * s + k * 20 * s, 1250 - k * 170 * s), (x, 1250 - (k + 1) * 220 * s - 80 * s), (x + 120 * s - k * 20 * s, 1250 - k * 170 * s)], c)
    img[1250:] = grad(mix((60, 110, 70), (25, 45, 30), night), mix((40, 80, 50), (15, 30, 20), night), 1250, H)
def tent(img, x, y, s=1.0, glowk=1.0, open_=0.0):
    if glowk: glow(img, x, y - 150 * s, int(380 * s), (60, 160, 255), 0.7 * glowk)
    poly(img, [(x - 260 * s, y), (x, y - 330 * s), (x + 260 * s, y)], (40, 120, 230))
    poly(img, [(x - 260 * s, y), (x, y - 330 * s), (x - 60 * s, y)], (30, 100, 200))
    poly(img, [(x - 60 * s, y), (x, y - 220 * s), (x + 60 * s + 80 * open_ * s, y)], mix((20, 60, 120), (10, 20, 30), open_))
def bear(img, x, y, s=1.0, stand=0.0, mouth=0.0, col=BEARC):
    """(x, y) = ground under the bear"""
    if stand < 0.5:
        ell(img, (x, y - 170 * s), 230 * s, 130 * s, col)
        for dx in (-150, -60, 70, 160): rrect(img, x + dx * s - 30 * s, y - 120 * s, 60 * s, 120 * s, 26 * s, mix(col, (0, 0, 0), 0.2))
        hx, hy = x + 220 * s, y - 230 * s
    else:
        rrect(img, x - 120 * s, y - 520 * s, 240 * s, 440 * s, 110 * s, col)
        for dx in (-70, 70): rrect(img, x + dx * s - 40 * s, y - 120 * s, 80 * s, 120 * s, 30 * s, mix(col, (0, 0, 0), 0.2))
        for sx in (-1, 1): line(img, (x + sx * 110 * s, y - 430 * s), (x + sx * 200 * s, y - 560 * s), col, 70 * s)
        hx, hy = x, y - 600 * s
    for sx in (-1, 1): circ(img, (hx + sx * 70 * s, hy - 75 * s), 36 * s, col); circ(img, (hx + sx * 70 * s, hy - 75 * s), 18 * s, BEARD)
    circ(img, (hx, hy), 100 * s, col); ell(img, (hx, hy + 40 * s), 56 * s, 44 * s, mix(col, (180, 210, 230), 0.4))
    circ(img, (hx, hy + 22 * s), 18 * s, INK)
    for sx in (-1, 1): circ(img, (hx + sx * 38 * s, hy - 20 * s), 11 * s, INK)
    if mouth: ell(img, (hx, hy + 62 * s), 26 * s, 22 * s * mouth, (40, 30, 120))
def followers(img, n, y=330, col=(255, 255, 255)):
    pill(img, W / 2, y, f'{n} FOLLOWERS', 44, INK, col, dot=(80, 80, 255))
def selfie(img, x, y, s=1.0):
    line(img, (x, y), (x + 120 * s, y - 160 * s), (80, 80, 80), 10 * s); rrect(img, x + 95 * s, y - 230 * s, 60 * s, 100 * s, 10 * s, INK)

def a1(img, t, d):
    forest(img, t, 0.2); tent(img, 760, 1300, 0.9, 0)
    person(img, TY, 400, 960 + 6 * abs(math.sin(t * 5)), 1.15, 'smile', al=20, ar=150); selfie(img, 560, 1000)
    namecard(img, t, 'TYLER TRAILMIX', 'OUTDOOR INFLUENCER', 690, 640, at=0.4)
    followers(img, int(counter(t, 0.8, 2.6, 0, 312)), y=440 + (1 - eout(ramp(t, 0.6, 0.9))) * -200)
    header(img, eout(ramp(t, 0.05, 0.35)))
def a2(img, t, d):
    forest(img, t, 0.5 + 0.5 * ramp(t, 0, d)); tent(img, W / 2, 1300, 1.1, glowk=ramp(t, 0.5, 1.5))
    k = back(ramp(t, 0.2, 0.45)); rrect(img, W / 2 - 300 * k, 300, 600 * k, 130, 20, RED)
    if k > 0.8: text(img, '24H ALONE IN THE WOODS', W / 2, 365, 54, WHITE, ANT)
    emoji(img, '🏕️', 860, 560, 120 * k)
def a3(img, t, d):
    forest(img, t, 1.0); tent(img, W / 2, 1300, 1.2, glowk=1, open_=ramp(t, 0.6, 1.6))
    if t > 0.8: text(img, 'ZZZZIIIP', W / 2, 520, 120, YEL, ANT, scale=0.6 + 0.4 * back(ramp(t, 0.8, 1.0)), stroke=8, scol=INK)
    pill(img, W / 2, 330, '2:00 AM', 54, INK, WHITE, dot=RED)
def a4(img, t, d):
    forest(img, t, 1.0); tent(img, 220, 1300, 0.7, glowk=1, open_=1)
    bear(img, 650, 1330, 1.0, stand=1.0 if t > 0.7 else 0.0, mouth=0.4 + 0.4 * math.sin(t * 8))
    if t > 0.7: flash(img, t, 0.7, 0.12, WHITE, 0.6)
    if t > 2.0:
        k = back(ramp(t, 2.0, 2.25)); rrect(img, W / 2 - 330 * k, 300, 660 * k, 120, 22, INK)
        if k > 0.8: text(img, '"IF IT\'S BROWN, LIE DOWN"', W / 2, 360, 52, YEL, ANT)
def a5(img, t, d):
    img[:] = grad((40, 30, 180), (20, 10, 70)); vignette(img, 0.5)
    rotated(img, lambda c: person(c, TY, W / 2, 620, 1.3, 'closed', al=170, ar=170), (W / 2, 900), 90)
    flash(img, t, 0, 0.12, WHITE, 0.8)
def a6(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    for i, (lab, col) in enumerate((('BLACK BEAR', (40, 60, 95)), ('ALSO A BLACK BEAR', (70, 30, 30)))):
        x = 290 + i * 500; k = back(ramp(t, 0.3 + i * 0.6, 0.6 + i * 0.6))
        if k > 0: bear(img, x, 1000, 0.55 * k, stand=0, col=col if i == 0 else BEARC); text(img, lab, x, 1060, 46, INK, ANT, alpha=k)
    fact(img, t, 'BLACK BEARS CAN BE BROWN, CINNAMON OR BLOND', 1.5, y=380, size=34)
def a7(img, t, d):
    rule_card(img, t, d, "DON'T PLAY DEAD", 'FIGHT BACK.', bg=lambda im, tt: forest(im, tt, 1.0))
    fact(img, t, 'NPS: BEAR IN YOUR TENT = FIGHT BACK', 1.2, y=860)
def a8(img, t, d):
    forest(img, t, 1.0); streaks(img, t, 0.7, (200, 200, 200))
    person(img, TY, 300 + 140 * t, 980, 1.0, 'scream', al=120 + 40 * math.sin(t * 20), ar=120 - 40 * math.sin(t * 20))
    bear(img, -150 + 200 * t, 1330, 0.75, stand=0, mouth=0.8)
    statbox(img, t, 'BEAR TOP SPEED', f'{int(counter(t, 0.2, 1.4, 0, 56))} KM/H', RED)
def a9(img, t, d):
    forest(img, t, 1.0)
    rrect(img, 520, 500, 80, 830, 10, (40, 60, 90))
    person(img, TY, 560, 620, 0.8, 'scream', al=170, ar=170)
    bear(img, 600, 1330, 0.8, stand=1.0, mouth=0.6)
    k = back(ramp(t, 0.5, 0.8)); text(img, 'NOPE', W / 2, 360, 150, RED, ANT, scale=k, stroke=10, scol=INK)
def a10(img, t, d):
    forest(img, t, 1.0); tent(img, W / 2, 1300, 1.1, glowk=1, open_=1)
    for k in range(3): text(img, '?', 700 + k * 60, 700 - 30 * math.sin(t * 4 + k), 120, YEL, ANT, alpha=ramp(t, 0.2 + k * 0.2, 0.4 + k * 0.2))
def a11(img, t, d):
    forest(img, t, 1.0); bear(img, 800, 1330, 0.7, stand=1.0, mouth=0.3)
    person(img, TY, 330, 950, 1.1, 'smile', al=20, ar=150); selfie(img, 490, 990)
    k = back(ramp(t, 0.1, 0.35)); rrect(img, W / 2 - 200 * k, 300, 400 * k, 110, 22, RED)
    if k > 0.8: circ(img, (W / 2 - 95, 355), 16, WHITE); text(img, 'LIVE', W / 2 + 25, 355, 70, WHITE, ANT)
def a12(img, t, d):
    img[:] = grad((40, 30, 30), (20, 15, 15))
    rrect(img, 120, 250, 840, 110, 22, RED); circ(img, (330, 305), 14, WHITE); text(img, 'LIVE   12 VIEWERS', W / 2 + 30, 305, 52, WHITE, ANT)
    msgs = [('hikerdave', 'FIGHT BACK'), ('gran_ola', 'fight back!!'), ('xX_bearX', 'FIGHT BACK BRO'), ('mel.outdoors', 'fight back'),
            ('trailqueen', 'FIGHT BACK'), ('ranger_rick', 'fight back. we said this'), ('josh', 'fight back'), ('ana', 'FIGHT BACK!!!'),
            ('kev', 'fight back'), ('lulu', 'FIGHT BACK'), ('pete', 'fight back'), ('brandbro_mgmt', 'collab? 👀')]
    n = int(ramp(t, 0, d - 0.6) * len(msgs)) + 1
    for i, (u, m) in enumerate(msgs[:n]):
        y = 420 + i * 66; last = i == len(msgs) - 1
        if y > 1250: continue
        k = back(ramp(t, (i) * (d - 0.6) / len(msgs), (i) * (d - 0.6) / len(msgs) + 0.15))
        text(img, u, 160 + twidth(u, 40, INTER_B) / 2, y, 40, YEL if last else (170, 170, 175), INTER_B, alpha=k)
        text(img, m, 160 + twidth(u, 40, INTER_B) + 30 + twidth(m, 40, INTER_M) / 2, y, 40, RED if last else WHITE, INTER_M, alpha=k)
    if n >= len(msgs): emoji(img, '🤝', 880, 1150, 120)
def end_char(img, t):
    img[1500:1720] = (40, 80, 50); bear(img, 720, 1700, 0.35, stand=1.0); person(img, TY, 380, 1440, 0.45, 'scream', al=160, ar=160)
def a13(img, t, d): end_card(img, t, d, "TYLER VS THE BEAR", end_char)

NOZOOM = (a5, a13, a12, a6)
def timeline(ls, dur):
    fs = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13]
    return [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'pop': [ls(0) + 2.6], 'snap': [ls(2) + 0.8], 'boom': [ls(3) + 0.7, ls(6) + 0.2], 'mistake': ls(4),
            'heart': [(ls(7), ls(9))], 'notif': [ls(11) + k * dur(11) / 12 for k in range(12)], 'end': ls(12) - 0.05}

POST = {
 'title': "If A Bear Opened Your Tent, DON'T Do This 🐻 Part 1 #shorts",
 'caption': "Outdoor influencer Tyler Trailmix (312 followers) vs a bear at 2 AM. He remembered the rhyme... and that was the mistake. 🐻 Would you know what to do?",
 'tags': '#whatif #bear #survival #camping #funny #animation',
 'source': 'Source: US National Park Service bear safety guidance (bear in your tent: fight back; bears reach ~35 mph; black bears can be brown).',
}
