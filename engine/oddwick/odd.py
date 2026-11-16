"""Oddwick Shorts engine (PLAYBOOK 2026-11-15): HyperFrames HTML generated from a Python episode.
Own recurring cast ("Wickfolk": tall wax-capsule people with stub arms), lit toon sets, gliding camera,
1-2 word captions, Oddwick the candle host. Episode modules call:  odd.build(EP) where EP has
SLUG, VOICE(json path), SHOTS [(line_from, line_to_incl, scene_fn, cam_keys, extra)], SFX, MUSIC, OUTRO.
Pipeline: build -> work/<slug>/hf/index.html -> render (npx hyperframes render) -> mix audio -> mux.
"""
import json, os, math, random, subprocess, html

W, H = 1080, 1920
OUT = '#1d1430'          # outline (avatar palette)
WARM = '#ffb35c'; WARM2 = '#ffd27a'; NIGHT = '#241a3d'; NIGHT2 = '#3a2560'; COOL = '#4b3a8c'

# ---------------------------------------------------------------- helpers
def _c(h):
    h = h.lstrip('#'); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
def _h(c): return '#%02x%02x%02x' % tuple(max(0, min(255, int(v))) for v in c)
def mix(a, b, t): a, b = _c(a), _c(b); return _h([a[i] + (b[i] - a[i]) * t for i in range(3)])
def lit(c, t=.35): return mix(c, '#fff1d6', t)          # warm light side
def shade(c, t=.45): return mix(c, '#2a1f5c', t)        # cool shadow side

_GR = {}
def grad(c, vertical=False):
    """horizontal gradient: warm-lit left -> cool shadow right (light comes from the candle side)"""
    key = (c, vertical)
    if key not in _GR:
        gid = f'g{len(_GR)}'
        x2, y2 = ('0', '1') if vertical else ('1', '0')
        _GR[key] = (gid, f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{lit(c)}"/>'
                         f'<stop offset=".55" stop-color="{c}"/><stop offset="1" stop-color="{shade(c)}"/></linearGradient>')
    return f'url(#{_GR[key][0]})'
def defs():
    return '<defs>' + ''.join(v[1] for v in _GR.values()) + '''
<radialGradient id="pool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffc77a" stop-opacity=".55"/><stop offset="1" stop-color="#ffc77a" stop-opacity="0"/></radialGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffe2a0" stop-opacity=".95"/><stop offset=".4" stop-color="#ff9a4d" stop-opacity=".45"/><stop offset="1" stop-color="#ff9a4d" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#140c26" stop-opacity="0"/><stop offset="1" stop-color="#140c26" stop-opacity=".75"/></radialGradient>
<radialGradient id="gas" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#c8d66a" stop-opacity=".85"/><stop offset="1" stop-color="#9aa84a" stop-opacity="0"/></radialGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1233"/><stop offset=".55" stop-color="#3a2560"/><stop offset=".85" stop-color="#8a3f6e"/><stop offset="1" stop-color="#ff9a4d"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b2a6b"/><stop offset="1" stop-color="#1f1640"/></linearGradient>
</defs>'''

def ell(cx, cy, rx, ry, fill, sw=0, extra=''):
    s = f' stroke="{OUT}" stroke-width="{sw}"' if sw else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{s} {extra}/>'
def rect(x, y, w, h, fill, r=0, sw=6, extra=''):
    s = f' stroke="{OUT}" stroke-width="{sw}"' if sw else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s} {extra}/>'
def path(d, fill='none', sw=6, extra='', stroke=OUT):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if sw else ''
    return f'<path d="{d}" fill="{fill}"{s} {extra}/>'
def text(x, y, s, size=60, fill='#fff', weight=900, anchor='middle', extra='', font='Montserrat'):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-weight="{weight}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" stroke="{OUT}" stroke-width="{max(4, size // 9)}" paint-order="stroke" {extra}>{html.escape(s)}</text>')
def _close_fix(svg): return svg   # wrappers are closed by g() itself (see below)
def g(inner, id=None, tr=None, extra=''):
    if id and tr:   # outer placement group + inner animated group, so GSAP transforms are relative to the placement
        return f'<g transform="{tr}"><g id="{id}" {extra}>{inner}</g></g>'
    a = f' id="{id}"' if id else ''
    t = f' transform="{tr}"' if tr else ''
    return f'<g{a}{t} {extra}>{inner}</g>'

