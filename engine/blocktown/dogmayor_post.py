"""Sound, captions, overlays and assembly for the 2026-11-23 daily Short "I Ran for Mayor Against a Dog".
python3.13 donut_post.py            -> out/<slug>.mp4      (YouTube + Instagram)
TT=1 python3.13 donut_post.py       -> out/<slug>_tt.mp4   (TikTok: different first 2 s hook banner + zoom, own encode)
Music: Kevin MacLeod (incompetech.com, CC BY 4.0) via github.com/dinglegames/dingle-radio. SFX: wyzowl/sfx-kit (CC0) +
Meta-open-sound corpora/oculus-audio-pack (CC BY 4.0, credited) + crowd_sfx.py layers (Kokoro voices + CC0 claps).
House style (PLAYBOOK "OWNER REFERENCE STYLE 2026-11-20"): 1-word Fredoka Bold yellow captions with a thick black outline at
70 % height, hours/players counter at the top, Oddwick candle (brand/oddwick_avatar.png) sign-on + A/B candles blowing out."""
import os, sys, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, f"{REPO}/engine/oddwick")
import mix as MX

SLUG = "2026-11-23-i-ran-for-mayor-against-a-dog"; W = f"/home/claude/work/{SLUG}"; TT = bool(os.environ.get("TT"))
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
# --- hook: candle pop, Mayor Biscuit, crowd, confetti, bark
S("pops/pop-medium-in.wav", 0.12, -6); S("crowd_cheer.wav", 0.05, -6); S("celebration/celebration-popper.wav", 0.2, -4); S("celebration/celebration-confetti.wav", 0.3, -6)
S("ANMLDog_DogBark_OS_01", st("s02") + 0.15, -2); S("whooshes/whoosh-medium-soft.wav", st("s02") - 0.05, -6)
S("whooshes/whoosh-fast-medium.wav", st("s03") - 0.05, -6); S("foley/foley-paper-slide.wav", st("s03") + 0.1, -4)
S("booms-and-bass/boom-hit-soft.wav", st("s04"), -4); S("MUSCStngr_MarchingSnare_OS_01", st("s04") + 0.05, -8)
# --- Biscuit: 5 wins, can't read
S("ANMLDog_DogAttention_OS_01", st("s05") + 0.1, -6); S("swishes-and-zips/swish-medium.wav", st("s05") - 0.05, -8)
S("cinematic-hits/cinematic-drum-big.wav", st("s06"), -6); S("crowd_cheer.wav", st("s06") + 0.1, -12)
S("foley/foley-paper-touch.wav", st("s07") + 0.05, -2); S("foley/foley-paper-slide.wav", st("s07") + 0.5, -6); S("MUSCStngr_BanjoHumorous_OS_01", st("s07") + 0.5, -8)
# --- the rule: $1 = 1 vote
S("money/money-register.wav", st("s08") + 0.05, -2); S("booms-and-bass/boom-hit-soft.wav", st("s08"), -6)
S("money/money-notes.wav", st("s09") + 0.1, -4); S("money/money-notes.wav", st("s09") + 0.6, -6); S("crowd_cheer.wav", st("s09"), -10)
# --- day 1: posters; Biscuit pees on them
S("whooshes/whoosh-fast-medium.wav", st("s10") - 0.1, -6)
for k in range(8): S(f"FEETHmn_ShoeConcreteRun_OS_0{k % 5 + 1}", st("s10") + 0.05 + k * 0.2, -10)
for k in range(4): S("everyday-props/props-tape.wav", st("s10") + 0.25 + k * 0.42, -6)
S("WATRPlmb_FaucetWaterRun_LOOP_01", st("s11", frames=NF("s11") // 4), -12, 0, 1.0); S("crowd_gasp.wav", st("s12"), -8)
S("MUSCStngr_LossMallet_OS_01", st("s12") + 0.2, -8)
# --- day 2: free pizza rally, Biscuit rolls over
S("pops/pop-large-in.wav", st("s13") + 0.1, -6); S("crowd_cheer.wav", st("s14") - 0.05, -4); S("celebration/celebration-applause-small.wav", st("s14") + 0.2, -10)
S("whooshes/whoosh-slow-medium.wav", st("s15") + 0.15, -6); S("ANMLDog_DogBark_OS_02", st("s15") + 0.6, -6)
S("crowd_cheer.wav", st("s16") - 0.05, 0); S("celebration/celebration-applause-big.wav", st("s16") + 0.1, -4); S("celebration/celebration-popper.wav", st("s16") + 0.15, -4)
# --- day 3: the baby
S("pops/pop-small-bubble.wav", st("s17", frames=NF("s17") // 2), -4); S("crowd_aww.wav", st("s17") + 0.4, -10)
S("whooshes/whoosh-fast-soft.wav", st("s18") + 0.05, -6); S("pops/pop-medium-bubble.wav", st("s18", frames=NF("s18") // 3), -4)
S("VOXLaff_Female01Laugh_OS_01", st("s18", frames=NF("s18") // 2), -8)
S("money/money-notes.wav", st("s19") + 0.1, -4); S("crowd_cheer.wav", st("s19"), -8)
# --- day 4: Benny's cookies, $300
S("everyday-props/props-shop-bell.wav", st("s20") - 0.05, -4); S("money/money-coin-drop.wav", st("s20") + 0.7, -6)
S("money/money-coins-pour.wav", st("s21") + 0.05, -4); S("money/money-register.wav", st("s21") + 0.4, -2)
S("MUSCStngr_VictoryMallet_OS_01", st("s22"), -6); S("celebration/celebration-confetti.wav", st("s22") + 0.1, -6)
# --- day 5: the TV ad
S("mechanical/mechanical-switch-heavy.wav", st("s23"), -6); S("whooshes/whoosh-slow-soft.wav", st("s23") + 0.1, -8)
S("crowd_aww.wav", st("s25") - 0.05, -2); S("pops/pop-small-bubble.wav", st("s25") + 0.3, -8); S("pops/pop-small-bubble.wav", st("s25") + 0.6, -8)
# --- day 6: the debate
S("cinematic-hits/cinematic-drum-big.wav", st("s26") - 0.03, -4); S("crowd_murmur.wav", st("s26") + 0.2, -12)
S("whooshes/whoosh-fast-soft.wav", st("s27"), -10); S("crowd_murmur.wav", st("s28"), -14)
S("pops/pop-medium-in.wav", st("s29", frames=NF("s29") // 3), -4); S("ANMLDog_DogAttention_OS_01", st("s30") + 0.2, -8); S("impacts/impact-light-soft.wav", st("s30", frames=NF("s30") // 3), -4)
S("crowd_cheer.wav", st("s31") - 0.05, 0); S("celebration/celebration-applause-big.wav", st("s31") + 0.05, -2); S("celebration/celebration-confetti.wav", st("s31") + 0.2, -6)
# --- election night
S("whooshes/whoosh-slow-hard.wav", st("s32") - 0.15, -4); S("booms-and-bass/boom-hit-medium.wav", st("s32") + 0.05, -6); S("crowd_murmur.wav", st("s32") + 0.2, -10)
S("money/money-register.wav", st("s33") + 0.05, -4); S("money/money-register.wav", st("s33", frames=NF("s33") // 2), -4)
S("money/money-register.wav", st("s34") + 0.05, -2); S("booms-and-bass/bass-rumble-medium.wav", st("s35"), -8)
S("cinematic-hits/cinematic-slam-big.wav", st("s36"), -2); S("crowd_gasp.wav", st("s36") + 0.1, -2)
# --- Mrs. Pickles' one dollar
for k in range(6): S(f"FEETHmn_ShoeConcreteRun_OS_0{k % 5 + 1}", st("s37") + 0.1 + k * 0.34, -14)
S("everyday-props/props-zip.wav", st("s38") + 0.1, -2); S("foley/foley-paper-slide.wav", st("s38", frames=NF("s38") // 3), -4)
S("money/money-notes.wav", st("s39") + 0.2, -4); S("ANMLDog_DogBark_OS_01", st("s39") + 0.8, -6)
# --- BISCUIT WINS. Again.
S("cinematic-hits/cinematic-drum-massive.wav", st("s40") - 0.02, -2); S("crowd_cheer.wav", st("s40"), -2); S("celebration/celebration-fireworks.wav", st("s40") + 0.15, -4)
S("MUSCStngr_LossPiano_OS_01", st("s41") + 0.05, -6)
# --- $625: the school roof
S("money/money-register.wav", st("s42") + 0.05, -2); S("appear-and-vanish/appear-materialise.wav", st("s42") + 0.1, -6)
S("whooshes/whoosh-slow-medium.wav", st("s43") - 0.05, -6); S("crowd_cheer.wav", st("s43") + 0.15, -6); S("MUSCStngr_LevelUpOrchestral_OS_01", st("s43") + 0.3, -8)
S("everyday-props/props-scissors.wav", st("s45", frames=NF("s45") // 3), 0); S("celebration/celebration-popper.wav", st("s45", frames=NF("s45") // 3) + 0.1, -4)
S("celebration/celebration-applause-small.wav", st("s45", frames=NF("s45") // 3) + 0.2, -8)
# --- this part is real
S("booms-and-bass/boom-hit-soft.wav", st("s46"), -4); S("whooshes/whoosh-medium-medium.wav", st("s46") - 0.05, -8)
S("ANMLDog_DogBark_OS_01", st("s47") + 0.2, -8); S("ANMLDog_DogBark_OS_02", st("s47") + 0.7, -10)
S("money/money-coin-drop.wav", st("s48", frames=NF("s48") // 2), -4); S("appear-and-vanish/appear-burst.wav", st("s48", frames=NF("s48") // 2) + 0.05, -10)
# --- the callback: peed on my poster. Again.
for k in range(6): S(f"FEETHmn_ShoeConcreteRun_OS_0{k % 5 + 1}", st("s49") + 0.05 + k * 0.18, -16)
S("WATRPlmb_FaucetWaterRun_LOOP_01", st("s50", frames=NF("s50") // 5), -12, 0, 1.0); S("MUSCStngr_BanjoHumorous_OS_02", L[16] + 2.4, -6)
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
    (lp("club-seamus"), 0, 0.0, L[5] - 0.05, MB + 0, (0.02, 0.3)),                         # bouncy: the Mayor is a dog
    (lp("hillbilly-swing"), 0, L[5] - 0.05, L[8] - 0.1, MB - 1, (0.1, 0.3)),                 # the campaign days
    (lp("sergios-magic-dustbin"), 0, L[8] - 0.1, L[10] - 0.15, MB - 1, (0.1, 0.3)),         # the debate
    (lp("goblin-tinker-soldier-spy"), 0, L[10] - 0.1, L[13] - 0.25, MB - 2, (0.1, 0.15)),   # election night tension; cut before the result
    (lp("le-grand-chase"), 2, L[13] + 0.05, L[14] - 0.05, MB - 1, (0.05, 0.2)),             # BISCUIT WINS
    (lp("cloud-dancer"), 0, L[14] + 0.05, L[16] - 0.35, MB - 1, (0.3, 0.3)),               # bright: the school roof, the real fact
    (lp("farting-around"), 0, L[16] + 0.3, TOTAL, MB - 2, (0.2, 0.8)),                      # the callback + A/B
]
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
    T(0.0, L[2], f"I LOST AN ELECTION\\N{Y}TO A DOG", "H", 190)
else:
    T(0.0, L[2], f"THE MAYOR\\NIS {Y}A DOG", "H", 190)
C = [(L[2], L[3], f"{Y}$1{Wt} = 1 VOTE"), (L[3], L[4], f"DAY {Y}1{Wt} OF 7"), (L[4], L[5], f"DAY {Y}2{Wt} OF 7"), (L[5], L[6], f"DAY {Y}3{Wt} OF 7"),
     (L[6], L[7], f"DAY {Y}4{Wt} OF 7"), (L[7], L[8], f"DAY {Y}5{Wt} OF 7"), (L[8], L[10], f"DAY {Y}6{Wt} OF 7"), (L[10], L[11], f"ELECTION NIGHT"),
     (L[11], L[13], f"ME {Y}312{Wt}  ·  BISCUIT {Y}312"), (L[13], L[14], f"ME 312  ·  BISCUIT {Y}313"), (L[14], L[15], f"{Y}$625{Wt} RAISED"),
     (L[15], L[16], f"{Y}REAL:{Wt} DOG MAYORS SINCE 1998"), (L[16], TOTAL - 3.7, f"AGAIN.")]
for t0, t1, txt in C: T(t0, t1, txt)
ass += f"Dialogue: 1,{ts(TOTAL - 3.7)},{ts(TOTAL)},T,,0,0,0,,{{\\pos(540,215)\\fad(120,0)}}WHO GETS YOUR VOTE?\n"
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
    for k, (cx, tag, line1, line2) in enumerate(((290, "A", "THE", "KID"), (790, "B", "THE", "DOG"))):
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
