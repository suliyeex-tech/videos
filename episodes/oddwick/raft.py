import sys, json; sys.path.insert(0, '/home/claude/videos/engine/oddwick')
from odd import *
from props2 import *

SLUG = '2026-11-18-133-days-alone-on-a-raft'
VO = json.load(open(f'/home/claude/work/{SLUG}/vo.json'))
TOTAL = round(VO['total'] + 3.3, 2)
def L(i): return VO['lines'][i]['start']
def E(i): return VO['lines'][i]['start'] + VO['lines'][i]['dur']
def D(i): return L(i + 1) - L(i)

def hud(prefix, day=None, food=None, water=None):
    """top status cards: DAY n, FOOD bar, WATER bar (bars in prefix-fb / prefix-wb, scaleX animatable)"""
    s = ''
    if day is not None: s += g(rect(-170, -60, 340, 110, '#140c26', 22, 7, 'fill-opacity=".75"') + text(0, 26, f'DAY {day}', 72, WARM2), f'{prefix}d', 'translate(540,520)')
    def bar(lbl, y, col, bid, v):
        return (text(250, y + 22, lbl, 54, anchor='end') + rect(280, y - 26, 520, 56, '#140c26', 20, 6, 'fill-opacity=".7"')
                + rect(286, y - 20, 508 * v, 44, col, 16, 0, f'id="{bid}"'))
    if food is not None: s += bar('FOOD', 650, '#ffb35c', f'{prefix}fb', food)
    if water is not None: s += bar('WATER', 730, '#7fd0ff', f'{prefix}wb', water)
    return s
def sailor_close(pid, x, y, s=1, eyes='norm', mouth='smile'):
    return person(pid, x, y, s, coat='#e8e0d0', skin='b', hair='tuft', eyes=eyes, mouth=mouth)
def rock(sel, t0, d, amp=4, period=1.4):
    out = []
    for k in range(int(d / (period / 2))):
        out.append((t0 + k * period / 2, f'tl.to("{sel}",{{rotation:{amp if k % 2 == 0 else -amp},y:{-10 if k % 2 == 0 else 6},duration:{period / 2:.2f},ease:"sine.inOut",transformOrigin:"50% 100%"}},{{T}});'))
    return out

