"""Synthesize crowd SFX (cheer, laugh, gasp, applause) by layering many Kokoro voices with pitch/time offsets + CC0 claps.
python3.13 crowd_sfx.py <out_dir> [clap.wav]   (used when no CC0 crowd recording is reachable from the cloud)"""
import sys, os, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
OUT = sys.argv[1]; CLAP = sys.argv[2] if len(sys.argv) > 2 else None; os.makedirs(OUT, exist_ok=True)
k = Kokoro('/home/claude/tts/kokoro.onnx', '/home/claude/tts/voices.bin'); SR = 24000
V = ['am_puck', 'am_echo', 'af_heart', 'af_bella', 'am_michael', 'af_nicole', 'bm_george', 'bf_emma', 'am_liam', 'af_sky', 'am_adam', 'bf_isabella']
def tts(t, v, sp):
    a, _ = k.create(t, voice=v, speed=sp, lang='en-us'); return a.astype(np.float32)
def shift(a, semis):
    r = 2 ** (semis / 12); idx = np.arange(0, len(a), r); return np.interp(idx, np.arange(len(a)), a).astype(np.float32)
def layer(phrases, n, dur, seed, spread=0.35):
    rng = np.random.RandomState(seed); out = np.zeros(int(dur * SR), np.float32)
    for i in range(n):
        a = shift(tts(phrases[i % len(phrases)], V[i % len(V)], rng.uniform(0.9, 1.3)), rng.uniform(-3, 4))
        a *= rng.uniform(0.4, 1.0); s = int(rng.uniform(0, spread) * SR); e = min(len(out), s + len(a)); out[s:e] += a[:e - s]
    # room: short multi-tap echo + lowpass for distance
    for d, g in ((0.031, .35), (0.057, .25), (0.089, .18)):
        n_ = int(d * SR); out[n_:] += g * out[:-n_]
    return out / (np.abs(out).max() + 1e-9) * 0.9
def claps(dur, rate, seed):
    if not CLAP: return np.zeros(int(dur * SR), np.float32)
    c, sr = sf.read(CLAP); c = c.mean(1) if c.ndim > 1 else c
    c = np.interp(np.arange(0, len(c), sr / SR), np.arange(len(c)), c).astype(np.float32)
    rng = np.random.RandomState(seed); out = np.zeros(int(dur * SR), np.float32)
    for _ in range(int(rate * dur)):
        s = int(rng.uniform(0, dur - 0.2) * SR); a = shift(c, rng.uniform(-4, 4)) * rng.uniform(0.2, 1); out[s:s + len(a)] += a[:len(out) - s]
    env = np.minimum(1, np.minimum(np.arange(len(out)) / (0.15 * SR), (len(out) - np.arange(len(out))) / (0.6 * SR)))
    return out * env / (np.abs(out).max() + 1e-9) * 0.8
W = lambda name, a: sf.write(f'{OUT}/{name}.wav', a, SR)
cheer = layer(['Yaaay!', 'Woo-hoo!', 'Hooray!', 'Yeah!', 'Woooo!', 'Yes!'], 16, 2.6, 1); W('crowd_cheer', cheer * 0.85 + claps(2.6, 30, 2) * 0.5)
W('crowd_laugh', layer(['Ha ha ha ha!', 'Hah hah hah!', 'Hee hee hee!', 'Ho ho ho!'], 12, 2.2, 3, 0.25))
W('crowd_gasp', layer(['Ooooh!', 'Whoa!', 'Oh!', 'Huh!'], 12, 1.5, 4, 0.15))
W('crowd_murmur', layer(['Wow, look.', 'So many lights.', 'Here we go.', 'Is that the Mayor?', 'Shh, it is starting.', 'I love this show.'], 10, 3.2, 5, 1.2) * 0.6)
W('applause', claps(3.0, 45, 6))
print('crowd sfx ->', OUT)
