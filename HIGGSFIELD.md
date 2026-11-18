# open-higgsfield-skills in Oddwick (owner 2026-11-18) — how and when to use it

Owner: "install and use https://github.com/mojomast/open-higgsfield-skills for this content from now on; mix Google Colab
and the no-GPU parts; when I'm not here it must be automatic, as long as it is free."

The pack (37 skills, `video-director` on top) turns a shot plan into AI stills and video with open-weights models on a
ComfyUI GPU server. Our cloud sessions have NO GPU (2 CPU, 7 GB RAM), so we split the work:

| part | where | cost | who |
|---|---|---|---|
| story, script, voice (Kokoro), music + SFX (mix.py) | cloud CPU, as today | free | every scheduled run |
| shot plan → `video-director` manifest (`engine/higgsfield/make_manifest.py`) | cloud CPU | free | every scheduled run |
| AI stills (FLUX.2 Klein 4B, Apache-2.0) | Google Colab free T4 (`engine/higgsfield/colab_bundle.py`) | free, but the OWNER presses Run | owner, when present |
| camera moves on the stills, Oddwick host, captions, assembly (`film-assembly`), QC (`shot-qc`) | cloud CPU (`engine/higgsfield/animate_stills.py`) | free | every scheduled run |
| AI video shots (LTX-2.5) | needs ≥24 GB GPU (L4/A100, paid Colab or other) | NOT free | only if the owner says so |

Installed by `engine/setup.sh` at a pinned commit into `/home/claude/tools/open-higgsfield-skills` and copied into
`~/.claude/skills/` (skills load from there in later sessions; in the same session read `skills/<name>/SKILL.md` directly).

## Rule 1 — unattended runs (owner away): never wait for a GPU, never pay
1. Make the Shorts exactly as PLAYBOOK.md says (HyperFrames / Blender / Claude Animation Base). Nothing changes there.
2. Also run the pack's free CPU checks on every finished Short before scheduling it:
   `python3 $HIGGS/skills/shot-qc/scripts/shot_qc.py out/<slug>.mp4 --duration <s> --ratio 9:16 --audio --json`
   (fails on freeze/black frames; a fail = fix or drop, like the MONEY.md quality gate).
3. Colab stills waiting? If the owner ran a Colab bundle, its outputs land in Google Drive
   (`MyDrive/<slug>-google-colab-outputs*`). Look with the Google Drive connector (search the slug). If found: download,
   `python3 $HIGGS/skills/google-colab-runner/scripts/colab.py ingest <manifest> <zip>` (or unzip into work/<slug>/stills),
   then `animate_stills.py <manifest> --stills <dir> --music work/<slug>/mix.wav` and publish it in one of the day's slots
   (it counts as one of the 3 Shorts, never a 4th). If nothing is there, carry on without it.
4. Every run, prepare ONE Colab-ready episode for the owner (see Rule 2, steps 1-3) and list it in the report:
   "Colab bundle ready: <link to the .ipynb in the repo>".
5. Never start a paid GPU, never ask for credits, never wait.

## Rule 2 — owner present: the Colab round trip (free T4, ~15-25 min)
1. Script + voice as usual: `engine/oddwick/voice.py episodes/higgsfield/<ep>.json` (≈220 wpm).
2. One shot per narration line in `episodes/higgsfield/<ep>.shots.json` (`still` = the end-state picture, `video` = motion
   only, `camera`, `cast`). Then `python3 engine/higgsfield/make_manifest.py <ep>.json <ep>.shots.json <ep>.manifest.json`
   and `python3 $HIGGS/skills/video-director/scripts/direct.py validate <ep>.manifest.json`.
3. `python3 engine/higgsfield/colab_bundle.py <ep>.manifest.json --out colab/` → commit `colab/<slug>-google-colab/<slug>.ipynb`.
4. Owner: open the notebook in Colab (File > Upload notebook, or "Open in Colab" from GitHub), Runtime > T4 GPU, OUTPUT = drive,
   Run all. ~5 GB of models download, then 15 stills. Release the runtime at the end (cell 11).
5. Next run (or now): Rule 1 step 3 picks them up from Drive, animates, mixes, QCs and publishes.
- Optional free preview before Colab: `python3 -I engine/higgsfield/cpu_preview_stills.py <manifest> work/preview_stills`
  (SD-Turbo on CPU, ~45 s/still, rough, NOT for publishing).

## Brand rules that the pack must follow
- Oddwick (the candle) is NEVER AI-generated: `animate_stills.py` composites brand/oddwick_avatar.png (lights up at the
  start, small in a corner, big again at the A/B ending, blows out on the last frame).
- The style string and cast descriptors in make_manifest.py are pasted verbatim into every still prompt, so the same cast
  looks the same every time. Add new recurring characters there, once.
- Voice, music and SFX stay ours (Kokoro + mix.py), never Chatterbox/ACE-Step, so every video sounds the same.
- Licences: FLUX.2 Klein 4B + Qwen3-4B encoder = Apache-2.0. LTX-2.x video weights = Lightricks LTX-2 Community License
  (not open source; read it before monetised use). Never use FLUX.2 Klein 9B (non-commercial).

## Example (2026-11-18): "Why Fire Stations Have Poles"
episodes/higgsfield/firepole.{json,shots.json,manifest.json}, Colab bundle in colab/. A CPU-stills preview was sent to the owner
(not committed, not publishable). Facts: Smithsonian, Mental Floss, Wikipedia "Fireman's pole" (horse/spiral-stair link is "the story
goes": some historians dispute it).
