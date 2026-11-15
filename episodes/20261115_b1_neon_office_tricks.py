import math, random
from kit import *
from neon import *

FORMAT = 'neon'
SLUG = '2026-11-15-office-psychology-tricks'
VOICE = 'mom'; SPEED = 1.25; VOICE_SPEED = {'mom': 1.3, 'girl': 1.22}
CAPTION = 'sub'; SUB_Y = 1500; MOOD = {'style': 'funny', 'root': 55.0}
ACCENT = NB; PROGRESS_COL = NB; VIGNETTE = 0.0; ZOOM = 0.7
PINK = (200, 120, 255); GW = (140, 110, 255)   # Owen = neon blue, Gwen = neon red/pink
LINES = [
 ("This is Owen Onboarding. Day one at a new job. His desk neighbor hates him.", 0.3),
 ("Meet Grumpy Gwen. Eleven years at this desk. Words said to Owen: zero.", 0.3),
 ("Owen's goal: make Gwen say good morning by Friday. Five days. Four psychology tricks.", 0.35),
 ("Monday. Trick one: the Ben Franklin effect.", 0.25),
 ("Franklin won over a rival by borrowing a rare book. Studies agree: we like people more after doing them a favor.", 0.3),
 ("So Owen asks to borrow her stapler. She hands it over. Without looking.", 0.25),
 ("Like meter: two percent... to nine. It's working.", 0.35),
 ("Tuesday. Trick two: the mere exposure effect. We like what we see a lot.", 0.25),
 ("So Owen walks past her desk. Forty-seven times. H R sends him a meeting invite.", 0.35),
 ("Wednesday. Trick three: mirroring. People who copy your posture seem more likable.", 0.25),
 ("Gwen sips coffee. Owen sips coffee. Gwen sneezes. Owen... fake sneezes. Like meter: minus four.", 0.35),
 ("Thursday. Trick four: the pratfall effect. In a 1966 study, a brilliant quiz contestant spilled coffee, and got MORE likable.", 0.3),
 ("So Owen spills coffee. On purpose. On his own shirt.", 0.3),
 ("Catch: it only works if you're already good at your job. The average contestant who spilled got LESS likable.", 0.25),
 ("Owen's spreadsheet crashed three times this week. Like meter: zero.", 0.4),
 ("Friday. Owen gives up on tricks. He just says: good morning, Gwen.", 0.45),
 ("Good morning, Owen. Can I borrow your stapler?", 0.35, 'girl'),
 ("Wait. Is she using the Ben Franklin effect on HIM?", 0.3),
 ("Which trick have you used without knowing? Comment one, two, three or four.", 1.0),
]
CAPS = [
 ["This is {Owen Onboarding.}", "Day one.", "His desk neighbor", "{hates him.}"], ["Meet {Grumpy Gwen.}", "11 years.", "Words to Owen:", "{zero.}"],
 ["Goal:", "{good morning}", "by Friday.", "5 days.", "4 tricks."], ["Monday.", "{Ben Franklin effect.}"],
 ["Franklin", "borrowed a", "{rare book.}", "People like you", "more after", "{a favor.}"], ["Borrow", "her {stapler.}", "Without", "{looking.}"],
 ["Like meter:", "2%", "to {9%.}", "Working."], ["Tuesday.", "{Mere exposure.}", "We like", "what we see."],
 ["Walks past", "her desk", "{47 times.}", "HR sends", "{an invite.}"], ["Wednesday.", "{Mirroring.}", "Copy their", "posture."],
 ["Gwen sips.", "Owen sips.", "Gwen sneezes.", "Owen", "{fake sneezes.}", "Like meter:", "{minus 4.}"],
 ["Thursday.", "{Pratfall effect.}", "1966 study:", "a brilliant", "contestant", "spills coffee,", "gets {more likable.}"],
 ["Owen spills", "coffee.", "{On purpose.}"], ["Catch:", "only if you're", "{good at your job.}", "Average contestant", "got {less likable.}"],
 ["Spreadsheet", "crashed", "{3 times.}", "Like meter:", "{zero.}"], ["Friday.", "No tricks.", "{Good morning, Gwen.}"],
 ["{Good morning, Owen.}", "Can I borrow", "your {stapler?}"], ["Wait.", "Is she using it", "{on HIM?}"],
 ["Which trick", "have you used?", "Comment", "{1, 2, 3 or 4.}"]]

