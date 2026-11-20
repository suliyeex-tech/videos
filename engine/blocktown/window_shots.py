"""Oddwick house-style SAMPLE (owner 2026-11-20): "I Have 3 Days to Pay for a Window".
Sunny blocky town (day) + neon game-show stage on the town square (night). Cast with big cartoon eyes + blush.
python3 window_shots.py [sid ...] [--still]   -> /home/claude/work/<slug>/shots/<sid>/####.png (resumable)"""
import sys, os, json, math, random, time, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move

SLUG = "sample-oddwick-style-window"; FPS = 15
W = f"/home/claude/work/{SLUG}"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; END = vo["total"] + 0.5
PREV = "--still" in sys.argv
RES = (216, 384) if PREV else (432, 768)
sc, cam, tgt = lib.setup(res=RES, samples=4 if PREV else 10, fps=FPS)
sc.render.threads_mode = "AUTO"
town = lib.build_town()
FONT = None
for fp in ("/root/.fonts/Fredoka-Bold.ttf", "/home/claude/work/fonts/Fredoka-Bold.ttf"):
    if os.path.exists(fp): FONT = bpy.data.fonts.load(fp); break

bg = sc.world.node_tree.nodes["Background"]
sun = sc.objects["moonlight"]; sc.objects["moon"].hide_render = True
STREETLAMPS = [o for o in sc.objects if o.type == "LIGHT" and o.name.startswith("lamp")]

def mktext(name, body, loc, size, col, emit=0.0, rot=(90, 0, 0), extrude=0.04):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = extrude
    if FONT: cu.font = FONT
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    cu.materials.append(mat(name + "m", col, 0.5, emit)); return o

# ---------------------------------------------------------------- town hall windows (the story's windows)
frame_m, glass_m = mat("winframe", "#f4f1e8", 0.5), mat("glass", "#9fd8ff", 0.1, 0.6, "#bfe6ff")
dark_m, tape_m = mat("hole", "#141018", 0.9), mat("tape", "#e8d9a8", 0.8)
WIN = {}
def window(key, x, y, z, w=1.8, h=2.2):
    cube(f"wf_{key}", (x, y - 0.06, z), (w + 0.3, 0.08, h + 0.3), frame_m, 0.03)
    g = cube(f"wg_{key}", (x, y - 0.12, z), (w, 0.05, h), glass_m, 0)
    cube(f"wbar_{key}", (x, y - 0.15, z), (0.1, 0.04, h), frame_m, 0); cube(f"wbarh_{key}", (x, y - 0.15, z), (w, 0.04, 0.1), frame_m, 0)
    hole = cube(f"wh_{key}", (x, y - 0.1, z), (w, 0.05, h), dark_m, 0); hole.hide_render = True
    shards = []
    for i in range(7):
        s = cube(f"ws_{key}{i}", (x + random.uniform(-w / 2, w / 2), y - 0.3, z + random.uniform(-h / 2, h / 2)), (0.35, 0.03, 0.5), glass_m, 0, None,
                 (0, random.uniform(0, 3), 0)); s.hide_render = True; shards.append(s)
    tape = [cube(f"wt_{key}{sd}", (x, y - 0.2, z), (0.25, 0.03, h * 1.25), tape_m, 0, None, (0, math.radians(38 * sd), 0)) for sd in (-1, 1)]
    for t in tape: t.hide_render = True
    WIN[key] = dict(glass=g, hole=hole, shards=shards, tape=tape, pos=(x, y, z))
for row, z in (("a", 2.6), ("b", 6.0)):
    for x in (-7.2, -4.4, 4.4, 7.2): window(f"{row}{x}", x, 32.0, z)
window("tw1", -1.4, 33.0, 11.5, 1.4, 1.8); window("tw2", 1.4, 33.0, 11.5, 1.4, 1.8)
BALLWIN, HATWIN = "b4.4", "tw2"
def broken(key, on=True, f=None, taped=False):
    w = WIN[key]; w["glass"].hide_render = on; w["hole"].hide_render = not on
    for t in w["tape"]: t.hide_render = not taped
def shatter(key, f0, n_frames=12):
    w = WIN[key]; x, y, z = w["pos"]
    w["glass"].hide_render = False; w["glass"].keyframe_insert("hide_render", frame=f0 - 1)
    w["glass"].hide_render = True; w["glass"].keyframe_insert("hide_render", frame=f0)
    w["hole"].hide_render = True; w["hole"].keyframe_insert("hide_render", frame=f0 - 1)
    w["hole"].hide_render = False; w["hole"].keyframe_insert("hide_render", frame=f0)
    r = random.Random(hash(key) & 255)
    for s in w["shards"]:
        s.hide_render = True; s.keyframe_insert("hide_render", frame=f0 - 1); s.hide_render = False; s.keyframe_insert("hide_render", frame=f0)
        s.location = (x + r.uniform(-.6, .6), y - 0.3, z + r.uniform(-.7, .7)); s.keyframe_insert("location", frame=f0)
        s.location = (x + r.uniform(-2.5, 2.5), y - r.uniform(2, 5), max(0.1, z - r.uniform(2.5, 6))); s.rotation_euler = (r.uniform(0, 6), r.uniform(0, 6), 0)
        s.keyframe_insert("location", frame=f0 + n_frames); s.keyframe_insert("rotation_euler", frame=f0 + n_frames)

# ---------------------------------------------------------------- props: lemonade stand, poster, ball, bat
stand = empty("stand", (6, -5.6, 0.17))
wood = mat("standwood", "#e6b35a", 0.7)
cube("st_top", (0, 0, 1.6), (3.6, 1.4, 0.15), wood, 0.03, stand); cube("st_front", (0, -0.65, 0.85), (3.6, 0.1, 1.5), mat("standfront", "#fff3b0", 0.7), 0.02, stand)
for i in range(5): cube(f"st_stripe{i}", (-1.44 + i * 0.72, -0.71, 0.85), (0.36, 0.03, 1.5), mat("stripe", "#f2c53d", 0.7), 0, stand)
for sd in (-1, 1): cube(f"st_post{sd}", (1.7 * sd, 0.4, 2.3), (0.12, 0.12, 1.5), wood, 0.02, stand)
cube("st_sign", (0, 0.4, 3.2), (3.7, 0.12, 0.8), mat("signbg", "#ffffff", 0.6), 0.04, stand)
t = mktext("st_signt", "LEMONADE 50c", (0, 0.31, 3.2), 0.48, "#e8423f", 0.2); t.parent = stand; t.location = (0, 0.31, 3.2)
jug = cyl("st_jug", (-0.8, 0, 2.15), 0.35, 0.95, mat("lemon", "#ffe44a", 0.15, 0.8, "#fff07a"), parent=stand, verts=16)
for i in range(3): cyl(f"st_cup{i}", (0.3 + i * 0.5, -0.2, 1.88), 0.15, 0.4, mat("cup", "#ffffff", 0.4), parent=stand, verts=10)
poster = empty("poster", (-4.5, 8.4, 0))
cube("po_board", (0, 0.1, 3.4), (3.4, 0.15, 4.6), mat("poboard", "#2b2050", 0.5), 0.05, poster)
for nm, body, z, sz, col in (("po1", "TOWN", 4.9, 0.75, "#ffe14a"), ("po2", "GAME SHOW", 4.1, 0.62, "#ff5fc8"),
                             ("po3", "$1,000", 2.95, 1.0, "#5fffd0"), ("po4", "SATURDAY", 1.85, 0.5, "#ffffff")):
    o = mktext(nm, body, (0, 0, z), sz, col, 1.2); o.parent = poster; o.location = (0, -0.04, z)
