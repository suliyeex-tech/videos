"""Synth SFX for the alarm-clock long-form: cartoon snore (rattling low noise) and a soft 'gulp' for the pigeon. -> /home/claude/work/syn"""
import numpy as np, soundfile as sf
SR = 48000; rng = np.random.default_rng(3)
def lp(x, a):  # one-pole lowpass
    y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x): s += a * (v - s); y[i] = s
    return y
def snore(dur=2.4, f_rattle=34, big=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = lp(rng.standard_normal(n), 0.08)
    rattle = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * f_rattle * t))          # palate flutter
    tone = np.sin(2 * np.pi * 70 * t + 3 * np.sin(2 * np.pi * 3 * t))
    env = np.sin(np.pi * np.clip(t / (dur * 0.62), 0, 1)) ** 1.5             # inhale snore, then quiet exhale
    exh = np.sin(np.pi * np.clip((t - dur * 0.65) / (dur * 0.33), 0, 1)) * 0.25 * lp(rng.standard_normal(n), 0.2)
    x = (noise * rattle * 1.4 + 0.5 * tone * rattle) * env * big + exh
    return (x / np.abs(x).max() * 0.9).astype(np.float32)
sf.write('/home/claude/work/syn/snore.wav', snore(), SR)
sf.write('/home/claude/work/syn/snore_big.wav', np.concatenate([snore(2.2, 30, 1.0), snore(2.4, 26, 1.2)]), SR)
n = int(0.25 * SR); t = np.arange(n) / SR
g = np.sin(2 * np.pi * (300 - 500 * t) * t) * np.exp(-t * 18); sf.write('/home/claude/work/syn/gulp.wav', (g * 0.8).astype(np.float32), SR)
print('syn ok')
