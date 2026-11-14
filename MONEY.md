# Growth & monetization plan (owner decision 2026-11-13)

Goal: get paid. This file overrides DAILY.md / FORMATS.md where they disagree.


## OWNER FEEDBACK 2026-11-14 (overrides everything below; read REFERENCES.md "E" first)
The owner said the last shorts are boring: (1) a "tic tic tic" in the background (removed from the engine: caption ticks,
clock ticks and hi-hats are gone; NEVER add a tick/clock/hi-hat sound again, also not for quiz timers), (2) boring stories
(e.g. the Chad Gainsworth gym/landlord chat stories get no views), (3) the voice is boring and slow, (4) the videos don't
grab you in the first seconds. He sent a viral reference he loves (REFERENCES.md E: "La vida de Víctor"). From now on:
- **STORY FIRST, not facts.** Every short is a story about ONE funny, flawed character with a concrete GOAL and a DEADLINE,
  said in the first sentence: "This is <Name>. He has 28 days to <goal>." Facts may appear only as jokes inside the story.
  No lecture/explainer videos (neon psychology lectures, fact lists read aloud, "scientists say..." intros). Chat-story
  influencer drama (Chad) is retired: no new chat stories; Chad Part 3 is NOT to be made unless his Part 2 beats 1,000 views.
- **HOOK in 1 s:** first frame = a big close-up of the character in their worst state (visual gag: flies, stink lines,
  pimples, mess) + the first line names him and his impossible goal. No title cards, no "What if..." intros, no logos.
- **Interactive series "YOU DECIDE"** (new `vote` format, FORMATS.md) is now the main shorts series: Day N; the viewers'
  A/B comment choice from the previous part is what happens in this part; stats cards change on screen; ends with
  "You decide: A ... or B ... Comment and we'll see it tomorrow." Use the REAL comment majority from Zernio
  (comments_list_inbox_comments); if there are no votes, say "You didn't vote, so <character> chose..." (never invent vote
  percentages or fake viewer comments: the reference shows fake vote counts, WE DON'T).
- **Writing:** short sentences (3–10 words), deadpan punchlines every 2–3 sentences ("He still smells bad. But now he smells
  bad with style."), numbers on screen that move (probability %, kg, days left, money). ~190–220 wpm WITH natural pauses
  between sentences (gap 0.25–0.4 s), not one breathless run-on.
- **Voice:** use VOICE='story' (am_puck 60% + am_fenrir 40%, speed 1.3) = the most expressive male blend measured; or
  'storyuk' (bm_fable, the most expressive voice measured) for variety. Never 'hype' (am_echo is flat), 'suspense' or
  'classic' for stories. Female narrator: af_heart at 1.25.
- **Look:** polished flat vector (like E): one character always centred, cosy detailed rooms (night palette purple/blue,
  fairy lights, desk, posters), small white karaoke subtitles 1–2 words at a time (CAPTION='sub'), ONE stat card at the top
  that changes every 3–5 s, recurring background gags (a sleeping pet, flies), scene change every 4–6 s.
- **Music:** light, quiet bed (MOOD style 'funny' or 'cinematic'), no drums ticking; SFX only on real events (pop on
  stat change, whoosh on scene change, ding on good news, record-scratch on fails).
- **Per run:** at least 1 `vote` episode (shorts A starts the first series and builds engine/formats/vote.py if it does not
  exist yet; every later run continues it with the next Day). The other slots: character stories with goal + deadline in
  other formats (cartoon survival, stickpov horror, sim3d with a character, map list told through a character). The
  '4 different genres/formats' rule still applies to the rest.
- Still 61–80 s for TikTok rewards: a Day episode = recap (5 s) + 4–6 beats + stats + A/B ending.

## CHANNEL NAME IS NOT THE CONTENT (owner 2026-11-13, overrides everything)
- The owner is renaming the channels to something totally different and funny. The content is "a bit of everything":
  never shape topics, titles, hooks or captions around "What if it vanished" or any channel name.
- "What if..." is just ONE of many title formulas; use it only when it is the best hook for that video.
- Never say or show the channel name in videos, captions, titles or descriptions (it may change again). Say "follow for Part 2",
  "full story on the channel", etc. Account IDs in Zernio stay the same after a rename; usernames/handles may change, ignore them.
- Playlist names stay generic by genre; the "What If It Vanished? | ..." prefix will be renamed by the owner.

## Owner's favourite reference videos
- 2026-11-14: owner added reference F ("1 MINUTE", Last Soul): QUALITY over quantity of gimmicks — storytelling music that builds, intensity, suspense about what will happen, a message, polished animation. See REFERENCES.md F (full breakdown from the file the owner sent). Long-form must set MUSIC_ARC/MUSIC_MOOD (music with an arc, silence before reveals, peak at the payoff).
- Read REFERENCES.md every run: at least 1 video per run in the style of one of them (original story and visuals).

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
