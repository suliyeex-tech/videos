# PLAYBOOK (owner 2026-11-15, evening) — read before EVERY video. Overrides older style rules.

Model channel: Ricks Clips (@RicksClips3000). ~150 videos, 430M+ views, ~10M avg per video, and it posts only
~0.8 Shorts/day (15 Shorts in 19 days = 167M views). Lesson: few, excellent, same recognisable format every time.
Copy the FORMAT and craft, never its stories, titles, characters or drawings.

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
- YouTube Shorts + Instagram Reels: 3/day at 20:00, 21:00, 23:00 Madrid (our best slots: ~620-820 avg views; 13:00/17:00 were ~75-100).
- TikTok: 1/day (the best one, 21:00, own file + own caption). Goes to 2/day only after 3 TikToks in a row pass 200 views.
- Long-form: Wed + Sat 18:00.
- Raise to 4/day only if avg views per short grows 2 weeks in a row; if a video fails the quality gate, publish fewer that day.

## 7. Description
YouTube: title (formula above) + #shorts; description = 1 curiosity sentence + question + sources + 3 hashtags.
Instagram: 1-2 lines + question + 4-5 niche hashtags. TikTok: different wording, 3-5 niche hashtags, no #fyp.
