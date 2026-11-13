# Daily "What If" shorts: 2 runs x 4 shorts, all 61-80 s. READ MONEY.md FIRST (schedule, genres, voices, series), it overrides this file.

This is the routine the scheduled task follows every day. The account owner asked for it to run without any input from them.

## 0. FIRST: duplicate guard + new rules (owner, 2026-11-13)
- Before anything else call `mcp__Zernio__call_tool` name `posts_list_posts` with `{"status": "scheduled", "limit": 50}`.
  If 5 or more posts are already scheduled between 18:00 Madrid today and midnight, today's shorts are already done:
  do NOT make more; send the owner one line in Spanish saying so, and stop.
- Read **FORMATS.md**: 5 COMPLETELY DIFFERENT formats per day (neon, stick POV, chat story, cinema, cartoon, or new ones),
  mix of interesting / funny / suspense, funny influencer-style names, cheerful FAST voice (`VOICE='hype'`), and the
  DOPAMINE rules. Copy the matching `episodes/20261113_*.py` for each format. The old "same cartoon every time" style is retired.

## 1. Setup (fresh session)
```
git clone https://github.com/suliyeex-tech/videos /home/claude/videos   # or git pull if it is already there
sh /home/claude/videos/engine/setup.sh
```

## 2. Research (last 24 h)
- Search the web for the most viral AI-made and animated videos of the last 24 hours on TikTok, YouTube Shorts and Instagram Reels. Note their topics, hooks and format.
- Read STYLE.md and **FORMATS.md** (5 different formats per day, funny influencer names, dopamine rules). Pick **5 new topics**, each riding a different trend of the day: any kind of viral AI content
  (survival "what if" stories, 2nd-person mystery stories, AI characters, science "what happens if", funny AI
  scenarios…), all in English. Never repeat a topic that already has a file in `episodes/` or `longform/episodes/`.
- When the trend is a survival "what if" story, use the cartoon format below; otherwise adapt the episode
  (it does not need every element, but it always needs a hook in the first 2 seconds and a payoff or cliffhanger):
  - a named character with an age and a place,
  - a "THE RULE" card,
  - a "STUPID MISTAKE" beat,
  - real facts, each with a `REAL ·` badge,
  - a Part 2 cliffhanger.
- Verify every fact with a web search before using it. Put the source in the YouTube description.

## 3. Write the episodes
- Set `VOICE` and `SPEED` at the top of the episode to the voice of the day (STYLE.md; fast and cheerful, speed >= 1.0).
- Copy an existing file from `episodes/`, for example `e03_sinking_car.py`, and name the new one `episodes/YYYYMMDD_eNN_<topic>.py`.
- Each file defines:
  - `SLUG` (start it with the date),
  - `TITLE`, `INFO`, `LINES`, `CAPS`, `MOOD`,
  - the shot functions,
  - `timeline(ls, dur)`, `SFX(ls, dur)`, `NOZOOM` and `POST`.
- Caption markup in `CAPS`:
  - `{text}` is red,
  - `[text]` is yellow,
  - a leading `!` makes a big punch line.
- Keep each video at 40–50 s and about 13–14 voice lines.
- `engine/kit.py` provides the drawing kit:
  - `person`/`Look`, `rule_card`, `end_card`, `statbox`, `fact`, `namecard`, `pill`, `header`,
  - `rotated`, `rain`, `stars`, `streaks` and the easing helpers.

## 4. Render and check
```
cd /home/claude/videos/engine
python3 run.py ../episodes/<file>.py tts     # voice: set VOICE/SPEED in the episode to match the day's viral style (STYLE.md)
python3 run.py ../episodes/<file>.py sheet   # contact sheet in /home/claude/work/<slug>/sheet.jpg. LOOK at it and fix overlaps first
python3 run.py ../episodes/<file>.py all     # renders and mixes (-14 LUFS); output goes to out/<slug>.mp4
```

## 5. Host
- `git add episodes out/<new files> && git commit && git push`
- The public URL is `https://raw.githubusercontent.com/suliyeex-tech/videos/<commit-sha>/out/<slug>.mp4`.
- Always use the commit SHA, not `main`. Do NOT use jsDelivr (`...@sha` URLs): Zernio encodes the `@` as `%40` and the upload fails with "Failed to fetch video source: 400".

## 6. Publish with Zernio: 1 video per hour, 18:00Z to 22:00Z (19:00 to 23:00 Madrid)
- `mcp__Zernio__call_tool` name `posts_create_post`, one post per video:
  - `media_items: [{type: "video", url: <raw.githubusercontent.com URL with the commit SHA>, mimeType: "video/mp4"}]`
  - `scheduled_for`: the slot in UTC (winter 18:00Z…22:00Z, summer 17:00Z…21:00Z)
  - platforms: TikTok `6af5fc430c1b54f421bc4837` (caption + hashtags + #fyp), Instagram `6af5fc55f318bbc43a0fe3d3`
    (caption + hashtags + #reels), YouTube `6af5fcdd2fd432bb239b9515` (platformSpecificData.title ending in #shorts,
    caption + sources + hashtags + #shorts)
  - `tiktok_settings: {privacyLevel: "PUBLIC_TO_EVERYONE", allowComment: true, allowDuet: true, allowStitch: true,
    commercialContentType: "none", contentPreviewConfirmed: true, expressConsentGiven: true, videoMadeWithAi: true}`
- Mix the order: interesting, funny, suspense, interesting, funny (never two of the same format back to back).
- Fallback only if Zernio fails: Upload-Post `upload_video` (Instagram user `default`, YouTube user `@ifitvanishedd`).
  Never retry a plan-limit refusal and never pay or upgrade anything.
- Report every video, platform and time to the owner. Say plainly what could not be published and why.
