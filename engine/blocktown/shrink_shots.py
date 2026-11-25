"""Oddwick daily Short 2026-11-25: "Every Wrong Answer, I Got Smaller" (Blocktown house style, owner 2026-11-20).
Game-show countdown shape: the town game show on the square stage, 10 questions for $10,000, every wrong answer you shrink
(a shrink-ray lamp over each podium zaps you). Rival Mrs. Pickles (91, never lost, not even bingo) knits the whole show and,
unseen, gets a bit taller with every right answer. Hero shrinks to a fire hydrant, a cat (who sniffs him), a hamster (the mic
towers over him); 8-1 on the big screen; the wind blows away the Mayor's cards, he grabs the octopus card again (10 points);
the tiny hero jumps on the buzzer with his whole body: THREE! 11-8, $10,000, right answers make you grow, he grows back.
Real fact: an octopus has three hearts. Callback twist: Mrs. Pickles got 8 right -> giant, taller than the clock tower,
knitting the tower a scarf.
python3.13 shrink_shots.py [sid ...] [--still]   -> /home/claude/work/<slug>/shots/<sid>/####.png (resumable)
Set: town square stage (x=0, y=23.5..29.5, top z=1.4), big screen y=29.45, clock tower x=0 y=36 (lib.build_town)."""
import sys, os, json, math, random, time, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move

SLUG = "2026-11-25-every-wrong-answer-i-shrank"; FPS = 12
W = f"/home/claude/work/{SLUG}"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; END = vo["total"] + 1.5
WORDS = vo["words"]
def wt(line, k):
    ws = [w for w in WORDS if w["line"] == line]; return ws[min(k, len(ws) - 1)]["s"] - 0.04
PREV = "--still" in sys.argv
RES = (216, 384) if PREV else (432, 768)
sc, cam, tgt = lib.setup(res=RES, samples=4 if PREV else 8, fps=FPS)
sc.render.threads_mode = "AUTO"
town = lib.build_town()
import re as _re
for _o in list(bpy.data.objects):   # clear street houses/trees/lamps that sit on the plaza edges
    if (_re.match(r'^(hw|hsid|hrf|hwin|hwf|hdoor|hstep|pk|pkr)(-?12)(_|$)', _o.name) or _re.match(r'^(trunk|leaf)(-6|6|18)_9\.5', _o.name)
            or _o.name in ("lpole0", "larm0", "lbulb0", "lamp0_6.8", "lpole16", "larm16", "lbulb16", "lamp16_6.8")):
        bpy.data.objects.remove(_o, do_unlink=True)
FONT = None
for fp in ("/root/.fonts/Fredoka-Bold.ttf",):
    if os.path.exists(fp): FONT = bpy.data.fonts.load(fp); break
bg = sc.world.node_tree.nodes["Background"]
sun = sc.objects["moonlight"]; sc.objects["moon"].hide_render = True
STREETLAMPS = [o for o in sc.objects if o.type == "LIGHT" and o.name.startswith("lamp")]
R = math.radians

def mktext(name, body, loc, size, col, emit=0.0, rot=(90, 0, 0), extrude=0.04, parent=None):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = extrude
    if FONT: cu.font = FONT
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = tuple(R(a) for a in rot)
    if parent: o.parent = parent
    cu.materials.append(mat(name + "m", col, 0.5, emit)); return o

GLASS = bpy.data.materials.new("glass"); GLASS.use_nodes = True
_gb = GLASS.node_tree.nodes["Principled BSDF"]; _gb.inputs["Base Color"].default_value = (0.85, 0.95, 1, 1)
_gb.inputs["Roughness"].default_value = 0.03; _gb.inputs["Transmission Weight"].default_value = 1.0; _gb.inputs["IOR"].default_value = 1.1

# ---------------------------------------------------------------- the game-show stage on the square
ST = 1.4   # stage top
cube("plaza", (0, 22, 0.02), (40, 22, 0.06), mat("plaza", "#c9b79a", 0.85), 0)
cube("stage", (0, 26.5, 0.7), (18, 6, 1.4), mat("stagefloor", "#2a1f4a", 0.3, metal=0.2), 0.05)
for k in range(9): cube(f"stagestripe{k}", (-8 + k * 2, 26.5, ST + 0.005), (0.08, 6, 0.01), mat("stline", "#5a3fa0", 0.3, 1.0), 0)
cube("stage_edge", (0, 23.48, 1.3), (18.2, 0.12, 0.2), mat("neon_cyan", "#40f0ff", 0.3, 10, "#40f0ff"), 0)
cube("stage_edge2", (0, 23.48, 0.25), (18.2, 0.12, 0.15), mat("neon_pink", "#ff4fd0", 0.3, 10, "#ff4fd0"), 0)
cube("screenwall", (0, 29.8, 5.0), (19, 0.6, 9.6), mat("screenwall", "#120e22", 0.4), 0.05)
scr_cols = {"blue": mat("scr_blue", "#2a3cff", 0.3, 3.0, "#3a5cff"), "red": mat("scr_red", "#ff2a3a", 0.3, 4.0, "#ff2a3a"),
            "green": mat("scr_green", "#1fc85a", 0.3, 4.0, "#2aff6a"), "purple": mat("scr_purple", "#8a2aff", 0.3, 3.5, "#9a3aff"),
            "pink": mat("scr_pink", "#ff3fae", 0.3, 3.5, "#ff3fae"), "gold": mat("scr_gold", "#e0a020", 0.3, 3.5, "#ffb020")}
screen = cube("bigscreen", (0, 29.45, 6.0), (9.5, 0.1, 5.2), scr_cols["blue"], 0)
for sd in (-1, 1):
    cube(f"sidescr{sd}", (7.2 * sd, 29.45, 5.2), (2.6, 0.1, 6.4), mat(f"sidescr{sd}", "#ff4fd0" if sd < 0 else "#40f0ff", 0.3, 5.0), 0)
    for i in range(6): cube(f"sidebar{sd}{i}", (7.2 * sd, 29.38, 2.6 + i * 1.05), (2.2, 0.05, 0.18), mat("barw", "#ffffff", 0.3, 6.0), 0)
for i in range(22):
    a = i / 22
    x = -5.2 + 10.4 * a if i < 11 else -5.2 + 10.4 * (a - 0.5) * 2
    sphere(f"bulb{i}", (x, 29.35, 8.95 if i < 11 else 3.05), (0.16, 0.16, 0.16), mat("bulbm", "#ffe27a", 0.3, 12, "#ffcf4a"), seg=8)
mktext("showsign", "THE SHRINK SHOW", (0, 29.4, 10.4), 1.15, "#ffe14a", 4.0, extrude=0.06)
TXT = {}
for key, body, size, col in (("show", "THE\nSHRINK\nSHOW", 1.35, "#ffe14a"), ("ten", "10\nQUESTIONS", 1.45, "#ffffff"),
                             ("prize", "$10,000", 2.4, "#ffe14a"), ("rule", "WRONG =\nSHRINK", 1.8, "#ffffff"),
                             ("age", "AGE: 91\nWINS: ALL", 1.35, "#ffffff"), ("banana", "WHAT COLOR\nIS A BANANA?", 1.05, "#ffffff"),
                             ("correct", "CORRECT!", 1.8, "#ffffff"), ("octo", "HOW MANY\nHEARTS DOES AN\nOCTOPUS HAVE?", 0.85, "#ffffff"),
                             ("wrong", "WRONG!", 2.2, "#ffffff"), ("shark", "DOES A SHARK\nHAVE BONES?", 1.0, "#ffffff"),
                             ("q4", "QUESTION 4", 1.5, "#ffffff"), ("q9", "QUESTION 9", 1.5, "#ffffff"),
                             ("score", "PICKLES  8\nME  1", 1.3, "#ffffff"), ("last", "LAST QUESTION\n10 POINTS", 1.0, "#ffe14a"),
                             ("final", "11 - 8", 2.6, "#ffffff"), ("real", "THIS PART\nIS REAL", 1.4, "#ffffff"),
                             ("hearts", "3 HEARTS", 2.0, "#ffffff"), ("gills", "2 FOR THE GILLS\n1 FOR THE BODY", 0.95, "#ffffff")):
    TXT[key] = mktext("scr_" + key, body, (0, 29.36, 6.0), size, col, 4.0, extrude=0.01)
for i in range(16):
    x = -12 + i * 1.6
    cube(f"bunt{i}", (x, 21.5, 9.6 - 0.9 * math.sin(math.pi * i / 15)), (0.9, 0.05, 0.9), mat(f"bunt{i % 3}", ["#e8423f", "#ffffff", "#2f63d6"][i % 3], 0.6, 0.4), 0, None, (0, R(45), 0))
BUNT = [o for o in bpy.data.objects if o.name.startswith("bunt")]

