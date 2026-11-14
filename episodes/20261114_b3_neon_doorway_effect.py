import math, random
from kit import *
from neon import *

FORMAT = 'neon'
SLUG = '2026-11-14-doorway-effect-forget'
VOICE = 'girl'; SPEED = 1.22; CAPTION = 'top'; TICKS = True; MOOD = {'style': 'hype', 'root': 52.0}
ACCENT = NB; PROGRESS_COL = NB; VIGNETTE = 0.0; ZOOM = 0.7; TOP_Y = 330
PINK = (200, 120, 255)
LINES = [
 ("You walk into the kitchen... and forget why. It's not you. It's the door.", 0.3),
 ("Meet Kylie Kombucha. Wellness influencer. Ninety thousand followers, and one dying phone.", 0.25),
 ("Her phone is at two percent. She gets up to grab the charger from the kitchen.", 0.25),
 ("She steps through the doorway... and it's gone. Total blank.", 0.35),
 ("In 2011, psychologists at the University of Notre Dame tested exactly this.", 0.25),
 ("People carried objects around a virtual house. Some walked through a doorway. Others walked the same distance inside one room.", 0.25),
 ("The doorway group forgot more. Same distance. Same task.", 0.3),
 ("Then they ran it in a real lab, with real boxes. Same result.", 0.3),
 ("Here's why. Your brain saves life in episodes, like scenes in a movie.", 0.25),
 ("A doorway is a cut. New room, new scene. So your brain files the last scene away.", 0.3),
 ("The researchers call it an event boundary.", 0.3),
 ("So Kylie walks back to the couch to remember. Nope. Still blank.", 0.25),
 ("And that matched the study too: going back to the first room didn't bring the memory back.", 0.3),
 ("The fix? Hold the thought in your head as you move. Say it out loud: charger, charger, charger.", 0.25),
 ("Kylie chants it all the way to the kitchen. Grabs the charger. Victory.", 0.25),
 ("Then she looks at her phone. It died. She forgot what she needed it for.", 0.35),
 ("What's the weirdest thing a door ever made you forget?", 1.0),
]
CAPS = [
 ["You walk into the kitchen and {forget why.} It's not you. It's {the door.}"],
 ["Meet {Kylie Kombucha.} Wellness influencer. {90K} followers, one dying phone."],
 ["Phone at {2%.} She goes to grab the {charger.}"], ["She steps through the doorway... {total blank.}"],
 ["{2011:} psychologists at {Notre Dame} tested this."],
 ["A {virtual house.} Through a {doorway,} or the same distance in {one room.}"],
 ["The doorway group {forgot more.} Same distance. Same task."], ["Then a {real lab,} real boxes. {Same result.}"],
 ["Your brain saves life in {episodes,} like {scenes in a movie.}"], ["A doorway is a {cut.} New scene. The last one gets {filed away.}"],
 ["Researchers call it an {event boundary.}"], ["Back to the couch to remember. {Nope.}"],
 ["In the study, going back to the first room {didn't help} either."],
 ["The fix: {hold the thought} as you move. Say it out loud."],
 ["{Charger, charger, charger.} Grabs it. {Victory.}"], ["Her phone {died.} She forgot what she needed it {for.}"],
 ["What's the weirdest thing a {door} made you forget?"]]

def door(img, x, y, s=1.0, a=1.0, col=NW, glowk=0.0):
    c = mix(BG, col, a)
    if glowk: neon_glow(img, x, y - 230 * s, 260 * s, col, glowk)
    rrect(img, x - 110 * s, y - 470 * s, 220 * s, 470 * s, 8, c, max(2, int(5 * s)))
    circ(img, (x + 70 * s, y - 230 * s), 9 * s, c)
def bubble(img, x, y, txt, a=1.0, col=NB, size=40):
    if a <= 0.02: return
    w = twidth(txt, size, INTER_B) + 60; c = mix(BG, col, a)
    rrect(img, x - w / 2, y - 50, w, 100, 40, c, 3); text(img, txt, x, y, size, c, INTER_B)
    circ(img, (x - w / 4, y + 70), 12, c, 3); circ(img, (x - w / 4 - 30, y + 105), 8, c, 3)
