"""Sound, captions, overlays and assembly for the Oddwick house-style SAMPLE ("I Have 3 Days to Pay for a Window").
python3.13 window_post.py -> samples/oddwick_style_sample.mp4  (run after window_shots.py)
Music: Kevin MacLeod (incompetech.com, CC BY 4.0) via github.com/dinglegames/dingle-radio (incompetech itself is blocked
from the cloud). SFX: wyzowl/sfx-kit (CC0) + Meta-open-sound corpora/oculus-audio-pack (CC BY 4.0, credit required) + crowd_sfx.py layers.
House style: 1-word Fredoka Bold yellow captions with a thick black outline at 70% height, money/days counter at the top,
Oddwick candle (brand/oddwick_avatar.png) lights up in second 1 and blows out on the last frame over the A/B candles."""
import os, sys, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, f"{REPO}/engine/oddwick")
import mix as MX

SLUG = "sample-oddwick-style-window"; W = f"/home/claude/work/{SLUG}"
DL = "/home/claude/dl"; KX = f"{DL}/sfx/sounds"; SYN = "/home/claude/work/syn"; FONT = "/root/.fonts/Fredoka-Bold.ttf"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; TOTAL = round(vo["total"] + 0.5, 2)
def meta(name):
    for r, _, fs in os.walk(f"{DL}/meta"):
        for f in fs:
            if f.startswith(name): return os.path.join(r, f)
    raise FileNotFoundError(name)
sfx = []
def S(f, t, g=0, *rest):
    p = f if f.startswith("/") else (f"{KX}/{f}" if "/" in f else (f"{SYN}/{f}" if os.path.exists(f"{SYN}/{f}") else meta(f)))
    sfx.append((p, t, g, *rest))