# podiums: hero x=-2.2, Pickles x=+2.8 (both y=25.2), host desk x=-6.4
def podium(name, x, col, label):
    root = empty(name, (x, 25.2, ST))
    cube(name + "_body", (0, 0, 0.8), (1.7, 1.2, 1.6), mat(name + "_m", "#f4f1e8", 0.4), 0.05, root)
    cube(name + "_panel", (0, -0.61, 0.85), (1.5, 0.04, 1.1), mat(name + "_p", col, 0.3, 3.0, col), 0.02, root)
    mktext(name + "_lbl", label, (0, -0.65, 0.85), 0.42, "#ffffff", 2.0, extrude=0.01, parent=root)
    cube(name + "_top", (0, 0, 1.63), (1.85, 1.35, 0.08), mat("podtop", "#2b2d48", 0.3), 0.02, root)
    bz = sphere(name + "_buzz", (0.35, -0.15, 1.7), (0.32, 0.32, 0.18), mat(name + "_bz", "#e8282f", 0.25, 0.12, "#ff3a3a"), root, 20)
    cyl(name + "_bzbase", (0.35, -0.15, 1.69), 0.4, 0.1, mat("bzbase", "#1a1a1a", 0.4), parent=root, verts=20)
    mic = empty(name + "_mic", (-0.45, 0.1, 1.67), root)
    cyl(name + "_micpole", (0, 0, 0.55), 0.04, 1.1, mat("micpole", "#2b2d36", 0.3, metal=0.8), parent=mic, verts=8)
    sphere(name + "_michead", (0, -0.12, 1.15), (0.15, 0.15, 0.2), mat("michead", "#3a3d47", 0.4, metal=0.6), mic, 12)
    # shrink-ray lamp over the podium
    lamp = empty(name + "_ray", (0, 0.1, 6.0), root)
    cyl(name + "_raypole", (0, 0.0, 1.2), 0.06, 2.4, mat("micpole", "#2b2d36", 0.3, metal=0.8), parent=lamp, verts=8)
    sphere(name + "_raydome", (0, 0, 0), (0.75, 0.75, 0.45), mat("raydome", "#9a9aa8", 0.25, metal=0.9), lamp, 20)
    ring = cyl(name + "_rayring", (0, 0, -0.38), 0.55, 0.08, mat(name + "_rr", "#7aff6a", 0.3, 6.0, "#7aff6a"), parent=lamp, verts=20)
    zl = point(name + "_zapl", (0, -0.5, -1.0), "#9affff", 0, 1.0, lamp)
    return root, bz, mic, zl
POD_H, BUZ_H, MIC_H, ZAP_H = podium("pod_me", -2.2, "#2f63d6", "ME")
POD_P, BUZ_P, MIC_P, ZAP_P = podium("pod_pk", 2.8, "#3fae4a", "PICKLES")
PODTOP = ST + 1.67
desk = empty("hostdesk", (-6.4, 25.4, ST))
cube("hd_body", (0, 0, 0.7), (2.2, 1.1, 1.4), mat("hdm", "#ffb020", 0.35, 1.0, "#ffb020"), 0.05, desk)
cube("hd_top", (0, 0, 1.43), (2.4, 1.3, 0.08), mat("podtop", "#2b2d48", 0.3), 0.02, desk)
mktext("hd_lbl", "HOST", (0, -0.57, 0.75), 0.45, "#2b2d48", 0.0, extrude=0.01, parent=desk)
# zap bolt (zigzag of emissive bars from the lamp to the podium top)
ZMAT = mat("zap", "#bfffff", 0.2, 40, "#a0ffff")
BOLT = empty("bolt", (0, 0, -500))
_bz = random.Random(9); _p = (0, 0, 0)
for k in range(7):
    q = (_bz.uniform(-0.35, 0.35), _bz.uniform(-0.1, 0.1), -0.62 * (k + 1))
    mid = tuple((a + b) / 2 for a, b in zip(_p, q)); dx, dz = q[0] - _p[0], q[2] - _p[2]
    cube(f"bolt{k}", mid, (0.12, 0.12, math.hypot(dx, dz) + 0.06), ZMAT, 0, BOLT, (0, math.atan2(dx, dz), 0)); _p = q
ZRING = [cube(f"zring{i}", (0, 0, -500), (0.12, 0.12, 0.6), ZMAT, 0) for i in range(10)]
# trophies on Pickles' podium side (bingo)
TROPH = []
GOLD = mat("gold", "#e2b23a", 0.25, metal=1.0)
for k, (x, y, s) in enumerate(((4.2, 24.8, 1.0), (4.7, 25.5, 0.8), (4.0, 25.8, 0.7), (4.9, 24.6, 0.6), (4.45, 26.2, 0.9))):
    t = empty(f"troph{k}", (x, y, ST))
    cyl(f"tr_base{k}", (0, 0, 0.12 * s), 0.3 * s, 0.24 * s, mat("trbase", "#2b2d36", 0.4), parent=t, verts=12)
    cyl(f"tr_stem{k}", (0, 0, 0.45 * s), 0.08 * s, 0.5 * s, GOLD, parent=t, verts=10)
    cyl(f"tr_cup{k}", (0, 0, 0.95 * s), 0.34 * s, 0.6 * s, GOLD, parent=t, verts=16)
    for sd in (-1, 1): cyl(f"tr_h{k}{sd}", (0.4 * s * sd, 0, 1.0 * s), 0.1 * s, 0.06 * s, GOLD, rot=(R(90), 0, 0), parent=t, verts=10)
    TROPH.append(t)
mktext("bingosign", "BINGO\nCHAMP", (4.45, 24.3, ST + 2.4), 0.35, "#ffe14a", 2.0, extrude=0.02)
# fire hydrant on the stage next to the hero podium
hyd = empty("hydrant", (-0.4, 24.4, ST))
HR = mat("hydred", "#d8282f", 0.35)
cyl("hy_body", (0, 0, 0.55), 0.3, 1.1, HR, parent=hyd, verts=16); sphere("hy_cap", (0, 0, 1.12), (0.32, 0.32, 0.22), HR, hyd, 14)
cyl("hy_top", (0, 0, 1.32), 0.08, 0.15, HR, parent=hyd, verts=8); cyl("hy_ring", (0, 0, 0.95), 0.36, 0.1, HR, parent=hyd, verts=16)
for sd in (-1, 1): cyl(f"hy_noz{sd}", (0.34 * sd, 0, 0.7), 0.12, 0.2, mat("hyds", "#f2f2f2", 0.4), rot=(0, R(90), 0), parent=hyd, verts=10)
cyl("hy_base", (0, 0, 0.05), 0.38, 0.1, HR, parent=hyd, verts=16)
# octopus tank (stage right)
TX, TY = 6.8, 25.6
cube("tank_base", (TX, TY, ST + 0.35), (2.6, 2.0, 0.7), mat("tankbase", "#2b2d48", 0.3), 0.04)
TG = bpy.data.materials.new("tankglass"); TG.use_nodes = True; _t = TG.node_tree.nodes["Principled BSDF"]
_t.inputs["Base Color"].default_value = (0.75, 0.92, 1, 1); _t.inputs["Roughness"].default_value = 0.02; _t.inputs["Transmission Weight"].default_value = 1.0; _t.inputs["IOR"].default_value = 1.05
cube("tank_glass", (TX, TY, ST + 1.85), (2.4, 1.8, 2.3), TG, 0.02)
cube("tank_back", (TX, TY + 0.85, ST + 1.85), (2.3, 0.05, 2.2), mat("tankback", "#2a7fd0", 0.5, 0.8, "#3a9fff"), 0)
cube("tank_sand", (TX, TY, ST + 0.78), (2.3, 1.7, 0.12), mat("sand", "#f2d8a0", 0.9), 0)
point("tank_l", (TX, TY - 0.3, ST + 2.8), "#dff4ff", 90, 0.4)
octo = empty("octo", (TX, TY - 0.1, ST + 1.7))
OP = mat("octop", "#ff7aa8", 0.45, 0.2)
sphere("oc_head", (0, 0, 0.45), (0.55, 0.5, 0.62), OP, octo, 20)
for sd in (-1, 1):
    sphere(f"oc_eye{sd}", (0.2 * sd, -0.44, 0.45), (0.13, 0.05, 0.16), mat("sclera", "#ffffff", 0.35, 0.25), octo, 12)
    sphere(f"oc_pup{sd}", (0.2 * sd, -0.48, 0.43), (0.07, 0.04, 0.09), mat("eyeblack", "#141414", 0.25), octo, 10)
TENT = []
for i in range(8):
    a = 2 * math.pi * i / 8; tp = empty(f"oc_tp{i}", (0.35 * math.cos(a), 0.35 * math.sin(a), 0.05), octo)
    tp.rotation_euler = (R(55) * math.sin(a) * -1, R(55) * math.cos(a), 0)
    cyl(f"oc_t{i}", (0, 0, -0.35), 0.09, 0.75, OP, parent=tp, verts=8); TENT.append(tp)
def heart(name, s=1.0, col="#ff2a4a"):
    o = empty(name, (0, 0, -500)); m = mat("heartm", col, 0.3, 3.0, col)
    for sd in (-1, 1): sphere(f"{name}_l{sd}", (0.22 * s * sd, 0, 0.12 * s), (0.3 * s, 0.12 * s, 0.3 * s), m, o, 14)
    cube(f"{name}_b", (0, 0, -0.08 * s), (0.42 * s, 0.2 * s, 0.42 * s), m, 0.05, o, (0, R(45), 0))
    return o
HEARTS = [heart(f"heart{i}", 0.8) for i in range(3)]
# the cat (sniffs the tiny hero)
cat = empty("cat", (0, 0, -500)); CM = mat("catfur", "#f0952a", 0.8)
cube("cat_body", (0, 0.25, 0.4), (0.55, 0.95, 0.5), CM, 0.1, cat)
for sx in (-1, 1):
    for sy in (-1, 1): cube(f"cat_leg{sx}{sy}", (0.18 * sx, 0.25 + 0.32 * sy, 0.12), (0.14, 0.14, 0.26), CM, 0.03, cat)
