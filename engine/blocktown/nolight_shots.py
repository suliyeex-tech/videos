"""In This Town #3 (WONDER variant): the town where it was always night. Pip finds a tiny smirking candle; touching it
spreads light (fingers -> lantern -> cat -> Benny's hoodie -> bakery -> Grandma's knitting -> street lamps), the Mayor
blows the lamps out, Pip lights the clock tower, the sun rises, and the Mayor turns out to hide a lamp under his hat.
python3 nolight_shots.py [sid ...] [--still]   -> /home/claude/work/<slug>/shots/<sid>/####.png (resumable)"""
import sys, os, json, math, random, time, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move

SLUG = "2026-11-20-the-town-where-it-was-always-night"; FPS = 12
W = f"/home/claude/work/{SLUG}"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; END = vo["total"] + 0.6
def D(i): return (L[i + 1] if i + 1 < len(L) else END) - L[i]
PREV = "--still" in sys.argv
sc, cam, tgt = lib.setup(res=(432, 768) if not PREV else (216, 384), samples=8 if not PREV else 4, fps=FPS)
town = lib.build_town(); lib.build_bedroom(300); lib.build_stairs(500); cr = lib.build_clockroom(700)
bg = sc.world.node_tree.nodes["Background"]; sun = sc.objects["moonlight"]
for n in ("candle", "flame", "flamelight", "candle_eyeL", "candle_eyeR", "ped"): sc.objects[n].hide_render = True
for o in sc.objects:
    if o.name.startswith("key"): o.hide_render = True

def bsdf(m): return m.node_tree.nodes["Principled BSDF"]
ANIM_M = []
def emit(m, val, f=None, col=None):
    b = bsdf(m)
    if col: b.inputs["Emission Color"].default_value = (*lib.srgb(col), 1)
    b.inputs["Emission Strength"].default_value = val
    if f is not None:
        b.inputs["Emission Strength"].keyframe_insert("default_value", frame=f)
        if m not in ANIM_M: ANIM_M.append(m)
def lkey(o, val, f=None):
    o.data.energy = val
    if f is not None: o.data.keyframe_insert("energy", frame=f)

# ---------------------------------------------------------------- the town with NO light: every window / bulb gets its own material
WIN = []      # (object, material, distance to the clock tower)
for o in list(sc.objects):
    if o.name.startswith("hwin"):
        m = mat(f"win_{o.name}", "#1c2346", 0.3, 0.001, "#ffbf5e"); o.data.materials[0] = m
        WIN.append((o, m, math.dist((o.location.x, o.location.y), (0, 34))))
BULB = []     # (bulb obj, material, light obj, x)
for o in list(sc.objects):
    if o.name.startswith("lbulb"):
        x = float(o.name[5:].split("_")[0]) if "_" in o.name[5:] else float(o.name[5:])
        m = mat(f"bulb_{o.name}", "#3a3a48", 0.3, 0.001, "#ffd9a0"); o.data.materials[0] = m
        BULB.append([o, m, None, o.location.x, o.location.y])
for o in sc.objects:
    if o.type == "LIGHT" and o.name.startswith("lamp"):
        for b in BULB:
            if abs(b[3] - o.location.x) < 0.01 and abs(b[4] - o.location.y) < 0.6: b[2] = o
BULB.sort(key=lambda b: (b[3], b[4]))
CLOCKM = sc.objects["clockface"].data.materials[0]; CRFACE = sc.objects["cr_face"].data.materials[0]
plaza = cube("plaza", (0, 23, 0.02), (34, 18, 0.06), mat("plaza", "#b9a88c", 0.85), 0)
# 'NO LIGHTS' sign on the town hall steps
def mktext(name, body, loc, size, col, emit_=0.0, rot=(90, 0, 0)):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = 0.04
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = tuple(math.radians(r) for r in rot)
    cu.materials.append(mat(name + "m", col, 0.5, emit_)); return o
sign = empty("sign", (5.5, 29.5, 0))
cyl("signpost", (0, 0, 1.6), 0.12, 3.2, mat("pole", "#2b2d36", 0.4, metal=0.6), parent=sign, verts=8)
cube("signboard", (0, -0.1, 3.4), (3.6, 0.15, 1.6), mat("signb", "#f2efe6", 0.6), 0.05, sign)
t1 = mktext("signt1", "NO LIGHTS", (0, -0.2, 3.65), 0.62, "#c8282f"); t1.parent = sign
t2 = mktext("signt2", "BY ORDER OF THE MAYOR", (0, -0.2, 3.05), 0.27, "#23253b"); t2.parent = sign
# grandma's living room at x=1100
def room(ox, wallc, floorc):
    cube(f"rf{ox}", (ox, 0, -0.05), (16, 16, 0.1), mat(f"rfm{ox}", floorc, 0.7), 0)
    cube(f"rb{ox}", (ox, 6, 4), (16, 0.3, 8), mat(f"rwm{ox}", wallc, 0.8), 0); cube(f"rl{ox}", (ox - 7, 0, 4), (0.3, 16, 8), mat(f"rwm{ox}", wallc, 0.8), 0)
    cube(f"rr{ox}", (ox + 7, 0, 4), (0.3, 16, 8), mat(f"rwm{ox}", wallc, 0.8), 0)
