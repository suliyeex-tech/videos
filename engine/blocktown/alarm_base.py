"""Scene, cast, lighting and shot helpers for "In This Town, Nobody Owns an Alarm Clock" (16:9 long-form, 2026-11-21)."""
import sys, os, json, math, random, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, alarm_sets as AS
from lib import cube, sphere, cyl, empty, point, spot, mat, cam_move
from alarm_sets import show

SLUG = "2026-11-21-nobody-owns-an-alarm-clock"; FPS = 12
W = f"/home/claude/work/{SLUG}"
PREV = "--still" in sys.argv
RES = (480, 270) if PREV else (768, 432)
sc, cam, tgt = lib.setup(res=RES, samples=4 if PREV else 6, fps=FPS)
sc.cycles.adaptive_threshold = 0.03
G = AS.build_all(sc)
bg = sc.world.node_tree.nodes["Background"]
sun = sc.objects["moonlight"]; sc.objects["moon"].hide_render = True
LAMPS = [o for o in sc.objects if o.type == "LIGHT" and o.name.startswith("lamp")]
WINLIT = bpy.data.materials.get("winlit")

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
curlers = empty("curlers", (0, 0, 1.1), pick.neck)
for i in range(5): cyl(f"curl{i}", (-0.4 + i * 0.2, -0.1, 0.05), 0.11, 0.5, mat("curler", "#ff8fb0", 0.4), rot=(math.pi / 2, 0, 0), parent=curlers, verts=10)
show(curlers, False)
robe = cube("pk_robe", (0, 0, 1.6), (1.3, 0.7, 2.2), mat("robe", "#ffb0d0", 0.9), 0.1, pick.body); robe.hide_render = True
gus = lib.Char("gus", skin="#efc4a0", top="#8a6a4a", pants="#4a4a5a", hair="#f2f2f2", hair_style="flat", kid=False, **K)
cube("gus_beard", (0, -0.5 * gus.hs, 0.2 * gus.hs), (0.9 * gus.hs, 0.1, 0.4 * gus.hs), mat("gusbeard", "#f2f2f2", 0.8), 0.06, gus.neck)
for sd in (-1, 1):
    cube(f"gus_gl{sd}", (0.22 * sd * gus.hs, -0.56 * gus.hs, 0.6 * gus.hs), (0.36 * gus.hs, 0.03, 0.05), mat("glassfr", "#111111", 0.3), 0, gus.neck)
cube("gus_vest", (0, -0.33, 1.95), (1.0, 0.05, 1.2), mat("gusvest", "#3f6b4a", 0.8), 0.02, gus.body)
tw1 = lib.Char("twin1", skin="#f3c89a", top="#2fb0a8", pants="#2f4a7a", hair="#e0702e", hair_style="spiky", **K)
tw2 = lib.Char("twin2", skin="#f3c89a", top="#2fb0a8", pants="#2f4a7a", hair="#e0702e", hair_style="spiky", **K)
crowd = []
CC = [("#3f8fd8", "#6b3f22"), ("#e86fb0", "#1d1310"), ("#57b65a", "#e0c070"), ("#8b4fb0", "#6b3f22"), ("#e8823f", "#1d1310"),
      ("#2fb0a8", "#e0702e"), ("#c94a4a", "#3a2414"), ("#6a7ad8", "#eeeeee"), ("#f2c53d", "#3a2414"), ("#ff8fb0", "#1d1310"),
      ("#4ac0e8", "#3a2414"), ("#a0d040", "#1d1310"), ("#e85a3a", "#e0c070"), ("#7a5ad8", "#1d1310")]
for i, (top, hair) in enumerate(CC):
    crowd.append(lib.Char(f"cr{i}", skin=["#f3c89a", "#c98d62", "#8d5a3b", "#e9b892"][i % 4], top=top, pants=["#3b3b55", "#c9b48a", "#2f4a7a"][i % 3],
                          hair=hair, hair_style="spiky" if i % 3 == 0 else "flat", kid=i % 2 == 0, **K))
