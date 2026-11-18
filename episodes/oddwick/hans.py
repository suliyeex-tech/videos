import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *
from props2 import *

SLUG = '2026-11-18-this-horse-fooled-every-scientist'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.3, 2)
def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']
def D(i): return L(i + 1) - L(i)

def teacher(pid, x, y, s=1, eyes='norm', mouth='smile', flip=False):
    return person(pid, x, y, s, coat='#5a3a7a', skin='a', mustache=True, glasses=False, eyes=eyes, mouth=mouth, flip=flip,
                  extra_acc=path('M-60,-310 Q0,-345 60,-310 L60,-290 L-60,-290 Z', '#e8e8e8', 6))   # white hair band
def mocker(pid, x, y, s=1, eyes='side', mouth='smirk', flip=False):
    return person(pid, x, y, s, coat='#2f4f4a', skin='d', glasses=True, eyes=eyes, mouth=mouth, flip=flip, extra_acc=tophat(-300))
def young(pid, x, y, s=1, eyes='norm', mouth='smile', flip=False):
    book = g(rect(-50, -70, 100, 130, '#e8d8a0', 8, 6) + path('M-30,-30 L30,-30 M-30,0 L30,0', sw=5), tr='translate(-110,-120)')
    return person(pid, x, y, s, coat='#3f6fb0', skin='b', hair='tuft', eyes=eyes, mouth=mouth, flip=flip, extra_acc=book)

def counter(prefix, n, x, y, size=220, start=1):
    return ''.join(text(x, y, str(start + k), size, WARM2, extra=f'id="{prefix}{k}" opacity="0"') for k in range(n))

