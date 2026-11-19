import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *
from props2 import *
from props3 import *

SLUG = '2026-11-19-how-bats-burned-their-own-base'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.3, 2)
def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']
def D(i): return L(i + 1) - L(i)

def dentist(pid, x, y, s=1, eyes='norm', mouth='smile', flip=False):
    mirror = g(path('M-86,-250 L86,-250', sw=10, stroke='#c8ccd8') + ell(0, -262, 30, 30, '#e8eef8', 7), tr='translate(0,0)')
    return person(pid, x, y, s, coat='#f4f4ee', skin='a', glasses=True, eyes=eyes, mouth=mouth, flip=flip, hair='tuft', extra_acc=mirror)
def officer(pid, x, y, s=1, eyes='side', mouth='smirk', flip=False):
    return person(pid, x, y, s, coat='#5a6a3a', skin='d', mustache=True, hat='cap', eyes=eyes, mouth=mouth, flip=flip,
                  extra_acc=rect(-60, -150, 40, 16, '#ffd27a', 4, 4) + rect(20, -150, 40, 16, '#ffd27a', 4, 4))
def bulb(id, x, y):
    return g(ell(0, 0, 70, 80, '#ffe27a', 8) + rect(-34, 70, 68, 50, grad('#9aa0b0'), 8, 7) + ell(0, 0, 150, 150, 'url(#glow)'), id, f'translate({x},{y})', 'opacity="0"')
def roofs(y=1350, fire=False):
    s = ''
    for k in range(6):
        x = -60 + k * 200; h = 160 + (k % 3) * 40
        s += rect(x, y - h, 180, h, grad('#a8743c'), 4, 7) + path(f'M{x - 20},{y - h} L{x + 90},{y - h - 90} L{x + 200},{y - h} Z', grad('#5a3a2a'), 7)
    return s

