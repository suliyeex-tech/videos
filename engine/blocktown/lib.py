"""Blocktown kit (owner 2026-11-18): reusable night town, blocky cast with painted faces, interiors, shot helpers.
Headless Blender (pip install bpy). Look target: owner's reference Shorts — night suburb, saturated neon light,
cube-head toy characters with big oval painted eyes, 1-word captions. Our own designs only (never Roblox assets/name).
Units: 1 = ~30 cm. Characters ~3.6 tall. Sets live at different X offsets in one scene:
town x=0, bedroom x=300, stairs x=500, clock room x=700."""
import bpy, math, random
from mathutils import Vector

def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)

_M = {}
def mat(name, hexc, rough=0.55, emit=0.0, ehex=None, metal=0.0):
    key = (name, hexc, rough, emit, ehex, metal)
    if key in _M: return _M[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*srgb(hexc), 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*srgb(ehex or hexc), 1); b.inputs["Emission Strength"].default_value = emit
    _M[key] = m; return m

def link(o, coll=None):
    return o

def cube(name, loc, size, m, bevel=0.05, parent=None, rot=None):
    me = bpy.data.meshes.new(name)
    import bmesh
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    for v in me.vertices: v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    o.location = loc
    if rot: o.rotation_euler = rot
    if bevel:
        bv = o.modifiers.new("b", "BEVEL"); bv.width = min(bevel, min(size) * 0.45); bv.segments = 2
    me.materials.append(m)
    if parent: o.parent = parent
    return o

