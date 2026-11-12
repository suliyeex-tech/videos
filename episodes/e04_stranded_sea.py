import math, random
import cv2
from kit import *

SLUG = '2026-11-12-stranded-at-sea'
TITLE = 'IF YOU WERE STRANDED AT SEA'
INFO = 'PACIFIC · DAY 1'
LINES = [
 ("If you were stranded in the middle of the ocean...", 0.10),
 ("the water all around you could kill you faster than thirst.", 0.30),
 ("This is Kai. He's twenty-six. His sailboat just sank, and all he has is a tiny raft.", 0.25),
 ("Survival experts use the rule of three.", 0.20),
 ("Three minutes without air. Three days without water. Three weeks without food.", 0.30),
 ("So water is his real clock.", 0.35),
 ("The rule: never drink seawater.", 0.30),
 ("Day two. Kai can't take it anymore, and gulps it down.", 0.15),
 ("Stupid mistake.", 0.40),
 ("Seawater is about three and a half percent salt. To flush it out, his kidneys need more water than he just drank.", 0.30),
 ("So every sip makes him thirstier.", 0.35),
 ("On day three, dark clouds finally roll in...", 0.25),
 ("but something big is circling the raft.", 0.50),
 ("Follow for part two.", 1.0),
]
CAPS = [
 ["IF YOU WERE", "{STRANDED}", "IN THE MIDDLE", "OF THE [OCEAN...]"], ["THE WATER", "[ALL AROUND YOU]", "COULD KILL YOU", "{FASTER THAN THIRST.}"],
 ["THIS IS [KAI.]", "HE'S [26.]", "HIS SAILBOAT", "{JUST SANK,}", "AND ALL HE HAS", "IS A [TINY RAFT.]"], ["SURVIVAL EXPERTS", "USE THE", "[RULE OF THREE.]"],
 ["[3 MINUTES]", "WITHOUT AIR.", "[3 DAYS]", "WITHOUT WATER.", "[3 WEEKS]", "WITHOUT FOOD."], ["SO [WATER]", "IS HIS", "{REAL CLOCK.}"],
 ["THE RULE:", "{NEVER DRINK}", "{SEAWATER.}"], ["[DAY TWO.]", "KAI CAN'T", "TAKE IT ANYMORE,", "AND {GULPS IT DOWN.}"], ["!STUPID MISTAKE."],
 ["SEAWATER IS", "ABOUT [3.5% SALT.]", "TO FLUSH IT OUT,", "HIS KIDNEYS NEED", "{MORE WATER}", "THAN HE JUST DRANK."], ["SO EVERY SIP", "MAKES HIM", "{THIRSTIER.}"],
 ["ON [DAY THREE,]", "DARK CLOUDS", "[FINALLY ROLL IN...]"], ["BUT {SOMETHING BIG}", "IS {CIRCLING}", "THE RAFT."], ["[FOLLOW]", "FOR PART TWO."]]
