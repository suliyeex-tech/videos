"""Oddwick daily Short 2026-11-24: "Every Door in This House Is a Lie" (Blocktown house style, owner 2026-11-20).
Mystery-place-to-escape shape: the Mayor locks the hero in the town's Lying House, 1 hour, $5,000 or a year of mowing his lawn.
Stairs into the ceiling, a red door onto a brick wall, window behind window (Benny squished on the glass), a 2nd-floor door into
the kitchen sink, a shoebox door into a broom closet, the town watches the countdown on the big screen (Mrs. Pickles' popcorn),
the door that says NOT AN EXIT is the way out (3 s left), the mailman lost for 3 years walks out behind him (beard), real fact
(Winchester Mystery House, San Jose CA: stairs to the ceiling, doors onto walls, built for 38 years), callback twist: the golden
envelope holds... another envelope.
python3.13 doorlie_shots.py [sid ...] [--still]   -> /home/claude/work/<slug>/shots/<sid>/####.png (resumable)
Sets: town square x=0 (crazy house at HX,HY), corridor x=300, stairs x=400, windows x=500, kitchen x=600, broom closet x=700."""
import sys, os, json, math, random, time, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move

SLUG = "2026-11-24-every-door-in-this-house-lies"; FPS = 12
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
for _o in list(bpy.data.objects):   # clear the street houses/trees/lamps that would sit in front of the Lying House on the square
    if (_re.match(r'^(hw|hsid|hrf|hwin|hwf|hdoor|hstep|pk|pkr)(-?12)(_|$)', _o.name) or _re.match(r'^(trunk|leaf)(-6|6|18)_9\.5', _o.name)
            or _o.name in ("lpole0", "larm0", "lbulb0", "lamp0_6.8", "lpole16", "larm16", "lbulb16", "lamp16_6.8")):
        bpy.data.objects.remove(_o, do_unlink=True)
FONT = None
for fp in ("/root/.fonts/Fredoka-Bold.ttf", "/home/claude/work/fonts/Fredoka-Bold.ttf"):
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

