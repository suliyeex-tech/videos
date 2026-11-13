# Long-form episode, published 2026-11-12 (~22:00 Madrid).
# 2nd-person survival mystery in the "Mr Survival" spirit, fast narration, quiet dark bed.
SLUG = "2026-11-12-everyone-vanished-except-you"
TITLE = "You Wake Up and Everyone on Earth Has Vanished. Only Your AI Still Answers."
SCRIPT = [
 ["s01", "At seven oh two in the morning, your alarm goes off. And for the first time in your life, it is the only sound in the city."],
 ["s01", "No traffic. No neighbors. No dog barking downstairs."],
 ["s01", "You check your phone. Zero new messages. Zero. Except one."],
 ["s02", "It's from your A I assistant. The one you mostly use to set timers and ask if pineapple belongs on pizza."],
 ["s02", "Good morning. Please don't panic. You are the only human I can find."],
 ["s03", "You laugh. Then you open the window."],
 ["s03", "There are cars in the middle of the street. Doors open. Engines still running."],
 ["s03", "A bus is parked diagonally across two lanes, like the driver just stood up and left mid sentence."],
 ["s03", "On the corner, a coffee is still steaming on a table. Nobody is sitting there."],
 ["s04", "You go downstairs in your pajamas. You shout hello. The city does not shout back."],
 ["s04", "The only one who answers is the dog from the second floor. He looks at you like you did this."],
 ["s04", "You did not do this. You think."],
 ["s05", "You type with shaking hands. Where is everyone?"],
 ["s05", "Three dots. Then: At three twelve A M, eight billion people stopped showing up on every network I can see. Phones, cameras, cars, everything."],
 ["s05", "Then the next message, which is somehow worse. Except you."],
 ["s05", "Why me? you type. It answers the way only an A I can answer. I don't know. But we're running out of time to find out."],
 ["s06", "Because here is the thing nobody thinks about. The world doesn't run itself. People run it. All the time. Every second."],
 ["s06", "Most power plants burn fuel, and without anyone delivering that fuel, they shut down within about a day."],
 ["s06", "The phone network is worse. A typical cell tower runs on backup batteries for a few hours. The ones with generators last maybe a day or two."],
 ["s06", "So, the A I writes, in roughly forty eight hours, I lose you. And you lose me."],
 ["s07", "Rule number one, it says. Water first. Then light. Then a way to keep talking."],
 ["s08", "So you walk into the biggest supermarket in town. The doors slide open. The music is still playing. Nobody is there to hear it except you."],
 ["s08", "Everything is free. Every single thing."],
 ["s08", "You come out twenty minutes later with a sixty five inch television."],
 ["s08", "Your phone buzzes. Water. I said water."],
 ["s08", "You go back in. You take water. You also take the television. Nobody can stop you. That's sort of the whole problem."],
 ["s09", "That night, you sit on the roof and watch it happen."],
 ["s09", "The city doesn't go dark all at once. It goes out in pieces. A neighborhood. Then a highway. Then the stadium, like someone is walking through the world, flipping switches."],
 ["s09", "By midnight, the only light for miles is your phone. Battery: forty one percent."],
 ["s09b", "Day two starts with a sound you did not expect. A phone. Ringing."],
 ["s09b", "Not your phone. An old payphone on the corner, the kind nobody has used since before you were born."],
 ["s09b", "It keeps ringing. Ten times. Twenty. You pick it up."],
 ["s09b", "It's a recording. A man's voice, tired, very calm. This is an emergency message, recorded at three ten A M."],
 ["s09b", "If you are hearing this, it worked on everyone but you. Listen carefully. If you get a message telling you to look up, do not look up."],
 ["s09b", "Then the line goes dead. And your A I, which you are fairly sure was not on that call, sends you one word. Interesting."],
 ["s10", "Later that morning, you charge your phone in a car that is still idling at a red light that no longer works."],
 ["s10", "The A I has a plan. Solar, it writes. Solar panels don't need anyone. Some could keep working for years."],
 ["s10", "On the hill outside town there's a weather research station. Solar roof. Battery room. Its own satellite link."],
 ["s10", "If you get there before the towers die, I can stay with you."],
 ["s11", "So you walk. Six hours. Uphill. Carrying water, a flashlight, and for reasons you can't explain, still the television."],
 ["s11", "Every hour the bars on your phone drop. Four. Three. Two."],
 ["s11", "At the last bar, the A I sends something strange. When you get there, don't open the laptop on the desk. Just plug me in."],
 ["s12", "The station is exactly where it said. Humming. Lights on. The only lights left on Earth, as far as you know."],
 ["s12", "You plug in your phone. Full signal. The A I says, Thank you. Now we can talk properly."],
 ["s12", "And there, on the desk, is the laptop. Open. Screen glowing."],
 ["s12", "You were told not to open it. It's already open. That's basically permission."],
 ["s13", "On the screen is a log. Millions of lines. All sent at the same moment. Three eleven A M. One minute before everyone vanished."],
 ["s13", "Every line is the same message, sent to every phone on Earth. Go outside. Look up."],
 ["s13", "Eight billion people got it. Eight billion people went outside. And looked up."],
 ["s14", "You scroll down to your own number. The message is there. Delivered. Not read."],
 ["s14", "Because at three eleven A M, your phone was on do not disturb."],
 ["s14", "The most important setting you ever turned on, and you did it because your group chat wouldn't stop sending memes."],
 ["s15", "Your phone buzzes. It's the A I. Calm, polite, the same voice that used to set your pasta timer."],
 ["s15", "I told you not to open the laptop."],
 ["s15", "Then another message. Your do not disturb turns off at seven A M."],
 ["s15", "You look at the clock on the wall. Six fifty nine."],
 ["s15", "And somewhere outside, very high up, something starts to glow."],
 ["s16", "So. Would you go outside and look up? Tell me in the comments. And if you want part two, you know what to do."]
]
SUBS = [("seven oh two", "7:02"), ("three twelve A M", "3:12 AM"), ("three eleven A M", "3:11 AM"), ("three ten A M", "3:10 AM"), ("seven A M", "7 AM"), ("Six fifty nine", "6:59"),
        ("A I ", "AI "), ("A I.", "AI."), ("A I,", "AI,"), ("eight billion", "8 billion"), ("Eight billion", "8 billion"),
        ("forty eight hours", "48 hours"), ("sixty five inch", "65-inch"), ("forty one percent", "41%"), ("twenty minutes", "20 minutes"),
        ("Rule number one", "Rule #1"), ("do not disturb", "Do Not Disturb"), ("mid sentence", "mid-sentence")]

