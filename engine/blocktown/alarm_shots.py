"""Shots for the 2026-11-21 long-form "In This Town, Nobody Owns an Alarm Clock" (Blocktown house style, 16:9).
python3.13 alarm_shots.py [sid ...] [--still]  -> /home/claude/work/<slug>/shots/<sid>/####.png (resumable; 12 fps, 768x432)"""
import sys, os, json, math, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alarm_base import *

vo = json.load(open(f"{W}/vo.json")); END = vo["total"] + 0.6
def LS(prefix):
    for l in vo["lines"]:
        if l["text"].startswith(prefix): return l["start"]
    raise KeyError(prefix)

dog = lib.Dog("dog"); dog.root.location = OFF
for o in [dog.root, *dog.root.children_recursive]: BASE[o.name] = (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent); OBJ.append(o)
frost = point("frost", (300.5, -2.5, 3.0), "#9fe8ff", 0, 0.5); BASE[frost.name] = (tuple(frost.location), tuple(frost.rotation_euler), tuple(frost.scale), frost.hide_render, frost.parent); OBJ.append(frost); LIGHTS[frost.name] = 0
ladder = empty("ladder", OFF)
for sx in (-0.6, 0.6): cube(f"ladder_s{sx}", (sx, 0, 0), (0.15, 0.15, 7.4), mat("ladder", "#c9a46a", 0.7), 0.02, ladder)
for k in range(9): cube(f"ladder_r{k}", (0, 0, -3.2 + k * 0.8), (1.2, 0.12, 0.12), mat("ladder", "#c9a46a", 0.7), 0.02, ladder)
for o in [ladder, *ladder.children]: BASE[o.name] = (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent); OBJ.append(o)
# glass pane for the window set (peas stick to it)
gm = mat("wglassm", "#cfefff", 0.05); gm.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 0.12
glass = cube("wglass", (WX, -0.12, 3.4), (3.0, 0.04, 3.0), gm, 0); glass.hide_render = True
stuck = [sphere(f"stuck{i}", OFF, (0.13, 0.06, 0.13), mat("pea", "#6fcf3a", 0.4, 0.4, "#6fcf3a"), seg=8) for i in range(60)]
for o in (glass, *stuck): BASE[o.name] = (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.hide_render, o.parent); OBJ.append(o)

def yaw_to(frm, to):
    return math.degrees(math.atan2(to[0] - frm[0], -(to[1] - frm[1])))
def head(c):
    return c.root.location.z + (2.66 * c.s + 0.52 * c.hs)
def CU(c, f0, f1, dist0=3.2, dist1=2.7, side=0.4, dz=0.0, lens=40, look=None):
    """gentle push-in close-up on a character's face (camera in front of where it looks)"""
    p = c.root.location; a = c.root.rotation_euler.z
    fx, fy = math.sin(a), -math.cos(a); sx, sy = math.cos(a), math.sin(a); hz = head(c) + dz
    cam_move(cam, tgt, f0, f1, (p.x + fx * dist0 + sx * side, p.y + fy * dist0 + sy * side, hz + 0.25), (p.x + fx * dist1 + sx * side * 0.6, p.y + fy * dist1 + sy * side * 0.6, hz + 0.2),
             (p.x, p.y, hz - 0.1), (p.x, p.y, hz - 0.05), lens, lens + 4)
def at(c, loc, look_at=None, yaw=None):
    c.place(loc, yaw if yaw is not None else (yaw_to(loc, look_at) if look_at else 0))
def winshot(c, N, face="neutral", col="#5b7fd1", m="dawn", push=True, cap_on=False, muff=False, wide=False):
    mood(m); wall(col); at(c, (WX, 1.3, 0.7), yaw=0); c.face(face); cap(c, cap_on); muffs(c, muff)
    hz = 0.7 + 2.66 * c.s + 0.52 * c.hs
    if wide: cam_move(cam, tgt, 1, N, (WX - 1.0, -9.5, 3.0), (WX - 0.5, -8.6, 3.1), (WX, 0, 3.3), (WX, 0, 3.4), 30, 32)
    else: cam_move(cam, tgt, 1, N, (WX + 0.6, -6.2, hz + 0.1), (WX + 0.3, -5.0, hz + 0.05), (WX, 1.3, hz - 0.15), (WX, 1.3, hz - 0.1), 34, 38)
def roof(N, x=-12, y=13, m="dawn", face="determined", aim=True, side=1, close=False):
    mood(m); P = ROOF(x, y); at(hero, P, yaw=0); hero.face(face)
    if aim: shooter_on(hero)
    else: hero.pose(armR=-20)
    hz = head(hero)
    if close: cam_move(cam, tgt, 1, N, (x + 2.3 * side, y - 3.2, hz + 0.2), (x + 1.9 * side, y - 2.7, hz + 0.1), (x, y, hz - 0.1), (x, y - 0.4, hz - 0.1), 34, 38)
    else: cam_move(cam, tgt, 1, N, (x + 6.5 * side, y - 10.5, 11.0), (x + 5.2 * side, y - 9.5, 11.3), (x, y, 8.4), (x - 0.3 * side, y - 0.5, 8.6), 30, 32)
def street(N, m="dawn", p0=(-20, -7, 3.0), p1=(-12, -7, 3.4), t0=(10, 6, 3.5), t1=(14, 6, 3.8), lens=24):
    mood(m); cam_move(cam, tgt, 1, N, p0, p1, t0, t1, lens, lens)
