"""Oddwick daily Short 2026-11-21: "Last One Touching It Wins $10,000" (Blocktown house style, owner 2026-11-20).
Sunny town square with a GIANT donut in front of the neon game-show stage (countdown on the big screen), rain, night,
Mrs. Pickles' blanket trick and a pigeon that wins. Same cast as the house-style sample (hero, Benny, baker, Grandma, Mayor,
Mrs. Pickles) = our recurring Blocktown cast.
python3.13 donut_shots.py [sid ...] [--still]   -> /home/claude/work/<slug>/shots/<sid>/####.png (resumable)"""
import sys, os, json, math, random, time, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move

SLUG = "2026-11-21-last-one-touching-it-wins"; FPS = 15
W = f"/home/claude/work/{SLUG}"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; END = vo["total"] + 0.5
PREV = "--still" in sys.argv
RES = (216, 384) if PREV else (432, 768)
sc, cam, tgt = lib.setup(res=RES, samples=4 if PREV else 10, fps=FPS)
sc.render.threads_mode = "AUTO"
town = lib.build_town()
lib.build_bedroom(300)
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
def torus(name, loc, R, r, m, zs=1.0):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=56, minor_segments=18, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = (1, 1, zs); o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o

# ---------------------------------------------------------------- the GIANT donut on a pedestal (centre of the square)
DC = (0.0, 17.0); DZ = 1.45
ped = cyl("pedestal", (DC[0], DC[1], 0.35), 2.3, 0.7, mat("ped", "#f4f1e8", 0.5), verts=40)
cyl("pedstripe", (DC[0], DC[1], 0.62), 2.33, 0.12, mat("pedred", "#e8423f", 0.5), verts=40)
donut = empty("donut", (DC[0], DC[1], DZ))
dough = torus("dough", (0, 0, 0), 2.0, 0.75, mat("dough", "#d9933f", 0.65)); dough.parent = donut; dough.location = (0, 0, 0)
icing = torus("icing", (0, 0, 0), 2.0, 0.78, mat("icingpink", "#ff7fb8", 0.3), 0.55); icing.parent = donut; icing.location = (0, 0, 0.3)
rs = random.Random(11); scol = ["#ffffff", "#40f0ff", "#ffe14a", "#5fff7a", "#8a5aff"]
for i in range(70):
    a = rs.uniform(0, 2 * math.pi); rr = 2.0 + rs.uniform(-0.55, 0.55)
    cube(f"spr{i}", (rr * math.cos(a), rr * math.sin(a), 0.3 + 0.78 * 0.55 * math.sqrt(max(0, 1 - ((rr - 2) / 0.78) ** 2)) + 0.02),
         (0.32, 0.08, 0.08), mat(f"spr{i % 5}", scol[i % 5], 0.4, 0.3), 0, donut, (0, 0, rs.uniform(0, 3)))
BITE = sphere("bite", (0, 0, -500), (0.75, 0.75, 0.7), mat("bitehole", "#f2e2c0", 0.8))   # pale crumb hollow after Grandma's bite
def ring(a_deg, R=3.5):
    a = math.radians(a_deg); return (DC[0] + R * math.sin(a), DC[1] - R * math.cos(a), 0.06), a_deg + 180

