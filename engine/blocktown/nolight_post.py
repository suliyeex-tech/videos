"""Sound, captions and assembly for In This Town #3 (The town where it was always night). Run after whisper_shots.py.
python3 whisper_post.py -> out/2026-11-19-in-this-town-everyone-shouts.mp4
Music: Kevin MacLeod (incompetech.com, CC BY 4.0, credit in the description). SFX: CC0 OpenGameArt packs + our synthesized 'shh'."""
import os, sys, json, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/videos/engine/oddwick")
import mix as MX

SLUG = "2026-11-20-the-town-where-it-was-always-night"; W = f"/home/claude/work/{SLUG}"; REPO = "/home/claude/videos"
OGA = "/home/claude/work/oga"; LIB = "/home/claude/work/lib"; SR = 48000
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; TOTAL = vo["total"] + 0.6
C = "80-cc0-creature-sfx/"; O = "100-cc0-sfx/"; O2 = "100-cc0-sfx-2/sfx100v2_"; SW = "swishes-sound-pack/swishes/swish-"
B = "75-cc0-breaking-falling-hit-sfx/bfh1_"; MW = "100-cc0-metal-and-wood-sfx/"; CAT = "cat-purr-meow/"; FS = "footsteps-0/"
sfx = []
def S(f, t, g=0, *rest): sfx.append((f if f.startswith("/") else f"{OGA}/{f}", t, g, *rest))
def D(i): return (L[i + 1] if i + 1 < len(L) else TOTAL) - L[i]
S("mild-wind-background-noise/wind background noise 2.wav", 0, -12, 0, L[5]); S(SW + "3.wav", 1.9, -6)
S(O + "slam_02.ogg", L[1] + .4, -4); S(O + "paper_03.ogg", L[1] + 1.4, -8)
for k in range(5): S("25-cc0-mud-sfx/mud_0" + str(k % 5 + 1) + ".ogg", L[2] + .2 + k * .28, -12)
S(B + "hit_06.ogg", L[2] + 1.7 + .85, -2); S(C + "hurt_01.ogg", L[2] + 1.7 + .95, -6)
S(O2 + "misc_12.ogg", L[3] + .3, -8); S(C + "grunt_04.ogg", L[3] + 1.4, -6)
for k in range(3): S(O2 + "footstep_0" + str(k % 2 + 1) + ".ogg", L[4] + .2 + k * .4, -14)
S(B + "hit_04.ogg", L[4] + .55 * D(4), 0); S(C + "hurt_03.ogg", L[4] + .55 * D(4) + .15, -6)
S(MW + "wood_squeak_02.ogg", L[5] + .2, -6); S(O + "wooded_box_open.ogg", L[5] + 1.2, -4)
S(O + "weird_02.ogg", L[6] + .4, -8); S(O + "bell_03.ogg", L[6] + 1.0, -10)
S("air-whoosh/whoosh2_0.wav", L[7] + .4 * D(7) - .1, 0); S("fire-crackling/fire-1.ogg", L[7] + .4 * D(7), -6, 0, D(7) + D(8))
S("electricity-sound-effects-0/spark.wav", L[8] + .3, -8); S(O + "bell_01.ogg", L[8] + .4, -6)
S(O + "switch_01.ogg", L[9] + D(9) / 3 - .1, -4); S(O + "gong_01.ogg", L[9] + D(9) / 3 + .05, -2); S(MW + "metal_sheet_01.ogg", L[9] + D(9) / 3 + .1, -6)
S(CAT + "cat_softmew.wav", L[10] + .4, -4); S(O + "bell_03.ogg", L[10] + D(10) / 2, -6); S(CAT + "cat_mewfood.wav", L[10] + D(10) / 2 + .6, -2)
for k in range(5): S(FS + "0" + str(k % 6 + 1) + "-footstep.ogg", L[11] + .1 + k * .28, -8)
S(O + "slam_01.ogg", L[11] + 1.6 + .4 * (L[11] + 3.0 - L[11] - 1.6), 0); S("air-whoosh/whoosh2_0.wav", L[11] + 2.2, -4); S(C + "ooh.ogg", L[11] + 3.1, -6)
S(O + "bell_02.ogg", L[12] + D(12) / 3 + .1, -4); S(O2 + "glass_02.ogg", L[12] + D(12) / 3 + .2, -6); S(C + "ooh.ogg", L[12] + D(12) / 3 + .5, -8)
S(O + "bell_01.ogg", L[13] + .35 * D(13), -4); S("do-you-remember-laughter/ogalaughter_2.ogg", L[13] + D(13) - 1.2, -6, 22.5, 1.4)
step = D(14) / 5
for k in range(4): S(O + ("plop_01.ogg" if k % 2 == 0 else "plop_02.ogg"), L[14] + (k + .2) * step, -2); S(O + "switch_02.ogg", L[14] + (k + .2) * step, -8)
S(O + "door_01.ogg", L[15] + .05, -2); S(O + "slam_06.ogg", L[15] + .2, 0); S("crowd-shoutingspeaking-ambience/crowd_shouting_0.ogg", L[15] + .4, -10, 0, 1.2)
S(C + "grunt_05.ogg", L[16] + .1, -8)
for k in range(5): S(C + "breath.ogg", L[17] + .4 + k * D(17) / 5.5, -6); S(O + "switch_01.ogg", L[17] + .6 + k * D(17) / 5.5, -10)
S(O2 + "air_02.ogg", L[18] + .2, -10); S(O + "weird_05.ogg", L[19] + .4, -8)
for k in range(10): S(O2 + "footstep_wood_0" + str(k % 4 + 1) + ".ogg", L[20] + .2 + k * .32, -8)
S("breathing-tired/breathing tired.ogg", L[20] + 1.2, -8, 0, 2.0)
for k in range(4): S("electricity-sound-effects-0/spark.wav", L[21] + .3 + k * .6, -6)
S(O + "gong_02.ogg", L[22] + .6 * D(22), -2); S(SW + "12.wav", L[22] + .6 * D(22) - .1, -4)
S("muffled-distant-explosion/NenadSimic - Muffled Distant Explosion.wav", L[23] + .05, 0, 0, 1.8); S(O + "bell_01.ogg", L[23] + .3, -4); S(SW + "9.wav", L[23] + 1.0, -2); S(C + "ooh.ogg", L[23] + 1.6, -6)
S("solo-seagull-sound-effects/Seagull Ambient 1.wav", L[24] + .5, -14, 0, 2.5); S(O + "bell_03.ogg", L[24] + 2.4, -8)
S("applause-in-a-large-hall-or-church/applause-clapping-church-crowd-immersive.wav", L[25] + .05, -4, 2, 1.8); S("crowd-shoutingspeaking-ambience/crowd_shouting.ogg", L[25] + .1, -8, 0, 1.0)
S(O + "spring_05.ogg", L[26] + D(26) / 3, -4); S(O + "bell_02.ogg", L[26] + D(26) / 3 + .2, -6); S(C + "ooh.ogg", L[26] + D(26) / 3 + .5, -8)
S("group-giggling/group_giggling.ogg", L[27] + .4, -6, 0, 1.6)
S(SW + "1.wav", L[28] - .05, -6); S(O2 + "air_01.ogg", L[28] + .62 * D(28) - .1, 0)
music = [
    (f"{LIB}/km_Lightless_Dawn.mp3", 3, 0.0, L[5] - 0.05, -1, (0.02, 0.3)),
    (f"{LIB}/km_Mesmerize.mp3", 0, L[5], L[9], -2, (0.1, 0.2)),
    (f"{LIB}/km_Carefree.mp3", 0, L[9], L[15] - 0.05, -2, (0.05, 0.2)),
    (f"{LIB}/km_Scheming_Weasel_faster.mp3", 0, L[15], L[18] - 0.05, -1, (0.05, 0.3)),
    (f"{LIB}/km_Gathering_Darkness.mp3", 0, L[18], L[22] + .6 * D(22) - 0.3, 0, (0.2, 0.3)),
    (f"{LIB}/km_Eternal_Hope.mp3", 0, L[23] + .5, L[25] - .1, -1, (0.4, 0.4)),
    (f"{LIB}/km_Fluffing_a_Duck.mp3", 0, L[25], TOTAL, -2, (0.05, 0.8)),
]
mixf = MX.mix(SLUG, TOTAL, music, sfx)
# ---- picture: shots -> one 12 fps film -> 1080x1920 @24
DARK = {"s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s14", "s22", "s23", "s25", "s26"}
timing = json.load(open(f"{W}/shots_timing.json")); parts = []
for sid, t0, t1 in timing:
    n = len([f for f in os.listdir(f"{W}/shots/{sid}") if f.endswith(".png")]); o = f"{W}/shots/{sid}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "12", "-i", f"{W}/shots/{sid}/%04d.png",
                    "-vf", "scale=1080:1920:flags=lanczos,fps=24" + (",eq=gamma=1.22:saturation=1.1" if sid in DARK else ""), "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", o], check=True)
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
KEY = {"light", "lights", "candle", "glow", "boom", "fwoosh", "whoosh", "pop", "mayor", "clock", "sun", "orange", "pip", "lamp", "hat", "hundred", "gold", "horse", "share", "two"} or {"hush", "shout", "shouting", "whispering", "whisper", "trophy", "golden", "bear", "mayor", "benny", "grandma", "silent", "louder", "five", "two", "hundred", "quiet", "practicing"}
def ts(x): return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"
ass = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
       "Style: C,DejaVu Sans,128,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,1,0,0,0,100,100,0,0,1,10,5,5,40,40,0,1\n\n"
       "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
for i, (s0, s1, w) in enumerate(words):
    e = words[i + 1][0] if i + 1 < len(words) and words[i + 1][0] - s1 < 0.35 else s1 + 0.12
    clean = w.strip(".,!?:;\"'…").lower()
    if not clean: continue
    col = "{\\c&H00E6FF&}" if clean in KEY else ""
    ass += f"Dialogue: 0,{ts(s0)},{ts(max(e, s0 + 0.12))},C,,0,0,0,,{{\\pos(540,1330)\\fscx80\\fscy80\\t(0,70,\\fscx100\\fscy100)}}{col}{clean.upper()}\n"
open(f"{W}/caps.ass", "w").write(ass)
out = f"{REPO}/out/{SLUG}.mp4"; os.makedirs(f"{REPO}/out", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", film, "-i", mixf, "-vf", f"ass={W}/caps.ass", "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
print(out)
