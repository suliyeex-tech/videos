import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *

SLUG = '2026-11-16-skyscraper-fixed-at-night'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.4, 2)

def tower(x=540, base=1300, s=1.0, dark=False, lean=0, tid='tw'):
    w = 400; top = 150; body_bot = 1050
    win = ''
    r = random.Random(3)
    for yy in range(top + 230, body_bot - 30, 40):
        for xx in range(-w // 2 + 24, w // 2 - 30, 34):
            if r.random() < (.06 if dark else .45): win += rect(xx, yy - base, 16, 22, WARM2, 2, 0)
    t = (rect(-w // 2, top + 180 - base, w, body_bot - top - 180, grad('#7d8fb8'), 0, 9)
         + path(f'M{-w // 2},{top + 180 - base} L{w // 2},{top - base} L{w // 2},{top + 180 - base} Z', grad('#9aa9cc'), 9)
         + ''.join(path(f'M{-w // 2},{yy - base} L{w // 2},{yy - base}', sw=2, stroke='#5a6a90') for yy in range(top + 260, body_bot, 120))
         + win
         + rect(-30, body_bot - base, 60, base - body_bot, grad('#8e9cc0'), 4, 8)       # front stilt (middle of the side)
         + rect(150, body_bot - base, 40, base - body_bot - 40, shade('#8e9cc0', .4), 4, 6)  # back stilt
         + path(f'M{-w // 2},{body_bot - base} L{w // 2},{body_bot - base}', sw=12))
    return g(g(t, f'{tid}-sway', extra='class="sway"'), tid, f'translate({x},{base}) scale({s})')

def church(x, base, s=1.0):
    c = (rect(-90, -150, 180, 150, grad('#b98a6a'), 6, 7) + path('M-100,-150 L0,-230 L100,-150 Z', grad('#7a4a3a'), 7)
         + rect(-20, -60, 40, 60, '#3a2418', 14, 6) + rect(-40, -330, 50, 120, grad('#b98a6a'), 4, 6) + path('M-48,-330 L-15,-400 L18,-330 Z', grad('#7a4a3a'), 6)
         + path('M-15,-420 L-15,-395 M-24,-410 L-6,-410', sw=5) + rect(-60, -130, 30, 40, WARM2, 10, 5) + rect(30, -130, 30, 40, WARM2, 10, 5))
    return g(c, tr=f'translate({x},{base}) scale({s})')

def city(dark=False, rain=False, extra=''):
    sk = sky(moon=not rain)
    bl = ''.join(building(x, 1300, w, h, '#2c2150', seed=x, lit_frac=.05 if dark else .3) for x, w, h in
                 [(-300, 260, 700), (-60, 200, 520), (760, 240, 640), (980, 300, 820), (1250, 220, 500)])
    clouds = ''
    if rain:
        clouds = ''.join(ell(x, y, 260, 90, '#2a2140', extra='opacity=".9"') for x, y in [(100, 160), (420, 120), (760, 170), (1040, 130)])
        clouds += ''.join(path(f'M{x},{y} L{x - 40},{y + 140}', sw=4, stroke='#8f8fd0', extra='opacity=".5"') for x, y in
                          [(random.Random(i).randint(-200, 1300), random.Random(i * 3).randint(250, 1500)) for i in range(70)])
    return sk + clouds + bl + floor_(1300) + tower(dark=dark) + church(330, 1300, .8) + extra

def office(night=True):
    return (wall('#5a4590') + window_(120, 300, 380, 520) + window_(580, 300, 380, 520) + floor_(1250)
            + rect(80, 1060, 920, 60, grad('#8a5a3c'), 10, 8) + rect(120, 1120, 40, 200, shade('#8a5a3c'), 4, 6) + rect(920, 1120, 40, 200, shade('#8a5a3c'), 4, 6)
            + lamp(860, 880))

def joint(welds=False):
    beam = (rect(-400, 700, 1900, 260, grad('#7a8296', True), 0, 10) + path('M540,-400 L540,700', sw=0)
            + rect(400, -400, 280, 1100, grad('#6c7488'), 0, 10) + rect(330, 640, 420, 380, grad('#8a92a6'), 16, 10))
    bolts = ''.join(g(ell(0, 0, 34, 34, grad('#c0c6d4'), 7) + path('M-16,0 L16,0 M0,-16 L0,16', sw=6), f'bolt{i}', f'translate({x},{y})')
                    for i, (x, y) in enumerate([(400, 700), (540, 700), (680, 700), (400, 830), (540, 830), (680, 830), (400, 960), (540, 960), (680, 960)]))
    return wall('#2d2350', 2400) + beam + bolts + pool(540, 830, 500, 400)

def weather_map(hx=900, hy=1500):
    land = path('M-300,200 L380,200 Q420,500 360,760 Q300,980 420,1200 Q520,1400 430,1700 L-300,2200 Z', grad('#3f8a5a'), 9)
    sea = rect(-400, -400, W + 800, H + 800, '#2a5a9a', sw=0) + ''.join(path(f'M{x},{y} q30,-14 60,0 q30,14 60,0', sw=4, stroke='#4a7ac0') for x in range(-200, 1300, 220) for y in range(100, 1900, 160))
    city_dot = ell(380, 760, 26, 26, '#ff5a5a', 7) + text(420, 790, 'NEW YORK', 58, anchor='start')
    spiral = g(''.join(path(f'M{-r},0 a{r},{r} 0 1,1 {2 * r},0 a{r * .8},{r * .8} 0 1,1 {-r * 1.6},0', sw=26 - k * 4, stroke='#e8eefc', extra='opacity=".85"') for k, r in enumerate([170, 120, 75, 35])) + ell(0, 0, 22, 22, '#2a5a9a', 6), 'hur', f'translate({hx},{hy})')
    tv = rect(40, 140, 1000, 1640, 'none', 40, 30)
    return sea + land + city_dot + spiral + tv

def table_scene():
    t = (wall('#5a4590') + floor_(1250) + pool(540, 1250, 520, 220)
         + g(rect(200, 860, 680, 70, grad('#c08a5a'), 14, 9) + rect(510, 930, 60, 320, grad('#a0704a'), 6, 8) + rect(800, 930, 40, 280, shade('#a0704a'), 6, 7)
             + ell(360, 840, 60, 30, grad('#e0e0f0'), 7) + rect(620, 790, 90, 70, grad('#ff8a5a'), 10, 7), 'tbl', extra=''))
    return t

def outro():
    return (sky(moon=False) + floor_(1300) + pool(540, 1300, 600, 260)
            + candle('ca', 300, 900, 1.15, 'A', face='wow') + candle('cb', 780, 900, 1.15, 'B', face='smirk')
            + text(300, 570, 'TELL', 64) + text(300, 650, 'EVERYONE', 64) + text(780, 570, 'FIX IT', 64) + text(780, 650, 'IN SECRET', 64))

def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']

def shots(lines, total):
    S = []
    # 0 hook: tower sways in a storm, student points up
    stud = person('st', 760, 1420, .55, coat='#e05a7a', skin='d', hair='bob', eyes='wide', mouth='o')
    a0 = [setp('#tw', 0, rotation=0, transformOrigin='50% 100%')] + [move('#tw', .25 + i * .5, .5, 'sine.inOut', rotation=(2.4 if i % 2 == 0 else -2.4)) for i in range(9)]
    a0 += [arm('st', 'r', .4, -150), face('st', 1.6, 'wide', 'open')] + bob('st', 0, 4, 6, .4)
    S.append(Shot(0, L(1), city(rain=True, extra=stud), [(0, 1.5, 540, 420), (1.6, 1.15, 560, 700), (L(1), 1.0, 600, 960)], a0))
    # 1 the tower on stilts + church
    S.append(Shot(L(1), L(2), city(), [(0, 1.0, 540, 700), (1.6, 1.25, 540, 1050), (E(1) - L(1), 1.7, 420, 1170)], []))
    # 2 phone call: student at desk, engineer answers
    eng = person('en', 720, 1300, .95, coat='#3f5f9f', skin='a', glasses=True, hair='tuft', eyes='norm', mouth='smile')
    stu2 = person('s2', 330, 1300, .95, coat='#e05a7a', skin='d', hair='bob', eyes='norm', mouth='smile')
    phone = g(rect(-26, -50, 52, 100, '#2b2b3b', 12, 6) + rect(-18, -40, 36, 70, '#7fd0ff', 6, 0), 'ph', 'translate(420,1060) rotate(-15)')
    paper = g(rect(-120, -80, 240, 160, '#fdf6e3', 8, 6) + ''.join(path(f'M-90,{y} L{random.Random(y).randint(20, 90)},{y}', sw=5, stroke='#6a6aa0') for y in (-40, -10, 20, 50)), 'pp', 'translate(560,1040)')
    a2 = [arm('s2', 'r', .1, -120)] + talk('s2', .2, 3.4) + [face('en', L(3) - L(2), 'wide', 'o'), arm('en', 'l', L(3) - L(2), 80)] + bob('en', 0, 6, 5, .45) + blink('en', [1.0, 2.6])
    S.append(Shot(L(2), L(4), office() + stu2 + eng + phone, [(0, 1.25, 330, 1000), (2.0, 1.25, 400, 1000), (L(3) - L(2), 1.6, 700, 960), (E(3) - L(2), 1.75, 700, 920)], a2))
    # 3 bolts instead of welds
    a3 = []
    for i in range(9): a3 += [(0.3 + i * .25, f'tl.to("#bolt{i}",{{rotation:25,duration:.12,yoyo:true,repeat:5,transformOrigin:"50% 50%"}},{{T}});')]
    S.append(Shot(L(4), L(5), joint(), [(0, 1.0, 540, 800), (1.5, 1.4, 540, 830), (E(4) - L(4), 1.9, 600, 760)], a3))
    # 4 storm + power fails -> lights out
    a4 = [setp('#tw', 0, transformOrigin='50% 100%')] + [move('#tw', i * .55, .55, 'sine.inOut', rotation=(3.5 if i % 2 == 0 else -3)) for i in range(8)]
    S.append(Shot(L(5), L(6), city(rain=True, dark=False), [(0, 1.0, 540, 900), (E(5) - L(5), 1.35, 540, 700)], a4 + [setp('#s4dark', 1.2, opacity=.55)]))
    S[-1].svg += rect(-400, -400, W + 800, H + 800, '#0a0618', sw=0, extra='id="s4dark" opacity="0"')
    # 5 hurricane season starts now: calendar flip + engineer sweats
    cal = g(rect(-170, -220, 340, 400, '#fdf6e3', 16, 9) + rect(-170, -220, 340, 90, '#e05a5a', 16, 9) + text(0, -150, 'AUGUST', 56)
            + text(0, 40, 'STORM', 72, '#e05a5a') + text(0, 120, 'SEASON', 72, '#e05a5a'), 'cal', 'translate(540,640)')
    eng2 = person('e2', 540, 1450, 1.15, coat='#3f5f9f', skin='a', glasses=True, hair='tuft', eyes='wide', mouth='frown')
    drop = g(path('M0,0 Q16,26 0,40 Q-16,26 0,0 Z', '#9fd8ff', 5), 'drop', 'translate(640,1000)')
    a5 = [fromto('#cal', 0, .35, {'rotationX': 90, 'opacity': 0}, {'rotationX': 0, 'opacity': 1}), fromto('#drop', .4, 1.0, {'y': 0, 'opacity': 1}, {'y': 140, 'opacity': 0})]
    S.append(Shot(L(6), L(7), office() + cal + eng2 + drop, [(0, 1.1, 540, 800), (E(6) - L(6) + .1, 1.35, 540, 950)], a5))
    # 6 the choice: fix it at night
    eng3 = person('e3', 540, 1420, 1.15, coat='#3f5f9f', skin='a', glasses=True, hair='tuft', eyes='side', mouth='smirk')
    a6 = [arm('e3', 'r', .3, -160), face('e3', 1.2, 'side', 'grin')] + bob('e3', 0, 3, 6, .5)
    S.append(Shot(L(7), L(8), office() + eng3 + rect(-400, -400, W + 800, H + 800, '#140c26', sw=0, extra='id="s6n" opacity="0"'),
                  [(0, 1.3, 540, 980), (E(7) - L(7), 1.5, 540, 1000)], a6 + [move('#s6n', 1.4, .8, opacity=.45)]))
    # 7 night welding inside the walls, workers leave; morning
    wl = person('w1', 380, 1330, .9, coat='#c06a2a', skin='b', hat='welder', eyes='norm', mouth='flat')
    w2 = person('w2', 760, 1330, .9, coat='#7a8a3a', skin='c', hat='welder', eyes='norm', mouth='flat')
    walkers = person('k1', 100, 1450, .6, coat='#4f7cc9', skin='a', hair='tuft') + person('k2', 0, 1460, .6, coat='#c95f9a', skin='d', hair='bun')
    sc = joint() + rect(-400, -400, W + 800, H + 800, '#140c26', sw=0, extra='opacity=".35"') + sparks('sp1', 470, 830, seed=2) + sparks('sp2', 660, 960, seed=5) + wl + w2 + walkers
    a7 = spark_burst('sp1', .6, seed=2, reps=12, every=.38) + spark_burst('sp2', .8, seed=5, reps=12, every=.41)
    a7 += [move('#k1', 0, 2.2, 'none', x=-250), move('#k2', 0, 2.2, 'none', x=-350)] + bob('w1', 0, 5, 4, .3) + bob('w2', 0, 5, 4, .33)
    S.append(Shot(L(8), L(9), sc, [(0, 1.0, 540, 900), (1.6, 1.35, 470, 860), (3.2, 1.45, 660, 950), (E(8) - L(8), 1.2, 540, 900)], a7))
    # morning: offices open like nothing happened
    hap = person('h1', 300, 1330, .9, coat='#4f7cc9', skin='a', hair='tuft', eyes='happy', mouth='smile') + person('h2', 760, 1330, .9, coat='#c95f9a', skin='d', hair='bun', eyes='happy', mouth='grin')
    sun = rect(-400, -400, W + 800, H + 800, '#ffcf8a', sw=0, extra='opacity=".22"')
    S.append(Shot(L(9), L(10), office(night=False) + sun + hap + pool(540, 900, 600, 500), [(0, 1.2, 540, 1000), (E(9) - L(9), 1.05, 540, 950)],
                  bob('h1', 0, 2.5, 8, .35) + bob('h2', 0, 2.5, 8, .4) + [arm('h2', 'r', .3, -140), arm('h1', 'l', .5, 140)]))
    # 8 weather report: hurricane heads to NY
    a8 = [fromto('#hur', 0, E(10) - L(10) + .3, {'x': 0, 'y': 0, 'rotation': 0}, {'x': -170, 'y': -330, 'rotation': -540}, 'none')]
    S.append(Shot(L(10), L(11), weather_map(), [(0, 1.0, 540, 950), (E(10) - L(10), 1.25, 520, 900)], a8))
    # 9 secret evacuation plan, volunteers waiting on the street
    vols = ''.join(person(f'v{i}', 120 + i * 140, 1500 + (i % 2) * 40, .45, coat=['#e05a5a', '#4f7cc9', '#7a8a3a', '#c95f9a', '#c06a2a', '#3f5f9f', '#e0a040'][i % 7], skin='abcd'[i % 4],
                          hair=['tuft', 'bob', 'bun', None][i % 4], eyes='wide', mouth='o') for i in range(7))
    zone = rect(140, 980, 800, 330, '#ff5a5a', 20, 0, 'opacity=".22" id="zone"')
    a9 = [fromto('#zone', .2, .5, {'opacity': 0}, {'opacity': .35})] + sum((bob(f'v{i}', i * .07, 4, 5, .3 + i * .02) for i in range(7)), [])
    S.append(Shot(L(11), L(12), city(rain=True) + zone + vols, [(0, 1.0, 540, 1000), (2.0, 1.2, 540, 1150), (E(11) - L(11), 1.35, 500, 1350)], a9))
    # 10 table analogy: someone leans on the corner, it tips
    lean = person('ln', 950, 1330, .9, coat='#7a8a3a', skin='b', hair='tuft', eyes='norm', mouth='smile', flip=True)
    a10 = [setp('#tbl', 0, transformOrigin='540px 1250px'), arm('ln', 'r', 2.4, -70), move('#ln', 2.4, .5, x=-90),
           move('#tbl', 3.0, .35, 'power3.in', rotation=9), face('ln', 3.0, 'wide', 'open')]
    S.append(Shot(L(12), L(13), table_scene() + lean, [(0, 1.0, 540, 1000), (2.6, 1.35, 760, 980), (E(12) - L(12), 1.45, 700, 1040)], a10))
    # 11 welders keep going, storm closer
    S.append(Shot(L(13), L(14), joint() + rect(-400, -400, W + 800, H + 800, '#140c26', sw=0, extra='opacity=".45"') + sparks('sp3', 540, 830, seed=9)
                  + person('w3', 540, 1360, 1.0, coat='#c06a2a', skin='b', hat='welder'), [(0, 1.3, 540, 900), (E(13) - L(13), 1.6, 540, 860)],
                  spark_burst('sp3', 0, seed=9, reps=6, every=.3) + bob('w3', 0, 2, 4, .25)))
    # 12 the hurricane turns out to sea
    a12 = [fromto('#hur', 0, 2.0, {'x': -170, 'y': -330, 'rotation': 0}, {'x': 280, 'y': -380, 'rotation': -420}, 'power1.inOut')]
    S.append(Shot(L(14), L(15), weather_map(), [(0, 1.1, 600, 1100), (E(14) - L(14) + .4, 1.0, 640, 1000)], a12))
    # 13 repairs finish, secret for 17 years; people inside never knew
    zipped = person('e4', 540, 1450, 1.1, coat='#3f5f9f', skin='a', glasses=True, hair='tuft', eyes='side', mouth='flat')
    S.append(Shot(L(15), L(16), office() + zipped + text(600, 700, '17 YEARS', 130, WARM2, extra='id="yrs"'),
                  [(0, 1.0, 540, 900), (E(15) - L(15), 1.3, 540, 1000)], [fromto('#yrs', .8, .4, {'scale': .3, 'opacity': 0, 'transformOrigin': '50% 50%'}, {'scale': 1, 'opacity': 1}, 'back.out(3)'),
                                                                         arm('e4', 'r', .4, -150)]))
    S.append(Shot(L(16), L(17), city(), [(0, 1.6, 540, 600), (E(16) - L(16), 1.0, 540, 900)], [setp('#tw', 0, transformOrigin='50% 100%'), move('#tw', 2.5, .4, 'sine.inOut', rotation=1.5), move('#tw', 2.9, .6, 'sine.inOut', rotation=0)]))
    # 14 A/B candles + blow out
    a14 = [fromto('#ca', 0, .4, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'), fromto('#cb', .2, .4, {'y': 300, 'opacity': 0}, {'y': 0, 'opacity': 1}, 'back.out(2)'),
           move('#ca-flame', 1.2, .2, scale=1.4, transformOrigin='50% 100%'), move('#ca-flame', 1.4, .3, scale=1), move('#cb-flame', 2.0, .2, scale=1.4, transformOrigin='50% 100%'), move('#cb-flame', 2.2, .3, scale=1)]
    S.append(Shot(L(17), total, outro(), [(0, 1.0, 540, 950), (total - L(17), 1.12, 540, 1000)], a14))
    return S

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(17) - .3, 'flares': [(L(3), 'flare'), (L(6), 'shrink'), (L(10), 'shrink'), (L(14) + .9, 'flare')]}
if __name__ == '__main__':
    print(build(EP), TOTAL)

def audio():
    T = TOTAL; P = L(14)
    music = [('investigations.mp3', 0, 0, L(7), 0, (.02, .5)),
             ('fivearmies.mp3', 14, L(7) - .2, P - .25, 1, (.4, .25)),
             ('carefree.mp3', 0, P + 1.25, T, -1, (.4, 1.2)),
             ('/home/claude/work/oga/rain-long-thunder/rain-thunder.ogg', 0, 0, L(1) + .3, 4, (.01, .6)),
             ('/home/claude/work/oga/rain-long-thunder/rain-thunder.ogg', 6, L(5), L(6) + .5, 3, (.3, .6)),
             ('/home/claude/work/oga/rain-long-thunder/rain-thunder.ogg', 12, L(11), P - .3, 0, (.4, .3))]
    O = '100-cc0-sfx-2/sfx100v2_'
    sp = 'electricity-sound-effects-0/spark.wav'; csp = 'electricity-sound-effects-0/continuousspark.wav'
    sfx = [(O + 'thunder_01.ogg', 0.0, 0, .35, 4), ('whoosh-cinematic.mp3', L(1) - .15, -2),
           ('crank-movie-telephone-ringtone/crank_ringtone.mp3', L(2) - .1, -6, 0, 1.4),
           ('100-cc0-sfx/paper_01.ogg', L(3), -2), ('heartbeat-sounds/heartbeat_fast_0.wav', L(3) + .5, -2),
           ('100-cc0-metal-and-wood-sfx/metal_hit_01.ogg', L(4) + .3, -1), ('100-cc0-metal-and-wood-sfx/metal_hit_03.ogg', L(4) + 1.2, -2),
           ('100-cc0-metal-and-wood-sfx/keys_02.ogg', L(4) + 2.0, -3),
           (O + 'thunder_01.ogg', L(5) + .2, 0), (O + 'switch_01.ogg', L(5) + 1.2, 0),
           ('100-cc0-sfx/paper_03.ogg', L(6), 0), ('whoosh-short.mp3', L(7) - .1, -2), (O + 'switch_02.ogg', L(7) + 1.4, -3),
           ('sound-effects-pack/Footsteps/step2.wav', L(8) + .1, -6), ('sound-effects-pack/Footsteps/step3.wav', L(8) + .45, -6),
           ('100-cc0-sfx/door_close_01.ogg', L(9), -3), ('whoosh.mp3', L(9) - .1, -4),
           ('static/ScatterNoise1.mp3', L(10) - .05, -6, 0, .5), (O + 'air_02.ogg', L(10) + .3, -3),
           ('crowd-shoutingspeaking-ambience/crowd_shouting.ogg', L(11) + .2, -9, 3, 3.5),
           ('100-cc0-sfx-2/sfx100v2_wood_hit_01.ogg', L(12) + 3.0, 0), ('100-cc0-sfx/dishes_02.ogg', L(12) + 3.2, -2),
           (O + 'thunder_01.ogg', L(13) + .3, -1),
           ('impact-bass-1.mp3', P - .2, -2), ('whoosh-cinematic.mp3', P + .7, -3),
           ('100-cc0-sfx/plop_01.ogg', L(15) + .8, -3), ('whoosh-short.mp3', L(16) - .1, -4),
           ('whoosh.mp3', L(17) - .05, -3), ('fire-crackling/fire-1.ogg', L(17) + .1, -6, 0, 1.2),
           (O + 'air_01.ogg', T - 1.0, -1)]
    for k in range(10): sfx.append((sp if k % 2 else csp, L(8) + .6 + k * .38, -4))   # welding crackle on every spark burst
    for k in range(5): sfx.append((sp, L(13) + k * .3, -4))
    return music, sfx

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'mix':
    from mix import mix, mux
    mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
