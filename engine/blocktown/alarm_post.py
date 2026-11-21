"""Sound, captions, overlays and assembly for the 2026-11-21 long-form "In This Town, Nobody Owns an Alarm Clock" (1920x1080).
python3.13 alarm_post.py   -> out/<slug>.mp4
Music: Kevin MacLeod (incompetech.com, CC BY 4.0) via github.com/dinglegames/dingle-radio. SFX: wyzowl/sfx-kit (CC0) +
Meta-open-sound corpora/oculus-audio-pack (CC BY 4.0, credited) + crowd_sfx.py / alarm_syn.py synth layers.
House style: 1-word Fredoka Bold yellow captions with a thick black outline at ~70 % height, day/score counter at the top,
Oddwick candle (brand/oddwick_avatar.png) sign-on + A/B candles that blow out on the last frame."""
import os, sys, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, f"{REPO}/engine/oddwick")
import mix as MX

SLUG = "2026-11-21-nobody-owns-an-alarm-clock"; W = f"/home/claude/work/{SLUG}"; FPS = 12
DL = "/home/claude/dl"; KX = f"{DL}/sfx/sounds"; SYN = "/home/claude/work/syn"; FONT = "/root/.fonts/Fredoka-Bold.ttf"
vo = json.load(open(f"{W}/vo.json")); TOTAL = round(vo["total"] + 0.6, 2)
def LS(prefix):
    for l in vo["lines"]:
        if l["text"].startswith(prefix): return l["start"]
    raise KeyError(prefix)
def LE(prefix):
    for l in vo["lines"]:
        if l["text"].startswith(prefix): return l["start"] + l["dur"]
    raise KeyError(prefix)
def WT(word, prefix, nth=1):
    """start time of the nth occurrence of a word inside the line starting with prefix"""
    li = [l["i"] for l in vo["lines"] if l["text"].startswith(prefix)][0]; k = 0
    for w in vo["words"]:
        if w["line"] == li and w["w"].strip(".,!?:;'\"").lower() == word.lower():
            k += 1
            if k == nth: return w["s"]
    raise KeyError((word, prefix))
timing = json.load(open(f"{W}/shots_timing.json"))
def SH(fn_name, k=1):
    hits = [(t0, t1) for sid, t0, t1, fn in timing if fn == fn_name]; return hits[k - 1]
def meta(name):
    for r, _, fs in os.walk(f"{DL}/meta"):
        for f in sorted(fs):
            if f.startswith(name) and f.endswith(".ogg"): return os.path.join(r, f)
    raise FileNotFoundError(name)
sfx = []
def S(f, t, g=0, *rest):
    p = f if f.startswith("/") else (f"{KX}/{f}" if "/" in f else (f"{SYN}/{f}" if os.path.exists(f"{SYN}/{f}") else meta(f)))
    sfx.append((p, max(0.0, t), g, *rest))
TINK = "foley/foley-glass-touch.wav"; SHOOT = "pops/pop-small-out.wav"
def shot_pea(t, g=-4, tink=True, dt=0.35):
    S(SHOOT, t, g); S("whooshes/whoosh-fast-soft.wav", t + 0.03, -12)
    if tink: S(TINK, t + dt, g + 2)

