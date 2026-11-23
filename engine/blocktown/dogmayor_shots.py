"""Oddwick daily Short 2026-11-23: "I Ran for Mayor Against a Dog" (Blocktown house style, owner 2026-11-20).
The town's Mayor is a dog (Biscuit: top hat + sash). 7-day campaign, $1 = 1 vote: posters (he pees on them), free pizza rally
(he rolls over), the baby kiss (he licks the baby), Benny's cookie stand ($300), Biscuit's TV ad (he sleeps), the debate (he
gives the host his paw), election night tie 312-312, Mrs. Pickles' one dollar, Biscuit wins again; $625 fixes the school roof;
real fact: Rabbit Hash, Kentucky has had dog mayors since 1998, $1 a vote; callback: he pees on my poster. Again.
python3.13 dogmayor_shots.py [sid ...] [--still]   -> /home/claude/work/<slug>/shots/<sid>/####.png (resumable)"""
import sys, os, json, math, random, time, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move

SLUG = "2026-11-23-i-ran-for-mayor-against-a-dog"; FPS = 12
W = f"/home/claude/work/{SLUG}"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; END = vo["total"] + 1.5
WORDS = vo["words"]
def wt(line, k):
    """start time of the k-th word (0-based) of a line"""
    ws = [w for w in WORDS if w["line"] == line]; return ws[min(k, len(ws) - 1)]["s"] - 0.04
PREV = "--still" in sys.argv
RES = (216, 384) if PREV else (432, 768)
sc, cam, tgt = lib.setup(res=RES, samples=4 if PREV else 8, fps=FPS)
sc.render.threads_mode = "AUTO"
town = lib.build_town()
FONT = None
for fp in ("/root/.fonts/Fredoka-Bold.ttf", "/home/claude/work/fonts/Fredoka-Bold.ttf"):
    if os.path.exists(fp): FONT = bpy.data.fonts.load(fp); break
bg = sc.world.node_tree.nodes["Background"]
sun = sc.objects["moonlight"]; sc.objects["moon"].hide_render = True
STREETLAMPS = [o for o in sc.objects if o.type == "LIGHT" and o.name.startswith("lamp")]

def mktext(name, body, loc, size, col, emit=0.0, rot=(90, 0, 0), extrude=0.04, parent=None):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = extrude
    if FONT: cu.font = FONT
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    if parent: o.parent = parent
    cu.materials.append(mat(name + "m", col, 0.5, emit)); return o

# ---------------------------------------------------------------- town square: stage + big screen (election show)
cube("plaza", (0, 22, 0.02), (40, 22, 0.06), mat("plaza", "#c9b79a", 0.85), 0)
cube("stage", (0, 26.5, 0.7), (16, 6, 1.4), mat("stagefloor", "#1c1830", 0.3, metal=0.2), 0.05)
cube("stage_edge", (0, 23.48, 1.3), (16.2, 0.12, 0.2), mat("neon_cyan", "#40f0ff", 0.3, 10, "#40f0ff"), 0)
cube("stage_edge2", (0, 23.48, 0.25), (16.2, 0.12, 0.15), mat("neon_pink", "#ff4fd0", 0.3, 10, "#ff4fd0"), 0)
cube("screenwall", (0, 29.8, 5.0), (17, 0.6, 9.6), mat("screenwall", "#120e22", 0.4), 0.05)
scr_cols = {"blue": mat("scr_blue", "#2a3cff", 0.3, 3.0, "#3a5cff"), "red": mat("scr_red", "#ff2a3a", 0.3, 4.0, "#ff2a3a"),
            "green": mat("scr_green", "#1fc85a", 0.3, 4.0, "#2aff6a"), "purple": mat("scr_purple", "#8a2aff", 0.3, 3.5, "#9a3aff"),
            "pink": mat("scr_pink", "#ff3fae", 0.3, 3.5, "#ff3fae"), "gold": mat("scr_gold", "#e0a020", 0.3, 3.5, "#ffb020")}
screen = cube("bigscreen", (0, 29.45, 6.0), (9.5, 0.1, 5.2), scr_cols["blue"], 0)
for sd in (-1, 1):
    cube(f"sidescr{sd}", (6.6 * sd, 29.45, 5.2), (2.6, 0.1, 6.4), mat(f"sidescr{sd}", "#ff4fd0" if sd < 0 else "#40f0ff", 0.3, 5.0), 0)
    for i in range(6): cube(f"sidebar{sd}{i}", (6.6 * sd, 29.38, 2.6 + i * 1.05), (2.2, 0.05, 0.18), mat("barw", "#ffffff", 0.3, 6.0), 0)
for i in range(22):
    a = i / 22
    x = -5.2 + 10.4 * a if i < 11 else -5.2 + 10.4 * (a - 0.5) * 2
    sphere(f"bulb{i}", (x, 29.35, 8.95 if i < 11 else 3.05), (0.16, 0.16, 0.16), mat("bulbm", "#ffe27a", 0.3, 12, "#ffcf4a"), seg=8)
for i in range(9):
    a = math.pi * i / 8
    sphere(f"arch{i}", (-8.6 * math.cos(a), 29.0, 1.4 + 9.6 * math.sin(a) * 0.95), (0.3, 0.3, 0.3), mat("archm", "#ff4fd0" if i % 2 else "#40f0ff", 0.3, 14), seg=8)
SPOTS = [spot(f"stspot{i}", (x, 10, 12), c, 0, 30, rot=(math.radians(45), 0, math.radians(-x * 2)))
         for i, (x, c) in enumerate(((-6, "#ff6fd8"), (0, "#ffffff"), (6, "#5ff0ff")))]
point("stagefill", (0, 21, 6), "#c9b6ff", 0, 4.0)
TXT = {}
for key, body, size, col in (("mayor", "MAYOR\nBISCUIT", 1.5, "#ffe14a"), ("days", "ELECTION\nIN 7 DAYS", 1.2, "#ffffff"),
                             ("wins", "5 ELECTIONS\n5 WINS", 1.15, "#ffffff"), ("rule", "1 VOTE = $1", 1.45, "#ffe14a"),
                             ("vote", "VOTE AS MUCH\nAS YOU WANT", 1.0, "#ffffff"), ("pizza", "FREE PIZZA\nFRIDAYS!", 1.25, "#ffffff"),
                             ("me300", "ME: 300", 2.0, "#ffffff"), ("ad", "VOTE\nBISCUIT", 1.6, "#ffffff"),
                             ("debate", "THE BIG\nDEBATE", 1.5, "#ffe14a"), ("plan", "ROADS\nPARK\nSCHOOL ROOF", 0.95, "#ffffff"),
                             ("night", "ELECTION\nNIGHT", 1.5, "#ffe14a"),
                             ("c1", "ME  205\nBISCUIT  190", 0.95, "#ffffff"), ("c2", "ME  288\nBISCUIT  301", 0.95, "#ffffff"),
                             ("c3", "ME  312\nBISCUIT  312", 0.95, "#ffffff"), ("tie", "TIE!", 3.0, "#ffffff"),
                             ("c4", "ME  312\nBISCUIT  313", 0.95, "#ffffff"), ("win", "BISCUIT\nWINS!", 1.7, "#ffffff"),
                             ("raised", "$625\nRAISED", 1.7, "#ffffff"), ("real", "THIS PART\nIS REAL", 1.4, "#ffffff"),
                             ("since", "DOG MAYORS\nSINCE 1998", 1.2, "#ffffff")):
    TXT[key] = mktext("scr_" + key, body, (0, 29.36, 6.0), size, col, 4.0, extrude=0.01)
# election bunting
for i in range(16):
    x = -12 + i * 1.6
    cube(f"bunt{i}", (x, 21.5, 9.6 - 0.9 * math.sin(math.pi * i / 15)), (0.9, 0.05, 0.9), mat(f"bunt{i % 3}", ["#e8423f", "#ffffff", "#2f63d6"][i % 3], 0.6, 0.4), 0, None, (0, math.radians(45), 0))
# debate podiums
podium = empty("podiums", (0, 0, 0))
for k, (x, col, lab) in enumerate(((-3.6, "#ffd23a", "ME"), (3.6, "#ff4fd0", "BISCUIT"))):
    cube(f"pod{k}", (x, 25.2, 2.0), (1.8, 1.2, 1.3), mat(f"podm{k}", "#2a2050", 0.4), 0.05, podium)
    cube(f"podl{k}", (x, 24.58, 2.4), (1.6, 0.05, 0.22), mat(f"podn{k}", col, 0.3, 10, col), 0, podium)
    mktext(f"podt{k}", lab, (x, 24.55, 1.9), 0.38 if k else 0.5, "#ffffff", 3.0, extrude=0.01, parent=podium)
# confetti + fireworks
CONF = []
rr = random.Random(7); ccols = ["#ff4fd0", "#40f0ff", "#ffe14a", "#5fff7a", "#ff7a3a", "#ffffff"]
for i in range(90): CONF.append(cube(f"conf{i}", (0, 0, -500), (0.22, 0.04, 0.32), mat(f"conf{i % 6}", ccols[i % 6], 0.5, 1.5), 0))
FW = []
for b, (x, z, col) in enumerate(((-9, 24, "#ff4fd0"), (0, 30, "#ffe14a"), (9, 25, "#40f0ff"))):
    FW.append((x, z, [sphere(f"fw{b}_{i}", (0, 0, -500), (0.25, 0.25, 0.25), mat(f"fwm{b}", col, 0.3, 30, col), seg=6) for i in range(26)]))