def D(i): return (L[i + 1] if i + 1 < len(L) else TOTAL) - L[i]
# --- hook: swing, smash
S("pops/pop-medium-in.wav", 0.12, -6); S("swishes-and-zips/swish-hard.wav", 0.25, -2)
S("GLASBrk_WindowPaneSmallBreak", 0.78, 0); S("GLASBrk_GlassBottleBreak", 0.8, -4); S("impacts/impact-medium-hard.wav", 0.78, -6)
S("TOONBoing_BounceCartoony_OS_02", 1.65, -6); S("foley/foley-glass-touch.wav", 2.8, -10); S("GLASImpt_GlassBottleDrop", 3.3, -10)
S("crowd_gasp.wav", L[1] + 0.45, -3); S("SWSH_Swoosh_OS_02", L[1] + 1.15, -6)
S("impacts/impact-light-firm.wav", L[2] + 0.6, -4); S("whooshes/whoosh-slow-soft.wav", L[2] + 2.3, -6); S("booms-and-bass/bass-rumble-short.wav", L[2] + 3.4, -4)
S("money/money-coin-drop.wav", L[3] + 0.35, -2); S("OBJCoin_CoinDrop", L[3] + 1.2, -6)
S("whooshes/whoosh-medium-soft.wav", L[4] - 0.1, -6); S("transform-deflate" and "shape-changes/transform-deflate.wav", L[4] + 1.2, -8)
# --- day one
S("whooshes/whoosh-fast-medium.wav", L[5] - 0.1, -4); S("foley/foley-wood-touch.wav", L[5] + 0.5, -4); S("shape-changes/transform-fill.wav", L[5] + 1.8, -6)
S("money/money-coin-drop.wav", L[6] + 0.4, -4); S("shape-changes/transform-empty.wav", L[6] + 0.7, -8); S("SWSH_Swoosh_OS_04", L[6] + 1.35, -8)
S("money/money-coin-spin.wav", L[6] + 1.9, -8)
# --- day two: dogs, bakery crash
S("ANMLDog_DogBark_OS_01", L[7] + 0.4, -2); S("ANMLDog_DogBark_OS_02", L[7] + 1.5, -4); S("ANMLDog_DogAttention", L[7] + 2.3, -6)
S("whooshes/whoosh-fast-hard.wav", L[8] - 0.05, -2); S("ANMLDog_DogBark_OS_02", L[8] + 0.3, -4)
for k in range(5): S(f"FEETHmn_ShoeConcreteRun_OS_0{k + 1}", L[8] + 0.15 + k * 0.22, -8)
S("DOORWood_FrontDoorOpen", L[8] + 1.25, -2); S("impacts/impact-heavy-hard.wav", L[8] + 1.35, -2); S("CERMImpt_CeramicSmallImpact", L[8] + 1.55, -4)
for k in range(3): S(f"GORESqsh_BloodSquishSlimy_OS_0{k + 1}", L[8] + 1.7 + k * 0.3, -8)
S("ANMLDog_DogBark_OS_01", L[8] + 2.2, -6)
S("CREAHmn_GiantEffort", L[9] + 0.1, -8); S("impacts/impact-light-firm.wav", L[9] + 1.0, -6); S("money/money-notes.wav", L[9] + 2.5, -4)
S("DOORKnck_OfficeDoorKnock", L[10] + 0.6, -2); S("PAPRHndl_PaperCrumple", L[10] + 2.3, -6); S("HMNBurp_Burp_OS_01", L[10] + 3.55, -4)
S("shape-changes/transform-deflate.wav", L[11] + 0.3, -6); S("money/money-coin-spin.wav", L[11] + 2.1, -6); S("OBJCoin_CoinDrop", L[11] + 3.3, -6)
# --- poster + game show
S("PAPRRip_PaperTear", L[12] + 0.2, -8); S("whooshes/whoosh-medium-medium.wav", L[12] + 0.0, -6); S("booms-and-bass/boom-hit-soft.wav", L[12] + 2.4, -4)
S("bounce-spin-zoom/move-zoom-in.wav", L[12] + 2.6, -6)
S("crowd_murmur.wav", L[13] - 0.1, -6); S("crowd_cheer.wav", L[13] + 0.3, -4); S("mechanical/mechanical-shutter-heavy.wav", L[13] + 1.5, -4)
S("mechanical/mechanical-shutter-light.wav", L[13] + 1.75, -6); S("applause.wav", L[13] + 2.6, -8)
S("mechanical/mechanical-switch-heavy.wav", L[14] + 0.45, -2); S("MUSCStngr_BanjoHumorous_OS_01", L[14] + 1.1, -4)
S("MUSCStngr_BanjoHumorous_OS_02", L[14] + 2.5, -4); S("crowd_laugh.wav", L[14] + 3.2, -8)
S("whooshes/whoosh-medium-soft.wav", L[15] - 0.05, -6); S("crowd_gasp.wav", L[15] + 1.7, -6); S("SWSH_Swoosh_OS_05", L[15] + 3.0, -8)
S("risers-and-fallers/riser-4s-soft.wav", L[16] + 0.2, -6); S("booms-and-bass/boom-hit-soft.wav", L[17] + 0.05, -4)
fb = L[18] + max(2, round(D(18) * 15) // 4) / 15
S("mechanical/mechanical-switch-heavy.wav", fb, 0); S("impacts/impact-heavy-hard.wav", fb, -4); S("crowd_cheer.wav", L[18] + 1.7, -2); S("applause.wav", L[18] + 1.9, -6)
# --- WRONG: hit + short silence
S("MUSCStngr_LossOrchestral_OS_01", L[19] - 0.05, 0); S("booms-and-bass/boom-drop-soft.wav", L[19], -4)
S("whooshes/whoosh-slow-soft.wav", L[20] + 1.4, -8)
S("MUSCStngr_VictoryOrchestral_OS_01", L[21] - 0.05, -2); S("celebration/celebration-confetti.wav", L[21] + 0.1, -4); S("crowd_cheer.wav", L[21] + 0.2, -2)
S("celebration/celebration-fireworks.wav", L[21] + 0.9, -2); S("celebration/celebration-popper.wav", L[21] + 2.0, -6); S("applause.wav", L[21] + 2.2, -6)
S("money/money-notes.wav", L[22] + 0.9, -4); S("crowd_cheer.wav", L[22] + 2.3, -8)
# --- the hat: throw, silence, smash (the twist)
S("whooshes/whoosh-medium-hard.wav", L[23] + 0.25, -2); S("whooshes/whoosh-slow-medium.wav", L[23] + 1.2, -6)
hit = (L[24] - 0.5) + max(3, int(round(1.5 * 15) * 0.5)) / 15
S("GLASBrk_WindowPaneSmallBreak", hit, 0); S("GLASBrk_GlassBottleBreak", hit + 0.02, -2); S("impacts/impact-deep-hard.wav", hit, -4)
S("crowd_gasp.wav", L[24] + 1.0, -4)
S("pops/pop-medium-in.wav", L[25] + 0.1, -8); S("TOONBoing_BounceCartoony_OS_03", L[25] + 2.5, -6); S("money/money-coin-drop.wav", L[25] + 2.9, -8)
S("pops/pop-large-in.wav", TOTAL - 3.6, -4); S("pops/pop-large-in.wav", TOTAL - 3.4, -4)
S("appear-and-vanish/appear-poof.wav", TOTAL - 0.65, -2)

# --- music: story-shaped, low-passed so no hats/bright percussion poke out under the voice
MUS = f"{W}/music"; os.makedirs(MUS, exist_ok=True)
def lp(name):
    o = f"{MUS}/{name}.wav"
    if not os.path.exists(o):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{DL}/km/{name}.mp3", "-af", "lowpass=f=5500,highpass=f=60", "-ac", "1", "-ar", "48000", o], check=True)
    return o
MB = float(os.environ.get("MUSIC_DB", "5"))
music = [
    (lp("sergios-magic-dustbin"), 0, 0.0, L[5] - 0.05, MB + 0, (0.02, 0.3)),            # curious set-up
    (lp("club-seamus"), 0, L[5] - 0.05, L[12], MB + 0, (0.05, 0.4)),                       # bouncy hustle montage
    (lp("le-grand-chase"), 2, L[12], L[16], MB - 1, (0.1, 0.4)),                            # game show energy
    (lp("goblin-tinker-soldier-spy"), 0, L[16], L[19] - 0.05, MB - 2, (0.3, 0.05)),         # tension; hard stop on WRONG
    (lp("hillbilly-swing"), 0, L[21] - 0.05, L[23] + 2.45, MB - 1, (0.05, 0.25)),            # bright celebration
    (lp("cloud-dancer"), 0, hit + 0.15, TOTAL, MB - 1, (0.3, 0.8)),                         # bright ending after the twist
]
mixf = MX.mix(SLUG, TOTAL, music, sfx)
def integ(p):
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(r[r.rfind("I:"):].split()[1])
dI = -14.0 - integ(mixf)          # single-pass loudnorm lands ~1 LU low: trim to exactly -14 LUFS with a true-peak limiter
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mixf, "-af", f"volume={dI:.2f}dB,alimiter=limit=0.84:level=false", f"{W}/mix_final.wav"], check=True)
mixf = f"{W}/mix_final.wav"; print("final mix I =", integ(mixf), "LUFS")
st = np.load(f"{W}/stems.npz")
def lufs_of(x, name):
    p = f"{W}/stem_{name}.wav"; sf.write(p, x, 12000)
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(r[r.rfind("I:"):].split()[1])
# stems are pre-loudnorm: report music bed relative to the final mix gain
r = subprocess.run(["ffmpeg", "-i", f"{W}/mix_raw.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
raw_I = float(r[r.rfind("I:"):].split()[1]); gain = integ(mixf) - raw_I
lv = {"music_bed_lufs_in_final": round(lufs_of(st["m"], "m") + gain, 1), "voice_lufs_in_final": round(lufs_of(st["v"], "v") + gain, 1),
      "sfx_lufs_in_final": round(lufs_of(st["s"], "s") + gain, 1)}
print("levels", lv); json.dump(lv, open(f"{W}/levels.json", "w"))
if os.environ.get("AUDIO_ONLY"): sys.exit()

# ---- picture: shots (15 fps) -> one 30 fps 1080x1920 film
timing = [] if os.environ.get("FAKE_FILM") else json.load(open(f"{W}/shots_timing.json")); parts = []
for sid, t0, t1 in timing:
    o = f"{W}/shots/{sid}.mp4"; parts.append(o)
    if os.path.exists(o) and os.path.getmtime(o) > os.path.getmtime(f"{W}/shots/{sid}/done"): continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "15", "-i", f"{W}/shots/{sid}/%04d.png",
                    "-vf", "scale=1080:1920:flags=lanczos,unsharp=5:5:0.7:5:5:0,fps=30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", o], check=True)
