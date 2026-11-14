import math, random
from kit import *
from quiz import *
import quiz as Q

FORMAT = 'quiz'
SLUG = '2026-11-14-animal-quiz-5-out-of-5'
VOICE = 'girl'; SPEED = 1.2; CAPTION = 'karaoke'; TICKS = True; MOOD = {'style': 'hype', 'root': 58.27}; ZOOM = 0.7; VIGNETTE = 0.15
Q.QZ.update({'host': 'TESSA TRIVIALICIOUS', 'host_emoji': '🎤', 'total': 5})
QS = [
 dict(q="Which animal has THREE hearts?", opts=["Octopus", "Shark", "Frog"], c=0, e='🐙',
      ask="Question one. Which animal has three hearts? Octopus, shark, or frog?",
      ans="Octopus! Two hearts pump blood to the gills, one to the body. And its blood is blue.",
      cap=["[OCTOPUS!]", "2 HEARTS", "FOR THE GILLS,", "1 FOR THE BODY.", "ITS BLOOD", "IS {BLUE.}"]),
 dict(q="Which animal poops CUBES?", opts=["Panda", "Wombat", "Sloth"], c=1, e='🟫',
      ask="Question two. Which animal poops cubes? Panda, wombat, or sloth?",
      ans="Wombat! Cube-shaped poop, left on rocks and logs like little signs that say: mine.",
      cap=["[WOMBAT!]", "CUBE-SHAPED POOP,", "LEFT ON ROCKS", "LIKE LITTLE SIGNS:", "{MINE.}"]),
 dict(q="Which of these CAN'T jump?", opts=["Kangaroo", "Goat", "Elephant"], c=2, e='🐘',
      ask="Question three. Which of these can't jump? Kangaroo, goat, or elephant?",
      ans="Elephant! Even running, one foot always stays on the ground.",
      cap=["[ELEPHANT!]", "EVEN RUNNING,", "ONE FOOT", "{ALWAYS} STAYS", "ON THE GROUND."]),
 dict(q="Who sleeps up to 22 HOURS a day?", opts=["Koala", "Lion", "Owl"], c=0, e='🐨',
      ask="Question four. Which animal sleeps up to twenty-two hours a day? Koala, lion, or owl?",
      ans="Koala! Eucalyptus leaves give so little energy, they nap almost all day. Honestly? Goals.",
      cap=["[KOALA!]", "EUCALYPTUS GIVES", "SO LITTLE ENERGY,", "THEY NAP", "ALL DAY.", "{GOALS.}"]),
 dict(q="A group of flamingos is called...", opts=["A party", "A flamboyance", "A pinkie"], c=1, e='🦩',
      ask="Final question. What do you call a group of flamingos? A party, a flamboyance, or a pinkie?",
      ans="A flamboyance! Yes. That's the real name.",
      cap=["[A FLAMBOYANCE!]", "YES.", "THAT'S THE", "{REAL NAME.}"]),
]
LINES = [("Five animal questions. Bet you can't get all five. I'm Tessa. Go!", 0.2)]
CAPS = [["[5] ANIMAL QUESTIONS.", "BET YOU", "{CAN'T GET 5/5.}", "GO!"]]
for q in QS:
    LINES += [(q['ask'], 0.05), (None, 3.0), (q['ans'], 0.35)]
    CAPS += [[], [], q['cap']]
LINES.append(("Comment your score out of five. Be honest. Tessa is watching.", 2.3))
CAPS.append(["COMMENT", "YOUR [SCORE /5.]", "BE {HONEST.}"])
ST = {}; TQ = {}

def s_intro(img, t, d):
    stage(img, t); top_bar(img, 0, [])
    k = back(ramp(t, 0.05, 0.35)); emoji(img, '🐾', W / 2, 560, 220 * k, rot=8 * math.sin(t * 5))
    text(img, 'ANIMAL QUIZ', W / 2, 820, 150, YEL, ANT, scale=0.6 + 0.4 * back(ramp(t, 0.1, 0.4)), stroke=10, scol=INK)
    text(img, 'CAN YOU GET 5/5?', W / 2, 960, 70, WHITE, ANT, alpha=ramp(t, 0.4, 0.7))
    for i, ch in enumerate('🐙🟫🐘🐨🦩'):
        kk = back(ramp(t, 0.8 + i * 0.15, 1.05 + i * 0.15)); emoji(img, ch, 180 + i * 180, 1600, 110 * kk)
