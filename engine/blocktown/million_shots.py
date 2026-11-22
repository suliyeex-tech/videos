"""Oddwick daily Short 2026-11-22: "I Had 24 Hours to Spend $1,000,000" (Blocktown house style, owner 2026-11-20).
Sunny town square with the neon stage + big money screen, a candy shop, Mister Frosty's ice cream truck, Benny's hotel with a
roof pool, the game show, Mrs. Pickles' "lucky" rock and lemonade stand; night finale with the countdown and the one-cent twist.
Same recurring Blocktown cast (hero, Benny, Mayor, Mrs. Pickles + townsfolk) and town (lib.build_town).
python3.13 million_shots.py [sid ...] [--still]   -> /home/claude/work/<slug>/shots/<sid>/####.png (resumable)"""
import sys, os, json, math, random, time, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move

SLUG = "2026-11-22-spend-a-million-in-24-hours"; FPS = 12
W = f"/home/claude/work/{SLUG}"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; END = vo["total"] + 1.5
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

# ---------------------------------------------------------------- town square: neon stage + big money screen
SHOW = []
def S_(o): SHOW.append(o); return o
cube("plaza", (0, 22, 0.02), (40, 22, 0.06), mat("plaza", "#c9b79a", 0.85), 0)
S_(cube("stage", (0, 26.5, 0.7), (16, 6, 1.4), mat("stagefloor", "#1c1830", 0.3, metal=0.2), 0.05))
S_(cube("stage_edge", (0, 23.48, 1.3), (16.2, 0.12, 0.2), mat("neon_cyan", "#40f0ff", 0.3, 10, "#40f0ff"), 0))
S_(cube("stage_edge2", (0, 23.48, 0.25), (16.2, 0.12, 0.15), mat("neon_pink", "#ff4fd0", 0.3, 10, "#ff4fd0"), 0))
S_(cube("screenwall", (0, 29.8, 5.0), (17, 0.6, 9.6), mat("screenwall", "#120e22", 0.4), 0.05))
scr_cols = {"blue": mat("scr_blue", "#2a3cff", 0.3, 3.0, "#3a5cff"), "red": mat("scr_red", "#ff2a3a", 0.3, 4.0, "#ff2a3a"),
            "green": mat("scr_green", "#1fc85a", 0.3, 4.0, "#2aff6a"), "purple": mat("scr_purple", "#8a2aff", 0.3, 3.5, "#9a3aff"),
            "pink": mat("scr_pink", "#ff3fae", 0.3, 3.5, "#ff3fae")}
screen = S_(cube("bigscreen", (0, 29.45, 6.0), (9.5, 0.1, 5.2), scr_cols["blue"], 0))
for sd in (-1, 1):
    S_(cube(f"sidescr{sd}", (6.6 * sd, 29.45, 5.2), (2.6, 0.1, 6.4), mat(f"sidescr{sd}", "#ff4fd0" if sd < 0 else "#40f0ff", 0.3, 5.0), 0))
    for i in range(6): S_(cube(f"sidebar{sd}{i}", (6.6 * sd, 29.38, 2.6 + i * 1.05), (2.2, 0.05, 0.18), mat("barw", "#ffffff", 0.3, 6.0), 0))
for i in range(22):
    a = i / 22
    x = -5.2 + 10.4 * a if i < 11 else -5.2 + 10.4 * (a - 0.5) * 2
    S_(sphere(f"bulb{i}", (x, 29.35, 8.95 if i < 11 else 3.05), (0.16, 0.16, 0.16), mat("bulbm", "#ffe27a", 0.3, 12, "#ffcf4a"), seg=8))
for i in range(9):
    a = math.pi * i / 8
    S_(sphere(f"arch{i}", (-8.6 * math.cos(a), 29.0, 1.4 + 9.6 * math.sin(a) * 0.95), (0.3, 0.3, 0.3), mat("archm", "#ff4fd0" if i % 2 else "#40f0ff", 0.3, 14), seg=8))
SPOTS = [S_(spot(f"stspot{i}", (x, 10, 12), c, 0, 30, rot=(math.radians(45), 0, math.radians(-x * 2))))
         for i, (x, c) in enumerate(((-6, "#ff6fd8"), (0, "#ffffff"), (6, "#5ff0ff")))]
S_(point("stagefill", (0, 21, 6), "#c9b6ff", 0, 4.0))
TXT = {}
for key, body, size, col in (("prize", "$1,000,000", 1.45, "#ffe14a"), ("rule", "SPEND IT ALL\nIN 24 HOURS", 1.05, "#ffffff"),
                             ("lose", "1 CENT LEFT\n= LOSE IT ALL", 1.0, "#ffffff"), ("m999", "$999,000\nLEFT", 1.35, "#ffffff"),
                             ("show", "THE\nME SHOW", 1.35, "#ffe14a"), ("winme", "WINNER:\nME", 1.4, "#ffffff"),
                             ("m1240", "$12.40\nLEFT", 1.7, "#ffffff"), ("t59", "0:59", 2.6, "#ffffff"), ("t10", "0:10", 2.6, "#ffffff"),
                             ("zero", "$0.00", 2.4, "#ffffff"), ("cent", "$0.01\nYOU LOSE", 1.45, "#ffffff")):
    TXT[key] = S_(mktext("scr_" + key, body, (0, 29.36, 6.0), size, col, 4.0, extrude=0.01))
# bunting (birthday)
for i in range(16):
    x = -12 + i * 1.6
    cube(f"bunt{i}", (x, 21.5, 9.6 - 0.9 * math.sin(math.pi * i / 15)), (0.9, 0.05, 0.9), mat(f"bunt{i % 4}", ["#ff4fd0", "#ffe14a", "#40f0ff", "#5fff7a"][i % 4], 0.6, 0.4), 0, None, (0, math.radians(45), 0))
# podiums for the game show
podium = empty("podiums", (0, 0, 0))
for k, (x, col) in enumerate(((-4.2, "#ff4fd0"), (3.6, "#40f0ff"))):
    cube(f"pod{k}", (x, 25.2, 2.0), (1.8, 1.2, 1.3), mat(f"podm{k}", "#2a2050", 0.4), 0.05, podium)
    cube(f"podl{k}", (x, 24.58, 2.0), (1.6, 0.05, 0.25), mat(f"podn{k}", col, 0.3, 10, col), 0, podium)
# confetti + fireworks
CONF = []
rr = random.Random(7); ccols = ["#ff4fd0", "#40f0ff", "#ffe14a", "#5fff7a", "#ff7a3a", "#ffffff"]
for i in range(90): CONF.append(cube(f"conf{i}", (0, 0, -500), (0.22, 0.04, 0.32), mat(f"conf{i % 6}", ccols[i % 6], 0.5, 1.5), 0))
FW = []
for b, (x, z, col) in enumerate(((-9, 24, "#ff4fd0"), (0, 30, "#ffe14a"), (9, 25, "#40f0ff"))):
    FW.append((x, z, [sphere(f"fw{b}_{i}", (0, 0, -500), (0.25, 0.25, 0.25), mat(f"fwm{b}", col, 0.3, 30, col), seg=6) for i in range(26)]))

