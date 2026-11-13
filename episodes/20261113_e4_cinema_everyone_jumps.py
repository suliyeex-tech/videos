import math, random
from kit import *
from cinema import *

FORMAT = 'cinema'
SLUG = '2026-11-13-what-if-everyone-jumped-at-once'
CAPTION = 'serif'; MOOD = {'style': 'cinematic', 'root': 55.0}; PROGRESS = False; VIGNETTE = 0.35; ZOOM = 0.8
LINES = [(None, 3.4), (None, 2.6), (None, 2.6), (None, 2.8), (None, 2.6), (None, 2.4), (None, 2.8), (None, 3.4), (None, 3.6), (None, 3.0), (None, 2.8), (None, 3.2), (None, 3.6)]
CAPS = [
 ["Every human on Earth agreed to {jump.} At the exact same second."], ["Stadiums went quiet."], ["Farmers stopped their tractors."],
 ["Pilots kindly asked passengers to {remain seated.}"], ["10... 9... 8..."], ["3... 2... 1..."], ["{Jump.}"],
 ["Together, all of us weigh less than a {ten-trillionth} of the planet."], ["So Earth moved... by {less than the width of a single atom.}"],
 ["Then we all landed. And it moved {right back.}"], ["Total effect on the planet: {zero.}"], ["Total effect on group chats: {unmeasurable.}"], []]
POP0 = 8_300_412_087
ST = {}; TL = {}
def T(f, t): return ST.get(f, 0) + t
def pop(Tabs): return POP0 + int(Tabs * 2.4)

def c1(img, t, d):
    city(img, t, night=0.15); crowd(img, t, 1150, 1700, 70, seed=2); grade(img, warm=0.08)
    counter_overlay(img, 'WORLD POPULATION', pop(T(c1, t)), 'NOON · UTC')
def c2(img, t, d):
    stadium(img, t); crowd(img, t, 1300, 1750, 40, seed=5, s0=0.6, s1=1.0)
    counter_overlay(img, 'WORLD POPULATION', pop(T(c2, t)))
def c3(img, t, d):
    field(img, t); grade(img, warm=0.1); counter_overlay(img, 'WORLD POPULATION', pop(T(c3, t)))
def c4(img, t, d):
    cabin(img, t); lower_third(img)
def countdown(img, t, d, nums):
    city(img, t, night=0.85); crowd(img, t, 1150, 1750, 90, seed=8, arms=0.15); lower_third(img)
    seg = d / len(nums); i = min(len(nums) - 1, int(t / seg)); u = (t - i * seg) / seg
    k = back(ramp(u, 0, 0.25)); glow(img, W / 2, 700, 420, (60, 80, 120), 0.6)
    text(img, str(nums[i]), W / 2, 700, 380, WHITE, SERIF_I, scale=0.6 + 0.4 * k, alpha=1 - ramp(u, 0.8, 1))
def c5(img, t, d): countdown(img, t, d, [10, 9, 8])
def c6(img, t, d): countdown(img, t, d, [3, 2, 1])
def c7(img, t, d):
    city(img, t, night=0.6); j = eout(ramp(t, 0.05, 0.6)) * (1 - ease(ramp(t, 1.8, d)))
    crowd(img, t, 1150, 1750, 110, seed=8, jump=j, arms=j)
    counter_overlay(img, 'PEOPLE IN THE AIR', pop(T(c7, t)) * eout(ramp(t, 0, 0.5)))
    flash(img, t, 0.05, 0.2, WHITE, 0.4)
