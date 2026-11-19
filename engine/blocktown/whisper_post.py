"""Sound, captions and assembly for In This Town #2 (Whisper Boy). Run after whisper_shots.py.
python3 whisper_post.py -> out/2026-11-19-in-this-town-everyone-shouts.mp4
Music: Kevin MacLeod (incompetech.com, CC BY 4.0, credit in the description). SFX: CC0 OpenGameArt packs + our synthesized 'shh'."""
import os, sys, json, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/videos/engine/oddwick")
import mix as MX

SLUG = "2026-11-19-in-this-town-everyone-shouts"; W = f"/home/claude/work/{SLUG}"; REPO = "/home/claude/videos"
OGA = "/home/claude/work/oga"; LIB = "/home/claude/work/lib"; SR = 48000
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; TOTAL = vo["total"] + 0.6
os.makedirs(f"{OGA}/syn", exist_ok=True)
def wr(name, x): sf.write(f"{OGA}/syn/{name}.wav", x.astype(np.float32), SR)
r = np.random.RandomState(5); n = int(.32 * SR); t = np.arange(n) / SR
noise = r.randn(n); from scipy.signal import butter, lfilter
b, a = butter(4, [2500 / (SR / 2), 9000 / (SR / 2)], btype="band"); shh = lfilter(b, a, noise) * np.sin(np.pi * t / t[-1]) ** 1.5
wr("shh", shh)
C = "80-cc0-creature-sfx/"; O = "100-cc0-sfx/"; O2 = "100-cc0-sfx-2/sfx100v2_"; SW = "swishes-sound-pack/swishes/swish-"
sfx = []
def S(f, t, g=0, *rest): sfx.append((f if f.startswith("/") else f"{OGA}/{f}", t, g, *rest))
def hush(t0, gap=0.42, g=-4):
    for k in range(3): S("syn/shh.wav", t0 + k * gap, g)
# line 0: hush x3 at the end of the line
hush(L[0] + 2.9); S(SW + "3.wav", 2.25, -6)
S(O + "bell_02.ogg", L[1] + 1.2, -5); S("crowd-shoutingspeaking-ambience/crowd_shouting.ogg", L[1] + 2.6, -4, 0, 2.5)
S("crowd-shoutingspeaking-ambience/crowd_shouting_0.ogg", L[2] + 0.2, -6, 3, 1.5); S(O + "dishes_02.ogg", L[2] + 0.4, -6)
S(O2 + "wood_hit_01.ogg", L[3] + 0.2, -3); S(C + "grunt_02.ogg", L[3] + 0.3, -6)
S(O + "slam_03.ogg", L[4] + 0.3, -5); S(C + "grunt_04.ogg", L[4] + 0.5, -6); S(O + "switch_01.ogg", L[4] + 2.0, -4)
S(O + "door_open.ogg", L[5] + 0.2, -8)
for k in range(10): S(O2 + f"footstep_wood_0{k % 4 + 1}.ogg", L[5] + 0.6 + k * 0.5, -14)
S(O2 + "wood_01.ogg", L[5] + 2.2, -8); S(O2 + "wood_03.ogg", L[5] + 3.9, -8)
S("cat-purr-meow/cat_softmew.wav", L[6] + 0.1, -6); S("cat-purr-meow/cat_purrsleepy_loop.wav", L[6] + 0.9, -10, 0, 1.0)
S(C + "barking_01.ogg", L[6] + 1.6, -10); S(C + "snore.ogg", L[6] + 2.1, -8); S(O + "bell_03.ogg", L[6] + 2.6, -16)
hush(L[6] + 2.55, 0.4, -6)
for k in range(6): S(O2 + f"footstep_wood_0{k % 4 + 1}.ogg", L[7] + 0.2 + k * 0.5, -16)
S("do-you-remember-laughter/ogalaughter_2.ogg", L[8] + 0.2, -3, 22.5, 2.4); S("group-giggling/group_giggling.ogg", L[8] + 0.5, -6, 0, 2.0)
S(SW + "7.wav", L[9] - 0.1, -4); S("group-giggling/group_giggling_0.ogg", L[9] + 1.6, -6, 0, 1.0)
S("applause-in-a-large-hall-or-church/applause-clapping-church-crowd-immersive.wav", L[10] + 0.1, -8, 2, 2.6)
for k in range(5): S(O2 + f"footstep_wood_0{k % 4 + 1}.ogg", L[10] + 2.7 + k * 0.45, -9)
S(O + "switch_02.ogg", L[11] - 0.1, -6)
S("crowd-shoutingspeaking-ambience/crowd_shouting.ogg", L[12] - 0.05, 0, 0, 2.2); S(O2 + "glass_04.ogg", L[12] + 1.0, -4); S(O2 + "glass_02.ogg", L[12] + 1.3, -6)
S(SW + "9.wav", L[12] + 2.0, -4); S(SW + "11.wav", L[12] + 2.3, -6); S(O2 + "metal_hit_01.ogg", L[12] + 3.3, -4)
S(C + "breath.ogg", L[13] + 0.1, -2); S(C + "snore.ogg", L[13] + 0.5, -8)
S(C + "monster_04.ogg", L[14] + 0.1, -3); S(O + "slam_06.ogg", L[14] + 0.6, -4)
S(C + "ooh.ogg", L[15] + 0.1, -6); S(C + "scream_01.ogg", L[15] + 1.8, -4); S("crowd-shoutingspeaking-ambience/crowd_shouting_0.ogg", L[15] + 1.9, -2, 0, 1.5)
S(C + "roar_02.ogg", L[16] + 0.6, 0); S(C + "roar_03.ogg", L[16] + 2.0, -2); S(O + "metal_08.ogg", L[16] + 3.3, -2); S(O + "hit_03.ogg", L[16] + 4.1, -4)
S(SW + "5.wav", L[17] - 0.1, -6)
for k in range(5): S(O2 + f"footstep_wood_0{k % 4 + 1}.ogg", L[18] + 0.1 + k * 0.42, -18)
hush(L[18] + 1.7, 0.38, -5)
S(C + "grunt_01.ogg", L[19] + 1.4, -8); S("cat-purr-meow/cat_purrsleepy_loop.wav", L[19] + 0.4, -14, 0, 1.6)
S(C + "troll_01.ogg", L[20] + 1.1, -4); S(C + "snore.ogg", L[20] + 3.0, -4); S(O2 + "wood_hit_02.ogg", L[20] + 3.6, -6)
S(C + "snore.ogg", L[21] + 0.8, -10)
S(O + "bell_01.ogg", L[22] + 0.4, -6); S("applause-in-a-large-hall-or-church/applause-clapping-church-crowd-immersive.wav", L[22] + 0.7, -6, 4, 2.0)
S(SW + "12.wav", L[23] - 0.05, -4); S(O + "gong_02.ogg", L[23] + 1.4, -8)
hush(L[24] + 3.2, 0.42, -4); S(SW + "2.wav", L[24] + 2.45, -6)
S(SW + "1.wav", L[25] - 0.05, -6); S(O + "bell_02.ogg", TOTAL - 1.0, -6)

