"""PREVIEW ONLY: rough AI stills on CPU (no GPU, free) with SD-Turbo, so the owner can see a shot list before spending a
Colab session. ~45 s per 512x896 still on the 2-CPU cloud container. Not for publishing: the published look comes from
FLUX.2 Klein on Colab (colab_bundle.py). SD-Turbo weights: Stability AI Community License (check before any commercial use).
python3 -I cpu_preview_stills.py <manifest.json> <out_dir>
Needs: pip install --break-system-packages torch --index-url https://download.pytorch.org/whl/cpu ; pip install diffusers transformers accelerate"""
import sys, os, json, re, torch
from diffusers import AutoPipelineForText2Image

STYLE = ", flat 2D cartoon, thick dark outlines, simple shapes, night, warm orange candlelight, deep purple shadows, storybook illustration"
m = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
torch.set_num_threads(os.cpu_count() or 2)
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float32)
for sh in m["shots"]:
    f = f"{out}/{sh['id']}_still_preview.png"
    if os.path.exists(f): continue
    desc = sh["still"]["prompt"].replace(m["brief"]["style"], "").strip()
    first = re.split(r"(?<=[.;])\s", desc)[0]                       # CLIP reads only ~77 tokens: subject first
    first = " ".join(first.replace(":", ",").split()[:32]).rstrip(".")
    img = pipe(prompt=first + STYLE, num_inference_steps=3, guidance_scale=0.0, width=512, height=896,
               generator=torch.Generator().manual_seed(sh["still"].get("seed") or 7)).images[0]
    img.save(f); print(sh["id"], first[:70], flush=True)
