import math, random
from kit import *
from neon import *

FORMAT = 'neon'
SLUG = '2026-11-13-why-you-cant-stop-scrolling'
VOICE = 'hype'; CAPTION = 'top'; TICKS = True; MOOD = {'style': 'hype', 'root': 55.0}
ACCENT = NB; PROGRESS_COL = NB; VIGNETTE = 0.0; ZOOM = 0.7; TOP_Y = 330
LINES = [
 ("The reason you can't stop scrolling was invented by one guy, in 2006.", 0.15),
 ("His name is Aza Raskin. And today, he regrets it.", 0.2),
 ("Before him, every page had a bottom. You hit next, and your brain got a tiny chance to stop.", 0.15),
 ("So he deleted the bottom.", 0.25),
 ("Then apps added one more trick. You never know if the next video is boring... or amazing.", 0.15),
 ("Psychologists call that a variable reward. It's the same pattern slot machines use.", 0.15),
 ("And in experiments, it's the reward pattern that's hardest to quit.", 0.2),
 ("So every swipe is basically a pull of the lever.", 0.2),
 ("Raskin estimates infinite scroll eats about two hundred thousand human lifetimes. Every single day.", 0.25),
 ("The fix? Give your brain the bottom back.", 0.15),
 ("Decide when you'll stop, before you start.", 0.2),
 ("And if you're still here... prove it. Don't swipe.", 0.6),
]
CAPS = [
 ["The reason you can't stop {scrolling} was invented by one guy, in {2006.}"], ["His name is {Aza Raskin.} And today, he {regrets it.}"],
 ["Before him, every page had a {bottom.} Your brain got a tiny chance to {stop.}"], ["So he {deleted} the bottom."],
 ["You never know if the next video is {boring...} or {amazing.}"], ["Psychologists call it a {variable reward.} Slot machines use the {same pattern.}"],
 ["It's the reward pattern that's {hardest to quit.}"], ["Every swipe is a {pull of the lever.}"],
 ["About {200,000 human lifetimes.} Every single day."], ["The fix? Give your brain {the bottom back.}"],
 ["Decide when you'll {stop,} before you {start.}"], ["Still here? Prove it. {Don't swipe.}"]]

def s_hook(img, t, d):
    stage(img, t)
    phone(img, W / 2, 900, 1.0, a=eout(ramp(t, 0, 0.25)), col=NW,
          screen=lambda cx, cy, w, h: feed(img, cx, cy, w, h, t * 900, hi=lambda k: NB if k % 5 == 2 else DIM))
    k = back(ramp(t, 2.3, 2.6)); big(img, '2006', W / 2, 1400, 150, NB, a=k, sc=0.6 + 0.4 * k)
def s_aza(img, t, d):
    stage(img, t)
    fig(img, W / 2, FLOOR, 1.6, NB, a=eout(ramp(t, 0, 0.3)))
    label(img, W / 2, FLOOR + 50, 'INVENTOR OF INFINITE SCROLL', NW, ramp(t, 0.3, 0.6))
    if t > 1.6:
        q = back(ramp(t, 1.6, 1.85)); window(img, 790, 760, 300, 150, '', q); text(img, 'REGRETS IT', 790, 790, 40, NRED, INTER_B, alpha=q)
def s_bottom(img, t, d):
    stage(img, t)
    window(img, 400, 860, 440, 620, 'PAGE 1', eout(ramp(t, 0, 0.3)))
    for j in range(5): rrect(img, 210, 640 + j * 90, 380, 50, 6, mix(BG, DIM, 0.8))
    k = back(ramp(t, 1.0, 1.3)); rrect(img, 300, 1110, 200 * k, 56, 28, mix(BG, NB, k)); text(img, 'NEXT >', 400, 1138, 32, BG, INTER_B, alpha=k)
    fig(img, 820, FLOOR, 1.2, NB, sad=False)
    if t > 2.6: label(img, 820, FLOOR + 50, 'STOP POINT', NB, ramp(t, 2.6, 2.9))
def s_delete(img, t, d):
    stage(img, t)
    off = 400 * eout(ramp(t, 0.3, 1.2))
    window(img, W / 2, 860, 460, 700, 'PAGE 1', 1)
    for j in range(8):
        y = 640 + j * 90 - off
        if 560 < y < 1180: rrect(img, W / 2 - 190, y, 380, 50, 6, mix(BG, DIM, 0.8))
    k = 1 - ramp(t, 0.1, 0.4); rrect(img, W / 2 - 100, 1150 + 30 * (1 - k), 200, 56, 28, mix(BG, NB, k))
    for j in range(3):
        y = 1230 + 40 * j + 20 * math.sin(t * 6 + j); poly(img, [(W / 2 - 24, y), (W / 2 + 24, y), (W / 2, y + 26)], mix(BG, NB, 1 - j * 0.3))
    flash(img, t, 0.1, 0.15, NB, 0.25)
def s_unknown(img, t, d):
    stage(img, t)
    off = t * 520
    phone(img, W / 2, 900, 1.05, screen=lambda cx, cy, w, h: feed(img, cx, cy, w, h, off, hi=lambda k: GOLD if (k * 7) % 5 == 0 else DIM))
    q = int(t * 3) % 2
    big(img, 'BORING' if q == 0 else 'AMAZING?!', W / 2, 1390, 90, DIM if q == 0 else GOLD, a=ramp(t, 0.4, 0.6))