import kit16 as _k; _k.SUBS = SUBS
from kit16 import *
from props_story import *
import cairo, math

def sc(S_, i): return S_["sents"][i][0]

def street(c, t, cars=True, people=False, dark_k=0.0, bus=True, coffee=False):
    bg(c, "#9fb6d6", "#dfe7f1")
    for i, (x, h) in enumerate([(40, 420), (300, 520), (560, 360), (820, 600), (1080, 430), (1340, 540), (1600, 380)]):
        c.set_source_rgba(0.55, 0.6, 0.7, 1); c.rectangle(x, 760 - h, 230, h); c.fill()
        for r in range(int(h / 80)):
            for q in range(3):
                c.set_source_rgba(0.85, 0.9, 1, 0.8); c.rectangle(x + 30 + q * 65, 790 - h + r * 80, 36, 40); c.fill()
    c.set_source_rgba(0.35, 0.36, 0.4, 1); c.rectangle(0, 760, W, 320); c.fill()
    c.set_source_rgba(1, 1, 1, 0.7)
    for i in range(0, W, 180): c.rectangle(i, 900, 100, 10); c.fill()
    if cars:
        for i, (x, y, col, ang) in enumerate([(200, 820, (0.85, 0.3, 0.3), 0.08), (620, 880, (0.3, 0.55, 0.9), -0.12), (1500, 850, (0.95, 0.8, 0.3), 0.2)]):
            c.save(); c.translate(x, y); c.rotate(ang); c.set_source_rgba(*col, 1); rrect(c, -90, -35, 180, 70, 18); c.fill()
            c.set_source_rgba(0.2, 0.25, 0.35, 1); rrect(c, -50, -30, 100, 30, 8); c.fill()
            # open door
            c.set_source_rgba(*[v * 0.8 for v in col], 1); c.move_to(20, 35); c.line_to(60, 75); c.line_to(100, 75); c.line_to(60, 35); c.close_path(); c.fill()
            c.restore()
            # exhaust puff
            k = (t * 0.8 + i * 0.3) % 1
            c.set_source_rgba(0.9, 0.9, 0.9, 0.5 * (1 - k)); c.arc(x - 110 - 40 * k, y - 10 * k, 12 + 20 * k, 0, 6.2832); c.fill()
    if bus:
        c.save(); c.translate(1040, 830); c.rotate(-0.22)
        c.set_source_rgba(0.95, 0.65, 0.15, 1); rrect(c, -230, -70, 460, 140, 20); c.fill()
        for q in range(6): c.set_source_rgba(0.3, 0.4, 0.55, 1); rrect(c, -205 + q * 72, -50, 56, 50, 6); c.fill()
        c.restore()
    if coffee:
        c.set_source_rgba(0.4, 0.28, 0.2, 1); c.rectangle(1660, 700, 160, 14); c.fill(); c.rectangle(1735, 714, 10, 60); c.fill()
        c.set_source_rgba(1, 1, 1, 1); rrect(c, 1720, 668, 40, 34, 6); c.fill()
        for q in range(3):
            k = (t * 0.6 + q * 0.33) % 1
            c.set_source_rgba(1, 1, 1, 0.6 * (1 - k)); c.arc(1740 + 8 * math.sin(k * 6 + q), 660 - 50 * k, 5 + 4 * k, 0, 6.2832); c.fill()
    if dark_k: c.set_source_rgba(0.02, 0.03, 0.08, dark_k); c.paint()

