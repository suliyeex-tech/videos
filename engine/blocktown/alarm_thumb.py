"""Thumbnail render for the alarm-clock long-form: big shocked blocky face + pea shooter in the alarm-clock attic. -> work/thumb/thumb_3d.png"""
import sys, os, math
sys.argv.append("--still")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alarm_shots import *
sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.cycles.samples = 32
reset(); mood("day")
at(hero, (AX + 1.2, 0.5, 0.05), yaw=-15); hero.face("shock"); shooter_on(hero); hero.pose(armR=-80, armL=-80)
at(gus, (AX - 2.4, 3.5, 0.05), yaw=20); gus.face("evil"); shooter_on(gus, G["gusshooter"])
pg.root.location = (AX + 3.3, -0.6, 2.1); pg.root.rotation_euler = (0, 0, math.radians(-30)); pg.fat(1.4)
for i, p in enumerate(G["peas"][:7]): p.location = (AX + 0.3 - i * 0.55, -1.5 - i * 0.2, 3.1 + 0.25 * math.sin(i)); p.scale = (0.16, 0.16, 0.16)
hz = head(hero); cam.location = (AX + 2.6, -3.2, hz + 0.3); tgt.location = (AX + 0.6, 1.0, hz - 0.2); cam.data.lens = 30
sc.frame_set(1); sc.render.filepath = "/home/claude/work/thumb/thumb_3d.png"; bpy.ops.render.render(write_still=True); print("thumb ok")