# ---------------------------------------------------------------- the Wickfolk cast
SKIN = {'a': '#f6d2b0', 'b': '#c98d62', 'c': '#8a5a3c', 'd': '#f2c49a'}
def person(pid, x, y, s=1.0, coat='#4f7cc9', skin='a', hat=None, hair=None, mustache=False, glasses=False,
           coatlen=.55, eyes='norm', mouth='smile', flip=False, extra_acc='', tall=1.0):
    """A Wickfolk: one tall rounded capsule (head and body are one shape), stub arms, short legs.
    States: eyes norm|wide|happy|angry|shut|side, mouth smile|open|flat|grin|o|frown. Animated ids: pid-b (body),
    pid-al / pid-ar (arms), pid-e-<state>, pid-m-<state>."""
    sk = SKIN.get(skin, skin); hgt = 300 * tall; top = -hgt; wd = 82
    body = f'M{-wd},{-40} L{-wd},{top + wd} A{wd},{wd} 0 0 1 {wd},{top + wd} L{wd},-40 Q{wd},0 {wd - 40},0 L{-wd + 40},0 Q{-wd},0 {-wd},-40 Z'
    cy = top + hgt * (1 - coatlen)
    coatp = f'M{-wd},{cy} L{wd},{cy} L{wd},-40 Q{wd},0 {wd - 40},0 L{-wd + 40},0 Q{-wd},0 {-wd},-40 Z'
    fy = top + 110          # eye line
    E = {
        'norm': ell(-30, fy, 20, 24, '#fff', 5) + ell(30, fy, 20, 24, '#fff', 5) + ell(-26, fy + 4, 9, 11, OUT) + ell(34, fy + 4, 9, 11, OUT),
        'wide': ell(-32, fy, 26, 32, '#fff', 5) + ell(32, fy, 26, 32, '#fff', 5) + ell(-32, fy, 7, 8, OUT) + ell(32, fy, 7, 8, OUT),
        'happy': path(f'M-50,{fy + 6} Q-30,{fy - 18} -10,{fy + 6}', sw=8) + path(f'M10,{fy + 6} Q30,{fy - 18} 50,{fy + 6}', sw=8),
        'angry': ell(-30, fy + 4, 18, 18, '#fff', 5) + ell(30, fy + 4, 18, 18, '#fff', 5) + ell(-26, fy + 8, 8, 9, OUT) + ell(26, fy + 8, 8, 9, OUT)
                 + path(f'M-56,{fy - 26} L-10,{fy - 10}', sw=9) + path(f'M56,{fy - 26} L10,{fy - 10}', sw=9),
        'shut': path(f'M-48,{fy + 4} L-12,{fy + 4}', sw=8) + path(f'M12,{fy + 4} L48,{fy + 4}', sw=8),
        'side': ell(-30, fy, 20, 24, '#fff', 5) + ell(30, fy, 20, 24, '#fff', 5) + ell(-40, fy + 2, 9, 11, OUT) + ell(20, fy + 2, 9, 11, OUT)
                + path(f'M-52,{fy - 32} L-8,{fy - 28}', sw=7) + path(f'M12,{fy - 40} L52,{fy - 26}', sw=7),
    }
    my = fy + 62
    M = {
        'smile': path(f'M-26,{my} Q0,{my + 22} 26,{my}', sw=8),
        'grin': path(f'M-36,{my - 6} Q0,{my + 40} 36,{my - 6} Z', fill='#fff', sw=7) + path(f'M-30,{my + 2} L30,{my + 2}', sw=4),
        'open': ell(0, my + 6, 24, 30, '#7a2440', 7) + ell(0, my + 22, 14, 9, '#e0607a'),
        'o': ell(0, my + 4, 14, 18, '#7a2440', 7),
        'flat': path(f'M-24,{my + 4} L24,{my + 4}', sw=8),
        'frown': path(f'M-26,{my + 14} Q0,{my - 8} 26,{my + 14}', sw=8),
        'smirk': path(f'M-24,{my + 8} Q10,{my + 14} 30,{my - 6}', sw=8),
    }
    face = ''.join(g(v, f'{pid}-e-{k}', extra=f'opacity="{1 if k == eyes else 0}"') for k, v in E.items())
    face += ''.join(g(v, f'{pid}-m-{k}', extra=f'opacity="{1 if k == mouth else 0}"') for k, v in M.items())
    acc = ''
    if mustache: acc += path(f'M-46,{my - 14} Q-24,{my - 34} 0,{my - 18} Q24,{my - 34} 46,{my - 14} Q24,{my - 4} 0,{my - 14} Q-24,{my - 4} -46,{my - 14} Z', fill='#3a2418', sw=5)
    if glasses: acc += (ell(-30, fy, 30, 30, 'none', 6) + ell(30, fy, 30, 30, 'none', 6) + path(f'M-2,{fy} L2,{fy}', sw=6))
    if hair == 'tuft': acc += path(f'M-30,{top + 8} Q-10,{top - 50} 10,{top + 4} Q24,{top - 34} 36,{top + 10}', fill=hair_col(pid), sw=6)
    elif hair == 'bob': acc += path(f'M{-wd - 6},{top + 150} L{-wd - 6},{top + wd} A{wd + 6},{wd + 6} 0 0 1 {wd + 6},{top + wd} L{wd + 6},{top + 150} L{wd - 22},{top + 150} L{wd - 22},{top + 60} Q0,{top + 40} {-wd + 22},{top + 60} L{-wd + 22},{top + 150} Z', fill='#5a3220', sw=6)
    elif hair == 'bun': acc += ell(0, top - 10, 40, 34, '#8a4a2a', 6) + path(f'M{-wd + 4},{top + 70} Q0,{top - 10} {wd - 4},{top + 70}', fill='#8a4a2a', sw=6)
    if hat == 'helmet': acc += path(f'M-110,{top + 52} Q-100,{top - 30} 0,{top - 34} Q100,{top - 30} 110,{top + 52} Z', fill=grad('#6b7a4a'), sw=7)
    elif hat == 'cap': acc += path(f'M{-wd},{top + 50} Q0,{top - 40} {wd},{top + 50} Z', fill=grad('#2f3f7a'), sw=7) + path(f'M{wd - 10},{top + 50} L{wd + 60},{top + 56}', sw=10)
    elif hat == 'hard': acc += path(f'M-96,{top + 52} Q-90,{top - 36} 0,{top - 40} Q90,{top - 36} 96,{top + 52} Z', fill=grad('#f2b632'), sw=7) + path(f'M-110,{top + 52} L110,{top + 52}', sw=10)
    elif hat == 'beanie': acc += path(f'M{-wd},{top + 56} Q0,{top - 60} {wd},{top + 56} Z', fill=grad('#3b3b3b'), sw=7)
    elif hat == 'campaign': acc += path(f'M-140,{top + 40} L140,{top + 40} L90,{top + 20} L40,{top - 50} L0,{top - 20} L-40,{top - 50} L-90,{top + 20} Z', fill=grad('#7a6a3a'), sw=7)
    elif hat == 'welder': acc += rect(-wd - 4, top + 50, 2 * wd + 8, 110, grad('#55606e'), 20, 7) + rect(-56, fy - 22, 112, 44, '#1b2a2a', 8, 5) + rect(-50, fy - 16, 50, 14, '#ffd27a', 4, 0, 'opacity=".35"')
    acc += extra_acc
    arm = lambda side: g(path(f'M0,0 L{side * 12},{70}', sw=34, stroke=OUT) + path(f'M0,0 L{side * 12},{70}', sw=22, stroke=coat) + ell(side * 12, 80, 20, 20, sk, 6),
                         f'{pid}-a{"l" if side < 0 else "r"}', f'translate({side * (wd - 6)},{cy + 20})', 'class="arm"')
    legs = rect(-48, -14, 36, 50, shade(coat, .6), 12, 6) + rect(12, -14, 36, 50, shade(coat, .6), 12, 6) + ell(-34, 40, 34, 16, OUT) + ell(32, 40, 34, 16, OUT)
    inner = (legs + arm(-1) + path(body, grad(sk), 9) + path(coatp, grad(coat), 9) + path(f'M-18,{cy} L0,{cy + 34} L18,{cy}', fill=lit(coat, .5), sw=6)
             + g(face + acc, f'{pid}-face') + arm(1))
    shadow = ell(0, 44, 120, 24, '#120a24', extra='opacity=".45"')
    sx = -s if flip else s
    return g(shadow + g(inner, f'{pid}-b'), pid, f'translate({x},{y}) scale({sx},{s})')