# ---------------------------------------------------------------- SFX (one per on-screen action)
# hook
S("appear-and-vanish/appear-materialise.wav", 0.05, -8); S("whooshes/whoosh-slow-soft.wav", 0.2, -6); S("AMBForst_ForestBirds_OS_01", 0.0, -16, 0, 4.5)
t = SH("h02")[0]; shot_pea(t + 0.1); S("pops/pop-small-in.wav", t + 0.75, -6)
S("whooshes/whoosh-medium-soft.wav", SH("h04")[0], -8); S("money/money-register.wav", WT("five", "Three hundred people.", 2) + 0.1, -4); S("money/money-coins-pour.wav", WT("thousand", "Three hundred people.") + 0.2, -8)
S("snore_big.wav", SH("h06")[0], -2); S("pops/pop-small-bubble.wav", SH("h07")[0] + 0.3, -6); S("gulp.wav", SH("h07")[0] + 0.6, -6)
S("foley/foley-fabric-touch.wav", SH("h08")[0] + 0.2, -6); S("MUSCStngr_BanjoHumorous_OS_01", SH("h08")[0] + 0.3, -8)
S("DOORWood_FrontDoorOpen_OS_01", SH("h09")[0] + 0.2, -6); S("booms-and-bass/boom-hit-soft.wav", LE("And I'd finally") - 0.2, -4)
# the job
S("crowd_cheer.wav", SH("j01")[0] + 0.1, -10); S("celebration/celebration-popper.wav", SH("j01")[0] + 0.4, -8)
S("snore.wav", SH("j03")[0] + 0.3, -4); S("snore.wav", SH("j04")[0] + 0.2, -6)
for k in range(4): S(f"FEETHmn_ShoeConcreteWalk_OS_0{k + 1}", SH("j04")[0] + 0.3 + k * 0.45, -12)
S("whooshes/whoosh-medium-medium.wav", SH("j05")[0] - 0.05, -8); S("crowd_murmur.wav", SH("j05")[0], -14)
S("booms-and-bass/boom-hit-medium.wav", SH("j07")[0] + 0.05, -4); S("crowd_gasp.wav", SH("j07")[0] + 0.2, -6)
S("money/money-register.wav", SH("j08")[0] + 0.05, -4); S("crowd_gasp.wav", SH("j08")[0] + 0.25, -8)
S("appear-and-vanish/appear-burst.wav", SH("j09")[0] + 0.1, -6); S("MUSCStngr_VictoryMallet_OS_01", SH("j09")[0] + 0.3, -6)
S("swishes-and-zips/swish-medium.wav", SH("j10")[0] + 0.45, -6); S("crowd_gasp.wav", SH("j10")[0] + 0.6, -12)
S("foley/foley-plastic-touch.wav", SH("j12")[0] + 0.3, -4); S("foley/foley-paper-touch.wav", SH("j12")[0] + 0.8, -6)
S("VOXLaff_Male01Laugh_OS_01", SH("j13")[0] + 0.1, -6); S("WOODImpt_LargeWoodDrop_OS_01" if False else "impacts/impact-medium-firm.wav", SH("j13")[0] + (SH("j13")[1] - SH("j13")[0]) / 2, -2)
S("crowd_laugh.wav", SH("j15")[0], -4); S("crowd_laugh.wav", SH("j15")[0] + 1.4, -10)
S("writing-and-drawing/" + sorted(os.listdir(f"{KX}/writing-and-drawing"))[0], SH("j16")[0] + 0.5, -6)
S("snore.wav", SH("j17")[0] + 0.1, -8); S("PAPRHndl_BookPageTurns_OS_01", SH("j18")[0] + 0.2, -4)
S("whooshes/whoosh-slow-medium.wav", LS("This was a real job") - 0.1, -8); S("PAPRHndl_BookPageTurns_OS_01", LS("This was a real job") + 0.1, -10)
S("money/money-coin-drop.wav", WT("sixpence", "Each customer paid"), -6); S("money/money-register.wav", WT("dollars", "Each customer paid") - 0.3, -4)
# day 1
S("booms-and-bass/boom-drop-soft.wav", LS("Day one."), -6); S("AMBForst_ForestBirds_OS_03", LS("Day one."), -18, 0, 6)
S("FEETHmn_ShoeWoodLand_OS_01", SH("d101")[0] + 0.4, -6); shot_pea(WT("Pea", "Day one.") - 0.1); S(TINK, WT("Tink", "Day one."), -2)
S("whooshes/whoosh-fast-medium.wav", SH("d104")[0] + 0.9, -4); S("VOXEfrt_Male01Effort_OS_01", SH("d104")[0] + 0.8, -8); S("impacts/impact-light-soft.wav", SH("d105")[0] + 0.1, -4)
S("pops/pop-medium-in.wav", SH("d105")[0] + 0.9, -8)
for k in range(9): S(TINK, SH("d107")[0] + 0.2 + k * (SH("d107")[1] - SH("d107")[0]) / 10, -6)
S("MUSCStngr_BanjoHumorous_OS_02", SH("d108")[0] + 0.4, -8)
S("pops/pop-small-in.wav", SH("d109")[0] + 0.4, -6); S("impacts/impact-medium-soft.wav", SH("d110")[0] + (SH("d110")[1] - SH("d110")[0]) / 2, -2); S("VOXEfrt_Male02Effort_OS_01", SH("d110")[0] + (SH("d110")[1] - SH("d110")[0]) / 2 + 0.05, -10)
for k in range(6): S(f"FEETHmn_ShoeWoodRun_OS_0{k % 5 + 1}", SH("d111")[0] + 0.15 + k * 0.3, -10)
for k in range(4): shot_pea(SH("d112")[0] + k * (SH("d112")[1] - SH("d112")[0]) / 4, -8, False)
S("snore.wav", SH("d113")[0], -6)
for k in range(8): S(TINK, SH("d114")[0] + 0.15 + k * 0.22, -6 - k % 3)
S("PAPRHndl_PaperCrumple_OS_01", SH("d114")[0] + 0.4, -14); S("snore.wav", SH("d116", 1)[0], -6)
S("booms-and-bass/boom-hit-medium.wav", SH("d117")[0] + 0.05, -4); S("MUSCStngr_LossMallet_OS_01", SH("d118")[0] + 0.1, -4)
# day 2
S("booms-and-bass/boom-drop-soft.wav", LS("Day two."), -6); S("OBJBag_CanvasCaseDrop_OS_01", SH("d201")[0] + 0.5, -4)
S("CLOTHFlp_FlagFlapping_LOOP_01", SH("d202")[0] + 0.1, -4, 0.5, 1.2); S("FEETHmn_ShoeWoodLand_OS_01", SH("d202")[0] + 1.0, -12)
for w in ("Load", "Eat"):
    for n in (1, 2):
        tt = WT(w, "A pigeon.", n); S("foley/foley-plastic-touch.wav" if w == "Load" else "gulp.wav", tt, -4 if w == "Eat" else -6)