def shots(lines, total):
    S = []
    # 0 hook: ship sinks in the night (explosion flash, tilts under), the raft in front; FOOD 50 vs NEED 133
    boom = ell(0, 0, 260, 200, 'url(#glow)', extra='id="boom" opacity="0"')
    a = [fromto('#boom', .1, .6, {'opacity': 1, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 0, 'scale': 2.2}, 'power2.out'),
         move('#shp', .3, 2.0, 'power2.in', rotation=24, y=420, transformOrigin='50% 50%'), setp('#shp', 2.4, opacity=0)]
    a += rock('#rf', 0, D(0), 3) + [fromto('#n50', D(0) * .45, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'),
                                     fromto('#n133', D(0) * .78, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    S.append(Shot(0, L(1), night_sea(1150) + ship('shp', 620, 1120, .75) + g(boom, tr='translate(560,1050)') + raft('rf', 520, 1520, 1.15, eyes='wide', mouth='o') + waves_front('wv', 1600)
                  + badge('n50', 540, 540, 'FOOD: 50 DAYS', '#ffb35c', 62) + badge('n133', 540, 680, 'NEED: 133 DAYS', '#e05a5a', 62),
                  [(0, 1.0, 600, 1050), (1.8, 1.35, 520, 1350), (D(0) * .45, 1.05, 540, 820), (D(0), 1.1, 540, 900)], a))
    # 1 the ship's steward, middle of the Atlantic, can't really swim (tiny raft on a huge sea)
    mapc = g(rect(-200, -140, 400, 280, '#e8d8a0', 20, 8) + path('M-150,-80 Q-120,-120 -60,-100 L-80,40 Q-140,60 -160,0 Z', '#7aa060', 5) + path('M90,-110 Q160,-60 140,40 L90,90 Q60,0 80,-60 Z', '#7aa060', 5)
            + ell(10, 0, 16, 16, '#e05a5a', 5) + text(0, 120, 'ATLANTIC', 44, OUT, extra='stroke-width="0"'), 'map', 'translate(780,700)', 'opacity="0"')
    a = rock('#rf', 0, D(1), 4) + [fromto('#map', .6, .4, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(2)'),
                                    arm('rfp', 'l', D(1) * .65, 160), arm('rfp', 'r', D(1) * .65, -160), face('rfp', D(1) * .65, 'wide', 'frown')]
    S.append(Shot(L(1), L(2), night_sea(1000) + raft('rf', 540, 1180, .6) + waves_front('wv', 1500) + mapc,
                  [(0, 1.0, 540, 1000), (1.5, 1.2, 700, 800), (D(1) * .6, 1.6, 540, 1080), (D(1), 1.3, 540, 1050)], a))
    # 2 rope from the raft to his wrist, every single day (close-up)
    ropep = path('M200,1500 Q420,1300 560,1180', sw=18, stroke='#c9a06a', extra='id="rope" stroke-dasharray="900" stroke-dashoffset="900"')
    a = [(.2, 'tl.to("#rope",{strokeDashoffset:0,duration:1.0,ease:"power2.out"},{T});'), arm('sc', 'r', .2, -60), face('sc', 1.4, 'shut', 'smile')] + rock('#scw', 0, D(2), 2, 1.6)
    S.append(Shot(L(2), L(3), night_sea(900) + g(sailor_close('sc', 540, 1900, 2.2) + rect(-400, 1500, 1900, 600, grad('#a8743c', True), 0, 8), 'scw') + ropep + ell(565, 1175, 34, 26, 'none', 10, 'stroke="#c9a06a"'),
                  [(0, 1.0, 540, 1100), (1.2, 1.45, 520, 1250), (D(2), 1.25, 540, 1150)], a))
    # 3 food runs out (day 55), water ~15 days later (day 70): bars drain
    a = [fromto('#h3fb', .2, 1.4, {'scaleX': 1, 'transformOrigin': '0% 50%'}, {'scaleX': 0}, 'power1.in'), fromto('#h3wb', D(3) * .55, 1.2, {'scaleX': 1, 'transformOrigin': '0% 50%'}, {'scaleX': 0}, 'power1.in'),
         fromto('#d55', .2, .25, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'), setp('#d55', D(3) * .55, opacity=0),
         fromto('#d70', D(3) * .55, .25, {'opacity': 0, 'scale': .4, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'), face('rfp', D(3) * .6, 'wide', 'frown')] + rock('#rf', 0, D(3), 3)
    tin = ''.join(g(rect(-40, -60, 80, 60, grad('#b0b8c8'), 8, 6), tr=f'translate({-200 + k * 120},-50) rotate({k * 20 - 30})') for k in range(4))
    S.append(Shot(L(3), L(4), night_sea(1150) + raft('rf', 540, 1520, 1.0, mouth='flat', extra=tin) + waves_front('wv', 1640)
                  + hud('h3', None, 1, 1) + badge('d55', 540, 520, 'DAY 55', '#ffb35c', 80) + badge('d70', 540, 520, 'DAY 70', '#7fd0ff', 80),
                  [(0, 1.0, 540, 900), (1.6, 1.1, 540, 700), (D(3) * .6, 1.1, 540, 760), (D(3), 1.15, 540, 1100)], a))
    # 4 he pulls a nail out of the raft and bends it into a fishing hook (big close-up)
    plank = rect(-200, 1250, 1480, 220, grad('#a8743c', True), 14, 9) + ''.join(path(f'M-200,{1300 + k * 60} L1280,{1300 + k * 60}', sw=4, stroke='#7a5228') for k in range(3))
    nail = g(rect(-14, -260, 28, 260, grad('#c8ccd8'), 6, 6) + rect(-40, -280, 80, 26, grad('#c8ccd8'), 8, 6), 'nail', 'translate(540,1330)')
    hook = g(path('M0,-260 L0,-40 Q0,40 -70,40 Q-130,40 -130,-30', sw=26, stroke=OUT) + path('M0,-260 L0,-40 Q0,40 -70,40 Q-130,40 -130,-30', sw=14, stroke='#d8dce8') + path('M-130,-30 L-150,-70 L-100,-50 Z', '#d8dce8', 6), 'hook', 'translate(560,1100)', 'opacity="0"')
    tb = D(4) * .55
    a = [move('#nail', .3, 1.2, 'power3.in', y=-280), (1.4, 'tl.to("#nail",{rotation:8,duration:.06,yoyo:true,repeat:5},{T});'), move('#nail', tb - .1, .2, opacity=0),
         fromto('#hook', tb, .4, {'opacity': 0, 'scale': .5, 'rotation': -40, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1, 'rotation': 0}, 'back.out(3)')]
    a += [fromto('#hand', .2, .3, {'y': 300}, {'y': 0}), move('#hand', .3, 1.2, 'power3.in', y=-280)]
    hand = g(ell(0, 0, 90, 70, grad(SKIN['b']), 9) + ell(-60, -40, 30, 40, grad(SKIN['b']), 7), 'hand', 'translate(540,1040)')
    S.append(Shot(L(4), L(5), night_sea(800) + plank + nail + hand + hook,
                  [(0, 1.1, 540, 1150), (1.4, 1.5, 540, 1050), (tb, 1.35, 560, 1050), (D(4), 1.6, 560, 1060)], a))
    # 5 rope -> fishing line, biscuit crumbs -> bait
    a = [(.1, 'tl.fromTo("#line",{strokeDashoffset:1100},{strokeDashoffset:0,duration:1.0,ease:"power2.out"},{T});'), fromto('#bis', D(5) * .5, .3, {'opacity': 0, 'y': -100}, {'opacity': 1, 'y': 0}, 'bounce.out')]
    a += [fromto(f'#cr{k}', D(5) * .55 + k * .12, .4, {'opacity': 1, 'y': -60}, {'opacity': 1, 'y': 0}, 'bounce.out') for k in range(5)]
    bis = g(rect(-110, -70, 220, 140, grad('#e0b070'), 20, 8) + ''.join(ell(-60 + (k % 3) * 60, -20 + (k // 3) * 40, 8, 8, '#a8743c') for k in range(6)), 'bis', 'translate(300,900)', 'opacity="0"')
    crumbs = ''.join(ell(0, 0, 12, 10, '#e0b070', 4, f'id="cr{k}"') for k in range(5)).replace('cx="0"', 'cx="0"')
    crumbs = ''.join(g(ell(0, 0, 12, 10, '#e0b070', 4), f'cr{k}', f'translate({600 + k * 18},{1180 + (k % 2) * 14})', 'opacity="0"') for k in range(5))
    S.append(Shot(L(5), L(6), night_sea(800) + path('M540,300 Q380,800 560,1100', sw=10, stroke='#c9a06a', extra='id="line" stroke-dasharray="1100" stroke-dashoffset="1100"')
                  + g(path('M0,0 L0,40 Q0,80 -40,80 Q-70,80 -70,50', sw=12, stroke='#d8dce8'), tr='translate(560,1100)') + bis + crumbs,
                  [(0, 1.1, 540, 800), (1.6, 1.4, 420, 1000), (D(5), 1.5, 600, 1150)], a))
    # 6 little fish catch bigger fish; rain fills the jacket; a gull lands... dinner
    d6 = D(6); t1 = d6 * .36; t2 = d6 * .66
    a = [fromto('#f1', 0, 1.0, {'x': -300}, {'x': 200}, 'none'), fromto('#f2', .6, .8, {'x': 700, 'opacity': 0}, {'x': 260, 'opacity': 1}, 'power2.out'), move('#f1', 1.4, .1, opacity=0), (1.4, 'tl.fromTo("#f2",{scale:1},{scale:1.15,duration:.15,yoyo:true,repeat:1,transformOrigin:"50% 50%"},{T});')]
    a += rain_fall('rn', t1, t2 - t1 + .2) + [fromto('#jk', t1, t2 - t1, {'scaleY': .2, 'transformOrigin': '50% 100%'}, {'scaleY': 1})]
    a += [fromto('#gl', t2, .8, {'x': 600, 'y': -500}, {'x': 0, 'y': 0}, 'power2.out'), (t2, 'tl.to("#gl-w",{rotation:-30,duration:.12,yoyo:true,repeat:5,transformOrigin:"100% 100%"},{T});'),
          fromto('#yum', d6 - .9, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'), face('rfp', d6 - .9, 'happy', 'grin')]
    jacket = g(rect(-90, -110, 180, 110, grad('#ff8a3a'), 20, 8) + rect(-78, -100, 156, 100, '#7fd0ff', 16, 0, 'id="jk"'), tr='translate(760,1480)')
    S.append(Shot(L(6), L(7), night_sea(1150) + fish('f1', 300, 1700, .6, '#9ad0ff') + fish('f2', 300, 1720, 1.1, '#ffb35c') + raft('rf', 520, 1520, 1.0) + jacket + gull('gl', 700, 1330, .8)
                  + waves_front('wv', 1640) + rain('rn') + badge('yum', 540, 640, 'DINNER', '#ffd27a', 90),
                  [(0, 1.3, 300, 1600), (t1, 1.25, 700, 1300), (t2, 1.2, 640, 1250), (d6, 1.1, 540, 1000)], a))
    # 7 a ship passes close; he waves and screams; it keeps going
    a = [move('#sh2', 0, D(7), 'none', x=1700)] + [arm('rfp', 'l', .4, 160), arm('rfp', 'r', .4, -160), face('rfp', .4, 'wide', 'open')] + sum(([arm('rfp', 'r', .7 + k * .5, -110), arm('rfp', 'r', .95 + k * .5, -170)] for k in range(5)), []) + [face('rfp', D(7) - .8, 'shut', 'frown')]
    S.append(Shot(L(7), L(8), night_sea(1100) + ship('sh2', -700, 1090, .55, lit_=True) + raft('rf', 600, 1520, 1.0) + waves_front('wv', 1640),
                  [(0, 1.1, 400, 1100), (1.4, 1.3, 600, 1350), (2.8, 1.2, 800, 1100), (D(7), 1.3, 600, 1300)], a))
    # 8 a plane flies over, drops a marker... then a storm blows him away from it
    tsto = D(8) * .5
    a = [move('#pl', 0, 2.2, 'none', x=1900), fromto('#mk', 1.0, .8, {'y': -700, 'opacity': 1}, {'y': 0, 'opacity': 1}, 'power1.in'),
         fromto('#storm', tsto, .4, {'opacity': 0}, {'opacity': .55}), move('#rf', tsto, D(8) - tsto, 'power1.in', x=-700, rotation=-14)]
    a += rain_fall('rn', tsto, D(8) - tsto) + [setp('#ltn', tsto + .3, opacity=.9), setp('#ltn', tsto + .38, opacity=0), setp('#ltn', tsto + .9, opacity=.7), setp('#ltn', tsto + .96, opacity=0)]
    marker = g(path('M0,0 L0,-80', sw=8) + path('M0,-80 L60,-60 L0,-40 Z', '#e05a5a', 5) + ell(0, 0, 30, 14, '#ffd27a', 6), 'mk', 'translate(900,1500)', 'opacity="0"')
    S.append(Shot(L(8), L(9), night_sea(1150) + plane('pl', -500, 500, .9) + marker + raft('rf', 520, 1520, 1.0, eyes='wide', mouth='o') + waves_front('wv', 1640)
                  + rect(-400, -400, 1900, 2800, '#140c26', sw=0, extra='id="storm" opacity="0"') + rain('rn', 110, 8) + rect(-400, -400, 1900, 2800, '#eaf2ff', sw=0, extra='id="ltn" opacity="0"'),
                  [(0, 1.0, 300, 700), (1.2, 1.15, 800, 1200), (tsto, 1.2, 600, 1300), (D(8), 1.0, 300, 1200)], a))
    # 9 he hooks a shark and it fights back, right on the raft
    a = [fromto('#sk', 0, .6, {'y': 500, 'rotation': 30}, {'y': 0, 'rotation': -10}, 'back.out(1.5)')] + [(0.7 + k * .3, f'tl.to("#sk",{{rotation:{8 if k % 2 else -12},x:{20 if k % 2 else -20},duration:.15}},{{T}});') for k in range(int((D(9) - .8) / .3))]
    a += rock('#rf', .6, D(9) - .6, 9, .5) + [face('rfp', .5, 'wide', 'open'), arm('rfp', 'l', .5, 150), arm('rfp', 'r', .5, -150)]
    S.append(Shot(L(9), L(10), night_sea(1150) + raft('rf', 420, 1520, 1.1) + shark('sk', 760, 1440, .7) + waves_front('wv', 1640),
                  [(0, 1.2, 640, 1400), (1.2, 1.45, 700, 1350), (2.4, 1.3, 500, 1300), (D(9), 1.4, 600, 1350)], a))
    # 10 he wins with the water jug; the shark's liver -> something to drink
    jug = g(rect(-60, -140, 120, 140, grad('#7a8aa0'), 20, 8) + rect(-26, -170, 52, 40, grad('#7a8aa0'), 8, 7), 'jug', 'translate(110,-300)')
    a = [fromto('#jug', .1, .3, {'rotation': 0, 'transformOrigin': '50% 100%'}, {'rotation': -60}, 'power2.in'), fromto('#jug', .4, .2, {'rotation': -60}, {'rotation': 30}, 'power3.in'),
         move('#sk2', .55, .4, rotation=90, y=120, opacity=.0), face('sw', .7, 'happy', 'grin'), fromto('#drop', D(10) * .55, .4, {'opacity': 0, 'y': -60}, {'opacity': 1, 'y': 0}, 'bounce.out')]
    S.append(Shot(L(10), L(11), night_sea(1150) + g(person('sw', 0, 0, 1.3, coat='#e8e0d0', skin='b', hair='tuft', eyes='angry', mouth='flat', extra_acc=jug), tr='translate(380,1560)')
                  + shark('sk2', 820, 1500, .6) + waves_front('wv', 1660) + g(path('M0,-90 Q60,0 0,40 Q-60,0 0,-90 Z', '#c0404a', 8), 'drop', 'translate(800,800)', 'opacity="0"') + text(800, 980, 'DRINK', 80, extra='id="dt" opacity="0"'),
                  [(0, 1.3, 400, 1250), (1.0, 1.15, 600, 1200), (D(10) * .55, 1.3, 800, 900), (D(10), 1.1, 600, 1100)], a + [move('#dt', D(10) * .6, .2, opacity=1)]))
    # 11 you see: out there the deadline is water, not food -> every thing becomes a tool (4 icons pop in)
    icons = [g(rect(-14, -110, 28, 160, grad('#c8ccd8'), 6, 6), tr='translate(0,30)'), path('M-90,0 Q-45,-60 0,0 Q45,60 90,0', sw=18, stroke='#c9a06a'),
             g(rect(-60, -80, 120, 140, grad('#7a8aa0'), 20, 8), tr=''), g(rect(-80, -70, 160, 130, grad('#ff8a3a'), 20, 8), tr='')]
    names = ['NAIL', 'ROPE', 'JUG', 'JACKET']
    tiles = ''.join(g(rect(-170, -170, 340, 340, '#fdfcf8', 30, 9) + icons[k] + text(0, 140, names[k], 56, OUT, extra='stroke-width="0"'), f'ic{k}', f'translate({310 + (k % 2) * 460},{820 + (k // 2) * 380})', 'opacity="0"') for k in range(4))
    t4 = D(11) * .5
    a = [fromto('#wf', .2, .35, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')] + seq_show([f'ic{k}' for k in range(4)], t4, (D(11) - t4 - .4) / 4)
    S.append(Shot(L(11), L(12), wall('#2a3a6a', 2400) + pool(540, 1200, 700, 700) + badge('wf', 540, 440, 'WATER > FOOD', '#7fd0ff', 90) + tiles,
                  [(0, 1.15, 540, 560), (t4 - .3, 1.0, 540, 900), (t4 + 1.5, 1.1, 440, 900), (t4 + 3.0, 1.1, 640, 1000), (D(11), 1.0, 540, 960)], a))
    # 12 day 133: three fishermen find him near Brazil; drifted 1,000+ km
    boat = g(path('M-300,0 L300,0 L240,110 L-260,110 Z', grad('#3a8a7a'), 9) + ''.join(person(f'fm{k}', -170 + k * 150, 0, .45, coat=['#e0b040', '#c06a2a', '#4f7cc9'][k], skin='c', hat='cap', eyes='happy', mouth='grin') for k in range(3)), 'bt', 'translate(760,1430)')
    coast = path('M-400,1150 Q200,1080 500,1150 L500,1160 L-400,1160 Z', '#3a6a4a', 7) + ''.join(g(path('M0,0 L10,-150', sw=14, stroke='#7a5228') + path('M10,-150 Q-60,-170 -90,-120 M10,-150 Q80,-180 110,-120 M10,-150 Q-20,-210 -60,-210 M10,-150 Q50,-210 90,-200', sw=12, stroke='#4a8a5a'), tr=f'translate({x0},1120)') for x0 in (40, 240))
    a = [fromto('#bt', 0, 1.2, {'x': 600}, {'x': 0}, 'power2.out')] + [arm(f'fm{k}', 'r', 1.2 + k * .1, -160) for k in range(3)] + rock('#rf', 0, D(12), 3)
    a += [fromto('#d133', .2, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)'), fromto('#km', D(12) * .6, .3, {'opacity': 0, 'scale': .3, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1}, 'back.out(3)')]
    S.append(Shot(L(12), L(13), night_sea(1150) + coast + raft('rf', 300, 1520, .9, mouth='grin', eyes='happy', canopy=True) + boat + waves_front('wv', 1660)
                  + badge('d133', 540, 520, 'DAY 133', '#5fd36a', 100) + badge('km', 540, 720, '1,000+ KM', '#ffd27a', 80),
                  [(0, 1.0, 540, 1100), (1.6, 1.2, 600, 1250), (D(12) * .6, 1.1, 540, 820), (D(12), 1.1, 400, 1200)], a))
    # 13 'nobody ever survived that long on a raft' -> medal
    medal = g(path('M-60,-260 L0,-120 L60,-260', sw=30, stroke='#c0404a') + ell(0, 0, 140, 140, grad('#ffd27a'), 10) + text(0, 30, '133', 90, OUT, extra='stroke-width="0"'), 'md', 'translate(540,700)', 'opacity="0"')
    a = [fromto('#md', .3, .5, {'opacity': 0, 'scale': .2, 'rotation': -30, 'transformOrigin': '50% 50%'}, {'opacity': 1, 'scale': 1, 'rotation': 0}, 'back.out(2)')] + talk('fm1', .2, D(13) - .5)
    S.append(Shot(L(13), L(14), wall('#5a3a2a', 1300) + floor_(1300, '#6a4a3a') + lamp(900, 800) + medal + person('fm1', 280, 1520, 1.0, coat='#c06a2a', skin='c', hat='cap', eyes='happy', mouth='smile')
                  + sailor_close('sp', 760, 1540, 1.0, 'norm', 'smile'), [(0, 1.0, 540, 1000), (1.4, 1.3, 540, 760), (D(13), 1.2, 760, 1150)], a))
    # 14 the quote: soft close-up, warm light, he smiles
    a = [face('sp', .2, 'happy', 'smile'), fromto('#warm', 0, 1.0, {'opacity': 0}, {'opacity': 1})] + talk('sp', .3, D(14) - .7, .15)
    S.append(Shot(L(14), L(15), wall('#5a3a2a', 2400) + ell(540, 1000, 700, 700, 'url(#pool)', extra='id="warm" opacity="0"') + lamp(900, 700) + sailor_close('sp', 540, 1800, 2.1, 'norm', 'smile'),
                  [(0, 1.0, 540, 1050), (D(14), 1.3, 540, 980)], a))
    # 15 A/B
    S.append(Shot(L(15), total, outro('SAVE THE', 'FOOD', 'SAVE THE', 'ROPE'), [(0, 1.0, 540, 950), (total - L(15), 1.12, 540, 1000)], outro_anims()))
    return S

EP = {'slug': SLUG, 'total': TOTAL, 'shots': shots, 'outro_t': L(15) - .3,
      'flares': [(0.2, 'flare'), (L(3) + 1.6, 'shrink'), (L(4) + D(4) * .55, 'flare'), (L(8) + D(8) * .5, 'shrink'), (L(9) + .3, 'shrink'), (L(12) + .3, 'flare')]}

def audio():
    T = TOTAL; Q = L(14)
    music = [('Celtic_Impulse.mp3', 8, 0, L(3), -1, (.02, .4)),
             ('Achaidh_Cheide.mp3', 0, L(3), L(7) - .05, -1, (.3, .3)),
             ('Lightless_Dawn.mp3', 30, L(7), L(11), 0, (.2, .3)),
             ('Despair_and_Triumph.mp3', 0, L(11), Q - .5, -2, (.2, .3)),
             ('Heroic_Age.mp3', 0, Q + .2, T, -3, (1.0, 1.2))]
    O = '100-cc0-sfx/'; O2 = '100-cc0-sfx-2/sfx100v2_'; SW = 'swishes-sound-pack/swishes/swish-'; WV = 'beach-ocean-waves/wave_0%d_cc0-18363__jasinski__alkaibeach.flac'; SP = '40-cc0-water-splash-slime-sfx/'
    sfx = [('battle-at-sea/ship_destroyed_1.ogg', 0.0, 0, 0, 3.0), ('war-on-water-sndfx/Guns/torpedo1.ogg', 0.05, -3), ('war-on-water-sndfx/Ships/shipsink.ogg', .8, -4, 0, 2.6),
           (WV % 1, 0.5, -10, 0, D(0)), (SP + 'splash_10.ogg', 2.2, -3)]
    sfx += [(WV % 2, L(1), -9, 0, D(1)), ('solo-seagull-sound-effects/Seagull Ambient 1.wav', L(1) + .6, -10), (SP + 'splash_02.ogg', L(1) + D(1) * .65, -5),
            (O + 'other_02.ogg', L(2) + .2, -6), ('wood-wobbling-rattling/montageAudio-20110719@161647.mp3', L(2) + .3, -9, 0, 1.2), (WV % 3, L(2), -12, 0, D(2)),
            (O + 'metal_04.ogg', L(3) + .3, -6), (O + 'metal_05.ogg', L(3) + .7, -7), (O2 + 'glass_02.ogg', L(3) + D(3) * .55, -8), (WV % 4, L(3), -12, 0, D(3)),
            ('75-cc0-breaking-falling-hit-sfx/bfh1_wood_breaking_01.ogg', L(4) + 1.2, -3), (O + 'metal_09.ogg', L(4) + 1.5, -5), (O + 'metal_12.ogg', L(4) + D(4) * .55, -2),
            (SW + '3.wav', L(5) - .1, -5), (O + 'paper_03.ogg', L(5) + .3, -5), (O + 'plop_01.ogg', L(5) + D(5) * .5, -4), (O + 'plop_02.ogg', L(5) + D(5) * .55 + .3, -6),
            (SP + 'splash_04.ogg', L(6) + .2, -4), (SP + 'splash_06.ogg', L(6) + 1.4, -3), ('rain-long-thunder/rain-thunder.ogg', L(6) + D(6) * .36, -6, 2, D(6) * .32),
            ('solo-seagull-sound-effects/Seagull Big Hit.wav', L(6) + D(6) * .66, -2), ('solo-seagull-sound-effects/Seagull Ambient 3.wav', L(6) + D(6) * .7, -6), (O + 'dishes_01.ogg', L(7) - .9, -7),
            ('war-on-water-sndfx/Ships/friendlyship.ogg', L(7), -5, 0, D(7)), (WV % 1, L(7), -12, 2, D(7)),
            ('war-on-water-sndfx/Airplanes/airplane1.ogg', L(8), -3, 0, 2.4), (SP + 'splash_01.ogg', L(8) + 1.8, -5), ('rain-long-thunder/rain-thunder.ogg', L(8) + D(8) * .5, -1, 6, D(8) * .5),
            ('100-cc0-sfx-2/sfx100v2_thunder_01.ogg', L(8) + D(8) * .5 + .3, 0),
            (SP + 'splash_12.ogg', L(9) + .1, 0), ('75-cc0-breaking-falling-hit-sfx/bfh1_wood_hit_01.ogg', L(9) + .7, -3), (SP + 'splash_08.ogg', L(9) + 1.3, -3), (SP + 'slime_05.ogg', L(9) + 1.9, -5),
            ('75-cc0-breaking-falling-hit-sfx/bfh1_hit_06.ogg', L(10) + .45, 0), (SP + 'splash_13.ogg', L(10) + .7, -4), (O + 'plop_02.ogg', L(10) + D(10) * .55, -5),
            (SW + '9.wav', L(11) - .1, -4), (O + 'spring_04.ogg', L(11) + .2, -6)]
    t4 = D(11) * .5; ev = (D(11) - t4 - .4) / 4
    sfx += [(O + 'switch_0%d.ogg' % (1 + k % 2), L(11) + t4 + k * ev, -3) for k in range(4)]
    sfx += [(WV % 2, L(12), -9, 0, D(12)), ('war-on-water-sndfx/Pirates/motorboat1.ogg', L(12), -8, 0, 1.6), ('crowd-shoutingspeaking-ambience/crowd_shouting.ogg', L(12) + 1.2, -12, 0, 1.6),
            ('solo-seagull-sound-effects/Seagull Ambient 5.wav', L(12) + 1.8, -9), (O + 'bell_02.ogg', L(12) + .2, -8),
            ('applause-in-a-large-hall-or-church/applause-clapping-church-crowd-immersive.wav', L(13) + .3, -12, 1, 1.8), (O + 'bell_03.ogg', L(13) + .4, -8),
            ('fire-crackling/fire-1.ogg', Q, -12, 2, D(14)), (SW + '1.wav', L(15) - .05, -3), ('fire-crackling/fire-1.ogg', L(15) + .1, -6, 0, 1.2), (O2 + 'air_01.ogg', T - 1.0, -1)]
    return music, sfx

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mix':
        from mix import mix
        mu, sx = audio(); mix(SLUG, TOTAL, mu, sx)
    else: print(build(EP), TOTAL)
