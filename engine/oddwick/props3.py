"""More Oddwick props (2026-11-19): terraced street + windows with sleepers, pea tube + flying peas, flames, alarm clock,
coins, searchlights, bats, cave, hangar, army car, ice tray, bomb canister, map arrow. Same style as odd.py/props2.py."""
import random, math
from odd import *
from props2 import *

BRICK = '#7a3a4a'

# ---------------------------------------------------------------- street of terraced houses (night)
WIN = [(x, y) for y in (560, 860) for x in (110, 400, 690, 980)]       # upper / lower window centres (w 190 x h 210)
def terrace(lit=(), sleepers=(), ids=True, fire=None, base=1200):
    """a row of brick terraced houses filling the frame; windows dark unless in `lit`. ids: win{k}-lit (warm overlay)."""
    s = sky(moon=True)
    for k, x0 in enumerate((-60, 250, 540, 830)):
        s += rect(x0 - 40, 340, 330, base - 340, grad(BRICK if k % 2 else '#6a3445'), 4, 6)
        s += path(f'M{x0 - 50},{340} L{x0 + 125},{240} L{x0 + 300},{340} Z', grad('#3a2a4a'), 6)
        s += rect(x0 + 215, 190, 40, 90, grad('#5a3a3a'), 4, 6)                                     # chimney
        s += rect(x0 + 60, base - 230, 110, 230, grad('#3a2a40'), 6, 6) + ell(x0 + 150, base - 120, 7, 7, WARM2)   # door
    for k, (x, y) in enumerate(WIN):
        s += rect(x - 95, y - 105, 190, 210, '#1c1538', 8, 9)
        if k in sleepers: s += g(person(f'sl{k}', 0, 120, .42, coat='#d8d0c0', skin='abcd'[k % 4], eyes='shut', mouth='flat', hat='beanie' if k % 2 else None), tr=f'translate({x},{y})')
        lid = f'id="win{k}-lit"' if ids else ''
        s += rect(x - 95, y - 105, 190, 210, WARM2, 8, 0, f'{lid} opacity="{.85 if k in lit else 0}"')
        s += path(f'M{x},{y - 105} L{x},{y + 105} M{x - 95},{y} L{x + 95},{y}', sw=8)
    s += floor_(base, '#3a3048', lines=True) + lamp(1000, 980)
    return s

def knocker(pid, x, y, s=1, eyes='norm', mouth='smirk', flip=False, coat='#5a4a8a', tube=True, young=False):
    """our knocker-up: long coat, shawl, bun; holds a long pea tube (id pid-tube) up and to the right"""
    t = g(rect(0, -14, 330, 28, grad('#b08a5a'), 14, 7) + ell(330, 0, 18, 18, '#3a2a20', 6), f'{pid}-tube', 'translate(60,-250) rotate(-38)') if tube else ''
    shawl = path('M-96,-210 Q0,-150 96,-210 L90,-170 Q0,-110 -90,-170 Z', '#8a2a4a' if not young else '#2a7a8a', 6)
    return person(pid, x, y, s, coat=coat, skin='a' if not young else 'd', hair='bun', coatlen=.7, eyes=eyes, mouth=mouth, flip=flip, extra_acc=shawl + t)

def pea(id, x, y, r=13): return ell(x, y, r, r, '#9ad04a', 5, f'id="{id}" opacity="0"')
def shoot(id, t, x0, y0, x1, y1, d=.28):
    """pea flies from (x0,y0) to (x1,y1) in d s, then vanishes"""
    return [fromto(f'#{id}', t, d, {'opacity': 1, 'x': 0, 'y': 0}, {'x': x1 - x0, 'y': y1 - y0}, 'power1.in'), setp(f'#{id}', t + d + .02, opacity=0)]
