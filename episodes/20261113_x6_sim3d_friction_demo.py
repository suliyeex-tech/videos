# TEMPLATE for the SIM3D format (whatif.sim style). Not published; copy it for real episodes.
import math, random
from kit import *
from sim3d import *

FORMAT = 'sim3d'
SLUG = '2026-11-13-demo-friction-vanished'
VOICE = 'hype'; CAPTION = 'serif'; MOOD = {'style': 'cinematic', 'root': 55.0}; PROGRESS = True; TICKS = True; ZOOM = 0.6; VIGNETTE = 0.25
LINES = [
 ("What if friction disappeared for five seconds?", 0.2),
 ("You're on Fifth Avenue. Rush hour. Two thousand people, three hundred cars.", 0.15),
 ("Zero. Everyone's next step just... slides.", 0.15),
 ("Walking is pushing the ground backwards. No grip, no push.", 0.15),
 ("Every car keeps rolling. Brakes, steering, useless.", 0.15),
 ("Shoelaces untie. Knots slip. Screws start backing out.", 0.2),
 ("And then... friction comes back. All at once.", 0.15),
 ("How many seconds would you survive? Comment below.", 0.6),
]
CAPS = [[], ["You're on Fifth Avenue.", "[2,000] people, [300] cars."], ["[Zero.]", "Everyone's next step slides."],
        ["Walking = pushing the ground back.", "No grip, no push."], ["Every car keeps rolling."], ["Shoelaces untie. Knots slip."], ["And then... it comes back.", "[All at once.]"], []]

C_WIDE = Cam((0, 140, -260), 0, -24, 62); C_LOW = Cam((-30, 14, -40), 18, -4, 66); C_HIGH = Cam((60, 220, 40), -25, -55, 62)

def world(img, t, cam, P, night=0.0):
    p = []; city_scene(p, t, P)
    render(img, cam, p, sky=(mix((200, 150, 90), (60, 30, 20), night), mix((240, 210, 170), (90, 60, 40), night)), fog=mix((235, 215, 190), (80, 60, 50), night), t=t)

def s1(img, t, d):
    world(img, t, lerp_cam(C_HIGH, C_WIDE, t / d), {})
    title(img, 'What if friction', 'disappeared for 5 seconds?', a=ramp(t, 0.1, 0.5), y=560)
def s2(img, t, d):
    world(img, t, lerp_cam(C_WIDE, C_LOW, t / d), {})
    hud(img, 'Friction', f'{100:.0f} %', 'Fifth Avenue, New York', a=ramp(t, 0, 0.3))
def s3(img, t, d):
    world(img, t, C_LOW, {'lift': 0.4 * ramp(t, 0.3, d), 'crowd': 90}); flash(img, t, 0, 0.2, WHITE, 0.6)
    hud(img, 'Friction', f'{100 * (1 - ramp(t, 0, 0.4)):.0f} %', 'Fifth Avenue, New York')
def s4(img, t, d):
    world(img, t, lerp_cam(C_LOW, C_WIDE, t / d * 0.5), {'lift': 0.6})
    countdown(img, t, 0, 5, 'Friction returns in', 6)
def s5(img, t, d):
    world(img, t * 2.5, Cam((14, 10, -30 + 30 * t), 0, -3, 70), {'lift': 0.6})
    countdown(img, t + 2.6, 0, 5, 'Friction returns in', 6)
def s6(img, t, d):
    world(img, t, lerp_cam(C_WIDE, C_HIGH, t / d), {'lift': 0.8})
    countdown(img, t + 5.0, 0, 5, 'Friction returns in', 6)
def s7(img, t, d):
    world(img, t, C_WIDE, {'lift': 0.8 * (1 - ramp(t, 1.2, 1.4))})
    if t > 1.2: flash(img, t, 1.2, 0.25, WHITE, 0.9)
    hud(img, 'Friction', f'{100 * ramp(t, 1.2, 1.3):.0f} %', 'Fifth Avenue, New York')
def s8(img, t, d):
    world(img, t, C_HIGH, {}, night=0.3); title(img, 'How long', 'would you last?', a=ramp(t, 0.1, 0.4), y=700)

def timeline(ls, dur):
    fs = [s1, s2, s3, s4, s5, s6, s7, s8]
    return [(0 if i == 0 else ls(i) - 0.05, f) for i, f in enumerate(fs)]
def SFX(ls, dur):
    return {'riser': ls(0), 'boom': [ls(2), ls(6) + 1.2], 'whoosh': [ls(4)], 'end': ls(7)}

POST = {'title': 'What If Friction Disappeared For 5 Seconds? #shorts', 'caption': 'DEMO', 'tags': '#whatif', 'source': 'Template only.'}