music = [
    (f"{LIB}/km_Monkeys_Spinning_Monkeys.mp3", 0, 0.0, L[5] - 0.05, -1, (0.02, 0.3)),
    (f"{LIB}/km_Sneaky_Snitch.mp3", 0, L[5], L[8], -1, (0.1, 0.3)),
    (f"{LIB}/km_Fluffing_a_Duck.mp3", 0, L[8], L[10], -2, (0.05, 0.2)),
    (f"{LIB}/km_Pixel_Peeker_Polka_-_faster.mp3", 0, L[10], L[11] + 0.6, -1, (0.05, 0.2)),
    (f"{LIB}/km_Volatile_Reaction.mp3", 3, L[13], L[17], 0, (0.05, 0.4)),
    (f"{LIB}/km_Sneaky_Snitch.mp3", 20, L[17] + 0.2, L[21], -4, (0.3, 0.6)),
    (f"{LIB}/km_Carefree.mp3", 0, L[22], TOTAL, -1, (0.2, 0.8)),
]
mixf = MX.mix(SLUG, TOTAL, music, sfx)
# ---- picture: shots -> one 12 fps film -> 1080x1920 @24
timing = json.load(open(f"{W}/shots_timing.json")); parts = []
for sid, t0, t1 in timing:
    n = len([f for f in os.listdir(f"{W}/shots/{sid}") if f.endswith(".png")]); o = f"{W}/shots/{sid}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "12", "-i", f"{W}/shots/{sid}/%04d.png",
                    "-vf", "scale=1080:1920:flags=lanczos,fps=24", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", o], check=True)
    parts.append(o)
open(f"{W}/concat.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
film = f"{W}/film.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{W}/concat.txt", "-c", "copy", film], check=True)

# ---- 1-word captions from whisper word timings
from faster_whisper import WhisperModel
a = MX.load(f"{W}/voice.wav")
a16 = np.interp(np.arange(0, len(a), SR / 16000), np.arange(len(a)), a).astype(np.float32)
words = []
for seg in WhisperModel("base.en", device="cpu", compute_type="int8").transcribe(a16, word_timestamps=True)[0]:
    words += [(w.start, w.end, w.word.strip()) for w in seg.words]
KEY = {"hush", "shout", "shouting", "whispering", "whisper", "trophy", "golden", "bear", "mayor", "benny", "grandma", "silent", "louder", "five", "two", "hundred", "quiet", "practicing"}
def ts(x): return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"
ass = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
       "Style: C,DejaVu Sans,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,1,0,0,0,100,100,0,0,1,8,4,5,40,40,0,1\n\n"
       "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
for i, (s0, s1, w) in enumerate(words):
    e = words[i + 1][0] if i + 1 < len(words) and words[i + 1][0] - s1 < 0.35 else s1 + 0.12
    clean = w.strip(".,!?:;\"'…").lower()
    if not clean: continue
    col = "{\\c&H00E6FF&}" if clean in KEY else ""
    ass += f"Dialogue: 0,{ts(s0)},{ts(max(e, s0 + 0.12))},C,,0,0,0,,{{\\pos(540,1330)\\fscx80\\fscy80\\t(0,70,\\fscx100\\fscy100)}}{col}{clean}\n"
open(f"{W}/caps.ass", "w").write(ass)
out = f"{REPO}/out/{SLUG}.mp4"; os.makedirs(f"{REPO}/out", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", film, "-i", mixf, "-vf", f"ass={W}/caps.ass", "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
print(out)