def shots(lines, total):
    S = []
    # 0 hook: dentist in a cave full of bats -> light bulb
    a = swarm_fly('cb', 14, 0, D(0), 300, -150) + [face('dn', 1.6, 'happy', 'grin')] + pop('bl', 1.9)
    S.append(Shot(0, L(1), cave() + swarm('cb', 14, 540, 520, 420, .55) + dentist('dn', 540, 1560, 1.2, 'wide', 'o') + bulb('bl', 760, 1000),
                  [(0, 1.0, 540, 700), (1.5, 1.25, 540, 1150), (D(0), 1.35, 650, 1080)], a))
    # 1 a bat weighs half an ounce; carries a bomb heavier than itself (scale tips, then it flies off with it)
    h = D(1) * .55
    sc_ = g(path('M0,0 L0,-420', sw=14) + g(path('M-320,0 L320,0', sw=14) + path('M-320,0 L-360,120 L-280,120 Z M320,0 L280,120 L360,120 Z', sw=6)
             + g(bat('sb', 0, 60, .9), tr='translate(-320,0)') + g(rect(-50, 30, 100, 130, grad('#c0c4d0'), 20, 8) + rect(-50, 30, 100, 30, '#d8423f', 6, 0), tr='translate(320,0)'), 'beam', 'translate(0,-420)')
             + path('M-160,0 L160,0', sw=18), 'scl', 'translate(540,1250)')
    a = [(.6, 'tl.to("#beam",{rotation:12,duration:.6,ease:"bounce.out",transformOrigin:"50% 0%"},{T});')] + pop('w1', .9) + pop('w2', 1.6)
    S.append(Shot(L(1), L(1) + h, wall('#3a3060', 2400) + pool(540, 1000, 600, 500) + sc_ + badge('w1', 300, 640, '1/2 OZ', '#ffd27a', 64) + badge('w2', 820, 600, 'HEAVIER', '#ff8a5a', 64),
                  [(0, 1.0, 540, 900), (h, 1.2, 540, 950)], a))
    a = swarm_fly('fb', 1, 0, D(1) - h, 0, 0) + [fromto('#fbw', 0, D(1) - h, {'x': -500, 'y': 200}, {'x': 500, 'y': -150}, 'sine.inOut')]
    S.append(Shot(L(1) + h, L(2), sky(moon=True) + roofs() + g(bat('fb0', 540, 700, 1.6, bomb=True), 'fbw'), [(0, 1.1, 340, 800), (D(1) - h, 1.2, 740, 650)], a))
    # 2 the plan: canister with a parachute, 1,000 sleeping bats, over wooden houses
    h = D(2) * .5
    a = [fromto('#cn', 0, h, {'y': -600}, {'y': 0}, 'sine.out')] + pop('k1', .8)
    S.append(Shot(L(2), L(2) + h, sky(moon=True) + roofs(1650) + canister('cn', 540, 1000, 1.0, chute=True) + badge('k1', 540, 420, '1,000 BATS', '#ffd27a', 76),
                  [(0, 1.0, 540, 800), (h, 1.15, 540, 900)], a))
    a = swarm_fly('rb', 12, .3, D(2) - h - .3, 0, 500) + [fromto('#cnb', 0, .4, {'opacity': 1}, {'opacity': 0})]
    S.append(Shot(L(2) + h, L(3), sky(moon=True) + roofs(1650) + swarm('rb', 12, 540, 700, 300, .5) + canister('cnb', 540, 900, .8),
                  [(0, 1.1, 540, 800), (D(2) - h, 1.0, 540, 1100)], a))
    # 3 the mocker: 'Bats? Sure. And next we'll train squirrels!'
    a = talk('of', .05, D(3) - .3, .12, rest='smirk') + [arm('of', 'r', .3, -140), arm('of', 'r', 1.2, -40)]
    sq = g(ell(0, 0, 70, 60, grad('#b07a4a'), 7) + ell(-40, -60, 40, 40, grad('#b07a4a'), 7) + ell(-50, -66, 7, 8, OUT) + path('M60,0 Q150,-60 90,-150 Q50,-90 40,-20', grad('#b07a4a'), 7), 'sq', 'translate(860,620)', 'opacity="0"')
    S.append(Shot(L(3), L(4), wall('#3a4a3a', 2400) + pool(540, 1100, 600, 500) + officer('of', 470, 1720, 2.0) + sq,
                  [(0, 1.0, 470, 1100), (D(3), 1.3, 560, 980)], a + [fromto('#sq', D(3) - 1.0, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]))
    # 4 the President's reply letter: 'This man is not a nut.'
    a = [fromto('#lt', .1, .5, {'opacity': 0, 'y': 300, 'rotation': -8}, {'opacity': 1, 'y': 0, 'rotation': -3}, 'back.out(2)'),
         fromto('#nn', 1.6, .3, {'opacity': 0, 'scale': 2.2, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'power3.in')]
    nn = g(rect(-330, -60, 660, 120, 'none', 16, 10, 'stroke="#d8423f"') + text(0, 26, 'NOT A NUT', 82, '#d8423f', extra='stroke-width="0"'), 'nn', 'translate(540,400) rotate(-6)', 'opacity="0"')
    S.append(Shot(L(4), L(5), wall('#4a3a6a', 2400) + pool(540, 900, 600, 600) + letter('lt', 540, 860, ['"This man', 'is not a nut."']) + nn,
                  [(0, 1.0, 540, 900), (1.4, 1.15, 540, 980), (D(4), 1.2, 540, 1000)], a))
    # 5 ice cube trays (frost) then a tiny bomb clipped to each bat
    h = D(5) * .5
    frost = ''.join(path(f'M{x},{y} l20,20 m-20,0 l20,-20 m-10,-6 l0,32', sw=4, stroke='#e6f6ff', extra='opacity=".7"') for x, y in ((180, 520), (900, 640), (300, 1500), (820, 1450), (520, 380)))
    a = [fromto('#tr', 0, .5, {'y': 400, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)')] + pop('ic', .9)
    S.append(Shot(L(5), L(5) + h, wall('#3a5a7a', 2400) + pool(540, 900, 600, 500) + frost + ice_tray('tr', 540, 900, 1.5) + badge('ic', 540, 560, 'ZZZ...', '#bfe6ff', 70),
                  [(0, 1.0, 540, 900), (h, 1.2, 540, 900)], a))
    clip_ = g(path('M0,0 L0,40', sw=5) + rect(-24, 40, 48, 70, grad('#c0c4d0'), 12, 6) + rect(-24, 40, 48, 18, '#d8423f', 4, 0), 'clp', 'translate(540,980)', 'opacity="0"')
    a = [fromto('#clp', .5, .35, {'opacity': 0, 'y': 200}, {'opacity': 1, 'y': 0}, 'back.out(3)'), fromto('#tw', .1, .5, {'x': 300}, {'x': 0}, 'power2.out')] + pop('ck', 1.2)
    tweez = g(path('M0,0 L260,-120 M0,10 L260,-80', sw=12, stroke='#c8ccd8'), 'tw', 'translate(600,1000)')
    S.append(Shot(L(5) + h, L(6), wall('#3a5a7a', 2400) + pool(540, 900, 600, 500) + bat('bb', 540, 900, 2.4, eyes='shut') + clip_ + tweez + check('ck', 820, 600, 1.2),
                  [(0, 1.2, 540, 900), (D(5) - h, 1.35, 560, 960)], a))
    # 6 mocker again, cockier: 'They're gonna nap through the whole war!'
    a = talk('of', .05, D(6) - .3, .11, rest='grin') + bob('of', 0, D(6), 10, .2) + [arm('of', 'l', .1, 140)]
    S.append(Shot(L(6), L(7), wall('#3a4a3a', 2400) + pool(540, 1100, 600, 500) + officer('of', 560, 1640, 1.7, eyes='happy', mouth='grin', flip=True),
                  [(0, 1.3, 560, 1000), (D(6), 1.5, 560, 950)], a))
    # 7 desert air base, somebody left a door open (door swings, wind lines)
    door = g(rect(0, 0, 150, 300, grad('#55607a'), 6, 8) + ell(126, 150, 10, 10, WARM2), 'dr', 'translate(465,1000)')
    a = [(.6, 'tl.to("#dr",{scaleX:-.25,duration:.5,ease:"power2.out",transformOrigin:"0% 50%"},{T});')] + pop('op', 1.2)
    S.append(Shot(L(7), L(8), desert_base() + hangar('hg', 270, 1250, .8) + rect(450, 990, 180, 320, '#1c1538', 6, 8) + rect(380, 960, 330, 360, 'none', 6, 8)
                  + path('M380,960 L545,860 L710,960', grad('#7a8090'), 8) + door + text(545, 920, 'BAT LAB', 46, '#fdfcf8') + badge('op', 760, 760, 'OPEN!', '#ff8a5a', 70) + army_car('car', 860, 1330, .7, flip=True),
                  [(0, 1.0, 540, 950), (1.0, 1.35, 545, 1080), (D(7), 1.3, 600, 1020)], a))
    # 8 the bats wake up, with live bombs still clipped on
    a = swarm_fly('wk', 10, .6, D(8) - .6, 200, -500)
    eyes = g(ell(-60, 0, 40, 46, '#fff', 7) + ell(60, 0, 40, 46, '#fff', 7) + ell(-56, 4, 16, 20, OUT) + ell(64, 4, 16, 20, OUT), 'ey', 'translate(540,820)')
    a += [fromto('#ey', 0, .25, {'scaleY': .05, 'transformOrigin': '50% 50%'}, {'scaleY': 1}, 'back.out(3)'), setp('#ey', .6, opacity=0)]
    S.append(Shot(L(8), L(9), rect(-400, -400, W + 800, H + 800, '#140c26', sw=0) + eyes + swarm('wk', 10, 540, 1000, 300, .8, bomb=True),
                  [(0, 1.5, 540, 820), (.6, 1.0, 540, 900), (D(8), 1.05, 640, 700)], a))
    # 9 they found the darkest corners: under the hangar roof, under a parked car
    a = swarm_fly('dc', 6, 0, 1.3, 0, -250) + swarm_fly('dd', 4, 1.0, 1.6, 150, 280)
    S.append(Shot(L(9), L(10), desert_base() + hangar('hg', 380, 1250, 1.1, door_open=True) + army_car('car', 830, 1330, .9, flip=True)
                  + swarm('dc', 6, 380, 1000, 220, .45, seed=7, bomb=True) + swarm('dd', 4, 640, 1050, 120, .45, seed=8, bomb=True),
                  [(0, 1.0, 540, 1000), (1.3, 1.3, 380, 900), (2.6, 1.3, 800, 1200), (D(9), 1.15, 600, 1050)], a))
    # 10 you see: normal bomb bounces off the roof / a bat crawls under the beams
    h = D(10) * .4
    bm = g(rect(-40, -90, 80, 180, grad('#9aa0b0'), 30, 8) + path('M-40,-90 L-70,-150 L70,-150 L40,-90', fill=grad('#7a8090'), sw=7), 'nb', 'translate(540,200)')
    a = [fromto('#nb', 0, .6, {'y': 0}, {'y': 700}, 'power2.in'), (.6, 'tl.to("#nb",{x:380,y:500,rotation:70,duration:.6,ease:"power1.out"},{T});'), (.6, 'tl.fromTo("#rc",{y:0},{y:8,duration:.06,yoyo:true,repeat:3},{T});')]
    a += pop('roof', 1.2)
    S.append(Shot(L(10), L(10) + h, sky(moon=True) + roof_cut('rc', 540, 1180, 1.4) + bm + badge('roof', 540, 1560, 'HITS THE ROOF', '#9aa0b0', 64),
                  [(0, 1.0, 540, 800), (h, 1.1, 540, 950)], a))
    a = [fromto('#cr', 0, D(10) - h - .5, {'x': -320, 'y': 200}, {'x': 0, 'y': 0}, 'sine.inOut')] + flap('cr', 0, 1.0, .15) + pop('att', 1.6) + pop('nob', 3.0)
    S.append(Shot(L(10) + h, L(11), sky(moon=True) + roof_cut('rc', 540, 1180, 1.4) + g(bat('cr', 540, 870, .55, bomb=True), tr='') + badge('att', 420, 420, 'ATTIC', '#ffd27a', 70) + badge('nob', 760, 1560, 'NO ONE CAN REACH', '#ff8a5a', 56),
                  [(0, 1.2, 440, 950), (1.6, 1.6, 540, 860), (D(10) - h, 1.3, 560, 900)], a))
    # 11 tests: ~10x more fires (bars), flames pop
    a = [fromto('#b11a', .3, .4, {'scaleY': 0, 'transformOrigin': '50% 100%'}, {'scaleY': 1}), fromto('#b11b', .9, .9, {'scaleY': 0, 'transformOrigin': '50% 100%'}, {'scaleY': 1}, 'power3.out')] + pop('x10', 1.9)
    fl = ''.join(flame(f'f{k}', 650 + (k % 3) * 70, 420 - (k // 3) * 90, .35) for k in range(6))
    a += [pop(f'f{k}', 1.9 + k * .12)[0] for k in range(6)]
    S.append(Shot(L(11), L(12), wall('#3a3060', 2400) + pool(540, 900, 600, 500) + bars2('b11', 'NORMAL', 'BATS', 70, 640, 540, 980) + badge('x10', 540, 1560, 'x10', '#ff8a5a', 110)
                  + g(fl, tr='translate(0,0)').replace('<g id="f', '<g opacity="0" id="f'),
                  [(0, 1.0, 540, 820), (D(11), 1.08, 560, 760)], a))
    # 12 too slow: CANCELLED stamp + $2,000,000
    a = pop('mn', .3) + [fromto('#st', 1.4, .25, {'opacity': 0, 'scale': 2.5, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'power3.in'), face('of', 1.7, 'happy', 'grin')]
    st = g(rect(-360, -90, 720, 180, 'none', 18, 14, 'stroke="#e05a5a"') + text(0, 40, 'CANCELLED', 120, '#e05a5a', extra='stroke-width="0"'), 'st', 'translate(540,820) rotate(-8)', 'opacity="0"')
    S.append(Shot(L(12), L(13), wall('#3a4a3a', 2400) + pool(540, 1000, 600, 500) + text(540, 560, '$2,000,000', 130, '#5fd36a', extra='id="mn" opacity="0"') + officer('of', 820, 1700, 1.0, flip=True) + st,
                  [(0, 1.05, 540, 700), (D(12), 1.15, 560, 860)], a))
    # 13 that first escape: the hangar burns
    a = sum((flicker(f'h{k}', k * .05, D(13)) for k in range(4)), []) + pop('h0', .3) + pop('h1', .6) + pop('h2', .9) + pop('h3', 1.1)
    hf = ''.join(flame(f'h{k}', 380 + k * 110 - 160, 1000 - (k % 2) * 140, 1.0 + (k % 2) * .3) for k in range(4)).replace('<g id="h', '<g opacity="0" id="h')
    S.append(Shot(L(13), L(14), desert_base() + hangar('hg', 380, 1250, 1.2) + g(hf, tr='') + rect(-400, -400, W + 800, H + 800, '#ff6a2e', sw=0, extra='opacity=".12"'),
                  [(0, 1.0, 540, 900), (D(13), 1.25, 380, 950)], a))
    # 14 payoff: ...and a general's car (car in flames, the mocker drops his jaw)
    a = flicker('cf0', 0, D(14) + .5) + flicker('cf1', .06, D(14) + .5) + [face('of', .15, 'wide', 'open'), arm('of', 'l', .2, 150), arm('of', 'r', .2, -150)]
    S.append(Shot(L(14), L(15), desert_base() + army_car('car', 640, 1330, 1.15, flip=True) + flame('cf0', 560, 1150, 1.1) + flame('cf1', 760, 1170, .9)
                  + officer('of', 200, 1560, 1.0, 'wide', 'open') + rect(-400, -400, W + 800, H + 800, '#ff6a2e', sw=0, extra='opacity=".12"'),
                  [(0, 1.45, 640, 1100), (D(14), 1.2, 450, 1050)], a))
    # 15 A/B
    S.append(Shot(L(15), total, outro('KEEP', 'BATS', 'NEW', 'CAR'), [(0, 1.0, 540, 950), (total - L(15), 1.12, 540, 1000)], outro_anims()))
    return S

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(15) - .3,
      'flares': [(L(0) + 1.8, 'flare'), (L(3) + .4, 'shrink'), (L(8) + .3, 'flare'), (L(13) + .5, 'shrink'), (L(14) + .2, 'flare')]}

def audio():
    T = TOTAL
    music = [('km_Sneaky_Snitch.mp3', 0, 0, L(3) - .05, -1, (.02, .2)),
             ('km_Fluffing_a_Duck.mp3', 0, L(3), L(7), -2, (.05, .2)),
             ('km_Volatile_Reaction.mp3', 3, L(7), L(10), 0, (.1, .2)),
             ('km_Investigations.mp3', 0, L(10), L(13) - .35, -2, (.2, .1)),
             ('km_Fun_in_a_Bottle.mp3', 0, L(14) + .6, T, -1, (.05, 1.0))]
    O = '100-cc0-sfx/'; O2 = '100-cc0-sfx-2/sfx100v2_'; SW = 'swishes-sound-pack/swishes/swish-'; CR = '80-cc0-creature-sfx/'
    SQ = [CR + f'cute_0{k}.ogg' for k in (1, 3, 5, 7)]; FL = O2 + 'air_02.ogg'
    sfx = [(O2 + 'loop_water_01.ogg', 0, -14, 0, D(0)), (SQ[0], .3, -5), (SQ[1], .9, -6), (FL, .5, -8, 0, .6), (O + 'bell_02.ogg', L(0) + 1.9, -4)]
    sfx += [(SW + '3.wav', L(1) - .1, -4), (O + 'metal_05.ogg', L(1) + .6, -2), (O + 'spring_02.ogg', L(1) + .9, -6), (SW + '5.wav', L(1) + D(1) * .55 - .05, -4),
            (FL, L(1) + D(1) * .55 + .2, -6, 0, .8), (SQ[2], L(1) + D(1) * .55 + .6, -4)]
    sfx += [(SW + '9.wav', L(2) - .05, -4), (O2 + 'air_03.ogg', L(2) + .2, -6), (O + 'switch_02.ogg', L(2) + .8, -4), (O + 'metal_03.ogg', L(2) + D(2) * .5, -2),
            (FL, L(2) + D(2) * .5 + .3, -4, 0, 1.2), (SQ[3], L(2) + D(2) * .5 + .5, -5), (SQ[0], L(2) + D(2) * .5 + .9, -6)]
    sfx += [(SW + '7.wav', L(3) - .1, -4), ('do-you-remember-laughter/ogalaughter_2.ogg', E(3) - .1, -4, 22.5, 1.7), (O + 'spring_04.ogg', E(3) - 1.0, -6)]
    sfx += [(O + 'paper_02.ogg', L(4) + .1, -3), (O + 'slam_04.ogg', L(4) + 1.6, -2)]
    sfx += [(O2 + 'glass_03.ogg', L(5) + .2, -5), (CR + 'snore.ogg', L(5) + .7, -6, 0, 1.6), (O + 'switch_01.ogg', L(5) + D(5) * .5 + .5, -2), (O + 'spring_07.ogg', L(5) + D(5) * .5 + 1.2, -6)]
    sfx += [(SW + '2.wav', L(6) - .1, -4), ('group-giggling/group_giggling.ogg', L(6) + .2, -6, 0, 1.3)]
    sfx += [(O2 + 'loop_ambient_02.ogg', L(7), -14, 0, D(7)), (O + 'door_open.ogg', L(7) + .6, -1), (O2 + 'air_01.ogg', L(7) + 1.0, -6)]
    sfx += [(CR + 'breath.ogg', L(8) - .05, -4), (O + 'weird_03.ogg', L(8) + .1, -6), (FL, L(8) + .6, -2, 0, 1.6)] + [(SQ[k % 4], L(8) + .7 + k * .3, -4) for k in range(5)]
    sfx += [(FL, L(9), -4, 0, 1.4), (O + 'metal_08.ogg', L(9) + 1.3, -6), (FL, L(9) + 1.0, -6, 0, 1.4), (SQ[2], L(9) + 1.2, -6), (O + 'metal_02.ogg', L(9) + 2.6, -6)]
    sfx += [(SW + '4.wav', L(10) - .05, -4), (O2 + 'air_03.ogg', L(10) + .05, -6), (O + 'metal_01.ogg', L(10) + .6, 0), (O + 'hit_02.ogg', L(10) + 1.15, -4),
            (O2 + 'wood_01.ogg', L(10) + D(10) * .4 + .3, -6), (O2 + 'wood_02.ogg', L(10) + D(10) * .4 + 1.0, -6), (SQ[1], L(10) + D(10) * .4 + 1.6, -5)]
    sfx += [(SW + '12.wav', L(11) - .05, -4), (O + 'spring_07.ogg', L(11) + .3, -6), (O + 'switch_02.ogg', L(11) + .9, -4), ('fire-crackling/fire-1.ogg', L(11) + 1.9, -6, 0, D(11) - 1.9)]
    sfx += [(O + 'metal_05.ogg', L(12) + .3, -4), (O + 'slam_02.ogg', L(12) + 1.4, 0)]
    sfx += [('fire-crackling/fire-1.ogg', L(13), -1, 2, D(13) + D(14)), ('muffled-distant-explosion/NenadSimic - Muffled Distant Explosion.wav', L(13) + .3, -3, 0, 1.6)]
    sfx += [('muffled-distant-explosion/NenadSimic - Muffled Distant Explosion.wav', L(14) - .05, 0, 0, 1.6), (O + 'glass_02.ogg', L(14) + .15, -4), (CR + 'ooh.ogg', L(14) + .3, -6)]
    sfx += [(SW + '1.wav', L(15) - .05, -3), ('fire-crackling/fire-1.ogg', L(15) + .1, -10, 0, 1.2), (O2 + 'air_01.ogg', T - 1.0, -1)]
    return music, sfx

def build_tt():
    def shots_tt(lines, total):
        S = shots(lines, total)
        S[0].cam = [(0, 1.9, 540, 560), (1.2, 1.5, 540, 800), (2.4, 1.25, 540, 1150), (D(0), 1.35, 650, 1080)]
        return S
    ov = ('<div id="ttq" class="clip" data-start="0" data-duration="2.4" data-track-index="5" style="position:absolute;left:0;top:300px;width:1080px;text-align:center;z-index:960">'
          '<span style="display:inline-block;font-family:Montserrat;font-weight:900;font-size:76px;line-height:1.05;color:#140c26;background:#ffd27a;padding:18px 34px;border-radius:26px;border:8px solid #140c26">'
          'THE ARMY TRAINED BATS<br>WAIT FOR THE ENDING</span></div>')
    js = 'tl.fromTo("#ttq span",{scale:.6,rotation:-4},{scale:1,rotation:-2,duration:.25,ease:"back.out(3)"},0.05);'
    return build(dict(EP, shots=shots_tt, hfdir='hf_tt', overlay=ov, overlay_js=js))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mix':
        from mix import mix
        mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
    elif len(sys.argv) > 1 and sys.argv[1] == 'tt': print(build_tt())
    else: print(build(EP), TOTAL)