def make_q(qi):
    q = QS[qi]
    def f(img, t, d):
        T = ST[f] + t; a = TQ[qi]['ask']; b = TQ[qi]['beat']; r = TQ[qi]['rev']
        stage(img, T); top_bar(img, qi + 1, [True] * qi + ([True] if T >= r else []))
        question_card(img, T, q['q'], a)
        answers(img, T, q['opts'], a + 0.4, reveal=r, correct=q['c'])
        if T < r: timer(img, T, b, 3.0, cy=1560)
        else: big_emoji(img, T, q['e'], r, cy=1580, size=240)
        if T >= r: flash(img, T, r, 0.15, WHITE, 0.5)
    f.__name__ = f'q{qi}_{random.random():.5f}'; return f
def s_end(img, t, d):
    stage(img, t); top_bar(img, 0, [True] * 5)
    for i in range(6):
        k = back(ramp(t, 0.1 + i * 0.12, 0.35 + i * 0.12)); x = 150 + i * 156
        rrect(img, x - 65, 620, 130 * k, 160, 24, YEL if i == 5 else WHITE)
        if k > 0.8: text(img, str(i), x, 700, 100, INK, ANT)
    text(img, 'YOUR SCORE?', W / 2, 500, 120, WHITE, ANT, scale=0.7 + 0.3 * back(ramp(t, 0, 0.3)), stroke=8, scol=INK)
    text(img, 'COMMENT 👇'.replace(' 👇', ''), W / 2, 900, 90, YEL, ANT, scale=1 + 0.05 * math.sin(t * 8))
    emoji(img, '👀', W / 2, 1600, 160 * back(ramp(t, 1.5, 1.8)))

NOZOOM = ()
def timeline(ls, dur):
    tl = [(0, s_intro)]
    for qi in range(5):
        i0 = 1 + qi * 3; TQ[qi] = {'ask': ls(i0), 'beat': ls(i0 + 1), 'rev': ls(i0 + 2)}
        for j in range(3): tl.append((ls(i0 + j) - 0.05, make_q(qi)))
    tl.append((ls(16) - 0.05, s_end))
    for a, f in tl: ST[f] = round(a * 30) / 30
    return tl
def SFX(ls, dur):
    ticks = []; dings = []; whoosh = []
    for qi in range(5):
        i0 = 1 + qi * 3; ticks += [ls(i0 + 1) + k for k in range(3)]; dings.append(ls(i0 + 2)); whoosh.append(ls(i0) + 0.1)
    return {'hook_end': ls(1), 'tick': ticks, 'ding': dings, 'whoosh': whoosh, 'pop': [ls(0) + 0.8 + k * 0.15 for k in range(5)] + [ls(i) + 0.4 + k * 0.15 for i in (1, 4, 7, 10, 13) for k in range(3)],
            'end': ls(16) - 0.05}

POST = {
 'title': "Animal Quiz: Can You Get 5/5? 🐙🐘🦩 #shorts",
 'caption': "5 animal questions, 3 seconds each. The last one sounds fake but it's 100% real 🦩 Comment your score out of 5 (be honest) 👇",
 'tags': '#quiz #animals #trivia #animalfacts #funfacts #challenge',
 'source': 'Sources: Smithsonian / National Geographic (octopus: three hearts, blue copper-based blood); Georgia Tech study 2018 (wombat cube-shaped scat used as territory markers); elephants cannot jump and keep a foot on the ground even at top speed (Hutchinson et al., Nature 2003); Australian Koala Foundation (koalas sleep 18-22 h); "flamboyance" = group of flamingos (Smithsonian National Zoo).',
}