room(1100, "#5a4a7a", "#5a4030")
cube("sofa", (1098, 3.5, 0.7), (5, 2, 1.4), mat("sofa", "#3f6fb0", 0.8), 0.25); cube("sofaback", (1098, 4.4, 1.6), (5, 0.6, 1.6), mat("sofa", "#3f6fb0", 0.8), 0.25)
roomfill = point("roomfill", (1098, -3, 6), "#6b7bff", 120, 2.0)
SOCKM = mat("sock", "#e8423f", 0.8, 0.001, "#ff7a5a")
sock = empty("sock")   # a sock for a horse: very long leg + foot
cube("sockleg", (0, 0, 1.6), (0.9, 0.7, 3.2), SOCKM, 0.2, sock); cube("sockfoot", (0, -0.9, 0.2), (0.9, 2.2, 0.8), SOCKM, 0.25, sock)
for i in range(4): cube(f"sockstripe{i}", (0, 0, 2.6 + i * 0.35), (0.95, 0.75, 0.14), mat("sockw", "#f2efe6", 0.8), 0.03, sock)
for sd in (-1, 1): cyl(f"needle{sd}", (0.5 * sd, -0.2, 3.6), 0.05, 2.4, mat("needle", "#c8ccd8", 0.3, metal=0.8), (0, math.radians(30 * sd), 0), sock, 6)
yarn = sphere("yarn", (0, 0, 0), (0.6, 0.6, 0.6), SOCKM)
# bakery loaves (on a sill in front of the bakery window, house x=-12, y=13)
LOAFM = mat("loaf", "#c98a3a", 0.8, 0.001, "#ffcf6a")
for i in range(4): cube(f"loaf{i}", (-14.5 + i * 1.6, 9.7, 3.0), (1.2, 0.7, 0.55), LOAFM, 0.22)
cube("sill", (-12, 9.8, 2.65), (7, 1.2, 0.2), mat("sillw", "#8a5a32", 0.7), 0.04)
for i in range(4): sc.objects[f"loaf{i}"].hide_render = False

# ---------------------------------------------------------------- the candle (Oddwick in 3D: wax, flame, painted smirk)
WAX = mat("wax3", "#f3e6c8", 0.6)
FLM = mat("flame3", "#ffb347", 0.3, 40, "#ff9a2e")
cnd = empty("cnd")
cyl("cnd_wax", (0, 0, 0.45), 0.32, 0.9, WAX, parent=cnd, verts=20)
cyl("cnd_drip", (0.2, -0.1, 0.8), 0.1, 0.3, WAX, parent=cnd, verts=8)
cyl("cnd_wick", (0, 0, 0.98), 0.03, 0.18, mat("wick", "#222222"), parent=cnd, verts=6)
cflame = empty("cnd_flamep", (0, 0, 1.05), cnd)
sphere("cnd_flame", (0, 0, 0.2), (0.16, 0.16, 0.32), FLM, cflame, 12)
clight = point("cnd_light", (0, -0.3, 1.2), "#ff9a2e", 60, 0.1, cnd)
blk = mat("eyeblack", "#141414", 0.25)
for sd in (-1, 1): cube(f"cnd_eye{sd}", (0.11 * sd, -0.31, 0.62), (0.06, 0.02, 0.1), blk, 0, cnd)
cbrow = cube("cnd_brow", (0.11, -0.315, 0.74), (0.1, 0.02, 0.025), blk, 0, cnd, (0, math.radians(-20), 0))
cmouth = cube("cnd_mouth", (0.03, -0.315, 0.45), (0.16, 0.02, 0.035), blk, 0, cnd, (0, math.radians(-12), 0))

# ---------------------------------------------------------------- cast
pip = lib.Char("pip", skin="#f3c89a", top="#7a4fd0", pants="#2f4a7a", hair="#e0702e", hair_style="flat", hood=True, extra="#5a35a8")
for sd in (-1, 1): cube(f"pip_tail{sd}", (0.62 * sd, 0.2, 0.75), (0.3, 0.3, 0.55), pip.mhair, 0.08, pip.neck)
GLOWM = mat("glowhand", "#fff0b0", 0.3, 0.001, "#ffd36a")
glow = sphere("pipglow", (0, 0, -1.0 * pip.s), (0.32, 0.34, 0.3), GLOWM, pip.arms[1], 12)
glowl = point("pipglowl", (0, -0.4, -1.0 * pip.s), "#ffc65a", 0, 0.2, pip.arms[1])
ben = lib.Char("benny", skin="#c98d62", top="#d8423f", pants="#3b3b55", hair="#1d1310", hair_style="flat", hood=True, extra="#a83030")
cube("bencap", (0, -0.15, 1.05), (1.08, 1.2, 0.25), mat("bencap", "#2f63d6", 0.5), 0.06, ben.neck)
benl = point("benlight", (0, -1.2, 2.2), "#ff7a5a", 0, 1.0, ben.root)
brush = empty("brush", (0, -0.35, -1.0), ben.arms[1]); cube("brushh", (0, -0.2, 0.35), (0.12, 0.12, 0.9), mat("brushm", "#2fb0a8", 0.4), 0.02, brush)
baker = lib.Char("baker", skin="#f0c29a", top="#f4f4f4", pants="#5a5a6a", hair="#5b4636", hair_style="flat", kid=False)
cyl("bakerhat", (0, 0, 1.45), 0.48, 0.9, mat("bakerhat", "#ffffff", 0.6), parent=baker.neck, verts=16)
bread = cube("bread", (0, -0.5, -1.05), (0.9, 0.5, 0.45), LOAFM, 0.2, baker.arms[1])
gran = lib.Char("gran", skin="#e9b892", top="#8b4fb0", pants="#8b4fb0", hair="#eeeeee", hair_style="flat", kid=False)
cube("granbun", (0, 0.35, 1.1), (0.5, 0.5, 0.4), gran.mhair, 0.15, gran.neck)
for sd in (-1, 1): cube(f"granspec{sd}", (0.22 * sd, -0.53, 0.62), (0.3, 0.03, 0.26), mat("spec", "#d8d8e8", 0.2, metal=0.6), 0.03, gran.neck)
mayor = lib.Char("mayor", skin="#f0c29a", top="#23253b", pants="#23253b", hair="#5b4636", hair_style="flat", kid=False); mayor.mayor_kit()
HATLM = mat("hatlamp", "#ffe08a", 0.3, 20, "#ffc65a")
hatlamp = empty("hatlamp", (0, 0, 1.05), mayor.neck)
cube("hatlamp_b", (0, 0, 0.2), (0.4, 0.4, 0.4), HATLM, 0.06, hatlamp); cube("hatlamp_t", (0, 0, 0.48), (0.5, 0.5, 0.12), mat("hatlampt", "#2b2d36", 0.4, metal=0.6), 0.02, hatlamp)
hatl = point("hatlampl", (0, -0.6, 0.4), "#ffc65a", 0, 0.2, hatlamp)
crowd = []
CC = [("#3f8fd8", "#6b3f22"), ("#e86fb0", "#1d1310"), ("#57b65a", "#e0c070"), ("#e8823f", "#1d1310"), ("#2fb0a8", "#e0702e"), ("#6a7ad8", "#eeeeee")]
for i, (top, hair) in enumerate(CC):
    crowd.append(lib.Char(f"cr{i}", skin=["#f3c89a", "#c98d62", "#8d5a3b", "#e9b892"][i % 4], top=top, pants=["#3b3b55", "#c9b48a", "#2f4a7a"][i % 3],
                          hair=hair, hair_style="spiky" if i % 3 == 0 else "flat", kid=i % 2 == 0))