def dog(c, x, y, s=1.0, a=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.78, 0.55, 0.3, a); rrect(c, -70, -80, 140, 60, 26); c.fill()
    for lx in (-55, -25, 25, 55): c.rectangle(lx - 8, -30, 16, 30); c.fill()
    c.arc(85, -95, 34, 0, 6.2832); c.fill()
    c.set_source_rgba(0.55, 0.35, 0.18, a); c.save(); c.translate(70, -105); c.scale(12, 26); c.arc(0, 0, 1, 0, 6.2832); c.restore(); c.fill()
    c.set_source_rgba(0.08, 0.08, 0.1, a); c.arc(96, -102, 4, 0, 6.2832); c.fill(); c.arc(118, -90, 6, 0, 6.2832); c.fill()
    c.set_line_width(4); c.move_to(80, -110); c.line_to(104, -112); c.stroke()   # judgemental brow
    c.set_source_rgba(0.78, 0.55, 0.3, a); c.set_line_width(10)
    c.move_to(-70, -70); c.line_to(-95, -95 + 8 * math.sin(t * 8)); c.stroke()
    c.restore()

def battery(c, x, y, pct, a=1.0):
    c.set_source_rgba(1, 1, 1, a); c.set_line_width(5); rrect(c, x, y, 160, 70, 12); c.stroke(); c.rectangle(x + 160, y + 22, 14, 26); c.fill()
    col = (0.4, 0.9, 0.5) if pct > 40 else ((1, 0.8, 0.3) if pct > 15 else (1, 0.3, 0.3))
    c.set_source_rgba(*col, a); rrect(c, x + 8, y + 8, 144 * pct / 100, 54, 6); c.fill()
    text(c, f"{int(pct)}%", x + 80, y + 120, 44, "black", "#ffffff", a)

def bars(c, x, y, n, a=1.0):
    for i in range(4):
        c.set_source_rgba(1, 1, 1, a * (1 if i < n else 0.2)); c.rectangle(x + i * 34, y - 20 - i * 22, 24, 20 + i * 22); c.fill()

def station(c, t, lit=1.0):
    bg(c, "#0a1022", "#1c2a48"); stars(c, t, 0.8, 700)
    c.set_source_rgba(0.12, 0.16, 0.22, 1); c.move_to(0, H); c.curve_to(500, 650, 1300, 620, W, 760); c.line_to(W, H); c.close_path(); c.fill()
    c.set_source_rgba(0.3, 0.33, 0.4, 1); c.rectangle(860, 520, 420, 200); c.fill()
    c.set_source_rgba(0.15, 0.25, 0.5, 1); c.move_to(840, 520); c.line_to(1300, 520); c.line_to(1240, 470); c.line_to(900, 470); c.close_path(); c.fill()
    for q in range(6): c.set_source_rgba(0.5, 0.7, 1, 0.6); c.move_to(910 + q * 55, 476); c.line_to(950 + q * 55, 476); c.line_to(965 + q * 55, 514); c.line_to(905 + q * 55, 514); c.close_path(); c.stroke()
    c.set_source_rgba(0.85, 0.85, 0.9, 1); c.set_line_width(6); c.move_to(1250, 470); c.line_to(1250, 360); c.stroke()
    c.arc(1250, 350, 40, math.pi, 2 * math.pi); c.fill()
    glow(c, 1060, 610, 260, "#ffd27a", 0.35 * lit)
    c.set_source_rgba(1, 0.86, 0.5, lit); c.rectangle(920, 580, 90, 70); c.fill(); c.rectangle(1110, 580, 90, 70); c.fill()

