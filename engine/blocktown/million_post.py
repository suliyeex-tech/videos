"""Sound, captions, overlays and assembly for the 2026-11-22 daily Short "I Had 24 Hours to Spend $1,000,000".
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

SLUG = "2026-11-22-spend-a-million-in-24-hours"; W = f"/home/claude/work/{SLUG}"; TT = bool(os.environ.get("TT"))
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
# --- hook: candle pop, cheque, crowd, confetti
S("pops/pop-medium-in.wav", 0.12, -6); S("crowd_cheer.wav", 0.05, -6); S("celebration/celebration-popper.wav", 0.2, -4); S("celebration/celebration-confetti.wav", 0.3, -6)
S("money/money-register.wav", L[0] + 3.0, -2); S("money/money-coins-pour.wav", L[0] + 3.2, -8)
S("whooshes/whoosh-medium-soft.wav", st("s02") - 0.05, -6); S("crowd_gasp.wav", st("s02") + 0.1, -8)
# --- the rule
S("whooshes/whoosh-slow-medium.wav", L[1] - 0.05, -6); S("pops/pop-small-in.wav", st("s03", frames=NF("s03") // 3), -4)
S("booms-and-bass/boom-hit-soft.wav", st("s04"), -2); S("mechanical/mechanical-switch-heavy.wav", st("s04") + 0.05, -8)
S("cinematic-hits/cinematic-drum-big.wav", st("s05"), -4); S("crowd_gasp.wav", st("s05") + 0.15, -8)
S("celebration/celebration-popper.wav", L[2] + 0.1, -4); S("MUSCStngr_BanjoHumorous_OS_01", L[2] + 0.5, -8)
# --- hour 1: candy shop
S("everyday-props/props-shop-bell.wav", L[3] - 0.05, -2); S("whooshes/whoosh-fast-medium.wav", L[3] - 0.1, -6)
for k in range(5): S(f"FEETHmn_ShoeWoodRun_OS_0{k + 1}", L[3] + 0.1 + k * 0.22, -10)
S("crowd_gasp.wav", st("s08") + 0.1, -10); S("pops/pop-medium-bubble.wav", st("s08") + 0.3, -6); S("pops/pop-small-bubble.wav", st("s08") + 0.7, -6)
S("money/money-register.wav", st("s09") + 0.05, -2); S("booms-and-bass/boom-hit-soft.wav", st("s09"), -6)
S("foley/foley-plastic-slide.wav", L[4] + 0.05, -2); S("shape-changes/transform-stretch.wav", L[4] + 0.6, -8)
# --- hour 3: the ice cream truck
S("VEHCar_CarEngineSlow_LOOP_01", L[5] - 0.1, -6, 0.0, 1.8); S("whooshes/whoosh-slow-medium.wav", L[5] + 0.6, -8)
for k in range(6): S(f"FEETHmn_ShoeConcreteRun_OS_0{k % 5 + 1}", L[5] + 0.05 + k * 0.24, -10)
S("VEHDoor_CarDoorClose_OS_01", st("s12") + 0.0, -6); S("crowd_gasp.wav", st("s12") + 0.2, -12)
S("money/money-notes.wav", st("s12") + 0.6, -4); S("pops/pop-small-in.wav", st("s13", frames=NF("s13") // 3), -4); S("MUSCStngr_LevelUpMallet_OS_01", st("s13") + 0.3, -8)
# --- hour 6: Hotel Benny, the roof pool
S("whooshes/whoosh-slow-hard.wav", L[6] - 0.1, -6); S("booms-and-bass/boom-hit-medium.wav", L[6] + 0.05, -6); S("crowd_gasp.wav", L[6] + 0.4, -10)
S("swishes-and-zips/swish-medium.wav", st("s15") - 0.05, -8); S("pops/pop-medium-in.wav", st("s15", frames=NF("s15") // 2), -6)
S("whooshes/whoosh-fast-soft.wav", st("s16") + 0.1, -6); S("everyday-props/props-splash.wav", st("s16", frames=int(NF("s16") * 0.45)), 0)
S("WATRLap_WaterLapping_LOOP_01", st("s16", frames=int(NF("s16") * 0.45)) + 0.2, -10, 0, 0.9)
# --- hour 9: the game show
S("cinematic-hits/cinematic-drum-big.wav", L[7] - 0.05, -4); S("crowd_cheer.wav", L[7] + 0.1, -6); S("celebration/celebration-applause-big.wav", L[7] + 0.3, -10)
S("MUSCStngr_VictoryMallet_OS_01", st("s18"), -6); S("celebration/celebration-confetti.wav", st("s18") + 0.1, -4); S("celebration/celebration-popper.wav", st("s18") + 0.2, -6)
# --- the lucky rock
S("swishes-and-zips/swish-medium.wav", L[8] - 0.05, -8); S("impacts/impact-medium-soft.wav", L[8] + 0.3, -4)
S("money/money-register.wav", L[8] + 1.4, -4); S("shimmers" if False else "appear-and-vanish/appear-materialise.wav", st("s20") + 0.15, -4)
# --- night, hour 23, $12.40 left, everything closed
S("whooshes/whoosh-slow-hard.wav", L[9] - 0.15, -4); S("booms-and-bass/boom-hit-medium.wav", L[9] + 0.05, -4)
S("mechanical/mechanical-switch-heavy.wav", st("s22"), -4); S("booms-and-bass/bass-rumble-medium.wav", st("s22") + 0.05, -6)
for k in range(8): S(f"FEETHmn_ShoeConcreteRun_OS_0{k % 5 + 1}", st("s23") + 0.05 + k * 0.2, -8)
S("DOORMetl_GarageDoorClose_OS_01", st("s23") + 0.6, -8)
# --- the lemonade stand, $12.50, ten cents short
S("pops/pop-medium-in.wav", L[10] + 0.1, -6); S("foley/foley-glass-touch.wav", L[10] + 0.9, -4)
S("cinematic-hits/cinematic-slam-big.wav", st("s25") + 0.05, -6); S("swishes-and-zips/swish-soft.wav", st("s26") - 0.05, -8)
S("money/money-coin-drop.wav", L[11] + 0.1, -4); S("money/money-coin-spin.wav", L[11] + 0.3, -8); S("MUSCStngr_LossMallet_OS_01", L[11] + 0.9, -6)
S("whooshes/whoosh-fast-soft.wav", st("s28") + 0.1, -10); S("whooshes/whoosh-fast-soft.wav", st("s28") + 0.4, -10)
# --- one minute: pockets, the town counts down
S("cinematic-hits/cinematic-drum-big.wav", L[12] - 0.02, -4); S("booms-and-bass/boom-hit-soft.wav", L[12] + 0.6, -6)
S("foley/foley-fabric-slide.wav", st("s30", frames=NF("s30") // 3), -2); S("foley/foley-fabric-touch.wav", st("s30", frames=NF("s30") // 3) + 0.25, -4)
S("crowd_count.wav", st("s31") - 0.1, -6)
# --- the idea, the truck, the salary
S("appear-and-vanish/appear-materialise.wav", L[13] + 0.25, -4); S("reverse-whooshes/reverse-whoosh-short-strong.wav", L[13] + 0.1, -8)
for k in range(6): S(f"FEETHmn_ShoeConcreteRun_OS_0{k % 5 + 1}", st("s33") + 0.05 + k * 0.2, -8)
S("impacts/impact-light-hard.wav", st("s34", frames=NF("s34") // 3), -2); S("money/money-notes.wav", st("s34", frames=NF("s34") // 3) + 0.05, 0)
S("money/money-register.wav", st("s35"), 0); S("cinematic-hits/cinematic-drum-massive.wav", st("s35") + 0.02, -4)
# --- crowd goes wild, trophy
S("crowd_cheer.wav", L[15], -2); S("celebration/celebration-fireworks.wav", L[15] + 0.2, -6); S("celebration/celebration-applause-big.wav", L[15] + 0.3, -8)
S("MUSCStngr_VictoryOrchestral_OS_01", st("s37") - 0.05, -4); S("celebration/celebration-confetti.wav", st("s37") + 0.1, -6)
# --- "thanks, boss... here's your change"
S("swishes-and-zips/swish-soft.wav", L[16] - 0.05, -10); S("foley/foley-card-slide.wav", st("s39") + 0.3, -6)
# --- ONE CENT: silence, then the coin
S("money/money-coin-drop.wav", L[17] + 0.05, 0)
S("cinematic-hits/cinematic-drum-massive.wav", L[18] - 0.02, -2); S("MUSCStngr_LossOrchestral_OS_01", L[18] + 0.05, -4); S("crowd_gasp.wav", L[18] + 0.15, -4)
# --- the Mayor takes it all back
S("VEHCar_CarStartRunStop_OS_01", L[19] - 0.1, -6, 1.0, 2.0); S("crowd_aww.wav", L[19] + 0.4, -8)
S("mechanical/mechanical-switch-heavy.wav", st("s44") + 0.1, -4); S("WATRLap_WaterLapping_LOOP_01", st("s44"), -14, 0, 1.4)
S("impacts/impact-deep-soft.wav", L[20] + 0.4, -6); S("MUSCStngr_LossPiano_OS_01", L[20] + 1.4, -6)
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
    (lp("club-seamus"), 0, 0.0, L[5] - 0.05, MB + 0, (0.02, 0.3)),                       # bouncy: a million dollars!
    (lp("hillbilly-swing"), 0, L[5] - 0.05, L[9] - 0.15, MB - 1, (0.1, 0.3)),             # spending spree
    (lp("goblin-tinker-soldier-spy"), 0, L[9] - 0.1, L[13] - 0.05, MB - 2, (0.1, 0.2)),   # night, $12.40, tension
    (lp("le-grand-chase"), 2, L[13] + 0.2, L[16] - 0.05, MB - 1, (0.1, 0.3)),            # the idea, the win
    (lp("farting-around"), 0, L[16] - 0.05, L[17] - 0.05, MB - 3, (0.05, 0.05)),          # polite Frosty; hard stop on "One cent."
    (lp("cloud-dancer"), 0, L[19] + 0.1, TOTAL, MB - 1, (0.3, 0.8)),                      # bright ending after the twist
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
    T(0.0, L[2], f"I LOST {Y}$1,000,000{Wt}\\NBY ONE CENT", "H", 190)
else:
    T(0.0, L[2], f"SPEND {Y}$1,000,000{Wt}\\NIN 24 HOURS", "H", 190)
C = [(L[2], L[3], f"24 HOURS  ·  {Y}$1,000,000"), (L[3], L[5], f"HOUR 1  ·  {Y}$999,000{Wt} LEFT"), (L[5], L[6], f"HOUR 3  ·  {Y}$940,000{Wt} LEFT"),
     (L[6], L[7], f"HOUR 6  ·  {Y}$540,000{Wt} LEFT"), (L[7], L[8] + 2.0, f"HOUR 9  ·  {Y}$100,012.40"), (L[8] + 2.0, L[9], f"HOUR 9  ·  {Y}$12.40{Wt} LEFT"),
     (L[9], L[12], f"HOUR 23  ·  {Y}$12.40{Wt} LEFT"), (L[12], st("s35"), f"{Y}0:59{Wt}  ·  $12.40 LEFT"), (st("s35"), L[17] - 0.1, f"{Y}$0.00{Wt} LEFT!"),
     (L[17] - 0.1, L[18], f"{Y}$0.01{Wt} LEFT..."), (L[18], TOTAL - 3.7, f"YOU LOSE IT ALL")]
for t0, t1, txt in C: T(t0, t1, txt)
ass += f"Dialogue: 1,{ts(TOTAL - 3.7)},{ts(TOTAL)},T,,0,0,0,,{{\\pos(540,215)\\fad(120,0)}}WHAT WOULD YOU BUY FIRST?\n"
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
    for k, (cx, tag, line1, line2) in enumerate(((290, "A", "THE CANDY", "SHOP"), (790, "B", "THE GAME", "SHOW"))):
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
