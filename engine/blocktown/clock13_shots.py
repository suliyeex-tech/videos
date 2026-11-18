"""In This Town #1: the clock that stops at midnight. Renders every shot to /home/claude/work/<slug>/shots/<sid>/####.png
python3 clock13_shots.py [sid ...]   (no args = all shots, resumable: finished shots are skipped)"""
import sys, os, json, math, random, time, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move

SLUG = "2026-11-18-in-this-town-clock-13"; FPS = 12
W = f"/home/claude/work/{SLUG}"
vo = json.load(open(f"{W}/vo.json")); L = [l["start"] for l in vo["lines"]]; END = vo["total"] + 0.6

sc, cam, tgt = lib.setup(res=(432, 768) if "--still" not in sys.argv else (216, 384), samples=8 if "--still" not in sys.argv else 4, fps=FPS)
town = lib.build_town(); lib.build_bedroom(300); lib.build_stairs(500); cr = lib.build_clockroom(700)
leo = lib.Char("leo", top="#2f63d6", pants="#c9b48a", hair="#7a4524", hood=True, extra="#2550ad")
mx = lib.Char("max", top="#2f9a4a", pants="#3b3b55", hair="#e0702e", hair_style="flat", hood=True, extra="#256f37")
kid = lib.Char("zoe", skin="#8d5a3b", top="#e2a23a", pants="#5a3d7a", hair="#1d1310", hair_style="flat")
mayor = lib.Char("mayor", skin="#f0c29a", top="#23253b", pants="#23253b", hair="#5b4636", hair_style="flat", kid=False)
mayor.mayor_kit()
dog = lib.Dog()
# props
board = empty("board"); cube("deck", (0, 0, 0.25), (1.0, 2.6, 0.12), mat("deck", "#d23b3b", 0.5), 0.05, board)
for x, y in ((-0.35, -0.9), (0.35, -0.9), (-0.35, 0.9), (0.35, 0.9)):
    cyl(f"wheel{x}{y}", (x, y, 0.1), 0.13, 0.12, mat("wheel", "#f2e9c0"), (0, math.pi / 2, 0), board, 10)
flash = empty("flash", (0, -0.3, -1.05), leo.arms[1])
cyl("flashbody", (0, 0, 0), 0.12, 0.7, mat("flashb", "#2a2a2a", 0.3, metal=0.5), (math.pi / 2, 0, 0), flash, 10)
cyl("flashlens", (0, -0.36, 0), 0.13, 0.04, mat("lens", "#fff6d0", 0.2, 12), (math.pi / 2, 0, 0), flash, 10)
beam = spot("beam", (0, -0.4, 0), "#fff1c8", 0, 30, flash, (math.radians(90), 0, 0))
phone = empty("phone", (0.0, -0.35, -1.0), leo.arms[0])
cube("phonebody", (0, 0, 0), (0.5, 0.06, 0.8), mat("phone", "#111111", 0.3), 0.04, phone)
cube("phonescreen", (0, -0.035, 0), (0.42, 0.01, 0.7), mat("screen", "#9fd8ff", 0.2, 8), 0, phone)
phlight = point("phonelight", (0, -0.6, 0.2), "#9fd8ff", 0, 0.2, phone)
mphone = empty("mphone", (0.0, -0.35, -1.0), mx.arms[1])
cube("mphonebody", (0, 0, 0), (0.5, 0.06, 0.8), mat("phone", "#111111", 0.3), 0.04, mphone)
cube("mphonescreen", (0, -0.035, 0), (0.42, 0.01, 0.7), mat("screen", "#9fd8ff", 0.2, 8), 0, mphone)
can = empty("trashcan", (9.0, -4.8, 0.17))
cyl("canbody", (0, 0, 0.9), 0.7, 1.8, mat("can", "#6d7a86", 0.4, metal=0.6), parent=can, verts=16)
lid = cyl("canlid", (0, 0, 1.85), 0.78, 0.12, mat("can", "#6d7a86", 0.4, metal=0.6), parent=can, verts=16)
rnd = random.Random(7)
leaves = [cube(f"leafF{i}", (-8 + rnd.uniform(-3, 3), 6.5 + rnd.uniform(-2, 2), rnd.uniform(1.5, 5)), (0.35, 0.05, 0.25),
               mat("leafO", rnd.choice(["#e0702e", "#d9a43a", "#9c3b2a"]), 0.7), 0.0, None,
               (rnd.uniform(0, 3), rnd.uniform(0, 3), rnd.uniform(0, 3))) for i in range(26)]