S("shape-changes/transform-inflate.wav", SH("d204", 1)[0] + 0.3, -6); S("shape-changes/transform-inflate.wav", SH("d204", 2)[0] + 0.2, -6)
S("OBJBag_KnapsackNylonOpen_OS_01", SH("d205")[0] + 0.2, -6); S("transform-empty" and "shape-changes/transform-empty.wav", SH("d205")[0] + 0.5, -8)
S("snore.wav", SH("d206")[0] + 0.3, -12); S("pops/pop-small-bubble.wav", SH("d206")[0] + 1.6, -10)
for k in range(6): S(f"FEETHmn_ShoeConcreteRun_OS_0{k % 5 + 1}", SH("d207")[0] + 0.1 + k * 0.25, -8)
S("DRWRWood_DrawerOpen_OS_01", SH("d208")[0] + 0.1, -6); S("shimmers/" + sorted(os.listdir(f"{KX}/shimmers"))[0], SH("d208")[0] + 0.3, -10)
t = SH("d209")[0]; shot_pea(t + 0.1, -4, False); S("impacts/impact-light-hard.wav", t + 0.42, 0); S("CERMImpt_CeramicSmallImpact_OS_01", t + 0.45, -4)
S("VOXMale_Male02Hurt_OS_01", SH("d210")[0] + 0.1, -12)
S("snore_big.wav", SH("d211")[0], 0); S("GLASImpt_GlassBottleDrop_OS_01", SH("d211")[0] + 0.6, -14); S("snore_big.wav", SH("d212")[0], 0)
S("FEETHmn_ShoeWoodLand_OS_01", SH("d213")[0] + 0.3, -8); S("VOXEfrt_Male01Effort_OS_01", SH("d213")[0] + 0.5, -14)
S("snore.wav", SH("d214")[0], -4); S("reverse-whooshes/" + sorted(os.listdir(f"{KX}/reverse-whooshes"))[0], SH("d215")[0] + 0.1, -6)
S("pops/pop-small-in.wav", SH("d215")[1] - 0.25, -2); S("gulp.wav", SH("d215")[1] - 0.15, -2)
S("VOXMale_Male01Hurt_OS_01", SH("d216")[0] + 0.25, -6); S("impacts/impact-light-firm.wav", SH("d216")[0] + 0.3, -6)
S("MUSCStngr_BanjoHumorous_OS_01", SH("d217")[0] + 0.6, -8); S("crowd_cheer.wav", SH("d218")[0] + 0.1, -4); S("MUSCStngr_VictoryMallet_OS_01", SH("d218")[0] + 0.15, -6)
# day 3
S("booms-and-bass/boom-drop-soft.wav", LS("Day three."), -6); S("money/money-coin-spin.wav", SH("d301")[0] + 0.5, -8); S("shimmers/" + sorted(os.listdir(f"{KX}/shimmers"))[-1], SH("d301")[0] + 1.2, -10)
S("ANMLDog_DogBark_OS_01", SH("d303")[0] + 1.6, -10)
S("mechanical/mechanical-ratchet-heavy.wav", SH("d304")[0] + 0.3, -6); S("CLOTHFlp_FlagFlapping_LOOP_01", SH("d304")[0] + 0.4, -8, 0, 2.0)
t = SH("d305", 1)[0]; shot_pea(t + 0.1, -4, False); S("TOONBoing_BounceCartoony_OS_01", t + 0.5, -4); S("VOXMale_Male01Hurt_OS_01", t + 0.85, -10)
for n in (1, 2):
    S(SHOOT, WT("Pea", "Pea. Ow.", n) - 0.1, -6); S("TOONBoing_BounceCartoony_OS_01", WT("Ow", "Pea. Ow.", n) - 0.15, -4)