# ---------------------------------------------------------------- props: giant cheque, trophy, rock, coin, money stack
cheque = empty("cheque", (0, 0, -500))
cube("chq", (0, 0, 0.4), (3.2, 0.06, 1.4), mat("chq", "#e8ffe8", 0.6), 0.03, cheque)
mktext("chqt", "$1,000,000", (0, -0.05, 0.4), 0.55, "#1a7a3a", 0.0, extrude=0.01, parent=cheque).location = (0, -0.05, 0.42)
trophy = empty("trophy", (0, 0, -500)); gold = mat("gold2", "#f2c230", 0.2, 0.3, "#f2c230", metal=1.0)
cyl("tr_base", (0, 0, 0.1), 0.35, 0.2, gold, parent=trophy, verts=16); cyl("tr_stem", (0, 0, 0.45), 0.1, 0.5, gold, parent=trophy, verts=12)
cyl("tr_cup", (0, 0, 0.95), 0.45, 0.6, gold, parent=trophy, verts=20)
for sd in (-1, 1): cube(f"tr_h{sd}", (0.55 * sd, 0, 1.0), (0.12, 0.08, 0.4), gold, 0.03, trophy)
rock = empty("rock", (0, 0, -500)); rm_ = mat("rockm", "#8d8a84", 0.95)
cube("rk1", (0, 0, 0), (0.75, 0.6, 0.55), rm_, 0.2, rock, (0.3, 0.2, 0.4)); cube("rk2", (0.15, 0.05, 0.18), (0.45, 0.4, 0.35), rm_, 0.15, rock, (0.1, 0.5, 0.1))
cube("rkbow", (0, -0.2, 0.33), (0.6, 0.08, 0.12), mat("bowred", "#e8423f", 0.5), 0.03, rock)
cube("rkbow2", (0, -0.2, 0.42), (0.28, 0.1, 0.22), mat("bowred", "#e8423f", 0.5), 0.05, rock)
coin = cyl("coin", (0, 0, -500), 0.22, 0.05, mat("copper", "#c87533", 0.25, 0.4, "#ff9a4a", metal=1.0), verts=24)
cash = empty("cash", (0, 0, -500))
for k in range(4): cube(f"bill{k}", (0, 0, k * 0.05), (0.7, 0.35, 0.04), mat("billg", "#6fbf6a", 0.7), 0.0, cash, (0, 0, 0.15 * k))
SPARK = [sphere(f"spark{i}", (0, 0, -500), (0.1, 0.1, 0.1), mat("sparkm", "#fff6a0", 0.3, 20, "#fff2a0"), seg=6) for i in range(8)]

# ---------------------------------------------------------------- candy shop interior (ox=200)
CX = 200
cube("cs_floor", (CX, 0, 0.0), (16, 12, 0.1), mat("cs_floor", "#f6d6e8", 0.6), 0)
for i in range(8):
    for j in range(6):
        if (i + j) % 2: cube(f"cs_tile{i}{j}", (CX - 7 + i * 2, -5 + j * 2, 0.06), (2, 2, 0.02), mat("cs_tile", "#ffffff", 0.5), 0)
cube("cs_back", (CX, 6, 4), (16, 0.3, 8), mat("cs_wall", "#ff9ec8", 0.7), 0)
for sd in (-1, 1): cube(f"cs_side{sd}", (CX + 8 * sd, 0, 4), (0.3, 12, 8), mat("cs_wall2", "#ffc0dc", 0.7), 0)
jar_cols = ["#ff4f6f", "#ffd23a", "#4fd0ff", "#7aff6a", "#c070ff", "#ff9a3a"]
rs = random.Random(3)
for row in range(4):
    cube(f"cs_shelf{row}", (CX, 5.4, 1.2 + row * 1.6), (14, 1.0, 0.15), mat("cs_shelf", "#ffffff", 0.4), 0.02)
    for k in range(11):
        x = CX - 6.2 + k * 1.24; c = jar_cols[(k + row) % 6]
        cyl(f"cs_jar{row}_{k}", (x, 5.3, 1.75 + row * 1.6), 0.42, 0.95, mat(f"cs_jar{c}", c, 0.25, 0.6, c), verts=12)
        cyl(f"cs_lid{row}_{k}", (x, 5.3, 2.28 + row * 1.6), 0.45, 0.12, mat("cs_lid", "#ffffff", 0.3), verts=12)
        for q in range(3): sphere(f"cs_c{row}_{k}_{q}", (x + rs.uniform(-0.2, 0.2), 5.3 + rs.uniform(-0.2, 0.2), 1.45 + row * 1.6 + q * 0.22), (0.22, 0.22, 0.2), mat(f"cs_cm{c}", c, 0.3, 0.6), seg=8)
cube("cs_counter", (CX + 4, 1.5, 1.0), (5, 1.6, 2.0), mat("cs_counter", "#5fd0c0", 0.5), 0.06)
cube("cs_countertop", (CX + 4, 1.5, 2.05), (5.2, 1.8, 0.12), mat("cs_ctop", "#ffffff", 0.3), 0.03)
for k in range(5):   # giant lollipops
    x = CX - 6 + k * 3.0
    cyl(f"cs_lst{k}", (x, 3.2, 1.4), 0.07, 2.8, mat("cs_stick", "#ffffff", 0.4), verts=8)
    cyl(f"cs_lol{k}", (x, 3.2, 3.2), 0.75, 0.18, mat(f"cs_lol{k}", jar_cols[k], 0.3, 0.5), rot=(math.pi / 2, 0, 0), verts=24)
point("cs_light1", (CX - 3, -2, 7), "#fff0f6", 700, 1.5); point("cs_light2", (CX + 3, -2, 7), "#fff0f6", 700, 1.5)
mktext("cs_sign", "CANDY", (CX, 5.8, 7.4), 1.0, "#ffffff", 3.0, extrude=0.05)
# candy mountain (hero sits on it) + bags
mountain = empty("mountain", (0, 0, -500))
for i in range(60):
    a = rs.uniform(0, 2 * math.pi); r = rs.uniform(0, 2.6); h = 2.2 * (1 - r / 2.8)
    sphere(f"mt_c{i}", (r * math.cos(a), r * math.sin(a), rs.uniform(0, max(0.2, h))), (0.38, 0.38, 0.32), mat(f"cs_cm{jar_cols[i % 6]}", jar_cols[i % 6], 0.3, 0.6), mountain, 8)
cube("mt_core", (0, 0, 0.9), (3.4, 3.4, 1.8), mat("cs_cm#ffd23a", "#ffd23a", 0.3, 0.6), 0.8, mountain)

# ---------------------------------------------------------------- Mister Frosty's ice cream truck
truck = empty("truck", (0, 0, -500))
tw_, tp = mat("trk_white", "#f8f6f2", 0.4), mat("trk_pink", "#ff7fb8", 0.4)
cube("trk_low", (0, 0, 1.4), (7.0, 3.0, 1.6), tw_, 0.1, truck)
cube("trk_stripe", (0, -1.52, 1.3), (7.0, 0.04, 0.35), tp, 0, truck)
cube("trk_backwall", (0, 1.35, 3.0), (7.0, 0.3, 1.8), tw_, 0.05, truck)
cube("trk_roof", (0, 0, 4.05), (7.2, 3.2, 0.3), tp, 0.08, truck)
for x in (-3.4, 3.4): cube(f"trk_end{x}", (x, 0, 3.0), (0.25, 3.0, 1.8), tw_, 0.04, truck)
cube("trk_cab", (-4.2, 0, 1.7), (1.8, 2.9, 2.2), tw_, 0.25, truck)
cube("trk_wind", (-5.06, 0, 2.2), (0.06, 2.4, 0.9), mat("trk_glass", "#7fc8ff", 0.1, 0.5), 0.02, truck)
cube("trk_awning", (0, -1.9, 3.85), (5.2, 1.0, 0.12), mat("trk_awn", "#ffd23a", 0.5), 0.02, truck, (math.radians(-12), 0, 0))
cube("trk_shelf", (0, -1.6, 2.25), (5.0, 0.5, 0.12), tp, 0.02, truck)
for x, y in ((-4.0, -1.5), (-4.0, 1.5), (2.2, -1.5), (2.2, 1.5)):
    cyl(f"trk_wh{x}{y}", (x, y, 0.6), 0.6, 0.4, mat("tyre", "#1e1e24", 0.7), rot=(math.pi / 2, 0, 0), parent=truck, verts=20)
