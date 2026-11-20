import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *
from props2 import *
from props3 import *

SLUG = '2026-11-20-the-navy-tried-to-build-a-ship-from-ice'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.3, 2)
def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']
def D(i): return L(i + 1) - L(i)

ICE = '#bfe6ff'; PYK = '#c9b48a'
def block(id, x, y, s=1, kind='ice', cracked=False):
    """a big block on its own: ice (clear blue, shine lines) or the new stuff (ice + wood pulp: beige fibres)"""
    col = ICE if kind == 'ice' else PYK
    b = rect(-170, -170, 340, 300, grad(col), 26, 9) + path('M-170,-170 L-110,-230 L230,-230 L170,-170 Z', lit(col, .5), 8) + path('M170,-170 L230,-230 L230,70 L170,130 Z', shade(col, .3), 8)
    if kind == 'ice': b += path('M-120,-120 L-60,-140 M-130,-70 L-100,-80', sw=8, stroke='#ffffff', extra='opacity=".8"')
    else:
        r = random.Random(3)
        b += ''.join(path(f'M{r.randint(-150, 120)},{r.randint(-150, 100)} q{r.randint(10, 30)},{r.randint(-14, 14)} {r.randint(30, 60)},{r.randint(-8, 8)}', sw=5, stroke='#8a6a3a', extra='opacity=".75"') for _ in range(22))
    return g(b, id, f'translate({x},{y}) scale({s})')
def crack(id, d, sw=8, n=900): return path(d, sw=sw, stroke='#1d1430', extra=f'id="{id}" stroke-dasharray="{n}" stroke-dashoffset="{n}"')
def draw(id, t, d=.25, n=900): return fromto(f'#{id}', t, d, {'strokeDashoffset': n}, {'strokeDashoffset': 0}, 'power2.in')
def pistol(id, x, y, s=1, flip=False):
    p = rect(0, -30, 190, 50, grad('#5a5a6a'), 10, 7) + path('M20,10 L0,110 L50,110 L70,10 Z', grad('#6b4a32'), 7) + rect(180, -24, 40, 22, '#3a3a48', 4, 5) + path('M70,20 Q90,50 110,20', sw=6)
    return g(p, id, f'translate({x},{y}) scale({-s if flip else s},{s})')
def muzzle(id, x, y): return g(path('M0,0 L60,-40 L50,-10 L110,0 L50,10 L60,40 Z', '#ffd27a', 6) + ell(0, 0, 80, 80, 'url(#glow)'), id, f'translate({x},{y})', 'opacity="0"')
def chopper(id, x, y, s=1):
    return g(rect(-14, -40, 28, 300, grad('#8a5a32'), 10, 7) + path('M-14,-40 L-150,-60 L-150,60 L-14,30 Z', grad('#c8ccd8'), 7), id, f'translate({x},{y}) scale({s})')
def commander(pid, x, y, s=1, eyes='norm', mouth='smirk', flip=False):
    return person(pid, x, y, s, coat='#2a3a6a', skin='a', hat='cap', mustache=True, eyes=eyes, mouth=mouth, flip=flip)
def general(pid, x, y, s=1, eyes='norm', mouth='flat', flip=False, coat='#6a6a3a'):
    return person(pid, x, y, s, coat=coat, skin='d', hat='cap', eyes=eyes, mouth=mouth, flip=flip, tall=.9)
def inventor(pid, x, y, s=1, eyes='happy', mouth='grin', flip=False):
    return person(pid, x, y, s, coat='#7a5a9a', skin='a', glasses=True, hair='tuft', eyes=eyes, mouth=mouth, flip=flip)
def table(y=1350): return rect(-200, y, 1480, 60, grad('#7a4a2a'), 10, 8) + rect(-200, y + 60, 1480, 400, '#3a2418', 0, 0)
def meeting_bg(): return wall('#3a3060', 2400) + window_(120, 420, 260, 340) + window_(700, 420, 260, 340) + pool(540, 1100, 650, 500)
def carrier(id, x, y, s=1, ice=True, planes=3):
    col = ICE if ice else '#6a7088'
    c = path('M-500,0 L520,0 L460,110 L-460,110 Z', grad(col), 9) + rect(-480, -30, 980, 34, grad(lit(col, .3)), 6, 7) + rect(220, -150, 120, 120, grad(shade(col, .2)), 10, 8)
    if ice: c += path('M-400,40 L-340,20 M-200,70 L-150,50 M100,40 L170,20', sw=7, stroke='#fff', extra='opacity=".8"')
    c += ''.join(g(plane(f'{id}p{k}', 0, 0, .35), tr=f'translate({-360 + k * 200},-60)') for k in range(planes))
    return g(c, id, f'translate({x},{y}) scale({s})')