open(f"{W}/concat.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
film = f"{W}/film.mp4"
if os.environ.get("FAKE_FILM"):
    film = os.environ["FAKE_FILM"]
else:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{W}/concat.txt", "-c", "copy", film], check=True)

# ---- captions (1 word, yellow, thick black outline, ~70% height) + top counter
def ts(x): return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"
ass = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\n"
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
       "Style: C,Fredoka,138,&H0042F5F5,&H0042F5F5,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,13,6,5,30,30,0,1\n"
       "Style: T,Fredoka,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,8,4,8,40,40,0,1\n"
       "Style: H,Fredoka,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,10,5,8,40,40,0,1\n\n"
       "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
words = vo["words"]
for i, wd in enumerate(words):
    s0, s1 = wd["s"], wd["e"]; e = words[i + 1]["s"] if i + 1 < len(words) and words[i + 1]["s"] - s1 < 0.4 else s1 + 0.15
    clean = wd["w"].strip(".,!?:;\"'…")
    if not clean: continue
    ass += f"Dialogue: 0,{ts(s0)},{ts(max(e, s0 + 0.1))},C,,0,0,0,,{{\\pos(540,1344)\\fscx78\\fscy78\\t(0,80,\\fscx100\\fscy100)}}{clean.upper()}\n"
Y = "{\\c&H0042F5F5&}"
def T(t0, t1, txt, style="T", y=215):
    global ass; ass += f"Dialogue: 1,{ts(t0)},{ts(t1)},{style},,0,0,0,,{{\\pos(540,{y})\\fad(80,80)}}{txt}\n"
T(0.0, L[2], f"I BROKE IT.\\N{Y}NOW I OWE $1,000", "H", 190)
C = [(L[2], L[3], f"OWE {Y}$1,000{{\\c&HFFFFFF&}} BY SATURDAY"), (L[3], L[5], f"3 DAYS  ·  HAVE {Y}$4{{\\c&HFFFFFF&}} / $1,000"),
     (L[5], L[6] + 1.0, f"DAY 1  ·  HAVE {Y}$4"), (L[6] + 1.0, L[6] + 2.0, f"DAY 1  ·  HAVE {Y}$4.50"), (L[6] + 2.0, L[7], f"DAY 1  ·  HAVE {Y}$4"),
     (L[7], L[9] + 2.4, f"DAY 2  ·  OWE {Y}$1,000"), (L[9] + 2.4, L[11], f"DAY 2  ·  OWE {Y}$1,060"),
     (L[11], L[11] + 2.4, f"DAY 3  ·  HAVE {Y}$4"), (L[11] + 2.4, L[12], f"DAY 3  ·  HAVE {Y}$3"),
     (L[12], L[21], f"SATURDAY  ·  PRIZE {Y}$1,000"), (L[21], L[22] + 1.2, f"HAVE {Y}$1,003"), (L[22] + 1.2, L[24] + 1.0, f"HAVE {Y}$3  ·  WINDOW PAID"),
     (L[24] + 1.0, TOTAL - 3.7, f"MAYOR OWES ME {Y}$1,000")]
for t0, t1, txt in C: T(t0, t1, txt)
ass += f"Dialogue: 1,{ts(TOTAL - 3.7)},{ts(TOTAL)},T,,0,0,0,,{{\\pos(540,215)\\fad(120,0)}}WHAT SHOULD I DO?\n"
open(f"{W}/caps.ass", "w").write(ass)

# ---- Oddwick candle overlays (real brand PNG, never AI): sign-on + A/B candles that blow out on the last frame
av = Image.open(f"{REPO}/brand/oddwick_avatar.png").convert("RGBA")
def card(img, size, radius=0.18):
    im = img.resize((size, size), Image.LANCZOS); m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), int(size * radius), fill=255); im.putalpha(m); return im
