"""Pipeline: python3 run.py <episode.py> [tts|info|still t..|sheet [t..]|render|audio|mux|all]
Work files go to /home/claude/work/<slug>/ and the final mp4 to <repo>/out/<slug>.mp4

Episode module contract (see FORMATS.md):
  SLUG, LINES, timeline(ls, dur), optional: TITLE, INFO, CAPS, CAPTION, VOICE, SPEED, MOOD, SFX(ls, dur), NOZOOM, PROGRESS, ZOOM, POST
  LINES items: (text, gap) | (text, gap, voice_key) | (None, seconds)  -> None = silent beat (no voice), for no-narration formats
"""
import sys, os, json, math, random, subprocess, importlib.util
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'formats'))
import kit as K
from kit import W, H, FPS
TTS_DIR = os.environ.get('TTS_DIR') or next((d for d in ('/home/claude/tts', '/home/claude/vid/tts') if os.path.exists(f'{d}/kokoro.onnx')), '/home/claude/tts')
REPO = os.path.dirname(HERE)

def load(path):
    spec = importlib.util.spec_from_file_location('ep', path); ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep); return ep
EP = load(sys.argv[1]); WD = f'/home/claude/work/{EP.SLUG}'; os.makedirs(WD, exist_ok=True)
K.HEADER['title'] = getattr(EP, 'TITLE', ''); K.HEADER['info'] = getattr(EP, 'INFO', '')

# ---------------- voices ----------------
# key -> (blend of Kokoro voices, default speed). 'hype' = cheerful + fast (closest to the darkset / viral narrators)
VOICES = {
    'default':  ((('am_puck', 0.4), ('am_eric', 0.3), ('am_fenrir', 0.3)), 1.05),   # owner-approved fallback (STYLE.md)
    'classic':  ((('am_michael', 0.7), ('am_fenrir', 0.3)), 1.08),
    'hype':     ((('am_echo', 0.5), ('am_puck', 0.5)), 1.25),
    'suspense': ((('am_adam', 0.6), ('am_michael', 0.4)), 1.08),
    'story':    ((('am_puck', 0.6), ('am_fenrir', 0.4)), 1.3),    # owner 2026-11-14: most expressive male blend, fast (default for stories)
    'storyuk':  ((('bm_fable', 1.0),), 1.25),                       # most expressive voice measured (British)
    'guy':      ((('am_puck', 1.0),), 1.22),
    'bro':      ((('am_liam', 0.6), ('am_puck', 0.4)), 1.25),
    'girl':     ((('af_sarah', 0.6), ('af_nova', 0.4)), 1.22),
    'mom':      ((('af_heart', 1.0),), 1.12),
    'old':      ((('bm_george', 1.0),), 1.05),
}
def tts():
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(f'{TTS_DIR}/kokoro.onnx', f'{TTS_DIR}/voices.bin')
    styles = {}
    def style(key):
        if key not in styles: styles[key] = sum(k.get_voice_style(n) * w for n, w in VOICES[key][0])
        return styles[key]
    base = getattr(EP, 'VOICE', 'default')
    if not isinstance(base, str):   # a raw blend list, e.g. [["am_puck", 0.4], ["am_eric", 0.6]]
        VOICES['_ep'] = (tuple(tuple(x) for x in base), getattr(EP, 'SPEED', None) or 1.05); base = '_ep'
    out = []; cur = 0.3; SR = 24000
    for i, item in enumerate(EP.LINES):
        txt, gap = item[0], item[1]; vk = item[2] if len(item) > 2 else base
        if txt is None:   # silent beat
            out.append({'i': i, 'text': None, 'start': round(cur, 3), 'dur': round(gap, 3)}); cur += gap; continue
        sp = getattr(EP, 'SPEED', None) or VOICES[vk][1]
        if len(item) > 2: sp = VOICES[vk][1]
        sp = getattr(EP, 'VOICE_SPEED', {}).get(vk, sp)   # per-voice speed override (MONEY.md: never below 1.15)
        s, sr = k.create(txt, voice=style(vk), speed=sp, lang='en-us')
        idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0] - 400): idx[-1] + 1600]
        sf.write(f'{WD}/vo_{i:02d}.wav', s, SR); d = len(s) / SR
        out.append({'i': i, 'text': txt, 'start': round(cur, 3), 'dur': round(d, 3), 'voice': vk}); cur += d + gap
    json.dump({'lines': out, 'total': round(cur + 0.2, 3)}, open(f'{WD}/vo.json', 'w'), indent=1)
    print('tts total', round(cur, 2))

