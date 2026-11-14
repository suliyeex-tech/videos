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
VOICE_MIX = (('am_echo', 0.5), ('am_puck', 0.5)); SPEED = 1.2   # owner 2026-11-13: same cheerful fast voice as the Shorts (~240 wpm)
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
    # make the voice bright and present: high-pass, presence boost, gentle compression
    from scipy.signal import butter, sosfilt
    voice = sosfilt(butter(2, 80 / (SR / 2), 'high', output='sos'), voice)
    pres = sosfilt(butter(2, [2500 / (SR / 2), 6000 / (SR / 2)], 'band', output='sos'), voice)
    voice = voice + 0.6 * pres
    envc = np.convolve(np.abs(voice), np.ones(int(0.02 * SR)) / (0.02 * SR), mode='same')
    thr = np.percentile(envc[envc > 1e-4], 70); gain = np.where(envc > thr, (thr / np.maximum(envc, 1e-9)) ** 0.5, 1.0)
    voice = voice * gain
    voice = voice / max(1e-9, np.abs(voice).max()) * 0.95
    t = np.arange(N) / SR
    # dark, quiet ambient bed (references: music ~26 dB under the voice): low drone + slow swells + soft pulse
    rng = np.random.default_rng(3)
    roots = [55.0, 49.0, 58.27, 43.65]                      # A1 G1 Bb1 F1, 16 s each
    m = np.zeros(N)
    for kk in range(int(tot / 16) + 2):
        s0 = int(kk * 16 * SR); e = min(N, s0 + int(18 * SR))
        if s0 >= N: break
        tt = np.arange(e - s0) / SR; f = roots[kk % 4]
        envd = np.minimum(1, tt / 3) * np.clip((18 - tt) / 3, 0, 1)
        m[s0:e] += envd * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.5 * tt + 1) + 0.25 * np.sin(2 * np.pi * f * 2.01 * tt))
    pulse = 0.5 + 0.5 * np.sin(2 * np.pi * t * (90 / 60) / 2) ** 8   # heartbeat-ish pulse
    noise = np.convolve(rng.standard_normal(N), np.ones(400) / 400, mode='same')
    m = m * (0.7 + 0.3 * pulse) + 0.6 * noise / (np.abs(noise).max() + 1e-9)
    m /= np.abs(m).max()
    ev = np.convolve(np.abs(voice), np.ones(int(0.3 * SR)) / (0.3 * SR), mode='same')
    arc = None
    try: arc = literal('MUSIC_ARC')
    except SystemExit: pass
    if arc:
        mood = {}
        try: mood = literal('MUSIC_MOOD')
        except SystemExit: pass
        m, lvl = story_score(k, arc, mood, SR, N)
        duck = 1 - 0.35 * np.clip(ev / 0.05, 0, 1)
        mix = voice + m * 0.11 * lvl * duck * np.clip((tot - t) / 2, 0, 1)
    else:
        mix = voice + m * 0.06 * (1 - 0.4 * np.clip(ev / 0.05, 0, 1)) * np.minimum(1, t / 1.5) * np.clip((tot - t) / 3, 0, 1)
    out = (np.stack([np.clip(mix, -1, 1)] * 2, 1) * 32767).astype(np.int16)
    w = wave.open(f'{WD}/mix.wav', 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()

def story_score(k, arc, mood, SR, N):
    """Storytelling score (owner reference E, '1 MINUTE'): the music follows the story instead of a flat drone.
    MUSIC_ARC = {scene: level 0..1}  (0 = silence before a reveal / on a quote card, 1 = emotional peak); scenes not
    listed keep the previous level. MUSIC_MOOD = {scene: 'dark' | 'tense' | 'hope'} picks the chords (default 'dark').
    Level also sets density: < 0.35 pad only, >= 0.35 + soft piano notes, >= 0.6 + arpeggio, >= 0.8 + low pulse."""
    CH = {'dark': [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]],      # Am F C G
          'tense': [[57, 60, 64], [58, 62, 65], [57, 60, 64], [56, 59, 64]],     # Am Bb Am E/G#
          'hope': [[48, 52, 55], [55, 59, 62], [57, 60, 64], [53, 57, 60]]}      # C G Am F
    hz = lambda n: 440.0 * 2 ** ((n - 69) / 12)
    tot = N / SR; t = np.arange(N) / SR
    lv_pts, md = [], 'dark'; cur_l = 0.5
    for name in k.ORDER:
        st = k.SCENES[name]['start']
        if name in arc: cur_l = float(arc[name])
        md = mood.get(name, md)
        lv_pts.append((st, cur_l, md))
    lvl = np.zeros(N); moods = []
    for i, (st, l, md_) in enumerate(lv_pts):
        en = lv_pts[i + 1][0] if i + 1 < len(lv_pts) else tot
        lvl[int(st * SR):int(en * SR)] = l; moods.append((st, en, md_))
    win = int(1.2 * SR); cs = np.cumsum(np.concatenate([[0.0], np.pad(lvl, (win // 2, win - win // 2), mode='edge')])); lvl = (cs[win:] - cs[:-win])[:N] / win   # smooth swells, ~1 s
    bpm = 76; beat = 60 / bpm; bar = beat * 4
    m = np.zeros(N); rng = np.random.default_rng(5)
    def note(start, f, dur, amp, kind):
        s0 = int(start * SR)
        if s0 >= N: return
        e = min(N, s0 + int(dur * SR)); tt = np.arange(e - s0) / SR
        if kind == 'pad':
            env = np.minimum(1, tt / 1.5) * np.clip((dur - tt) / 1.5, 0, 1)
            w = sum(np.sin(2 * np.pi * f * d * tt + p) for d, p in ((1, 0), (1.003, 1.3), (0.997, 2.1))) / 3 + 0.25 * np.sin(2 * np.pi * 2 * f * tt)
        else:   # soft felt-piano pluck
            env = np.exp(-tt * (2.2 if kind == 'piano' else 3.5)) * np.minimum(1, tt / 0.008)
            w = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 4) + 0.12 * np.sin(2 * np.pi * 3 * f * tt) * np.exp(-tt * 6)
        m[s0:e] += amp * env * w
    b = 0; tb = 0.0
    while tb < tot:
        md_ = next((x[2] for x in moods if x[0] <= tb < x[1]), 'dark')
        ch = CH.get(md_, CH['dark'])[b % 4]; L = lvl[min(N - 1, int(tb * SR))]
        if L > 0.02:
            for n_ in ch: note(tb, hz(n_ - 12), bar + 1.5, 0.22, 'pad')
            note(tb, hz(ch[0] - 24), bar + 1.0, 0.18, 'pad')
            if L >= 0.35:
                for q in (0, 2): note(tb + q * beat, hz(ch[(q // 2) % 3] + 12), 2.5, 0.16, 'piano')
            if L >= 0.6:
                for q in range(8): note(tb + q * beat / 2, hz(ch[[0, 1, 2, 1][q % 4]] + 12 + (12 if q % 4 == 2 else 0)), 0.9, 0.07, 'arp')
            if L >= 0.8:
                for q in range(4):
                    s0 = int((tb + q * beat) * SR); e = min(N, s0 + int(0.25 * SR))
                    if s0 < N: tt = np.arange(e - s0) / SR; m[s0:e] += 0.35 * np.sin(2 * np.pi * (55 + 40 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14)
        b += 1; tb += bar
    # small room reverb (comb + smoothing) for warmth
    rev = np.zeros(N)
    for d, g in ((0.031, 0.35), (0.047, 0.28), (0.071, 0.22), (0.113, 0.15)):
        s_ = int(d * SR); rev[s_:] += g * m[:-s_]
    cs = np.cumsum(np.concatenate([[0.0], rev])); m = m + np.concatenate([np.zeros(59), (cs[60:] - cs[:-60]) / 60])[:N]
    m /= max(1e-9, np.abs(m).max())
    return m, np.clip(lvl, 0, 1)

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
                    '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], check=True)
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
