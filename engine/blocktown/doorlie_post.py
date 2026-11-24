"""Sound, captions, overlays and assembly for the 2026-11-24 daily Short "Every Door in This House Is a Lie".
python3.13 doorlie_post.py            -> out/<slug>.mp4      (YouTube + Instagram)
TT=1 python3.13 doorlie_post.py       -> out/<slug>_tt.mp4   (TikTok: different first 2 s hook banner + zoom, own encode)
Music: Kevin MacLeod (incompetech.com, CC BY 4.0) via github.com/dinglegames/dingle-radio. SFX: wyzowl/sfx-kit (CC0) +
Meta-open-sound corpora/oculus-audio-pack (CC BY 4.0, credited) + crowd_sfx.py layers (Kokoro voices + CC0 claps).
House style (PLAYBOOK "OWNER REFERENCE STYLE 2026-11-20"): 1-word Fredoka Bold yellow captions with a thick black outline at
70 % height, hours/players counter at the top, Oddwick candle (brand/oddwick_avatar.png) sign-on + A/B candles blowing out."""
import os, sys, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, f"{REPO}/engine/oddwick")
import mix as MX

SLUG = "2026-11-24-every-door-in-this-house-lies"; W = f"/home/claude/work/{SLUG}"; TT = bool(os.environ.get("TT"))
DL = "/home/claude/dl"; KX = f"{DL}/sfx/sounds"; SYN = "/home/claude/work/syn"; FONT = "/root/.fonts/Fredoka-Bold.ttf"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; TOTAL = round(vo["total"] + 1.5, 2)
tim = {sid: (t0, t1) for sid, t0, t1 in json.load(open(f"{W}/shots_timing.json"))}
def st(sid, frac=0.0, frames=None):
    t0, t1 = tim[sid]; return t0 + (frames / 12 if frames is not None else (t1 - t0) * frac)
def NF(sid): t0, t1 = tim[sid]; return max(2, round((t1 - t0) * 12))
def meta(name):
    for r, _, fs in os.walk(f"{DL}/meta"):
        for f in sorted(fs):
            if f.startswith(name): return os.path.join(r, f)
    raise FileNotFoundError(name)
sfx = []
def S(f, t, g=0, *rest):
    p = f if f.startswith("/") else (f"{KX}/{f}" if "/" in f else (f"{SYN}/{f}" if os.path.exists(f"{SYN}/{f}") else meta(f)))
    sfx.append((p, t, g, *rest))

def walk(prefix, t0, n, gap, g=-12):
    for k in range(n): S(f"{prefix}_OS_0{k % 5 + 1}", t0 + k * gap, g)