_HC = {}
def hair_col(pid): return _HC.get(pid, '#5a3220')

# ---------------------------------------------------------------- props
def lemon(x, y, s=1, rot=0):
    return g(path('M-60,0 Q-50,-48 0,-50 Q50,-48 60,0 Q50,48 0,50 Q-50,48 -60,0 Z', grad('#ffd84a'), 8) + path('M-60,0 L-78,-4', sw=10) + path('M60,0 L78,4', sw=10)
             + ell(-18, -20, 14, 8, '#fff6b0', extra='opacity=".7"'), tr=f'translate({x},{y}) rotate({rot}) scale({s})')
def slug(sid, x, y, s=1, col='#c98a4a', flip=False):
    """our slug: one soft lump + two eye stalks; sid-body squashes into a ball"""
    b = g(path('M-120,0 Q-110,-60 -20,-62 Q40,-64 80,-40 L120,-70 L128,-60 L96,-30 Q112,-14 110,0 Z', grad(col), 8)
          + ell(-40, -30, 12, 8, '#fff', extra='opacity=".35"') + ell(-60, -14, 9, 6, shade(col, .3), extra='opacity=".6"')
          + g(path('M90,-44 L104,-100', sw=7) + ell(104, -104, 12, 12, '#fff', 5) + ell(106, -103, 5, 6, OUT)
              + path('M76,-48 L80,-104', sw=7) + ell(80, -108, 12, 12, '#fff', 5) + ell(82, -107, 5, 6, OUT), f'{sid}-eyes'), f'{sid}-body')
    sx = -s if flip else s
    return g(ell(0, 6, 120, 14, '#120a24', extra='opacity=".4"') + b, sid, f'translate({x},{y}) scale({sx},{s})')
