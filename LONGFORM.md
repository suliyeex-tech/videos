# Daily long-form YouTube videos (16:9, 6–9 min): 2 per day (18:00 and 21:00 Madrid). MONEY.md (genres, voices, series, topic claiming) overrides this file.

## OWNER FEEDBACK 2026-11-13 (evening) — overrides anything below
- **Same themes as the Shorts.** The long video uses the same kinds of stories and formats as FORMATS.md, just longer:
  "If X happens while you're at Y" cartoon survival with a funny influencer-named character (Tyler Trailmix, 24, ski
  instructor…), "What if X disappeared / everyone did Y for 5 seconds?" science sims, funny chat/influencer stories,
  stick-figure POV suspense with A/B choices, neon "why your brain…" psychology. Pick the one whose YouTube trend is
  hottest today. Never reuse a topic the Shorts used.
- **Based on viral AI videos ON YOUTUBE.** Research = AI-made / AI-animated videos that went viral on YouTube (long-form
  and Shorts) in the last 24–72 h: search YouTube trending, "AI animated story", "what if" channels, news about viral AI
  YouTube videos. Note title formula, hook, voice, style, length, views. Ride the strongest one and go further.
- **Grab attention instantly**: the first line is the hook (scored, >= 72), something visible happens in the first
  2 seconds, a new visual every 1.5–3 s (pop-in labels, counters, zoom punches, character reactions), a joke or twist
  every 10–15 s, open loops ("but that's not even the worst part…"), mini-cliffhangers before each chapter, and a
  question at the end.
- **Voice = the Shorts' cheerful fast voice**: `VOICE = [["am_echo", 0.5], ["am_puck", 0.5]]`, `SPEED = 1.2`
  (~240 wpm, measured). Never slower. Word count therefore 1,500–2,200 (75–110 SCRIPT lines) for 6–9 min.