def cyl(name, loc, r, depth, m, rot=None, parent=None, verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc)
    o = bpy.context.object; o.name = name
    if rot: o.rotation_euler = rot
    o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def sphere(name, loc, scale, m, parent=None, seg=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale; o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    if parent: o.parent = parent
    return o

def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(o); o.location = loc
    if parent: o.parent = parent
    return o

def point(name, loc, color, energy, radius=0.3, parent=None):
    d = bpy.data.lights.new(name, "POINT"); d.color = srgb(color); d.energy = energy; d.shadow_soft_size = radius
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.location = loc
    if parent: o.parent = parent
    return o

def spot(name, loc, color, energy, angle=45, parent=None, rot=(0, 0, 0)):
    d = bpy.data.lights.new(name, "SPOT"); d.color = srgb(color); d.energy = energy; d.spot_size = math.radians(angle); d.spot_blend = 0.5
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    return o

# ---------------------------------------------------------------- scene / render
def setup(res=(540, 960), samples=14, fps=12):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples
    sc.cycles.use_denoising = True; sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 1
    sc.cycles.transmission_bounces = 1; sc.cycles.volume_bounces = 0; sc.cycles.use_adaptive_sampling = True
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.resolution_percentage = 100
    sc.render.fps = fps; sc.render.image_settings.file_format = "PNG"
    try:
        sc.view_settings.view_transform = "AgX"
        for lk in ("AgX - Punchy", "Punchy"):
            try: sc.view_settings.look = lk; break
            except Exception: pass
    except Exception:
        sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs["Color"].default_value = (*srgb("#1a1f4a"), 1); bg.inputs["Strength"].default_value = 1.2
    sc.view_settings.exposure = 0.8; sc.render.use_persistent_data = True
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.lens = 28; cam.data.clip_end = 400
    tgt = empty("cam_target"); c = cam.constraints.new("TRACK_TO"); c.target = tgt; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
    return sc, cam, tgt

# ---------------------------------------------------------------- characters
class Char:
    """root (empty) -> hips; parts with pivots so we can pose: head, armL, armR, legL, legR. face: eyes, pupils, mouth, brows."""
    def __init__(self, name, skin="#f3c89a", top="#3f6fd8", pants="#c9b48a", hair="#6b3f22", hair_style="spiky",
                 shoes="#f2f2f2", hood=False, kid=True, extra=None, cartoon=False, blush=False):
        """cartoon=True (house style 2026-11-20): big white eyes with black pupils + glints parented to the white (so face()
        scaling squashes the whole eye), thick dark brows; blush=True adds pink cheeks."""
        s = 0.88 if kid else 1.0
        self.name = name; self.s = s
        self.root = empty(name)
        self.body = empty(name + "_body", (0, 0, 0), self.root)
        M = lambda n, c, **k: mat(f"{name}_{n}", c, **k)
        self.mskin, self.mtop, self.mpants, self.mhair = M("skin", skin), M("top", top), M("pants", pants), M("hair", hair)
        mshoe = M("shoe", shoes)
        self.legs = []
        for side in (-1, 1):
            hip = empty(f"{name}_hip{side}", (0.29 * side * s, 0, 1.25 * s), self.body)
            cube(f"{name}_leg{side}", (0, 0, -0.55 * s), (0.52 * s, 0.55 * s, 1.1 * s), self.mpants, 0.05, hip)
            cube(f"{name}_shoe{side}", (0, -0.04, -1.16 * s), (0.54 * s, 0.62 * s, 0.18 * s), mshoe, 0.05, hip)
            self.legs.append(hip)
        self.torso = cube(f"{name}_torso", (0, 0, 1.95 * s), (1.18 * s, 0.62 * s, 1.4 * s), self.mtop, 0.07, self.body)
        if hood:
            cube(f"{name}_hood", (0, 0.27 * s, 2.62 * s), (1.0 * s, 0.25 * s, 0.32 * s), self.mtop, 0.08, self.body)
            cube(f"{name}_pocket", (0, -0.32 * s, 1.62 * s), (0.7 * s, 0.03, 0.32 * s), M("pocket", extra or top), 0.03, self.body)
        self.arms = []
        for side in (-1, 1):
            sh = empty(f"{name}_sh{side}", (0.86 * side * s, 0, 2.55 * s), self.body)
            cube(f"{name}_sleeve{side}", (0, 0, -0.38 * s), (0.5 * s, 0.56 * s, 0.8 * s), self.mtop, 0.05, sh)
            cube(f"{name}_hand{side}", (0, 0, -0.98 * s), (0.46 * s, 0.5 * s, 0.42 * s), self.mskin, 0.06, sh)
            self.arms.append(sh)
        self.neck = empty(f"{name}_neck", (0, 0, 2.66 * s), self.body)
        hs = 1.0 * s
        self.head = cube(f"{name}_head", (0, 0, 0.52 * hs), (hs, hs, hs), self.mskin, 0.14, self.neck)
        self.hair = []
        hz = 0.52 * hs + 0.5 * hs
        if hair_style == "spiky":
            self.hair.append(cube(f"{name}_hairtop", (0, 0.03, hz), (1.06 * hs, 1.06 * hs, 0.26 * hs), self.mhair, 0.06, self.neck))
            self.hair.append(cube(f"{name}_hairback", (0, 0.45 * hs, 0.62 * hs), (1.06 * hs, 0.18 * hs, 0.9 * hs), self.mhair, 0.05, self.neck))
            for i, (x, y, r) in enumerate(((-0.3, -0.25, 25), (0.05, -0.32, -10), (0.32, -0.2, -30), (-0.1, 0.1, 15), (0.25, 0.25, -20))):
                self.hair.append(cube(f"{name}_spike{i}", (x * hs, y * hs, hz + 0.16 * hs), (0.34 * hs, 0.34 * hs, 0.34 * hs), self.mhair, 0.03,
                                      self.neck, (math.radians(r), math.radians(r * 0.6), math.radians(45))))
            self.hair.append(cube(f"{name}_fringe", (0, -0.5 * hs, hz - 0.08 * hs), (1.06 * hs, 0.12 * hs, 0.22 * hs), self.mhair, 0.03, self.neck))
        elif hair_style == "flat":
            self.hair.append(cube(f"{name}_hairtop", (0, 0.04, hz), (1.06 * hs, 1.06 * hs, 0.22 * hs), self.mhair, 0.06, self.neck))
            self.hair.append(cube(f"{name}_hairback", (0, 0.45 * hs, 0.6 * hs), (1.06 * hs, 0.18 * hs, 0.85 * hs), self.mhair, 0.05, self.neck))
            for sd in (-1, 1):
                self.hair.append(cube(f"{name}_side{sd}", (0.5 * sd * hs, 0.05, 0.75 * hs), (0.1 * hs, 0.9 * hs, 0.45 * hs), self.mhair, 0.03, self.neck))
        # face (painted look: glossy black ovals with a white glint)
        fy = -0.505 * hs; ez = 0.6 * hs
        blk, wht = mat("eyeblack", "#141414", 0.25), mat("eyewhite", "#ffffff", 0.3, 1.5)
        self.eyes, self.glints = [], []
        self.cartoon = cartoon; self.EB = (0.15, 0.03, 0.19) if cartoon else (0.085, 0.03, 0.135)
        for sd in (-1, 1):
            if cartoon:
                sclera = mat("sclera", "#ffffff", 0.35, 0.25)
                e = sphere(f"{name}_eye{sd}", (0.22 * sd * hs, fy + 0.005, ez - 0.02 * hs), (0.15 * hs, 0.03, 0.19 * hs), sclera, self.neck)
                p = sphere(f"{name}_pupil{sd}", (0.06 * sd, -0.75, -0.08), (0.58, 0.9, 0.62), blk, e)
                g = sphere(f"{name}_glint{sd}", (0.24 * sd + 0.06, -1.5, 0.22), (0.2, 0.5, 0.22), wht, e, 8)
            else:
                e = sphere(f"{name}_eye{sd}", (0.2 * sd * hs, fy, ez), (0.085 * hs, 0.03, 0.135 * hs), blk, self.neck)
                g = sphere(f"{name}_glint{sd}", (0.2 * sd * hs + 0.03 * hs, fy - 0.025, ez + 0.05 * hs), (0.028 * hs, 0.012, 0.035 * hs), wht, self.neck, 8)
            self.eyes.append(e); self.glints.append(g)
        if blush:
            for sd in (-1, 1):
                sphere(f"{name}_blush{sd}", (0.33 * sd * hs, fy - 0.005, 0.33 * hs), (0.1 * hs, 0.02, 0.06 * hs), mat("blush", "#ff7a9a", 0.6, 0.4, "#ff6f91"), self.neck, 10)
        self.mouth = cube(f"{name}_mouth", (0, fy, 0.3 * hs), (0.2 * hs, 0.03, 0.045 * hs), mat("mouth", "#3a1512", 0.5), 0.0, self.neck)
        bw = (0.26 * hs, 0.04, 0.085 * hs) if cartoon else (0.2 * hs, 0.03, 0.05 * hs)
        self.brows = [cube(f"{name}_brow{sd}", (0.21 * sd * hs, fy - 0.01, 0.84 * hs if cartoon else 0.82 * hs), bw, mat(f"{name}_brow", hair if hair_style != "bald" else "#555555"), 0.0, self.neck)
                      for sd in (-1, 1)]
        self.hs = hs; self._ez = ez
        self.face("neutral")

    def mayor_kit(self):
        s = self.s; hs = self.hs
        blk = mat("hat", "#15151c", 0.4)
        self.hat = empty(self.name + "_hat", (0, 0, 1.05 * hs), self.neck)
        cyl(self.name + "_brim", (0, 0, 0), 0.78 * hs, 0.08, blk, parent=self.hat, verts=24)
        cyl(self.name + "_crown", (0, 0, 0.55 * hs), 0.52 * hs, 1.05 * hs, blk, parent=self.hat, verts=24)
        cyl(self.name + "_band", (0, 0, 0.18 * hs), 0.535 * hs, 0.18 * hs, mat("hatband", "#b0262e"), parent=self.hat, verts=24)
        cube(self.name + "_sash", (0, -0.33 * s, 1.95 * s), (0.32 * s, 0.05, 1.6 * s), mat("sash", "#c8282f", 0.5), 0.02, self.body, (0, math.radians(35), 0))
        cube(self.name + "_medal", (0.22 * s, -0.37 * s, 1.75 * s), (0.22 * s, 0.04, 0.22 * s), mat("gold", "#e2b23a", 0.25, metal=1.0), 0.04, self.body)
        self.mustache = cube(self.name + "_mustache", (0, -0.53 * hs, 0.42 * hs), (0.5 * hs, 0.06, 0.12 * hs), self.mhair, 0.03, self.neck)
        for sd in (-1, 1):
            cube(f"{self.name}_tie{sd}", (0, -0.32 * s, 2.45 * s), (0.16 * s, 0.04, 0.18 * s), mat("shirtw", "#eeeeee"), 0.02, self.body)

    def face(self, kind, f=None):
        hs = self.hs
        E = {"neutral": (1, 1, 0.2, 0.045, 0, 0), "happy": (1, 0.85, 0.26, 0.07, 0, 0), "surprised": (1.25, 1.3, 0.13, 0.14, 0, 0.06),
             "scared": (1.2, 1.25, 0.24, 0.1, 15, 0.05), "evil": (0.9, 0.7, 0.28, 0.05, -25, -0.02), "shock": (1.4, 1.45, 0.16, 0.18, 10, 0.08),
             "determined": (1, 0.8, 0.18, 0.04, -15, -0.03), "frozen": (1, 1, 0.12, 0.12, 0, 0.04)}[kind]
        ew, eh, mw, mh, brow, by = E
        for sd, e, g, b in zip((-1, 1), self.eyes, self.glints, self.brows):
            e.scale = (self.EB[0] * hs * ew, self.EB[1], self.EB[2] * hs * eh)
            b.location.z = (0.86 if self.cartoon else 0.82) * hs + by * hs; b.rotation_euler = (0, math.radians(brow * sd), 0)
            if f is not None:
                e.keyframe_insert("scale", frame=f); b.keyframe_insert("location", frame=f); b.keyframe_insert("rotation_euler", frame=f)
        self.mouth.scale = (mw / 0.2, 1, mh / 0.045)
        if f is not None: self.mouth.keyframe_insert("scale", frame=f)

    def place(self, loc, yaw=0, f=None):
        self.root.location = loc; self.root.rotation_euler = (0, 0, math.radians(yaw))
        if f is not None: self.root.keyframe_insert("location", frame=f); self.root.keyframe_insert("rotation_euler", frame=f)

    def pose(self, f=None, armL=0, armR=0, armLs=0, armRs=0, legL=0, legR=0, head=0, headyaw=0, lean=0, bob=0):
        """angles in degrees: arm X rotation (forward +), arm side spread, leg swing, head pitch/yaw, body lean."""
        self.arms[0].rotation_euler = (math.radians(armL), math.radians(-armLs), 0)
        self.arms[1].rotation_euler = (math.radians(armR), math.radians(armRs), 0)
        self.legs[0].rotation_euler = (math.radians(legL), 0, 0); self.legs[1].rotation_euler = (math.radians(legR), 0, 0)
        self.neck.rotation_euler = (math.radians(head), 0, math.radians(headyaw))
        self.body.rotation_euler = (math.radians(lean), 0, 0); self.body.location = (0, 0, bob)
        if f is not None:
            for o in (*self.arms, *self.legs, self.neck):
                o.keyframe_insert("rotation_euler", frame=f)
            self.body.keyframe_insert("rotation_euler", frame=f); self.body.keyframe_insert("location", frame=f)

    def run(self, f0, f1, period=6, amp=45, lean=12):
        f = f0; k = 0
        while f <= f1:
            s = 1 if k % 2 == 0 else -1
            self.pose(f, armL=amp * s, armR=-amp * s, legL=-amp * 0.8 * s, legR=amp * 0.8 * s, lean=lean, bob=0.12 * (k % 2))
            f += period / 2; k += 1

    def walk(self, f0, f1, period=10):
        self.run(f0, f1, period, amp=25, lean=3)

    def talk(self, f0, f1, open_h=0.12, rate=3):
        f = f0; k = 0
        while f <= f1:
            self.mouth.scale = (1, 1, (open_h if k % 2 == 0 else 0.05) / 0.045); self.mouth.keyframe_insert("scale", frame=f)
            f += rate; k += 1

    def recolor_hair(self, hexc):
        for n in self.mhair.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED": n.inputs["Base Color"].default_value = (*srgb(hexc), 1)

# ---------------------------------------------------------------- props
def tree(x, y, s=1.0):
    cyl(f"trunk{x}_{y}", (x, y, 1.2 * s), 0.25 * s, 2.4 * s, mat("trunk", "#5a3b26"), verts=8)
    g = mat("leaf", "#2f7d3a", 0.8)
    for dx, dy, dz, r in ((0, 0, 3.2, 1.5), (0.8, 0.3, 2.7, 1.0), (-0.7, -0.2, 2.8, 1.1), (0.1, -0.5, 3.9, 1.0)):
        o = sphere(f"leaf{x}_{y}_{dx}", (x + dx * s, y + dy * s, dz * s), (r * s, r * s, r * 0.9 * s), g, seg=8)
        bpy.ops.object.shade_flat()

def lamp(x, y, facing=1):
    pole = mat("pole", "#2b2d36", 0.4, metal=0.6)
    cyl(f"lpole{x}", (x, y, 2.6), 0.1, 5.2, pole, verts=8)
    cube(f"larm{x}", (x - 0.6 * facing, y, 5.15), (1.3, 0.14, 0.14), pole, 0.02)
    cube(f"lbulb{x}", (x - 1.15 * facing, y, 4.98), (0.45, 0.3, 0.18), mat("bulb", "#ffd9a0", 0.3, 18), 0.03)
    point(f"lamp{x}_{y}", (x - 1.15 * facing, y, 4.7), "#ffc27a", 1800, 0.4)

def house(x, y, wall, roof, lit=True, door="#8a2d2d"):
    cube(f"hw{x}", (x, y, 2.6), (7, 6, 5.2), mat(f"hw{wall}", wall, 0.7), 0.08)
    for i in range(4):
        cube(f"hsid{x}_{i}", (x, y - 3.02, 0.6 + i * 1.2), (7.02, 0.05, 0.12), mat("siding", "#000000", 0.9), 0)  # siding lines
    rf = mat(f"hr{roof}", roof, 0.8)
    for i in range(5):
        cube(f"hrf{x}_{i}", (x, y, 5.4 + i * 0.45), (7.8 - i * 1.5, 6.6, 0.5), rf, 0.05)
    win = mat("winlit", "#ffd27a", 0.4, 6.0, "#ffbf5e") if lit else mat("windark", "#20284a", 0.2)
    for wx in (-2, 2):
        cube(f"hwin{x}_{wx}", (x + wx, y - 3.0, 3.4), (1.4, 0.1, 1.3), win, 0.02)
        cube(f"hwf{x}_{wx}", (x + wx, y - 3.06, 3.4), (1.6, 0.04, 1.5), mat("trim", "#f4f1e8"), 0.02)
    cube(f"hdoor{x}", (x, y - 3.02, 1.2), (1.2, 0.1, 2.4), mat(f"door{door}", door), 0.03)
    cube(f"hstep{x}", (x, y - 3.5, 0.15), (2, 1, 0.3), mat("step", "#9a9a9a"), 0.03)
    # picket fence
    fm = mat("fence", "#f1efe8", 0.6)
    for fx in range(-3, 4):
        if fx == 0: continue
        cube(f"pk{x}_{fx}", (x + fx * 1.0, y - 5.5, 0.6), (0.22, 0.12, 1.2), fm, 0.03)
    cube(f"pkr{x}", (x, y - 5.5, 0.8), (7, 0.08, 0.14), fm, 0.02)

def build_town():
    grass, road, side = mat("grass", "#3f8a3a", 0.9), mat("road", "#3a3d47", 0.85), mat("side", "#8d8f97", 0.8)
    cube("grass", (0, 20, -0.06), (300, 140, 0.1), grass, 0)
    cube("road", (0, 0, 0.0), (300, 8, 0.04), road, 0)
    for sy in (-5.3, 5.3): cube(f"sidewalk{sy}", (0, sy, 0.08), (300, 2.4, 0.18), side, 0.02)
    ym = mat("roadline", "#e8c64a", 0.6)
    for x in range(-120, 121, 5): cube(f"ln{x}", (x, 0, 0.03), (2.4, 0.2, 0.02), ym, 0)
    rnd = random.Random(4)
    cols = ["#5b7fd1", "#e3a24b", "#d0638f", "#6bb7a3", "#c9c4e9", "#e07a52", "#8fb3d9"]
    for i, x in enumerate(range(-60, 61, 12)):
        if abs(x) < 8: continue
        house(x, 13, cols[i % len(cols)], "#4a3328" if i % 2 else "#3c4660", lit=rnd.random() > 0.35)
        house(x + 6, -13, cols[(i + 3) % len(cols)], "#3a3040", lit=rnd.random() > 0.5)
        o = bpy.context.scene.objects
    for x in range(-58, 61, 12):
        if abs(x + 4) > 7: tree(x + 4, 9.5, 0.9)
        if abs(x - 2) > 9: tree(x - 2, -9.5, 0.8)
    for x in range(-48, 49, 16):
        lamp(x, 6.8, 1); lamp(x + 8, -6.8, -1)
    # town hall + tall clock tower at the end of the street (x=0, y=34)
    brick, white = mat("brick", "#a8433a", 0.75), mat("white", "#efece3", 0.5)
    cube("hall", (0, 36, 4), (18, 8, 8), brick, 0.1)
    cube("hallroof", (0, 36, 8.4), (19, 8.8, 0.8), white, 0.06)
    for x in (-6, -2, 2, 6): cyl(f"col{x}", (x, 31.6, 3.5), 0.45, 7, white)
    cube("tower", (0, 36, 15), (6, 6, 14), brick, 0.1)
    cube("towercap", (0, 36, 22.4), (6.8, 6.8, 0.8), white, 0.05)
    for i in range(4): cube(f"spire{i}", (0, 36, 23.4 + i * 0.9), (5 - i * 1.3, 5 - i * 1.3, 0.9), mat("spire", "#2e3a5c", 0.6), 0.04)
    face = cyl("clockface", (0, 32.9, 17.5), 2.4, 0.2, mat("clockface", "#fff3cf", 0.4, 4.0, "#ffe7a8"), rot=(math.pi / 2, 0, 0), verts=48)
    cyl("clockrim", (0, 32.95, 17.5), 2.65, 0.15, white, rot=(math.pi / 2, 0, 0), verts=48)
    piv = empty("clockpivot", (0, 32.7, 17.5))
    hk = mat("hands", "#1a1a1a", 0.3)
    hh = empty("hourhand", (0, 0, 0), piv); cube("hourbar", (0, 0, 0.75), (0.22, 0.06, 1.5), hk, 0, hh)
    mh = empty("minhand", (0, -0.05, 0), piv); cube("minbar", (0, 0, 1.05), (0.14, 0.06, 2.1), hk, 0, mh)
    for i in range(12):
        a = i * math.pi / 6
        cube(f"tick{i}", (1.95 * math.sin(a), 32.78, 17.5 + 1.95 * math.cos(a)), (0.12, 0.05, 0.38), hk, 0, None, (0, a, 0))
    tw = cube("towerwindow", (0, 32.9, 21.0), (1.3, 0.1, 1.0), mat("towerwin", "#c58bff", 0.3, 0.0, "#b46bff"), 0.02)
    point("towerglow", (0, 32.0, 21.0), "#b46bff", 0, 0.5)
    point("hallglow", (0, 30.5, 4), "#ffd08a", 600, 1.0)
    # moon
    sphere("moon", (-60, 160, 75), (7, 7, 7), mat("moon", "#fff6d8", 0.5, 8))
    sun = bpy.data.lights.new("moonlight", "SUN"); sun.color = srgb("#8aa6ff"); sun.energy = 2.2; sun.angle = math.radians(3)
    so = bpy.data.objects.new("moonlight", sun); bpy.context.scene.collection.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(200))
    return {"hourhand": hh, "minhand": mh, "towerwin": tw}