def candle(cid, x, y, s=1, label=None, face='smirk', lit_=True, col='#fff2d6'):
    """Oddwick (host) or a choice candle. ids: cid-flame (scale for flares), cid-glow"""
    flame = g(ell(0, -40, 160, 160, 'url(#glow)', extra=f'id="{cid}-glow"') +
              path('M0,-130 Q40,-70 34,-40 Q30,-6 0,-4 Q-30,-6 -34,-40 Q-40,-70 0,-130 Z', '#ffa82e', 8) +
              path('M0,-84 Q18,-52 14,-36 Q10,-20 0,-20 Q-10,-20 -14,-36 Q-18,-52 0,-84 Z', '#ffe27a', 0), f'{cid}-flame',
              extra=f'opacity="{1 if lit_ else 0}"')
    faces = {'smirk': ell(-24, 70, 9, 10, OUT) + ell(24, 70, 9, 10, OUT) + path('M-18,104 Q6,118 26,96', sw=7) + path('M14,40 L40,34', sw=7),
             'wow': ell(-24, 66, 12, 14, OUT) + ell(24, 66, 12, 14, OUT) + ell(0, 106, 12, 16, OUT),
             'scared': ell(-24, 70, 7, 7, OUT) + ell(24, 70, 7, 7, OUT) + path('M-20,108 Q-10,98 0,108 Q10,118 20,108', sw=6),
             'happy': path('M-34,72 Q-24,58 -14,72', sw=7) + path('M14,72 Q24,58 34,72', sw=7) + path('M-22,96 Q0,122 22,96', sw=7),
             'blow': ell(-24, 70, 9, 10, OUT) + ell(24, 70, 9, 10, OUT) + ell(0, 104, 8, 8, OUT)}
    fg = ''.join(g(v, f'{cid}-f-{k}', extra=f'opacity="{1 if k == face else 0}"') for k, v in faces.items())
    body = (path('M0,0 L0,-26', sw=7) + rect(-62, 0, 124, 190, grad(col), 26, 9) + path('M-62,28 Q-40,40 -30,26 L-30,60 Q-22,70 -14,60 L-14,30 Q20,40 62,26', fill=lit(col, .6), sw=0) + fg)
    lab = text(0, 260, label, 84) if label else ''
    return g(g(flame, tr='translate(0,-10)') + g(body, f'{cid}-body') + lab, cid, f'translate({x},{y}) scale({s})')

# ---------------------------------------------------------------- sets (all are "told by candlelight": dusk/night, warm vs purple)
def sky(moon=True, stars=True, horizon='#ff9a4d'):
    r = random.Random(7); st = ''
    if stars: st = ''.join(ell(r.randint(0, W), r.randint(0, 900), 3, 3, '#fff', extra=f'opacity="{r.uniform(.3, .9):.2f}"') for _ in range(60))
    m = ell(820, 320, 90, 90, '#ffe9c2', extra='opacity=".95"') + ell(850, 300, 90, 90, '#3a2560', extra='opacity=".0"') if moon else ''
    return rect(-400, -400, W + 800, H + 800, 'url(#sky)', sw=0) + st + m
