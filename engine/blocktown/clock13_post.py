"""Sound, captions and assembly for In This Town #1 (clock13). Run after clock13_shots.py has rendered every shot.
python3 clock13_post.py  -> out/2026-11-18-in-this-town-clock-13.mp4
Music: Kevin MacLeod (incompetech.com, CC BY 4.0, credit in the description). SFX: CC0 OpenGameArt packs + synthesized ticks/buzz."""
import os, sys, json, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/videos/engine/oddwick")
import mix as MX

SLUG = "2026-11-18-in-this-town-clock-13"; W = f"/home/claude/work/{SLUG}"; REPO = "/home/claude/videos"
OGA = "/home/claude/work/oga"; LIB = "/home/claude/work/lib"; SR = 48000
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; TOTAL = vo["total"] + 0.6

# ---- synthesized sounds (ours)
def wr(name, x): sf.write(f"{OGA}/{name}.wav", x.astype(np.float32), SR)
t = np.arange(int(0.09 * SR)) / SR
tick = (np.sin(2 * np.pi * 2300 * t) * 0.6 + np.random.RandomState(1).randn(len(t)) * 0.25) * np.exp(-t * 70)
tock = (np.sin(2 * np.pi * 1500 * t) * 0.7 + np.random.RandomState(2).randn(len(t)) * 0.2) * np.exp(-t * 55)
wr("syn_tick", tick); wr("syn_tock", tock); wr("syn_tick_rev", tick[::-1]); wr("syn_tock_rev", tock[::-1])
tb = np.arange(int(0.35 * SR)) / SR
buzz = np.sign(np.sin(2 * np.pi * 150 * tb)) * 0.5 * (np.sin(2 * np.pi * 25 * tb) > -0.2)
wr("syn_buzz", np.concatenate([buzz, np.zeros(int(0.15 * SR)), buzz]))
for src, dst in (("gong_01", "rev_gong"), ("bell_03", "rev_bell")):
    x = MX.load(f"{OGA}/{src}.ogg"); wr(dst, x[::-1])

sfx = []
def S(f, t, g=0, *rest): sfx.append((f, t, g, *rest))
for i in range(9): S("syn_tick.wav" if i % 2 == 0 else "syn_tock.wav", 0.15 + i * 0.5, -6)
S("gong_01.ogg", 3.9, -4)
S("sfx100v2_air_01.ogg", L[1] - 0.15, -8); S("sfx100v2_air_01.ogg", L[2] - 0.15, -8)
S("syn_tick_rev.wav", L[3] + 1.6, -3); S("syn_tock_rev.wav", L[3] + 2.0, -3)
S("rev_gong.wav", L[4] - 0.4, -4)
for i in range(5): S("syn_tick.wav" if i % 2 == 0 else "syn_tock.wav", L[6] + i * 0.5, -6)
S("syn_buzz.wav", L[7] + 0.25, -4); S("syn_buzz.wav", L[7] + 1.1, -6)
S("switch_01.ogg", L[9] + 0.1, -2)
S("door_close_01.ogg", L[10] + 0.25, -3)
for i in range(9): S("sfx100v2_footstep_01.ogg", L[10] + 0.6 + i * 0.3, -9)
S("rev_bell.wav", L[11] - 0.5, -5); S("rev_gong.wav", L[12] - 0.3, -8)
S("syn_tick_rev.wav", L[13] + 0.75, 0); S("syn_tock_rev.wav", L[13] + 1.15, 0); S("syn_tick_rev.wav", L[13] + 1.55, -2)
S("sfx100v2_air_01.ogg", L[14] - 0.1, -7); S("rev_bell.wav", L[14] + 2.2, -6)
S("bfh1_metal_hit_03.ogg", L[15] + 1.5, -6)
for i in range(8): S("syn_tick_rev.wav", L[16] + i * 0.17, -5)
for i in range(9): S("sfx100v2_footstep_01.ogg", L[17] + 0.05 + i * 0.22, -8)
for k in range(2): S("sfx100v2_loop_machine_01.ogg", L[18] + k * 7.4, -14, 0, 7.5)
S("gong_02.ogg", L[19], -2); S("ooh.ogg", L[19] + 0.3, -10)
S("metal_12.ogg", L[21] + 0.1, -5); S("rev_gong.wav", L[21] + 1.8, -5)
S("sfx100v2_loop_machine_01.ogg", L[22], -15, 0, 6.5)
S("breath.ogg", L[24] + 1.7, 0); S("weird_03.ogg", L[24] + 1.95, -8)
S("machine_02.ogg", L[25] + 0.05, -3); S("bfh1_metal_hit_03.ogg", L[25] + 0.9, 0)
S("gong_01.ogg", L[25] + 2.0, 0); S("sfx100v2_thunder_01.ogg", L[25] + 2.05, -6, 0, 3.0)
S("barking_01.ogg", L[26] + 0.5, -2); S("barking_01.ogg", L[26] + 0.9, -4)
S("bfh1_metal_falling_01.ogg", L[27] - 0.45, 0); S("slam_01.ogg", L[27] - 0.4, -4)
S("rev_bell.wav", L[27] + 1.6, -4); S("ooh.ogg", L[27] + 2.6, -8)
S("bell_01.ogg", L[28] + 0.1, -4)
for i in range(6): S("syn_tick_rev.wav" if i % 2 == 0 else "syn_tock_rev.wav", L[29] + 2.2 + i * 0.36, -2 - i * 0.0)
S("rev_gong.wav", TOTAL - 1.2, -3)

music = [  # (file, track offset, t0, t1, gain_db, (fade_in, fade_out))
    (f"{LIB}/km_Investigations.mp3", 0, 0.0, L[9] + 0.9, 0, (0.05, 0.6)),
    (f"{LIB}/km_Darkling.mp3", 5, L[10], L[19], 0, (0.1, 0.5)),
    (f"{LIB}/km_Gathering_Darkness.mp3", 20, L[19], L[24] + 1.5, 1, (0.05, 0.4)),
    (f"{LIB}/km_Volatile_Reaction.mp3", 3, L[25] + 2.1, L[28], 0, (0.05, 0.5)),
    (f"{LIB}/km_Carefree.mp3", 0, L[28], L[29], 0, (0.1, 0.4)),
    (f"{LIB}/km_Ghost_Story.mp3", 8, L[29], TOTAL, 0, (0.3, 0.6)),
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
KEY = {"clock", "midnight", "three", "rules", "outside", "backwards", "hide", "frozen", "forever", "leo", "max", "stopped", "mayor",
       "thirteen", "candle", "blew", "tower", "white", "one", "two", "number", "never", "rule"}
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