def build_bedroom(ox=300):
    wall, floor = mat("bwall", "#2d3d7a", 0.8), mat("bfloor", "#6b4b33", 0.7)
    cube("bfloor", (ox, 0, -0.05), (16, 16, 0.1), floor, 0)
    cube("bwallback", (ox, 6, 4), (16, 0.3, 8), wall, 0); cube("bwallL", (ox - 7, 0, 4), (0.3, 16, 8), wall, 0)
    cube("bwallR", (ox + 7, 0, 4), (0.3, 16, 8), wall, 0)
    cube("rug", (ox, -1, 0.02), (6, 4, 0.03), mat("rug", "#2aa6a0", 0.9), 0)
    # bed
    cube("bedframe", (ox - 3.5, 3, 0.6), (4.5, 6, 1.2), mat("bedwood", "#5a3b26"), 0.06)
    cube("blanket", (ox - 3.5, 2.6, 1.3), (4.6, 4.6, 0.4), mat("blanket", "#3f6fd8", 0.9), 0.15)
    cube("pillow", (ox - 3.5, 5.2, 1.4), (3, 1.2, 0.5), mat("pillow", "#f2f2f2"), 0.2)
    # window with curtains (on right wall)
    cube("bwin", (ox + 6.84, 1.5, 4.2), (0.05, 3.2, 3.0), mat("nightwin", "#2b3b8f", 0.2, 1.5, "#3a4cb0"), 0)
    cur = mat("curtain", "#7b2f5c", 0.9)
    cube("curL", (ox + 6.6, -0.6, 4.2), (0.2, 1.2, 3.8), cur, 0.08); cube("curR", (ox + 6.6, 3.6, 4.2), (0.2, 1.2, 3.8), cur, 0.08)
    cube("desk", (ox + 3.5, 4.8, 1.2), (4, 1.8, 0.2), mat("desk", "#8a6a4a"), 0.03)
    for dx in (-1.8, 1.8): cube(f"dleg{dx}", (ox + 3.5 + dx, 4.8, 0.55), (0.2, 1.6, 1.1), mat("desk", "#8a6a4a"), 0)
    # alarm clock on nightstand
    cube("nightstand", (ox - 0.4, 5, 0.8), (1.4, 1.4, 1.6), mat("bedwood", "#5a3b26"), 0.05)
    ac = cube("alarmclock", (ox - 0.4, 4.9, 1.95), (0.9, 0.5, 0.7), mat("alarm", "#d23b3b", 0.4), 0.12)
    cube("alarmface", (ox - 0.4, 4.63, 1.95), (0.6, 0.04, 0.45), mat("alarmface", "#9dffb0", 0.3, 3.0), 0.02)
    point("bedlamp", (ox - 0.4, 3.5, 3.5), "#ffb36b", 120, 0.3)
    point("moonwin", (ox + 5.5, 1.5, 4.5), "#7f8fff", 250, 1.5)

