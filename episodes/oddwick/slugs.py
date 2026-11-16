import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *

SLUG = '2026-11-16-garden-slugs-gas-alarms'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.3, 2)
def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']

def mask(mid):
    m = (path('M-78,-200 Q0,-240 78,-200 L78,-110 Q0,-60 -78,-110 Z', grad('#5a6a4a'), 7) + ell(-34, -190, 26, 26, '#bfe8ff', 7) + ell(34, -190, 26, 26, '#bfe8ff', 7)
         + rect(-28, -120, 56, 70, grad('#3a4a3a'), 14, 7))
    return g(m, mid, extra='opacity="0"')
def soldier(pid, x, y, s=1, coat='#6a7a4a', skin='a', eyes='norm', mouth='smile', flip=False, with_mask=False):
    return person(pid, x, y, s, coat=coat, skin=skin, hat='helmet', eyes=eyes, mouth=mouth, flip=flip, extra_acc=mask(f'{pid}-mask') if with_mask else '')
def sarge(pid, x, y, s=1, eyes='side', mouth='smirk', flip=False, with_mask=False):
    return person(pid, x, y, s, coat='#7a6a3a', skin='b', hat='campaign', mustache=True, eyes=eyes, mouth=mouth, flip=flip, extra_acc=mask(f'{pid}-mask') if with_mask else '')
def prof(pid, x, y, s=1, eyes='norm', mouth='smile', flip=False):
    return person(pid, x, y, s, coat='#f0ece0', skin='a', glasses=True, hair='tuft', eyes=eyes, mouth=mouth, flip=flip)
def jar(jid, x, y, s=1, with_slug=True):
    inner = slug(f'{jid}-sl', 0, 70, .55) if with_slug else ''
    return g(rect(-110, -120, 220, 230, '#bfe8ff', 40, 8, 'opacity=".35"') + inner + rect(-110, -120, 220, 230, 'none', 40, 8) + rect(-90, -150, 180, 40, grad('#a07a4a'), 10, 7)
             + ell(-60, -60, 14, 40, '#fff', extra='opacity=".5"'), jid, f'translate({x},{y}) scale({s})')
def gas(gid, x, y, s=1, op=.0):
    return g(''.join(ell(dx, dy, r, r * .7, 'url(#gas)') for dx, dy, r in [(-160, 0, 220), (60, -40, 260), (260, 20, 220), (-40, 80, 240), (180, 110, 200)]), gid, f'translate({x},{y}) scale({s})', f'opacity="{op}"')

