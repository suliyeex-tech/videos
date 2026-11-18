import sys, time, bpy, math
sys.path.insert(0, "/home/claude/videos/engine/blocktown")
import lib
sc, cam, tgt = lib.setup()
town = lib.build_town(); lib.build_bedroom(); lib.build_clockroom()
leo = lib.Char("leo", top="#2f63d6", pants="#c9b48a", hair="#7a4524", hood=True)
max_ = lib.Char("max", top="#2f9a4a", pants="#3b3b55", hair="#e0702e", hair_style="flat", hood=True, extra="#256f37")
mayor = lib.Char("mayor", skin="#f0c29a", top="#22243a", pants="#22243a", hair="#6b6b6b", hair_style="flat", kid=False)
leo.place((-1.5, -3, 0.16), 15); leo.pose(armL=10, armR=-60, head=5); leo.face("surprised")
max_.place((1.8, -2, 0.16), -20); max_.pose(armL=-30, armR=40, legL=20, legR=-20); max_.face("frozen")
mayor.place((700, -1, 0), 0); mayor.face("evil")
cam.location = (0.5, -12, 3.2); tgt.location = (0, 4, 4.5)
which = sys.argv[-1]
if which == "clock":
    cam.location = (700, -9, 4.5); tgt.location = (700, 2, 5)
sc.render.filepath = f"/home/claude/work/look_{which}.png"
t = time.time(); bpy.ops.render.render(write_still=True); print("render s", round(time.time() - t, 1))
