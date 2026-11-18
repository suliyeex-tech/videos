import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *
from props2 import *

SLUG = '2026-11-18-londons-bridge-lasted-2-days'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.3, 2)
def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']
def D(i): return L(i + 1) - L(i)

def engineer(pid, x, y, s=1, eyes='norm', mouth='flat', flip=False):
    clip = g(rect(-50, -70, 100, 130, '#fdfcf8', 8, 6) + path('M-30,-30 L30,-30 M-30,0 L30,0 M-30,30 L20,30', sw=5), tr='translate(110,-120)')
    return person(pid, x, y, s, coat='#e0702a', skin='c', hat='hard', eyes=eyes, mouth=mouth, flip=flip, extra_acc=clip)

def walkers(prefix, n, y, x0, x1, s=.5, seed=2, step=False):
    r = random.Random(seed); cols = ['#4f7cc9', '#e05a7a', '#7a8a3a', '#c06a2a', '#3f5f9f', '#9a5ac9', '#2f7a8a']
    return ''.join(person(f'{prefix}{i}', x0 + (x1 - x0) * i / max(1, n - 1), y + r.randint(-10, 10), s, coat=r.choice(cols), skin=r.choice('abcd'),
                          hair=r.choice(['tuft', 'bob', None, 'bun']), eyes='norm', mouth='smile') for i in range(n))