def build_stairs(ox=500):
    stone = mat("stone", "#4b4560", 0.85)
    cyl("stair_core", (ox, 0, 15), 1.2, 30, stone)
    cyl("stair_wall", (ox, 0, 15), 6.5, 30, mat("towerin", "#3a2e4e", 0.9), verts=32)
    bpy.context.object.scale = (1, 1, 1)
    sol = bpy.context.object.modifiers.new("s", "SOLIDIFY"); sol.thickness = 0.4
    bpy.context.object.data.polygons.foreach_set("use_smooth", [False] * len(bpy.context.object.data.polygons))
    # remove caps so we can be inside: flip normals not needed for render
    st = mat("step2", "#6c6488", 0.8)
    for i in range(60):
        a = i * math.radians(18)
        cube(f"st{i}", (ox + 3.6 * math.cos(a), 3.6 * math.sin(a), 0.25 + i * 0.45), (4.6, 1.3, 0.25), st, 0.04, None, (0, 0, a))
    for i in range(0, 60, 8):
        a = i * math.radians(18)
        point(f"torch{i}", (ox + 5.6 * math.cos(a), 5.6 * math.sin(a), 2.5 + i * 0.45), "#b46bff", 180, 0.3)

def gear(name, loc, r, teeth, m_body, m_teeth, rot_axis="y", parent=None):
    g = empty(name, loc, parent)
    rot = (math.pi / 2, 0, 0) if rot_axis == "y" else (0, 0, 0)
    c = cyl(name + "_disc", (0, 0, 0), r, 0.6, m_body, rot=rot, parent=g, verts=40)
    cyl(name + "_hub", (0, -0.1, 0), r * 0.25, 0.9, m_teeth, rot=rot, parent=g, verts=16)
    for i in range(teeth):
        a = i * 2 * math.pi / teeth
        cube(f"{name}_t{i}", (math.sin(a) * (r + 0.3), 0, math.cos(a) * (r + 0.3)), (0.5, 0.5, 0.7), m_teeth, 0.04, g, (0, a, 0))
    for i in range(6):
        a = i * math.pi / 3
        cube(f"{name}_sp{i}", (math.sin(a) * r * 0.55, -0.32, math.cos(a) * r * 0.55), (0.25, 0.1, r * 0.8), m_teeth, 0.02, g, (0, a, 0))
    return g

