import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *

SLUG = '2026-11-16-robber-trusted-lemon-juice'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.3, 2)
def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']

JUICE = '<rect x="-82" y="-300" width="164" height="190" rx="70" fill="#ffe34a" opacity=".32"/>'
def robber(pid, x, y, s=1, eyes='side', mouth='smirk', juice=True, flip=False):
    return person(pid, x, y, s, coat='#2f7a8a', skin='d', hat='beanie', eyes=eyes, mouth=mouth, flip=flip,
                  extra_acc=(JUICE + ell(-50, -150, 8, 12, '#ffe34a', 4) + ell(56, -130, 7, 10, '#ffe34a', 4)) if juice else '')
def cop(pid, x, y, s=1, eyes='norm', mouth='flat', flip=False):
    return person(pid, x, y, s, coat='#2f4f9a', skin='b', hat='cap', eyes=eyes, mouth=mouth, mustache=True, flip=flip)

def kitchen():
    return (wall('#6a4a8a') + window_(620, 260, 340, 460) + floor_(1250) + lamp(200, 760)
            + rect(60, 1080, 960, 50, grad('#8a5a3c'), 10, 8) + rect(100, 1130, 40, 200, shade('#8a5a3c'), 4, 6) + rect(940, 1130, 40, 200, shade('#8a5a3c'), 4, 6)
            + lemon(300, 1040, .8) + lemon(420, 1050, .7, 30) + lemon(820, 1040, .8, -20) + g(path('M-40,0 L40,0 L30,-60 L-30,-60 Z', grad('#bfe0ff'), 7), tr='translate(660,1080)'))

def bank(col='#3f6a5a', label='BANK'):
    cam = g(rect(-70, -40, 140, 80, grad('#d0d4e0'), 14, 8) + rect(60, -26, 40, 52, grad('#a0a4b0'), 6, 7) + ell(-80, 0, 30, 30, '#202030', 7)
            + ell(-80, 0, 12, 12, '#7fd0ff') + ell(40, -24, 10, 10, '#ff3a3a', 0, 'id="rec"') + path('M60,30 L120,120', sw=12), 'scam', 'translate(820,330) rotate(15)')
    return (wall(col) + floor_(1250) + rect(-400, 300, W + 800, 30, shade(col, .3), 0, 0)
            + text(540, 250, label, 110, WARM2) + rect(-100, 980, 1280, 300, grad('#8a5a3c', True), 0, 9)
            + rect(80, 600, 300, 380, '#1c1538', 10, 8) + rect(700, 600, 300, 380, '#1c1538', 10, 8) + pool(540, 1100, 520, 220) + cam)

def tv_room(face=True, label='11 PM NEWS'):
    scr = rect(140, 420, 800, 600, '#1c2a4a', 30, 14)
    if face:
        scr += g(robber('tvr', 540, 1010, 1.25, eyes='norm', mouth='smile', juice=False), tr='') + rect(140, 900, 800, 120, '#e05a5a', 0, 0) + text(540, 985, label, 70)
    return (wall('#4a3a7a') + floor_(1300) + rect(100, 380, 880, 680, grad('#3a3048'), 40, 12) + scr + rect(400, 1060, 280, 60, grad('#3a3048'), 10, 8)
            + rect(-60, 1300, 1200, 400, '#2a2050', 0, 0) + rect(140, 1180, 800, 200, grad('#c95f5a', True), 60, 9) + pool(540, 740, 600, 500))

def station():
    phones = ''.join(g(rect(-80, -40, 160, 80, grad('#e05a5a'), 18, 8) + path('M-70,-50 Q0,-110 70,-50', sw=22) + ell(0, 0, 22, 22, '#fff', 5), f'p{i}', f'translate({x},{y})')
                     for i, (x, y) in enumerate([(200, 1000), (540, 960), (880, 1000), (360, 1150), (720, 1150)]))
    return wall('#3a4a7a') + floor_(1250) + rect(40, 1040, 1000, 300, grad('#8a5a3c', True), 14, 9) + phones + text(540, 380, 'POLICE', 120, '#9fc8ff') + pool(540, 1000, 600, 300)