for sd in (-1, 1): cyl(f"po_leg{sd}", (1.3 * sd, 0.2, 1.0), 0.1, 2.0, mat("pole", "#2b2d36", 0.4, metal=0.6), parent=poster, verts=8)
ball = sphere("ball", (0, 0, -500), (0.28, 0.28, 0.28), mat("ball", "#f6f6f2", 0.4))
bat = empty("bat", (0, 0, -500))
cyl("batbody", (0, -0.0, 0.9), 0.13, 2.0, mat("batwood", "#c98a4a", 0.6), parent=bat, verts=12)

# ---------------------------------------------------------------- night game show on the square (hidden by day)
SHOW = []
def S_(o): SHOW.append(o); return o
plaza = cube("plaza", (0, 22, 0.02), (36, 20, 0.06), mat("plaza", "#c9b79a", 0.85), 0)
S_(cube("stage", (0, 26.5, 0.7), (16, 6, 1.4), mat("stagefloor", "#1c1830", 0.3, metal=0.2), 0.05))
S_(cube("stage_edge", (0, 23.48, 1.3), (16.2, 0.12, 0.2), mat("neon_cyan", "#40f0ff", 0.3, 10, "#40f0ff"), 0))
S_(cube("stage_edge2", (0, 23.48, 0.25), (16.2, 0.12, 0.15), mat("neon_pink", "#ff4fd0", 0.3, 10, "#ff4fd0"), 0))
S_(cube("screenwall", (0, 29.8, 5.0), (17, 0.6, 9.6), mat("screenwall", "#120e22", 0.4), 0.05))
scr_cols = {"blue": mat("scr_blue", "#2a3cff", 0.3, 3.0, "#3a5cff"), "red": mat("scr_red", "#ff2a3a", 0.3, 4.0, "#ff2a3a"),
            "green": mat("scr_green", "#2aff6a", 0.3, 4.0, "#2aff6a"), "purple": mat("scr_purple", "#8a2aff", 0.3, 3.5, "#9a3aff")}
screen = S_(cube("bigscreen", (0, 29.45, 6.0), (9.5, 0.1, 5.2), scr_cols["blue"], 0))
for sd in (-1, 1):
    S_(cube(f"sidescr{sd}", (6.6 * sd, 29.45, 5.2), (2.6, 0.1, 6.4), mat(f"sidescr{sd}", "#ff4fd0" if sd < 0 else "#40f0ff", 0.3, 5.0), 0))
    for i in range(6): S_(cube(f"sidebar{sd}{i}", (6.6 * sd, 29.38, 2.6 + i * 1.05), (2.2, 0.05, 0.18), mat("barw", "#ffffff", 0.3, 6.0), 0))
for i in range(22):   # marquee bulbs around the big screen
    a = i / 22
    x = -5.2 + 10.4 * a if i < 11 else -5.2 + 10.4 * (a - 0.5) * 2
    z = 8.95 if i < 11 else 3.05
    S_(sphere(f"bulb{i}", (x, 29.35, z), (0.16, 0.16, 0.16), mat("bulbm", "#ffe27a", 0.3, 12, "#ffcf4a"), seg=8))
TXT = {}
for key, body, size, col in (("title", "TOWN GAME SHOW", 0.95, "#ffffff"), ("prize", "$1,000", 2.0, "#ffe14a"), ("q", "HOW MANY\nWINDOWS?", 1.05, "#ffffff"),
                             ("x", "X", 3.8, "#ffffff"), ("forty", "40?", 2.6, "#ffffff"), ("correct", "CORRECT!", 1.45, "#ffffff"), ("n39", "39", 3.0, "#ffffff")):
    TXT[key] = S_(mktext("scr_" + key, body, (0, 29.36, 6.0), size, col, 4.0, extrude=0.01))
PODS = []
for i, x in enumerate((-4.5, 0.0, 4.5)):
    pc = ["#ff4fd0", "#40f0ff", "#ffe14a"][i]
    S_(cube(f"pod{i}", (x, 26.0, 2.25), (1.9, 1.3, 1.7), mat(f"pod{i}", "#2a2346", 0.4), 0.06))
    S_(cube(f"podstripe{i}", (x, 25.33, 2.25), (1.95, 0.05, 0.25), mat(f"podn{i}", pc, 0.3, 8, pc), 0))
    bz = S_(sphere(f"buzz{i}", (x, 26.0, 3.15), (0.42, 0.42, 0.25), mat(f"buzz{i}", "#ff2a2a", 0.3, 1.0, "#ff2a2a")))
    PODS.append((x, bz))
ARCH = []
for i in range(9):
    a = math.pi * i / 8
    S_(sphere(f"arch{i}", (-8.6 * math.cos(a), 29.0, 1.4 + 9.6 * math.sin(a) * 0.95), (0.3, 0.3, 0.3), mat("archm", "#ff4fd0" if i % 2 else "#40f0ff", 0.3, 14), seg=8))
SPOTS = [S_(spot(f"stspot{i}", (x, 17, 12), c, 0, 30, rot=(math.radians(52), 0, math.radians(-x * 2))))
         for i, (x, c) in enumerate(((-6, "#ff6fd8"), (0, "#ffffff"), (6, "#5ff0ff")))]
S_(point("stagefill", (0, 21, 6), "#c9b6ff", 0, 4.0))
CAMS = []
for sd in (-1, 1):   # TV cameras on tripods
    r = empty(f"tvcam{sd}", (9.5 * sd, 20.5, 0.06)); SHOW.append(r)
    for k in range(3): S_(cube(f"tri{sd}{k}", (0.4 * math.cos(k * 2.1), 0.4 * math.sin(k * 2.1), 1.1), (0.08, 0.08, 2.3), mat("tri", "#222222", 0.5), 0, r, (0.2 * math.cos(k * 2.1), 0.2 * math.sin(k * 2.1), 0)))
    S_(cube(f"tvbody{sd}", (0, 0, 2.5), (0.8, 1.6, 0.8), mat("tvcam", "#2a2a33", 0.4), 0.06, r)); S_(cyl(f"tvlens{sd}", (0, 1.0, 2.5), 0.3, 0.6, mat("lens", "#111111", 0.2), (math.pi / 2, 0, 0), r, 12))
    S_(sphere(f"tvred{sd}", (0.3, -0.82, 2.8), (0.08, 0.08, 0.08), mat("tally", "#ff2020", 0.3, 20), r, 8))
    r.rotation_euler = (0, 0, math.radians(20 * sd)); CAMS.append(r)
# confetti + fireworks
CONF = []
rr = random.Random(7); ccols = ["#ff4fd0", "#40f0ff", "#ffe14a", "#5fff7a", "#ff7a3a", "#ffffff"]
for i in range(90):
    c = cube(f"conf{i}", (0, 0, -500), (0.22, 0.04, 0.32), mat(f"conf{i % 6}", ccols[i % 6], 0.5, 1.5), 0); CONF.append(c)
FW = []
for b, (x, z, col) in enumerate(((-9, 24, "#ff4fd0"), (0, 30, "#ffe14a"), (9, 25, "#40f0ff"))):
    parts = [sphere(f"fw{b}_{i}", (0, 0, -500), (0.25, 0.25, 0.25), mat(f"fwm{b}", col, 0.3, 30, col), seg=6) for i in range(26)]
    FW.append((x, z, parts))