S("CLOTHFlp_FlagFlapping_LOOP_01", SH("d306")[0] + 0.2, -6, 0.2, 1.4); t = SH("d305", 2)[0]; S("TOONBoing_BounceCartoony_OS_01", t + 0.4, -6)
S("pops/pop-small-in.wav", SH("d308")[0] + (SH("d308")[1] - SH("d308")[0]) / 2, -2); S("VOXFem_Female01Hurt_OS_01", SH("d308")[0] + (SH("d308")[1] - SH("d308")[0]) / 2 + 0.1, -10)
for k in range(3): S(f"FEETHmn_ShoeWoodWalk_OS_0{k + 1}", SH("d309")[0] + 0.3 + k * 0.5, -8)
S("pops/pop-small-out.wav", SH("d310")[0] + 0.6, -6); S("whooshes/whoosh-fast-soft.wav", SH("d310")[0] + 0.7, -8); S("METLImpt_CanDrop_OS_01", SH("d310")[1] - 0.15, -12)
for k in range(6): S(f"FEETHmn_ShoeWoodRun_OS_0{k % 5 + 1}", SH("d311")[0] + 0.1 + k * 0.28, -10)
S("shape-changes/transform-deflate.wav", SH("d312")[0] + 0.2, -8); S("mechanical/mechanical-slider-light.wav", SH("d313")[0] + 0.3, -8)
S("crowd_cheer.wav", SH("d315")[0] + 0.1, -4); S("MUSCStngr_VictoryMallet_OS_01", SH("d315")[0] + 0.2, -6); S("booms-and-bass/boom-hit-soft.wav", SH("d316", 2)[0] + 0.05, -6)
# day 4
S("booms-and-bass/boom-drop-soft.wav", LS("Day four."), -6); S("AMBForst_ForestBirds_OS_01", LS("Day four.") + 0.2, -16, 3, 4.5)
S("pops/pop-medium-in.wav", SH("d402")[0] + 0.4, -6); S("VEHCar_CarEngineSlow_LOOP_01", SH("d403")[0], -8, 0, SH("d403")[1] - SH("d403")[0] + 0.6)
S("VEHDoor_CarTrunkClose_OS_01", SH("d404")[0] + 0.3, -8); S("OBJLug_CaseOpen_OS_01", SH("d404")[0] + 0.9, -10); S("everyday-props/props-box-open.wav", SH("d405")[0] + 0.2, -4)
S("pops/pop-medium-in.wav", WT("two", "The box said") , -4); S("pops/pop-medium-in.wav", WT("pairs", "The box said"), -4)
S("AMBForst_Night_LOOP_01" if False else "AMBForst_Night", SH("d407")[0], -14, 0, SH("d408")[1] - SH("d407")[0])
S("booms-and-bass/bass-rumble-medium.wav", WT("fluff", "Tomorrow was") - 0.4, -6)
# parade day
S("booms-and-bass/boom-drop-medium.wav", LS("Day five."), -4)
for k in range(5): S(TINK, SH("p01")[0] + 0.3 + k * 0.4, -10 - 2 * k)
S("snore.wav", SH("p02")[0] + 0.2, -6); S("snore.wav", SH("p03")[0] + 0.1, -10); S("snore.wav", SH("p03")[0] + 1.3, -12)
S("cinematic-hits/cinematic-drum-big.wav", WT("zero", "Five fifteen."), -4); S("MUSCStngr_LossPiano_OS_01", WT("zero", "Five fifteen.") + 0.4, -6)
S("pops/pop-small-bubble.wav", SH("p05")[0] + 1.4, -12)
S("shimmers/" + sorted(os.listdir(f"{KX}/shimmers"))[0], SH("p06")[0] + 0.2, -6); S("HMNBrth_MaleBreathing_OS_01", SH("p06")[0] + 1.0, -8, 0, 1.6)
S("DOORWood_FrontDoorOpen_OS_01", SH("p07")[0] + 0.1, -14); S("appear-and-vanish/appear-burst.wav", SH("p08")[0] + 0.15, -6)
S("everyday-props/props-shop-bell.wav" if False else "foley/foley-glass-slide.wav", SH("p09")[0] + 0.3, -8)
S("OBJBag_ToolBagDrop_OS_01", SH("p11")[0] + 0.2, -8); S("METLFric_ScratchCreepy_OS_01" if False else "foley/foley-wood-slide.wav", SH("p11")[0] + 0.5, -4, 0, 2.5)
S("MACHFan_FanStart_OS_01", SH("p12")[0], -2); S("MACHFan_Fan_LOOP_01", SH("p12")[0] + 1.0, -6, 0, SH("p13")[1] - SH("p12")[0])
S("whooshes/whoosh-slow-hard.wav", SH("p12")[0] + 0.8, -4)
for k in range(5): S("DOORWood_FrontDoorOpen_OS_01", SH("p13")[0] + 0.2 + k * 0.7, -10 - k)
S("crowd_murmur.wav", SH("p13")[0] + 0.5, -14); S("move-bounce" and "bounce-spin-zoom/move-spring.wav", SH("p14")[0] + 0.3, -6)
for k in range(4): S(f"FEETHmn_ShoeConcreteWalk_OS_0{k + 1}", SH("p15")[0] + 0.2 + k * 0.5, -8)
S("FOODTware_SpoonDrop_OS_01", SH("p16")[0] + 1.0, -12); S("snore_big.wav", SH("p17")[0], -2)
S("crowd_murmur.wav", SH("p18")[0], -10); S("cinematic-hits/cinematic-drum-big.wav", WT("ninety", "Six AM.", 2) - 0.1, -6)
S("cinematic-hits/cinematic-slam-big.wav", SH("p19")[0] + 0.05, -2); S("crowd_gasp.wav", SH("p19")[0] + 0.25, -6)
# the attic
S("whooshes/whoosh-fast-hard.wav", SH("a01")[0] - 0.1, -4); S("cinematic-hits/cinematic-drum-massive.wav", SH("a01")[0] + 0.05, -2)
for k in range(6): S(f"FEETHmn_ShoeWoodRun_OS_0{k % 5 + 1}", SH("a02")[0] + 0.1 + k * 0.26, -8)
S("DOORWood_FrontDoorOpen_OS_01", WT("Door", "I ran to his house."), -6); S("FEETHmn_ShoeWoodLand_OS_01", WT("Attic", "I ran to his house."), -6)
S("booms-and-bass/boom-hit-soft.wav", SH("a03")[0] + 0.1, -4); S("swishes-and-zips/zip-in-medium.wav", SH("a05")[0] + 0.05, -6)
S("whooshes/whoosh-slow-medium.wav", SH("a06")[0] + 0.1, -4); S("appear-and-vanish/appear-dissolve.wav", SH("a06")[0] + 0.4, -6); S("cinematic-hits/cinematic-metal-big.wav", SH("a06")[0] + 0.5, -10)
S("swishes-and-zips/swish-soft.wav", SH("a07")[0] + 0.1, -10); S("crowd_gasp.wav" if False else "pops/pop-small-in.wav", SH("a08", 1)[0] + 0.1, -8)
S("MUSCStngr_BanjoHumorous_OS_02", SH("a09", 2)[0] + 0.6, -10)
S(TINK, WT("Tink", "It was Gus."), -2); S(SHOOT, WT("pea", "It was Gus.") + 0.0, -8)
# ending
S("crowd_cheer.wav", SH("e01")[0] + 0.1, -4); S("celebration/celebration-applause-big.wav", SH("e01")[0] + 0.4, -10)
S("crowd_cheer.wav", SH("e02")[0], -6); S("celebration/celebration-confetti.wav", SH("e02")[0] + 0.2, -8); S("MUSCStngr_VictoryOrchestral_OS_01", SH("e02")[0] + 0.1, -4)
S("money/money-register.wav", WT("dollars", "I got the job,") - 0.2, -4); S("appear-and-vanish/appear-burst.wav", WT("Golden", "I got the job,"), -8)
S("gulp.wav", SH("e05")[0] + 0.4, -6); S("gulp.wav", SH("e05")[0] + 1.0, -8); S("snore.wav", SH("e04")[0] + 0.2, -6)
S("foley/foley-plastic-slide.wav", SH("e06")[0] + 0.6, -6); S("shimmers/" + sorted(os.listdir(f"{KX}/shimmers"))[-1], SH("e07")[0] + 0.2, -8)
S("snore.wav", SH("e08")[0] + 0.2, -6); S("snore.wav", SH("e08")[0] + 2.2, -8); S("MUSCStngr_BanjoHumorous_OS_01", WT("through", "So now I'm the only") + 0.2, -6)
S("pops/pop-large-in.wav", LS("Should I keep the job?") + 0.4, -4); S("pops/pop-large-in.wav", LS("Should I keep the job?") + 0.6, -4)
S("appear-and-vanish/appear-poof.wav", TOTAL - 0.7, -2)

