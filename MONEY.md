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

## Learn from data (every run)
- Read LEARNINGS.md (written by the weekly report) and lean into the formats/topics that retain and convert best; drop the worst.

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
