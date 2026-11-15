import math, random
from kit import *
from gameui import *

FORMAT = 'gameui'
SLUG = '2026-11-15-great-emu-war-game'
VOICE = 'storyuk'; SPEED = 1.3; CAPTION = 'sub'; SUB_Y = 1560; MOOD = {'style': 'funny', 'root': 55.0, 'bpm': 120}
PROGRESS = True; PROGRESS_COL = GGOLD; VIGNETTE = 0.2; ZOOM = 0.8
LINES = [
 ("Pixel Pam has beaten every strategy game. Today she loads the level nobody wins: the Great Emu War. Australia, 1932.", 0.2),
 ("And it's real. About twenty thousand emus are eating the wheat farms of Western Australia.", 0.25),
 ("The farmers call the army. Your units: one major, two soldiers, two machine guns, ten thousand bullets.", 0.25),
 ("Mission: protect the wheat. How hard can it be?", 0.35),
 ("Day one. Fifty emus spotted. First volley... out of range. The emus scatter in every direction.", 0.25),
 ("Achievement unlocked: the enemy splits into tiny groups. Like guerrillas.", 0.3),
 ("Day three. Over a thousand emus walk straight into an ambush by a dam. Perfect setup.", 0.25),
 ("And the gun jams. After twelve birds. A thousand emus run away.", 0.35),
 ("So Pam upgrades. A machine gun on a truck!", 0.2),
 ("Emus can sprint about fifty kilometers an hour. The truck can't catch them, and it's too bumpy to aim.", 0.3),
 ("Day seven. The newspapers are laughing. The army pulls out. Mission failed.", 0.3),
 ("The major said the emus could face machine guns with the invulnerability of tanks.", 0.35),
 ("Then the farmers beg. Respawn! Round two, November thirteenth.", 0.3),
 ("A month later, the army's own count: nine thousand eight hundred sixty bullets, nine hundred eighty-six emus. Ten bullets per bird. Probably inflated.", 0.3),
 ("The emus kept eating the wheat. Farmers asked for the army three more times. The answer was no.", 0.35),
 ("Final screen: emus win. Pam rates the level ten out of ten. Would lose again.", 0.25),
 ("Rematch: A, the army, or B, the emus? Comment A or B.", 0.7),
]
CAPS = [
 ["{Pixel Pam} beats every strategy game. Today: the level {nobody wins.} The [Great Emu War.]"],
 ["It's {real.} About [20,000 emus] eating the wheat farms."], ["Your units: [1 major,] [2 soldiers,] [2 machine guns,] [10,000 bullets.]"],
 ["Mission: {protect the wheat.} How hard can it be?"], ["[Day 1.] 50 emus. First volley: {out of range.} They {scatter.}"],
 ["Achievement: tiny groups. Like {guerrilla fighters.}"], ["[Day 3.] Over [1,000 emus] walk into an {ambush.}"],
 ["The gun {jams.} After [12 birds.]"], ["Upgrade: a machine gun {on a truck!}"],
 ["Emus sprint about [50 km/h.] The truck {can't catch them.} Too bumpy {to aim.}"],
 ["[Day 7.] Newspapers {laughing.} The army {pulls out.}"], ["\"The {invulnerability} of [tanks.]\""],
 ["Farmers beg. {Respawn!} Round two, [Nov 13.]"],
 ["The army's count: [9,860 bullets,] [986 emus.] {10 bullets per bird.} Historians: probably {inflated.}"],
 ["Emus kept eating. Farmers asked [3 more times.] The answer: {no.}"], ["{Emus win.} Pam: [10/10,] would lose again."],
 ["Rematch: {A} the army or [B] the emus?"]]
G = {}

def res_at(t):
    L = G['ls']
    ammo = 10000
    if t > L(4) + 1.5: ammo = 9900
    if t > L(10): ammo = 7500   # ~2,500 rounds fired by 8 Nov (Meredith's report)
    if t > L(13): ammo = int(counter(t, L(13) + 2.0, L(13) + 4.0, 7500, 140))
    emus = 20000
    wheat = int(100 - 70 * ramp(t, L(1), L(15)))
    return [('🪖', 'TROOPS', '3', WHITE, None), ('🔫'.replace('🔫', '📦'), 'AMMO', f'{ammo:,}', GGOLD, L(13) + 3.0 if t > L(13) else L(10) if t > L(9) else None),
            ('🪶', 'EMUS', f'~{emus:,}', GRED, None), ('🌾', 'WHEAT', f'{wheat}%', GGREEN if wheat > 50 else GRED, None)]