def floor_(y0=1250, col='#3b2a6b', lines=True):
    f = rect(-400, y0, W + 800, H - y0 + 400, 'url(#floor)', sw=0)
    if lines:
        for i in range(-8, 9): f += path(f'M{540 + i * 40},{y0} L{540 + i * 260},{H + 300}', sw=3, stroke='#2a1f50')
        for k in range(1, 7): yy = y0 + (k ** 1.6) * 30; f += path(f'M-400,{yy} L{W + 400},{yy}', sw=3, stroke='#2a1f50')
    return f
def pool(x, y, rx=420, ry=200): return ell(x, y, rx, ry, 'url(#pool)')
def wall(col='#5a4590', y1=1250):
    return rect(-400, -400, W + 800, y1 + 400, grad(col, True), sw=0)
def window_(x, y, w, h, night=True):
    inner = rect(x, y, w, h, '#1c1538' if night else '#ffcf8a', 8, 10)
    if night:
        r = random.Random(x * 7 + y)
        inner += ''.join(rect(x + 20 + i * (w - 40) / 5, y + h - 30 - r.randint(40, int(h * .7)), (w - 40) / 5 - 8, 400, '#2a2050', sw=0, extra='opacity=".9"') for i in range(5))
        inner += ''.join(rect(x + 30 + r.randint(0, w - 60), y + r.randint(int(h * .35), h - 40), 10, 14, WARM2, sw=0) for _ in range(10))
    return inner + path(f'M{x + w / 2},{y} L{x + w / 2},{y + h} M{x},{y + h / 2} L{x + w},{y + h / 2}', sw=8)
def lamp(x, y):
    return (ell(x, y + 120, 260, 120, 'url(#pool)') + path(f'M{x},{y} L{x},{y + 90}', sw=10) + path(f'M{x - 70},{y} L{x + 70},{y} L{x + 40},{y - 70} L{x - 40},{y - 70} Z', grad('#e0a040'), 7)
            + ell(x, y + 6, 60, 40, 'url(#glow)'))
def building(x, base, w, h, col='#2c2150', seed=1, lit_frac=.35):
    r = random.Random(seed); s = rect(x, base - h, w, h, grad(col), 6, 6)
    for yy in range(int(base - h + 30), int(base - 30), 44):
        for xx in range(int(x + 16), int(x + w - 26), 34):
            if r.random() < lit_frac: s += rect(xx, yy, 16, 22, WARM2, 2, 0, f'opacity="{r.uniform(.6, 1):.2f}"')
    return s
def vignette(): return rect(-400, -400, W + 800, H + 800, 'url(#vig)', sw=0)

# ---------------------------------------------------------------- composition
class Shot:
    def __init__(self, a, b, svg, cam=None, anims=None, note=''):
        self.a, self.b, self.svg, self.cam, self.anims, self.note = a, b, svg, cam or [], anims or [], note

def _norm(w): return ''.join(c for c in w.lower() if c.isalnum())
def aligned_words(lines, tr_path):
    """script words with times from the whisper transcript (difflib alignment); unmatched words interpolated in their line"""
    import difflib
    tr = json.load(open(tr_path)); tw = [_norm(x['text']) for x in tr]
    sw = []
    for L in lines:
        for w in L['text'].replace('...', '… ').split(): sw.append([w, None, None, L])
    sm = difflib.SequenceMatcher(None, [_norm(x[0]) for x in sw], tw, autojunk=False)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n): sw[a + k][1] = tr[b + k]['start']; sw[a + k][2] = max(tr[b + k]['end'], tr[b + k]['start'] + .08)
    # interpolate gaps inside each line
    i = 0
    while i < len(sw):
        if sw[i][1] is None:
            j = i
            while j < len(sw) and sw[j][1] is None and sw[j][3] is sw[i][3]: j += 1
            L = sw[i][3]
            t0 = sw[i - 1][2] if i > 0 and sw[i - 1][3] is L else L['start']
            t1 = sw[j][1] if j < len(sw) and sw[j][3] is L else L['start'] + L['dur']
            n = j - i
            for k in range(n): sw[i + k][1] = t0 + (t1 - t0) * k / n; sw[i + k][2] = t0 + (t1 - t0) * (k + 1) / n
            i = j
        else: i += 1
    return [(w, s, e) for w, s, e, _ in sw]

def caption_chunks(lines, tr_path=None):
    if tr_path and os.path.exists(tr_path):
        timed = aligned_words(lines, tr_path); out = []; i = 0
        while i < len(timed):
            w, s_, e = timed[i]
            if i + 1 < len(timed) and len(w) + len(timed[i + 1][0]) <= 11 and not w.endswith(('.', '!', '?', ',', '…')) and timed[i + 1][1] - e < .2:
                out.append((w + ' ' + timed[i + 1][0], s_, timed[i + 1][2])); i += 2
            else: out.append((w, s_, e)); i += 1
        return out
    return caption_chunks_prop(lines)