freeze = point("freeze", (0, -2, 6), "#7fe9ff", 0, 3.0)
# new mayor for the ending: Leo's grandma (sash, white bun)
gran = lib.Char("gran", skin="#e9b892", top="#8b4fb0", pants="#8b4fb0", hair="#eeeeee", hair_style="flat", kid=False)
cube("granbun", (0, 0.35, 1.1), (0.5, 0.5, 0.4), gran.mhair, 0.15, gran.neck)
cube("gransash", (0, -0.33, 1.95), (0.32, 0.05, 1.6), mat("sash", "#c8282f", 0.5), 0.02, gran.body, (0, math.radians(35), 0))

fill = point("camfill", (0.6, 0.4, 0.2), "#ffe6cc", 260, 1.0, cam)
for lf in leaves: lf.hide_render = True
for o in flash.children_recursive: o.hide_render = True
for o in phone.children_recursive: o.hide_render = True
# ---- save the base state so every shot starts clean
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
WORLD = (tuple(sc.world.node_tree.nodes["Background"].inputs["Color"].default_value), sc.world.node_tree.nodes["Background"].inputs["Strength"].default_value)
OFF = (0, 0, -500)  # parking spot for unused characters

def reset():
    for o in OBJ:
        o.animation_data_clear()
        if o.type == "CAMERA" and o.data.animation_data: o.data.animation_data_clear()
        l, r, s, h = BASE[o.name]; o.location, o.rotation_euler, o.scale, o.hide_render = l, r, s, h
        if o.type == "LIGHT":
            o.data.energy = LIGHTS[o.name]
            if o.data.animation_data: o.data.animation_data_clear()
    bg = sc.world.node_tree.nodes["Background"]; bg.inputs["Color"].default_value = WORLD[0]; bg.inputs["Strength"].default_value = WORLD[1]
    for c in (leo, mx, kid, mayor, gran):
        c.place(OFF); c.pose(); c.face("neutral")
    mayor.recolor_hair("#5b4636"); dog.root.location = OFF; board.location = OFF
    cam.data.lens = 28

def show(objs, on=True):
    for o in objs: o.hide_render = not on
def torch(on=True):
    show(flash.children_recursive, on)

def shake(f0, f1, amt=0.15):
    for f in range(f0, f1 + 1):
        cam.delta_location = (random.uniform(-amt, amt), random.uniform(-amt, amt), random.uniform(-amt, amt)); cam.keyframe_insert("delta_location", frame=f)

def end_shake(f):
    cam.delta_location = (0, 0, 0); cam.keyframe_insert("delta_location", frame=f)

def hands(f0, f1, a_min0, a_min1, a_h0, a_h1):
    for f, am, ah in ((f0, a_min0, a_h0), (f1, a_min1, a_h1)):
        town["minhand"].rotation_euler = (0, math.radians(am), 0); town["minhand"].keyframe_insert("rotation_euler", frame=f)
        town["hourhand"].rotation_euler = (0, math.radians(ah), 0); town["hourhand"].keyframe_insert("rotation_euler", frame=f)

def linear_all():
    for o in OBJ + [cam]:
        ad = o.animation_data
        if ad and ad.action:
            try:
                for fc in ad.action.fcurves:
                    for k in fc.keyframe_points: k.interpolation = "BEZIER"
            except Exception: pass

# ---------------------------------------------------------------- shots: (id, start_s, fn(N))
def s01(N):  # wide street, push to the clock at midnight
    hands(1, N, 0, 0, 0, 0)
    cam_move(cam, tgt, 1, N, (0, -22, 2.2), (0, -12, 3.5), (0, 30, 12), (0, 32, 15))
def s02(N):  # empty street, slide sideways
    cam_move(cam, tgt, 1, N, (-18, -3, 1.2), (-10, -3, 1.4), (-4, 8, 3), (4, 8, 3))
def s03(N):  # clock face close
    hands(1, N, 0, 0, 0, 0)
    cam_move(cam, tgt, 1, N, (0, 14, 16), (0, 22, 17.2), (0, 33, 17.5), (0, 33, 17.5), 40, 50)