SPARK = [sphere(f"spark{i}", (0, 0, -500), (0.1, 0.1, 0.1), mat("sparkm", "#fff6a0", 0.3, 20, "#fff2a0"), seg=6) for i in range(8)]

# ---------------------------------------------------------------- props
def poster(name):
    o = empty(name, (0, 0, -500))
    cube(name + "_b", (0, 0, 0), (1.5, 0.06, 1.9), mat("posterbg", "#ffd23a", 0.6), 0.02, o)
    cube(name + "_f", (0, -0.04, 0.32), (0.75, 0.03, 0.75), mat("posterface", "#f3c89a", 0.6), 0.03, o)   # tiny hero head
    cube(name + "_h", (0, -0.05, 0.66), (0.78, 0.03, 0.2), mat("posterhair", "#3a2414", 0.6), 0.01, o)
    for sd in (-1, 1): cube(f"{name}_e{sd}", (0.16 * sd, -0.06, 0.38), (0.1, 0.02, 0.14), mat("eyeblack", "#141414", 0.25), 0, o)
    cube(name + "_m", (0, -0.06, 0.15), (0.28, 0.02, 0.06), mat("mouth", "#3a1512", 0.5), 0, o)
    t = mktext(name + "_t", "VOTE ME", (0, -0.06, -0.55), 0.36, "#c8282f", 0.3, extrude=0.01, parent=o); t.location = (0, -0.06, -0.58)
    return o
POSTERS = [poster(f"poster{i}") for i in range(7)]
BIG_POSTER = POSTERS[0]
puddle = cyl("puddle", (0, 0, -500), 0.6, 0.03, mat("puddlem", "#f2d43a", 0.1, 0.4, "#f2d43a"), verts=20)
pizza = empty("pizza", (0, 0, -500))
cyl("pz_base", (0, 0, 0), 0.75, 0.1, mat("pz_crust", "#e8b15a", 0.6), parent=pizza, verts=24)
cyl("pz_top", (0, 0, 0.06), 0.66, 0.04, mat("pz_cheese", "#ffd24a", 0.5, 0.2), parent=pizza, verts=24)
for k in range(7):
    a = k * 2 * math.pi / 7; r = 0.38 if k else 0
    cyl(f"pz_pep{k}", (r * math.cos(a), r * math.sin(a), 0.09), 0.12, 0.03, mat("pz_pep", "#c8322a", 0.5), parent=pizza, verts=12)
mega = empty("mega", (0, 0, -500))
bpy.ops.mesh.primitive_cone_add(radius1=0.42, radius2=0.12, depth=0.9, location=(0, 0, 0), rotation=(math.radians(90), 0, 0))
_m = bpy.context.active_object; _m.data.materials.append(mat("megam", "#e8423f", 0.4)); _m.parent = mega
paper = empty("paper", (0, 0, -500))
cube("pp_sheet", (0, 0, 0), (1.5, 0.04, 1.0), mat("paperm", "#f4f1e8", 0.7), 0.01, paper)
pt = mktext("pp_t", "NEWS", (0, -0.03, 0.2), 0.36, "#141414", 0.0, rot=(90, 180, 0), extrude=0.005, parent=paper); pt.location = (0, -0.03, -0.18)
for k in range(3): cube(f"pp_l{k}", (0, -0.03, 0.08 + k * 0.14), (1.2, 0.01, 0.05), mat("pp_line", "#555555", 0.7), 0, paper)
jar = empty("jar", (0, 0, -500))
cyl("jar_glass", (0, 0, 1.0), 0.95, 2.0, mat("jarm", "#9fd4f0", 0.1, 0.12, "#cfefff"), parent=jar, verts=24)
cyl("jar_lid", (0, 0, 2.05), 1.0, 0.14, mat("jarlid", "#2f63d6", 0.4), parent=jar, verts=24)
jl = mktext("jar_t", "VOTES $1", (0, -0.97, 1.1), 0.36, "#c8282f", 0.2, extrude=0.01, parent=jar); jl.location = (0, -0.97, 1.1)
for k in range(9): cube(f"jar_bill{k}", (random.Random(k).uniform(-0.5, 0.5), random.Random(k + 9).uniform(-0.5, 0.5), 0.15 + k * 0.1), (0.7, 0.35, 0.04), mat("billg", "#6fbf6a", 0.7), 0, jar, (0, 0, 0.7 * k))
bill = cube("bill", (0, 0, -500), (0.7, 0.04, 0.35), mat("billg", "#6fbf6a", 0.7), 0.01)
BILLS = [cube(f"fbill{i}", (0, 0, -500), (0.55, 0.04, 0.28), mat("billg", "#6fbf6a", 0.7), 0.01) for i in range(10)]
purse = empty("purse", (0, 0, -500))
cube("pu_body", (0, 0, 0), (0.75, 0.32, 0.55), mat("pursem", "#8a3fb0", 0.5), 0.08, purse)
cube("pu_clasp", (0, -0.17, 0.2), (0.16, 0.04, 0.1), mat("gold2", "#f2c230", 0.2, 0.3, "#f2c230", metal=1.0), 0.02, purse)
cushion = cube("cushion", (0, 0, -500), (2.6, 2.8, 0.45), mat("cushm", "#c8282f", 0.6), 0.2)
ZZ = [mktext(f"zz{i}", "Z", (0, 0, -500), 0.55 + 0.2 * i, "#ffffff", 2.0, extrude=0.04) for i in range(3)]
def heart(name):
    o = empty(name, (0, 0, -500)); hm_ = mat("heartm", "#ff4f8a", 0.4, 2.5, "#ff4f8a")
    for sd in (-1, 1): sphere(f"{name}_l{sd}", (0.17 * sd, 0, 0.12), (0.22, 0.12, 0.22), hm_, o, 10)
    cube(f"{name}_b", (0, 0, -0.05), (0.34, 0.2, 0.34), hm_, 0.06, o, (0, math.radians(45), 0)); return o
