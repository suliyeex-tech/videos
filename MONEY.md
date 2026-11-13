# Growth & monetization plan (owner decision 2026-11-13)

Goal: get paid. This file overrides DAILY.md / FORMATS.md where they disagree.

## Targets (check progress weekly)
- YouTube Partner Program, lower tier (fan funding): 500 subs + 3 public uploads in 90 days + (3,000 watch hours in 12 months OR 3M Shorts views in 90 days).
- YouTube Partner Program, full (ads): 1,000 subs + (4,000 watch hours in 12 months OR 10M Shorts views in 90 days).
  From 2027-02-01 new channels need 8,000 hours or 20M Shorts views. **Get in before then.** Long-form watch hours are the realistic path.
- TikTok Creator Rewards: 10k followers, 100k views in 30 days, only videos LONGER than 60 s count (check the app for whether Spain is eligible).
- Instagram: gifts at 500 followers, subscriptions at 10k; real money there = brand deals + affiliates.

## Biggest risk: YouTube "inauthentic / mass-produced / repetitive content"
Channels made of templated AI videos get refused for ads. So:
- **Owner decision 2026-11-13 (late): as many shorts as are worth it = 8 per day (2 runs of 4), all 61–80 s, plus 2 long-form videos per day.** Scale up/down only on weekly data (LEARNINGS.md). Each one a distinct idea with its own angle, joke and twist; never a template clone with swapped words.
- Every video needs a clear point of view (an opinion, a surprising comparison, a joke only this channel makes), not a read-aloud of facts.
- Recurring named series ("What if it vanished?", "If X happens while you're at Y", "Chat stories") so the channel has a recognizable identity.
- Mark realistic synthetic media as AI (madeWithAi / videoMadeWithAi true). Never misleading, never fake news.

## Shorts → long-form funnel
- Shorts exist to bring people to the long video. Where it fits, the last line says something like
  "The full story is on our channel" or "Part 2 drops tomorrow". Never lie about content that doesn't exist.
- Same themes as the long-form so a Short viewer wants the long one.

## TikTok >60 s
- ALL daily shorts are 61–80 s (verify with ffprobe), so they count for TikTok Creator Rewards. Pick story-shaped ideas that
  can hold 60+ s (chat stories, POV, cartoon survival, countdowns, tier lists); retention beats length, so no filler.
  The same file goes to Reels and YouTube Shorts (both accept up to 3 min).
- Use "Part 1 / Part 2" series to earn follows.

## Improve EVERY day (owner: "hay que ir mejorando todos los días, muy importante")
- Every run (shorts A/B, long A/B) starts with a 5-minute DAILY REVIEW: mcp__Zernio__analytics_get_analytics for the last
  3 days (sort by views, all platforms) and compare with LEARNINGS.md. Append 1–3 dated lines under "## Daily notes" in
  LEARNINGS.md (what won, what flopped, one change you are making today), git pull --rebase, commit, push.
- Then apply it: copy the hook/title pattern, genre, length and slot of the top videos; never repeat what flopped twice.
- Each run must change at least ONE thing vs the previous run on purpose (hook style, title formula, thumbnail, length,
  pacing, music, voice) and note it in Daily notes, so we learn what moves the numbers.
- The weekly report (Sunday) condenses the Daily notes into the rules at the top of LEARNINGS.md.

## Daily schedule (Madrid time; English audience is mostly US/UK, US Eastern = Madrid − 6 h)
- Shorts run A (starts 06:33): slots 13:00, 15:00, 17:00 and 01:00 (next day, = 19:00 New York prime time).
- Shorts run B (starts 12:33): slots 19:00, 20:00, 22:00, 23:00.
- Long-form A (starts 08:37): 21:00 Madrid (15:00 New York). Long-form B (starts 14:37): 18:00 Madrid (12:00 New York).
- Per-slot guard: before making a video for a slot, check Zernio for a post already scheduled at that exact time on that platform; if there is one, skip that slot.

## Genres and voices (owner request: all styles, voice matches the style, always FAST)
Rotate across many genres, never only three: funny/comedy, interesting/science, horror/creepy, mystery, survival,
psychology, history, space, animals/nature, food, money facts (no advice), sports/records, gaming-style, chat drama,
quiz/tier list, satisfying/sims, motivational, "would you rather"/choices. Each run: 4 different genres + 4 different formats.
Voice by genre (keys in engine/run.py VOICES; set SPEED in the episode, never below 1.15):
- funny / chat drama / influencer stories: 'hype' or 'bro' (cheerful, fast, 1.25)
- interesting / science / space / quiz: 'guy' (lively, fast, 1.22) or 'hype'
- horror / creepy / mystery / POV suspense: 'suspense' at SPEED 1.15–1.2 (dark but fast), tension music
- history / documentary: 'old' (British) at 1.15–1.2
- female-narrator trends (relationship, lifestyle, "my mom..." stories): 'girl' or 'mom' at 1.2
Use a different voice than the previous slot when possible.

## Series (Part 1 → Part 2 → Part 3)
- See SERIES.md. Each run should make at least 1 Part 2/3 of an earlier Part 1 (prefer the Part 1 with the most views in
  Zernio analytics) and at most 1 new Part 1. Only end a video with "Part 2" if its Part 2 is planned in SERIES.md.

## Topic claiming (4 tasks run each day)
- Right after choosing topics, append them to TOPICS.md (date, task, topic), git pull --rebase, commit, push. Never pick a
  topic already in TOPICS.md, episodes/ or longform/episodes/.

## YouTube playlists (created 2026-11-13) — put EVERY new YouTube upload in one
Pass platformSpecificData.playlistId in posts_create_post (or posts_update_post_metadata playlist_id after publishing):
- PLZAdnXuDrMpg  "What If It Vanished? | Science What-Ifs"  (science, space, psychology, tech, history, animals)
- PLfKTN3t7rM-g  "Would You Survive? | Survival What-Ifs"   (survival, "if you were...", deadly-mistake)
- PLDFFSLtQWAZo  "3 AM Stories | Creepy POV & Mysteries"     (horror, mystery, POV suspense, 2nd-person stories)
- PLSI0CBh67sig  "Influencer Chaos | Funny Chat Stories"     (funny, chat stories, influencer characters)
Create a new playlist (connect_create_youtube_playlist, public) only for a new genre with 3+ videos, and add it here.
Long-form descriptions: first line = hook; add "▶ More: <playlist name>" and the chapters. Short descriptions mention the
related long video by title when one exists.

## Engagement (every run, 5 min)
- mcp__Zernio__comments_list_inbox_comments for the last 3 days: reply to every new genuine comment (max 20 per run) in
  English, short, friendly, in the channel's voice, ideally with a question back or a "Part 2 is coming" when true.
  Never spam, never argue, never reply to hateful comments (hide them if the tool allows).
- Pinned-comment style CTA in captions: ask a specific A/B question ("Comment A or B"), not "like and subscribe".

## Duplicates
- NEVER publish the same video twice on one platform. 2026-11-13: duplicates YbAEAV1HI1E and 4_tdCUuq2ao set to private;
  8_M3WwVgJow still public (owner to make it private in YouTube Studio).