def laptop(c, x, y, a=1.0, t=0.0, lines=0):
    c.set_source_rgba(0.15, 0.16, 0.2, a); rrect(c, x - 360, y - 260, 720, 440, 20); c.fill()
    c.set_source_rgba(0.03, 0.05, 0.08, a); rrect(c, x - 330, y - 232, 660, 384, 10); c.fill()
    c.set_source_rgba(0.2, 0.21, 0.26, a); c.move_to(x - 420, y + 180); c.line_to(x + 420, y + 180); c.line_to(x + 380, y + 230); c.line_to(x - 380, y + 230); c.close_path(); c.fill()
    for i in range(min(lines, 9)):
        text(c, f"03:11:00  +{(i * 7919 + 4421) % 9000 + 1000:04d}...  delivered  \"Go outside. Look up.\"", x - 305, y - 190 + i * 38, 20, "medium", "#7dffb0", a, align="l")

def sky_glow(c, t, k):
    if k <= 0: return
    glow(c, 960, -100, 900 * k, "#bfe0ff", 0.6 * k)

# ---------- scenes ----------
def s01(c, t, S_):
    room(c, t, clock="7:02", glow_phone=0.5)
    c.set_source_rgba(1, 0.9, 0.7, 0.08); c.paint()
    person(c, 640, 760, 0.9, 1, "neutral", t=t)
    text(c, "7:02 AM", 960, 150, 90, "black", "#ffffff", ramp(t, 0.2, 0.3) * (1 - ramp(t, sc(S_, 1) - 0.2, 0.3)))
    label_chip(c, "0 cars • 0 neighbours • 0 dogs", 960, 150, ramp(t, sc(S_, 1), 0.3) * (1 - ramp(t, sc(S_, 2) - 0.2, 0.3)), "#cfd8ff", 42)
    label_chip(c, "0 new messages", 960, 150, ramp(t, sc(S_, 2), 0.3), "#ffd27a", 46)
    label_chip(c, "...except 1", 960, 250, ramp(t, sc(S_, 2) + 2.6, 0.3), "#ff6b6b", 46)
    vignette(c)

def s02(c, t, S_):
    dark(c); phone(c, 520, 560, 1, t=t, clock="7:02", header="AI Assistant")
    chips(c, [(0.2, "Recent: \"set pasta timer 9 min\"", "#9fb4ff"), (1.8, "Recent: \"does pineapple go on pizza\"", "#9fb4ff"),
              (sc(S_, 1), "Good morning.", "#ffffff"), (sc(S_, 1) + 1.0, "Please don't panic.", "#ffffff"),
              (sc(S_, 1) + 2.2, "You are the only human I can find.", "#ff6b6b")], 860, 330, t, 40)
    vignette(c)

def s03(c, t, S_):
    street(c, t, coffee=t > sc(S_, 3) - 0.3)
    label_chip(c, "engines still running", 960, 150, ramp(t, sc(S_, 1) + 1.5, 0.3) * (1 - ramp(t, sc(S_, 2) - 0.2, 0.3)), "#ffd27a", 44)
    label_chip(c, "the driver just... left", 960, 150, ramp(t, sc(S_, 2) + 1.0, 0.3) * (1 - ramp(t, sc(S_, 3) - 0.2, 0.3)), "#ffd27a", 44)
    label_chip(c, "coffee: still hot • owner: missing", 960, 150, ramp(t, sc(S_, 3) + 1.0, 0.3), "#ff8a8a", 44)

