# Shorts formats: 5 different videos every day (owner feedback 2026-11-13)

The owner said the videos were "all the same, same drawings, same people". From now on:

- **The 5 videos of a day must be 5 DIFFERENT formats.** Never two in the same visual style on the same day. Rotate,
  so the same format does not open the evening two days in a row. Invent new formats too (see "Ideas" below).
- **Mix tones to reach different audiences**: every day at least 2 INTERESTING (science / psychology / "what happens if"),
  at least 2 FUNNY (comedy, text stories, absurd influencers), and 1 SUSPENSE / POV story.
- **Characters get funny influencer-style names**, never ordinary names and never the same character twice:
  Tyler Trailmix, Chad Gainsworth, Livestream Larry, Brenda Brunchwell, Kyle Kettlebell, Crypto Kevin, Skylar Selfie,
  Gary Gluten-Free, Madison Matcha, Duke Dropshipper, Penny Podcast, Logan Lifehack… (invent new ones every day;
  never a real person's name or handle).
- **Narration voice: cheerful and FAST** like the viral references (darkset, Stick Motion, meanwhile animations).
  Default `VOICE = 'hype'` (am_echo + am_puck, speed 1.25) or `'default'` (puck/eric/fenrir 1.05). Use `'suspense'` only
  for POV stories, and side voices (`'old'`, `'girl'`, `'bro'`, `'mom'`) for characters in chat stories. Silent beats
  with serif subtitles are fine for the cinematic format.

## DOPAMINE rules (owner: "necesito que tengan más dopamina")
Every short must have, on top of a hook in the first 1.5 s:
1. Something changes on screen every 1.5–3 s (new shot, zoom punch, pop-in, counter, emoji burst).
2. Karaoke or pop captions word by word (`CAPTION='karaoke'` or `'top'`) with key words coloured; `TICKS=True`.
3. SFX on every beat: `pop`, `whoosh`, `boom`, `ding`, `notif`, `typing`, `mistake`, `riser`/`drop`.
4. A number that counts up/down on screen (followers, speed, population, countdown).
5. A twist or joke every ~8–10 s and a cliffhanger or question at the end ("Part 2", "A or B?", "Comment…").
6. Progress bar on (except cinematic). Length 25–45 s.

## The formats in the engine (engine/formats/*.py; examples in episodes/20261113_*.py)
| key | look | best for | example |
|---|---|---|---|
| `neon` | black background, neon-blue line figures, glowing numbers, top captions (darkset style) | psychology, money, "why you…" facts | e1_neon_scroll |
| `stickpov` | stick figure 1st-person POV, HUD with clock/countdown, phone in hand, A/B choice ending (Stick Motion style) | suspense, creepy, choose-your-path | e2_stickpov_lasttrain |
| `chat` | text-message story: bubbles, typing dots, reactions, emoji bursts, several voices | comedy, influencer drama | e3_chat_chad_rent |
| `cinema` | 2.5D mannequins/crowds, silent beats with serif subtitles, giant counters (meanwhile style) | "what if everyone…", big-scale science | e4_cinema_everyone_jumps |
| `cartoon` | flat 2D cartoon (kit.person), rule card, STUPID MISTAKE beat, live-chat gag | survival "what if" with a funny influencer | e5_cartoon_bear_tent |

## Ideas for new formats (build one when a trend fits)
- **Ranking / tier list** ("Ranking every way to survive X", animated tier list S→F with sound per drop).
- **Fake game UI** (health bar, XP, "achievement unlocked", inventory) for survival or daily-life comedy.
- **Split screen "Expectation vs Reality"** or "$1 vs $1,000,000" side by side.
- **Map / satellite zoom** explainer with a moving pin and distance counters.
- **Quiz** ("Only 1% get this": 3 s countdown, answer reveal, score).
- **Courtroom / interview** comedy with two characters and subtitles.
Keep everything original: never copy another creator's story, characters or drawings, never use copyrighted
characters, brands or real people.
