"""Build an open-higgsfield-skills (video-director) manifest from an Oddwick episode.
python3 make_manifest.py <episode.json> <shots.json> <out_manifest.json>
- episode.json: the usual Oddwick episode (slug, title, lines). Voice timing is read from /home/claude/work/<slug>/vo.json
  (run engine/oddwick/voice.py first), so every shot lasts exactly as long as its narration line (+ gap).
- shots.json: one entry per line: {"still": <end-state picture>, "video": <motion only>, "static": bool, "cast": [...]}
The style and cast descriptors below are pasted verbatim into every still prompt (story-bible rule)."""
import json, sys, datetime

STYLE = ("Flat 2D cartoon illustration with thick dark-purple outlines and simple rounded shapes, characters with "
         "simple dot eyes and small expressive mouths, inside a softly lit toon 3D set. Night scene told by candlelight: "
         "warm candle-orange light against deep purple and blue shadows. Clean, bold, readable at phone size. "
         "Vertical 9:16 composition, subject in the middle third. No text, no letters, no logos, no watermark.")
CAST = {
    "kenyon": "Captain Kenyon, a tall 1870s fire captain, light skin, square jaw, bushy brown mustache, red leather "
              "fire helmet, navy wool coat with two rows of brass buttons",
    "reid": "the buddy, a short broad 1870s firefighter, dark brown skin, round cheerful face, short black beard, "
            "red flannel shirt with suspenders",
    "horse": "a chunky cartoon fire horse, chestnut brown, white blaze on the nose, black mane, big curious eyes",
    "mocker": "a lanky smug firefighter from a rival station, pale skin, long thin nose, slicked black hair, "
              "green-trimmed grey coat",
    "chief": "a stern round fire chief, grey sideburns, white fire helmet, long black coat",
}

def main(ep_path, shots_path, out_path):
    ep = json.load(open(ep_path)); shots_in = json.load(open(shots_path))
    vo = json.load(open(f"/home/claude/work/{ep['slug']}/vo.json"))
    lines = vo["lines"]; assert len(lines) == len(shots_in) == len(ep["lines"]), "one shot per narration line"
    total = round(vo["total"] + 0.6, 2)  # 0.6 s tail for the end beat
    shots = []
    for i, (L, S) in enumerate(zip(lines, shots_in)):
        start = 0.0 if i == 0 else lines[i]["start"]
        end = lines[i + 1]["start"] if i + 1 < len(lines) else total
        cast_txt = " ".join(CAST[c] + "." for c in S.get("cast", []))
        shots.append({
            "id": f"s{i+1:02d}", "beat": S.get("beat", ""), "start_s": round(start, 3), "duration_s": round(end - start, 3),
            "type": S.get("type", "action"), "framing": S.get("framing", "medium"),
            "camera": "static locked-off" if S.get("static") else S.get("camera", "slow push-in"),
            "cast": S.get("cast", []), "location": S.get("location", "firehouse"),
            "narration": L["text"], "sfx": S.get("sfx"), "chain_from": None, "transition_in": "cut",
            "still": {"route": "still.flux2_4b", "status": "pending",
                      "prompt": f"{STYLE} {S['still']} {cast_txt}".strip(), "seed": 1000 + i},
            "video": {"route": "video.i2v", "status": "pending", "prompt": S["video"], "seed": 2000 + i},
            "status": "pending"})
    m = {
        "schema_version": "1.0", "created": datetime.datetime.now().isoformat(timespec="seconds"), "id": ep["slug"],
        "brief": {"prompt": ep["title"], "kind": "story", "length_s": total, "aspect": "9:16", "fps": 24,
                  "style": STYLE,
                  "audio": {"narration": True, "music": True, "sfx": True, "lip_sync": False, "music_file": None, "language": "en"},
                  "captions": "burned", "deliverables": ["9:16"], "commercial_use": True,
                  "defaults_used": ["Oddwick: voice, music and SFX are made on CPU (Kokoro + engine/oddwick/mix.py), not on the GPU",
                                    "Oddwick host is composited from brand/oddwick_avatar.png, never generated"]},
        "target": {"kind": "google_colab", "url": "", "gpu": "T4 (free)", "vram_gb": 16,
                   "budget": {"max_gpu_minutes": 60, "max_credits": 0, "credit_unit": "Google Colab compute units (free tier: 0 paid)",
                              "deadline_minutes": 120}},
        "tier": "draft", "tier_reason": "free Colab T4 = 16 GB, so draft tier (FLUX.2 Klein 4B stills, LTX at small size)",
        "caps": {"still_retries": 1, "still_variants": 1, "video_retries": 0, "continuity_regens": 0,
                 "max_renders": 40, "max_gpu_minutes": 60, "pass_mean": 3.0, "pass_min": 2},
        "gates": {"bible": "auto", "plan": "auto", "spend": "human", "final": "human"},
        "stages": {k: "pending" for k in ["preflight", "bible", "plan", "stills", "video", "continuity", "audio", "post", "assembly", "critique"]} | {"intake": "done", "bible": "done", "plan": "done"},
        "bible": {"path": "episodes/higgsfield/firepole.manifest.json", "logline": ep["title"], "cast": [{"id": k, "descriptor": v, "ref_image": None, "seed": None} for k, v in CAST.items()],
                  "style": STYLE, "lut": None, "voice": "Oddwick narrator: Kokoro am_puck 60% + am_fenrir 40%, ~220 wpm (CPU)"},
        "shots": shots,
        "audio": {"voiceover": {"route": "audio.voice", "status": "done", "params": {"note": "made on CPU with engine/oddwick/voice.py"}, "seed": 0}},
        "post": [],
        "assembly": {"status": "pending", "xfade": 0, "beats_file": None, "captions": "burned",
                     "exports": [{"aspect": "9:16", "method": "crop", "file": None}], "output": None},
        "cost": {"renders": 0, "estimate_gpu_minutes": None, "actual_gpu_minutes": 0, "rates_s_per_render": {},
                 "rates_note": "default rates in direct.py are unverified assumptions"},
        "log": []}
    json.dump(m, open(out_path, "w"), indent=1)
    print(out_path, len(shots), "shots", total, "s")

if __name__ == "__main__":
    main(*sys.argv[1:4])
