#!/usr/bin/env python3
"""Long-form (16:9, 1080p30) video runner.

    python3 lf.py <episode.py> tts      # narration, one wav per SCRIPT line -> timing.json
    python3 lf.py <episode.py> frames   # 1 still per scene + every caption change -> sheet_*.jpg (LOOK at them)
    python3 lf.py <episode.py> frame SCENE T OUT.png
    python3 lf.py <episode.py> all      # render scenes, music, mux, thumbnail -> ../out/<SLUG>.mp4 + ../out/<SLUG>.png

The narrator is the same voice as the Shorts (Kokoro 50% am_onyx + 50% am_puck, see STYLE.md).
Output is kept under 19 MB so jsDelivr (20 MB per file limit) can serve it.
"""
import ast, json, math, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
TTS_DIR = os.environ.get('TTS_DIR', '/home/claude/tts')
VOICE_MIX = (('am_onyx', 0.5), ('am_puck', 0.5)); SPEED = 0.88   # same narrator as the Shorts
EP_PATH = os.path.abspath(sys.argv[1]); MODE = sys.argv[2]

def literal(name):
    tree = ast.parse(open(EP_PATH).read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == name:
            return ast.literal_eval(n.value)
    raise SystemExit(f'{name} missing in episode')

SLUG = literal('SLUG'); WD = f'/home/claude/work/lf_{SLUG}'; os.makedirs(WD, exist_ok=True)
os.environ['LF_TIMING'] = f'{WD}/timing.json'
try: os.environ['LF_GAP'] = str(literal('GAP'))
except SystemExit: pass

def tts():
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(f'{TTS_DIR}/kokoro.onnx', f'{TTS_DIR}/voices.bin')
    try: mix = literal('VOICE')
    except SystemExit: mix = VOICE_MIX
    try: speed = literal('SPEED')
    except SystemExit: speed = SPEED
    style = sum(k.get_voice_style(n) * w for n, w in mix)
    out = []
    for i, (sc, txt) in enumerate(literal('SCRIPT')):
        s, sr = k.create(txt, voice=style, speed=speed, lang='en-us')
        idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0] - 400): idx[-1] + 2400]
        sf.write(f'{WD}/vo_{i:02d}.wav', s, sr); out.append([sc, txt, round(len(s) / sr, 3)])
    json.dump(out, open(f'{WD}/timing.json', 'w'), indent=0)
    print('narration', round(sum(x[2] for x in out), 1), 's')

def load_ep():
    import importlib.util
    spec = importlib.util.spec_from_file_location('ep', EP_PATH); ep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ep); return ep

def draw(ep, name, t, surf):
    import cairo, kit16 as k
    c = cairo.Context(surf); sc = k.SCENES[name]
    ep.DRAW[name](c, t, sc); k.caption(c, sc, t)
    f = min(k.ramp(t, 0, 0.3), 1 - k.ramp(t, sc['dur'] - 0.3, 0.3))
    if name == k.ORDER[0]: f = 1 - k.ramp(t, sc['dur'] - 0.3, 0.3)
    if f < 1: c.set_source_rgba(0, 0, 0, 1 - f); c.paint()

def frame(name, t, out):
    import cairo, kit16 as k
    ep = load_ep(); s = cairo.ImageSurface(cairo.FORMAT_RGB24, k.W, k.H); draw(ep, name, t, s); s.write_to_png(out)

