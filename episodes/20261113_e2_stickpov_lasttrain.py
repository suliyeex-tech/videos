import math, random
from kit import *
from stickpov import *
import stickpov as S

FORMAT = 'stickpov'
SLUG = '2026-11-13-pov-the-last-train'
VOICE = 'suspense'; CAPTION = 'karaoke'; MOOD = {'style': 'tension', 'root': 49.0}; ZOOM = 1.2; PROGRESS_COL = YEL
S.HUD.update({'clock': (3, 12), 'tag': 'NIGHT 1', 'place': 'LAST TRAIN', 'cd_label': 'DOORS OPEN IN'})
LINES = [
 ("You fall asleep on the last train home.", 0.15),
 ("You wake up at 3:12 AM. The train is still moving.", 0.2),
 ("Your phone says: no service. The next stop sign says... nothing.", 0.2),
 ("Every seat is empty. Except one.", 0.2),
 ("A guy with a ring light, live-streaming. His username? Livestream Larry.", 0.2),
 ("He whispers: rule one. Don't look at the windows.", 0.15),
 ("Too late. You look.", 0.3),
 ("There's no tunnel. Just your own station, passing by. Again. And again.", 0.2),
 ("Larry's viewer count drops to zero.", 0.25),
 ("Rule two, he says. When the doors open, only one of us gets off.", 0.25),
 ("The train slows down. The doors slide open.", 0.3),
 ("Do you step off? Or let Larry go first? Comment A or B. Part two decides.", 1.0),
]
CAPS = [
 ["YOU FALL {ASLEEP}", "ON THE [LAST TRAIN]", "HOME."], ["YOU WAKE UP", "AT [3:12 AM.]", "THE TRAIN IS", "{STILL MOVING.}"],
 ["YOUR PHONE SAYS:", "{NO SERVICE.}", "THE NEXT STOP", "SIGN SAYS...", "[NOTHING.]"], ["EVERY SEAT", "IS EMPTY.", "{EXCEPT ONE.}"],
 ["A GUY WITH", "A [RING LIGHT,]", "LIVE-STREAMING.", "HIS USERNAME?", "[LIVESTREAM LARRY.]"], ["HE WHISPERS:", "[RULE ONE.]", "{DON'T LOOK}", "AT THE WINDOWS."],
 ["TOO LATE.", "{YOU LOOK.}"], ["THERE'S NO TUNNEL.", "JUST [YOUR STATION,]", "PASSING BY.", "{AGAIN.}", "{AND AGAIN.}"],
 ["LARRY'S VIEWERS", "DROP TO {ZERO.}"], ["[RULE TWO:]", "WHEN THE DOORS OPEN,", "{ONLY ONE OF US}", "GETS OFF."],
 ["THE TRAIN", "SLOWS DOWN.", "THE DOORS", "[SLIDE OPEN.]"], []]
YOU = (210, 130, 50); LARRY = (40, 140, 245)
ST = {}; TL = {}
def T(f, t): return ST.get(f, 0) + t
def cd(f, t): return max(0, TL['open'] - T(f, t))

def station(sub, t, wx):
    sub[:] = (60, 70, 60); off = int((t * 900 + wx * 2) % 700) - 350
    cv2.rectangle(sub, (off, 60), (off + 220, 130), (230, 230, 235), -1); cv2.putText(sub, 'MAPLE ST', (off + 18, 112), cv2.FONT_HERSHEY_DUPLEX, 1.2, (40, 30, 30), 2, cv2.LINE_AA)
    cv2.rectangle(sub, (0, 230), (259, 319), (90, 100, 90), -1)

def s1(img, t, d):
    train(img, t, dark=0.2)
    stick(img, 540, 1400, 0.95, YOU, 'closed' if t < d - 0.4 else 'o', look=0)
    for k in range(3): text(img, 'z', 640 + k * 34 + 10 * math.sin(t * 3 + k), 760 - k * 50 - 20 * ((t + k * 0.3) % 1), 50 + k * 10, WHITE, INTER_B, alpha=0.8 * (1 - ramp(t, d - 0.5, d)))
    hud(img, T(s1, t), None)
def s2(img, t, d):
    train(img, t, speed=1.4)
    stick(img, 540, 1400, 0.95, YOU, 'shock', look=-1 + 2 * (int(t * 1.5) % 2))
    hud(img, T(s2, t), None)
def s3(img, t, d):
    train(img, t, dark=0.3)
    hand_phone(img, t, lambda im, cx, cy, w, h: lock_screen(im, cx, cy, w, h, '3:13', 'No Service', note='No service' if t > 0.6 else None), rise=ramp(t, 0, 0.35))
    hud(img, T(s3, t), None)
def s4(img, t, d):
    train(img, t)
    pan = 200 * ease(ramp(t, 0, d))
    stick(img, 300 - pan, 1400, 0.85, YOU, 'flat', look=1)
    if t > 1.0: stick(img, 980 - pan, 1400, 0.85, LARRY, 'flat', look=-1, arm='phone')
    hud(img, T(s4, t), None)
def s5(img, t, d):
    train(img, t)
    stick(img, 560, 1420, 1.1, LARRY, 'happy', look=-1, arm='phone')
    glow(img, 700, 650, 300, (100, 100, 100), 0.9); cv2.circle(img, P(700, 650), 90 * 8, (230, 230, 240), 10, cv2.LINE_AA, 3)
    k = back(ramp(t, 1.8, 2.1))
    rrect(img, 120, 330, 840 * k, 110, 26, RED)
    if k > 0.8: text(img, '● LIVE  @LivestreamLarry  1,204', W / 2, 385, 40, WHITE, INTER_B)
    hud(img, T(s5, t), None)
