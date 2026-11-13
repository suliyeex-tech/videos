# Channel style (set by the owner on 2026-11-12; Shorts formats updated 2026-11-13, see FORMATS.md)

SHORTS: read FORMATS.md first. 5 different formats per day, funny influencer-style names, cheerful fast narrator
(`VOICE='hype'`), dopamine rules. The music bed may follow the format (hype / funny / tension / cinematic) but stays quiet under the voice.

The channel posts ANY kind of AI-made content that is going viral right now. It is no longer limited to
"what if X vanished": follow the trend of the day (survival "what if" stories, 2nd-person mystery stories, AI-made
characters and memes, "what happens if…" science, rankings, true stories retold, animated explainers, funny AI
scenarios…). Everything in English.

## Voice and pacing (owner feedback 2026-11-12)
The voice is chosen EVERY DAY to match the style of the most viral AI videos you researched (Shorts and long-form),
not fixed. For each viral reference, note the narrator: gender, pitch (deep / medium / high), energy (calm documentary,
hyped, cheerful storyteller, creepy whisper…), and pace. Then pick the closest Kokoro voice or blend below and set it
in the episode file (`VOICE = [["am_puck", 0.4], ["am_eric", 0.3], ["am_fenrir", 0.3]]`, `SPEED = 1.05`).
Shorts and long-form of the same day may use different voices if their trends differ. Say in the final report which
voice you picked and which viral video it imitates.

Hard rules from the owner (never break them, whatever the trend):
- FAST: at least ~200 words per minute (Kokoro speed >= 1.0); the owner rejected 167 and 190 wpm as too slow.
- CHEERFUL / LIVELY and bright: never flat or sleepy. The deep, slow am_onyx blend was rejected as "boring".
- Presence EQ, compression and -14 LUFS are applied automatically by the engines.

Default when no clear reference exists (approved by the owner): 40% am_puck + 30% am_eric + 30% am_fenrir, speed 1.05
(~215 wpm, ~125 Hz).

Kokoro voices measured on the same line (median pitch, intonation variation; higher variation = livelier):
| voice | pitch | variation | character |
|---|---|---|---|
| am_puck | 104 Hz | 0.30 | lively, expressive storyteller |
| am_fenrir | 129–137 Hz | 0.30 | bright, energetic |
| am_eric | 155 Hz | 0.24 | upbeat, higher, fast |
| am_michael | 117 Hz | 0.19 | neutral explainer |
| am_liam | 128 Hz | 0.25 | casual, younger |
| am_echo | 108 Hz | 0.26 | smooth, mid-deep |
| am_onyx | 85 Hz | 0.17 | very deep, flat (only as a small part of a blend, for a "documentary" trend) |
| bm_george / bm_daniel / bm_lewis | 141 / 123 / 86 Hz | ~0.2 | British |
| af_* / bf_* | — | — | female voices exist too (e.g. af_heart, af_bella, bf_emma) if the trend uses a female narrator |
Test a blend in 10 seconds: create one line with kokoro_onnx and check its pitch/pace before rendering everything.

- Almost no dead air: pauses between lines ~0.12 s.
- Music is a quiet dark bed ~25 dB under the voice. No cheerful melodies.
- Long-form: 6–9 minutes (1,300–1,900 words at ~215 wpm).
- Something changes on screen every 2–4 seconds; a joke or a twist every ~20 seconds.

## The two reference formats (both very popular)
1. Vertical "what if" survival Short (~67 s, the_what_if_animator style): flat 2D cartoon, snowy/real places, a named
   character with age and job ("WES · 19 · SKI PATROL"), "PART 1" tag, a "RULE #2" card, a "STUPID MISTAKE." beat,
   real data badges (altitude, temperature, "REAL feels like -19°F (NWS)"), a cute side character (a 140-lb Saint
   Bernard), big uppercase captions with key words in yellow/red, cliffhanger ending ("Nobody had stopped the lift.").
2. Long-form "Mr Survival" story (16:9, ~9.5 min): told in 2nd person ("At 3:12 AM, your phone buzzes."), a mystery
   driving it (unknown texts, a countdown "seven days left"), dark minimal rooms, a simple round-head character,
   phone close-ups with short message chips appearing line by line, small on-screen labels ("$4,200", "20 minutes…"),
   a deadpan joke every ~20 s ("There's half a pizza and a broken umbrella in your fridge. Stop laughing."), and a
   twist that recontextualises the start.

Long-form example in this style: longform/episodes/20261112_everyone_vanished.py (shared props in longform/props_story.py).
Never copy those videos' stories, characters or drawings; make original ones in the same spirit.
