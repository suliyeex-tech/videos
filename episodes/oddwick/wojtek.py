import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *
from props2 import *
from props3 import *

SLUG = '2026-11-20-the-bear-who-joined-the-army'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.3, 2)
def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']
def D(i): return L(i + 1) - L(i)

FUR = '#8a5a34'; SNOUT = '#d8b088'; OLIVE = '#5a6a3a'
def bear(bid, x, y, s=1, eyes='norm', mouth='smile', helmet=False, stripes=False, flip=False):
    """our chunky toy bear, front view. ids: bid-b (body), bid-al / bid-ar (arms, rotate at the shoulder), bid-e-*, bid-m-*"""
    E = {'norm': ell(-46, -330, 16, 20, OUT) + ell(46, -330, 16, 20, OUT) + ell(-40, -338, 5, 6, '#fff') + ell(52, -338, 5, 6, '#fff'),
         'happy': path('M-66,-326 Q-46,-350 -26,-326', sw=9) + path('M26,-326 Q46,-350 66,-326', sw=9),
         'wide': ell(-46, -334, 24, 28, '#fff', 6) + ell(46, -334, 24, 28, '#fff', 6) + ell(-46, -332, 9, 10, OUT) + ell(46, -332, 9, 10, OUT),
         'shut': path('M-66,-330 L-26,-330 M26,-330 L66,-330', sw=9)}
    M = {'smile': path('M-30,-262 Q0,-238 30,-262', sw=8), 'open': ell(0, -250, 26, 22, '#7a2440', 7), 'grin': path('M-40,-268 Q0,-220 40,-268 Z', '#fff', 7),
         'chew': path('M-24,-256 L24,-256', sw=9)}
    face = ''.join(g(v, f'{bid}-e-{k}', extra=f'opacity="{1 if k == eyes else 0}"') for k, v in E.items()) + ''.join(g(v, f'{bid}-m-{k}', extra=f'opacity="{1 if k == mouth else 0}"') for k, v in M.items())
    arm = lambda sd: g(path(f'M0,0 Q{sd * 40},60 {sd * 30},140', sw=70, stroke=OUT) + path(f'M0,0 Q{sd * 40},60 {sd * 30},140', sw=56, stroke=FUR) + ell(sd * 30, 150, 34, 30, shade(FUR, .3), 6),
                       f'{bid}-a{"l" if sd < 0 else "r"}', f'translate({sd * 120},-180)')
    body = (ell(-80, 0, 60, 34, shade(FUR, .3), 7) + ell(80, 0, 60, 34, shade(FUR, .3), 7) + path('M-150,-10 Q-170,-240 0,-250 Q170,-240 150,-10 Q0,30 -150,-10 Z', grad(FUR), 9)
            + ell(0, -90, 90, 100, grad(SNOUT), 0) + arm(-1) + arm(1)
            + ell(-110, -420, 46, 46, grad(FUR), 8) + ell(110, -420, 46, 46, grad(FUR), 8) + ell(-110, -420, 22, 22, SNOUT) + ell(110, -420, 22, 22, SNOUT)
            + ell(0, -320, 150, 128, grad(FUR), 9) + ell(0, -262, 70, 52, grad(SNOUT), 7) + ell(0, -288, 24, 16, OUT) + face)
    if helmet: body += path('M-160,-380 Q-150,-480 0,-484 Q150,-480 160,-380 Z', grad('#6b7a4a'), 8) + path('M-176,-380 L176,-380', sw=12)
    if stripes: body += g(path('M-10,40 L30,10 L70,40 M-10,70 L30,40 L70,70', sw=12, stroke='#ffd27a'), tr='translate(-170,-170) scale(.9)', extra='id="' + bid + '-str"')
    return g(ell(0, 30, 200, 30, '#120a24', extra='opacity=".45"') + g(body, f'{bid}-b'), bid, f'translate({x},{y}) scale({-s if flip else s},{s})')
def soldier(pid, x, y, s=1, eyes='norm', mouth='smile', flip=False, skin='a'):
    return person(pid, x, y, s, coat=OLIVE, skin=skin, hat='helmet', eyes=eyes, mouth=mouth, flip=flip)
def officer(pid, x, y, s=1, eyes='side', mouth='smirk', flip=False):
    return person(pid, x, y, s, coat='#4a5a32', skin='d', mustache=True, hat='cap', eyes=eyes, mouth=mouth, flip=flip,
                  extra_acc=rect(-60, -150, 40, 16, '#ffd27a', 4, 4) + rect(20, -150, 40, 16, '#ffd27a', 4, 4))