ST = {}
LIKE = {}
def desk(img, x, y, w=300, a=1.0, col=NW):
    c = mix(BG, col, a); line(img, (x - w / 2, y), (x + w / 2, y), c, 5)
    for sx in (-1, 1): line(img, (x + sx * (w / 2 - 20), y), (x + sx * (w / 2 - 20), FLOOR), c, 4)
    rrect(img, x - 70, y - 120, 140, 100, 8, c, 3); line(img, (x, y - 20), (x, y), c, 4)
def mug(img, x, y, s=1.0, a=1.0, col=GOLD, tilt=0.0):
    c = mix(BG, col, a)
    pts = [(-30, -50), (30, -50), (24, 20), (-24, 20)]
    ct, st_ = math.cos(tilt), math.sin(tilt)
    poly(img, [(x + (px * ct - py * st_) * s, y + (px * st_ + py * ct) * s) for px, py in pts], c)
    for i in range(2): line(img, (x - 10 + i * 20, y - 60 * s), (x - 16 + i * 20, y - 95 * s), mix(BG, NW, 0.5 * a), 3)
def stapler(img, x, y, s=1.0, a=1.0, col=NRED):
    c = mix(BG, col, a); rrect(img, x - 90 * s, y - 20 * s, 180 * s, 26 * s, 8, c); rrect(img, x - 90 * s, y - 50 * s, 170 * s, 24 * s, 10, c, 3)
def chip(img, txt, a=1.0, col=GOLD):
    label(img, W / 2, 220, txt, col, a, 40)
def meter(img, t, v0, v1, at=0.2, y=420, a=1.0):
    v = counter(t, at, at + 1.0, v0, v1); c = mix(BG, NW, a)
    text(img, 'GWEN LIKES OWEN', W / 2, y - 60, 34, mix(BG, PINK, a), INTER_B)
    rrect(img, 140, y - 22, 800, 44, 22, c, 3)
    fw = max(0, min(1, v / 100)) * 788
    if fw > 4: rrect(img, 146, y - 16, fw, 32, 16, mix(BG, (90, 220, 120) if v1 >= v0 else NRED, a))
    big(img, f'{int(round(v))}%', W / 2, y + 90, 80, (90, 220, 120) if v >= 5 else NRED, a=a)
def gwen(img, x, s=1.2, a=1.0, cloud=True, t=0.0):
    fig(img, x, FLOOR, s, GW, a)
    if cloud:
        cy = FLOOR - 270 * s + 6 * math.sin(t * 3)
        for dx, r in ((-40, 34), (0, 46), (44, 34)): circ(img, (x + dx * s, cy), r * s, mix(BG, DIM, a))
        if int(t * 3) % 3 == 0: line(img, (x, cy + 40 * s), (x - 14 * s, cy + 80 * s), mix(BG, GOLD, a), 4)

def s1(img, t, d):
    stage(img, t); z = 1.6 - 0.25 * eout(ramp(t, 0, 0.6))
    fig(img, 380, FLOOR, z, NB); emoji(img, '😰', 380, FLOOR - 150 * z, 64 * z / 1.6)
    gwen(img, 820, 1.2, t=t)
    if t > 0.6: label(img, 380, 1310, 'OWEN · DAY 1', NB, ramp(t, 0.6, 0.9), 34)
    if t < 2.6: big(img, 'DAY 1. NEW JOB.', W / 2, 560, 100, GOLD, a=ramp(t, 0.0, 0.15), sc=0.8 + 0.2 * back(ramp(t, 0, 0.25)))
    if t > 2.6: big(img, 'HATES HIM', W / 2, 560, 120, NRED, a=ramp(t, 2.6, 2.9), sc=0.7 + 0.3 * back(ramp(t, 2.6, 2.9)))