# ---------------------------------------------------------------- music: story-shaped, low-passed (no hats), well under the voice
MUS = f"{W}/music"; os.makedirs(MUS, exist_ok=True)
def lp(name):
    o = f"{MUS}/{name}.wav"
    if not os.path.exists(o):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{DL}/dr/{name}.mp3", "-af", "lowpass=f=5500,highpass=f=60", "-ac", "1", "-ar", "48000", o], check=True)
    return o
MB = float(os.environ.get("MUSIC_DB", "4"))
music = [
    (lp("club-seamus"), 0, 0.0, LS("It started on Sunday") - 0.1, MB, (0.05, 0.4)),                              # bouncy hook
    (lp("sergios-magic-dustbin"), 2, LS("It started on Sunday") + 0.1, LS("Day one.") - 0.15, MB - 1, (0.3, 0.3)),  # curious set-up
    (lp("le-grand-chase"), 0, LS("Day one.") + 0.1, LS("Benny slept until lunch") - 0.1, MB - 1, (0.1, 0.4)),       # rooftop morning run
    (lp("farting-around"), 0, LS("Day two.") - 0.1, LS("Then I got to the Mayor's house.") - 0.1, MB - 2, (0.05, 0.4)),  # comic pigeon
    (lp("goblin-tinker-soldier-spy"), 6, LS("Then I got to the Mayor's house.") + 0.1, LS("I want to say I aimed.") - 0.1, MB - 3, (0.2, 0.05)),  # sneak; stop before the shot
    (lp("hillbilly-swing"), 0, LS("He sat straight up") + 1.6, LS("Day three.") - 0.1, MB - 2, (0.05, 0.4)),      # room service win
    (lp("club-seamus"), 60, LS("Day three.") + 0.1, LS("Day four.") - 0.1, MB - 1, (0.2, 0.4)),                  # net / chimneys
    (lp("goblin-tinker-soldier-spy"), 40, LS("Day four.") + 0.1, LS("Day five.") - 0.15, MB - 3, (0.3, 0.4)),     # Pickles' plan
    (lp("goblin-tinker-soldier-spy"), 80, LS("Day five.") + 0.05, LS("I sat on the curb.") - 0.1, MB - 2, (0.2, 0.2)),
    (lp("sergios-magic-dustbin"), 60, LS("I sat on the curb.") + 0.2, LS("Then I dragged the giant fan") - 0.1, MB - 3, (0.4, 0.3)),
    (lp("le-grand-chase"), 40, LS("Then I dragged the giant fan") + 0.05, LS("And the screen stopped.") - 0.1, MB - 1, (0.1, 0.05)),  # hard stop: silence
    (lp("sergios-magic-dustbin"), 100, LS("I ran to his house.") + 1.0, LS("It was Gus. Every morning.") - 0.2, MB - 4, (0.6, 0.4)),  # attic mystery, soft
    (lp("cloud-dancer"), 0, LS("It was Gus. Every morning.") + 0.3, LS("He walked to the parade") - 0.1, MB - 3, (1.0, 0.2)),
    (lp("hillbilly-swing"), 30, LS("He walked to the parade"), LS("And Gus gave me a present.") - 0.1, MB - 1, (0.05, 0.4)),
    (lp("cloud-dancer"), 40, LS("And Gus gave me a present.") + 0.1, TOTAL, MB - 2, (0.4, 1.0)),
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

# ---------------------------------------------------------------- picture: 12 fps shots -> 1920x1080 30 fps film
parts = []
for sid, t0, t1, fn in timing:
    o = f"{W}/shots/{sid}.mp4"; parts.append(o)
    if os.path.exists(o) and os.path.getmtime(o) > os.path.getmtime(f"{W}/shots/{sid}/done"): continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{W}/shots/{sid}/%04d.png",
                    "-vf", "scale=1920:1080:flags=lanczos,unsharp=5:5:0.6:5:5:0,fps=30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", o], check=True)