def s04(N):  # Leo hiding under the blanket, peeking
    in_bed(); leo.face("scared"); leo.pose(1, headyaw=-25); leo.pose(N, headyaw=25)
    cam_move(cam, tgt, 1, N, (299.5, 0.5, 4.6), (298.6, 1.6, 4.0), (296.5, 3.9, 1.9), (296.5, 3.9, 1.9), 30, 38)
def in_bed():
    leo.root.location = (296.5, 0.9, 1.45); leo.root.rotation_euler = (math.radians(-90), 0, 0)
    b = sc.objects["blanket"]; b.location = (296.5, 1.4, 1.75); b.scale = (1.0, 0.9, 1.0)
def s05(N):  # a frozen kid mid-run on the street, cold light, slow orbit
    kid.place((-20, 1.5, 0.16), -30); kid.pose(armL=60, armR=-60, legL=-45, legR=40, lean=12); kid.face("frozen")
    freeze.location = (-20, -2, 5); freeze.data.energy = 900
    cam_move(cam, tgt, 1, N, (-25, -5, 2.4), (-15.5, -5.5, 2.6), (-20, 1.5, 2.4), (-20, 1.5, 2.6))
def s06(N):  # Leo intro close-up in his room
    leo.place((302, 0, 0), 0); leo.pose(armR=-20, armRs=10); leo.face("happy"); leo.talk(1, N - 2)
    cam_move(cam, tgt, 1, N, (302.6, -5.8, 3.0), (302.4, -4.6, 3.0), (302, 0, 2.9), (302, 0, 2.9), 35, 38)
def s07(N):  # over-shoulder at the window: the ticking stops
    leo.place((304.6, 1.5, 0), 90); leo.pose(armL=-10, head=-5); leo.face("surprised")
    cam_move(cam, tgt, 1, N, (300.2, 0.0, 4.2), (301.4, 0.4, 3.9), (306.8, 1.5, 4.0), (306.8, 1.5, 4.0))
def s08(N):  # phone buzzes
    leo.place((302, 0, 0), 0); leo.pose(armL=-70, head=8); leo.face("surprised")
    phlight.data.energy = 60; show(phone.children_recursive)
    for f in range(1, N + 1, 2):
        phone.location = (0.03 * (1 if f % 4 == 1 else -1), -0.35, -1.0); phone.keyframe_insert("location", frame=f)
    cam_move(cam, tgt, 1, N, (302.5, -5.2, 3.4), (302.3, -4.3, 3.3), (301.9, 0, 2.6), (301.9, 0, 2.7), 32, 36)
def s09(N):  # Max on the street, scared, phone at ear
    mx.place((3, -1, 0.16), -15); mx.pose(armR=-150, armRs=-15, armL=20, head=5); mx.face("scared"); mx.talk(1, N - 3)
    freeze.location = (3, -4, 5); freeze.data.energy = 400
    cam_move(cam, tgt, 1, N, (4.5, -7, 3.0), (4.0, -5.8, 3.0), (3, -1, 2.9), (3, -1, 2.9), 35, 40)
def s10(N):  # Leo shock
    leo.place((302, 0, 0), 0); leo.pose(armL=-70, head=-5); leo.face("shock"); show(phone.children_recursive)
    cam_move(cam, tgt, 1, N, (302.3, -4.0, 3.0), (302.2, -3.4, 3.0), (302, 0, 2.95), (302, 0, 2.95), 38, 42)
def s11(N):  # Leo runs out of his house with the flashlight
    beam.data.energy = 900; torch()
    leo.place((12, 9.0, 0.17), 0, 1); leo.place((10, 0.5, 0.17), -15, N); leo.run(1, N); leo.face("determined", 1)
    cam_move(cam, tgt, 1, N, (14, -4, 2.2), (9, -5, 2.4), (12, 8, 2), (10, 0, 2))
def s12(N):  # frozen dog mid-jump over a fence + floating leaves
    dog.root.location = (-12, 7.6, 1.6); dog.root.rotation_euler = (math.radians(-20), 0, 0); dog.jump_pose(); show(leaves)
    freeze.location = (-10, 2, 5); freeze.data.energy = 900
    fill.data.energy = 0
    cam_move(cam, tgt, 1, N, (-5.0, 3.8, 3.0), (-5.4, 6.4, 3.2), (-12, 7.2, 2.0), (-12, 7.8, 2.3), 30, 32)
