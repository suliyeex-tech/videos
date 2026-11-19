"""In This Town #2 (hustle variant): Whisper Boy vs the Big Shout Festival. Daylight town + festival square + bear.
python3 whisper_shots.py [sid ...] [--still]   -> /home/claude/work/<slug>/shots/<sid>/####.png (resumable)"""
import sys, os, json, math, random, time, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move

SLUG = "2026-11-19-in-this-town-everyone-shouts"; FPS = 12
W = f"/home/claude/work/{SLUG}"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; END = vo["total"] + 0.6
PREV = "--still" in sys.argv
sc, cam, tgt = lib.setup(res=(432, 768) if not PREV else (216, 384), samples=8 if not PREV else 4, fps=FPS)
town = lib.build_town(); lib.build_bedroom(300)

# ---------------------------------------------------------------- daylight look
bg = sc.world.node_tree.nodes["Background"]; bg.inputs["Color"].default_value = (*lib.srgb("#8fc8ff"), 1); bg.inputs["Strength"].default_value = 1.5
sun = sc.objects["moonlight"]; sun.data.energy = 4.5; sun.data.color = lib.srgb("#fff0d8"); sun.rotation_euler = (math.radians(50), 0, math.radians(215))
sc.objects["moon"].hide_render = True
for o in list(sc.objects):
    if o.type == "LIGHT" and o.name.startswith("lamp"): o.data.energy = 0
sc.view_settings.exposure = 0.3

# ---------------------------------------------------------------- festival square (in front of the town hall)
plaza = cube("plaza", (0, 23, 0.02), (34, 18, 0.06), mat("plaza", "#c9b79a", 0.85), 0)
wood, wood2 = mat("stagewood", "#9a5a32", 0.7), mat("stageskirt", "#c8282f", 0.6)
cube("stage", (0, 27.5, 0.7), (12, 5, 1.4), wood, 0.05)
for i in range(12): cube(f"skirt{i}", (-5.5 + i, 24.98, 0.6), (0.96, 0.06, 1.2), wood2 if i % 2 else mat("skirtw", "#f2efe6", 0.6), 0.0)
cube("stepsS", (0, 24.4, 0.3), (2.4, 1.2, 0.6), wood, 0.04)
trophy = empty("trophy", (2.5, 27.5, 1.4))
gold = mat("tgold", "#f2c53d", 0.2, 0.6, "#ffcf4a", metal=1.0)
cube("tbase", (0, 0, 0.25), (0.9, 0.9, 0.5), mat("tblack", "#222222", 0.4), 0.05, trophy)
cyl("tstem", (0, 0, 0.75), 0.12, 0.6, gold, parent=trophy, verts=12)
bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.35, radius2=0.75, depth=1.0, location=(0, 0, 1.5)); cup = bpy.context.object; cup.parent = trophy; cup.data.materials.append(gold)
for sd in (-1, 1): cube(f"thandle{sd}", (0.8 * sd, 0, 1.55), (0.14, 0.14, 0.6), gold, 0.05, trophy)
point("tglow", (2.5, 26.5, 3.6), "#ffd86a", 120, 0.3)
# bunting
rnd = random.Random(3); cols = ["#e8423f", "#f2c53d", "#3f8fd8", "#57b65a", "#e86fb0"]
for side in (-1, 1):
    cyl(f"bpole{side}", (8.5 * side, 26, 3), 0.15, 6, mat("pole", "#2b2d36", 0.4, metal=0.6), verts=8)
for i in range(17):
    x = -8 + i; z = 5.6 - 0.9 * math.sin(math.pi * i / 16)
    cube(f"flag{i}", (x, 26, z - 0.35), (0.6, 0.05, 0.7), mat(f"flag{i % 5}", cols[i % 5], 0.6), 0.0, None, (0, math.radians(45), 0))
# banner (text) above the stage
cube("bannerbg", (0, 29.9, 6.8), (11, 0.2, 1.8), mat("bannerbg", "#c8282f", 0.6), 0.05)
def mktext(name, body, loc, size, col, emit=0.0):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = 0.04
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = (math.radians(90), 0, 0)
    cu.materials.append(mat(name + "m", col, 0.5, emit)); return o
t_shout = mktext("t_shout", "BIG SHOUT FESTIVAL", (0, 29.75, 6.8), 1.0, "#ffe58a", 1.5)
t_whisp = mktext("t_whisp", "BIG WHISPER FESTIVAL", (0, 29.75, 6.8), 0.92, "#ffffff", 1.5); t_whisp.hide_render = True
# megaphone
mega = empty("mega", (0, -0.35, -1.0))
bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=0.12, radius2=0.5, depth=1.1, location=(0, 0, 0), rotation=(math.radians(90), 0, 0))
mc = bpy.context.object; mc.parent = mega; mc.data.materials.append(mat("megam", "#f2efe6", 0.4)); mc.location = (0, -0.4, 0)