# ---------------------------------------------------------------- night game-show stage behind the donut (screens = countdown)
SHOW = []
def S_(o): SHOW.append(o); return o
plaza = cube("plaza", (0, 22, 0.02), (40, 22, 0.06), mat("plaza", "#c9b79a", 0.85), 0)
S_(cube("stage", (0, 26.5, 0.7), (16, 6, 1.4), mat("stagefloor", "#1c1830", 0.3, metal=0.2), 0.05))
S_(cube("stage_edge", (0, 23.48, 1.3), (16.2, 0.12, 0.2), mat("neon_cyan", "#40f0ff", 0.3, 10, "#40f0ff"), 0))
S_(cube("stage_edge2", (0, 23.48, 0.25), (16.2, 0.12, 0.15), mat("neon_pink", "#ff4fd0", 0.3, 10, "#ff4fd0"), 0))
S_(cube("screenwall", (0, 29.8, 5.0), (17, 0.6, 9.6), mat("screenwall", "#120e22", 0.4), 0.05))
scr_cols = {"blue": mat("scr_blue", "#2a3cff", 0.3, 3.0, "#3a5cff"), "red": mat("scr_red", "#ff2a3a", 0.3, 4.0, "#ff2a3a"),
            "green": mat("scr_green", "#2aff6a", 0.3, 4.0, "#2aff6a"), "purple": mat("scr_purple", "#8a2aff", 0.3, 3.5, "#9a3aff"),
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
for key, body, size, col in (("title", "DONUT\nCHALLENGE", 1.25, "#ffffff"), ("prize", "$10,000", 1.9, "#ffe14a"),
                             ("rules", "NO SLEEP\nNO SNACKS", 1.2, "#ffffff"), ("h1", "HOUR 1\n49 LEFT", 1.25, "#ffffff"),
                             ("h3", "HOUR 3\n48 LEFT", 1.25, "#ffffff"), ("h5", "HOUR 5\n18 LEFT", 1.25, "#ffffff"),
                             ("h9", "HOUR 9", 1.6, "#ffffff"), ("h12", "HOUR 12\n3 LEFT", 1.25, "#ffffff"), ("h16", "HOUR 16", 1.6, "#ffffff"),
                             ("left2", "2 LEFT", 1.9, "#ffffff"), ("out", "OUT!", 2.6, "#ffffff"), ("dq", "DISQUALIFIED", 0.95, "#ffffff"),
                             ("winner", "WINNER\n???", 1.3, "#ffffff"), ("pigeon", "WINNER:\nPIGEON", 1.25, "#ffe14a")):
    TXT[key] = S_(mktext("scr_" + key, body, (0, 29.36, 6.0), size, col, 4.0, extrude=0.01))
# confetti + fireworks
CONF = []
rr = random.Random(7); ccols = ["#ff4fd0", "#40f0ff", "#ffe14a", "#5fff7a", "#ff7a3a", "#ffffff"]
for i in range(90): CONF.append(cube(f"conf{i}", (0, 0, -500), (0.22, 0.04, 0.32), mat(f"conf{i % 6}", ccols[i % 6], 0.5, 1.5), 0))
FW = []
for b, (x, z, col) in enumerate(((-9, 24, "#ff4fd0"), (0, 30, "#ffe14a"), (9, 25, "#40f0ff"))):
    FW.append((x, z, [sphere(f"fw{b}_{i}", (0, 0, -500), (0.25, 0.25, 0.25), mat(f"fwm{b}", col, 0.3, 30, col), seg=6) for i in range(26)]))
# rain streaks (only in the rain shots)
RAIN = [cube(f"rain{i}", (0, 0, -500), (0.05, 0.05, 1.1), mat("rain", "#e6f3ff", 0.1, 3.0, "#e6f3ff"), 0) for i in range(160)]
# party bunting over the square (birthday)
for i in range(16):
    x = -12 + i * 1.6
    cube(f"bunt{i}", (x, 21.5, 9.6 - 0.9 * math.sin(math.pi * i / 15)), (0.9, 0.05, 0.9), mat(f"bunt{i % 4}", ["#ff4fd0", "#ffe14a", "#40f0ff", "#5fff7a"][i % 4], 0.6, 0.4), 0, None, (0, math.radians(45), 0))

# ---------------------------------------------------------------- Mrs. Pickles' camp: chair, blanket, tiny TV, then the dummy
PK_POS, PK_YAW = ring(135, 3.8)
camp = empty("camp", PK_POS); camp.rotation_euler = (0, 0, math.radians(PK_YAW))
cm = mat("chair", "#3f8fd8", 0.5)
chair = empty("chair", (0, 0, 0), camp)
cube("ch_seat", (0, 0.2, 0.9), (1.4, 1.3, 0.2), cm, 0.05, chair); cube("ch_back", (0, 0.85, 1.7), (1.4, 0.15, 1.5), cm, 0.05, chair)
for sx in (-0.6, 0.6):
    for sy in (-0.4, 0.8): cube(f"ch_leg{sx}{sy}", (sx, sy, 0.45), (0.1, 0.1, 0.9), mat("chleg", "#dddddd", 0.3, metal=0.7), 0, chair)
blanket = cube("blanket_lap", (0, -0.1, 1.25), (1.7, 1.6, 0.5), mat("plaid", "#b0263a", 0.9), 0.2, camp)
tv = empty("tinytv", (0, 0, 0), camp)
cube("tv_body", (0.0, -0.5, 1.95), (0.8, 0.5, 0.6), mat("tvbody", "#2a2a33", 0.4), 0.06, tv)
cube("tv_scr", (0.0, -0.76, 1.95), (0.62, 0.03, 0.44), mat("tvscr", "#7fe6ff", 0.2, 6, "#7fe6ff"), 0.0, tv)
point("tvglow", (0, -1.4, 2.0), "#7fe6ff", 60, 0.3, tv)
mound = cube("mound", (0, 0.2, 1.95), (1.6, 1.6, 2.1), mat("plaid", "#b0263a", 0.9), 0.55, camp)    # blanket over "her" head
wig = empty("wig", (0, 0.2, 3.0), camp)
cube("wig_top", (0, 0, 0.05), (1.0, 1.0, 0.3), mat("wighair", "#c8c8c8", 0.8), 0.1, wig); cube("wig_bun", (0, 0.2, 0.35), (0.55, 0.55, 0.45), mat("wighair", "#c8c8c8", 0.8), 0.15, wig)
for sd in (-1, 1): cube(f"wig_gl{sd}", (0.22 * sd, -0.52, -0.1), (0.36, 0.03, 0.06), mat("glassfr", "#111111", 0.3), 0, wig)
pillows = empty("pillows", (0, 0, 0), camp)
for i, (z, s) in enumerate(((1.25, 1.3), (1.85, 1.1), (2.4, 0.9))):
    cube(f"pil{i}", (0, 0.25, z), (s, 0.9 * s, 0.5), mat("pillow", "#f2f2f2", 0.7), 0.22, pillows, (0, 0, math.radians((i - 1) * 12)))
glove_arm = empty("glovearm", (0, 0, 0), camp)
cube("gl_sleeve", (0.45, -0.9, 2.15), (0.4, 1.6, 0.4), mat("pkgreen", "#5c9a3a", 0.7), 0.08, glove_arm)
gm = mat("glove", "#ffd23a", 0.35)
cube("gl_palm", (0.45, -1.85, 2.3), (0.5, 0.45, 0.22), gm, 0.08, glove_arm)
for k in range(4): cube(f"gl_f{k}", (0.27 + k * 0.12, -2.22, 2.27), (0.1, 0.35, 0.12), gm, 0.04, glove_arm)
for k in range(3): cube(f"gl_tape{k}", (0.45, -1.75 - k * 0.18, 2.42), (0.75, 0.08, 0.02), mat("tape", "#e8d9a8", 0.8), 0, glove_arm, (0, 0, math.radians(15 * (k - 1))))
_t = math.radians(PK_YAW); GW = (PK_POS[0] + 0.45 * math.cos(_t) + 1.85 * math.sin(_t), PK_POS[1] + 0.45 * math.sin(_t) - 1.85 * math.cos(_t), 2.3)
pk_items = dict(chair=chair, blanket=blanket, tv=tv, mound=mound, wig=wig, pillows=pillows, glove=glove_arm)

# ---------------------------------------------------------------- pizza, cheque, Zzz
pizza = empty("pizza", (0, 0, -500))
for i in range(3): cube(f"pz_box{i}", (0, 0, i * 0.22), (1.6, 1.6, 0.2), mat("pzbox", "#e8d0a0", 0.8), 0.02, pizza)
cube("pz_lid", (0, 0.8, 1.2), (1.6, 0.06, 1.6), mat("pzbox", "#e8d0a0", 0.8), 0.02, pizza)
cyl("pz_pie", (0, 0, 0.56), 0.7, 0.06, mat("cheese", "#ffcf4a", 0.5), parent=pizza, verts=24)
for k in range(6): cyl(f"pz_pep{k}", (0.42 * math.cos(k), 0.42 * math.sin(k), 0.6), 0.12, 0.03, mat("pep", "#c8282f", 0.5), parent=pizza, verts=12)
STEAM = [sphere(f"steam{i}", (0, 0, -500), (0.18, 0.18, 0.25), mat("steam", "#ffffff", 0.9, 0.6), seg=8) for i in range(6)]
cheque = empty("cheque", (0, 0, -500))
cube("chq", (0, 0, 0.4), (2.6, 0.06, 1.2), mat("chq", "#e8ffe8", 0.6), 0.03, cheque)
o = mktext("chqt", "$10,000", (0, -0.05, 0.4), 0.55, "#1a7a3a", 0.0, extrude=0.01); o.parent = cheque; o.location = (0, -0.05, 0.4)
ZZ = [mktext(f"zz{i}", "Z", (0, 0, -500), 0.45 + 0.12 * i, "#ffffff", 1.0) for i in range(3)]
crumbs = [cube(f"crumb{i}", (0, 0, -500), (0.14, 0.14, 0.12), mat("dough", "#d9933f", 0.65), 0.03) for i in range(10)]

# ---------------------------------------------------------------- pigeon (our own blocky bird)
class Pigeon:
    def __init__(self):
        g, dg, w = mat("pg_body", "#8f95a8", 0.7), mat("pg_dark", "#5d6275", 0.7), mat("pg_neck", "#5fb89a", 0.4, 0.2)
        self.root = empty("pigeon", (0, 0, -500))
        cube("pg_torso", (0, 0.1, 0.45), (0.55, 0.85, 0.55), g, 0.18, self.root)
        cube("pg_tail", (0, 0.65, 0.5), (0.4, 0.45, 0.12), dg, 0.05, self.root, (math.radians(-20), 0, 0))
        self.wings = []
        for sd in (-1, 1):
            p = empty(f"pg_wp{sd}", (0.28 * sd, 0.05, 0.6), self.root)
            cube(f"pg_wing{sd}", (0.08 * sd, 0.15, -0.05), (0.12, 0.7, 0.4), dg, 0.05, p); self.wings.append(p)
            cube(f"pg_leg{sd}", (0.12 * sd, 0.1, 0.1), (0.07, 0.07, 0.22), mat("pg_leg", "#ff6f6f", 0.5), 0, self.root)
        self.neck = empty("pg_neck", (0, -0.25, 0.7), self.root)
        cube("pg_collar", (0, 0, 0.05), (0.42, 0.42, 0.25), w, 0.1, self.neck)
        cube("pg_head", (0, -0.05, 0.32), (0.44, 0.46, 0.42), g, 0.14, self.neck)
        cube("pg_beak", (0, -0.36, 0.28), (0.12, 0.22, 0.1), mat("pg_beak", "#ffb43a", 0.4), 0.03, self.neck)
        for sd in (-1, 1):
            e = sphere(f"pg_eye{sd}", (0.17 * sd, -0.25, 0.4), (0.09, 0.05, 0.11), mat("sclera", "#ffffff", 0.35, 0.25), self.neck, 10)
            sphere(f"pg_pup{sd}", (0.0, -0.8, -0.05), (0.55, 0.6, 0.6), mat("eyeblack", "#141414", 0.25), e, 8)
        self.hat = empty("pg_hat", (0, -0.05, 0.58), self.neck); self.hat.hide_render = True
        cyl("pg_hatb", (0, 0, 0), 0.32, 0.04, mat("hat", "#15151c", 0.4), parent=self.hat, verts=16).hide_render = True
        cyl("pg_hatc", (0, 0, 0.2), 0.2, 0.4, mat("hat", "#15151c", 0.4), parent=self.hat, verts=16).hide_render = True
    def peck(self, f0, f1, rate=4, deep=40):
        f = f0; k = 0
        while f <= f1:
            self.neck.rotation_euler = (math.radians(deep if k % 2 else 0), 0, 0); self.neck.keyframe_insert("rotation_euler", frame=f); f += rate; k += 1
    def bob(self, f0, f1, rate=5):
        f = f0; k = 0
        while f <= f1:
            self.neck.location = (0, -0.25 - (0.12 if k % 2 else 0), 0.7); self.neck.keyframe_insert("location", frame=f); f += rate; k += 1
    def flap(self, f0, f1, rate=2):
        f = f0; k = 0
        while f <= f1:
            for sd, p in zip((-1, 1), self.wings):
                p.rotation_euler = (0, math.radians(sd * (70 if k % 2 else -10)), 0); p.keyframe_insert("rotation_euler", frame=f)
            f += rate; k += 1
        for p in self.wings: p.rotation_euler = (0, 0, 0); p.keyframe_insert("rotation_euler", frame=f1 + 1)
pg = Pigeon()
PG_SPOT = (DC[0] - 1.2, DC[1] + 1.55, DZ + 0.72)   # standing on top of the icing, back-left (seen from the front camera)

# ---------------------------------------------------------------- cast
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
sweat = [sphere(f"sweat{i}", (0, 0, -500), (0.07, 0.04, 0.11), mat("tear", "#6fc8ff", 0.1, 2.0, "#6fc8ff"), seg=8) for i in range(4)]
crowd = []
CC = [("#3f8fd8", "#6b3f22"), ("#e86fb0", "#1d1310"), ("#57b65a", "#e0c070"), ("#8b4fb0", "#6b3f22"), ("#e8823f", "#1d1310"),
      ("#2fb0a8", "#e0702e"), ("#c94a4a", "#3a2414"), ("#6a7ad8", "#eeeeee"), ("#f2c53d", "#3a2414"), ("#ff8fb0", "#1d1310"),
      ("#4ac0e8", "#3a2414"), ("#a0d040", "#1d1310"), ("#e85a3a", "#e0c070"), ("#7a5ad8", "#1d1310")]
for i, (top, hair) in enumerate(CC):
    crowd.append(lib.Char(f"cr{i}", skin=["#f3c89a", "#c98d62", "#8d5a3b", "#e9b892"][i % 4], top=top, pants=["#3b3b55", "#c9b48a", "#2f4a7a"][i % 3],
                          hair=hair, hair_style="spiky" if i % 3 == 0 else "flat", kid=i % 2 == 0, **K))
fill = point("camfill", (0.6, 0.4, 0.2), "#ffe6cc", 160, 1.0, cam)
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
OFF = (0, 0, -500)
CAST = [hero, ben, baker, gran, mayor, pick] + crowd
# ring slots (degrees around the donut; 0 = front, nearest the camera; 180 = back, facing the camera)
A_HERO, A_GRAN, A_BEN, A_BAKER = 180, 225, 250, 110

def day(rain=False):
    bg.inputs["Color"].default_value = (*lib.srgb("#9aa6b8" if rain else "#8fc8ff"), 1); bg.inputs["Strength"].default_value = 1.0 if rain else 1.5
    sun.data.energy = 1.6 if rain else 4.5; sun.data.color = lib.srgb("#dfe6f5" if rain else "#fff0d8"); sun.rotation_euler = (math.radians(50), 0, math.radians(215))
    for l in STREETLAMPS: l.data.energy = 0
    for o in SHOW: o.hide_render = False          # the stage + countdown screens stand on the square all day
    for s in SPOTS: s.data.energy = 0
    sc.objects["stagefill"].data.energy = 0
    for k, o in TXT.items(): o.hide_render = True
    sc.view_settings.exposure = 0.45 if rain else 0.3; fill.data.energy = 160
def night():
    bg.inputs["Color"].default_value = (*lib.srgb("#2a2470"), 1); bg.inputs["Strength"].default_value = 0.9
    sun.data.energy = 0.9; sun.data.color = lib.srgb("#9aa8ff"); sun.rotation_euler = (math.radians(55), 0, math.radians(200))
    for l in STREETLAMPS: l.data.energy = 1500
    for o in SHOW: o.hide_render = False
    for k, o in TXT.items(): o.hide_render = True
    for s in SPOTS: s.data.energy = 7000
    sc.objects["stagefill"].data.energy = 2500
    sc.view_settings.exposure = 0.55; fill.data.energy = 320
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
    for c in CAST: c.place(OFF); c.pose(); c.face("neutral")
    screen.data.materials[0] = scr_cols["blue"]
    cam.data.lens = 28; cam.delta_location = (0, 0, 0)
    camp.location = OFF
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
def sleep_face(c, f=None):
    c.face("neutral", f)
    for e in c.eyes:
        e.scale = (e.scale[0], e.scale[1], e.scale[2] * 0.12)
        if f is not None: e.keyframe_insert("scale", frame=f)
def touch(c, a_deg, face="determined", R=3.5, arm=-78, f=None):
    loc, yaw = ring(a_deg, R); c.place(loc, yaw, f); c.pose(f, armR=arm, armL=-10); c.face(face, f)
def players(n=14, face="determined", skip=()):
    """fill the ring with townsfolk, each with one hand on the donut"""
    slots = [a for a in range(0, 360, 24) if all(abs((a - b + 180) % 360 - 180) > 16 for b in skip)]
    for c, a in zip(crowd[:n], slots): touch(c, a, face if crowd.index(c) % 3 else "happy", 3.6 if crowd.index(c) % 2 else 3.4)
def audience(face="happy", n=10, y0=9.5):
    for i, c in enumerate(crowd[:n]):
        x = -8 + (i % 5) * 4.0 + (1.6 if i // 5 else 0); y = y0 - (i // 5) * 2.6 + (i % 2) * 0.5
        c.place((x, y, 0.06), 180 - x * 2.5); c.face(face)
def mayor_host(face="happy"):
    mayor.place((-5.5, 25.2, 1.4), -20); hold(mic, mayor, 1); mayor.pose(armR=-95); mayor.face(face)
def pigeon_on(f=None):
    pg.root.location = PG_SPOT; pg.root.rotation_euler = (0, 0, math.radians(20))
    if f is not None: pg.root.keyframe_insert("location", frame=f)
def pickles_camp(stage):
    """stage: 'chair' | 'blanket' | 'tv' (real Pickles) | 'mound' (dummy, covered) | 'reveal' (pillows + wig + glove)"""
    camp.location = PK_POS
    for k, o in pk_items.items(): o.hide_render = True
    for o in (chair,): o.hide_render = False
    for ch in chair.children: ch.hide_render = False
    def show(o, on=True):
        o.hide_render = not on
        for ch in o.children_recursive: ch.hide_render = not on
    for o in pk_items.values(): show(o, False)
    show(chair, stage != "none")
    if stage in ("chair", "blanket", "tv"):
        loc = (PK_POS[0], PK_POS[1], PK_POS[2] - 0.35); pick.place(loc, PK_YAW); pick.pose(armR=-62, armL=-30, legL=-85, legR=-85); pick.face("evil")
        show(blanket, stage in ("blanket", "tv")); show(tv, stage == "tv")
    elif stage == "mound":
        show(mound); show(wig); show(glove_arm); show(tv)
        wig.location = (0, 0.25, 3.05)
    elif stage == "reveal":
        show(pillows); show(wig); show(glove_arm); wig.location = (0, 0.25, 2.75)
def rain(N, cx=0, cy=14, sp=16):
    r = random.Random(9)
    for d in RAIN:
        x, y = cx + r.uniform(-sp, sp), cy + r.uniform(-sp * 0.8, sp * 0.4); P = 4; ph = r.randrange(P)
        for f in range(1 - ph, N + P, P):
            d.location = (x, y, 13); d.keyframe_insert("location", frame=f); d.location = (x - 0.4, y, -0.5); d.keyframe_insert("location", frame=f + P - 1)
        if d.animation_data:
            for fc in d.animation_data.action.fcurves if hasattr(d.animation_data.action, "fcurves") else []:
                for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
def confetti(f0, f1, cx=0, cy=20, spread=10):
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
def zzz(f0, f1, base):
    for i, z in enumerate(ZZ):
        s0 = f0 + i * 5
        z.location = base; z.keyframe_insert("location", frame=s0); z.location = (base[0] + 0.6 + 0.3 * i, base[1], base[2] + 1.6 + 0.4 * i); z.keyframe_insert("location", frame=min(f1, s0 + 18))
def hpos(a, R=3.5, z=0):
    p, _ = ring(a, R); return (p[0], p[1], z)

# ---------------------------------------------------------------- shots
def s01(N):  # HOOK: low wide, sunny square, a ring of townsfolk all touching a GIANT donut, neon screen $10,000 behind
    players(14, skip=(A_HERO,)); touch(hero, A_HERO); scr("prize", "pink"); mayor_host()
    cam_move(cam, tgt, 1, N, (-0.8, 8.5, 9.5), (0.3, 10.8, 8.0), (0, 17.5, 1.2), (0, 19.5, 2.6), 22, 24)
def s02(N):  # Mayor close, birthday grin, mic
    mayor_host(); mayor.talk(1, N - 2, 0.12, 3); mayor.pose(N // 2, armR=-95, armL=-150, armLs=30); scr("title", "purple")
    cam_move(cam, tgt, 1, N, (-4.2, 20.0, 3.4), (-4.7, 20.9, 3.6), (-5.5, 25.2, 3.9), (-5.5, 25.2, 4.0), 34, 40)
def s03(N):  # hands on icing, close: everyone touching it
    players(14, skip=(A_HERO,)); touch(hero, A_HERO)
    cam_move(cam, tgt, 1, N, (-0.6, 17.2, 5.6), (0.6, 17.0, 5.2), (2.4, 15.3, 2.0), (2.8, 15.8, 2.0), 26, 28)
def s04(N):  # hero close (back of the ring, facing camera), hand on the donut, determined
    touch(hero, A_HERO, "determined"); players(14, skip=(A_HERO,)); hero.pose(N, armR=-80, head=-5)
    p = hpos(A_HERO)
    cam_move(cam, tgt, 1, N, (p[0] + 0.5, p[1] - 4.3, 2.8), (p[0] + 0.2, p[1] - 3.6, 2.7), (p[0], p[1], 2.55), (p[0], p[1], 2.6), 36, 42)
def s05(N):  # high crane over the ring: fifty people, one donut
    players(14, skip=(A_HERO,)); touch(hero, A_HERO); scr("rules", "blue")
    cam_move(cam, tgt, 1, N, (6, 6, 15), (2, 9, 13), (0, 17, 1.0), (0, 17.5, 1.0), 24, 26)
def s06(N):  # big screen: NO SLEEP / NO SNACKS
    scr("rules", "red")
    cam_move(cam, tgt, 1, N, (-1.5, 18.5, 3.5), (-0.6, 20.8, 4.6), (0, 29.5, 6.0), (0, 29.5, 6.0), 26, 32)
def s07(N):  # hero close, deadpan: I'm eleven
    touch(hero, A_HERO, "neutral"); hero.pose(N // 2, armR=-78, head=8); hero.face("evil", N - 2)
    p = hpos(A_HERO)
    cam_move(cam, tgt, 1, N, (p[0] - 0.4, p[1] - 3.9, 2.55), (p[0] - 0.2, p[1] - 3.4, 2.55), (p[0], p[1], 2.55), (p[0], p[1], 2.6), 40, 46)
def s08(N):  # flashback gag on the street: rock-paper-scissors, Benny wins, hero face falls
    hero.place((-1.1, -1, 0.06), 70); ben.place((1.1, -1, 0.06), -70); hero.face("determined", 1); ben.face("happy", 1)
    for k, f in enumerate((1, 4, 7)):
        hero.pose(f, armR=-60 if k % 2 else -110); ben.pose(f, armR=-60 if k % 2 else -110)
    hero.pose(10, armR=-85); ben.pose(10, armR=-85, armRs=10); hero.face("shock", 11); ben.face("evil", 11); ben.pose(N, armR=-85, armL=-150, armLs=30)
    cam_move(cam, tgt, 1, N, (0.5, -6.5, 2.4), (0.2, -5.6, 2.3), (0, -1, 2.3), (0, -1, 2.4), 32, 36)
def s09(N):  # HOUR 1: the baker lets go, throws up his hands and walks off
    scr("h1", "blue"); players(10, skip=(A_HERO, A_BAKER)); touch(hero, A_HERO)
    loc, yaw = ring(A_BAKER); baker.place(loc, yaw, 1); baker.pose(1, armR=-78); baker.face("neutral", 1)
    fl = max(2, N // 3); baker.pose(fl, armR=-160, armL=-160, armLs=25, armRs=25); baker.face("happy", fl)
    baker.place(loc, yaw, fl); baker.place((loc[0] + 4, loc[1] - 3, loc[2]), yaw - 120, N); baker.walk(fl + 1, N, 8)
    cam_move(cam, tgt, 1, N, (0.2, 16.0, 4.4), (0.6, 16.6, 4.2), (3.3, 18.2, 2.8), (4.6, 16.5, 2.6), 28, 30)
def s10(N):  # baker close, bored: he sees donuts all day
    baker.place((6, 13, 0.06), 20); baker.face("neutral", 1); baker.talk(1, N - 2, 0.1, 3); baker.pose(1, armL=-30, armR=-30); baker.pose(N, armL=-35, armR=-35, head=-8)
    cam_move(cam, tgt, 1, N, (7.5, 9.2, 3.4), (7.2, 9.9, 3.4), (6, 13, 3.3), (6, 13, 3.35), 36, 42)
def s11(N):  # HOUR 3: Benny lets go to scratch his nose
    scr("h3", "blue"); loc, yaw = ring(A_BEN); ben.place(loc, yaw); ben.pose(1, armR=-78); ben.face("neutral", 1)
    fl = max(2, N // 3)
    for f in range(fl, N + 1, 3): ben.pose(f, armR=-30, armL=-150 if (f // 3) % 2 else -140, armLs=-35, head=-6)
    ben.face("happy", fl); touch(gran, A_GRAN, "happy")
    cam_move(cam, tgt, 1, N, (loc[0] + 3.2, loc[1] - 2.6, 3.1), (loc[0] + 2.8, loc[1] - 2.1, 3.1), (loc[0], loc[1], 2.7), (loc[0], loc[1], 2.75), 32, 38)
def s12(N):  # Benny begs the Mayor for a do-over; Mayor shakes his head
    ben.place((-1.3, 22.4, 0.06), 140); ben.face("scared"); ben.pose(1, armL=-100, armR=-100, armLs=-20, armRs=-20); ben.talk(1, N // 2, 0.12, 2)
    mayor.place((0.8, 25.2, 1.4), -37); mayor.face("evil")
    for f in range(1, N + 1, 4): mayor.pose(f, armL=-45, armR=-45, armLs=-40, armRs=-40, headyaw=20 if (f // 4) % 2 else -20)
    cam_move(cam, tgt, 1, N, (3.5, 18.5, 2.4), (3.0, 19.2, 2.6), (-0.3, 24, 3.0), (-0.3, 24, 3.1), 28, 32)
def s13(N):  # HOUR 5: rain starts, grey sky, everyone flinches
    day(True); scr("h5", "blue"); players(14, "scared", skip=(A_HERO,)); touch(hero, A_HERO, "scared"); rain(N)
    cam_move(cam, tgt, 1, N, (3, 6.5, 4.8), (1.5, 7.5, 4.4), (0, 17, 2.4), (0, 17, 2.8), 24, 26)
def s14(N):  # thirty people run home down the rainy street
    day(True); rain(N, -4, 0, 18)
    for i, c in enumerate(crowd[:12]):
        x0 = 2 + (i % 4) * 1.6; y0 = -2.5 + (i // 4) * 1.6
        c.place((x0, y0, 0.06), -90, 1); c.place((x0 - 16, y0, 0.06), -90, N); c.run(1, N, 4, 40, 15); c.face("shock")
        c.pose(1, armL=-160, armR=-160)
    cam_move(cam, tgt, 1, N, (-14, -3.2, 1.8), (-17, -3.2, 2.0), (-4, -1, 2.0), (-9, -1, 2.0), 26, 26)
def s15(N):  # HOUR 9: Grandma asleep standing up, still holding on
    scr("h9", "blue"); loc, yaw = ring(A_GRAN); gran.place(loc, yaw); gran.pose(armR=-78, head=18); sleep_face(gran)
    for f in range(1, N + 1, 8): gran.pose(f, armR=-78, head=18 if (f // 8) % 2 else 24, lean=4 if (f // 8) % 2 else 7)
    zzz(1, N, (loc[0] + 0.4, loc[1], 3.4))
    cam_move(cam, tgt, 1, N, (loc[0] + 2.8, loc[1] - 3.8, 3.2), (loc[0] + 2.4, loc[1] - 3.3, 3.1), (loc[0], loc[1], 2.8), (loc[0], loc[1], 2.85), 30, 36)
def s16(N):  # Grandma close: Zzz (eyes shut, mouth open)
    loc, yaw = ring(A_GRAN); gran.place(loc, yaw); gran.pose(armR=-78, head=20); sleep_face(gran); gran.talk(1, N, 0.14, 6)
    zzz(1, N, (loc[0] + 0.4, loc[1], 3.3))
    d = (math.sin(math.radians(A_GRAN)), -math.cos(math.radians(A_GRAN)))
    cam_move(cam, tgt, 1, N, (loc[0] - d[0] * 3.6, loc[1] - d[1] * 3.6 - 0.4, 3.2), (loc[0] - d[0] * 3.0, loc[1] - d[1] * 3.0 - 0.3, 3.2), (loc[0], loc[1], 3.0), (loc[0], loc[1], 3.05), 34, 40)
def s17(N):  # Mayor checks with a magnifying squint, then thumbs up: it counts
    mayor.place((-2.8, 22.6, 0.06), 0); mayor.face("evil", 1); mayor.pose(1, armR=-40, lean=10); fh = max(2, N // 2)
    mayor.pose(fh, armR=-140, armRs=10, lean=0); mayor.face("happy", fh); mayor.talk(fh, N, 0.12, 3)
    loc, yaw = ring(A_GRAN); gran.place(loc, yaw); gran.pose(armR=-78, head=20); sleep_face(gran)
    cam_move(cam, tgt, 1, N, (-5.8, 15.0, 2.8), (-5.2, 15.6, 2.9), (-2.6, 21.2, 3.0), (-2.6, 21.2, 3.2), 28, 32)
def s18(N):  # a pigeon flaps down and lands on the donut
    pigeon_on(); fl = max(3, int(N * 0.6))
    pg.root.location = (PG_SPOT[0] - 3, PG_SPOT[1] + 2, PG_SPOT[2] + 5); pg.root.keyframe_insert("location", frame=1)
    pg.root.location = PG_SPOT; pg.root.keyframe_insert("location", frame=fl); pg.flap(1, fl); pg.bob(fl + 1, N)
    touch(gran, A_GRAN); sleep_face(gran); touch(hero, A_HERO, "neutral")
    cam_move(cam, tgt, 1, N, (-3.5, 12.5, 2.6), (-3.0, 13.2, 2.8), (PG_SPOT[0] - 1, PG_SPOT[1], PG_SPOT[2] + 1.5), PG_SPOT, 30, 34)
def s19(N):  # pigeon close, head bobbing; nobody cares
    pigeon_on(); pg.bob(1, N, 4); touch(hero, A_HERO, "neutral"); scr("h9", "blue")
    cam_move(cam, tgt, 1, N, (PG_SPOT[0] - 0.4, PG_SPOT[1] - 2.6, PG_SPOT[2] + 0.6), (PG_SPOT[0] - 0.2, PG_SPOT[1] - 2.1, PG_SPOT[2] + 0.6),
             (PG_SPOT[0], PG_SPOT[1], PG_SPOT[2] + 0.55), (PG_SPOT[0], PG_SPOT[1], PG_SPOT[2] + 0.6), 40, 46)
def s20(N):  # NIGHT: neon stage, three players left around the donut, empty square
    night(); scr("h12", "purple"); pigeon_on(); touch(hero, A_HERO); touch(gran, A_GRAN, "neutral"); pickles_camp("chair"); mayor_host()
    cam_move(cam, tgt, 1, N, (-11, 5, 7.5), (-7, 7.5, 5.5), (0, 19, 3.0), (0, 19, 3.4), 22, 24)
def s21(N):  # big screen close: HOUR 12 / 3 LEFT
    night(); scr("h12", "purple")
    cam_move(cam, tgt, 1, N, (1.8, 19.5, 4.2), (0.8, 21.5, 5.0), (0, 29.5, 6.0), (0, 29.5, 6.0), 28, 34)
def s22(N):  # the three: me, Grandma, Mrs. Pickles (slow arc)
    night(); scr("h12", "purple"); pigeon_on(); touch(hero, A_HERO); touch(gran, A_GRAN, "happy"); pickles_camp("none")
    loc = PK_POS; pick.place(loc, PK_YAW); pick.pose(armR=-70); pick.face("evil")
    cam_move(cam, tgt, 1, N, (-5, 9.5, 3.2), (3, 9.0, 3.2), (0, 18, 2.4), (0, 18, 2.5), 24, 26)
def s23(N):  # Mrs. Pickles close, smug: undefeated at everything
    night(); pickles_camp("none"); loc = PK_POS; pick.place(loc, PK_YAW); pick.pose(1, armR=-70, armL=-20); pick.pose(N, armR=-70, armL=-30, head=-6); pick.face("evil")
    d = (math.sin(math.radians(135)), -math.cos(math.radians(135)))
    cam_move(cam, tgt, 1, N, (loc[0] - d[0] * 3.6 - 0.6, loc[1] - d[1] * 3.6, 3.4), (loc[0] - d[0] * 3.0 - 0.5, loc[1] - d[1] * 3.0, 3.4), (loc[0], loc[1], 3.3), (loc[0], loc[1], 3.35), 36, 42)
def s24(N):  # a chair: she sits down (pop)
    night(); pickles_camp("chair"); loc = PK_POS
    cam_move(cam, tgt, 1, N, (loc[0] - 1.4, loc[1] - 4.4, 2.8), (loc[0] - 1.2, loc[1] - 3.9, 2.8), (loc[0], loc[1], 1.9), (loc[0], loc[1], 2.0), 30, 34)
def s25(N):  # then a blanket
    night(); pickles_camp("blanket"); loc = PK_POS; pick.face("happy")
    cam_move(cam, tgt, 1, N, (loc[0] - 1.0, loc[1] - 3.5, 3.1), (loc[0] - 0.9, loc[1] - 3.1, 3.0), (loc[0], loc[1], 2.1), (loc[0], loc[1], 2.1), 32, 36)
def s26(N):  # then a tiny TV (glow on her face)
    night(); pickles_camp("tv"); loc = PK_POS; pick.face("happy")
    cam_move(cam, tgt, 1, N, (loc[0] - 0.7, loc[1] - 2.7, 2.7), (loc[0] - 0.6, loc[1] - 2.3, 2.7), (loc[0], loc[1], 2.4), (loc[0], loc[1], 2.5), 36, 42)
def s27(N):  # HOUR 16: hero's arm droops, shaking (close on the hand on the icing)
    night(); scr("h16", "blue"); touch(hero, A_HERO, "scared")
    for f in range(1, N + 1, 2): hero.pose(f, armR=-74 if f % 4 < 2 else -80, head=10)
    p = hpos(A_HERO)
    cam_move(cam, tgt, 1, N, (p[0] + 2.2, p[1] - 3.2, 2.4), (p[0] + 1.8, p[1] - 2.9, 2.3), (p[0] + 0.7, p[1] - 1.2, 2.1), (p[0] + 0.7, p[1] - 1.2, 2.1), 34, 40)
def s28(N):  # hero close: the stomach growl (shake, sweat)
    night(); touch(hero, A_HERO, "shock"); p = hpos(A_HERO)
    for i, s in enumerate(sweat):
        f0 = 1 + i * max(2, N // 4); s.location = (p[0] + 0.45, p[1] - 0.52, 3.15); s.keyframe_insert("location", frame=f0)
        s.location = (p[0] + 0.5, p[1] - 0.55, 2.6); s.keyframe_insert("location", frame=f0 + 6)
    cam_move(cam, tgt, 1, N, (p[0] + 0.4, p[1] - 3.6, 2.7), (p[0] + 0.2, p[1] - 3.0, 2.6), (p[0], p[1], 2.55), (p[0], p[1], 2.6), 40, 46); shake(2, 8, 0.1)
def s29(N):  # the pigeon slowly turns to look at the hero
    night(); pigeon_on(); touch(hero, A_HERO, "shock")
    pg.neck.rotation_euler = (0, 0, 0); pg.neck.keyframe_insert("rotation_euler", frame=1)
    pg.neck.rotation_euler = (0, 0, math.radians(-75)); pg.neck.keyframe_insert("rotation_euler", frame=max(2, N // 2))
    cam_move(cam, tgt, 1, N, (PG_SPOT[0] - 2.6, PG_SPOT[1] - 1.6, PG_SPOT[2] + 0.7), (PG_SPOT[0] - 2.2, PG_SPOT[1] - 1.3, PG_SPOT[2] + 0.6),
             (PG_SPOT[0], PG_SPOT[1], PG_SPOT[2] + 0.55), (PG_SPOT[0], PG_SPOT[1], PG_SPOT[2] + 0.55), 40, 44)
def s30(N):  # Grandma wakes up, looks at the donut
    night(); scr("h16", "blue"); loc, yaw = ring(A_GRAN); gran.place(loc, yaw); gran.pose(1, armR=-78, head=20); sleep_face(gran, 1)
    fw = max(2, N // 3); gran.face("surprised", fw); gran.pose(fw, armR=-78, head=25)
    d = (math.sin(math.radians(A_GRAN)), -math.cos(math.radians(A_GRAN)))
    cam_move(cam, tgt, 1, N, (loc[0] - d[0] * 3.4, loc[1] - d[1] * 3.4 - 0.5, 3.2), (loc[0] - d[0] * 2.9, loc[1] - d[1] * 2.9 - 0.4, 3.2), (loc[0], loc[1], 3.0), (loc[0], loc[1], 3.0), 36, 40)
def s31(N):  # ...and takes a big bite. OUT! (screen goes red)
    night(); scr("out", "red"); loc, yaw = ring(A_GRAN); gran.place(loc, yaw, 1); gran.pose(1, armR=-78, head=10); gran.face("happy", 1)
    fb = max(2, N // 3); bp = hpos(A_GRAN, 2.3, DZ + 0.4)
    gran.place(((loc[0] + bp[0]) / 2, (loc[1] + bp[1]) / 2, 0.06), yaw, fb); gran.pose(fb, armR=-78, lean=35, head=30); gran.talk(fb, N, 0.14, 2)
    BITE.location = bp; BITE.hide_render = True; BITE.keyframe_insert("hide_render", frame=fb - 1); BITE.hide_render = False; BITE.keyframe_insert("hide_render", frame=fb)
    r = random.Random(4)
    for c in crumbs:
        c.location = bp; c.keyframe_insert("location", frame=fb); c.location = (bp[0] + r.uniform(-1.5, 1.5), bp[1] + r.uniform(-1.5, 0.5), 0.1); c.keyframe_insert("location", frame=fb + 8)
    touch(hero, A_HERO, "shock")
    cam_move(cam, tgt, 1, N, (-6.5, 11.5, 3.5), (-6.0, 12.3, 3.6), (-1.8, 16.5, 2.4), (-1.6, 16.8, 2.6), 28, 30); shake(fb, fb + 3, 0.1)
def s32(N):  # the Mayor plays dirty: walks in with a tower of pizza boxes, evil grin
    night(); scr("left2", "purple"); mayor.place((-5, 13, 0.06), 30, 1); mayor.place((-2.2, 13.6, 0.06), 10, N); mayor.walk(1, N, 8)
    hold(pizza, mayor, 0, (0.95, -0.9, -1.0)); mayor.pose(1, armL=-80, armR=-80); mayor.face("evil")
    BITE.location = hpos(A_GRAN, 2.3, DZ + 0.4); BITE.hide_render = False
    cam_move(cam, tgt, 1, N, (-3.0, 8.6, 2.3), (-2.4, 9.0, 2.5), (-4, 13.2, 3.0), (-2.2, 13.6, 3.0), 30, 32)
def s33(N):  # open pizza box close, steam
    night(); pizza.location = (-1.2, 13.8, 2.0); pizza.rotation_euler = (0, 0, math.radians(15))
    r = random.Random(2)
    for i, s in enumerate(STEAM):
        f0 = 1 + i * 3; x, y = -1.2 + r.uniform(-0.4, 0.4), 13.8 + r.uniform(-0.4, 0.4)
        s.location = (x, y, 2.7); s.scale = (0.1, 0.1, 0.1); s.keyframe_insert("location", frame=f0); s.keyframe_insert("scale", frame=f0)
        s.location = (x + 0.2, y, 4.0); s.scale = (0.4, 0.4, 0.5); s.keyframe_insert("location", frame=f0 + 14); s.keyframe_insert("scale", frame=f0 + 14)
    cam_move(cam, tgt, 1, N, (-1.0, 10.7, 3.3), (-1.1, 11.3, 3.1), (-1.2, 13.8, 2.6), (-1.2, 13.8, 2.6), 34, 40)
def s34(N):  # hero close: sweating, NOT moving
    night(); touch(hero, A_HERO, "determined"); p = hpos(A_HERO)
    for i, s in enumerate(sweat):
        f0 = 1 + i * max(2, N // 4); s.location = (p[0] - 0.45, p[1] - 0.52, 3.15); s.keyframe_insert("location", frame=f0)
        s.location = (p[0] - 0.5, p[1] - 0.55, 2.6); s.keyframe_insert("location", frame=f0 + 6)
    cam_move(cam, tgt, 1, N, (p[0] - 0.2, p[1] - 3.2, 2.62), (p[0] - 0.1, p[1] - 2.8, 2.62), (p[0], p[1], 2.6), (p[0], p[1], 2.62), 44, 50)
def s35(N):  # Mrs. Pickles under her blanket: perfectly still, TV glowing (the dummy)
    night(); pickles_camp("mound"); loc = PK_POS
    cam_move(cam, tgt, 1, N, (loc[0] - 1.4, loc[1] - 4.3, 3.0), (loc[0] - 1.2, loc[1] - 3.8, 3.0), (loc[0], loc[1], 2.2), (loc[0], loc[1], 2.2), 30, 34)
def s36(N):  # the pigeon pecks "her" hand... nothing
    night(); pickles_camp("mound"); pigeon_on()
    gw = GW
    pg.root.location = (gw[0] + 0.15, gw[1] + 0.4, DZ + 0.62); pg.root.rotation_euler = (0, 0, math.radians(PK_YAW + 180)); pg.peck(1, N, 3, 55)
    cam_move(cam, tgt, 1, N, (gw[0] + 1.4, gw[1] - 2.3, gw[2] + 0.8), (gw[0] + 1.1, gw[1] - 1.9, gw[2] + 0.7), (gw[0], gw[1], gw[2] + 0.2), (gw[0], gw[1], gw[2] + 0.2), 38, 44)
def s37(N):  # WAIT. hero eyes narrow, snap push
    night(); touch(hero, A_HERO, "surprised"); hero.face("determined", max(2, N // 2)); p = hpos(A_HERO)
    cam_move(cam, tgt, 1, N, (p[0], p[1] - 3.4, 2.62), (p[0], p[1] - 2.3, 2.62), (p[0], p[1], 2.62), (p[0], p[1], 2.62), 44, 56)
def s38(N):  # hero yanks the blanket off (it flies away), keeping one hand on the donut
    night(); pickles_camp("mound"); loc = PK_POS; touch(hero, 160, "determined"); hero.pose(1, armR=-78, armL=-20)
    fy = max(2, N // 3); hero.pose(fy, armR=-78, armL=-150, armLs=40)
    mound.keyframe_insert("location", frame=fy); mound.keyframe_insert("rotation_euler", frame=fy)
    mound.location = (2.5, 1.0, 6.0); mound.rotation_euler = (1.2, 0.6, 0.4); mound.keyframe_insert("location", frame=N); mound.keyframe_insert("rotation_euler", frame=N)
    pillows.hide_render = True; pillows.keyframe_insert("hide_render", frame=fy)
    for ch in pillows.children: ch.hide_render = True; ch.keyframe_insert("hide_render", frame=fy); ch.hide_render = False; ch.keyframe_insert("hide_render", frame=fy + 1)
    cam_move(cam, tgt, 1, N, (loc[0] + 4.5, loc[1] - 5.0, 3.0), (loc[0] + 4.0, loc[1] - 4.6, 3.2), (loc[0] - 0.5, loc[1] - 0.5, 2.3), (loc[0] - 0.5, loc[1] - 0.5, 2.6), 26, 28); shake(fy, fy + 3, 0.1)
def s39(N):  # reveal: pillows, a wig, glasses
    night(); pickles_camp("reveal"); loc = PK_POS
    cam_move(cam, tgt, 1, N, (loc[0] - 0.9, loc[1] - 3.2, 3.0), (loc[0] - 0.8, loc[1] - 2.7, 2.9), (loc[0], loc[1], 2.2), (loc[0], loc[1], 2.3), 34, 40); shake(1, 3, 0.08)
def s40(N):  # ...and a rubber glove taped to the donut (close)
    night(); pickles_camp("reveal"); gw = GW
    cam_move(cam, tgt, 1, N, (gw[0] + 1.0, gw[1] - 1.9, gw[2] + 0.9), (gw[0] + 0.8, gw[1] - 1.5, gw[2] + 0.7), (gw[0], gw[1], gw[2]), (gw[0], gw[1], gw[2]), 40, 46)
def s41(N):  # cutaway: Mrs. Pickles at home in bed, asleep, smug (Zzz)
    pick.root.location = (296.5, 0.9, 1.75); pick.root.rotation_euler = (math.radians(-90), 0, 0); sleep_face(pick); pick.talk(1, N, 0.1, 7)
    for l in STREETLAMPS: l.data.energy = 0
    bg.inputs["Strength"].default_value = 0.3; sun.data.energy = 0.2; sc.view_settings.exposure = 1.1; sc.objects["bedlamp"].data.energy = 700; fill.data.energy = 260
    zzz(1, N, (296.5, 3.6, 2.8))
    cam_move(cam, tgt, 1, N, (294.0, -3.5, 5.5), (294.6, -2.8, 5.0), (296.5, 2.2, 1.8), (296.5, 2.4, 1.9), 28, 32)
def s42(N):  # DISQUALIFIED: screen red, Mayor points
    night(); scr("dq", "red"); mayor_host("evil"); mayor.pose(1, armR=-95, armL=-90); mayor.talk(1, N // 2, 0.14, 2)
    cam_move(cam, tgt, 1, N, (-1.5, 18.0, 3.4), (-2.2, 19.0, 3.8), (-2.5, 27, 4.8), (-2.5, 27, 5.0), 24, 26); shake(1, 3, 0.12)
def s43(N):  # the crowd (back for the finale) goes wild
    night(); scr("dq", "red"); audience("happy", 14, 8.5)
    for i, c in enumerate(crowd): cheer(c, 1 + i % 3, N, i)
    cam_move(cam, tgt, 1, N, (2.0, 13.0, 3.0), (-1.5, 13.0, 3.2), (0, 5, 2.6), (0, 5, 2.8), 22, 24); shake(1, N, 0.05)
def s44(N):  # hero triumphant (free hand up), confetti, screen WINNER ???
    night(); scr("winner", "green"); touch(hero, A_HERO, "happy"); pigeon_on(); hero.pose(1, armR=-78, armL=-165, armLs=25)
    confetti(1, N + 20, 0, 17, 7); p = hpos(A_HERO)
    cam_move(cam, tgt, 1, N, (p[0] - 1.0, p[1] - 5.6, 2.2), (p[0] - 0.6, p[1] - 4.8, 2.4), (p[0], p[1], 2.8), (p[0], p[1], 3.0), 30, 34)
def s45(N):  # Mayor with the mic: lift your hand, champion
    night(); scr("winner", "green"); mayor.place((-4.2, 15.8, 0.06), -20); hold(mic, mayor, 1); mayor.pose(1, armR=-95, armL=-140, armLs=20); mayor.face("happy"); mayor.talk(1, N - 2, 0.14, 3)
    cam_move(cam, tgt, 1, N, (-5.2, 11.4, 3.4), (-5.0, 12.1, 3.5), (-4.2, 15.8, 3.3), (-4.2, 15.8, 3.4), 34, 40)
def s46(N):  # hero lifts his hand off the donut... slowly, proudly (music drops out)
    night(); scr("winner", "green"); touch(hero, A_HERO, "happy"); pigeon_on(); p = hpos(A_HERO)
    hero.pose(1, armR=-78); hero.pose(N - 2, armR=-170, armRs=10)
    cam_move(cam, tgt, 1, N, (p[0] + 0.2, p[1] - 4.6, 2.3), (p[0] + 0.1, p[1] - 4.2, 2.4), (p[0], p[1], 3.0), (p[0], p[1], 3.6), 32, 34)
def s47(N):  # reveal: the pigeon is still standing on the donut (snap zoom)
    night(); scr("winner", "green"); pigeon_on(); pg.bob(1, N, 6); touch(hero, A_HERO, "shock"); hero.pose(1, armR=-170, armRs=10)
    cam_move(cam, tgt, 1, N, (PG_SPOT[0] - 0.6, PG_SPOT[1] - 4.8, PG_SPOT[2] + 0.8), (PG_SPOT[0] - 0.3, PG_SPOT[1] - 2.4, PG_SPOT[2] + 0.6),
             (PG_SPOT[0], PG_SPOT[1], PG_SPOT[2] + 0.5), (PG_SPOT[0], PG_SPOT[1], PG_SPOT[2] + 0.55), 34, 48); shake(2, 5, 0.06)
def s48(N):  # Mayor hands the giant cheque to the pigeon; screen WINNER: PIGEON
    night(); scr("pigeon", "pink"); pigeon_on(); mayor.place((PG_SPOT[0] - 2.6, PG_SPOT[1] - 1.8, 0.06), 125); mayor.face("happy")
    hold(cheque, mayor, 1, (0, -0.5, -1.1)); mayor.pose(1, armR=-60); mayor.pose(N // 2, armR=-95)
    cam_move(cam, tgt, 1, N, (0.0, 12.5, 3.3), (-0.3, 13.0, 3.3), (-3.0, 17.0, 2.8), (-2.8, 17.2, 2.8), 24, 26)
def s49(N):  # pigeon in a tiny top hat with the cheque, confetti, crowd cheers
    night(); scr("pigeon", "pink"); pigeon_on(); pg.hat.hide_render = False
    for ch in pg.hat.children: ch.hide_render = False
    cheque.location = (PG_SPOT[0] + 0.1, PG_SPOT[1] - 0.6, PG_SPOT[2] - 0.35); cheque.scale = (0.45, 0.45, 0.45); cheque.rotation_euler = (0, 0, math.radians(10))
    pg.flap(1, N, 3); confetti(-6, N + 10, PG_SPOT[0], PG_SPOT[1], 4)
    cam_move(cam, tgt, 1, N, (PG_SPOT[0] + 1.6, PG_SPOT[1] - 3.0, PG_SPOT[2] + 0.4), (PG_SPOT[0] + 1.0, PG_SPOT[1] - 2.6, PG_SPOT[2] + 0.5),
             (PG_SPOT[0], PG_SPOT[1], PG_SPOT[2] + 0.6), (PG_SPOT[0], PG_SPOT[1], PG_SPOT[2] + 0.6), 36, 40)
def s50(N):  # hero close, deadpan to camera: I lost to a pigeon
    night(); scr("pigeon", "pink"); touch(hero, A_HERO, "neutral"); hero.pose(1, armR=-20, head=6); hero.face("evil", N // 2); hero.talk(1, N - 3, 0.08, 3)
    p = hpos(A_HERO)
    cam_move(cam, tgt, 1, N, (p[0] + 0.3, p[1] - 3.6, 2.6), (p[0] + 0.15, p[1] - 3.0, 2.6), (p[0], p[1], 2.58), (p[0], p[1], 2.6), 40, 46)
def s51(N):  # wide finale: the pigeon in its hat on the donut, fireworks over the clock tower, crane up
    night(); scr("pigeon", "pink"); pigeon_on(); pg.hat.hide_render = False
    for ch in pg.hat.children: ch.hide_render = False
    touch(hero, A_HERO, "neutral"); hero.pose(armR=-10, head=10); mayor.place((-3.0, 15.5, 0.06), 20); mayor.face("happy"); fireworks(1, N); audience("happy", 10, 8.5)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
    cam_move(cam, tgt, 1, N, (2, 7, 2.5), (1, 2, 7.0), (0, 18, 2.6), (0, 24, 8.0), 26, 24)

T = [("s01", 0.0, s01), ("s02", 1.6, s02), ("s03", 3.2, s03), ("s04", 4.5, s04),
     ("s05", L[1], s05), ("s06", L[1] + 1.7, s06), ("s07", L[2], s07), ("s08", L[2] + 1.65, s08),
     ("s09", L[3], s09), ("s10", L[3] + 1.7, s10), ("s11", L[4], s11), ("s12", L[4] + 1.85, s12),
     ("s13", L[5], s13), ("s14", L[5] + 1.45, s14), ("s15", L[6], s15), ("s16", L[6] + 1.95, s16), ("s17", L[6] + 3.15, s17),
     ("s18", L[7], s18), ("s19", L[7] + 1.7, s19), ("s20", L[8], s20), ("s21", L[8] + 1.8, s21), ("s22", L[8] + 3.4, s22),
     ("s23", L[9], s23), ("s24", L[9] + 1.7, s24), ("s25", L[9] + 3.0, s25), ("s26", L[9] + 4.15, s26),
     ("s27", L[10], s27), ("s28", L[10] + 1.75, s28), ("s29", L[10] + 3.15, s29), ("s30", L[11], s30), ("s31", L[11] + 1.4, s31),
     ("s32", L[12], s32), ("s33", L[12] + 1.5, s33), ("s34", L[13], s34), ("s35", L[13] + 1.6, s35), ("s36", L[14], s36),
     ("s37", L[15], s37), ("s38", L[16], s38), ("s39", L[16] + 1.3, s39), ("s40", L[16] + 2.6, s40), ("s41", L[17], s41),
     ("s42", L[18], s42), ("s43", L[18] + 1.4, s43), ("s44", L[18] + 2.7, s44), ("s45", L[19], s45), ("s46", L[20], s46),
     ("s47", L[21], s47), ("s48", L[22], s48), ("s49", L[22] + 1.8, s49), ("s50", L[23], s50), ("s51", L[23] + 1.9, s51)]
TIMES = [(sid, t, (T[i + 1][1] if i + 1 < len(T) else END), fn) for i, (sid, t, fn) in enumerate(T)]
os.makedirs(W, exist_ok=True)
json.dump([(sid, t0, t1) for sid, t0, t1, _ in TIMES], open(f"{W}/shots_timing.json", "w"))

only = [a for a in sys.argv[1:] if a.startswith("s")]
for sid, t0, t1, fn in TIMES:
    if only and sid not in only: continue
    N = max(2, round((t1 - t0) * FPS)); d = f"{W}/shots/{sid}"
    if not PREV and os.path.exists(f"{d}/done"): continue
    reset(); fn(N)
    if sid >= "s18" and sid != "s41" and pg.root.location[2] < -100: pigeon_on()
    if sid >= "s32" and sid != "s41" and not BITE.animation_data: BITE.location = hpos(A_GRAN, 2.3, DZ + 0.4); BITE.hide_render = False
    if PREV:
        os.makedirs(f"{W}/stills", exist_ok=True)
        sc.frame_set(max(1, int(N * 0.6))); sc.render.filepath = f"{W}/stills/{sid}.png"; bpy.ops.render.render(write_still=True)
        continue
    os.makedirs(d, exist_ok=True)
    sc.frame_start, sc.frame_end = 1, N; sc.render.filepath = f"{d}/"
    t = time.time(); bpy.ops.render.render(animation=True)
    open(f"{d}/done", "w").write(str(N)); print(sid, N, "frames", round(time.time() - t), "s", flush=True)