def frames():
    import cairo, kit16 as k
    from PIL import Image
    ep = load_ep(); shots = []
    for name in k.ORDER:
        for st, d, _ in k.SCENES[name]['sents']:
            shots.append((name, st + d * 0.75))
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, k.W, k.H)
    for p in range(0, len(shots), 12):
        sheet = Image.new('RGB', (4 * 480, 3 * 270))
        for i, (name, t) in enumerate(shots[p:p + 12]):
            draw(ep, name, t, s); s.write_to_png(f'{WD}/f.png')
            sheet.paste(Image.open(f'{WD}/f.png').convert('RGB').resize((480, 270)), ((i % 4) * 480, (i // 4) * 270))
        sheet.save(f'{WD}/sheet_{p // 12}.jpg', quality=85); print(f'{WD}/sheet_{p // 12}.jpg')

def render_scene(name, crf):
    import cairo, kit16 as k
    ep = load_ep(); sc = k.SCENES[name]; n = round(sc['dur'] * k.FPS)
    tmp, fin = f'{WD}/{name}.tmp.mp4', f'{WD}/{name}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{k.W}x{k.H}',
                          '-r', str(k.FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(crf),
                          '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, k.W, k.H)
    for i in range(n):
        draw(ep, name, i / k.FPS, s); s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close()
    if p.wait() != 0: raise SystemExit(f'render failed: {name}')
    os.replace(tmp, fin)

def music_and_voice(k):
    SR = 44100; tot = k.TOTAL; N = int(tot * SR) + SR
    voice = np.zeros(N); i = 0
    for name in k.ORDER:
        sc = k.SCENES[name]
        for st, d, _ in sc['sents']:
            w = wave.open(f'{WD}/vo_{i:02d}.wav'); sr = w.getframerate()
            raw = w.readframes(w.getnframes())
            x = (np.frombuffer(raw, dtype=np.int16).astype(float) / 32768) if w.getsampwidth() == 2 else np.frombuffer(raw, dtype=np.float32).astype(float)
            x = np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x)
            p = int((sc['start'] + st) * SR); voice[p:p + len(x)] += x[:N - p]; i += 1
    voice = voice / max(1e-9, np.abs(voice).max()) * 0.89
    t = np.arange(N) / SR
    beat = 60 / 100; eighth = beat / 2
    chords = [[261.63, 329.63, 392.0], [196.0, 246.94, 293.66], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63]]
    m = np.zeros(N); L = int(0.35 * SR); envl = np.exp(-np.arange(L) / SR * 9); pat = [0, 1, 2, 1, 0, 2, 1, 2]
    for kk in range(int(tot / eighth) + 1):
        ch = chords[(kk // 16) % 4]; f = ch[pat[kk % 8]]; s0 = int(kk * eighth * SR)
        if s0 >= N: break
        tt = np.arange(L) / SR; seg = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * envl * 0.18
        e = min(N, s0 + L); m[s0:e] += seg[:e - s0]
        if kk % 4 == 0:
            Lb = int(beat * 2 * SR); tb = np.arange(Lb) / SR; sb = np.sin(2 * np.pi * ch[0] / 2 * tb) * np.exp(-tb * 2.5) * 0.22
            e = min(N, s0 + Lb); m[s0:e] += sb[:e - s0]
    m /= np.abs(m).max()
    ev = np.convolve(np.abs(voice), np.ones(int(0.3 * SR)) / (0.3 * SR), mode='same')
    mix = voice + m * 0.2 * (1 - 0.6 * np.clip(ev / 0.05, 0, 1)) * np.minimum(1, t / 1.5) * np.clip((tot - t) / 3, 0, 1)
    out = (np.stack([np.clip(mix, -1, 1)] * 2, 1) * 32767).astype(np.int16)
    w = wave.open(f'{WD}/mix.wav', 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()

def thumb(ep):
    import cairo
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1280, 720); c = cairo.Context(s); c.scale(1280 / 1920, 720 / 1080)
    ep.THUMB(c); os.makedirs(f'{REPO}/out', exist_ok=True); s.write_to_png(f'{REPO}/out/{SLUG}.png')

def all_(crf=20):
    import kit16 as k
    from concurrent.futures import ProcessPoolExecutor
    ep = load_ep()
    with ProcessPoolExecutor(max_workers=max(1, min(4, os.cpu_count() or 2))) as ex:
        list(ex.map(render_scene, k.ORDER, [crf] * len(k.ORDER)))
    open(f'{WD}/list.txt', 'w').write(''.join(f"file '{WD}/{n}.mp4'\n" for n in k.ORDER))
    music_and_voice(k)
    out = f'{REPO}/out/{SLUG}.mp4'; os.makedirs(f'{REPO}/out', exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{WD}/list.txt', '-c', 'copy', f'{WD}/v.mp4'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{WD}/v.mp4', '-i', f'{WD}/mix.wav', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], check=True)
    size = os.path.getsize(out)
    if size > 19_000_000 and crf < 34:   # jsDelivr serves at most 20 MB per file
        print(f'{size/1e6:.1f} MB > 19 MB, re-encoding smaller'); return all_(crf + 4)
    thumb(ep)
    print(out, f'{size/1e6:.1f} MB', f'{k.TOTAL:.1f} s'); print(f'{REPO}/out/{SLUG}.png')

if __name__ == '__main__':
    if MODE == 'tts': tts()
    elif MODE == 'frames': frames()
    elif MODE == 'frame': frame(sys.argv[3], float(sys.argv[4]), sys.argv[5])
    elif MODE == 'all': all_()
    else: raise SystemExit(__doc__)