def trench(moon=True):
    sb = ''.join(ell(x, 1030 + (x // 90 % 2) * 6, 70, 34, grad('#a08a5a'), 6) for x in range(-200, 1300, 120))
    return (sky(moon=moon) + rect(-400, 1040, W + 800, 900, grad('#5a3a2a', True), 0, 0) + sb
            + ''.join(rect(x, 1060, 26, 600, grad('#7a5a3a'), 4, 5) for x in range(-160, 1260, 140)) + rect(-400, 1380, W + 800, 1400, '#3a2418', 0, 0)
            + ''.join(rect(x, 1380, 120, 26, grad('#8a6a4a'), 4, 5) for x in range(-300, 1300, 130)) + pool(540, 1300, 600, 260))

def basement():
    fur = (rect(560, 640, 380, 640, grad('#5a5a6a'), 20, 10) + rect(640, 900, 220, 160, '#2a1810', 12, 8) + rect(660, 920, 180, 120, '#ff7a2a', 8, 0, 'id="fire" opacity=".9"')
           + rect(700, 300, 90, 360, grad('#6a6a7a'), 6, 8) + ell(750, 980, 220, 160, 'url(#glow)', extra='opacity=".8"'))
    return wall('#4a3a5a', 1300) + floor_(1300) + fur + pool(700, 1300, 520, 200)

def tent():
    return (rect(-400, -400, W + 800, H + 800, grad('#6a6a3a', True), sw=0) + path('M-200,1260 L540,180 L1280,1260', fill='none', sw=14, stroke='#3a3a1a')
            + path('M540,180 L540,1260', sw=10, stroke='#4a3a1a') + floor_(1260, lines=False) + lamp(540, 520)
            + rect(240, 1080, 600, 50, grad('#8a5a3c'), 10, 8) + rect(270, 1130, 30, 180, shade('#8a5a3c'), 4, 6) + rect(780, 1130, 30, 180, shade('#8a5a3c'), 4, 6))

def outro():
    return (sky(moon=False) + floor_(1300) + pool(540, 1300, 600, 260)
            + candle('ca', 300, 900, 1.15, 'A', face='happy') + candle('cb', 780, 900, 1.15, 'B', face='smirk')
            + text(300, 580, 'THE SLUG', 64) + text(780, 580, 'THE DOG', 64))

def squeeze(sel, t, d=.35):   # slug scrunches into a ball (eyes pull in) and holds
    return [move(f'{sel}-body', t, d, 'back.in(2)', scaleX=.45, scaleY=1.25, transformOrigin='50% 100%'), move(f'{sel}-eyes', t, .2, scaleY=.1, opacity=0, transformOrigin='50% 100%')]
def relax(sel, t, d=.5):
    return [move(f'{sel}-body', t, d, 'elastic.out(1,.5)', scaleX=1, scaleY=1, transformOrigin='50% 100%'), move(f'{sel}-eyes', t + .2, .3, scaleY=1, opacity=1, transformOrigin='50% 100%')]

def shots(lines, total):
    S = []
    # 0 hook: night trench, a soldier holds a jar; the slug inside scrunches, gas creeps in
    a = [fromto('#gs', 0, 4, {'x': 500, 'opacity': 0}, {'x': 120, 'opacity': .8}, 'power1.out')] + squeeze('#j0-sl', 1.6) + [face('s0', 1.7, 'wide', 'o')] + bob('s0', 0, 4, 5, .45)
    S.append(Shot(0, L(1), trench() + soldier('s0', 400, 1420, 1.15) + jar('j0', 700, 1180, 1.1) + gas('gs', 600, 1050, 1.2),
                  [(0, 1.6, 700, 1150), (1.8, 1.8, 700, 1180), (E(0) - .1, 1.15, 560, 1050)], a))
    # 1 museum scientist, basement furnace leaks fumes, slugs scrunch
    a = [fromto('#fm', 1.6, 2.0, {'opacity': 0, 'y': 0}, {'opacity': .8, 'y': 200}, 'none')] + squeeze('#sa', 2.8) + squeeze('#sb', 3.0) + [face('pr', 3.1, 'wide', 'o'), arm('pr', 'r', 3.3, -110)]
    a += [move('#fire', k * .3, .15, opacity=(.6 if k % 2 else 1)) for k in range(18)] + blink('pr', [.8, 2.2])
    S.append(Shot(L(1), L(2), basement() + prof('pr', 330, 1360, 1.0, flip=False) + slug('sa', 560, 1380, .7) + slug('sb', 820, 1420, .6, flip=True)
                  + gas('fm', 700, 900, .6), [(0, 1.0, 540, 950), (2.4, 1.4, 680, 1250), (E(1) - L(1), 1.15, 450, 1100)], a))
    # 2 he goes to the army with a jar
    a = [fromto('#p2', 0, 1.2, {'x': -400}, {'x': 0}, 'power2.out')] + bob('p2', 0, 1.2, 12, .2) + talk('p2', 1.2, 1.0) + [arm('p2', 'r', 1.2, -120)]
    S.append(Shot(L(2), L(3), tent() + prof('p2', 330, 1360, 1.0) + jar('j2', 470, 1190, .5) + sarge('sg', 780, 1360, 1.05, eyes='norm', mouth='flat', flip=True),
                  [(0, 1.0, 540, 950), (E(2) - L(2), 1.25, 600, 1000)], a + [fromto('#j2', 0, 1.2, {'x': -400}, {'x': 0}, 'power2.out')]))
    # 3 the sergeant mocks
    a = talk('s3', 0, E(3) - L(3), rest='smirk') + [arm('s3', 'l', .4, 120), face('s3', 1.6, 'side', 'grin')] + bob('s3', 0, 3, 6, .3)
    S.append(Shot(L(3), L(4), tent() + sarge('s3', 540, 1450, 1.3, eyes='side', mouth='smirk'), [(0, 1.9, 540, 1000), (1.5, 1.6, 600, 1030), (E(3) - L(3), 1.8, 540, 1000)], a))
    # 4 the whole tent laughs
    crowd = ''.join(soldier(f'l{i}', 120 + i * 210, 1430 + (i % 2) * 30, .75, coat=['#6a7a4a', '#5a6a3a', '#7a8a5a'][i % 3], skin='abcd'[i % 4], eyes='happy', mouth='grin') for i in range(5))
    a = sum((bob(f'l{i}', i * .04, 1.2, 16, .12 + i * .01) for i in range(5)), [])
    S.append(Shot(L(4), L(5), tent() + crowd, [(0, 1.1, 540, 1250), (E(4) - L(4) + .1, 1.25, 540, 1250)], a))
    # 5 calm demo: a slug in a jar, a tiny bit of gas (a dropper puff)
    drop = g(rect(-14, -160, 28, 140, '#e8e8f0', 8, 6) + ell(0, -170, 24, 18, '#d05a5a', 6), 'dp', 'translate(540,880)')
    a = [fromto('#dp', .3, .6, {'y': -200, 'opacity': 0}, {'y': 0, 'opacity': 1}), fromto('#pf', 2.2, .8, {'scale': .2, 'opacity': 0, 'transformOrigin': '50% 50%'}, {'scale': 1, 'opacity': .7})]
    a += [face('s5', 3.0, 'side', 'smirk')] + blink('p5', [1.0, 3.6])
    S.append(Shot(L(5), L(6), tent() + prof('p5', 230, 1380, .95) + sarge('s5', 860, 1380, .95, flip=True) + jar('j5', 540, 1100, 1.0) + drop
                  + g(ell(0, 0, 90, 60, 'url(#gas)'), 'pf', 'translate(540,1050)', 'opacity="0"'),
                  [(0, 1.0, 540, 1000), (2.0, 1.5, 540, 1060), (E(5) - L(5), 1.3, 700, 1060)], a))
    # 6 squeezes into a ball (big close-up)
    S.append(Shot(L(6), L(7), tent() + jar('j6', 540, 1100, 1.0) + g(ell(0, 0, 90, 60, 'url(#gas)'), tr='translate(540,1050)', extra='opacity=".6"'),
                  [(0, 2.2, 540, 1140), (E(6) - L(6), 2.6, 540, 1150)], squeeze('#j6-sl', .25, .3)))
    # 7 'Lucky slug.' sergeant shrugs
    S.append(Shot(L(7), L(8), tent() + sarge('s7', 540, 1450, 1.3, eyes='side', mouth='smirk'), [(0, 1.9, 540, 1010), (E(7) - L(7), 2.0, 540, 1000)],
                  [arm('s7', 'l', 0, 70), arm('s7', 'r', 0, -70)] + talk('s7', 0, .7, rest='smirk')))
    # 8 even less gas: squeeze again, laughing stops
    a = [fromto('#pg', .1, .5, {'scale': .1, 'opacity': 0, 'transformOrigin': '50% 50%'}, {'scale': .5, 'opacity': .6})] + squeeze('#j8-sl', .7, .25) + [face('s8', 1.2, 'wide', 'frown')]
    S.append(Shot(L(8), L(9), tent() + sarge('s8', 860, 1380, .95, flip=True) + jar('j8', 540, 1100, 1.0) + g(ell(0, 0, 90, 60, 'url(#gas)'), 'pg', 'translate(540,1050)', 'opacity="0"'),
                  [(0, 1.6, 540, 1080), (1.1, 1.7, 860, 1000), (E(8) - L(8), 1.8, 860, 990)], a))
    # 9 'You see': diagram, one breathing hole on the side that shuts
    hole = g(ell(0, 0, 34, 24, '#3a1a1a', 7), 'hole', 'translate(560,1060)')
    arrow = g(path('M0,0 L-120,-160', sw=14, stroke=WARM2) + path('M-20,-10 L0,0 L-6,-24', sw=14, stroke=WARM2), 'arw', 'translate(600,1020)')
    a = [fromto('#arw', .4, .4, {'opacity': 0, 'scale': .3}, {'opacity': 1, 'scale': 1}, 'back.out(2)'), move('#hole', 3.0, .25, scaleY=.1, transformOrigin='50% 50%')]
    a += squeeze('#big', 3.4, .4)
    S.append(Shot(L(9), L(10), wall('#3a5a4a', 1250) + floor_(1250) + pool(540, 1150, 600, 260) + slug('big', 540, 1200, 3.0) + hole + arrow + text(640, 700, 'BREATHING HOLE', 64, '#fff', extra='id="lbl"'),
                  [(0, 1.0, 540, 1000), (2.5, 1.35, 560, 1060), (E(9) - L(9), 1.15, 540, 1050)], a))
    # 10 smoke alarm that crawls; 3x better than a human nose
    alarm = g(ell(0, 0, 50, 22, '#e8e8f0', 6) + ell(0, -8, 18, 12, '#ff3a3a', 0, 'id="al"'), 'alm', 'translate(500,1020)')
    nose = g(path('M0,-120 Q60,40 30,70 Q0,90 -30,70 Q-20,20 0,-120 Z', grad(SKIN['a']), 8), 'nose', 'translate(260,600)')
    a = [move('#crawl', 0, 2.3, 'none', x=160)] + [setp('#al', k * .25, opacity=(1 if k % 2 == 0 else .2)) for k in range(9)]
    a += [fromto('#b1', 2.4, .4, {'scaleY': 0, 'transformOrigin': '50% 100%'}, {'scaleY': 1}), fromto('#b2', 2.8, .6, {'scaleY': 0, 'transformOrigin': '50% 100%'}, {'scaleY': 1}, 'back.out(1.5)')]
    bars = (g(rect(180, -120, 160, 120, '#c9a080', 10, 7), 'b1', 'translate(0,900)') + g(rect(700, -360, 160, 360, '#c98a4a', 10, 7), 'b2', 'translate(0,900)')
            + text(800, 470, 'x3', 110, WARM2) + nose + g(slug('ms', 0, 0, .7), tr='translate(780,620)'))
    S.append(Shot(L(10), L(11), wall('#3a5a4a', 1250) + floor_(1250) + pool(540, 1150, 600, 260) + g(slug('cr', 400, 1200, 1.6) + alarm, 'crawl') + bars,
                  [(0, 1.5, 480, 1120), (2.2, 1.0, 540, 900), (E(10) - L(10), 1.1, 540, 780)], a))
    # 11 not even hurt: unscrunches, crawls on
    a = squeeze('#u', 0, .01) + relax('#u', 1.4) + [move('#u', 2.0, 1.0, 'none', x=260)]
    S.append(Shot(L(11), L(12), wall('#3a5a4a', 1250) + floor_(1250) + pool(540, 1200, 600, 260) + slug('u', 420, 1260, 1.8), [(0, 1.3, 460, 1150), (E(11) - L(11), 1.2, 640, 1150)], a))
    # 12 to the trenches, officially, a five-month tour of duty
    marchers = ''.join(soldier(f'm{i}', -120 - i * 260, 1420, .9, skin='abcd'[i % 4]) + jar(f'mj{i}', -10 - i * 260, 1210, .42) for i in range(4))
    a = [move('#mr', 0, E(12) - L(12), 'none', x=1100)] + sum((bob(f'm{i}', i * .1, 3.8, 10, .22) for i in range(4)), [])
    a += [fromto('#stamp', 2.4, .25, {'scale': 3, 'opacity': 0, 'transformOrigin': '50% 50%', 'rotation': -14}, {'scale': 1, 'opacity': 1, 'rotation': -14}, 'power3.in')]
    S.append(Shot(L(12), L(13), trench() + g(marchers, 'mr') + g(rect(-260, -80, 520, 160, 'none', 20, 12, 'stroke="#e05a5a"') + text(0, 36, '5 MONTHS', 100, '#e05a5a'), 'stamp', 'translate(540,600)', 'opacity="0"'),
                  [(0, 1.2, 400, 1050), (E(12) - L(12), 1.2, 640, 1000)], a))
    # 13 night watch: a slug starts to shrink, nobody smells a thing
    a = [face('t1', .5, 'shut', 'smile'), face('t2', .5, 'shut', 'flat')] + squeeze('#j13-sl', 1.8, .9) + [face('t1', 2.8, 'wide', 'o')]
    S.append(Shot(L(13), L(14), trench() + rect(-400, -400, W + 800, H + 800, '#0a0618', sw=0, extra='opacity=".35"') + soldier('t1', 300, 1420, 1.0) + soldier('t2', 800, 1420, 1.0, flip=True, skin='c')
                  + jar('j13', 540, 1230, .8) + ell(540, 1200, 240, 240, 'url(#glow)', extra='opacity=".5"'),
                  [(0, 1.0, 540, 1050), (1.6, 1.9, 540, 1220), (3.0, 1.35, 400, 1050), (E(13) - L(13), 1.2, 540, 1050)], a))
    # 14 masks on anyway
    a = [fromto('#k1-mask', .1, .2, {'opacity': 0, 'y': -80}, {'opacity': 1, 'y': 0}), fromto('#k2-mask', .3, .2, {'opacity': 0, 'y': -80}, {'opacity': 1, 'y': 0}),
         arm('k1', 'l', 0, 160), arm('k1', 'l', .3, 0), arm('k2', 'r', .2, -160), arm('k2', 'r', .5, 0)]
    S.append(Shot(L(14), L(15), trench() + rect(-400, -400, W + 800, H + 800, '#0a0618', sw=0, extra='opacity=".3"') + soldier('k1', 330, 1420, 1.1, with_mask=True) + soldier('k2', 760, 1420, 1.1, flip=True, skin='c', with_mask=True),
                  [(0, 1.4, 540, 1050), (E(14) - L(14), 1.3, 540, 1050)], a))
    # 15 the gas rolls in over masks that are already on
    a = [fromto('#gr', 0, 2.2, {'x': 900, 'opacity': .9}, {'x': -100, 'opacity': .9}, 'power1.inOut'), arm('k3', 'r', 1.4, -150), arm('k4', 'l', 1.6, 150)]
    S.append(Shot(L(15), L(16), trench() + soldier('k3', 330, 1420, 1.1, with_mask=True).replace('opacity="0"><g id="k3-mask"', 'opacity="1"><g id="k3-mask"')
                  + soldier('k4', 760, 1420, 1.1, flip=True, skin='c', with_mask=True) + gas('gr', 540, 1100, 1.8, .9),
                  [(0, 1.0, 540, 1000), (E(15) - L(15), 1.15, 540, 1050)], a + [setp('#k3-mask', 0, opacity=1), setp('#k4-mask', 0, opacity=1)]))
    # 16 payoff: the sergeant who laughed now checks his slug first (hugs the jar)
    rifle = g(path('M0,0 L40,-420', sw=26, stroke=OUT) + path('M0,0 L40,-420', sw=14, stroke='#6a4a2a'), tr='translate(900,1380)')
    a = [face('s16', 1.0, 'happy', 'grin'), arm('s16', 'l', .3, 60), arm('s16', 'r', .3, -150), fromto('#hrt', 1.4, .5, {'y': 0, 'opacity': 0}, {'y': -120, 'opacity': 1})] + bob('s16', 0, 3.4, 6, .4)
    S.append(Shot(L(16), L(17), trench() + rifle + sarge('s16', 540, 1440, 1.2, eyes='norm', mouth='smile') + jar('j16', 720, 1020, .5)
                  + g(path('M0,30 L-40,-10 Q-60,-50 -20,-50 Q0,-50 0,-26 Q0,-50 20,-50 Q60,-50 40,-10 Z', '#ff5a7a', 7), 'hrt', 'translate(640,800)', 'opacity="0"'),
                  [(0, 1.0, 540, 1000), (1.5, 1.5, 620, 1000), (E(16) - L(16), 1.6, 620, 980)], a))
    # 17 A/B candles
    a = [fromto('#ca', 0, .4, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'), fromto('#cb', .2, .4, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'),
         move('#ca-flame', 2.2, .2, scale=1.4, transformOrigin='50% 100%'), move('#ca-flame', 2.4, .3, scale=1), move('#cb-flame', 3.2, .2, scale=1.4, transformOrigin='50% 100%'), move('#cb-flame', 3.4, .3, scale=1)]
    S.append(Shot(L(17), total, outro(), [(0, 1.0, 540, 950), (total - L(17), 1.12, 540, 1000)], a))
    return S

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(17) - .3, 'flares': [(L(1) + 2.8, 'flare'), (L(4), 'flare'), (L(13) + 1.8, 'shrink'), (L(15), 'shrink'), (L(16) + .8, 'flare')]}

def audio():
    T = TOTAL; P = L(15)
    music = [('thinking.mp3', 0, 0, L(2), 0, (.02, .3)),
             ('bumbly.mp3', 15, L(2) - .1, L(9), -1, (.1, .3)),
             ('thinking.mp3', 60, L(9), L(12), -2, (.2, .3)),
             ('darkest.mp3', 40, L(12), P - .3, 1, (.3, .2)),
             ('heroic.mp3', 55, L(16) - .1, T, -1, (.2, 1.2))]
    O = '100-cc0-sfx-2/sfx100v2_'
    sfx = [('compressed-gas-leak-sfx/compressed_gas_leak.ogg', 0.1, -6), ('25-cc0-mud-sfx/mud_03.ogg', 1.6, -1), ('low-rumbling/low-rumbling-176033.mp3', 0, -10, 0, 4),
           ('whoosh-cinematic.mp3', L(1) - .15, -3), ('fire-crackling/fire-1.ogg', L(1), -8, 0, 3), ('compressed-gas-leak-sfx/compressed_gas_leak.ogg', L(1) + 1.6, -6),
           ('25-cc0-mud-sfx/mud_07.ogg', L(1) + 2.8, -2), ('25-cc0-mud-sfx/mud_09.ogg', L(1) + 3.0, -3),
           ('100-cc0-sfx/door_open.ogg', L(2) - .05, -5)]
    sfx += [('sound-effects-pack/Footsteps/step%d.wav' % (2 + k % 3), L(2) + .1 + k * .2, -8) for k in range(6)]
    sfx += [('do-you-remember-laughter/ogalaughter_2.ogg', L(4) - .15, -1, 22.3, 2.4), ('whoosh-short.mp3', L(5) - .05, -4),
            ('100-cc0-sfx/glass_01.ogg', L(5) + .9, -3), ('compressed-gas-leak-sfx/compressed_gas_leak.ogg', L(5) + 2.2, -6, 0, .8),
            ('25-cc0-mud-sfx/mud_05.ogg', L(6) + .25, 0), ('100-cc0-sfx/spring_01.ogg', L(7), -8),
            ('compressed-gas-leak-sfx/compressed_gas_leak.ogg', L(8) + .1, -9, 0, .5), ('25-cc0-mud-sfx/mud_11.ogg', L(8) + .7, 0), ('impact-bass-2.mp3', L(8) + 1.2, -6),
            ('whoosh.mp3', L(9) - .1, -3), ('100-cc0-sfx/plop_01.ogg', L(9) + .4, -4), ('25-cc0-mud-sfx/mud_14.ogg', L(9) + 3.0, -2),
            ('whoosh-short.mp3', L(10) - .05, -4), ('100-cc0-sfx/spring_03.ogg', L(10) + 2.4, -5), ('100-cc0-sfx/plop_02.ogg', L(10) + 2.9, -3),
            ('25-cc0-mud-sfx/mud_16.ogg', L(11) + 1.4, -3), ('25-cc0-mud-sfx/mud_18.ogg', L(11) + 2.1, -6), ('25-cc0-mud-sfx/mud_20.ogg', L(11) + 2.6, -6),
            ('whoosh-cinematic.mp3', L(12) - .15, -3), ('impact-bass-1.mp3', L(12) + 2.55, -2)]
    sfx += [('sound-effects-pack/Footsteps/hard-footstep%d.wav' % (1 + k % 2), L(12) + .1 + k * .22, -9) for k in range(10)]
    sfx += [('low-rumbling/low-rumbling-176033.mp3', L(13), -9, 4, 4), ('25-cc0-mud-sfx/mud_22.ogg', L(13) + 1.8, -1), ('heartbeat-sounds/heartbeat_fast_0.wav', L(13) + 2.4, -2),
            ('202-more-sound-effects/Cloth/Cloth_02.wav', L(14) + .1, 0), ('202-more-sound-effects/Cloth/Cloth_04.wav', L(14) + .3, 0),
            ('breathing-tired/breathing%20tired.ogg', L(14) + .6, -5),
            ('compressed-gas-leak-sfx/compressed_gas_leak.ogg', P, -3), ('storm-siren/storm_3_siren.mp3', P, -6, 2, 2.2), ('impact-bass-1.mp3', P + .05, 0),
            ('whoosh.mp3', L(16) - .1, -3), ('100-cc0-sfx/plop_02.ogg', L(16) + 1.4, -4),
            ('whoosh.mp3', L(17) - .05, -3), ('fire-crackling/fire-1.ogg', L(17) + .1, -6, 0, 1.2), (O + 'air_01.ogg', T - 1.0, -1)]
    return music, sfx

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mix':
        from mix import mix
        mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
    else: print(build(EP), TOTAL)