# ---------------- timeline / captions ----------------
def setup():
    global L, TOTAL, BOUNDS, CH, LINECAP
    V = json.load(open(f'{WD}/vo.json')); L = V['lines']; TOTAL = V['total']
    ls = lambda i: L[i]['start']; dur = lambda i: L[i]['dur']
    shots = [(round(a * FPS) / FPS, f) for a, f in EP.timeline(ls, dur)]
    END = math.ceil(TOTAL * FPS) / FPS
    BOUNDS = [(a, (shots[i + 1][0] if i + 1 < len(shots) else END), f) for i, (a, f) in enumerate(shots)]
    CH = []; LINECAP = []
    for v, groups in zip(L, getattr(EP, 'CAPS', [])):
        if not groups: continue
        LINECAP.append([v['start'], v['start'] + v['dur'] + 0.25, groups])
        tot = sum(len(g) + 3 for g in groups); t = v['start']
        for g in groups:
            d = v['dur'] * (len(g) + 3) / tot; CH.append([t, t + d, g]); t += d
        CH[-1][1] += 0.22
def segs(g, accent=None):
    out = []; cur = ''; col = K.WHITE
    for c in g:
        if c in '{[':
            if cur: out.append((cur, col)); cur = ''
            col = accent or (K.RED if c == '{' else K.YEL)
            if accent is None and c == '{': col = K.RED
        elif c in '}]':
            if cur: out.append((cur, col)); cur = ''
            col = K.WHITE
        else: cur += c
    if cur: out.append((cur, col))
    return out
def words_of(sg):
    """split coloured segments into (word, colour) tokens"""
    out = []
    for s_, c in sg:
        for wd in s_.split(' '):
            if wd: out.append((wd, c))
    return out

def cap_pop(img, t, karaoke=False):
    for a, b, g in CH:
        if a <= t < b:
            big = g.startswith('!'); g = g.lstrip('!')
            toks = words_of(segs(g)); size = 150 if big else 104
            n = len(toks); shown = n if not karaoke else max(1, min(n, int((t - a) / max(0.05, (b - a - 0.22)) * n) + 1))
            sp = K.twidth(' ', size, K.ANT) * 0.9
            ws = [K.twidth(w_, size, K.ANT, 10) for w_, _ in toks]; tw = sum(ws) + sp * (n - 1)
            sc0 = 1.0 if tw < 1000 else 1000 / tw
            y = 1240 if big else 1290; x = W / 2 - tw * sc0 / 2
            for j, ((w_, c), w) in enumerate(zip(toks, ws)):
                if j >= shown: break
                ta = a + (b - a - 0.22) * j / n if karaoke else a
                k = K.back(K.ramp(t, ta, ta + 0.12)); sc = sc0 * (0.6 + 0.4 * k) if karaoke else sc0 * (0.8 + 0.2 * K.back(K.ramp(t, a, a + 0.1)))
                col = (K.RED if big and c == K.WHITE else c)
                if karaoke and j == shown - 1 and not big and c == K.WHITE: col = K.YEL
                cx = x + w * sc0 / 2
                K.text(img, w_, cx + 5, y + 7, size, (0, 0, 0), K.ANT, alpha=0.55, scale=sc, stroke=10)
                K.text(img, w_, cx, y, size, col, K.ANT, scale=sc, stroke=10, scol=(18, 14, 14)); x += w * sc0 + sp * sc0
            return

def wrap(toks, size, font, maxw):
    lines = [[]]; wcur = 0; sp = K.twidth(' ', size, font)
    for w_, c in toks:
        w = K.twidth(w_, size, font)
        if lines[-1] and wcur + sp + w > maxw: lines.append([]); wcur = 0
        lines[-1].append((w_, c, w)); wcur += (sp if wcur else 0) + w
    return lines, sp

def cap_block(img, t, style):
    """whole-line captions: 'top' (neon, sentence at the top) or 'serif' (cinematic subtitles)"""
    for a, b, groups in LINECAP:
        if a <= t < b:
            text_ = ' '.join(g.lstrip('!') for g in groups)
            if style == 'top':
                toks = words_of(segs(text_, accent=getattr(EP, 'ACCENT', (255, 170, 40)))); size, font, y0, lh = 58, K.INTER_B, getattr(EP, 'TOP_Y', 300), 72
                toks = [(w_.upper(), c) for w_, c in toks]
            else:
                toks = words_of(segs(text_, accent=(200, 225, 245))); size, font, y0, lh = 56, K.SERIF_I, 1330, 74
            lines, sp = wrap(toks, size, font, 900)
            al = K.ramp(t, a, a + 0.18) * (1 - K.ramp(t, b - 0.15, b))
            for li, ln in enumerate(lines):
                tw = sum(w for _, _, w in ln) + sp * (len(ln) - 1); x = W / 2 - tw / 2; y = y0 + li * lh + (1 - K.eout(K.ramp(t, a, a + 0.2))) * 14
                for w_, c, w in ln:
                    if style == 'top' and c != K.WHITE: K.glow(img, x + w / 2, y, int(w * 0.6), tuple(int(v * 0.25) for v in c), 0.6)
                    K.text(img, w_, x + w / 2 + (3 if style == 'serif' else 0), y + 3, size, (0, 0, 0), font, alpha=0.6 * al)
                    K.text(img, w_, x + w / 2, y, size, c, font, alpha=al); x += w + sp
            return