def c8(img, t, d):
    img[:] = grad((30, 10, 5), (10, 4, 2)); stars(img, t, 0.7, base=(20, 8, 4))
    earth(img, W / 2 + 120, 760, 380, t)
    for i in range(int(eout(ramp(t, 0.3, 1.6)) * 60)): circ(img, (180 + (i % 10) * 10, 1100 - (i // 10) * 10), 3, (220, 220, 255))
    text(img, 'ALL OF US', 230, 1160, 30, WHITE, INTER_B)
def c9(img, t, d):
    img[:] = grad((40, 15, 10), (10, 5, 3)); z = 1 + 3 * ease(ramp(t, 0, 2.0))
    atom(img, W / 2, 760, t, s=0.5 * z)
    k = ramp(t, 2.0, 2.4); line(img, (W / 2 - 4, 380), (W / 2 + 4, 380), YEL, 6)
    text(img, 'EARTH MOVED  <  THIS', W / 2, 330, 34, YEL, INTER_B, alpha=k)
def c10(img, t, d):
    city(img, t, night=0.5); j = 1 - eout(ramp(t, 0, 0.5))
    crowd(img, t, 1150, 1750, 110, seed=8, jump=j * 0.6)
    if t > 0.5:
        for s_ in range(3): cv2.ellipse(img, P(W / 2, 1600), (int((200 + 300 * ramp(t, 0.5, 1.5) + s_ * 80) * 8), int((40 + 60 * ramp(t, 0.5, 1.5) + s_ * 16) * 8)), 0, 0, 360, (200, 200, 210), 3, cv2.LINE_AA, 3)
    lower_third(img)
def c11(img, t, d):
    img[:] = grad((30, 10, 5), (10, 4, 2)); stars(img, t, 0.7, base=(20, 8, 4)); earth(img, W / 2, 700, 340, t)
    counter_overlay(img, 'EFFECT ON THE PLANET', 0, None, 1)
def c12(img, t, d):
    img[:] = grad((50, 30, 25), (20, 12, 10))
    rb = random.Random(4)
    for i in range(int(t * 26)):
        x = rb.uniform(80, W - 80); y = rb.uniform(250, 1200); rrect(img, x - 120, y - 40, 240, 80, 24, (70, 64, 62)); emoji(img, rb.choice(['😂', '🤣', '😭', '🔥', '💀', '🦘']), x - 80, y, 46)
        text(img, rb.choice(['did u feel it', 'THAT WAS IT??', 'lmaooo', 'i jumped late', 'my knee']), x + 20, y, 26, WHITE, INTER_M)
    counter_overlay(img, 'MESSAGES SENT', 12_000_000 * ease(ramp(t, 0, d)) * (1 + 40 * ramp(t, 1, d)))
def c13(img, t, d):
    img[:] = (8, 8, 10)
    text(img, 'What if every human on', W / 2, 860, 62, WHITE, SERIF_I, alpha=ramp(t, 0.2, 0.7))
    text(img, 'Earth jumped at once?', W / 2, 950, 62, WHITE, SERIF_I, alpha=ramp(t, 0.4, 0.9))
    text(img, 'FOLLOW FOR MORE WHAT IFS', W / 2, 1600, 30, (190, 190, 195), INTER_B, alpha=ramp(t, 1.2, 1.6))

NOZOOM = (c13,)
def timeline(ls, dur):
    fs = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13]
    tl = [(ls(i), f) for i, f in enumerate(fs)]
    for a, f in tl: ST[f] = a
    return tl
def SFX(ls, dur):
    return {'hook_end': 0.5, 'tick': [ls(4) + k * dur(4) / 3 for k in range(3)] + [ls(5) + k * dur(5) / 3 for k in range(3)],
            'boom': [ls(6) + 0.05, ls(9) + 0.5], 'whoosh': [ls(6)], 'notif': [ls(11) + k * 0.25 for k in range(10)], 'end': ls(12)}

POST = {
 'title': "What If Every Human Jumped At Once? 🌍 #shorts",
 'caption': "8.3 billion people. One second. One jump. Here's what would actually happen to the planet 🌍",
 'tags': '#whatif #science #earth #physics #animation #cinematic',
 'source': 'Sources: UN World Population Prospects 2024 (~8.3 billion in 2026); xkcd What If #8 / HowStuffWorks: Earth would move less than an atom\'s width.',
}