# ---------------------------------------------------------------- cast
hero = lib.Char("hero", top="#f2b51f", pants="#2f4a7a", hair="#3a2414", hood=True, extra="#d89a12")
ben = lib.Char("benny", skin="#c98d62", top="#d8423f", pants="#3b3b55", hair="#1d1310", hair_style="flat")
cube("bencap", (0, -0.15, 1.05), (1.08, 1.2, 0.25), mat("bencap", "#2f63d6", 0.5), 0.06, ben.neck)
baker = lib.Char("baker", skin="#f0c29a", top="#f4f4f4", pants="#5a5a6a", hair="#5b4636", hair_style="flat", kid=False)
cyl("bakerhat", (0, 0, 1.45), 0.48, 0.9, mat("bakerhat", "#ffffff", 0.6), parent=baker.neck, verts=16)
bread = cube("bread", (0, -0.5, -1.05), (0.9, 0.5, 0.45), mat("bread", "#c98a3a", 0.8), 0.2, baker.arms[1])
gran = lib.Char("gran", skin="#e9b892", top="#8b4fb0", pants="#8b4fb0", hair="#eeeeee", hair_style="flat", kid=False)
cube("granbun", (0, 0.35, 1.1), (0.5, 0.5, 0.4), gran.mhair, 0.15, gran.neck)
sis = lib.Char("sis", skin="#f3c89a", top="#57b65a", pants="#e86fb0", hair="#e0702e", hair_style="flat")
mayor = lib.Char("mayor", skin="#f0c29a", top="#23253b", pants="#23253b", hair="#5b4636", hair_style="flat", kid=False); mayor.mayor_kit()
crowd = []
CC = [("#3f8fd8", "#6b3f22"), ("#e86fb0", "#1d1310"), ("#57b65a", "#e0c070"), ("#8b4fb0", "#6b3f22"), ("#e8823f", "#1d1310"),
      ("#2fb0a8", "#e0702e"), ("#c94a4a", "#3a2414"), ("#6a7ad8", "#eeeeee")]
for i, (top, hair) in enumerate(CC):
    crowd.append(lib.Char(f"cr{i}", skin=["#f3c89a", "#c98d62", "#8d5a3b", "#e9b892"][i % 4], top=top, pants=["#3b3b55", "#c9b48a", "#2f4a7a"][i % 3],
                          hair=hair, hair_style="spiky" if i % 3 == 0 else "flat", kid=i % 2 == 0))
dog = lib.Dog("dog", "#a8682f"); cat = lib.Dog("cat", "#8a8f9c")
cat.root.scale = (0.55, 0.55, 0.55)

class Bear:
    def __init__(self, s=2.3):
        fur, dk, sn = mat("bearfur", "#6b4226", 0.85), mat("beardk", "#3d2414", 0.85), mat("bearsn", "#c9a17a", 0.8)
        blk = mat("eyeblack", "#141414", 0.25)
        self.root = empty("bear"); self.root.scale = (s, s, s)
        self.body = cube("bear_body", (0, 0, 1.5), (1.9, 2.6, 1.7), fur, 0.25, self.root)
        cube("bear_belly", (0, -1.0, 1.4), (1.3, 0.8, 1.2), sn, 0.2, self.root)
        self.neck = empty("bear_neck", (0, -1.4, 2.4), self.root)
        cube("bear_head", (0, -0.4, 0.3), (1.5, 1.3, 1.3), fur, 0.25, self.neck)
        cube("bear_snout", (0, -1.15, 0.05), (0.7, 0.5, 0.55), sn, 0.15, self.neck)
        cube("bear_nose", (0, -1.42, 0.25), (0.32, 0.08, 0.2), blk, 0.05, self.neck)
        self.mouth = cube("bear_mouth", (0, -1.41, -0.12), (0.45, 0.04, 0.06), mat("bearmouth", "#5a1414", 0.5), 0.0, self.neck)
        self.eyes = []
        for sd in (-1, 1):
            sphere(f"bear_ear{sd}", (0.6 * sd, -0.3, 1.0), (0.32, 0.18, 0.32), dk, self.neck, 10)
            self.eyes.append(sphere(f"bear_eye{sd}", (0.36 * sd, -1.06, 0.55), (0.13, 0.04, 0.17), blk, self.neck, 10))
        self.legs = []
        for i, (x, y) in enumerate(((-0.6, -0.9), (0.6, -0.9), (-0.6, 0.9), (0.6, 0.9))):
            h = empty(f"bear_hip{i}", (x, y, 1.0), self.root); cube(f"bear_leg{i}", (0, 0, -0.5), (0.65, 0.7, 1.05), dk, 0.12, h); self.legs.append(h)
    def eyes_open(self, k, f=None):   # 0 shut .. 1 open
        for e in self.eyes:
            e.scale = (0.13, 0.04, 0.17 * max(0.08, k))
            if f is not None: e.keyframe_insert("scale", frame=f)
    def roar(self, k, f=None):
        self.mouth.scale = (1, 1, max(1, k * 9)); self.mouth.location.z = -0.12 - 0.02 * k * 9
        if f is not None: self.mouth.keyframe_insert("scale", frame=f); self.mouth.keyframe_insert("location", frame=f)