def frame(t):
    for a, b, f in BOUNDS:
        if a <= t < b - 1e-6: break
    tl = t - a; d = b - a
    img = np.zeros((H, W, 3), np.uint8); random.seed(int(t * 30))
    f(img, tl, d)
    zk = getattr(EP, 'ZOOM', 1.0)
    if f not in getattr(EP, 'NOZOOM', ()) and zk > 0:
        z = 1.0 + zk * (0.05 * tl / max(d, 1.5) + (0.07 * (1 - K.eout(K.ramp(tl, 0, 0.16))) if a > 0 else 0))
        M = cv2.getRotationMatrix2D((W / 2, H * 0.5), 0, z); img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    if getattr(EP, 'VIGNETTE', 0.28): K.vignette(img, getattr(EP, 'VIGNETTE', 0.28))
    style = getattr(EP, 'CAPTION', 'pop')
    if style in ('pop', 'karaoke'): cap_pop(img, t, karaoke=(style == 'karaoke'))
    elif style in ('top', 'serif'): cap_block(img, t, style)
    if hasattr(EP, 'OVERLAY'): EP.OVERLAY(img, t, TOTAL)
    if getattr(EP, 'PROGRESS', True):
        col = getattr(EP, 'PROGRESS_COL', K.YEL); k = min(1, t / TOTAL)
        img[H - 14:H] = (img[H - 14:H] * 0.4).astype(np.uint8); img[H - 14:H, :int(W * k)] = col
    return img

def render_shot(i):
    a, b, f = BOUNDS[i]; n0, n1 = round(a * FPS), round(b * FPS); tmp = f'{WD}/tmp_{i:02d}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
    for n in range(n0, n1): p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit(f'shot {i} failed')
    os.rename(tmp, f'{WD}/s{i:02d}.mp4')

def render_all(workers=2):
    n = len(BOUNDS); procs = []
    for w in range(workers):
        idx = [i for i in range(n) if i % workers == w]
        procs.append(subprocess.Popen([sys.executable, __file__, sys.argv[1], 'shots'] + [str(i) for i in idx]))
    if any(p.wait() for p in procs): raise SystemExit('render failed')
    with open(f'{WD}/list.txt', 'w') as fh:
        for i in range(n): fh.write(f"file '{WD}/s{i:02d}.mp4'\n")
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{WD}/list.txt', '-c', 'copy', f'{WD}/silent.mp4'])

def audio():
    import audio as A
    sfx = EP.SFX(lambda i: L[i]['start'], lambda i: L[i]['dur']) if hasattr(EP, 'SFX') else {}
    # owner 2026-11-14: NO tick sounds under captions (TICKS is ignored; never re-enable)
    A.build(WD, L, TOTAL, [a for a, b, f in BOUNDS], sfx, getattr(EP, 'MOOD', {}))

def mux():
    os.makedirs(f'{REPO}/out', exist_ok=True); out = f'{REPO}/out/{EP.SLUG}.mp4'
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{WD}/silent.mp4', '-i', f'{WD}/mix.wav', '-map', '0:v', '-map', '1:a',
                           '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out + '.tmp.mp4'])
    os.rename(out + '.tmp.mp4', out); print('done', out, os.path.getsize(out))

if __name__ == '__main__':
    cmd = sys.argv[2] if len(sys.argv) > 2 else 'all'
    if cmd == 'tts': tts(); sys.exit()
    if cmd == 'all' and not os.path.exists(f'{WD}/vo.json'): tts()
    setup()
    if cmd == 'info': print(round(TOTAL, 2), [(round(a, 2), round(b, 2), f.__name__) for a, b, f in BOUNDS])
    elif cmd == 'still':
        for ts in sys.argv[3:]: cv2.imwrite(f'{WD}/still_{float(ts):05.2f}.jpg', frame(float(ts)), [cv2.IMWRITE_JPEG_QUALITY, 85])
    elif cmd == 'sheet':
        ts = [float(x) for x in sys.argv[3:]] or [(a + b) / 2 for a, b, f in BOUNDS]
        ims = [cv2.resize(frame(x), (270, 480)) for x in ts]
        while len(ims) % 5: ims.append(np.zeros_like(ims[0]))
        rows = [np.hstack(ims[i:i + 5]) for i in range(0, len(ims), 5)]
        cv2.imwrite(f'{WD}/sheet.jpg', np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 82]); print(f'{WD}/sheet.jpg')
    elif cmd == 'shots':
        for i in sys.argv[3:]: render_shot(int(i))
    elif cmd == 'render': render_all()
    elif cmd == 'audio': audio()
    elif cmd == 'mux': mux()
    elif cmd == 'all': render_all(); audio(); mux()