CATH = empty("cat_neck", (0, -0.25, 0.75), cat)
cube("cat_head", (0, -0.1, 0.0), (0.62, 0.52, 0.5), CM, 0.12, CATH)
for sd in (-1, 1):
    cube(f"cat_ear{sd}", (0.2 * sd, -0.05, 0.3), (0.16, 0.08, 0.2), CM, 0.02, CATH, (0, R(20 * sd), 0))
    sphere(f"cat_eye{sd}", (0.13 * sd, -0.37, 0.05), (0.07, 0.03, 0.1), mat("cateye", "#6aff3a", 0.3, 0.8), CATH, 8)
    sphere(f"cat_pup{sd}", (0.13 * sd, -0.39, 0.05), (0.025, 0.02, 0.08), mat("eyeblack", "#141414", 0.25), CATH, 8)
sphere("cat_nose", (0, -0.37, -0.08), (0.05, 0.03, 0.04), mat("catnose", "#ff7a9a", 0.4), CATH, 8)
CATT = empty("cat_tailp", (0, 0.7, 0.5), cat)
cyl("cat_tail", (0, 0.1, 0.35), 0.06, 0.75, CM, rot=(R(-25), 0, 0), parent=CATT, verts=8)
# Benny's chair in the front row
chair = empty("chair", (-3.5, 17.2, 0.06))
CH = mat("chairm", "#e8423f", 0.5)
cube("ch_seat", (0, 0, 1.0), (1.2, 1.1, 0.14), CH, 0.03, chair); cube("ch_back", (0, -0.5, 1.7), (1.2, 0.12, 1.3), CH, 0.03, chair)
for sx in (-1, 1):
    for sy in (-1, 1): cyl(f"ch_leg{sx}{sy}", (0.5 * sx, 0.45 * sy, 0.5), 0.05, 1.0, mat("micpole", "#2b2d36", 0.3, metal=0.8), parent=chair, verts=6)
CHAIRS = []
for k, x in enumerate(()):
    c = empty(f"chairs{k}", (x, 17.2 + (k % 2) * 0.2, 0.06)); cube(f"chs_seat{k}", (0, 0, 1.0), (1.2, 1.1, 0.14), CH, 0.03, c)
    cube(f"chs_back{k}", (0, 0.5, 1.7), (1.2, 0.12, 1.3), CH, 0.03, c); CHAIRS.append(c)
    for sx in (-1, 1): cyl(f"chs_leg{k}{sx}", (0.5 * sx, 0, 0.5), 0.05, 1.0, mat("micpole", "#2b2d36", 0.3, metal=0.8), parent=c, verts=6)
# question cards (Mayor's) + knitting
CARDS = [cube(f"card{i}", (0, 0, -500), (0.5, 0.03, 0.34), mat("cardm", "#fff6e0", 0.5), 0.01) for i in range(12)]
for c in CARDS: cube(c.name + "_s", (0, -0.02, 0.06), (0.4, 0.01, 0.04), mat("cardline", "#2f63d6", 0.5), 0, c)
handcard = cube("handcard", (0, 0, -500), (0.55, 0.03, 0.38), mat("cardm", "#fff6e0", 0.5), 0.01)
cube("handcard_s", (0, -0.02, 0.08), (0.45, 0.01, 0.05), mat("cardline", "#2f63d6", 0.5), 0, handcard)
knit = empty("knit", (0, 0, -500))
for sd in (-1, 1): cyl(f"kn_needle{sd}", (0.12 * sd, 0, 0.1), 0.03, 0.9, mat("needle", "#d8d8e0", 0.2, metal=0.9), rot=(R(30), R(25 * sd), 0), parent=knit, verts=6)
cube("kn_work", (0, 0.02, -0.15), (0.5, 0.08, 0.35), mat("yarnp", "#e84a8a", 0.9), 0.04, knit)
yarn = sphere("yarnball", (0, 0, -500), (0.3, 0.3, 0.3), mat("yarnp", "#e84a8a", 0.9), seg=12)
# giant scarf on the clock tower (striped)
SCARF = empty("scarf", (0, 0, -500))
for k in range(4):
    for side, (dx, dy, sx, sy) in enumerate(((0, -3.25, 6.9, 0.5), (0, 3.25, 6.9, 0.5), (-3.25, 0, 0.5, 6.9), (3.25, 0, 0.5, 6.9))):
        cube(f"sc_{k}_{side}", (dx, dy, k * 0.55), (sx, sy, 0.55), mat(f"scarf{k % 2}", ["#e84a8a", "#ffffff"][k % 2], 0.95), 0.08, SCARF)
for k in range(6): cube(f"sc_tail{k}", (2.2, -3.4, -0.6 - k * 0.55), (1.4, 0.4, 0.55), mat(f"scarf{k % 2}", ["#e84a8a", "#ffffff"][k % 2], 0.95), 0.06, SCARF)
GIANT_NEEDLE = empty("gneedle", (0, 0, -500))
for sd in (-1, 1): cyl(f"gn{sd}", (0.12 * sd, 0, 0), 0.03, 1.1, mat("needle", "#d8d8e0", 0.2, metal=0.9), rot=(R(30), R(25 * sd), 0), parent=GIANT_NEEDLE, verts=6)

CONF = []
rr = random.Random(7); ccols = ["#ff4fd0", "#40f0ff", "#ffe14a", "#5fff7a", "#ff7a3a", "#ffffff"]
for i in range(90): CONF.append(cube(f"conf{i}", (0, 0, -500), (0.22, 0.04, 0.32), mat(f"conf{i % 6}", ccols[i % 6], 0.5, 1.5), 0))
FW = []
for b, (x, z, col) in enumerate(((-9, 24, "#ff4fd0"), (0, 30, "#ffe14a"), (9, 25, "#40f0ff"))):
    FW.append((x, z, [sphere(f"fw{b}_{i}", (0, 0, -500), (0.25, 0.25, 0.25), mat(f"fwm{b}", col, 0.3, 30, col), seg=6) for i in range(26)]))
SPARK = [sphere(f"spark{i}", (0, 0, -500), (0.1, 0.1, 0.1), mat("sparkm", "#fff6a0", 0.3, 20, "#fff2a0"), seg=6) for i in range(10)]
STARS = [mktext(f"star{i}", "*", (0, 0, -500), 0.9, "#ffe14a", 3.0, extrude=0.06) for i in range(4)]

# ---------------------------------------------------------------- cast
K = dict(cartoon=True, blush=True)
hero = lib.Char("hero", top="#f2b51f", pants="#2f4a7a", hair="#3a2414", hood=True, extra="#d89a12", **K)
ben = lib.Char("benny", skin="#c98d62", top="#d8423f", pants="#3b3b55", hair="#1d1310", hair_style="flat", **K)
cube("bencap", (0, -0.15, 1.05), (1.08, 1.2, 0.25), mat("bencap", "#2f63d6", 0.5), 0.06, ben.neck)
pick = lib.Char("pickles", skin="#f0c8a8", top="#5c9a3a", pants="#3a5a2a", hair="#c8c8c8", hair_style="flat", kid=False, **K)
cube("pk_bun", (0, 0.2, 1.2), (0.55, 0.55, 0.45), pick.mhair, 0.15, pick.neck)
for sd in (-1, 1):
    cube(f"pk_glass{sd}", (0.22 * sd * pick.hs, -0.56 * pick.hs, 0.58 * pick.hs), (0.36 * pick.hs, 0.03, 0.06), mat("glassfr", "#111111", 0.3), 0, pick.neck)
    cube(f"pk_glassb{sd}", (0.22 * sd * pick.hs, -0.56 * pick.hs, 0.38 * pick.hs), (0.36 * pick.hs, 0.03, 0.05), mat("glassfr", "#111111", 0.3), 0, pick.neck)
mayor = lib.Char("mayor", skin="#f0c8a8", top="#2b2d48", pants="#2b2d48", hair="#8a8a8a", hair_style="flat", kid=False, **K); mayor.mayor_kit()
crowd = []
CC = [("#3f8fd8", "#6b3f22"), ("#e86fb0", "#1d1310"), ("#57b65a", "#e0c070"), ("#8b4fb0", "#6b3f22"), ("#e8823f", "#1d1310"),
      ("#2fb0a8", "#e0702e"), ("#c94a4a", "#3a2414"), ("#6a7ad8", "#eeeeee"), ("#f2c53d", "#3a2414"), ("#ff8fb0", "#1d1310"),
      ("#4ac0e8", "#3a2414"), ("#a0d040", "#1d1310")]
for i, (top, hair) in enumerate(CC):
    crowd.append(lib.Char(f"cr{i}", skin=["#f3c89a", "#c98d62", "#8d5a3b", "#e9b892"][i % 4], top=top, pants=["#3b3b55", "#c9b48a", "#2f4a7a"][i % 3],
                          hair=hair, hair_style="spiky" if i % 3 == 0 else "flat", kid=i % 2 == 0, **K))
for _o in CONF + SPARK + STARS + ZRING + [p for _, _, ps in FW for p in ps]: _o.hide_render = True
fill = point("camfill", (0.6, 0.4, 0.2), "#ffe6cc", 160, 1.0, cam)
stagel = [point(f"stagel{k}", (-6 + k * 6, 21.0, 8.5), "#fff0e0", 900, 2.0) for k in range(3)]
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
OFF = (0, 0, -500)
CAST = [hero, ben, pick, mayor] + crowd