def build_clockroom(ox=700):
    cube("cr_floor", (ox, 0, -0.1), (30, 30, 0.2), mat("crfloor", "#2a2238", 0.7), 0)
    cube("cr_back", (ox, 9, 10), (30, 0.4, 20), mat("crwall", "#241c33", 0.9), 0)
    cube("cr_L", (ox - 12, 0, 10), (0.4, 30, 20), mat("crwall", "#241c33", 0.9), 0)
    cube("cr_R", (ox + 12, 0, 10), (0.4, 30, 20), mat("crwall", "#241c33", 0.9), 0)
    # the clock face from inside (glowing, backwards)
    cyl("cr_face", (ox, 8.7, 11), 5, 0.2, mat("crface", "#fff1c4", 0.4, 2.5, "#ffe2a0"), rot=(math.pi / 2, 0, 0), verts=48)
    body, glow = mat("gearbody", "#3b2f57", 0.4, metal=0.7), mat("geartooth", "#b46bff", 0.3, 6.0, "#b46bff")
    gold = mat("gold", "#e2b23a", 0.25, metal=1.0)
    G = [gear("g1", (ox - 5, 6, 7), 3.2, 18, body, glow), gear("g2", (ox + 4.5, 6.5, 9), 2.4, 14, body, glow),
         gear("g3", (ox + 1, 7, 15), 1.8, 10, body, gold), gear("g4", (ox - 7.5, 7.5, 14), 2.0, 12, body, glow)]
    # pedestal + candle (Oddwick cameo) in the middle of the clockwork
    cyl("ped", (ox, 2, 1.5), 0.9, 3, mat("ped", "#4a3d66", 0.5, metal=0.4), verts=16)
    cyl("candle", (ox, 2, 3.75), 0.42, 1.5, mat("wax", "#f3e6c8", 0.6), verts=24)
    flame = sphere("flame", (ox, 2, 4.85), (0.22, 0.22, 0.42), mat("flame", "#ffb347", 0.3, 40, "#ff9a2e"))
    fl = point("flamelight", (ox, 1.6, 5.0), "#ff9a2e", 220, 0.2)
    cube("candle_eyeL", (ox - 0.14, 1.57, 3.95), (0.07, 0.02, 0.13), mat("eyeblack", "#141414", 0.25), 0)
    cube("candle_eyeR", (ox + 0.14, 1.57, 3.95), (0.07, 0.02, 0.13), mat("eyeblack", "#141414", 0.25), 0)
    # the golden key (big wind-up key) on the right
    key = empty("key", (ox + 5, 1, 4))
    cyl("key_shaft", (0, 0, 0), 0.25, 4, gold, rot=(0, math.pi / 2, 0), parent=key, verts=12)
    for sd in (-1, 1):
        cube(f"key_bow{sd}", (2.3, 0, 0.9 * sd), (0.4, 0.4, 1.6), gold, 0.15, key)
    cube("key_bowmid", (2.3, 0, 0), (0.4, 0.5, 0.6), gold, 0.1, key)
    point("cr_purple", (ox - 3, -2, 12), "#9b5bff", 2200, 2.0)
    point("cr_fill", (ox + 4, -6, 6), "#5a6bff", 600, 2.0)
    return {"gears": G, "flame": flame, "flamelight": fl, "key": key}