def caption_chunks_prop(lines):
    """word timings proportional to (letters + 2) inside each spoken line; 1-2 words per caption"""
    out = []
    for L in lines:
        ws = L['text'].replace('...', '… ').split()
        wt = [len(w.strip('.,!?…')) + 2 for w in ws]; tot = sum(wt); t = L['start']
        timed = []
        for w, k in zip(ws, wt):
            d = L['dur'] * k / tot; timed.append((w, t, t + d)); t += d
        i = 0
        while i < len(timed):
            w, s, e = timed[i]
            if i + 1 < len(timed) and len(w) + len(timed[i + 1][0]) <= 11 and not w.endswith(('.', '!', '?', ',', '…')):
                out.append((w + ' ' + timed[i + 1][0], s, timed[i + 1][2])); i += 2
            else:
                out.append((w, s, e)); i += 1
    return out

def build(EP):
    vo = json.load(open(f"/home/claude/work/{EP['slug']}/vo.json")); lines = vo['lines']
    total = EP['total']
    WD = f"/home/claude/work/{EP['slug']}/" + EP.get('hfdir', 'hf'); os.makedirs(WD, exist_ok=True)
    shots = EP['shots'](lines, total)
    hl = []; js = []
    for k, sh in enumerate(shots):
        sid = f's{k}'; dur = round(sh.b - sh.a, 3)
        import re
        sh.svg = _close_fix(sh.svg)
        sh.svg = re.sub(r'id="([A-Za-z][\w-]*)"', lambda m: f'id="{sid}-{m.group(1)}"', sh.svg)
        sh.anims = [(t, re.sub(r'"#([A-Za-z][\w-]*)', lambda m: f'"#{sid}-{m.group(1)}', j)) for t, j in sh.anims]
        hl.append(f'<div id="{sid}" class="clip shot" data-start="{sh.a:.3f}" data-duration="{dur}" data-track-index="1" style="z-index:{k + 1}">'
                  f'<div id="{sid}-cam" class="cam"><svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" overflow="visible">{defs()}{sh.svg}</svg></div>'
                  f'<svg class="vig" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs><radialGradient id="v{k}" cx=".5" cy=".42" r=".78"><stop offset=".55" stop-color="#140c26" stop-opacity="0"/><stop offset="1" stop-color="#140c26" stop-opacity=".8"/></radialGradient></defs><rect width="{W}" height="{H}" fill="url(#v{k})"/></svg></div>')
        # camera: keys (t_rel, zoom, fx, fy) -> focus point to (540, 820)
        cam = sh.cam or [(0, 1.08, 540, 900), (dur, 1.18, 540, 880)]
        def tf(z, fx, fy): return dict(scale=z, x=round(540 - fx * z + (z - 1) * 0 , 1), y=round(820 - fy * z, 1))
        z, fx, fy = cam[0][1:]; t0 = tf(z, fx, fy)
        js.append(f'tl.set("#{sid}-cam",{{x:{t0["x"]},y:{t0["y"]},scale:{z},transformOrigin:"0 0"}},{sh.a:.3f});')
        for (ta, za, fxa, fya), (tb, zb, fxb, fyb) in zip(cam, cam[1:]):
            tt = tf(zb, fxb, fyb)
            js.append(f'tl.to("#{sid}-cam",{{x:{tt["x"]},y:{tt["y"]},scale:{zb},duration:{max(.05, tb - ta):.3f},ease:"sine.inOut"}},{sh.a + ta:.3f});')
        for an in sh.anims:   # (t_rel, js_template) template uses {T}
            js.append(an[1].replace('{T}', f'{sh.a + an[0]:.3f}'))
    # captions
    caps = caption_chunks(lines, f"/home/claude/work/{EP['slug']}/transcript.json"); ch = []
    for i, (w, s, e) in enumerate(caps):
        e2 = caps[i + 1][1] if i + 1 < len(caps) and caps[i + 1][1] - e < .25 else e + .12
        big = ' big' if w.strip('.,!?…').isupper() or any(c.isdigit() for c in w) else ''
        ch.append(f'<div id="c{i}" class="clip cap{big}" data-start="{s:.3f}" data-duration="{max(.12, e2 - s):.3f}" data-track-index="3"><span>{html.escape(w.upper())}</span></div>')
        js.append(f'tl.fromTo("#c{i} span",{{scale:.72,y:18}},{{scale:1,y:0,duration:.12,ease:"back.out(3)"}},{s:.3f});')
    # host Oddwick (top-left, inside the safe band): lights up at 0.1 s, flares on EP['flares'], blows out at the end
    host = f'<div id="host" class="clip" data-start="0" data-duration="{total}" data-track-index="2"><svg viewBox="0 0 400 520" width="230" height="300">{defs()}' + candle('odd', 200, 300, 1.0, face='smirk', lit_=False) + '</svg></div>'
    js.append('tl.set("#odd-flame",{opacity:1,scale:0.2,transformOrigin:"50% 100%"},0.12);tl.to("#odd-flame",{scale:1,duration:.35,ease:"back.out(4)"},0.12);')
    for ft, kind in EP.get('flares', []):
        if kind == 'flare': js.append(f'tl.to("#odd-flame",{{scale:1.55,duration:.15,ease:"power2.out"}},{ft});tl.to("#odd-flame",{{scale:1,duration:.5,ease:"sine.inOut"}},{ft + .3});')
        elif kind == 'shrink': js.append(f'tl.to("#odd-flame",{{scale:.55,duration:.2}},{ft});tl.to("#odd-flame",{{scale:1,duration:.6}},{ft + 1.2});')
        js.append(f'tl.set("#odd-f-smirk",{{opacity:0}},{ft});tl.set("#odd-f-{"wow" if kind == "flare" else "scared"}",{{opacity:1}},{ft});'
                  f'tl.set("#odd-f-{"wow" if kind == "flare" else "scared"}",{{opacity:0}},{ft + 1.3});tl.set("#odd-f-smirk",{{opacity:1}},{ft + 1.3});')
    # gentle idle wobble of the host flame (deterministic)
    n = int(total / 0.9)
    for i in range(n): js.append(f'tl.to("#odd-body",{{rotation:{(-1) ** i * 2},duration:.9,ease:"sine.inOut",transformOrigin:"50% 100%"}},{i * .9:.2f});')
    if EP.get('outro_t'): js.append(f'tl.to("#host",{{x:400,y:-20,scale:1.15,duration:.5,ease:"power2.inOut"}},{EP["outro_t"]:.3f});')
    hide = total - 0.75
    js.append(f'tl.set("#odd-f-smirk",{{opacity:0}},{hide - .5});tl.set("#odd-f-blow",{{opacity:1}},{hide - .5});'
              f'tl.to("#odd-flame",{{scale:0,opacity:0,duration:.3,ease:"power2.in",transformOrigin:"50% 100%"}},{hide - .2});'
              f'tl.to("#blackout",{{opacity:1,duration:.45}},{hide});')
    page = f'''<!doctype html><html><head><meta charset="utf-8"><script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
html,body{{margin:0;background:#140c26}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#140c26}}
.shot{{position:absolute;inset:0;overflow:hidden}}
.cam{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;will-change:transform}}
.vig{{position:absolute;left:0;top:0}}
#host{{position:absolute;left:34px;top:178px;z-index:900}}
.cap{{position:absolute;left:0;top:1215px;width:{W}px;text-align:center;z-index:950;overflow:visible}}
.cap span{{display:inline-block;font-family:Montserrat;font-weight:900;font-size:104px;line-height:1;color:#fff;
  -webkit-text-stroke:14px #140c26;paint-order:stroke fill;text-shadow:0 8px 0 #140c26, 0 0 30px rgba(20,12,38,.6)}}
.cap.big span{{color:#ffd27a;font-size:124px}}
#blackout{{position:absolute;inset:0;background:#0b0716;opacity:0;z-index:990}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}">
{''.join(hl)}
{host}
{''.join(ch)}
{EP.get('overlay', '')}
<div id="blackout" class="clip" data-start="0" data-duration="{total}" data-track-index="4"></div>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
{chr(10).join(js)}
{EP.get('overlay_js', '')}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>'''
    open(f'{WD}/index.html', 'w').write(page)
    for f in ('hyperframes.json', 'package.json'):
        if not os.path.exists(f'{WD}/{f}'): open(f'{WD}/{f}', 'w').write(open(f'/home/claude/videos/engine/oddwick/{f}').read())
    _GR.clear()
    return WD