cone = empty("trk_cone", (1.0, 0, 4.2), truck)
cyl("trk_conec", (0, 0, 0.8), 0.6, 1.6, mat("cone", "#d9a05a", 0.7), parent=cone, verts=12)
sphere("trk_scoop", (0, 0, 1.9), (0.85, 0.85, 0.75), mat("scoop", "#ffb6d8", 0.4, 0.3), cone, 14)
sphere("trk_scoop2", (0, 0, 2.6), (0.6, 0.6, 0.5), mat("scoopm", "#fff4dc", 0.4, 0.3), cone, 12)
mktext("trk_sign", "FROSTY", (0, -1.53, 1.7), 0.55, "#ff4f9a", 0.6, extrude=0.02, parent=truck).location = (-0.2, -1.53, 1.75)
point("trk_in", (0, 0.3, 3.4), "#fff2dc", 300, 0.8, truck)
TRUCK_ST = (-14.0, -2.2, 0.0)   # parked on the street, serving window facing -y (the camera side)

# ---------------------------------------------------------------- Benny's hotel with a roof pool (behind the houses, left)
HX, HY = -17.0, 27.0
hm, hw = mat("htl", "#f2a74a", 0.6), mat("htlwin", "#ffe6a0", 0.3, 4.0, "#ffd27a")
cube("hotel", (HX, HY, 12), (12, 9, 24), hm, 0.1)
for fl in range(7):
    for k in range(4): cube(f"hwn{fl}{k}", (HX - 4.2 + k * 2.8, HY - 4.53, 3.2 + fl * 3.0), (1.5, 0.08, 1.7), hw, 0.02)
cube("htl_door", (HX, HY - 4.55, 1.3), (3.0, 0.08, 2.6), mat("htldoor", "#5a2d8a", 0.4, 0.5), 0.02)
cube("htl_awn", (HX, HY - 5.2, 2.9), (4.2, 1.4, 0.15), mat("htlawn", "#c8282f", 0.5), 0.03)
mktext("htl_sign", "HOTEL BENNY", (HX, HY - 4.7, 25.4), 1.5, "#ff4fd0", 6.0, extrude=0.15)
cube("htl_signbar", (HX, HY - 4.4, 24.6), (11, 0.3, 0.3), mat("pole", "#2b2d36", 0.4, metal=0.6), 0)
cube("pool_rim", (HX, HY, 24.15), (9, 6.5, 0.3), mat("poolrim", "#ffffff", 0.4), 0.05)
pool = cube("pool_water", (HX, HY, 24.3), (8.2, 5.7, 0.12), mat("poolw", "#3fd6ff", 0.05, 1.2, "#3fd6ff"), 0)
float_ring = empty("ring", (0, 0, -500))
bpy.ops.mesh.primitive_torus_add(major_radius=0.8, minor_radius=0.28, location=(0, 0, 0)); _r = bpy.context.active_object
_r.data.materials.append(mat("ringm", "#ff7fb8", 0.4)); _r.parent = float_ring; bpy.ops.object.shade_smooth()
SPLASH = [sphere(f"spl{i}", (0, 0, -500), (0.25, 0.25, 0.3), mat("splash", "#e6faff", 0.1, 2.0, "#bff4ff"), seg=8) for i in range(14)]
point("pool_glow", (HX, HY, 26), "#9ff0ff", 0, 3.0)

# ---------------------------------------------------------------- Mrs. Pickles' lemonade stand (square, front right)
LX, LY = 7.5, 15.5
stand = empty("stand", (LX, LY, 0))
cube("ls_box", (0, 0, 1.1), (3.2, 1.4, 2.2), mat("ls_wood", "#ffe14a", 0.6), 0.05, stand)
cube("ls_top", (0, 0, 2.25), (3.5, 1.7, 0.12), mat("ls_white", "#ffffff", 0.4), 0.02, stand)
for sd in (-1, 1): cube(f"ls_post{sd}", (1.55 * sd, 0.55, 3.3), (0.14, 0.14, 2.2), mat("ls_white", "#ffffff", 0.4), 0, stand)
cube("ls_roof", (0, 0.2, 4.45), (3.9, 2.2, 0.2), mat("ls_red", "#e8423f", 0.5), 0.03, stand, (math.radians(-10), 0, 0))
cube("ls_signb", (0, -0.73, 1.45), (2.8, 0.05, 0.9), mat("ls_white", "#ffffff", 0.4), 0.02, stand)
mktext("ls_sign", "LEMONADE", (0, -0.77, 1.6), 0.48, "#e8423f", 0.4, extrude=0.01, parent=stand).location = (0, -0.77, 1.62)
price = mktext("ls_price", "$12.50", (0, -0.77, 1.15), 0.42, "#1a7a3a", 0.4, extrude=0.01, parent=stand); price.location = (0, -0.77, 1.12)
cyl("ls_jug", (0.8, 0, 2.7), 0.32, 0.8, mat("ls_lem", "#fff07a", 0.1, 0.8, "#fff07a"), parent=stand, verts=14)
for k in range(3): cyl(f"ls_cup{k}", (-0.9 + k * 0.4, -0.2, 2.45), 0.14, 0.3, mat("ls_white", "#ffffff", 0.4), parent=stand, verts=10)
point("ls_lamp", (0, -0.8, 4.0), "#ffd9a0", 0, 1.0, stand)
stand_hidden = True

