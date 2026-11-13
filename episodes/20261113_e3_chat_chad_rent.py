import math, random
from kit import *
from chat import *
import chat as C

FORMAT = 'chat'
SLUG = '2026-11-13-chad-pays-rent-with-exposure'
VOICE = 'hype'; CAPTION = 'none'; MOOD = {'style': 'funny', 'root': 65.4}; ZOOM = 0.6; VIGNETTE = 0.0; PROGRESS_COL = BR
C.CHAT.update({'name': 'Mr. Landlordson', 'avatar': '🏠', 'status': 'online'})
MSGS = [
 dict(side='n', text="Fitness influencer Chad Gainsworth, fourteen followers, tries to pay his rent... with exposure."),
 dict(side='l', text="Chad. Rent was due 9 days ago."),
 dict(side='r', text="Bro I got you. Huge news", emoji='🔥'),
 dict(side='r', text="I'll post your building on my story. 14 followers. ORGANIC reach", emoji='📈'),
 dict(side='l', text="I don't want reach. I want $1,200.", punch=True, react='💀'),
 dict(side='r', text="What if I tag you? Exposure is the new currency", emoji='💸'),
 dict(side='l', text="Will exposure fix the hole you punched in the wall?", punch=True),
 dict(side='r', text="That's a CONTENT wall. It's for my day-in-my-life series", emoji='🎥', react='😂'),
 dict(side='l', text="Chad."),
 dict(side='r', text="Ok ok final offer. I name my protein shake after you", emoji='🥤'),
 dict(side='l', text="...what flavor"),
 dict(side='r', text="Landlord Lemon", emoji='🍋', punch=True, react='😭'),
 dict(side='l', text="Deal. Rent goes up 20% though.", punch=True, react='💀'),
 dict(side='n', text="Follow for part two. Chad discovers taxes."),
]
VO = {'n': 'hype', 'l': 'old', 'r': 'bro'}
SPOKEN = {"Bro I got you. Huge news": "Bro, I got you. Huge news.", "I'll post your building on my story. 14 followers. ORGANIC reach": "I'll post your building on my story. Fourteen followers. Organic reach.",
          "I don't want reach. I want $1,200.": "I don't want reach. I want twelve hundred dollars.", "Ok ok final offer. I name my protein shake after you": "Okay, okay. Final offer. I name my protein shake after you.",
          "...what flavor": "What flavor.", "Deal. Rent goes up 20% though.": "Deal. Rent goes up twenty percent, though."}
LINES = []
for i, m in enumerate(MSGS):
    gap = 0.9 if (i + 1 < len(MSGS) and MSGS[i + 1]['side'] == 'l') else 0.25
    if m.get('punch'): gap += 0.35
    LINES.append((SPOKEN.get(m['text'], m['text']), gap, VO[m['side']]))
CAPS = []
ST = {}; STARTS = []

def s_title(img, t, d): title_card(img, t, 'CHAD GAINSWORTH', 'PAYS RENT', 'WITH EXPOSURE', '💪')
def make_chat_shot(a):
    def f(img, t, d):
        draw(img, a + t, MSGS, STARTS)
        for i, m in enumerate(MSGS):
            if m.get('punch'): punch(img, a + t, STARTS[i], W / 2, 1100); burst(img, a + t, STARTS[i] + 0.1, m.get('react') or '😂', W / 2, 1300, 10)
    f.__name__ = f'chat_{a:.1f}'; return f
def s_end(img, t, d): title_card(img, t, 'PART 2', 'CHAD VS TAXES', 'FOLLOW SO YOU DON\'T MISS IT', '🧾')

NOZOOM = ()
def timeline(ls, dur):
    STARTS[:] = [ls(i) for i in range(len(MSGS))]
    tl = [(0, s_title)]
    for i in range(1, len(MSGS) - 1):
        a = ls(i) - (0.85 if MSGS[i]['side'] == 'l' else 0.05)
        tl.append((a, make_chat_shot(round(a * 30) / 30)))
    tl.append((ls(len(MSGS) - 1) - 0.05, s_end))
    return tl
def SFX(ls, dur):
    n = len(MSGS)
    return {'hook_end': 0.3, 'notif': [ls(i) for i in range(1, n - 1)], 'typing': [ls(i) - 0.85 for i in range(1, n - 1) if MSGS[i]['side'] == 'l'],
            'boom': [ls(i) + 0.05 for i in range(n) if MSGS[i].get('punch')], 'end': ls(n - 1) - 0.05}

POST = {
 'title': "He Tried To Pay Rent With EXPOSURE 💀 #shorts",
 'caption': "Fitness influencer Chad Gainsworth (14 followers) vs his landlord. Landlord Lemon might be the worst deal ever made 🍋💀 Part 2: Chad vs taxes.",
 'tags': '#funny #textstory #landlord #influencer #comedy #relatable',
 'source': 'Original comedy sketch. All characters are fictional.',
}