def s1(img, t, d):
    field(img, t); flock(img, t, 14, 80, 1000, 880, 1250, 0.55, run=0.0, seed=3)
    z = 1 + 0.5 * (1 - eout(ramp(t, 0, 0.7)))
    facecam(img, t, '😎' if t < 4 else '😳', x=W / 2, y=560, r=150 * z / 1.5 * 1.3)
    if t < 4.6: text(img, 'THE LEVEL NOBODY WINS', W / 2, 1000, 84, WHITE, ANT, stroke=8, scol=(10, 10, 10), scale=0.7 + 0.3 * back(ramp(t, 0.1, 0.4)))
    if t > 4.6: banner(img, t, 'THE GREAT EMU WAR', GGOLD, at=4.6, y=1020, size=96, sub='AUSTRALIA · 1932 · DIFFICULTY: ???')
def s2(img, t, d):
    field(img, t, eaten=0.2 * ramp(t, 0, d)); flock(img, t, 40, -50, 1130, 860, 1450, 0.5, run=0.3, seed=5, vx=-10)
    k = back(ramp(t, 0.3, 0.6)); pill(img, W / 2, 330, 'REAL HISTORY', 44, INK, GGOLD, dot=GRED, alpha=min(1, max(0, k)))
    text(img, '~20,000', W / 2, 560, 150, WHITE, ANT, stroke=8, scol=(10, 10, 10), alpha=ramp(t, 1.2, 1.5))
def s3(img, t, d):
    field(img, t)
    units = [(240, 1330, 'MAJOR'), (480, 1330, 'SOLDIER'), (720, 1330, 'SOLDIER')]
    for i, (x, y, lab) in enumerate(units):
        if t > 1.2 + i * 0.5: soldier(img, x, y, 1.5, sel=t > 3.0, t=t); text(img, lab, x, y + 40, 32, WHITE, INTER_B)
    if t > 3.6: lewis(img, 540, 760, 1.1); lewis(img, 540, 880, 1.1)
    if t > 3.0:
        k = ease(ramp(t, 3.0, 3.6)); rrect(img, 130, 940, 820 * k, 450 * k, 6, GGREEN, 2)
    cursor(img, 760 - 300 * ease(ramp(t, 0.4, 2.8)), 1100 - 100 * ease(ramp(t, 0.4, 2.8)), click=ramp(t, 2.9, 3.2) if t < 3.3 else 0)
def s4(img, t, d):
    field(img, t); objective(img, 'MISSION: PROTECT THE WHEAT', a=ramp(t, 0.1, 0.3), y=330)
    health(img, 240, 600, 600, 1.0, GGREEN, 'WHEAT')
    facecam(img, t, '😏', x=W / 2, y=900, r=110)
    if t > 1.8: text(img, 'EASY.', W / 2, 1160, 100, GGREEN, ANT, scale=back(ramp(t, 1.8, 2.1)), stroke=6, scol=(10, 10, 10))
def s5(img, t, d):
    field(img, t)
    pill(img, W / 2, 330, 'DAY 1 · 2 NOV 1932', 44, INK, WHITE, dot=GGOLD)
    sc = ramp(t, 3.0, 3.2) * 0.9
    flock(img, t - 3.0 if t > 3.0 else 0, 12, 450, 850, 900, 1050, 0.4, run=1.0 if t > 3.0 else 0.0, seed=7, scatter=sc)
    soldier(img, 160, 1400, 0.9); lewis(img, 300, 1370, 0.8)
    if 1.6 < t < 3.0:
        for i in range(4): circ(img, (360 + (t - 1.6) * 260 + i * 40, 1320 - (t - 1.6) * 200), 6, GGOLD)
        if t > 2.2: text(img, 'OUT OF RANGE', W / 2, 650, 64, GRED, INTER_B, scale=back(ramp(t, 2.2, 2.5)))
def s6(img, t, d):
    field(img, t); flock(img, t, 15, 100, 980, 880, 1300, 0.45, run=1.0, seed=8, scatter=0.25)
    achievement(img, t, 0.1, 'TINY GUERRILLA GROUPS', '🪶', dur=d - 0.1, y=320)
def s7(img, t, d):
    field(img, t); pill(img, W / 2, 330, 'DAY 3 · AMBUSH AT THE DAM', 44, INK, WHITE, dot=GGOLD)
    ell(img, (W / 2, 1000), 260, 50, (170, 130, 80))
    flock(img, t, 60, -200, 900, 860, 1250, 0.38, run=0.6, seed=9, vx=90)
    soldier(img, 900, 1450, 0.8); lewis(img, 760, 1430, 0.8)
    text(img, str(int(counter(t, 0.3, 2.4, 0, 1000))) + '+', W / 2, 620, 130, WHITE, ANT, stroke=8, scol=(10, 10, 10))