def door_scene():
    return (wall('#5a3a6a') + floor_(1300) + rect(300, 420, 480, 880, grad('#8a4a2a'), 14, 10) + ell(720, 880, 22, 22, '#e0b040', 6)
            + rect(330, 450, 420, 360, shade('#8a4a2a', .2), 10, 6) + rect(330, 860, 420, 400, shade('#8a4a2a', .2), 10, 6)
            + rect(-400, -400, W + 800, H + 800, '#ff2a4a', sw=0, extra='id="red" opacity="0"') + rect(-400, -400, W + 800, H + 800, '#2a6aff', sw=0, extra='id="blue" opacity="0"'))

def classroom(board_lines=(), chart=False):
    b = rect(90, 260, 900, 640, grad('#2d5a4a'), 20, 12) + rect(70, 900, 940, 30, grad('#a0704a'), 8, 7)
    for k, t in enumerate(board_lines): b += text(540, 400 + k * 140, t, 92, '#f4f4e8', extra=f'id="bl{k}" opacity="0"')
    if chart:
        b += path('M180,840 L180,320 M180,840 L920,840', sw=8, stroke='#f4f4e8')
        b += g(rect(260, -150, 220, 150, '#ff8a5a', 10, 6), 'bar1', 'translate(0,840)') + g(rect(600, -420, 220, 420, '#ffd27a', 10, 6), 'bar2', 'translate(0,840)')
        b += text(370, 880 - 40, '', 1) + text(370, 640, 'REAL', 60, '#fff') + text(710, 380, 'THEY THINK', 56, '#fff')
    return wall('#4a3a6a') + floor_(1250) + b + pool(540, 1100, 520, 220)

def photo_card(blank=True):
    inner = rect(-200, -230, 400, 380, '#cfc6b8' if blank else '#ffe34a', 4, 0) + (path('M-200,60 L200,60', sw=4, stroke='#a8a090') + ell(80, -120, 60, 30, '#fffbe0', extra='opacity=".8"') if blank else '')
    return g(rect(-240, -270, 480, 560, '#fdfcf8', 14, 9) + inner, 'card', 'translate(540,820)')

def outro():
    return (sky(moon=False) + floor_(1300) + pool(540, 1300, 600, 260)
            + candle('ca', 300, 900, 1.15, 'A', face='happy') + candle('cb', 780, 900, 1.15, 'B', face='smirk')
            + text(300, 570, 'TRUST', 64) + text(300, 650, 'THE PHOTO', 64) + text(780, 570, 'TEST IT', 64) + text(780, 650, 'TWICE', 64))