CAST = [hero, ben, baker, gran, mayor, pick, gus, tw1, tw2] + crowd
for c in CAST: AS.add_muffs(c)
for c in (ben, mayor, tw1, tw2, hero): AS.add_pyjama_cap(c, {"benny": "#3f6fd8", "mayor": "#c8282f", "hero": "#57b65a"}.get(c.name, "#ff8fb0"))
gran.muffs2 = empty("gran_muffs2", (0, 0, 0.75 * gran.hs), gran.neck)
for sd in (-1, 1): sphere(f"gran_m2{sd}", (0.62 * sd * gran.hs, 0, 0), (0.2 * gran.hs, 0.32 * gran.hs, 0.32 * gran.hs), mat("muff2", "#7fe6ff", 0.95), gran.muffs2, 12)
show(gran.muffs2, False)
pg = AS.Pigeon()
fill = point("camfill", (0.6, 0.4, 0.2), "#ffe6cc", 160, 1.0, cam)
OBJ = [o for o in bpy.data.objects]
BASE = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent) for o in OBJ}
LIGHTS = {o.name: o.data.energy for o in OBJ if o.type == "LIGHT"}
OFF = (0, 0, -500)
WX, AX = G["WX"], G["AX"]

# ------------------------------------------------ lighting moods
def mood(kind):
    sc.objects["hallglow"].data.energy = 600
    if kind == "day":
        bg.inputs["Color"].default_value = (*lib.srgb("#8fc8ff"), 1); bg.inputs["Strength"].default_value = 1.5
        sun.data.energy = 4.5; sun.data.color = lib.srgb("#fff0d8"); sun.rotation_euler = (math.radians(50), 0, math.radians(215))
        for l in LAMPS: l.data.energy = 0
        sc.view_settings.exposure = 0.3; fill.data.energy = 160
    elif kind == "dawn":     # 5 AM: deep blue sky with a pink edge, street lamps + warm windows, cool sun
        bg.inputs["Color"].default_value = (*lib.srgb("#4a4fb0"), 1); bg.inputs["Strength"].default_value = 0.9
        sun.data.energy = 1.4; sun.data.color = lib.srgb("#ffb0c8"); sun.rotation_euler = (math.radians(72), 0, math.radians(120))
        for l in LAMPS: l.data.energy = 1400
        sc.view_settings.exposure = 0.75; fill.data.energy = 300
    elif kind == "sunrise":  # parade: golden low sun
        bg.inputs["Color"].default_value = (*lib.srgb("#ffb98a"), 1); bg.inputs["Strength"].default_value = 1.3
        sun.data.energy = 4.0; sun.data.color = lib.srgb("#ffc27a"); sun.rotation_euler = (math.radians(68), 0, math.radians(250))
        for l in LAMPS: l.data.energy = 300
        sc.view_settings.exposure = 0.45; fill.data.energy = 200
    elif kind == "dusk":
        bg.inputs["Color"].default_value = (*lib.srgb("#7a5ab8"), 1); bg.inputs["Strength"].default_value = 1.0
        sun.data.energy = 2.2; sun.data.color = lib.srgb("#ff9a6a"); sun.rotation_euler = (math.radians(70), 0, math.radians(300))
        for l in LAMPS: l.data.energy = 1200
        sc.view_settings.exposure = 0.6; fill.data.energy = 260
    elif kind == "night":
        bg.inputs["Color"].default_value = (*lib.srgb("#2a2470"), 1); bg.inputs["Strength"].default_value = 0.8
        sun.data.energy = 0.8; sun.data.color = lib.srgb("#9aa8ff"); sun.rotation_euler = (math.radians(55), 0, math.radians(200))
        for l in LAMPS: l.data.energy = 1500
        sc.view_settings.exposure = 0.7; fill.data.energy = 300

