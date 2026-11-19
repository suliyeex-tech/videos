import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *
from props2 import *
from props3 import *

SLUG = '2026-11-19-before-alarm-clocks-she-shot-peas'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.3, 2)
def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']
def D(i): return L(i + 1) - L(i)
TIP = (330 * math.cos(math.radians(-38)) + 60, 330 * math.sin(math.radians(-38)) - 250)   # tube tip relative to the knocker's feet (scale 1)

def tip(x, y, s=1): return (x + TIP[0] * s, y + TIP[1] * s)
def clock3(id='c3', x=760, y=250):
    return g(rect(-150, -70, 300, 140, '#140c26', 20, 7) + text(0, 30, '3:00 AM', 76, WARM2), id, f'translate({x},{y})')

def shots(lines, total):
    S = []
    # 0 hook: 3 AM street, she walks in, aims, pea flies, TAK on a dark window
    kx, ky, ks = 380, 1560, 1.0; tx, ty = tip(kx, ky, ks)
    t1 = 2.0; t2 = 3.2
    a = [fromto('#kn', 0, 1.5, {'x': -400}, {'x': 0}, 'power2.out')] + bob('kn', 0, 1.5, 10, .25) + [(0, 'tl.from("#c3",{opacity:0,y:-80,duration:.3,ease:"back.out(3)"},{T});')]
    a += shoot('p0', t1, tx, ty, *WIN[2]) + pop('t0', t1 + .3, hold=.6) + shoot('p1', t2, tx, ty, *WIN[1]) + pop('t1', t2 + .3, hold=.6) + [light_win(1, E(0) - .4)]
    S.append(Shot(0, L(1), terrace(sleepers=(1, 2)) + knocker('kn', kx, ky, ks) + pea('p0', tx, ty) + pea('p1', tx, ty) + tak('t0', WIN[2][0], WIN[2][1] - 140) + tak('t1', WIN[1][0], WIN[1][1] - 140) + clock3(),
                  [(0, 1.15, 420, 1150), (1.6, 1.25, 520, 900), (t1 + .3, 1.35, 690, 640), (t2 + .3, 1.3, 420, 640), (D(0), 1.2, 480, 820)], a))
    # 1 they paid her: a hand drops a coin, SIXPENCE A WEEK
    a = [fromto('#cn', .2, .5, {'opacity': 0, 'y': -500, 'rotation': -90}, {'opacity': 1, 'y': 0, 'rotation': 0}, 'bounce.out'), face('kn', .7, 'happy', 'grin')] + pop('spw', .9)
    S.append(Shot(L(1), L(2), wall('#4a3a6a', 2400) + pool(540, 1150, 620, 520) + knocker('kn', 540, 1750, 1.6, tube=False) + coin('cn', 540, 650, 1.6)
                  + badge('spw', 540, 930, 'SIXPENCE A WEEK', '#ffd27a', 66),
                  [(0, 1.1, 540, 900), (D(1), 1.25, 540, 850)], a))
    # 2 alarm clocks cost too much -> factory: LATE = NO JOB
    h = D(2) * .5
    a = [fromto('#ac', 0, .4, {'scale': .3, 'opacity': 0, 'transformOrigin': '50% 50%'}, {'scale': 1, 'opacity': 1}, 'back.out(2)')] + pop('pt', .9)
    a += [(1.2 + k * .14, f'tl.to("#ac",{{rotation:{6 if k % 2 else -6},duration:.12,transformOrigin:"50% 50%"}},{{T}});') for k in range(6)]
    S.append(Shot(L(2), L(2) + h, wall('#3a3060', 2400) + pool(540, 900, 600, 500) + alarm_clock('ac', 540, 820, 2.2, 0) + price_tag('pt', 700, 1060, 'TOO MUCH!'),
                  [(0, 1.0, 540, 900), (h, 1.15, 600, 900)], a))
    fac = (sky(moon=True) + building(80, 1250, 920, 760, '#3a2a50', 31, .5) + rect(380, 380, 320, 120, '#140c26', 12, 7) + text(540, 465, 'FACTORY', 80, WARM2)
           + ell(540, 640, 110, 110, '#fdfcf8', 8) + path('M540,640 L540,560 M540,640 L600,660', sw=10) + floor_(1250))
    boss = person('bs', 760, 1520, 1.15, coat='#3a3a4a', skin='a', mustache=True, eyes='angry', mouth='frown', extra_acc=tophat(-300))
    late = person('lt', 300, 1560, 1.0, coat='#7a5a2a', skin='c', hat='cap', eyes='wide', mouth='o')
    a = [arm('bs', 'r', .2, -100), fromto('#lt', 0, .5, {'x': -300}, {'x': 0}, 'power2.out')] + bob('lt', 0, .5, 12, .15) + pop('lj', .7)
    S.append(Shot(L(2) + h, L(3), fac + late + boss + badge('lj', 540, 900, 'LATE = NO JOB', '#e05a5a', 80),
                  [(0, 1.1, 540, 1150), (D(2) - h, 1.25, 600, 1000)], a))
    # 3 she WAS the alarm clock: KNOCKER-UP title
    a = [face('kn', .2, 'happy', 'smirk'), fromto('#ttl', .9, .3, {'opacity': 0, 'scale': 2.4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'power3.in')]
    ttl = g(rect(-400, -90, 800, 180, '#ffd27a', 24, 10) + text(0, 38, 'KNOCKER-UP', 110, OUT, extra='stroke-width="0"'), 'ttl', 'translate(540,640) rotate(-4)', 'opacity="0"')
    S.append(Shot(L(3), L(4), terrace() + knocker('kn', 540, 1600, 1.35) + ttl, [(0, 1.3, 540, 1100), (D(3), 1.1, 540, 900)], a))
    # 4 her tool: tube + peas; TAK TAK TAK on three windows
    kx, ky = 260, 1600; tx, ty = tip(kx, ky)
    a = []
    for k, (w, t) in enumerate(((0, 1.4), (2, 2.1), (3, 2.8))):
        a += shoot(f'q{k}', t, tx, ty, *WIN[w], .25) + pop(f'tk{k}', t + .25, hold=.5) + [light_win(w, t + .3)]
    pk = g(ell(0, 0, 120, 70, grad('#7a5a3a'), 8) + ''.join(ell(-60 + i * 28, -30 + (i % 2) * 12, 15, 15, '#9ad04a', 5) for i in range(5)), 'pk', 'translate(560,1450)', 'opacity="0"')
    a += [fromto('#pk', .2, .3, {'opacity': 0, 'y': 80}, {'opacity': 1, 'y': 0}, 'back.out(2)'), setp('#pk', 1.3, opacity=0)]
    S.append(Shot(L(4), L(5), terrace(sleepers=(0, 2, 3)) + knocker('kn', kx, ky) + pk + ''.join(pea(f'q{k}', tx, ty) for k in range(3))
                  + ''.join(tak(f'tk{k}', WIN[w][0], WIN[w][1] - 140, 70) for k, w in enumerate((0, 2, 3))),
                  [(0, 1.6, 450, 1150), (1.3, 1.2, 380, 800), (2.2, 1.25, 700, 650), (D(4), 1.2, 700, 800)], a))
    # 5 she waits until you come to the window (foot taps, the sleeper wakes, opens his eyes)
    win = g(rect(-330, -380, 660, 760, '#1c1538', 12, 12) + rect(-330, -380, 660, 760, WARM2, 12, 0, 'id="bw" opacity="0"') + person('sw', 0, 380, 1.1, coat='#d8d0c0', skin='b', eyes='shut', mouth='flat', hat='beanie')
            + path('M0,-380 L0,380 M-330,0 L330,0', sw=12) + rect(-360, 380, 720, 40, grad('#a0704a'), 6, 8), tr='translate(560,760)')
    a = [(k * .3, 'tl.fromTo("#kn",{y:0},{y:-10,duration:.12,yoyo:true,repeat:1},{T});') for k in range(4)] + [fromto('#bw', 1.2, .2, {'opacity': 0}, {'opacity': .55})]
    a += [face('sw', 1.3, 'wide', 'o'), arm('kn', 'l', .4, 30)]
    S.append(Shot(L(5), L(6), wall(BRICK, 2400) + win + knocker('kn', 830, 1800, .9, flip=True), [(0, 1.2, 700, 1350), (1.0, 1.15, 560, 820), (D(5), 1.3, 560, 760)], a))
    # 6 grumpy vs happy: split windows
    h = D(6) * .5
    left = g(rect(-230, -300, 460, 600, WARM2, 10, 10) + person('gr', 0, 300, .95, coat='#8a8070', skin='a', mustache=True, eyes='angry', mouth='open') + path('M0,-300 L0,300 M-230,0 L230,0', sw=10), tr='translate(270,760)')
    right = g(rect(-230, -300, 460, 600, WARM2, 10, 10) + person('hp', 0, 300, .95, coat='#e08aa0', skin='d', hair='bob', eyes='happy', mouth='grin') + path('M0,-300 L0,300 M-230,0 L230,0', sw=10), tr='translate(810,760)')
    a = talk('gr', .1, h - .3, .1, rest='frown') + [arm('gr', 'r', .2, -150), arm('gr', 'r', .5, -60), arm('gr', 'r', .8, -150)]
    a += [(.2 + k * .1, f'tl.to("#s6g",{{x:{8 if k % 2 else -8},duration:.08}},{{T}});') for k in range(int(h / .1) - 2)]
    a += [arm('hp', 'r', h + .1, -130), arm('hp', 'r', h + .35, -90), arm('hp', 'r', h + .6, -130)] + pop('nt', h + .3) + bob('hp', h, h, 8, .25)
    S.append(Shot(L(6), L(7), wall(BRICK, 2400) + g(left, 's6g') + right + notes('nt', 900, 380) + text(270, 300, 'GRRR!', 90, '#ff8a5a') ,
                  [(0, 1.45, 270, 760), (h - .2, 1.35, 300, 760), (h + .2, 1.45, 810, 760), (D(6), 1.3, 800, 720)], a))
    # 7 the rival three miles away with a fishing rod
    rod = g(path('M0,0 L420,-520', sw=12, stroke='#6a4a2a') + path('M420,-520 Q470,-300 440,-160', sw=3, stroke='#f4f4e8') + ell(440, -150, 12, 12, '#e05a5a', 4), 'rod', 'translate(60,-240)')
    a = [fromto('#arr', .1, .5, {'scaleX': 0, 'transformOrigin': '0% 50%'}, {'scaleX': 1}, 'power2.out')] + pop('m3', .4)
    a += [(1.4 + k * .4, 'tl.fromTo("#rod",{rotation:0},{rotation:-6,duration:.15,yoyo:true,repeat:1,transformOrigin:"0% 100%"},{T});') for k in range(3)] + [light_win(2, 2.6)]
    arr = g(path('M0,0 L700,0', sw=16, stroke=WARM2) + path('M680,-40 L740,0 L680,40', fill=WARM2, sw=6), 'arr', 'translate(180,360)')
    S.append(Shot(L(7), L(8), terrace(sleepers=(2,)) + arr + badge('m3', 540, 270, '3 MILES', '#ffd27a', 70)
                  + person('rv', 360, 1560, 1.0, coat='#3f5f7a', skin='c', mustache=True, hat='cap', eyes='norm', mouth='smirk', extra_acc=rod),
                  [(0, 1.15, 540, 500), (1.2, 1.2, 420, 1000), (D(7), 1.25, 600, 800)], a))
    # 8 others: bamboo pole / whistling
    pole = g(path('M0,0 L80,-700', sw=14, stroke='#c8b060') + path('M30,-260 L36,-300 M50,-430 L56,-470', sw=6, stroke='#8a7030'), 'pl', 'translate(40,-250)')
    a = [(.2 + k * .35, 'tl.fromTo("#pl",{rotation:0},{rotation:4,duration:.12,yoyo:true,repeat:1,transformOrigin:"0% 100%"},{T});') for k in range(3)]
    a += [face('wh', D(8) * .5, 'happy', 'o')] + pop('wn', D(8) * .5 + .1) + [light_win(0, 1.1), light_win(3, D(8) * .5 + .4)]
    S.append(Shot(L(8), L(9), terrace(sleepers=(0, 3)) + person('bp', 120, 1560, .9, coat='#6a7a3a', skin='b', hat='cap', eyes='norm', mouth='flat', extra_acc=pole)
                  + person('wh', 900, 1560, .9, coat='#9a5ac9', skin='a', hair='tuft', eyes='norm', mouth='smile') + notes('wn', 960, 1150),
                  [(0, 1.25, 200, 950), (D(8) * .5, 1.25, 860, 1000), (D(8), 1.15, 700, 900)], a))
    # 9 you see: pea vs glass (LOUD / NO BROKEN GLASS / ONE WINDOW)
    big = g(rect(-300, -360, 600, 720, '#9fc8e8', 12, 12, 'fill-opacity=".55"') + path('M0,-360 L0,360 M-300,0 L300,0', sw=12) + ell(-150, -200, 60, 20, '#fff', extra='opacity=".5" transform="rotate(-30 -150 -200)"'), 'bg9', 'translate(540,780)')
    a = [fromto('#pb', .1, .35, {'x': -700, 'y': 300, 'opacity': 1}, {'x': 0, 'y': 0}, 'power1.in'), (.45, 'tl.to("#pb",{x:-220,y:420,duration:.6,ease:"power1.out"},{T});'),
         (.45, 'tl.fromTo("#bg9",{x:0},{x:10,duration:.06,yoyo:true,repeat:3},{T});')] + pop('ck0', 1.0) + pop('ck1', 2.2) + pop('ck2', 3.6)
    a += [fromto('#tg', 3.4, .4, {'opacity': 0, 'scale': 2, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'power2.out')]
    tgt_ = g(ell(0, 0, 330, 330, 'none', 10, 'stroke="#e05a5a"') + ell(0, 0, 200, 200, 'none', 8, 'stroke="#e05a5a"') + path('M-380,0 L380,0 M0,-380 L0,380', sw=6, stroke='#e05a5a'), 'tg', 'translate(540,780)', 'opacity="0"')
    S.append(Shot(L(9), L(10), wall(BRICK, 2400) + big + ell(540, 780, 34, 34, '#9ad04a', 7, 'id="pb" opacity="0"') + tgt_
                  + badge('ck0', 300, 300, 'LOUD', '#5fd36a', 70) + badge('ck1', 760, 300, 'GLASS OK', '#5fd36a', 64) + badge('ck2', 540, 1560, 'ONE WINDOW', '#ffd27a', 70),
                  [(0, 1.05, 540, 820), (2.0, .98, 540, 780), (3.6, .95, 540, 860), (D(9), 1.02, 540, 850)], a))
    # 10 her daughter, peas through the air raids (searchlights)
    kx, ky = 380, 1600; tx, ty = tip(kx, ky)
    a = sweep('sl', 3, 0, D(10)) + shoot('d0', 1.5, tx, ty, *WIN[1]) + shoot('d1', 2.6, tx, ty, *WIN[2]) + [light_win(1, 1.8), light_win(2, 2.9), face('dt', 1.0, 'angry', 'flat')]
    S.append(Shot(L(10), L(11), terrace(sleepers=(1, 2)) + searchlights('sl') + knocker('dt', kx, ky, 1.0, young=True, coat='#2a6a7a') + pea('d0', tx, ty) + pea('d1', tx, ty),
                  [(0, 1.0, 540, 700), (1.4, 1.2, 420, 1000), (D(10), 1.15, 600, 800)], a))
    # 11 cheap alarm clocks rain down; she walks away
    r = random.Random(4); cl = ''.join(alarm_clock(f'ac{k}', r.randint(120, 960), -200, r.uniform(.5, .8)) for k in range(9))
    a = [fromto(f'#ac{k}', k * .22, .5, {'y': 0}, {'y': 1200 + r.randint(0, 250)}, 'bounce.out') for k in range(9)] + [face('kn', .8, 'shut', 'frown'), move('#kn', 1.2, D(11) - 1.2, x=600)] + bob('kn', 1.2, D(11) - 1.2, 8, .3)
    S.append(Shot(L(11), L(12), terrace() + cl + knocker('kn', 460, 1600, 1.0, tube=True), [(0, 1.05, 540, 900), (D(11), 1.15, 760, 1050)], a))
    # 12 the only people awake while the street slept (wide, Zzz)
    zz = ''.join(text(x + 60, y - 120, 'z', 70, '#fdfcf8', extra=f'id="z{k}" opacity="0"') for k, (x, y) in enumerate(WIN))
    a = [(.2 + k * .25, f'tl.fromTo("#z{k}",{{opacity:0,y:0}},{{opacity:1,y:-60,duration:.8,repeat:2,ease:"sine.out"}},{{T}});') for k in range(8)]
    S.append(Shot(L(12), L(13), terrace(sleepers=range(8)) + zz + knocker('kn', 540, 1600, .9),
                  [(0, .95, 540, 800), (D(12), 1.15, 540, 1100)], a))
    # 13 one night: a house on fire (one window glows red, flames), she gasps
    a = flicker('fl0', 0, D(13)) + flicker('fl1', .08, D(13)) + [face('kn', .6, 'wide', 'open'), arm('kn', 'r', .7, -150)]
    S.append(Shot(L(13), L(14), terrace(lit=(6,), sleepers=(2, 3, 7)) + rect(WIN[6][0] - 95, WIN[6][1] - 105, 190, 210, '#ff5a2e', 8, 0, 'opacity=".8"')
                  + flame('fl0', WIN[6][0] - 20, WIN[6][1] + 90, 1.0) + flame('fl1', WIN[6][0] + 60, WIN[6][1] - 40, .7) + knocker('kn', 300, 1620, 1.0),
                  [(0, 1.1, 600, 800), (1.0, 1.4, 690, 860), (D(13), 1.3, 400, 1150)], a))
    # 14 payoff: rapid peas at every window, all wake, family runs out
    kx, ky = 200, 1640; tx, ty = tip(kx, ky, .9)
    a = flicker('fl0', 0, D(14)) + []
    for k, w in enumerate((2, 3, 7, 1, 0, 5)):
        a += shoot(f'r{k}', .15 + k * .22, tx, ty, *WIN[w], .2) + [light_win(w, .4 + k * .22)]
    fam = ''.join(person(f'fm{i}', 0, 0, .55, coat=['#4f7cc9', '#e05a7a', '#7a8a3a'][i], skin='abcd'[i], hair=[None, 'bob', 'tuft'][i], eyes='wide', mouth='open') for i in range(3))
    a += [fromto('#fam', 1.8, .8, {'x': 0, 'opacity': 0}, {'x': -260, 'opacity': 1}, 'power2.out')] + pop('saf', D(14) - .9)
    S.append(Shot(L(14), L(15), terrace(lit=(6,), sleepers=(0, 1, 2, 3, 5, 7)) + flame('fl0', WIN[6][0] - 20, WIN[6][1] + 90, 1.0) + knocker('kn', kx, ky, .9)
                  + ''.join(pea(f'r{k}', tx, ty) for k in range(6)) + g(''.join(g(person(f'fm{i}', 0, 0, .55, coat=['#4f7cc9', '#e05a7a', '#7a8a3a'][i], skin='abcd'[i], hair=[None, 'bob', 'tuft'][i], eyes='wide', mouth='open'), tr=f'translate({i * 120},0)') for i in range(3)), 'fam', 'translate(820,1560)', 'opacity="0"')
                  + badge('saf', 540, 300, 'EVERYONE OUT', '#5fd36a', 72),
                  [(0, 1.05, 540, 800), (1.4, 1.15, 640, 900), (D(14), 1.2, 600, 1000)], a))
    # 15 A/B
    S.append(Shot(L(15), total, outro('DEAL', '', 'MY', 'CHANCES'), [(0, 1.0, 540, 950), (total - L(15), 1.12, 540, 1000)], outro_anims()))
    return S

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(15) - .3,
      'flares': [(L(0) + 2.3, 'flare'), (L(2) + 2.8, 'shrink'), (L(7) + .6, 'flare'), (L(13) + .5, 'shrink'), (L(14) + 1.6, 'flare')]}

def audio():
    T = TOTAL
    music = [('km_Ghost_Story.mp3', 8, 0, L(1) - .05, -2, (.02, .2)),
             ('km_Merry_Go.mp3', 0, L(1), L(9), -1, (.05, .3)),
             ('km_Investigations.mp3', 0, L(9), L(12), -2, (.2, .2)),
             ('km_Darkling.mp3', 5, L(12), L(14) - .35, 0, (.2, .1)),
             ('km_Fun_in_a_Bottle.mp3', 0, L(14) + .7, T, -1, (.05, 1.0))]
    O = '100-cc0-sfx/'; O2 = '100-cc0-sfx-2/sfx100v2_'; SW = 'swishes-sound-pack/swishes/swish-'
    TAK = O + 'wooden_01.ogg'; PFF = O2 + 'air_01.ogg'
    fs = [(f'footsteps-0/0{k % 6 + 1}-footstep.ogg', .1 + k * .25, -8) for k in range(6)]
    sfx = fs + [(PFF, 2.0, -6, 0, .4), (TAK, 2.3, 0), (PFF, 3.2, -6, 0, .4), (TAK, 3.5, 0)]
    sfx += [(SW + '3.wav', L(1) - .1, -4), (O + 'metal_05.ogg', L(1) + .55, -2), (O + 'metal_05.ogg', L(1) + .75, -6),
            (SW + '5.wav', L(2) - .05, -5), (O + 'bell_02.ogg', L(2) + 1.2, -5), (O + 'paper_02.ogg', L(2) + .9, -6),
            (O + 'slam_04.ogg', L(2) + D(2) * .5 + .7, -3), ('footsteps-0/01-footstep.ogg', L(2) + D(2) * .5 + .1, -6), ('footsteps-0/02-footstep.ogg', L(2) + D(2) * .5 + .3, -6),
            (SW + '7.wav', L(3) - .05, -4), (O + 'slam_02.ogg', L(3) + .95, -2)]
    for k, t in enumerate((1.4, 2.1, 2.8)): sfx += [(PFF, L(4) + t, -6, 0, .3), (TAK, L(4) + t + .25, 0)]
    sfx += [(O + 'paper_01.ogg', L(4) + .2, -6)]
    sfx += [(TAK, L(5) + k * .3, -10) for k in range(4)] + [(O + 'door_close_01.ogg', L(5) + 1.2, -6)]
    sfx += [('angry-grunt/grunt.ogg', L(6) + .1, -4) if False else (O + 'slam_01.ogg', L(6) + .3, -5), (O + 'slam_03.ogg', L(6) + .8, -6), (TAK, L(6) + D(6) * .5 + .1, -2), (TAK, L(6) + D(6) * .5 + .3, -4), (TAK, L(6) + D(6) * .5 + .45, -3)]
    sfx += [(SW + '2.wav', L(7) - .05, -4)] + [(TAK, L(7) + 1.55 + k * .4, -3) for k in range(3)]
    sfx += [(SW + '8.wav', L(8) - .05, -5)] + [(TAK, L(8) + .3 + k * .35, -4) for k in range(3)]
    sfx += [(SW + '4.wav', L(9) - .05, -4), (PFF, L(9) + .1, -4, 0, .4), ('glass-tap/glass_tap.ogg', L(9) + .45, 0) if False else (O + 'glass_01.ogg', L(9) + .45, 0),
            (O + 'spring_02.ogg', L(9) + 1.0, -6), (O + 'spring_04.ogg', L(9) + 2.2, -6), (O + 'switch_02.ogg', L(9) + 3.5, -4)]
    sfx += [('muffled-distant-explosion/NenadSimic - Muffled Distant Explosion.wav', L(10) + .3, -6, 0, 1.6), (PFF, L(10) + 1.5, -6, 0, .3), (TAK, L(10) + 1.8, 0),
            (PFF, L(10) + 2.6, -6, 0, .3), (TAK, L(10) + 2.9, 0), ('muffled-distant-explosion/NenadSimic - Muffled Distant Explosion.wav', L(10) + 3.4, -8, 0, 1.2)]
    sfx += [(O + 'bell_01.ogg', L(11) + k * .22 + .3, -9) for k in range(9)] + [(O + 'metal_01.ogg', L(11) + .5, -8)]
    sfx += [(SW + '6.wav', L(12) - .05, -6), ('fire-crackling/fire-1.ogg', L(13) - .1, -2, 0, D(13) + D(14))]
    sfx += [(O + 'weird_04.ogg', L(13) + .6, -6)]
    for k in range(6): sfx += [(TAK, L(14) + .35 + k * .22, -1)]
    sfx += [('crowd-shoutingspeaking-ambience/crowd_shouting.ogg', L(14) + 1.8, -8, 0, 1.6), (O + 'door_close_01.ogg', L(14) + 1.7, -4)]
    sfx += [(SW + '1.wav', L(15) - .05, -3), ('fire-crackling/fire-1.ogg', L(15) + .1, -10, 0, 1.2), (O2 + 'air_01.ogg', T - 1.0, -1)]
    return music, sfx

def build_tt():
    def shots_tt(lines, total):
        S = shots(lines, total)
        S[0].cam = [(0, 2.0, 690, 640), (1.0, 1.7, 600, 700), (2.4, 1.3, 520, 900), (D(0), 1.2, 480, 820)]
        return S
    ov = ('<div id="ttq" class="clip" data-start="0" data-duration="2.4" data-track-index="5" style="position:absolute;left:0;top:300px;width:1080px;text-align:center;z-index:960">'
          '<span style="display:inline-block;font-family:Montserrat;font-weight:900;font-size:76px;line-height:1.05;color:#140c26;background:#ffd27a;padding:18px 34px;border-radius:26px;border:8px solid #140c26">'
          'PAID TO SHOOT PEAS<br>AT YOUR WINDOW?</span></div>')
    js = 'tl.fromTo("#ttq span",{scale:.6,rotation:-4},{scale:1,rotation:-2,duration:.25,ease:"back.out(3)"},0.05);'
    return build(dict(EP, shots=shots_tt, hfdir='hf_tt', overlay=ov, overlay_js=js))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mix':
        from mix import mix
        mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
    elif len(sys.argv) > 1 and sys.argv[1] == 'tt': print(build_tt())
    else: print(build(EP), TOTAL)