def s_slot(img, t, d):
    stage(img, t)
    slot(img, W / 2 - 30, 860, t, spin=True, a=eout(ramp(t, 0, 0.3)))
    label(img, W / 2, 1130, 'VARIABLE REWARD', NB, ramp(t, 0.5, 0.8), 34)
def s_graph(img, t, d):
    stage(img, t, floor=False)
    x0, y0, w, h = 170, 1200, 740, 560
    line(img, (x0, y0), (x0 + w, y0), DIM, 3); line(img, (x0, y0), (x0, y0 - h), DIM, 3)
    curve(img, t, x0, y0, w, h * 0.55, 'fi', 0.8, DIM, 'FIXED')
    curve(img, t - 0.2, x0, y0, w, h * 0.85, 'fr', 0.8, DIM, '')
    curve(img, t - 0.4, x0, y0, w, h, 'vr', 1, NB, 'VARIABLE')
    text(img, 'KEEP GOING AFTER REWARDS STOP', W / 2, y0 + 60, 30, DIM, INTER_B)
def s_lever(img, t, d):
    stage(img, t)
    sw = (t * 1.6) % 1; up = eout(min(1, sw * 2.5))
    phone(img, 330, 880, 0.75, screen=lambda cx, cy, w, h: feed(img, cx, cy, w, h, up * 300 + int(t * 1.6) * 300))
    circ(img, (330, 1000 - 220 * up), 34, mix(BG, NW, 0.9), 3)
    slot(img, 760, 880, t * 1.6, spin=True)
    text(img, '=', 545, 880, 120, NB, INTER_B)
def s_lifetimes(img, t, d):
    stage(img, t, floor=False)
    v = counter(t, 0.2, max(1.0, d - 1.4), 0, 200000)
    n = int(v / 200000 * 180)
    for i in range(n):
        x = 120 + (i % 18) * 47; y = 1560 - (i // 18) * 64; fig(img, x, y, 0.28, NB if i % 7 else NW, g=False)
    big(img, counter_text(v), W / 2, 680, 130, NB)
    text(img, 'LIFETIMES PER DAY', W / 2, 790, 40, NW, INTER_B)
def s_fix(img, t, d):
    stage(img, t)
    window(img, W / 2, 860, 460, 620, 'YOUR FEED', 1)
    for j in range(4): rrect(img, W / 2 - 190, 640 + j * 90, 380, 50, 6, mix(BG, DIM, 0.8))
    k = back(ramp(t, 0.6, 0.9)); line(img, (W / 2 - 200 * k, 1060), (W / 2 + 200 * k, 1060), NB, 8); neon_glow(img, W / 2, 1060, 240 * k, NB, 0.8)
    text(img, 'THE END', W / 2, 1110, 40, NB, INTER_B, alpha=k)
def s_timer(img, t, d):
    stage(img, t)
    cx, cy = W / 2, 880; circ(img, (cx, cy), 210, NW, 4)
    a = -math.pi / 2 + 2 * math.pi * eout(ramp(t, 0.2, 1.6)) * 0.33
    cv2.ellipse(img, P(cx, cy), (210 * 8, 210 * 8), -90, 0, math.degrees(a + math.pi / 2), NB, 14, cv2.LINE_AA, 3)
    line(img, (cx, cy), (cx + 160 * math.cos(a), cy + 160 * math.sin(a)), NB, 8); circ(img, (cx, cy), 14, NB)
    label(img, cx, cy + 290, 'STOP AT 10 MIN', NB, ramp(t, 0.8, 1.1), 34)
def s_end(img, t, d):
    stage(img, t)
    phone(img, W / 2, 880, 1.0, screen=lambda cx, cy, w, h: feed(img, cx, cy, w, h, 0))
    k = back(ramp(t, 1.4, 1.65)); big(img, "DON'T.", W / 2, 1330, 150, NRED, a=k, sc=0.5 + 0.5 * k)
    sh = 30 * math.sin(t * 7) if t < 1.4 else 0
    for j in range(3): poly(img, [(W / 2 - 30, 1180 - j * 50 + sh), (W / 2 + 30, 1180 - j * 50 + sh), (W / 2, 1150 - j * 50 + sh)], mix(BG, NW, 1 - j * 0.3))

NOZOOM = ()
def timeline(ls, dur):
    return [(0, s_hook), (ls(1) - 0.05, s_aza), (ls(2) - 0.05, s_bottom), (ls(3) - 0.05, s_delete), (ls(4) - 0.05, s_unknown), (ls(5) - 0.05, s_slot),
            (ls(6) - 0.05, s_graph), (ls(7) - 0.05, s_lever), (ls(8) - 0.05, s_lifetimes), (ls(9) - 0.05, s_fix), (ls(10) - 0.05, s_timer), (ls(11) - 0.05, s_end)]
def SFX(ls, dur):
    return {'hook_end': 0.5, 'boom': [ls(3) + 0.1, ls(8) + dur(8) - 1.2], 'ding': [ls(1) + 1.6, ls(9) + 0.6], 'pop': [ls(0) + 2.3], 'end': ls(11) + 1.3}

POST = {
 'title': "Why You Can't Stop Scrolling 🎰 #shorts",
 'caption': "The reason you can't stop scrolling was invented in 2006, and the guy who made it regrets it. Every swipe is a pull of the lever. 🎰 Still here? Prove it.",
 'tags': '#psychology #dopamine #scrolling #brain #facts #mindset',
 'source': "Sources: Aza Raskin's own estimate of 200,000 lifetimes/day (BBC, 2018); variable-ratio reinforcement (Skinner).",
}