def battery(img, x, y, pct, a=1.0):
    c = mix(BG, NW, a); rrect(img, x - 90, y - 40, 180, 80, 10, c, 4); rrect(img, x + 90, y - 16, 14, 32, 4, c)
    col = NRED if pct < 20 else (90, 220, 120)
    rrect(img, x - 80, y - 30, max(4, 160 * pct / 100), 60, 6, mix(BG, col, a))
    text(img, f'{int(pct)}%', x, y + 80, 44, mix(BG, col, a), INTER_B)
def plug(img, x, y, a=1.0, col=GOLD):
    c = mix(BG, col, a); rrect(img, x - 40, y - 50, 80, 100, 14, c, 4)
    for sx in (-16, 16): line(img, (x + sx, y - 50), (x + sx, y - 80), c, 6)
    line(img, (x, y + 50), (x - 30, y + 160), c, 5)

def s1(img, t, d):
    stage(img, t)
    door(img, W / 2 + 150, FLOOR, 1.1, glowk=0.5)
    x = 260 + 320 * eout(ramp(t, 0.1, 1.6)); fig(img, x, FLOOR, 1.3, PINK)
    if t > 1.7:
        k = back(ramp(t, 1.7, 2.0)); text(img, '?', x, FLOOR - 330, 180, NW, INTER_B, scale=k)
    if t > 3.4: big(img, 'THE DOOR', W / 2, 1450, 120, NB, a=ramp(t, 3.4, 3.7))
def s2(img, t, d):
    stage(img, t); fig(img, W / 2, FLOOR, 1.6, PINK, a=eout(ramp(t, 0, 0.3)))
    label(img, W / 2, FLOOR + 55, 'KYLIE KOMBUCHA · WELLNESS', PINK, ramp(t, 0.3, 0.6))
    big(img, f'{int(counter(t, 0.6, 2.4, 0, 90000)):,}', W / 2, 780, 110, PINK, a=ramp(t, 0.5, 0.8))
    label(img, W / 2, 880, 'FOLLOWERS', NW, ramp(t, 0.6, 0.9))
    if t > 3.4: emoji(img, '🍵', 820, 1000, 110 * back(ramp(t, 3.4, 3.7)))
def s3(img, t, d):
    stage(img, t); battery(img, W / 2, 680, counter(t, 0, 1.0, 9, 2))
    if t % 0.6 < 0.3: neon_glow(img, W / 2, 680, 220, NRED, 0.6)
    plug(img, 800, 1050, ramp(t, 1.8, 2.1)); fig(img, 300, FLOOR, 1.1, PINK)
    bubble(img, 380, 900, 'CHARGER', ramp(t, 2.0, 2.3))
def s4(img, t, d):
    stage(img, t); door(img, W / 2, FLOOR, 1.2, glowk=0.6 * ramp(t, 0.8, 1.0))
    x = 220 + 640 * ease(ramp(t, 0.1, 1.8)); fig(img, x, FLOOR, 1.2, PINK)
    if x < W / 2: bubble(img, x + 60, 820, 'CHARGER', 1)
    else:
        flash(img, t, 1.0, 0.2, NW, 0.5); bubble(img, x + 20, 820, '...', 1, NRED)
    if t > 2.6: big(img, 'BLANK', W / 2, 520, 140, NRED, a=ramp(t, 2.6, 2.9))
def s5(img, t, d):
    stage(img, t)
    big(img, '2011', W / 2, 760, 220, NB, a=ramp(t, 0, 0.3), sc=0.7 + 0.3 * back(ramp(t, 0, 0.3)))
    label(img, W / 2, 940, 'UNIVERSITY OF NOTRE DAME', NW, ramp(t, 0.8, 1.1), 34)
    label(img, W / 2, 1020, 'RADVANSKY ET AL.', DIM, ramp(t, 1.3, 1.6), 30)
def room_plan(img, cx, cy, w, h, a, col=NW, door_gap=False):
    c = mix(BG, col, a)
    if door_gap:
        rrect(img, cx - w / 2, cy - h / 2, w / 2 - 50, h, 6, c, 3); rrect(img, cx + 50, cy - h / 2, w / 2 - 50, h, 6, c, 3)
        line(img, (cx - 50, cy - 60), (cx + 50, cy - 60), mix(BG, NB, a), 6); line(img, (cx - 50, cy + 60), (cx + 50, cy + 60), mix(BG, NB, a), 6)
    else: rrect(img, cx - w / 2, cy - h / 2, w, h, 6, c, 3)
