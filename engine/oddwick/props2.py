"""More Oddwick props + helpers (2026-11-18): horse, sea/raft/ship/plane/shark/fish/gull, footbridge, panels, camera helper.
Everything is drawn in our own style (thick #1d1430 outline, warm-lit/cool-shadow gradients)."""
import random, math
from odd import *

# ---------------------------------------------------------------- camera helper: retarget every ~1.4 s
def cam(dur, pts, z0=1.05, z1=1.3, step=1.4):
    """pts: list of (fx, fy) focus points cycled; zoom alternates between z0 and z1"""
    n = max(1, int(round(dur / step))); keys = []
    for i in range(n + 1):
        t = min(dur, i * dur / n); fx, fy = pts[i % len(pts)]
        keys.append((t, z0 if i % 2 == 0 else z1, fx, fy))
    return keys

def seq_show(ids, t0, every, d=.18):
    """pop ids in one after another (opacity 0 -> 1 with a back.out scale)"""
    return [fromto(f'#{i}', t0 + k * every, d, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)') for k, i in enumerate(ids)]
def flash_seq(ids, t0, every):
    """show one id at a time (counter digits): each visible for `every` seconds, last one stays"""
    out = []
    for k, i in enumerate(ids):
        out.append(fromto(f'#{i}', t0 + k * every, .12, {'opacity': 0, 'scale': 1.6, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'))
        if k < len(ids) - 1: out.append(setp(f'#{i}', t0 + (k + 1) * every, opacity=0))
    return out
def hidden_text(id, x, y, s, size=90, fill='#fff'):
    return text(x, y, s, size, fill, extra=f'id="{id}" opacity="0"')
def badge(id, x, y, s, fill='#ffd27a', size=70, w=None):
    w = w or (len(s) * size * .62 + 80)
    return g(rect(-w / 2, -size * .85, w, size * 1.35, fill, 24, 8) + text(0, size * .3, s, size, OUT, extra=f'stroke-width="0"'), id, f'translate({x},{y})', 'opacity="0"')
def tophat(top, wd=82, col='#2a2440'):
    return (path(f'M{-wd - 40},{top + 40} L{wd + 40},{top + 40}', sw=14) + rect(-wd + 14, top - 120, 2 * wd - 28, 160, grad(col), 8, 7)
            + rect(-wd + 14, top - 10, 2 * wd - 28, 22, '#8a2a3a', 0, 0))
def check(id, x, y, s=1, col='#5fd36a'):
    return g(ell(0, 0, 60, 60, col, 8) + path('M-28,2 L-8,24 L30,-22', sw=14, stroke='#fff'), id, f'translate({x},{y}) scale({s})', 'opacity="0"')
def cross(id, x, y, s=1):
    return g(ell(0, 0, 60, 60, '#e05a5a', 8) + path('M-24,-24 L24,24 M24,-24 L-24,24', sw=14, stroke='#fff'), id, f'translate({x},{y}) scale({s})', 'opacity="0"')

# ---------------------------------------------------------------- horse (Hans): our own chunky toy horse, side view facing right
def horse(hid, x, y, s=1, col='#c07a3a', mane='#3a2418', blinders=False, eyes='norm', flip=False):
    """ids: hid-b (whole, for bob), hid-leg (front right leg, tap with rotation), hid-head (nod), hid-tail, hid-e-norm/wide/side, hid-sweat"""
    leg = lambda lx, lid=None: (g(rect(-22, 0, 44, 190, grad(shade(col, .15)), 18, 8) + rect(-26, 170, 52, 36, '#3a2a20', 10, 7), lid, f'translate({lx},-210)') if lid
                                else g(rect(-22, 0, 44, 190, grad(shade(col, .15)), 18, 8) + rect(-26, 170, 52, 36, '#3a2a20', 10, 7), tr=f'translate({lx},-210)'))
    back_legs = leg(-150) + leg(70)
    front = leg(-90) + leg(130, f'{hid}-leg')
    body = ell(0, -270, 210, 110, grad(col), 9) + ell(-40, -300, 120, 40, lit(col, .4), extra='opacity=".35"')
    tail = g(path('M-200,-300 Q-290,-260 -270,-140 Q-240,-200 -200,-250 Z', mane, 8), f'{hid}-tail')
    eyes_ = {'norm': ell(330, -485, 18, 20, '#fff', 5) + ell(336, -482, 8, 10, OUT),
             'wide': ell(330, -488, 24, 28, '#fff', 5) + ell(332, -488, 6, 7, OUT),
             'side': ell(330, -485, 18, 20, '#fff', 5) + ell(320, -480, 8, 10, OUT) + path('M306,-512 L352,-506', sw=6)}
    ef = ''.join(g(v, f'{hid}-e-{k}', extra=f'opacity="{1 if k == eyes else 0}"') for k, v in eyes_.items())
    head = (path('M150,-330 L230,-470 L300,-450 L230,-300 Z', grad(col), 9)                     # neck
            + path('M240,-470 Q260,-540 330,-530 Q420,-520 440,-430 Q450,-390 410,-380 L300,-400 Q250,-410 240,-470 Z', grad(col), 9)
            + path('M250,-520 L262,-590 L292,-528 Z', grad(col), 7) + path('M285,-528 L300,-596 L320,-526 Z', grad(col), 7)  # ears
            + path('M232,-540 Q200,-480 196,-380 Q170,-420 182,-340 L230,-300 Q210,-400 262,-470 Z', mane, 7)
            + ell(424, -410, 8, 6, OUT) + path('M380,-382 Q404,-372 426,-386', sw=6) + ef
            + (rect(300, -520, 60, 70, '#2a2030', 10, 6) if blinders else '')
            + g(path('M360,-560 Q370,-530 362,-512 Q350,-530 360,-560 Z', '#8fd3ff', 5), f'{hid}-sweat', extra='opacity="0"'))
    inner = back_legs + tail + body + front + g(head, f'{hid}-head')
    sx = -s if flip else s
    return g(ell(0, 0, 260, 26, '#120a24', extra='opacity=".45"') + g(inner, f'{hid}-b'), hid, f'translate({x},{y}) scale({sx},{s})')
def taps(hid, t0, n, every=.32):
    """front leg taps n times starting at t0 (relative)"""
    out = []
    for k in range(n):
        t = t0 + k * every
        out.append((t, f'tl.to("#{hid}-leg",{{rotation:-28,duration:{every * .45:.3f},ease:"power2.out",transformOrigin:"50% 0%"}},{{T}});'
                       f'tl.to("#{hid}-leg",{{rotation:0,duration:{every * .4:.3f},ease:"power2.in"}},{{T}}+{every * .5:.3f});'))
    return out
def nod(hid, t, d=.4):
    return (t, f'tl.fromTo("#{hid}-head",{{rotation:0}},{{rotation:8,duration:{d / 2:.2f},yoyo:true,repeat:1,transformOrigin:"60% 90%"}},{{T}});')

def blackboard(x, y, w=520, h=360, lines=(), size=110, ids=None):
    s = rect(x - w / 2, y - h / 2, w, h, grad('#2d5a4a'), 18, 12) + rect(x - w / 2 - 20, y + h / 2, w + 40, 26, grad('#a0704a'), 8, 7)
    for k, t in enumerate(lines):
        ex = f'id="{ids[k]}" opacity="0"' if ids else ''
        s += text(x, y - h / 2 + 130 + k * (size + 20), t, size, '#f4f4e8', extra=ex)
    return s
def yard(col='#5a3a6a'):
    """old-town yard at dusk: tall houses with lit windows, cobbles, a wooden fence"""
    s = sky(moon=True) + building(-60, 1200, 300, 700, '#3a2a5a', 3, .4) + building(250, 1200, 260, 560, '#4a2f5f', 4, .3) + building(520, 1200, 280, 760, '#3a2a5a', 5, .35) + building(800, 1200, 340, 620, '#4a2f5f', 6, .4)
    s += floor_(1200, '#4a3a5a', lines=True)
    for i in range(-1, 14): s += rect(i * 90, 1130, 26, 140, grad('#8a5a3c'), 6, 6)
    s += rect(-100, 1160, 1300, 22, grad('#8a5a3c'), 4, 6) + rect(-100, 1220, 1300, 22, grad('#8a5a3c'), 4, 6)
    return s + pool(540, 1500, 620, 260) + lamp(120, 820)

# ---------------------------------------------------------------- sea
def night_sea(y0=1150, moon=True, horizon='#ff9a4d'):
    s = sky(moon=moon) + rect(-400, y0, W + 800, H - y0 + 500, grad('#2a3a7a', True), sw=0)
    r = random.Random(11)
    for k in range(9):
        yy = y0 + 30 + k ** 1.7 * 22
        s += path(' '.join(f'{"M" if i == 0 else "L"}{-400 + i * 60},{yy + (8 if i % 2 else -8) * (1 + k * .3):.0f}' for i in range(32)), sw=4 + k, stroke=lit('#2a3a7a', .25), extra='opacity=".6"')
    s += ell(820, y0 + 40, 160, 14, '#ffe9c2', extra='opacity=".35"')   # moon glint
    return s
def waves_front(id, y=1500, col='#2c3f86'):
    d = f'M-400,{y} ' + ' '.join(f'Q{-340 + i * 120},{y - 50} {-280 + i * 120},{y} Q{-220 + i * 120},{y + 40} {-160 + i * 120},{y}' for i in range(0, 16, 1)) + f' L1500,{y + 900} L-400,{y + 900} Z'
    return g(path(d, grad(col, True), 8) + path(f'M-400,{y + 10} ' + ' '.join(f'L{-340 + i * 60},{y + (6 if i % 2 else -6)}' for i in range(32)), sw=6, stroke=lit(col, .5), extra='opacity=".6"'), id)
def raft(rid, x, y, s=1, with_sailor=True, eyes='norm', mouth='smile', canopy=False, extra=''):
    planks = ''.join(rect(-260 + i * 104, -40, 100, 50, grad('#a8743c'), 8, 7) for i in range(5))
    r = (rect(-280, -10, 560, 30, grad('#7a5228'), 10, 7) + planks + path('M-250,-15 L250,-15', sw=5))
    if canopy: r += path('M-200,-40 L-200,-300 M200,-40 L200,-300', sw=10) + path('M-230,-300 Q0,-360 230,-300 L230,-280 Q0,-330 -230,-280 Z', grad('#c9b08a'), 7)
    sailor = person(f'{rid}p', 0, -40, .8, coat='#e8e0d0', skin='b', hair='tuft', eyes=eyes, mouth=mouth) if with_sailor else ''
    return g(r + sailor + extra, rid, f'translate({x},{y}) scale({s})')
def ship(sid, x, y, s=1, col='#4a4060', lit_=True):
    hull = path('M-420,0 L420,0 L360,120 L-380,120 Z', grad(col), 9) + rect(-260, -140, 300, 140, grad(lit(col, .2)), 10, 8) + rect(-120, -260, 70, 120, grad('#7a3a3a'), 6, 8)
    if lit_: hull += ''.join(rect(-240 + i * 60, -100, 30, 30, WARM2, 4, 0) for i in range(5))
    return g(hull + path('M120,-10 L120,-220 M120,-200 L300,-10', sw=8), sid, f'translate({x},{y}) scale({s})')
def plane(pid, x, y, s=1):
    p = (path('M-200,0 Q-180,-40 0,-40 Q180,-40 220,0 Q180,30 0,30 Q-180,30 -200,0 Z', grad('#8aa0c0'), 8)
         + path('M-40,-10 L-120,-170 L-60,-170 L60,-10 Z', grad('#7a90b0'), 8) + path('M-170,-10 L-230,-100 L-190,-100 L-130,-10 Z', grad('#7a90b0'), 7)
         + ell(150, -14, 30, 16, '#bfe0ff', 6) + ell(-40, 40, 50, 14, '#5a6a80', 6))
    return g(p, pid, f'translate({x},{y}) scale({s})')
def shark(kid, x, y, s=1, mouth=True):
    k = (path('M-300,0 Q-160,-120 120,-90 Q260,-70 320,0 Q240,70 80,70 Q-160,80 -300,0 Z', grad('#6a7a9a'), 9)
         + path('M-40,-100 L20,-240 L80,-90 Z', grad('#5a6a8a'), 8) + path('M-300,0 L-420,-110 L-380,0 L-420,110 Z', grad('#5a6a8a'), 8)
         + path('M-120,20 Q60,70 240,20 Q120,60 -120,20 Z', '#d8dce8', 0) + ell(210, -30, 14, 14, '#fff', 5) + ell(214, -28, 6, 6, OUT)
         + (path('M220,20 L300,6 L230,40 Z', '#fff', 5) if mouth else '') + path('M100,-30 L110,10 M130,-34 L140,6 M160,-36 L170,4', sw=5))
    return g(k, kid, f'translate({x},{y}) scale({s})')
def fish(fid, x, y, s=1, col='#ffb35c', flip=False):
    f = path('M-80,0 Q-30,-50 40,-30 Q70,-20 80,0 Q70,20 40,30 Q-30,50 -80,0 Z', grad(col), 7) + path('M-80,0 L-130,-40 L-120,0 L-130,40 Z', grad(col), 6) + ell(50, -6, 8, 8, OUT)
    return g(f, fid, f'translate({x},{y}) scale({-s if flip else s},{s})')
def gull(gid, x, y, s=1):
    gg = (ell(0, 0, 90, 46, grad('#f4f0e8'), 8) + ell(80, -40, 40, 36, grad('#f4f0e8'), 8) + path('M110,-44 L160,-34 L112,-26 Z', '#ffb33c', 5) + ell(90, -50, 6, 6, OUT)
          + g(path('M-30,-20 Q-120,-140 -200,-120 Q-110,-60 -40,10 Z', grad('#c8c8d8'), 7), f'{gid}-w') + path('M-20,40 L-20,80 M20,40 L20,80', sw=6, stroke='#ffb33c'))
    return g(gg, gid, f'translate({x},{y}) scale({s})')
def rain(id, n=70, seed=3):
    r = random.Random(seed)
    return g(''.join(path(f'M{r.randint(-100, 1180)},{r.randint(-200, 1900)} l-18,60', sw=5, stroke='#bfd8ff', extra='opacity=".7"') for _ in range(n)), id, extra='opacity="0"')
def rain_fall(id, t0, d, every=.3):
    out = [setp(f'#{id}', t0, opacity=1)]
    for k in range(int(d / every)): out.append(fromto(f'#{id}', t0 + k * every, every, {'y': -240}, {'y': 0}, 'none'))
    return out

# ---------------------------------------------------------------- footbridge over the river (London, our own drawing)
def city_river(y0=1180):
    s = sky(moon=True)
    s += building(-80, y0, 240, 520, '#2c2150', 21, .3) + building(150, y0, 200, 700, '#33265a', 22, .35) + building(330, y0, 180, 460, '#2c2150', 23, .25)
    s += g(ell(0, 0, 150, 150, grad('#4a3a70'), 8) + rect(-150, 0, 300, 300, grad('#4a3a70'), 0, 8) + path('M0,-150 L0,-230', sw=10) + ell(0, -240, 16, 16, WARM2, 5), tr=f'translate(620,{y0 - 300})')   # a domed church of our own
    s += building(800, y0, 220, 640, '#33265a', 24, .35) + building(990, y0, 220, 520, '#2c2150', 25, .3)
    s += rect(-400, y0, W + 800, H - y0 + 500, grad('#283670', True), sw=0)
    for k in range(8):
        yy = y0 + 40 + k ** 1.6 * 30
        s += path(' '.join(f'{"M" if i == 0 else "L"}{-400 + i * 70},{yy + (6 if i % 2 else -6)}' for i in range(28)), sw=4, stroke='#4a5aa0', extra='opacity=".6"')
    for xx in (180, 360, 900): s += rect(xx, y0 + 20, 12, 200, WARM2, 4, 0, 'opacity=".25"')   # reflections
    return s
def footbridge(did, y=1080, crowd=0, seed=5, crowd_id='crowd', x0=-300, x1=1380, sway_ids=False):
    """thin steel blade deck + Y piers + low cables. did = deck group (sway it). crowd = number of tiny walkers"""
    r = random.Random(seed)
    piers = ''.join(path(f'M{px},{y + 40} L{px},{y + 260} M{px},{y + 60} L{px - 60},{y + 10} M{px},{y + 60} L{px + 60},{y + 10}', sw=22, stroke='#55607a') + path(f'M{px},{y + 40} L{px},{y + 260}', sw=8, stroke='#8a96b0') for px in (200, 880))
    cab = ''.join(path(f'M{x0},{y - 40 + k * 10} Q540,{y + 30 + k * 10} {x1},{y - 40 + k * 10}', sw=6, stroke='#c8d0e8') for k in range(3))
    deck = rect(x0, y, x1 - x0, 34, grad('#9aa6c0', True), 6, 7) + path(f'M{x0},{y - 70} L{x1},{y - 70}', sw=6, stroke='#c8d0e8') + ''.join(path(f'M{xx},{y - 70} L{xx},{y}', sw=4, stroke='#c8d0e8') for xx in range(x0, x1, 60))
    people = ''
    cols = ['#4f7cc9', '#e05a7a', '#7a8a3a', '#c06a2a', '#3f5f9f', '#9a5ac9', '#2f7a8a']
    for i in range(crowd):
        px = x0 + 80 + (x1 - x0 - 160) * (i + r.random() * .5) / crowd
        people += person(f'{crowd_id}{i}', px, y, .24 + r.random() * .05, coat=r.choice(cols), skin=r.choice('abcd'), hair=r.choice(['tuft', 'bob', None, 'bun']), eyes=r.choice(['norm', 'happy']), mouth='smile')
    return piers + g(cab + deck + people, did) + pool(540, y, 600, 160)
def sway(sel, t0, d, amp=14, period=.7, grow=1.0, rot=0.8):
    """sideways rock: x and a tiny rotation, amplitude can grow"""
    out = []; n = int(d / (period / 2))
    for k in range(n):
        a = amp * (1 + (grow - 1) * k / max(1, n - 1)) * (1 if k % 2 == 0 else -1)
        out.append((t0 + k * period / 2, f'tl.to("{sel}",{{x:{a:.1f},rotation:{rot * a / amp:.2f},duration:{period / 2:.2f},ease:"sine.inOut",transformOrigin:"50% 100%"}},{{T}});'))
    out.append((t0 + n * period / 2, f'tl.to("{sel}",{{x:0,rotation:0,duration:.3}},{{T}});'))
    return out
def newspaper(id, x, y, head1, head2='', s=1):
    p = (rect(-300, -380, 600, 760, '#f4efe2', 10, 10) + text(0, -290, 'THE DAILY CANDLE', 46, OUT, extra='stroke-width="0"') + path('M-260,-260 L260,-260', sw=6)
         + text(0, -160, head1, 92, OUT, extra='stroke-width="0"') + (text(0, -60, head2, 92, OUT, extra='stroke-width="0"') if head2 else '')
         + rect(-260, 0, 250, 200, '#cfc6b8', 6, 5) + ''.join(path(f'M20,{20 + k * 40} L260,{20 + k * 40}', sw=8, stroke='#b8b0a0') for k in range(5))
         + ''.join(path(f'M-260,{250 + k * 40} L260,{250 + k * 40}', sw=8, stroke='#b8b0a0') for k in range(3)))
    return g(p, id, f'translate({x},{y}) scale({s})')
def meter(id, x, y, label='SWAY'):
    m = (path('M-220,0 A220,220 0 0 1 220,0 Z', '#fdfcf8', 9) + path('M-200,0 A200,200 0 0 1 -60,-190', sw=26, stroke='#5fd36a') + path('M-60,-190 A200,200 0 0 1 100,-174', sw=26, stroke='#ffd27a')
         + path('M100,-174 A200,200 0 0 1 200,0', sw=26, stroke='#e05a5a') + text(0, 70, label, 60) + g(path('M0,0 L-170,-30', sw=14) + ell(0, 0, 22, 22, OUT), f'{id}-n'))
    return g(m, id, f'translate({x},{y})')
def needle(id, t, rot, d=.4, ease='back.out(2)'):
    return (t, f'tl.to("#{id}-n",{{rotation:{rot},duration:{d},ease:"{ease}",transformOrigin:"0px 0px"}},{{T}});')
def damper(x, y, s=1):
    return g(rect(-40, -160, 80, 160, grad('#c8ccd8'), 10, 8) + rect(-24, -260, 48, 110, grad('#e8a040'), 8, 7) + rect(-60, -10, 120, 30, grad('#55607a'), 6, 7) + rect(-60, -280, 120, 30, grad('#55607a'), 6, 7), tr=f'translate({x},{y}) scale({s})')

def outro(a1, a2, b1, b2, face_a='happy', face_b='smirk'):
    return (sky(moon=False) + floor_(1300) + pool(540, 1300, 600, 260)
            + candle('ca', 300, 900, 1.15, 'A', face=face_a) + candle('cb', 780, 900, 1.15, 'B', face=face_b)
            + text(300, 600, a1, 60) + text(300, 670, a2, 60) + text(780, 600, b1, 60) + text(780, 670, b2, 60))
def outro_anims():
    return [fromto('#ca', 0, .4, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'), fromto('#cb', .2, .4, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'),
            move('#ca-flame', 1.0, .2, scale=1.4, transformOrigin='50% 100%'), move('#ca-flame', 1.2, .3, scale=1), move('#cb-flame', 1.8, .2, scale=1.4, transformOrigin='50% 100%'), move('#cb-flame', 2.0, .3, scale=1)]