# ---------------------------------------------------------------- interiors: bakery (x=1100), grandma (x=1300)
def room(ox, wallc, floorc):
    cube(f"rf{ox}", (ox, 0, -0.05), (18, 16, 0.1), mat(f"rfm{ox}", floorc, 0.7), 0)
    cube(f"rb{ox}", (ox, 6, 4), (18, 0.3, 8), mat(f"rwm{ox}", wallc, 0.8), 0); cube(f"rl{ox}", (ox - 8, 0, 4), (0.3, 16, 8), mat(f"rwm{ox}", wallc, 0.8), 0)
    cube(f"rr{ox}", (ox + 8, 0, 4), (0.3, 16, 8), mat(f"rwm{ox}", wallc, 0.8), 0)
room(1100, "#ffd6e0", "#d9b48a")
for i in range(9): cube(f"bk_tile{i}", (1092 + i * 2, 5.8, 1.0), (1.0, 0.05, 2.0), mat("bktile", "#ffffff" if i % 2 else "#ff9fb8", 0.6), 0)
cube("counter", (1100, 2.5, 1.2), (12, 1.6, 2.4), mat("counter", "#8a5a3a", 0.6), 0.05)
cube("countertop", (1100, 2.5, 2.45), (12.3, 1.8, 0.15), mat("countertop", "#f4f1e8", 0.4), 0.03)
CAKES = []
cake_cols = ["#ff8fb0", "#ffffff", "#ffe14a", "#9fd8ff", "#c98a4a", "#b88aff"]
for i in range(6):
    c = empty(f"cake{i}", (1095 + i * 2, 2.5, 2.55))
    cyl(f"cakeb{i}", (0, 0, 0.35), 0.62, 0.7, mat(f"cakeb{i}", cake_cols[i], 0.6), parent=c, verts=20)
    cyl(f"caket{i}", (0, 0, 0.75), 0.5, 0.1, mat("icing", "#fff6f0", 0.4), parent=c, verts=20)
    sphere(f"cakec{i}", (0, 0, 0.9), (0.14, 0.14, 0.14), mat("cherry", "#e0202a", 0.3), c, 8)
    CAKES.append(c)
cube("bk_door", (1092.5, -7.8, 2.0), (2.4, 0.2, 4.0), mat("bkdoor", "#4fb0a0", 0.6), 0.04)
point("bk_l1", (1098, -2, 7), "#ffe8cc", 900, 2.0); point("bk_l2", (1103, 1, 7), "#ffd8b0", 600, 2.0)
room(1300, "#a8d8a0", "#8a6a4a")
cube("sofa", (1300, 3.5, 0.7), (6, 2, 1.4), mat("sofa", "#e8823f", 0.8), 0.25); cube("sofaback", (1300, 4.4, 1.7), (6, 0.6, 1.8), mat("sofa", "#e8823f", 0.8), 0.25)
cookiebox = empty("cookiebox", (0, 0, -500))
cube("cb_box", (0, 0, 0), (1.4, 0.9, 0.5), mat("cbox", "#4a7fd8", 0.6), 0.05, cookiebox)
for i in range(4): cyl(f"cb_c{i}", (-0.45 + i * 0.3, 0, 0.3), 0.2, 0.08, mat("cookie", "#c98a3a", 0.8), (math.pi / 2, 0, 0), cookiebox, 12)
cube("frame1", (1297, 5.8, 4.8), (2.2, 0.1, 1.6), mat("frame1", "#ffe14a", 0.6), 0.05)
point("gr_l1", (1298, -1, 7), "#ffe8c0", 900, 2.0)

# ---------------------------------------------------------------- cast (big cartoon eyes + blush = house style)
K = dict(cartoon=True, blush=True)
hero = lib.Char("hero", top="#f2b51f", pants="#2f4a7a", hair="#3a2414", hood=True, extra="#d89a12", **K)
ben = lib.Char("benny", skin="#c98d62", top="#d8423f", pants="#3b3b55", hair="#1d1310", hair_style="flat", **K)
cube("bencap", (0, -0.15, 1.05), (1.08, 1.2, 0.25), mat("bencap", "#2f63d6", 0.5), 0.06, ben.neck)
baker = lib.Char("baker", skin="#f0c29a", top="#f4f4f4", pants="#5a5a6a", hair="#5b4636", hair_style="flat", kid=False, **K)
cyl("bakerhat", (0, 0, 1.45), 0.48, 0.9, mat("bakerhat", "#ffffff", 0.6), parent=baker.neck, verts=16)
gran = lib.Char("gran", skin="#e9b892", top="#8b4fb0", pants="#8b4fb0", hair="#eeeeee", hair_style="flat", kid=False, **K)
cube("granbun", (0, 0.35, 1.1), (0.5, 0.5, 0.4), gran.mhair, 0.15, gran.neck)
mayor = lib.Char("mayor", skin="#f0c29a", top="#23253b", pants="#23253b", hair="#5b4636", hair_style="flat", kid=False, **K); mayor.mayor_kit()
pick = lib.Char("pickles", skin="#f0c8a8", top="#5c9a3a", pants="#3a5a2a", hair="#c8c8c8", hair_style="flat", kid=False, **K)
cube("pk_bun", (0, 0.2, 1.2), (0.55, 0.55, 0.45), pick.mhair, 0.15, pick.neck)
for sd in (-1, 1):
    cube(f"pk_glass{sd}", (0.22 * sd * pick.hs, -0.56 * pick.hs, 0.58 * pick.hs), (0.36 * pick.hs, 0.03, 0.06), mat("glassfr", "#111111", 0.3), 0, pick.neck)
    cube(f"pk_glassb{sd}", (0.22 * sd * pick.hs, -0.56 * pick.hs, 0.38 * pick.hs), (0.36 * pick.hs, 0.03, 0.05), mat("glassfr", "#111111", 0.3), 0, pick.neck)
mic = empty("mic", (0, 0, -500))
cyl("micstick", (0, 0, 0.25), 0.07, 0.6, mat("micm", "#222222", 0.3), parent=mic, verts=8); sphere("michead", (0, 0, 0.6), (0.17, 0.17, 0.17), mat("michd", "#9a9aa8", 0.3, metal=0.8), mic, 10)
coins = empty("coins", (0, 0, -500))
for i in range(4): cyl(f"coin{i}", (-0.24 + i * 0.16, -0.05 * i, 0.05 + 0.06 * i), 0.14, 0.04, mat("coin", "#f2c53d", 0.25, 0.4, "#ffcf4a", metal=1.0), parent=coins, verts=14)
cheque = empty("cheque", (0, 0, -500))
cube("chq", (0, 0, 0.4), (2.4, 0.06, 1.1), mat("chq", "#e8ffe8", 0.6), 0.03, cheque)
o = mktext("chqt", "$1,000", (0, -0.05, 0.4), 0.55, "#1a7a3a", 0.0, extrude=0.01); o.parent = cheque; o.location = (0, -0.05, 0.4)
tears = [sphere(f"tear{i}", (0, 0, -500), (0.07, 0.04, 0.11), mat("tear", "#6fc8ff", 0.1, 2.0, "#6fc8ff"), seg=8) for i in range(6)]
crowd = []
CC = [("#3f8fd8", "#6b3f22"), ("#e86fb0", "#1d1310"), ("#57b65a", "#e0c070"), ("#8b4fb0", "#6b3f22"), ("#e8823f", "#1d1310"),
      ("#2fb0a8", "#e0702e"), ("#c94a4a", "#3a2414"), ("#6a7ad8", "#eeeeee"), ("#f2c53d", "#3a2414"), ("#ff8fb0", "#1d1310")]