# ---------------------------------------------------------------- cast
K = dict(cartoon=True, blush=True)
hero = lib.Char("hero", top="#f2b51f", pants="#2f4a7a", hair="#3a2414", hood=True, extra="#d89a12", **K)
phat = empty("partyhat", (0, 0, 1.02 * hero.hs), hero.neck); phat.hide_render = True
bpy.ops.mesh.primitive_cone_add(radius1=0.32, depth=0.8, location=(0, 0, 0.4)); _c = bpy.context.active_object; _c.parent = phat
_c.data.materials.append(mat("phat", "#40c0ff", 0.5, 0.3)); _c.hide_render = True
ben = lib.Char("benny", skin="#c98d62", top="#d8423f", pants="#3b3b55", hair="#1d1310", hair_style="flat", **K)
cube("bencap", (0, -0.15, 1.05), (1.08, 1.2, 0.25), mat("bencap", "#2f63d6", 0.5), 0.06, ben.neck)
POCKETS = [cube(f"benpocket{sd}", (0.62 * sd * ben.s, -0.1, 1.25 * ben.s), (0.25, 0.4, 0.45), mat("pocketw", "#ffffff", 0.6), 0.04, ben.body) for sd in (-1, 1)]
frosty = lib.Char("frosty", skin="#f0c29a", top="#ffffff", pants="#5a5a6a", hair="#c9883a", hair_style="flat", kid=False, **K)
cube("fr_hat", (0, 0, 1.12), (1.1, 0.6, 0.35), mat("frhat", "#ffffff", 0.6), 0.05, frosty.neck)
cube("fr_band", (0, -0.31, 1.05), (1.1, 0.02, 0.1), mat("trk_pink", "#ff7fb8", 0.4), 0, frosty.neck)
cube("fr_bow", (0, -0.33, 2.6), (0.5, 0.05, 0.22), mat("frbow", "#ff4f9a", 0.5), 0.03, frosty.body)
frosty.mustache = cube("fr_mus", (0, -0.53, 0.42), (0.55, 0.06, 0.13), frosty.mhair, 0.03, frosty.neck)
mayor = lib.Char("mayor", skin="#f0c29a", top="#23253b", pants="#23253b", hair="#5b4636", hair_style="flat", kid=False, **K); mayor.mayor_kit()
pick = lib.Char("pickles", skin="#f0c8a8", top="#5c9a3a", pants="#3a5a2a", hair="#c8c8c8", hair_style="flat", kid=False, **K)
cube("pk_bun", (0, 0.2, 1.2), (0.55, 0.55, 0.45), pick.mhair, 0.15, pick.neck)
for sd in (-1, 1):
    cube(f"pk_glass{sd}", (0.22 * sd * pick.hs, -0.56 * pick.hs, 0.58 * pick.hs), (0.36 * pick.hs, 0.03, 0.06), mat("glassfr", "#111111", 0.3), 0, pick.neck)
    cube(f"pk_glassb{sd}", (0.22 * sd * pick.hs, -0.56 * pick.hs, 0.38 * pick.hs), (0.36 * pick.hs, 0.03, 0.05), mat("glassfr", "#111111", 0.3), 0, pick.neck)
candyman = lib.Char("candyman", skin="#8d5a3b", top="#ff7fb8", pants="#3b3b55", hair="#1d1310", hair_style="flat", kid=False, **K)
mic = empty("mic", (0, 0, -500))
cyl("micstick", (0, 0, 0.25), 0.07, 0.6, mat("micm", "#222222", 0.3), parent=mic, verts=8); sphere("michead", (0, 0, 0.6), (0.17, 0.17, 0.17), mat("michd", "#9a9aa8", 0.3, metal=0.8), mic, 10)
crowd = []
CC = [("#3f8fd8", "#6b3f22"), ("#e86fb0", "#1d1310"), ("#57b65a", "#e0c070"), ("#8b4fb0", "#6b3f22"), ("#e8823f", "#1d1310"),
      ("#2fb0a8", "#e0702e"), ("#c94a4a", "#3a2414"), ("#6a7ad8", "#eeeeee"), ("#f2c53d", "#3a2414"), ("#ff8fb0", "#1d1310"),
      ("#4ac0e8", "#3a2414"), ("#a0d040", "#1d1310")]
for i, (top, hair) in enumerate(CC):
    crowd.append(lib.Char(f"cr{i}", skin=["#f3c89a", "#c98d62", "#8d5a3b", "#e9b892"][i % 4], top=top, pants=["#3b3b55", "#c9b48a", "#2f4a7a"][i % 3],
                          hair=hair, hair_style="spiky" if i % 3 == 0 else "flat", kid=i % 2 == 0, **K))
for _o in CONF + SPLASH + SPARK + [p for _, _, ps in FW for p in ps]: _o.hide_render = True
fill = point("camfill", (0.6, 0.4, 0.2), "#ffe6cc", 160, 1.0, cam)
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
OFF = (0, 0, -500)
CAST = [hero, ben, frosty, mayor, pick, candyman] + crowd

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
    sc.objects["stagefill"].data.energy = 2500; sc.objects["ls_lamp"].data.energy = 400; sc.objects["pool_glow"].data.energy = 600
    sc.view_settings.exposure = 0.55; fill.data.energy = 320
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
    for c in CAST: c.place(OFF); c.pose(); c.face("neutral")
    screen.data.materials[0] = scr_cols["blue"]
    cam.data.lens = 28; cam.delta_location = (0, 0, 0)
    for k, o in TXT.items(): o.hide_render = True
    show(phat, False); show(podium, False); show(stand, False)
    for p in POCKETS: p.hide_render = True
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
def mayor_host(face="happy", x=-5.5):
    mayor.place((x, 25.2, 1.4), -20); hold(mic, mayor, 1); mayor.pose(armR=-95); mayor.face(face)
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
    r = random.Random(2)
    for i, p in enumerate(SPARK):
        a = 2 * math.pi * i / len(SPARK); p.hide_render = False
        p.location = c; p.scale = (0.01,) * 3; p.keyframe_insert("location", frame=f0); p.keyframe_insert("scale", frame=f0)
        p.location = (c[0] + 0.9 * math.cos(a), c[1] - 0.2, c[2] + 0.9 * math.sin(a)); p.scale = (1, 1, 1)
        p.keyframe_insert("location", frame=f0 + 5); p.keyframe_insert("scale", frame=f0 + 5)
        p.scale = (0.01,) * 3; p.keyframe_insert("scale", frame=min(f1, f0 + 12))
def truck_at(loc, f=None):
    truck.location = loc
    if f is not None: truck.keyframe_insert("location", frame=f)
def frosty_in(f=None, face="happy"):
    """Mister Frosty standing inside the truck, head + shoulders in the serving window"""
    frosty.place((truck.location[0] + 0.3, truck.location[1] - 0.6, truck.location[2] + 0.25), 0, f); frosty.face(face, f)
def eyes(c, k, f=None):   # widen/narrow eyes on top of a face
    for e in c.eyes:
        e.scale = (e.scale[0] * k, e.scale[1], e.scale[2] * k)
        if f is not None: e.keyframe_insert("scale", frame=f)
def splash(f0, f1, c):
    r = random.Random(4)
    for i, p in enumerate(SPLASH):
        a = 2 * math.pi * i / len(SPLASH); p.hide_render = False
        p.location = c; p.keyframe_insert("location", frame=f0)
        p.location = (c[0] + 1.4 * math.cos(a), c[1] + 1.4 * math.sin(a), c[2] + r.uniform(1.2, 2.4)); p.keyframe_insert("location", frame=f0 + 5)
        p.location = (c[0] + 2.2 * math.cos(a), c[1] + 2.2 * math.sin(a), c[2] - 0.3); p.keyframe_insert("location", frame=min(f1, f0 + 11))
HERO_SQ = (0.0, 21.5, 0.06)

# ---------------------------------------------------------------- shots
def s01(N):  # HOOK: sunny square, Mayor on stage hands a GIANT $1,000,000 cheque to the hero, screen $1,000,000, confetti
    scr("prize", "pink"); mayor.place((-1.8, 25.0, 1.4), 25); mayor.face("happy"); mayor.pose(armR=-80, armL=-150, armLs=25)
    hero.place((1.6, 25.0, 1.4), -20); hero.face("shock"); hero.pose(armR=-80, armL=-80); show(phat)
    cheque.location = (1.9, 24.0, 3.1); cheque.rotation_euler = (0, 0, math.radians(-20)); cheque.scale = (0.75, 0.75, 0.75)
    audience("happy", 10, 18.5)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    confetti(1, N + 10, 0, 23, 8); cheer(mayor, 1, N, 1)
    cam_move(cam, tgt, 1, N, (-0.6, 15.2, 6.2), (0.3, 16.8, 5.6), (0, 25, 3.6), (0.3, 25, 3.8), 26, 30)