open(f"{W}/concat.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
film = f"{W}/film.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{W}/concat.txt", "-c", "copy", film], check=True)

# ---------------------------------------------------------------- captions (1 word, yellow, thick black outline, ~70 % height) + top counter
def ts(x): return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"
ass = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\n\n[V4+ Styles]\n"
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
       "Style: C,Fredoka,118,&H0042F5F5,&H0042F5F5,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,11,5,5,30,30,0,1\n"
       "Style: T,Fredoka,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,7,3,8,40,40,0,1\n"
       "Style: H,Fredoka,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,9,4,8,40,40,0,1\n\n"
       "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
words = vo["words"]
NUMW = {"three": "3", "five": "5", "forty": "40", "ninety": "90", "nine": "9", "ten": "10", "twenty": "20", "seventy": "70", "eleven": "11", "zero": "0", "one": "1", "two": "2", "six": "6", "sixpence": "SIXPENCE"}
for i, wd in enumerate(words):
    s0, s1 = wd["s"], wd["e"]; e = words[i + 1]["s"] if i + 1 < len(words) and words[i + 1]["s"] - s1 < 0.4 else s1 + 0.15
    clean = wd["w"].strip(".,!?:;\"'…")
    if not clean: continue
    ass += f"Dialogue: 0,{ts(s0)},{ts(max(e, s0 + 0.1))},C,,0,0,0,,{{\\pos(960,790)\\fscx80\\fscy80\\t(0,80,\\fscx100\\fscy100)}}{clean.upper()}\n"