def s8(img, t, d):
    field(img, t); jx, jy = shake(t, 0.4, 0.4, 12)
    flock(img, max(0, t - 1.0), 50, 0, 900, 860, 1250, 0.38, run=1.0, seed=9, vx=0, scatter=0.5 if t > 1.0 else 0.0)
    lewis(img, 540 + jx, 1400 + jy, 1.6, jam=1.0 if t > 0.4 else 0.0, t=t)
    if t > 0.4: text(img, '12', 200, 620, 120, GRED, ANT, stroke=6, scol=(10, 10, 10)); text(img, 'BIRDS', 200, 720, 40, WHITE, INTER_B)
    facecam(img, t, '🤬' if t > 0.8 else '😮', x=900, y=560, r=100)
def s9(img, t, d):
    field(img, t)
    rrect(img, 240, 500, 600, 560, 30, UI); rrect(img, 240, 500, 600, 560, 30, GGOLD, 3)
    text(img, 'UPGRADE', W / 2, 560, 44, GGOLD, INTER_B)
    truck(img, W / 2 + 30, 900, 1.2 * back(ramp(t, 0.3, 0.6)), t)
    if t > 1.2: text(img, 'SPEED +200%', W / 2, 980, 44, GGREEN, INTER_B, alpha=ramp(t, 1.2, 1.4))
def s10(img, t, d):
    field(img, t)
    off = (t * 600) % 1600
    flock(img, t, 10, 300 + t * 120, 1000 + t * 120, 900, 1100, 0.45, run=1.0, seed=12)
    truck(img, 200 + t * 60, 1350, 1.0, t, bump=1.0)
    hud_y = 560; text(img, f'{int(counter(t, 0.2, 1.5, 0, 50))} KM/H', W / 2, hud_y, 110, WHITE, ANT, stroke=6, scol=(10, 10, 10))
    if t > 3.8:
        text(img, 'MISS', 300, 760, 70, GRED, ANT, scale=back(ramp(t, 3.8, 4.0))); text(img, 'MISS', 760, 820, 70, GRED, ANT, scale=back(ramp(t, 4.4, 4.6)))
def s11(img, t, d):
    field(img, t, eaten=0.35); flock(img, t, 25, 0, 1080, 880, 1350, 0.45, run=0.2, seed=13)
    k = back(ramp(t, 0.3, 0.6)); rrect(img, 190, 380, 700 * min(1, k), 250, 10, (225, 230, 235))
    if k > 0.8: text(img, 'EMUS 1 · ARMY 0', W / 2 - 0, 470, 64, (30, 30, 30), ANT); text(img, 'THE DAILY GIGGLE', W / 2, 560, 30, (80, 80, 80), INTER_B)
    if t > 2.6: banner(img, t, 'MISSION FAILED', GRED, at=2.6, y=900, size=120)
def s12(img, t, d):
    img[:] = grad((50, 40, 40), (20, 15, 15))
    emu(img, W / 2, 1300, 2.6, t, 0.0, -1, boss=True)
    health(img, 190, 380, 700, 1.0, GRED, 'BOSS: EMU · ARMOR: TANK')
    if t > 2.4: text(img, '"INVULNERABILITY OF TANKS"', W / 2, 520, 52, GGOLD, INTER_B, alpha=ramp(t, 2.4, 2.7))
def s13(img, t, d):
    field(img, t, eaten=0.4); flock(img, t, 20, 0, 1080, 880, 1350, 0.45, run=0.3, seed=14)
    banner(img, t, 'RESPAWN', GGREEN, at=1.4, y=760, size=130, sub='ROUND 2 · 13 NOV 1932')
def s14(img, t, d):
    img[:] = grad((50, 40, 40), (20, 15, 15))
    rows = [('BULLETS FIRED', '9,860', GGOLD), ('EMUS (CLAIMED)', '986', WHITE), ('BULLETS PER BIRD', '10', GRED)]
    for i, (lab, val, col) in enumerate(rows):
        a = 1.2 + i * 1.5; k = ramp(t, a, a + 0.3)
        if k > 0:
            y = 560 + i * 220; rrect(img, 120, y - 80, 840, 160, 20, UI); rrect(img, 120, y - 80, 840, 160, 20, col, 2)
            text(img, lab, 120 + 30 + twidth(lab, 40, INTER_B) / 2, y, 40, WHITE, INTER_B, alpha=k)
            text(img, val, 900 - twidth(val, 90, ANT) / 2, y, 90, col, ANT, scale=back(ramp(t, a, a + 0.3)))
    text(img, 'ARMY REPORT · 10 DEC 1932', W / 2, 360, 38, GGOLD, INTER_B)
    if t > 6.0:
        k = back(ramp(t, 6.0, 6.3)); rrect(img, W / 2 - 300 * k, 1230, 600 * k, 110, 20, GRED)
        if k > 0.8: text(img, 'PROBABLY INFLATED', W / 2, 1285, 48, WHITE, ANT)
