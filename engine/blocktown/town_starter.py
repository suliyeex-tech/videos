"""Proof of concept: blocky toy-town frame rendered headless with bpy (Cycles CPU)."""
import bpy, math, sys

out = sys.argv[-1] if sys.argv[-1].endswith(".png") else "/home/claude/poc/town_poc.png"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, rgb, rough=0.6):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    return m

def cube(name, loc, size, m, bevel=0.06):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = name; o.scale = [s / 2 for s in size]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        bv = o.modifiers.new("b", "BEVEL"); bv.width = bevel; bv.segments = 3
    o.data.materials.append(m); return o

def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)

# ground, road, grass
cube("grass", (0, 0, -0.05), (60, 60, 0.1), mat("g", srgb("#6cc24a")), 0)
cube("road", (0, 2, 0.001), (60, 5, 0.02), mat("r", srgb("#44474f")), 0)
for x in range(-20, 21, 4):
    cube(f"line{x}", (x, 2, 0.02), (1.8, 0.2, 0.01), mat("y", srgb("#f2d14b")), 0)

# town hall (brick + white columns + clock)
brick, white = mat("brick", srgb("#b8473a")), mat("white", srgb("#f1efe8"))
cube("hall", (0, 12, 3), (10, 5, 6), brick)
cube("roof", (0, 12, 6.3), (10.6, 5.6, 0.6), white)
cube("tower", (0, 12, 8), (3, 3, 3.4), brick)
for x in (-3, -1, 1, 3):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=4.5, location=(x, 9.3, 2.25))
    bpy.context.object.data.materials.append(white)
bpy.ops.mesh.primitive_cylinder_add(radius=1.1, depth=0.2, location=(0, 10.45, 8.2), rotation=(math.pi/2, 0, 0))
bpy.context.object.data.materials.append(white)
for i, (l, a) in enumerate(((0.8, 0), (0.55, 100))):
    h = cube(f"hand{i}", (0, 10.33, 8.2), (0.09, 0.02, l), mat("k", (0.02, 0.02, 0.02)), 0)
    h.rotation_euler[1] = math.radians(a)

# houses
for x, c in ((-11, "#4f8fd6"), (11, "#e6a43a"), (-17, "#d65b8f")):
    cube(f"house{x}", (x, 10, 2), (5, 5, 4), mat(f"h{x}", srgb(c)))
    cube(f"hroof{x}", (x, 10, 4.4), (5.6, 5.6, 0.8), mat(f"hr{x}", srgb("#5a3a2a")))

# blocky character: cube head, block torso, arms, legs
skin, shirt, pants = mat("skin", srgb("#f3c89a")), mat("shirt", srgb("#7b3fe4")), mat("pants", srgb("#2c3e70"))
cx, cy = 0, -1.5
cube("legL", (cx - 0.28, cy, 0.6), (0.5, 0.5, 1.2), pants)
cube("legR", (cx + 0.28, cy, 0.6), (0.5, 0.5, 1.2), pants)
cube("torso", (cx, cy, 1.85), (1.15, 0.6, 1.3), shirt)
cube("armL", (cx - 0.82, cy, 1.9), (0.45, 0.5, 1.2), skin).rotation_euler[1] = math.radians(-12)
cube("armR", (cx + 0.82, cy, 2.05), (0.45, 0.5, 1.2), skin).rotation_euler[1] = math.radians(40)
cube("head", (cx, cy, 3.0), (0.95, 0.95, 0.95), skin, 0.15)
cube("hair", (cx, cy + 0.05, 3.5), (1.0, 1.0, 0.25), mat("hair", srgb("#3b2416")), 0.08)
black, wht = mat("eye", (0.01, 0.01, 0.01), 0.3), mat("ew", (1, 1, 1), 0.3)
for s in (-1, 1):
    cube(f"eyeW{s}", (cx + 0.2 * s, cy - 0.48, 3.08), (0.22, 0.02, 0.26), wht, 0)
    cube(f"eye{s}", (cx + 0.2 * s, cy - 0.49, 3.06), (0.11, 0.02, 0.14), black, 0)
cube("mouth", (cx, cy - 0.48, 2.78), (0.34, 0.02, 0.07), black, 0)

# light + sky + camera (low, slightly wide, close-up)
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), math.radians(10), math.radians(-35)))
bpy.context.object.data.energy = 3.5
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (*srgb("#8fc8ff"), 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
bpy.ops.object.camera_add(location=(1.2, -7.2, 2.6), rotation=(math.radians(88), 0, math.radians(9)))
sc.camera = bpy.context.object; sc.camera.data.lens = 32

sc.render.engine = "CYCLES"; sc.cycles.samples = 24; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 576, 1024
sc.view_settings.view_transform = "Standard"
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("wrote", out)