def day(ex=0.35):
    bg.inputs["Color"].default_value = (*lib.srgb("#8fc8ff"), 1); bg.inputs["Strength"].default_value = 1.5
    sun.data.energy = 4.5; sun.data.color = lib.srgb("#fff0d8"); sun.rotation_euler = (R(50), 0, R(215))
    for l in STREETLAMPS: l.data.energy = 0
    sc.view_settings.exposure = ex; fill.data.energy = 160
def scr(key, col="blue"):
    for k, o in TXT.items(): o.hide_render = (k != key)
    screen.data.materials[0] = scr_cols[col]
def reset():
    for o in OBJ:
        o.animation_data_clear()
        l, r, s, h, p = BASE[o.name]
        if o.parent is not p: o.parent = p
        o.location, o.rotation_euler, o.scale, o.hide_render = l, r, s, h
        if o.type == "LIGHT":
            o.data.energy = LIGHTS[o.name]
            if o.data.animation_data: o.data.animation_data_clear()
    if cam.data.animation_data: cam.data.animation_data_clear()
    for c in CAST: c.place(OFF); c.pose(); c.face("neutral"); c.root.scale = (1, 1, 1)
    screen.data.materials[0] = scr_cols["blue"]
    cam.data.lens = 28; cam.delta_location = (0, 0, 0)
    for k, o in TXT.items(): o.hide_render = True
    day()
def hold(obj, ch, side=1, loc=(0, -0.3, -1.05)):
    obj.parent = ch.arms[side]; obj.location = loc
def shake(f0, f1, amt=0.15, seed=1):
    r = random.Random(seed)
    for f in range(f0, f1 + 1):
        cam.delta_location = (r.uniform(-amt, amt), r.uniform(-amt, amt), r.uniform(-amt, amt)); cam.keyframe_insert("delta_location", frame=f)
    cam.delta_location = (0, 0, 0); cam.keyframe_insert("delta_location", frame=f1 + 1)
def cheer(c, f0, f1, seed=0):
    c.face("happy", f0); f = f0 + seed % 3; k = 0
    while f <= f1:
        c.pose(f, armL=-160 if k % 2 else -130, armR=-130 if k % 2 else -165, armLs=20, armRs=20, bob=0.25 if k % 2 else 0); f += 3; k += 1
    c.talk(f0, f1, 0.16, 2)
def audience(face="happy", n=12, benny=True):
    """crowd on the plaza facing the stage (+y)"""
    for i, c in enumerate(crowd[:n]):
        row = i // 6; x = -8.0 + (i % 6) * 3.0 + (1.5 if row else 0); y = 15.2 - row * 2.6 + (i % 2) * 0.4
        c.place((x, y, 0.06), 180 + x * 1.5); c.face(face)
    if benny: ben.place((-3.5, 17.0, 0.2), 180); ben.pose(legL=-90, legR=-90); ben.face(face)
def confetti(f0, f1, cx=0, cy=22, spread=10, ztop=13):
    r = random.Random(3)
    for c in CONF:
        x, y = cx + r.uniform(-spread, spread), cy + r.uniform(-spread * 0.6, spread * 0.4); c.hide_render = False
        c.location = (x, y, ztop + r.uniform(0, 4)); c.rotation_euler = (r.uniform(0, 6), r.uniform(0, 6), 0); c.keyframe_insert("location", frame=f0); c.keyframe_insert("rotation_euler", frame=f0)
        c.location = (x + r.uniform(-2, 2), y + r.uniform(-1, 1), ztop - 13 + r.uniform(0.2, 5)); c.rotation_euler = (r.uniform(0, 30), r.uniform(0, 30), r.uniform(0, 6))
        c.keyframe_insert("location", frame=f1); c.keyframe_insert("rotation_euler", frame=f1)
def fireworks(f0, f1, yb=40):
    r = random.Random(5)
    for b, (x, z, parts) in enumerate(FW):
        fb = f0 + b * 4
        for i, p in enumerate(parts):
            a = 2 * math.pi * i / len(parts); e = r.uniform(-1, 1); p.hide_render = False
            p.location = (x, yb, z); p.scale = (0.01, 0.01, 0.01); p.keyframe_insert("location", frame=fb); p.keyframe_insert("scale", frame=fb)
            p.scale = (0.35, 0.35, 0.35); p.keyframe_insert("scale", frame=fb + 4)
            p.location = (x + 6 * math.cos(a) * math.sqrt(1 - e * e), yb + 2 * e, z + 6 * math.sin(a) * math.sqrt(1 - e * e) - 1.5)
            p.scale = (0.05, 0.05, 0.05); p.keyframe_insert("location", frame=min(f1, fb + 18)); p.keyframe_insert("scale", frame=min(f1, fb + 18))
def sparkle(f0, f1, c, r_=0.9):
    for i, p in enumerate(SPARK):
        a = 2 * math.pi * i / len(SPARK); p.hide_render = False
        p.location = c; p.scale = (0.01,) * 3; p.keyframe_insert("location", frame=f0); p.keyframe_insert("scale", frame=f0)
        p.location = (c[0] + r_ * math.cos(a), c[1] - 0.2, c[2] + r_ * math.sin(a)); p.scale = (0.12, 0.12, 0.12)
        p.keyframe_insert("location", frame=f0 + 5); p.keyframe_insert("scale", frame=f0 + 5)
        p.scale = (0.01,) * 3; p.keyframe_insert("scale", frame=min(f1, f0 + 12))
def stars(f0, f1, c, r_=0.9):
    for i, s in enumerate(STARS):
        s.hide_render = False; a = f0 + i * 2
        for f in range(a, f1 + 1, 2):
            ang = (f - a) * 0.5 + i * math.pi / 2
            s.location = (c[0] + r_ * math.cos(ang), c[1] - 0.6 * math.sin(ang) - 0.4, c[2] + 0.25 * math.sin(ang * 2)); s.keyframe_insert("location", frame=f)
def eyes(c, k, f=None):
    for e in c.eyes:
        e.scale = (e.scale[0] * k, e.scale[1], e.scale[2] * k)
        if f is not None: e.keyframe_insert("scale", frame=f)
def scale_at(c, s, f=None):
    c.root.scale = (s, s, s)
    if f is not None: c.root.keyframe_insert("scale", frame=f)
def zap(f0, root=POD_H, zl=ZAP_H, dur=3, pos=None):
    """bolt from the hero's shrink-ray lamp down to the podium + flash"""
    BOLT.parent = None; BOLT.location = pos or (root.location[0], root.location[1] + 0.0, root.location[2] + 5.6)
    for ch in BOLT.children_recursive: ch.hide_render = True; ch.keyframe_insert("hide_render", frame=f0 - 1); ch.hide_render = False; ch.keyframe_insert("hide_render", frame=f0); ch.hide_render = True; ch.keyframe_insert("hide_render", frame=f0 + dur)
    zl.data.energy = 0; zl.data.keyframe_insert("energy", frame=f0 - 1); zl.data.energy = 6000; zl.data.keyframe_insert("energy", frame=f0)
    zl.data.energy = 0; zl.data.keyframe_insert("energy", frame=f0 + dur + 1)
def octo_wiggle(N, k=1.0):
    for f in range(1, N + 1, 3):
        for i, tp in enumerate(TENT):
            a = 2 * math.pi * i / 8; w = math.sin(f * 0.6 + i) * 0.35 * k
            tp.rotation_euler = (R(55) * -math.sin(a) + w * math.sin(a), R(55) * math.cos(a) + w * math.cos(a), 0); tp.keyframe_insert("rotation_euler", frame=f)
        octo.location = (TX, TY - 0.1, ST + 1.7 + 0.12 * math.sin(f * 0.3)); octo.keyframe_insert("location", frame=f)
HERO_POD = (-2.2, 26.15, ST)      # standing behind his podium (podium at y=25.2, depth 1.2)
PK_POD = (2.8, 26.15, ST)
def hero_tiny_on_top(s, x_off=-0.05, y_off=0.1):
    """tiny hero standing on the podium top (next to buzzer + mic)"""
    hero.place((-2.2 + x_off, 25.2 + y_off, PODTOP + 0.0), 0); scale_at(hero, s)
def pickles_at_pod(s=1.0, knitting=True):
    pick.place(PK_POD, 0); scale_at(pick, s); pick.face("happy")
    if knitting:
        hold(knit, pick, 0, (0.45, -0.55, -1.0)); knit.rotation_euler = (R(-20), 0, 0)
        pick.pose(armL=-60, armR=-60, armLs=-25, armRs=-25, head=12)
