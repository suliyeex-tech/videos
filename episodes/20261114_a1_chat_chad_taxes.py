import math, random
from kit import *
from chat import *
import chat as C

FORMAT = 'chat'
SLUG = '2026-11-14-chad-does-his-taxes-part-2'
VOICE = 'hype'; CAPTION = 'none'; MOOD = {'style': 'funny', 'root': 61.7}; ZOOM = 0.6; VIGNETTE = 0.0; PROGRESS_COL = BR
VOICE_SPEED = {'hype': 1.25, 'bro': 1.27, 'girl': 1.2}
C.CHAT.update({'name': 'Deb Deductible · Accountant', 'avatar': '🧮', 'status': 'online'})
MSGS = [
 dict(side='n', text="Part two. Fitness influencer Chad Gainsworth just made his first money online. Now he has to do his taxes."),
 dict(side='l', text="Hi Chad, it's Deb, your new accountant. Your sister hired me."),
 dict(side='r', text="DEB!! Huge year. Landlord Lemon made me $14", emoji='🍋'),
 dict(side='l', text="Great. Send me your receipts."),
 dict(side='r', text="Sent you 312 receipts", emoji='🧾', react='😳'),
 dict(side='l', text="Chad, these are all protein shakes."),
 dict(side='r', text="Business expense. I drink them ON CAMERA", emoji='🎥'),
 dict(side='l', text="Your camera points at the floor in every video.", punch=True, react='💀'),
 dict(side='r', text="That's my aesthetic. Floorcore", emoji='✨'),
 dict(side='l', text="You also listed your abs as equipment.", punch=True, react='😭'),
 dict(side='r', text="They took 6 years to build. They lose value every Thanksgiving", emoji='🦃', react='😂'),
 dict(side='l', text="Total income: $14. Total spent: $3,012."),
 dict(side='r', text="So I'm a STARTUP??", emoji='🚀'),
 dict(side='l', text="You bought FOUR ring lights."),
 dict(side='r', text="One for each angle of my jawline", emoji='💡', react='😭'),
 dict(side='l', text="You're a hobby with a ring light.", punch=True, react='💀'),
 dict(side='r', text="Can I pay you in exposure", emoji='📈'),
 dict(side='l', text="Your landlord warned me about you.", punch=True),
 dict(side='r', text="Wait. You know Mr. Landlordson??", emoji='😳'),
 dict(side='l', text="He's my husband.", punch=True, react='😱'),
 dict(side='r', text="...", react='💀'),
 dict(side='r', text="Does he still want the 20%"),
 dict(side='l', text="He wants you at dinner. Sunday. Bring the lemon shakes.", punch=True, react='🍋'),
 dict(side='n', text="Part three: Chad meets the family. Follow so you don't miss it."),
]
VO = {'n': 'hype', 'l': 'girl', 'r': 'bro'}
SPOKEN = {
 "Hi Chad, it's Deb, your new accountant. Your sister hired me.": "Hi Chad, it's Deb, your new accountant. Your sister hired me.",
 "DEB!! Huge year. Landlord Lemon made me $14": "Deb! Huge year. Landlord Lemon made me fourteen dollars!",
 "Sent you 312 receipts": "Sent you three hundred and twelve receipts.",
 "Business expense. I drink them ON CAMERA": "Business expense. I drink them on camera.",
 "That's my aesthetic. Floorcore": "That's my aesthetic. Floor-core.",
 "They took 6 years to build. They lose value every Thanksgiving": "They took six years to build. They lose value every Thanksgiving.",
 "Total income: $14. Total spent: $3,012.": "Total income: fourteen dollars. Total spent: three thousand and twelve.",
 "So I'm a STARTUP??": "So I'm a startup?!", "You bought FOUR ring lights.": "You bought four ring lights.",
 "Can I pay you in exposure": "Can I pay you in exposure?",
 "Wait. You know Mr. Landlordson??": "Wait. You know Mister Landlordson?!",
 "...": "Uh.",
 "Does he still want the 20%": "Does he still want the twenty percent?",
}
LINES = []
for i, m in enumerate(MSGS):
    gap = 0.85 if (i + 1 < len(MSGS) and MSGS[i + 1]['side'] == 'l') else 0.25
    if m.get('punch'): gap += 0.35
    LINES.append((SPOKEN.get(m['text'], m['text']), gap, VO[m['side']]))
CAPS = []
STARTS = []
SP = next(i for i, m in enumerate(MSGS) if m['text'].startswith('Total income'))

def s_title(img, t, d):
    title_card(img, t, 'CHAD GAINSWORTH', 'DOES HIS TAXES', '14 FOLLOWERS · $14 INCOME', '🧾')
    k = back(ramp(t, 0.5, 0.75)); rrect(img, W / 2 - 150 * k, 300, 300 * k, 100, 18, RED)
    if k > 0.8: text(img, 'PART 2', W / 2, 350, 64, WHITE, ANT)
def make_chat_shot(a):
    def f(img, t, d):
        T = a + t; draw(img, T, MSGS, STARTS)
        for i, m in enumerate(MSGS):
            if m.get('punch'): punch(img, T, STARTS[i], W / 2, 1100); burst(img, T, STARTS[i] + 0.1, m.get('react') or '😂', W / 2, 1300, 10)
        # running money tracker
        inc = 14 if T >= STARTS[2] else 0; spent = int(counter(T, STARTS[SP], STARTS[SP] + 1.2, 0, 3012)) if T >= STARTS[SP] else 0
        rrect(img, W - 300, 70, 270, 100, 20, (44, 42, 42))
        text(img, f'IN  ${inc}', W - 165, 100, 30, (110, 200, 110), INTER_B); text(img, f'OUT ${spent:,}', W - 165, 142, 30, RED, INTER_B)
    f.__name__ = f'chat_{a:.1f}'; return f
def s_end(img, t, d):
    title_card(img, t, 'PART 3', 'MEETS THE FAMILY', "FOLLOW SO YOU DON'T MISS IT", '🍽️')

def timeline(ls, dur):
    STARTS[:] = [ls(i) for i in range(len(MSGS))]
    tl = [(0, s_title)]
    for i in range(1, len(MSGS) - 1):
        a = ls(i) - (0.8 if MSGS[i]['side'] == 'l' else 0.05)
        tl.append((a, make_chat_shot(round(a * 30) / 30)))
    tl.append((ls(len(MSGS) - 1) - 0.05, s_end))
    return tl
def SFX(ls, dur):
    n = len(MSGS)
    return {'hook_end': 0.3, 'notif': [ls(i) for i in range(1, n - 1)], 'typing': [ls(i) - 0.8 for i in range(1, n - 1) if MSGS[i]['side'] == 'l'],
            'boom': [ls(i) + 0.05 for i in range(n) if MSGS[i].get('punch')], 'pop': [ls(0) + 0.5], 'end': ls(n - 1) - 0.05}

POST = {
 'title': "He Listed His ABS As Business Equipment 💀 Part 2 #shorts",
 'caption': "Part 2: fitness influencer Chad Gainsworth made $14 and spent $3,012... then his accountant dropped the biggest plot twist of his life 🍋💀 Should Chad go to that dinner? Comment YES or RUN 👇",
 'tags': '#funny #textstory #chatstory #influencer #comedy #taxes #part2',
 'source': 'Original comedy sketch. All characters are fictional. Not tax advice. Part 1: "He Tried To Pay Rent With EXPOSURE".',
}