def brickmat(name="bricks", c1="#b5523b", c2="#93402f", scale=3.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexBrick"); tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); cb = nt.nodes.new("ShaderNodeCombineXYZ"); ad = nt.nodes.new("ShaderNodeMath")
    nt.links.new(tc.outputs["Object"], sp.inputs[0]); nt.links.new(sp.outputs[0], ad.inputs[0]); nt.links.new(sp.outputs[1], ad.inputs[1])
    nt.links.new(ad.outputs[0], cb.inputs[0]); nt.links.new(sp.outputs[2], cb.inputs[1]); nt.links.new(cb.outputs[0], t.inputs["Vector"])
    t.inputs["Color1"].default_value = (*lib.srgb(c1), 1); t.inputs["Color2"].default_value = (*lib.srgb(c2), 1)
    t.inputs["Mortar"].default_value = (*lib.srgb("#e8dfcf"), 1); t.inputs["Scale"].default_value = scale
    t.inputs["Mortar Size"].default_value = 0.03
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.85
    return m
BRICK = brickmat()
GLASS = bpy.data.materials.new("glass"); GLASS.use_nodes = True
_gb = GLASS.node_tree.nodes["Principled BSDF"]; _gb.inputs["Base Color"].default_value = (0.85, 0.95, 1, 1)
_gb.inputs["Roughness"].default_value = 0.03; _gb.inputs["Transmission Weight"].default_value = 1.0; _gb.inputs["IOR"].default_value = 1.2

# ---------------------------------------------------------------- town square: stage + big screen (countdown show)
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
TXT = {}
for key, body, size, col in (("house", "THE LYING\nHOUSE", 1.5, "#ffe14a"), ("hour", "60:00", 3.0, "#ffffff"),
                             ("nobody", "ESCAPED:\n0", 1.7, "#ffffff"), ("prize", "$5,000", 2.6, "#ffe14a"),
                             ("ten", "10:00\nLEFT", 2.0, "#ffffff"), ("five", "5:00", 3.0, "#ffffff"),
                             ("three", "0:03", 3.0, "#ffffff"), ("won", "ESCAPED!", 1.8, "#ffffff"),
                             ("real", "THIS PART\nIS REAL", 1.4, "#ffffff"), ("years", "BUILT FOR\n38 YEARS", 1.3, "#ffffff")):
    TXT[key] = mktext("scr_" + key, body, (0, 29.36, 6.0), size, col, 4.0, extrude=0.01)
for i in range(16):
    x = -12 + i * 1.6
    cube(f"bunt{i}", (x, 21.5, 9.6 - 0.9 * math.sin(math.pi * i / 15)), (0.9, 0.05, 0.9), mat(f"bunt{i % 3}", ["#e8423f", "#ffffff", "#2f63d6"][i % 3], 0.6, 0.4), 0, None, (0, R(45), 0))
CONF = []
rr = random.Random(7); ccols = ["#ff4fd0", "#40f0ff", "#ffe14a", "#5fff7a", "#ff7a3a", "#ffffff"]
for i in range(90): CONF.append(cube(f"conf{i}", (0, 0, -500), (0.22, 0.04, 0.32), mat(f"conf{i % 6}", ccols[i % 6], 0.5, 1.5), 0))
FW = []
for b, (x, z, col) in enumerate(((-9, 24, "#ff4fd0"), (0, 30, "#ffe14a"), (9, 25, "#40f0ff"))):
    FW.append((x, z, [sphere(f"fw{b}_{i}", (0, 0, -500), (0.25, 0.25, 0.25), mat(f"fwm{b}", col, 0.3, 30, col), seg=6) for i in range(26)]))
SPARK = [sphere(f"spark{i}", (0, 0, -500), (0.1, 0.1, 0.1), mat("sparkm", "#fff6a0", 0.3, 20, "#fff2a0"), seg=6) for i in range(8)]

# ---------------------------------------------------------------- door kit
TRIM = mat("trim", "#f4f1e8", 0.5)
def door(name, loc, yaw, col, w=1.6, h=3.0, knob=True, frame=TRIM):
    """door facing -y (local). returns (root, hinge). open: hinge.rotation_euler.z -> -100 deg (swings toward the viewer)"""
    root = empty(name, loc); root.rotation_euler = (0, 0, R(yaw))
    for sd in (-1, 1): cube(f"{name}_post{sd}", (sd * (w / 2 + 0.12), -0.02, h / 2), (0.24, 0.32, h + 0.1), frame, 0.03, root)
    cube(f"{name}_lintel", (0, -0.02, h + 0.12), (w + 0.48, 0.32, 0.24), frame, 0.03, root)
    hinge = empty(f"{name}_hinge", (-w / 2, -0.05, 0), root)
    cube(f"{name}_panel", (w / 2, 0, h / 2), (w - 0.04, 0.12, h - 0.04), mat(f"door_{col}", col, 0.45), 0.03, hinge)
    for k in range(2): cube(f"{name}_inset{k}", (w / 2, -0.07, h * (0.3 + 0.42 * k)), (w * 0.62, 0.03, h * 0.3), mat(f"doori_{col}", col, 0.35), 0.03, hinge)
    if knob: sphere(f"{name}_knob", (w - 0.22, -0.14, h * 0.48), (0.11, 0.11, 0.11), mat("gold", "#e2b23a", 0.25, metal=1.0), hinge, 10)
    return root, hinge
def open_door(hinge, f0, f1, ang=-100):
    hinge.rotation_euler = (0, 0, 0); hinge.keyframe_insert("rotation_euler", frame=f0)
    hinge.rotation_euler = (0, 0, R(ang)); hinge.keyframe_insert("rotation_euler", frame=f1)

# ---------------------------------------------------------------- the Lying House on the square
HX, HY = 13.5, 23.0; HF = HY - 4.0     # front face y
hp = mat("hpurple", "#8a5fd0", 0.6); ht = mat("hteal", "#3fb8a8", 0.6); hr_ = mat("hroof", "#d8423f", 0.7)
cube("lh_body", (HX, HY, 4.5), (8, 8, 9), hp, 0.1)
up = cube("lh_up", (HX + 0.3, HY + 0.3, 11.6), (7, 7, 5.4), ht, 0.1, rot=(0, R(5), 0))
for i in range(4): cube(f"lh_roof{i}", (HX + 0.9 - i * 0.05, HY + 0.3, 14.6 + i * 0.6), (7.6 - i * 1.7, 7.6, 0.6), hr_, 0.05, rot=(0, R(8), 0))
cube("lh_chim", (HX + 2.6, HY + 1, 17.6), (1, 1, 2.6), BRICK, 0.05, rot=(0, R(-14), 0))
WIN = mat("winlit", "#ffd27a", 0.4, 6.0, "#ffbf5e")
for k, (x, z, w, h) in enumerate(((-2.6, 6.2, 1.2, 1.4), (2.7, 3.2, 0.7, 2.2), (2.4, 7.0, 1.8, 0.8), (-2.3, 2.6, 0.9, 0.9),
                                   (-1.6, 11.2, 1.3, 1.3), (2.0, 12.6, 0.8, 1.6))):
    cube(f"lh_win{k}", (HX + x, HF - 0.03, z), (w, 0.1, h), WIN, 0.02); cube(f"lh_winf{k}", (HX + x, HF - 0.01, z), (w + 0.3, 0.06, h + 0.3), TRIM, 0.02)
cube("lh_glow", (HX, HF - 0.02, 1.5), (1.55, 0.02, 2.95), mat("glowin", "#ffd27a", 0.5, 3.0, "#ffbf5e"), 0)
LH_FRONT, LH_FRONT_H = door("lh_front", (HX, HF - 0.06, 0.06), 0, "#d8423f", 1.6, 3.0)
door("lh_d2", (HX + 0.2, HF - 0.06, 5.0), 0, "#3fae4a", 1.3, 2.4)          # 2nd-floor door, no stairs
door("lh_d3", (HX - 3.1, HF - 0.06, 0.06), 0, "#2f63d6", 0.55, 0.8)        # tiny door
_sd, _ = door("lh_d4", (HX - 0.5, HF + 0.3 - 3.5 - 0.06, 10.4), 0, "#ffb020", 1.2, 2.2); _sd.rotation_euler = (0, R(90), 0)  # sideways door
door("lh_d5", (HX + 2.6, HF - 0.06, 9.6), 0, "#ff4fd0", 0.9, 1.6)
mktext("lh_sign", "THE LYING HOUSE", (HX, HF - 0.12, 3.75), 0.55, "#ffe14a", 2.0, extrude=0.03)
cube("lh_path", (HX, HF - 3.2, 0.06), (2.2, 6, 0.04), mat("path", "#e8d9b8", 0.8), 0)
# mailbox stuffed with 3 years of letters
mbox = empty("mbox", (HX - 3.8, HF - 3.0, 0))
cyl("mb_post", (0, 0, 0.8), 0.1, 1.6, mat("pole", "#2b2d36", 0.4, metal=0.6), parent=mbox, verts=8)
cube("mb_box", (0, 0, 1.85), (0.7, 1.1, 0.65), mat("mbm", "#2f63d6", 0.4), 0.15, mbox)
LETTERS = []
rl = random.Random(11)
for i in range(14):
    LETTERS.append(cube(f"mb_l{i}", (rl.uniform(-0.5, 0.5), -0.6 - rl.uniform(0, 0.4), rl.uniform(0.2, 2.6)), (0.5, 0.03, 0.34), mat("letterw", "#f6f3ea", 0.6), 0.01, mbox,
                        (rl.uniform(-0.8, 0.8), rl.uniform(-0.8, 0.8), rl.uniform(-1, 1))))
# the door of light (behind the house front door, used for the exit shot)
# ---------------------------------------------------------------- corridor x=300 (yellow office-style corridor, many doors)
CX = 300
YW = mat("ywall", "#f2d34a", 0.75); YF = mat("yfloor", "#c99a4a", 0.6); YC = mat("yceil", "#fff3c0", 0.8)
cube("co_floor", (CX, 20, -0.05), (8.6, 44, 0.1), YF, 0)
for k in range(22): cube(f"co_tile{k}", (CX, k * 2.0, 0.005), (8.6, 0.06, 0.01), mat("tileline", "#a37a36", 0.6), 0)
cube("co_ceil", (CX, 20, 7.05), (8.6, 44, 0.1), YC, 0)
for sd in (-1, 1):
    cube(f"co_wall{sd}", (CX + sd * 4.15, 20, 3.5), (0.3, 44, 7), YW, 0)
    cube(f"co_wain{sd}", (CX + sd * 3.98, 20, 0.6), (0.06, 44, 1.2), mat("wain", "#e0a22a", 0.6), 0)
cube("co_end", (CX, 40.1, 3.5), (8.6, 0.3, 7), YW, 0); cube("co_back", (CX, -2.1, 3.5), (8.6, 0.3, 7), YW, 0)
for k in range(7):
    cube(f"co_lamp{k}", (CX, 2 + k * 6, 6.97), (1.8, 0.8, 0.06), mat("panel", "#fffbe8", 0.3, 12, "#fff6d8"), 0)
    point(f"co_pl{k}", (CX, 2 + k * 6, 6.2), "#fff0cc", 260, 1.2)
CDOORS = {}
rd = random.Random(3); dcols = ["#2f63d6", "#3fae4a", "#8a3fb0", "#e8823f", "#d8423f", "#2fb0a8", "#ff4fd0"]
for k in range(12):
    sd = -1 if k % 2 == 0 else 1; y = 4 + (k // 2) * 5.5 + (1.2 if sd > 0 else 0)
    CDOORS[k] = door(f"cd{k}", (CX + sd * 3.98, y, 0.0), -90 * sd if sd > 0 else 90, dcols[k % 7], 1.5, 3.0)
    # brick wall right behind every corridor door (seen when one opens)
    cube(f"cdb{k}", (CX + sd * 4.0, y, 1.5), (0.04, 1.5, 3.0), BRICK, 0)
TINY, TINY_H = door("tiny", (CX + 3.97, 14.0, 0.0), -90, "#ff4fd0", 0.55, 0.75)
RED_D, RED_H = door("reddoor", (CX, 39.9, 0.0), 0, "#c8282f", 2.0, 3.6)
cube("redbrick", (CX, 39.96, 1.8), (2.0, 0.04, 3.6), BRICK, 0)
# the NOT AN EXIT door: separate end wall at y=30 inside a short cul-de-sac (we move it in when needed)
NX = empty("nx", (0, 0, -500))
for _k, (_x, _z, _sx, _sz) in enumerate(((-2.5, 3.5, 3.4, 7), (2.5, 3.5, 3.4, 7), (0, 5.05, 1.6, 3.9))):
    cube(f"nx_wall{_k}", (_x, 0.2, _z), (_sx, 0.3, _sz), YW, 0, NX)
nxd, NXH = door("nxdoor", (0, 0, 0), 0, "#9a9aa8", 1.4, 2.8); nxd.parent = NX
sign = empty("nxsign", (0.7, -0.22, 2.0), NXH)
cube("nx_signb", (0, 0, 0), (1.05, 0.04, 0.5), mat("signw", "#ffffff", 0.4, 0.5), 0.02, sign)
st_ = mktext("nx_signt", "NOT AN\nEXIT", (0, -0.03, 0), 0.17, "#c8282f", 0.4, extrude=0.005, parent=sign)
LIGHTPLANE = cube("nx_light", (0, 0.45, 1.4), (1.8, 0.05, 3.2), mat("sunwhite", "#ffffff", 0.2, 40, "#fff6d0"), 0, NX)
NXL = point("nx_lamp", (0, -0.6, 1.6), "#fff2c0", 0, 1.0, NX)
NXLIGHT_E = 0
# ---------------------------------------------------------------- stairs x=400 (stairs straight into the ceiling)
SX = 400
cube("st_floor", (SX, 0, -0.05), (24, 10, 0.1), YF, 0)
cube("st_back", (SX, 2.6, 4.5), (24, 0.3, 9), mat("stwall", "#ffd86a", 0.75), 0)
cube("st_ceil", (SX, 0, 7.2), (24, 10, 0.4), YC, 0)
STEPS = []
for i in range(14):
    h_ = 0.55 * (i + 1)
    STEPS.append(cube(f"st_s{i}", (SX - 6 + i * 0.95, 1.0, h_ / 2), (0.95, 2.6, h_), mat("stepw", "#b87a3a", 0.6), 0.03))
cube("st_rail", (SX - 0.0, -0.3, 4.9), (13.6, 0.12, 0.12), mat("rail", "#7a4a22", 0.5), 0.02, rot=(0, R(-30), 0))
for k in range(3): point(f"st_pl{k}", (SX - 5 + k * 5, -2, 6.4), "#fff0cc", 500, 1.5)
cube("st_lampp", (SX, 0, 6.98), (2, 1, 0.06), mat("panel", "#fffbe8", 0.3, 12, "#fff6d8"), 0)
def step_top(x):   # z of the stair top under x
    i = max(0, min(13, int((x - (SX - 6) + 0.475) / 0.95))); return 0.55 + i * 0.55
# ---------------------------------------------------------------- windows x=500 (window behind a window behind a window)
WX = 500
cube("wi_floor", (WX, -3, -0.05), (12, 8, 0.1), mat("wfloor", "#7a5a3a", 0.6), 0)
WSASH = []
for k, (y, col) in enumerate(((0.0, "#8fc3e8"), (0.75, "#a4d48a"), (1.5, "#f2b0c8"))):
    for part, (px, pz, sx, sz) in enumerate(((-3.9, 3.5, 5.0, 7), (3.9, 3.5, 5.0, 7), (0, 1.25, 2.8, 2.5), (0, 6.25, 2.8, 1.5))):
        cube(f"wi_w{k}_{part}", (WX + px, y, pz), (sx, 0.3, sz), mat(f"wiw{k}", col, 0.7), 0)
    for part, (px, pz, sx, sz) in enumerate(((-1.5, 4.0, 0.25, 3.3), (1.5, 4.0, 0.25, 3.3), (0, 2.4, 3.25, 0.25), (0, 5.6, 3.25, 0.25))):
        cube(f"wi_fr{k}_{part}", (WX + px, y - 0.17, pz), (sx, 0.08, sz), TRIM, 0.02)
    hg = empty(f"wi_h{k}", (WX - 1.38, y - 0.2, 2.55))
    for part, (px, pz, sx, sz) in enumerate(((0.07, 1.45, 0.14, 2.9), (2.69, 1.45, 0.14, 2.9), (1.38, 0.07, 2.76, 0.14), (1.38, 2.83, 2.76, 0.14), (1.38, 1.45, 2.6, 0.08))):
        cube(f"wi_sash{k}_{part}", (px, 0, pz), (sx, 0.12, sz), TRIM, 0.01, hg)
    cube(f"wi_pane{k}", (1.38, 0.0, 1.45), (2.6, 0.04, 2.7), GLASS if k == 2 else mat("pane", "#cfe8ff", 0.05, 0.6, "#dff2ff"), 0, hg)
    WSASH.append(hg)
cube("wi_out", (WX, 4.5, 3.5), (12, 0.2, 9), mat("sky", "#9fd4ff", 0.5, 3.0, "#bfe4ff"), 0)
point("wi_sun", (WX, 3.0, 5), "#fff4dd", 900, 2.0); WFRONT = point("wi_front", (WX + 0.4, 0.9, 3.9), "#ffe8d0", 0, 0.6); point("wi_in", (WX - 1, -4, 5.5), "#fff0d0", 700, 2.0)
# ---------------------------------------------------------------- kitchen x=600 (door high in the wall above the sink)
KX = 600
cube("k_floor", (KX, 0, -0.05), (14, 10, 0.1), mat("kfloor", "#e8e2d8", 0.5), 0)
for i in range(7):
    for j in range(5):
        if (i + j) % 2: cube(f"k_t{i}{j}", (KX - 6 + i * 2, -4 + j * 2, 0.005), (2, 2, 0.01), mat("ktile", "#3a8fd0", 0.5), 0)
KW = mat("kwall", "#9be0c8", 0.7)
cube("k_backL", (KX - 4.0, 4.15, 4.5), (6.0, 0.3, 9), KW, 0); cube("k_backR", (KX + 4.0, 4.15, 4.5), (6.0, 0.3, 9), KW, 0)
cube("k_backB", (KX, 4.15, 2.25), (2.0, 0.3, 4.5), KW, 0); cube("k_backT", (KX, 4.15, 8.2), (2.0, 0.3, 1.6), KW, 0)
cube("k_ceil", (KX, 0, 9.05), (14, 10, 0.1), YC, 0)
cube("k_counter", (KX, 3.0, 1.0), (10, 2.0, 2.0), mat("kcab", "#ffffff", 0.5), 0.05)
cube("k_top", (KX, 3.0, 2.05), (10.2, 2.2, 0.16), mat("ktop", "#e8823f", 0.4), 0.03)
cube("k_sink", (KX, 2.9, 2.0), (2.4, 1.5, 0.3), mat("sinkm", "#c8d0d8", 0.2, metal=0.8), 0.04)
cube("k_water", (KX, 2.9, 2.12), (2.1, 1.25, 0.06), mat("water", "#6fc8ff", 0.05, 0.8, "#8fd8ff"), 0)
cyl("k_tap", (KX, 3.75, 2.7), 0.09, 1.2, mat("sinkm", "#c8d0d8", 0.2, metal=0.8), verts=10)
cube("k_tapn", (KX, 3.5, 3.25), (0.16, 0.6, 0.14), mat("sinkm", "#c8d0d8", 0.2, metal=0.8), 0.03)
for k, x in enumerate((-4, -2.2, 2.2, 4)): cube(f"k_cab{k}", (KX + x, 3.6, 7.2), (1.6, 1.1, 1.8), mat("kcab", "#ffffff", 0.5), 0.05)
cube("k_landing", (KX, 5.4, 4.45), (2.4, 2.2, 0.1), YF, 0); cube("k_lback", (KX, 6.6, 6.5), (2.6, 0.2, 4.2), YW, 0)
KD, KDH = door("k_door", (KX, 4.0, 4.5), 0, "#3fae4a", 1.4, 2.8)
for k in range(3): point(f"k_pl{k}", (KX - 4 + k * 4, -2, 8), "#fff0d8", 600, 1.5)
point("k_landl", (KX, 5.6, 7), "#fff0cc", 120, 0.5)
SPLASH = [sphere(f"spl{i}", (0, 0, -500), (0.16, 0.16, 0.16), mat("water", "#6fc8ff", 0.05, 0.8, "#8fd8ff"), seg=8) for i in range(14)]
# ---------------------------------------------------------------- broom closet x=700
BX = 700
cube("b_floor", (BX, 0, -0.05), (6, 6, 0.1), YF, 0)
cube("b_back", (BX, 1.0, 2.5), (3.2, 0.2, 5), mat("bwall", "#5a4a8a", 0.8), 0)
for sd in (-1, 1): cube(f"b_side{sd}", (BX + sd * 1.6, 0, 2.5), (0.2, 2.2, 5), mat("bwall", "#5a4a8a", 0.8), 0)
cube("b_ceil", (BX, 0, 4.0), (3.2, 2.2, 0.1), mat("bwall", "#5a4a8a", 0.8), 0)
BROOMS = []
for k, (x, tilt, col) in enumerate(((-1.1, -14, "#e8c64a"), (-0.6, 8, "#e8823f"), (0.55, -9, "#e8c64a"), (1.05, 12, "#c8a23a"), (0.0, 3, "#e8823f"), (-0.25, -5, "#c8a23a"))):
    b = empty(f"broom{k}", (BX + x, 0.4 - (k % 3) * 0.25, 0.05)); b.rotation_euler = (R(tilt * 0.4), R(tilt), 0)
    cyl(f"br_stick{k}", (0, 0, 2.2), 0.06, 3.6, mat("stick", "#8a5a2a", 0.6), parent=b, verts=8)
    cube(f"br_head{k}", (0, 0, 0.35), (0.7, 0.25, 0.7), mat(f"bristle{k}", col, 0.9), 0.08, b)
    BROOMS.append(b)
point("b_bulb", (BX, -0.6, 3.6), "#ffd08a", 90, 0.3)
CL_D, CL_H = door("cl_door", (BX, -1.12, 0), 0, "#8a3fb0", 1.6, 3.2)
cube("b_front", (BX, -1.25, 3.6), (6, 0.2, 0.8), YW, 0)
for sd in (-1, 1): cube(f"b_frontw{sd}", (BX + sd * 2.0, -1.25, 2.5), (2.4, 0.2, 5), YW, 0)
cube("b_hall", (BX, -4, -0.04), (6, 6, 0.1), YF, 0)
point("b_hl", (BX, -4, 4), "#fff0cc", 300, 1.5)

# ---------------------------------------------------------------- props
lawnmower = empty("mower", (0, 0, -500))
cube("mw_body", (0, 0, 0.55), (1.5, 1.8, 0.7), mat("mwred", "#d8423f", 0.4), 0.15, lawnmower)
cube("mw_eng", (0, 0.1, 1.05), (0.7, 0.7, 0.4), mat("mwblk", "#2b2d36", 0.4), 0.08, lawnmower)
for sx in (-1, 1):
    for sy in (-1, 1): cyl(f"mw_w{sx}{sy}", (0.8 * sx, 0.7 * sy, 0.3), 0.3, 0.2, mat("tyre", "#1a1a1a", 0.8), (0, R(90), 0), lawnmower, 12)
    cube(f"mw_h{sx}", (0.55 * sx, -1.6, 1.4), (0.08, 0.08, 2.0), mat("mwblk", "#2b2d36", 0.4), 0.01, lawnmower, (R(-50), 0, 0))
cube("mw_bar", (0, -2.35, 2.05), (1.2, 0.1, 0.1), mat("mwblk", "#2b2d36", 0.4), 0.01, lawnmower)
BIGKEY = empty("bigkey", (0, 0, -500)); GOLD = mat("gold", "#e2b23a", 0.25, metal=1.0)
cyl("bk_shaft", (0, 0, 0), 0.1, 1.4, GOLD, rot=(0, R(90), 0), parent=BIGKEY, verts=10)
cyl("bk_bow", (-0.85, 0, 0), 0.35, 0.12, GOLD, rot=(R(90), 0, 0), parent=BIGKEY, verts=18)
cube("bk_bit", (0.6, 0, -0.2), (0.25, 0.1, 0.35), GOLD, 0.02, BIGKEY)
popcorn = empty("popcorn", (0, 0, -500))
cyl("pc_tub", (0, 0, 0), 0.42, 0.9, mat("pcred", "#e8423f", 0.5), parent=popcorn, verts=16)
for k in range(8): cube(f"pc_str{k}", (0.42 * math.cos(k * math.pi / 4), 0.42 * math.sin(k * math.pi / 4), 0), (0.1, 0.1, 0.92), mat("pcw", "#ffffff", 0.5), 0, popcorn, (0, 0, k * math.pi / 4))
for k in range(14): sphere(f"pc_k{k}", (random.Random(k).uniform(-0.3, 0.3), random.Random(k + 5).uniform(-0.3, 0.3), 0.5 + random.Random(k + 9).uniform(0, 0.2)), (0.13, 0.13, 0.11), mat("pcy", "#fff3b0", 0.7, 0.3), popcorn, 8)
POPS = [sphere(f"pop{i}", (0, 0, -500), (0.12, 0.12, 0.1), mat("pcy", "#fff3b0", 0.7, 0.3), seg=8) for i in range(6)]
def envelope(name, s=1.0):
    o = empty(name, (0, 0, -500))
    cube(name + "_b", (0, 0, 0), (1.2 * s, 0.06, 0.75 * s), mat("envgold", "#f2c230", 0.25, 0.4, "#f2c230", metal=0.6), 0.02, o)
    fl = empty(name + "_flh", (0, -0.035, 0.37 * s), o)
    cube(name + "_flap", (0, 0, -0.18 * s), (1.18 * s, 0.03, 0.4 * s), mat("envgold2", "#e0a820", 0.3, 0.3, "#e0a820", metal=0.6), 0.01, fl, (0, R(45), 0)).scale = (0.72, 1, 0.72)
    cube(name + "_seal", (0, -0.06, 0.05 * s), (0.2 * s, 0.03, 0.2 * s), mat("wax", "#c8282f", 0.4), 0.04, o)
    return o, fl
ENV1, ENV1F = envelope("env1"); ENV2, _ = envelope("env2", 0.62)
letter = cube("letter", (0, 0, -500), (0.65, 0.04, 0.42), mat("letterw", "#f6f3ea", 0.6), 0.01)
cube("letter_stamp", (0.2, -0.03, 0.1), (0.14, 0.02, 0.16), mat("stamp", "#c8282f", 0.4), 0, letter)
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
mail = lib.Char("mailman", skin="#e9b892", top="#3a6fc0", pants="#2b3d66", hair="#bfbfbf", hair_style="flat", kid=False, **K)
cube("mm_cap", (0, -0.12, 1.05), (1.08, 1.25, 0.28), mat("mmcap", "#2b3d66", 0.5), 0.06, mail.neck)
cube("mm_beard", (0, -0.5, -0.2), (0.95, 0.3, 0.8), mat("beard", "#d8d8d8", 0.9), 0.12, mail.neck)
cube("mm_bag", (0.75, -0.1, 1.7), (0.35, 1.0, 0.9), mat("mmbag", "#8a5a2a", 0.6), 0.08, mail.body)
crowd = []
CC = [("#3f8fd8", "#6b3f22"), ("#e86fb0", "#1d1310"), ("#57b65a", "#e0c070"), ("#8b4fb0", "#6b3f22"), ("#e8823f", "#1d1310"),
      ("#2fb0a8", "#e0702e"), ("#c94a4a", "#3a2414"), ("#6a7ad8", "#eeeeee"), ("#f2c53d", "#3a2414"), ("#ff8fb0", "#1d1310"),
      ("#4ac0e8", "#3a2414"), ("#a0d040", "#1d1310")]
for i, (top, hair) in enumerate(CC):
    crowd.append(lib.Char(f"cr{i}", skin=["#f3c89a", "#c98d62", "#8d5a3b", "#e9b892"][i % 4], top=top, pants=["#3b3b55", "#c9b48a", "#2f4a7a"][i % 3],
                          hair=hair, hair_style="spiky" if i % 3 == 0 else "flat", kid=i % 2 == 0, **K))
for _o in CONF + SPARK + SPLASH + POPS + STARS + [p for _, _, ps in FW for p in ps]: _o.hide_render = True
fill = point("camfill", (0.6, 0.4, 0.2), "#ffe6cc", 160, 1.0, cam)
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
OFF = (0, 0, -500)
CAST = [hero, ben, pick, mayor, mail] + crowd

def day(ex=0.3):
    bg.inputs["Color"].default_value = (*lib.srgb("#8fc8ff"), 1); bg.inputs["Strength"].default_value = 1.5
    sun.data.energy = 4.5; sun.data.color = lib.srgb("#fff0d8"); sun.rotation_euler = (R(50), 0, R(215))
    for l in STREETLAMPS: l.data.energy = 0
    sc.view_settings.exposure = ex; fill.data.energy = 160
def inside(ex=0.45):
    day(ex); fill.data.energy = 220
def scr(key, col="blue"):
    for k, o in TXT.items(): o.hide_render = (k != key)
    screen.data.materials[0] = scr_cols[col]
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
def audience(face="happy", n=10, y0=12.5, x0=2.0, yaw=None):
    """crowd on the square watching the Lying House (at +x, +y)"""
    for i, c in enumerate(crowd[:n]):
        x = x0 + (i % 5) * 3.2 + (1.4 if i // 5 else 0); y = y0 - (i // 5) * 2.6 + (i % 2) * 0.5
        c.place((x, y, 0.06), 180 + (x - HX) * 2.0 if yaw is None else yaw); c.face(face)
def confetti(f0, f1, cx=0, cy=20, spread=10, ztop=13):
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
def stars(f0, f1, c):
    for i, s in enumerate(STARS):
        s.hide_render = False; a = f0 + i * 2
        for f in range(a, f1 + 1, 2):
            ang = (f - a) * 0.5 + i * math.pi / 2
            s.location = (c[0] + 0.9 * math.cos(ang), c[1] - 0.6 * math.sin(ang) - 0.4, c[2] + 0.25 * math.sin(ang * 2)); s.keyframe_insert("location", frame=f)
def eyes(c, k, f=None):
    for e in c.eyes:
        e.scale = (e.scale[0] * k, e.scale[1], e.scale[2] * k)
        if f is not None: e.keyframe_insert("scale", frame=f)
def blink_closed(c):
    for e in c.eyes: e.scale = (e.scale[0], e.scale[1], e.scale[2] * 0.15)
def nx_at(x, y, f_on=None, f_full=None):
    """put the NOT AN EXIT wall+door at (x, y) in the corridor"""
    NX.location = (x, y, 0.0)
    if f_on is not None:
        NXL.data.energy = 0; NXL.data.keyframe_insert("energy", frame=f_on)
        NXL.data.energy = 9000; NXL.data.keyframe_insert("energy", frame=f_full)
HERO_SQ = (HX, HF - 3.2, 0.06)

# ---------------------------------------------------------------- shots
def s01(N):  # HOOK: sunny square, the crooked Lying House full of doors, crowd, hero small at its door, screen THE LYING HOUSE
    scr("house", "purple"); audience("surprised", 10, 12.0, 1.0)
    hero.place((HX, HF - 1.6, 0.06), 180); hero.pose(head=-20)
    cam_move(cam, tgt, 1, N, (2.0, 2.0, 3.0), (3.6, 4.4, 3.4), (HX - 1, HY, 6.5), (HX - 0.5, HY, 7.0), 24, 26)
def s02(N):  # "every door is a lie": the facade: doors everywhere (2nd floor, tiny, sideways) - tilt up
    cam_move(cam, tgt, 1, N, (HX - 2.0, HF - 9.0, 2.0), (HX - 1.5, HF - 8.0, 4.0), (HX, HF, 2.5), (HX, HF, 9.5), 30, 30)
def s03(N):  # "And I have one hour": hero close, determined, screen 60:00 red behind
    scr("hour", "red"); hero.place((-1.0, 22.2, 0.06), 0); hero.face("determined"); hero.pose(armL=-10, armR=-10)
    hero.pose(N, armL=-10, armR=-10, head=-5)
    cam_move(cam, tgt, 1, N, (-0.4, 17.8, 3.0), (-0.6, 18.5, 3.0), (-1.0, 22.2, 2.85), (-1.0, 22.2, 3.0), 36, 42)
def s04(N):  # "Nobody has ever made it out": screen ESCAPED: 0, crowd shakes heads, scared
    scr("nobody", "red"); audience("scared", 10, 17.0, -8.0, 0)
    for i, c in enumerate(crowd[:10]):
        for f in range(1, N + 1, 4): c.pose(f, headyaw=18 if (f // 4 + i) % 2 else -18)
    cam_move(cam, tgt, 1, N, (0.0, 9.5, 3.5), (0.0, 11.0, 4.0), (0, 26, 5.0), (0, 26, 5.2), 24, 26)
def s05(N):  # "Not even the mailman. He went in with one letter": mailman walks up the path into the house, the front door shuts
    mail.place((HX - 0.4, HF - 6.0, 0.06), 180, 1); fw = max(2, int(N * 0.65)); mail.place((HX, HF + 0.3, 0.06), 180, fw); mail.walk(1, fw, 8)
    hold(letter, mail, 0, (0, -0.4, -1.05)); letter.rotation_euler = (0, 0, 0)
    LH_FRONT_H.rotation_euler = (0, 0, R(-95)); LH_FRONT_H.keyframe_insert("rotation_euler", frame=fw)
    LH_FRONT_H.rotation_euler = (0, 0, 0); LH_FRONT_H.keyframe_insert("rotation_euler", frame=min(N, fw + 4))
    cam_move(cam, tgt, 1, N, (HX + 4.5, HF - 9.0, 2.6), (HX + 3.5, HF - 8.0, 2.6), (HX - 0.3, HF - 2.0, 2.0), (HX, HF, 2.2), 30, 32)
def s06(N):  # "three years ago": the mailbox stuffed with three years of letters, letters slide out
    for i, lt in enumerate(LETTERS[:4]):
        l0 = tuple(lt.location); lt.keyframe_insert("location", frame=1 + i * 2)
        lt.location = (l0[0] + 0.3, l0[1] - 0.4, -0.5 + 0.1 * i); lt.keyframe_insert("location", frame=min(N, 6 + i * 3))
    cam_move(cam, tgt, 1, N, (HX - 6.6, HF - 8.0, 2.6), (HX - 6.2, HF - 7.4, 2.4), (HX - 3.8, HF - 3.0, 1.8), (HX - 3.8, HF - 3.0, 1.7), 30, 34)
def s07(N):  # "The Mayor locked me in himself": Mayor turns the huge golden key in the front door, smug
    mayor.place((HX + 0.4, HF - 1.4, 0.06), 160); mayor.face("evil"); hold(BIGKEY, mayor, 1, (0, -0.9, -1.0))
    for k, f in enumerate(range(1, N + 1, 4)):
        mayor.pose(f, armR=-80, head=-5); BIGKEY.rotation_euler = (R(90 * (k % 2)), 0, R(90)); BIGKEY.keyframe_insert("rotation_euler", frame=f)
    cam_move(cam, tgt, 1, N, (HX + 3.4, HF - 0.6, 3.4), (HX + 3.1, HF - 0.8, 3.4), (HX + 0.3, HF - 1.4, 3.1), (HX + 0.3, HF - 1.4, 3.1), 30, 33)
def s08(N):  # "Escape in time, I win five thousand dollars": screen $5,000 gold, crowd cheers
    scr("prize", "gold"); audience("happy", 10, 18.0, -8.0, 180)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    confetti(1, N + 10, 0, 23, 8)
    cam_move(cam, tgt, 1, N, (-2.0, 12.0, 4.0), (-1.0, 13.5, 4.4), (0, 28, 5.6), (0, 28, 5.8), 26, 28)
def s09(N):  # "If I don't, I mow his lawn for a whole year": hero pushes a lawnmower, sad, on a huge lawn
    x0 = 30.0; hero.place((x0 - 3, 22.0, 0.06), 90, 1); hero.place((x0 + 2, 22.0, 0.06), 90, N); hero.face("scared")
    for f in range(1, N + 1, 4): hero.pose(f, armL=-70, armR=-70, lean=12, legL=20 if (f // 4) % 2 else -20, legR=-20 if (f // 4) % 2 else 20, head=8)
    lawnmower.parent = hero.root; lawnmower.location = (0, -2.9, 0); lawnmower.rotation_euler = (0, 0, 0)
    sun.data.color = lib.srgb("#ffd8a0")
    cam_move(cam, tgt, 1, N, (x0 - 1, 15.0, 2.6), (x0 + 2.5, 15.5, 2.6), (x0 - 1, 22.0, 1.8), (x0 + 2.5, 22.0, 1.8), 26, 26)
def s10(N):  # "Minute one. Stairs!": corridor, hero spots the stairs (stairs set), happy
    inside(); hero.place((SX - 7.6, 0.2, 0.06), 60); hero.face("happy", 1); eyes(hero, 1.0, 1); eyes(hero, 1.2, 4); hero.pose(1, armR=-40); hero.pose(5, armR=-100, armRs=20)
    cam_move(cam, tgt, 1, N, (SX - 11.5, -6.0, 3.2), (SX - 10.5, -6.5, 3.4), (SX - 5, 1.0, 3.2), (SX - 4, 1.0, 3.6), 24, 24)
def s11(N):  # "I ran up all of them": side view, hero runs up the stairs
    inside(); xs = SX - 7.0; xe = SX - 1.3
    for f in range(1, N + 1):
        x = xs + (xe - xs) * (f - 1) / max(1, N - 1); hero.place((x, 0.6, (step_top(x) if x > SX - 6.4 else 0.0) + 0.06), 90, f)
    hero.run(1, N, 4, 50, 16); hero.face("determined")
    cam_move(cam, tgt, 1, N, (SX - 6.5, -9.0, 3.6), (SX - 1.5, -9.0, 4.6), (SX - 5, 0.6, 3.0), (SX - 1, 0.6, 4.4), 26, 26)
def s12(N):  # "and hit my head on the ceiling": BONK, stars, shake
    inside(); x = SX - 1.3; z = step_top(x) + 0.06; hero.place((x, 0.6, z), 90, 1); hero.place((x, 0.6, z + 0.25), 90, 3); hero.place((x - 0.5, 0.6, z - 0.4), 90, 6)
    hero.face("shock", 1); hero.pose(1, armL=40, armR=-40, legL=-30, legR=30, lean=15); hero.pose(4, armL=-150, armR=-150, head=20, lean=-10)
    stars(4, N, (x, 0.0, z + 3.4)); shake(3, 6, 0.18)
    cam_move(cam, tgt, 1, N, (x - 1.0, -6.5, z + 2.6), (x - 0.8, -6.0, z + 2.6), (x, 0.6, z + 2.6), (x, 0.6, z + 2.5), 34, 36)
def s13(N):  # "They just stop.": low angle, the stairs run straight into the ceiling; hero dizzy sitting on a step
    inside(); x = SX - 2.2; z = step_top(x) + 0.06; hero.place((x, 0.6, z - 0.9), 60); hero.pose(legL=-90, legR=-90, head=-10, armL=-20, armR=-20); hero.face("frozen")
    stars(1, N, (x, 0.2, z + 2.0))
    cam_move(cam, tgt, 1, N, (SX - 6.0, -4.0, 1.6), (SX - 5.4, -4.4, 1.8), (SX + 2.5, 1.0, 6.4), (SX + 3.0, 1.0, 6.8), 22, 24)
def s14(N):  # "Minute ten. A big red door.": corridor dolly toward the red door at the end, hero walks to it
    inside(); hero.place((CX - 0.6, 30.0, 0.06), 180, 1); hero.place((CX - 0.3, 37.0, 0.06), 180, N); hero.walk(1, N, 8)
    cam_move(cam, tgt, 1, N, (CX + 1.2, 22.0, 3.4), (CX + 0.8, 27.0, 3.2), (CX, 40, 2.4), (CX, 40, 2.2), 24, 26)
def s15(N):  # "I yanked it open": close, hero pulls the red door open hard
    inside(); hero.place((CX - 1.6, 38.0, 0.06), 160); hero.face("determined"); hero.pose(1, armR=-80); hero.pose(3, armR=-80, lean=-12)
    open_door(RED_H, 1, 4, -105); shake(3, 5, 0.06)
    cam_move(cam, tgt, 1, N, (CX + 2.6, 33.5, 2.8), (CX + 2.2, 34.0, 2.8), (CX, 39.5, 2.2), (CX, 39.5, 2.2), 30, 32)
def s16(N):  # "Behind it? A wall.": brick wall in the frame; hero deadpan
    inside(); RED_H.rotation_euler = (0, 0, R(-105)); hero.place((CX - 1.9, 37.6, 0.06), 200); hero.pose(head=-3)
    cam_move(cam, tgt, 1, N, (CX - 0.4, 33.0, 2.4), (CX - 0.4, 34.5, 2.4), (CX, 39.9, 2.0), (CX, 39.9, 2.0), 30, 34)
def s17(N):  # "Minute twenty. Benny yelled from outside. Try the window!": Benny outside the house, hands around mouth
    ben.place((HX + 2.6, HF - 1.4, 0.06), -20); ben.face("surprised"); ben.pose(armL=-110, armR=-110, armLs=-25, armRs=-25, head=-12); ben.talk(1, N, 0.18, 2)
    cam_move(cam, tgt, 1, N, (HX + 4.4, HF - 5.5, 2.4), (HX + 4.0, HF - 5.0, 2.5), (HX + 2.6, HF - 1.4, 3.0), (HX + 2.6, HF - 1.4, 3.0), 30, 34)
def s18(N):  # "I opened it.": window set, hero swings the window open
    inside(); hero.place((WX, -1.3, 0.06), 180); hero.pose(1, armR=-110); hero.pose(4, armR=-80, armRs=-30)
    open_door(WSASH[0], 1, 4, -110)
    cam_move(cam, tgt, 1, N, (WX + 2.2, -6.0, 3.6), (WX + 1.8, -5.6, 3.6), (WX, 0, 3.6), (WX, 0, 3.6), 30, 32)
def s19(N):  # "Behind it was another window": hero face close, shock, window behind
    inside(); WSASH[0].rotation_euler = (0, 0, R(-110)); hero.place((WX + 0.4, -1.3, 0.06), 20); hero.face("shock"); eyes(hero, 1.0, 1); eyes(hero, 1.2, N)
    cam_move(cam, tgt, 1, N, (WX + 1.6, -5.0, 3.0), (WX + 1.4, -4.6, 3.0), (WX + 0.3, -1.3, 2.9), (WX + 0.3, -1.3, 2.95), 40, 44)
def s20(N):  # "And behind that one?": hero opens the second window
    inside(); WSASH[0].rotation_euler = (0, 0, R(-110)); hero.place((WX, -0.7, 0.06), 180); hero.pose(1, armR=-120); hero.pose(4, armR=-90, armRs=-30)
    open_door(WSASH[1], 1, 4, -100)
    cam_move(cam, tgt, 1, N, (WX - 1.8, -5.0, 3.8), (WX - 1.4, -4.6, 3.8), (WX, 0.7, 3.8), (WX, 0.7, 3.8), 32, 34)
def s21(N):  # "Benny's face. Squished on the glass.": Benny squished on the third window's glass
    inside(); WSASH[0].rotation_euler = (0, 0, R(-110)); WSASH[1].rotation_euler = (0, 0, R(-100))
    ben.place((WX - 0.05, 1.62, 0.9), 0); ben.face("happy"); ben.pose(armL=-150, armR=-150, armLs=-20, armRs=-20)
    ben.head.scale = (1.15, 0.7, 1.05); ben.mouth.scale = (2.2, 1, 3.0); WFRONT.data.energy = 700
    cam_move(cam, tgt, 1, N, (WX + 0.3, -2.5, 3.9), (WX + 0.1, -2.0, 3.9), (WX, 1.5, 3.85), (WX, 1.5, 3.85), 36, 42)
def s22(N):  # "Minute thirty. A door on the second floor": hero on the upstairs landing reaches for the green door
    inside()
    cam_move(cam, tgt, 1, N, (KX + 2.2, -5.0, 1.4), (KX + 1.8, -4.0, 1.6), (KX, 4.0, 5.4), (KX, 4.0, 5.6), 24, 26)
def s23(N):  # "I stepped through it": from the kitchen: the high door opens, hero steps out into the air
    inside(); open_door(KDH, 1, 4, -100); hero.place((KX, 5.4, 4.56), 0, 1); hero.place((KX, 4.6, 4.56), 0, max(2, N - 3)); hero.place((KX, 3.9, 4.3), 0, N)
    hero.walk(1, N, 8); hero.face("happy", 1); hero.face("surprised", N)
    cam_move(cam, tgt, 1, N, (KX - 2.0, -6.0, 3.0), (KX - 1.6, -5.4, 3.4), (KX, 3.6, 4.4), (KX, 3.6, 4.6), 28, 30)
def s24(N):  # "and fell straight into the kitchen sink": drop, SPLASH
    inside(); KDH.rotation_euler = (0, 0, R(-100)); fl = max(3, N // 3)
    hero.place((KX, 3.7, 4.2), 0, 1); hero.place((KX, 3.1, 1.35), 0, fl); hero.place((KX, 3.0, 1.2), 0, N)
    hero.face("shock", 1); hero.pose(1, armL=-160, armR=-160, legL=-20, legR=20); hero.pose(fl, armL=-170, armR=-170, legL=-80, legR=-80)
    r = random.Random(2)
    for i, s in enumerate(SPLASH):
        s.hide_render = False; a = 2 * math.pi * i / len(SPLASH)
        s.location = (KX, 2.9, 2.1); s.keyframe_insert("location", frame=fl)
        s.location = (KX + 1.8 * math.cos(a), 2.9 + 0.4 * math.sin(a), 3.4 + r.uniform(0, 1.6)); s.keyframe_insert("location", frame=fl + 4)
        s.location = (KX + 2.4 * math.cos(a), 2.9 + 0.6 * math.sin(a), 1.4); s.keyframe_insert("location", frame=fl + 9)
    shake(fl, fl + 3, 0.12)
    cam_move(cam, tgt, 1, N, (KX + 1.4, -5.0, 3.6), (KX + 1.2, -4.0, 3.2), (KX, 3.0, 3.0), (KX, 3.0, 2.4), 28, 32)
def s25(N):  # "Minute forty. A tiny door, the size of a shoebox": hero on his knees peers at a tiny door at floor level
    inside()
    hero.place((CX + 2.0, 13.3, -0.95), 70); hero.pose(legL=-90, legR=-90, lean=30, head=15); hero.face("surprised")
    cam_move(cam, tgt, 1, N, (CX - 2.0, 15.6, 1.0), (CX - 1.4, 15.4, 0.9), (CX + 3.9, 13.8, 0.6), (CX + 3.9, 13.8, 0.6), 26, 30)
def s26(N):  # "I squeezed through": squashed flat, his top half already through the tiny door, legs kicking in the corridor
    inside(); TINY_H.rotation_euler = (0, 0, R(-100))
    hero.root.scale = (0.5, 1, 0.3); hero.place((CX + 2.6, 14.0, 0.3), 90, 1); hero.place((CX + 3.15, 14.0, 0.3), 90, N)
    for f in range(1, N + 1, 2): hero.pose(f, legL=30 if (f // 2) % 2 else -10, legR=-10 if (f // 2) % 2 else 30, lean=75, armL=-170, armR=-170)
    cam_move(cam, tgt, 1, N, (CX + 1.0, 12.0, 1.1), (CX + 1.2, 12.3, 1.0), (CX + 3.5, 14.0, 0.4), (CX + 3.6, 14.0, 0.4), 30, 34)
def s27(N):  # "Brooms. Just brooms.": hero inside the broom closet, brooms in his face
    inside(); CL_H.rotation_euler = (0, 0, R(-100)); hero.place((BX, 0.45, 0.06), 0); hero.face("frozen"); hero.pose(armL=-10, armR=-10)
    BROOMS[4].location = (BX + 0.5, -0.4, 0.05); BROOMS[4].rotation_euler = (R(-8), R(-20), 0)
    BROOMS[1].location = (BX - 0.6, -0.3, 0.05); BROOMS[1].rotation_euler = (R(-6), R(16), 0)
    cam_move(cam, tgt, 1, N, (BX + 0.2, -3.2, 3.0), (BX + 0.15, -2.8, 3.0), (BX, 0.45, 2.8), (BX, 0.45, 2.8), 32, 36)
def s28(N):  # "Minute fifty. The big screen: ten minutes left": screen 10:00 LEFT red, push
    scr("ten", "red")
    cam_move(cam, tgt, 1, N, (-1.0, 18.0, 4.4), (-0.5, 20.0, 5.0), (0, 29.5, 6.0), (0, 29.5, 6.0), 30, 34)
def s29(N):  # "The whole town was watching": crowd on the square facing the Lying House
    scr("ten", "red"); audience("surprised", 10, 11.0, 1.0)
    for i, c in enumerate(crowd[:10]): c.pose(1, head=-12); c.pose(N, head=-16, headyaw=(-1) ** i * 8)
    cam_move(cam, tgt, 1, N, (4.0, 2.0, 2.6), (5.0, 3.2, 2.8), (HX - 1, HY, 4.0), (HX - 1, HY, 4.4), 24, 26)
def s30(N):  # "Mrs. Pickles brought popcorn": Pickles close, munching from a striped tub, pieces flying
    pick.place((6.0, 12.5, 0.06), 15); pick.face("happy"); hold(popcorn, pick, 0, (0, -0.35, -1.2)); pick.pose(armL=-55)
    for f in range(1, N + 1, 4): pick.pose(f, armL=-55, armR=-140 if (f // 4) % 2 else -95)
    pick.talk(1, N, 0.1, 2)
    for i, p in enumerate(POPS):
        p.hide_render = False; d = 1 + i * 3
        p.location = (6.2, 12.0, 3.4); p.keyframe_insert("location", frame=d)
        p.location = (6.2 + (i - 3) * 0.3, 11.0, 4.4 + (i % 2) * 0.3); p.keyframe_insert("location", frame=d + 5)
    cam_move(cam, tgt, 1, N, (4.6, 8.2, 3.4), (4.9, 8.8, 3.4), (6.0, 12.5, 3.5), (6.0, 12.5, 3.5), 34, 38)
def s31(N):  # "Five minutes.": hero sprinting down the corridor toward camera
    inside(); hero.place((CX + 0.4, 34.0, 0.06), 0, 1); hero.place((CX + 0.4, 22.0, 0.06), 0, N); hero.run(1, N, 4, 55, 18); hero.face("scared")
    cam_move(cam, tgt, 1, N, (CX + 0.6, 27.0, 2.8), (CX + 0.6, 16.5, 2.8), (CX + 0.4, 34.0, 2.4), (CX + 0.4, 22.0, 2.4), 26, 26)
def door_gag(N, k, closet=False):
    inside()
    if closet:
        open_door(CL_H, 1, 3, -105); hero.place((BX - 1.6, -2.6, 0.06), 150); hero.face("frozen")
        cam_move(cam, tgt, 1, N, (BX + 1.4, -7.0, 2.6), (BX + 1.3, -6.6, 2.6), (BX - 0.2, -0.4, 2.0), (BX - 0.2, -0.4, 2.0), 26, 28); return
    root, hg = CDOORS[k]; open_door(hg, 1, 3, -105)
    x, y = root.location[0], root.location[1]; sd = 1 if x > CX else -1
    hero.place((x - sd * 1.1, y - 1.5, 0.06), -90 * sd + 30 * sd); hero.face("frozen")
    cam_move(cam, tgt, 1, N, (x - sd * 7.6, y - 2.6, 2.6), (x - sd * 7.4, y - 2.2, 2.6), (x, y - 0.6, 1.8), (x, y - 0.6, 1.8), 26, 28)
def s32(N): door_gag(N, 1)
def s33(N): door_gag(N, 4)
def s34(N): door_gag(N, 0, closet=True)
def s35(N): door_gag(N, 7)
def s36(N):  # "Then I saw one last door": the grey door at the end of a dead end, the lights flicker on it
    inside(); nx_at(CX, 12.0)
    hero.place((CX - 0.6, 8.0, 0.06), 180); hero.pose(head=-5)
    cam_move(cam, tgt, 1, N, (CX + 1.6, 3.0, 3.4), (CX + 1.2, 4.0, 3.0), (CX, 12.0, 2.0), (CX, 12.0, 1.8), 24, 26)
def s37(N):  # "With a sign. Not an exit.": close on the sign
    inside(); nx_at(CX, 12.0)
    cam_move(cam, tgt, 1, N, (CX + 0.9, 9.8, 2.3), (CX + 0.75, 10.4, 2.2), (CX + 0.0, 11.78, 2.0), (CX + 0.0, 11.78, 2.0), 40, 44)
def s38(N):  # "Wait.": hero close, eyes go wide, brows up
    inside(); nx_at(CX, 12.0); hero.place((CX - 0.3, 9.6, 0.06), 0); hero.face("neutral", 1); hero.face("surprised", 4); eyes(hero, 1.0, 4); eyes(hero, 1.25, N)
    cam_move(cam, tgt, 1, N, (CX - 0.1, 6.4, 2.9), (CX - 0.1, 6.8, 2.9), (CX - 0.3, 9.6, 2.85), (CX - 0.3, 9.6, 2.85), 40, 46)
def s39(N):  # "Every door in this house lies": fast dolly down the corridor of doors (all of them)
    inside()
    cam_move(cam, tgt, 1, N, (CX + 0.0, 2.0, 2.0), (CX + 0.0, 22.0, 2.2), (CX + 0.0, 30.0, 2.0), (CX + 0.0, 40.0, 2.2), 20, 20)
def s40(N):  # "So the one that says no...": hero close at the grey door, hand on the knob, determined
    inside(); nx_at(CX, 12.0); hero.place((CX - 0.9, 11.0, 0.06), -15); hero.face("determined"); hero.pose(1, armL=-20); hero.pose(N, armL=-40)
    cam_move(cam, tgt, 1, N, (CX - 0.3, 7.0, 3.0), (CX - 0.3, 7.5, 3.0), (CX - 0.5, 11.2, 2.4), (CX - 0.5, 11.2, 2.5), 32, 36)
def s41(N):  # "I opened it. Sunlight!": the door opens onto blinding white light
    inside(); nx_at(CX, 12.0, 1, 4); open_door(NXH, 1, 4, -100)
    hero.place((CX + 0.0, 10.2, 0.06), 180); hero.pose(1, armR=-70); hero.pose(5, armL=-120, armR=-120, head=-8)
    cam_move(cam, tgt, 1, N, (CX - 0.6, 5.0, 2.8), (CX - 0.4, 6.4, 2.6), (CX, 12.0, 1.8), (CX, 12.0, 1.8), 26, 28)
def sides(face="happy"):
    P = [(HX - 6.5, 14.5, -40), (HX - 5.0, 12.8, -35), (HX - 7.6, 12.2, -45), (HX - 4.4, 15.6, -30), (HX + 4.6, 14.6, 40), (HX + 6.0, 12.9, 35), (HX + 3.6, 12.2, 30), (HX + 7.2, 15.4, 45),
         (HX - 9.0, 14.0, -50), (HX + 8.8, 13.4, 50)]
    for c, (x, y, yw) in zip(crowd, P): c.place((x, y, 0.06), yw); c.face(face)
def s42(N):  # "The town square!": hero bursts out of the Lying House front door into the sun, crowd
    LH_FRONT_H.rotation_euler = (0, 0, R(-100)); sides("surprised")
    hero.place((HX, HF + 0.4, 0.06), 0, 1); hero.place((HX - 0.6, HF - 4.5, 0.06), 0, N); hero.run(1, N, 4, 55, 14); hero.face("happy")
    cam_move(cam, tgt, 1, N, (HX - 2.6, HF - 11.0, 2.4), (HX - 2.4, HF - 10.0, 2.6), (HX, HF, 2.4), (HX - 0.4, HF - 3, 2.4), 28, 30)
def s43(N):  # "Three seconds left!": screen 0:03 red, push, shake
    scr("three", "red"); shake(1, 3, 0.08)
    cam_move(cam, tgt, 1, N, (-0.6, 20.0, 5.2), (-0.3, 21.6, 5.6), (0, 29.5, 6.0), (0, 29.5, 6.0), 34, 40)
def s44(N):  # "I won!": confetti, fireworks, screen ESCAPED!, crowd lifts the hero
    scr("won", "green"); sides("happy")
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    hero.place((HX - 1.0, HF - 3.4, 0.06), 0); cheer(hero, 1, N, 0)
    confetti(1, N + 8, HX - 3, HF - 3, 7, 11); fireworks(1, N, 45)
    cam_move(cam, tgt, 1, N, (HX - 5.0, HF - 12.0, 3.4), (HX - 4.6, HF - 11.0, 3.8), (HX - 2, HF, 4.0), (HX - 2, HF, 4.4), 24, 26)
def s45(N):  # "And right behind me? The mailman.": the bearded mailman walks out of the house behind the cheering hero
    LH_FRONT_H.rotation_euler = (0, 0, R(-100)); hero.place((HX - 1.6, HF - 3.4, 0.06), 30); hero.face("surprised"); hero.pose(headyaw=50)
    mail.place((HX, HF + 0.6, 0.06), 0, 1); mail.place((HX + 0.2, HF - 2.2, 0.06), 0, N); mail.walk(1, N, 10); mail.face("frozen")
    hold(letter, mail, 1, (0, -0.4, -1.05)); mail.pose(1, armR=-60)
    for f in range(1, N + 1, 5): mail.arms[1].rotation_euler = (R(-60), 0, 0); mail.arms[1].keyframe_insert("rotation_euler", frame=f)
    cam_move(cam, tgt, 1, N, (HX - 2.0, HF - 9.0, 2.8), (HX - 1.8, HF - 8.0, 2.9), (HX - 0.4, HF - 1, 2.8), (HX - 0.4, HF - 1.5, 2.8), 30, 32)
def s46(N):  # "Still holding his letter.": mailman close, beard, holds up the letter proudly
    mail.place((HX + 0.2, HF - 2.4, 0.06), 0); mail.face("happy"); hold(letter, mail, 1, (0, -0.4, -1.05)); mail.pose(1, armR=-100); mail.pose(N, armR=-120)
    cam_move(cam, tgt, 1, N, (HX + 0.6, HF - 6.6, 3.4), (HX + 0.5, HF - 6.0, 3.4), (HX + 0.2, HF - 2.4, 3.3), (HX + 0.2, HF - 2.4, 3.3), 36, 40)
def s47(N):  # "And this part is real": hero points at the screen THIS PART IS REAL
    scr("real", "blue"); hero.place((-3.0, 20.0, 0.06), 160); hero.face("happy"); hero.pose(1, armR=-120, armRs=-10); hero.talk(1, N, 0.12, 3)
    cam_move(cam, tgt, 1, N, (-6.0, 12.0, 3.4), (-5.2, 13.0, 3.6), (-1.0, 26, 4.4), (-1.0, 26, 4.6), 26, 28)
def s48(N):  # "...stairs that go up into the ceiling": the empty stairs, slow crane up to where they hit the ceiling
    inside(0.5)
    cam_move(cam, tgt, 1, N, (SX - 7.0, -7.0, 2.0), (SX - 6.0, -7.0, 4.0), (SX - 1, 1.0, 3.0), (SX + 1.5, 1.0, 6.4), 24, 26)
def s49(N):  # "and doors that open onto walls": a corridor door swings open on bricks (no hero)
    inside(); root, hg = CDOORS[10]; open_door(hg, 2, 6, -105); x, y = root.location[0], root.location[1]
    cam_move(cam, tgt, 1, N, (x + 3.0, y - 2.8, 2.6), (x + 2.8, y - 2.4, 2.6), (x, y, 1.6), (x, y, 1.6), 28, 30)
def s50(N):  # "They kept building it for thirty-eight years": screen BUILT FOR 38 YEARS, wide square + house, hammer-y crowd
    scr("years", "gold"); audience("surprised", 6, 15.0, -6.0, 180)
    cam_move(cam, tgt, 1, N, (-4.0, 6.0, 5.0), (-2.0, 7.5, 6.0), (2, 27, 6.0), (3, 27, 6.4), 22, 24)
def s51(N):  # "Then the Mayor gave me a golden envelope": Mayor hands it over, hero takes it
    mayor.place((HX - 3.4, HF - 4.0, 0.06), -60); mayor.face("evil"); mayor.pose(1, armR=-70); mayor.pose(N, armR=-80)
    hero.place((HX - 0.8, HF - 4.6, 0.06), 70); hero.face("happy"); hero.pose(1, armL=-40); hero.pose(N, armL=-75)
    hold(ENV1, mayor, 1, (0, -0.5, -1.1)); ENV1.rotation_euler = (0, 0, R(30))
    cam_move(cam, tgt, 1, N, (HX - 2.0, HF - 13.0, 3.2), (HX - 2.0, HF - 12.2, 3.3), (HX - 2.1, HF - 4.3, 2.7), (HX - 2.1, HF - 4.3, 2.8), 32, 35)
def s52(N):  # "I opened it. Inside?": close: hero's hands open the golden envelope, flap up, sparkle
    ENV1.location = (HX - 1.0, HF - 5.2, 2.4); ENV1.rotation_euler = (R(-10), 0, 0)
    ENV1F.rotation_euler = (0, 0, 0); ENV1F.keyframe_insert("rotation_euler", frame=1); ENV1F.rotation_euler = (R(-160), 0, 0); ENV1F.keyframe_insert("rotation_euler", frame=max(3, N // 2))
    hero.place((HX - 1.0, HF - 4.2, 0.06), 180); hero.pose(armL=-70, armR=-70)
    cam_move(cam, tgt, 1, N, (HX - 1.2, HF - 7.4, 3.4), (HX - 1.1, HF - 7.0, 3.3), (HX - 1.0, HF - 5.2, 2.4), (HX - 1.0, HF - 5.2, 2.5), 40, 44)
def s53(N):  # "Another envelope.": hero close, deadpan, holding up a smaller golden envelope
    hero.place((HX - 1.0, HF - 4.6, 0.06), 0); hero.face("frozen"); hero.pose(armR=-100); hold(ENV2, hero, 1, (0, -0.4, -1.1))
    cam_move(cam, tgt, 1, N, (HX - 0.7, HF - 8.4, 3.0), (HX - 0.8, HF - 8.0, 3.0), (HX - 1.0, HF - 4.6, 2.9), (HX - 1.0, HF - 4.6, 2.9), 38, 42)
def s54(N):  # END: golden-hour crane up over the Lying House (A/B candles overlay in post)
    hero.place((HX - 1.0, HF - 4.6, 0.06), 0); hero.face("neutral"); hold(ENV2, hero, 1, (0, -0.4, -1.1)); hero.pose(armR=-100)
    sun.data.color = lib.srgb("#ffc890"); sun.rotation_euler = (R(72), 0, R(235)); bg.inputs["Color"].default_value = (*lib.srgb("#ffb98a"), 1)
    cam_move(cam, tgt, 1, N, (HX - 2, HF - 9.0, 3.0), (HX - 8, HF - 18.0, 13.0), (HX - 1, HF - 4, 2.4), (HX, HY, 9.0), 28, 24)

T = [("s01", 0.0, s01), ("s02", wt(0, 7), s02), ("s03", wt(0, 12), s03),
     ("s04", L[1], s04), ("s05", wt(1, 6), s05), ("s06", wt(1, 16), s06),
     ("s07", L[2], s07), ("s08", wt(2, 6), s08), ("s09", wt(2, 16), s09),
     ("s10", L[3], s10), ("s11", wt(3, 3), s11), ("s12", wt(3, 9), s12), ("s13", wt(3, 16), s13),
     ("s14", L[4], s14), ("s15", wt(4, 6), s15), ("s16", wt(4, 10), s16),
     ("s17", L[5], s17), ("s18", wt(5, 12), s18), ("s19", wt(5, 15), s19),
     ("s20", L[6], s20), ("s21", wt(6, 4), s21),
     ("s22", L[7], s22), ("s23", wt(7, 8), s23), ("s24", wt(7, 12), s24),
     ("s25", L[8], s25), ("s26", wt(8, 10), s26), ("s27", wt(8, 13), s27),
     ("s28", L[9], s28), ("s29", wt(9, 12), s29), ("s30", wt(9, 17), s30),
     ("s31", L[10], s31), ("s32", wt(10, 2), s32), ("s33", wt(10, 3), s33), ("s34", wt(10, 4), s34), ("s35", wt(10, 5), s35),
     ("s36", L[11], s36), ("s37", wt(11, 6), s37),
     ("s38", L[12], s38), ("s39", wt(12, 1), s39), ("s40", wt(12, 7), s40),
     ("s41", L[13], s41), ("s42", wt(13, 4), s42), ("s43", wt(13, 7), s43),
     ("s44", L[14], s44), ("s45", L[15], s45), ("s46", wt(15, 6), s46),
     ("s47", L[16], s47), ("s48", wt(16, 5), s48), ("s49", wt(16, 17), s49), ("s50", wt(16, 23), s50),
     ("s51", L[17], s51), ("s52", wt(17, 8), s52), ("s53", wt(17, 12), s53), ("s54", L[18], s54)]
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