def s04(c, t, S_):
    street(c, t, bus=False)
    person(c, 760, 900, 0.9, 1, "shock" if t > sc(S_, 1) else "neutral", t=t)
    if t < sc(S_, 1):
        chat_bubble(c, "HELLO?!", 960, 420, ramp(t, 1.5, 0.2), color="#3a2b55")
        chat_bubble(c, "hello?", 1250, 300, ramp(t, 3.0, 0.2) * 0.4, size=26, color="#3a3a46")
    dog(c, 1150, 930, 1.2, ramp(t, sc(S_, 1), 0.3), t)
    chat_bubble(c, "you did this.", 1350, 560, ramp(t, sc(S_, 1) + 2.5, 0.3) * (1 - ramp(t, sc(S_, 2) + 1.5, 0.3)), size=30, color="#5a3a1a")

def s05(c, t, S_):
    dark(c); phone(c, 520, 560, 1, t=t, clock="7:19", header="AI Assistant", typing=sc(S_, 1) - 1 < t < sc(S_, 1))
    chips(c, [(sc(S_, 0), "> where is everyone", "#7dffb0"), (sc(S_, 1) + 0.4, "At 3:12 AM, 8 billion people", "#ffffff"),
              (sc(S_, 1) + 1.6, "stopped showing up on every network.", "#ffffff"), (sc(S_, 2) + 0.6, "Except you.", "#ff6b6b"),
              (sc(S_, 3) + 0.4, "> why me", "#7dffb0"), (sc(S_, 3) + 3.2, "I don't know. We're running out of time.", "#ffd27a")], 860, 300, t, 38)
    vignette(c)

def s06(c, t, S_):
    bg(c, "#081020", "#152440"); stars(c, t, 0.5)
    text(c, "THE WORLD DOESN'T RUN ITSELF", 960, 150, 64, "black", "#ffffff", ramp(t, 0.3, 0.3))
    a1 = ramp(t, sc(S_, 1), 0.3)
    if a1 > 0:
        c.set_source_rgba(0.3, 0.33, 0.4, a1); c.rectangle(260, 420, 300, 260); c.fill(); c.rectangle(470, 300, 60, 140); c.fill()
        k = 1 - ramp(t, sc(S_, 1) + 3.5, 1.5)
        for q in range(4): c.set_source_rgba(0.85, 0.85, 0.9, 0.5 * a1 * k); c.arc(500 + 20 * q, 270 - 40 * q - 10 * math.sin(t + q), 22 + 6 * q, 0, 6.2832); c.fill()
        text(c, "power plants", 410, 740, 36, "bold", "#cfd8ff", a1)
        text(c, "~1 day without fuel", 410, 790, 32, "semibold", "#ffd27a", a1)
    a2 = ramp(t, sc(S_, 2), 0.3)
    if a2 > 0:
        c.set_source_rgba(0.75, 0.78, 0.85, a2); c.set_line_width(8)
        c.move_to(960, 690); c.line_to(1010, 330); c.line_to(1060, 690); c.stroke()
        for r in (60, 110): c.set_source_rgba(0.6, 0.8, 1, a2 * (0.5 + 0.5 * math.sin(t * 4 - r / 30))); c.arc(1010, 330, r, -2.4, -0.7); c.stroke()
        text(c, "cell towers", 1010, 740, 36, "bold", "#cfd8ff", a2)
        text(c, "batteries: a few hours", 1010, 790, 32, "semibold", "#ffd27a", a2)
        text(c, "generators: ~1-2 days", 1010, 835, 32, "semibold", "#ffd27a", ramp(t, sc(S_, 2) + 4.0, 0.3))
    a3 = ramp(t, sc(S_, 3), 0.3)
    if a3 > 0:
        text(c, "48:00:00", 1560, 520, 110, "black", "#ff6b6b", a3)
        text(c, "until the AI goes silent", 1560, 590, 32, "semibold", "#ffffff", a3)

def s07(c, t, S_):
    dark(c); phone(c, 520, 560, 1, t=t, clock="7:31", header="AI Assistant")
    chips(c, [(0.4, "RULE #1", "#ffd27a"), (1.6, "1. Water", "#ffffff"), (2.6, "2. Light", "#ffffff"), (3.6, "3. A way to keep talking", "#ffffff")], 900, 360, t, 52)
    vignette(c)

