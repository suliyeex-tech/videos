"""Pipeline: python3 run.py <episode.py> [tts|info|still t..|shot i|render|audio|mux|all]
Output goes to /home/claude/work/<slug>/ and the final mp4 to /home/claude/videos/out/<slug>.mp4"""
import sys, os, json, math, random, subprocess, importlib.util
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kit as K
from kit import W, H, FPS
TTS_DIR = os.environ.get('TTS_DIR') or next((d for d in ('/home/claude/tts', '/home/claude/vid/tts') if os.path.exists(f'{d}/kokoro.onnx')), '/home/claude/tts')
REPO = os.path.dirname(HERE)

def load(path):
    spec = importlib.util.spec_from_file_location('ep', path); ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep); return ep
EP = load(sys.argv[1]); WD = f'/home/claude/work/{EP.SLUG}'; os.makedirs(WD, exist_ok=True)
K.HEADER['title'] = EP.TITLE; K.HEADER['info'] = EP.INFO

# ---------------- voice ----------------
VOICE_MIX = (('am_onyx', 0.5), ('am_puck', 0.5))   # deep warm documentary narrator, matched to the owner's reference videos (~100 Hz)
SPEED = 0.95
def tts():
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(f'{TTS_DIR}/kokoro.onnx', f'{TTS_DIR}/voices.bin')
    style = sum(k.get_voice_style(n) * w for n, w in VOICE_MIX)
    out = []; cur = 0.3; SR = 24000
    for i, (txt, gap) in enumerate(EP.LINES):
        s, sr = k.create(txt, voice=style, speed=SPEED, lang='en-us')
        idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0] - 400): idx[-1] + 1600]
        sf.write(f'{WD}/vo_{i:02d}.wav', s, SR); d = len(s) / SR
        out.append({'i': i, 'text': txt, 'start': round(cur, 3), 'dur': round(d, 3)}); cur += d + gap
    json.dump({'lines': out, 'total': round(cur, 3)}, open(f'{WD}/vo.json', 'w'), indent=1)
    print('tts total', round(cur, 2))

# ---------------- timeline / captions ----------------
def setup():
    global L, TOTAL, BOUNDS, CH
    V = json.load(open(f'{WD}/vo.json')); L = V['lines']; TOTAL = V['total']
    ls = lambda i: L[i]['start']; dur = lambda i: L[i]['dur']
    shots = [(round(a * FPS) / FPS, f) for a, f in EP.timeline(ls, dur)]
    END = math.ceil(TOTAL * FPS) / FPS
    BOUNDS = [(a, (shots[i + 1][0] if i + 1 < len(shots) else END), f) for i, (a, f) in enumerate(shots)]
    CH = []
    for v, groups in zip(L, EP.CAPS):
        tot = sum(len(g) + 3 for g in groups); t = v['start']
        for g in groups:
            d = v['dur'] * (len(g) + 3) / tot; CH.append([t, t + d, g]); t += d
        CH[-1][1] += 0.22
def segs(g):
    out = []; cur = ''; col = K.WHITE
    for c in g:
        if c in '{[':
            if cur: out.append((cur, col)); cur = ''
            col = K.RED if c == '{' else K.YEL
        elif c in '}]':
            if cur: out.append((cur, col)); cur = ''
            col = K.WHITE
        else: cur += c
    if cur: out.append((cur, col))
    return out
def caption(img, t):
    for a, b, g in CH:
        if a <= t < b:
            big = g.startswith('!'); g = g.lstrip('!')
            sg = segs(g); size = 150 if big else 104
            k = K.back(K.ramp(t, a, a + 0.1)); sc = 0.8 + 0.2 * k
            ws = [K.twidth(s_, size, K.ANT, 10) for s_, _ in sg]; tw = sum(ws)
            if tw * sc > 1000: sc *= 1000 / (tw * sc)
            y = 1240 if big else 1290
            x = W / 2 - tw * sc / 2
            for (s_, c), w in zip(sg, ws): K.text(img, s_, x + w * sc / 2 + 5, y + 7, size, (0, 0, 0), K.ANT, alpha=0.55, scale=sc, stroke=10); x += w * sc
            x = W / 2 - tw * sc / 2
            for (s_, c), w in zip(sg, ws): K.text(img, s_, x + w * sc / 2, y, size, (K.RED if big and c == K.WHITE else c), K.ANT, scale=sc, stroke=10, scol=(18, 14, 14)); x += w * sc
            return
def frame(t):
    for a, b, f in BOUNDS:
        if a <= t < b - 1e-6: break
    tl = t - a; d = b - a
    img = np.zeros((H, W, 3), np.uint8); random.seed(int(t * 30))
    f(img, tl, d)
    if f not in getattr(EP, 'NOZOOM', ()):
        z = 1.0 + 0.05 * tl / max(d, 1.5) + (0.05 * (1 - K.eout(K.ramp(tl, 0, 0.18))) if a > 0 else 0)
        M = cv2.getRotationMatrix2D((W / 2, H * 0.5), 0, z); img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    if a == 0 or f in getattr(EP, 'HEADER_SHOTS', ()): pass
    K.vignette(img, 0.28)
    caption(img, t)
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
    A.build(WD, L, TOTAL, [a for a, b, f in BOUNDS], EP.SFX(lambda i: L[i]['start'], lambda i: L[i]['dur']) if hasattr(EP, 'SFX') else {}, getattr(EP, 'MOOD', {}))

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
