# Shorts formats: 4 different videos every day, all 61-80 s (see MONEY.md, it overrides counts here)

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
| `sim3d` | small 3D world rendered in code at a real famous place, HUD (TEMPERATURE 72 °F · PLACE), serif title, countdown "X RETURNS IN 1.77 S · SHOWN 6x SLOWER", serif subtitles (whatif.sim style) | "What if X disappeared for 5 seconds?" science sims | x6_sim3d_friction_demo (template, not published) |

## Reference videos from the owner (2026-11-13) — study these, never copy their stories or drawings
1. **@whatif.sim** (3D sims, 46.8K followers, 1.3M likes; hits of 3.5M, 2.7M, 2.1M, 1.5M views). Formula:
   - Title as a question: "What if X disappeared / hit absolute zero / every human did Y **for 5 seconds**?"
   - A REAL famous place and 2nd person: "You're on the Santa Monica pier…", "Fold it in front of the Burj Khalifa…".
   - Calm 3D low-poly world, HUD with real data top-left, countdown "THE HEAT RETURNS IN 1.77 S · SHOWN 6x SLOWER",
     elegant serif title and italic subtitles ("The ocean is ice. The birds fall."), then everything "comes back".
   - Engagement: "You asked for it (18,543 of you)", "Comment your city 👇", "How long would you last? 👇".
     Funny absurd variants do best ("every human farted at the same time" = 3.5M).
   - Use `sim3d` (beach_scene / city_scene + Cam + lerp_cam, hud, countdown, title). Pick topics they have NOT done
     (they did: water, atmosphere, electrons, oceans, ice melting, absolute zero, Yellowstone, Betelgeuse, stock market,
     paper folded 103 times, farting, twerking, tsunami waves).
2. **@mr.survival4** ("7 Days To build a bunker", 9.5 min, 16:9, 5.9M views on TikTok): 2nd-person mystery driven by
   texts at 3:12 AM, a countdown of days, progress labels ("Bunker 45%", "Money left $1,400"), a nosy neighbour,
   deadpan jokes, a twist (the texts come from your missing dad). Simple stick figures with name labels. → long-form
   (LONGFORM.md) and it is also posted to TikTok. For Shorts, the `stickpov` format can do a 60-s "Day 1 of 7" Part 1.
3. **@the_what_if_animator** (zombie apocalypse on a ski trip, 63 s, 3.9M views): "If X happens while you're at Y…
   don't do Z (Part 1)", named character with age and job ("Wes, 19, first day on ski patrol"), real numbers
   (5 °F, 30 mph wind, bare skin freezes in 30 min), a cute side character (Barry, 140-lb Saint Bernard),
   "one very stupid mistake", cliffhanger ("Nobody had stopped the lift."). → `cartoon` format.
Each day at least ONE short should follow reference 1 (sim3d) or 3 (cartoon "If X while Y" Part 1), because they are the
top performers right now; the other slots rotate the remaining formats.

## Ideas for new formats (build one when a trend fits)
- **Ranking / tier list** ("Ranking every way to survive X", animated tier list S→F with sound per drop).
- **Fake game UI** (health bar, XP, "achievement unlocked", inventory) for survival or daily-life comedy.
- **Split screen "Expectation vs Reality"** or "$1 vs $1,000,000" side by side.
- **Map / satellite zoom** explainer with a moving pin and distance counters.
- **Quiz** ("Only 1% get this": 3 s countdown, answer reveal, score).
- **Courtroom / interview** comedy with two characters and subtitles.
Keep everything original: never copy another creator's story, characters or drawings, never use copyrighted
characters, brands or real people.