bear = Bear()
# birds
birds = []
for i in range(9):
    b = empty(f"bird{i}"); b.scale = (2, 2, 2); cube(f"birdb{i}", (0, 0, 0), (0.3, 0.6, 0.25), mat("bird", "#f4f4f4", 0.6), 0.05, b)
    for sd in (-1, 1): cube(f"birdw{i}{sd}", (0.4 * sd, 0, 0.05), (0.6, 0.35, 0.05), mat("bird", "#f4f4f4", 0.6), 0.0, b)
    birds.append(b)
# living room (gran + TV) at x=1100, hallway at x=1300, under-stage crawlspace at x=900
def room(ox, wallc, floorc):
    cube(f"rf{ox}", (ox, 0, -0.05), (16, 16, 0.1), mat(f"rfm{ox}", floorc, 0.7), 0)
    cube(f"rb{ox}", (ox, 6, 4), (16, 0.3, 8), mat(f"rwm{ox}", wallc, 0.8), 0); cube(f"rl{ox}", (ox - 7, 0, 4), (0.3, 16, 8), mat(f"rwm{ox}", wallc, 0.8), 0)
    cube(f"rr{ox}", (ox + 7, 0, 4), (0.3, 16, 8), mat(f"rwm{ox}", wallc, 0.8), 0)
room(1100, "#d8825a", "#7a5236")
cube("sofa", (1098, 3.5, 0.7), (5, 2, 1.4), mat("sofa", "#3f6fb0", 0.8), 0.25); cube("sofaback", (1098, 4.4, 1.6), (5, 0.6, 1.6), mat("sofa", "#3f6fb0", 0.8), 0.25)
cube("tvstand", (1101.5, -2.5, 0.6), (3.2, 1.2, 1.2), mat("tvstand", "#5a3b26"), 0.05)
cube("tv", (1101.5, -2.5, 2.3), (3.0, 0.3, 1.9), mat("tvbody", "#151515", 0.3), 0.06)
cube("tvscreen", (1101.5, -2.33, 2.3), (2.7, 0.05, 1.6), mat("tvscreen", "#20242a", 0.15), 0)
point("lvlamp", (1096, 1, 5), "#ffd2a0", 500, 1.0)
room(1300, "#7a9ad8", "#8a6a4a")
cube("sisdoor", (1300, 5.84, 1.9), (2.0, 0.08, 3.8), mat("doorw", "#f2efe6", 0.6), 0.03)
cube("doorgap", (1300, 5.88, 1.9), (2.1, 0.02, 3.9), mat("doordk", "#1a1a22", 0.6), 0)
point("halllamp", (1300, 0, 7), "#ffe2b8", 700, 1.0)
cube("crawl_floor", (900, 0, -0.05), (20, 20, 0.1), mat("dirt", "#3a2c22", 0.95), 0)
for i in range(14): cube(f"plank{i}", (893.5 + i, 0, 6.5), (0.94, 20, 0.3), mat("plank", "#4a3020", 0.8), 0.0)
for i in range(13): cube(f"slit{i}", (894 + i, 0, 6.66), (0.06, 20, 0.02), mat("slit", "#fff1c8", 0.5, 30.0), 0.0)
crawl_l = point("crawl_l", (900, -3, 4), "#ffcf8a", 140, 2.0)

fill = point("camfill", (0.6, 0.4, 0.2), "#ffe6cc", 160, 1.0, cam)
for o in mega.children_recursive: o.hide_render = True
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
WORLD = (tuple(bg.inputs["Color"].default_value), bg.inputs["Strength"].default_value)
OFF = (0, 0, -500)
CAST = [hero, ben, baker, gran, sis, mayor] + crowd

def reset():
    for o in OBJ:
        o.animation_data_clear()
        if o.type == "CAMERA" and o.data.animation_data: o.data.animation_data_clear()
        l, r, s, h = BASE[o.name]; o.location, o.rotation_euler, o.scale, o.hide_render = l, r, s, h
        if o.type == "LIGHT":
            o.data.energy = LIGHTS[o.name]
            if o.data.animation_data: o.data.animation_data_clear()
    bg.inputs["Color"].default_value = WORLD[0]; bg.inputs["Strength"].default_value = WORLD[1]
    trophy.parent = None; mega.parent = None; sun.data.color = lib.srgb("#fff0d8")
    am = sc.objects["alarmface"].data.materials[0]
    if am.node_tree.animation_data: am.node_tree.animation_data_clear()
    am.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 3.0
    for c in CAST: c.place(OFF); c.pose(); c.face("neutral")
    for a in (dog, cat): a.root.location = OFF
    bear.root.location = OFF; bear.eyes_open(1); bear.roar(0)
    for b in birds: b.location = OFF
    cam.data.lens = 28; cam.delta_location = (0, 0, 0)

def show(objs, on=True):
    for o in objs: o.hide_render = not on
def megaphone(ch):
    mega.parent = ch.arms[1]; mega.location = (0, -0.35, -1.0); show(mega.children_recursive)
def shake(f0, f1, amt=0.15, seed=1):
    r = random.Random(seed)
    for f in range(f0, f1 + 1):
        cam.delta_location = (r.uniform(-amt, amt), r.uniform(-amt, amt), r.uniform(-amt, amt)); cam.keyframe_insert("delta_location", frame=f)
def shh(c, f=None):   # finger-to-lips pose
    c.pose(f, armR=-118, armRs=-28, head=-4); c.face("determined", f)
