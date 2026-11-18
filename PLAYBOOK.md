# PLAYBOOK (owner 2026-11-15, evening) — read before EVERY video. Overrides older style rules.

Model channel: Ricks Clips (@RicksClips3000). ~150 videos, 430M+ views, ~10M avg per video, and it posts only
~0.8 Shorts/day (15 Shorts in 19 days = 167M views). Lesson: few, excellent, same recognisable format every time.
Copy the FORMAT and craft, never its stories, titles, characters or drawings.

## NEW MAIN FORMAT (owner 2026-11-18): "In this town..." blocky-town stories. Overrides §1-§3, §6 hours and §8 world.
Owner sent 3 reference Shorts blowing up right now (2 Spanish "En este pueblo...", 1 English "In this town..."). Analysed:
- LINE 1, SECOND 0, ALWAYS: "In this town, <absurd rule or fact about the whole town>" (e.g. a newspaper that prints
  tomorrow's news; saying a phrase 3 times summons something; everyone parties except me). Never a real-world fact story.
- Narrator = "I", a kid who is the odd one out in the town, deadpan and fast (~220-235 wpm; Kokoro, measure it).
- Beats (85-100 s, ~330-380 words; TikTok rewards > 60 s, retention held because a new shot every 1-2 s):
  1) Rule (0-4 s). 2) Three rapid examples with named townsfolk: "My friend <name>... <name>... even my grandma..." each
  a 2-3 s gag. 3) "But me..." — the narrator breaks or bends the rule. 4) The town turns on him (sandbags around his house,
  banned from the festival, laughed at). 5) The BIG TOWN EVENT: the Mayor (sash, top hat, speech in the square) / festival /
  biggest party of the year. 6) The narrator's weird thing saves the day or flips the rule. 7) Callback twist in the last
  line (the rule strikes again, one level bigger). Optional last line: "...and if you don't want to miss what happens in
  this town next, subscribe."
- SOUND HOOK: one repeated chant/catchphrase/noise (like a "hush hush hush" loop) that returns 4-6 times. Must be OUR OWN,
  not a meme or a song lyric.
- PICTURE: blocky toy-like 3D characters (cube heads, block bodies, simple painted faces) in a bright, saturated little town:
  red-brick clock-tower town hall, main street with traffic light, houses with picket fences, square with stalls. Big face
  close-ups for reactions, crowd shots of the whole town, the Mayor in every video. Recurring cast + same town = brand;
  Oddwick the candle can live in a window of the town hall as a cameo. 1-word captions, bold white/yellow, dark outline,
  centred. "Looks like a game", but NEVER the Roblox name/logo/UI, real Roblox avatars, branded meme characters
  (e.g. Tung Tung Sahur, Skibidi), or anyone's characters/stories. Design everything ourselves.
- English only, written for US + UK viewers (US spelling, "Mayor", "candy", "mom"). Clean language (young audience):
  no swearing, no adult jokes. Not "made for kids" on YouTube (madeForKids false), but nothing unsuitable for teens.
- Titles: "In This Town, <the rule>" <= 45 chars + #shorts. Caption = the rule + a question ("Would you say it a 3rd time?").
- HOURS (owner audience = US + UK; old 20/21/23h Madrid slots landed at 11-14h in California and US school hours):
  YouTube + Instagram 21:00, 23:00, 01:00 Madrid (= UK 20/22/00h, New York 15/17/19h). TikTok: the best one at 23:00 Madrid.
  Own data (YouTube, NY time): best 17h, then 13-14h and 16h; 01:00 Madrid post (Internet Part 2) got 1,011 YT views.

## 0. Research first (every run, 5-6 searches, last 24-48 h)
Most-viewed animated/AI Shorts right now + the newest Ricks Clips titles (search "Ricks Clips shorts", revid.ai/true-story-cartoon-shorts).
Write in LEARNINGS.md Daily notes: 3 titles + views + what the hook was. Pick topics in the same VEIN, never the same story.

## 1. Topic = a TRUE, little-known story with a twist
Title formulas that win: "Why X Don't Work", "The X That Y", "The Job Nobody Wants in Z", "Why Sailors Carried X", "How a X Rigged a Y".
<= 45 characters, no "Part 2", no "What if". Every fact checked with a web search; sources in the YouTube description.