- **Upload time = when it gets the most views.** Default 18:00 Madrid = 12:00 New York (Buffer's 1.8M-video study:
  midday/late-morning local time is the peak, the channel's audience is English-speaking, mostly US; publishing
  12:00 ET gets indexed before the US afternoon/evening peak and catches Europe's evening). Each run, also call
  `mcp__Zernio__analytics_get_best_time_to_post` for account 6af5fcdd2fd432bb239b9515: once a slot has >= 3 posts and
  clearly better engagement, use that slot instead (it is in UTC) and say so in the report.


The scheduled task follows this every day. The owner asked for it to run on its own, every day, without asking them.
It runs alongside the 5 daily Shorts (DAILY.md). Never reuse a Shorts topic from the same day.

## Music with an arc (owner reference F "1 MINUTE", 2026-11-14)
Set in every episode, e.g. `MUSIC_ARC = {"s01": 0.7, "s05": 0.3, "s12": 0.0, "s13": 1.0}` and `MUSIC_MOOD = {"s01": "tense", "s16": "hope"}` (levels hold until the next listed scene; 0 = silence before a reveal). Without it the old flat drone is used. See REFERENCES.md F for the story/colour/shot rules.

## 1. Setup
```
git clone https://github.com/suliyeex-tech/videos /home/claude/videos   # or: git -C /home/claude/videos pull --rebase
sh /home/claude/videos/engine/setup.sh
pip install --break-system-packages -q pycairo pillow numpy 2>&1 | tail -1
mkdir -p ~/.fonts && cp /home/claude/videos/longform/fonts/*.otf ~/.fonts/ && fc-cache -f >/dev/null
```

## 2. Research: what went viral with AI in the last 24 hours (max ~25 min)
Use WebSearch (mode "extended" for at least one query) and WebFetch on the articles it returns. Look for the most viral
AI-made or AI-narrated videos and memes of the last 24–48 hours (TikTok, YouTube, Instagram, X), and for each note:
- what it was about and its hook,
- the voice (deep documentary narrator, AI voice clone, character voice, text-to-speech meme voice…),
- the visual style (cartoon, realistic AI footage, slideshow, 3D, meme),
- the audience it hit (kids, gamers, science fans, US/LatAm…) and what it achieved (views, likes, shares, trends spawned).
Real-time view counts are often not public; say "reported" figures only when a source gives them, never invent numbers.
Also check the channel's own results with Zernio (`analytics_get_analytics`, `analytics_get_best_time_to_post`) and lean
into whatever did best.

Then read STYLE.md and pick ONE topic that rides the strongest current trend but goes further. Any kind of viral
AI content works (2nd-person mystery story like longform/episodes/20261112_everyone_vanished.py, survival "what if",
"what happens if…" science, funny AI scenarios…), in English, original (never copy another creator's story,
characters or drawings). Never repeat a topic in `longform/episodes/` or `episodes/`. No real people, no politics,
no medical advice, no copyrighted characters or brands (a meme can be *referenced* in words, never redrawn),
no fake news. Fiction is fine when it is clearly a story; real facts must be checked.

## 3. Script (use the yt-script method)
- Write 5 hooks, score them with the hook scorer from the yt-script skill if it is available
  (`python3 /tmp/yt-script/hookscore.py hooks.txt`), keep the best (aim for STRONG, >= 70).
- 1,500–2,200 words, 75–110 SCRIPT lines, 18–26 scenes (6–9 minutes at ~240 wpm): hook (confirm the title, open a question) → turn (say what the
  video will do, no channel intro) → body beats with a joke every ~20 s → a "plot twist" → the real-world stakes →
  payoff that answers the hook → one ask ("which would you miss most? comments").
- Fact-check EVERY real-world number with a web search; keep the sources for the description.
- Pick the voice of the day as STYLE.md explains and set `VOICE` and `SPEED` in the episode (never slower than speed 1.0). Leave `GAP` at its default.

## 4. Build the episode
- Copy `longform/episodes/20261112_everyone_vanished.py` (story style, uses props_story.py) or `longform/episodes/20261115_polar_bears.py` (explainer style) to `longform/episodes/YYYYMMDD_<topic>.py`.
- Set `SLUG` (start with the date), `TITLE`, `SCRIPT` ([scene, line] pairs), `SUBS` (spoken words → digits for captions),
  write one draw function per scene in `DRAW`, and `THUMB(c)` (big 3-line title left, one bold illustration right,
  max 4 words per line, high contrast). Drawing helpers live in `longform/kit16.py` (text, label_chip, chat_bubble,
  glow, rrect, ramp/ease, stars, bg…) and the example episode (sky, ice, bear, seal, fox, gull, calendar, counter).
  Draw everything yourself as simple cartoons; no downloaded images.
```
cd /home/claude/videos/longform
python3 lf.py episodes/<file>.py tts      # narration (same narrator as the Shorts)
python3 lf.py episodes/<file>.py frames   # contact sheets: READ every sheet_*.jpg, fix overlaps / cut text / text under captions
python3 lf.py episodes/<file>.py all      # ~3 min render -> ../out/<SLUG>.mp4 (< 19 MB) + ../out/<SLUG>.png
```
Look at the thumbnail PNG before publishing.

## 5. Host
```
cd /home/claude/videos && git pull --rebase && git add longform/episodes out/<SLUG>.mp4 out/<SLUG>.png && git commit -m "Long-form: <topic>" && git push
```
URLs: `https://raw.githubusercontent.com/suliyeex-tech/videos/<commit-sha>/out/<SLUG>.mp4` (and `.png`).
Check both with `curl -sI` (HTTP 200). Do NOT use jsDelivr `@sha` URLs: Zernio encodes the `@` and the upload fails with a 400. If the push is rejected, pull --rebase and push again (the Shorts
task pushes to the same repo).

## 6. Publish with Zernio (18:00 Madrid = 17:00Z in winter, 16:00Z in summer; see the owner feedback at the top)
`mcp__Zernio__call_tool` name `posts_create_post`:
- `media_items`: `[{type:"video", url:<mp4 URL>, mimeType:"video/mp4", thumbnail:<png URL>}]`
- `platforms`: `[{platform:"youtube", accountId:"6af5fcdd2fd432bb239b9515", customContent:<description>,
  platformSpecificData:{title:<title, max 100 chars, no #shorts>, madeWithAi:true}},
  {platform:"tiktok", accountId:"6af5fc430c1b54f421bc4837", customContent:<1-line hook + 4-6 hashtags incl. #fyp, e.g. "7 days to build a bunker #survival #story #fyp">}]`
  plus `tiktok_settings` {privacyLevel:"PUBLIC_TO_EVERYONE", allowComment:true, allowDuet:true, allowStitch:true,
  commercialContentType:"none", contentPreviewConfirmed:true, expressConsentGiven:true, videoMadeWithAi:true}.
  WHY TikTok too (owner reference, 2026-11-13): @mr.survival4 posts the full 9.5-min horizontal story on TikTok
  ("7 Days To build a bunker", 5.9M views, 981K likes). Long horizontal stories work there. TikTok accepts up to 10 min:
  if the video is longer or TikTok rejects it, keep YouTube only and say so in the report.
- `tags`: 8–12 keywords, `scheduled_for`: the slot in UTC, `timezone`: "Europe/Madrid".
- Description: 2-line summary with the hook, chapter timestamps (0:00 …, from the scene start times printed by
  `python3 -c "import os,sys;os.environ['LF_TIMING']='/home/claude/work/lf_<SLUG>/timing.json';sys.path.insert(0,'.');import kit16 as k;[print(n,k.SCENES[n]['start']) for n in k.ORDER]"`),
  the comment question, and "Sources:" with every source.
If the slot has already passed, schedule for the next full hour before 23:59 Madrid. Verify with `posts_get` that the
post is scheduled. If Zernio fails, use Upload-Post `upload_video` (user "@ifitvanishedd", platforms ["youtube"],
videoPathOrUrl = mp4 URL, scheduledDate, platformOptions {youtubePrivacyStatus:"public", youtubeContainsSyntheticMedia:true,
youtubeSelfDeclaredMadeForKids:false, youtubeThumbnailUrl:<png URL>, youtubeTags:[…]}; first without `confirmed`,
then with `confirmed:true`). Never retry a plan-limit refusal in a loop and never pay or upgrade anything.

## 7. Report (Spanish, short, SendUserMessage)
The viral trend it is based on (and why), title, time it goes live, link, and anything that failed.