def blown(img):
    im = img.copy(); reg = (300, 40, 560, 350)
    patch = im.crop(reg).filter(ImageFilter.GaussianBlur(40)); im.paste(patch, reg[:2])
    d = ImageDraw.Draw(im, "RGBA")
    d.line((400, 375, 392, 340, 405, 318), fill=(30, 22, 48, 255), width=12)           # bare wick
    for k, (x, y, r) in enumerate(((405, 290, 22), (420, 240, 30), (400, 185, 36), (430, 125, 40))):
        d.ellipse((x - r, y - r, x + r, y + r), fill=(205, 200, 215, 150 - k * 25))
    im = Image.blend(im, Image.new("RGBA", im.size, (20, 12, 40, 255)), 0.35); return im
lit, out = av, blown(av)
OV = f"{W}/ov"; os.makedirs(OV, exist_ok=True)
fnt = ImageFont.truetype(FONT, 54); fbig = ImageFont.truetype(FONT, 96)
def label(d, xy, txt, f, fill=(255, 255, 255), anchor="mm"):
    d.text(xy, txt, font=f, fill=fill, anchor=anchor, stroke_width=8, stroke_fill=(0, 0, 0))
# sign-on (0 - 1.3 s): unlit candle pops in top-right, lights at 0.2 s, shrinks away
n_in = int(1.3 * 30)
for f in range(n_in):
    t = f / 30; fr = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    s = 170 * min(1, t / 0.12) * (1 if t < 1.05 else max(0.01, 1 - (t - 1.05) / 0.25))
    if s > 4:
        c = card(lit if t >= 0.2 else out, int(s)); fr.alpha_composite(c, (int(985 - s / 2), int(395 - s / 2)))
    fr.save(f"{OV}/in_{f:03d}.png")
