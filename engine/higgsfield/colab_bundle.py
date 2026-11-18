"""Oddwick wrapper around open-higgsfield-skills' google-colab-runner `package`.
python3 colab_bundle.py <manifest.json> --out <dir> [--with-video]

Why a wrapper (2026-11-18):
- Default = STILLS ONLY. The free Colab GPU is a T4 (16 GB VRAM, ~12 GB RAM). FLUX.2 Klein 4B stills fit; the LTX-2.5
  video graph (22B + a 12B bf16 text encoder) does not fit a free runtime reliably. The stills are animated on CPU
  afterwards (engine/higgsfield/animate_stills.py). --with-video keeps the LTX jobs for a paid/bigger GPU.
- Audio jobs are always dropped: Oddwick's voice, music and SFX are made on CPU (engine/oddwick/voice.py + mix.py).
- The pack leaves `qwen_3_4b_fp8_mixed.safetensors` (FLUX.2 Klein 4B text encoder) unresolved; we pin it here to
  Comfy-Org/z_image_turbo (same Qwen3-4B, 5.6 GB, Apache-2.0)."""
import os, sys, argparse

PACK = os.environ.get("HIGGS", "/home/claude/tools/open-higgsfield-skills")
sys.path.insert(0, os.path.join(PACK, "skills", "google-colab-runner", "scripts"))
import colab  # noqa: E402

REV = "6fc90a3b1b653e935a0d175e260736de25b84df5"
colab.MODELS["qwen_3_4b_fp8_mixed.safetensors"] = ({
    "dir": "text_encoders", "skills": ["flux3-klein-stills"], "loaders": ["CLIPLoader.clip_name"],
    "license": "apache-2.0 (Qwen3-4B; confirm on the model card)", "repo": "Comfy-Org/z_image_turbo",
    "path": "split_files/text_encoders/qwen_3_4b_fp8_mixed.safetensors", "revision": REV, "bytes": 5631994051, "gated": False,
    "url": f"https://huggingface.co/Comfy-Org/z_image_turbo/resolve/{REV}/split_files/text_encoders/qwen_3_4b_fp8_mixed.safetensors"})

ap = argparse.ArgumentParser()
ap.add_argument("manifest"); ap.add_argument("--out", default="/home/claude/work/colab"); ap.add_argument("--with-video", action="store_true")
a = ap.parse_args()
keep = {"still", "video"} if a.with_video else {"still"}
_build = colab.build_jobs

def build_jobs(m0, tier, mdir):
    m, jobs, notes, assets = _build(m0, tier, mdir)
    dropped = [j["id"] for j in jobs if j["kind"] not in keep]
    jobs = [j for j in jobs if j["kind"] in keep]
    if dropped: notes.append(f"Oddwick wrapper dropped {len(dropped)} jobs ({', '.join(sorted({d.split('_')[-1] for d in dropped}))}); made on CPU instead")
    return m, jobs, notes, assets

colab.build_jobs = build_jobs
sys.exit(colab.package(a.manifest, a.out))