Y = "{\\c&H0042F5F5&}"; Wt = "{\\c&HFFFFFF&}"
def T(t0, t1, txt, style="T", y=70):
    global ass; ass += f"Dialogue: 1,{ts(t0)},{ts(t1)},{style},,0,0,0,,{{\\pos(960,{y})\\fad(80,80)}}{txt}\n"
T(0.0, LS("It started on Sunday") - 0.1, f"{Y}300{Wt} PEOPLE  ·  {Y}5{Wt} MORNINGS  ·  {Y}$5,000", "H", 80)
C = [(LS("It started on Sunday"), LS("Day one."), f"SUNDAY  ·  THE JOB"),
     (LS("Day one."), WT("Benny", "Two hundred and ninety eight"), f"DAY 1  ·  5 AM"),
     (WT("Benny", "Two hundred and ninety eight"), LS("Day two."), f"DAY 1  ·  {Y}299{Wt}/300  ·  1 STRIKE"),
     (LS("Day two."), WT("three", "He sat straight up") - 0.1, f"DAY 2  ·  5 AM"),
     (WT("three", "He sat straight up") - 0.1, LS("Day three."), f"DAY 2  ·  {Y}300{Wt}/300"),
     (LS("Day three."), LS("But the screen said"), f"DAY 3  ·  THE NET"),
     (LS("But the screen said"), LS("Day four."), f"DAY 3  ·  {Y}300{Wt}/300"),
     (LS("Day four."), LS("Day five."), f"DAY 4  ·  {Y}300{Wt}/300"),
     (LS("Day five."), WT("zero", "Five fifteen."), f"DAY 5  ·  PARADE AT 6 AM"),
     (WT("zero", "Five fifteen."), LS("Six AM."), f"DAY 5  ·  {Y}0{Wt}/300"),
     (LS("Six AM."), LS("And the screen stopped."), f"6 AM  ·  COUNTING..."),
     (LS("And the screen stopped."), LS("He walked to the parade"), f"{Y}299{Wt}/300  ·  WHO'S MISSING?"),
     (LS("He walked to the parade"), LS("Should I keep the job?"), f"{Y}300{Wt}/300")]
for t0, t1, txt in C: T(t0, t1, txt)
ass += f"Dialogue: 1,{ts(LS('Should I keep the job?'))},{ts(TOTAL)},H,,0,0,0,,{{\\pos(960,90)\\fad(120,0)}}SHOULD I KEEP THE JOB?\n"
open(f"{W}/caps.ass", "w").write(ass)

# ---------------------------------------------------------------- overlays: history card + Oddwick candle sign-on + A/B candles
OV = f"{W}/ov"; os.makedirs(OV, exist_ok=True)
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
fnt = ImageFont.truetype(FONT, 50); fbig = ImageFont.truetype(FONT, 92); fmid = ImageFont.truetype(FONT, 46); fsm = ImageFont.truetype(FONT, 34)
def label(d, xy, txt, f, fill=(255, 255, 255), anchor="mm", sw=8):
    d.text(xy, txt, font=f, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=(0, 0, 0))
# candle sign-on (top-right, first 1.3 s)
n_in = int(1.3 * 30)
for f in range(n_in):
    t = f / 30; fr = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    s = 150 * min(1, t / 0.12) * (1 if t < 1.05 else max(0.01, 1 - (t - 1.05) / 0.25))
    if s > 4:
        c = card(lit if t >= 0.2 else out, int(s)); fr.alpha_composite(c, (int(1810 - s / 2), int(150 - s / 2)))
    fr.save(f"{OV}/in_{f:03d}.png")