dog = lib.Dog("dog", "#a8682f"); cat = lib.Dog("cat", "#8a8f9c"); cat.root.scale = (0.55, 0.55, 0.55)
CATM = bpy.data.materials["cat_fur"]
lant = empty("lantern")
LANTM = mat("langlass", "#3a3020", 0.2, 0.001, "#ffc65a")
cube("lant_base", (0, 0, 0.1), (0.9, 0.9, 0.2), mat("lantmet", "#3b3b44", 0.4, metal=0.7), 0.03, lant)
cube("lant_glass", (0, 0, 0.75), (0.75, 0.75, 1.0), LANTM, 0.04, lant)
cube("lant_top", (0, 0, 1.35), (0.95, 0.95, 0.2), mat("lantmet", "#3b3b44", 0.4, metal=0.7), 0.03, lant)
lantl = point("lantl", (0, -0.6, 0.8), "#ffc65a", 0, 0.3, lant)
# attic = the bedroom set at x=300, with boxes and a dusty chest
for i, (x, y, s) in enumerate(((304, 3.5, 1.6), (305.5, 1.5, 1.2), (303.2, 4.6, 1.0))):
    cube(f"box{i}", (x, y, s / 2), (s, s, s), mat("box", "#b08a5a", 0.9), 0.04)
cube("chest", (302.5, 2.0, 0.6), (2.2, 1.4, 1.2), mat("chest", "#6b4226", 0.7), 0.06)

fill = point("camfill", (0.6, 0.4, 0.2), "#9fb0ff", 90, 1.0, cam)
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
OFF = (0, 0, -500)
CAST = [pip, ben, baker, gran, mayor] + crowd

def night():
    """the dark town: no lamps, dark windows, dim blue moon so we can still see shapes"""
    bg.inputs["Color"].default_value = (*lib.srgb("#141a3e"), 1); bg.inputs["Strength"].default_value = 0.9
    sun.data.energy = 1.4; sun.data.color = lib.srgb("#7f96ff"); sun.rotation_euler = (math.radians(55), 0, math.radians(200))
    sc.objects["moon"].hide_render = True
    for o in OBJ:
        if o.type == "LIGHT" and (o.name.startswith("lamp") or o.name.startswith("torch") or o.name in ("hallglow", "towerglow", "bedlamp", "cr_purple")):
            o.data.energy = 0
    for _, m, _ in WIN: emit(m, 0.0)
    for b in BULB: emit(b[1], 0.0)
    emit(CLOCKM, 0.0); emit(CRFACE, 0.0)
    sc.view_settings.exposure = 1.1

def reset():
    for o in OBJ:
        o.animation_data_clear()
        if o.type == "CAMERA" and o.data.animation_data: o.data.animation_data_clear()
        l, r, s, h, p = BASE[o.name]
        if o.parent != p: o.parent = p
        o.location, o.rotation_euler, o.scale, o.hide_render = l, r, s, h
        if o.type == "LIGHT":
            o.data.energy = LIGHTS[o.name]
            if o.data.animation_data: o.data.animation_data_clear()
    for m in ANIM_M:
        if m.node_tree.animation_data: m.node_tree.animation_data_clear()
    ANIM_M.clear()
    if sc.world.node_tree.animation_data: sc.world.node_tree.animation_data_clear()
    for m in (GLOWM, LANTM, SOCKM, LOAFM, CATM, ben.mtop): emit(m, 0.0)
    emit(HATLM, 20)
    for c in CAST: c.place(OFF); c.pose(); c.face("neutral")
    glow.hide_render = True
    for a in (dog, cat): a.root.location = OFF
    for o in (cnd, sock, yarn, lant, sign): o.location = OFF
    cam.data.lens = 28; cam.delta_location = (0, 0, 0)
    night()

def candle_at(loc, yaw=0, s=1.0):
    cnd.location = loc; cnd.rotation_euler = (0, 0, math.radians(yaw)); cnd.scale = (s, s, s)
def candle_in_hand(c, side=1):
    cnd.parent = c.arms[side]; cnd.location = (0, -0.45, -1.25 * c.s); cnd.rotation_euler = (math.radians(90), 0, 0); cnd.scale = (0.7, 0.7, 0.7)
def candle_talk(f0, f1, rate=2):
    f = f0; k = 0
    while f <= f1:
        cmouth.scale = (1, 1, 3.2 if k % 2 == 0 else 1); cmouth.keyframe_insert("scale", frame=f); f += rate; k += 1
    cmouth.scale = (1, 1, 1); cmouth.keyframe_insert("scale", frame=f1 + 1)
def flame_flicker(f0, f1, base=1.0, every=2, seed=1):
    r = random.Random(seed)
    for f in range(f0, f1 + 1, every):
        k = base * r.uniform(0.85, 1.15); cflame.scale = (k, k, k * r.uniform(0.9, 1.2)); cflame.keyframe_insert("scale", frame=f)
        clight.data.energy = 60 * k; clight.data.keyframe_insert("energy", frame=f)
def hand_glow(on=True, f=None, k=1.0, boost=1.0):
    glow.hide_render = not on
    emit(GLOWM, 25 * k if on else 0.0, f); lkey(glowl, 90 * k * boost if on else 0, f)
def shake(f0, f1, amt=0.15, seed=1):
    r = random.Random(seed)
    for f in range(f0, f1 + 1):
        cam.delta_location = (r.uniform(-amt, amt), r.uniform(-amt, amt), r.uniform(-amt, amt)); cam.keyframe_insert("delta_location", frame=f)