## 2. Script: 60-66 s, ~220 words, told like a kid explaining to a friend (no dates, at most one name)
1. Hook 0-3 s: one plain sentence about something that makes no sense, reason hidden.
2. Setup 3-12 s: who, where, ONE exact number, what is at stake.
3. The mocker 12-20 s: someone laughs at the hero (short sarcastic line, big close-up). Hero stays calm.
4. Escalation 20-40 s: it gets weirder three times; the mocker gets cockier.
5. "You see," once: explain the trick with an everyday comparison in 3-5 short lines.
6. Payoff last 10 s: SHOWN, lands on the mocker. Last line = biggest reveal. No moral, no "follow for more".

## 3. Picture
Our OWN flat 2D characters (thick outline, simple faces, design our own shapes/colours; keep ONE recurring cast so the
channel is recognisable) acting inside lit 3D-looking toon sets. Warm low sun vs cool purple-blue shadows. Camera low and wide,
always gliding, few hard cuts. Captions 1-2 words at a time, bold white, dark outline. Build with HyperFrames (+ registry
blocks, Paper Shaders) or Claude Animation Base; 1080x1920.

## 4. Voice (owner: old voice was slow and boring)
ONE energetic storyteller, fast but natural, ~220 wpm (Kokoro am_puck-led blend, SPEED 1.25-1.35; measure wpm and re-render
if < 210). Smiling, surprised, sarcastic on the mocker's lines. Same voice every video = brand.

## 5. Music and SFX (owner: music had nothing to do with the video; SFX were inaudible)
- Use the `media-use` skill (HyperFrames) to get REAL music and sound effects; engine/audio.py synth is last resort.
- Music follows the STORY: light/curious at the setup, tension in the escalation, a hit + silence right before the payoff,
  then a resolved bright ending. Genre fits the setting (sea story = shanty-like, Japan = koto-like, etc.). Bed ~-22 LUFS under voice.
- SFX on EVERYTHING that happens on screen: breaking, falling, doors, water, footsteps, crowd laugh for the mocker, whooshes on
  camera moves. They must be clearly audible (peaks about -8 dB, louder than music, just under the voice). No beeps/dings.
- Listen to the hook, one SFX moment and the payoff before publishing.

## 6. Volume and hours (max quantity WITHOUT videos eating each other)
- YouTube Shorts + Instagram Reels: 3/day at 21:00, 23:00, 01:00 Madrid (changed 2026-11-18 for US + UK; see NEW MAIN FORMAT).
- TikTok: 1/day (the best one, 23:00 Madrid, own file + own caption). Goes to 2/day only after 3 TikToks in a row pass 200 views.
- Long-form: Wed + Sat 18:00.
- Raise to 4/day only if avg views per short grows 2 weeks in a row; if a video fails the quality gate, publish fewer that day.

## 7. Description
YouTube: title (formula above) + #shorts; description = 1 curiosity sentence + question + sources + 3 hashtags.
Instagram: 1-2 lines + question + 4-5 niche hashtags. TikTok: different wording, 3-5 niche hashtags, no #fyp.

## 8. BE DIFFERENT (owner 2026-11-15 night): Ricks Clips is a craft reference, NOT a template
Platforms demonetise look-alike/mass-produced channels, and a clone never stands out. What is ONLY ours:
- HOST: Oddwick, a smirking candle (brand/oddwick_avatar.png). He appears on screen in every video: lights up in the first
  second, reacts to the story (flame flares on surprises, shrinks when scared), and blows himself out as the last frame.
- WORLD: every story is "told by candlelight": dusk/night scenes, warm orange light against deep purple (the avatar palette).
  Our own cast of 2D characters with our own shapes (not round-head bean people); design them once in brand/ and reuse.
- STORIES: mix 50/50 (a) true little-known stories with a twist and (b) OUR proven winners from LEARNINGS.md: survival
  "don't do this" with a deadline and second-person POV with an A/B choice. No other channel has that mix.
- SIGNATURE: the viewer chooses. End on an A/B question shown as two candles; the pinned comment answers it next day.
- Vary structure: the 6 beats in section 2 are a default, not a mould. At most 1 of the 3 daily videos may use the
  "mocker" beat; the others use a deadline, a mystery, or a POV choice. Never reuse a title formula two days in a row.
- Channel name everywhere: Oddwick. Never mention or imitate other channels in titles, captions or hashtags.
- Kids channel: dropped by the owner; ignore it.

## 9. Accounts after the rename (2026-11-15)
YouTube: Oddwick, @oddwicktales. Instagram: Oddwick, @oddwick.tales. TikTok: photo + bio changed; TikTok locks the nickname
until after 2026-11-16 and the username (@ifitvanished_) until after 2026-12-09, then they become Oddwick / oddwick.tales.
Zernio account IDs are unchanged. Never say "What If It Vanished" in new videos, titles or captions.