def s6(img, t, d):
    stage(img, t, floor=False)
    room_plan(img, W / 2, 780, 760, 300, ramp(t, 0.2, 0.5), door_gap=True); label(img, W / 2, 590, 'DOORWAY', NB, ramp(t, 0.3, 0.6))
    room_plan(img, W / 2, 1250, 760, 300, ramp(t, 2.6, 2.9)); label(img, W / 2, 1060, 'ONE BIG ROOM', NW, ramp(t, 2.7, 3.0))
    u = (t * 0.35) % 1; circ(img, (W / 2 - 330 + 660 * u, 780), 18, PINK); circ(img, (W / 2 - 330 + 660 * u, 1250), 18 * ramp(t, 2.8, 3.0), PINK)
    label(img, W / 2, 1470, 'SAME DISTANCE', GOLD, ramp(t, 4.4, 4.7))
def bar(img, x, y0, hgt, col, lab, a):
    c = mix(BG, col, a); rrect(img, x - 90, y0 - hgt, 180, hgt, 10, c); neon_glow(img, x, y0 - hgt / 2, 160, col, 0.4 * a)
    text(img, lab, x, y0 + 50, 36, mix(BG, NW, a), INTER_B)
def s7(img, t, d):
    stage(img, t)
    bar(img, 360, 1150, 250 * eout(ramp(t, 0.2, 0.9)), DIM, 'ONE ROOM', 1)
    bar(img, 720, 1150, 470 * eout(ramp(t, 0.5, 1.4)), NRED, 'DOORWAY', 1)
    label(img, W / 2, 1320, 'FORGOT MORE', NRED, ramp(t, 1.4, 1.7), 40)
def s8(img, t, d):
    stage(img, t)
    for i in range(3):
        k = back(ramp(t, 0.2 + i * 0.3, 0.5 + i * 0.3)); x = 240 + i * 300
        if k > 0: rrect(img, x - 90 * k, 900 - 90 * k, 180 * k, 180 * k, 10, NW, 4)
    door(img, W / 2, 1240, 0.5, glowk=0.4)
    k = back(ramp(t, 2.3, 2.6)); text(img, 'SAME RESULT', W / 2, 650, 100, NB, INTER_B, scale=k)
def s9(img, t, d):
    stage(img, t, floor=False)
    off = t * 120
    for i in range(6):
        x = 120 + i * 260 - off % 260; rrect(img, x, 700, 220, 380, 10, mix(BG, NW, 0.9), 3)
        for hy in (712, 1052):
            for hx in range(int(x) + 14, int(x) + 210, 40): rrect(img, hx, hy, 20, 16, 3, mix(BG, NW, 0.6))
        text(img, f'SCENE {i + 1 + int(off // 260)}', x + 110, 890, 34, mix(BG, NB, 0.9), INTER_B)
    big(img, '🎬', W / 2, 1300, 10, NW, a=0)
    emoji(img, '🎬', W / 2, 1320, 140, alpha=ramp(t, 0.4, 0.7))
def s10(img, t, d):
    stage(img, t); door(img, 320, FLOOR, 1.0, glowk=0.6)
    k = ease(ramp(t, 0.6, 2.2))
    rrect(img, 520, 620 + 300 * k, 300, 200, 10, mix(BG, NB, 1 - 0.6 * k), 3); text(img, 'CHARGER', 670, 720 + 300 * k, 40, mix(BG, NB, 1 - 0.5 * k), INTER_B)
    rrect(img, 520, 1060, 300, 140, 10, NW, 3); text(img, 'ARCHIVE', 670, 1130, 40, NW, INTER_B)
    if t > 3.0: big(img, 'CUT!', W / 2, 450, 130, GOLD, a=ramp(t, 3.0, 3.3))
