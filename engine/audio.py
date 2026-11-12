"""Music bed + SFX + processed voice-over, mastered to -14 LUFS / -1 dBTP."""
import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, lfilter, resample_poly
SR = 44100
def lp(x, f, o=2): b, a = butter(o, f / (SR / 2)); return lfilter(b, a, x)
def hp(x, f, o=2): b, a = butter(o, f / (SR / 2), 'high'); return lfilter(b, a, x)
def env(n, a=0.005, d=0.3):
    t = np.arange(n) / SR; return np.minimum(t / a, 1) * np.exp(-t / d)

def build(WD, L, TOTAL, cuts, sfx, mood):
    N = int(SR * (TOTAL + 0.2)); t = np.arange(N) / SR; rng = np.random.default_rng(11)
    def put(buf, x, at, g=1.0):
        i = int(at * SR)
        if i >= N or i + len(x) <= 0: return
        if i < 0: x = x[-i:]; i = 0
        j = min(N, i + len(x)); buf[i:j] += x[:j - i] * g
    root = mood.get('root', 55.0); bpm = mood.get('bpm', 105); beat = 60 / bpm
    mistake = sfx.get('mistake'); end = sfx.get('end', TOTAL - 2.5); hook_end = sfx.get('hook_end', 3.0)
    drop = sfx.get('drop', (mistake, mistake + 0.9) if mistake else None)
    # intensity curve 0..1
    inten = np.clip((t - hook_end) / max(1, (end - hook_end)), 0, 1) * 0.5 + 0.5 * (t > hook_end)
    # ---- pad (detuned saws, low-passed) ----
    prog = mood.get('prog', [0, -4, 3, -2])   # semitones: i VI III VII
    bar = beat * 4; pad = np.zeros(N)
    for k in range(int(TOTAL / (bar * 2)) + 2):
        st = k * bar * 2; n = int(bar * 2 * SR); tt = np.arange(n) / SR
        f0 = root * 2 ** (prog[k % len(prog)] / 12)
        x = np.zeros(n)
        for mul, g in ((1, .5), (1.5, .25), (2, .3), (2.4 if mood.get('minor', True) else 2.5, .18)):
            for det in (-0.4, 0.4): x += g * (2 * ((f0 * mul * 2 + det) * tt % 1) - 1)
        x = lp(x, 900) * np.minimum(1, np.minimum(tt / 0.3, (bar * 2 - tt) / 0.3))
        put(pad, x, st, 0.05)
    # ---- sub bass on 8ths, kick, hats ----
    drums = np.zeros(N); bass = np.zeros(N)
    kn = int(0.3 * SR); kt = np.arange(kn) / SR
    kick = np.sin(2 * np.pi * (45 * kt + 70 * (1 - np.exp(-kt * 28)) / 28)) * np.exp(-kt / 0.11)
    hat = hp(rng.standard_normal(int(0.04 * SR)), 7000) * env(int(0.04 * SR), 0.001, 0.01)
    clap = lp(hp(rng.standard_normal(int(0.18 * SR)), 900), 5000) * env(int(0.18 * SR), 0.002, 0.05)
    b = 0
    while b * beat / 2 < TOTAL:
        at = b * beat / 2; k = b // 2
        if drop and drop[0] <= at < drop[1]: b += 1; continue
        if at < end:
            if at >= hook_end:
                if b % 2 == 0: put(drums, kick, at, 0.8)
                if b % 4 == 2 and at > hook_end + bar: put(drums, clap, at, 0.35)
                put(drums, hat, at, 0.18 if b % 2 else 0.1)
                f = root * 2 ** (prog[int(at / (bar * 2)) % len(prog)] / 12)
                nn = int(beat / 2 * SR); tt = np.arange(nn) / SR
                put(bass, np.sin(2 * np.pi * f * tt) * env(nn, 0.004, 0.16), at, 0.35)
            else:
                put(drums, hat, at, 0.12)
                if b % 4 == 0: put(drums, kick, at, 0.35)
        b += 1
    # ---- pluck arp ----
    arp = np.zeros(N); scale = [0, 3, 7, 10, 12, 10, 7, 3]; i = 0; at = hook_end
    while at < end:
        if not (drop and drop[0] <= at < drop[1]):
            f = root * 4 * 2 ** ((prog[int(at / (bar * 2)) % len(prog)] + scale[i % 8]) / 12)
            nn = int(0.25 * SR); tt = np.arange(nn) / SR
            x = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) + 0.1 * np.sin(6 * np.pi * f * tt)) * env(nn, 0.003, 0.08)
            put(arp, x, at, 0.05 + 0.04 * float(at > (hook_end + end) / 2))
        at += beat / 2; i += 1
    music = pad + bass + drums * 0.9 + arp
    music *= (0.7 + 0.3 * inten)
    if drop: g = np.ones(N); g[int(drop[0] * SR):int(drop[1] * SR)] = 0.15; music *= lp(g, 6, 1)
    # ---- sfx ----
    fx = np.zeros(N)
    def whoosh(d=0.35):
        n = int(d * SR); x = rng.standard_normal(n); tt = np.linspace(0, 1, n); return lp(hp(x, 400), 6000) * tt ** 2 * 0.5
    def boom(d=1.4, f=40):
        n = int(d * SR); tt = np.arange(n) / SR
        return (np.sin(2 * np.pi * (f * tt + 30 * (1 - np.exp(-tt * 10)) / 10)) + 0.3 * lp(rng.standard_normal(n), 250)) * np.exp(-tt / 0.4)
    def ding(f=1318.5, d=0.9):
        n = int(d * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(3 * np.pi * f * tt)) * env(n, 0.003, 0.22)
    def snap(d=0.25):
        n = int(d * SR); return hp(rng.standard_normal(n), 1500) * env(n, 0.0005, 0.03) + np.sin(2 * np.pi * 180 * np.arange(n) / SR) * env(n, 0.001, 0.05)
    def splash(d=1.2):
        n = int(d * SR); tt = np.arange(n) / SR; return lp(hp(rng.standard_normal(n), 300), 4000) * np.minimum(tt / 0.02, 1) * np.exp(-tt / 0.35)
    def scratch(d=0.45):
        n = int(d * SR); tt = np.arange(n) / SR; fm = 300 + 900 * np.abs(np.sin(2 * np.pi * 4 * tt))
        return lp(hp(rng.standard_normal(n), 800), 3000) * 0.5 * np.sin(2 * np.pi * np.cumsum(fm) / SR) * env(n, 0.005, 0.2)
    def heart():
        n = int(0.2 * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * 45 * tt) * np.exp(-tt / 0.06)
    def riser(d=1.6):
        n = int(d * SR); tt = np.linspace(0, 1, n); return lp(rng.standard_normal(n), 3000) * tt ** 3 * 0.6 + np.sin(2 * np.pi * np.cumsum(200 + 900 * tt ** 2) / SR) * tt ** 2 * 0.15
    for c in cuts[1:]: put(fx, whoosh(), c - 0.33, 0.35)
    for c in sfx.get('boom', []): put(fx, boom(), c, 0.8)
    for c in sfx.get('ding', []): put(fx, ding(), c, 0.3)
    for c in sfx.get('snap', []): put(fx, snap(), c, 0.8)
    for c in sfx.get('splash', []): put(fx, splash(), c, 0.6)
    for c in sfx.get('pop', []): put(fx, ding(880, 0.25), c, 0.25)
    if mistake is not None: put(fx, scratch(), mistake - 0.05, 0.9); put(fx, boom(1.8, 34), mistake + 0.05, 0.6)
    for a_, b_ in sfx.get('heart', []):
        at = a_
        while at < b_: put(fx, heart(), at, 0.8); put(fx, heart(), at + 0.22, 0.5); at += 0.8
    if end: put(fx, riser(), end - 1.6, 0.45); put(fx, boom(2.0, 36), end, 0.9)
    # ---- voice: per-line, then broadcast chain in ffmpeg ----
    voice = np.zeros(N)
    for v in L:
        x, sr = sf.read(f"{WD}/vo_{v['i']:02d}.wav"); x = resample_poly(x, 147, 80)
        put(voice, x / (np.max(np.abs(x)) + 1e-9) * 0.8, v['start'])
    sf.write(f'{WD}/vo_raw.wav', voice, SR)
    chain = ('highpass=f=75,equalizer=f=160:t=q:w=1:g=2.5,equalizer=f=420:t=q:w=1.2:g=-2.5,equalizer=f=3200:t=q:w=1.4:g=3,'
             'equalizer=f=7500:t=q:w=2:g=-2,acompressor=threshold=0.08:ratio=3.5:attack=4:release=90:makeup=2.2,'
             'alimiter=limit=0.89:level=false')
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{WD}/vo_raw.wav', '-af', chain, '-ar', str(SR), f'{WD}/vo_proc.wav'])
    voice, _ = sf.read(f'{WD}/vo_proc.wav'); voice = voice[:N] if len(voice) >= N else np.pad(voice, (0, N - len(voice)))
    e = lp(np.abs(voice), 7, 1); duck = 1 - 0.55 * np.clip(e / 0.1, 0, 1)
    bed = music * duck * 0.55 + fx * 0.5
    # stereo: widen the bed with a short Haas delay, voice centred
    dl = int(0.012 * SR); bl = bed; br = np.concatenate([np.zeros(dl), bed[:-dl]])
    st = np.stack([voice + bl * 0.95 + br * 0.15, voice + br * 0.95 + bl * 0.15], 1)
    fo = int(0.3 * SR); st[-fo:] *= np.linspace(1, 0, fo)[:, None]
    st /= np.max(np.abs(st)) / 0.9
    sf.write(f'{WD}/premix.wav', st, SR)
    # two-pass loudness normalisation
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f'{WD}/premix.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = json.loads(r[r.rfind('{'):r.rfind('}') + 1])
    af = (f"loudnorm=I=-14:TP=-1.0:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{WD}/premix.wav', '-af', af, '-ar', str(SR), f'{WD}/mix.wav'])
    print('audio ok', m['input_i'], '->', -14)
