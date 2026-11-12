# Daily long-form YouTube video (16:9, 6–9 min), published 20:30 Madrid

The scheduled task follows this every day. The owner asked for it to run on its own, every day, without asking them.
It runs alongside the 5 daily Shorts (DAILY.md). Never reuse a Shorts topic from the same day.

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
- 1,300–1,900 words, 65–95 SCRIPT lines, 18–24 scenes (6–9 minutes at ~215 wpm): hook (confirm the title, open a question) → turn (say what the
  video will do, no channel intro) → body beats with a joke every ~20 s → a "plot twist" → the real-world stakes →
  payoff that answers the hook → one ask ("which would you miss most? comments").
- Fact-check EVERY real-world number with a web search; keep the sources for the description.
- Do NOT set `VOICE`, `SPEED` or `GAP`: the defaults are the channel narrator at the right pace (see STYLE.md).

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

## 6. Publish with Zernio (20:30 Madrid = 19:30Z in winter, 18:30Z in summer)
`mcp__Zernio__call_tool` name `posts_create_post`:
- `media_items`: `[{type:"video", url:<mp4 URL>, mimeType:"video/mp4", thumbnail:<png URL>}]`
- `platforms`: `[{platform:"youtube", accountId:"6af5fcdd2fd432bb239b9515", customContent:<description>,
  platformSpecificData:{title:<title, max 100 chars, no #shorts>, madeWithAi:true}}]`
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