# history card: "THIS WAS A REAL JOB" (our own drawing: a knocker-up figure with a long pole, a pea shooter, a window)
h0, h1 = LS("This was a real job"), LS("Day one.") - 0.2
hc = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(hc)
d.rounded_rectangle((250, 150, 1670, 700), 40, fill=(244, 226, 190, 245), outline=(70, 45, 25, 255), width=8)
label(d, (960, 225), "THIS WAS A REAL JOB", fbig, (245, 245, 66))
label(d, (960, 310), "KNOCKER-UPS  ·  BRITAIN & IRELAND, 1800s - 1900s", fmid, (255, 255, 255), sw=6)
# window (left) + figure with pole (middle) + figure with pea shooter (right)
d.rectangle((330, 380, 520, 600), fill=(60, 80, 140), outline=(70, 45, 25), width=8); d.line((425, 380, 425, 600), fill=(70, 45, 25), width=6); d.line((330, 490, 520, 490), fill=(70, 45, 25), width=6)
for cx, pole in ((760, True), (1180, False)):
    d.rectangle((cx - 40, 470, cx + 40, 600), fill=(60, 60, 80)); d.rectangle((cx - 35, 400, cx + 35, 470), fill=(240, 200, 160)); d.rectangle((cx - 45, 385, cx + 45, 405), fill=(30, 30, 40))
    d.rectangle((cx - 30, 360, cx + 30, 390), fill=(30, 30, 40))
    if pole: d.line((cx - 30, 500, 470, 395), fill=(110, 75, 40), width=10)
    else:
        d.line((cx - 40, 440, cx - 150, 430), fill=(60, 140, 70), width=12)
        for k in range(4): d.ellipse((cx - 190 - k * 55, 420 - k * 6, cx - 172 - k * 55, 438 - k * 6), fill=(110, 200, 60))
label(d, (760, 640), "LONG POLES", fsm, (255, 255, 255), sw=5); label(d, (1180, 640), "DRIED PEAS", fsm, (255, 255, 255), sw=5)
label(d, (1460, 470), "MARY SMITH", fmid, (255, 255, 255), sw=6); label(d, (1460, 530), "LONDON", fsm, (255, 255, 255), sw=5); label(d, (1460, 580), "6d a week", fmid, (245, 245, 66), sw=6)
hc.save(f"{OV}/history.png")
# A/B candles at the end
t_ab = LS("Should I keep the job?"); n_out = int((TOTAL - t_ab) * 30) + 1
for f in range(n_out):
    t = f / 30; fr = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(fr)
    for k, (cx, tag, l1, l2) in enumerate(((620, "A", "KEEP SHOOTING", "PEAS"), (1300, "B", "GIVE BACK THE", "ALARM CLOCKS"))):
        a = min(1, max(0, (t - 0.25 * k) / 0.18))
        if a <= 0: continue
        s = int(300 * (0.6 + 0.4 * a)); src = out if t > (TOTAL - t_ab) - 0.55 + 0.08 * k else lit
        fr.alpha_composite(card(src, s), (cx - s // 2, 470 - s // 2))
        label(d, (cx, 470 - s // 2 - 55), tag, fbig, (245, 245, 66)); label(d, (cx, 470 + s // 2 + 42), l1, fnt); label(d, (cx, 470 + s // 2 + 98), l2, fnt)
    fr.save(f"{OV}/out_{f:03d}.png")

# ---------------------------------------------------------------- final mux
os.makedirs(f"{REPO}/out", exist_ok=True); outp = f"{REPO}/out/{SLUG}.mp4"
fc = (f"[1:v]setpts=PTS-STARTPTS[a];[2:v]setpts=PTS-STARTPTS+{t_ab:.3f}/TB[b];"
      f"[0:v][a]overlay=0:0:eof_action=pass[v1];[v1][3:v]overlay=0:0:enable='between(t,{h0:.2f},{h1:.2f})'[v1b];"
      f"[v1b][b]overlay=0:0:eof_action=repeat:enable='gte(t,{t_ab:.3f})'[v2];[v2]ass={W}/caps.ass[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", film, "-framerate", "30", "-i", f"{OV}/in_%03d.png", "-framerate", "30", "-i", f"{OV}/out_%03d.png",
                "-loop", "1", "-i", f"{OV}/history.png", "-i", mixf,
                "-filter_complex", fc, "-map", "[v]", "-map", "4:a", "-t", f"{TOTAL:.2f}", "-r", "30",
                "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p", "-profile:v", "high",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", outp], check=True)
print(outp, round(os.path.getsize(outp) / 1e6, 1), "MB")