DOPEN = "DOORWood_FrontDoorOpen_OS_01"
# --- hook: candle pop, the Lying House, crowd
S("pops/pop-medium-in.wav", 0.12, -6); S("crowd_murmur.wav", 0.1, -12); S("whooshes/whoosh-medium-soft.wav", 0.05, -8)
S("whooshes/whoosh-slow-medium.wav", st("s02") - 0.1, -6); S("WOODFric_CreaksCreepy_OS_01", st("s02") + 0.1, -10)
S("cinematic-hits/cinematic-drum-big.wav", st("s03"), -4); S("booms-and-bass/boom-hit-soft.wav", st("s03"), -6)
# --- nobody got out, not even the mailman
S("crowd_gasp.wav", st("s04") + 0.1, -6); S("MUSCStngr_LossMallet_OS_01", st("s04") + 0.3, -10)
walk("FEETHmn_ShoeConcreteWalk", st("s05") + 0.05, 5, 0.33, -14); S("DOORWood_FrontDoorClose_OS_01", st("s05", 0.68), -4)
S("foley/foley-paper-slide.wav", st("s06") + 0.05, -4); S("foley/foley-paper-slide.wav", st("s06") + 0.35, -6); S("PAPRImpt_PaperBallDrop_OS_01", st("s06") + 0.5, -6)
# --- the Mayor locks me in; $5,000 or a year of mowing
S("MECHLock_DoorLockKey_OS_02", st("s07") + 0.1, -2); S("MECHLock_DoorLockKey_OS_03", st("s07") + 0.6, -4); S("VOXLaff_EvilLaugh_OS_01", st("s07") + 0.9, -14)
S("money/money-register.wav", st("s08") + 0.05, -2); S("crowd_cheer.wav", st("s08"), -4); S("celebration/celebration-confetti.wav", st("s08") + 0.15, -6)
S("VEHCar_CarEngineSlow_LOOP_01", st("s09"), -14, 0, 2.2); S("MUSCStngr_LossPiano_OS_01", st("s09") + 0.6, -8)
# --- minute 1: stairs into the ceiling
S("whooshes/whoosh-fast-medium.wav", st("s10") - 0.05, -6); S("MUSCStngr_AcousticGuitarPositive_OS_02", st("s10") + 0.1, -10)
walk("FEETHmn_ShoeWoodRun", st("s11") + 0.05, 8, 0.17, -10)
S("impacts/impact-heavy-hard.wav", st("s12", frames=3), 0); S("bounce-spin-zoom/move-spring.wav", st("s12", frames=3) + 0.05, -6); S("cinematic-hits/cinematic-metal-big.wav", st("s12", frames=3), -16)
S("bounce-spin-zoom/move-spin.wav", st("s13") + 0.1, -10)
# --- minute 10: the red door, a brick wall
walk("FEETHmn_ShoeWoodWalk", st("s14") + 0.05, 4, 0.38, -12)
S(DOPEN, st("s15") + 0.02, 0); S("whooshes/whoosh-fast-hard.wav", st("s15") + 0.05, -8)
S("booms-and-bass/boom-drop-soft.wav", st("s16") + 0.1, -4); S("MUSCStngr_LossMallet_OS_01", st("s16") + 0.3, -8)
# --- minute 20: window behind a window, Benny squished
S("whooshes/whoosh-medium-soft.wav", st("s17") - 0.05, -8)
S("DOORHdwr_GlassDoorKnob_OS_01", st("s18") + 0.02, -2); S("foley/foley-glass-slide.wav", st("s18") + 0.12, -4)
S("booms-and-bass/boom-hit-soft.wav", st("s19") + 0.05, -6); S("pops/pop-small-out.wav", st("s19") + 0.1, -6)
S("foley/foley-glass-slide.wav", st("s20") + 0.05, -4); S("DOORHdwr_GlassDoorKnob_OS_01", st("s20"), -6)
S("foley/foley-glass-touch.wav", st("s21") + 0.02, 0); S("pops/pop-large-bubble.wav", st("s21") + 0.08, -4); S("VOXLaff_Male02Laugh_OS_01", st("s21") + 0.6, -14)
# --- minute 30: 2nd-floor door, the kitchen sink
S("whooshes/whoosh-slow-medium.wav", st("s22"), -8); S("WOODFric_CreaksCreepy_OS_02", st("s22") + 0.2, -10)
S(DOPEN, st("s23") + 0.02, -2)
S("whooshes/whoosh-fast-medium.wav", st("s24"), -4); S("everyday-props/props-splash.wav", st("s24", frames=max(3, NF("s24") // 3)), 0)
S("impacts/impact-medium-soft.wav", st("s24", frames=max(3, NF("s24") // 3)), -6); S("everyday-props/props-drip.wav", st("s24", frames=max(3, NF("s24") // 3)) + 0.5, -8)
# --- minute 40: shoebox door, brooms
S("bounce-spin-zoom/move-zoom-in.wav", st("s25") + 0.05, -8); S("pops/pop-small-in.wav", st("s25") + 0.3, -8)
S("foley/foley-fabric-slide.wav", st("s26"), -2); S("foley/foley-fabric-slide.wav", st("s26") + 0.35, -4); S("bounce-spin-zoom/move-spring.wav", st("s26") + 0.2, -8)
S("foley/foley-wood-touch.wav", st("s27") + 0.02, -2); S("foley/foley-wood-slide.wav", st("s27") + 0.15, -4); S("MUSCStngr_BanjoHumorous_OS_01", st("s27") + 0.5, -8)
# --- minute 50: the town watches, popcorn
S("cinematic-hits/cinematic-drum-big.wav", st("s28"), -4); S("crowd_murmur.wav", st("s29"), -8)
for k in range(5): S("pops/pop-small-bubble.wav", st("s30") + 0.1 + k * 0.25, -6)
# --- five minutes: wall, wall, closet, wall
walk("FEETHmn_ShoeWoodRun", st("s31") + 0.03, 4, 0.15, -10)
for sid, hit in (("s32", "impacts/impact-heavy-soft.wav"), ("s33", "impacts/impact-heavy-firm.wav"), ("s34", "foley/foley-wood-slide.wav"), ("s35", "impacts/impact-heavy-hard.wav")):
    S(DOPEN, st(sid) + 0.0, -2); S(hit, st(sid) + 0.2, -4)
# --- the last door: NOT AN EXIT
S("booms-and-bass/bass-rumble-short.wav", st("s36"), -8); S("whooshes/whoosh-slow-soft.wav", st("s36") + 0.1, -10)
S("foley/foley-paper-touch.wav", st("s37") + 0.05, -4); S("cinematic-hits/cinematic-drum-big.wav", st("s38") + 0.02, -4)
S("whooshes/whoosh-slow-hard.wav", st("s39") + 0.05, -6); S("DOORHdwr_OfficeDoorKnob_OS_01", st("s40") + 0.3, -4)
# --- the door opens: sunlight, the square, 3 seconds left
S(DOPEN, st("s41") + 0.02, 0); S("whooshes/whoosh-medium-hard.wav", st("s41") + 0.1, -4); S("AMBForst_ForestBirds_OS_01", st("s41") + 0.2, -10)
S("crowd_gasp.wav", st("s42") + 0.05, -4); walk("FEETHmn_ShoeConcreteRun", st("s42") + 0.05, 5, 0.15, -10)
S("cinematic-hits/cinematic-drum-massive.wav", st("s43") - 0.02, -2)
S("crowd_cheer.wav", st("s44") - 0.05, 0); S("celebration/celebration-applause-big.wav", st("s44") + 0.1, -4); S("celebration/celebration-fireworks.wav", st("s44") + 0.2, -6)
S("celebration/celebration-popper.wav", st("s44") + 0.05, -4); S("MUSCStngr_VictoryOrchestral_OS_01", st("s44") + 0.1, -8); S("money/money-register.wav", st("s44") + 1.0, -6)
# --- the mailman walks out
walk("FEETHmn_ShoeConcreteWalk", st("s45") + 0.1, 4, 0.42, -12); S("crowd_gasp.wav", st("s45") + 0.6, -8)
S("foley/foley-paper-slide.wav", st("s46") + 0.1, -4); S("MUSCStngr_BanjoHumorous_OS_02", st("s46") + 0.3, -8)
# --- this part is real
S("booms-and-bass/boom-hit-soft.wav", st("s47"), -4); S("whooshes/whoosh-medium-medium.wav", st("s47") - 0.05, -8)
S("whooshes/whoosh-slow-soft.wav", st("s48") + 0.1, -8); S(DOPEN, st("s49") + 0.15, -2); S("impacts/impact-heavy-soft.wav", st("s49") + 0.5, -6)
S("AMBCnst_ConstructionSiteMedium_LOOP_01", st("s50"), -14, 0, 2.4); S("crowd_murmur.wav", st("s50") + 0.2, -14)
# --- the golden envelope... one more envelope
S("whooshes/whoosh-fast-soft.wav", st("s51") + 0.1, -8); S("celebration/celebration-popper.wav", st("s51") + 0.6, -8)
S("foley/foley-paper-slide.wav", st("s52") + 0.1, -2); S("foley/foley-paper-touch.wav", st("s52") + 0.4, -4)
S("MUSCStngr_LossMallet_OS_01", st("s53") + 0.15, -4); S("crowd_laugh.wav", st("s53") + 0.35, -10)
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
    (lp("sergios-magic-dustbin"), 0, 0.0, L[3] - 0.05, MB + 0, (0.02, 0.3)),               # curious: the Lying House
    (lp("club-seamus"), 0, L[3] - 0.05, L[9] - 0.1, MB - 1, (0.1, 0.3)),                     # bouncy: the door gags
    (lp("goblin-tinker-soldier-spy"), 0, L[9] - 0.1, L[12] - 0.05, MB - 1, (0.1, 0.12)),     # tension: the countdown; hit + silence on "Wait."
    (lp("cloud-dancer"), 0, L[13] + 0.6, L[16] - 0.3, MB - 1, (0.3, 0.3)),                  # bright: sunlight, I made it, the mailman
    (lp("hillbilly-swing"), 0, L[16] - 0.3, L[17] - 0.1, MB - 2, (0.2, 0.3)),               # the real fact
    (lp("farting-around"), 0, L[17] - 0.05, TOTAL, MB - 2, (0.2, 0.8)),                      # the envelope callback + A/B
]
S("cinematic-hits/cinematic-slam-big.wav", L[12] - 0.08, -4)
mixf = MX.mix(SLUG, TOTAL, music, sfx)
def integ(p):
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(r[r.rfind("I:"):].split()[1])
dI = -14.0 - integ(mixf)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mixf, "-af", f"volume={dI:.2f}dB,alimiter=limit=0.84:level=false", f"{W}/mix_final.wav"], check=True)
mixf = f"{W}/mix_final.wav"; print("final mix I =", integ(mixf), "LUFS")
stm = np.load(f"{W}/stems.npz")
def lufs_of(x, name):
    p = f"{W}/stem_{name}.wav"; sf.write(p, x, 12000)
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(r[r.rfind("I:"):].split()[1])
r = subprocess.run(["ffmpeg", "-i", f"{W}/mix_raw.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
raw_I = float(r[r.rfind("I:"):].split()[1]); gain = integ(mixf) - raw_I
lv = {"music_bed_lufs_in_final": round(lufs_of(stm["m"], "m") + gain, 1), "voice_lufs_in_final": round(lufs_of(stm["v"], "v") + gain, 1),
      "sfx_lufs_in_final": round(lufs_of(stm["s"], "s") + gain, 1)}
print("levels", lv); json.dump(lv, open(f"{W}/levels.json", "w"))
if os.environ.get("AUDIO_ONLY"): sys.exit()

# ---- picture: shots (12 fps) -> one 30 fps 1080x1920 film
timing = json.load(open(f"{W}/shots_timing.json")); parts = []
for sid, t0, t1 in timing:
    o = f"{W}/shots/{sid}.mp4"; parts.append(o)
    if os.path.exists(o) and os.path.getmtime(o) > os.path.getmtime(f"{W}/shots/{sid}/done"): continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "12", "-i", f"{W}/shots/{sid}/%04d.png",
                    "-vf", "scale=1080:1920:flags=lanczos,unsharp=5:5:0.7:5:5:0,fps=30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", o], check=True)
open(f"{W}/concat.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
film = f"{W}/film.mp4"
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
Y = "{\\c&H0042F5F5&}"; Wt = "{\\c&HFFFFFF&}"
def T(t0, t1, txt, style="T", y=215):
    global ass; ass += f"Dialogue: 1,{ts(t0)},{ts(t1)},{style},,0,0,0,,{{\\pos(540,{y})\\fad(80,80)}}{txt}\n"
if TT:
    T(0.0, L[2], f"I HAD {Y}1 HOUR{Wt}\\NTO ESCAPE THIS", "H", 190)
else:
    T(0.0, L[2], f"EVERY DOOR\\NIS A {Y}LIE", "H", 190)
C = [(L[2], L[3], f"WIN {Y}$5,000{Wt} IN 1 HOUR"), (L[3], L[4], f"{Y}59:00{Wt} LEFT"), (L[4], L[5], f"{Y}50:00{Wt} LEFT"), (L[5], L[7], f"{Y}40:00{Wt} LEFT"),
     (L[7], L[8], f"{Y}30:00{Wt} LEFT"), (L[8], L[9], f"{Y}20:00{Wt} LEFT"), (L[9], L[10], f"{Y}10:00{Wt} LEFT"), (L[10], L[11], f"{Y}5:00{Wt} LEFT"),
     (L[11], L[12], f"{Y}0:30{Wt} LEFT"), (L[12], L[13], f"{Y}0:10{Wt} LEFT"), (L[13], L[14], f"{Y}0:03{Wt} LEFT"), (L[14], L[15], f"{Y}ESCAPED!"),
     (L[15], L[16], f"LOST FOR {Y}3 YEARS"), (L[16], L[17], f"{Y}REAL:{Wt} WINCHESTER HOUSE, CA"), (L[17], TOTAL - 3.7, f"THE {Y}PRIZE{Wt}...")]
for t0, t1, txt in C: T(t0, t1, txt)
ass += f"Dialogue: 1,{ts(TOTAL - 3.7)},{ts(TOTAL)},T,,0,0,0,,{{\\pos(540,215)\\fad(120,0)}}TRUST THE DOOR?\n"
open(f"{W}/caps{'_tt' if TT else ''}.ass", "w").write(ass)

# ---- Oddwick candle overlays (real brand PNG, never AI): sign-on + A/B candles that blow out on the last frame
av = Image.open(f"{REPO}/brand/oddwick_avatar.png").convert("RGBA")
def card(img, size, radius=0.18):
    im = img.resize((size, size), Image.LANCZOS); m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), int(size * radius), fill=255); im.putalpha(m); return im
def blown(img):
    im = img.copy(); reg = (300, 40, 560, 350)
    patch = im.crop(reg).filter(ImageFilter.GaussianBlur(40)); im.paste(patch, reg[:2])
    d = ImageDraw.Draw(im, "RGBA")
    d.line((400, 375, 392, 340, 405, 318), fill=(30, 22, 48, 255), width=12)
    for k, (x, y, r) in enumerate(((405, 290, 22), (420, 240, 30), (400, 185, 36), (430, 125, 40))):
        d.ellipse((x - r, y - r, x + r, y + r), fill=(205, 200, 215, 150 - k * 25))
    return Image.blend(im, Image.new("RGBA", im.size, (20, 12, 40, 255)), 0.35)
lit, out = av, blown(av)
OV = f"{W}/ov"; os.makedirs(OV, exist_ok=True)
fnt = ImageFont.truetype(FONT, 54); fbig = ImageFont.truetype(FONT, 96)
def label(d, xy, txt, f, fill=(255, 255, 255), anchor="mm"):
    d.text(xy, txt, font=f, fill=fill, anchor=anchor, stroke_width=8, stroke_fill=(0, 0, 0))
n_in = int(1.3 * 30)
for f in range(n_in):
    t = f / 30; fr = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    s = 170 * min(1, t / 0.12) * (1 if t < 1.05 else max(0.01, 1 - (t - 1.05) / 0.25))
    if s > 4:
        c = card(lit if t >= 0.2 else out, int(s)); fr.alpha_composite(c, (int(985 - s / 2), int(395 - s / 2)))
    fr.save(f"{OV}/in_{f:03d}.png")
n_out = int(3.7 * 30)
for f in range(n_out):
    t = f / 30; fr = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(fr)
    for k, (cx, tag, line1, line2) in enumerate(((290, "A", "TRUST", "IT"), (790, "B", "NO", "WAY"))):
        a = min(1, max(0, (t - 0.2 * k) / 0.18))
        if a <= 0: continue
        s = int(340 * (0.6 + 0.4 * a)); src = out if t > 3.7 - 0.55 + 0.08 * k else lit
        fr.alpha_composite(card(src, s), (cx - s // 2, 760 - s // 2))
        label(d, (cx, 760 - s // 2 - 60), tag, fbig, (245, 245, 66)); label(d, (cx, 760 + s // 2 + 45), line1, fnt); label(d, (cx, 760 + s // 2 + 105), line2, fnt)
    fr.save(f"{OV}/out_{f:03d}.png")

# ---- final mux: film + overlays + captions + mix
os.makedirs(f"{REPO}/out", exist_ok=True); outp = f"{REPO}/out/{SLUG}{'_tt' if TT else ''}.mp4"
t_out = TOTAL - 3.7
# TikTok cut: the first 2 s are punched in 8 % (different opening frames) + its own banner and encode
v0 = "[0:v]split[q0][q1];[q0]trim=0:2,crop=iw/1.08:ih/1.08:(iw-iw/1.08)/2:(ih-ih/1.08)/3,scale=1080:1920,setsar=1[p0];[q1]setsar=1[q2];[q2][p0]overlay=0:0:eof_action=pass[base];" if TT else "[0:v]null[base];"
fc = (v0 + f"[1:v]setpts=PTS-STARTPTS[a];[2:v]setpts=PTS-STARTPTS+{t_out:.3f}/TB[b];"
      f"[base][a]overlay=0:0:eof_action=pass[v1];[v1][b]overlay=0:0:eof_action=repeat:enable='gte(t,{t_out:.3f})'[v2];[v2]ass={W}/caps{'_tt' if TT else ''}.ass[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", film, "-framerate", "30", "-i", f"{OV}/in_%03d.png", "-framerate", "30", "-i", f"{OV}/out_%03d.png", "-i", mixf,
                "-filter_complex", fc, "-map", "[v]", "-map", "3:a", "-t", f"{TOTAL:.2f}", "-r", "30",
                "-c:v", "libx264", "-preset", "medium", "-crf", "22" if TT else "23", "-pix_fmt", "yuv420p", "-profile:v", "high",
                "-c:a", "aac", "-b:a", "160k" if not TT else "192k", "-movflags", "+faststart", outp], check=True)
print(outp, round(os.path.getsize(outp) / 1e6, 1), "MB")