def lamps_on(f=None, which=None, k=1.0):
    for i, b in enumerate(BULB):
        if which is not None and i not in which: continue
        emit(b[1], 18 * k, f)
        if b[2]: lkey(b[2], 1800 * k, f)
def windows_on(f=None, k=1.0):
    for _, m, _ in WIN: emit(m, 6 * k, f)
def sunrise(k=1.0):
    c0, c1 = lib.srgb("#141a3e"), lib.srgb("#ffb37a")
    bg.inputs["Color"].default_value = (*[a + (b - a) * k for a, b in zip(c0, c1)], 1); bg.inputs["Strength"].default_value = 0.9 + 0.2 * k
    sun.data.color = lib.srgb("#ffb070") if k > .5 else lib.srgb("#7f96ff"); sun.data.energy = 1.4 + 1.4 * k
    sun.rotation_euler = (math.radians(55 + 23 * k), 0, math.radians(200 + 15 * k))
def crowd_in_square(face="happy", n=6, ystart=19.5):
    for i, c in enumerate(crowd[:n]):
        x = -6.5 + (i % 3) * 5.0 + (1.2 if i // 3 else 0); y = ystart + (i // 3) * 2.6 + (i % 2) * 0.4
        c.place((x, y, 0.06), 180 + (x * -2)); c.face(face)
def cheer(c, f0, f1, seed=0):
    c.face("happy", f0); f = f0 + seed % 3; k = 0
    while f <= f1:
        up = k % 2 == 0
        c.pose(f, armL=-160 if up else -140, armR=-160 if up else -140, armLs=30, armRs=30, bob=0.5 if up else 0); f += 3; k += 1

# ---------------------------------------------------------------- shots
def s01(N):  # hook: dark town, slow glide down the street toward the clock tower (it never turns orange)
    cam_move(cam, tgt, 1, N, (3, -24, 4.0), (1.0, -12, 3.2), (0, 20, 10), (0, 25, 9), 24, 28)
    pip.place((0.5, -4, 0.16), 0); pip.face("neutral")
def s02(N):  # pip in the dark looking up: 'nobody has ever seen a single light'
    pip.place((0, 0, 0.16), 0); pip.pose(1, head=15); pip.pose(N, head=22, headyaw=-10)
    cam_move(cam, tgt, 1, N, (0.8, -5.4, 2.4), (0.4, -4.4, 2.2), (0, 0, 3.0), (0, 0, 3.1), 34, 40)
def s03(N):  # the NO LIGHTS sign at the town hall, Mayor beside it
    sign.location = (5.5, 29.5, 0); mayor.place((1.5, 29.2, 0.06), 0); mayor.face("evil"); mayor.pose(1, armR=-70, armRs=-40)
    mayor.pose(N, armR=-80, armRs=-50, head=-5)
    cam_move(cam, tgt, 1, N, (2.0, 19.5, 2.6), (3.4, 21.0, 3.0), (3.5, 29.5, 3.2), (4.5, 29.5, 3.4), 28, 34)
def s04(N):  # Benny brushes his teeth in the dark (pokes his cheek)
    ben.place((300, -1, 0), 0); ben.face("frozen"); f = 1; k = 0
    while f <= N:
        ben.pose(f, armR=-130 + (10 if k % 2 else -10), armRs=-35 if k % 3 else -15, head=0, headyaw=(-6 if k % 2 else 6)); f += 2; k += 1
    cam_move(cam, tgt, 1, N, (300.4, -6.0, 2.9), (300.2, -5.2, 2.85), (300, -1, 2.8), (300, -1, 2.9), 36, 42)
def s05(N):  # the baker 'bakes in the dark': walks into his own door with the bread
    baker.place((-12, 6.5, 0.17), 180, 1); baker.place((-12, 9.0, 0.17), 180, N // 2); baker.walk(1, N // 2)
    baker.place((-12, 8.6, 0.17), 180, N // 2 + 2); baker.pose(N // 2 + 1, lean=-20, armR=-60); baker.face("shock", N // 2 + 1)
    cam_move(cam, tgt, 1, N, (-14.5, 1.0, 3.2), (-13.5, 2.2, 3.0), (-12, 8.5, 2.8), (-12, 9.0, 3.0), 30, 34)
def s06(N):  # grandma knits in the dark: a huge tangle
    gran.place((1098, 3.0, 0.5), 0); gran.face("determined"); yarn.location = (1098.6, 1.6, 1.6); yarn.scale = (1.4, 1.2, 1.1)
    f = 1; k = 0
    while f <= N: gran.pose(f, armL=-70 + (15 if k % 2 else 0), armR=-70 + (0 if k % 2 else 15), lean=8); f += 2; k += 1
    cam_move(cam, tgt, 1, N, (1096.0, -5.0, 3.2), (1096.6, -4.0, 3.0), (1098, 2.5, 2.4), (1098.3, 2.4, 2.3), 30, 34)
def s07(N):  # the dog walks into the same tree. bonk.
    a = int(N * 0.55)
    dog.root.location = (18, 4.5, 0.17); dog.root.rotation_euler = (0, 0, math.radians(180)); dog.root.keyframe_insert("location", frame=1)
    dog.root.location = (18, 8.35, 0.17); dog.root.keyframe_insert("location", frame=a)
    dog.root.location = (18, 7.6, 0.17); dog.root.keyframe_insert("location", frame=a + 2)
    dog.head.rotation_euler = (0, 0, 0); dog.head.keyframe_insert("rotation_euler", frame=a); dog.head.rotation_euler = (math.radians(-25), 0, 0); dog.head.keyframe_insert("rotation_euler", frame=a + 2)
    dog.root.rotation_euler = (0, 0, math.radians(180)); dog.root.keyframe_insert("rotation_euler", frame=a + 2)
    dog.root.rotation_euler = (math.radians(4), math.radians(-6), math.radians(180)); dog.root.keyframe_insert("rotation_euler", frame=a + 5)
    cam_move(cam, tgt, 1, N, (22.5, 3.0, 1.6), (22.0, 3.6, 1.5), (18, 7.5, 1.4), (18, 8.2, 1.5), 32, 38)
    if a + 2 <= N: shake(a, min(N, a + 4), 0.08)
def s08(N):  # attic: Pip opens the chest, something inside
    pip.place((301.5, -0.5, 0), -150); pip.face("surprised"); pip.pose(1, armL=-60, armR=-60, lean=20)
    candle_at((302.5, 1.6, 1.25), -15, 0.9); cflame.scale = (0.001, 0.001, 0.001); clight.data.energy = 0
    cam_move(cam, tgt, 1, N, (298.0, -5.5, 3.3), (299.0, -4.0, 2.8), (302, 1, 1.6), (302.4, 1.5, 1.4), 26, 32)
def s09(N):  # close: a tiny candle, smirking
    candle_at((302.5, 1.6, 1.25), -15, 0.9); cflame.scale = (0.001, 0.001, 0.001); clight.data.energy = 0
    pf = point("cfill09", (301.8, 0.2, 2.2), "#9fb0ff", 40, 0.5)
    cbrow.rotation_euler = (0, math.radians(-20), 0); cbrow.keyframe_insert("rotation_euler", frame=1)
    cbrow.location.z = 0.74; cbrow.keyframe_insert("location", frame=N // 2); cbrow.location.z = 0.8; cbrow.keyframe_insert("location", frame=N // 2 + 3)
    cam_move(cam, tgt, 1, N, (302.2, -1.6, 2.1), (302.3, -1.0, 2.0), (302.5, 1.6, 1.85), (302.5, 1.6, 1.85), 50, 58)
def s10(N):  # she touches the wick: FWOOSH (flame bursts, attic lights up)
    a = max(2, int(N * 0.4))
    pip.place((301.6, 0.2, 0), -160); pip.face("surprised"); pip.pose(1, armR=-40, lean=15); pip.pose(a, armR=-80, lean=25, head=10)
    candle_at((302.5, 1.6, 1.25), -15, 0.9)
    cflame.scale = (0.001, 0.001, 0.001); cflame.keyframe_insert("scale", frame=a); clight.data.energy = 0; clight.data.keyframe_insert("energy", frame=a)
    cflame.scale = (2.2, 2.2, 2.6); cflame.keyframe_insert("scale", frame=a + 2); clight.data.energy = 400; clight.data.keyframe_insert("energy", frame=a + 2)
    flame_flicker(a + 4, N, 1.3)
    cam_move(cam, tgt, 1, N, (299.3, -3.0, 2.6), (299.6, -2.6, 2.5), (302.2, 1.2, 1.9), (302.2, 1.2, 2.0), 30, 34)
def s11(N):  # her fingers start to glow (hand up, close)
    pip.place((301.0, 0.0, 0), -20); pip.face("surprised"); pip.pose(1, armR=-100, armRs=10, head=-5)
    hand_glow(False, 1); hand_glow(True, max(2, N // 3))
    candle_at((302.5, 1.6, 1.25), -15, 0.9); flame_flicker(1, N, 1.0)
    cam_move(cam, tgt, 1, N, (300.2, -3.8, 3.0), (300.4, -3.2, 3.0), (300.9, -0.6, 3.1), (300.9, -0.6, 3.2), 38, 44)
def s12(N):  # she taps her old lantern: BOOM, it lights up
    a = max(2, N // 3)
    pip.place((299.0, -1.0, 0), 40); pip.face("happy"); hand_glow(True); pip.pose(1, armR=-40); pip.pose(a, armR=-75, lean=10)
    lant.location = (298.0, -2.4, 1.6); emit(LANTM, 0.0, a); lkey(lantl, 0, a); emit(LANTM, 6, a + 2); lkey(lantl, 600, a + 2)
    sc.objects["desk"].location = BASE["desk"][0]
    cam_move(cam, tgt, 1, N, (296.0, -6.5, 2.6), (296.5, -5.8, 2.4), (298.4, -1.8, 2.1), (298.3, -2.0, 2.0), 32, 36)
    shake(a + 1, min(N, a + 4), 0.06)
def s13(N):  # the cat walks by, brushes her leg, and starts glowing (not happy about it)
    a = N // 2
    cat.root.location = (296, -1.5, 0); cat.root.rotation_euler = (0, 0, math.radians(-90)); cat.root.keyframe_insert("location", frame=1)
    cat.root.location = (300.5, -1.5, 0); cat.root.keyframe_insert("location", frame=a)
    emit(CATM, 0.0, a - 1, "#9fd8ff"); emit(CATM, 6, a + 2)
    lant.location = (298.0, -2.4, 1.6); emit(LANTM, 6); lantl.data.energy = 600
    pip.place((301.5, -0.2, 0), 200); pip.face("happy"); hand_glow(True)
    cat.head.rotation_euler = (0, 0, 0); cat.head.keyframe_insert("rotation_euler", frame=a + 2)
    cat.head.rotation_euler = (0, 0, math.radians(70)); cat.head.keyframe_insert("rotation_euler", frame=a + 5)
    cam_move(cam, tgt, 1, N, (297.0, -6.0, 1.4), (298.6, -6.0, 1.2), (297.5, -1.5, 0.8), (300.5, -1.5, 0.7), 30, 34)
def s14(N):  # she runs outside, down the dark street
    pip.place((-6, -3.5, 0.16), -90, 1); pip.place((4, -3.5, 0.16), -90, N); pip.run(1, N, 6, 45, 12); pip.face("happy"); hand_glow(True)
    cam_move(cam, tgt, 1, N, (-8, -11, 2.2), (3, -11, 2.2), (-6, -3, 2.0), (4, -3, 2.0), 28, 28)
def s15(N):  # high-five Benny: WHOOSH, his hoodie shines
    a = max(2, int(N * 0.4))
    pip.place((-1.2, -3.5, 0.16), -90); pip.face("happy"); hand_glow(True)
    ben.place((1.2, -3.5, 0.16), 90); ben.face("surprised")
    pip.pose(1, armR=-60); pip.pose(a, armR=-160, armRs=-10); ben.pose(1, armL=-60); ben.pose(a, armL=-160, armLs=-10)
    emit(ben.mtop, 0.0, a, "#ff6a4a"); lkey(benl, 0, a); emit(ben.mtop, 4, a + 2); lkey(benl, 500, a + 2)
    ben.face("happy", a + 3)
    cam_move(cam, tgt, 1, N, (0.6, -12.5, 3.0), (0.2, -11.0, 3.4), (0, -3.5, 2.6), (0, -3.5, 3.2), 26, 28)
    shake(a, min(N, a + 3), 0.05)
def s16(N):  # Benny shines: close, he looks at his glowing hoodie
    ben.place((1.2, -3.5, 0.16), 0); ben.face("happy"); emit(ben.mtop, 4, None, "#ff6a4a"); benl.data.energy = 500
    ben.pose(1, armL=-30, armR=-30, head=20); ben.pose(N, armL=-70, armR=-70, armLs=30, armRs=30, head=-5)
    cam_move(cam, tgt, 1, N, (2.4, -8.6, 2.2), (1.8, -7.8, 2.6), (1.2, -3.5, 2.8), (1.2, -3.5, 3.0), 32, 36)
def s17(N):  # bakery window: every loaf glows like gold
    a = max(2, N // 3)
    ben.place((-13.8, 7.6, 0.17), 180); emit(ben.mtop, 4, None, "#ff6a4a"); benl.data.energy = 500; ben.pose(1, armR=-40); ben.pose(a, armR=-95)
    baker.place((-8.6, 7.0, 0.17), 150); baker.face("shock", a + 2)
    emit(LOAFM, 0.0, a); emit(LOAFM, 14, a + 3)
    wl = point("bakelight", (-12, 8.6, 3.4), "#ffcf6a", 0, 1.0); lkey(wl, 0, a); lkey(wl, 900, a + 3)
    cam_move(cam, tgt, 1, N, (-15.5, 0.5, 2.6), (-14.5, 1.8, 3.0), (-12, 9.5, 2.8), (-12, 9.7, 3.0), 28, 34)
def s18(N):  # grandma's knitting lights up... it's a sock for a horse
    a = max(2, int(N * 0.35))
    gran.place((1096.5, 3.0, 0.5), 20); gran.face("neutral"); gran.pose(1, armL=-60, armR=-60, lean=5)
    sock.location = (1099.6, 1.4, 0.0); sock.scale = (1.0, 1.0, 1.0)
    emit(SOCKM, 0.0, a); emit(SOCKM, 10, a + 3); gran.face("surprised", a + 3)
    sl = point("socklight", (1099.6, -0.5, 2.5), "#ff8a6a", 0, 1.0); lkey(sl, 0, a); lkey(sl, 700, a + 3)
    cam_move(cam, tgt, 1, N, (1095.0, -5.2, 2.6), (1096.5, -6.5, 4.0), (1098, 1.8, 2.2), (1098.5, 1.5, 2.6), 30, 26)
def s19(N):  # street lamps: pop, pop, pop, pop (one by one down the street)
    pip.place((-4, -3.5, 0.16), 0); pip.face("happy"); hand_glow(True)
    which = [i for i, b in enumerate(BULB) if b[4] > 0]   # the north-side row, left to right
    step = max(2, N // (len(which) + 1))
    for j, i in enumerate(which):
        emit(BULB[i][1], 0.0, 1 + j * step); lkey(BULB[i][2], 0, 1 + j * step)
        emit(BULB[i][1], 18, 2 + j * step); lkey(BULB[i][2], 1800, 2 + j * step)
    cam_move(cam, tgt, 1, N, (-30, -9, 4.5), (25, -9, 4.5), (-28, 6, 3.5), (27, 6, 3.5), 24, 24)
def lit_street(): lamps_on(); emit(ben.mtop, 4, None, "#ff6a4a")
def s20(N):  # the town hall doors slam open (light spills out)
    lit_street()
    mayor.place((0, 32.2, 0.06), 0, 1); mayor.place((0, 28.5, 0.06), 0, N); mayor.walk(1, N); mayor.face("evil", 1)
    sc.objects["hallglow"].data.energy = 1200
    cam_move(cam, tgt, 1, N, (1.0, 16.0, 3.0), (0.5, 19.5, 3.2), (0, 30, 3.8), (0, 29, 3.4), 28, 32)
    shake(1, 4, 0.12)
def s21(N):  # Mayor: 'Lights are against the rules!'
    lit_street(); mayor.place((0, 28.5, 0.06), 0); mayor.face("evil"); mayor.talk(1, N - 2, 0.16, 2)
    mayor.pose(1, armR=-90, lean=-5); mayor.pose(N // 2, armR=-120, armL=-20, lean=8); mayor.pose(N, armR=-100, lean=5)
    cam_move(cam, tgt, 1, N, (0.6, 23.4, 2.6), (0.3, 24.4, 2.7), (0, 28.5, 3.6), (0, 28.5, 3.7), 32, 38)
def s22(N):  # he blows the lamps out one by one, the street goes dark again
    which = [i for i, b in enumerate(BULB) if b[4] > 0]; which = which[::-1]
    lamps_on(); step = max(2, N // (len(which) + 1))
    mayor.place((30, 5.5, 0.17), 90, 1); mayor.place((-26, 5.5, 0.17), 90, N); mayor.walk(1, N, 10); mayor.face("evil", 1)
    for j, i in enumerate(which):
        emit(BULB[i][1], 18, 1 + j * step); lkey(BULB[i][2], 1800, 1 + j * step)
        emit(BULB[i][1], 0.0, 3 + j * step); lkey(BULB[i][2], 0, 3 + j * step)
    cam_move(cam, tgt, 1, N, (34, -6, 4.0), (-20, -6, 4.0), (30, 6, 3.0), (-24, 6, 3.0), 26, 26)
def s23(N):  # everyone freezes; Pip looks down at the candle in her hand
    crowd_in_square("frozen", 6, 17.0); pip.place((0, 13.0, 0.06), 0); pip.face("scared"); candle_in_hand(pip, 0); flame_flicker(1, N, 0.8)
    pip.pose(1, armL=-60, head=0); pip.pose(N, armL=-70, head=-25)
    for c in crowd: c.pose(armL=-40, armR=-40, armLs=30, armRs=30)
    cam_move(cam, tgt, 1, N, (2.5, 8.0, 3.4), (1.8, 9.0, 3.2), (0, 13, 2.8), (0, 13, 2.4), 30, 36)
def s24(N):  # the candle whispers: 'Light the clock.' (extreme close)
    pip.place((0, 13.0, 0.06), 0); pip.face("scared"); candle_in_hand(pip, 0); pip.pose(armL=-75, head=-25); flame_flicker(1, N, 0.9)
    candle_talk(N // 2, N - 2, 2)
    bpy.context.view_layer.update(); p = cnd.matrix_world.translation.copy()
    cam_move(cam, tgt, 1, N, (p.x + 0.6, p.y - 2.6, p.z + 0.4), (p.x + 0.35, p.y - 2.0, p.z + 0.3), (p.x, p.y, p.z + 0.5), (p.x, p.y, p.z + 0.5), 50, 60)
def s25(N):  # Pip climbs the tower stairs, total darkness, her hand is the only light
    hand_glow(True, boost=8)
    for f in range(1, N + 1, 2):
        a = math.radians(-60 + f * 2.2); r = 3.6
        pip.place((500 + r * math.cos(a), r * math.sin(a), 0.25 + 0.45 * (-60 + f * 2.2) / 18 + 4.0), math.degrees(a) + 180, f)
    pip.run(1, N, 6, 40, 10); pip.face("determined")
    for f in (1, N // 2, N):
        a = math.radians(-60 + f * 2.2 - 40); z = 0.25 + 0.45 * (-60 + f * 2.2) / 18 + 4.0
        cam.location = (500 + 5.4 * math.cos(a), 5.4 * math.sin(a), z + 3.4); cam.keyframe_insert("location", frame=f)
        a2 = math.radians(-60 + f * 2.2); tgt.location = (500 + 3.6 * math.cos(a2), 3.6 * math.sin(a2), z + 2.4); tgt.keyframe_insert("location", frame=f)
    cam.data.lens = 18
def s26(N):  # halfway: her hand flickers, the light is running out
    a = math.radians(30); r = 3.6
    pip.place((500 + r * math.cos(a), r * math.sin(a), 0.25 + 0.45 * 30 / 18 + 4.0), math.degrees(a) + 180); pip.face("scared"); pip.pose(1, armR=-90, head=-10)
    rr = random.Random(2)
    for f in range(1, N + 1, 2):
        k = max(0.12, 1 - f / N) * rr.uniform(0.3, 1.0); hand_glow(True, f, k, 8)
    bpy.context.view_layer.update(); p = pip.root.location
    a2 = math.radians(-10); c0 = (500 + 5.6 * math.cos(a2), 5.6 * math.sin(a2), p.z + 3.2)
    cam_move(cam, tgt, 1, N, c0, (c0[0], c0[1] + 0.3, c0[2] - 0.2), (p.x, p.y, p.z + 2.6), (p.x, p.y, p.z + 2.7), 24, 28)
def s27(N):  # clock room: she presses her hand on the giant clock face
    a = max(2, int(N * 0.6))
    pip.place((700, 7.4, 0), 180); pip.face("determined"); hand_glow(True, 1, 0.3); pip.pose(1, armR=-40); pip.pose(a, armR=-100, lean=-5)
    emit(CRFACE, 0.0, a); emit(CRFACE, 12, a + 2); hand_glow(True, a, 1.0)
    cl = point("crblaze", (700, 6, 9), "#ffd08a", 0, 3.0); lkey(cl, 0, a); lkey(cl, 6000, a + 2)
    cam_move(cam, tgt, 1, N, (694, 0, 4.5), (695.5, 1.0, 5.5), (700, 8, 6), (700, 8.5, 8), 24, 22)
    shake(a, min(N, a + 4), 0.1)
def s28(N):  # outside: BOOM, the clock blazes and the light rolls over every roof (windows turn on by distance)
    emit(CLOCKM, 0.0, 1); emit(CLOCKM, 25, 3); sc.objects["towerglow"].data.energy = 3000
    tg = sc.objects["towerglow"]; tg.data.color = lib.srgb("#ffd08a"); lkey(tg, 0, 1); lkey(tg, 4000, 3)
    dmax = max(d for _, _, d in WIN)
    for _, m, d in WIN:
        f = 3 + int((N - 6) * d / dmax); emit(m, 0.0, f); emit(m, 6, f + 2)
    for b in BULB:
        f = 3 + int((N - 6) * math.dist((b[3], b[4]), (0, 34)) / dmax); emit(b[1], 0.0, f); emit(b[1], 18, f + 2)
        if b[2]: lkey(b[2], 0, f); lkey(b[2], 1800, f + 2)
    cam_move(cam, tgt, 1, N, (0, 24, 16), (0, -30, 26), (0, 33, 17.5), (0, 20, 6), 30, 26)
    shake(1, 6, 0.25)
def s29(N):  # the sky turns orange; the sun comes up for the first time (time-lapse, keyframed world)
    lamps_on(); windows_on(); emit(CLOCKM, 25)
    c0, c1 = lib.srgb("#141a3e"), lib.srgb("#ffb37a")
    for f in range(1, N + 1, 2):
        k = min(1, f / (N * 0.8)); k = k * k * (3 - 2 * k)
        bg.inputs["Color"].default_value = (*[a + (b - a) * k for a, b in zip(c0, c1)], 1); bg.inputs["Color"].keyframe_insert("default_value", frame=f)
        bg.inputs["Strength"].default_value = 0.9 + 0.2 * k; bg.inputs["Strength"].keyframe_insert("default_value", frame=f)
        sun.data.energy = 1.4 + 1.4 * k; sun.data.keyframe_insert("energy", frame=f)
        sun.data.color = [a + (b - a) * k for a, b in zip(lib.srgb("#7f96ff"), lib.srgb("#ffb070"))]; sun.data.keyframe_insert("color", frame=f)
    crowd_in_square("surprised", 6, 19.0); pip.place((0, 15.5, 0.06), 180); pip.face("happy")
    cam_move(cam, tgt, 1, N, (-6, 4, 2.0), (-4, 6, 2.6), (0, 30, 9), (0, 35, 14), 22, 22)
def day(): lamps_on(); windows_on(0.4); emit(CLOCKM, 8); sunrise(1.0)
def s30(N):  # the whole town cheers (jumping crowd, Benny, baker, gran)
    day(); crowd_in_square("happy", 6, 19.0)
    for i, c in enumerate(crowd): cheer(c, 1, N, i)
    pip.place((0, 16.0, 0.06), 180); cheer(pip, 1, N, 2); ben.place((-3, 16.4, 0.06), 170); cheer(ben, 1, N, 1)
    cam_move(cam, tgt, 1, N, (0, 29.0, 4.0), (1.5, 29.5, 5.0), (0, 17, 2.6), (0, 17, 2.8), 22, 24)
def s31(N):  # ...except the Mayor (grumpy, alone on the steps)
    day(); mayor.place((0, 29.0, 0.06), 0); mayor.face("evil"); mayor.pose(1, armL=-20, armR=-20, armLs=20, armRs=20)
    cam_move(cam, tgt, 1, N, (1.5, 23.0, 2.2), (1.0, 24.0, 2.4), (0, 29, 3.6), (0, 29, 3.8), 34, 40)
def s32(N):  # he takes off his hat... a tiny lamp is hidden inside
    day(); mayor.place((0, 29.0, 0.06), 0); mayor.face("scared")
    a = max(2, N // 3)
    mayor.pose(1, armR=-150, armRs=-10); mayor.pose(a, armR=-170, armRs=-15)
    mayor.hat.location = (0, 0, 1.05 * mayor.hs); mayor.hat.keyframe_insert("location", frame=a)
    mayor.hat.location = (0.4, 0, 2.4 * mayor.hs); mayor.hat.keyframe_insert("location", frame=a + 4)
    lkey(hatl, 0, a); lkey(hatl, 300, a + 3)
    for c in crowd[:3]: pass
    cam_move(cam, tgt, 1, N, (0.8, 24.8, 3.6), (0.5, 25.6, 3.8), (0, 29, 4.4), (0, 29, 5.0), 36, 42)
def s33(N):  # Pip and Benny stare; the Mayor shrugs: he just didn't want to share
    day(); mayor.place((0, 29.0, 0.06), 0); mayor.face("happy"); mayor.hat.location = (0.4, 0, 2.4 * mayor.hs); hatl.data.energy = 300
    mayor.pose(1, armR=-170, armRs=-15); mayor.pose(N // 2, armR=-170, armRs=-15, armL=-30, armLs=40, head=8)
    pip.place((-3.2, 25.0, 0.06), 150); pip.face("surprised"); ben.place((3.2, 25.0, 0.06), 210); ben.face("surprised")
    cam_move(cam, tgt, 1, N, (-4.5, 21.0, 3.4), (-3.5, 21.5, 3.6), (0, 28, 3.4), (0, 28.5, 3.8), 26, 30)
def s34(N):  # the candle on the tower ledge smirks... and blows himself out
    day(); candle_at((1.5, 32.6, 9.0), 0, 1.0)
    a = int(N * 0.62)
    flame_flicker(1, a, 1.0)
    cmouth.scale = (0.6, 1, 2.6); cmouth.keyframe_insert("scale", frame=a - 2)
    cflame.scale = (1, 1, 1); cflame.keyframe_insert("scale", frame=a); cflame.scale = (0.001, 0.001, 0.001); cflame.keyframe_insert("scale", frame=a + 3)
    clight.data.energy = 60; clight.data.keyframe_insert("energy", frame=a); clight.data.energy = 0; clight.data.keyframe_insert("energy", frame=a + 3)
    candle_talk(2, a - 4, 2)
    cam_move(cam, tgt, 1, N, (1.9, 29.0, 9.5), (1.75, 29.8, 9.5), (1.5, 32.6, 9.7), (1.5, 32.6, 9.7), 48, 56)

SHOTS = [("s01", 0.0, s01), ("s02", L[0] + 1.9, s02), ("s03", L[1], s03), ("s04", L[2], s04), ("s05", L[2] + 1.7, s05),
         ("s06", L[3], s06), ("s07", L[4], s07), ("s08", L[5], s08), ("s09", L[6], s09), ("s10", L[7], s10), ("s11", L[8], s11),
         ("s12", L[9], s12), ("s13", L[10], s13), ("s14", L[11], s14), ("s15", L[11] + 1.6, s15), ("s16", L[11] + 3.0, s16),
         ("s17", L[12], s17), ("s18", L[13], s18), ("s19", L[14], s19), ("s20", L[15], s20), ("s21", L[16], s21),
         ("s22", L[17], s22), ("s23", L[18], s23), ("s24", L[19], s24), ("s25", L[20], s25), ("s26", L[21], s26),
         ("s27", L[22], s27), ("s28", L[23], s28), ("s29", L[24], s29), ("s30", L[25], s30), ("s31", L[25] + 1.0, s31),
         ("s32", L[26], s32), ("s33", L[27], s33), ("s34", L[28], s34)]
TIMES = [(sid, t, (SHOTS[i + 1][1] if i + 1 < len(SHOTS) else END), fn) for i, (sid, t, fn) in enumerate(SHOTS)]
os.makedirs(W, exist_ok=True)
json.dump([(sid, t0, t1) for sid, t0, t1, _ in TIMES], open(f"{W}/shots_timing.json", "w"))

only = [a for a in sys.argv[1:] if a.startswith("s")]
for sid, t0, t1, fn in TIMES:
    if only and sid not in only: continue
    N = max(2, round((t1 - t0) * FPS)); d = f"{W}/shots/{sid}"
    if not PREV and os.path.exists(f"{d}/done"): continue
    os.makedirs(d, exist_ok=True); reset(); fn(N)
    if PREV:
        sc.frame_set(max(1, int(N * 0.7))); sc.render.filepath = f"{W}/stills/{sid}.png"; bpy.ops.render.render(write_still=True)
        continue
    sc.frame_start, sc.frame_end = 1, N; sc.render.filepath = f"{d}/"
    t = time.time(); bpy.ops.render.render(animation=True)
    open(f"{d}/done", "w").write(str(N)); print(sid, N, "frames", round(time.time() - t), "s", flush=True)