def s02(N):  # hero close, jaw dropped, holding the cheque
    hero.place((1.6, 25.0, 1.4), -20); hero.face("shock"); show(phat); hero.pose(armR=-80, armL=-80)
    cheque.location = (1.9, 24.0, 2.75); cheque.rotation_euler = (0, 0, math.radians(-20)); cheque.scale = (0.75, 0.75, 0.75)
    eyes(hero, 1.0, 1); eyes(hero, 1.15, N); confetti(-10, N + 10, 1, 24, 4, 7)
    cam_move(cam, tgt, 1, N, (3.0, 19.8, 4.3), (2.8, 20.6, 4.2), (1.7, 24.6, 3.8), (1.7, 24.6, 3.9), 34, 40)
def s03(N):  # Mayor close, one finger up: one rule
    mayor_host("evil", -1.8); mayor.talk(1, N - 2, 0.12, 3); mayor.pose(1, armR=-95, armL=-30); mayor.pose(max(2, N // 3), armR=-95, armL=-165, armLs=10); scr("rule", "blue")
    cam_move(cam, tgt, 1, N, (-0.2, 20.3, 3.6), (-0.6, 21.0, 3.8), (-1.8, 25.2, 4.0), (-1.8, 25.2, 4.1), 36, 42)
def s04(N):  # big screen: SPEND IT ALL IN 24 HOURS
    scr("rule", "blue")
    cam_move(cam, tgt, 1, N, (-1.5, 18.5, 3.5), (-0.6, 20.8, 4.6), (0, 29.5, 6.0), (0, 29.5, 6.0), 26, 32)
def s05(N):  # screen turns red: 1 CENT LEFT = LOSE IT ALL; hero gulps in front of it
    scr("lose", "red"); hero.place((1.5, 22.0, 0.06), 160); hero.face("scared"); show(phat); hero.pose(head=-12)
    cam_move(cam, tgt, 1, N, (3.2, 16.0, 2.6), (2.6, 17.0, 3.0), (0.8, 26, 5.0), (0.6, 26, 5.4), 26, 30); shake(1, 3, 0.1)
def s06(N):  # hero close, party hat, birthday grin: today I turned twelve
    hero.place(HERO_SQ, 0); show(phat); hero.face("neutral", 1); hero.face("evil", max(2, N // 2)); hero.pose(1, head=6); hero.pose(N, head=0, armR=-40)
    confetti(-14, N, 0, 21, 3, 7)
    cam_move(cam, tgt, 1, N, (0.3, 17.6, 2.7), (0.15, 18.1, 2.7), (0, 21.5, 2.75), (0, 21.5, 2.8), 40, 46)
def s07(N):  # HOUR 1: hero bursts into the candy shop waving the cheque
    hero.place((CX - 4, -4.5, 0.06), -30, 1); hero.place((CX - 1, -1.0, 0.06), -10, N); hero.run(1, N, 6, 40, 10); hero.face("happy")
    candyman.place((CX + 4, 2.8, 0.06), 0); candyman.face("surprised"); candyman.pose(armL=-40, armR=-40)
    cam_move(cam, tgt, 1, N, (CX + 0.5, -9.0, 3.4), (CX + 0.8, -8.2, 3.2), (CX + 0.5, 1.5, 2.6), (CX + 1.0, 1.5, 2.6), 20, 22)
def s08(N):  # hero points at everything: "all of it" - shopkeeper's jaw drops
    hero.place((CX - 1, -0.5, 0.06), 170); hero.face("happy")
    for f in range(1, N + 1, 4): hero.pose(f, armR=-150 if (f // 4) % 2 else -120, armRs=25 if (f // 4) % 2 else -15, head=-8)
    candyman.place((CX + 4, 2.8, 0.06), -20); candyman.face("shock", 1); candyman.pose(1, armL=-150, armR=-150, armLs=20, armRs=20)
    cam_move(cam, tgt, 1, N, (CX + 1.0, -6.8, 3.4), (CX + 1.5, -6.2, 3.3), (CX + 1.5, 1.8, 2.8), (CX + 1.5, 1.8, 2.9), 22, 24)
def s09(N):  # back at the square: screen $999,000 LEFT
    scr("m999", "blue")
    cam_move(cam, tgt, 1, N, (1.8, 19.5, 4.2), (0.8, 21.5, 5.0), (0, 29.5, 6.0), (0, 29.5, 6.0), 28, 34)
def s10(N):  # hero on top of a candy mountain, tiny, overwhelmed: a million is a LOT
    mountain.location = (CX - 1.5, 0.5, 0.06); hero.place((CX - 1.5, 0.5, 2.2), 0); hero.face("surprised"); hero.pose(armL=-30, armR=-30, legL=-80, legR=-80)
    eyes(hero, 1.0, 1); eyes(hero, 1.2, N)
    cam_move(cam, tgt, 1, N, (CX - 1.0, -6.0, 5.6), (CX - 1.3, -4.3, 5.0), (CX - 1.5, 0.5, 3.6), (CX - 1.5, 0.5, 4.4), 26, 30)
def s11(N):  # HOUR 3: ice cream truck rolls down the sunny street; hero runs beside it waving the cheque
    truck_at((TRUCK_ST[0] - 14, TRUCK_ST[1], 0), 1); truck_at(TRUCK_ST, N); frosty.place(OFF)
    hero.place((TRUCK_ST[0] - 9, -5.2, 0.24), -90, 1); hero.place((TRUCK_ST[0] + 1, -5.2, 0.24), -90, N); hero.run(1, N, 5, 45, 12); hero.face("happy")
    hold(cheque, hero, 1, (0, -0.3, -1.6)); cheque.scale = (0.5, 0.5, 0.5)
    cam_move(cam, tgt, 1, N, (TRUCK_ST[0] + 6, -8.3, 2.2), (TRUCK_ST[0] + 4, -8.0, 2.4), (TRUCK_ST[0] - 6, -1.5, 2.4), (TRUCK_ST[0] - 1, -1.5, 2.6), 22, 24)
def s12(N):  # Mister Frosty in the window, eyes wide at the cheque
    truck_at(TRUCK_ST); frosty_in(1, "surprised"); frosty.pose(1, armL=-30, armR=-30); frosty.pose(N, armL=-100, armR=-100); eyes(frosty, 1.0, 1); eyes(frosty, 1.2, N)
    hero.place((TRUCK_ST[0] + 1.6, -5.0, 0.24), 160); hero.pose(armR=-150)
    cam_move(cam, tgt, 1, N, (TRUCK_ST[0] - 1.6, -8.4, 3.2), (TRUCK_ST[0] - 1.2, -7.8, 3.3), (TRUCK_ST[0] + 0.3, -2.8, 3.5), (TRUCK_ST[0] + 0.3, -2.8, 3.55), 30, 34)
def s13(N):  # Frosty salutes: he works for me now
    truck_at(TRUCK_ST); frosty_in(1, "happy"); frosty.pose(1, armR=-30); frosty.pose(max(2, N // 3), armR=-150, armRs=-35, head=-5); frosty.talk(1, N // 2, 0.1, 3)
    cam_move(cam, tgt, 1, N, (TRUCK_ST[0] + 1.2, -7.0, 3.7), (TRUCK_ST[0] + 1.0, -6.4, 3.7), (TRUCK_ST[0] + 0.3, -2.8, 3.55), (TRUCK_ST[0] + 0.3, -2.8, 3.6), 38, 44)
def s14(N):  # HOUR 6: HOTEL BENNY, low wide looking up, hero + Benny tiny at the door
    hero.place((HX - 1.2, 20.0, 0.06), 30); ben.place((HX + 1.2, 20.0, 0.06), 20); ben.face("shock"); hero.face("happy")
    ben.pose(1, armL=-30, armR=-30); ben.pose(N, armL=-160, armR=-160, armLs=25, armRs=25)
    cam_move(cam, tgt, 1, N, (-7.0, 14.8, 1.4), (-6.4, 15.6, 1.6), (HX + 0.5, 22, 6), (HX + 0.5, 24, 10), 18, 18)
def s15(N):  # Benny close, ecstatic, pointing up: a pool on the roof
    ben.place((HX + 1.2, 20.0, 0.06), 10); ben.face("happy"); ben.talk(1, N - 3, 0.14, 2)
    ben.pose(1, armR=-120); ben.pose(max(2, N // 2), armR=-170, armRs=8, head=-12)
    cam_move(cam, tgt, 1, N, (HX + 1.8, 16.6, 2.6), (HX + 1.9, 17.1, 2.6), (HX + 1.2, 20.0, 2.7), (HX + 1.2, 20.0, 2.9), 36, 40)
def s16(N):  # roof pool: Benny cannonballs in. Done.
    fl = max(3, int(N * 0.45))
    ben.place((HX - 3.2, HY - 1, 24.4), 90, 1); ben.place((HX - 1.0, HY - 0.5, 27.0), 90, fl // 2); ben.place((HX + 0.5, HY, 23.4), 90, fl)
    ben.pose(1, armL=-160, armR=-160, legL=-60, legR=-60); ben.face("happy"); splash(fl, N, (HX + 0.5, HY, 24.3))
    float_ring.location = (HX + 2.4, HY + 1.2, 24.45)
    cam_move(cam, tgt, 1, N, (HX + 6.5, HY - 7.5, 29.0), (HX + 5.8, HY - 6.8, 28.0), (HX, HY, 24.6), (HX, HY, 24.6), 22, 24)
def s17(N):  # HOUR 9: hero hosts his own game show (neon, podium, mic): THE ME SHOW
    night(); scr("show", "purple"); show(podium); hero.place((-4.2, 25.8, 1.4), 0); hold(mic, hero, 1); hero.pose(armR=-100); hero.face("happy"); hero.talk(1, N - 2, 0.12, 3)
    audience("happy", 10, 18.5)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    cam_move(cam, tgt, 1, N, (-6.2, 21.2, 3.8), (-4.9, 21.5, 3.9), (-3.0, 26, 3.7), (-2.6, 26, 3.8), 26, 30)
def s18(N):  # ...and the winner: hero jumps at the other podium, confetti, WINNER: ME
    night(); scr("winme", "green"); show(podium); hero.place((3.6, 25.8, 1.4), 0); hero.face("happy")
    for f in range(1, N + 1, 3): hero.pose(f, armL=-165, armR=-165, armLs=20, armRs=20, bob=0.3 if (f // 3) % 2 else 0)
    hold(trophy, hero, 1, (0, -0.3, -1.3)); confetti(1, N + 10, 3, 25, 4, 10)
    cam_move(cam, tgt, 1, N, (5.5, 19.2, 3.2), (4.6, 19.8, 3.5), (3.6, 25.8, 3.8), (3.6, 25.8, 4.0), 30, 34)
def s19(N):  # Mrs. Pickles close, smug, holding up a rock with a red bow
    pick.place((2.5, 18.0, 0.06), 0); pick.face("evil"); pick.talk(1, N - 2, 0.1, 3); pick.pose(armR=-100)
    rock.location = (3.36, 16.85, 2.95); rock.scale = (1.2, 1.2, 1.2)
    cam_move(cam, tgt, 1, N, (2.2, 13.9, 3.4), (2.3, 14.5, 3.4), (2.8, 18.0, 3.2), (2.8, 18.0, 3.3), 32, 36)
def s20(N):  # hero holds the "lucky" rock up, sparkles, proud: $100,000
    hero.place((0.2, 18.0, 0.06), 0); hero.face("happy"); hero.pose(armR=-150)
    rock.location = (0.96, 17.4, 3.45); rock.scale = (1.1, 1.1, 1.1); sparkle(2, N, (0.96, 17.0, 3.6))
    cam_move(cam, tgt, 1, N, (0.5, 13.8, 2.6), (0.4, 14.4, 2.8), (0.5, 18.0, 3.0), (0.5, 18.0, 3.3), 32, 36)
def s21(N):  # HOUR 23: night, square empty, hero alone in front of the red screen $12.40 LEFT
    night(); scr("m1240", "red"); hero.place(HERO_SQ, 180); hero.face("scared")
    cam_move(cam, tgt, 1, N, (-9, 6, 7.0), (-6, 8.5, 5.0), (0, 23, 3.5), (0, 23, 4.0), 22, 24)
def s22(N):  # screen close $12.40
    night(); scr("m1240", "red")
    cam_move(cam, tgt, 1, N, (-1.4, 21.0, 4.8), (-0.6, 22.6, 5.4), (0, 29.5, 6.0), (0, 29.5, 6.0), 30, 36); shake(1, 2, 0.06)
def s23(N):  # hero runs down the dark street past closed houses
    night(); hero.place((14, -4.6, 0.24), -90, 1); hero.place((2, -4.6, 0.24), -90, N); hero.run(1, N, 5, 45, 14); hero.face("scared")
    cam_move(cam, tgt, 1, N, (-4, -9.0, 1.8), (-4.5, -9.0, 2.0), (12, -3, 2.0), (3, -3, 2.0), 24, 24)
def s24(N):  # one stand still lit: Mrs. Pickles' lemonade stand
    night(); show(stand); pick.place((LX, LY + 1.5, 0.06), 0); pick.face("evil")
    hero.place((LX - 3.0, LY - 4.5, 0.06), 30, 1); hero.place((LX - 1.2, LY - 3.2, 0.06), 20, N); hero.walk(1, N, 8); hero.face("happy")
    cam_move(cam, tgt, 1, N, (LX - 7, LY - 9.5, 2.4), (LX - 5.5, LY - 8.5, 2.6), (LX, LY, 2.4), (LX, LY, 2.6), 26, 28)
def s25(N):  # price close: $12.50
    night(); show(stand); pick.place((LX, LY + 1.5, 0.06), 0); pick.face("evil")
    cam_move(cam, tgt, 1, N, (LX - 0.6, LY - 4.2, 1.3), (LX - 0.3, LY - 3.2, 1.25), (LX, LY - 0.77, 1.15), (LX, LY - 0.77, 1.15), 34, 44)
def s26(N):  # Pickles close, evil grin, tapping the sign
    night(); show(stand); pick.place((LX, LY + 1.5, 0.06), 0); pick.face("evil"); pick.talk(1, N // 2, 0.1, 3)
    for f in range(1, N + 1, 4): pick.pose(f, armR=-60 if (f // 4) % 2 else -75, head=-4)
    cam_move(cam, tgt, 1, N, (LX + 0.8, LY - 2.9, 3.6), (LX + 0.6, LY - 2.4, 3.6), (LX, LY + 1.5, 3.3), (LX, LY + 1.5, 3.35), 38, 44)
def s27(N):  # hero close, counting coins in his palm, face drops: ten cents short
    night(); show(stand); hero.place((LX - 1.2, LY - 3.2, 0.06), 20); hero.face("neutral", 1); hero.face("shock", max(2, N // 2)); hero.pose(1, armR=-70, head=12)
    hold(cash, hero, 1, (0, -0.4, -1.2)); cash.scale = (0.8, 0.8, 0.8)
    cam_move(cam, tgt, 1, N, (LX - 2.4, LY - 6.4, 2.8), (LX - 2.2, LY - 5.9, 2.8), (LX - 1.2, LY - 3.2, 2.7), (LX - 1.2, LY - 3.2, 2.75), 38, 44)
def s28(N):  # Pickles shakes her head, arms crossed: rules are rules
    night(); show(stand); pick.place((LX, LY + 1.5, 0.06), 0); pick.face("evil")
    for f in range(1, N + 1, 3): pick.pose(f, armL=-75, armR=-75, armLs=-45, armRs=-45, headyaw=18 if (f // 3) % 2 else -18)
    pick.talk(1, N - 2, 0.1, 3)
    cam_move(cam, tgt, 1, N, (LX - 0.8, LY - 3.4, 3.3), (LX - 0.6, LY - 2.9, 3.3), (LX, LY + 1.5, 3.2), (LX, LY + 1.5, 3.25), 36, 42)
def s29(N):  # ONE MINUTE: screen 0:59, red
    night(); scr("t59", "red"); hero.place((0.8, 21.0, 0.06), 170); hero.face("scared")
    cam_move(cam, tgt, 1, N, (2.6, 15.0, 2.0), (1.8, 16.6, 2.6), (0, 29.5, 6.0), (0, 29.5, 6.0), 24, 26)
def s30(N):  # Benny turns out his pockets: nothing
    night(); ben.place((-2.0, 20.0, 0.06), 10); ben.face("scared"); ben.talk(1, N // 2, 0.08, 3)
    fl = max(2, N // 3); ben.pose(1, armL=-20, armR=-20); ben.pose(fl, armL=-45, armR=-45, armLs=45, armRs=45, head=-10)
    for p in POCKETS: p.hide_render = False
    cam_move(cam, tgt, 1, N, (-1.4, 16.0, 2.0), (-1.6, 16.6, 2.2), (-2.0, 20, 1.9), (-2.0, 20, 2.1), 32, 36)
def s31(N):  # the whole town counts down, screen 0:10 behind them
    night(); scr("t10", "red"); audience("surprised", 12, 12.5)
    for i, c in enumerate(crowd[:12]):
        c.talk(1 + i % 3, N, 0.16, 3); c.pose(1, armR=-120 - (i % 3) * 15, armL=-20)
    cam_move(cam, tgt, 1, N, (-3.0, 7.6, 2.8), (2.0, 7.8, 3.0), (0, 14, 3.0), (0, 14, 3.2), 24, 26)
def s32(N):  # hero close, idea: eyes go wide, grin
    night(); hero.place(HERO_SQ, 0); hero.face("scared", 1); fl = max(2, int(N * 0.4)); hero.face("evil", fl); eyes(hero, 1.0, fl); eyes(hero, 1.25, fl + 2)
    hero.pose(1, head=10); hero.pose(fl, head=-6, armR=-150)
    cam_move(cam, tgt, 1, N, (0.25, 18.3, 2.7), (0.1, 18.9, 2.7), (0, 21.5, 2.75), (0, 21.5, 2.8), 40, 48)
def s33(N):  # the ice cream truck, lit up at night, Frosty in the window
    night(); truck_at(TRUCK_ST); frosty_in(1, "happy"); frosty.pose(armL=-30, armR=-30)
    hero.place((TRUCK_ST[0] + 6, -5.0, 0.24), -90, 1); hero.place((TRUCK_ST[0] + 1.5, -5.0, 0.24), -90, N); hero.run(1, N, 5, 45, 12)
    cam_move(cam, tgt, 1, N, (TRUCK_ST[0] - 5, -8.4, 2.4), (TRUCK_ST[0] - 4.2, -8.0, 2.6), (TRUCK_ST[0] + 0.5, -2.5, 2.8), (TRUCK_ST[0] + 0.5, -2.5, 3.0), 24, 26)
def s34(N):  # hero slaps the cash on the shelf: your salary
    night(); truck_at(TRUCK_ST); frosty_in(1, "surprised"); hero.place((TRUCK_ST[0] + 0.5, -5.3, 0.24), 180); hero.face("determined")
    fl = max(2, N // 3); hero.pose(1, armR=-40); hero.pose(fl, armR=-95)
    cash.location = (TRUCK_ST[0] + 0.7, -3.8, -500); cash.keyframe_insert("location", frame=fl - 1)
    cash.location = (TRUCK_ST[0] + 0.7, -3.8, 2.35); cash.keyframe_insert("location", frame=fl); cash.scale = (1.3, 1.3, 1.3)
    frosty.pose(fl + 2, armR=-80)
    cam_move(cam, tgt, 1, N, (TRUCK_ST[0] - 3.0, -7.4, 3.2), (TRUCK_ST[0] - 2.6, -7.0, 3.2), (TRUCK_ST[0] + 0.5, -3.6, 2.9), (TRUCK_ST[0] + 0.5, -3.6, 2.95), 30, 34)
def s35(N):  # screen $0.00 green!
    night(); scr("zero", "green"); confetti(1, N + 14, 0, 25, 6)
    cam_move(cam, tgt, 1, N, (1.0, 21.0, 4.6), (0.4, 22.4, 5.2), (0, 29.5, 6.0), (0, 29.5, 6.0), 32, 36); shake(1, 3, 0.1)
def s36(N):  # the crowd goes wild, fireworks
    night(); scr("zero", "green"); audience("happy", 12, 12.5); fireworks(1, N)
    for i, c in enumerate(crowd[:12]): cheer(c, 1 + i % 3, N, i)
    hero.place((0, 15.5, 0.06), 180); cheer(hero, 1, N, 0); ben.place((-2.4, 15.2, 0.06), 160); cheer(ben, 1, N, 1)
    cam_move(cam, tgt, 1, N, (2.0, 7.6, 3.0), (-1.5, 7.6, 3.2), (0, 14, 3.4), (0, 14, 3.6), 22, 24); shake(1, N, 0.04)
def s37(N):  # Mayor lifts the golden trophy on stage
    night(); scr("zero", "green"); mayor.place((-1.0, 25.0, 1.4), 0); mayor.face("happy"); hold(trophy, mayor, 1, (0, -0.3, -1.3))
    mayor.pose(1, armR=-90); mayor.pose(N, armR=-170, armRs=5); mayor.talk(1, N - 2, 0.12, 3); confetti(-6, N + 10, -1, 25, 4, 10)
    cam_move(cam, tgt, 1, N, (0.5, 19.0, 2.8), (0.2, 19.8, 3.0), (-1.0, 25, 4.4), (-1.0, 25, 5.2), 30, 32)
def s38(N):  # Frosty, polite, talking from the window: thanks, boss
    night(); truck_at(TRUCK_ST); frosty_in(1, "happy"); frosty.talk(1, N - 2, 0.1, 3); frosty.pose(1, armR=-30); frosty.pose(N, armR=-60, head=-4)
    cam_move(cam, tgt, 1, N, (TRUCK_ST[0] - 0.4, -7.0, 3.7), (TRUCK_ST[0] - 0.2, -6.4, 3.7), (TRUCK_ST[0] + 0.3, -2.8, 3.55), (TRUCK_ST[0] + 0.3, -2.8, 3.6), 38, 44)
def s39(N):  # his hand reaches out with one tiny copper coin
    night(); truck_at(TRUCK_ST); frosty_in(1, "happy"); frosty.pose(1, armR=-40); frosty.pose(N, armR=-95)
    hold(coin, frosty, 1, (0, -0.3, -1.22)); coin.rotation_euler = (math.pi / 2, 0, 0); coin.scale = (1.4, 1.4, 1.4)
    cam_move(cam, tgt, 1, N, (TRUCK_ST[0] + 0.4, -6.6, 3.3), (TRUCK_ST[0] + 0.7, -5.8, 3.1), (TRUCK_ST[0] + 1.16, -3.8, 2.95), (TRUCK_ST[0] + 1.16, -3.9, 2.85), 40, 50)
def s40(N):  # ONE CENT: the coin lands in the hero's palm (extreme close, music stops)
    night(); hero.place(HERO_SQ, 0); hero.face("neutral"); hero.pose(armR=-80, head=20)
    hp = (0.76, 20.6, 2.05)
    coin.location = (hp[0], hp[1], hp[2] + 1.5); coin.keyframe_insert("location", frame=1); coin.scale = (1.3, 1.3, 1.3)
    coin.location = (hp[0], hp[1], hp[2] + 0.28); coin.keyframe_insert("location", frame=max(2, N // 2))
    cam_move(cam, tgt, 1, N, (hp[0] - 0.4, hp[1] - 2.2, hp[2] + 1.3), (hp[0] - 0.3, hp[1] - 1.8, hp[2] + 1.1), (hp[0], hp[1], hp[2] + 0.3), (hp[0], hp[1], hp[2] + 0.3), 46, 54)
def s41(N):  # screen snaps red: $0.01 YOU LOSE
    night(); scr("cent", "red"); hero.place((0.8, 21.0, 0.06), 170); hero.face("shock")
    cam_move(cam, tgt, 1, N, (-1.6, 20.4, 4.2), (-0.8, 21.8, 5.0), (0, 29.5, 6.0), (0, 29.5, 6.0), 26, 30); shake(1, 4, 0.14)
def s42(N):  # hero close, total shock
    night(); scr("cent", "red"); hero.place(HERO_SQ, 0); hero.face("shock"); eyes(hero, 1.0, 1); eyes(hero, 1.3, 4); hero.pose(armL=-30, armR=-30, head=-4)
    cam_move(cam, tgt, 1, N, (0.0, 17.4, 2.7), (0.0, 18.6, 2.7), (0, 21.5, 2.8), (0, 21.5, 2.8), 40, 50)
def s43(N):  # the Mayor takes it all back: drives off in the ice cream truck, waving
    night(); truck_at(TRUCK_ST, 1); truck_at((TRUCK_ST[0] + 18, TRUCK_ST[1], 0), N); frosty.place(OFF)
    mayor.face("happy"); mayor.pose(armR=-160, armRs=20); mayor.root.parent = truck; mayor.root.location = (0.3, -0.6, 0.25); mayor.root.rotation_euler = (0, 0, 0)
    hero.place((TRUCK_ST[0] + 3, -5.2, 0.24), 0); hero.face("scared"); hero.pose(armR=-90, armL=-90)
    cam_move(cam, tgt, 1, N, (TRUCK_ST[0] - 1, -7.8, 2.4), (TRUCK_ST[0] + 2, -7.6, 2.6), (TRUCK_ST[0] + 1, -2, 2.8), (TRUCK_ST[0] + 9, -2, 2.8), 22, 24)
def s44(N):  # HOTEL BENNY's sign goes dark; Benny climbs out of the pool, dripping, sad
    night(); sc.objects["pool_glow"].data.energy = 600
    ben.place((HX + 1.0, HY - 2.4, 24.3), 0); ben.face("scared"); ben.pose(armL=-20, armR=-20, head=10)
    float_ring.location = (HX + 2.4, HY + 1.2, 24.45)
    cam_move(cam, tgt, 1, N, (HX + 5.0, HY - 9.0, 27.0), (HX + 4.4, HY - 8.2, 26.6), (HX + 0.5, HY - 2.4, 25.6), (HX + 0.5, HY - 2.4, 25.8), 26, 30)
def s45(N):  # hero alone on the curb at night, holding the rock, deadpan
    night(); hero.place((-4.0, -5.0, 0.24), 0); hero.face("neutral"); hero.pose(armR=-70, legL=-80, legR=-80, head=6)
    hero.root.location.z = -0.5; hold(rock, hero, 1, (0, -0.45, -1.15))
    cam_move(cam, tgt, 1, N, (-2.4, -10.0, 1.6), (-2.8, -9.2, 1.6), (-4.0, -5.0, 1.6), (-4.0, -5.0, 1.65), 32, 36)
def s46(N):  # rock close; the hero's deadpan face behind it: it is not lucky
    night(); hero.place((-4.0, -5.0, -0.26), 0); hero.face("neutral", 1); hero.face("evil", max(2, N // 2)); hero.pose(armR=-70, legL=-80, legR=-80, head=6)
    hold(rock, hero, 1, (0, -0.45, -1.15)); hero.talk(1, N - 3, 0.06, 3)
    cam_move(cam, tgt, 1, N, (-3.6, -8.2, 1.9), (-3.7, -7.7, 1.95), (-3.9, -5.0, 1.8), (-3.9, -5.0, 1.85), 40, 46)
def s47(N):  # wide finale: night town, money screen red, crane up over the clock tower
    night(); scr("cent", "red"); hero.place((-4.0, -5.0, -0.26), 0); hero.pose(armR=-70, legL=-80, legR=-80); hold(rock, hero, 1, (0, -0.45, -1.15))
    cam_move(cam, tgt, 1, N, (-2, -12, 2.5), (-1, -16, 9.0), (-3, 0, 2.0), (0, 24, 8.0), 26, 24)

T = [("s01", 0.0, s01), ("s02", L[0] + 1.85, s02),
     ("s03", L[1], s03), ("s04", L[1] + 1.55, s04), ("s05", L[1] + 3.2, s05),
     ("s06", L[2], s06),
     ("s07", L[3], s07), ("s08", L[3] + 1.6, s08), ("s09", L[3] + 3.3, s09),
     ("s10", L[4], s10),
     ("s11", L[5], s11), ("s12", L[5] + 1.6, s12), ("s13", L[5] + 3.1, s13),
     ("s14", L[6], s14), ("s15", L[6] + 1.45, s15), ("s16", L[6] + 2.75, s16),
     ("s17", L[7], s17), ("s18", L[7] + 1.65, s18),
     ("s19", L[8], s19), ("s20", L[8] + 2.3, s20),
     ("s21", L[9], s21), ("s22", L[9] + 1.6, s22), ("s23", L[9] + 3.1, s23),
     ("s24", L[10], s24), ("s25", L[10] + 2.2, s25), ("s26", L[10] + 3.5, s26),
     ("s27", L[11], s27), ("s28", L[11] + 1.25, s28),
     ("s29", L[12], s29), ("s30", L[12] + 1.25, s30), ("s31", L[12] + 2.7, s31),
     ("s32", L[13], s32), ("s33", L[13] + 1.3, s33),
     ("s34", L[14], s34), ("s35", L[14] + 2.3, s35),
     ("s36", L[15], s36), ("s37", L[15] + 1.4, s37),
     ("s38", L[16], s38), ("s39", L[16] + 2.6, s39),
     ("s40", L[17] - 0.1, s40), ("s41", L[18], s41), ("s42", L[18] + 1.0, s42),
     ("s43", L[19], s43), ("s44", L[19] + 1.75, s44),
     ("s45", L[20], s45), ("s46", L[20] + 1.2, s46), ("s47", L[21], s47)]
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