def s15(img, t, d):
    field(img, t, eaten=0.6 + 0.2 * ramp(t, 0, d)); flock(img, t, 30, 0, 1080, 880, 1400, 0.45, run=0.15, seed=15)
    for i, yr in enumerate(('1934', '1943', '1948')):
        k = back(ramp(t, 2.0 + i * 0.5, 2.3 + i * 0.5)); x = 240 + i * 300
        if k > 0: rrect(img, x - 120 * k, 420, 240 * k, 140, 20, UI)
        if k > 0.8: text(img, yr, x, 470, 50, WHITE, ANT); text(img, 'DENIED', x, 525, 32, GRED, INTER_B)
def s16(img, t, d):
    field(img, t, eaten=0.8); flock(img, t, 20, 100, 1000, 900, 1350, 0.5, run=0.0, seed=16)
    banner(img, t, 'EMUS WIN', GGOLD, at=0.1, y=620, size=150)
    if t > 2.2:
        for i in range(10): emoji(img, '⭐', 130 + i * 92, 900, 70 * back(ramp(t, 2.2 + i * 0.08, 2.5 + i * 0.08)))
    facecam(img, t, '🥲', x=W / 2, y=1180, r=110)
def s17(img, t, d):
    img[:] = grad((60, 45, 40), (20, 15, 15))
    text(img, 'REMATCH?', W / 2, 400, 120, WHITE, ANT, stroke=8, scol=(10, 10, 10))
    for i, (lab, ic, col) in enumerate((('A · THE ARMY', '🪖', GBLUE), ('B · THE EMUS', None, (40, 140, 245)))):
        k = back(ramp(t, 0.2 + i * 0.3, 0.5 + i * 0.3)); y = 720 + i * 300
        if k > 0: rrect(img, W / 2 - 400 * k, y - 110, 800 * k, 220, 40, col)
        if k > 0.8:
            if ic: emoji(img, ic, W / 2 - 280, y, 120)
            else: emu(img, W / 2 - 280, y + 95, 0.85, t, 0.0, 1)
            text(img, lab, W / 2 + 80, y, 60, WHITE, ANT)
    pill(img, W / 2, 1360, 'COMMENT A OR B', 54, INK, WHITE, alpha=eout(ramp(t, 1.2, 1.5)))

def OVERLAY(img, t, total):
    if t > G['ls'](2) and t < G['ls'](16): topbar(img, t, res_at(t))
    scanlines(img)

NOZOOM = (s14, s17)
def timeline(ls, dur):
    G['ls'] = ls
    fs = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17]
    return [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'ding': [ls(5) + 0.2, ls(8) + 0.4, ls(12) + 1.4], 'pop': [ls(2) + 1.2, ls(2) + 1.7, ls(2) + 2.2, ls(13) + 1.2, ls(13) + 2.7, ls(13) + 4.2, ls(14) + 2.0, ls(14) + 2.5, ls(14) + 3.0],
            'mistake': ls(7) + 0.4, 'boom': [ls(10) + 2.6, ls(15) + 0.1], 'whoosh': [ls(4), ls(6), ls(9), ls(11)], 'end': ls(16) - 0.05}

POST = {
 'title': "The Great Emu War, But It's A Strategy Game 🎮 #shorts",
 'caption': "Pixel Pam loads the one level nobody wins: Australia, 1932. 3 soldiers, 2 machine guns, 10,000 bullets vs ~20,000 emus. The gun jams, the truck can't catch them, the army pulls out... and the emus win 🏆 Rematch: A) the army or B) the emus? 👇",
 'tags': '#history #emuwar #funny #gaming #australia #animation',
 'source': "Sources: Wikipedia 'Emu War' (Campion district, Western Australia, 2 Nov–10 Dec 1932; ~20,000 emus; Major Meredith with 2 soldiers, 2 Lewis guns, 10,000 rounds; 4 Nov ambush near a dam, gun jammed after 12 birds; truck-mounted gun too slow and bumpy; withdrawn 8 Nov, resumed 13 Nov; Meredith's report 986 kills with 9,860 rounds, figure 'highly disputed'; 'invulnerability of tanks' quote; farmers' requests refused in 1934, 1943, 1948); History Hit, Britannica 'Emu War'. Emu top speed ~48–50 km/h. Pixel Pam is fictional.",
}