def camp(base=1300):
    s = sky(moon=True) + rect(-400, base, W + 800, H - base + 400, grad('#7a5a3a', True), sw=0)
    for x in (80, 860): s += path(f'M{x - 200},{base} L{x},{base - 260} L{x + 200},{base} Z', grad('#6b7a4a'), 8) + path(f'M{x},{base} L{x},{base - 260}', sw=6)
    return s
def mountain(base=1500):
    s = sky(moon=True) + path(f'M-400,{base} L300,500 L540,380 L800,520 L1480,{base} Z', grad('#5a4a6a'), 9)
    s += rect(430, 280, 220, 110, grad('#c9b48a'), 6, 7) + path('M430,280 L540,220 L650,280 Z', grad('#a8743c'), 7)   # the monastery on top
    s += path(f'M150,{base} Q300,1200 260,1000 Q220,800 420,640', sw=26, stroke='#7a6a5a', extra='opacity=".8"')   # the path up
    return s
def crate(id, x, y, s=1, label='SHELLS'):
    return g(rect(-90, -70, 180, 140, grad('#a8743c'), 10, 8) + path('M-90,-70 L90,70 M90,-70 L-90,70', sw=6, stroke='#6b4a2a') + rect(-70, -22, 140, 44, '#f2e6c8', 6, 4) + text(0, 12, label, 30, OUT, extra='stroke-width="0"'), id, f'translate({x},{y}) scale({s})')
def bottle(id, x, y, s=1):
    return g(rect(-30, -60, 60, 130, grad('#bfe6ff'), 16, 7) + rect(-14, -110, 28, 54, grad('#bfe6ff'), 6, 7) + rect(-30, 0, 60, 70, '#fffaf0', 14, 0) + text(0, 44, 'MILK', 22, OUT, extra='stroke-width="0"'), id, f'translate({x},{y}) scale({s})')
def mug(id, x, y, s=1, beer=True):
    c = '#ffcf4a' if beer else '#6b4226'
    return g(rect(-60, -80, 120, 150, grad(c), 14, 8) + rect(-60, -100, 120, 34, '#fffaf0', 16, 7) + path('M60,-50 Q120,-40 110,10 Q100,40 60,40', sw=14), id, f'translate({x},{y}) scale({s})')
def ship_dock():
    return sky(moon=True) + rect(-400, 1350, W + 800, 900, grad('#2a3a7a', True), sw=0) + ship('sh', 540, 1250, 1.1) + rect(-400, 1380, W + 800, 80, grad('#7a5a3a'), 0, 7)
def badge_round(id, x, y, s=1):
    b = (ell(0, 0, 250, 250, grad('#2a3a2a'), 12) + ell(0, 0, 210, 210, 'none', 6, 'stroke="#ffd27a"')
         + g(bear('bdg', 0, 0, .55, 'norm', 'smile'), tr='translate(-20,140)')
         + g(rect(-28, -90, 56, 180, grad('#c8ccd8'), 24, 6) + path('M-28,-90 Q0,-150 28,-90 Z', grad('#ffd27a'), 6), tr='translate(70,-30) rotate(-20)'))
    return g(b, id, f'translate({x},{y}) scale({s})', 'opacity="0"')