def tak(id, x, y, size=80): return text(x, y, 'TAK!', size, WARM2, extra=f'id="{id}" opacity="0"')
def pop(id, t, d=.18, hold=None):
    out = [fromto(f'#{id}', t, d, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    if hold: out.append(setp(f'#{id}', t + hold, opacity=0))
    return out
def light_win(k, t, on=True): return fromto(f'#win{k}-lit', t, .15, {'opacity': 0 if on else .85}, {'opacity': .85 if on else 0})

def flame(id, x, y, s=1):
    return g(path('M0,0 Q-70,-60 -40,-170 Q-20,-110 0,-120 Q10,-200 50,-240 Q40,-150 80,-110 Q100,-60 60,0 Z', '#ff8a2e', 7)
             + path('M0,-10 Q-30,-50 -14,-110 Q0,-80 14,-90 Q24,-60 30,-10 Z', '#ffe27a', 0), id, f'translate({x},{y}) scale({s})')
def flicker(id, t, d, every=.16):
    return [(t + k * every, f'tl.to("#{id}",{{scaleY:{1.15 if k % 2 else .88},scaleX:{.92 if k % 2 else 1.08},duration:{every:.2f},transformOrigin:"50% 100%"}},{{T}});') for k in range(int(d / every))]

def alarm_clock(id, x, y, s=1, opacity=1):
    c = (path('M-90,-70 L-130,-120 M90,-70 L130,-120', sw=14) + ell(-110, -115, 40, 30, grad('#c0c4d0'), 7) + ell(110, -115, 40, 30, grad('#c0c4d0'), 7)
         + ell(0, 0, 120, 120, grad('#d8423f'), 9) + ell(0, 0, 92, 92, '#fdfcf8', 7) + path('M0,0 L0,-60 M0,0 L42,20', sw=9)
         + path('M-70,110 L-90,150 M70,110 L90,150', sw=12))
    return g(c, id, f'translate({x},{y}) scale({s})', f'opacity="{opacity}"')
def price_tag(id, x, y, txt):
    return g(path('M-120,-50 L120,-50 L170,0 L120,50 L-120,50 Z', '#fdfcf8', 8) + ell(130, 0, 10, 10, OUT) + text(-10, 22, txt, 62, '#d8423f', extra='stroke-width="0"'), id, f'translate({x},{y}) rotate(-10)', 'opacity="0"')
def coin(id, x, y, s=1, label='6d'):
    return g(ell(0, 0, 90, 90, grad('#c8ccd8'), 9) + ell(0, 0, 66, 66, 'none', 5) + text(0, 26, label, 74, OUT, extra='stroke-width="0"'), id, f'translate({x},{y}) scale({s})', 'opacity="0"')
def notes(id, x, y, n=3):
    return g(''.join(path(f'M{i * 70},{-i * 40} l0,-70 l40,12', sw=8) + ell(i * 70 - 14, -i * 40, 18, 14, OUT) for i in range(n)), id, f'translate({x},{y})', 'opacity="0"')
def searchlights(id, n=3):
    return g(''.join(path(f'M{200 + i * 340},1250 L{80 + i * 340},-200 L{260 + i * 340},-200 Z', '#fff6c8', 0, f'id="{id}{i}" opacity=".22"') for i in range(n)), id)
def sweep(id, n, t, d):
    return [(t, f'tl.fromTo("#{id}{i}",{{rotation:{-14 + i * 9}}},{{rotation:{14 - i * 7},duration:{d:.2f},ease:"sine.inOut",transformOrigin:"{200 + i * 340}px 1250px"}},{{T}});') for i in range(n)]

# ---------------------------------------------------------------- bats story
def bat(id, x, y, s=1, bomb=False, eyes='norm'):
    """our bat: round fuzzy body, big ears, two scalloped wings (ids id-wl / id-wr flap with scaleY); optional tiny bomb"""
    wing = lambda side: g(path(f'M0,0 Q{side * 70},-70 {side * 150},-40 Q{side * 130},-10 {side * 120},10 Q{side * 95},0 {side * 85},20 Q{side * 60},10 {side * 50},26 Q{side * 30},12 0,20 Z', grad('#4a3a60'), 7),
                          f'{id}-w{"l" if side < 0 else "r"}')
    E = (ell(-18, -10, 12, 14, '#fff', 4) + ell(18, -10, 12, 14, '#fff', 4) + ell(-16, -8, 5, 6, OUT) + ell(20, -8, 5, 6, OUT)) if eyes == 'norm' else \
        (path('M-28,-8 L-8,-8 M8,-8 L28,-8', sw=6))
    body = (path('M-34,-40 L-46,-90 L-14,-52 Z', grad('#5a4a72'), 6) + path('M34,-40 L46,-90 L14,-52 Z', grad('#5a4a72'), 6)
            + ell(0, 0, 50, 54, grad('#5a4a72'), 8) + E + path('M-10,18 L-5,28 L0,18 L5,28 L10,18', sw=4, fill='#fff'))
    bm = g(path('M0,50 L0,64', sw=4) + rect(-16, 62, 32, 44, grad('#c0c4d0'), 10, 6) + rect(-16, 62, 32, 12, '#d8423f', 4, 0), tr='translate(0,0)') if bomb else ''
    return g(wing(-1) + wing(1) + bm + body, id, f'translate({x},{y}) scale({s})')
def flap(id, t, d, every=.12):
    return [(t + k * every, f'tl.to(["#{id}-wl","#{id}-wr"],{{scaleY:{-.4 if k % 2 == 0 else 1},duration:{every:.2f},transformOrigin:"50% 80%"}},{{T}});') for k in range(int(d / every))]
def swarm(prefix, n, cx, cy, spread=360, s=.6, seed=4, bomb=False):
    r = random.Random(seed)
    return ''.join(bat(f'{prefix}{i}', cx + r.randint(-spread, spread), cy + r.randint(-spread // 2, spread // 2), s * r.uniform(.7, 1.1), bomb) for i in range(n))
def swarm_fly(prefix, n, t, d, dx=600, dy=-300, seed=5):
    r = random.Random(seed); out = []
    for i in range(n):
        out.append(fromto(f'#{prefix}{i}', t + r.uniform(0, .3), d, {'x': 0, 'y': 0}, {'x': dx + r.randint(-200, 200), 'y': dy + r.randint(-200, 200)}, 'sine.inOut'))
        out += flap(f'{prefix}{i}', t, d, r.uniform(.09, .14))
    return out
def cave(dark='#1a1230'):
    s = rect(-400, -400, W + 800, H + 800, grad('#3a2a50', True), sw=0)
    s += path('M-400,-400 L1480,-400 L1480,500 Q1300,300 1100,420 Q900,250 700,380 Q500,220 300,360 Q100,240 -400,420 Z', grad('#2a1d40', True), 8)
    for k in range(9):   # stalactites
        x = 40 + k * 125; s += path(f'M{x - 40},{300 + (k % 3) * 40} L{x},{520 + (k % 4) * 60} L{x + 40},{300 + (k % 3) * 40} Z', grad('#4a3a66'), 7)
    s += rect(-400, 1350, W + 800, 900, grad('#2a1d40', True), sw=0) + pool(540, 1350, 600, 240)
    return s
def desert_base(base=1250):
    s = sky(moon=True, horizon='#ff9a4d') + path(f'M-400,{base - 120} Q200,{base - 260} 600,{base - 140} Q900,{base - 230} 1480,{base - 130} L1480,{base} L-400,{base} Z', grad('#6a4a5a'), 0)
    s += rect(-400, base, W + 800, H - base + 500, grad('#b07a4a', True), sw=0)
    for k in range(6): s += path(f'M{-300 + k * 260},{base + 60 + k % 2 * 30} L{-200 + k * 260},{base + 60 + k % 2 * 30}', sw=6, stroke='#8a5a3a')
    return s
def hangar(id, x, y, s=1, door_open=False):
    h = (path('M-330,0 L-330,-260 Q0,-470 330,-260 L330,0 Z', grad('#7a8090'), 9)
         + ''.join(path(f'M{-330 + k * 66},{-260 - (0 if k in (0, 10) else 0)} L{-330 + k * 66},0', sw=3, stroke='#5a6070') for k in range(1, 10))
         + rect(-220, -230, 440, 230, '#1c1538' if door_open else grad('#55607a'), 6, 8) + text(0, -300, 'HANGAR 1', 50, '#fdfcf8'))
    return g(h, id, f'translate({x},{y}) scale({s})')
def army_car(id, x, y, s=1, flip=False):
    c = (path('M-230,-60 L-200,-130 L-60,-140 L-20,-210 L140,-210 L190,-130 L240,-120 L250,-40 L-240,-40 Z', grad('#5a6a3a'), 9)
         + rect(0, -195, 120, 60, '#9fc8e8', 8, 6) + ell(-140, -30, 50, 50, '#2a2030', 8) + ell(150, -30, 50, 50, '#2a2030', 8)
         + ell(-140, -30, 20, 20, '#9a9aa8') + ell(150, -30, 20, 20, '#9a9aa8')
         + g(path('M-30,-90 L0,-120 L30,-90 L60,-120 L90,-90', sw=0) + path('M-120,-95 l14,-30 l14,30 z M-80,-95 l14,-30 l14,30 z', '#fdfcf8', 4), tr='translate(0,0)')
         + text(30, -70, '★', 60, '#fdfcf8', extra='stroke-width="0"'))
    sx = -s if flip else s
    return g(c, id, f'translate({x},{y}) scale({sx},{s})')
def canister(id, x, y, s=1, chute=False):
    c = rect(-60, -220, 120, 440, grad('#9aa0b0'), 30, 9) + ''.join(path(f'M-60,{-150 + k * 80} L60,{-150 + k * 80}', sw=5) for k in range(5)) + path('M-60,220 L0,280 L60,220', fill=grad('#7a8090'), sw=8)
    if chute: c = path('M-260,-560 Q0,-760 260,-560 Z', grad('#e8e2d0'), 9) + path('M-260,-560 L-50,-220 M260,-560 L50,-220 M0,-700 L0,-220', sw=4) + c
    return g(c, id, f'translate({x},{y}) scale({s})')
def ice_tray(id, x, y, s=1, bats=True):
    t = rect(-300, -60, 600, 120, '#bfe6ff', 14, 8)
    for k in range(5):
        t += rect(-280 + k * 116, -44, 100, 88, '#e6f6ff', 10, 5)
        if bats: t += g(bat(f'{id}b{k}', 0, 0, .55, eyes='shut'), tr=f'translate({-230 + k * 116},6)')
    return g(t, id, f'translate({x},{y}) scale({s})')
def letter(id, x, y, lines, s=1):
    l = rect(-260, -320, 520, 640, '#fdfcf8', 14, 9) + ''.join(path(f'M-200,{-220 + k * 60} L{200 - (k * 37 % 90)},{-220 + k * 60}', sw=6, stroke='#b0a8a0') for k in range(5))
    l += ''.join(text(0, 130 + k * 80, t, 62, '#2a2440', extra='stroke-width="0" font-style="italic"') for k, t in enumerate(lines))
    return g(l, id, f'translate({x},{y}) scale({s})', 'opacity="0"')
def roof_cut(id, x, y, s=1):
    """cut-away wooden house: attic beams with hidden bats"""
    h = rect(-300, -100, 600, 420, grad('#a8743c'), 6, 8) + path('M-340,-100 L0,-380 L340,-100 Z', grad('#8a4a2a'), 9)
    h += path('M-260,-130 L0,-340 L260,-130 M-200,-130 L-200,-180 M0,-130 L0,-340 M200,-130 L200,-180 M-280,-130 L280,-130', sw=14, stroke='#5a3a20')
    return g(h, id, f'translate({x},{y}) scale({s})')
def bars2(id, a_lbl, b_lbl, a_h, b_h, x=540, y=1150):
    return g(path(f'M{-360},0 L360,0', sw=8, stroke='#f4f4e8') + g(rect(-260, -a_h, 200, a_h, '#9aa0b0', 10, 7), f'{id}a') + g(rect(60, -b_h, 200, b_h, '#ff8a2e', 10, 7), f'{id}b')
             + text(-160, 80, a_lbl, 56) + text(160, 80, b_lbl, 56), id, f'translate({x},{y})')