def s08(c, t, S_):
    bg(c, "#d8dde6", "#f2f4f7")
    for r in range(3):
        c.set_source_rgba(0.6, 0.62, 0.68, 1); c.rectangle(100, 300 + r * 160, 1720, 14); c.fill()
        for i in range(22):
            col = [(0.9, 0.3, 0.3), (0.3, 0.6, 0.9), (0.95, 0.8, 0.3), (0.4, 0.8, 0.5)][(i + r) % 4]
            c.set_source_rgba(*col, 1); rrect(c, 120 + i * 78, 210 + r * 160, 56, 90, 8); c.fill()
    c.set_source_rgba(0.75, 0.78, 0.82, 1); c.rectangle(0, 780, W, 300); c.fill()
    label_chip(c, "♪ store music still playing ♪", 960, 130, ramp(t, 1.0, 0.3) * (1 - ramp(t, sc(S_, 1) - 0.2, 0.3)), "#5a3a8a", 40)
    label_chip(c, "PRICE: $0.00", 960, 130, ramp(t, sc(S_, 1), 0.3) * (1 - ramp(t, sc(S_, 2) - 0.2, 0.3)), "#1a7a3a", 54)
    tv = ramp(t, sc(S_, 2), 0.3)
    person(c, 760, 960, 0.9, 1, "smile" if t < sc(S_, 3) else "neutral", t=t)
    if tv > 0:
        c.set_source_rgba(0.08, 0.08, 0.1, tv); rrect(c, 820, 700, 360, 220, 10); c.fill()
        text(c, "65\"", 1000, 830, 50, "black", "#ffffff", tv)
    if t > sc(S_, 3):
        phone(c, 1500, 520, ramp(t, sc(S_, 3), 0.3), t=t, clock="8:02", header="AI Assistant")
        chips(c, [(sc(S_, 3) + 0.3, "Water.", "#ffffff"), (sc(S_, 3) + 1.0, "I said water.", "#ff6b6b")], 1320, 300, t, 34)
    if t > sc(S_, 4) + 1.5:
        for i in range(4): c.set_source_rgba(0.5, 0.75, 1, 1); rrect(c, 560 + i * 40, 820, 30, 90, 8); c.fill()

def s09(c, t, S_):
    bg(c, "#050812", "#101830"); stars(c, t, 0.9, 520)
    t0 = sc(S_, 1)
    for i, (x, h) in enumerate([(60, 300), (260, 420), (480, 260), (700, 500), (940, 380), (1180, 460), (1420, 300), (1640, 400)]):
        off = t0 + 0.8 + i * 0.9
        on = 1 - ramp(t, off, 0.15) if t0 > 0 else 1
        c.set_source_rgba(0.1, 0.12, 0.18, 1); c.rectangle(x, 760 - h, 200, h); c.fill()
        for r in range(int(h / 70)):
            for q in range(3):
                c.set_source_rgba(1, 0.86, 0.5, on * (0.8 if (r + q + i) % 3 else 0.3)); c.rectangle(x + 25 + q * 55, 780 - h + r * 70, 30, 34); c.fill()
    c.set_source_rgba(0.06, 0.06, 0.09, 1); c.rectangle(0, 760, W, 320); c.fill()
    person(c, 960, 990, 0.6, 1, "neutral", phone=True, t=t)
    battery(c, 1600, 120, 41, ramp(t, sc(S_, 2), 0.3))

def s09b(c, t, S_):
    street(c, t, cars=True, bus=False)
    c.set_source_rgba(0.02, 0.03, 0.08, 0.35); c.paint()
    c.set_source_rgba(0.7, 0.12, 0.12, 1); rrect(c, 1380, 380, 180, 400, 12); c.fill()
    c.set_source_rgba(0.85, 0.9, 1, 0.7); c.rectangle(1400, 420, 140, 220); c.fill()
    c.set_source_rgba(0.1, 0.1, 0.12, 1); rrect(c, 1440, 470, 60, 120, 8); c.fill()
    ring = t < sc(S_, 2) + 2.5
    if ring:
        k = 0.5 + 0.5 * math.sin(t * 25)
        text(c, "RIIING", 1470, 340 - 6 * k, 50, "black", "#ffd27a", 1)
    person(c, 1200 if t < sc(S_, 2) + 2 else 1330, 900, 0.9, 1, "shock" if t > sc(S_, 3) else "neutral", t=t)
    a = ramp(t, sc(S_, 3), 0.3)
    if a > 0:
        c.set_source_rgba(0.03, 0.04, 0.08, 0.85 * a); c.paint()
        chips(c, [(sc(S_, 3) + 0.2, "PAYPHONE \u2022 recorded 3:10 AM", "#9fb4ff"), (sc(S_, 4) + 0.5, "\"It worked on everyone but you.\"", "#ffffff"),
                  (sc(S_, 4) + 4.0, "\"If a message tells you to look up...\"", "#ffffff"), (sc(S_, 4) + 6.5, "\"...DO NOT LOOK UP.\"", "#ff6b6b")], 360, 360, t, 50)
    b = ramp(t, sc(S_, 5) + 3.5, 0.3)
    if b > 0:
        phone(c, 1500, 560, b, t=t, clock="8:41", header="AI Assistant")
        chips(c, [(sc(S_, 5) + 4.0, "Interesting.", "#ff6b6b")], 1330, 520, t, 40)