def tiptoe(c, f0, f1, period=8):
    f = f0; k = 0
    while f <= f1:
        s = 1 if k % 2 == 0 else -1
        c.pose(f, armL=-25, armR=-25, armLs=20, armRs=20, legL=-18 * s, legR=18 * s, lean=8, bob=0.1); f += period / 2; k += 1
def shout(c, f0, f1, rate=3):
    c.face("surprised", f0); c.pose(f0, armL=-150, armR=-150, armLs=25, armRs=25, head=10)
    f = f0; k = 0
    while f <= f1:
        c.mouth.scale = (1.6, 1, (0.26 if k % 2 == 0 else 0.18) / 0.045); c.mouth.keyframe_insert("scale", frame=f); f += rate; k += 1
def laugh(c, f0, f1, seed=0):
    c.face("happy", f0); f = f0 + seed % 3; k = 0
    while f <= f1:
        c.pose(f, armL=-30 if k % 2 else -10, armR=-100, lean=-8 if k % 2 else 4, head=12 if k % 2 else 0); f += 3; k += 1
    c.talk(f0, f1, 0.14, 2)
def crowd_in_square(face="happy", n=8, ystart=19.5):
    for i, c in enumerate(crowd[:n]):
        x = -6.5 + (i % 4) * 4.2 + (0.9 if i // 4 else 0); y = ystart + (i // 4) * 2.4 + (i % 2) * 0.4
        c.place((x, y, 0.06), 180 + (x * -2)); c.face(face)
def mayor_on_stage(): mayor.place((-1.5, 27.2, 1.4), 0)

# ---------------------------------------------------------------- shots
def s01(N):  # wide sunny street, push past the hero toward the town hall
    hero.place((0, -2, 0.16), 0); shh(hero)
    cam_move(cam, tgt, 1, N, (2, -18, 3.2), (0.8, -9, 2.8), (0, 20, 8), (0, 0, 2.7), 24, 30)
def s02(N):  # hero close, 'hush hush hush'
    hero.place((0, 0, 0.16), 0); hero.pose(1); shh(hero, max(2, N // 4)); hero.talk(N // 4, N - 2, 0.07, 3)
    cam_move(cam, tgt, 1, N, (0.6, -5.2, 2.9), (0.3, -4.2, 2.8), (0, 0, 2.7), (0, 0, 2.75), 38, 42)
def s03(N):  # the square: banner, stage, the golden trophy
    cam_move(cam, tgt, 1, N, (-6, 12, 2.5), (1.5, 20, 3.4), (0, 28, 5.5), (2.5, 27.5, 3.3), 26, 34)
def s04(N):  # people practising shouting in the square
    crowd_in_square("surprised")
    for i, c in enumerate(crowd): shout(c, 1 + i % 3, N)
    cam_move(cam, tgt, 1, N, (-8, 13, 2.6), (6, 13.5, 3.0), (0, 21, 2.6), (0, 21, 2.6), 26, 26); shake(1, N, 0.06)
def s05(N):  # Benny shouts his breakfast order on his porch
    ben.place((12, 8.5, 0.17), 0); shout(ben, 1, N)
    cam_move(cam, tgt, 1, N, (12.8, 4.2, 2.6), (12.5, 5.0, 2.7), (12, 8.5, 2.7), (12, 8.5, 2.8), 34, 40); shake(1, N, 0.05)
def s06(N):  # the baker yells at a loaf of bread
    baker.place((-12, 8.5, 0.17), 0); shout(baker, 1, N); baker.pose(1, armR=-80, armL=-150, armLs=25, head=-15)
    cam_move(cam, tgt, 1, N, (-10.5, 4.5, 3.0), (-11.0, 5.2, 3.2), (-12, 8.5, 2.9), (-12, 8.5, 3.0), 32, 36)
def s07(N):  # grandma shouts at a TV that is off
    gran.place((1100, 1.5, 0), 10); shout(gran, 1, N); gran.pose(1, armR=-110, armL=-20, head=5)
    cam_move(cam, tgt, 1, N, (1097.8, -5.6, 3.4), (1098.2, -4.8, 3.3), (1100, 1.0, 2.9), (1100, 1.2, 2.9), 26, 30)
def s08(N):  # 5 AM: dark room, alarm clock, hero gets out of bed
    bg.inputs["Strength"].default_value = 0.25; sun.data.energy = 0.3
    hero.place((297, 0.5, 0), -20, 1); hero.place((299.5, -0.5, 0), -60, N); tiptoe(hero, 1, N, 10); hero.face("determined", 1)
    cam_move(cam, tgt, 1, N, (300.5, -5.5, 2.4), (301.5, -5.0, 2.6), (298.5, 3.5, 1.9), (299.5, 0, 2.2), 30, 30)
def s09(N):  # tiptoe across the creaky floor, back and forth (camera tracks him)
    bg.inputs["Strength"].default_value = 0.35; sun.data.energy = 0.5
    h = N // 2
    hero.place((297, -2, 0), -90, 1); hero.place((303, -2, 0), -90, h); hero.place((303, -2, 0), 90, h + 1); hero.place((297.5, -2, 0), 90, N)
    tiptoe(hero, 1, N, 8); hero.face("determined", 1)
    cam_move(cam, tgt, 1, h, (297.5, -8.0, 1.3), (302.0, -8.0, 1.5), (297, -2, 1.2), (303, -2, 1.5), 26, 26)
    cam_move(cam, tgt, h + 1, N, (302.5, -7.6, 1.5), (298.5, -7.6, 1.3), (303, -2, 1.5), (297.5, -2, 1.2), 26, 26)
def s10(N):  # whisper the cat to sleep
    cat.root.location = (301, -1.0, 0); cat.root.rotation_euler = (0, 0, math.radians(200)); cat.root.keyframe_insert("location", frame=1)
    cat.root.location = (301, -1.0, -0.3); cat.root.keyframe_insert("location", frame=N)
    cat.head.rotation_euler = (0, 0, 0); cat.head.keyframe_insert("rotation_euler", frame=N // 2); cat.head.rotation_euler = (math.radians(35), 0, 0); cat.head.keyframe_insert("rotation_euler", frame=N)
    hero.place((302.6, -2.4, 0), 50); hero.pose(lean=25, head=20, armR=-40); hero.face("happy"); hero.talk(1, N // 2, 0.06, 3)
    cam_move(cam, tgt, 1, N, (298.0, -6.6, 2.2), (298.6, -5.8, 2.0), (302.0, -1.6, 1.4), (302.0, -1.6, 1.3), 26, 30)
def s11(N):  # then the dog, then the alarm clock
    a = N // 2
    dog.root.location = (299, -1.5, 0); dog.root.rotation_euler = (0, 0, math.radians(160)); dog.root.keyframe_insert("location", frame=1)
    dog.root.location = (299, -1.5, -0.45); dog.root.keyframe_insert("location", frame=a)
    hero.place((300.5, -3.6, 0), 40); hero.pose(lean=20, head=15, armR=-40); hero.face("happy")
    cam_move(cam, tgt, 1, a, (296.5, -5.4, 2.0), (297.0, -5.0, 1.8), (299, -1.5, 1.0), (299, -1.5, 1.0), 32, 34)
    ac = sc.objects["alarmface"].data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    ac.default_value = 3; ac.keyframe_insert("default_value", frame=a + 3); ac.default_value = 0.05; ac.keyframe_insert("default_value", frame=N - 2)
    cam_move(cam, tgt, a + 1, N, (299.6, 2.4, 2.3), (299.7, 2.9, 2.2), (299.6, 4.9, 1.95), (299.6, 4.9, 1.95), 40, 46)
def s12(N):  # past his sister's door so quietly she thinks he moved out
    hero.place((1296, -1.5, 0), -90, 1); hero.place((1304, -1.5, 0), -90, N); tiptoe(hero, 1, N, 8); hero.face("determined", 1)
    sis.place((1300, 4.8, 0), 0); sis.face("neutral"); sis.pose(1, headyaw=-30); sis.pose(N, headyaw=30, armR=-60, armRs=10)
    cam_move(cam, tgt, 1, N, (1300.5, -8.5, 2.6), (1300.0, -7.8, 2.8), (1300, 1.5, 2.2), (1300.5, 1.5, 2.3), 26, 28)
def s13(N):  # the whole town laughs at Whisper Boy
    hero.place((0, 15.2, 0.06), 180); hero.face("neutral")
    for i, c in enumerate(crowd):
        x = -7 + i * 2; c.place((x, 19.0 + (i % 2) * 1.2, 0.06), -15 * (x / 7)); laugh(c, 1, N, i)
    ben.place((2.5, 17.6, 0.06), 20); laugh(ben, 1, N, 5); ben.pose(N // 2, armR=-90, armRs=-10, lean=-6)
    cam_move(cam, tgt, 1, N, (-1, 11.0, 3.4), (1.5, 11.6, 3.1), (0, 19, 2.6), (0.5, 18.5, 2.4), 24, 28)
def s14(N):  # Benny close: 'Nobody ever won a trophy for being quiet!'
    ben.place((0, 18, 0.06), 180); ben.face("happy"); ben.talk(1, N - 2, 0.16, 2); ben.pose(1, armR=-90, lean=-5); ben.pose(N, armR=-95, armL=-30, lean=-10)
    cam_move(cam, tgt, 1, N, (0.4, 22.6, 2.9), (0.2, 21.8, 2.85), (0, 18, 2.75), (0, 18, 2.8), 36, 40)
def s15(N):  # festival day: wide square, crowd, bunting
    crowd_in_square(); hero.place((5.5, 18.5, 0.06), 185); ben.place((-3.0, 18.3, 0.06), 175)
    for i, c in enumerate(crowd): c.walk(1 + i % 4, N, 12)
    cam_move(cam, tgt, 1, N, (-10, 6, 8), (-4, 9, 5.5), (0, 26, 3), (0, 25, 3.5), 22, 24)
def s16(N):  # the Mayor climbs onto the stage with his megaphone
    crowd_in_square(); megaphone(mayor)
    mayor.place((0, 23.6, 0.06), 0, 1); mayor.place((0, 25.0, 0.6), 90, N // 2); mayor.place((-1.5, 27.2, 1.4), 0, N); mayor.walk(1, N)
    mayor.face("happy", 1)
    cam_move(cam, tgt, 1, N, (5.0, 15.0, 5.0), (3.0, 17.0, 5.4), (0, 24.5, 2.5), (-1.5, 27.2, 4.0), 26, 30)
def s17(N):  # 'Ready... set... SHOUT!'
    mayor_on_stage(); megaphone(mayor); mayor.face("happy"); mayor.pose(1, armR=-95, armL=-20)
    mayor.pose(N - 3, armR=-95, armL=-160, armLs=30); shout(mayor, N // 2, N); mayor.pose(N // 2, armR=-95, armL=-160, armLs=30, head=8)
    cam_move(cam, tgt, 1, N, (-1.2, 22.8, 4.5), (-1.3, 23.6, 4.4), (-1.5, 27.2, 4.4), (-1.5, 27.2, 4.4), 34, 42)
def s18(N):  # everyone screams at once, windows rattle
    crowd_in_square("surprised"); hero.place((5.5, 18.5, 0.06), 185); hero.face("neutral"); hero.pose(armL=-150, armR=-150, armLs=-40, armRs=-40)
    for i, c in enumerate(crowd): shout(c, 1 + i % 2, N, 2)
    mayor_on_stage(); megaphone(mayor); shout(mayor, 1, N); mayor.pose(1, armR=-95, armL=-160, armLs=30)
    cam_move(cam, tgt, 1, N, (0, 30.6, 4.6), (0, 30.4, 5.4), (0, 19, 2.4), (0, 19, 2.4), 20, 22); shake(1, N, 0.25)
def s19(N):  # birds fly off the clock tower, the tower shakes
    for i, b in enumerate(birds):
        b.location = (-2.5 + (i % 3) * 2.5, 33.2, 22.6 + (i // 3) * 0.6); b.keyframe_insert("location", frame=1)
        b.location = (-14 + i * 3.5, 26 - i, 30 + (i % 3) * 3); b.keyframe_insert("location", frame=N)
        for f in range(1, N + 1, 2):
            for sd, w in zip((-1, 1), [o for o in b.children if "birdw" in o.name]):
                w.rotation_euler = (0, math.radians(40 * sd * (1 if f % 4 == 1 else -1)), 0); w.keyframe_insert("rotation_euler", frame=f)
    cam_move(cam, tgt, 1, N, (3, 14, 4), (2, 15, 5), (0, 34, 20), (0, 33, 23), 30, 30); shake(1, N, 0.3)
def s20(N):  # under the stage, something wakes up
    bg.inputs["Strength"].default_value = 0.1; sun.data.energy = 0
    bear.root.location = (900, 2, -1.6); bear.root.rotation_euler = (0, 0, math.radians(20))
    bear.eyes_open(0.05, 1); bear.eyes_open(0.05, N // 2); bear.eyes_open(1, N // 2 + 3)
    for f in range(1, N + 1, 2):
        crawl_l.data.energy = 140 + (80 if f % 4 == 1 else -60); crawl_l.data.keyframe_insert("energy", frame=f)
    point("bearkey", (898.5, -4.5, 3.2), "#ffb070", 0, 1.0); sc.objects["bearkey"].data.energy = 260
    cam_move(cam, tgt, 1, N, (897.6, -9.2, 2.6), (898.2, -7.9, 3.0), (899.3, -2.6, 4.0), (899.5, -2.8, 4.3), 30, 36); shake(1, N, 0.08)
def s21(N):  # a bear rises behind the stage, huge
    crowd_in_square("shock"); mayor_on_stage(); megaphone(mayor); mayor.face("shock")
    bear.root.location = (1, 31.5, -5.5); bear.root.keyframe_insert("location", frame=1)
    bear.root.location = (1, 31.0, 0.06); bear.root.keyframe_insert("location", frame=max(2, int(N * 0.6)))
    bear.root.rotation_euler = (0, 0, 0)
    cam_move(cam, tgt, 1, N, (-3, 14, 3.0), (-2.5, 15, 3.2), (0.5, 29, 7), (1, 31, 9.5), 22, 22); shake(1, N, 0.12)
def s22(N):  # everyone freezes
    crowd_in_square("frozen"); hero.place((5.5, 18.5, 0.06), 185); hero.face("surprised")
    for c in crowd: c.pose(armL=-40, armR=-40, armLs=30, armRs=30)
    cam_move(cam, tgt, 1, N, (-8, 23.5, 3.2), (-7, 22.5, 3.2), (2, 19.5, 2.5), (2, 19.5, 2.6), 26, 30)
def s23(N):  # ...they scream louder
    crowd_in_square("shock")
    for i, c in enumerate(crowd): shout(c, 1 + i % 2, N, 2)
    bear.root.location = (1, 31.0, 0.06); bear.eyes_open(1)
    cam_move(cam, tgt, 1, N, (3, 13.5, 2.8), (2, 14.5, 3.0), (0.5, 26, 4.5), (1, 28, 6.0), 22, 24); shake(1, N, 0.2)
def s24(N):  # the bear roars at the Mayor
    mayor_on_stage(); mayor.face("shock"); megaphone(mayor); mayor.pose(1, armR=-95, lean=-10)
    bear.root.location = (1, 31.0, 0.06); bear.root.rotation_euler = (0, 0, math.radians(-15))
    bear.neck.rotation_euler = (0, 0, 0); bear.neck.keyframe_insert("rotation_euler", frame=1)
    bear.neck.rotation_euler = (math.radians(15), 0, 0); bear.neck.keyframe_insert("rotation_euler", frame=N // 3)
    bear.roar(0, 1); bear.roar(1, N // 3); bear.roar(1, N - 2)
    cam_move(cam, tgt, 1, N, (-6, 22.5, 5.5), (-5.5, 23.5, 6.0), (0, 29, 6.5), (0, 29.5, 7.2), 24, 28); shake(N // 3, N, 0.2)
def s25(N):  # the Mayor drops his megaphone
    mayor_on_stage(); mayor.face("shock"); mayor.pose(1, armR=-95); mayor.pose(N // 3, armR=-20, armL=-160, armLs=40, armRs=40, lean=-15)
    megaphone(mayor); mega.parent = None; mega.location = (-0.8, 26.6, 4.2); mega.keyframe_insert("location", frame=N // 3)
    mega.location = (-0.3, 25.6, 1.5); mega.rotation_euler = (1.4, 0.3, 0.5); mega.keyframe_insert("location", frame=N - 3); mega.keyframe_insert("rotation_euler", frame=N - 3)
    cam_move(cam, tgt, 1, N, (-3.5, 22.2, 2.2), (-3.0, 22.6, 2.0), (-1.5, 27, 4), (-0.8, 25.8, 2.0), 28, 30)
def s26(N):  # hero: 'I've been training for this my whole life'
    crowd_in_square("frozen"); hero.place((0.5, 23.3, 0.06), 180); hero.face("determined")
    hero.pose(1, armL=-10, armR=-10); hero.pose(N, armL=-20, armR=-20, head=-5)
    cam_move(cam, tgt, 1, N, (0.9, 27.6, 3.4), (0.7, 26.9, 3.3), (0.5, 23.3, 2.7), (0.5, 23.3, 2.75), 32, 38)
def s27(N):  # tiptoe across the stage, not one creak (low angle)
    hero.place((-4.5, 25.8, 1.4), -90, 1); hero.place((0.5, 26.3, 1.4), -90, N); tiptoe(hero, 1, N, 8); hero.face("determined", 1)
    bear.root.location = (1, 31.0, 0.06); bear.roar(0.4)
    cam_move(cam, tgt, 1, N, (-3, 21.8, 1.7), (-0.5, 22.2, 1.8), (-3, 26, 2.2), (0.5, 27.5, 3.5), 24, 26)
def s28(N):  # hero whispers to the bear like to his cat
    hero.place((0.5, 27.0, 1.4), 180); shh(hero); hero.talk(1, N - 2, 0.06, 3)
    bear.root.location = (1, 31.0, 0.06); bear.neck.rotation_euler = (math.radians(25), 0, 0); bear.roar(0.2)
    cam_move(cam, tgt, 1, N, (-4.5, 24.4, 4.0), (-4.0, 25.2, 4.2), (0.8, 28.5, 4.5), (0.8, 29, 5.0), 26, 30)
def s29(N):  # eyes get heavy, yawn
    bear.root.location = (1, 31.0, 0.06); bear.neck.rotation_euler = (math.radians(25), 0, 0)
    bear.eyes_open(1, 1); bear.eyes_open(0.4, N // 3); bear.eyes_open(0.55, N // 2); bear.eyes_open(0.15, N - 2)
    bear.roar(0, N // 2); bear.roar(1.3, int(N * 0.75)); bear.roar(0, N)
    cam_move(cam, tgt, 1, N, (0.4, 19.0, 6.6), (0.6, 21.0, 6.5), (1, 28.4, 6.6), (1, 28.4, 6.6), 40, 46)
def s30(N):  # it curls up and falls asleep on the trophy
    hero.place((-2.5, 25.8, 1.4), 160); hero.face("happy")
    bear.root.location = (1, 31.0, 0.06); bear.root.keyframe_insert("location", frame=1); bear.root.rotation_euler = (0, 0, 0); bear.root.keyframe_insert("rotation_euler", frame=1)
    bear.root.location = (2.5, 28.0, -0.9); bear.root.rotation_euler = (0, math.radians(-12), math.radians(70)); bear.root.keyframe_insert("location", frame=int(N * 0.6)); bear.root.keyframe_insert("rotation_euler", frame=int(N * 0.6))
    bear.eyes_open(0.15, 1); bear.eyes_open(0.05, N)
    cam_move(cam, tgt, 1, N, (-5, 19.5, 4.5), (-4, 20.5, 4.0), (1.5, 28, 3), (2.5, 27.8, 2.4), 26, 30)
def s31(N):  # for the first time in a hundred years, silence (slow pull back)
    crowd_in_square("surprised"); mayor.place((-4.5, 26.0, 1.4), -10); mayor.face("surprised"); hero.place((-2.5, 25.8, 1.4), 180); hero.face("happy")
    bear.root.location = (2.5, 28.0, -0.9); bear.root.rotation_euler = (0, math.radians(-12), math.radians(70)); bear.eyes_open(0.05)
    cam_move(cam, tgt, 1, N, (1, 12, 5), (3, 2, 12), (0, 24, 2.5), (0, 26, 4), 26, 24)
def s32(N):  # the Mayor hands the trophy to the hero (after the bear moved)
    mayor.place((-2, 27.0, 1.4), 90); mayor.face("happy"); hero.place((1.0, 27.0, 1.4), -90); hero.face("happy")
    trophy.location = (-0.9, 26.6, 2.3); trophy.scale = (0.6, 0.6, 0.6); trophy.keyframe_insert("location", frame=1)
    trophy.location = (0.1, 26.6, 2.3); trophy.keyframe_insert("location", frame=N // 2)
    mayor.pose(1, armR=-80); mayor.pose(N // 2, armR=-90); hero.pose(N // 2, armL=-150, armR=-150, armLs=20, armRs=20)
    bear.root.location = (7, 31, 0.06); bear.root.rotation_euler = (0, 0, math.radians(120)); bear.walk = None
    cam_move(cam, tgt, 1, N, (-0.5, 21.0, 3.6), (-0.4, 22.0, 3.5), (-0.5, 27, 3.3), (0, 27, 3.4), 30, 34)
def s33(N):  # next year: the banner says BIG WHISPER
    t_shout.hide_render = True; t_whisp.hide_render = False
    cam_move(cam, tgt, 1, N, (0, 16, 3), (0, 19, 4.5), (0, 30, 6.8), (0, 30, 6.8), 30, 40)
def s34(N):  # Benny asks, hero answers
    ben.place((-1.2, 3.0, 0.16), -60); ben.face("surprised"); ben.talk(1, N // 3, 0.12, 2)
    hero.place((1.2, 2.8, 0.16), 60); hero.face("happy"); hero.talk(N // 3, N - 2, 0.08, 3)
    trophy.location = (0, -0.35, -1.2); trophy.parent = hero.arms[0]; trophy.scale = (0.4, 0.4, 0.4); hero.pose(armL=-60)
    cam_move(cam, tgt, 1, N, (3.6, -4.0, 3.0), (3.0, -3.4, 2.9), (0.6, 2.9, 2.6), (0.9, 2.9, 2.7), 30, 34)
def s35(N):  # hush, hush, hush (finger to lips, wink to camera)
    hero.place((0, 0, 0.16), 0); hero.pose(1); shh(hero, 4); hero.talk(4, N - 2, 0.06, 3)
    cam_move(cam, tgt, 1, N, (0.2, -4.4, 2.8), (0.1, -3.6, 2.8), (0, 0, 2.75), (0, 0, 2.8), 40, 46)
def s36(N):  # end: the town at sunset, pull back over the square
    bg.inputs["Color"].default_value = (*lib.srgb("#ffb37a"), 1); sun.data.color = lib.srgb("#ffb070"); sun.data.energy = 3
    sun.rotation_euler = (math.radians(78), 0, math.radians(215))
    for o in OBJ:
        if o.type == "LIGHT" and o.name.startswith("lamp"): o.data.energy = 900
    crowd_in_square("happy"); hero.place((0, 21.5, 0.06), 0); hero.face("happy")
    cam_move(cam, tgt, 1, N, (0, 10, 4.5), (0, -6, 14), (0, 24, 4), (0, 30, 10), 26, 24)

SHOTS = [("s01", 0.0, s01), ("s02", 2.3, s02), ("s03", L[1], s03), ("s04", L[1] + 2.6, s04), ("s05", L[2], s05), ("s06", L[3], s06),
         ("s07", L[4], s07), ("s08", L[5], s08), ("s09", L[5] + 3.0, s09), ("s10", L[6], s10), ("s11", L[6] + 1.6, s11), ("s12", L[7], s12),
         ("s13", L[8], s13), ("s14", L[9], s14), ("s15", L[10], s15), ("s16", L[10] + 2.6, s16), ("s17", L[11], s17), ("s18", L[12], s18),
         ("s19", L[12] + 2.0, s19), ("s20", L[13], s20), ("s21", L[14], s21), ("s22", L[15], s22), ("s23", L[15] + 1.6, s23),
         ("s24", L[16], s24), ("s25", L[16] + 2.6, s25), ("s26", L[17], s26), ("s27", L[18], s27), ("s28", L[19], s28),
         ("s29", L[20], s29), ("s30", L[20] + 2.5, s30), ("s31", L[21], s31), ("s32", L[22], s32), ("s33", L[23], s33),
         ("s34", L[24], s34), ("s35", L[24] + 2.5, s35), ("s36", L[25], s36)]
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
        sc.frame_set(max(1, int(N * 0.6))); sc.render.filepath = f"{W}/stills/{sid}.png"; bpy.ops.render.render(write_still=True)
        continue
    sc.frame_start, sc.frame_end = 1, N; sc.render.filepath = f"{d}/"
    t = time.time(); bpy.ops.render.render(animation=True)
    open(f"{d}/done", "w").write(str(N)); print(sid, N, "frames", round(time.time() - t), "s", flush=True)
