"""Oddwick narrator: python3 voice.py <episode.json>  -> work/<slug>/vo_XX.wav + vo.json (+ wpm)
One energetic storyteller (PLAYBOOK §4): am_puck 60% + am_fenrir 40%. Lines may set "v":"mock" (sarcastic, slightly different blend)."""
import sys, json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
ep = json.load(open(sys.argv[1])); WD = f"/home/claude/work/{ep['slug']}"; os.makedirs(WD, exist_ok=True)
k = Kokoro('/home/claude/tts/kokoro.onnx', '/home/claude/tts/voices.bin')
BL = {'nar': [('am_puck', .6), ('am_fenrir', .4)], 'mock': [('am_fenrir', .5), ('am_michael', .5)], 'her': [('af_heart', 1.0)]}
st = {key: sum(k.get_voice_style(n) * w for n, w in b) for key, b in BL.items()}
SP = ep.get('speed', 1.3); cur = 0.25; out = []; words = 0
for i, L in enumerate(ep['lines']):
    v = L.get('v', 'nar'); s, sr = k.create(L['t'], voice=st[v], speed=L.get('sp', SP), lang='en-us')
    idx = np.where(np.abs(s) > 0.008)[0]; s = s[max(0, idx[0] - 300): idx[-1] + 1200]
    sf.write(f'{WD}/vo_{i:02d}.wav', s, sr); d = len(s) / sr
    out.append({'i': i, 'text': L['t'], 'start': round(cur, 3), 'dur': round(d, 3), 'v': v}); cur += d + L.get('gap', 0.12)
    words += len(L['t'].split())
tot = cur
json.dump({'lines': out, 'total': round(tot, 3), 'words': words, 'wpm': round(words / (tot / 60), 1)}, open(f'{WD}/vo.json', 'w'), indent=1)
# concatenated voice track
voice = np.zeros(int((tot + 0.5) * 24000), np.float32)
for o in out:
    a, _ = sf.read(f"{WD}/vo_{o['i']:02d}.wav"); st0 = int(o['start'] * 24000); voice[st0:st0 + len(a)] += a
sf.write(f'{WD}/voice.wav', voice, 24000)
print(ep['slug'], 'voice', round(tot, 2), 's', words, 'words', round(words / (tot / 60), 1), 'wpm')