def knit_anim(N, s=1.0):
    for f in range(1, N + 1, 2):
        k = (f // 2) % 2; pick.pose(f, armL=-60 - 8 * k, armR=-52 + 8 * k, armLs=-25, armRs=-25, head=12)
def mayor_host(face="happy", card=True):
    mayor.place((-6.4, 26.3, ST), 25); mayor.face(face)
    if card: hold(handcard, mayor, 1, (0, -0.4, -1.05)); handcard.rotation_euler = (R(-30), 0, 0); mayor.pose(armR=-70, armL=-10)

# ---------------------------------------------------------------- shots
def s01(N):  # HOOK: the hero at his podium gets ZAPPED and shrinks (teaser); neon stage, THE SHRINK SHOW on the screen
    scr("show", "purple"); audience("surprised", 12); pickles_at_pod(); knit_anim(N)
    hero.place((-3.7, 24.6, ST), 15); hero.face("shock", 1); hero.pose(1, armL=-30, armR=-30, armLs=30, armRs=30)
    zf = 3; zap(zf, pos=(-3.7, 24.6, ST + 5.6)); scale_at(hero, 1.0, zf); scale_at(hero, 0.5, zf + 4); hero.pose(zf + 4, armL=-160, armR=-160)
    shake(zf, zf + 3, 0.12)
    cam_move(cam, tgt, 1, N, (-5.6, 19.0, 3.4), (-5.2, 19.8, 3.5), (-3.0, 25.0, 3.0), (-3.0, 25.0, 2.8), 26, 28)
def s02(N):  # "Ten questions": screen 10 QUESTIONS, fast push from the crowd
    scr("ten", "blue"); audience("happy", 12)
    cam_move(cam, tgt, 1, N, (1.5, 8.0, 3.0), (1.0, 11.0, 3.8), (0, 29.5, 6.0), (0, 29.5, 6.0), 26, 30)
def s03(N):  # "Ten thousand dollars": $10,000 gold, crowd cheers, confetti
    scr("prize", "gold"); audience("happy", 12)
    for i, c in enumerate(crowd[:12]): cheer(c, 1 + i % 3, N, i)
    confetti(1, N + 10, 0, 23, 8)
    cam_move(cam, tgt, 1, N, (-2.0, 10.5, 4.0), (-1.0, 12.0, 4.4), (0, 28, 5.6), (0, 28, 5.8), 26, 28)
def s04(N):  # "But every wrong answer, you shrink": hero close behind his podium, worried look up at the ray lamp
    scr("rule", "red"); hero.place(HERO_POD, 0); hero.face("scared"); hero.pose(1, head=-15); hero.pose(N, head=-24)
    cam_move(cam, tgt, 1, N, (-1.4, 20.8, 4.4), (-1.6, 21.4, 4.6), (-2.2, 26.15, 4.0), (-2.2, 26.15, 4.6), 34, 38)
def s05(N):  # "My opponent? Mrs. Pickles.": dolly across to Pickles at her podium, knitting
    scr("age", "green"); pickles_at_pod(); knit_anim(N); hero.place(HERO_POD, 0); hero.pose(headyaw=-40)
    cam_move(cam, tgt, 1, N, (-1.0, 19.5, 3.6), (2.0, 19.8, 3.8), (0.0, 26.0, 3.5), (2.8, 26.0, 3.9), 30, 32)
def s06(N):  # "She's ninety-one": Pickles close, smug knitting smile, screen AGE 91 behind
    scr("age", "green"); pickles_at_pod(); knit_anim(N); pick.face("evil", 1); pick.face("happy", max(2, N // 2))
    cam_move(cam, tgt, 1, N, (2.3, 22.0, 4.4), (2.4, 22.5, 4.4), (2.8, 26.15, 4.2), (2.8, 26.15, 4.2), 38, 42)
def s07(N):  # "Not even bingo": her pile of gold trophies + BINGO CHAMP sign, slow orbit
    pickles_at_pod(); knit_anim(N)
    cam_move(cam, tgt, 1, N, (6.4, 21.2, 3.0), (5.6, 21.0, 3.2), (4.4, 25.3, 2.3), (4.4, 25.3, 2.4), 32, 34)
def s08(N):  # "The host was the Mayor": Mayor at the host desk lifts his top hat
    scr("show", "purple"); mayor_host("happy", card=False)
    mayor.pose(1, armR=-20); mayor.pose(5, armR=-160, armRs=10); mayor.hat.keyframe_insert("location", frame=4)
    mayor.hat.location = (0, 0, 1.05 * mayor.hs + 0.5); mayor.hat.keyframe_insert("location", frame=7); mayor.talk(1, N, 0.12, 2)
    cam_move(cam, tgt, 1, N, (-4.5, 20.5, 3.4), (-4.9, 21.2, 3.6), (-6.4, 26.3, 4.1), (-6.4, 26.3, 4.2), 32, 36)
def s09(N):  # "Question one. What color is a banana?": wide, Mayor reads the card, screen shows the question
    scr("banana", "blue"); mayor_host(); mayor.talk(1, N, 0.12, 2); hero.place(HERO_POD, 0); pickles_at_pod(); knit_anim(N)
    cam_move(cam, tgt, 1, N, (-2.0, 14.0, 4.2), (-1.4, 15.2, 4.4), (-1.0, 27.0, 4.5), (-0.6, 27.0, 4.6), 22, 24)
def s10(N):  # "Yellow. Easy!": hero slaps his buzzer, screen CORRECT green, cocky grin
    scr("correct", "green"); hero.place(HERO_POD, 0); hero.face("happy"); hero.pose(1, armR=-70); hero.pose(3, armR=-40); hero.talk(1, N, 0.14, 2)
    BUZ_H.scale = (0.32, 0.32, 0.18); BUZ_H.keyframe_insert("scale", frame=2); BUZ_H.scale = (0.34, 0.34, 0.08); BUZ_H.keyframe_insert("scale", frame=3)
    BUZ_H.scale = (0.32, 0.32, 0.18); BUZ_H.keyframe_insert("scale", frame=6)
    cam_move(cam, tgt, 1, N, (-0.6, 21.8, 3.6), (-0.8, 22.2, 3.6), (-2.2, 25.8, 3.4), (-2.2, 25.8, 3.5), 34, 36)
def s11(N):  # "Question two. How many hearts does an octopus have?": the octopus tank close, octopus waves
    scr("octo", "blue"); octo_wiggle(N, 1.5)
    cam_move(cam, tgt, 1, N, (5.2, 21.0, 3.6), (5.6, 21.6, 3.5), (TX, TY, 3.1), (TX, TY, 3.15), 34, 38)
def s12(N):  # "I said one.": hero confident, one arm straight up
    scr("octo", "blue"); hero.place(HERO_POD, 0); hero.face("happy"); hero.pose(1, armR=-40); hero.pose(4, armR=-175); hero.talk(1, N, 0.14, 2)
    cam_move(cam, tgt, 1, N, (-2.6, 21.6, 3.2), (-2.4, 22.0, 3.3), (-2.2, 26.15, 3.6), (-2.2, 26.15, 3.7), 30, 32)
def s13(N):  # "Wrong!": screen red WRONG, ray lamp ring turns red, hero's smile drops, looks up
    scr("wrong", "red"); hero.place(HERO_POD, 0); hero.face("happy", 1); hero.face("shock", 3); hero.pose(1, armR=-175); hero.pose(4, armR=-20, head=-25)
    cam_move(cam, tgt, 1, N, (-1.0, 19.0, 4.6), (-1.2, 19.6, 4.8), (-2.2, 26.0, 5.0), (-2.2, 26.0, 5.4), 26, 28)
def s14(N):  # "Zap!": the bolt hits, hero shrinks to hydrant size, shake
    scr("wrong", "red"); hero.place(HERO_POD, 0); hero.face("shock"); hero.pose(1, armL=-30, armR=-30, armLs=30, armRs=30)
    zap(2); scale_at(hero, 1.0, 2); scale_at(hero, 0.5, 6); shake(2, 5, 0.14)
    cam_move(cam, tgt, 1, N, (-3.4, 20.0, 5.0), (-3.2, 20.4, 4.8), (-2.2, 26.0, 3.6), (-2.2, 26.0, 2.6), 28, 30)
def s15(N):  # "Now I was as small as a fire hydrant": hero (0.5) side by side with the hydrant, same height
    hero.place((-1.25, 24.4, ST), 30); scale_at(hero, 0.5); hero.face("frozen"); hero.pose(armL=-5, armR=-5, headyaw=-30)
    cam_move(cam, tgt, 1, N, (-1.2, 20.4, 2.0), (-0.9, 20.7, 2.0), (-0.85, 24.4, 2.0), (-0.8, 24.4, 2.0), 32, 36)
def s16(N):  # "Mrs. Pickles just said, three, dear.": Pickles leans to her mic, three fingers (arm up), sweet
    pickles_at_pod(knitting=False); pick.pose(1, armR=-60, head=8); pick.pose(4, armR=-150, head=8); pick.talk(1, N, 0.12, 2)
    cam_move(cam, tgt, 1, N, (3.5, 21.6, 4.4), (3.4, 22.1, 4.4), (2.8, 26.0, 4.3), (2.8, 26.0, 4.3), 36, 38)
def s17(N):  # "And she kept on knitting.": close on the needles + pink knitting, yarn ball rolling
    pickles_at_pod(); knit_anim(N)
    yarn.location = (3.6, 24.4, ST + 0.3); yarn.keyframe_insert("location", frame=1); yarn.location = (4.4, 24.0, ST + 0.3); yarn.keyframe_insert("location", frame=N)
    cam_move(cam, tgt, 1, N, (4.4, 22.4, 3.6), (4.2, 22.7, 3.5), (2.9, 25.9, 3.4), (2.9, 25.9, 3.4), 34, 38)
def s18(N):  # "Question three. Does a shark have bones?": screen question, Mayor reads
    scr("shark", "blue"); mayor_host(); mayor.talk(1, N, 0.12, 2); pickles_at_pod(); knit_anim(N)
    hero.place(HERO_POD, 0); scale_at(hero, 0.5)
    cam_move(cam, tgt, 1, N, (2.0, 13.6, 4.0), (1.4, 14.8, 4.4), (0.0, 28.0, 5.5), (-0.5, 28.0, 5.6), 24, 26)
def s19(N):  # "I said yes.": tiny hero jumps behind his podium, only his head pops over it
    scr("shark", "blue"); hero.face("happy")
    for f in range(1, N + 1, 3):
        up = (f // 3) % 2; hero.place((-2.2, 26.0, ST + (0.9 if up else 0.0)), 0, f)
    scale_at(hero, 0.5); hero.pose(armL=-170, armR=-170); hero.talk(1, N, 0.14, 2)
    cam_move(cam, tgt, 1, N, (-2.4, 21.0, 3.2), (-2.3, 21.4, 3.2), (-2.2, 25.6, 3.0), (-2.2, 25.6, 3.0), 32, 34)
def s20(N):  # "Zap!": second bolt, shrink 0.5 -> 0.3; now he stands on the podium top
    scr("wrong", "red"); hero_tiny_on_top(0.5); hero.face("shock"); zap(2); scale_at(hero, 0.5, 2); scale_at(hero, 0.3, 6); shake(2, 5, 0.12)
    hero.pose(1, armL=-30, armR=-30, armLs=30, armRs=30)
    cam_move(cam, tgt, 1, N, (-1.4, 21.6, 4.4), (-1.6, 22.0, 4.2), (-2.2, 25.2, 3.6), (-2.2, 25.2, 3.4), 30, 34)
def s21(N):  # "Now I was the size of a cat.": a cat on the podium top sniffs the tiny hero nose to nose
    hero_tiny_on_top(0.3, -0.45, 0.1); hero.face("scared"); hero.pose(lean=-8)
    cat.location = (-1.75, 25.25, PODTOP); cat.rotation_euler = (0, 0, R(-90)); cat.scale = (0.75, 0.75, 0.75)
    for f in range(1, N + 1, 4): CATH.rotation_euler = (R(8 if (f // 4) % 2 else -4), 0, R(-10)); CATH.keyframe_insert("rotation_euler", frame=f)
    for f in range(1, N + 1, 3): CATT.rotation_euler = (0, R(25 if (f // 3) % 2 else -25), 0); CATT.keyframe_insert("rotation_euler", frame=f)
    cam_move(cam, tgt, 1, N, (-2.2, 22.6, PODTOP + 0.9), (-2.0, 22.9, PODTOP + 0.8), (-2.05, 25.2, PODTOP + 0.45), (-2.05, 25.2, PODTOP + 0.45), 36, 40)
def s22(N):  # "My best friend Benny laughed so hard": Benny in the front row, howling
    audience("happy", 8); ben.face("happy"); ben.talk(1, N, 0.2, 2)
    for f in range(1, N + 1, 3): ben.pose(f, legL=-90, legR=-90, armL=-60 if (f // 3) % 2 else -30, armR=-30 if (f // 3) % 2 else -60, lean=-10 if (f // 3) % 2 else 6, head=-15)
    cam_move(cam, tgt, 1, N, (-2.4, 22.2, 2.6), (-2.6, 21.8, 2.7), (-3.5, 17.0, 3.0), (-3.5, 17.0, 3.0), 32, 36)
def s23(N):  # "he fell off his chair": Benny tips backwards, chair over, legs up
    audience("happy", 0); fb = max(2, N // 3)
    chair.keyframe_insert("rotation_euler", frame=fb - 1); chair.rotation_euler = (R(85), 0, 0); chair.keyframe_insert("rotation_euler", frame=fb + 3)
    ben.place((-3.5, 17.0, 0.2), 180, fb - 1); ben.place((-3.5, 15.6, 0.5), 180, fb + 3); ben.root.keyframe_insert("rotation_euler", frame=fb - 1)
    ben.root.rotation_euler = (R(-80), 0, R(180)); ben.root.keyframe_insert("rotation_euler", frame=fb + 3)
    ben.pose(1, legL=-90, legR=-90, armL=-40); ben.pose(fb + 3, legL=-120, legR=-140, armL=-170, armR=-160); ben.face("happy"); ben.talk(1, N, 0.2, 2)
    shake(fb + 3, fb + 5, 0.06)
    cam_move(cam, tgt, 1, N, (-6.0, 20.6, 2.2), (-5.8, 20.3, 2.2), (-3.5, 16.6, 1.0), (-3.5, 16.4, 0.9), 26, 28)
def s24(N):  # "Question four. I said pizza.": tiny hero on the podium top yells into the giant mic
    scr("q4", "blue"); hero_tiny_on_top(0.3, -0.2, 0.25); hero.face("happy"); hero.pose(1, armR=-120); hero.talk(1, N, 0.16, 2)
    cam_move(cam, tgt, 1, N, (-2.9, 22.6, PODTOP + 0.6), (-2.8, 22.9, PODTOP + 0.6), (-2.5, 25.3, PODTOP + 0.6), (-2.5, 25.3, PODTOP + 0.6), 34, 38)
def s25(N):  # "I don't even know what the question was.": Mayor deadpan stare, the crowd face-palms
    mayor_host("frozen"); audience("frozen", 12)
    for i, c in enumerate(crowd[:12]): c.pose(1 + i % 3, armR=-150, head=10)
    cam_move(cam, tgt, 1, N, (-9.0, 21.8, 3.6), (-8.6, 22.2, 3.6), (-6.4, 26.3, 4.0), (-6.4, 26.3, 4.0), 34, 36)
def s26(N):  # "Zap!": third bolt, 0.3 -> 0.12 (hamster size)
    scr("wrong", "red"); hero_tiny_on_top(0.3); hero.face("shock"); zap(2); scale_at(hero, 0.3, 2); scale_at(hero, 0.12, 6); shake(2, 5, 0.12)
    cam_move(cam, tgt, 1, N, (-1.6, 22.2, 3.9), (-1.7, 22.6, 3.7), (-2.2, 25.2, PODTOP + 0.4), (-2.2, 25.2, PODTOP + 0.2), 34, 38)
def s27(N):  # "By question nine, I was the size of a hamster": macro shot: tiny hero next to the buzzer, it is bigger than him
    scr("q9", "blue"); hero_tiny_on_top(0.12, -0.1, -0.15); hero.face("frozen"); hero.pose(headyaw=30)
    cam_move(cam, tgt, 1, N, (-2.6, 23.9, PODTOP + 0.3), (-2.5, 24.0, PODTOP + 0.3), (-2.15, 25.05, PODTOP + 0.18), (-2.1, 25.05, PODTOP + 0.18), 36, 40)
def s28(N):  # "The microphone was taller than me.": worm's-eye up the mic stand, tiny hero looking up
    hero_tiny_on_top(0.12, -0.32, 0.12); hero.face("surprised"); hero.pose(head=-35)
    cam_move(cam, tgt, 1, N, (-2.55, 24.25, PODTOP + 0.06), (-2.55, 24.3, PODTOP + 0.06), (-2.6, 25.3, PODTOP + 0.6), (-2.65, 25.3, PODTOP + 1.1), 22, 22)
def s29(N):  # "And Mrs. Pickles? She hadn't missed one.": screen CORRECT green behind Pickles, knitting, a bit bigger (1.15)
    scr("correct", "green"); pickles_at_pod(1.15); knit_anim(N)
    cam_move(cam, tgt, 1, N, (1.2, 20.4, 3.6), (1.6, 20.9, 3.8), (2.8, 26.0, 4.2), (2.8, 26.0, 4.4), 32, 34)
def s30(N):  # "Was Mrs. Pickles getting taller?": tilt up her: she now reaches into her ray lamp (1.3)
    pickles_at_pod(1.3); knit_anim(N)
    cam_move(cam, tgt, 1, N, (3.4, 20.8, 2.4), (3.3, 21.0, 2.6), (2.8, 26.0, 2.2), (2.8, 26.0, 6.4), 28, 30)
def s31(N):  # "Nah.": tiny hero shrugs it off (arms out)
    hero_tiny_on_top(0.12, -0.1, -0.1); hero.face("neutral"); hero.pose(1, armL=-10, armR=-10); hero.pose(3, armL=-40, armR=-40, armLs=45, armRs=45, head=6)
    cam_move(cam, tgt, 1, N, (-2.25, 24.0, PODTOP + 0.3), (-2.2, 24.15, PODTOP + 0.28), (-2.15, 25.1, PODTOP + 0.18), (-2.15, 25.1, PODTOP + 0.18), 44, 46)
def s32(N):  # "The big screen said: Pickles, eight points.": score screen, push
    scr("score", "purple"); pickles_at_pod(1.3); knit_anim(N)
    cam_move(cam, tgt, 1, N, (-1.0, 16.0, 5.0), (-0.5, 18.6, 5.6), (0, 29.5, 6.0), (0, 29.5, 6.0), 30, 34)
def s33(N):  # "Me, just one.": tiny hero sits down sad on the podium edge
    hero_tiny_on_top(0.12, -0.2, -0.45); hero.face("scared"); hero.pose(legL=-90, legR=-90, head=18, armL=-20, armR=-20)
    hero.root.location.z = PODTOP - 0.03
    cam_move(cam, tgt, 1, N, (-2.7, 23.9, PODTOP + 0.3), (-2.65, 24.0, PODTOP + 0.3), (-2.4, 24.75, PODTOP + 0.22), (-2.4, 24.75, PODTOP + 0.22), 36, 40)
def s34(N):  # "Then a gust of wind blew away all the Mayor's cards": cards fly off, bunting flaps, his hat spins off
    mayor_host("shock", card=False); mayor.pose(1, armR=-70); mayor.pose(4, armR=-150, armL=-150, armRs=20, armLs=20)
    r = random.Random(4)
    for i, c in enumerate(CARDS):
        f0 = 1 + i % 4; c.location = (-6.0, 25.8, ST + 2.1); c.rotation_euler = (0, 0, 0); c.keyframe_insert("location", frame=f0); c.keyframe_insert("rotation_euler", frame=f0)
        c.location = (-6.0 + r.uniform(4, 14), 25.8 + r.uniform(-4, 1), ST + r.uniform(3, 8)); c.rotation_euler = (r.uniform(0, 12), r.uniform(0, 12), r.uniform(0, 6))
        c.keyframe_insert("location", frame=N); c.keyframe_insert("rotation_euler", frame=N)
    mayor.hat.keyframe_insert("location", frame=2); mayor.hat.keyframe_insert("rotation_euler", frame=2)
    mayor.hat.location = (2.5, -1.0, 3.0); mayor.hat.rotation_euler = (R(200), R(90), 0); mayor.hat.keyframe_insert("location", frame=N); mayor.hat.keyframe_insert("rotation_euler", frame=N)
    for f in range(1, N + 1, 2):
        for k, b in enumerate(BUNT):
            b.rotation_euler = (R(30 * math.sin(f + k)), R(45), 0); b.keyframe_insert("rotation_euler", frame=f)
    cam_move(cam, tgt, 1, N, (-9.8, 19.6, 3.6), (-9.0, 19.8, 4.2), (-5.4, 26.0, 4.2), (-3.4, 26.0, 5.4), 26, 26)
def s35(N):  # "He grabbed the first one he could find": Mayor snatches a card out of the air
    mayor_host("determined", card=False); mayor.hat.hide_render = True
    for ch in mayor.hat.children_recursive: ch.hide_render = True
    hold(handcard, mayor, 1, (0, -0.4, -1.05)); handcard.rotation_euler = (R(-30), 0, 0)
    mayor.pose(1, armR=-175, armRs=20); mayor.pose(4, armR=-150); mayor.pose(N, armR=-80); mayor.face("happy", N)
    cam_move(cam, tgt, 1, N, (-5.0, 21.4, 4.0), (-5.2, 21.8, 4.2), (-6.4, 26.3, 4.8), (-6.4, 26.3, 4.4), 32, 34)
def s36(N):  # "Last question. Ten points.": screen LAST QUESTION 10 POINTS gold, fast push, shake on the drum
    scr("last", "gold"); shake(1, 3, 0.06); pickles_at_pod(1.3); knit_anim(N)
    cam_move(cam, tgt, 1, N, (0.6, 14.0, 4.6), (0.3, 17.5, 5.4), (0, 29.5, 6.0), (0, 29.5, 6.0), 26, 32)
def s37(N):  # "How many hearts does an octopus have?": octopus close again (callback), it waves three tentacles
    scr("octo", "blue"); octo_wiggle(N, 2.5)
    cam_move(cam, tgt, 1, N, (6.0, 22.0, 3.3), (6.2, 22.4, 3.3), (TX, TY, 3.1), (TX, TY, 3.1), 40, 44)
def s38(N):  # "Wait a second. I know this one!": tiny hero close, eyes go wide, stands up determined
    hero_tiny_on_top(0.12, -0.1, -0.1); hero.face("neutral", 1); hero.face("surprised", 3); eyes(hero, 1.0, 3); eyes(hero, 1.25, max(4, N - 4)); hero.face("determined", N)
    hero.pose(1, head=-5); hero.pose(N, armL=-20, armR=-20, lean=-6)
    cam_move(cam, tgt, 1, N, (-2.18, 24.4, PODTOP + 0.3), (-2.17, 24.55, PODTOP + 0.3), (-2.3, 25.1, PODTOP + 0.3), (-2.3, 25.1, PODTOP + 0.3), 46, 52)
def s39(N):  # "Mrs. Pickles reached for her buzzer": her big hand slowly comes down toward her buzzer
    pickles_at_pod(1.3, knitting=False); pick.face("determined"); pick.pose(1, armR=-20); pick.pose(N, armR=-70, lean=8)
    cam_move(cam, tgt, 1, N, (4.4, 21.4, 4.8), (4.2, 21.8, 4.6), (3.0, 25.6, 3.8), (3.0, 25.4, 3.4), 30, 32)
def s40(N):  # "But I jumped on mine": tiny hero leaps off the podium top edge in an arc toward the buzzer (slow-mo feel)
    x0, y0 = -2.55, 25.35; x1, y1 = -1.85, 25.05
    for f in range(1, N + 1):
        a = (f - 1) / max(1, N - 1); hero.place((x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, PODTOP + 0.35 * math.sin(math.pi * a) * 1.6), 30, f)
    scale_at(hero, 0.12); hero.face("determined"); hero.pose(1, armL=-160, armR=-160, legL=40, legR=-40, lean=40)
    cam_move(cam, tgt, 1, N, (-2.9, 24.0, PODTOP + 0.35), (-2.4, 24.0, PODTOP + 0.4), (-2.3, 25.2, PODTOP + 0.3), (-1.9, 25.1, PODTOP + 0.25), 34, 36)
def s41(N):  # "with my whole body": belly-flop onto the buzzer, it slams down, red light flash, shake
    hero.place((-1.85, 25.05, PODTOP + 0.4), 0, 1); hero.place((-1.85, 25.05, PODTOP + 0.12), 0, 3); scale_at(hero, 0.12)
    hero.root.rotation_euler = (R(60), 0, 0); hero.root.keyframe_insert("rotation_euler", frame=1); hero.root.rotation_euler = (R(85), 0, 0); hero.root.keyframe_insert("rotation_euler", frame=3); hero.pose(armL=-170, armR=-170); hero.face("determined")
    BUZ_H.scale = (0.32, 0.32, 0.18); BUZ_H.keyframe_insert("scale", frame=2); BUZ_H.scale = (0.35, 0.35, 0.07); BUZ_H.keyframe_insert("scale", frame=3)
    BUZ_H.scale = (0.33, 0.33, 0.12); BUZ_H.keyframe_insert("scale", frame=N)
    zl = point("buzlight", (-1.85, 24.6, PODTOP + 0.6), "#ff3a3a", 0, 0.5); zl.data.keyframe_insert("energy", frame=2); zl.data.energy = 600; zl.data.keyframe_insert("energy", frame=3)
    shake(3, 6, 0.05)
    cam_move(cam, tgt, 1, N, (-2.4, 24.1, PODTOP + 0.55), (-2.35, 24.2, PODTOP + 0.5), (-1.85, 25.05, PODTOP + 0.1), (-1.85, 25.05, PODTOP + 0.1), 36, 40)
def s42(N):  # "Three!": tiny hero on the buzzer shouts up, three arms... one arm up, Mayor in the background
    hero.place((-1.85, 25.05, PODTOP + 0.15), 0); scale_at(hero, 0.12); hero.face("happy"); hero.pose(1, armR=-120); hero.pose(3, armR=-175, armL=-175); hero.talk(1, N, 0.18, 2)
    mayor_host("surprised")
    cam_move(cam, tgt, 1, N, (-1.6, 24.3, PODTOP + 0.3), (-1.65, 24.4, PODTOP + 0.3), (-1.9, 25.05, PODTOP + 0.3), (-1.9, 25.05, PODTOP + 0.3), 40, 44)
def s43(N):  # "Correct! Eleven to eight!": screen 11 - 8 green, crowd erupts, confetti
    scr("final", "green"); audience("happy", 12)
    for i, c in enumerate(crowd[:12]): cheer(c, 1 + i % 3, N, i)
    cheer(ben, 1, N, 1); ben.place((-3.5, 17.0, 0.06), 180); ben.pose()
    confetti(1, N + 8, 0, 22, 9)
    cam_move(cam, tgt, 1, N, (0.0, 7.0, 3.4), (0.4, 8.6, 4.0), (0, 27, 5.0), (0, 27, 5.4), 22, 24)
def s44(N):  # "Ten thousand dollars!": $10,000 gold, fireworks over the stage
    scr("prize", "gold"); audience("happy", 12)
    for i, c in enumerate(crowd[:12]): cheer(c, 1 + i % 3, N, i)
    confetti(1, N + 8, 0, 22, 9); fireworks(1, N, 40)
    cam_move(cam, tgt, 1, N, (-4.0, 8.5, 5.0), (-3.4, 9.2, 5.6), (0, 30, 9.0), (0, 30, 9.6), 22, 22)
def s45(N):  # "And every right answer makes you grow.": golden sparkles swirl around the tiny hero, ring turns gold
    hero.place((-1.85, 25.05, PODTOP + 0.15), 0); scale_at(hero, 0.12); hero.face("surprised")
    sparkle(1, N, (-1.85, 24.9, PODTOP + 0.4), 0.5); sparkle(max(2, N // 2), N, (-1.85, 24.9, PODTOP + 0.6), 0.7)
    cam_move(cam, tgt, 1, N, (-1.9, 23.6, PODTOP + 0.6), (-1.9, 23.8, PODTOP + 0.6), (-1.85, 25.05, PODTOP + 0.4), (-1.85, 25.05, PODTOP + 0.45), 40, 44)
def s46(N):  # "So I grew right back.": hero grows from tiny to full size in front of his podium, arms up, crowd cheers
    audience("happy", 12); hero.place((-2.2, 24.0, ST), 0); scale_at(hero, 0.12, 1); scale_at(hero, 1.0, max(3, N // 2)); hero.face("happy")
    cheer(hero, max(3, N // 2), N, 0); sparkle(1, N, (-2.2, 23.6, ST + 1.6), 1.6)
    for i, c in enumerate(crowd[:12]): cheer(c, 1 + i % 3, N, i)
    cam_move(cam, tgt, 1, N, (-2.6, 15.6, 3.0), (-2.4, 16.6, 3.4), (-2.2, 24.0, 2.6), (-2.2, 24.0, 3.6), 30, 30)
def s47(N):  # "And this part is real.": hero points at the screen THIS PART IS REAL
    scr("real", "blue"); hero.place((-3.6, 23.9, ST), 140); hero.face("happy"); hero.pose(1, armR=-120, armRs=-10); hero.talk(1, N, 0.12, 3)
    cam_move(cam, tgt, 1, N, (-7.0, 16.0, 3.4), (-6.2, 17.0, 3.6), (-1.0, 27, 4.6), (-1.0, 27, 4.8), 26, 28)
def s48(N):  # "An octopus really has three hearts": octopus in the tank, three glowing hearts pop out above it
    scr("hearts", "red"); octo_wiggle(N, 1.2)
    for i, h in enumerate(HEARTS):
        f0 = 1 + i * 4; x = TX - 0.8 + i * 0.8; h.hide_render = False
        h.location = (x, TY - 1.0, ST + 2.4); h.scale = (0.01,) * 3; h.keyframe_insert("location", frame=f0); h.keyframe_insert("scale", frame=f0)
        h.location = (x, TY - 1.0, ST + 3.6 + 0.2 * (i % 2)); h.scale = (1, 1, 1); h.keyframe_insert("location", frame=f0 + 4); h.keyframe_insert("scale", frame=f0 + 4)
        h.scale = (1.12, 1.12, 1.12); h.keyframe_insert("scale", frame=min(N, f0 + 8))
    cam_move(cam, tgt, 1, N, (5.0, 20.8, 3.6), (5.3, 21.4, 3.8), (TX, TY - 0.6, 3.6), (TX, TY - 0.6, 3.8), 32, 36)
def s49(N):  # "Two pump blood through its gills, and one...": screen 2 FOR THE GILLS / 1 FOR THE BODY, slow push past the tank
    scr("gills", "blue"); octo_wiggle(N, 1.0)
    for i, h in enumerate(HEARTS):
        h.hide_render = False; h.location = (TX - 0.8 + i * 0.8, TY - 1.0, ST + 3.6 + 0.2 * (i % 2))
        h.keyframe_insert("location", frame=1); h.location.z += 0.25; h.keyframe_insert("location", frame=N)
    cam_move(cam, tgt, 1, N, (8.6, 17.0, 3.8), (6.0, 17.6, 4.4), (3.0, 29.0, 5.6), (1.0, 29.0, 5.8), 24, 26)
def s50(N):  # "But Mrs. Pickles got eight right.": Pickles' podium is empty; a huge shadow falls; hero + crowd look up, shocked
    hero.place((-2.2, 24.0, ST), 0); hero.face("shock"); hero.pose(head=-35); audience("shock", 12)
    for i, c in enumerate(crowd[:12]): c.pose(1, head=-30, headyaw=(-1) ** i * 6)
    yarn.location = (2.8, 24.8, ST + 0.3)
    cam_move(cam, tgt, 1, N, (-1.4, 20.0, 2.6), (-1.6, 20.4, 2.4), (-2.2, 24.0, 3.2), (-2.2, 24.0, 3.4), 30, 32)
def giant_pickles(knitting=True):
    pick.place((-10.5, 39.5, 0.0), 55); scale_at(pick, 8.2); pick.face("happy")
    if knitting:
        hold(GIANT_NEEDLE, pick, 0, (0.45, -0.55, -1.0)); pick.pose(armL=-75, armR=-75, armLs=-45, armRs=-45, head=10)
    SCARF.location = (0, 36, 18.6)
def s51(N):  # "Now she's taller than the clock tower.": low wide tilt up: giant Mrs. Pickles next to the tower, waving
    giant_pickles(knitting=False); pick.place((-10.5, 39.5, 0.0), -15); audience("shock", 12); hero.place((-2.2, 24.0, ST), 0); hero.face("shock"); hero.pose(head=-40)
    pick.pose(1, armR=-120, armRs=20); pick.pose(max(2, N // 2), armR=-170, armRs=30); pick.pose(N, armR=-120, armRs=20)
    SCARF.location = (0, 0, -500)
    cam_move(cam, tgt, 1, N, (-13.0, 19.0, 1.2), (-13.4, 18.4, 1.4), (-10.0, 39.0, 11.0), (-9.0, 39.0, 23.0), 15, 15)
def s52(N):  # "Mrs. Pickles is knitting the tower a scarf.": she wraps the striped scarf round the clock tower, smiling
    giant_pickles(); pick.pose(1, armL=-80, armR=-70, armLs=-45, armRs=-45, head=10); pick.pose(N, armL=-70, armR=-80, armLs=-45, armRs=-45, head=10)
    SCARF.location = (0, 36, 18.6); SCARF.scale = (1, 1, 0.3); SCARF.keyframe_insert("scale", frame=1); SCARF.scale = (1, 1, 1); SCARF.keyframe_insert("scale", frame=max(3, N // 2))
    cam_move(cam, tgt, 1, N, (-12.0, 8.0, 10.0), (-11.0, 9.0, 11.5), (-5.0, 36.0, 19.0), (-5.0, 36.0, 19.6), 26, 26)
def s53(N):  # END: golden-hour crane back from the scarfed tower + giant Pickles; A/B candles overlay in post
    giant_pickles()
    for f in range(1, N + 1, 2): pick.pose(f, armL=-75 - 6 * ((f // 2) % 2), armR=-75 + 6 * ((f // 2) % 2), armLs=-45, armRs=-45, head=10)
    audience("happy", 12); hero.place((-2.2, 24.0, ST), 0); hero.face("happy")
    sun.data.color = lib.srgb("#ffc890"); sun.rotation_euler = (R(72), 0, R(235)); bg.inputs["Color"].default_value = (*lib.srgb("#ffb98a"), 1)
    cam_move(cam, tgt, 1, N, (-2.0, 4.0, 6.0), (-4.0, -6.0, 14.0), (-4.0, 32.0, 14.0), (-4.0, 32.0, 16.0), 22, 20)

T = [("s01", 0.0, s01), ("s02", wt(0, 10), s02), ("s03", wt(0, 12), s03), ("s04", wt(0, 15), s04),
     ("s05", L[1], s05), ("s06", wt(1, 4), s06), ("s07", wt(1, 14), s07),
     ("s08", L[2], s08), ("s09", wt(2, 5), s09), ("s10", wt(2, 12), s10),
     ("s11", L[3], s11), ("s12", wt(3, 9), s12),
     ("s13", L[4], s13), ("s14", wt(4, 1), s14), ("s15", wt(4, 2), s15),
     ("s16", L[5], s16), ("s17", wt(5, 6), s17),
     ("s18", L[6], s18), ("s19", wt(6, 7), s19), ("s20", wt(6, 10), s20), ("s21", wt(6, 11), s21),
     ("s22", L[7], s22), ("s23", wt(7, 6), s23),
     ("s24", L[8], s24), ("s25", wt(8, 5), s25), ("s26", wt(8, 13), s26),
     ("s27", L[9], s27), ("s28", wt(9, 10), s28),
     ("s29", L[10], s29), ("s30", wt(10, 7), s30), ("s31", wt(10, 12), s31),
     ("s32", L[11], s32), ("s33", wt(11, 6), s33),
     ("s34", L[12], s34), ("s35", wt(12, 10), s35),
     ("s36", L[13], s36), ("s37", wt(13, 4), s37),
     ("s38", L[14], s38),
     ("s39", L[15], s39), ("s40", wt(15, 6), s40), ("s41", wt(15, 10), s41),
     ("s42", L[16], s42), ("s43", wt(16, 1), s43), ("s44", wt(16, 5), s44),
     ("s45", L[17], s45), ("s46", wt(17, 7), s46),
     ("s47", L[18], s47), ("s48", wt(18, 5), s48), ("s49", wt(18, 10), s49),
     ("s50", L[19], s50), ("s51", L[20], s51), ("s52", wt(20, 7), s52), ("s53", L[21], s53)]
TIMES = [(sid, t, (T[i + 1][1] if i + 1 < len(T) else END), fn) for i, (sid, t, fn) in enumerate(T)]
os.makedirs(W, exist_ok=True)
json.dump([(sid, t0, t1) for sid, t0, t1, _ in TIMES], open(f"{W}/shots_timing.json", "w"))

only = [a for a in sys.argv[1:] if a.startswith("s")]
for sid, t0, t1, fn in TIMES:
    if only and sid not in only: continue
    N = max(2, round((t1 - t0) * FPS)); d = f"{W}/shots/{sid}"
    if not PREV and os.path.exists(f"{d}/done"): continue
    reset(); fn(N)
    if PREV:
        os.makedirs(f"{W}/stills", exist_ok=True)
        sc.frame_set(max(1, int(N * 0.6))); sc.render.filepath = f"{W}/stills/{sid}.png"; bpy.ops.render.render(write_still=True)
        continue
    os.makedirs(d, exist_ok=True)
    sc.frame_start, sc.frame_end = 1, N; sc.render.filepath = f"{d}/"
    t = time.time(); bpy.ops.render.render(animation=True)
    open(f"{d}/done", "w").write(str(N)); print(sid, N, "frames", round(time.time() - t), "s", flush=True)