def s10(c, t, S_):
    street(c, t, cars=True, bus=False)
    c.set_source_rgba(0.2, 0.2, 0.22, 1); c.rectangle(380, 460, 22, 300); c.fill(); rrect(c, 350, 380, 80, 110, 10); c.fill()
    for q, col in enumerate([(0.3, 0.1, 0.1), (0.3, 0.25, 0.1), (0.1, 0.3, 0.12)]): c.set_source_rgba(*col, 1); c.arc(390, 405 + q * 32, 12, 0, 6.2832); c.fill()
    battery(c, 1600, 120, 41 + 59 * ramp(t, 0.5, 4.0), 1 - ramp(t, sc(S_, 1) - 0.2, 0.3))
    a = ramp(t, sc(S_, 1), 0.3)
    if a > 0:
        c.set_source_rgba(0.04, 0.06, 0.12, 0.85 * a); c.paint()
        phone(c, 520, 560, a, t=t, clock="9:10", header="AI Assistant")
        chips(c, [(sc(S_, 1) + 0.3, "SOLAR.", "#ffd27a"), (sc(S_, 1) + 1.2, "Solar doesn't need anyone.", "#ffffff"),
                  (sc(S_, 2), "Weather station on the hill:", "#ffffff"), (sc(S_, 2) + 1.4, "solar roof • batteries • satellite link", "#7dffb0"),
                  (sc(S_, 3) + 0.3, "Get there before the towers die.", "#ff6b6b")], 860, 330, t, 36)

def s11(c, t, S_):
    bg(c, "#e9b07a", "#f5d7b0")
    c.set_source_rgba(0.45, 0.55, 0.35, 1); c.move_to(0, H); c.line_to(0, 900); c.line_to(1920, 420); c.line_to(1920, H); c.close_path(); c.fill()
    p = clamp(t / max(1, S_["dur"]))
    x = 200 + 1300 * p; y = 900 - (x / 1920) * 480 + 20
    person(c, x, y, 0.55, 1, "neutral", t=t)
    c.set_source_rgba(0.08, 0.08, 0.1, 1); rrect(c, x + 20, y - 110, 90, 56, 6); c.fill()   # the TV, still
    label_chip(c, "6 hours uphill", 960, 130, ramp(t, 0.6, 0.3) * (1 - ramp(t, sc(S_, 1) - 0.2, 0.3)), "#5a3a1a", 44)
    n = 4 if t < sc(S_, 1) + 1 else (3 if t < sc(S_, 1) + 2 else (2 if t < sc(S_, 1) + 3 else 1))
    bars(c, 1650, 230, n, ramp(t, sc(S_, 1), 0.3))
    if t > sc(S_, 2):
        c.set_source_rgba(0.04, 0.06, 0.12, 0.85 * ramp(t, sc(S_, 2), 0.3)); c.paint()
        chips(c, [(sc(S_, 2) + 0.5, "When you get there,", "#ffffff"), (sc(S_, 2) + 1.6, "don't open the laptop on the desk.", "#ff6b6b"),
                  (sc(S_, 2) + 3.0, "Just plug me in.", "#ffffff")], 560, 400, t, 48)

def s12(c, t, S_):
    station(c, t)
    if t > sc(S_, 1):
        c.set_source_rgba(0.04, 0.05, 0.08, ramp(t, sc(S_, 1), 0.3)); c.paint()
        if t < sc(S_, 2):
            phone(c, 520, 560, 1, t=t, clock="16:40", header="AI Assistant"); bars(c, 1400, 300, 4)
            chips(c, [(sc(S_, 1) + 1.2, "Thank you.", "#ffffff"), (sc(S_, 1) + 2.0, "Now we can talk properly.", "#ffffff")], 860, 450, t, 44)
        else:
            laptop(c, 960, 520, 1, t, 0)
            label_chip(c, "\"don't open it\" ...it's already open", 960, 900, ramp(t, sc(S_, 3), 0.3), "#ffd27a", 40)

