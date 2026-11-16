"""Audio mix for Oddwick shorts: voice + story-shaped music (several real tracks, cut to the story beats) + clearly audible SFX.
mix(slug, total, music=[(file, track_offset_s, t0, t1, gain_db)], sfx=[(file, t, gain_db)]) -> work/<slug>/mix.wav
Levels (PLAYBOOK §5): voice ~-16 LUFS; music bed ~-22..-24 LUFS under voice; SFX peaks ~-8 dBFS (louder than music, under voice)."""
import numpy as np, subprocess, json, os
SR = 48000
LIB = '/home/claude/work/lib'; OGA = '/home/claude/work/oga'

def load(path, offset=0.0, dur=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(offset), '-i', path]
    if dur: cmd += ['-t', str(dur)]
    cmd += ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()

def rms_db(x):
    x = x[np.abs(x) > 1e-4]
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9) if len(x) else -99

def fade(x, fi=.05, fo=.3):
    n = len(x); a = int(fi * SR); b = int(fo * SR)
    if a: x[:a] *= np.linspace(0, 1, min(a, n))[:min(a, n)]
    if b and n > b: x[-b:] *= np.linspace(1, 0, b)
    return x

def mix(slug, total, music, sfx, out=None):
    WD = f'/home/claude/work/{slug}'
    N = int(total * SR) + SR
    voice = load(f'{WD}/voice.wav'); v = np.zeros(N, np.float32); v[:min(N, len(voice))] = voice[:N]
    v *= 10 ** ((-19 - rms_db(v)) / 20)                      # speech RMS ~ -19 dBFS
    m = np.zeros(N, np.float32)
    for f, off, t0, t1, gdb, *fx in music:
        seg = load(f if f.startswith('/') else f'{LIB}/{f}', off, t1 - t0 + .05)
        seg = seg * 10 ** ((-19 - 12 + gdb - rms_db(seg)) / 20)   # bed ~15 dB under the voice
        fi, fo = (fx[0] if fx else (.08, .35))
        seg = fade(seg, fi, fo); a = int(t0 * SR); m[a:a + len(seg)] += seg[:N - a]
    s = np.zeros(N, np.float32)
    ev = []
    for f, t, gdb, *rest in sfx:
        ev.append(t)
        p = f if f.startswith('/') else (f'{OGA}/{f}' if os.path.exists(f'{OGA}/{f}') else f'{LIB}/{f}')
        off = rest[0] if rest else 0; du = rest[1] if len(rest) > 1 else 6
        x = load(p, off, du)
        pk = np.max(np.abs(x)) + 1e-9; x = x * (10 ** ((-8 + gdb) / 20) / pk)
        x = fade(x, .005, min(.4, len(x) / SR / 3)); a = max(0, int(t * SR)); s[a:a + len(x)] += x[:N - a]
    mixd = v + m + s
    np.savez_compressed(f'{WD}/stems.npz', v=v[::4], m=m[::4], s=s[::4], ev=np.array(ev))
    mixd = mixd[:int(total * SR)]
    tmp = f'{WD}/mix_raw.wav'; out = out or f'{WD}/mix.wav'
    import soundfile as sf
    sf.write(tmp, mixd, SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), '-ac', '2', out], check=True)
    # report
    r = subprocess.run(['ffmpeg', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    summ = r[r.rfind('Summary:'):]
    print(' '.join(summ.split())[:200])
    return out

def mux(slug, video, audio, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
    return out
