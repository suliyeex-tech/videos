"""Sets, cast and helpers for the 2026-11-21 long-form "In This Town, Nobody Owns an Alarm Clock" (16:9).
Imported by alarm_shots.py. Our own Blocktown cast + town (engine/blocktown/lib.py); never Roblox assets/name/UI.
Set offsets: town x=0, bedroom x=300 (hero / Benny / Mayor via recolour), window set x=1100, attic x=900."""
import math, random, bpy
import lib
from lib import cube, sphere, cyl, empty, point, spot, mat

_F = {}
def font():
    if "f" not in _F or _F["f"] is None:
        try: _F["f"] = bpy.data.fonts.load("/root/.fonts/Fredoka-Bold.ttf", check_existing=True)
        except Exception: _F["f"] = None
    return _F["f"]

def mktext(name, body, loc, size, col, emit=0.0, rot=(90, 0, 0), extrude=0.04):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = extrude
    if font(): cu.font = font()
    o = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(o); o.location = loc
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    cu.materials.append(mat(name + "m", col, 0.5, emit)); return o

def torus(name, loc, R, r, m, zs=1.0, parent=None, seg=(32, 12)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=seg[0], minor_segments=seg[1], location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = (1, 1, zs); o.data.materials.append(m); bpy.ops.object.shade_smooth()
    if parent: o.parent = parent
    return o

def show(o, on=True):
    o.hide_render = not on
    for ch in o.children_recursive: ch.hide_render = not on

def build_all(sc):
    G = {}
    G["town"] = lib.build_town()
    lib.build_bedroom(300)
    for n in ("alarmclock", "alarmface"): sc.objects[n].hide_render = True       # nobody owns an alarm clock (until the end)
    # ------------------------------------------------ bakery (house at x=12, y=13): sign + striped awning
    cube("bk_sign", (12, 9.9, 5.0), (5.2, 0.25, 1.1), mat("bksign", "#ffe7b0", 0.5), 0.08)
    mktext("bk_txt", "BAKERY", (12, 9.72, 5.0), 0.8, "#b3412e", 0.0)
    for i in range(7): cube(f"bk_aw{i}", (12 - 3 + i, 9.6, 4.15), (1.0, 1.4, 0.15), mat(f"bkaw{i % 2}", "#e8423f" if i % 2 else "#ffffff", 0.6), 0.02, None, (math.radians(-20), 0, 0))
    G["bkglow"] = point("bkglow", (12, 9.0, 3.2), "#ffb35a", 0, 1.0)
    # chimneys on the north-row houses (for the chimney drops)
    for x in (-60, -48, -36, -24, -12, 12, 24, 36, 48, 60):
        cube(f"chim{x}", (x + 2.2, 14.2, 7.6), (1.0, 1.0, 2.0), mat("chim", "#9a4a3a", 0.8), 0.04)
    # ------------------------------------------------ stage + big screen on the square (in front of the town hall)
    st = []
    st.append(cube("stage", (0, 26.5, 0.7), (14, 5, 1.4), mat("stagefloor", "#2a2350", 0.4), 0.05))
    st.append(cube("stage_edge", (0, 23.98, 1.3), (14.2, 0.12, 0.2), mat("neon_cyan", "#40f0ff", 0.3, 8, "#40f0ff"), 0))
    st.append(cube("screenwall", (0, 28.8, 5.0), (12, 0.5, 8.6), mat("screenwall", "#120e22", 0.4), 0.05))
    G["scrmats"] = {k: mat("scr_" + k, c, 0.3, 1.0, c) for k, c in (("blue", "#1a2a9a"), ("red", "#a01020"), ("green", "#0f7a34"), ("pink", "#a0186a"), ("gold", "#a06a08"))}
    G["screen"] = cube("bigscreen", (0, 28.5, 5.6), (9.0, 0.1, 5.0), G["scrmats"]["blue"], 0); st.append(G["screen"])
    for i in range(18):
        x = -4.6 + 9.2 * (i % 9) / 8
        st.append(sphere(f"bulb{i}", (x, 28.4, 8.3 if i < 9 else 2.95), (0.15, 0.15, 0.15), mat("bulbm", "#ffe27a", 0.3, 10, "#ffcf4a"), seg=8))
    for i in range(14):
        x = -6.6 + i * 1.0
        st.append(cube(f"bunt{i}", (x, 24.2, 9.3 - 0.7 * math.sin(math.pi * i / 13)), (0.7, 0.05, 0.7), mat(f"bunt{i % 4}", ["#ff4fd0", "#ffe14a", "#40f0ff", "#5fff7a"][i % 4], 0.6, 0.3), 0, None, (0, math.radians(45), 0)))
    G["stage"] = st
    G["txt"] = {}
    for key, body, size, col in (("sunrise", "SUNRISE\nPARADE", 1.15, "#ffffff"), ("fri", "FRIDAY\n6 AM", 1.4, "#ffffff"), ("prize", "$5,000", 1.9, "#ffe14a"),
                                 ("d1", "DAY 1\n299/300", 1.3, "#ffffff"), ("d2", "DAY 2\n300/300", 1.3, "#ffffff"), ("d3", "DAY 3\n300/300", 1.3, "#ffffff"),
                                 ("d4", "DAY 4\n300/300", 1.3, "#ffffff"), ("zero", "0/300", 2.2, "#ffffff"), ("c298", "298", 2.6, "#ffffff"),
                                 ("c299", "299/300", 2.0, "#ffffff"), ("c300", "300/300", 2.0, "#ffe14a"), ("strike", "1 STRIKE", 1.6, "#ffffff"), ("bye", "HAPPY\nRETIREMENT\nGUS!", 1.0, "#ffffff")):
        G["txt"][key] = mktext("scr_" + key, body, (0, 28.42, 5.6), size, col, 4.0, extrude=0.01)
    # ------------------------------------------------ window set (x=1100): wall with a window opening, lit room behind
    WX = 1100
    G["wallm"] = mat("winwall", "#5b7fd1", 0.7)
    for nm, loc, sz in (("wl_L", (WX - 4.25, 0, 3.6), (5.5, 0.4, 7.2)), ("wl_R", (WX + 4.25, 0, 3.6), (5.5, 0.4, 7.2)),
                        ("wl_B", (WX, 0, 0.95), (3.0, 0.4, 1.9)), ("wl_T", (WX, 0, 6.05), (3.0, 0.4, 2.3))):
        cube(nm, loc, sz, G["wallm"], 0.03)
    trim = mat("trim", "#f4f1e8")
    for nm, loc, sz in (("wf_l", (WX - 1.55, -0.25, 3.4), (0.2, 0.2, 3.2)), ("wf_r", (WX + 1.55, -0.25, 3.4), (0.2, 0.2, 3.2)),
                        ("wf_t", (WX, -0.25, 4.95), (3.3, 0.2, 0.2)), ("wf_s", (WX, -0.4, 1.85), (3.6, 0.5, 0.18)), ("wf_m", (WX, -0.22, 3.4), (0.08, 0.08, 3.0))):
        cube(nm, loc, sz, trim, 0.02)
    G["curtm"] = mat("wcurt", "#d0638f", 0.9)
    cube("wcurL", (WX - 1.25, 0.35, 3.5), (0.6, 0.15, 3.0), G["curtm"], 0.05); cube("wcurR", (WX + 1.25, 0.35, 3.5), (0.6, 0.15, 3.0), G["curtm"], 0.05)
    cube("wroom_floor", (WX, 4, 0.6), (12, 8, 0.2), mat("wfloor", "#7a5236", 0.7), 0)
    cube("wroom_back", (WX, 7, 4), (12, 0.3, 8), mat("wback", "#f2d9a8", 0.8), 0)
    cube("wroom_pic", (WX + 1.5, 6.8, 4.6), (1.4, 0.1, 1.0), mat("wpic", "#6bb7a3", 0.6), 0.03)
    G["wlamp"] = point("wlamp", (WX - 1.5, 3.5, 5.5), "#ffc27a", 350, 0.6)
    cube("wbush", (WX, -1.0, 0.6), (9, 1.2, 1.2), mat("leaf", "#2f7d3a", 0.8), 0.4)
    G["WX"] = WX
    # ------------------------------------------------ attic (x=900): sloped roof, round window, hundreds of alarm clocks
    AX = 900
    wood = mat("atwood", "#8a6440", 0.75)
    cube("at_floor", (AX, 0, -0.05), (16, 18, 0.1), wood, 0)
    for sd in (-1, 1):
        cube(f"at_roof{sd}", (AX + 4.2 * sd, 0, 4.6), (0.3, 18, 11), mat("atroof", "#6b4a33", 0.85), 0, None, (0, math.radians(-38 * sd), 0))
    cube("at_back", (AX, 8.0, 4.5), (16, 0.3, 9), mat("atback", "#7a5638", 0.85), 0)
    cube("at_front", (AX, -9.0, 4.5), (16, 0.3, 9), mat("atback", "#7a5638", 0.85), 0)
    cube("at_door", (AX - 3, -8.8, 1.6), (2.0, 0.1, 3.2), mat("atdoor", "#5a3b26", 0.7), 0.03)
    cyl("at_window", (AX, 7.8, 5.2), 1.3, 0.3, mat("atwin", "#ffe9b8", 0.3, 4.0, "#ffd89a"), rot=(math.pi / 2, 0, 0), verts=32)
    cyl("at_winrim", (AX, 7.75, 5.2), 1.45, 0.2, mat("trim", "#f4f1e8"), rot=(math.pi / 2, 0, 0), verts=32)
    for i in range(4): cube(f"at_beam{i}", (AX, -6 + i * 4, 8.6), (0.4, 0.4, 0.4), wood, 0.02)
    cube("at_ridge", (AX, 0, 8.7), (0.4, 18, 0.4), wood, 0.02)
    G["atglow"] = point("at_sun", (AX, 6.0, 5.2), "#ffd08a", 900, 1.5)
    point("at_fill", (AX, -4, 5), "#ffd9b0", 500, 2.0)
    # one master alarm clock, many linked copies
    clk = empty("clk_master", (0, 0, -600))
    body_cols = ["#e8423f", "#3f8fd8", "#ffe14a", "#5fbf5a", "#ff8fb0", "#ffffff", "#8b4fb0"]
    face_m = mat("clkface", "#fffbe8", 0.4, 0.3); hand_m = mat("clkhand", "#1a1a1a", 0.3); bell_m = mat("clkbell", "#d9d9e0", 0.25, metal=0.9)
    masters = []
    for ci, col in enumerate(body_cols):
        root = empty(f"clkM{ci}", (0, 0, -600))
        cyl(f"clkM{ci}_b", (0, 0, 0.45), 0.42, 0.3, mat(f"clkb{ci}", col, 0.45), rot=(math.pi / 2, 0, 0), parent=root, verts=20)
        cyl(f"clkM{ci}_f", (0, -0.16, 0.45), 0.33, 0.04, face_m, rot=(math.pi / 2, 0, 0), parent=root, verts=20)
        cube(f"clkM{ci}_h1", (0.0, -0.19, 0.52), (0.05, 0.02, 0.18), hand_m, 0, root); cube(f"clkM{ci}_h2", (0.08, -0.19, 0.45), (0.16, 0.02, 0.04), hand_m, 0, root)
        for sd in (-1, 1):
            sphere(f"clkM{ci}_bell{sd}", (0.27 * sd, 0.0, 0.88), (0.16, 0.16, 0.12), bell_m, root, 10)
            cube(f"clkM{ci}_leg{sd}", (0.25 * sd, 0, 0.1), (0.06, 0.06, 0.2), hand_m, 0, root)
        masters.append(root)
    rr = random.Random(21); clocks = []
    def place_copy(root, loc, rz, s):
        new = empty(root.name + f"_c{len(clocks)}", loc); new.rotation_euler = (0, 0, rz); new.scale = (s, s, s)
        for ch in root.children:
            c = ch.copy(); bpy.context.scene.collection.objects.link(c); c.parent = new
        clocks.append(new)
    # piles: rows on shelves along both sides + heaps on the floor
    for side in (-1, 1):
        for row in range(4):
            for k in range(14):
                place_copy(masters[rr.randrange(7)], (AX + side * (5.2 - row * 0.55), -6.5 + k * 1.0 + rr.uniform(-0.1, 0.1), 0.05 + row * 0.95), math.radians(90 * side + rr.uniform(-25, 25)), 1.0)
    for k in range(70):
        a = rr.uniform(0, 2 * math.pi); r = rr.uniform(0.5, 3.0)
        place_copy(masters[rr.randrange(7)], (AX + 2.6 * math.cos(a) * (r / 3), 2.0 + r * math.sin(a) * 0.9, 0.05 + max(0, 1.4 - r * 0.45) * rr.random()), rr.uniform(-1, 1), 1.0)
    G["clockmasters"] = masters
    G["giftclock"] = empty("giftclock", (0, 0, -500))
    for ch in masters[0].children:
        c = ch.copy(); bpy.context.scene.collection.objects.link(c); c.parent = G["giftclock"]
    G["AX"] = AX
    # ------------------------------------------------ the net over Main Street
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=60, y_subdivisions=14, size=1, location=(0, 0, 8.5))
    net = bpy.context.object; net.name = "net"; net.scale = (60, 16, 1)
    for v in net.data.vertices: v.co.z = -0.035 * (1 - (2 * v.co.y) ** 2) * 16
    wf = net.modifiers.new("w", "WIREFRAME"); wf.thickness = 0.004; net.data.materials.append(mat("netm", "#2f6b3a", 0.6))
    net.hide_render = True; G["net"] = net
    # ------------------------------------------------ the giant fan (summer fair)
    fan = empty("fan", (0, 0, -500))
    cube("fan_base", (0, 0, 0.4), (2.6, 2.0, 0.8), mat("fanbase", "#3f8fd8", 0.5), 0.1, fan)
    cyl("fan_pole", (0, 0, 2.2), 0.25, 3.2, mat("fanpole", "#dddddd", 0.3, metal=0.6), parent=fan, verts=12)
    torus("fan_ring", (0, 0, 4.6), 2.4, 0.16, mat("fanring", "#e8e8f0", 0.3, metal=0.5), 1.0, fan).rotation_euler = (math.pi / 2, 0, 0)
    G["fanhub"] = empty("fan_hub", (0, -0.1, 4.6), fan)
    cyl("fan_hubc", (0, 0, 0), 0.45, 0.5, mat("fanhubm", "#ffe14a", 0.4), rot=(math.pi / 2, 0, 0), parent=G["fanhub"], verts=16)
    for i in range(4):
        b = empty(f"fan_bp{i}", (0, 0, 0), G["fanhub"]); b.rotation_euler = (0, math.radians(90 * i), 0)
        cube(f"fan_blade{i}", (0, 0, 1.2), (0.9, 0.08, 1.9), mat("fanblade", "#ff8fb0", 0.4), 0.06, b, (0, 0, math.radians(20)))
    G["fan"] = fan
    # ------------------------------------------------ delivery truck (earmuffs)
    trk = empty("truck", (0, 0, -500))
    cube("tr_box", (0, 1.2, 2.4), (3.0, 5.0, 3.2), mat("trbox", "#ff8fb0", 0.5), 0.1, trk)
    mktext("tr_txt", "FREE\nEARMUFFS", (1.52, 1.2, 2.5), 0.55, "#ffffff", 0.3, rot=(90, 0, 90)).parent = trk
    cube("tr_cab", (0, -2.3, 1.9), (2.9, 2.0, 2.3), mat("trcab", "#5c9a3a", 0.5), 0.12, trk)
    cube("tr_glass", (0, -3.32, 2.4), (2.4, 0.05, 0.9), mat("trglass", "#9fd8ff", 0.1, 0.6), 0.02, trk)
    for x in (-1.3, 1.3):
        for y in (-2.3, 2.6): cyl(f"tr_wh{x}{y}", (x, y, 0.55), 0.55, 0.4, mat("tire", "#1c1c1c", 0.8), rot=(0, math.pi / 2, 0), parent=trk, verts=16)
    G["truck"] = trk
    # ------------------------------------------------ small props
    G["peas"] = [sphere(f"pea{i}", (0, 0, -500), (0.12, 0.12, 0.12), mat("pea", "#6fcf3a", 0.4, 0.4, "#6fcf3a"), seg=8) for i in range(40)]
    G["shooter"] = empty("shooter", (0, 0, -500))
    cyl("sh_tube", (0, -0.6, 0), 0.09, 1.3, mat("shtube", "#3fae5a", 0.35), rot=(math.pi / 2, 0, 0), parent=G["shooter"], verts=12)
    G["gshooter"] = empty("gshooter", (0, 0, -500))
    cyl("gsh_tube", (0, -0.6, 0), 0.12, 1.5, mat("gold", "#e2b23a", 0.25, metal=1.0), rot=(math.pi / 2, 0, 0), parent=G["gshooter"], verts=16)
    point("gsh_glow", (0, -0.6, 0.4), "#ffcf4a", 0, 0.3, G["gshooter"])
    G["gusshooter"] = empty("gusshooter", (0, 0, -500))
    cyl("gus_tube", (0, -0.7, 0), 0.08, 1.5, mat("gustube", "#8a6440", 0.5), rot=(math.pi / 2, 0, 0), parent=G["gusshooter"], verts=12)
    G["bag"] = empty("peabag", (0, 0, -500))
    cube("bag_b", (0, 0, 0.45), (0.8, 0.6, 0.9), mat("bag", "#c9a46a", 0.9), 0.25, G["bag"]); cube("bag_tie", (0, 0, 0.95), (0.3, 0.3, 0.2), mat("bagtie", "#7a5236", 0.8), 0.05, G["bag"])
    G["frozen"] = empty("frozenbag", (0, 0, -500))
    cube("fz_b", (0, 0, 0.5), (0.9, 0.25, 1.1), mat("fzbag", "#4ac0e8", 0.3, 0.2), 0.08, G["frozen"]); mktext("fz_t", "PEAS", (0, -0.14, 0.55), 0.28, "#ffffff", 0.3).parent = G["frozen"]
    G["croissant"] = empty("croissant", (0, 0, -500))
    for i in range(5):
        a = math.radians(-60 + i * 30); s = 0.32 - abs(i - 2) * 0.06
        sphere(f"cr_seg{i}", (0.7 * math.sin(a), 0, 0.7 * math.cos(a) - 0.5), (s, s, s), mat("croiss", "#d99a3f", 0.55), G["croissant"], 10)
    G["rolls"] = []
    for i in range(12):
        o = torus(f"roll{i}", (0, 0, -500), 0.32, 0.18, mat("roll", "#c98540", 0.6), 0.8); G["rolls"].append(o)
        torus(f"rollic{i}", (0, 0, 0.12), 0.26, 0.09, mat("icing", "#fff6e8", 0.4), 0.6, o)
    G["smell"] = [sphere(f"smell{i}", (0, 0, -500), (0.35, 0.35, 0.35), mat("smellm", "#ffb35a", 0.5, 2.5, "#ffa040"), seg=8) for i in range(36)]
    G["zz"] = [mktext(f"zz{i}", "Z", (0, 0, -500), 0.45 + 0.12 * i, "#ffffff", 1.0) for i in range(3)]
    G["box"] = empty("muffbox", (0, 0, -500))
    cube("mb_b", (0, 0, 0.5), (1.6, 1.2, 1.0), mat("mbox", "#e8d0a0", 0.8), 0.04, G["box"])
    mktext("mb_t", "SLEEP TIGHT\nlove, Mrs. P", (0, -0.62, 0.55), 0.2, "#b0263a", 0.0).parent = G["box"]
    G["muffs_spare"] = []
    G["plate"] = empty("plate", (0, 0, -500))
    cyl("pl_p", (0, 0, 0), 0.55, 0.06, mat("platem", "#ffffff", 0.3), parent=G["plate"], verts=20)
    G["cheque"] = empty("cheque", (0, 0, -500))
    cube("chq", (0, 0, 0.4), (2.6, 0.06, 1.2), mat("chq", "#e8ffe8", 0.6), 0.03, G["cheque"])
    mktext("chqt", "$5,000", (0, -0.05, 0.4), 0.55, "#1a7a3a", 0.0, extrude=0.01).parent = G["cheque"]
    return G