def cam_move(cam, tgt, f0, f1, p0, p1, t0, t1, lens0=None, lens1=None):
    cam.location = p0; tgt.location = t0; cam.keyframe_insert("location", frame=f0); tgt.keyframe_insert("location", frame=f0)
    cam.location = p1; tgt.location = t1; cam.keyframe_insert("location", frame=f1); tgt.keyframe_insert("location", frame=f1)
    if lens0:
        cam.data.lens = lens0; cam.data.keyframe_insert("lens", frame=f0)
        cam.data.lens = lens1 or lens0; cam.data.keyframe_insert("lens", frame=f1)


class Dog:
    def __init__(self, name="dog", col="#a8682f"):
        m, dk = mat(name + "_fur", col, 0.8), mat(name + "_dark", "#4a2a14", 0.8)
        self.root = empty(name)
        cube(name + "_body", (0, 0, 1.0), (0.9, 1.9, 0.8), m, 0.1, self.root)
        self.head = empty(name + "_neck", (0, -1.0, 1.4), self.root)
        cube(name + "_head", (0, -0.3, 0.2), (0.85, 0.8, 0.75), m, 0.12, self.head)
        cube(name + "_snout", (0, -0.85, 0.05), (0.5, 0.45, 0.38), m, 0.08, self.head)
        cube(name + "_nose", (0, -1.08, 0.18), (0.2, 0.06, 0.14), mat("eyeblack", "#141414", 0.25), 0.02, self.head)
        for sd in (-1, 1):
            cube(f"{name}_ear{sd}", (0.38 * sd, -0.2, 0.6), (0.18, 0.3, 0.4), dk, 0.04, self.head)
            sphere(f"{name}_eye{sd}", (0.2 * sd, -0.71, 0.35), (0.07, 0.03, 0.1), mat("eyeblack", "#141414", 0.25), self.head, 8)
        self.legs = []
        for i, (x, y) in enumerate(((-0.3, -0.7), (0.3, -0.7), (-0.3, 0.7), (0.3, 0.7))):
            h = empty(f"{name}_hip{i}", (x, y, 0.75), self.root)
            cube(f"{name}_leg{i}", (0, 0, -0.35), (0.28, 0.28, 0.7), m, 0.04, h); self.legs.append(h)
        self.tail = empty(name + "_tailp", (0, 0.95, 1.3), self.root)
        cube(name + "_tail", (0, 0.25, 0.25), (0.16, 0.16, 0.6), m, 0.04, self.tail, (math.radians(-40), 0, 0))
    def jump_pose(self, f=None, k=1.0):
        for i, h in enumerate(self.legs):
            h.rotation_euler = (math.radians((-60 if i < 2 else 60) * k), 0, 0)
            if f is not None: h.keyframe_insert("rotation_euler", frame=f)