def s6(img, t, d):
    train(img, t, dark=0.35)
    stick(img, 540, 1450, 1.25, LARRY, 'o', look=0, arm='phone')
    k = back(ramp(t, 0.6, 0.85)); rrect(img, W / 2 - 250 * k, 300, 500 * k, 90, 20, YEL)
    if k > 0.8: text(img, 'RULE 1', W / 2, 345, 54, INK2, INTER_B)
    hud(img, T(s6, t), None)
def s7(img, t, d):
    train(img, t, outside=station, dark=0.2)
    stick(img, 540, 1400, 0.95, YOU, 'shock', look=-1)
    hud(img, T(s7, t), None)
def s8(img, t, d):
    img[:] = (60, 70, 60)
    off = int((t * 1500) % 1400) - 700
    for k in range(2):
        x = off + k * 1400
        rrect(img, x + 100, 700, 700, 220, 16, (230, 230, 235)); text(img, 'MAPLE ST', x + 450, 810, 140, (40, 30, 30), INTER_B)
    rrect(img, 0, 1200, W, 720, 0, (90, 100, 90))
    for k in range(int(t * 1.6)): text(img, 'AGAIN', 220 + (k % 4) * 210, 1520 + (k // 4) * 90 + (k % 2) * 40, 64, RED, INTER_B)
    hud(img, T(s8, t), None, red=True)
def s9(img, t, d):
    train(img, t, dark=0.4)
    def scr(im, cx, cy, w, h):
        x0, y0 = int(cx - w / 2), int(cy - h / 2); im[max(0, y0):max(0, min(H, y0 + int(h))), x0:x0 + int(w)] = (40, 30, 30)
        v = int(1204 * (1 - ease(ramp(t, 0.3, 1.6))))
        rrect(im, cx - 160, cy - 300, 320, 90, 20, RED); text(im, '● LIVE', cx, cy - 255, 44, WHITE, INTER_B)
        text(im, f'{v:,}', cx, cy, 170, WHITE if v else RED, INTER_B); text(im, 'watching', cx, cy + 110, 40, (190, 190, 190), INTER_M)
    hand_phone(img, t, scr, rise=ramp(t, 0, 0.3))
    hud(img, T(s9, t), None)
def s10(img, t, d):
    train(img, t, dark=0.45, light_flicker=True)
    stick(img, 330, 1400, 0.95, YOU, 'shock', look=1); stick(img, 760, 1400, 0.95, LARRY, 'flat', look=-1)
    k = back(ramp(t, 0.2, 0.45)); rrect(img, W / 2 - 250 * k, 300, 500 * k, 90, 20, YEL)
    if k > 0.8: text(img, 'RULE 2', W / 2, 345, 54, INK2, INTER_B)
    hud(img, T(s10, t), cd(s10, t))
def s11(img, t, d):
    train(img, t, speed=max(0.05, 1 - t / 1.5), dark=0.3)
    op = eout(ramp(t, 1.4, 2.4))
    rrect(img, 300 - 200 * op, 420, 240, 960, 6, (120, 130, 125)); rrect(img, 540 + 200 * op, 420, 240, 960, 6, (120, 130, 125))
    if op > 0: glow(img, W / 2, 900, int(500 * op), (230, 240, 250), 1.6 * op); rrect(img, 540 - 200 * op, 420, 400 * op, 960, 0, mix((60, 60, 60), (250, 250, 250), op))
    hud(img, T(s11, t), cd(s11, t))
def bg_end(img, t):
    train(img, t, dark=0.5); rrect(img, 340, 420, 400, 960, 0, (240, 240, 245)); glow(img, W / 2, 900, 500, (200, 210, 220), 1.2)
    stick(img, 260, 1400, 0.8, YOU, 'o', look=1); stick(img, 820, 1400, 0.8, LARRY, 'happy', look=-1, arm='phone')
def s12(img, t, d): choice_end(img, t, 'STEP OFF', 'LET LARRY GO', 'PART 2', bg=bg_end)

NOZOOM = (s12,)
def timeline(ls, dur):
    tl = [(0, s1), (ls(1) - 0.05, s2), (ls(2) - 0.05, s3), (ls(3) - 0.05, s4), (ls(4) - 0.05, s5), (ls(5) - 0.05, s6), (ls(6) - 0.05, s7),
          (ls(7) - 0.05, s8), (ls(8) - 0.05, s9), (ls(9) - 0.05, s10), (ls(10) - 0.05, s11), (ls(11) - 0.05, s12)]
    for a, f in tl: ST[f] = round(a * 30) / 30
    TL['open'] = ls(10) + 2.0
    return tl
def SFX(ls, dur):
    return {'hook_end': ls(1), 'notif': [ls(2) + 0.6], 'boom': [ls(6) + 0.3, ls(8) + 1.6], 'heart': [(ls(7), ls(10))], 'riser': [ls(10) + 1.9],
            'whoosh': [ls(7) + 0.2], 'end': ls(11) - 0.05}

POST = {
 'title': "POV: You Wake Up On The Last Train 🚇 Part 1 #shorts",
 'caption': "You fall asleep on the last train. 3:12 AM. No service. One other passenger: Livestream Larry. Do you step off, or let Larry go first? Comment A or B 👇",
 'tags': '#pov #storytime #creepy #animation #choices #part1',
 'source': 'Original fiction.',
}