HEARTS = [heart(f"hrt{i}") for i in range(6)]
# cookie stand (Benny)
LX, LY = -3.5, 17.5
stand = empty("stand", (LX, LY, 0))
cube("ls_box", (0, 0, 1.1), (3.2, 1.4, 2.2), mat("ls_wood", "#ffe14a", 0.6), 0.05, stand)
cube("ls_top", (0, 0, 2.25), (3.5, 1.7, 0.12), mat("ls_white", "#ffffff", 0.4), 0.02, stand)
for sd in (-1, 1): cube(f"ls_post{sd}", (1.55 * sd, 0.55, 3.3), (0.14, 0.14, 2.2), mat("ls_white", "#ffffff", 0.4), 0, stand)
cube("ls_roof", (0, 0.2, 4.45), (3.9, 2.2, 0.2), mat("ls_red", "#2f63d6", 0.5), 0.03, stand, (math.radians(-10), 0, 0))
cube("ls_signb", (0, -0.73, 1.45), (2.8, 0.05, 0.9), mat("ls_white", "#ffffff", 0.4), 0.02, stand)
mktext("ls_sign", "COOKIES", (0, -0.77, 1.6), 0.5, "#c8282f", 0.4, extrude=0.01, parent=stand).location = (0, -0.77, 1.64)
mktext("ls_price", "$1 = 1 VOTE", (0, -0.77, 1.15), 0.32, "#1a7a3a", 0.4, extrude=0.01, parent=stand).location = (0, -0.77, 1.14)
for k in range(8):
    cyl(f"ck{k}", (-1.3 + (k % 4) * 0.42, -0.25 + (k // 4) * 0.45, 2.36), 0.19, 0.08, mat("cookie", "#c98a4a", 0.7), parent=stand, verts=12)
point("ls_lamp", (0, -0.8, 4.0), "#ffd9a0", 0, 1.0, stand)
cashpile = empty("cashpile", (0, 0, -500))
rc = random.Random(11)
for k in range(26): cube(f"cp{k}", (rc.uniform(-0.9, 0.9), rc.uniform(-0.5, 0.5), 0.04 + k * 0.035), (0.7, 0.35, 0.04), mat("billg", "#6fbf6a", 0.7), 0, cashpile, (0, 0, rc.uniform(0, 3)))
# TV ad plane (texture = a frame of the sleeping-Biscuit shot, loaded at shot time)
tvimg = bpy.data.materials.new("tvimg"); tvimg.use_nodes = True
_nt = tvimg.node_tree; _nt.nodes.clear()
_tex = _nt.nodes.new("ShaderNodeTexImage"); _em = _nt.nodes.new("ShaderNodeEmission"); _out = _nt.nodes.new("ShaderNodeOutputMaterial")
_nt.links.new(_tex.outputs["Color"], _em.inputs["Color"]); _em.inputs["Strength"].default_value = 1.6; _nt.links.new(_em.outputs["Emission"], _out.inputs["Surface"])
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -500), rotation=(math.radians(90), 0, 0)); tvp = bpy.context.active_object; tvp.name = "tvplane"
tvp.scale = (2.75, 4.9, 1); tvp.data.materials.append(tvimg)
# the school (end of the street, north side)
SX, SY = -92.0, 15.0
cube("sch", (SX, SY, 3.2), (16, 7, 6.4), mat("schw", "#f2e2b0", 0.7), 0.08)
for i in range(5): cube(f"schrf{i}", (SX, SY, 6.7 + i * 0.5), (17 - i * 3, 7.6, 0.55), mat("schroof", "#e8423f", 0.5, 0.15), 0.05)
cube("sch_patch", (SX + 3, SY - 1.6, 7.9), (2.6, 2.2, 0.1), mat("schpatch", "#ff6a5a", 0.3, 0.4), 0.04, None, (math.radians(-25), 0, 0))
for wx in (-6, -3, 3, 6):
    cube(f"schwin{wx}", (SX + wx, SY - 3.52, 3.6), (1.6, 0.1, 1.6), mat("winlit", "#ffd27a", 0.4, 6.0, "#ffbf5e"), 0.02)
cube("sch_door", (SX, SY - 3.52, 1.4), (2.4, 0.1, 2.8), mat("schdoor", "#2f63d6", 0.5), 0.03)
mktext("sch_sign", "SCHOOL", (SX, SY - 3.6, 5.3), 1.0, "#2f63d6", 0.3, extrude=0.05)
banner = empty("banner", (SX, SY - 3.75, 4.55))
cube("bn_b", (0, 0, 0), (6.5, 0.05, 0.75), mat("bnm", "#ffffff", 0.5), 0.02, banner)
mktext("bn_t", "NEW ROOF!", (0, -0.05, 0), 0.5, "#c8282f", 0.3, extrude=0.01, parent=banner).location = (0, -0.05, 0)
RIB = [cube(f"rib{sd}", (SX + 0.8 * sd, SY - 5.2, 1.6), (1.6, 0.06, 0.18), mat("ribm", "#e8423f", 0.4), 0) for sd in (-1, 1)]
for sd in (-1, 1): cyl(f"ribpost{sd}", (SX + 1.75 * sd, SY - 5.2, 0.85), 0.08, 1.7, mat("pole", "#2b2d36", 0.4, metal=0.6), verts=8)
point("sch_sun", (SX, SY - 10, 9), "#fff2dc", 900, 2.0)
SCHOOL_FRONT = (SX, SY - 6.5)

# ---------------------------------------------------------------- Biscuit (cartoon dog Mayor) + two other dog mayors
class Mutt:
    """facing -y. root -> roll (pivot at body centre) -> body, head, legs, tail. Big cartoon eyes (house style)."""
    def __init__(self, name, fur="#e0a050", belly="#fff1dc", ear="#9a5a2a", mayor=True, s=1.0):
        self.name = name; self.s = s
        M = lambda n, c, *a, **k: mat(f"{name}_{n}", c, *a, **k)
        mf, mb, me = M("fur", fur, 0.75), M("belly", belly, 0.75), M("ear", ear, 0.75)
        self.root = empty(name); self.root.scale = (s, s, s)
        self.roll = empty(name + "_roll", (0, 0, 0.95), self.root)
        cube(name + "_body", (0, 0, 0), (1.05, 1.9, 0.85), mf, 0.14, self.roll)
        cube(name + "_chest", (0, -0.78, -0.05), (0.8, 0.4, 0.7), mb, 0.1, self.roll)
        self.legs = []
        for i, (x, y) in enumerate(((-0.32, -0.68), (0.32, -0.68), (-0.32, 0.68), (0.32, 0.68))):
            h = empty(f"{name}_hip{i}", (x, y, -0.3), self.roll)
            cube(f"{name}_leg{i}", (0, 0, -0.33), (0.3, 0.3, 0.68), mf, 0.05, h)
            cube(f"{name}_paw{i}", (0, -0.04, -0.66), (0.34, 0.38, 0.14), mb, 0.04, h); self.legs.append(h)
        self.tail = empty(name + "_tailp", (0, 0.95, 0.3), self.roll)
        cube(name + "_tail", (0, 0.18, 0.28), (0.18, 0.18, 0.62), mf, 0.06, self.tail, (math.radians(-35), 0, 0))
        self.head = empty(name + "_neck", (0, -0.95, 0.45), self.roll)
        hd = cube(name + "_head", (0, -0.15, 0.42), (1.08, 1.0, 0.98), mf, 0.18, self.head)
        cube(name + "_snout", (0, -0.75, 0.2), (0.62, 0.42, 0.42), mb, 0.12, self.head)
        cube(name + "_nose", (0, -0.98, 0.36), (0.26, 0.08, 0.17), mat("eyeblack", "#141414", 0.25), 0.04, self.head)
        self.tongue = cube(name + "_tongue", (0, -0.86, -0.06), (0.24, 0.2, 0.3), M("tongue", "#ff6f8a", 0.4), 0.06, self.head)
        self.tongue.scale = (1, 1, 0.01)
        self.ears = []
        for sd in (-1, 1):
            ep = empty(f"{name}_earp{sd}", (0.52 * sd, -0.1, 0.85), self.head)
            cube(f"{name}_ear{sd}", (0.06 * sd, 0, -0.32), (0.18, 0.5, 0.72), me, 0.06, ep); self.ears.append(ep)
        sclera, blk, wht = mat("sclera", "#ffffff", 0.35, 0.25), mat("eyeblack", "#141414", 0.25), mat("eyewhite", "#ffffff", 0.3, 1.5)
        self.eyes, self.lids = [], []
        for sd in (-1, 1):
            e = sphere(f"{name}_eye{sd}", (0.24 * sd, -0.655, 0.62), (0.17, 0.03, 0.21), sclera, self.head)
            sphere(f"{name}_pupil{sd}", (0.05 * sd, -0.75, -0.08), (0.58, 0.9, 0.62), blk, e)
            sphere(f"{name}_glint{sd}", (0.24 * sd + 0.06, -1.5, 0.22), (0.2, 0.5, 0.22), wht, e, 8)
            lid = cube(f"{name}_lid{sd}", (0.24 * sd, -0.665, 0.6), (0.3, 0.03, 0.05), blk, 0, self.head); lid.hide_render = True
            sphere(f"{name}_blush{sd}", (0.4 * sd, -0.66, 0.36), (0.1, 0.02, 0.06), mat("blush", "#ff7a9a", 0.6, 0.4, "#ff6f91"), self.head, 10)
            self.eyes.append(e); self.lids.append(lid)
        self.brows = [cube(f"{name}_brow{sd}", (0.24 * sd, -0.67, 0.9), (0.26, 0.04, 0.08), mat("dogbrow", "#4a2a14"), 0, self.head) for sd in (-1, 1)]
        if mayor:
            blkh = mat("hat", "#15151c", 0.4)
            self.hat = empty(name + "_hat", (0.1, -0.15, 0.93), self.head); self.hat.rotation_euler = (0, math.radians(12), 0)
            cyl(name + "_brim", (0, 0, 0), 0.55, 0.06, blkh, parent=self.hat, verts=20)
            cyl(name + "_crown", (0, 0, 0.38), 0.36, 0.72, blkh, parent=self.hat, verts=20)
            cyl(name + "_band", (0, 0, 0.12), 0.37, 0.13, mat("hatband", "#b0262e"), parent=self.hat, verts=20)
            cube(name + "_sash", (0, -0.1, 0.05), (1.1, 0.42, 0.9), mat("sash", "#c8282f", 0.5), 0.05, self.roll, (0, 0, 0)).scale = (1.04, 0.5, 1.05)
            cube(name + "_medal", (0, -0.98, -0.02), (0.26, 0.05, 0.26), mat("gold", "#e2b23a", 0.25, metal=1.0), 0.04, self.roll)
        self.face("happy")
    def face(self, kind, f=None):
        ew, eh, brow, by, closed, tongue = {"happy": (1, 1, 0, 0, False, 0.01), "smug": (1, 0.7, -18, -0.03, False, 0.01),
                                            "tongue": (1, 1, 0, 0.02, False, 1.0), "surprised": (1.2, 1.3, 10, 0.06, False, 0.01),
                                            "sleep": (1, 0.08, 0, -0.04, True, 0.01), "proud": (0.95, 0.85, -8, 0, False, 0.6)}[kind]
        for sd, e, b, lid in zip((-1, 1), self.eyes, self.brows, self.lids):
            e.scale = (0.17 * ew, 0.03, 0.21 * eh); b.location.z = 0.9 + by; b.rotation_euler = (0, math.radians(brow * sd), 0)
            lid.hide_render = not closed
            for ch in e.children: ch.hide_render = closed
            if f is not None:
                e.keyframe_insert("scale", frame=f); b.keyframe_insert("location", frame=f); b.keyframe_insert("rotation_euler", frame=f)
                lid.keyframe_insert("hide_render", frame=f)
                for ch in e.children: ch.keyframe_insert("hide_render", frame=f)
        self.tongue.scale = (1, 1, tongue)
        if f is not None: self.tongue.keyframe_insert("scale", frame=f)
    def place(self, loc, yaw=0, f=None):
        self.root.location = loc; self.root.rotation_euler = (0, 0, math.radians(yaw))
        if f is not None: self.root.keyframe_insert("location", frame=f); self.root.keyframe_insert("rotation_euler", frame=f)
    def pose(self, f=None, legs=(0, 0, 0, 0), legs_y=(0, 0, 0, 0), pitch=0, rolly=0, rollz=0.95, head=0, headyaw=0, headtilt=0):
        for h, a, b in zip(self.legs, legs, legs_y): h.rotation_euler = (math.radians(a), math.radians(b), 0)
        self.roll.rotation_euler = (math.radians(pitch), math.radians(rolly), 0); self.roll.location = (0, 0, rollz)
        self.head.rotation_euler = (math.radians(head), math.radians(headtilt), math.radians(headyaw))
        if f is not None:
            for h in self.legs: h.keyframe_insert("rotation_euler", frame=f)
            self.roll.keyframe_insert("rotation_euler", frame=f); self.roll.keyframe_insert("location", frame=f); self.head.keyframe_insert("rotation_euler", frame=f)
    def sit(self, f=None, **k):
        self.pose(f, legs=(35, 35, -55, -55), pitch=-32, rollz=1.05, head=k.get("head", 28), headtilt=k.get("headtilt", 0), headyaw=k.get("headyaw", 0))
    def wag(self, f0, f1, amp=35, period=3):
        f = f0; k = 0
        while f <= f1:
            self.tail.rotation_euler = (0, 0, math.radians(amp if k % 2 else -amp)); self.tail.keyframe_insert("rotation_euler", frame=f); f += period / 2; k += 1
    def trot(self, f0, f1, period=6, amp=35):
        f = f0; k = 0
        while f <= f1:
            s = 1 if k % 2 == 0 else -1
            self.pose(f, legs=(amp * s, -amp * s, -amp * s, amp * s), rollz=0.95 + 0.08 * (k % 2)); f += period / 2; k += 1
    def pant(self, f0, f1, rate=3):
        f = f0; k = 0
        while f <= f1:
            self.tongue.scale = (1, 1, 1.0 if k % 2 == 0 else 0.7); self.tongue.keyframe_insert("scale", frame=f); f += rate; k += 1

bis = Mutt("biscuit")
dog2 = Mutt("dog2", fur="#f4f1e8", belly="#ffffff", ear="#3a2a20")
dog3 = Mutt("dog3", fur="#4a3a30", belly="#c9a882", ear="#2a1a10")

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
host = lib.Char("host", skin="#8d5a3b", top="#ff7fb8", pants="#3b3b55", hair="#1d1310", hair_style="flat", kid=False, **K)
cube("host_bow", (0, -0.33, 2.6), (0.5, 0.05, 0.22), mat("frbow", "#ff4f9a", 0.5), 0.03, host.body)
baby = lib.Char("baby", skin="#f6d2b0", top="#9fd8ff", pants="#9fd8ff", hair="#e0b060", hair_style="flat", **K)
mic = empty("mic", (0, 0, -500))
cyl("micstick", (0, 0, 0.25), 0.07, 0.6, mat("micm", "#222222", 0.3), parent=mic, verts=8); sphere("michead", (0, 0, 0.6), (0.17, 0.17, 0.17), mat("michd", "#9a9aa8", 0.3, metal=0.8), mic, 10)
crowd = []
CC = [("#3f8fd8", "#6b3f22"), ("#e86fb0", "#1d1310"), ("#57b65a", "#e0c070"), ("#8b4fb0", "#6b3f22"), ("#e8823f", "#1d1310"),
      ("#2fb0a8", "#e0702e"), ("#c94a4a", "#3a2414"), ("#6a7ad8", "#eeeeee"), ("#f2c53d", "#3a2414"), ("#ff8fb0", "#1d1310"),
      ("#4ac0e8", "#3a2414"), ("#a0d040", "#1d1310")]
for i, (top, hair) in enumerate(CC):
    crowd.append(lib.Char(f"cr{i}", skin=["#f3c89a", "#c98d62", "#8d5a3b", "#e9b892"][i % 4], top=top, pants=["#3b3b55", "#c9b48a", "#2f4a7a"][i % 3],
                          hair=hair, hair_style="spiky" if i % 3 == 0 else "flat", kid=i % 2 == 0, **K))
for _o in CONF + SPARK + BILLS + ZZ + [ch for h in HEARTS for ch in h.children] + [p for _, _, ps in FW for p in ps]: _o.hide_render = True
fill = point("camfill", (0.6, 0.4, 0.2), "#ffe6cc", 160, 1.0, cam)
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
OFF = (0, 0, -500)
CAST = [hero, ben, pick, host, baby] + crowd
DOGS = [bis, dog2, dog3]

def day():
    bg.inputs["Color"].default_value = (*lib.srgb("#8fc8ff"), 1); bg.inputs["Strength"].default_value = 1.5
    sun.data.energy = 4.5; sun.data.color = lib.srgb("#fff0d8"); sun.rotation_euler = (math.radians(50), 0, math.radians(215))
    for l in STREETLAMPS: l.data.energy = 0
    for s in SPOTS: s.data.energy = 0
    sc.objects["stagefill"].data.energy = 0
    sc.view_settings.exposure = 0.3; fill.data.energy = 160
def night():
    bg.inputs["Color"].default_value = (*lib.srgb("#2a2470"), 1); bg.inputs["Strength"].default_value = 0.9
    sun.data.energy = 0.9; sun.data.color = lib.srgb("#9aa8ff"); sun.rotation_euler = (math.radians(55), 0, math.radians(200))
    for l in STREETLAMPS: l.data.energy = 1500
    for s in SPOTS: s.data.energy = 7000
    sc.objects["stagefill"].data.energy = 2500; sc.objects["ls_lamp"].data.energy = 400
    sc.view_settings.exposure = 0.55; fill.data.energy = 320
def scr(key, col="blue"):
    for k, o in TXT.items(): o.hide_render = (k != key)
    screen.data.materials[0] = scr_cols[col]
def scr_seq(seq):
    """[(frame, key), ...] switch screen text over time"""
    for f, key in seq:
        for k, o in TXT.items(): o.hide_render = (k != key); o.keyframe_insert("hide_render", frame=f)
def show(o, on=True):
    o.hide_render = not on
    for ch in o.children_recursive: ch.hide_render = not on

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
    for c in CAST: c.place(OFF); c.pose(); c.face("neutral")
    for d in DOGS: d.place(OFF); d.pose(); d.face("happy")
    screen.data.materials[0] = scr_cols["blue"]
    cam.data.lens = 28; cam.delta_location = (0, 0, 0)
    for k, o in TXT.items(): o.hide_render = True
    show(podium, False); show(stand, False)
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
def audience(face="happy", n=10, y0=9.5, x0=-8):
    for i, c in enumerate(crowd[:n]):
        x = x0 + (i % 5) * 4.0 + (1.6 if i // 5 else 0); y = y0 - (i // 5) * 2.6 + (i % 2) * 0.5
        c.place((x, y, 0.06), 180 - x * 2.5); c.face(face)
def confetti(f0, f1, cx=0, cy=20, spread=10, ztop=13):
    r = random.Random(3)
    for c in CONF:
        x, y = cx + r.uniform(-spread, spread), cy + r.uniform(-spread * 0.6, spread * 0.4); c.hide_render = False
        c.location = (x, y, ztop + r.uniform(0, 4)); c.rotation_euler = (r.uniform(0, 6), r.uniform(0, 6), 0); c.keyframe_insert("location", frame=f0); c.keyframe_insert("rotation_euler", frame=f0)
        c.location = (x + r.uniform(-2, 2), y + r.uniform(-1, 1), ztop - 13 + r.uniform(0.2, 5)); c.rotation_euler = (r.uniform(0, 30), r.uniform(0, 30), r.uniform(0, 6))
        c.keyframe_insert("location", frame=f1); c.keyframe_insert("rotation_euler", frame=f1)
def fireworks(f0, f1):
    r = random.Random(5)
    for b, (x, z, parts) in enumerate(FW):
        fb = f0 + b * 4
        for i, p in enumerate(parts):
            a = 2 * math.pi * i / len(parts); e = r.uniform(-1, 1); p.hide_render = False
            p.location = (x, 40, z); p.scale = (0.01, 0.01, 0.01); p.keyframe_insert("location", frame=fb); p.keyframe_insert("scale", frame=fb)
            p.scale = (0.35, 0.35, 0.35); p.keyframe_insert("scale", frame=fb + 4)
            p.location = (x + 6 * math.cos(a) * math.sqrt(1 - e * e), 40 + 2 * e, z + 6 * math.sin(a) * math.sqrt(1 - e * e) - 1.5)
            p.scale = (0.05, 0.05, 0.05); p.keyframe_insert("location", frame=min(f1, fb + 18)); p.keyframe_insert("scale", frame=min(f1, fb + 18))
def sparkle(f0, f1, c):
    for i, p in enumerate(SPARK):
        a = 2 * math.pi * i / len(SPARK); p.hide_render = False
        p.location = c; p.scale = (0.01,) * 3; p.keyframe_insert("location", frame=f0); p.keyframe_insert("scale", frame=f0)
        p.location = (c[0] + 0.9 * math.cos(a), c[1] - 0.2, c[2] + 0.9 * math.sin(a)); p.scale = (0.12, 0.12, 0.12)
        p.keyframe_insert("location", frame=f0 + 5); p.keyframe_insert("scale", frame=f0 + 5)
        p.scale = (0.01,) * 3; p.keyframe_insert("scale", frame=min(f1, f0 + 12))
def eyes(c, k, f=None):
    for e in c.eyes:
        e.scale = (e.scale[0] * k, e.scale[1], e.scale[2] * k)
        if f is not None: e.keyframe_insert("scale", frame=f)
def rise(objs, f0, f1, base, seed=1, h=3.0, spread=1.2):
    """things (hearts, bills, Zs) float up from base"""
    r = random.Random(seed)
    for i, o in enumerate(objs):
        show(o); d = f0 + i * 2
        x, y = base[0] + r.uniform(-spread, spread), base[1]
        o.location = (x, y, base[2]); o.scale = (0.2,) * 3; o.keyframe_insert("location", frame=d); o.keyframe_insert("scale", frame=d)
        o.location = (x + r.uniform(-0.4, 0.4), y, base[2] + h); o.scale = (1, 1, 1); o.keyframe_insert("location", frame=min(f1, d + 14)); o.keyframe_insert("scale", frame=min(f1, d + 6))
def throw_bills(f0, f1, src, dst, n=10, seed=2):
    r = random.Random(seed)
    for i, b in enumerate(BILLS[:n]):
        b.hide_render = False; d = f0 + (i * 2) % max(2, f1 - f0 - 6)
        b.location = (src[0] + r.uniform(-4, 4), src[1] + r.uniform(-1, 1), src[2]); b.rotation_euler = (0, 0, 0)
        b.keyframe_insert("location", frame=d); b.keyframe_insert("rotation_euler", frame=d)
        b.location = (dst[0] + r.uniform(-0.4, 0.4), dst[1] + r.uniform(-0.3, 0.3), dst[2]); b.rotation_euler = (r.uniform(0, 6), r.uniform(0, 6), r.uniform(0, 6))
        b.keyframe_insert("location", frame=d + 7); b.keyframe_insert("rotation_euler", frame=d + 7)
HERO_SQ = (0.0, 21.5, 0.06)
FX_ = 24.0   # x of the house used for the poster gags (house at x=24, y=13; fence at y=7.5)
def poster_on_fence(p, x, f=None):
    p.location = (x, 7.38, 1.35); p.rotation_euler = (0, 0, 0)
    if f is not None: p.keyframe_insert("location", frame=f)
def bis_stage(face="happy", x=0.0, y=25.0):
    bis.place((x, y, 1.4), 0); bis.sit(); bis.face(face)

# ---------------------------------------------------------------- shots
def s01(N):  # HOOK: sunny square, Biscuit (top hat + sash) sits on stage, screen MAYOR BISCUIT, crowd cheering, confetti
    scr("mayor", "pink"); bis_stage("tongue"); bis.wag(1, N); bis.pant(1, N)
    audience("happy", 10, 18.5)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    confetti(1, N + 10, 0, 23, 8)
    cam_move(cam, tgt, 1, N, (-0.6, 18.6, 4.2), (0.1, 19.7, 3.8), (0, 25, 3.2), (0, 25, 3.0), 32, 36)
def s02(N):  # Biscuit close, proud, hat, wagging: "is a dog"
    bis_stage("proud"); bis.wag(1, N, 40, 2); bis.sit(1, head=28); bis.sit(N, head=20, headtilt=12)
    confetti(-12, N, 0, 25, 4, 8)
    cam_move(cam, tgt, 1, N, (0.6, 20.6, 3.6), (0.4, 21.2, 3.5), (0, 24.6, 3.5), (0, 24.6, 3.5), 40, 46)
def s03(N):  # hero close, determined, holding his VOTE ME poster: "And in seven days..."
    hero.place(HERO_SQ, 0); hero.face("determined"); hero.pose(armL=-80, armR=-80)
    BIG_POSTER.parent = hero.body; BIG_POSTER.location = (0, -0.85, 1.85); BIG_POSTER.scale = (0.8, 0.8, 0.8)
    cam_move(cam, tgt, 1, N, (0.6, 17.2, 2.9), (0.3, 17.9, 2.9), (0, 21.5, 2.65), (0, 21.5, 2.7), 36, 42)
def s04(N):  # screen: ELECTION IN 7 DAYS; hero (back to us) vs Biscuit on the stage
    scr("days", "blue"); hero.place((0, 21.0, 0.06), 180); bis_stage("smug", 0, 24.6)
    cam_move(cam, tgt, 1, N, (-1.2, 16.0, 3.0), (-0.4, 17.2, 3.6), (0, 27, 4.6), (0, 27, 5.0), 26, 30)
def s05(N):  # Biscuit close: "His name is Biscuit" - head tilt, tongue
    bis_stage("tongue"); bis.wag(1, N); bis.sit(1, head=28, headtilt=-14); bis.sit(N, head=28, headtilt=10); bis.pant(1, N)
    cam_move(cam, tgt, 1, N, (-2.6, 21.4, 3.0), (-2.2, 21.9, 3.1), (0, 24.8, 3.4), (0, 24.8, 3.5), 40, 46)
def s06(N):  # screen 5 ELECTIONS 5 WINS, five gold trophies on the stage, Biscuit smug
    scr("wins", "gold"); bis_stage("smug", 0, 24.8); bis.wag(1, N, 25, 4)
    cam_move(cam, tgt, 1, N, (2.4, 17.5, 4.0), (1.6, 18.6, 4.4), (0, 27, 5.2), (0, 27, 5.0), 26, 28)
def s07(N):  # "He can't even read": Biscuit holding a newspaper upside down, head tilted
    bis_stage("surprised"); bis.sit(1, head=26, headtilt=-18); bis.sit(N, head=26, headtilt=18)
    paper.location = (0, 23.3, 2.45); paper.rotation_euler = (0, 0, 0)
    cam_move(cam, tgt, 1, N, (0.8, 19.4, 3.4), (0.5, 20.0, 3.4), (0, 23.6, 3.0), (0, 23.6, 3.0), 36, 40)
def s08(N):  # THE RULE: screen 1 VOTE = $1, the big vote jar on the stage
    scr("rule", "green"); jar.location = (-3.5, 24.8, 1.4); bis_stage("happy", 3.0, 24.8); bis.wag(1, N)
    cam_move(cam, tgt, 1, N, (-1.8, 17.5, 3.0), (-0.8, 18.6, 3.6), (-0.5, 27, 4.6), (-0.3, 27, 5.0), 26, 30)
def s09(N):  # "Vote as many times as you want": townsfolk throw dollar bills into the jar
    scr("vote", "green"); jar.location = (0, 24.6, 1.4)
    audience("happy", 10, 19.0, -8)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    throw_bills(1, N, (0, 19.5, 3.5), (0, 24.6, 3.6), 10)
    cam_move(cam, tgt, 1, N, (4.5, 15.0, 5.0), (3.5, 15.8, 4.6), (0, 23, 2.8), (0, 23, 3.0), 26, 28)
def s10(N):  # DAY 1: hero runs along the fences of Main Street sticking posters on every house
    xs = [FX_ - 24, FX_ - 12, FX_, FX_ + 12]
    hero.place((xs[0] - 3, 6.3, 0.24), -90, 1); hero.place((xs[-1] + 2, 6.3, 0.24), -90, N); hero.run(1, N, 5, 45, 12); hero.face("happy")
    for k, x in enumerate(xs):
        p = POSTERS[k + 1]; fa = max(1, int(1 + (N - 1) * (x - xs[0] + 3) / (xs[-1] - xs[0] + 5)))
        p.location = OFF; p.keyframe_insert("location", frame=1); p.keyframe_insert("location", frame=max(1, fa - 1)); poster_on_fence(p, x, fa)
    cam_move(cam, tgt, 1, N, (xs[0] - 2, 1.2, 2.2), (xs[-1] - 2, 1.2, 2.2), (xs[0] + 1, 7.0, 1.6), (xs[-1] + 1, 7.0, 1.6), 24, 24)
def s11(N):  # Biscuit pees on the poster (side view, back leg up, puddle grows)
    p = POSTERS[3]; poster_on_fence(p, FX_)
    bis.place((FX_ - 0.4, 6.0, 0.06), 90); bis.face("smug")
    fu = max(2, N // 4)
    bis.pose(1); bis.pose(fu, legs_y=(0, 0, 0, -70), headyaw=-35); bis.pose(N, legs_y=(0, 0, 0, -75), headyaw=-40)
    bis.wag(1, N, 25, 4)
    puddle.location = (FX_ + 0.55, 6.75, 0.08); puddle.scale = (0.01, 0.01, 1); puddle.keyframe_insert("scale", frame=fu)
    puddle.scale = (1.3, 1.0, 1); puddle.keyframe_insert("scale", frame=N)
    cam_move(cam, tgt, 1, N, (FX_ - 1.0, 1.0, 2.0), (FX_ - 0.6, 1.8, 1.9), (FX_, 7.0, 1.3), (FX_, 7.0, 1.3), 30, 34)
def s12(N):  # hero close, horrified, on the sidewalk
    hero.place((FX_ + 3.0, 5.6, 0.24), -30); hero.face("shock"); hero.pose(armL=-40, armR=-40, head=-8); eyes(hero, 1.0, 1); eyes(hero, 1.2, N)
    cam_move(cam, tgt, 1, N, (FX_ + 1.8, 2.0, 3.0), (FX_ + 2.1, 2.5, 3.0), (FX_ + 3.0, 5.6, 2.9), (FX_ + 3.0, 5.6, 3.0), 40, 44)
def s13(N):  # DAY 2: rally on the stage, hero with megaphone + pizza, screen FREE PIZZA FRIDAYS
    scr("pizza", "red"); hero.place((0, 25.0, 1.4), 0); hold(mega, hero, 1, (0, -0.45, -1.1)); hero.pose(armR=-95, armL=-120)
    pizza.parent = hero.arms[0]; pizza.location = (0, -0.3, -1.2); pizza.rotation_euler = (math.radians(80), 0, 0); hero.face("happy"); hero.talk(1, N, 0.14, 2)
    audience("happy", 10, 18.5)
    cam_move(cam, tgt, 1, N, (-2.0, 18.0, 3.2), (-1.0, 19.2, 3.4), (0, 25, 3.6), (0, 25, 3.8), 30, 34)
def s14(N):  # the crowd cheers (reverse angle from the stage)
    audience("happy", 10, 18.5)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    hero.place((0, 25.0, 1.4), 0); hold(mega, hero, 1, (0, -0.45, -1.1)); hero.pose(armR=-95)
    cam_move(cam, tgt, 1, N, (4.5, 26.5, 6.0), (3.5, 26.0, 5.6), (0, 17, 2.0), (-0.5, 17, 2.0), 24, 26)
def s15(N):  # Biscuit rolls over on the stage, belly up, legs in the air
    bis.place((2.6, 25.0, 1.4), -10); bis.face("tongue")
    fr = max(2, N // 4); f2 = max(fr + 2, N // 2)
    bis.pose(1); bis.pose(fr, rolly=60, rollz=1.25); bis.pose(f2, rolly=180, rollz=1.4, legs=(20, 20, -20, -20))
    bis.pose(N, rolly=180, rollz=1.4, legs=(-20, 30, 20, -30), headyaw=15)
    hero.place((-1.2, 25.4, 1.4), 20); hold(mega, hero, 1, (0, -0.45, -1.1)); hero.pose(armR=-60); hero.face("surprised")
    cam_move(cam, tgt, 1, N, (2.2, 20.0, 3.4), (1.8, 20.8, 3.2), (1.6, 25, 2.6), (1.8, 25, 2.5), 32, 36)
def s16(N):  # they cheer LOUDER: crowd wild, confetti, hero deadpan in front holding the pizza
    scr("mayor", "pink"); bis.place((2.6, 25.0, 1.4), -10); bis.pose(rolly=180, rollz=1.4, legs=(-20, 30, 20, -30)); bis.face("tongue")
    audience("happy", 10, 18.5)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 2, N, i)
    hero.place((-1.6, 24.4, 1.4), 0); hero.face("neutral"); hero.pose(armL=-70)
    pizza.parent = hero.arms[0]; pizza.location = (0, -0.3, -1.2); pizza.rotation_euler = (math.radians(80), 0, 0)
    confetti(1, N + 8, 0, 21, 9)
    cam_move(cam, tgt, 1, N, (-2.4, 18.4, 4.2), (-2.0, 19.4, 3.9), (-0.5, 24.5, 3.1), (-0.5, 24.5, 3.0), 30, 34); shake(1, 3, 0.08)
def s17(N):  # DAY 3: hero kisses a baby (a mum holds the baby out)
    mum = crowd[1]; mum.place((1.2, 18.0, 0.06), -20); mum.face("happy"); mum.pose(armL=-90, armR=-90)
    baby.root.scale = (0.48, 0.48, 0.48); baby.place((1.0, 17.0, 1.25), -20); baby.face("neutral"); baby.pose(armL=-40, armR=-40, legL=-60, legR=-60)
    hero.place((-0.7, 16.8, 0.06), 70, 1); hero.place((-0.25, 16.85, 0.06), 70, max(2, N // 2)); hero.face("happy"); hero.pose(1, lean=0); hero.pose(max(2, N // 2), lean=18, head=10)
    rise(HEARTS[:3], max(2, N // 2), N, (0.3, 16.6, 2.6), 3, 1.6, 0.5)
    cam_move(cam, tgt, 1, N, (0.6, 12.2, 2.6), (0.4, 12.8, 2.5), (0.3, 17.0, 2.2), (0.3, 17.0, 2.2), 34, 38)
def s18(N):  # Biscuit jumps up and licks the baby; baby giggles
    mum = crowd[1]; mum.place((1.2, 18.0, 0.06), -20); mum.face("surprised"); mum.pose(armL=-90, armR=-90)
    baby.root.scale = (0.48, 0.48, 0.48); baby.place((1.0, 17.0, 1.25), -20); baby.face("neutral", 1); baby.face("happy", max(2, N // 2)); baby.pose(armL=-150, armR=-150, armLs=20, armRs=20, legL=-60, legR=-60)
    bis.place((-0.3, 16.2, 0.06), -70); bis.pose(1, pitch=-10); bis.pose(max(2, N // 3), pitch=-48, rollz=1.5, legs=(-60, -70, -10, -10), head=-10); bis.face("tongue"); bis.wag(1, N, 45, 2)
    rise(HEARTS, max(2, N // 2), N, (1.0, 16.4, 2.4), 5, 1.8, 0.6)
    cam_move(cam, tgt, 1, N, (2.6, 12.4, 2.4), (2.2, 13.0, 2.4), (0.6, 16.8, 1.9), (0.6, 16.8, 2.0), 32, 36)
def s19(N):  # the baby's whole family waves dollar bills: vote Biscuit
    fam = crowd[1:5]
    for k, c in enumerate(fam):
        c.place((-3.6 + k * 2.4, 18.0 + (k % 2) * 0.4, 0.06), 0); cheer(c, 1 + k, N, k)
        b = BILLS[k]; b.hide_render = False; b.parent = c.arms[1]; b.location = (0, -0.35, -1.15); b.rotation_euler = (0, 0, 0)
    baby.root.scale = (0.48, 0.48, 0.48); baby.place((-1.0, 17.2, 1.3), 0); baby.face("happy"); baby.pose(armL=-150, armR=-150, armLs=20, armRs=20, legL=-60, legR=-60)
    cam_move(cam, tgt, 1, N, (0.2, 11.6, 3.0), (0.0, 12.6, 3.2), (-0.2, 18, 2.6), (-0.2, 18, 2.6), 28, 30)
def s20(N):  # DAY 4: Benny at the cookie stand, selling to a queue
    show(stand); ben.place((LX, LY + 1.3, 0.06), 0); ben.face("happy"); ben.talk(1, N, 0.14, 2)
    ben.pose(1, armR=-60); ben.pose(max(2, N // 2), armR=-100)
    for k, c in enumerate(crowd[6:9]):
        c.place((LX - 1.0 + k * 1.4, LY - 2.6 - k * 1.5, 0.06), 180 - 10 * k); c.face("happy")
    cam_move(cam, tgt, 1, N, (LX - 4.5, LY - 7.0, 2.8), (LX - 3.5, LY - 6.4, 2.8), (LX, LY, 2.4), (LX, LY, 2.6), 26, 28)
def s21(N):  # $300: a pile of dollar bills on the counter, Benny proud behind it
    show(stand); ben.place((LX, LY + 1.3, 0.06), 0); ben.face("happy"); ben.pose(armL=-100, armR=-100)
    cashpile.location = (LX, LY - 0.1, 2.32); cashpile.scale = (0.8, 0.8, 0.3); cashpile.keyframe_insert("scale", frame=1)
    cashpile.scale = (1, 1, 1); cashpile.keyframe_insert("scale", frame=N); sparkle(2, N, (LX, LY - 0.8, 2.8))
    cam_move(cam, tgt, 1, N, (LX + 0.6, LY - 4.2, 3.6), (LX + 0.4, LY - 3.6, 3.5), (LX, LY, 2.6), (LX, LY, 2.8), 34, 38)
def s22(N):  # "Three hundred votes!" hero + Benny jump on the stage, screen ME: 300
    scr("me300", "green"); hero.place((-1.2, 25.0, 1.4), 10); ben.place((1.2, 25.0, 1.4), -10)
    for c, sd in ((hero, 0), (ben, 1)):
        c.face("happy")
        for f in range(1 + sd, N + 1, 3): c.pose(f, armL=-165, armR=-165, armLs=20, armRs=20, bob=0.35 if ((f - sd) // 3) % 2 else 0)
    confetti(1, N + 8, 0, 24, 5, 10)
    cam_move(cam, tgt, 1, N, (0.4, 17.8, 3.6), (0.2, 18.8, 4.0), (0, 26, 4.2), (0, 26, 4.6), 28, 32)
def s23(N):  # DAY 5: the big screen VOTE BISCUIT ad comes on (night-ish evening light)
    scr("ad", "pink"); bis.place((5.5, 24.6, 1.4), -15); bis.sit(); bis.face("smug")
    hero.place((-3.0, 20.0, 0.06), 160); hero.face("surprised")
    cam_move(cam, tgt, 1, N, (-4.5, 15.5, 2.4), (-3.2, 16.5, 3.0), (0, 28, 5.4), (0, 28, 5.6), 24, 28)
def s24(N):  # THE AD: Biscuit asleep on a red cushion, Zzz, slow push-in (this frame also feeds the TV texture)
    cushion.location = (0, 24.8, 1.62); bis.place((0, 24.8, 1.55), 15); bis.pose(legs=(70, 70, -70, -70), rollz=0.6, head=15, headtilt=-15); bis.face("sleep")
    rise(ZZ, 1, N, (0.9, 23.6, 3.2), 2, 2.2, 0.3); bis.wag(1, N, 12, 8)
    for k, s in enumerate(SPOTS): s.data.energy = 2500 if k == 1 else 0
    cam_move(cam, tgt, 1, N, (1.2, 19.4, 3.4), (0.8, 20.6, 3.2), (0, 24.8, 2.3), (0, 24.8, 2.3), 34, 40)
def s25(N):  # "Everybody loved it": the town in front of the big screen showing the ad, hearts, two people crying with joy
    img = f"{W}/shots/s24/{max(1, NFR('s24') // 2):04d}.png"
    if not os.path.exists(img): img = f"{W}/stills/s24.png"
    if os.path.exists(img):
        _tex.image = bpy.data.images.load(img, check_existing=True)
        tvp.location = (0, 29.25, 6.0); scr("none" if False else "ad", "pink"); TXT["ad"].hide_render = True
    audience("happy", 10, 19.5)
    for i, c in enumerate(crowd[:10]): c.pose(armL=-120 if i % 2 else -20, armR=-20 if i % 2 else -120, head=-10)
    rise(HEARTS, 1, N, (0, 20.5, 3.5), 7, 3.5, 6)
    cam_move(cam, tgt, 1, N, (1.6, 16.6, 5.0), (1.0, 17.8, 5.0), (0, 27, 5.6), (0, 27, 5.8), 30, 32)
def s26(N):  # DAY 6: THE BIG DEBATE - night, neon, podiums ME vs BISCUIT, host in the middle with a mic
    night(); scr("debate", "purple"); show(podium)
    hero.place((-3.6, 25.8, 1.4), 0); hero.face("determined"); hero.pose(armL=-70, armR=-70)
    bis.place((3.6, 25.7, 2.72), 0); bis.sit(); bis.face("happy"); bis.wag(1, N)
    host.place((0, 26.2, 1.4), 0); hold(mic, host, 1); host.pose(armR=-100); host.face("happy"); host.talk(1, N // 2, 0.12, 3)
    audience("happy", 10, 18.5)
    cam_move(cam, tgt, 1, N, (0.0, 15.8, 4.8), (0.0, 17.4, 4.4), (0, 26, 3.8), (0, 26, 3.9), 24, 28)
def s27(N):  # hero close at his podium, talking fast, hands chopping the air; screen ROADS PARK SCHOOL ROOF
    night(); scr("plan", "blue"); show(podium); hero.place((-3.6, 25.8, 1.4), 15); hero.face("determined"); hero.talk(1, N, 0.13, 2)
    for f in range(1, N + 1, 4): hero.pose(f, armL=-90 if (f // 4) % 2 else -60, armR=-60 if (f // 4) % 2 else -100, head=-4)
    cam_move(cam, tgt, 1, N, (-2.3, 21.8, 3.9), (-2.6, 22.4, 3.9), (-3.6, 26, 3.7), (-3.4, 26, 3.8), 34, 38)
def s28(N):  # the audience: bored, one asleep - nobody cares about roads
    night(); audience("neutral", 10, 18.5)
    crowd[2].face("frozen"); crowd[3].pose(head=25); crowd[3].face("neutral")
    for e in crowd[3].eyes: e.scale = (e.scale[0], e.scale[1], e.scale[2] * 0.15)
    crowd[5].pose(head=-15, headyaw=40)
    cam_move(cam, tgt, 1, N, (-1.0, 25.5, 3.8), (0.0, 25.2, 3.7), (0, 16, 2.2), (0, 16, 2.2), 30, 32)
def s29(N):  # "Biscuit sat." close, perfect sit on his podium, wide innocent eyes
    night(); show(podium); bis.place((3.6, 25.7, 2.72), 0); bis.pose(1, rollz=0.95); bis.sit(max(2, N // 3)); bis.face("happy"); eyes(bis, 1.0, 1); eyes(bis, 1.15, N)
    bis.wag(1, N, 20, 3)
    cam_move(cam, tgt, 1, N, (3.0, 21.6, 4.6), (3.2, 22.2, 4.6), (3.6, 25.4, 4.3), (3.6, 25.4, 4.4), 40, 46)
def s30(N):  # he gives the host his paw - handshake
    night(); show(podium); bis.place((3.6, 25.7, 2.72), -25); bis.face("proud")
    fu = max(2, N // 3); bis.sit(1); bis.pose(fu, legs=(35, -110, -55, -55), pitch=-32, rollz=1.05, head=28)
    host.place((2.2, 24.6, 1.4), -60); host.face("surprised", 1); host.face("happy", fu + 2); host.pose(1, armR=-20); host.pose(fu, armR=-75); hold(mic, host, 0)
    cam_move(cam, tgt, 1, N, (5.6, 21.0, 3.8), (5.2, 21.6, 3.8), (3.0, 25.0, 3.4), (3.0, 25.0, 3.5), 34, 38)
def s31(N):  # STANDING OVATION: everyone up, confetti, hero facepalm at his podium
    night(); scr("mayor", "pink"); show(podium); audience("happy", 10, 18.5)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    hero.place((-3.6, 25.8, 1.4), 0); hero.face("neutral"); hero.pose(armR=-150, armRs=-35, head=12)
    bis.place((3.6, 25.7, 2.72), 0); bis.sit(); bis.face("proud"); bis.wag(1, N)
    confetti(1, N + 8, 0, 22, 9)
    cam_move(cam, tgt, 1, N, (-6.0, 15.0, 5.5), (-5.0, 16.0, 5.0), (0, 24, 3.2), (0, 24, 3.2), 22, 24); shake(1, 3, 0.08)
def s32(N):  # ELECTION NIGHT: wide night square, the town gathers, the jar glowing, screen ELECTION NIGHT
    night(); scr("night", "purple"); jar.location = (0, 24.6, 1.4)
    audience("neutral", 12, 18.0)
    cam_move(cam, tgt, 1, N, (-10.0, 4.0, 9.0), (-6.0, 7.0, 6.5), (0, 24, 4.0), (0, 24, 4.4), 22, 24)
def s33(N):  # the screen counting every dollar: 205-190 -> 288-301
    night(); scr("c1", "blue"); scr_seq([(1, "c1"), (max(2, N // 2), "c2")])
    cam_move(cam, tgt, 1, N, (-1.0, 20.8, 4.8), (-0.4, 22.0, 5.3), (0, 29.5, 6.0), (0, 29.5, 6.0), 30, 34)
def s34(N):  # ME 312 - BISCUIT 312
    night(); scr("c3", "blue")
    cam_move(cam, tgt, 1, N, (0.4, 22.4, 5.6), (0.2, 23.0, 5.8), (0, 29.5, 6.0), (0, 29.5, 6.0), 34, 38)
def s35(N):  # hero close, sweating, eyes darting
    night(); hero.place(HERO_SQ, 0); hero.face("scared"); hero.pose(1, headyaw=-15); hero.pose(max(2, N // 2), headyaw=15); hero.pose(N, headyaw=0)
    cam_move(cam, tgt, 1, N, (0.3, 18.0, 2.75), (0.2, 18.5, 2.75), (0, 21.5, 2.7), (0, 21.5, 2.75), 42, 46)
def s36(N):  # TIE! red screen, the crowd gasps (wide, shake)
    night(); scr("tie", "red"); audience("shock", 12, 18.0)
    for c in crowd[:12]: c.pose(armL=-150, armR=-150, armLs=10, armRs=10)
    hero.place((0, 20.4, 0.06), 180); hero.face("shock")
    cam_move(cam, tgt, 1, N, (4.0, 11.0, 4.0), (3.0, 12.5, 4.4), (0, 26, 4.2), (0, 26, 4.5), 22, 26); shake(1, 4, 0.12)
def s37(N):  # Mrs. Pickles walks out of the crowd towards the jar
    night(); jar.location = (0, 24.6, 1.4); audience("surprised", 10, 17.0)
    pick.place((4.0, 18.6, 0.06), 130, 1); pick.place((1.4, 22.0, 0.06), 160, N); pick.walk(1, N, 8); pick.face("evil")
    hold(purse, pick, 0, (0, -0.25, -1.1))
    cam_move(cam, tgt, 1, N, (7.5, 19.0, 3.6), (6.5, 19.8, 3.6), (2.5, 21, 2.4), (1.6, 22, 2.6), 26, 28)
def s38(N):  # purse close: she opens it, takes out ONE dollar
    night(); pick.place((1.4, 22.0, 0.06), 180); pick.face("evil"); pick.pose(armL=-80, armR=-80)
    purse.location = (1.4, 21.0, 2.75); purse.rotation_euler = (0, 0, math.radians(180))
    bill.location = (1.4, 20.95, 2.95); bill.keyframe_insert("location", frame=max(1, N // 3)); bill.location = (1.4, 20.85, 3.5); bill.keyframe_insert("location", frame=N)
    bill.rotation_euler = (0, 0, 0)
    cam_move(cam, tgt, 1, N, (2.1, 18.6, 3.2), (1.9, 19.1, 3.2), (1.4, 21.0, 2.95), (1.4, 21.0, 3.15), 42, 46)
def s39(N):  # "For Biscuit." - the dollar drops into the jar, Biscuit wags on the stage behind
    night(); jar.location = (0, 24.6, 1.4); pick.place((1.6, 23.2, 1.4), 110); pick.face("evil"); pick.pose(armR=-110)
    bill.location = (0.6, 23.8, 4.0); bill.keyframe_insert("location", frame=1); bill.location = (0, 24.6, 3.3); bill.keyframe_insert("location", frame=max(2, N // 2))
    bill.rotation_euler = (0, 0, 0); bill.keyframe_insert("rotation_euler", frame=1); bill.rotation_euler = (0.4, 2.0, 1.0); bill.keyframe_insert("rotation_euler", frame=max(2, N // 2))
    bis.place((-2.8, 25.6, 1.4), 15); bis.sit(); bis.face("tongue"); bis.wag(1, N, 45, 2)
    cam_move(cam, tgt, 1, N, (2.6, 18.6, 4.2), (2.0, 19.4, 4.0), (-0.8, 25, 3.0), (-0.8, 25, 3.0), 28, 30)
def s40(N):  # BISCUIT WINS! gold screen, fireworks, Biscuit on the stage, crowd up
    night(); scr_seq([(1, "c4"), (max(2, N // 3), "win")]); screen.data.materials[0] = scr_cols["gold"]
    bis_stage("proud", 0, 24.8); bis.wag(1, N, 45, 2)
    audience("happy", 10, 18.5)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    fireworks(1, N + 10); confetti(1, N + 8, 0, 23, 8)
    cam_move(cam, tgt, 1, N, (0.5, 16.5, 4.2), (0.2, 17.5, 4.0), (0, 26, 4.4), (0, 26, 4.4), 24, 26)
def s41(N):  # "Again." hero close, deadpan disbelief, confetti falling on him
    night(); hero.place(HERO_SQ, 0); hero.face("neutral"); hero.pose(); confetti(-8, N, 0, 21.5, 2.5, 6)
    cam_move(cam, tgt, 1, N, (0.2, 18.2, 2.8), (0.15, 18.5, 2.8), (0, 21.5, 2.75), (0, 21.5, 2.75), 46, 50)
def s42(N):  # "But the screen said": $625 RAISED (green)
    night(); scr("raised", "green"); hero.place((0, 21.0, 0.06), 180)
    cam_move(cam, tgt, 1, N, (-1.4, 17.5, 3.0), (-0.6, 18.8, 3.8), (0, 29, 5.6), (0, 29, 5.8), 28, 32)
def s43(N):  # the school with its shiny new roof and NEW ROOF banner (sunny next morning), kids cheering
    hero.place((SX - 1.5, SY - 7.5, 0.06), 160); ben.place((SX + 1.8, SY - 7.8, 0.06), 200)
    for k, c in enumerate(crowd[:4]): c.place((SX - 5 + k * 3.3, SY - 9.5 - (k % 2), 0.06), 180); cheer(c, 1 + k, N, k)
    cam_move(cam, tgt, 1, N, (SX + 7, SY - 22, 2.0), (SX + 5, SY - 20, 3.0), (SX, SY, 4.5), (SX, SY, 5.6), 22, 24)
def s44(N):  # "My promise came true": hero close, proud smile in front of the school
    hero.place((SX - 1.5, SY - 7.5, 0.06), -10); hero.face("neutral", 1); hero.face("happy", max(2, N // 3)); hero.pose(1); hero.pose(N, head=-6)
    cam_move(cam, tgt, 1, N, (SX - 1.0, SY - 11.6, 2.8), (SX - 1.2, SY - 11.0, 2.8), (SX - 1.5, SY - 7.5, 2.75), (SX - 1.5, SY - 7.5, 2.85), 38, 42)
def s45(N):  # "I just wasn't the Mayor": Biscuit (hat, sash) snaps the ribbon with his teeth, ribbon halves fall
    bis.place((SX, SY - 5.9, 0.06), 0); bis.face("proud"); bis.wag(1, N, 40, 2)
    fs = max(2, N // 3); bis.pose(1, head=-6); bis.pose(fs, head=10)
    for k, (r, sd) in enumerate(zip(RIB, (-1, 1))):
        r.keyframe_insert("location", frame=fs); r.keyframe_insert("rotation_euler", frame=fs)
        r.location = (SX + 1.3 * sd, SY - 5.2, 1.0); r.rotation_euler = (0, math.radians(-55 * sd), 0)
        r.keyframe_insert("location", frame=min(N, fs + 6)); r.keyframe_insert("rotation_euler", frame=min(N, fs + 6))
    hero.place((SX - 3.4, SY - 7.2, 0.06), -30); hero.face("neutral"); ben.place((SX + 3.2, SY - 7.4, 0.06), 30); cheer(ben, 1, N, 1)
    confetti(fs, N + 8, SX, SY - 6, 4, 9)
    cam_move(cam, tgt, 1, N, (SX + 1.2, SY - 13.5, 2.4), (SX + 0.8, SY - 12.6, 2.4), (SX, SY - 5.5, 1.7), (SX, SY - 5.5, 1.8), 30, 32)
def s46(N):  # "And yes, this part is real": hero points at the screen THIS PART IS REAL (day)
    scr("real", "blue"); hero.place((-2.2, 21.5, 0.06), 30); hero.face("happy"); hero.pose(armR=-150, armRs=-20, headyaw=0)
    cam_move(cam, tgt, 1, N, (-4.0, 16.0, 3.0), (-3.0, 17.0, 3.6), (0, 27, 4.8), (0, 27, 5.0), 26, 30)
def s47(N):  # three dog mayors in top hats sit in a row on the stage: DOG MAYORS SINCE 1998
    scr("since", "gold")
    for d, x in ((dog2, -3.4), (bis, 0.0), (dog3, 3.4)):
        d.place((x, 25.0, 1.4), 0); d.sit(); d.face("proud"); d.wag(1, N, 35, 2 + (x > 0))
    cam_move(cam, tgt, 1, N, (-2.0, 17.0, 3.4), (0.0, 18.0, 3.6), (0, 26, 4.0), (0, 26, 4.2), 26, 28)
def s48(N):  # "One dollar a vote": a hand drops a dollar in the jar, close
    jar.location = (0, 24.6, 1.4)
    bill.location = (0.3, 23.8, 4.4); bill.keyframe_insert("location", frame=1); bill.location = (0, 24.6, 3.3); bill.keyframe_insert("location", frame=max(2, N // 2))
    bill.rotation_euler = (0, 0, 0); bill.keyframe_insert("rotation_euler", frame=1); bill.rotation_euler = (0.3, 1.6, 0.8); bill.keyframe_insert("rotation_euler", frame=max(2, N // 2))
    sparkle(max(2, N // 2), N, (0, 24.0, 3.5))
    cam_move(cam, tgt, 1, N, (1.6, 18.6, 4.2), (1.2, 19.4, 4.2), (0, 24.6, 3.0), (0, 24.6, 3.1), 32, 34)
def s49(N):  # "Biscuit's first job as Mayor?" Biscuit trots down Main Street in his sash and hat
    poster_on_fence(POSTERS[3], FX_)
    bis.place((FX_ - 9, 5.8, 0.06), -90, 1); bis.place((FX_ - 1.0, 5.8, 0.06), -90, N); bis.trot(1, N, 5, 35); bis.face("proud"); bis.wag(1, N, 35, 2)
    cam_move(cam, tgt, 1, N, (FX_ + 2.0, 0.4, 1.6), (FX_ + 1.5, 1.0, 1.7), (FX_ - 6, 6.0, 1.4), (FX_ - 1.5, 6.0, 1.5), 26, 28)
def s50(N):  # "He peed on my poster. Again." leg up on the VOTE ME poster, hero deadpan beside it; pull back
    poster_on_fence(POSTERS[3], FX_)
    bis.place((FX_ - 0.4, 6.0, 0.06), 90); bis.face("smug"); fu = max(2, N // 5)
    bis.pose(1); bis.pose(fu, legs_y=(0, 0, 0, -70), headyaw=-35); bis.pose(N, legs_y=(0, 0, 0, -75), headyaw=-35); bis.wag(1, N, 25, 4)
    puddle.location = (FX_ + 0.55, 6.75, 0.08); puddle.scale = (0.01, 0.01, 1); puddle.keyframe_insert("scale", frame=fu)
    puddle.scale = (1.3, 1.0, 1); puddle.keyframe_insert("scale", frame=N)
    hero.place((FX_ + 2.6, 5.4, 0.24), -20); hero.face("neutral"); hero.pose(armL=-10, armR=-10)
    cam_move(cam, tgt, 1, N, (FX_ + 0.8, 2.2, 2.4), (FX_ + 0.8, -0.6, 2.9), (FX_ + 1.0, 6.6, 1.8), (FX_ + 1.0, 6.6, 2.0), 32, 28)
def s51(N):  # END: golden-hour crane up over Main Street to the clock tower (A/B candles overlay in post)
    poster_on_fence(POSTERS[3], FX_); bis.place((FX_ - 0.4, 6.0, 0.06), 90); bis.face("smug"); bis.pose(legs_y=(0, 0, 0, -70))
    hero.place((FX_ + 2.6, 5.4, 0.24), -20); hero.face("neutral")
    sun.data.color = lib.srgb("#ffc890"); sun.rotation_euler = (math.radians(72), 0, math.radians(235)); bg.inputs["Color"].default_value = (*lib.srgb("#ffb98a"), 1)
    cam_move(cam, tgt, 1, N, (FX_ + 1, -2.0, 3.0), (FX_ - 4, -10.0, 11.0), (FX_ + 1, 6.5, 1.8), (6, 30, 10.0), 28, 24)

def NFR(sid):
    for s, t0, t1, _ in TIMES:
        if s == sid: return max(2, round((t1 - t0) * FPS))
    return 2
T = [("s01", 0.0, s01), ("s02", wt(0, 5), s02), ("s03", wt(0, 8), s03), ("s04", wt(0, 13), s04),
     ("s05", L[1], s05), ("s06", wt(1, 4), s06), ("s07", wt(1, 11), s07),
     ("s08", L[2], s08), ("s09", wt(2, 7), s09),
     ("s10", L[3], s10), ("s11", wt(3, 11), s11), ("s12", wt(3, 14), s12),
     ("s13", L[4], s13), ("s14", wt(4, 8), s14), ("s15", wt(4, 11), s15), ("s16", wt(4, 15), s16),
     ("s17", L[5], s17), ("s18", wt(5, 6), s18), ("s19", wt(5, 10), s19),
     ("s20", L[6], s20), ("s21", wt(6, 9), s21), ("s22", wt(6, 12), s22),
     ("s23", L[7], s23), ("s24", wt(7, 6), s24), ("s25", wt(7, 11), s25),
     ("s26", L[8], s26), ("s27", wt(8, 5), s27), ("s28", wt(8, 13), s28),
     ("s29", L[9], s29), ("s30", wt(9, 2), s30), ("s31", wt(9, 9), s31),
     ("s32", L[10], s32), ("s33", wt(10, 8), s33),
     ("s34", L[11], s34), ("s35", wt(11, 5), s35), ("s36", wt(11, 10), s36),
     ("s37", L[12], s37), ("s38", wt(12, 4), s38), ("s39", wt(12, 9), s39),
     ("s40", L[13], s40), ("s41", wt(13, 2), s41),
     ("s42", L[14], s42), ("s43", wt(14, 8), s43), ("s44", wt(14, 15), s44), ("s45", wt(14, 19), s45),
     ("s46", L[15], s46), ("s47", wt(15, 6), s47), ("s48", wt(15, 15), s48),
     ("s49", L[16], s49), ("s50", wt(16, 5), s50), ("s51", L[17], s51)]
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