def s2(img, t, d):
    stage(img, t); desk(img, W / 2, 1080); gwen(img, W / 2, 1.5, t=t)
    label(img, W / 2, 1320, 'GRUMPY GWEN · 11 YEARS AT THIS DESK', PINK, ramp(t, 0.2, 0.5), 32)
    big(img, str(int(counter(t, 1.6, 2.6, 11, 0))), W / 2, 560, 200, NRED, a=ramp(t, 1.4, 1.7))
    label(img, W / 2, 700, 'WORDS SAID TO OWEN', NW, ramp(t, 1.6, 1.9), 30)
def s3(img, t, d):
    stage(img, t, floor=False)
    big(img, '"GOOD MORNING"', W / 2, 520, 92, GOLD, a=ramp(t, 0.1, 0.4))
    for i, dn in enumerate(['MON', 'TUE', 'WED', 'THU', 'FRI']):
        k = back(ramp(t, 1.4 + i * 0.18, 1.7 + i * 0.18)); x = 150 + i * 195
        if k > 0: rrect(img, x - 80 * k, 760 - 80 * k, 160 * k, 160 * k, 16, NW if i < 4 else GOLD, 3)
        if k > 0.8: text(img, dn, x, 760, 40, NW if i < 4 else GOLD, INTER_B)
    for i in range(4):
        k = back(ramp(t, 3.4 + i * 0.2, 3.7 + i * 0.2))
        if k > 0: circ(img, (240 + i * 200, 1060), 60 * k, NB, 4); text(img, str(i + 1), 240 + i * 200, 1060, 60, NB, INTER_B, scale=k)
    label(img, W / 2, 1180, 'PSYCHOLOGY TRICKS', NB, ramp(t, 3.6, 3.9), 34)
def trick_card(img, t, day, n, name, col=NB):
    stage(img, t); chip(img, day, ramp(t, 0, 0.2))
    k = back(ramp(t, 0.1, 0.4)); circ(img, (W / 2, 700), 130 * k, col, 6)
    if k > 0.5: big(img, str(n), W / 2, 700, 160, col)
    big(img, name, W / 2, 960, 74, NW, a=ramp(t, 0.6, 0.9))
def s4(img, t, d): trick_card(img, t, 'MONDAY', 1, 'BEN FRANKLIN EFFECT')
def s5(img, t, d):
    stage(img, t)
    k = ramp(t, 0.1, 0.4); rrect(img, 320, 560, 440, 300, 14, mix(BG, GOLD, k), 4); line(img, (540, 560), (540, 860), mix(BG, GOLD, k), 3)
    text(img, 'RARE BOOK', 540, 920, 40, mix(BG, GOLD, k), INTER_B)
    fig(img, 300, FLOOR, 1.0, NW, ramp(t, 0.2, 0.5)); fig(img, 780, FLOOR, 1.0, DIM, ramp(t, 0.2, 0.5))
    if t > 3.0:
        k2 = back(ramp(t, 3.0, 3.3)); emoji(img, '🤝', W / 2, 1120, 110 * k2)
    if t > 4.6: label(img, W / 2, 400, 'FAVOR DONE = MORE LIKING', NB, ramp(t, 4.6, 4.9), 36)
def s6(img, t, d):
    stage(img, t); desk(img, 780, 1080, 260); gwen(img, 780, 1.2, t=t)
    fig(img, 300, FLOOR, 1.2, NB)
    u = ease(ramp(t, 1.4, 2.6)); stapler(img, 700 - 300 * u, 940 + 60 * u, 0.9)
    if t > 2.8: label(img, 780, 700, 'DIDN\'T EVEN LOOK', PINK, ramp(t, 2.8, 3.1), 32)
def s7(img, t, d):
    stage(img, t); meter(img, t, 2, 9, 0.6); fig(img, W / 2, FLOOR, 1.4, NB)
    if t > 2.0: emoji(img, '😏', W / 2 + 150, FLOOR - 250, 90 * back(ramp(t, 2.0, 2.3)))
def s8(img, t, d):
    trick_card(img, t, 'TUESDAY', 2, 'MERE EXPOSURE EFFECT')
    if t > 2.6:
        for i in range(5): circ(img, (300 + i * 120, 1150), 26 * back(ramp(t, 2.6 + i * 0.1, 2.9 + i * 0.1)), mix(BG, NB, 0.7), 3)