def s13(N):  # Max frozen on his skateboard, Leo walks in with the beam
    board.location = (2, 0.5, 0.05); board.rotation_euler = (math.radians(8), 0, math.radians(70))
    mx.place((2, 0.5, 0.42), 70); mx.pose(armL=40, armLs=60, armR=-30, armRs=60, legL=15, legR=-15, lean=10, head=-5); mx.face("frozen")
    freeze.location = (2, -3, 5); freeze.data.energy = 700; beam.data.energy = 900; torch()
    leo.place((9, -2.5, 0.17), 115, 1); leo.place((6.0, -1.6, 0.17), 115, N); leo.walk(1, N); leo.face("scared", 1)
    cam_move(cam, tgt, 1, N, (-1.5, -8.5, 2.6), (0.5, -7.6, 2.4), (3.5, 0.0, 2.2), (4.0, -0.3, 2.2))
def s14(N):  # Leo turns to the sound
    leo.place((6, -1.6, 0.17), 115); leo.face("scared"); beam.data.energy = 600; torch()
    leo.pose(1, head=0, headyaw=0); leo.pose(N, head=12, headyaw=70)
    town["towerwin"].data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 15
    cam_move(cam, tgt, 1, N, (9.6, 0.6, 3.1), (9.2, 0.4, 3.1), (6, -1.6, 3.0), (6, -1.6, 3.1), 36, 40)
def s15(N):  # low angle up the tower, light at the top
    town["towerwin"].data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 15
    sc.objects["towerglow"].data.energy = 1500
    cam_move(cam, tgt, 1, N, (2, 8, 5.5), (1.6, 9.5, 6.0), (0, 34, 15), (0, 34, 21), 30, 32)
def s16(N):  # Leo looks right at the clock face (from behind, the face huge in frame)
    beam.data.energy = 500; torch()
    leo.place((0, 24, 0.17), 180); leo.pose(head=30, armR=20); leo.face("determined")
    hands(1, N, 0, 0, 0, 0)
    cam_move(cam, tgt, 1, N, (1.5, 19.5, 1.6), (0.8, 21, 1.8), (0, 33, 15), (0, 33, 16))
def s17(N):  # the hands spin backwards
    sc.objects["towerglow"].data.energy = 1500
    hands(1, N, 0, -720, 0, -60)
    cam_move(cam, tgt, 1, N, (0, 24, 17.5), (0, 25.5, 17.5), (0, 33, 17.5), (0, 33, 17.5), 45, 50)
def s18(N):  # running up the spiral stairs
    beam.data.energy = 700; torch()
    steps = 6
    for k in range(steps + 1):
        f = 1 + (N - 1) * k / steps; i = 10 + k * 3; a = i * math.radians(18)
        leo.place((500 + 3.6 * math.cos(a), 3.6 * math.sin(a), 0.5 + i * 0.45), math.degrees(a) + 180, f)
        ca = a - math.radians(70)
        cam.location = (500 + 4.8 * math.cos(ca), 4.8 * math.sin(ca), 2.6 + i * 0.45); cam.keyframe_insert("location", frame=f)
        tgt.location = (500 + 3.6 * math.cos(a), 3.6 * math.sin(a), 2.2 + i * 0.45); tgt.keyframe_insert("location", frame=f)
    leo.run(1, N); leo.face("determined", 1)
def gears_turn(N, speed=1.0):
    for g, d in zip(cr["gears"], (1, -1.35, 1.8, -1.6)):
        g.rotation_euler = (0, 0, 0); g.keyframe_insert("rotation_euler", frame=1)
        g.rotation_euler = (0, math.radians(d * 4 * N * speed), 0); g.keyframe_insert("rotation_euler", frame=N)
        for fc in (g.animation_data.action.fcurves if hasattr(g.animation_data.action, "fcurves") else []):
            for k in fc.keyframe_points: k.interpolation = "LINEAR"
def key_turn(N, deg=180):
    k = cr["key"]; k.rotation_euler = (0, 0, 0); k.keyframe_insert("rotation_euler", frame=1)
    k.rotation_euler = (math.radians(deg), 0, 0); k.keyframe_insert("rotation_euler", frame=N)
def s19(N):  # clock room reveal: gears + someone turning the key (from behind)
    gears_turn(N); key_turn(N)
    mayor.place((708.6, 0.6, 0), 90); mayor.pose(armL=80, armR=80)
    leo.place((698.5, -7.0, 0), 160); leo.face("surprised")
    cam_move(cam, tgt, 1, N, (695.5, -14, 4.5), (696.5, -12, 4.8), (703, 2, 5), (704, 2, 5.2), 24, 26)