# ---------------------------------------------------------------- animation snippets (return (t_rel, js))
def bob(pid, t, d, amp=10, period=.5):
    out = []
    for i in range(int(d / period)):
        out.append((t + i * period, f'tl.to("#{pid}-b",{{y:{-amp if i % 2 == 0 else 0},scaleY:{1.03 if i % 2 == 0 else .98},duration:{period},ease:"sine.inOut",transformOrigin:"50% 100%"}},{{T}});'))
    return out
def face(pid, t, eyes=None, mouth=None, all_e=('norm', 'wide', 'happy', 'angry', 'shut', 'side'), all_m=('smile', 'open', 'flat', 'grin', 'o', 'frown', 'smirk')):
    js = ''
    if eyes: js += ''.join(f'tl.set("#{pid}-e-{e}",{{opacity:{1 if e == eyes else 0}}},{{T}});' for e in all_e)
    if mouth: js += ''.join(f'tl.set("#{pid}-m-{m}",{{opacity:{1 if m == mouth else 0}}},{{T}});' for m in all_m)
    js += f'tl.fromTo("#{pid}-b",{{scaleY:.9,scaleX:1.06}},{{scaleY:1,scaleX:1,duration:.3,ease:"back.out(3)",transformOrigin:"50% 100%"}},{{T}});'
    return (t, js)