def shots(lines, total):
    S = []
    # 0 hook: the new bridge, full of people... a CLOSED barrier slams down. Nothing is broken (green check).
    bar = g(rect(-420, -60, 840, 120, '#e05a5a', 20, 9) + text(0, 30, 'CLOSED', 96), 'bar', 'translate(540,820)', 'opacity="0"')
    a = sway('#deck', 0, D(0), 8, .8) + [fromto('#bar', L(0) + 2.0, .3, {'opacity': 0, 'y': -500, 'rotation': -8}, {'opacity': 1, 'y': 0, 'rotation': -3}, 'bounce.out')]
    a += [fromto('#ok', E(0) - 1.4, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    S.append(Shot(0, L(1), city_river() + footbridge('deck', 1080, 22) + bar + check('ok', 860, 1000, 1.3) + text(860, 1130, 'NOT BROKEN', 52, extra='id="okt" opacity="0"'),
                  [(0, 1.5, 540, 1040), (1.6, 1.25, 700, 1000), (2.4, 1.1, 540, 900), (D(0), 1.3, 760, 1000)], a + [move('#okt', E(0) - 1.3, .2, opacity=1)]))
    # 1 a thin steel blade over the river, 325 m, glide along it
    meas = g(path('M-300,0 L1380,0', sw=8, stroke=WARM2) + path('M-300,-30 L-300,30 M1380,-30 L1380,30', sw=8, stroke=WARM2), 'ms', 'translate(0,1180)', 'opacity="0"')
    a = [fromto('#ms', .8, .4, {'opacity': 0, 'scaleX': 0, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scaleX': 1}), fromto('#m325', 1.5, .3, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    S.append(Shot(L(1), L(2), city_river() + footbridge('deck', 1080, 0) + meas + text(540, 1300, '325 m', 130, WARM2, extra='id="m325" opacity="0"'),
                  [(0, 1.6, 100, 1060), (1.5, 1.2, 540, 1080), (D(1), 1.5, 980, 1060)], a))
    # 2 opening day: 90,000 people come to cross; crowd pours in
    crowd = walkers('w', 9, 1500, 80, 1000, .62, 3)
    a = [fromto('#wg', 0, D(2), {'x': -700}, {'x': 120}, 'power1.out')] + sum((bob(f'w{i}', 0, D(2), 10, .25) for i in range(9)), [])
    a += [fromto('#n90', 1.2, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    flags = ''.join(g(path('M0,0 L0,-160', sw=6) + path('M0,-160 L70,-140 L0,-110 Z', ['#e05a5a', '#ffd27a', '#5fa0e0'][i % 3], 5), tr=f'translate({100 + i * 120},{1080})') for i in range(8))
    S.append(Shot(L(2), L(3), city_river() + footbridge('deck', 1080, 30, 8) + flags + g(crowd, 'wg') + text(540, 700, '90,000', 170, WARM2, extra='id="n90" opacity="0"'),
                  [(0, 1.0, 540, 1100), (1.4, 1.25, 540, 1200), (D(2), 1.1, 540, 950)], a))
    # 3 halfway... the bridge starts to sway: left, right, left (big tilt)
    a = sway('#deck', .6, D(3) - .6, 26, .75, 2.0, 1.5)
    a += [fromto(f'#lr{k}', 1.7 + k * .45, .15, {'opacity': 0, 'scale': .5, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)') for k in range(3)]
    a += [setp(f'#lr{k}', 1.7 + (k + 1) * .45, opacity=0) for k in range(2)]
    S.append(Shot(L(3), L(4), city_river() + footbridge('deck', 1080, 34, 9) + text(300, 760, 'LEFT', 120, extra='id="lr0" opacity="0"') + text(780, 760, 'RIGHT', 120, extra='id="lr1" opacity="0"') + text(300, 760, 'LEFT', 120, extra='id="lr2" opacity="0"'),
                  [(0, 1.3, 540, 1040), (1.4, 1.6, 400, 1050), (2.6, 1.6, 700, 1050), (D(3), 1.4, 540, 1050)], a))
    # 4 close-up: one grabs the rail, one freezes, one laughs
    rail = path('M-400,1060 L1500,1060', sw=16, stroke='#c8d0e8') + ''.join(path(f'M{xx},1060 L{xx},1300', sw=8, stroke='#c8d0e8') for xx in range(-300, 1400, 120))
    p3 = (person('pa', 230, 1400, 1.0, coat='#4f7cc9', skin='a', hair='bob', eyes='wide', mouth='o') + person('pb', 540, 1400, 1.0, coat='#7a8a3a', skin='c', eyes='shut', mouth='flat')
          + person('pc', 850, 1400, 1.0, coat='#e05a7a', skin='d', hair='tuft', eyes='happy', mouth='grin', flip=True))
    a = [arm('pa', 'r', .1, -70), arm('pa', 'l', .1, 70)] + sway('#set4', 0, D(4), 18, .7, 1.3, 1.2) + bob('pc', .8, D(4) - .8, 14, .2) + [arm('pc', 'r', .8, -150)]
    S.append(Shot(L(4), L(5), city_river() + g(rect(-400, 1300, 1900, 700, '#55607a', 0, 0) + rail + p3, 'set4'),
                  [(0, 1.5, 230, 1180), (1.1, 1.5, 540, 1180), (2.2, 1.5, 850, 1180), (D(4), 1.1, 540, 1150)], a))
    # 5 engineers check: steel fine, wind weak, bolts tight
    panel = g(rect(-330, -260, 660, 520, '#fdfcf8', 26, 10) + text(-60, -140, 'STEEL', 80, OUT, anchor='middle') + text(-60, 10, 'WIND', 80, OUT) + text(-60, 160, 'BOLTS', 80, OUT)
              + check('c0', 210, -165) + check('c1', 210, -15) + check('c2', 210, 135), 'pnl', 'translate(640,760)')
    st = L(5)
    a = [fromto('#pnl', 0, .4, {'opacity': 0, 'y': 200}, {'opacity': 1, 'y': 0}, 'back.out(2)')] + seq_show(['c0', 'c1', 'c2'], 1.1, .9) + talk('en', .2, D(5) - .4, rest='flat')
    S.append(Shot(L(5), L(6), wall('#3a4a7a') + floor_(1300) + pool(540, 1100, 520, 280) + panel + engineer('en', 230, 1500, 1.0),
                  [(0, 1.0, 540, 950), (1.3, 1.25, 640, 700), (2.6, 1.25, 640, 900), (D(5), 1.15, 400, 1100)], a))
    # 6 so why was it dancing? the bridge alone rocks, music notes, giant ?
    notes = ''.join(text(200 + k * 220, 760 - (k % 2) * 80, '♪', 130, WARM2, extra=f'id="nt{k}" opacity="0"') for k in range(4))
    a = sway('#deck', 0, D(6), 24, .5, 1.0, 1.5) + seq_show([f'nt{k}' for k in range(4)], .1, .25) + [fromto('#qm', .4, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    S.append(Shot(L(6), L(7), city_river() + footbridge('deck', 1080, 0) + notes + text(540, 600, '?', 300, WARM2, extra='id="qm" opacity="0"'),
                  [(0, 1.2, 540, 980), (D(6), 1.45, 540, 900)], a))
    # 7 shut down + the city's nickname: newspaper spins in
    a = [fromto('#np', .2, .7, {'rotation': -540, 'scale': .1, 'transformOrigin': '50% 50%'}, {'rotation': -4, 'scale': 1}, 'power3.out'), fromto('#np', 1.2, D(7) - 1.2, {'x': 0}, {'x': 0})]
    a += sway('#nph', 1.6, D(7) - 1.6, 10, .4, 1, 2)
    S.append(Shot(L(7), L(8), wall('#4a3a7a', 2400) + pool(540, 860, 640, 640) + g(newspaper('np', 540, 860, 'THE WOBBLY', 'BRIDGE'), 'nph'),
                  [(0, 1.0, 540, 900), (1.6, 1.3, 540, 760), (D(7), 1.15, 540, 900)], a))
    # 8 test with real people: a small crowd -> needle flat
    a = [fromto('#tg', 0, D(8), {'x': -200}, {'x': 120}, 'none')] + sum((bob(f't{i}', 0, D(8), 8, .3) for i in range(3)), []) + [needle('mt', .3, 0), needle('mt', 1.8, 4, .3)]
    S.append(Shot(L(8), L(9), city_river() + footbridge('deck', 1180, 0) + g(walkers('t', 3, 1180, 300, 700, .4, 4), 'tg') + meter('mt', 540, 760),
                  [(0, 1.1, 540, 1000), (1.3, 1.35, 540, 760), (D(8), 1.2, 540, 1080)], a))
    # 9 a bigger crowd... and suddenly it swings: needle to red, deck swings
    a = [fromto('#tg2', 0, D(9), {'x': -300}, {'x': 60}, 'none')] + sum((bob(f'u{i}', 0, D(9), 8, .3) for i in range(12)), []) + [needle('mt', .2, 30, .5), needle('mt', 1.3, 165, .4, 'elastic.out(1,.4)')]
    a += sway('#bigdeck', 1.2, D(9) - 1.2, 26, .6, 1.6, 1.4)
    S.append(Shot(L(9), L(10), city_river() + g(footbridge('deck2', 1180, 0) + g(walkers('u', 12, 1180, 40, 1040, .4, 5), 'tg2'), 'bigdeck') + meter('mt', 540, 760),
                  [(0, 1.0, 540, 1000), (1.2, 1.35, 540, 760), (D(9), 1.25, 540, 1100)], a))
    # 10 you see: the floor slides under you -> you spread your legs and sway, like on a boat
    flo = g(rect(-200, 1400, 1480, 120, grad('#9aa6c0', True), 10, 9) + ''.join(path(f'M{xx},1410 L{xx},1510', sw=6, stroke='#7a86a0') for xx in range(-160, 1300, 90)), 'flo')
    boat = g(path('M-160,0 L160,0 L120,70 L-120,70 Z', grad('#a8743c'), 7) + person('bp', 0, 0, .35, coat='#2f7a8a', skin='b', eyes='happy', mouth='grin') + path('M-260,80 Q-130,40 0,80 Q130,120 260,80', sw=8, stroke='#7fb0ff'), 'boat', 'translate(840,620)', 'opacity="0"')
    a = [fromto('#flo', 0, .4, {'x': 0}, {'x': 60})] + sway('#flo', .3, D(10) - .3, 60, .9, 1.0, 0) + sway('#me', .6, D(10) - .6, 30, .9, 1.0, -5)
    a += [arm('me', 'l', .9, 80), arm('me', 'r', .9, -80), face('me', .9, 'wide', 'o'), fromto('#boat', 3.6, .4, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(2)')]
    a += sway('#boat', 4.0, D(10) - 4.0, 12, .9, 1, 6)
    me = g(person('me', 0, 0, 1.3, coat='#4f7cc9', skin='a', hair='tuft', eyes='norm', mouth='smile'), 'mew', 'translate(380,1420)')
    S.append(Shot(L(10), L(11), wall('#3a3060', 2400) + pool(540, 1300, 640, 300) + flo + me + boat,
                  [(0, 1.0, 400, 1100), (1.5, 1.4, 380, 1250), (3.2, 1.0, 600, 900), (4.6, 1.3, 800, 700), (D(10), 1.05, 540, 1000)], a))
    # 11 thousands do it at the same time, in step -> every step pushes the bridge further (growing sway)
    rowp = ''.join(g(person(f'r{i}', 0, 0, .55, coat=['#4f7cc9', '#e05a7a', '#7a8a3a', '#c06a2a', '#3f5f9f', '#9a5ac9'][i % 6], skin='abcd'[i % 4], hair=['tuft', 'bob', None, 'bun'][i % 4], eyes='norm'), tr=f'translate({40 + i * 125},1240)') for i in range(9))
    a = []
    for i in range(9): a += sway(f'#r{i}', 0, D(11), 12, .8, 1.0, -6)
    a += sway('#deck3', .8, D(11) - .8, 12, .8, 3.2, .8)
    arrows = ''.join(g(path('M-60,0 L60,0 M30,-30 L60,0 L30,30', sw=14, stroke=WARM2), f'ar{k}', f'translate({240 + k * 300},1380)', 'opacity="0"') for k in range(3))
    a += [move(f'#ar{k}', 2.0 + k * .3, .2, opacity=1) for k in range(3)] + sway('#arg', 2.0, D(11) - 2.0, 30, .8, 1, 0)
    S.append(Shot(L(11), L(12), city_river() + g(footbridge('deck3x', 1240, 0) + rowp, 'deck3') + g(arrows, 'arg'),
                  [(0, 1.45, 300, 1100), (1.4, 1.45, 800, 1100), (2.8, 1.1, 540, 1050), (4.4, 1.3, 540, 1200), (D(11), 1.0, 540, 1000)], a))
    # 12 fix: almost 2 years + 5 million pounds of giant shock absorbers (welders, sparks)
    dmp = ''.join(damper(150 + k * 260, 1440, 1.0) for k in range(4))
    a = [fromto('#yrs', .2, .3, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'),
         fromto('#gbp', 2.0, .3, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')] + spark_burst('sp', .4, 12, 3, int(D(12) / .35) - 1)
    S.append(Shot(L(12), L(13), wall('#3a3060', 1300) + rect(-400, 1060, 1900, 60, grad('#9aa6c0', True), 0, 8) + dmp + floor_(1460) + person('wd', 680, 1700, .8, coat='#55606e', skin='b', hat='welder') + sparks('sp', 760, 1380)
                  + badge('yrs', 540, 560, '2 YEARS', '#ffd27a', 100) + badge('gbp', 540, 760, '£5,000,000', '#5fd36a', 100),
                  [(0, 1.1, 540, 900), (1.6, 1.3, 540, 700), (3.0, 1.25, 540, 1250), (D(12), 1.1, 540, 1100)], a))
    # 13 700 of their own staff march across: not a wobble
    a = [fromto('#mg', 0, D(13), {'x': -500}, {'x': 200}, 'none')] + sum((bob(f'm{i}', 0, D(13), 12, .25) for i in range(14)), [])
    a += [fromto('#n700', .6, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'), fromto('#ok2', 2.6, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    mar = ''.join(person(f'm{i}', -200 + i * 95, 1080, .3, coat='#e0702a', skin='abcd'[i % 4], hat='hard', eyes='happy', mouth='grin') for i in range(14))
    S.append(Shot(L(13), L(14), city_river() + footbridge('deck4', 1080, 0) + g(mar, 'mg') + text(540, 720, '700', 200, WARM2, extra='id="n700" opacity="0"') + check('ok2', 540, 900, 1.4),
                  [(0, 1.1, 300, 1000), (1.4, 1.35, 540, 1060), (D(13), 1.2, 540, 900)], a))
    # 14 payoff: the bridge was never the problem. The crowd was. (crowd looks guilty, spotlight)
    gl = ''.join(person(f'q{i}', 160 + i * 190, 1450, .75, coat=['#4f7cc9', '#e05a7a', '#7a8a3a', '#c06a2a', '#3f5f9f'][i], skin='abcd'[i % 4], hair=['tuft', 'bob', None, 'bun', 'tuft'][i], eyes='side', mouth='flat') for i in range(5))
    a = [fromto('#spot', D(14) * .45, .3, {'opacity': 0}, {'opacity': 1})] + [face(f'q{i}', D(14) * .5 + i * .08, 'wide', 'o') for i in range(5)]
    S.append(Shot(L(14), L(15), city_river() + rect(-400, 1200, 1900, 800, '#55607a', 0, 0) + footbridge('deck5', 1200, 0) + ell(540, 1300, 560, 300, 'url(#pool)', extra='id="spot" opacity="0"') + gl,
                  [(0, 1.0, 540, 900), (D(14) * .5, 1.35, 540, 1250), (D(14), 1.5, 540, 1250)], a))
    # 15 A/B
    S.append(Shot(L(15), total, outro('CROSS ON', 'DAY ONE', 'NO', 'WAY'), [(0, 1.0, 540, 950), (total - L(15), 1.12, 540, 1000)], outro_anims()))
    return S

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(15) - .3, 'flares': [(L(0) + 2.0, 'flare'), (L(3) + .8, 'shrink'), (L(6), 'flare'), (L(9) + 1.3, 'shrink'), (L(14) + 1.0, 'flare')]}

def audio():
    T = TOTAL; P = L(14)
    music = [('Monkeys_Spinning_Monkeys.mp3', 0, 0, L(3) + .2, 0, (.02, .4)),
             ('Hitman.mp3', 4, L(3) + .1, L(10) - .1, -1, (.2, .3)),
             ('Thinking_Music.mp3', 10, L(10), P - .4, -2, (.2, .2)),
             ('Wholesome.mp3', 5, P + .9, T, 0, (.05, 1.0))]
    O = '100-cc0-sfx/'; O2 = '100-cc0-sfx-2/sfx100v2_'; B = '75-cc0-breaking-falling-hit-sfx/bfh1_'; SW = 'swishes-sound-pack/swishes/swish-'
    sfx = [('crowd-shoutingspeaking-ambience/crowd_shouting.ogg', 0.0, -12, 2, 2.2),
           (SW + '3.wav', L(0) + 1.8, -4), (O + 'slam_03.ogg', L(0) + 2.15, 0), (B + 'metal_hit_01.ogg', L(0) + 2.2, -6), (O + 'bell_01.ogg', E(0) - 1.4, -9),
           (SW + '7.wav', L(1) - .1, -4), ('mild-wind-background-noise/wind background noise 2.wav', L(1), -12, 0, D(1)), (O + 'spring_02.ogg', L(1) + 1.5, -6),
           (SW + '2.wav', L(2) - .1, -4), ('crowd-shoutingspeaking-ambience/crowd_shouting.ogg', L(2), -5, 0, D(2)), ('applause-in-a-large-hall-or-church/applause-clapping-church-crowd-immersive.wav', L(2) + .8, -9, 1, 2.2)]
    sfx += [('footsteps-0/0%d-footstep.ogg' % (1 + k % 6), L(2) + .1 + k * .25, -10) for k in range(int(D(2) / .25))]
    sfx += [('tree-creaking/tree_creak.ogg', L(3) + .5, -2, 0, 3.0), ('wood-wobbling-rattling/montageAudio-20110719@161647.mp3', L(3) + 1.2, -4, 0, 2.2), (O + 'weird_03.ogg', L(3) + 1.7, -8)]
    sfx += [('group-giggling/group_giggling.ogg', L(4) + .9, -4, 0, 1.6), (B + 'metal_hit_02.ogg', L(4) + .1, -6), ('tree-creaking/tree_creak_0.ogg', L(4), -8, 0, 2.0),
            (O + 'paper_02.ogg', L(5) + .1, -4)]
    sfx += [(O + 'switch_01.ogg', L(5) + 1.1 + k * .9, -2) for k in range(3)]
    sfx += [('wood-wobbling-rattling/montageAudio-20110719@161647.mp3', L(6), -5, 2, 1.5), (O + 'spring_04.ogg', L(6) + .4, -5),
            ('air-whoosh/whoosh2_0.wav', L(7) + .15, -2), (O + 'paper_01.ogg', L(7) + .85, -1),
            ('footsteps-0/02-footstep.ogg', L(8) + .2, -8), ('footsteps-0/03-footstep.ogg', L(8) + .7, -8), ('footsteps-0/04-footstep.ogg', L(8) + 1.2, -8), (O + 'switch_02.ogg', L(8) + .3, -6),
            ('crowd-shoutingspeaking-ambience/crowd_shouting.ogg', L(9), -9, 4, D(9)), (O + 'spring_07.ogg', L(9) + 1.3, -2), ('tree-creaking/tree_creak.ogg', L(9) + 1.2, -2, 1, 2.2),
            (SW + '9.wav', L(10) - .1, -4), (O + 'wooden_02.ogg', L(10) + .3, -5), ('water-waves/wave_01_cc0-11505__transitking__wavesound.flac', L(10) + 3.6, -6, 0, 2.6)]
    sfx += [('footsteps-0/0%d-footstep.ogg' % (1 + k % 6), L(11) + .1 + k * .4, -5) for k in range(int(D(11) / .4))]
    sfx += [('tree-creaking/tree_creak_0.ogg', L(11) + 2.0, -3, 0, 2.5),
            (SW + '5.wav', L(12) - .1, -4), (O + 'metal_09.ogg', L(12) + .25, -3), (O + 'tools_04.ogg', L(12) + .8, -4), (O + 'tools_05.ogg', L(12) + 1.6, -4),
            ('fire-crackling/fire-1.ogg', L(12) + .4, -9, 0, D(12) - .5), ('100-cc0-sfx/bell_02.ogg', L(12) + 2.0, -6)]
    sfx += [('metal-footsteps-on-concrete/metal_steps.ogg', L(13), -5, 0, D(13)), (O + 'bell_03.ogg', L(13) + 2.6, -7),
            ('muffled-distant-explosion/NenadSimic - Muffled Distant Explosion.wav', P - .1, -2, 0, 1.6), ('do-you-remember-laughter/ogalaughter_2.ogg', P + 1.5, -7, 22.5, 1.6),
            (SW + '4.wav', L(15) - .05, -3), ('fire-crackling/fire-1.ogg', L(15) + .1, -6, 0, 1.2), (O2 + 'air_01.ogg', T - 1.0, -1)]
    return music, sfx

def build_tt(): return None

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mix':
        from mix import mix
        mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
    else: print(build(EP), TOTAL)