def s11(img, t, d):
    stage(img, t)
    line(img, (120, 860), (960, 860), mix(BG, NW, 0.6), 3)
    for i, x in enumerate((240, 540, 840)):
        k = back(ramp(t, 0.2 + 0.3 * i, 0.5 + 0.3 * i)); circ(img, (x, 860), 30 * k, NB if i == 1 else DIM)
    big(img, 'EVENT BOUNDARY', W / 2, 1080, 84, NB, a=ramp(t, 0.9, 1.2))
def s12(img, t, d):
    stage(img, t)
    rrect(img, 560, 1060, 380, 180, 30, mix(BG, NW, 0.8), 4)
    x = 300 + 400 * ease(ramp(t, 0.1, 1.6)); fig(img, x, FLOOR, 1.1, PINK)
    if t > 2.0: big(img, 'NOPE', W / 2, 560, 150, NRED, a=ramp(t, 2.0, 2.3), sc=0.7 + 0.3 * back(ramp(t, 2.0, 2.3)))
def s13(img, t, d):
    stage(img, t)
    bar(img, 360, 1150, 470 * eout(ramp(t, 0.2, 0.9)), NRED, 'NEW ROOM', 1)
    bar(img, 720, 1150, 470 * eout(ramp(t, 0.5, 1.4)), NRED, 'BACK HOME', 1)
    label(img, W / 2, 1320, "NO IMPROVEMENT", NRED, ramp(t, 1.6, 1.9), 40)
def s14(img, t, d):
    stage(img, t); fig(img, 300, FLOOR, 1.2, PINK)
    for i in range(3):
        k = back(ramp(t, 2.2 + i * 0.5, 2.5 + i * 0.5)); bubble(img, 700, 660 + i * 170, 'CHARGER', k, GOLD, 40) if k > 0 else None
    big(img, 'SAY IT', W / 2, 1450, 110, NB, a=ramp(t, 0.6, 0.9))
def s15(img, t, d):
    stage(img, t); door(img, W / 2, FLOOR, 1.1, glowk=0.6)
    x = 200 + 600 * ease(ramp(t, 0.1, 2.2)); fig(img, x, FLOOR, 1.1, PINK)
    bubble(img, x + 40, 780, 'CHARGER!', 1, GOLD)
    if t > 2.6: plug(img, 860, 1000, 1); emoji(img, '🏆', W / 2, 520, 150 * back(ramp(t, 2.8, 3.1)))
def s16(img, t, d):
    stage(img, t); battery(img, W / 2, 640, 0)
    if t > 0.6: big(img, 'DEAD', W / 2, 860, 120, NRED, a=ramp(t, 0.6, 0.9))
    fig(img, W / 2, FLOOR, 1.2, PINK)
    if t > 2.0: k = back(ramp(t, 2.0, 2.3)); text(img, '???', W / 2, FLOOR - 340, 140, NW, INTER_B, scale=k)
def s17(img, t, d):
    stage(img, t); door(img, W / 2, FLOOR, 1.3, glowk=0.8 + 0.2 * math.sin(t * 4))
    label(img, W / 2, 1420, 'COMMENT BELOW', NB, ramp(t, 0.4, 0.7), 44)

NOZOOM = (s6, s9, s11)
def timeline(ls, dur):
    fs = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17]
    return [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'whoosh': [ls(3) + 1.0, ls(9), ls(14)], 'boom': [ls(3) + 2.6, ls(6) + 1.4, ls(15) + 0.6], 'ding': [ls(4), ls(10) + 0.9, ls(14) + 2.8],
            'pop': [ls(1) + 2.4, ls(7) + 2.3, ls(13) + 2.2, ls(13) + 2.7, ls(13) + 3.2], 'notif': [ls(2) + 0.1, ls(2) + 0.7], 'end': ls(16) - 0.05}

POST = {
 'title': "Why You Forget Why You Walked Into A Room 🚪 #shorts",
 'caption': "Wellness influencer Kylie Kombucha walks into the kitchen for her charger... and her brain hits delete 🚪🧠 It's called the doorway effect, and science tested it. What's the weirdest thing a door ever made you forget? 👇",
 'tags': '#psychology #brain #doorwayeffect #memory #facts #funny',
 'source': "Source: Radvansky, Krawietz & Tamplin (2011), Quarterly Journal of Experimental Psychology — walking through doorways causes forgetting (University of Notre Dame news release, Nov 2011). Original characters.",
}