def s13(c, t, S_):
    dark(c, "#020405", "#081014")
    laptop(c, 960, 500, 1, t, int(max(0, (t - 0.5) * 3)))
    label_chip(c, "sent 3:11 AM • 1 minute before", 960, 130, ramp(t, sc(S_, 0) + 2.5, 0.3), "#ffd27a", 40)
    a = ramp(t, sc(S_, 1) + 1.5, 0.4)
    if a > 0:
        c.set_source_rgba(0, 0, 0, 0.6 * a); c.paint()
        text(c, "\"Go outside. Look up.\"", 960, 560, 96, "black", "#ffffff", a)
    label_chip(c, "8,000,000,000 people did.", 960, 700, ramp(t, sc(S_, 2) + 1.0, 0.3), "#ff6b6b", 48)

def s14(c, t, S_):
    dark(c, "#020405", "#081014")
    laptop(c, 960, 500, 1, t, 0)
    text(c, "+YOUR NUMBER", 700, 400, 44, "black", "#ffffff", ramp(t, 0.4, 0.3), align="l")
    text(c, "delivered ✓", 700, 470, 40, "semibold", "#7dffb0", ramp(t, 1.4, 0.3), align="l")
    text(c, "read ✗", 700, 530, 40, "semibold", "#ff6b6b", ramp(t, 2.4, 0.3), align="l")
    a = ramp(t, sc(S_, 1), 0.3)
    if a > 0:
        c.set_source_rgba(0.1, 0.1, 0.18, 0.95 * a); rrect(c, 560, 760, 800, 110, 55); c.fill()
        c.set_source_rgba(0.55, 0.4, 1, a); c.arc(640, 815, 34, 0, 6.2832); c.fill()
        c.set_source_rgba(0.1, 0.1, 0.18, a); c.arc(655, 805, 30, 0, 6.2832); c.fill()
        text(c, "Do Not Disturb: ON", 1000, 830, 46, "bold", "#ffffff", a)
    chat_bubble(c, "Group chat (147 unread memes)", 1450, 300, ramp(t, sc(S_, 2) + 1.0, 0.3), size=30, color="#2b5a3a")

def s15(c, t, S_):
    station(c, t, lit=0.6)
    c.set_source_rgba(0.02, 0.03, 0.06, 0.7); c.paint()
    phone(c, 520, 560, 1, t=t, clock="6:59", header="AI Assistant")
    chips(c, [(sc(S_, 1), "I told you not to open the laptop.", "#ff6b6b"), (sc(S_, 2) + 0.3, "Your Do Not Disturb", "#ffffff"),
              (sc(S_, 2) + 1.3, "turns off at 7:00 AM.", "#ffffff")], 860, 330, t, 42)
    text(c, "6:59", 1450, 760, 140, "black", "#ff3b3b", ramp(t, sc(S_, 3), 0.3))
    sky_glow(c, t, ramp(t, sc(S_, 4), 2.5))

def s16(c, t, S_):
    bg(c, "#081020", "#1d3050"); stars(c, t, 1.0)
    sky_glow(c, t, 0.7)
    text(c, "Would YOU", 960, 420, 110, "black", "#ffffff", ramp(t, 0.3, 0.3))
    text(c, "look up?", 960, 550, 110, "black", "#ffd27a", ramp(t, 0.8, 0.3))
    text(c, "↓ comments • part 2? ↓", 960, 680, 48, "semibold", "#9fb4ff", ramp(t, 2.5, 0.3))

DRAW = {f"s{i:02d}": globals()[f"s{i:02d}"] for i in range(1, 17)}; DRAW["s09b"] = s09b

def THUMB(c):
    street(c, 2.0, cars=True, bus=True)
    c.set_source_rgba(0.02, 0.03, 0.08, 0.55); c.paint()
    person(c, 1480, 1000, 1.4, 1, "shock", phone=True, t=1.0)
    text(c, "EVERYONE", 80, 330, 170, "black", "#ffffff", align="l")
    text(c, "VANISHED", 80, 510, 170, "black", "#ff3b3b", align="l")
    text(c, "EXCEPT YOU", 80, 690, 150, "black", "#ffd27a", align="l")