def scr(key, col="blue"):
    for k, o in G["txt"].items(): o.hide_render = (k != key)
    G["screen"].data.materials[0] = G["scrmats"][col]

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
    cam.data.lens = 28; cam.delta_location = (0, 0, 0)
    for k, o in G["txt"].items(): o.hide_render = True
    G["screen"].data.materials[0] = G["scrmats"]["blue"]
    G["wallm"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*lib.srgb("#5b7fd1"), 1)
    pg.fat(1.0)
    mood("day")

# ------------------------------------------------ helpers
def hold(obj, ch, side=1, loc=(0, -0.3, -1.05)):
    obj.parent = ch.arms[side]; obj.location = loc
def shake(f0, f1, amt=0.12, seed=1):
    r = random.Random(seed)
    for f in range(f0, f1 + 1):
        cam.delta_location = (r.uniform(-amt, amt), r.uniform(-amt, amt), r.uniform(-amt, amt)); cam.keyframe_insert("delta_location", frame=f)
    cam.delta_location = (0, 0, 0); cam.keyframe_insert("delta_location", frame=f1 + 1)
def cheer(c, f0, f1, seed=0):
    c.face("happy", f0); f = f0 + seed % 3; k = 0
    while f <= f1:
        c.pose(f, armL=-160 if k % 2 else -130, armR=-130 if k % 2 else -165, armLs=20, armRs=20, bob=0.2 if k % 2 else 0); f += 3; k += 1
    c.talk(f0, f1, 0.16, 2)
def sleep_face(c, f=None):
    c.face("neutral", f)
    for e in c.eyes:
        e.scale = (e.scale[0], e.scale[1], e.scale[2] * 0.1)
        if f is not None: e.keyframe_insert("scale", frame=f)
def blink_open(c, f):
    c.face("surprised", f)
def zzz(f0, f1, at):
    for i, z in enumerate(G["zz"]):
        p = f0 + i * 5
        z.location = at; z.scale = (0.2, 0.2, 0.2); z.keyframe_insert("location", frame=p); z.keyframe_insert("scale", frame=p)
        z.location = (at[0] + 0.6 + i * 0.3, at[1], at[2] + 1.6 + i * 0.4); z.scale = (1, 1, 1); z.keyframe_insert("location", frame=p + 14); z.keyframe_insert("scale", frame=p + 14)
def pea(i, f0, f1, p0, p1, arc=0.6, after=None):
    """one pea flying from p0 to p1 between frames f0..f1 (simple arc), then optional rest point"""
    o = G["peas"][i]
    o.location = OFF; o.keyframe_insert("location", frame=max(0, f0 - 1))
    for k in range(0, 5):
        t = k / 4; f = round(f0 + (f1 - f0) * t)
        o.location = tuple(p0[j] + (p1[j] - p0[j]) * t for j in range(3)); o.location.z += arc * 4 * t * (1 - t)
        o.keyframe_insert("location", frame=f)
    if after:
        o.location = after; o.keyframe_insert("location", frame=f1 + 4)
def shooter_on(c, obj=None):
    obj = obj or G["shooter"]; obj.parent = c.neck; obj.location = (0.0, -0.75 * c.hs, 0.32 * c.hs); obj.rotation_euler = (0, 0, 0)
    c.pose(armR=-80, armL=-80)
def muffs(c, on=True): show(c.muffs, on)
def cap(c, on=True):
    if hasattr(c, "cap"): show(c.cap, on)
def wall(col): G["wallm"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*lib.srgb(col), 1)
def lie(c, loc, f=None):
    c.root.location = loc; c.root.rotation_euler = (math.radians(-90), 0, 0)
ROOF = lambda x, y=13: (x, y, 7.42)   # top of a north-row roof (stand here)
def house_window(x, y=13, side=-2):
    return (x + side, y - 3.05, 3.4)