def s9(img, t, d):
    stage(img, t); desk(img, W / 2, 1080, 260); gwen(img, W / 2, 1.2, t=t)
    x = W / 2 + 520 * math.sin(t * 3.2); fig(img, x, FLOOR + 40, 0.9, NB, 0.9)
    big(img, str(int(counter(t, 0.1, 3.2, 1, 47))), W / 2, 500, 180, GOLD)
    label(img, W / 2, 640, 'TIMES WALKED PAST', NW, 1, 30)
    if t > 3.4:
        k = back(ramp(t, 3.4, 3.7)); rrect(img, 240, 720, 600 * k, 150, 18, NW, 3)
        if k > 0.8: text(img, 'HR: "Quick chat?" 📅'.replace(' 📅', ''), 540, 795, 46, NW, INTER_B); emoji(img, '📅', 800, 795, 60)
def s10(img, t, d): trick_card(img, t, 'WEDNESDAY', 3, 'MIRRORING')
def s11(img, t, d):
    stage(img, t); gwen(img, 300, 1.2, cloud=False, t=t); fig(img, 780, FLOOR, 1.2, NB)
    ph = int(t / 1.3)
    if ph < 2:
        for x, col in ((360, PINK), (840, GOLD)): mug(img, x, 1000 - 30 * abs(math.sin(t * 3)), 0.8, 1, col)
        label(img, W / 2, 420, 'SIP · SIP', NW, 1, 40)
    else:
        if t < 4.2: text(img, 'ACHOO!', 300, 820, 80, PINK, INTER_B, scale=back(ramp(t, 2.6, 2.9)))
        if t > 3.2: text(img, 'achoo?', 780, 820, 60, NB, INTER_B, scale=back(ramp(t, 3.2, 3.5)))
    if t > 4.3: meter(img, t, 9, -4, 4.3, y=420)
def s12(img, t, d):
    trick_card(img, t, 'THURSDAY', 4, 'PRATFALL EFFECT')
    if t > 2.0: big(img, '1966', W / 2, 1160, 90, GOLD, a=ramp(t, 2.0, 2.3))
    if t > 4.0:
        mug(img, 820, 1360, 0.9, 1, GOLD, tilt=1.2 * ease(ramp(t, 4.0, 4.6)))
        emoji(img, '🧠', 260, 1360, 90 * back(ramp(t, 4.2, 4.5)))
def s13(img, t, d):
    stage(img, t); fig(img, W / 2, FLOOR, 1.5, NB)
    k = ease(ramp(t, 0.6, 1.2)); mug(img, W / 2 + 120 - 40 * k, 980 + 80 * k, 0.9, 1, GOLD, tilt=2.0 * k)
    if t > 1.2:
        for i in range(10):
            u = ramp(t, 1.2, 2.0); circ(img, (W / 2 + 40 - i * 12, 1020 + i * 22 * u), 10, GOLD)
    if t > 2.0: big(img, 'ON PURPOSE', W / 2, 520, 110, GOLD, a=ramp(t, 2.0, 2.3))
def s14(img, t, d):
    stage(img, t, floor=False)
    for i, (lab, h, col) in enumerate((('BRILLIANT + SPILL', 470, (90, 220, 120)), ('AVERAGE + SPILL', 160, NRED))):
        x = 330 + i * 420; hh = h * eout(ramp(t, 0.6 + i * 2.2, 1.4 + i * 2.2))
        rrect(img, x - 100, 1150 - hh, 200, max(2, hh), 12, col); text(img, lab, x, 1210, 32, NW, INTER_B)
        if hh > 10: text(img, '▲' if i == 0 else '▼', x, 1100 - hh, 60, col, INTER_B)
    label(img, W / 2, 420, 'ONLY IF YOU\'RE GOOD AT YOUR JOB', GOLD, ramp(t, 0.3, 0.6), 34)
def s15(img, t, d):
    stage(img, t); window(img, W / 2, 760, 700, 440, 'budget_FINAL_v9.xlsx', 1)
    for i in range(3):
        k = back(ramp(t, 0.3 + i * 0.5, 0.6 + i * 0.5))
        if k > 0: text(img, 'CRASHED', W / 2, 700 + i * 70 - 40, 56, NRED, INTER_B, scale=k)
    if t > 2.4: meter(img, t, -4, 0, 2.4, y=1180)