def shots(lines, total):
    S = []
    # 0 hook: the enlistment desk; a giant paw signs... it's a bear in a helmet
    h = 1.9
    paw = g(ell(0, 0, 90, 70, grad(FUR), 8) + ''.join(ell(-50 + k * 34, -50, 16, 18, shade(FUR, .3), 5) for k in range(4)), 'pw', 'translate(700,1150)')
    a = [fromto('#pw', .2, .5, {'y': -500}, {'y': 0}, 'back.out(2)'), (.8, 'tl.fromTo("#pw",{x:0},{x:-120,duration:.15,yoyo:true,repeat:3},{T});')] + [draw_('sig', .8, .7)] + pop('en', .1)
    S.append(Shot(0, h, wall('#4a5a3a', 2400) + pool(540, 1100, 600, 500) + rect(80, 1200, 920, 60, grad('#7a4a2a'), 10, 8) + rect(320, 1000, 440, 220, '#f2e6c8', 6, 6)
                  + text(540, 1060, 'ENLIST', 44, OUT, extra='stroke-width="0"') + path('M380,1170 Q440,1120 500,1170 T620,1160 T720,1150', sw=7, extra='id="sig" stroke-dasharray="600" stroke-dashoffset="600"') + paw
                  + badge('en', 540, 600, 'NEW SOLDIER', '#ffd27a', 70),
                  [(0, 1.0, 540, 1000), (h, 1.2, 600, 1100)], a))
    a = [bface('bw', .3, 'happy', 'grin'), arm('bw', 'r', .4, -150)]
    S.append(Shot(h, L(1), wall('#4a5a3a', 2400) + pool(540, 1000, 600, 600) + bear('bw', 540, 1700, 1.5, 'wide', 'open', helmet=True),
                  [(0, 1.5, 540, 1150), (D(0) - h, 1.25, 540, 1100)], a))
    # 1 a long march; they buy a tiny orphan cub from a boy; milk from an old bottle
    h = D(1) * .5
    a = [fromto('#sq', 0, h, {'x': -300}, {'x': 100}, 'none')] + bob('s1', 0, h, 8, .35) + bob('s2', .15, h, 8, .35) + [bface('bo', .2, 'happy', 'smile')]
    S.append(Shot(L(1), L(1) + h, sky(moon=True) + rect(-400, 1300, W + 800, 900, grad('#c9a06a', True), sw=0) + path('M-400,1450 L1480,1350', sw=60, stroke='#a8805a', extra='opacity=".6"')
                  + g(soldier('s1', 300, 1420, .8) + soldier('s2', 500, 1410, .8, skin='b'), 'sq') + person('bo', 860, 1440, .6, coat='#c8a060', skin='b', hair='tuft') + bear('cb', 760, 1450, .35, 'norm', 'smile'),
                  [(0, 1.0, 540, 1150), (h, 1.3, 760, 1300)], a))
    a = [fromto('#bt', 0, .4, {'rotation': 0}, {'rotation': -40}, 'power2.out'), face('cb2', .4, 'happy', 'open')] + bob('cb2', .5, D(1) - h - .5, 6, .25)
    S.append(Shot(L(1) + h, L(2), camp() + soldier('s3', 380, 1560, 1.3, 'happy', 'smile') + bear('cb2', 680, 1560, .55, 'norm', 'smile') + g(bottle('bt0', 0, 0, 1.0), 'bt', 'translate(600,1240)'),
                  [(0, 1.2, 560, 1200), (D(1) - h, 1.35, 640, 1250)], a))
    # 2 he grew: fruit, honey, marmalade... favourite drink: beer
    a = [fromto('#gb', 0, 1.6, {'scale': .35, 'transformOrigin': '50% 100%'}, {'scale': 1}, 'back.out(1.4)')] + pop('fr', .4) + pop('hn', .8) + pop('mm', 1.2) + [fromto('#mg', 1.9, .3, {'opacity': 0, 'y': 200}, {'opacity': 1, 'y': 0}, 'back.out(2)'), face('gb', 2.0, 'happy', 'grin')] + pop('br', 2.0)
    S.append(Shot(L(2), L(3), camp() + bear('gb', 540, 1600, 1.4, 'norm', 'smile') + badge('fr', 220, 620, 'FRUIT', '#ff8a5a', 56) + badge('hn', 540, 520, 'HONEY', '#ffd27a', 56) + badge('mm', 860, 620, 'JAM', '#e05a7a', 56)
                  + g(mug('mg0', 0, 0, 1.1), 'mg', 'translate(860,1150)', 'opacity="0"') + badge('br', 860, 900, 'BEER', '#ffd27a', 70),
                  [(0, 1.0, 540, 1050), (D(2), 1.1, 620, 1050)], a))
    # 3 the mocker: 'A bear in the army? He'll eat the whole camp!'
    a = talk('of', .05, D(3) - .3, .12, rest='smirk') + [arm('of', 'r', .3, -140), arm('of', 'r', 1.2, -40)]
    S.append(Shot(L(3), L(4), camp() + pool(540, 1200, 600, 500) + officer('of', 470, 1720, 2.0),
                  [(0, 1.0, 470, 1100), (D(3), 1.3, 560, 980)], a))
    # 4 the ship: NO PETS. NO ANIMALS.
    sg = g(rect(-230, -110, 460, 220, '#f2e6c8', 14, 8) + text(0, -20, 'NO PETS', 64, '#e05a5a', extra='stroke-width="0"') + text(0, 60, 'NO ANIMALS', 52, '#e05a5a', extra='stroke-width="0"') + path('M0,110 L0,330', sw=14), 'sg', 'translate(300,1050)')
    a = [fromto('#sg', .3, .4, {'scale': 0, 'transformOrigin': '50% 100%'}, {'scale': 1}, 'back.out(2)'), face('sl', 1.2, 'angry', 'flat'), arm('sl', 'l', 1.2, 60), arm('sl', 'r', 1.2, -60)]
    S.append(Shot(L(4), L(5), ship_dock() + sg + person('sl', 800, 1440, 1.0, coat='#2a3a6a', skin='b', hat='cap'),
                  [(0, 1.0, 540, 1000), (D(4), 1.2, 520, 1150)], a))
    # 5 the idea: if he's not a pet... he's a soldier (helmet drops onto the bear)
    a = pop('bl5', .2) + [fromto('#hm', 1.6, .35, {'y': -700}, {'y': 0}, 'bounce.out'), bface('b5', 2.0, 'happy', 'grin')]
    hm = g(path('M-160,-380 Q-150,-480 0,-484 Q150,-480 160,-380 Z', grad('#6b7a4a'), 8) + path('M-176,-380 L176,-380', sw=12), 'hm', '')
    S.append(Shot(L(5), L(6), camp() + soldier('s5', 200, 1500, 1.0, 'happy', 'grin', flip=True) + soldier('s6', 880, 1500, 1.0, 'happy', 'grin', skin='b') + g(bear('b5', 0, 0, 1.0) + g(hm, tr='scale(1)'), tr='translate(540,1560)')
                  + g(ell(0, 0, 70, 80, '#ffe27a', 8) + rect(-34, 70, 68, 50, grad('#9aa0b0'), 8, 7) + ell(0, 0, 150, 150, 'url(#glow)'), 'bl5', 'translate(200,820)', 'opacity="0"'),
                  [(0, 1.0, 540, 1000), (1.6, 1.15, 540, 1100), (D(5), 1.3, 540, 1100)], a))
    # 6 signed up as a private, with his own number; taught to salute... and he saluted back
    h = D(6) * .42
    a = [fromto('#pp', 0, .4, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'), stamp_in('pv', .9)]
    pp = g(rect(-300, -380, 600, 760, '#f2e6c8', 10, 8) + text(0, -290, 'ARMY RECORD', 46, OUT, extra='stroke-width="0"') + text(-240, -190, 'NAME:', 36, OUT, anchor='start', extra='stroke-width="0"')
           + text(-80, -190, 'WOJTEK', 40, '#2a3a6a', anchor='start', extra='stroke-width="0"') + text(-240, -110, 'SPECIES:', 36, OUT, anchor='start', extra='stroke-width="0"') + text(-40, -110, 'BEAR', 40, '#2a3a6a', anchor='start', extra='stroke-width="0"')
           + g(bear('pb', 0, 0, .45), tr='translate(0,260)'), 'pp', 'translate(540,1050)')
    S.append(Shot(L(6), L(6) + h, wall('#4a5a3a', 2400) + pool(540, 1000, 600, 600) + pp + stamp('pv', 540, 900, 'PRIVATE'),
                  [(0, 1.0, 540, 1000), (h, 1.15, 540, 1000)], a))
    a = [arm('s7', 'r', .2, -160), arm('b7', 'r', 1.4, -160), bface('b7', 1.4, 'happy', 'smile'), face('s7', 1.7, 'wide', 'o')]
    S.append(Shot(L(6) + h, L(7), camp() + soldier('s7', 280, 1560, 1.2, 'norm', 'smile') + bear('b7', 740, 1600, 1.0, helmet=True),
                  [(0, 1.0, 400, 1150), (1.3, 1.15, 700, 1150), (D(6) - h, 1.25, 600, 1150)], a))
    # 7 mocker again: 'Next you'll give him a rifle!'
    a = talk('of', .05, D(7) - .2, .11, rest='grin') + bob('of', 0, D(7), 10, .2) + [arm('of', 'l', .1, 140)]
    S.append(Shot(L(7), L(8), camp() + pool(540, 1200, 600, 500) + officer('of', 560, 1640, 1.7, eyes='happy', mouth='grin', flip=True),
                  [(0, 1.3, 560, 1000), (D(7), 1.5, 560, 950)], a))
    # 8 wrestling / coffee every morning / cigarettes... he ate them
    t1 = D(8) * .34; t2 = D(8) * .66
    a = [fromto('#wr', 0, t1, {'rotation': -12, 'transformOrigin': '50% 100%'}, {'rotation': 12}, 'sine.inOut'), face('s8', .3, 'shut', 'grin'), bface('b8', .3, 'happy', 'grin')] + pop('dust', .5)
    S.append(Shot(L(8), L(8) + t1, camp() + g(soldier('s8', 430, 1500, 1.0, 'wide', 'open') + bear('b8', 640, 1520, .9), 'wr') + badge('dust', 540, 800, 'WRESTLE!', '#ffd27a', 70),
                  [(0, 1.1, 540, 1150), (t1, 1.25, 540, 1200)], a))
    a = [fromto('#mug8', 0, .4, {'y': 200, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'), bface('b9', .6, 'happy', 'smile')] + pop('am', .3)
    S.append(Shot(L(8) + t1, L(8) + t2, camp() + rect(-400, 0, W + 800, H, '#ff9a4d', sw=0, extra='opacity=".18"') + bear('b9', 540, 1620, 1.2) + g(mug('m9', 0, 0, .9, beer=False), 'mug8', 'translate(820,1250)') + badge('am', 540, 560, '6 AM: COFFEE', '#ffd27a', 64),
                  [(0, 1.15, 600, 1150), (t2 - t1, 1.25, 650, 1150)], a))
    cig = g(rect(-90, -30, 180, 60, '#f2f2f2', 10, 6) + rect(50, -30, 40, 60, '#e8a040', 0, 6), 'cg', 'translate(540,1340)')
    a = [fromto('#cg', .1, .4, {'x': 300, 'opacity': 1}, {'x': 0}, 'power2.out'), setp('#cg', .7, opacity=0), bface('b10', .7, 'happy', 'chew')] + [bface('b10', .7 + k * .2, None, 'chew' if k % 2 == 0 else 'smile') for k in range(5)] + pop('cr', .8)
    S.append(Shot(L(8) + t2, L(9), camp() + bear('b10', 540, 1700, 1.6, 'norm', 'open') + cig + badge('cr', 540, 560, 'CRUNCH', '#ffd27a', 76),
                  [(0, 1.3, 540, 1200), (D(8) - t2, 1.45, 540, 1250)], a))
    # 9 a huge battle on a mountain in Italy; men haul shell crates up to the guns
    h = D(9) * .45
    a = [setp(f'#fl{k}', .3 + k * .5, opacity=1) for k in range(4)] + [setp(f'#fl{k}', .45 + k * .5, opacity=0) for k in range(4)] + pop('it', .2)
    fl = ''.join(g(ell(0, 0, 70, 70, 'url(#glow)') + ell(0, 0, 24, 24, '#ffd27a'), f'fl{k}', f'translate({300 + k * 170},{560 + (k % 2) * 140})', 'opacity="0"') for k in range(4))
    S.append(Shot(L(9), L(9) + h, mountain() + fl + badge('it', 540, 1000, 'ITALY', '#ffd27a', 76), [(0, 1.0, 540, 900), (h, 1.15, 540, 800)], a))
    a = bob('s10', 0, D(9) - h, 8, .4) + bob('s11', .2, D(9) - h, 8, .4) + [fromto('#cl', 0, D(9) - h, {'x': 0, 'y': 0}, {'x': 160, 'y': -120}, 'none')]
    S.append(Shot(L(9) + h, L(10), mountain(1700) + g(soldier('s10', 300, 1560, 1.0, 'angry', 'flat') + crate('c10', 300, 1185, .7) + soldier('s11', 620, 1500, .9, 'angry', 'flat', skin='b') + crate('c11', 620, 1170, .65), 'cl'),
                  [(0, 1.1, 460, 1300), (D(9) - h, 1.2, 600, 1200)], a))
    # 10 'you see': a bear copies his friends -> he picks up a crate too, again and again, never dropped one
    h = D(10) * .4
    a = [arm('s12', 'l', .2, 170), arm('s12', 'r', .2, -170), fromto('#c12', .2, .4, {'y': 140}, {'y': 0}, 'power2.out'),
         arm('b12', 'l', 1.3, 170), arm('b12', 'r', 1.3, -170), fromto('#c13', 1.3, .4, {'y': 220}, {'y': 0}, 'power2.out'), bface('b12', 1.4, 'happy', 'grin')]
    S.append(Shot(L(10), L(10) + h, mountain(1800) + soldier('s12', 300, 1640, 1.1) + crate('c12', 300, 1230, .7) + bear('b12', 760, 1660, 1.0) + crate('c13', 760, 1080, .9),
                  [(0, 1.0, 540, 1250), (1.2, 1.1, 700, 1200), (h, 1.15, 650, 1200)], a))
    n = 3; sd_ = (D(10) - h) / n; a = []
    for k in range(n):
        a += [fromto('#cb3', k * sd_, sd_, {'x': -260, 'y': 260}, {'x': 260, 'y': -220}, 'none'), fromto(f'#nm{k}', k * sd_ + .1, .2, {'opacity': 0, 'scale': 1.6, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
        if k < n - 1: a.append(setp(f'#nm{k}', (k + 1) * sd_, opacity=0))
    a += bob('cb3', 0, D(10) - h, 10, .3) + pop('nd', D(10) - h - 1.3)
    S.append(Shot(L(10) + h, L(11), mountain(1700) + g(bear('b13', 0, 0, .7, 'happy', 'smile', helmet=True) + crate('c14', 0, -560, .8), 'cb3', 'translate(540,1450)')
                  + ''.join(text(820, 640, f'x{k + 1}', 110, '#ffd27a', extra=f'id="nm{k}" opacity="0"') for k in range(n)) + badge('nd', 540, 900, 'NEVER DROPPED ONE', '#5fd36a', 56),
                  [(0, 1.0, 540, 1100), (D(10) - h, 1.1, 560, 1050)], a))
    # 11 after the battle: choosing the company's new official badge (sketches on a table)
    a = [fromto('#sk', .2, .5, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'), face('o11', 1.2, 'side', 'flat')]
    sk = g(rect(-420, -260, 840, 520, '#f2e6c8', 10, 8) + text(0, -180, 'NEW BADGE?', 56, OUT, extra='stroke-width="0"') + ''.join(ell(-260 + k * 260, 40, 100, 100, 'none', 6) + text(-260 + k * 260, 60, '?', 90, '#9aa0b0', extra='stroke-width="0"') for k in range(3)), 'sk', 'translate(540,1050)')
    S.append(Shot(L(11), L(12), wall('#4a5a3a', 2400) + pool(540, 1000, 600, 600) + sk + officer('o11', 860, 1750, 1.2, flip=True),
                  [(0, 1.0, 540, 1050), (D(11), 1.15, 540, 1050)], a))
    # 12 the badge: a bear carrying an artillery shell (spin in, mocker's jaw drops behind)
    a = [fromto('#bd', 0, .6, {'opacity': 0, 'scale': .2, 'rotation': -200, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1, 'rotation': 0}, 'back.out(1.6)'), face('o12', .8, 'wide', 'open')]
    S.append(Shot(L(12), L(13), wall('#2a3a2a', 2400) + pool(540, 1000, 700, 700) + officer('o12', 860, 1800, 1.1, 'side', 'smirk', flip=True) + badge_round('bd', 540, 950, 1.3),
                  [(0, 1.2, 540, 950), (D(12), 1.05, 560, 1000)], a))
    # 13 'And Private Wojtek?' (bear close, looking at camera)
    a = [bface('b14', .3, 'norm', 'smile')] + blink('b14', [.6])
    S.append(Shot(L(13), L(14), camp() + bear('b14', 540, 1800, 2.0, 'side' if False else 'norm', 'smile', helmet=True), [(0, 1.3, 540, 1200), (D(13), 1.45, 540, 1150)], a))
    # 14 payoff: promoted. To corporal. (stripes slap onto his arm; the mocker has to salute)
    a = [fromto('#b15-str', .15, .3, {'opacity': 0, 'scale': 2.4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'power3.in'), bface('b15', .4, 'happy', 'grin'),
         arm('o15', 'r', .6, -160), face('o15', .6, 'wide', 'flat')] + pop('cp', .4)
    S.append(Shot(L(14), L(15), camp() + bear('b15', 420, 1640, 1.2, helmet=True, stripes=True) + officer('o15', 850, 1560, 1.0, 'norm', 'flat', flip=True) + badge('cp', 540, 560, 'CORPORAL', '#ffd27a', 80),
                  [(0, 1.15, 420, 1150), (D(14), 1.05, 560, 1150)], a))
    S.append(Shot(L(15), total, outro('SALUTE', 'HIM', 'HIDE', 'THE BEER'), [(0, 1.0, 540, 950), (total - L(15), 1.12, 540, 1000)], outro_anims()))
    return S

def bface(pid, t, eyes=None, mouth=None):
    return face(pid, t, eyes, mouth, all_e=('norm', 'happy', 'wide', 'shut'), all_m=('smile', 'open', 'grin', 'chew'))
def draw_(id, t, d=.25, n=600): return fromto(f'#{id}', t, d, {'strokeDashoffset': n}, {'strokeDashoffset': 0}, 'power1.inOut')
def stamp(id, x, y, txt, size=110, col='#e05a5a', w=760):
    return g(rect(-w / 2, -size * .8, w, size * 1.6, 'none', 18, 14, f'stroke="{col}"') + text(0, size * .36, txt, size, col, extra='stroke-width="0"'), id, f'translate({x},{y}) rotate(-8)', 'opacity="0"')
def stamp_in(id, t): return fromto(f'#{id}', t, .25, {'opacity': 0, 'scale': 2.5, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'power3.in')

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(15) - .3,
      'flares': [(L(0) + 2.0, 'flare'), (L(3) + .4, 'shrink'), (L(6) + 3.6, 'flare'), (L(9) + .3, 'shrink'), (L(12) + .3, 'flare'), (L(14) + .2, 'flare')]}

def audio():
    T = TOTAL
    music = [('km_Comic_Plodding.mp3', 0, 0, L(3) - .05, -1, (.02, .2)),
             ('km_Marty_Gots_a_Plan.mp3', 0, L(3), L(9) - .05, -2, (.05, .2)),
             ('km_Five_Armies.mp3', 0, L(9), L(11) - .3, -1, (.1, .3)),
             ('km_Investigations.mp3', 0, L(11), L(14) - .25, -4, (.1, .1)),
             ('km_Fun_in_a_Bottle.mp3', 0, L(14) + .5, T, -1, (.05, 1.0))]
    O = '100-cc0-sfx/'; O2 = '100-cc0-sfx-2/sfx100v2_'; SW = 'swishes-sound-pack/swishes/swish-'; CR = '80-cc0-creature-sfx/'; B = '75-cc0-breaking-falling-hit-sfx/bfh1_'
    MW = '100-cc0-metal-and-wood-sfx/'; FS = 'footsteps-0/'; BS = 'battle-at-sea/'
    sfx = [(O + 'paper_01.ogg', .1, -6), (O2 + 'wood_hit_01.ogg', .55, -2), (O + 'paper_03.ogg', .85, -4), (SW + '3.wav', 1.85, -4), (CR + 'roar_01.ogg', 1.95, -4), (O + 'bell_02.ogg', 2.3, -8)]
    sfx += [(SW + '5.wav', L(1) - .05, -4)] + [(FS + f'0{k % 6 + 1}-footstep.ogg', L(1) + .2 + k * .35, -10) for k in range(7)] + [(CR + 'cute_02.ogg', L(1) + 1.2, -4)]
    sfx += [(SW + '9.wav', L(1) + D(1) * .5 - .05, -4), (O + 'glass_02.ogg', L(1) + D(1) * .5 + .2, -6), (CR + 'eat_01.ogg', L(1) + D(1) * .5 + .6, -4), (CR + 'cute_05.ogg', L(1) + D(1) * .5 + 1.3, -4)]
    sfx += [(O + 'spring_01.ogg', L(2) + .1, -4), (O + 'spring_03.ogg', L(2) + .7, -6), (CR + 'eat_03.ogg', L(2) + .9, -4), (O + 'glass_04.ogg', L(2) + 1.9, -4), (CR + 'burp_01.ogg', L(2) + 2.5, -4)]
    sfx += [(SW + '7.wav', L(3) - .1, -4), ('do-you-remember-laughter/ogalaughter_2.ogg', E(3) - .1, -4, 22.5, 1.7)]
    sfx += [(O2 + 'loop_water_01.ogg', L(4), -14, 0, D(4)), ('solo-seagull-sound-effects/Seagull Ambient 2.wav', L(4) + .2, -10, 0, 1.5), (O + 'slam_03.ogg', L(4) + .4, -4), (CR + 'grunt_02.ogg', L(4) + 1.3, -6)]
    sfx += [(O + 'bell_01.ogg', L(5) + .2, -6), (SW + '11.wav', L(5) + 1.5, -4), (MW + 'metal_slam_01.ogg', L(5) + 1.85, 0), (CR + 'cute_07.ogg', L(5) + 2.1, -4)]
    sfx += [(O + 'paper_02.ogg', L(6) + .05, -4), (O + 'slam_04.ogg', L(6) + .95, 0), (SW + '2.wav', L(6) + D(6) * .42 - .05, -4), (O + 'switch_01.ogg', L(6) + D(6) * .42 + .25, -6), (O + 'switch_02.ogg', L(6) + D(6) * .42 + 1.45, -4), (CR + 'ooh.ogg', L(6) + D(6) * .42 + 1.8, -6)]
    sfx += [(SW + '6.wav', L(7) - .05, -4), ('group-giggling/group_giggling.ogg', L(7) + .2, -6, 0, 1.2)]
    t1 = D(8) * .34; t2 = D(8) * .66
    sfx += [(B + 'hit_06.ogg', L(8) + .3, -2), (CR + 'grunt_03.ogg', L(8) + .4, -4), (B + 'falling_02.ogg', L(8) + .9, -4), (SW + '8.wav', L(8) + t1 - .05, -4), (O + 'dishes_01.ogg', L(8) + t1 + .3, -4),
            (O2 + 'misc_05.ogg', L(8) + t1 + .7, -8), (SW + '4.wav', L(8) + t2 - .05, -4)] + [(CR + f'eat_0{k % 4 + 1}.ogg', L(8) + t2 + .7 + k * .3, -3) for k in range(4)]
    sfx += [(BS + 'cannon_fire_1.ogg', L(9) + .3, -2), (BS + 'cannon_fire_1.ogg', L(9) + .8, -4), ('muffled-distant-explosion/NenadSimic - Muffled Distant Explosion.wav', L(9) + 1.3, -2, 0, 1.6), (BS + 'cannon_hit_1.ogg', L(9) + 1.8, -4)]
    sfx += [(CR + 'breath.ogg', L(9) + D(9) * .45, -6), (MW + 'wood_hit_04.ogg', L(9) + D(9) * .45 + .5, -6)] + [(FS + f'0{k % 6 + 1}-footstep.ogg', L(9) + D(9) * .45 + .3 + k * .4, -10) for k in range(6)]
    h = D(10) * .4
    sfx += [(SW + '1.wav', L(10) - .05, -4), (MW + 'wood_hit_01.ogg', L(10) + .35, -2), (MW + 'wood_hit_08.ogg', L(10) + 1.45, 0), (CR + 'grunt_01.ogg', L(10) + 1.4, -4)]
    sfx += [(MW + 'wood_hit_09.ogg', L(10) + h + k * (D(10) - h) / 3 + .1, -4) for k in range(3)] + [(BS + 'cannon_fire_1.ogg', L(10) + h + .9, -10), (O + 'bell_02.ogg', L(10) + D(10) - 1.2, -6)]
    sfx += [(O + 'paper_04.ogg', L(11) + .2, -4), (O2 + 'misc_09.ogg', L(11) + 1.2, -8)]
    sfx += [(SW + '12.wav', L(12), -2), (O + 'gong_02.ogg', L(12) + .55, -4), (CR + 'ooh.ogg', L(12) + .8, -6)]
    sfx += [(CR + 'cute_09.ogg', L(13) + .3, -6)]
    sfx += [(O + 'slam_02.ogg', L(14) + .4, 0), (O + 'bell_01.ogg', L(14) + .5, -4), (O + 'switch_01.ogg', L(14) + .65, -4), ('applause-in-a-large-hall-or-church/applause-clapping-church-crowd-immersive.wav', L(14) + .7, -8, 2, 1.8)]
    sfx += [(SW + '1.wav', L(15) - .05, -3), (O2 + 'air_01.ogg', T - 1.0, -1)]
    return music, sfx

def build_tt():
    def shots_tt(lines, total):
        S = shots(lines, total)
        S[0].cam = [(0, 1.6, 700, 1150), (1.0, 1.3, 650, 1120), (1.9, 1.2, 600, 1100)]
        return S
    ov = ('<div id="ttq" class="clip" data-start="0" data-duration="2.4" data-track-index="5" style="position:absolute;left:0;top:300px;width:1080px;text-align:center;z-index:960">'
          '<span style="display:inline-block;font-family:Montserrat;font-weight:900;font-size:76px;line-height:1.05;color:#140c26;background:#ffd27a;padding:18px 34px;border-radius:26px;border:8px solid #140c26">'
          'THE ARMY HIRED A BEAR<br>WAIT FOR HIS RANK</span></div>')
    js = 'tl.fromTo("#ttq span",{scale:.6,rotation:-4},{scale:1,rotation:-2,duration:.25,ease:"back.out(3)"},0.05);'
    return build(dict(EP, shots=shots_tt, hfdir='hf_tt', overlay=ov, overlay_js=js))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mix':
        from mix import mix
        mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
    elif len(sys.argv) > 1 and sys.argv[1] == 'tt': print(build_tt())
    else: print(build(EP), TOTAL)
