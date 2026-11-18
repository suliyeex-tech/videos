# PLAYBOOK (owner 2026-11-15, evening) — read before EVERY video. Overrides older style rules.

Model channel: Ricks Clips (@RicksClips3000). ~150 videos, 430M+ views, ~10M avg per video, and it posts only
~0.8 Shorts/day (15 Shorts in 19 days = 167M views). Lesson: few, excellent, same recognisable format every time.
Copy the FORMAT and craft, never its stories, titles, characters or drawings.

## EXTRA FORMAT (owner 2026-11-18): "In this town..." blocky-town stories — for SOME videos, not all
Owner: do NOT make every video like this. Use it for about 1 of the 3 daily Shorts (on days when the trend is hot, max 2),
and keep improving it by watching which "In this town" Shorts are going viral right now. Other slots keep the formats below.
Owner sent 3 reference Shorts blowing up right now (2 Spanish "En este pueblo...", 1 English "In this town..."). Analysed:
- LINE 1, SECOND 0: "In this town, <absurd rule about the whole town>" OR the hustle variant the owner asked for:
  "In this town, while everyone is <studying / playing games / partying>, I'm <playing games / hustling / practicing>.
  Hush, hush, hush." (narrator does the opposite of the town, obsessively, and it pays off at the big event).
- Narrator = "I", a kid who is the odd one out in the town, deadpan and fast (~220-235 wpm; Kokoro, measure it).
- Beats (85-100 s, ~330-380 words; a new shot every 1-2 s):
  1) Rule / "while everyone is X, I'm Y" (0-4 s). 2) Three rapid gags with named townsfolk ("My friend..., ...even my
  grandma"). 3) "But me..." — his obsessive routine (5 AM, 200 reps before breakfast, absurd escalation: he wraps the cat).
  4) Setback / the town laughs or turns on him. 5) The BIG TOWN EVENT with the Mayor (speech, festival, biggest party).
  6) His weird skill saves the day. 7) Callback twist in the last line ("While you were partying..."). Optional:
  "...and if you don't want to miss what happens in this town next, subscribe."
- SOUND HOOK: one repeated chant ("hush, hush, hush") returning 4-6 times, with a matching SFX. Our own words, never a
  meme sound or a song lyric.
- PICTURE: blocky toy-like 3D characters (cube heads, block bodies, simple painted faces) in a bright saturated town:
  red-brick clock-tower town hall, main street, houses with picket fences, a square. Face close-ups for reactions, crowd shots,
  the Mayor (sash, top hat) in every video. Same cast + same town every time = brand. Oddwick can be a candle in a town-hall
  window. 1-word captions, bold white/yellow, dark outline, centred. Looks like a game, but NEVER the Roblox name/logo/UI,
  real Roblox avatars, branded meme characters (e.g. Tung Tung Sahur, Skibidi) or anyone's characters/stories.
- HOW TO BUILD IT: Blender headless (pip install bpy; see TOOLS.md and engine/blocktown/town_starter.py). Build the town
  and the cast ONCE as a reusable .blend in brand/blocktown/, then animate shots with keyframes. Captions/SFX on top with
  HyperFrames or ffmpeg.
- English for US + UK viewers, clean language (young audience: no swearing), YouTube madeForKids false.
- Title: "In This Town, ..." or "While Everyone Was X, I Was Y" (<= 45 chars) + #shorts.

## AI pictures with open-higgsfield-skills (owner 2026-11-18) — see HIGGSFIELD.md
Use it from now on, free only. Unattended runs: run `shot-qc` on every Short, pick up any Colab stills the owner already
rendered (Google Drive) and turn them into a Short on CPU, and prepare ONE Colab-ready episode per run. Never pay for a GPU.

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
- YouTube Shorts + Instagram Reels: 3/day at 21:00, 23:00, 01:00 Madrid (owner 2026-11-18: audience USA + UK = UK 20/22/00h, NY 15/17/19h).
- TikTok: 1/day (the best one, 23:00 Madrid, own file + own caption).
- Hour analysis 2026-11-18 (88 Shorts, 9-16 Nov): the SAME video gets wildly different views per platform (slug IG 1,686 vs YT 44;
  earth spin IG 1,328 vs YT 17), so content + first-hour test matter more than the hour. YouTube did best at 20h and 01h Madrid,
  Instagram at 21h and 13-15h Madrid (= US morning). TikTok stuck at ~250 views at every hour.
  The Sahara TikTok (4,070 views, 2026-11-09) had PAID promotion: never count it as organic or as a model to copy. Nothing was
  ever posted in the Madrid morning, so mornings are untested. Weekly report: keep tracking median views per Madrid hour per platform. Goes to 2/day only after 3 TikToks in a row pass 200 views.
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