# ------------------------------------------------ pigeon (same blocky bird as the donut Short)
class Pigeon:
    def __init__(self, fat=1.0):
        g, dg, w = mat("pg_body", "#8f95a8", 0.7), mat("pg_dark", "#5d6275", 0.7), mat("pg_neck", "#5fb89a", 0.4, 0.2)
        self.root = empty("pigeon", (0, 0, -500))
        self.torso = cube("pg_torso", (0, 0.1, 0.45), (0.55, 0.85, 0.55), g, 0.18, self.root)
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
    def fat(self, k, f=None):
        self.torso.scale = (k, 1 + (k - 1) * 0.5, k)
        if f is not None: self.torso.keyframe_insert("scale", frame=f)
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

def add_muffs(c):
    """fluffy pink earmuffs parented to the head (hidden until switched on)"""
    hs = c.hs; m = mat("muff", "#ff8fc8", 0.95); root = empty(c.name + "_muffs", (0, 0, 0.52 * hs), c.neck)
    for sd in (-1, 1): sphere(f"{c.name}_muff{sd}", (0.58 * sd * hs, 0, -0.02 * hs), (0.22 * hs, 0.36 * hs, 0.36 * hs), m, root, 12)
    cube(c.name + "_muffband", (0, 0, 0.62 * hs), (1.2 * hs, 0.14 * hs, 0.1 * hs), mat("muffband", "#d84a9a", 0.5), 0.03, root)
    show(root, False); c.muffs = root
    return root

def add_pyjama_cap(c, col="#3f6fd8"):
    hs = c.hs; root = empty(c.name + "_cap", (0, 0.1, 1.1 * hs), c.neck)
    cube(c.name + "_capc", (0, 0, 0), (1.1 * hs, 1.1 * hs, 0.35 * hs), mat("pjcap" + col, col, 0.8), 0.15, root)
    cube(c.name + "_capt", (0.3 * hs, 0.4 * hs, 0.25 * hs), (0.6 * hs, 0.6 * hs, 0.3 * hs), mat("pjcap" + col, col, 0.8), 0.15, root, (0, math.radians(30), 0))
    sphere(c.name + "_pom", (0.65 * hs, 0.6 * hs, 0.35 * hs), (0.18 * hs, 0.18 * hs, 0.18 * hs), mat("pom", "#ffffff", 0.9), root, 8)
    show(root, False); c.cap = root
    return root