MOOD = {'root': 51.9, 'bpm': 100}
KAI = Look(skin=SKINS[1], hair=(40, 70, 120), style='short', shirt=(200, 160, 60), pants=(60, 60, 60), shoes=(40, 40, 60))
SEA = (150, 100, 30); SEA2 = (120, 75, 20); RAFT = (40, 120, 245)
def ocean(img, t, horizon=760, sky=((235, 190, 120), (250, 225, 185)), dark=0.0):
    img[:horizon] = grad(mix(sky[0], (90, 80, 80), dark), mix(sky[1], (130, 120, 115), dark), 0, horizon)
    img[horizon:] = grad(mix(SEA, (90, 70, 50), dark), mix(SEA2, (60, 45, 30), dark), horizon, H)
    for k in range(14):
        y = horizon + 30 + k * k * 6; xo = (t * (20 + k * 6) + k * 70) % 160
        for x in range(-160, W + 160, 160): line(img, (x + xo, y), (x + xo + 60 + k * 3, y), mix((200, 160, 90), (120, 100, 80), dark), 2 + k // 4)
def raft(img, x, y, s=1.0, who=None):
    wc = tuple(int(c) for c in img[min(H - 1, int(y + 90 * s)), 3])
    ell(img, (x, y + 40 * s), 230 * s, 70 * s, (20, 80, 200)); ell(img, (x, y + 20 * s), 230 * s, 70 * s, RAFT); ell(img, (x, y + 20 * s), 180 * s, 45 * s, (30, 100, 220))
    if who: who()
    poly(img, [(x - 260 * s, y + 40 * s), (x + 260 * s, y + 40 * s), (x + 260 * s, y + 120 * s), (x - 260 * s, y + 120 * s)], wc)   # water in front
    for dx in range(-250, 251, 70): line(img, (x + dx * s, y + 46 * s), (x + (dx + 40) * s, y + 46 * s), (200, 160, 90), 4)
def sun(img, x, y, r, k=1.0):
    glow(img, x, y, int(r * 3), (60, 140, 200), 0.8 * k); circ(img, (x, y), r, (120, 230, 255))
def shotA(img, t, d):
    z = 1.0 - 0.55 * ease(ramp(t, 0.2, d))
    img[:] = SEA
    for k in range(40):
        x = (k * 263 % W); y = (k * 577 % H); ell(img, (W / 2 + (x - W / 2) * z, H / 2 + (y - H / 2) * z), 60 * z, 8 * z, (190, 150, 80))
    ell(img, (W / 2, 960), 70 * z, 45 * z, RAFT); ell(img, (W / 2, 960), 50 * z, 30 * z, (30, 100, 220)); circ(img, (W / 2, 955), 18 * z, KAI.hair)
    pill(img, W / 2, 1560, 'NO LAND IN SIGHT', 54, INK, YEL)
    header(img, eout(ramp(t, 0.05, 0.4)))
def shotB(img, t, d):
    ocean(img, t)
    sink = ramp(t, 0, d)
    poly(img, [(760, 760 + 120 * sink), (1000, 760 + 120 * sink), (960, 820 + 100 * sink), (800, 820 + 100 * sink)], WHITE)
    line(img, (880, 760 + 120 * sink), (880 + 40 * sink, 420 + 200 * sink), (120, 120, 130), 10); poly(img, [(885 + 40 * sink, 440 + 200 * sink), (885 + 30 * sink, 730 + 120 * sink), (1000, 720 + 120 * sink)], (235, 235, 240))
    bob = 10 * math.sin(t * 2)
    raft(img, 400, 1080 + bob, 1.0, who=lambda: person(img, KAI, 400, 880 + bob, 0.9, 'worry', al=40, ar=40, legs=False))
    namecard(img, t, 'KAI · 26', 'SOLO SAILOR', 760, 420)
OFF = [1.0, 2.3, 3.6]
def card3(img, t, i, at, icon, big, small, col):
    k = back(ramp(t, at, at + 0.3))
    if k <= 0: return
    x = 190 + i * 350; y = 760
    rrect(img, x - 155 * k, y - 230 * k, 310 * k, 460 * k, 30, INK)
    if k > 0.8:
        text(img, icon, x, y - 130, 60, (170, 170, 175)); text(img, big, x, y, 150, col, ANT); text(img, small, x, y + 130, 54, WHITE)
def shotC(img, t, d, base=0.0):
    ocean(img, t, dark=0.2); tint(img, (20, 15, 15), 0.45)
    T_ = base + t; o = [0.0] + OFF
    card3(img, T_, 0, o[1], 'AIR', '3', 'MINUTES', (200, 200, 255))
    card3(img, T_, 1, o[2], 'WATER', '3', 'DAYS', YEL)
    card3(img, T_, 2, o[3], 'FOOD', '3', 'WEEKS', GREEN)
    text(img, 'THE RULE OF THREE', W / 2, 400, 90, WHITE, ANT, alpha=ramp(T_, 0.1, 0.4))
def shotD(img, t, d):
    ocean(img, t); sun(img, 820, 360, 90)
    bob = 10 * math.sin(t * 2); raft(img, W / 2, 1100 + bob, 1.1, who=lambda: person(img, KAI, W / 2, 880 + bob, 1.0, 'flat', al=10, ar=10, legs=False))
    statbox(img, t, 'TIME WITHOUT WATER', 'DAY 1', YEL, y=500)
def shotE(img, t, d):
    rule_card(img, t, d, 'NEVER DRINK', 'SEAWATER.', bg=lambda im, tt: ocean(im, tt))
    bob = 10 * math.sin(t * 2); raft(img, W / 2, 1180 + bob, 1.0, who=lambda: person(img, KAI, W / 2, 980 + bob, 0.9, 'determined', al=10, ar=10, legs=False))
def shotF(img, t, d):
    ocean(img, t, sky=((200, 220, 250), (220, 240, 255))); sun(img, 820, 300, 110, 1.3); tint(img, (60, 160, 255), 0.12)
    bob = 8 * math.sin(t * 2); dip = ramp(t, 0.6, 1.4)
    raft(img, W / 2, 1150 + bob, 1.1, who=lambda: person(img, KAI, W / 2, 940 + bob + 40 * dip, 1.0, 'cheeks' if dip > 0.8 else 'worry', al=10 + 20 * dip, ar=10 + 20 * dip, legs=False, sweat=True))
    pill(img, W / 2, 330, 'DAY 2 · 34°C', 54, INK, (120, 160, 255), dot=(80, 140, 255))
def shotG(img, t, d):
    img[:] = grad((40, 30, 180), (20, 10, 70)); vignette(img, 0.5)
    person(img, KAI, W / 2, 620, 1.7, 'cheeks', al=150, ar=150)
    flash(img, t, 0, 0.12, WHITE, 0.8)
def kidney(img, x, y, s):
    ell(img, (x, y), 70 * s, 110 * s, (100, 100, 200)); ell(img, (x + 40 * s, y), 25 * s, 40 * s, (230, 238, 245))
def shotH(img, t, d):
    img[:] = grad((230, 238, 245), (205, 215, 225))
    # glass of seawater
    gx, gy = 260, 760
    poly(img, [(gx - 110, gy - 160), (gx + 110, gy - 160), (gx + 85, gy + 160), (gx - 85, gy + 160)], (210, 200, 190)); poly(img, [(gx - 100, gy - 100), (gx + 100, gy - 100), (gx + 82, gy + 150), (gx - 82, gy + 150)], SEA)
    for k in range(12): circ(img, (gx - 70 + (k * 37) % 140, gy - 60 + (k * 53) % 200), 8, WHITE)
    text(img, '3.5% SALT', gx, gy + 230, 70, INK, ANT)
    line(img, (400, gy), (560, gy), INK, 10); poly(img, [(560, gy - 26), (600, gy), (560, gy + 26)], INK)
    kidney(img, 700, gy, 1.0); kidney(img, 900, gy, -1.0) if False else kidney(img, 880, gy, 1.0)
    # in vs out bars
    def b(y, lab, v, col, at):
        k = eout(ramp(t, at, at + 0.8)); text(img, lab, 120 + twidth(lab, 50) / 2, y - 50, 50, INK)
        rrect(img, 120, y, 840, 100, 20, (205, 210, 215)); rrect(img, 120, y, max(30, 840 * v * k), 100, 20, col)
    b(1150 + 330, 'WATER IN (1 CUP)', 0.45, (200, 150, 60), 1.8)
    b(1450 + 260, 'WATER NEEDED TO FLUSH THE SALT', 0.75, RED, 3.0)
    fact(img, t, "NOAA: KIDNEYS CAN'T MAKE URINE AS SALTY AS SEAWATER", 4.0, y=380, size=32)
def shotI(img, t, d):
    ocean(img, t, sky=((200, 220, 250), (220, 240, 255))); sun(img, 820, 300, 110, 1.3); tint(img, (60, 160, 255), 0.18)
    bob = 8 * math.sin(t * 2)
    raft(img, W / 2, 1150 + bob, 1.1, who=lambda: person(img, KAI, W / 2, 940 + bob, 1.0, 'worry', al=5, ar=5, legs=False, sweat=True))
    v = counter(t, 0.2, d - 0.3, 60, 99)
    rrect(img, 140, 420, 800, 90, 40, INK); rrect(img, 150, 430, 780 * v / 100, 70, 35, RED); text(img, f'THIRST {int(v)}%', W / 2, 466, 54, WHITE)
def shotJ(img, t, d):
    dk = ramp(t, 0, 1.2); ocean(img, t, dark=0.6 * dk)
    for k in range(5):
        x = (k * 260 + t * 40) % (W + 300) - 150; y = 200 + (k % 2) * 120
        for j in range(4): circ(img, (x + j * 70, y + (j % 2) * 20), 80, mix((220, 220, 225), (110, 100, 100), dk))
    rain(img, t, ramp(t, 1.3, 2.0), (230, 210, 190))
    bob = 10 * math.sin(t * 2)
    raft(img, W / 2, 1150 + bob, 1.1, who=lambda: person(img, KAI, W / 2, 940 + bob, 1.0, 'smile' if t > 1.3 else 'worry', al=160, ar=160, legs=False))
    pill(img, W / 2, 330, 'DAY 3 · RAIN!', 54, INK, YEL, dot=(255, 200, 120), alpha=eout(ramp(t, 1.2, 1.5)))
def fin(img, x, y, s=1.0):
    poly(img, [(x - 60 * s, y), (x + 10 * s, y - 150 * s), (x + 60 * s, y)], (90, 85, 80)); line(img, (x - 80 * s, y + 4), (x + 90 * s, y + 4), WHITE, 5)
def shotK(img, t, d):
    ocean(img, t, dark=0.6); rain(img, t, 1.0, (230, 210, 190))
    a = t * 1.3; fx, fy = W / 2 + 380 * math.cos(a), 1180 + 120 * math.sin(a)
    if math.sin(a) < 0: fin(img, fx, fy, 1.1 * (0.85 + 0.15 * math.sin(a)))
    bob = 10 * math.sin(t * 2)
    raft(img, W / 2, 1150 + bob, 1.1, who=lambda: person(img, KAI, W / 2, 940 + bob, 1.0, 'shock', al=20, ar=20, legs=False))
    if math.sin(a) >= 0: fin(img, fx, fy, 1.1)
    for r in range(3): cv2.ellipse(img, P(W / 2, 1200), (int((380 + r * 40) * 8), int((120 + r * 14) * 8)), 0, 0, 360, (200, 170, 120), 2, cv2.LINE_AA, 3)
def end_char(img, t):
    img[1500:1720] = SEA
    a = t * 1.5; fin(img, W / 2 + 260 * math.cos(a), 1580, 0.8)
    ell(img, (W / 2, 1560), 150, 45, RAFT)
def shotL(img, t, d): end_card(img, t, d, "WHAT'S CIRCLING THE RAFT", end_char)

NOZOOM = (shotA, shotG, shotL, shotH)
def timeline(ls, dur):
    c3 = ls(3) - 0.1
    OFF[:] = [ls(4) - c3 + dur(4) * f for f in (0.0, 0.34, 0.68)]
    return [(0, shotA), (ls(2) - 0.1, shotB), (c3, shotC), (ls(5) - 0.1, shotD), (ls(6) - 0.1, shotE), (ls(7) - 0.1, shotF), (ls(8) - 0.05, shotG),
            (ls(9) - 0.1, shotH), (ls(10) - 0.1, shotI), (ls(11) - 0.1, shotJ), (ls(12) - 0.1, shotK), (ls(13) - 0.1, shotL)]
def SFX(ls, dur):
    return {'hook_end': ls(2) - 0.1, 'pop': [ls(4) + dur(4) * f for f in (0.0, 0.34, 0.68)], 'splash': [ls(7) + 1.2], 'mistake': ls(8),
            'heart': [(ls(12), ls(13))], 'boom': [ls(12)], 'end': ls(13) - 0.1}

POST = {
 'title': "If You Were Stranded at Sea, Don't Drink This 🌊 Part 1 #shorts",
 'caption': "Stranded on a tiny raft in the middle of the ocean. Water everywhere, and it could kill you faster than thirst. Would you last 3 days? Follow for Part 2. 🌊",
 'tags': '#whatif #survival #ocean #science #animation #storytime',
}