def s20(N):  # the Mayor turns around
    gears_turn(N)
    mayor.place((709.5, -1.5, 0), 90, 1); mayor.place((709.5, -1.5, 0), -25, min(N, 6)); mayor.face("evil")
    cam_move(cam, tgt, 1, N, (707.2, -6.3, 4.3), (707.4, -5.9, 4.3), (709.5, -1.5, 3.9), (709.5, -1.5, 3.9), 40, 44)
def s21(N):  # Mayor speech
    gears_turn(N)
    mayor.place((709.5, -1.5, 0), -30); mayor.face("evil"); mayor.talk(1, N - 3, 0.1, 3)
    mayor.pose(1, armR=-30, armL=-30); mayor.pose(N // 2, armR=-100, armRs=30, armL=-20); mayor.pose(N, armR=-120, armRs=40, armL=-60, armLs=30)
    cam_move(cam, tgt, 1, N, (705.8, -8.0, 3.2), (706.4, -7.1, 3.4), (709.5, -1.5, 4.0), (709.5, -1.5, 4.2), 30, 34)
def s22(N):  # he turns the key again
    gears_turn(N, 1.6); key_turn(N, 220)
    mayor.place((708.6, 0.6, 0), 90); mayor.pose(1, armL=80, armR=80); mayor.pose(N, armL=95, armR=95, lean=8); mayor.face("evil")
    cam_move(cam, tgt, 1, N, (704.5, -6.5, 5.2), (704.0, -6.8, 4.8), (707.5, 0.8, 4.0), (707.5, 0.8, 4.0), 30, 30)
def s23(N):  # the town sinks deeper into the freeze (wide from above, blue rising)
    freeze.location = (0, 0, 12); freeze.data.energy = 0; freeze.keyframe_insert(data_path="location", frame=1)
    freeze.data.energy = 200; freeze.data.keyframe_insert("energy", frame=1); freeze.data.energy = 9000; freeze.data.keyframe_insert("energy", frame=N)
    board.location = (2, 0.5, 0.05); board.rotation_euler = (math.radians(8), 0, math.radians(70))
    mx.place((2, 0.5, 0.42), 70); mx.pose(armL=40, armLs=60, armR=-30, armRs=60, legL=15, legR=-15, lean=10); mx.face("frozen")
    cam_move(cam, tgt, 1, N, (-7, -8, 24), (-5, -7, 20), (2, 3, 0), (2, 2, 0))
def s24(N):  # Leo notices the candle: push in, flame flickers with each gear turn
    gears_turn(N)
    for f in range(1, N + 1, 3):
        s = 1.0 + 0.35 * math.sin(f * 1.3); cr["flame"].scale = (0.22 * s, 0.22 * s, 0.42 * s); cr["flame"].keyframe_insert("scale", frame=f)
    leo.place((698.3, -2.5, 0), -30); leo.face("surprised"); leo.pose(head=-8)
    cam_move(cam, tgt, 1, N, (696.5, -7.5, 4.0), (698.6, -3.8, 4.6), (700, 2, 4.2), (700, 2, 4.4), 30, 40)
def s25(N):  # extreme close-up candle (Oddwick cameo)
    gears_turn(N)
    for f in range(1, N + 1, 2):
        s = 1.0 + 0.3 * math.sin(f * 1.9); cr["flame"].scale = (0.22 * s, 0.22 * s, 0.42 * s); cr["flame"].keyframe_insert("scale", frame=f)
    cam_move(cam, tgt, 1, N, (700, -0.6, 4.4), (700, 0.0, 4.4), (700, 2, 4.3), (700, 2, 4.35), 45, 50)
def s26(N):  # Leo blows it out
    leo.place((700, -0.5, 1.1), 180); leo.pose(lean=14, head=-10); leo.face("surprised")
    leo.mouth.scale = (0.6, 1, 2.6); leo.mouth.keyframe_insert("scale", frame=1)
    out = int(N * 0.65)
    for f in range(1, out, 2):
        s = 1.0 + 0.4 * math.sin(f * 2.1); cr["flame"].scale = (0.22 * s, 0.22 * s, 0.42 * s * (1 - 0.4 * f / out)); cr["flame"].keyframe_insert("scale", frame=f)
    cr["flame"].scale = (0.0, 0.0, 0.0); cr["flame"].keyframe_insert("scale", frame=out + 1)
    fl = cr["flamelight"].data; fl.energy = 220; fl.keyframe_insert("energy", frame=out); fl.energy = 0; fl.keyframe_insert("energy", frame=out + 1)
    cam_move(cam, tgt, 1, N, (703.6, -2.6, 4.5), (703.2, -2.2, 4.5), (700, 0.7, 4.2), (700, 0.7, 4.2), 28, 30)
def s27(N):  # gears screech, the key snaps, camera shakes
    gears_turn(N, 0.3); sc.objects["cr_purple"].data.energy = 2200
    k = cr["key"]; k.location = (705, 1, 4); k.keyframe_insert("location", frame=1)
    k.location = (709, -3, 9); k.rotation_euler = (2, 1, 3); k.keyframe_insert("location", frame=N); k.keyframe_insert("rotation_euler", frame=N)
    mayor.place((708.6, 0.6, 0), 120); mayor.face("shock"); mayor.pose(armL=-40, armLs=40, armR=-40, armRs=40)
    cam_move(cam, tgt, 1, N, (699, -8, 5), (699.5, -7.5, 5), (704, 3, 6), (704, 3, 6), 26, 26); shake(1, N, 0.12)
def s28(N):  # outside: the clock strikes thirteen (tower shakes in camera)
    hands(1, N, 0, 0, 0, 0)
    cam_move(cam, tgt, 1, N, (0, 15, 2.5), (0, 16.5, 3), (0, 33, 17), (0, 33, 18), 30, 32); shake(1, N, 0.2)
def s29(N):  # the town unfreezes: dog lands, leaves fall, Max rolls into the trash can
    a = max(2, N // 3)
    dog.root.location = (-12, 7.6, 1.6); dog.jump_pose(1)
    show(leaves); dog.root.rotation_euler = (math.radians(-20), 0, 0); dog.root.keyframe_insert("rotation_euler", frame=1); dog.root.keyframe_insert("location", frame=1)
    dog.root.location = (-12, 4.5, 0.17); dog.root.rotation_euler = (0, 0, 0); dog.root.keyframe_insert("location", frame=a); dog.root.keyframe_insert("rotation_euler", frame=a)
    dog.jump_pose(a, 0)
    for lf in leaves:
        lf.keyframe_insert("location", frame=1); z = lf.location.z; lf.location.z = 0.2; lf.keyframe_insert("location", frame=N)
    board.location = (2, 0.5, 0.05); board.rotation_euler = (0, 0, math.radians(70)); board.keyframe_insert("location", frame=1)
    mx.place((2, 0.5, 0.42), 70, 1); mx.pose(1, armL=40, armLs=60, armR=-30, armRs=60, legL=15, legR=-15, lean=10); mx.face("surprised", 1)
    board.location = (8.4, -3.8, 0.05); board.keyframe_insert("location", frame=N - 3)
    mx.place((8.4, -3.8, 0.42), 70, N - 4); mx.pose(N - 4, armL=60, armR=60, lean=20)
    mx.root.location = (9.0, -4.6, 0.6); mx.root.rotation_euler = (math.radians(-80), 0, math.radians(70)); mx.root.keyframe_insert("location", frame=N); mx.root.keyframe_insert("rotation_euler", frame=N)
    can.rotation_euler = (0, 0, 0); can.keyframe_insert("rotation_euler", frame=N - 3); can.rotation_euler = (math.radians(-75), 0, 0); can.keyframe_insert("rotation_euler", frame=N)
    cam_move(cam, tgt, 1, a, (-17, 1, 2.2), (-16, 0, 2.2), (-12, 6, 1.8), (-12, 5, 1.5))
    cam_move(cam, tgt, a + 1, N, (1, -11, 3.0), (4, -11.5, 3.2), (4, -1, 1.5), (8.5, -4, 1.2))
def s30(N):  # the Mayor gets old: hair goes white
    mayor.place((709.5, -1.5, 0), -30); mayor.face("shock")
    m = mayor.mhair.node_tree.nodes["Principled BSDF"].inputs["Base Color"]
    m.default_value = (*lib.srgb("#5b4636"), 1); m.keyframe_insert("default_value", frame=1)
    m.default_value = (*lib.srgb("#5b4636"), 1); m.keyframe_insert("default_value", frame=N // 3)
    m.default_value = (*lib.srgb("#f4f4f4"), 1); m.keyframe_insert("default_value", frame=N // 3 + 8)
    mayor.pose(1); mayor.pose(N, lean=18, head=-10, armL=20, armR=20); mayor.face("scared", N)
    cam_move(cam, tgt, 1, N, (707.5, -6.0, 4.2), (707.9, -5.3, 4.2), (709.5, -1.5, 4.1), (709.5, -1.5, 3.8), 38, 42)
def s31(N):  # next morning: daylight, grandma is the new Mayor
    bg = sc.world.node_tree.nodes["Background"]; bg.inputs["Color"].default_value = (*lib.srgb("#8fc8ff"), 1); bg.inputs["Strength"].default_value = 1.6
    sc.objects["moonlight"].data.energy = 5.0
    for o in OBJ:
        if o.type == "LIGHT" and o.name.startswith("lamp"): o.data.energy = 0
    hands(1, N, 0, 30, 0, 2.5)
    gran.place((0, 28.8, 0.0), 0); gran.pose(armR=-150, armRs=25); gran.face("happy")
    leo.place((-2.5, 26.5, 0.17), 20); leo.face("happy"); mx.place((2.5, 26.2, 0.17), -20); mx.face("happy")
    cam_move(cam, tgt, 1, N, (0, 16, 2.4), (0, 19, 3.2), (0, 30, 4.5), (0, 32, 9))
def s32(N):  # tonight: the alarm clock ticks backwards
    in_bed(); leo.face("shock")
    a = sc.objects["alarmface"].data.materials[0].node_tree.nodes["Principled BSDF"]
    a.inputs["Emission Color"].default_value = (*lib.srgb("#b46bff"), 1); a.inputs["Emission Strength"].default_value = 3
    point("alarmglow", (299.6, 4.0, 2.2), "#b46bff", 0, 0.2).data.energy = 120
    cam_move(cam, tgt, 1, N, (298.8, -0.6, 3.6), (299.4, 2.6, 2.3), (297.4, 4.2, 1.9), (299.6, 4.9, 1.95), 30, 42)

SHOTS = [("s01", L[0], s01), ("s02", L[1], s02), ("s03", L[2], s03), ("s04", L[3], s04), ("s05", L[4], s05), ("s06", L[5], s06),
         ("s07", L[6], s07), ("s08", L[7], s08), ("s09", L[8], s09), ("s10", L[9], s10), ("s11", L[10], s11), ("s12", L[11], s12),
         ("s13", L[12], s13), ("s14", L[13], s14), ("s15", L[14], s15), ("s16", L[15], s16), ("s17", L[16], s17), ("s18", L[17], s18),
         ("s19", L[18], s19), ("s20", L[19], s20), ("s21", L[20], s21), ("s22", L[21], s22), ("s23", L[21] + 2.0, s23),
         ("s24", L[22], s24), ("s25", L[23], s25), ("s26", L[24], s26), ("s27", L[25], s27), ("s28", L[25] + 1.7, s28),
         ("s29", L[26], s29), ("s30", L[27], s30), ("s31", L[28], s31), ("s32", L[29], s32)]
SHOTS[0] = ("s01", 0.0, s01)
TIMES = [(sid, t, (SHOTS[i + 1][1] if i + 1 < len(SHOTS) else END), fn) for i, (sid, t, fn) in enumerate(SHOTS)]
json.dump([(sid, t0, t1) for sid, t0, t1, _ in TIMES], open(f"{W}/shots_timing.json", "w"))

only = [a for a in sys.argv[1:] if a.startswith("s")]
preview = "--still" in sys.argv
for sid, t0, t1, fn in TIMES:
    if only and sid not in only: continue
    N = max(2, round((t1 - t0) * FPS)); d = f"{W}/shots/{sid}"
    if not preview and os.path.exists(f"{d}/done"): continue
    os.makedirs(d, exist_ok=True); reset(); fn(N)
    tgt.location = tgt.location  # noop
    if preview:
        sc.frame_set(max(1, N // 2)); sc.render.filepath = f"{W}/stills/{sid}.png"; bpy.ops.render.render(write_still=True)
        continue
    sc.frame_start, sc.frame_end = 1, N; sc.render.filepath = f"{d}/"
    t = time.time(); bpy.ops.render.render(animation=True)
    open(f"{d}/done", "w").write(str(N)); print(sid, N, "frames", round(time.time() - t), "s", flush=True)
