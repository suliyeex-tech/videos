"""Young energetic kid narrator for the Oddwick house style (owner 2026-11-20).
python3.13 kidvoice.py <episode.json>  -> /home/claude/work/<slug>/voice.wav + vo.json (lines, per-word timings, wpm, F0)
Kokoro blend am_puck .6 + am_echo .25 + af_heart .15 at speed ~1.22, synthesized SENTENCE BY SENTENCE (exact timing for 1-word
captions without Whisper), then 'kid' FX: +10% formant/pitch (asetrate) and rubberband pitch x1.25 (formant preserved)
=> median F0 ~170-180 Hz. Words inside a sentence are timed proportionally to their letters."""
import sys, json, os, re, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
BLEND = [('am_puck', .6), ('am_echo', .25), ('af_heart', .15)]
FX = 'asetrate=26400,aresample=24000,atempo=0.90909,rubberband=pitch=1.25:formant=preserved:pitchq=quality'
SR = 24000

def f0_median(x, sr=SR):
    fr = int(0.04 * sr); hop = fr // 2; out = []
    for i in range(0, len(x) - fr, hop):
        w = x[i:i + fr] * np.hanning(fr)
        if np.sqrt(np.mean(w ** 2)) < 0.02: continue
        ac = np.correlate(w, w, 'full')[fr - 1:]; ac /= ac[0] + 1e-9
        lo, hi = int(sr / 420), int(sr / 70); j = lo + np.argmax(ac[lo:hi])
        if ac[j] > 0.45: out.append(sr / j)
    return float(np.median(out)) if out else 0.0

def main(path):
    ep = json.load(open(path)); WD = f"/home/claude/work/{ep['slug']}"; os.makedirs(WD, exist_ok=True)
    k = Kokoro('/home/claude/tts/kokoro.onnx', '/home/claude/tts/voices.bin')
    st = sum(k.get_voice_style(n) * w for n, w in ep.get('blend', BLEND))
    SP = ep.get('speed', 1.22); cur = 0.35; lines = []; words = []; chunks = []
    for i, L in enumerate(ep['lines']):
        sents = [s for s in re.split(r'(?<=[.!?])\s+', L['t'].strip()) if s]
        t0 = cur
        for j, s in enumerate(sents):
            a, _ = k.create(s, voice=st, speed=L.get('sp', SP), lang='en-us')
            idx = np.where(np.abs(a) > 0.008)[0]; a = a[max(0, idx[0] - 200): idx[-1] + 600]
            d = len(a) / SR; chunks.append((cur, a))
            ws = s.split(); wt = np.array([len(re.sub(r'[^A-Za-z0-9]', '', w)) + 1.5 for w in ws], float)
            edges = cur + 0.03 + np.concatenate([[0], np.cumsum(wt)]) / wt.sum() * (d - 0.08)
            for w, a0, a1 in zip(ws, edges[:-1], edges[1:]): words.append({'w': w, 's': round(a0, 3), 'e': round(a1, 3), 'line': i})
            cur += d + (0.16 if j < len(sents) - 1 else 0)
        lines.append({'i': i, 'text': L['t'], 'start': round(t0, 3), 'dur': round(cur - t0, 3)})
        cur += L.get('gap', 0.14)
    tot = cur + 0.2
    raw = np.zeros(int(tot * SR) + SR, np.float32)
    for t, a in chunks: s0 = int(t * SR); raw[s0:s0 + len(a)] += a
    sf.write(f'{WD}/voice_raw.wav', raw, SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{WD}/voice_raw.wav', '-af', FX, '-ar', str(SR), f'{WD}/voice.wav'], check=True)
    v, _ = sf.read(f'{WD}/voice.wav'); f0 = f0_median(v.astype(np.float32))
    nw = len(words); spoken = sum(l['dur'] for l in lines)
    meta = {'lines': lines, 'words': words, 'total': round(tot, 3), 'n_words': nw, 'wpm_total': round(nw / (tot / 60), 1),
            'wpm_speaking': round(nw / (spoken / 60), 1), 'f0_median_hz': round(f0, 1), 'blend': ep.get('blend', BLEND), 'speed': SP, 'fx': FX}
    json.dump(meta, open(f'{WD}/vo.json', 'w'), indent=1)
    print(ep['slug'], 'total', round(tot, 1), 's', nw, 'words', meta['wpm_total'], 'wpm (whole track)', meta['wpm_speaking'], 'wpm (speaking)', 'F0', meta['f0_median_hz'], 'Hz')

if __name__ == '__main__': main(sys.argv[1])