def shots(lines, total):
    S = []
    # 0 hook: blackboard 3+2, Hans taps 5 times, the count pops 1..5
    t0 = E(0) - 2.0
    a = [fromto('#bq', .3, .3, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')] + taps('hs', t0, 5, .36) + flash_seq([f'k{k}' for k in range(5)], t0 + .1, .36)
    a += [setp('#hs-e-norm', E(0) - .1, opacity=0), setp('#hs-e-side', E(0) - .1, opacity=1)]
    S.append(Shot(0, L(1), yard() + blackboard(300, 760, 440, 300, ['3 + 2'], 120, ['bq']) + horse('hs', 600, 1420, 1.15) + counter('k', 5, 840, 760, 260),
                  [(0, 1.2, 540, 1020), (1.5, 1.25, 420, 900), (t0, 1.3, 700, 1150), (D(0), 1.4, 760, 1080)], a))
    # 1 owner = maths teacher: board with numbers, words, the calendar
    a = [arm('tc', 'r', .2, -130)] + talk('tc', .2, 1.2) + seq_show(['b0', 'b1', 'b2'], 1.2, .7) + [nod('hs', 1.4), nod('hs', 2.2)]
    S.append(Shot(L(1), L(2), yard() + blackboard(540, 680, 760, 520, ['1 2 3 4', 'HAUS  BROT', 'MON TUE WED'], 96, ['b0', 'b1', 'b2'])
                  + teacher('tc', 250, 1450, 1.0) + horse('hs', 720, 1460, .95),
                  [(0, 1.15, 300, 1150), (1.4, 1.05, 540, 640), (D(1), 1.15, 680, 1100)], a))
    # 2 crowds every day: banner CLEVER HANS, crowd bobbing behind the fence
    cr = ''.join(person(f'c{i}', 60 + i * 120, 1230, .55, coat=['#4f7cc9', '#e05a7a', '#7a8a3a', '#c06a2a', '#3f5f9f', '#9a5ac9'][i % 6], skin='abcd'[i % 4], hair=['tuft', 'bob', None, 'bun'][i % 4], eyes='happy', mouth='grin') for i in range(9))
    ban = g(path('M-420,0 Q0,60 420,0 L420,120 Q0,180 -420,120 Z', grad('#c0404a'), 8) + text(0, 100, 'CLEVER HANS', 92, WARM2), 'ban', 'translate(540,430)')
    a = sum((bob(f'c{i}', i * .05, D(2), 10, .3) for i in range(9)), []) + [fromto('#ban', 0, .5, {'y': -400}, {'y': 0}, 'bounce.out'), nod('hs', .8)]
    S.append(Shot(L(2), L(3), yard() + cr + horse('hs', 540, 1520, .9) + ban, [(0, 1.0, 540, 900), (D(2), 1.25, 540, 1150)], a))
    # 3 mocker close-up: 'Next you'll tell me he pays taxes'
    a = talk('mk', .05, D(3) - .5, .13, rest='smirk') + [arm('mk', 'r', .3, -140), arm('mk', 'r', 1.6, -40)]
    tax = g(rect(-130, -90, 260, 180, '#fdfcf8', 10, 7) + text(0, 30, 'TAX', 80, OUT), 'tax', 'translate(820,640)', 'opacity="0"')
    S.append(Shot(L(3), L(4), wall('#2f3a5a', 2400) + pool(540, 1100, 600, 500) + mocker('mk', 470, 1700, 2.0) + tax,
                  [(0, 1.0, 470, 1100), (1.5, 1.25, 520, 1000), (D(3), 1.35, 560, 960)], a + [fromto('#tax', D(3) - 1.4, .3, {'opacity': 0, 'rotation': -20, 'scale': .3}, {'opacity': 1, 'rotation': 8, 'scale': 1}, 'back.out(3)')]))
    # 4 the teacher just smiles: 'Ask him yourself' (calm, gestures to Hans)
    a = [face('tc', .1, 'happy', 'smile'), arm('tc', 'r', .5, -100)] + talk('tc', 1.0, D(4) - 1.2) + [nod('hs', 1.4)]
    S.append(Shot(L(4), L(5), yard() + teacher('tc', 330, 1460, 1.15) + horse('hs', 820, 1480, .85), [(0, 1.3, 330, 1100), (D(4), 1.15, 600, 1150)], a))
    # 5 the 13 experts: vet, circus boss, army officer, teachers
    hats = ['cap', 'helmet', None, 'campaign', None, 'beanie', None, 'cap', None, 'hard', None, 'helmet', None]
    ex = ''.join(person(f'x{i}', 60 + i * 80, 1250 + (i % 2) * 120, .55, coat=['#4f7cc9', '#c06a2a', '#3f5f9f', '#6a7a3a', '#9a5ac9'][i % 5], skin='abcd'[i % 4], hat=hats[i], mustache=i % 3 == 0, glasses=i % 4 == 1, eyes='norm', mouth='flat') for i in range(13))
    a = [fromto('#xg', 0, .9, {'x': -900}, {'x': 0}, 'power2.out')] + sum((bob(f'x{i}', 0, .9, 8, .15) for i in range(13)), []) + [fromto('#n13', 1.0, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'), setp('#n13', 2.8, opacity=0)]
    S.append(Shot(L(5), L(6), yard() + g(ex, 'xg') + text(540, 800, '13 EXPERTS', 110, WARM2, extra='id="n13" opacity="0"'),
                  [(0, 1.0, 540, 1050), (1.5, 1.05, 540, 1000), (3.0, 1.3, 300, 1200), (D(5), 1.3, 800, 1200)], a))
    # 6 looking for strings, secret signals, tricks: magnifier sweeps, 3 crosses
    mag = g(ell(0, 0, 110, 110, '#bfe0ff', 12, 'fill-opacity=".35"') + path('M78,78 L190,190', sw=30), 'mag', 'translate(300,1000)')
    a = [move('#mag', .1, .8, x=300, y=-120), move('#mag', .9, .8, x=520, y=150), move('#mag', 1.7, .8, x=200, y=200)] + seq_show(['q0', 'q1', 'q2'], .7, .8)
    S.append(Shot(L(6), L(7), yard() + horse('hs', 560, 1450, 1.05) + mag + badge('q0', 260, 560, 'STRINGS', '#e05a5a', 66) + badge('q1', 760, 680, 'SIGNALS', '#e05a5a', 66) + badge('q2', 380, 820, 'TRICKS', '#e05a5a', 66),
                  [(0, 1.2, 500, 1100), (1.3, 1.3, 700, 1000), (2.4, 1.1, 540, 900), (D(6), 1.2, 540, 1000)], a))
    # 7 mocker again, cockier: 'Fine. Then a stranger asks the questions.'
    a = talk('mk', .05, D(7) - .4, .13, rest='smirk') + [arm('mk', 'l', .2, 120), face('mk', .1, 'side', 'smirk')]
    S.append(Shot(L(7), L(8), yard() + mocker('mk', 620, 1600, 1.6, flip=True), [(0, 1.35, 600, 1000), (D(7), 1.55, 620, 950)], a))
    # 8 the owner leaves, a stranger asks... Hans still gets it right (check)
    a = [move('#tc', 0, 1.0, 'power1.in', x=700)] + bob('tc', 0, 1.0, 12, .2) + [fromto('#sg', 1.0, .6, {'x': -500}, {'x': 0}, 'power2.out')] + talk('sg', 1.6, 1.0) + taps('hs', 2.4, 4, .3)
    a += [fromto('#ok', D(8) - .9, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'), fromto('#bq', 1.7, .3, {'opacity': 0}, {'opacity': 1})]
    S.append(Shot(L(8), L(9), yard() + blackboard(820, 640, 380, 260, ['7 - 3'], 110, ['bq']) + teacher('tc', 860, 1450, .9, flip=True)
                  + g(person('sg', 180, 1450, .9, coat='#7a5a2a', skin='c', hat='beanie', eyes='norm', mouth='smile'), 'sg') + horse('hs', 560, 1480, .95) + check('ok', 820, 960, 1.4),
                  [(0, 1.1, 700, 1150), (1.6, 1.3, 300, 1100), (2.8, 1.3, 560, 1250), (D(8), 1.2, 700, 900)], a))
    # 9 the experts give up: NO TRICK stamp, experts shrug
    stamp = g(rect(-330, -90, 660, 180, 'none', 18, 14, 'stroke="#e05a5a"') + text(0, 40, 'NO TRICK', 120, '#e05a5a', extra='stroke-width="0"'), 'stp', 'translate(540,700) rotate(-8)', 'opacity="0"')
    a = [fromto('#stp', .3, .25, {'opacity': 0, 'scale': 2.5, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'power3.in')] + [arm(f'x{i}', 'l', .6, 150) for i in range(0, 13, 2)] + [arm(f'x{i}', 'r', .6, -150) for i in range(1, 13, 2)]
    S.append(Shot(L(9), L(10), yard() + ex.replace('x', 'x') + stamp, [(0, 1.3, 540, 760), (D(9), 1.05, 540, 1050)], a))
    # 10 the young scientist: a question he does NOT know the answer to (covered card)
    card = g(rect(-200, -140, 400, 280, '#fdfcf8', 14, 8) + text(0, -20, '? ? ?', 110, OUT, extra='stroke-width="0"') + rect(-160, 30, 320, 70, '#2a2440', 10, 0), 'card', 'translate(620,760)', 'opacity="0"')
    a = [fromto('#yg', 0, .7, {'x': -400}, {'x': 0}, 'power2.out')] + bob('ys', 0, .7, 10, .2) + [fromto('#card', 1.4, .4, {'opacity': 0, 'y': 120}, {'opacity': 1, 'y': 0}, 'back.out(2)'), face('ys', 2.4, 'side', 'smile')] + talk('ys', 2.6, D(10) - 2.8)
    S.append(Shot(L(10), L(11), yard() + g(young('ys', 260, 1460, 1.05), 'yg') + card + horse('hs', 800, 1480, .8, flip=True),
                  [(0, 1.1, 300, 1150), (1.6, 1.35, 600, 860), (D(10), 1.2, 450, 1050)], a))
    # 11 Hans keeps tapping: 6 7 8 9... he has no idea (sweat, wide eyes)
    a = taps('hs', 0, 12, .34) + flash_seq([f'k{k}' for k in range(4)], 1.0, .45) + [face('ys', .2, 'wide', 'o'), setp('#hs-e-norm', .9, opacity=0), setp('#hs-e-wide', .9, opacity=1), fromto('#hs-sweat', 1.8, .4, {'opacity': 0, 'y': 0}, {'opacity': 1, 'y': 30})]
    S.append(Shot(L(11), L(12), yard() + horse('hs', 600, 1480, 1.2) + young('ys', 140, 1500, .8) + counter('k', 4, 820, 760, 240, 6),
                  [(0, 1.2, 600, 1150), (1.4, 1.5, 820, 900), (2.6, 1.4, 700, 1100), (D(11), 1.6, 820, 980)], a))
    # 12 you see: questioner's face close-up; tense as the hoof nears the answer; at the answer the head lifts a tiny bit
    hoof = g(rect(-60, -140, 120, 200, grad('#a8743c'), 18, 8) + rect(-70, 40, 140, 50, '#3a2a20', 12, 7), 'hf', 'translate(0,40) scale(.8)')
    tense = L(12) + D(12) * .45; lift = L(12) + D(12) * .78
    a = [face('qq', tense - L(12), 'wide', 'flat'), fromto('#tn', tense - L(12), .3, {'opacity': 0}, {'opacity': 1}), (lift - L(12), 'tl.to("#qq-face",{y:-26,duration:.18,ease:"power2.out"},{T});'),
         face('qq', lift - L(12), 'happy', 'smile'), fromto('#up', lift - L(12), .3, {'opacity': 0, 'y': 40}, {'opacity': 1, 'y': 0}), setp('#tn', lift - L(12), opacity=0)]
    a += [(k * .5, f'tl.fromTo("#hf",{{rotation:0}},{{rotation:-25,duration:.2,yoyo:true,repeat:1,transformOrigin:"50% 0%"}},{{T}});') for k in range(int(D(12) / .5))]
    S.append(Shot(L(12), L(13), wall('#3a3060', 2400) + pool(540, 1100, 620, 520) + person('qq', 440, 1820, 2.4, coat='#7a5a2a', skin='a', eyes='norm', mouth='smile')
                  + g(rect(-160, -160, 320, 320, '#fdfcf8', 30, 8) + hoof, tr='translate(830,600)') + text(440, 700, 'TENSE', 90, '#ff8a5a', extra='id="tn" opacity="0"')
                  + g(path('M0,60 L0,-60 M-40,-20 L0,-60 L40,-20', sw=16, stroke='#5fd36a'), 'up', 'translate(170,760)', 'opacity="0"'),
                  [(0, 1.0, 540, 950), (2.0, 1.25, 830, 650), (tense - L(12), 1.3, 440, 1000), (lift - L(12), 1.45, 440, 980), (D(12), 1.3, 440, 960)], a))
    # 13 Hans saw it every time: big horse eye reflecting a face -> STOP
    eye = g(ell(0, 0, 300, 240, '#fff', 12) + ell(30, 10, 170, 170, '#3a2418', 8) + ell(30, 10, 80, 80, OUT) + ell(-30, -50, 40, 30, '#fff', extra='opacity=".9"')
            + g(person('rf', 0, 90, .32, coat='#7a5a2a', skin='a', eyes='happy', mouth='smile'), tr='translate(30,0)'), 'eye', 'translate(540,820)')
    a = [fromto('#eye', 0, .5, {'scale': .6, 'transformOrigin': '50% 50%'}, {'scale': 1}, 'back.out(2)'), fromto('#stop', D(13) * .55, .25, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    S.append(Shot(L(13), L(14), wall('#6a4a3a', 2400) + pool(540, 820, 700, 600) + eye + badge('stop', 540, 1500, 'STOP', '#e05a5a', 130),
                  [(0, 1.0, 540, 900), (1.2, 1.45, 570, 840), (D(13), 1.1, 540, 1000)], a))
    # 14 stats: sees the person 9/10, blinders ~never (bars) + Hans in blinders
    bars = (path('M160,1200 L160,500 M160,1200 L960,1200', sw=8, stroke='#f4f4e8') + g(rect(240, -620, 240, 620, '#5fd36a', 10, 7), 'bar1', 'translate(0,1200)') + g(rect(620, -50, 240, 50, '#e05a5a', 10, 7), 'bar2', 'translate(0,1200)')
            + text(360, 1290, 'SEES', 64) + text(740, 1290, 'BLINDERS', 64) + text(360, 540, '9 / 10', 80, '#5fd36a', extra='id="t1" opacity="0"') + text(740, 1110, 'ALMOST 0', 70, '#ff8a5a', extra='id="t2" opacity="0"'))
    a = [fromto('#bar1', .3, .7, {'scaleY': 0, 'transformOrigin': '50% 100%'}, {'scaleY': 1}, 'power3.out'), move('#t1', 1.0, .2, opacity=1),
         fromto('#bar2', D(14) * .6, .4, {'scaleY': 0, 'transformOrigin': '50% 100%'}, {'scaleY': 1}), move('#t2', D(14) * .6 + .3, .2, opacity=1), fromto('#hb', D(14) * .55, .4, {'opacity': 0, 'x': 200}, {'opacity': 1, 'x': 0})]
    S.append(Shot(L(14), L(15), wall('#2d4a40', 2400) + pool(540, 900, 600, 500) + g(bars, tr='translate(0,-220)') + g(horse('hb', 0, 0, .55, blinders=True, eyes='wide'), 'hbw', 'translate(760,1580)'),
                  [(0, 1.0, 540, 700), (D(14) * .5, 1.05, 560, 700), (D(14), 1.0, 540, 740)], a))
    # 15 payoff: Hans never knew maths, he read the smartest people in the city... the mocker gasps (lands on him)
    smart = ''.join(person(f'z{i}', 100 + i * 150, 1300, .6, coat=['#2f4f4a', '#3f5f9f', '#6a4a3a', '#4a3a6a'][i % 4], skin='abcd'[i % 4], glasses=True, mustache=i % 2 == 0, eyes='happy', mouth='smile',
                           extra_acc=tophat(-300) if i % 2 else '') for i in range(6))
    a = [nod('hs', .3), (1.2, 'tl.set("#hs-e-norm",{opacity:0},{T});tl.set("#hs-e-side",{opacity:1},{T});tl.set("#hs-e-side",{opacity:0},{T}+.5);tl.set("#hs-e-norm",{opacity:1},{T}+.5);'),
         fromto('#mkw', D(15) * .6, .4, {'x': 500}, {'x': 0}, 'power2.out'), face('mk', D(15) * .62, 'wide', 'open')] + [face(f'z{i}', D(15) * .7 + i * .05, 'wide', 'o') for i in range(6)]
    S.append(Shot(L(15), L(16), yard() + smart + horse('hs', 420, 1560, .95) + g(mocker('mk', 880, 1600, 1.1, eyes='norm', mouth='flat', flip=True), 'mkw'),
                  [(0, 1.3, 420, 1150), (1.6, 1.05, 540, 1000), (D(15) * .6, 1.35, 860, 1100), (D(15), 1.5, 880, 1060)], a))
    # 16 A/B
    S.append(Shot(L(16), total, outro('EASILY', '', 'NO', 'WAY'), [(0, 1.0, 540, 950), (total - L(16), 1.12, 540, 1000)], outro_anims()))
    return S

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(16) - .3,
      'flares': [(E(0) - .3, 'flare'), (L(3) + .4, 'shrink'), (L(8) + 2.8, 'flare'), (L(11) + 1.0, 'shrink'), (L(15) + 2.0, 'flare')]}

def audio():
    T = TOTAL; P = L(15)
    music = [('Merry_Go.mp3', 0, 0, L(3) - .05, 0, (.02, .2)),
             ('Fluffing_a_Duck.mp3', 0, L(3), L(5), -2, (.05, .2)),
             ('Hall_of_the_Mountain_King.mp3', 40, L(5), L(10) - .05, -1, (.2, .2)),
             ('Investigations.mp3', 0, L(10), P - .4, -2, (.2, .2)),
             ('Fun_in_a_Bottle.mp3', 0, P + .8, T, 0, (.05, 1.0))]
    O = '100-cc0-sfx/'; O2 = '100-cc0-sfx-2/sfx100v2_'; SW = 'swishes-sound-pack/swishes/swish-'
    TAP = O + 'wooden_01.ogg'
    t0 = E(0) - 2.0
    sfx = [('horse-trotting/Trot.ogg', 0.0, -10, 0, 1.2), ('chalk', 0, 0)] if False else [('horse-trotting/Trot.ogg', 0.0, -10, 0, 1.0), ('drawing-with-chalk/chalk_drawing_01.mp3', .3, -6, 0, .9)]
    sfx += [(TAP, t0 + k * .36 + .1, 0) for k in range(5)] + [(O + 'bell_02.ogg', E(0), -6)]
    sfx += [(SW + '3.wav', L(1) - .1, -4), ('drawing-with-chalk/chalk_drawing_02.mp3', L(1) + 1.2, -5, 0, 2.0), ('horse-trotting/Trot.ogg', L(1) + 1.4, -10, 1, .6),
            ('crowd-shoutingspeaking-ambience/crowd_shouting.ogg', L(2), -5, 0, D(2)), ('applause-in-a-large-hall-or-church/applause-clapping-church-crowd-immersive.wav', L(2) + .4, -6, 1, D(2)),
            (SW + '7.wav', L(3) - .1, -4), ('do-you-remember-laughter/ogalaughter_2.ogg', E(3) + .02, -4, 22.5, 1.7), (O + 'paper_02.ogg', E(3) - 1.3, -4),
            (O + 'spring_02.ogg', L(4) + .5, -8), ('horse-trotting/Trot.ogg', L(4) + 1.4, -10, 2, .5),
            ('footsteps-0/01-footstep.ogg', L(5) + .1, -5), ('footsteps-0/02-footstep.ogg', L(5) + .3, -5), ('footsteps-0/03-footstep.ogg', L(5) + .5, -5), ('footsteps-0/04-footstep.ogg', L(5) + .7, -5),
            (O + 'bell_01.ogg', L(5) + 1.0, -7), (SW + '5.wav', L(6) + .1, -6), (SW + '6.wav', L(6) + .9, -6), (SW + '8.wav', L(6) + 1.7, -6)]
    sfx += [(O2 + 'misc_0%d.ogg' % (4 + k), L(6) + .7 + k * .8, -5) for k in range(3)]
    sfx += [(SW + '2.wav', L(7) - .1, -4), ('group-giggling/group_giggling.ogg', E(7) - .1, -8, 0, 1.0),
            (O + 'door_close_01.ogg', L(8) + 1.0, -4), ('footsteps-0/05-footstep.ogg', L(8) + 1.1, -6), ('footsteps-0/06-footstep.ogg', L(8) + 1.4, -6)]
    sfx += [(TAP, L(8) + 2.4 + k * .3 + .08, -1) for k in range(4)] + [(O + 'bell_03.ogg', L(9) - .9, -4), ('applause-in-a-large-hall-or-church/applause-clapping-church-crowd-immersive.wav', L(9) - .6, -10, 4, 1.2)]
    sfx += [('muffled-distant-explosion/NenadSimic - Muffled Distant Explosion.wav', L(9) + .5, -4, 0, 1.0), (O + 'paper_01.ogg', L(10) + 1.4, -3), (SW + '9.wav', L(10) - .05, -5)]
    sfx += [(TAP, L(11) + k * .34 + .08, -2) for k in range(12)] + [(O + 'weird_04.ogg', L(11) + 1.8, -6)]
    sfx += [(SW + '4.wav', L(12) - .1, -4)] + [(TAP, L(12) + k * .5 + .1, -9) for k in range(int(D(12) / .5))] + [(O + 'spring_04.ogg', L(12) + D(12) * .78, -3)]
    sfx += [(SW + '11.wav', L(13) - .05, -4), (O + 'slam_04.ogg', L(13) + D(13) * .55, -3),
            (SW + '12.wav', L(14) - .05, -4), (O + 'spring_07.ogg', L(14) + .3, -6), (O + 'switch_02.ogg', L(14) + D(14) * .6, -4),
            ('muffled-distant-explosion/NenadSimic - Muffled Distant Explosion.wav', P - .1, -2, 0, 1.6), ('horse-trotting/Trot.ogg', P + .4, -9, 3, .6),
            ('group-giggling/group_giggling_0.ogg', P + D(15) * .7, -6, 0, 1.4), (SW + '1.wav', L(16) - .05, -3), ('fire-crackling/fire-1.ogg', L(16) + .1, -6, 0, 1.2), (O2 + 'air_01.ogg', T - 1.0, -1)]
    return music, sfx

def build_tt():
    """TikTok-only file: first 2.4 s = tight hoof close-up + a question banner, then the same film; re-encoded."""
    def shots_tt(lines, total):
        S = shots(lines, total)
        S[0].cam = [(0, 2.3, 820, 1350), (1.2, 1.9, 700, 1250), (2.4, 1.3, 600, 1100), (D(0), 1.45, 760, 1100)]
        return S
    ov = ('<div id="ttq" class="clip" data-start="0" data-duration="2.4" data-track-index="5" style="position:absolute;left:0;top:300px;width:1080px;text-align:center;z-index:960">'
          '<span style="display:inline-block;font-family:Montserrat;font-weight:900;font-size:76px;line-height:1.05;color:#140c26;background:#ffd27a;padding:18px 34px;border-radius:26px;border:8px solid #140c26">'
          'A HORSE THAT DID MATHS?<br>WAIT FOR THE TWIST</span></div>')
    js = 'tl.fromTo("#ttq span",{scale:.6,rotation:-4},{scale:1,rotation:-2,duration:.25,ease:"back.out(3)"},0.05);'
    return build(dict(EP, shots=shots_tt, hfdir='hf_tt', overlay=ov, overlay_js=js))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mix':
        from mix import mix
        mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
    elif len(sys.argv) > 1 and sys.argv[1] == 'tt': print(build_tt())
    else: print(build(EP), TOTAL)