# A/B ending (last 3.7 s): two Oddwick candles = the choices; both blow out over the final 0.5 s (last frame = smoke)
n_out = int(3.7 * 30)
for f in range(n_out):
    t = f / 30; fr = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(fr)
    for k, (cx, tag, line1, line2) in enumerate(((290, "A", "MAYOR CLEANS", "THE TOWER"), (790, "B", "DOUBLE OR", "NOTHING"))):
        a = min(1, max(0, (t - 0.2 * k) / 0.18));
        if a <= 0: continue
        s = int(340 * (0.6 + 0.4 * a)); src = out if t > 3.7 - 0.55 + 0.08 * k else lit
        fr.alpha_composite(card(src, s), (cx - s // 2, 760 - s // 2))
        label(d, (cx, 760 - s // 2 - 60), tag, fbig, (245, 245, 66)); label(d, (cx, 760 + s // 2 + 45), line1, fnt); label(d, (cx, 760 + s // 2 + 105), line2, fnt)
    fr.save(f"{OV}/out_{f:03d}.png")

# ---- final mux: film + overlays + captions + mix
os.makedirs(f"{REPO}/samples", exist_ok=True); outp = os.environ.get("OUT") or f"{REPO}/samples/oddwick_style_sample.mp4"
t_out = TOTAL - 3.7
fc = (f"[1:v]setpts=PTS-STARTPTS[a];[2:v]setpts=PTS-STARTPTS+{t_out:.3f}/TB[b];"
      f"[0:v][a]overlay=0:0:eof_action=pass[v1];[v1][b]overlay=0:0:eof_action=repeat:enable='gte(t,{t_out:.3f})'[v2];[v2]ass={W}/caps.ass[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", film, "-framerate", "30", "-i", f"{OV}/in_%03d.png", "-framerate", "30", "-i", f"{OV}/out_%03d.png", "-i", mixf,
                "-filter_complex", fc, "-map", "[v]", "-map", "3:a", "-t", f"{TOTAL:.2f}", "-r", "30",
                "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", "-profile:v", "high",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", outp], check=True)
print(outp, round(os.path.getsize(outp) / 1e6, 1), "MB")