def stage_shot(N, key, col="blue", m="day", mayor_on=True, crowd_n=10, cam_y=10.0, face="happy", talk=True):
    mood(m); scr(key, col)
    if mayor_on:
        mayor.place((-4.6, 25.2, 1.4), 15); mayor.face(face); mayor.pose(armR=-140, armL=-20)
        if talk: mayor.talk(1, N - 2, 0.14, 3)
    for i, c in enumerate(crowd[:crowd_n]):
        at(c, (-8 + (i % 5) * 4.0 + (1.6 if i // 5 else 0), 18.5 - (i // 5) * 2.6, 0.06), (0, 28)); c.face("happy")
    cy = cam_y - 4 if crowd_n else cam_y
    cam_move(cam, tgt, 1, N, (1.5, cy, 6.2), (0.5, cy + 1.2, 6.3), (0, 27, 4.6), (0, 27, 4.8), 26, 28)
def bed(c, N, face="sleep", m="night", wallc="#2d3d7a", cap_on=True, zz=True, lens=30, close=False, muff=False):
    mood(m); lie(c, (296.5, 1.0, 1.75)); cap(c, cap_on); muffs(c, muff)
    if face == "sleep": sleep_face(c); c.talk(1, N, 0.1, 7)
    else: c.face(face)
    bpy.data.materials["bwall"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*lib.srgb(wallc), 1)
    for l in LAMPS: l.data.energy = 0
    bg.inputs["Strength"].default_value = 0.3; sun.data.energy = 0.2; sc.view_settings.exposure = 1.0; sc.objects["bedlamp"].data.energy = 500; fill.data.energy = 260
    if zz: zzz(1, N, (296.5, 3.6, 2.8))
    if close: cam_move(cam, tgt, 1, N, (295.2, -0.6, 3.6), (295.5, -0.1, 3.4), (296.5, 2.4, 1.9), (296.5, 2.4, 1.9), 34, 40)
    else: cam_move(cam, tgt, 1, N, (294.0, -3.5, 5.5), (294.6, -2.8, 5.0), (296.5, 2.2, 1.8), (296.5, 2.4, 1.9), lens, lens + 4)
def peas_at_window(f0, N, n=6, spread=1.0, stick=0):
    r = random.Random(f0)
    for i in range(n):
        fs = f0 + i * max(1, N // (n + 1)); tx = WX + r.uniform(-spread, spread); tz = 3.4 + r.uniform(-1.0, 1.0)
        pea(i, fs, fs + 4, (WX + r.uniform(-3, 3), -9, 1.0), (tx, -0.2, tz), 0.8, after=(tx, -0.25, tz) if i < stick else (tx + 0.3, -1.5, 0.2))
def stick_peas(n):
    show(glass); r = random.Random(4)
    for i in range(n): stuck[i].location = (WX + r.uniform(-1.4, 1.4), -0.17, 3.4 + r.uniform(-1.4, 1.4)); stuck[i].hide_render = False
def crowd_street(n=14, face="happy", y=-2.5, x0=-10, dx=1.7, yaw=0, f_walk=None, N=0):
    for i, c in enumerate(crowd[:n]):
        c.place((x0 + i * dx + (0.6 if i % 2 else 0), y + (i % 3) * 1.1, 0.06), yaw); c.face(face)
        if f_walk: c.walk(1 + i % 3, N)
def pig(loc, yaw=0, fat=1.0):
    pg.root.location = loc; pg.root.rotation_euler = (0, 0, math.radians(yaw)); pg.fat(fat)
def smell_path(f0, f1, p0, p1, wig=1.2, n=36):
    for i, s in enumerate(G["smell"][:n]):
        ph = i / n
        for k in range(0, 4):
            t = min(1.0, ph + k * 0.33); f = round(f0 + (f1 - f0) * k / 3)
            x = p0[0] + (p1[0] - p0[0]) * t; y = p0[1] + (p1[1] - p0[1]) * t
            s.location = (x, y + wig * math.sin(t * 9 + k), p0[2] + (p1[2] - p0[2]) * t + 0.5 * math.sin(t * 13)); s.scale = (0.3 + 0.3 * t,) * 3
            s.keyframe_insert("location", frame=f); s.keyframe_insert("scale", frame=f)

# ======================================================================== shots
# --- HOOK -------------------------------------------------------------------
def h01(N):   # dawn town wide, crane down to the hero on a roof aiming the pea shooter
    roof(N); cam_move(cam, tgt, 1, N, (-2, -16, 14), (-6, -6, 9.5), (-12, 13, 7.0), (-12, 13, 8.0), 24, 28)
def h02(N):   # pea flies, hits the baker's window; baker in window
    winshot(baker, N, "neutral", "#f2d9a8", cap_on=False); sleep_face(baker); show(glass); pea(0, 2, 7, (WX + 2, -9, 2.0), (WX + 0.3, -0.2, 3.6), 0.8, after=(WX + 0.6, -1.4, 0.2)); blink_open(baker, 8)
def h03(N):   # hero close-up on the roof: determined squint
    roof(N, close=True)
def h04(N):   # 300 windows: wide crane along the street, lights coming on
    street(N, "dawn", (-30, -6, 6), (-18, -6, 7), (0, 10, 4), (10, 10, 5), 22)
def h05(N):   # big screen: $5,000 ; mayor
    stage_shot(N, "prize", "green", "dawn", crowd_n=0, cam_y=14)
def h06(N):   # Mayor asleep, snoring with windows shaking (preview)
    bed(mayor, N, "sleep", wallc="#7a2f3a", close=True); mayor.mouth.scale = (1.2, 1, 4.0); shake(1, N, 0.04)
def h07(N):   # fat pigeon on a roof edge, eating a pea (preview)
    roof(N, aim=True, face="evil", close=False); pig((-11, 11.4, 7.45), -30, 1.35); pg.peck(1, N, 3)
    cam_move(cam, tgt, 1, N, (-8.6, 7.6, 8.6), (-9.0, 8.2, 8.5), (-11, 11.4, 7.9), (-11, 11.4, 7.9), 40, 46)
def h08(N):   # a sea of fluffy earmuffs: crowd asleep standing with muffs (preview)
    mood("dawn"); crowd_street(14, "neutral", -1, -11, 1.7)
    for c in crowd: muffs(c); sleep_face(c)
    cam_move(cam, tgt, 1, N, (-6, -9, 3.4), (-2, -9, 3.6), (0, 0, 2.6), (2, 0, 2.8), 30, 32)
def h09(N):   # the attic door, light behind (preview)
    mood("day"); cam_move(cam, tgt, 1, N, (AX, -8, 2.0), (AX, -6.5, 2.2), (AX, 4, 1.5), (AX, 4, 1.8), 24, 26)
    for o in G["clockmasters"]: pass

# --- THE JOB --------------------------------------------------------------------
def j01(N):   # Gus's retirement party on the stage, banner on screen
    stage_shot(N, "bye", "pink", "day", mayor_on=False, crowd_n=8); gus.place((1.5, 25.0, 1.4), 0); gus.face("happy"); gus.pose(armR=-150)
    cam_move(cam, tgt, 1, N, (1.0, 15, 4.0), (1.4, 17, 4.2), (1.5, 25, 3.8), (1.5, 25, 4.2), 30, 34)
def j02(N):   # Gus close: 94, waving
    stage_shot(N, "bye", "pink", "day", mayor_on=False, crowd_n=0); gus.place((1.5, 25.0, 1.4), 0); gus.face("happy"); gus.pose(armR=-150); gus.talk(1, N // 2, 0.12, 3); CU(gus, 1, N)
def j03(N):   # Gus asleep in a chair at the party, Zzz
    stage_shot(N, "bye", "pink", "day", mayor_on=False, crowd_n=6); gus.place((1.5, 25.0, 1.0), 0); gus.pose(head=18, armL=-30, armR=-30); sleep_face(gus); zzz(1, N, (2.2, 24.8, 5.0))
    cam_move(cam, tgt, 1, N, (3.8, 19.6, 3.6), (3.2, 20.4, 3.6), (1.5, 25, 3.2), (1.5, 25, 3.3), 32, 36)
def j04(N):   # guests leave, Gus still asleep, lights go down
    j03(N); mood("dusk")
    for c in crowd: c.place(OFF)
    cam_move(cam, tgt, 1, N, (-2, 16, 4.5), (-1, 15, 5.0), (1.5, 25, 3.0), (1.5, 25, 3.2), 26, 26)
    for c in crowd[:6]: c.walk(1, N)
def j05(N):   # Mayor on stage with sash: SUNRISE PARADE
    stage_shot(N, "sunrise", "pink", "day", crowd_n=10)
def j06(N):   # Mayor close
    stage_shot(N, "fri", "blue", "day", crowd_n=0); CU(mayor, 1, N, 3.6, 3.0, -0.5)
def j07(N):   # FRIDAY 6 AM on the screen, crowd gasps
    stage_shot(N, "fri", "blue", "day", crowd_n=10, cam_y=12, talk=False)
    for c in crowd[:10]: c.face("surprised")
def j08(N):   # $5,000 on the screen (green)
    stage_shot(N, "prize", "green", "day", crowd_n=10, cam_y=13)
    for c in crowd[:10]: c.face("shock")
def j09(N):   # Golden Pea Shooter held up by the Mayor
    stage_shot(N, "prize", "gold", "day", crowd_n=0); hold(G["gshooter"], mayor, 1, (0, -0.5, -1.2)); G["gshooter"].rotation_euler = (math.radians(90), 0, 0)
    sc.objects["gsh_glow"].data.energy = 80; CU(mayor, 1, N, 4.2, 3.4, 0.8, -0.5)
def j10(N):   # hero puts his hand up in the crowd
    mood("day"); scr("prize", "green"); crowd_street(10, "happy", 13.0, -8, 1.9, 180)
    at(hero, (0.4, 16.5, 0.06), yaw=180); hero.face("determined"); hero.pose(1, armR=-20); hero.pose(6, armR=-170)
    cam_move(cam, tgt, 1, N, (2.2, 22.5, 3.6), (1.8, 21.8, 3.5), (0.4, 15.5, 2.6), (0.4, 15.5, 2.8), 30, 34)
def j11(N):   # hero close: I'm eleven
    mood("day"); at(hero, (0.4, 15.5, 0.06), yaw=180); hero.face("determined"); hero.pose(armR=-170)
    p = hero.root.location; hz = head(hero); cam_move(cam, tgt, 1, N, (1.0, 18.6, hz + 0.3), (0.8, 18.0, hz + 0.2), (0.4, 15.5, hz), (0.4, 15.5, hz), 40, 44)
def j12(N):   # props: one pea shooter + a bag of peas on a kitchen table (hero's hands)
    mood("day"); at(hero, (300, 0.0, 0.0), yaw=0); hero.face("happy"); hold(G["shooter"], hero, 1, (0, -0.4, -1.1)); G["shooter"].rotation_euler = (math.radians(90), 0, 0)
    G["bag"].location = (301.6, -0.6, 0.0)
    cam_move(cam, tgt, 1, N, (301.8, -4.0, 3.0), (301.2, -3.4, 2.9), (300.6, 0, 2.0), (300.6, 0, 2.1), 30, 34)
def j13(N):   # Benny laughs, falls off his chair
    mood("day"); at(ben, (3.5, 16.5, 0.06), (0, 10)); ben.face("happy"); ben.talk(1, N, 0.18, 2)
    ben.pose(1, lean=0); ben.pose(N // 2, lean=-40, armL=-120, armR=-120); ben.root.location.z = 0.06; ben.root.keyframe_insert("location", frame=N // 2)
    ben.place((3.5, 16.9, -0.9), ben.root.rotation_euler.z and math.degrees(ben.root.rotation_euler.z), N - 1)
    cam_move(cam, tgt, 1, N, (5.5, 11.5, 2.8), (5.2, 12.2, 2.8), (3.5, 16.5, 2.2), (3.5, 16.7, 1.8), 30, 32); shake(N // 2, N // 2 + 3, 0.08)
def j14(N):   # Benny close: you can't even wake YOURSELF up
    mood("day"); at(ben, (3.5, 16.5, 0.06), (1.0, 10)); ben.face("evil"); ben.talk(1, N - 2, 0.14, 3); ben.pose(armR=-90); CU(ben, 1, N)
def j15(N):   # the town laughs (wide crowd)
    mood("day"); scr("prize", "green"); crowd_street(14, "happy", 15.5, -12, 1.8, 180)
    for i, c in enumerate(crowd[:14]): cheer(c, 1 + i % 3, N, i)
    mayor.place((-4.6, 25.2, 1.4), 15); mayor.face("happy"); mayor.talk(1, N, 0.18, 2)
    cam_move(cam, tgt, 1, N, (-3, 6.0, 4.2), (3, 6.0, 4.2), (0, 18, 3.0), (0, 18, 3.4), 22, 22)
def j16(N):   # the Mayor writes the hero's name (screen shows name: we reuse 'sunrise' screen pink + mayor points)
    stage_shot(N, "sunrise", "pink", "day", crowd_n=10, cam_y=13); mayor.pose(1, armR=-90, armL=-20)
def j17(N):   # hero in bed, late for school (alarm-less): sun already up, he sleeps
    bed(hero, N, "sleep", m="day", wallc="#2d3d7a", cap_on=True)
    bg.inputs["Strength"].default_value = 1.0; sc.objects["moonwin"].data.energy = 1200; sc.objects["moonwin"].data.color = lib.srgb("#fff0c8")
def j18(N):   # hero reading a book about knocker-ups at the desk (research)
    mood("night"); at(hero, (303.5, 2.8, 0.0), yaw=180); hero.face("surprised"); hero.pose(armR=-70, armL=-70, head=20)
    sc.objects["bedlamp"].data.energy = 600; bg.inputs["Strength"].default_value = 0.3
    cam_move(cam, tgt, 1, N, (305.5, 0.0, 4.4), (305.0, 0.4, 4.2), (303.5, 3.2, 2.6), (303.5, 3.2, 2.6), 30, 34)
# the history beat is a 2D card in post (old-Britain illustration from our own shapes); shots j19/j20 are town b-roll under it
def j19(N):   # dawn street, lamps (b-roll behind the history card)
    street(N, "dawn", (-40, -2, 2.5), (-30, -2, 2.8), (0, 2, 3.2), (6, 2, 3.4), 22)
def j20(N):
    street(N, "dawn", (20, -6, 5), (14, -6, 5.5), (-10, 10, 5), (-14, 10, 5.2), 26)
def j21(N):   # hero imagines $5,000: grin close-up
    mood("day"); at(hero, (0.4, 15.5, 0.06), yaw=180); hero.face("happy"); hero.pose(armR=-20)
    hz = head(hero); cam_move(cam, tgt, 1, N, (0.9, 18.0, hz + 0.2), (0.7, 17.6, hz + 0.15), (0.4, 15.5, hz), (0.4, 15.5, hz), 42, 48)

# --- DAY 1 ---------------------------------------------------------------------------
def d101(N):  # 5 AM: hero climbs onto the bakery roof (wide)
    roof(N, 12, face="determined", side=-1)
def d102(N):  # aim close
    roof(N, 12, close=True, side=-1)
def d103(N):  # pea flies to the bakery window (street view)
    roof(N, 12, side=-1); pea(0, 3, 9, (12, 12.4, 8.4), (10, 10.0, 3.4), 0.5, after=(10, 9.4, 0.2))
    cam_move(cam, tgt, 1, N, (4, -2, 4.0), (5, -2, 4.2), (11, 11, 5.0), (11, 11, 5.0), 26, 28)
def d104(N):  # baker wakes, angry, throws a croissant
    winshot(baker, N, "evil", "#f2d9a8"); baker.pose(1, armR=-10); baker.pose(N // 2, armR=-170); baker.pose(N - 2, armR=-60)
    G["croissant"].location = (WX + 0.5, 1.0, 4.4); G["croissant"].keyframe_insert("location", frame=N // 2)
    G["croissant"].location = (WX + 0.3, -6.0, 3.6); G["croissant"].keyframe_insert("location", frame=N - 1)
def d105(N):  # hero catches the croissant, bites (breakfast)
    roof(N, 12, face="happy", aim=False, close=True, side=-1); hold(G["croissant"], hero, 1, (0, -0.4, -1.05)); hero.pose(1, armR=-130); hero.talk(1, N, 0.12, 3)
def d106(N):  # Grandma in her window, eyes wide open (asleep)
    winshot(gran, N, "surprised", "#c9c4e9")
def d107(N):  # peas bounce off Grandma's window
    winshot(gran, N, "surprised", "#c9c4e9", wide=True); show(glass); peas_at_window(1, N, 9)
def d108(N):  # Grandma's eyes slide to look at the camera: she was awake
    winshot(gran, N, "evil", "#c9c4e9"); gran.talk(N // 2, N - 2, 0.1, 4)
def d109(N):  # the twins' window: one twin wakes
    mood("dawn"); wall("#6bb7a3"); at(tw1, (WX - 0.6, 1.3, 0.7), yaw=0); at(tw2, (WX + 0.6, 1.8, 0.7), yaw=0)
    sleep_face(tw2); cap(tw1); cap(tw2); blink_open(tw1, 4); tw1.face("surprised", 4)
    cam_move(cam, tgt, 1, N, (WX + 0.4, -6.5, 3.5), (WX + 0.2, -5.6, 3.5), (WX, 1.5, 3.3), (WX, 1.5, 3.3), 32, 36)
def d110(N):  # twin one sits on twin two
    mood("dawn"); wall("#6bb7a3"); cap(tw1); cap(tw2); at(tw2, (WX + 0.3, 1.8, 0.7), yaw=0); tw2.face("shock")
    tw1.place((WX - 1.2, 1.4, 0.7), 0, 1); tw1.place((WX + 0.3, 1.6, 2.2), 0, N // 2); tw1.face("happy"); tw1.pose(N // 2, legL=-80, legR=-80)
    cam_move(cam, tgt, 1, N, (WX - 0.3, -6.2, 3.6), (WX, -5.4, 3.6), (WX, 1.5, 3.5), (WX, 1.5, 3.5), 32, 36); shake(N // 2, N // 2 + 2, 0.08)
def d111(N):  # rooftop run: hero jumps between roofs (wide), lights turning on
    roof(N, -24, face="happy", aim=False); hero.run(1, N, 4)
    hero.place((-24, 13, 7.42), 90, 1); hero.place((-14, 13, 7.42), 90, N)
    cam_move(cam, tgt, 1, N, (-22, -2, 8), (-14, -2, 8.5), (-22, 13, 7.0), (-14, 13, 7.5), 28, 28)
def d112(N):  # counter montage: hero firing fast (close)
    roof(N, -36, close=True, side=1)
    for k in range(4): pea(k, 1 + k * (N // 4), 4 + k * (N // 4), (-36, 12.2, 9.8), (-36, 4, 6.0), 0.2)
def d113(N):  # Benny's house: window, Benny asleep behind (bedroom)
    bed(ben, N, "sleep", wallc="#2d3d7a")
def d114(N):  # peas: window like soup (outside)
    winshot(ben, N, "neutral", "#d0638f", wide=True, cap_on=True); sleep_face(ben); ben.talk(1, N, 0.1, 7); stick_peas(45); peas_at_window(1, N, 8, 1.2)
def d115(N):  # hero close: puffed cheeks blowing
    roof(N, -48, close=True, side=1, face="shock")
def d116(N):  # Benny still asleep, close (Zzz)
    bed(ben, N, "sleep", close=True)
def d117(N):  # big screen: DAY 1 299/300 (red)
    stage_shot(N, "d1", "red", "day", crowd_n=8, cam_y=13, face="evil")
def d118(N):  # STRIKE close on screen + Mayor
    stage_shot(N, "strike", "red", "day", crowd_n=0, cam_y=18, face="evil")
def d119(N):  # Benny shrugs: on purpose, to test me
    mood("day"); at(ben, (3.5, 16.5, 0.06), (1.0, 10)); ben.face("happy"); ben.talk(1, N - 2, 0.14, 3); ben.pose(1, armL=-40, armR=-40, armLs=40, armRs=40); CU(ben, 1, N)
def d120(N):  # hero deadpan close
    mood("day"); at(hero, (1.2, 13.5, 0.06), (3.5, 16.5)); hero.face("evil"); CU(hero, 1, N, 2.8, 2.4)

# --- DAY 2 ---------------------------------------------------------------------------
def d201(N):  # Day two: hero on roof with a BIG bag
    roof(N, 24, aim=False, face="happy"); G["bag"].location = (25.0, 12.6, 7.45); G["bag"].scale = (1.6, 1.6, 1.6)
def d202(N):  # the pigeon lands next to him
    roof(N, 24, aim=True, face="neutral"); pig((25.2, 12.4, 12), 20); pg.flap(1, N // 2, 2)
    pg.root.keyframe_insert("location", frame=1); pg.root.location = (25.2, 12.4, 7.45); pg.root.keyframe_insert("location", frame=N // 2)
    cam_move(cam, tgt, 1, N, (27.5, 8.6, 8.8), (27.0, 9.2, 8.7), (24.6, 12.6, 8.4), (24.8, 12.6, 8.3), 32, 36)
def d203(N):  # load... eat. (close, two-shot)
    roof(N, 24, aim=True, face="evil"); pig((24.9, 12.1, 7.45), 20); pg.peck(1, N, 3, 50)
    for k in range(3): pea(k, 2 + k * (N // 3), 4 + k * (N // 3), (24.4, 12.2, 8.6), (24.9, 11.7, 8.0), 0.1)
    cam_move(cam, tgt, 1, N, (26.2, 9.6, 8.9), (25.9, 10.0, 8.8), (24.6, 12.4, 8.3), (24.6, 12.4, 8.3), 36, 40)
def d204(N):  # pigeon getting rounder (close)
    roof(N, 24, aim=False); pig((24.9, 12.1, 7.45), 20); pg.fat(1.0, 1); pg.fat(1.6, N - 2); pg.peck(1, N, 4, 40)
    cam_move(cam, tgt, 1, N, (26.6, 8.6, 8.6), (26.3, 9.1, 8.5), (24.9, 12.1, 7.9), (24.9, 12.1, 7.9), 38, 44)
def d205(N):  # zero peas: hero shakes the empty bag
    roof(N, 24, aim=False, face="shock", close=True); hold(G["bag"], hero, 1, (0, -0.3, -1.3)); hero.pose(1, armR=-150); hero.pose(N // 3, armR=-110); hero.pose(2 * N // 3, armR=-150)
def d206(N):  # pigeon sleeping on the hero's windowsill (night)
    mood("night"); wall("#57b65a"); show(glass); pig((WX + 0.6, -0.55, 1.98), 0, 1.5); at(hero, (WX, 1.6, 0.7), yaw=0); sleep_face(hero); cap(hero)
    cam_move(cam, tgt, 1, N, (WX + 1.4, -4.2, 2.9), (WX + 1.1, -3.6, 2.8), (WX + 0.5, -0.5, 2.5), (WX + 0.5, -0.5, 2.5), 36, 40)
def d207(N):  # hero runs home (street) at dawn
    mood("dawn"); hero.place((-4, 2.0, 0.06), 90, 1); hero.place((-14, 2.0, 0.06), 90, N); hero.run(1, N, 4); hero.face("determined")
    cam_move(cam, tgt, 1, N, (-2, -5, 2.6), (-12, -5, 2.6), (-4, 2, 2.0), (-14, 2, 2.0), 30, 30)
def d208(N):  # Grandma's freezer: frozen peas (bag held up, frosty light)
    mood("night"); at(hero, (300, 0.0, 0.0), yaw=0); hero.face("happy"); hold(G["frozen"], hero, 1, (0, -0.3, -1.25)); hero.pose(1, armR=-120)
    frost.data.energy = 700
    cam_move(cam, tgt, 1, N, (300.8, -3.8, 3.2), (300.6, -3.2, 3.1), (300.3, 0, 2.6), (300.3, 0, 2.6), 34, 38)
def d209(N):  # frozen pea BONK on Benny's window
    winshot(ben, N, "shock", "#d0638f", cap_on=True); show(glass); sleep_face(ben); pea(0, 2, 5, (WX - 2, -9, 2.0), (WX + 0.2, -0.2, 3.8), 0.5, after=(WX + 1.5, -3, 0.4)); ben.face("shock", 6); shake(5, 8, 0.1)
def d210(N):  # Benny awake, grumpy close
    winshot(ben, N, "evil", "#d0638f", cap_on=True)
def d211(N):  # the Mayor's house: windows shaking (exterior wide)
    mood("dawn"); wall("#d0638f"); at(mayor, (WX, 4.5, 0.7), yaw=0); cap(mayor); sleep_face(mayor)
    cam_move(cam, tgt, 1, N, (WX - 2, -10, 2.6), (WX - 1.5, -9, 2.8), (WX, 0, 3.6), (WX, 0, 3.6), 24, 26); shake(1, N, 0.06)
def d212(N):  # the Mayor snoring in bed, mouth wide
    bed(mayor, N, "sleep", wallc="#7a2f3a"); mayor.mouth.scale = (1.4, 1, 4.0); shake(1, N, 0.05)
def d213(N):  # hero climbs up to the open window (exterior close)
    mood("dawn"); wall("#7a2f3a"); at(hero, (WX + 0.2, -1.4, -1.6), yaw=180); hero.face("determined"); hero.pose(1, armR=-170, armL=-150)
    hero.place((WX + 0.2, -1.4, -1.4), 180, 1); hero.place((WX + 0.2, -1.4, -0.3), 180, N)
    cam_move(cam, tgt, 1, N, (WX + 2.4, -4.6, 3.0), (WX + 2.0, -4.0, 3.2), (WX, -0.6, 2.4), (WX, -0.6, 2.8), 30, 34)
def d214(N):  # POV over the hero's shoulder: the Mayor's open mouth
    bed(mayor, N, "sleep", wallc="#7a2f3a", close=True); mayor.mouth.scale = (1.5, 1, 4.6)
def d215(N):  # the pea goes in (slow)
    bed(mayor, N, "sleep", wallc="#7a2f3a", close=True, zz=False); mayor.mouth.scale = (1.5, 1, 4.6)
    pea(0, 2, N - 3, (299.0, -1.5, 3.2), (296.5, 0.45, 2.1), 0.4, after=(296.5, 1.0, 1.9))
def d216(N):  # the Mayor sits straight up, coughing
    mood("night"); bpy.data.materials["bwall"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*lib.srgb("#7a2f3a"), 1)
    sc.objects["bedlamp"].data.energy = 600; bg.inputs["Strength"].default_value = 0.3; cap(mayor)
    mayor.root.location = (296.5, 1.0, 1.75); mayor.root.rotation_euler = (math.radians(-90), 0, 0); mayor.root.keyframe_insert("rotation_euler", frame=1)
    mayor.root.rotation_euler = (0, 0, 0); mayor.root.keyframe_insert("rotation_euler", frame=4); mayor.root.location = (296.5, 2.0, 0.6); mayor.root.keyframe_insert("location", frame=4)
    mayor.face("shock", 4); mayor.talk(4, N, 0.2, 2); shake(4, 7, 0.1)
    cam_move(cam, tgt, 1, N, (295.0, -3.0, 4.2), (295.3, -2.4, 4.1), (296.5, 2.0, 3.4), (296.5, 2.0, 3.4), 32, 36)
def d217(N):  # hero at the window: room service (close, smug)
    mood("dawn"); wall("#7a2f3a"); at(hero, (WX + 0.75, -0.7, 0.4), yaw=180); hero.face("happy"); hero.talk(1, N - 2, 0.12, 3)
    hz = head(hero); cam_move(cam, tgt, 1, N, (WX + 0.85, 2.2, hz + 0.1), (WX + 0.8, 1.7, hz + 0.1), (WX + 0.75, -0.7, hz), (WX + 0.75, -0.7, hz), 40, 44)
def d218(N):  # screen DAY 2 300/300 green, crowd cheers
    stage_shot(N, "d2", "green", "day", crowd_n=10, cam_y=12)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)

# --- DAY 3 ---------------------------------------------------------------------------
def d301(N):  # Mrs. Pickles reads the $5,000 poster, glasses glint
    mood("day"); scr("prize", "green"); at(pick, (2, 20, 0.06), yaw=180); pick.face("evil")
    hz = head(pick); cam_move(cam, tgt, 1, N, (1.2, 23.5, hz + 0.3), (1.6, 23.0, hz + 0.2), (2, 20, hz), (2, 20, hz), 34, 40)
def d302(N):  # Pickles trophies montage: she holds a giant pie / bingo (use plate)
    mood("day"); at(pick, (-2, 4, 0.06), (0, -4)); pick.face("happy"); hold(G["plate"], pick, 1, (0, -0.4, -1.1)); pick.pose(armR=-40)
    CU(pick, 1, N, 5.0, 4.4, 1.0, -0.3, 34)
def d303(N):  # Pickles in a staring contest with a dog (dog = Lib Dog)
    mood("day"); at(pick, (-2, 4, 0.06), (2, 4)); pick.face("evil")
    dog.root.location = (1.6, 4, 0); dog.root.rotation_euler = (0, 0, math.radians(-90))
    hz = head(pick); cam_move(cam, tgt, 1, N, (0, -1.5, 2.6), (0, -1.0, 2.6), (0, 4, 2.2), (0, 4, 2.2), 30, 34)
def d304(N):  # the net goes up over Main Street (wide)
    street(N, "dawn", (-20, -8, 11), (-12, -8, 12), (0, 4, 8), (4, 4, 8), 22); show(G["net"])
    G["net"].location = (0, 0, 2.0); G["net"].keyframe_insert("location", frame=1); G["net"].location = (0, 0, 8.5); G["net"].keyframe_insert("location", frame=N - 2)
def d305(N):  # hero fires, pea bounces off the net back into his face
    roof(N, -24, close=True, side=1); show(G["net"]); pea(0, 2, 6, (-24, 12.3, 9.8), (-24, 9, 8.6), 0.3)
    pea(1, 7, 10, (-24, 9, 8.6), (-24, 12.4, 9.9), 0.3, after=(-24, 12.6, 9.3)); hero.face("shock", 10); shake(10, 13, 0.08)
def d306(N):  # Ow (closer) + pigeon flapping happily
    roof(N, -24, close=True, side=-1, face="shock"); show(G["net"]); pig((-23.0, 12.4, 7.45), 220, 1.3); pg.flap(1, N, 2)
    pea(0, 2, 5, (-24, 9, 8.6), (-24, 12.4, 9.9), 0.3); shake(5, 7, 0.08)
def d307(N):  # Pickles under the net in her bathrobe with curlers
    mood("dawn"); show(G["net"]); at(pick, (2, 5.5, 0.1), (0, -4)); show(curlers); sc.objects["pk_robe"].hide_render = False; pick.face("evil"); pick.talk(1, N - 2, 0.14, 3)
    CU(pick, 1, N, 4.2, 3.4, 0.6, -0.3, 34)
def d308(N):  # pea lands in her curlers
    d307(N); pick.face("shock", N // 2); pea(0, N // 2 - 4, N // 2, (2, 5.5, 9.0), (2, 5.5, 4.6), 0.0, after=(2, 5.5, 4.5)); shake(N // 2, N // 2 + 2, 0.06)
def d309(N):  # hero goes UP: climbs a chimney (low angle)
    roof(N, 36, aim=False, face="determined"); hero.place((36 + 2.2, 13.6, 7.42), 0); hero.pose(1, armR=-170, armL=-20); hero.pose(N // 2, armR=-20, armL=-170); hero.pose(N, armR=-170, armL=-20)
    cam_move(cam, tgt, 1, N, (33, 3, 9.0), (33.5, 3.5, 9.5), (38, 14, 8.6), (38, 14, 9.2), 28, 30)
def d310(N):  # dropping a pea down a chimney (top shot)
    mood("dawn"); at(hero, (12.8, 13.2, 7.42), yaw=-60); hero.face("evil"); hero.pose(armR=-100)
    pea(0, N // 3, N - 2, (14.0, 14.0, 9.6), (14.2, 14.2, 7.0), 0.0)
    cam_move(cam, tgt, 1, N, (13.6, 8.0, 12.5), (13.8, 8.6, 12.2), (13.6, 13.8, 8.4), (13.6, 13.8, 8.4), 28, 32)
def d311(N):  # chimney montage: rooftops wide, hero hopping, sky turning pink
    roof(N, -48, aim=False, face="happy"); hero.run(1, N, 4); hero.place((-48, 13, 7.42), 90, 1); hero.place((-36, 13, 7.42), 90, N)
    cam_move(cam, tgt, 1, N, (-42, 30, 14), (-40, 28, 13), (-44, 13, 7.5), (-38, 13, 7.5), 26, 26); mood("sunrise")
def d312(N):  # legs wobbling (close on shoes)
    roof(N, 48, aim=False, face="shock"); hero.pose(1, legL=10, legR=-10); hero.pose(3, legL=-10, legR=10); hero.pose(5, legL=10, legR=-10); hero.pose(7, legL=-10, legR=10)
    cam_move(cam, tgt, 1, N, (49.6, 10.4, 8.6), (49.3, 10.8, 8.5), (48, 13, 8.2), (48, 13, 8.6), 32, 34)
def d313(N):  # Benny holds the ladder (not helping)
    mood("sunrise"); at(ben, (24.6, 9.6, 0.06), yaw=10); ben.face("evil"); ben.pose(armR=-150, armL=-150)
    ladder.location = (24.0, 10.4, 3.7); ladder.rotation_euler = (math.radians(-10), 0, 0)
    at(hero, (24.0, 11.0, 6.0), yaw=180); hero.face("happy")
    cam_move(cam, tgt, 1, N, (27.5, 3.8, 3.5), (27.0, 4.4, 3.8), (24.3, 10, 4.0), (24.3, 10, 4.3), 26, 28)
def d314(N):  # Benny close: I'm just holding this ladder
    mood("sunrise"); at(ben, (24.6, 9.6, 0.06), yaw=10); ben.face("happy"); ben.talk(1, N - 2, 0.14, 3); ben.pose(armR=-150, armL=-150); CU(ben, 1, N)
def d315(N):  # screen: DAY 3 300/300
    stage_shot(N, "d3", "green", "day", crowd_n=10, cam_y=12)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
def d316(N):  # Pickles glare close
    mood("day"); scr("d3", "green"); at(pick, (2, 20, 0.06), (0, 10)); pick.face("evil"); CU(pick, 1, N, 3.0, 2.5, -0.4)

# --- DAY 4 ---------------------------------------------------------------------------
def d401(N):  # easy morning: everybody stretching at windows (street wide, sunrise)
    mood("sunrise"); crowd_street(12, "happy", -2.5, -10, 1.9, 0)
    for i, c in enumerate(crowd[:12]): c.pose(1 + i % 3, armL=-170, armR=-170, armLs=15, armRs=15)
    cam_move(cam, tgt, 1, N, (0, -12, 3.0), (0, -11, 3.6), (0, 0, 2.6), (0, 0, 2.8), 24, 26)
def d402(N):  # Mayor thumbs-up at the window, chewing carefully
    winshot(mayor, N, "happy", "#7a2f3a", m="sunrise", cap_on=True); mayor.pose(1, armR=-150); mayor.talk(1, N, 0.08, 4)
def d403(N):  # dusk: the truck drives down Main Street
    mood("dusk"); show(G["truck"]); G["truck"].rotation_euler = (0, 0, math.radians(90))
    G["truck"].location = (-30, -2, 0); G["truck"].keyframe_insert("location", frame=1); G["truck"].location = (-4, -2, 0); G["truck"].keyframe_insert("location", frame=N)
    cam_move(cam, tgt, 1, N, (-8, -7.5, 2.4), (-4, -7.2, 2.6), (-20, -2, 2.2), (-6, -2, 2.2), 26, 28)
def d404(N):  # Pickles hands out earmuffs to the crowd
    mood("dusk"); show(G["truck"]); G["truck"].location = (-4, -2, 0); G["truck"].rotation_euler = (0, 0, math.radians(90))
    at(pick, (0.5, -4.4, 0.06), (2, 2)); pick.face("happy"); pick.pose(armR=-90); pick.talk(1, N - 2, 0.12, 3)
    crowd_street(6, "happy", 0.5, 1.5, 1.9, 200); muffs(crowd[0]); muffs(crowd[2])
    cam_move(cam, tgt, 1, N, (6, -9, 3.0), (5, -8.4, 3.2), (1.5, -2, 2.4), (1.5, -2, 2.4), 28, 30)
def d405(N):  # the box: SLEEP TIGHT love, Mrs. P (insert)
    mood("dusk"); G["box"].location = (1.5, -2.0, 0.06)
    cam_move(cam, tgt, 1, N, (1.6, -4.2, 1.6), (1.55, -3.7, 1.4), (1.5, -2, 0.6), (1.5, -2, 0.6), 34, 40)
def d406(N):  # Grandma puts on two pairs
    mood("dusk"); at(gran, (-3, -3, 0.06), (0, -8)); gran.face("happy"); muffs(gran, True); show(gran.muffs2, False)
    gran.muffs2.hide_render = True
    for o in gran.muffs2.children: o.hide_render = True
    for o in gran.muffs2.children:
        o.hide_render = True; o.keyframe_insert("hide_render", frame=1); o.hide_render = False; o.keyframe_insert("hide_render", frame=N // 2)
    CU(gran, 1, N, 3.4, 2.8)
def d407(N):  # hero awake in bed at night, eyes open (can't sleep)
    bed(hero, N, "surprised", wallc="#2d3d7a", zz=False, close=True)
def d408(N):  # night town with everyone in earmuffs asleep (windows dark), screen SUNRISE PARADE
    mood("night"); scr("sunrise", "pink"); cam_move(cam, tgt, 1, N, (2.5, 2, 3.0), (2.5, 6, 3.6), (0, 28, 5.0), (0, 28, 5.6), 26, 30)

# --- DAY 5 / PARADE ------------------------------------------------------------------
def p01(N):   # 4 AM, hero fires at the baker: nothing
    winshot(baker, N, "neutral", "#f2d9a8", muff=True); sleep_face(baker); show(glass); peas_at_window(1, N, 5)
def p02(N):   # 20 peas at Benny: nothing (bed, muffs)
    bed(ben, N, "sleep", muff=True, close=True)
def p03(N):   # wrapped like burritos: crowd asleep standing in pyjamas + muffs (wide)
    h08(N); mood("dawn")
def p04(N):   # screen: 0/300 red
    stage_shot(N, "zero", "red", "dawn", crowd_n=0, cam_y=14, face="shock", talk=False); muffs(mayor); sleep_face(mayor); cap(mayor)
def p05(N):   # hero on the curb, pigeon next to him (quiet)
    mood("dawn"); hero.place((-1.0, -4.6, -0.6), 0); hero.pose(legL=-85, legR=-85, armL=-40, armR=-40, head=10); hero.face("neutral")
    pig((0.4, -4.9, 0.3), 330, 1.3)
    cam_move(cam, tgt, 1, N, (-0.4, -9.5, 2.0), (-0.3, -8.8, 1.9), (-0.3, -4.6, 1.5), (-0.3, -4.6, 1.5), 32, 36)
def p06(N):   # smell: orange wisps from the bakery chimney, hero sniffs
    mood("dawn"); sc.objects["bkglow"].data.energy = 900; smell_path(1, N, (12, 10, 4.0), (0, -3, 3.0), 0.8)
    at(hero, (-0.5, -4.0, 0.06), (12, 10)); hero.face("surprised"); hero.pose(head=-10)
    cam_move(cam, tgt, 1, N, (-4, -10, 3.0), (-3.2, -9.2, 3.2), (4, 3, 3.0), (3, 2, 3.0), 26, 28)
def p07(N):   # baker in the bakery window, lit, awake, kneading (no muffs on his head; muffs round his neck)
    winshot(baker, N, "happy", "#f2d9a8"); baker.pose(1, armR=-70, armL=-70); baker.pose(3, armR=-90, armL=-60); baker.pose(5, armR=-70, armL=-70); baker.pose(7, armR=-90, armL=-60)
    G["wlamp"].data.energy = 900
def p08(N):   # idea close: hero's eyes go wide (light-bulb moment)
    mood("dawn"); at(hero, (-0.5, -4.0, 0.06), (12, 10)); hero.face("shock"); CU(hero, 1, N, 3.4, 2.9)
def p09(N):   # tray of cinnamon rolls (insert)
    winshot(baker, N, "happy", "#f2d9a8"); hold(G["plate"], baker, 1, (0, -0.6, -1.1)); baker.pose(armR=-95)
    for i, r in enumerate(G["rolls"][:5]): r.parent = G["plate"]; r.location = (-0.3 + (i % 3) * 0.3, 0, 0.12 + (i // 3) * 0.2)
def p10(N):   # baker: who's paying? hero: Golden Pea Shooter (two-shot, window)
    winshot(baker, N, "evil", "#f2d9a8", wide=True); baker.talk(1, N // 2, 0.14, 3); at(hero, (WX + 2.4, -2.4, 0.06), (WX, 1)); hero.face("happy")
def p11(N):   # dragging the giant fan into the middle of Main Street
    mood("dawn"); show(G["fan"]); G["fan"].rotation_euler = (0, 0, math.radians(200))
    G["fan"].location = (-12, -3, 0); G["fan"].keyframe_insert("location", frame=1); G["fan"].location = (-3, -2, 0); G["fan"].keyframe_insert("location", frame=N)
    hero.place((-10, -4.2, 0.06), 90, 1); hero.place((-1, -3.2, 0.06), 90, N); hero.walk(1, N, 8); hero.face("determined"); hero.pose(1, lean=-15, armL=-70, armR=-70)
    cam_move(cam, tgt, 1, N, (-4, -8.2, 3.0), (0, -8.0, 3.2), (-9, -3, 2.6), (-2, -2, 2.6), 24, 24)
def p12(N):   # FAN ON: blades spin, wind lines, smell blasts down the street
    mood("dawn"); show(G["fan"]); G["fan"].location = (-3, -2, 0); G["fan"].rotation_euler = (0, 0, math.radians(200))
    G["fanhub"].rotation_euler = (0, 0, 0); G["fanhub"].keyframe_insert("rotation_euler", frame=1); G["fanhub"].rotation_euler = (0, math.radians(360 * N / 4), 0); G["fanhub"].keyframe_insert("rotation_euler", frame=N)
    for fc in (G["fanhub"].animation_data.action.fcurves if hasattr(G["fanhub"].animation_data.action, "fcurves") else []):
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    smell_path(1, N, (9, 9, 4.0), (-30, -1, 3.0), 1.0)
    cam_move(cam, tgt, 1, N, (2, -10, 3.4), (1, -9, 3.6), (-3, -2, 4.0), (-4, -2, 4.2), 26, 28); shake(1, N, 0.03)
def p13(N):   # doors open, people come out in pyjamas, eyes closed, noses first (street)
    mood("sunrise"); smell_path(1, N, (9, 9, 4.0), (-30, -1, 3.0), 1.0)
    for i, c in enumerate(crowd[:12]):
        x = -26 + i * 4.2; y0 = 9.0 if i % 2 == 0 else -9.0
        c.place((x, y0, 0.06), 0 if y0 > 0 else 180, 1); c.place((x + 1.5, y0 * 0.45, 0.06), 0 if y0 > 0 else 180, N); c.walk(1 + i % 3, N); sleep_face(c); muffs(c); c.pose(1, head=-15, armL=-80, armR=-80)
    cam_move(cam, tgt, 1, N, (-34, 0.0, 3.8), (-26, 0.0, 4.0), (0, 0, 2.6), (4, 0, 2.6), 26, 26)
def p14(N):   # Benny floats out like a cartoon (feet off the ground, following the smell)
    mood("sunrise"); muffs(ben); cap(ben); sleep_face(ben); ben.talk(1, N, 0.12, 5)
    ben.place((-6, 6, 0.06), -20, 1); ben.place((-4, 0, 1.4), -50, N); ben.pose(1, legL=-20, legR=-30, armL=-80, armR=-80, head=-15)
    smell_path(1, N, (6, 4, 3.6), (-12, -1, 3.0), 0.6)
    cam_move(cam, tgt, 1, N, (-1, -6, 2.8), (-1.5, -5.5, 3.0), (-6, 6, 2.6), (-4, 0, 3.6), 28, 30)
def p15(N):   # Grandma marches out with both pairs on
    mood("sunrise"); muffs(gran); show(gran.muffs2); sleep_face(gran); gran.place((8, 6, 0.06), 20, 1); gran.place((6, 1, 0.06), 20, N); gran.walk(1, N, 8)
    cam_move(cam, tgt, 1, N, (4.5, -4, 3.0), (4.2, -3.4, 3.1), (7, 3, 3.0), (6, 1, 3.0), 32, 34)
def p16(N):   # even Mrs. Pickles, holding a plate
    mood("sunrise"); muffs(pick); show(curlers); sc.objects["pk_robe"].hide_render = False; sleep_face(pick); hold(G["plate"], pick, 1, (0, -0.4, -1.1)); pick.pose(armR=-90)
    pick.place((-10, 7, 0.06), -20, 1); pick.place((-8.6, 2.4, 0.06), -20, N); pick.walk(1, N, 8); CU(pick, 1, N, 5.0, 4.2, 0.8, -0.6, 32)
    cam_move(cam, tgt, 1, N, (-6.8, -2.6, 3.0), (-7.2, -2.0, 3.0), (-10, 7, 2.6), (-8.6, 2.4, 2.6), 30, 32)
def p17(N):   # the Mayor sleepwalks, snoring (muffs + cap)
    mood("sunrise"); muffs(mayor); cap(mayor); sleep_face(mayor); mayor.mouth.scale = (1.3, 1, 3.5); mayor.place((2, 6, 0.06), 10, 1); mayor.place((1.5, 1.5, 0.06), 10, N); mayor.walk(1, N, 9)
    mayor.pose(1, armL=-85, armR=-85)
    cam_move(cam, tgt, 1, N, (3.4, -3.2, 3.6), (3.0, -2.6, 3.6), (2, 5, 3.4), (1.5, 2, 3.4), 30, 32)
def p18(N):   # the parade crowd on the square, munching rolls; screen counting (298)
    mood("sunrise"); scr("c298", "gold"); stage_shot(N, "c298", "gold", "sunrise", crowd_n=10, cam_y=10, talk=True)
    for c in crowd[:10]: muffs(c); c.talk(1, N, 0.1, 3)
def p19(N):   # screen 299/300 freezes (red)
    stage_shot(N, "c299", "red", "sunrise", crowd_n=0, cam_y=17, face="shock", talk=False)
def p20(N):   # hero looks around: someone is missing
    mood("sunrise"); at(hero, (0.4, 15.5, 0.06), yaw=180); hero.face("scared"); hero.pose(1, headyaw=-30); hero.pose(N // 2, headyaw=30)
    CU(hero, 1, N, 2.8, 2.4)
# --- THE ATTIC -----------------------------------------------------------------------
def a01(N):   # OLD GUS. snap zoom on Gus's dark house (south row)
    mood("sunrise"); cam_move(cam, tgt, 1, N, (-13, 4, 3.0), (-15, -1, 3.4), (-18, -13, 4.6), (-18, -13, 4.8), 22, 30)
def a02(N):   # hero runs into the house / up the stairs (bedroom set stairs not built: hero runs across the attic door)
    mood("sunrise"); hero.place((-24, -6, 0.06), 90, 1); hero.place((-18, -9.4, 0.06), 60, N); hero.run(1, N, 4); hero.face("determined")
    cam_move(cam, tgt, 1, N, (-26, 2, 2.6), (-22, 1, 2.6), (-24, -6, 2.2), (-18, -9.4, 2.2), 28, 30)
def a03(N):   # attic: Gus by the round window, wide awake, pea shooter (from behind the hero)
    mood("day"); at(gus, (AX, 5.4, 0.05), yaw=180); gus.face("happy"); gus.pose(legL=-80, legR=-80); gus.root.location.z = -0.4
    shooter_on(gus, G["gusshooter"]); G["gusshooter"].rotation_euler = (0, 0, 0)
    at(hero, (AX + 2.2, -2.4, 0.05), yaw=170); hero.face("surprised")
    cam_move(cam, tgt, 1, N, (AX + 1.6, -6.5, 3.4), (AX + 1.3, -5.6, 3.3), (AX, 5, 2.6), (AX, 5, 2.6), 26, 28)
def a04(N):   # Gus's shooter aims out of the window at... (close over his shoulder)
    a03(N); cam_move(cam, tgt, 1, N, (AX - 1.0, 3.6, 3.2), (AX - 0.8, 4.0, 3.1), (AX, 7.8, 4.2), (AX, 7.8, 4.4), 30, 36)
def a05(N):   # ...MY bedroom window (outside view: the hero's window, pea shooter tip in front)
    winshot(hero, N, "neutral", "#57b65a", m="sunrise"); hero.root.location = OFF; show(glass)
    cam_move(cam, tgt, 1, N, (WX + 0.1, -9.5, 3.4), (WX + 0.05, -6.5, 3.4), (WX, 0, 3.4), (WX, 0, 3.4), 30, 46)
def a06(N):   # reveal: the whole attic full of alarm clocks (pull back, crane)
    mood("day"); at(gus, (AX, 5.4, -0.4), yaw=180); gus.pose(legL=-80, legR=-80); gus.face("happy")
    cam_move(cam, tgt, 1, N, (AX, -1.5, 2.2), (AX + 0.4, -7.5, 5.0), (AX, 3, 1.4), (AX, 2, 2.2), 26, 22)
def a07(N):   # clock piles close, slow track
    mood("day"); cam_move(cam, tgt, 1, N, (AX + 2.2, -4, 1.6), (AX + 2.2, 2, 1.6), (AX + 5.0, -3, 1.4), (AX + 5.0, 3, 1.4), 30, 30)
def a08(N):   # hero shocked close
    mood("day"); at(hero, (AX + 0.6, -2.8, 0.05), (AX, 5)); hero.face("shock"); CU(hero, 1, N, 2.7, 2.3)
def a09(N):   # Gus close: seventy years / that's business (smug, talking)
    mood("day"); at(gus, (AX, 4.6, 0.05), (AX, -3)); gus.face("happy"); gus.talk(1, N - 2, 0.12, 3); CU(gus, 1, N, 3.2, 2.7, -0.4)
def a10(N):   # hero: Gus, that's cheating (point)
    mood("day"); at(hero, (AX + 0.6, -2.8, 0.05), (AX, 5)); hero.face("evil"); hero.pose(armR=-90); hero.talk(1, N // 2, 0.12, 3); CU(hero, 1, N, 3.0, 2.6, 0.5)
def a11(N):   # Gus leans in: who has been waking YOU up?
    mood("day"); at(gus, (AX, 4.0, 0.05), (AX, -3)); gus.face("evil"); gus.pose(1, lean=5); gus.pose(N, lean=18); gus.talk(1, N - 2, 0.12, 3); CU(gus, 1, N, 3.2, 2.6, 0.2)
def a12(N):   # flashback: hero asleep, a pea taps his window, he wakes (cool morning)
    bed(hero, N, "sleep", m="dawn", close=False); hero.face("surprised", N - 4)
def a13(N):   # flashback: Gus on his roof at 4:30 with the shooter (blue)
    roof(N, -18, -13 + 0, face="happy"); hero.root.location = OFF; at(gus, ROOF(-18, -13), yaw=180); gus.face("happy"); shooter_on(gus, G["gusshooter"])
    hz = head(gus); cam_move(cam, tgt, 1, N, (-16.4, -9.6, hz + 0.4), (-16.8, -10.1, hz + 0.3), (-18, -13, hz), (-18, -13, hz), 32, 36)
def a14(N):   # hero close: realisation, small smile
    mood("day"); at(hero, (AX + 0.6, -2.8, 0.05), (AX, 5)); hero.face("happy"); CU(hero, 1, N, 2.5, 2.2)
# --- ENDING --------------------------------------------------------------------------
def e01(N):   # parade: Gus and the hero walk onto the square together, crowd cheers, sunrise
    mood("sunrise"); scr("c300", "gold"); gus.place((-1.2, 8, 0.06), 180, 1); gus.place((-1.2, 13, 0.06), 180, N); gus.walk(1, N, 10); gus.face("happy")
    hero.place((0.6, 8, 0.06), 180, 1); hero.place((0.6, 13, 0.06), 180, N); hero.walk(1, N, 8); hero.face("happy")
    crowd_street(14, "happy", 17.5, -12, 1.8, 180)
    for i, c in enumerate(crowd[:14]): cheer(c, 1 + i % 3, N, i); muffs(c, i % 3 == 0)
    cam_move(cam, tgt, 1, N, (1.6, 2, 3.2), (1.6, 4, 3.6), (0, 14, 3.0), (0, 20, 4.2), 26, 28)
def e02(N):   # screen 300/300 gold, confetti-like bunting
    stage_shot(N, "c300", "gold", "sunrise", crowd_n=10, cam_y=12)
    for i, c in enumerate(crowd[:10]): cheer(c, 1 + i % 3, N, i)
def e03(N):   # the Mayor hands the cheque + Golden Pea Shooter to the hero
    mood("sunrise"); scr("c300", "gold"); at(mayor, (-1.2, 22.6, 1.4), (0.8, 21.0)); mayor.face("happy"); hold(G["cheque"], mayor, 1, (0, -0.5, -1.1)); mayor.pose(armR=-90)
    at(hero, (0.8, 21.0, 1.4), (-1.2, 22.6)); hero.face("happy"); hold(G["gshooter"], hero, 0, (0, -0.4, -1.1)); G["gshooter"].rotation_euler = (math.radians(90), 0, 0); hero.pose(armL=-150)
    sc.objects["gsh_glow"].data.energy = 80
    cam_move(cam, tgt, 1, N, (-4.0, 17.2, 3.8), (-3.4, 17.8, 3.9), (0, 22, 3.4), (0, 22, 3.6), 28, 32)
def e04(N):   # Benny asleep in the front row, muffs on, Zzz
    mood("sunrise"); at(ben, (1.5, 18.0, 0.06), yaw=180); muffs(ben); cap(ben); sleep_face(ben); ben.pose(head=15); zzz(1, N, (1.8, 18.0, 3.8)); CU(ben, 1, N, 3.6, 3.0, 0.5)
def e05(N):   # the pigeon eats the leftover rolls (close)
    mood("sunrise"); pig((2.0, 20.0, 1.45), 160, 1.6); pg.peck(1, N, 3, 45)
    for i, r in enumerate(G["rolls"][:6]): r.location = (1.4 + (i % 3) * 0.6, 19.4 + (i // 3) * 0.5, 1.5)
    cam_move(cam, tgt, 1, N, (3.2, 16.8, 2.6), (3.0, 17.3, 2.5), (2.0, 19.8, 1.8), (2.0, 19.8, 1.8), 36, 42)
def e06(N):   # Gus hands the hero one alarm clock
    mood("sunrise"); at(gus, (-0.8, 14.0, 0.06), (1.0, 13.0)); gus.face("happy"); gus.talk(1, N - 3, 0.12, 3); gus.pose(armR=-80)
    hold(G["giftclock"], gus, 1, (0, -0.4, -1.4)); at(hero, (1.0, 13.0, 0.06), (-0.8, 14.0)); hero.face("surprised")
    cam_move(cam, tgt, 1, N, (-1.8, 9.0, 3.4), (-1.5, 9.6, 3.3), (0.1, 13.5, 2.6), (0.1, 13.5, 2.6), 32, 36)
def e07(N):   # the alarm clock (close insert)
    mood("sunrise"); at(hero, (1.0, 13.0, 0.06), yaw=0); hero.face("happy"); hold(G["giftclock"], hero, 1, (0, -0.4, -1.4)); hero.pose(armR=-90)
    cam_move(cam, tgt, 1, N, (1.6, 9.8, 2.7), (1.5, 10.3, 2.6), (1.4, 12.6, 2.4), (1.4, 12.6, 2.4), 40, 48)
def e08(N):   # hero in bed, the alarm clock on the nightstand, sunshine, snoring (callback)
    bed(hero, N, "sleep", m="day", close=False); sc.objects["alarmclock"].hide_render = False; sc.objects["alarmface"].hide_render = False
    bg.inputs["Strength"].default_value = 1.0; sc.objects["moonwin"].data.energy = 1200; sc.objects["moonwin"].data.color = lib.srgb("#fff0c8")
def e09(N):   # last shot: the pea taps... Gus on his roof again? No: the pigeon on the hero's windowsill with a pea in its beak (button)
    winshot(hero, N, "neutral", "#57b65a", m="sunrise", cap_on=True); sleep_face(hero); show(glass); pig((WX + 0.6, -0.55, 1.98), 0, 1.4); pg.bob(1, N, 5)
    cam_move(cam, tgt, 1, N, (WX + 1.6, -6.0, 3.2), (WX + 1.0, -4.6, 3.0), (WX + 0.2, 0, 2.9), (WX + 0.3, -0.4, 2.6), 30, 36)
def e10(N):   # wide closing crane over the town at sunrise (A/B candles in post)
    mood("sunrise"); scr("c300", "gold"); crowd_street(14, "happy", 17.5, -12, 1.8, 180)
    cam_move(cam, tgt, 1, N, (0, -4, 4), (0, -14, 16), (0, 20, 4), (0, 28, 8), 24, 22)

# ======================================================================== timeline (line prefix, offset s, shot)
T = [
 ("In this town, nobody owns", 0.0, h01), ("In this town, nobody owns", 2.3, h02), ("Three hundred people.", 0.0, h04), ("Three hundred people.", 2.4, h05),
 ("By Friday,", 0.0, h06), ("By Friday,", 1.6, h07), ("By Friday,", 3.3, h08), ("And I'd finally", 0.0, h03), ("And I'd finally", 2.4, h09),
 ("It started on Sunday.", 0.0, j01), ("It started on Sunday.", 2.3, j02), ("He fell asleep", 0.0, j03), ("He fell asleep", 2.4, j04),
 ("Then the Mayor climbed", 0.0, j05), ("Then the Mayor climbed", 2.4, j06), ("Then the Mayor climbed", 4.3, j07),
 ("Whoever wakes up", 0.0, j06), ("Whoever wakes up", 2.6, j08), ("Whoever wakes up", 4.2, j09),
 ("I put my hand up.", 0.0, j10), ("I put my hand up.", 1.6, j11), ("I put my hand up.", 3.2, j12),
 ("My best friend Benny", 0.0, j13), ("My best friend Benny", 2.4, j14), ("The whole town laughed.", 0.0, j15), ("The whole town laughed.", 2.6, j16),
 ("Which is fair.", 0.0, j17), ("Which is fair.", 2.4, j18), ("This was a real job", 0.0, j19), ("This was a real job", 3.6, j20),
 ("Each customer paid", 0.0, j20), ("Each customer paid", 2.6, j21),
 ("Day one.", 0.0, d101), ("Day one.", 2.2, d102), ("Day one.", 3.9, d103), ("He opened the window", 0.0, d104), ("He opened the window", 2.0, d105),
 ("Then Grandma.", 0.0, d106), ("Then Grandma.", 2.0, d107), ("Then Grandma.", 4.3, d108), ("House forty", 0.0, d109), ("House forty", 2.6, d110),
 ("Two hundred and ninety eight", 0.0, d111), ("Two hundred and ninety eight", 2.0, d112), ("Two hundred and ninety eight", 3.6, d113),
 ("I shot a pea. Nothing.", 0.0, d115), ("I shot a pea. Nothing.", 1.8, d114), ("I shot a pea. Nothing.", 4.0, d116),
 ("Benny slept until lunch.", 0.0, d116), ("Benny slept until lunch.", 1.6, d117), ("Benny slept until lunch.", 4.4, d118),
 ("And Benny?", 0.0, d119), ("And Benny?", 1.9, d120),
 ("Day two.", 0.0, d201), ("Day two.", 2.0, d202), ("A pigeon.", 0.0, d203), ("A pigeon.", 3.0, d204), ("By four fifty", 0.0, d205), ("By four fifty", 1.6, d204),
 ("It followed me home", 0.0, d206), ("So I ran home", 0.0, d207), ("So I ran home", 1.8, d208), ("So I ran home", 3.7, d209),
 ("Benny woke up in one shot.", 0.0, d210), ("Then I got to the Mayor's house.", 0.0, d211), ("Then I got to the Mayor's house.", 2.4, d212),
 ("I climbed up to his open window.", 0.0, d213), ("I climbed up to his open window.", 2.2, d214), ("I want to say I aimed.", 0.0, d215),
 ("He sat straight up", 0.0, d216), ("He sat straight up", 2.0, d217), ("He sat straight up", 3.6, d218),
 ("Day three.", 0.0, d301), ("Mrs. Pickles is undefeated", 0.0, d302), ("Mrs. Pickles is undefeated", 2.5, d303),
 ("And now she wanted my job.", 0.0, d316), ("And now she wanted my job.", 1.8, d304), ("And now she wanted my job.", 4.3, d305),
 ("Pea. Ow.", 0.0, d306), ("Pea. Ow.", 1.9, d305), ("Mrs. Pickles stood under the net", 0.0, d307), ("Mrs. Pickles stood under the net", 3.5, d308),
 ("So I went UP.", 0.0, d309), ("So I went UP.", 2.0, d310), ("Three hundred chimneys.", 0.0, d311), ("Three hundred chimneys.", 1.8, d312),
 ("Then Benny showed up", 0.0, d313), ("Then Benny showed up", 2.4, d314), ("But the screen said", 0.0, d315), ("But the screen said", 2.6, d316),
 ("Day four. Easy.", 0.0, d401), ("The Mayor gave me a thumbs up", 0.0, d402), ("Because that evening", 0.0, d403), ("Because that evening", 2.8, d404),
 ("The box said", 0.0, d405), ("The box said", 2.0, d406), ("That night, I couldn't", 0.0, d407), ("Tomorrow was the Sunrise", 0.0, d408), ("Tomorrow was the Sunrise", 2.6, h08),
 ("Day five.", 0.0, p01), ("Day five.", 2.6, p02), ("Day five.", 4.8, p03), ("Five fifteen.", 0.0, p04), ("I sat on the curb.", 0.0, p05),
 ("And then I smelled", 0.0, p06), ("And then I smelled", 2.6, p07), ("Nobody in this town can hear", 0.0, p08), ("Nobody in this town can hear", 1.8, p09),
 ("I asked him for three hundred", 0.0, p10), ("Then I dragged the giant fan", 0.0, p11), ("Then I dragged the giant fan", 3.4, p12),
 ("The smell went down", 0.0, p13), ("Benny floated out", 0.0, p14), ("Benny floated out", 2.0, p15), ("Benny floated out", 4.2, p16),
 ("Then the Mayor. Still snoring.", 0.0, p17), ("Six AM.", 0.0, p18), ("And the screen stopped.", 0.0, p19), ("And the screen stopped.", 2.2, p20),
 ("Old Gus.", 0.0, a01), ("I ran to his house.", 0.0, a02), ("I ran to his house.", 2.6, a03), ("Pointed at MY", 0.0, a05),
 ("And behind him", 0.0, a06), ("And behind him", 3.2, a07), ("Gus had been buying", 0.0, a08), ("Gus had been buying", 1.8, a09),
 ("I said: Gus, that's cheating.", 0.0, a10), ("I said: Gus, that's cheating.", 1.5, a09), ("Then he said: kid,", 0.0, a11),
 ("Remember? I can't even", 0.0, a12), ("Remember? I can't even", 2.6, a08), ("It was Gus. Every morning.", 0.0, a13), ("It was Gus. Every morning.", 2.4, a14),
 ("He walked to the parade", 0.0, e01), ("He walked to the parade", 2.4, e02), ("I got the job,", 0.0, e03), ("I got the job,", 3.0, e05),
 ("Benny got a front row seat.", 0.0, e04), ("And Gus gave me a present.", 0.0, e06), ("And Gus gave me a present.", 2.4, e07),
 ("So now I'm the only person", 0.0, e08), ("So now I'm the only person", 2.6, e09), ("Should I keep the job?", 0.0, e10),
]
TIMES = []
for i, (pre, off, fn) in enumerate(T):
    t0 = 0.0 if i == 0 else LS(pre) + off
    TIMES.append([f"s{i + 1:03d}", round(t0, 3), fn])
for i in range(len(TIMES)):
    TIMES[i].insert(2, TIMES[i + 1][1] if i + 1 < len(TIMES) else END)
for a, b in zip(TIMES, TIMES[1:]):
    assert b[1] > a[1] + 0.5, (a[0], b[0], a[1], b[1])
os.makedirs(W, exist_ok=True)
json.dump([(sid, t0, t1, fn.__name__) for sid, t0, t1, fn in TIMES], open(f"{W}/shots_timing.json", "w"), indent=0)

if __name__ == "__main__":
    only = [a for a in sys.argv[1:] if a.startswith("s") and a[1:].isdigit()]
    names = [a for a in sys.argv[1:] if not a.startswith("-") and not (a.startswith("s") and a[1:].isdigit())]
    for sid, t0, t1, fn in TIMES:
        if only and sid not in only: continue
        if names and fn.__name__ not in names: continue
        N = max(2, round((t1 - t0) * FPS)); d = f"{W}/shots/{sid}"
        if not PREV and os.path.exists(f"{d}/done"): continue
        reset(); fn(N)
        if PREV:
            os.makedirs(f"{W}/stills", exist_ok=True)
            sc.frame_set(max(1, int(N * 0.6))); sc.render.filepath = f"{W}/stills/{sid}_{fn.__name__}.png"; bpy.ops.render.render(write_still=True)
            continue
        os.makedirs(d, exist_ok=True)
        sc.frame_start, sc.frame_end = 1, N; sc.render.filepath = f"{d}/"
        t = time.time(); bpy.ops.render.render(animation=True)
        open(f"{d}/done", "w").write(str(N)); print(sid, fn.__name__, N, "frames", round(time.time() - t), "s", flush=True)