def talk(pid, t, d, rate=.14, open_='open', rest='smile'):
    out = []; i = 0
    while i * rate < d - rate:
        m = open_ if i % 2 == 0 else ('o' if i % 4 == 1 else rest)
        out.append((t + i * rate, ''.join(f'tl.set("#{pid}-m-{k}",{{opacity:{1 if k == m else 0}}},{{T}});' for k in ('open', 'o', rest))))
        i += 1
    out.append((t + d, ''.join(f'tl.set("#{pid}-m-{k}",{{opacity:{1 if k == rest else 0}}},{{T}});' for k in ('open', 'o', rest))))
    return out
def arm(pid, side, t, rot, d=.25, ease='back.out(2)'):
    return (t, f'tl.to("#{pid}-a{side}",{{rotation:{rot},duration:{d},ease:"{ease}",transformOrigin:"50% 10%"}},{{T}});')
def move(sel, t, d, ease='power2.inOut', **kw):
    props = ','.join(f'{k}:{v if not isinstance(v, str) else json.dumps(v)}' for k, v in kw.items())
    return (t, f'tl.to("{sel}",{{{props},duration:{d},ease:"{ease}"}},{{T}});')
def setp(sel, t, **kw):
    props = ','.join(f'{k}:{v if not isinstance(v, str) else json.dumps(v)}' for k, v in kw.items())
    return (t, f'tl.set("{sel}",{{{props}}},{{T}});')
def fromto(sel, t, d, a, b, ease='power2.out'):
    fa = ','.join(f'{k}:{v if not isinstance(v, str) else json.dumps(v)}' for k, v in a.items())
    fb = ','.join(f'{k}:{v if not isinstance(v, str) else json.dumps(v)}' for k, v in b.items())
    return (t, f'tl.fromTo("{sel}",{{{fa}}},{{{fb},duration:{d},ease:"{ease}"}},{{T}});')
def blink(pid, ts):
    return [(t, f'tl.set("#{pid}-e-norm",{{opacity:0}},{{T}});tl.set("#{pid}-e-shut",{{opacity:1}},{{T}});tl.set("#{pid}-e-shut",{{opacity:0}},{{T}}+.1);tl.set("#{pid}-e-norm",{{opacity:1}},{{T}}+.1);') for t in ts]
def sparks(sid, x, y, n=14, seed=1):
    r = random.Random(seed)
    return g(''.join(path(f'M0,0 L{r.randint(-12, 12)},{r.randint(-12, 12)}', sw=6, stroke=WARM2, extra=f'id="{sid}-{i}" opacity="0"') for i in range(n)) + ell(0, 0, 60, 60, 'url(#glow)', extra=f'id="{sid}-g" opacity="0"'), sid, f'translate({x},{y})')
def spark_burst(sid, t, n=14, seed=1, reps=6, every=.35):
    r = random.Random(seed); out = []
    for k in range(reps):
        tt = t + k * every
        out.append((tt, f'tl.fromTo("#{sid}-g",{{opacity:.9,scale:.6}},{{opacity:.2,scale:1.3,duration:{every:.2f}}},{{T}});'))
        for i in range(n):
            a = r.uniform(-math.pi, 0.3); dist = r.uniform(80, 220)
            out.append((tt, f'tl.fromTo("#{sid}-{i}",{{opacity:1,x:0,y:0}},{{opacity:0,x:{math.cos(a) * dist:.0f},y:{math.sin(a) * dist + 60:.0f},duration:{every:.2f},ease:"power1.out"}},{{T}});'))
    return out
