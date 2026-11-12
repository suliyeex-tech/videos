# Daily "What If" shorts: 5 videos, 19:00 to 23:00 Madrid

This is the routine the scheduled task follows every day. The account owner asked for it to run without any input from them.

## 1. Setup (fresh session)
```
git clone https://github.com/suliyeex-tech/videos /home/claude/videos   # or git pull if it is already there
sh /home/claude/videos/engine/setup.sh
```

## 2. Research (last 24 h)
- Search the web for the most viral AI-made and animated videos of the last 24 hours on TikTok, YouTube Shorts and Instagram Reels. Note their topics, hooks and format.
- Read STYLE.md. Pick **5 new topics**, each riding a different trend of the day: any kind of viral AI content
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
python3 run.py ../episodes/<file>.py tts     # voice: 50% am_onyx + 50% am_puck (see STYLE.md)
python3 run.py ../episodes/<file>.py sheet   # contact sheet in /home/claude/work/<slug>/sheet.jpg. LOOK at it and fix overlaps first
python3 run.py ../episodes/<file>.py all     # renders and mixes (-14 LUFS); output goes to out/<slug>.mp4
```

## 5. Host
- `git add episodes out/<new files> && git commit && git push`
- The public URL is `https://raw.githubusercontent.com/suliyeex-tech/videos/<commit-sha>/out/<slug>.mp4`.
- Always use the commit SHA, not `main`. Do NOT use jsDelivr (`...@sha` URLs): Zernio encodes the `@` as `%40` and the upload fails with "Failed to fetch video source: 400".

## 6. Publish: 1 video per hour, 18:00Z to 22:00Z (19:00 to 23:00 Madrid)
- **Socialync** is the first choice. It posts to Instagram, YouTube and TikTok in one call.
  - Run `validate_post`, then `publish_scheduled`.
  - Settings: `tiktokPrivacyLevel PUBLIC_TO_EVERYONE` and `aiGenerated: true` on every platform.
  - Per-platform `customCaption`: add `#fyp` on TikTok and `#shorts` plus the sources on YouTube. Add `#reels` to the base caption.
  - The free plan allows only 5 posts per **month** (it resets on the 1st). If it answers `plan_limit_reached`, fall back to Upload-Post.
- **Upload-Post** is the fallback. It covers Instagram and YouTube only, because the free plan has no TikTok.
  - Use `upload_video` with `videoPathOrUrl` set to the jsDelivr URL, `scheduledDate` and `confirmed: true`.
  - Instagram: user `default`, `instagramMediaType REELS`, `instagramIsAiGenerated`.
  - YouTube: user `@ifitvanishedd`, `youtubePrivacyStatus public`, `youtubeContainsSyntheticMedia`.
- Report every video, platform and time to the owner. Say plainly what could not be published and why.