for i, (top, hair) in enumerate(CC):
    crowd.append(lib.Char(f"cr{i}", skin=["#f3c89a", "#c98d62", "#8d5a3b", "#e9b892"][i % 4], top=top, pants=["#3b3b55", "#c9b48a", "#2f4a7a"][i % 3],
                          hair=hair, hair_style="spiky" if i % 3 == 0 else "flat", kid=i % 2 == 0, **K))
dogs = [lib.Dog(f"dog{i}", c) for i, c in enumerate(["#a8682f", "#e8d8b8", "#3a2a22", "#d89a52", "#f4f4f4", "#7a6a5a"])]

SPLAT = cube("splat", (0, -0.52, 0.85), (0.6, 0.04, 0.35), mat("icing", "#fff6f0", 0.4), 0.1, baker.neck); SPLAT.hide_render = True
HSPLAT = cube("herosplat", (0, -0.1, 1.15), (1.1, 1.1, 0.35), mat("cakeb0", "#ff8fb0", 0.6), 0.15, hero.neck); HSPLAT.hide_render = True
fill = point("camfill", (0.6, 0.4, 0.2), "#ffe6cc", 160, 1.0, cam)
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
OFF = (0, 0, -500)
CAST = [hero, ben, baker, gran, mayor, pick] + crowd

def day():
    bg.inputs["Color"].default_value = (*lib.srgb("#8fc8ff"), 1); bg.inputs["Strength"].default_value = 1.5
    sun.data.energy = 4.5; sun.data.color = lib.srgb("#fff0d8"); sun.rotation_euler = (math.radians(50), 0, math.radians(215))
    for l in STREETLAMPS: l.data.energy = 0
    for o in SHOW: o.hide_render = True
    sc.view_settings.exposure = 0.3; fill.data.energy = 160
def night():
    bg.inputs["Color"].default_value = (*lib.srgb("#2a2470"), 1); bg.inputs["Strength"].default_value = 0.9
    sun.data.energy = 0.9; sun.data.color = lib.srgb("#9aa8ff"); sun.rotation_euler = (math.radians(55), 0, math.radians(200))
    for l in STREETLAMPS: l.data.energy = 1500
    for o in SHOW: o.hide_render = False
    for k, o in TXT.items(): o.hide_render = True
    for s in SPOTS: s.data.energy = 9000
    sc.objects["stagefill"].data.energy = 2500
    sc.view_settings.exposure = 0.55; fill.data.energy = 320
    broken(BALLWIN, True, taped=True)
def screen_show(key, col="blue"):
    for k, o in TXT.items(): o.hide_render = (k != key) if isinstance(key, str) else (k not in key)
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
    for c in CAST: c.place(OFF); c.pose(); c.face("neutral")
    for d in dogs: d.root.location = OFF
    screen.data.materials[0] = scr_cols["blue"]
    cam.data.lens = 28; cam.delta_location = (0, 0, 0)
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
def laugh(c, f0, f1, seed=0):
    c.face("happy", f0); f = f0 + seed % 3; k = 0
    while f <= f1:
        c.pose(f, armL=-30 if k % 2 else -10, armR=-100, lean=-8 if k % 2 else 4, head=12 if k % 2 else 0); f += 3; k += 1
    c.talk(f0, f1, 0.14, 2)