def beams(id, x, y, n=5, s=1):
    b = ''.join(rect(-200 + (k % 2) * 30, -k * 44, 400, 40, grad('#8a92a8'), 6, 7) + path(f'M{-200 + (k % 2) * 30},{-k * 44 + 20} L{200 + (k % 2) * 30},{-k * 44 + 20}', sw=4, stroke='#55607a') for k in range(n))
    return g(b, id, f'translate({x},{y}) scale({s})')
def lake(y0=1150):
    s = sky(moon=False, horizon='#ffb07a')
    for k, (x, h) in enumerate(((100, 520), (420, 700), (760, 560), (1050, 640))):
        s += path(f'M{x - 380},{y0} L{x},{y0 - h} L{x + 380},{y0} Z', grad('#4a3a7a'), 8) + path(f'M{x - 90},{y0 - h + 120} L{x},{y0 - h} L{x + 90},{y0 - h + 120} L{x + 40},{y0 - h + 100} L0,0 Z'.replace(' L0,0', ''), '#f2f4ff', 6)
    s += rect(-400, y0, W + 800, H - y0 + 400, grad('#3a5a9a', True), sw=0)
    for k in range(5): s += path(f'M{-300 + k * 60},{y0 + 60 + k * 70} L{1400 - k * 50},{y0 + 60 + k * 70}', sw=4, stroke='#6a8ad0', extra='opacity=".5"')
    for x in (60, 200, 880, 1000): s += path(f'M{x},{y0 + 20} L{x - 50},{y0 + 20} L{x},{y0 - 180} L{x + 50},{y0 + 20} Z', grad('#2a5a4a'), 6)
    return s
def sunk(id, x, y, s=1): return g(ell(0, 0, 110, 110, '#ffd27a', 8) + ell(0, 0, 200, 200, 'url(#glow)'), id, f'translate({x},{y}) scale({s})')
def stamp(id, x, y, txt, size=110, col='#e05a5a', w=760):
    return g(rect(-w / 2, -size * .8, w, size * 1.6, 'none', 18, 14, f'stroke="{col}"') + text(0, size * .36, txt, size, col, extra='stroke-width="0"'), id, f'translate({x},{y}) rotate(-8)', 'opacity="0"')
