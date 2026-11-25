"""Sound, captions, overlays and assembly for the 2026-11-25 daily Short "Every Wrong Answer, I Got Smaller".
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

SLUG = "2026-11-25-every-wrong-answer-i-shrank"; W = f"/home/claude/work/{SLUG}"; TT = bool(os.environ.get("TT"))
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
def ZAP(t):   # shrink-ray zap: thunder crack + magic + zoom-out whoosh (no beeps)
    S("cinematic-hits/cinematic-thunder-big.wav", t + 0.12, -13); S("MAGSpel_MagicSpell_OS_01", t + 0.1, -12); S("bounce-spin-zoom/move-zoom-out.wav", t + 0.2, -8)
    S("impacts/impact-medium-hard.wav", t + 0.12, -12)
fr = lambda sid, f: st(sid, frames=f - 1)
# --- hook: candle pop, zap, crowd
S("pops/pop-medium-in.wav", 0.12, -6); S("crowd_murmur.wav", 0.1, -12); ZAP(fr("s01", 3)); S("crowd_gasp.wav", fr("s01", 4), -8)
S("whooshes/whoosh-fast-medium.wav", st("s02") - 0.08, -6); S("cinematic-hits/cinematic-drum-big.wav", st("s02"), -8)
S("money/money-register.wav", st("s03") + 0.05, -2); S("crowd_cheer.wav", st("s03"), -4); S("celebration/celebration-confetti.wav", st("s03") + 0.15, -6)
S("booms-and-bass/boom-hit-soft.wav", st("s04"), -4); S("MUSCStngr_LossMallet_OS_01", st("s04") + 0.3, -10)
# --- Mrs. Pickles, bingo champ
S("whooshes/whoosh-slow-medium.wav", st("s05") - 0.05, -8)
for k in range(4): S("foley/foley-wood-touch.wav", st("s05") + 0.3 + k * 0.33, -12)
S("VOXLaff_Female01Laugh_OS_01", st("s06") + 0.2, -14); S("MUSCStngr_VictoryMallet_OS_01", st("s07") + 0.05, -10); S("foley/foley-glass-touch.wav", st("s07") + 0.1, -8)
# --- the Mayor; Q1 banana
S("crowd_cheer.wav", st("s08"), -8); S("celebration/celebration-applause-small.wav", st("s08") + 0.1, -8); S("whooshes/whoosh-medium-soft.wav", fr("s08", 5), -10)
S("foley/foley-card-slide.wav", st("s09") + 0.1, -6)
S("interface/click-button-firm.wav", fr("s10", 3), 0); S("impacts/impact-light-firm.wav", fr("s10", 3), -6); S("celebration/celebration-popper.wav", st("s10") + 0.25, -8); S("crowd_cheer.wav", st("s10") + 0.2, -10)
# --- Q2 octopus, wrong, zap, hydrant
S("WATRBubl_WaterBubbles_LOOP_01", st("s11"), -10, 0, 2.2); S("pops/pop-small-in.wav", fr("s12", 4), -6)
S("MUSCStngr_LossOrchestral_OS_01", st("s13") + 0.02, -6); S("crowd_gasp.wav", st("s13") + 0.15, -8)
ZAP(fr("s14", 2)); S("TOONBoing_BounceCartoony_OS_01", st("s15") + 0.1, -8); S("crowd_laugh.wav", st("s15") + 0.2, -12)
S("foley/foley-fabric-touch.wav", st("s16") + 0.1, -8)
for k in range(5): S("foley/foley-wood-touch.wav", st("s17") + 0.1 + k * 0.28, -8)
# --- Q3 shark, zap, the cat
S("foley/foley-card-slide.wav", st("s18") + 0.1, -6)
for k in range(3): S(f"FEETHmn_ShoeWoodLand_OS_0{k % 2 + 1}", st("s19") + 0.25 * (k + 1), -10)
ZAP(fr("s20", 2)); S("bounce-spin-zoom/move-spring.wav", st("s21") + 0.15, -8); S("crowd_laugh.wav", st("s21") + 0.3, -10)
# --- Benny falls off his chair
S("crowd_laugh.wav", st("s22"), -6); S("VOXLaff_Male02Laugh_OS_01", st("s22") + 0.1, -6)
S("WOODImpt_LargeWoodDrop_OS_01", fr("s23", max(2, NF("s23") // 3) + 4), 0); S("impacts/impact-medium-soft.wav", fr("s23", max(2, NF("s23") // 3) + 4), -6); S("VOXLaff_Male01Laugh_OS_01", st("s23") + 0.1, -8)
# --- Q4 pizza, zap, hamster size
S("pops/pop-small-bubble.wav", st("s24") + 0.4, -6); S("MUSCStngr_BanjoHumorous_OS_01", st("s25") + 0.2, -8); S("crowd_murmur.wav", st("s25"), -12)
ZAP(fr("s26", 2)); S("bounce-spin-zoom/move-zoom-in.wav", st("s27"), -8); S("whooshes/whoosh-slow-soft.wav", st("s28"), -8)
S("crowd_cheer.wav", st("s29"), -12); S("WOODFric_CreaksCreepy_OS_01", st("s30") + 0.1, -14); S("pops/pop-small-out.wav", fr("s31", 3), -6)
S("cinematic-hits/cinematic-drum-big.wav", st("s32"), -4); S("MUSCStngr_LossPiano_OS_01", st("s33") + 0.05, -8)
# --- the gust of wind, the cards
S("whooshes/whoosh-slow-hard.wav", st("s34") - 0.05, -2); S("CLOTHFlp_FlagFlapping_LOOP_01", st("s34"), -6, 0, 2.0); S("PAPRHndl_BookPageTurns_OS_01", st("s34") + 0.2, -4)
S("whooshes/whoosh-fast-soft.wav", st("s35") + 0.05, -6); S("foley/foley-card-touch.wav", fr("s35", 4), -2)
# --- last question
S("cinematic-hits/cinematic-drum-massive.wav", st("s36") - 0.02, -2); S("crowd_gasp.wav", st("s36") + 0.3, -10); S("WATRBubl_WaterBubbles_LOOP_01", st("s37"), -12, 0, 1.6)
S("cinematic-hits/cinematic-slam-big.wav", L[14] - 0.08, -4)
S("booms-and-bass/bass-rumble-short.wav", st("s39"), -8); S("foley/foley-fabric-slide.wav", st("s39") + 0.3, -8)
S("whooshes/whoosh-fast-medium.wav", st("s40"), -4); S("VOXEfrt_Male01Effort_OS_01", st("s40") + 0.05, -12)
S("impacts/impact-heavy-hard.wav", fr("s41", 3), 0); S("interface/click-button-firm.wav", fr("s41", 3), 0); S("crowd_gasp.wav", fr("s41", 3) + 0.1, -6)
# --- THREE! correct, 11-8, $10,000
S("crowd_cheer.wav", st("s43") + 0.45, -4); S("celebration/celebration-applause-big.wav", st("s43") + 0.5, -8); S("celebration/celebration-popper.wav", st("s43") + 0.05, -6)
S("MUSCStngr_VictoryOrchestral_OS_01", st("s43") + 0.1, -8); S("celebration/celebration-fireworks.wav", st("s44") + 0.1, -4); S("money/money-register.wav", st("s44") + 0.15, -4)
S("MAGSpel_MagicSpell_OS_02", st("s45"), -6); S("appear-and-vanish/appear-materialise.wav", st("s46") + 0.1, -4); S("bounce-spin-zoom/move-spring.wav", st("s46") + 0.4, -6); S("crowd_cheer.wav", st("s46") + 0.5, -8)
# --- this part is real: three hearts
S("booms-and-bass/boom-hit-soft.wav", st("s47"), -4); S("whooshes/whoosh-medium-medium.wav", st("s47") - 0.05, -8)
for k in range(3): S("pops/pop-large-bubble.wav", fr("s48", 1 + k * 4) + 0.05, -6)
S("WATRBubl_WaterBubbles_LOOP_01", st("s49"), -14, 0, 2.0)
# --- the twist: giant Mrs. Pickles
S("booms-and-bass/boom-drop-strong.wav", st("s50"), -2); S("impacts/impact-deep-hard.wav", st("s50") + 0.25, -4); S("crowd_gasp.wav", st("s50") + 0.3, -4)
S("impacts/impact-deep-hard.wav", st("s51") + 0.1, -4); S("impacts/impact-deep-firm.wav", st("s51") + 0.8, -6); S("crowd_gasp.wav", st("s51") + 0.4, -8)
S("foley/foley-fabric-slide.wav", st("s52") + 0.1, -2); S("VOXLaff_Female02Laugh_OS_01", st("s52") + 0.5, -10); S("crowd_laugh.wav", st("s52") + 0.8, -10)
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
    (lp("sergios-magic-dustbin"), 0, 0.0, L[3] - 0.05, MB + 0, (0.02, 0.3)),            # curious: the show, the rival, the host
    (lp("club-seamus"), 0, L[3] - 0.05, L[11] - 0.1, MB - 1, (0.1, 0.3)),                 # bouncy: zap gags
    (lp("goblin-tinker-soldier-spy"), 0, L[11] - 0.1, L[14] - 0.08, MB - 1, (0.1, 0.1)), # tension: 8-1, the wind, last question; hit + silence on "Wait"
    (lp("le-grand-chase"), 0, L[15] - 0.05, L[16] - 0.1, MB - 1, (0.05, 0.15)),          # the buzzer race
    (lp("cloud-dancer"), 0, L[16] - 0.1, L[18] - 0.2, MB - 1, (0.1, 0.3)),               # bright: I won, I grow back
    (lp("hillbilly-swing"), 0, L[18] - 0.2, L[19] - 0.08, MB - 2, (0.2, 0.08)),          # the real fact; hit + silence before the twist
    (lp("farting-around"), 0, L[19] + 0.45, TOTAL, MB - 2, (0.2, 0.8)),                  # the giant twist + A/B
]
S("cinematic-hits/cinematic-slam-big.wav", L[19] - 0.06, -6)
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
    T(0.0, L[1], f"I SHRANK ON\\N{Y}LIVE TV", "H", 190)
else:
    T(0.0, L[1], f"EVERY WRONG ANSWER\\N= {Y}YOU SHRINK", "H", 190)
C = [(L[1], L[2], f"RIVAL: {Y}AGE 91"), (L[2], L[3], f"QUESTION {Y}1/10"), (L[3], L[4], f"QUESTION {Y}2/10"), (L[4], L[6], f"MY SIZE: {Y}50%"),
     (L[6], L[7], f"QUESTION {Y}3/10"), (L[7], L[8], f"MY SIZE: {Y}30%"), (L[8], L[9], f"QUESTION {Y}4/10"), (L[9], L[11], f"MY SIZE: {Y}12%"),
     (L[11], L[13], f"PICKLES {Y}8{Wt} - ME {Y}1"), (L[13], L[16], f"LAST QUESTION: {Y}10 PTS"), (L[16], L[17], f"{Y}11 - 8{Wt}  $10,000!"),
     (L[17], L[18], f"MY SIZE: {Y}100%"), (L[18], L[19], f"{Y}REAL:{Wt} OCTOPUS = 3 HEARTS"), (L[19], TOTAL - 3.7, f"PICKLES: {Y}8 RIGHT{Wt}...")]
for t0, t1, txt in C: T(t0, t1, txt)
ass += f"Dialogue: 1,{ts(TOTAL - 3.7)},{ts(TOTAL)},T,,0,0,0,,{{\\pos(540,215)\\fad(120,0)}}SHRINK OR GROW?\n"
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
    for k, (cx, tag, line1, line2) in enumerate(((290, "A", "SHRINK", ""), (790, "B", "GROW", ""))):
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