def shots(lines, total):
    S = []
    # 0 hook: robber at bank counter, no mask, face glowing with lemon juice, waving at camera
    a = [arm('rb', 'r', .3, -150), face('rb', 1.8, 'side', 'grin')] + bob('rb', 0, 4, 8, .4) + [move('#rec', i * .5, .25, opacity=(0 if i % 2 else 1)) for i in range(8)]
    S.append(Shot(0, L(1), bank() + robber('rb', 540, 1300, 1.25) + lemon(820, 1180, .9, 20), [(0, 1.6, 540, 1000), (1.4, 1.25, 600, 900), (E(0) - .2, 1.55, 540, 1010)], a))
    # 1 friend tells the secret
    fr = person('fr', 300, 1320, 1.0, coat='#7a8a3a', skin='c', hair='tuft', eyes='side', mouth='smile')
    rb = robber('r1', 760, 1320, 1.0, juice=False, eyes='wide', mouth='o', flip=True)
    a = talk('fr', .1, 3.0) + [arm('fr', 'r', .2, -120), face('r1', 1.5, 'happy', 'grin'), arm('r1', 'l', 2.2, 160)] + bob('r1', 1.5, 3, 8, .35)
    S.append(Shot(L(1), L(2), kitchen() + fr + rb, [(0, 1.15, 380, 1000), (2.3, 1.35, 660, 990), (E(1) - L(1), 1.2, 540, 1000)], a))
    # 2 tests it: squeezes lemon on face + instant photo
    a = [arm('r2', 'l', .2, 150), arm('r2', 'r', .2, -150), fromto('#jz', .3, .8, {'opacity': 0}, {'opacity': 1}), face('r2', .9, 'shut', 'grin'),
         arm('r2', 'r', 1.8, -95), setp('#flash', 2.45, opacity=1), move('#flash', 2.5, .4, opacity=0)]
    S.append(Shot(L(2), L(3), kitchen() + robber('r2', 540, 1320, 1.2, juice=False) + g(JUICE, 'jz', 'translate(540,1320) scale(1.2)', 'opacity="0"')
                  + g(rect(-60, -40, 120, 80, grad('#d8d8e0'), 12, 7) + ell(0, 0, 26, 26, '#202030', 6), 'cm', 'translate(720,950)')
                  + rect(-400, -400, W + 800, H + 800, '#ffffff', sw=0, extra='id="flash" opacity="0"'),
                  [(0, 1.2, 540, 1000), (1.5, 1.45, 540, 960), (E(2) - L(2), 1.3, 620, 960)], a))
    # 3 the photo comes out: his face is not there
    a = [fromto('#card', 0, .8, {'y': 300, 'rotation': -8}, {'y': 0, 'rotation': 3}, 'back.out(1.5)'), fromto('#qm', .9, .3, {'scale': 0, 'transformOrigin': '50% 50%'}, {'scale': 1}, 'back.out(3)')]
    S.append(Shot(L(3), L(4), wall('#6a4a8a', 2400) + pool(540, 820, 600, 600) + photo_card() + text(540, 1250, '?', 240, WARM2, extra='id="qm"'),
                  [(0, 1.0, 540, 900), (E(3) - L(3), 1.35, 540, 820)], a))
    # 4 proof! (camera was aimed at the ceiling) - robber celebrates
    a = [arm('r3', 'l', 0, 160), arm('r3', 'r', 0, -160), face('r3', 0, 'happy', 'grin')] + bob('r3', 0, 2.8, 22, .25) + [fromto('#ceil', 1.0, .5, {'opacity': 0}, {'opacity': 1})]
    ceil = g(rect(140, 120, 800, 120, '#e8e0d0', 10, 8) + ell(540, 250, 50, 30, WARM2, 6) + path('M540,300 L720,560', sw=8, stroke='#ffe34a', extra='stroke-dasharray="20 18"'), 'ceil')
    S.append(Shot(L(4), L(5), kitchen() + robber('r3', 540, 1320, 1.15) + ceil, [(0, 1.3, 540, 980), (1.1, 1.0, 540, 800), (E(4) - L(4), 1.1, 540, 900)], a))
    # 5 walks into the bank, stares into the camera
    a = [fromto('#r4', 0, 1.6, {'x': -500}, {'x': 0}, 'power2.out')] + bob('r4', 0, 1.6, 14, .2) + [face('r4', 1.8, 'side', 'smirk'), arm('r4', 'r', 2.2, -160)]
    a += [move('#rec', i * .5, .25, opacity=(0 if i % 2 else 1)) for i in range(7)]
    S.append(Shot(L(5), L(6), bank() + robber('r4', 540, 1300, 1.0), [(0, 1.0, 540, 900), (1.8, 1.3, 700, 650), (E(5) - L(5), 1.4, 640, 800)], a))
    # 6 takes the money, walks out
    bag = g(path('M-60,0 Q-80,-120 0,-130 Q80,-120 60,0 Z', grad('#c8b090'), 8) + text(0, -40, '$', 90, '#3a7a3a'), 'bag', 'translate(700,1180)')
    teller = person('tl', 540, 1100, .8, coat='#c95f9a', skin='a', hair='bun', eyes='wide', mouth='o')
    a = [fromto('#bag', 0, .3, {'y': -200}, {'y': 0}, 'bounce.out'), move('#r5', .6, .9, 'power1.in', x=900)] + bob('r5', .6, .9, 14, .15)
    S.append(Shot(L(6), L(7), bank() + teller + robber('r5', 540, 1320, 1.1, mouth='grin') + bag, [(0, 1.3, 600, 1050), (E(6) - L(6), 1.1, 700, 1000)], a + [move('#bag', .6, .9, 'power1.in', x=900)]))
    # 7 second bank, same face, same camera, 'still invisible... he thinks'
    a = [arm('r6', 'r', .4, -160), face('r6', 1.0, 'side', 'grin')] + bob('r6', 0, 3, 8, .35) + [move('#rec', i * .5, .25, opacity=(0 if i % 2 else 1)) for i in range(7)]
    S.append(Shot(L(7), L(8), bank('#7a4a5a', 'BANK #2') + robber('r6', 540, 1300, 1.15), [(0, 1.0, 540, 900), (1.4, 1.3, 700, 650), (2.6, 1.4, 540, 1000)], a))
    # 8 eleven o'clock news: his face crystal clear
    a = [fromto('#tvr', 0, .4, {'scale': .6, 'transformOrigin': '50% 100%'}, {'scale': 1}, 'back.out(2)')]
    S.append(Shot(L(8), L(9), tv_room(), [(0, 1.0, 540, 800), (E(8) - L(8), 1.4, 540, 720)], a))
    # 9 phones at the station ring
    a = []
    for i in range(5):
        for k in range(8): a.append((.1 + i * .15 + k * .2, f'tl.to("#p{i}",{{rotation:{8 if k % 2 else -8},duration:.1,transformOrigin:"50% 50%"}},{{T}});'))
    S.append(Shot(L(9), L(10), station(), [(0, 1.0, 540, 900), (E(9) - L(9), 1.25, 540, 1000)], a))
    # 10 police knock on his door
    a = [(.3 + k * .3, f'tl.fromTo("#dr",{{x:0}},{{x:{-10 if k % 2 else 10},duration:.08,yoyo:true,repeat:1}},{{T}});') for k in range(3)]
    a += [setp('#red', .2 + k * .5, opacity=(.25 if k % 2 == 0 else 0)) for k in range(5)] + [setp('#blue', .45 + k * .5, opacity=(.25 if k % 2 == 0 else 0)) for k in range(5)]
    S.append(Shot(L(10), L(11), g(door_scene(), 'dr') + cop('cp', 900, 1450, 1.0, flip=True), [(0, 1.0, 540, 900), (1.0, 1.25, 600, 900), (E(10) - L(10), 1.1, 700, 1000)], a + [arm('cp', 'r', .2, -100)]))
    # 11 they show him the tape; 12 'But I wore the juice!'
    tape = g(rect(-200, -150, 400, 300, '#1c2a4a', 20, 10) + g(robber('tv2', 0, 140, .7, eyes='norm', mouth='smile', juice=False)), 'tape', 'translate(320,760)')
    a = [fromto('#tape', 0, .4, {'scale': .3, 'transformOrigin': '50% 50%'}, {'scale': 1}, 'back.out(2)'), face('r7', .8, 'wide', 'o'), face('r7', L(12) - L(11), 'wide', 'open'),
         arm('r7', 'l', L(12) - L(11), 170), arm('r7', 'r', L(12) - L(11), -170)] + bob('r7', L(12) - L(11), 1.2, 10, .12)
    S.append(Shot(L(11), L(13), wall('#3a3a5a') + floor_(1250) + pool(540, 1000, 500, 300) + tape + cop('c2', 160, 1350, .9) + robber('r7', 720, 1350, 1.15, eyes='norm', mouth='flat', flip=True),
                  [(0, 1.0, 460, 900), (L(12) - L(11), 1.7, 720, 1010), (E(12) - L(11) + .3, 1.85, 720, 1000)], a))
    # 13 he wasn't lying; he didn't know enough to know he was wrong (thought bubble with a lemon = invisibility cloak)
    bub = g(ell(0, 0, 260, 170, '#fdfcf8', 9) + ell(-200, 190, 30, 30, '#fdfcf8', 7) + ell(-250, 250, 18, 18, '#fdfcf8', 6) + lemon(-60, 0, .9) + path('M70,-10 L150,-10 M70,30 L150,30', sw=14) + text(200, 40, '?', 120, '#7fb0ff'), 'bub', 'translate(620,520)')
    a = [fromto('#bub', .2, .4, {'scale': 0, 'transformOrigin': '0% 100%'}, {'scale': 1}, 'back.out(2)'), face('r8', 1.5, 'happy', 'smile')] + bob('r8', 0, 3.5, 6, .5)
    S.append(Shot(L(13), L(14), wall('#4a3a7a') + floor_(1250) + pool(540, 1100, 500, 260) + robber('r8', 380, 1350, 1.2, eyes='norm', mouth='smile') + bub,
                  [(0, 1.0, 540, 900), (E(13) - L(13), 1.2, 480, 860)], a))
    # 14 twist: a professor reads about it, tests students on jokes, grammar, logic
    prof = person('pf', 840, 1320, 1.0, coat='#6a4a3a', skin='a', glasses=True, hair='tuft', eyes='norm', mouth='smile', flip=True)
    paper = g(rect(-150, -100, 300, 200, '#fdfcf8', 8, 7) + text(0, -40, 'NEWS', 50, OUT) + rect(-110, -10, 90, 80, '#ffe34a', 6, 5) + path('M10,0 L120,0 M10,30 L120,30 M10,60 L100,60', sw=6), 'np', 'translate(780,960)')
    studs = ''.join(person(f'u{i}', 140 + i * 160, 1500, .55, coat=['#4f7cc9', '#e05a7a', '#7a8a3a', '#c06a2a'][i], skin='abcd'[i], hair=['tuft', 'bob', None, 'bun'][i]) for i in range(4))
    t1 = L(14) + 1.6
    a = [fromto('#np', 0, .4, {'y': 200, 'opacity': 0}, {'y': 0, 'opacity': 1}), face('pf', 1.0, 'wide', 'o'), move('#np', 2.2, .3, opacity=0)]
    a += [fromto(f'#bl{k}', 3.4 + k * .6, .25, {'opacity': 0, 'scale': .5, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)') for k in range(3)]
    S.append(Shot(L(14), L(15), classroom(('JOKES', 'GRAMMAR', 'LOGIC')) + prof + paper + studs, [(0, 1.4, 780, 960), (2.3, 1.0, 540, 900), (E(14) - L(14), 1.15, 540, 760)], a))
    # 15 the worst scorers were sure they were above average: two bars
    a = [fromto('#bar1', .2, .5, {'scaleY': 0, 'transformOrigin': '50% 100%'}, {'scaleY': 1}), fromto('#bar2', 1.0, .9, {'scaleY': 0, 'transformOrigin': '50% 100%'}, {'scaleY': 1}, 'power3.out')]
    S.append(Shot(L(15), L(16), classroom(chart=True) + robber('r9', 900, 1400, .8, eyes='happy', mouth='grin', flip=True), [(0, 1.0, 540, 700), (E(15) - L(15), 1.25, 560, 640)], a))
    # 16 the name
    a = [fromto('#bl0', .5, .3, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'),
         fromto('#bl1', .8, .3, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'),
         fromto('#bl2', 1.1, .3, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    S.append(Shot(L(16), L(17), classroom(('DUNNING-', 'KRUGER', 'EFFECT')) + prof.replace('pf', 'pg'), [(0, 1.2, 540, 600), (E(16) - L(16), 1.05, 540, 700)], a))
    # 17 the robber who thought he was invisible became a classroom legend (his juice face on the slide)
    slide = g(rect(-300, -220, 600, 440, '#fdfcf8', 16, 10) + g(robber('sl', 0, 200, .75, eyes='side', mouth='smirk')), 'sld', 'translate(540,600)')
    studs2 = ''.join(person(f'w{i}', 120 + i * 210, 1450, .6, coat=['#4f7cc9', '#e05a7a', '#7a8a3a', '#c06a2a', '#3f5f9f'][i], skin='abcd'[i % 4], hair=['tuft', 'bob', None, 'bun', 'tuft'][i], eyes='happy', mouth='grin') for i in range(5))
    a = [fromto('#sld', 0, .5, {'scale': .5, 'transformOrigin': '50% 50%', 'opacity': 0}, {'scale': 1, 'opacity': 1}, 'back.out(2)')] + sum((bob(f'w{i}', 1.6 + i * .05, 2.2, 10, .22) for i in range(5)), [])
    S.append(Shot(L(17), L(18), wall('#3a3060') + floor_(1250) + pool(540, 600, 500, 400) + slide + studs2, [(0, 1.5, 540, 640), (E(17) - L(17), 1.0, 540, 950)], a))
    # 18 A/B candles
    a = [fromto('#ca', 0, .4, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'), fromto('#cb', .2, .4, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'),
         move('#ca-flame', 1.0, .2, scale=1.4, transformOrigin='50% 100%'), move('#ca-flame', 1.2, .3, scale=1), move('#cb-flame', 1.8, .2, scale=1.4, transformOrigin='50% 100%'), move('#cb-flame', 2.0, .3, scale=1)]
    S.append(Shot(L(18), total, outro(), [(0, 1.0, 540, 950), (total - L(18), 1.12, 540, 1000)], a))
    return S

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(18) - .3, 'flares': [(L(3) + .6, 'flare'), (L(10), 'shrink'), (L(12), 'flare'), (L(16), 'flare')]}

def audio():
    T = TOTAL; P = L(12)
    music = [('sneaky.mp3', 0, 0, L(8) - .1, 1, (.02, .3)),
             ('volatile.mp3', 20, L(8) - .1, P - .35, -2, (.15, .2)),
             ('duck.mp3', 0, P + 1.0, L(18), 0, (.05, .6)),
             ('carefree.mp3', 30, L(18) - .2, T, -1, (.3, 1.0))]
    O = '100-cc0-sfx-2/sfx100v2_'
    sfx = [('whoosh-short.mp3', 0.05, -3), ('202-more-sound-effects/Money/' + 'Money_01.wav', 1.6, -3),
           ('whoosh-cinematic.mp3', L(1) - .15, -3), ('8-wet-squish-slurp-impacts/im.mp3', L(2) + .3, -2, 0, .7), ('8-wet-squish-slurp-impacts/im.mp3', L(2) + .8, -3, 1.0, .7),
           ('camera/photo.ogg', L(2) + 2.35, 0), ('202-more-sound-effects/Camera/Camera_02.wav', L(3) - .1, -2),
           ('impact-bass-2.mp3', L(3) + .85, -4), ('100-cc0-sfx/spring_02.ogg', L(4) + .1, -3),
           ('100-cc0-sfx/door_open.ogg', L(5) - .05, -3)]
    sfx += [('sound-effects-pack/Footsteps/hard-footstep' + str(1 + k % 2) + '.wav', L(5) + .1 + k * .2, -7) for k in range(7)]
    sfx += [('100-cc0-sfx-2/sfx100v2_switch_01.ogg', L(5) + 1.85, -4), ('202-more-sound-effects/Money/Money_02.wav', L(6) + .1, -2), ('100-cc0-sfx/door_close_02.ogg', L(6) + 1.3, -3),
            ('whoosh.mp3', L(7) - .1, -3), ('100-cc0-sfx/door_open.ogg', L(7) + .1, -5),
            ('static/ScatterNoise1.mp3', L(8) - .1, -6, 2, .4), ('impact-bass-1.mp3', L(8) + .1, -4),
            ('crank-movie-telephone-ringtone/crank_ringtone.mp3', L(9), -2, 0, 1.7), ('crank-movie-telephone-ringtone/crank_ringtone.mp3', L(9) + .4, -6, .5, 1.2),
            ('202-more-sound-effects/Keys, Locks, Door/Key_Lock_Door_40.wav', L(10) + .3, 0), ('202-more-sound-effects/Keys, Locks, Door/Key_Lock_Door_40.wav', L(10) + .6, 0),
            ('202-more-sound-effects/Keys, Locks, Door/Key_Lock_Door_40.wav', L(10) + .9, 0), ('storm-siren/storm_3_siren.mp3', L(10) + .2, -10, 30, 2.0),
            ('whoosh-short.mp3', L(11) - .05, -4), ('static/ScatterNoise1.mp3', L(11) + .1, -10, 5, .5),
            ('impact-bass-2.mp3', P - .05, 0), ('do-you-remember-laughter/ogalaughter_2.ogg', E(12) + .05, -5, 22.5, 1.8),
            ('100-cc0-sfx/plop_02.ogg', L(13) + .2, -3), ('100-cc0-sfx/paper_02.ogg', L(14) + .05, -2), ('whoosh-short.mp3', L(14) + 2.2, -4)]
    sfx += [('202-more-sound-effects/Paper & Stationery/' + 'Stationery_0%d.wav' % (k + 1), L(14) + 3.4 + k * .6, -3) for k in range(3)]
    sfx += [('100-cc0-sfx/spring_04.ogg', L(15) + .2, -4), ('riser.mp3', L(15) + .8, -10, 7.5, 1.4), ('impact-bass-1.mp3', L(16) + .45, -2),
            ('whoosh.mp3', L(17) - .05, -3), ('applause-in-a-large-hall-or-church/applause-clapping-church-crowd-immersive.wav', L(17) + 1.5, -8, 2, 2.5),
            ('whoosh.mp3', L(18) - .05, -3), ('fire-crackling/fire-1.ogg', L(18) + .1, -6, 0, 1.2), (O + 'air_01.ogg', T - 1.0, -1)]
    return music, sfx

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mix':
        from mix import mix
        mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
    else: print(build(EP), TOTAL)

def build_tt():
    """TikTok-only file: different first 2.4 s (tight lemon close-up + a question banner), rest identical, re-encoded."""
    def shots_tt(lines, total):
        S = shots(lines, total)
        S[0].cam = [(0, 2.4, 820, 1150), (1.2, 2.0, 700, 1080), (2.4, 1.3, 600, 950), (E(0) - .2, 1.55, 540, 1010)]
        return S
    ov = ('<div id="ttq" class="clip" data-start="0" data-duration="2.4" data-track-index="5" style="position:absolute;left:0;top:300px;width:1080px;text-align:center;z-index:960">'
          '<span style="display:inline-block;font-family:Montserrat;font-weight:900;font-size:76px;line-height:1.05;color:#140c26;background:#ffe34a;padding:18px 34px;border-radius:26px;border:8px solid #140c26">'
          'HE THOUGHT LEMON JUICE<br>MADE HIM INVISIBLE</span></div>')
    js = 'tl.fromTo("#ttq span",{scale:.6,rotation:-4},{scale:1,rotation:-2,duration:.25,ease:"back.out(3)"},0.05);'
    return build(dict(EP, shots=shots_tt, hfdir='hf_tt', overlay=ov, overlay_js=js))

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'tt':
    print(build_tt())