def stamp_in(id, t): return fromto(f'#{id}', t, .25, {'opacity': 0, 'scale': 2.5, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'power3.in')
def shards(prefix, x, y, n=8, seed=2):
    r = random.Random(seed)
    return ''.join(g(path(f'M0,0 L{r.randint(30, 60)},{r.randint(-20, 20)} L{r.randint(0, 30)},{r.randint(30, 60)} Z', ICE, 5), f'{prefix}{k}', f'translate({x},{y})', 'opacity="0"') for k in range(n))
def shard_burst(prefix, t, n=8, seed=2):
    r = random.Random(seed + 9); out = []
    for k in range(n):
        a = r.uniform(-math.pi, 0); dd = r.uniform(250, 520)
        out.append(fromto(f'#{prefix}{k}', t, .55, {'opacity': 1, 'x': 0, 'y': 0, 'rotation': 0}, {'opacity': 1, 'x': math.cos(a) * dd, 'y': math.sin(a) * dd + 260, 'rotation': r.randint(-200, 200)}, 'power2.out'))
    return out

def shots(lines, total):
    S = []
    # 0 hook: secret meeting, the commander draws a pistol (A) ... and shoots a block of ice (B)
    h = 2.6
    a = [arm('cm', 'r', .4, -100), fromto('#ps', .4, .3, {'opacity': 0, 'x': -60}, {'opacity': 1, 'x': 0}, 'back.out(2)'), face('g1', 1.0, 'wide', 'o'), face('g2', 1.2, 'wide', 'open')] + pop('ts', .2)
    S.append(Shot(0, h, meeting_bg() + general('g1', 160, 1340, 1.0, flip=True) + general('g2', 920, 1340, 1.0, coat='#2a3a6a') + table() + block('bk', 620, 1290, .7) + commander('cm', 300, 1460, 1.2)
                  + g(pistol('ps', 0, 0, .8), tr='translate(380,1230)') + stamp('ts', 540, 470, 'TOP SECRET', 90, '#e05a5a', 700),
                  [(0, 1.0, 540, 1000), (h, 1.25, 520, 1150)], a))
    a = [setp('#mz', .3, opacity=1), setp('#mz', .45, opacity=0)] + [draw('ck1', .35, .2), draw('ck2', .45, .2)]
    S.append(Shot(h, L(1), meeting_bg() + table(1500) + block('bk2', 540, 1300, 1.6) + crack('ck1', 'M480,1050 L520,1130 L470,1200 L530,1290 L500,1380') + crack('ck2', 'M520,1130 L600,1170 L640,1240')
                  + g(pistol('ps2', 0, 0, 1.3, flip=True), tr='translate(1060,820)') + muzzle('mz', 780, 800),
                  [(0, 1.1, 640, 1000), (D(0) - h, 1.35, 540, 1180)], a))
    # 1 problem: steel. A shipyard with a hull frame and a dwindling pile of beams
    a = [fromto(f'#bm-{k}', 0, 0, {}, {}) for k in range(0)] + pop('stl', .5) + pop('ne', 3.2)
    bm = beams('bm', 540, 1500, 6, 1.2)
    a += [fromto('#bm', 1.6, 1.4, {'scaleY': 1, 'transformOrigin': '50% 100%'}, {'scaleY': .25}, 'power2.in')]
    hull = path('M100,1150 L980,1150 L900,1330 L180,1330 Z', 'none', 10, 'stroke-dasharray="30 20"') + ''.join(path(f'M{160 + k * 110},1150 L{200 + k * 100},1330', sw=10, stroke='#55607a') for k in range(8))
    S.append(Shot(L(1), L(2), sky(moon=True) + floor_(1350) + hull + bm + badge('stl', 540, 560, 'STEEL', '#c8ccd8', 100) + badge('ne', 540, 760, 'NOT ENOUGH', '#e05a5a', 70),
                  [(0, 1.0, 540, 1000), (2.5, 1.2, 540, 1250), (D(1), 1.1, 540, 1100)], a))
    # 2 an inventor's crazy idea: a carrier made of ice
    h = D(2) * .45
    a = pop('bl', .4) + [face('iv', .4, 'wide', 'open'), arm('iv', 'r', .5, -150)]
    S.append(Shot(L(2), L(2) + h, wall('#4a3a6a', 2400) + pool(540, 1100, 600, 500) + inventor('iv', 540, 1640, 1.6, 'norm', 'smile') + bulb('bl', 800, 700),
                  [(0, 1.0, 540, 1000), (h, 1.25, 600, 900)], a))
    a = [fromto('#ic', .2, .7, {'y': 500, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(1.5)')] + pop('oi', 1.0)
    S.append(Shot(L(2) + h, L(3), night_sea(1150) + carrier('ic', 540, 1180, .9) + badge('oi', 540, 600, 'MADE OF ICE', ICE, 80),
                  [(0, 1.1, 540, 1000), (D(2) - h, 1.25, 540, 1050)], a))
    # 3 size: 2,000 ft, 2 million tons; a normal carrier looks tiny next to it
    a = pop('ft', .5) + pop('tn', 1.5)
    S.append(Shot(L(3), L(4), night_sea(1150) + carrier('big', 540, 1180, 2.2, planes=4) + carrier('sm', 760, 1240, .35, ice=False, planes=1) + badge('ft', 540, 520, '2,000 FT', '#ffd27a', 90) + badge('tn', 540, 680, '2,000,000 TONS', '#ffd27a', 70),
                  [(0, 1.6, 760, 1200), (D(3), .95, 540, 1050)], a))
    # 4 but ice cracks / melts
    a = [draw('c4a', .1, .3), draw('c4b', .3, .3)] + [fromto(f'#dr{k}', .5 + k * .25, .6, {'opacity': 1, 'y': 0}, {'opacity': 0, 'y': 260}, 'power1.in') for k in range(4)]
    drips = ''.join(ell(420 + k * 70, 1480, 14, 20, '#9fd8ff', 4, f'id="dr{k}" opacity="0"') for k in range(4))
    S.append(Shot(L(4), L(5), wall('#2a4a6a', 2400) + pool(540, 1200, 600, 500) + block('b4', 540, 1350, 1.5) + crack('c4a', 'M450,1100 L500,1180 L460,1260 L520,1340') + crack('c4b', 'M500,1180 L600,1220 L620,1300') + drips,
                  [(0, 1.15, 540, 1200), (D(4), 1.3, 540, 1300)], a))
    # 5 water + wood pulp, mixed and frozen
    a = [fromto('#saw', .2, .8, {'y': -400, 'rotation': 0}, {'y': 0, 'rotation': 60}, 'power2.in')] + pop('mix', 1.4) + [fromto('#pk', 2.0, .4, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(2)')]
    bucket = path('M380,1200 L700,1200 L660,1500 L420,1500 Z', grad('#7a8090'), 9) + ell(540, 1200, 160, 30, '#5a9ad8', 7)
    saw = g(rect(-60, -40, 120, 80, grad('#c9a06a'), 14, 7) + text(0, 20, 'PULP', 34, OUT, extra='stroke-width="0"'), 'saw', 'translate(540,1160)')
    S.append(Shot(L(5), L(6), wall('#4a3a6a', 2400) + pool(540, 1200, 600, 500) + bucket + saw + badge('mix', 540, 560, 'ICE + WOOD PULP', '#ffd27a', 70) + g(block('pk0', 0, 0, .55, 'pyk'), 'pk', 'translate(860,1000)', 'opacity="0"'),
                  [(0, 1.1, 540, 1200), (D(5), 1.15, 640, 1050)], a))
    # 6 'you see': glass crack runs straight through / fibres stop it / it gets stuck
    t1 = D(6) * .36; t2 = D(6) * .72
    a = [draw('c6', .3, .5, 1400)] + pop('g6', 1.0)
    S.append(Shot(L(6), L(6) + t1, wall('#2a3a6a', 2400) + rect(240, 700, 600, 800, grad(ICE), 20, 9) + crack('c6', 'M300,720 L420,900 L380,1050 L520,1200 L480,1320 L640,1490', 9, 1400) + badge('g6', 540, 560, 'LIKE GLASS', ICE, 70),
                  [(0, 1.0, 540, 1100), (t1, 1.15, 540, 1150)], a))
    fib = ''.join(path(f'M{260 + k * 70},{700} q40,200 0,400 q-40,200 0,400', sw=12, stroke='#a8743c', extra='opacity=".85"') for k in range(9))
    a = [draw('c6b', .3, .35, 300)] + pop('st6', 1.0) + [(.65, 'tl.fromTo("#c6b",{x:0},{x:6,duration:.05,yoyo:true,repeat:5},{T});')]
    S.append(Shot(L(6) + t1, L(6) + t2, wall('#2a3a6a', 2400) + rect(240, 700, 600, 800, grad(PYK), 20, 9) + fib + crack('c6b', 'M260,900 L330,960 L300,1010', 10, 300) + badge('st6', 380, 700, 'STUCK!', '#ffd27a', 90),
                  [(0, 1.3, 330, 960), (t2 - t1, 1.5, 320, 970)], a))
    a = [draw('c6c', .1, .25, 1400), draw('c6d', .1, .15, 300)] + pop('x6', .5) + pop('k6', .7)
    S.append(Shot(L(6) + t2, L(7), wall('#2a3a6a', 2400) + rect(60, 760, 440, 700, grad(ICE), 20, 9) + rect(580, 760, 440, 700, grad(PYK), 20, 9) + ''.join(path(f'M{620 + k * 60},{780} q30,160 0,330 q-30,160 0,330', sw=12, stroke='#a8743c', extra='opacity=".85"') for k in range(7))
                  + crack('c6c', 'M100,780 L200,950 L160,1100 L300,1250 L250,1440', 9, 1400) + crack('c6d', 'M600,900 L660,950 L640,1000', 10, 300) + cross('x6', 280, 620) + check('k6', 800, 620),
                  [(0, 1.0, 540, 1100), (D(6) - t2, 1.08, 540, 1100)], a))
    # 7 test ship on a lake in Canada; motor off -> three hot summers to melt
    h = D(7) * .45
    tb = g(path('M-200,0 L200,0 L170,70 L-170,70 Z', grad(ICE), 8) + rect(-160, -110, 320, 110, grad(ICE), 14, 8) + rect(60, -170, 70, 60, grad('#7a8090'), 6, 7), 'tb', 'translate(540,1200)')
    a = pop('cn', .4) + [(.2 + k * .5, f'tl.fromTo("#mot",{{y:0}},{{y:-6,duration:.12,yoyo:true,repeat:1}},{{T}});') for k in range(4)]
    S.append(Shot(L(7), L(7) + h, lake() + tb + g(text(0, 0, 'MOTOR', 30, '#fff'), 'mot', 'translate(635,1010)') + badge('cn', 540, 640, 'CANADA', '#ffd27a', 80),
                  [(0, 1.0, 540, 950), (h, 1.3, 540, 1150)], a))
    sm = D(7) - h; a = []
    for k in range(3):
        t = k * sm / 3
        a += [fromto('#sun', t, sm / 3, {'x': -500, 'y': 200}, {'x': 500, 'y': 200}, 'sine.inOut'), fromto(f'#su{k}', t + .1, .2, {'opacity': 0, 'scale': 1.6, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
        if k < 2: a.append(setp(f'#su{k}', t + sm / 3, opacity=0))
        a.append(fromto('#tb2', t, sm / 3, {'scale': 1 - k * .3}, {'scale': .7 - k * .3}, 'none'))
    tb2 = g(path('M-200,0 L200,0 L170,70 L-170,70 Z', grad(ICE), 8) + rect(-160, -110, 320, 110, grad(ICE), 14, 8), 'tb2', 'translate(540,1250)')
    S.append(Shot(L(7) + h, L(8), lake() + g(sunk('sun0', 0, 0, .8), 'sun', 'translate(540,420)') + tb2 + ''.join(text(540, 760, f'SUMMER {k + 1}', 100, '#ffd27a', extra=f'id="su{k}" opacity="0"') for k in range(3)),
                  [(0, 1.0, 540, 950), (sm, 1.1, 540, 1050)], a))
    # 8 the big meeting: two blocks wheeled in, plain ice and the new stuff
    a = [fromto('#tr8', 0, 1.2, {'x': -700}, {'x': 0}, 'power2.out')] + pop('l1', 1.4) + pop('l2', 1.8) + [face('g3', 1.5, 'side', 'flat')]
    trolley = g(rect(-420, 0, 840, 40, grad('#7a8090'), 8, 7) + ell(-340, 70, 34, 34, '#3a3a48', 6) + ell(340, 70, 34, 34, '#3a3a48', 6) + block('i8', -200, -20, .9) + block('p8', 220, -20, .9, 'pyk'), 'tr8', 'translate(540,1300)')
    S.append(Shot(L(8), L(9), meeting_bg() + general('g3', 140, 1500, 1.1, flip=True) + general('g4', 950, 1500, 1.1, coat='#2a3a6a', mouth='o') + trolley
                  + badge('l1', 340, 860, 'ICE', ICE, 70) + badge('l2', 760, 860, 'NEW', PYK, 70),
                  [(0, 1.0, 540, 1100), (D(8), 1.15, 540, 1150)], a))
    # 9 the chopper test: ice splits / new block barely dents, his arms rattle
    h = D(9) * .45
    a = [fromto('#ch', .2, .35, {'rotation': -80, 'transformOrigin': '50% 90%'}, {'rotation': 10}, 'power3.in'), fromto('#hl', .55, .4, {'x': 0, 'rotation': 0}, {'x': -120, 'rotation': -14}, 'power2.out'),
         fromto('#hr', .55, .4, {'x': 0, 'rotation': 0}, {'x': 120, 'rotation': 14}, 'power2.out')]
    S.append(Shot(L(9), L(9) + h, meeting_bg() + table(1500) + g(path('M-170,-170 L0,-170 L-20,130 L-170,130 Z', grad(ICE), 9), 'hl', 'translate(540,1360)')
                  + g(path('M0,-170 L170,-170 L170,130 L-20,130 Z', grad(ICE), 9), 'hr', 'translate(540,1360)') + chopper('ch', 640, 900, 1.3),
                  [(0, 1.15, 540, 1150), (h, 1.3, 540, 1200)], a))
    sh = D(9) - h
    a = [fromto('#ch2', .2, .3, {'rotation': -80, 'transformOrigin': '50% 90%'}, {'rotation': 5}, 'power3.in'), (.5, 'tl.fromTo("#ch2",{rotation:5},{rotation:-25,duration:.1,yoyo:true,repeat:3},{T});')]
    a += [(.5, 'tl.fromTo("#g5-b",{x:-10},{x:10,duration:.05,yoyo:true,repeat:11},{T});'), face('g5', .5, 'wide', 'open'), arm('g5', 'r', .1, -150), arm('g5', 'l', .1, 150)]
    a += pop('dn', 1.1)
    S.append(Shot(L(9) + h, L(10), meeting_bg() + table(1500) + block('p9', 420, 1360, 1.0, 'pyk') + general('g5', 820, 1760, 1.4, 'angry', 'flat', flip=True) + chopper('ch2', 560, 950, 1.2) + badge('dn', 420, 980, 'DENT', PYK, 60),
                  [(0, 1.1, 600, 1150), (sh, 1.25, 700, 1150)], a))
    # 10 pistol: BANG, the plain ice shatters
    a = [setp('#mz10', .55, opacity=1), setp('#mz10', .7, opacity=0), setp('#ib10', .6, opacity=0)] + shard_burst('sh', .6, 10)
    S.append(Shot(L(10), L(11), meeting_bg() + table(1500) + g(block('ib', 0, 0, 1.1), 'ib10', 'translate(400,1360)') + shards('sh', 400, 1300, 10)
                  + g(pistol('ps10', 0, 0, 1.4, flip=True), tr='translate(1120,1000)') + muzzle('mz10', 810, 985) + commander('cm10', 980, 1900, 1.4, flip=True),
                  [(0, 1.0, 640, 1150), (.6, 1.2, 450, 1250), (D(10), 1.1, 450, 1200)], a))
    # 11 second shot: the bullet hits the new block... and bounces right back out
    bp = 'M800,990 L470,1240 Q380,1150 700,820 Q1000,560 260,700'
    a = [setp('#mz11', .3, opacity=1), setp('#mz11', .42, opacity=0), (.35, 'tl.fromTo("#pb",{x:0},{x:10,duration:.04,yoyo:true,repeat:5},{T});')]
    a += [draw('trail', .35, 1.6, 2200)]
    a += [face('g6', 1.0, 'wide', 'open'), face('g7', 1.2, 'wide', 'o')]
    S.append(Shot(L(11), L(12), meeting_bg() + general('g6', 160, 1500, 1.0) + general('g7', 930, 1500, 1.0, coat='#2a3a6a', flip=True) + table(1500) + g(block('pb0', 0, 0, 1.0, 'pyk'), 'pb', 'translate(420,1360)')
                  + path(bp, sw=8, stroke='#ffd27a', extra='id="trail" stroke-dasharray="2200" stroke-dashoffset="2200" stroke-linecap="round"') + g(pistol('ps11', 0, 0, 1.2, flip=True), tr='translate(1080,1000)') + muzzle('mz11', 820, 990),
                  [(0, 1.0, 600, 1050), (1.2, 1.1, 520, 950), (D(11), 1.2, 400, 900)], a))
    # 12 payoff: it grazed the trouser leg of an American admiral (big close-up on the leg, then his face)
    h = D(12) * .5
    leg = (rect(-200, 300, 1480, 420, grad('#1e2a5a', True), 30, 9) + ''.join(ell(460 + k * 160, 640, 18, 18, '#ffd27a', 5) for k in range(2))
           + rect(220, 700, 300, 1100, grad('#f2f2f2'), 30, 9) + rect(580, 700, 300, 1100, grad('#f2f2f2'), 30, 9)
           + path('M180,1800 L520,1800 L540,1900 L120,1900 Z', '#1d1430', 6) + path('M580,1800 L920,1800 L960,1900 L560,1900 Z', '#1d1430', 6))
    rip = g(path('M220,1100 L320,1070 L290,1140 L370,1115 L330,1185 L220,1170 Z', '#f6d2b0', 6) + path('M215,1060 L380,1060', sw=6, stroke='#e05a5a'), 'rip', '', 'opacity="0"')
    a = [fromto('#zz', 0, .35, {'x': -900}, {'x': 1400}, 'none'), setp('#rip', .2, opacity=1), (.2, 'tl.fromTo("#lg",{x:0},{x:14,duration:.05,yoyo:true,repeat:5},{T});')] + pop('zz2', .3)
    S.append(Shot(L(12), L(12) + h, wall('#3a3060', 2400) + g(leg + rip, 'lg') + g(ell(0, 0, 18, 10, '#ffd27a', 4) + path('M-20,0 L-260,0', sw=6, stroke='#ffd27a'), 'zz', 'translate(0,1110)') + badge('zz2', 760, 760, 'ZZZIP!', '#ffd27a', 70),
                  [(0, 1.0, 540, 1100), (h, 1.1, 480, 1120)], a))
    a = [face('ad', .1, 'wide', 'open'), arm('ad', 'l', .1, 150), arm('ad', 'r', .1, -150), (.1, 'tl.fromTo("#ad-b",{y:0},{y:-60,duration:.15,yoyo:true,repeat:1},{T});')]
    S.append(Shot(L(12) + h, L(13), meeting_bg() + person('ad', 540, 1700, 1.7, coat='#1e2a5a', skin='a', hat='cap', eyes='norm', mouth='flat') + table(1700),
                  [(0, 1.3, 540, 1100), (D(12) - h, 1.45, 540, 1050)], a))
    # 13 cancelled. The reason?
    a = [stamp_in('cx', .9)]
    bp_ = rect(60, 600, 960, 900, '#2a4a8a', 16, 9) + ''.join(path(f'M60,{600 + k * 90} L1020,{600 + k * 90}', sw=2, stroke='#6a8ad0') for k in range(10)) + carrier('bpc', 540, 1100, .85)
    S.append(Shot(L(13), L(14), wall('#3a3060', 2400) + bp_ + stamp('cx', 540, 1000, 'CANCELLED'), [(0, 1.0, 540, 1050), (D(13), 1.1, 540, 1050)], a))
    # 14 ...it needed too much steel (a mountain of beams drops on the blueprint; fridge pipes)
    a = [fromto(f'#bx{k}', k * .12, .35, {'y': -1400}, {'y': 0}, 'bounce.out') for k in range(5)] + pop('tm', .5)
    S.append(Shot(L(14), L(15), wall('#3a3060', 2400) + bp_ + ''.join(g(beams(f'bx{k}i', 0, 0, 2, 1.3), f'bx{k}', f'translate({540 + (k % 2) * 60 - 30},{1450 - k * 115})') for k in range(5))
                  + badge('tm', 540, 520, 'TOO MUCH STEEL', '#c8ccd8', 76),
                  [(0, 1.05, 540, 1100), (D(14), 1.15, 540, 1050)], a))
    S.append(Shot(L(15), total, outro('YES,', 'SAIL IT', 'NO', 'WAY'), [(0, 1.0, 540, 950), (total - L(15), 1.12, 540, 1000)], outro_anims()))
    return S

def bulb(id, x, y):
    return g(ell(0, 0, 70, 80, '#ffe27a', 8) + rect(-34, 70, 68, 50, grad('#9aa0b0'), 8, 7) + ell(0, 0, 150, 150, 'url(#glow)'), id, f'translate({x},{y})', 'opacity="0"')

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(15) - .3,
      'flares': [(L(0) + 3.0, 'flare'), (L(4) + .2, 'shrink'), (L(7) + 3.5, 'flare'), (L(11) + .5, 'shrink'), (L(12) + .2, 'flare'), (L(14) + .2, 'flare')]}

def audio():
    T = TOTAL
    music = [('km_Spy_Glass.mp3', 0, 0, L(4) - .05, -1, (.02, .2)),
             ('km_Frost_Waltz.mp3', 0, L(4), L(8) - .05, -2, (.1, .3)),
             ('km_Volatile_Reaction.mp3', 3, L(8), L(12) - .4, 0, (.1, .2)),
             ('km_Investigations.mp3', 0, L(13), L(15) - .1, -3, (.1, .1)),
             ('km_Fun_in_a_Bottle.mp3', 0, L(15), T, -1, (.05, 1.0))]
    O = '100-cc0-sfx/'; O2 = '100-cc0-sfx-2/sfx100v2_'; SW = 'swishes-sound-pack/swishes/swish-'; CR = '80-cc0-creature-sfx/'; B = '75-cc0-breaking-falling-hit-sfx/bfh1_'
    MW = '100-cc0-metal-and-wood-sfx/'
    sfx = [(O2 + 'loop_ambient_01.ogg', 0, -16, 0, 2.6), (MW + 'metal_open_01.ogg', .6, -3), (CR + 'ooh.ogg', 1.1, -6), (SW + '3.wav', 2.55, -4),
           (O + 'shot_01.ogg', 2.6 + .3, 0), (B + 'glass_breaking_02.ogg', 2.6 + .35, -3)]
    sfx += [(SW + '5.wav', L(1) - .05, -4), (O2 + 'loop_construction_site.ogg', L(1), -12, 0, D(1)), (O + 'metal_08.ogg', L(1) + 1.6, -2), (MW + 'metal_falling_02.ogg', L(1) + 2.2, -4), (O + 'slam_02.ogg', L(1) + 3.2, -4)]
    sfx += [(SW + '9.wav', L(2) - .05, -4), (O + 'bell_02.ogg', L(2) + .4, -4), (SW + '12.wav', L(2) + D(2) * .45, -3), (O2 + 'loop_water_02.ogg', L(2) + D(2) * .45, -12, 0, 2.5)]
    sfx += [(SW + '7.wav', L(3) - .05, -3), (O + 'gong_02.ogg', L(3) + .5, -8), (O + 'spring_04.ogg', L(3) + 1.5, -6)]
    sfx += [(B + 'glass_breaking_05.ogg', L(4) + .1, -3), (O + 'plop_01.ogg', L(4) + .55, -6), (O + 'plop_02.ogg', L(4) + .8, -6)]
    sfx += [(O + 'splash_01.ogg', L(5) + .9, -2), (O2 + 'loop_water_03.ogg', L(5) + 1.0, -10, 0, 1.2), (O + 'spring_02.ogg', L(5) + 2.0, -6)]
    t1 = D(6) * .36; t2 = D(6) * .72
    sfx += [(SW + '2.wav', L(6) - .05, -4), (B + 'glass_breaking_06.ogg', L(6) + .3, -2), (SW + '4.wav', L(6) + t1 - .05, -4), (B + 'hit_04.ogg', L(6) + t1 + .6, -2), (O + 'spring_07.ogg', L(6) + t1 + .7, -6),
            (SW + '1.wav', L(6) + t2 - .05, -4), (B + 'glass_breaking_02.ogg', L(6) + t2 + .1, -6), (O + 'bell_01.ogg', L(6) + t2 + .7, -6)]
    sfx += [(SW + '11.wav', L(7) - .05, -4), ('mild-wind-background-noise/wind background noise 2.wav', L(7), -12, 0, D(7)), (O2 + 'loop_machine_02.ogg', L(7) + .2, -10, 0, 2.4),
            (O + 'switch_01.ogg', L(7) + D(7) * .45 - .2, -2), (O + 'plop_01.ogg', L(7) + D(7) * .45 + .4, -8), (O + 'plop_02.ogg', L(7) + D(7) * .45 + 2.0, -8), (O + 'plop_01.ogg', L(7) + D(7) * .45 + 3.0, -8)]
    sfx += [(O2 + 'loop_machine_04.ogg', L(8), -12, 0, 1.3), (MW + 'metal_sheet_01.ogg', L(8) + 1.2, -4), (CR + 'cough_01.ogg', L(8) + 2.2, -10)]
    h9 = D(9) * .45
    sfx += [(SW + '6.wav', L(9) + .1, -2), (B + 'rock_breaking_01.ogg', L(9) + .55, 0), (SW + '8.wav', L(9) + h9 + .1, -2), (B + 'hit_10.ogg', L(9) + h9 + .5, 0), (O + 'spring_08.ogg', L(9) + h9 + .55, -4), (CR + 'hurt_02.ogg', L(9) + h9 + .7, -6)]
    sfx += [(MW + 'metal_open_01.ogg', L(10) + .1, -6), (O + 'shot_02.ogg', L(10) + .55, 0), (B + 'glass_breaking_06.ogg', L(10) + .6, 0), (B + 'glass_falling_03.ogg', L(10) + 1.1, -4)]
    sfx += [(O + 'shot_01.ogg', L(11) + .3, 0), (O + 'metal_05.ogg', L(11) + .4, -1), ('air-whoosh/whoosh2_0.wav', L(11) + .7, -2), (SW + '10.wav', L(11) + 1.3, -3), (CR + 'scream_02.ogg', L(11) + 1.2, -8)]
    sfx += [(SW + '1.wav', L(12) - .02, 0), (O + 'weird_04.ogg', L(12) + .2, -4), (CR + 'scream_01.ogg', L(12) + D(12) * .5 + .05, -5), (O + 'hit_03.ogg', L(12) + D(12) * .5 + .1, -6)]
    sfx += [(O + 'paper_02.ogg', L(13) + .1, -4), (O + 'slam_04.ogg', L(13) + .9, 0)]
    sfx += [(MW + 'metal_falling_02.ogg', L(14) + .05, 0), (B + 'metal_hit_02.ogg', L(14) + .3, -2), (B + 'metal_falling_05.ogg', L(14) + .5, -3)]
    sfx += [(SW + '1.wav', L(15) - .05, -3), (O2 + 'air_01.ogg', T - 1.0, -1)]
    return music, sfx

def build_tt():
    def shots_tt(lines, total):
        S = shots(lines, total)
        S[0].cam = [(0, 1.7, 400, 1300), (1.2, 1.35, 450, 1200), (2.6, 1.25, 520, 1150)]
        return S
    ov = ('<div id="ttq" class="clip" data-start="0" data-duration="2.4" data-track-index="5" style="position:absolute;left:0;top:300px;width:1080px;text-align:center;z-index:960">'
          '<span style="display:inline-block;font-family:Montserrat;font-weight:900;font-size:76px;line-height:1.05;color:#140c26;background:#bfe6ff;padding:18px 34px;border-radius:26px;border:8px solid #140c26">'
          'A WARSHIP MADE OF ICE?<br>WAIT FOR THE BULLET</span></div>')
    js = 'tl.fromTo("#ttq span",{scale:.6,rotation:-4},{scale:1,rotation:-2,duration:.25,ease:"back.out(3)"},0.05);'
    return build(dict(EP, shots=shots_tt, hfdir='hf_tt', overlay=ov, overlay_js=js))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mix':
        from mix import mix
        mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
    elif len(sys.argv) > 1 and sys.argv[1] == 'tt': print(build_tt())
    else: print(build(EP), TOTAL)