def s16(img, t, d):
    stage(img, t); desk(img, 780, 1080, 260); gwen(img, 780, 1.2, cloud=t < 3.4, t=t); fig(img, 300, FLOOR, 1.2, NB)
    chip(img, 'FRIDAY', 1)
    if t > 2.2: big(img, '"GOOD MORNING, GWEN."', W / 2, 560, 64, NB, a=ramp(t, 2.2, 2.5))
def s17(img, t, d):
    stage(img, t); desk(img, 780, 1080, 260); fig(img, 780, FLOOR, 1.4, PINK); fig(img, 300, FLOOR, 1.2, NB)
    emoji(img, '🙂', 780, FLOOR - 300, 80 * back(ramp(t, 0.1, 0.4)))
    if t > 1.3: stapler(img, 300, 820, 1.0, 1, NRED); text(img, '?', 300, 700, 90, NRED, INTER_B, scale=back(ramp(t, 1.3, 1.6)))
    meter(img, t, 0, 100, 0.4, y=420)
def s18(img, t, d):
    stage(img, t); fig(img, W / 2, FLOOR, 1.7, NB)
    for i, ch in enumerate('!?!'):
        text(img, ch, W / 2 - 80 + i * 80, FLOOR - 380, 120, GOLD, INTER_B, scale=back(ramp(t, 0.2 + i * 0.15, 0.5 + i * 0.15)))
    if t > 1.4: big(img, 'ON HIM?!', W / 2, 520, 140, NRED, a=ramp(t, 1.4, 1.7))
def s19(img, t, d):
    stage(img, t, floor=False)
    for i, nm in enumerate(['FAVOR', 'EXPOSURE', 'MIRROR', 'PRATFALL']):
        k = back(ramp(t, 0.1 + i * 0.2, 0.4 + i * 0.2)); x = 290 + (i % 2) * 500; y = 640 + (i // 2) * 360
        if k > 0: rrect(img, x - 210 * k, y - 140 * k, 420 * k, 280 * k, 26, NB if i % 3 == 0 else PINK, 4)
        if k > 0.8: big(img, str(i + 1), x, y - 30, 120, NW); text(img, nm, x, y + 80, 40, NW, INTER_B)
    label(img, W / 2, 1300, 'COMMENT 1 · 2 · 3 · 4', GOLD, ramp(t, 1.2, 1.5), 44)

NOZOOM = (s14, s19)
def timeline(ls, dur):
    fs = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19]
    return [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'hook_end': ls(1), 'whoosh': [ls(3), ls(7), ls(9), ls(11), ls(15)], 'ding': [ls(6) + 1.6, ls(16) + 0.5], 'pop': [ls(2) + 1.5, ls(2) + 3.5, ls(8) + 0.5, ls(8) + 1.5, ls(8) + 3.4, ls(18) + 0.2],
            'mistake': ls(10) + 4.3, 'boom': [ls(14) + 0.3, ls(17) + 1.4], 'notif': [ls(8) + 3.4], 'end': ls(18) - 0.05}

POST = {
 'title': "He Used 4 Psychology Tricks On His Grumpy Coworker 🧠 #shorts",
 'caption': "New guy Owen Onboarding has 5 days to make Grumpy Gwen say good morning. Ben Franklin effect, mere exposure, mirroring, the pratfall effect... one of them backfires badly ☕ And then Gwen asks for his stapler. Which trick have you used without knowing? Comment 1, 2, 3 or 4 👇",
 'tags': '#psychology #office #funny #storytime #benfranklineffect #animation',
 'source': "Sources: Jecker & Landy (1969), Human Relations — liking a person as a function of doing him a favour (Ben Franklin effect; Franklin's borrowed-book story from his Autobiography); Zajonc (1968), mere exposure effect; Chartrand & Bargh (1999), the chameleon effect (mimicry increases liking); Aronson, Willerman & Floyd (1966), Psychonomic Science — a blunder (spilled coffee) raised the likability of a superior contestant and lowered it for an average one. Owen and Gwen are fictional.",
}