def audience(face="happy", n=10, y0=17.0):
    for i, c in enumerate(crowd[:n]):
        x = -8 + (i % 5) * 4.0 + (1.6 if i // 5 else 0); y = y0 - (i // 5) * 2.6 + (i % 2) * 0.5
        c.place((x, y, 0.06), 180 - x * 1.5); c.face(face)
def on_pod(c, i, face="neutral"): c.place((PODS[i][0], 27.0, 1.4), 0); c.face(face)
def mayor_host(): mayor.place((-7.0, 25.2, 1.4), -25); hold(mic, mayor, 1); mayor.pose(armR=-95); mayor.face("happy")
def buzz_flash(i, f):
    m = PODS[i][1].data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    m.default_value = 1.0; m.keyframe_insert("default_value", frame=max(1, f - 1)); m.default_value = 25; m.keyframe_insert("default_value", frame=f)
def confetti(f0, f1, cx=0, cy=24, spread=10):
    r = random.Random(3)
    for c in CONF:
        x, y = cx + r.uniform(-spread, spread), cy + r.uniform(-spread * 0.6, spread * 0.4)
        c.location = (x, y, 13 + r.uniform(0, 4)); c.rotation_euler = (r.uniform(0, 6), r.uniform(0, 6), 0); c.keyframe_insert("location", frame=f0); c.keyframe_insert("rotation_euler", frame=f0)
        c.location = (x + r.uniform(-2, 2), y + r.uniform(-1, 1), r.uniform(0.2, 5)); c.rotation_euler = (r.uniform(0, 30), r.uniform(0, 30), r.uniform(0, 6))
        c.keyframe_insert("location", frame=f1); c.keyframe_insert("rotation_euler", frame=f1)
def fireworks(f0, f1):
    r = random.Random(5)
    for b, (x, z, parts) in enumerate(FW):
        fb = f0 + b * 4
        for i, p in enumerate(parts):
            a = 2 * math.pi * i / len(parts); e = r.uniform(-1, 1)
            p.location = (x, 40, z); p.scale = (0.01, 0.01, 0.01); p.keyframe_insert("location", frame=fb); p.keyframe_insert("scale", frame=fb)
            p.scale = (0.35, 0.35, 0.35); p.keyframe_insert("scale", frame=fb + 4)
            p.location = (x + 6 * math.cos(a) * math.sqrt(1 - e * e), 40 + 2 * e, z + 6 * math.sin(a) * math.sqrt(1 - e * e) - 1.5)
            p.scale = (0.05, 0.05, 0.05); p.keyframe_insert("location", frame=min(f1, fb + 18)); p.keyframe_insert("scale", frame=min(f1, fb + 18))

# ---------------------------------------------------------------- shots
def s01(N):  # HOOK: low wide sunny street, a baseball smashes the town hall window
    hero.place((2.5, 2, 0.16), 160); hold(bat, hero, 1); hero.pose(armR=-150, armRs=-40, lean=-10); hero.face("happy")
    x, y, z = WIN[BALLWIN]["pos"]; f_hit = max(3, int(N * 0.55))
    ball.location = (3, 1, 3); ball.keyframe_insert("location", frame=1); ball.location = (x, y - 0.3, z); ball.keyframe_insert("location", frame=f_hit)
    ball.location = (x - 1, y - 3, 0.3); ball.keyframe_insert("location", frame=N)
    shatter(BALLWIN, f_hit)
    cam_move(cam, tgt, 1, N, (6.5, -2.5, 2.2), (6.0, 1.0, 2.8), (3, 24, 6.5), (4, 28, 6.0), 22, 26); shake(f_hit, min(N, f_hit + 6), 0.2)
def s02(N):  # hero close holding the bat: "oops"
    hero.place((0, 0, 0.16), 0); hold(bat, hero, 1); hero.pose(1, armR=-40, armRs=-10); hero.face("shock", 1); hero.pose(N, armR=-35, head=-6)
    cam_move(cam, tgt, 1, N, (0.6, -4.8, 2.6), (0.3, -4.0, 2.7), (0, 0, 2.6), (0, 0, 2.65), 38, 44)
def s03(N):  # broken window close, shards falling
    broken(BALLWIN, True); x, y, z = WIN[BALLWIN]["pos"]
    cam_move(cam, tgt, 1, N, (x - 2.5, y - 8, z - 2.5), (x - 1.5, y - 6.5, z - 1.8), (x, y, z), (x, y, z), 30, 34)
def s04(N):  # the Mayor mid-speech at a podium in front of the hall, glass rains down
    broken(BALLWIN, True); mayor.place((3.5, 29.5, 0.06), 0); hold(mic, mayor, 1); mayor.pose(1, armR=-95, armL=-60); mayor.face("happy", 1)
    mayor.face("shock", N // 3); mayor.pose(N // 3, armR=-95, armL=-160, armLs=30, head=10)
    audience("happy", 10, 22.5)
    for c in crowd: c.place(tuple(c.root.location), 180)
    cam_move(cam, tgt, 1, N, (1.0, 23.5, 2.0), (1.5, 24.5, 2.2), (3.5, 29.5, 3.6), (3.5, 29.5, 3.8), 30, 34); shake(N // 3, N // 3 + 5, 0.12)
def s05(N):  # the whole crowd turns to look at the hero
    broken(BALLWIN, True); hero.place((0, 13, 0.06), 0); hold(bat, hero, 1); hero.pose(armR=-30); hero.face("scared")
    audience("surprised", 10, 22.0)
    for i, c in enumerate(crowd):
        c.place(tuple(c.root.location), 0, 1); c.place(tuple(c.root.location), 180 + (i % 3 - 1) * 15, 4 + i % 3)
    cam_move(cam, tgt, 1, N, (-2, 30, 3.5), (-1, 29, 3.3), (0, 13, 2.5), (0, 13, 2.4), 24, 28)
def s06(N):  # Mayor close, pointing: $1000 by Saturday
    broken(BALLWIN, True); mayor.place((0, 29.5, 0.06), 0); mayor.face("evil", 1); mayor.talk(1, N - 2, 0.12, 3)
    mayor.pose(1, armR=-90, armL=-10); mayor.pose(N // 2, armR=-95, armL=-10, head=-6)
    cam_move(cam, tgt, 1, N, (0.6, 25.0, 3.4), (0.3, 25.9, 3.3), (0, 29.5, 3.3), (0, 29.5, 3.35), 34, 40)
def s07(N):  # the clock tower, tilt up: forever
    cam_move(cam, tgt, 1, N, (2, 15, 1.5), (1.5, 17, 1.8), (0, 33, 8), (0, 33, 19), 22, 22)
def s08(N):  # hero close with 4 coins in his hand
    hero.place((0, 0, 0.16), 0); hold(coins, hero, 0, (0, -0.35, -1.2)); hero.pose(1, armL=-75); hero.face("scared", 1); hero.pose(N, armL=-80, head=12)
    cam_move(cam, tgt, 1, N, (-0.8, -4.4, 3.4), (-0.5, -3.8, 3.3), (-0.3, 0, 2.2), (-0.3, 0, 2.3), 34, 40)
def s09(N):  # tiny hero in front of the giant clock tower (from behind, low)
    hero.place((0, 24, 0.06), 180); hero.face("neutral"); hero.pose(1, head=20); hero.pose(N, head=24)
    cam_move(cam, tgt, 1, N, (0.8, 18.5, 0.8), (0.3, 19.5, 0.7), (0, 33, 14), (0, 33, 15.5), 18, 18)
def s10(N):  # day one: lemonade stand on the sidewalk
    hero.place((6, -4.6, 0.17), 0); hero.face("happy"); hero.pose(1, armL=-100, armLs=20, armR=-100, armRs=20)
    cam_move(cam, tgt, 1, N, (1.0, -15.0, 2.0), (3.0, -14.0, 2.2), (6, -5, 2.4), (6, -5, 2.5), 26, 30)
def s11(N):  # jug + hero pouring, close
    hero.place((6, -4.6, 0.17), 0); hero.face("happy", 1); hero.pose(1, armR=-70); hero.pose(N, armR=-85)
    cam_move(cam, tgt, 1, N, (4.0, -9.0, 2.4), (4.6, -8.6, 2.6), (5.2, -5.6, 2.3), (5.4, -5.4, 2.6), 34, 38)
def s12(N):  # Benny buys a cup, drinks
    hero.place((6, -4.6, 0.17), 0); hero.face("happy"); ben.place((6.6, -7.4, 0.17), 170); ben.face("happy")
    ben.pose(1, armR=-60); ben.pose(N // 2, armR=-150, head=-20); ben.pose(N, armR=-150, head=-25)
    cam_move(cam, tgt, 1, N, (10.5, -9.5, 2.3), (10.0, -10.2, 2.5), (6.2, -6.2, 2.6), (6.2, -6.0, 2.7), 28, 30)
def s13(N):  # Benny holds his hand out: refund. Hero face falls.
    ben.place((0, 0, 0.16), 0); ben.face("evil"); ben.pose(1, armR=-30); ben.pose(N // 3, armR=-85, armRs=5); ben.talk(1, N // 2, 0.12, 2)
    cam_move(cam, tgt, 1, N, (0.9, -4.4, 2.5), (0.5, -3.7, 2.6), (0, 0, 2.5), (0, 0, 2.6), 36, 42)
def s14(N):  # day two: hero with SIX dogs on the street
    hero.place((0, -1.5, 0.06), 0); hero.face("happy"); hero.pose(armL=-50, armR=-50)
    for i, d in enumerate(dogs):
        d.root.location = (-3.2 + (i % 3) * 1.6 + (0.8 if i // 3 else 0), -4.2 - (i // 3) * 1.8, 0.06); d.root.rotation_euler = (0, 0, math.radians((i - 2.5) * 8))
        d.tail.rotation_euler = (0, 0.4, 0); d.tail.keyframe_insert("rotation_euler", frame=1 + i % 3)
        d.tail.rotation_euler = (0, -0.4, 0); d.tail.keyframe_insert("rotation_euler", frame=4 + i % 3)
    cam_move(cam, tgt, 1, N, (3, -12.5, 1.6), (1, -12.0, 1.8), (0, -3, 1.7), (0, -3, 1.8), 26, 30)
def s15(N):  # the dogs drag the hero down the street (tracking)
    for i, d in enumerate(dogs):
        x0 = -6 + (i % 3) * 0.6; y0 = -1.5 + (i - 2.5) * 0.55
        d.root.rotation_euler = (0, 0, math.radians(-90)); d.root.location = (x0, y0, 0.06); d.root.keyframe_insert("location", frame=1)
        d.root.location = (x0 - 22, y0, 0.06); d.root.keyframe_insert("location", frame=N)
        for f in range(1, N + 1, 2): d.jump_pose(f, 1 if (f + i) % 4 < 2 else -0.6)
    hero.place((-1, -1.5, 0.06), -90, 1); hero.place((-23, -1.5, 0.06), -90, N); hero.run(1, N, 4, 20, 25); hero.face("shock", 1)
    for f in range(1, N + 1, 2): hero.pose(f, armL=-95, armR=-95, lean=-28, legL=-30 if f % 4 < 2 else 20, legR=20 if f % 4 < 2 else -30, bob=0.2 if f % 4 < 2 else 0)
    cam_move(cam, tgt, 1, N, (-4, -9, 1.6), (-24, -9, 1.6), (-3, -1.5, 1.5), (-23, -1.5, 1.6), 24, 24)
def s16(N):  # bakery: dogs + hero crash through, cakes fly
    baker.place((1100, 4.0, 0), 0); baker.face("shock", 1)
    for i, d in enumerate(dogs):
        d.root.rotation_euler = (0, 0, math.radians(-90)); d.root.location = (1108, -1.5 + (i - 2.5) * 0.6, 0); d.root.keyframe_insert("location", frame=1)
        d.root.location = (1090, -1.5 + (i - 2.5) * 0.6, 0); d.root.keyframe_insert("location", frame=N)
        for f in range(1, N + 1, 2): d.jump_pose(f, 1 if (f + i) % 4 < 2 else -0.6)
    hero.place((1111, -1.0, 0.8), -90, 1); hero.place((1092, -1.0, 0.8), -90, N); hero.pose(armL=-95, armR=-95, lean=-60); hero.face("shock")
    r = random.Random(2)
    for i, c in enumerate(CAKES):
        fs = 2 + i * max(1, N // 9)
        c.keyframe_insert("location", frame=fs); c.location = (c.location[0] + r.uniform(-2, 2), -3 + r.uniform(-1, 1), 5.5); c.rotation_euler = (r.uniform(1, 3), r.uniform(1, 3), 0)
        c.keyframe_insert("location", frame=fs + 5); c.keyframe_insert("rotation_euler", frame=fs + 5)
        c.location = (c.location[0], -5, 0.2); c.keyframe_insert("location", frame=fs + 10)
    cam_move(cam, tgt, 1, N, (1104, -11.5, 2.4), (1099, -11.5, 2.2), (1102, 0, 2.2), (1097, 0, 2.0), 24, 24); shake(1, N, 0.1)
def s17(N):  # baker close, frosting on his face, furious
    baker.place((1100, 3.6, 0), 0); baker.face("evil", 1); baker.talk(1, N - 2, 0.14, 2); baker.pose(1, armR=-90); baker.pose(N, armR=-95, armL=-60)
    SPLAT.hide_render = False
    cam_move(cam, tgt, 1, N, (1100.6, -1.0, 3.5), (1100.3, -0.2, 3.5), (1100, 3.6, 3.3), (1100, 3.6, 3.35), 36, 42)
def s18(N):  # hero close, covered in cake, shocked (1,060)
    hero.place((1100, 0, 0), 0); hero.face("shock", 1); hero.pose(1, armL=-20, armR=-20, armLs=30, armRs=30)
    HSPLAT.hide_render = False
    cam_move(cam, tgt, 1, N, (1100.5, -4.6, 2.5), (1100.2, -3.9, 2.5), (1100, 0, 2.6), (1100, 0, 2.7), 36, 42)
def s19(N):  # door to door with grandma's cookies
    hero.place((12, 7.2, 0.17), 0); hero.face("happy"); hold(cookiebox, hero, 0, (0, -0.45, -1.15)); hero.pose(1, armL=-70)
    for f in range(1, N, 4): hero.pose(f, armL=-70, armR=-100 if f % 8 < 4 else -80)
    cam_move(cam, tgt, 1, N, (16.5, 0.5, 2.0), (15.0, 1.0, 2.2), (12, 8.5, 2.5), (12, 8.5, 2.6), 26, 30)
def s20(N):  # grandma on the sofa, eats the whole box
    gran.place((1300, 2.8, 0.5), 0); gran.face("happy"); gran.pose(1, armL=-60, legL=-80, legR=-80)
    cookiebox.location = (1300.6, 1.9, 1.75); cookiebox.scale = (0.8, 0.8, 0.8)
    for f in range(1, N, 4): gran.pose(f, armL=-60, armR=-150 if f % 8 < 4 else -90, legL=-80, legR=-80, head=8 if f % 8 < 4 else 0)
    gran.talk(1, N, 0.1, 2)
    cam_move(cam, tgt, 1, N, (1302, -3.5, 2.4), (1301.2, -2.8, 2.5), (1300, 2.6, 2.6), (1300, 2.6, 2.7), 30, 34)
def s21(N):  # day three: hero sitting on the curb, sad
    hero.place((2, -4.3, 0.17), 0); hero.pose(1, legL=-80, legR=-80, head=15, armL=-40, armR=-40); hero.root.location.z = -0.5; hero.root.keyframe_insert("location", frame=1)
    hero.face("scared")
    cam_move(cam, tgt, 1, N, (-1.0, -10.8, 2.2), (0.2, -10.3, 2.1), (2, -4, 1.6), (2, -4, 1.6), 28, 32)
def s22(N):  # Benny strolls past, flipping his refund coin
    ben.place((-4, -6.5, 0.17), 90, 1); ben.place((4, -6.5, 0.17), 90, N); ben.walk(1, N, 10); ben.face("happy")
    hold(coins, ben, 1, (0, -0.35, -1.2)); hero.place((2, -4.3, -0.5), 0); hero.pose(legL=-80, legR=-80, head=15); hero.face("evil")
    cam_move(cam, tgt, 1, N, (-2, -14, 1.5), (2, -14, 1.5), (-2, -6, 2.4), (3, -6, 2.4), 28, 28)
def s23(N):  # the poster: TOWN GAME SHOW $1,000
    cam_move(cam, tgt, 1, N, (-3.0, -1.5, 3.0), (-4.0, 2.2, 3.4), (-4.5, 8.4, 3.4), (-4.5, 8.4, 3.4), 30, 38)
def s24(N):  # hero face lights up, determined
    hero.place((0, 0, 0.16), 0); hero.face("surprised", 1); hero.face("determined", N // 2); hero.pose(1); hero.pose(N, armR=-120, armRs=10)
    cam_move(cam, tgt, 1, N, (0.3, -4.8, 2.6), (0.2, -3.8, 2.7), (0, 0, 2.6), (0, 0, 2.7), 36, 46)
def s25(N):  # NIGHT: the whole town at the neon game show, wide crane
    night(); screen_show("title", "purple"); audience("happy"); mayor_host()
    for i, c in enumerate(crowd): cheer(c, 1 + i % 3, N, i)
    cam_move(cam, tgt, 1, N, (-12, 4, 9), (-7, 8, 6), (0, 26, 4), (0, 26, 4.5), 22, 24)
def s26(N):  # neon screens close sweep + TV camera
    night(); screen_show("prize", "blue")
    cam_move(cam, tgt, 1, N, (-9, 19, 3.0), (-5, 20, 3.6), (8, 21, 2.6), (2, 29, 6), 24, 26)
def s27(N):  # the host is the Mayor (spotlight, mic)
    night(); screen_show("title", "purple"); mayor_host(); mayor.talk(1, N, 0.14, 3); mayor.pose(N // 2, armR=-95, armL=-150, armLs=30)
    cam_move(cam, tgt, 1, N, (-5.0, 19.5, 2.4), (-5.6, 20.4, 2.5), (-7, 25.2, 3.9), (-7, 25.2, 4.0), 34, 40)
def s28(N):  # round one: the baker buzzes... wrong
    night(); screen_show("title", "blue"); on_pod(baker, 0, "happy"); on_pod(ben, 1); on_pod(hero, 2, "determined")
    baker.pose(1, armR=-60); baker.pose(N // 3, armR=-40, head=5); buzz_flash(0, N // 3); screen_show("title", "blue")
    TXT["x"].hide_render = True
    baker.face("shock", N // 2)
    cam_move(cam, tgt, 1, N, (-6.5, 21.0, 3.4), (-5.5, 21.6, 3.5), (-4.5, 27, 3.6), (-4.5, 27, 3.7), 30, 34)
def s29(N):  # big red X
    night(); screen_show("x", "red")
    cam_move(cam, tgt, 1, N, (0, 21, 4.5), (0, 22, 5.0), (0, 29.5, 6), (0, 29.5, 6), 30, 36); shake(1, 4, 0.15)
def s30(N):  # round two: Benny out, holds out his hand: refund
    night(); screen_show("x", "red"); on_pod(ben, 1, "evil"); ben.pose(1, armR=-30); ben.pose(N // 3, armR=-85); ben.talk(N // 3, N, 0.12, 2)
    cam_move(cam, tgt, 1, N, (0.7, 22.4, 3.9), (0.4, 23.2, 3.9), (0, 27, 3.9), (0, 27, 4.0), 34, 40)
def s31(N):  # just me and the champion: two podiums
    night(); screen_show("prize", "purple"); on_pod(pick, 0, "evil"); on_pod(hero, 2, "determined"); mayor_host()
    cam_move(cam, tgt, 1, N, (0, 15.5, 2.8), (0, 17, 3.2), (0, 27, 3.3), (0, 27, 3.5), 24, 28)
def s32(N):  # Mrs. Pickles close, smug
    night(); on_pod(pick, 0, "evil"); pick.pose(1, armL=-60, armLs=10); pick.pose(N, armL=-65, head=-5)
    cam_move(cam, tgt, 1, N, (-4.0, 22.8, 4.0), (-4.3, 23.5, 4.0), (-4.5, 27, 4.0), (-4.5, 27, 4.0), 36, 42)
def s33(N):  # hero close, determined
    night(); on_pod(hero, 2, "determined"); hero.pose(1); hero.pose(N, head=-5)
    cam_move(cam, tgt, 1, N, (4.9, 22.9, 4.0), (4.6, 23.6, 3.9), (4.5, 27, 3.85), (4.5, 27, 3.9), 36, 42)
def s34(N):  # last question: Mayor reads the card, spotlight
    night(); screen_show("prize", "blue"); mayor_host(); mayor.face("evil"); mayor.talk(1, N - 2, 0.12, 3); mayor.pose(1, armR=-95, armL=-80)
    cam_move(cam, tgt, 1, N, (-5.2, 20.0, 3.4), (-5.6, 20.6, 3.5), (-7, 25.2, 3.6), (-7, 25.2, 3.7), 30, 34)
def s35(N):  # the whole town holds its breath (frozen faces, slow push)
    night(); screen_show("prize", "blue"); audience("frozen")
    for c in crowd: c.pose(armL=-20, armR=-20)
    cam_move(cam, tgt, 1, N, (2.2, 23.4, 3.3), (1.5, 23.0, 3.2), (0, 15, 2.6), (0, 15, 2.6), 26, 32)
def s36(N):  # screen: HOW MANY WINDOWS?
    night(); screen_show("q", "purple")
    cam_move(cam, tgt, 1, N, (-1.5, 18, 3.0), (-0.5, 20.5, 4.5), (0, 29.5, 6.0), (0, 29.5, 6.0), 26, 32)
def s37(N):  # Mrs. Pickles slams the buzzer: FORTY!
    night(); screen_show("forty", "blue"); on_pod(pick, 0, "evil"); fb = max(2, N // 4)
    pick.pose(1, armR=-120); pick.pose(fb, armR=-60, lean=8); buzz_flash(0, fb); pick.talk(fb, N, 0.18, 2); pick.face("happy", fb + 1)
    cam_move(cam, tgt, 1, N, (-3.0, 23.2, 3.2), (-3.4, 23.8, 3.3), (-4.5, 26.3, 3.3), (-4.5, 26.6, 3.6), 32, 36); shake(fb, fb + 3, 0.12)
def s38(N):  # the crowd goes wild
    night(); screen_show("forty", "blue"); audience("happy")
    for i, c in enumerate(crowd): cheer(c, 1 + i % 3, N, i)
    cam_move(cam, tgt, 1, N, (2.0, 23.6, 3.2), (-1.5, 23.6, 3.4), (0, 14, 2.6), (0, 14, 2.8), 22, 24); shake(1, N, 0.06)
def s39(N):  # WRONG. (red X, everything stops)
    night(); screen_show("x", "red"); on_pod(pick, 0, "shock"); mayor_host(); mayor.face("evil")
    for s in SPOTS: s.data.energy = 2000
    cam_move(cam, tgt, 1, N, (-2.5, 20.0, 3.4), (-2.3, 20.3, 3.4), (-2, 27, 4.0), (-2, 27, 4.0), 24, 26); shake(1, 3, 0.2)
def s40(N):  # hero: thirty-nine
    night(); screen_show("n39", "purple"); on_pod(hero, 2, "happy"); hero.talk(1, N // 2, 0.1, 3); hero.pose(1); hero.pose(N // 3, armR=-110, armRs=5)
    cam_move(cam, tgt, 1, N, (4.9, 22.6, 4.1), (4.7, 23.3, 4.0), (4.5, 27, 3.9), (4.5, 27, 3.95), 34, 40)
def s41(N):  # callback: the taped-up broken window
    night(); x, y, z = WIN[BALLWIN]["pos"]
    for o in SHOW:
        if o.location.y > 28.5 and o.parent is None: o.hide_render = True
    cam_move(cam, tgt, 1, N, (x + 2.5, y - 4.5, z + 1.5), (x + 1.5, y - 3.8, z + 0.8), (x, y, z), (x, y, z), 30, 36)
def s42(N):  # CORRECT! confetti
    night(); screen_show("correct", "green"); audience("happy"); on_pod(hero, 2, "happy"); hero.pose(1, armL=-160, armR=-160, armLs=20, armRs=20)
    for i, c in enumerate(crowd): cheer(c, 1 + i % 3, N, i)
    confetti(1, N + 20)
    cam_move(cam, tgt, 1, N, (-2, 13, 4.5), (0, 15, 5.0), (0, 26, 4), (1, 26, 4.5), 24, 26)
def s43(N):  # fireworks over the clock tower
    night(); screen_show("correct", "green"); fireworks(1, N)
    cam_move(cam, tgt, 1, N, (2, 14, 2.0), (1, 15, 2.6), (0, 33, 18), (0, 33, 21), 22, 22)
def s44(N):  # Benny cries (happy tears)
    night(); ben.place((-2, 20, 0.06), 0); ben.face("happy"); ben.pose(1, armL=-120, armR=-120, head=10); ben.talk(1, N, 0.14, 2)
    confetti(-10, N + 10, -2, 20, 5)
    for i, tr in enumerate(tears):
        sd = -1 if i % 2 else 1; f0 = 1 + (i // 2) * max(2, N // 3)
        tr.location = (-2 + 0.2 * sd, 19.4, 2.85); tr.keyframe_insert("location", frame=f0)
        tr.location = (-2 + 0.32 * sd, 19.35, 2.35); tr.keyframe_insert("location", frame=f0 + 6)
    cam_move(cam, tgt, 1, N, (-1.6, 15.6, 2.6), (-1.8, 16.3, 2.6), (-2, 20, 2.5), (-2, 20, 2.55), 36, 42)
def s45(N):  # hero hands the whole $1,000 back to the Mayor
    night(); screen_show("prize", "green"); hero.place((-2.2, 25.5, 1.4), 55); mayor.place((1.0, 25.5, 1.4), -55); mayor.face("happy"); hero.face("happy")
    hold(cheque, hero, 0, (0, -0.4, -1.1)); hero.pose(1, armL=-30); hero.pose(N // 2, armL=-90)
    cheque.keyframe_insert("location", frame=1)
    cam_move(cam, tgt, 1, N, (-0.6, 19.8, 3.0), (-0.4, 20.6, 3.1), (-0.6, 25.5, 3.4), (-0.6, 25.5, 3.5), 28, 32)
def s46(N):  # Mayor close, beaming
    night(); mayor.place((0, 25.5, 1.4), 0); hold(cheque, mayor, 0, (0, -0.4, -1.1)); mayor.pose(1, armL=-80); mayor.face("happy"); mayor.talk(1, N // 2, 0.12, 3)
    cam_move(cam, tgt, 1, N, (0.5, 21.3, 4.6), (0.3, 22.1, 4.5), (0, 25.5, 4.4), (0, 25.5, 4.5), 34, 40)
def s47(N):  # the Mayor throws his top hat high into the air
    night(); mayor.place((0, 25.5, 1.4), 0); mayor.face("happy"); f_rel = max(2, N // 4)
    mayor.pose(1, armR=-60, armL=-60); mayor.pose(f_rel, armR=-170, armL=-170, armLs=20, armRs=20, bob=0.3)
    hat = mayor.hat; hat.parent = None; hat.location = (0, 25.5, 5.9); hat.keyframe_insert("location", frame=f_rel)
    hat.location = (0.8, 28, 11.5); hat.rotation_euler = (0.6, 2.5, 0); hat.keyframe_insert("location", frame=N); hat.keyframe_insert("rotation_euler", frame=N)
    cam_move(cam, tgt, 1, N, (-2, 18, 2.2), (-1.5, 18.5, 2.4), (0, 25.5, 5.0), (0.5, 28, 10.5), 26, 26)
def s48(N):  # hit + silence: the hat sails... right through window 38 (the tower window)
    night(); x, y, z = WIN[HATWIN]["pos"]; f_hit = max(3, int(N * 0.5))
    hat = mayor.hat; hat.parent = None
    hat.location = (0.5, 26, 13.5); hat.rotation_euler = (0.6, 2.5, 0); hat.keyframe_insert("location", frame=1); hat.keyframe_insert("rotation_euler", frame=1)
    hat.location = (x, y - 0.4, z); hat.rotation_euler = (0.2, 6.0, 0.3); hat.keyframe_insert("location", frame=f_hit); hat.keyframe_insert("rotation_euler", frame=f_hit)
    hat.location = (x, y + 1.5, z); hat.keyframe_insert("location", frame=f_hit + 2)
    shatter(HATWIN, f_hit, 14)
    cam_move(cam, tgt, 1, N, (-3.5, 22, 9), (-3, 23, 10), (1, 31, 12.0), (1.3, 33, 11.6), 34, 38); shake(f_hit, f_hit + 5, 0.15)
def s49(N):  # Mayor close: shock (no hat!)
    night(); mayor.place((0, 25.5, 1.4), 0); mayor.hat.location = OFF; mayor.face("shock"); mayor.pose(1, armL=-160, armR=-160, armLs=30, armRs=30)
    cam_move(cam, tgt, 1, N, (0.4, 21.6, 4.5), (0.2, 22.3, 4.4), (0, 25.5, 4.4), (0, 25.5, 4.5), 36, 42)
def s50(N):  # hero to camera, eyebrow up: if you break it, you pay for it
    night(); hero.place((3, 24.5, 1.4), 0); hero.face("happy", 1); hero.face("evil", N // 2); hero.talk(1, N - 2, 0.08, 3); hero.pose(1); hero.pose(N, armR=-110, armRs=5)
    cam_move(cam, tgt, 1, N, (3.3, 20.6, 4.0), (3.1, 21.4, 3.9), (3, 24.5, 3.85), (3, 24.5, 3.9), 34, 42)
def s51(N):  # wide finale: Mayor turns his pockets out, the hero holds out his hand, pull back over the night town
    night(); screen_show("prize", "purple"); mayor.place((-1.5, 25.5, 1.4), 30); mayor.hat.location = OFF; mayor.face("scared"); mayor.pose(1, armL=-30, armR=-30, armLs=40, armRs=40)
    hero.place((1.5, 25.5, 1.4), -30); hero.face("happy"); hero.pose(1, armR=-85); audience("happy"); broken(HATWIN, True)
    cam_move(cam, tgt, 1, N, (0, 17, 3.5), (0, 8, 9.0), (0, 26, 4.0), (0, 28, 7.0), 26, 24)

T = [("s01", 0.0, s01), ("s02", 1.55, s02), ("s03", 2.6, s03), ("s04", L[1], s04), ("s05", L[1] + 1.2, s05), ("s06", L[2], s06), ("s07", L[2] + 2.3, s07),
     ("s08", L[3], s08), ("s09", L[4], s09), ("s10", L[5], s10), ("s11", L[5] + 1.7, s11), ("s12", L[6], s12), ("s13", L[6] + 1.4, s13),
     ("s14", L[7], s14), ("s15", L[8], s15), ("s16", L[8] + 1.3, s16), ("s17", L[9], s17), ("s18", L[9] + 2.0, s18),
     ("s19", L[10], s19), ("s20", L[10] + 2.1, s20), ("s21", L[11], s21), ("s22", L[11] + 2.0, s22), ("s23", L[12], s23), ("s24", L[12] + 2.6, s24),
     ("s25", L[13], s25), ("s26", L[13] + 1.4, s26), ("s27", L[13] + 2.6, s27), ("s28", L[14], s28), ("s29", L[14] + 1.1, s29), ("s30", L[14] + 2.1, s30),
     ("s31", L[15], s31), ("s32", L[15] + 1.6, s32), ("s33", L[15] + 3.0, s33), ("s34", L[16], s34), ("s35", L[16] + 2.0, s35), ("s36", L[17], s36),
     ("s37", L[18], s37), ("s38", L[18] + 1.7, s38), ("s39", L[19], s39), ("s40", L[20], s40), ("s41", L[20] + 1.5, s41), ("s42", L[21], s42),
     ("s43", L[21] + 1.0, s43), ("s44", L[21] + 2.0, s44), ("s45", L[22], s45), ("s46", L[22] + 2.0, s46), ("s47", L[23], s47), ("s48", L[24] - 0.5, s48),
     ("s49", L[24] + 1.0, s49), ("s50", L[25], s50), ("s51", L[25] + 2.4, s51)]
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
        sc.frame_set(max(1, int(N * 0.6))); sc.render.filepath = f"{W}/stills/{sid}.png"; bpy.ops.render.render(write_still=True)
        continue
    os.makedirs(d, exist_ok=True)
    sc.frame_start, sc.frame_end = 1, N; sc.render.filepath = f"{d}/"
    t = time.time(); bpy.ops.render.render(animation=True)
    open(f"{d}/done", "w").write(str(N)); print(sid, N, "frames", round(time.time() - t), "s", flush=True)
