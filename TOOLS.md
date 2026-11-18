# Animation tools (owner request 2026-11-15) — installed by engine/setup.sh into /home/claude/tools

Use them to raise quality; the old Python formats stay as fallback only.

| Tool | What it is | Use it for |
|---|---|---|
| HyperFrames (`npx hyperframes`) | Write HTML/CSS/JS (GSAP) → MP4. `init`, `check`, `render`, `beats`, `audio`. Tested OK in the cloud container (10 s render ≈ 22 s, software GPU). | Main engine for Shorts/Reels/TikTok: kinetic captions, UI/chat/game overlays, map zooms, 9:16 and 16:9. Read its CLAUDE.md/AGENTS.md before building. |
| Lemo-Opuscar (`tools/lemo-opuscar`) | 66 film styles in code (keynote, whiteboard, retro CRT…). Read DIRECTOR.md + MY-STYLES.md. | Explainers and long-form chapters; pick ONE style per video and keep it consistent. |
| Claude Animation Base (`tools/ClaudeAnimationBase`) | Hand-painted p5.js + p5.brush character animation. Read ANIMATION_GUIDE.md; `node render.mjs --clip --out=...`. | Story Shorts with a recurring ORIGINAL character, and the kids channel. Never use its demo mascot in published videos; design our own characters. Avoid watercolour fills (slow without GPU). |
| Blender (`pip install --break-system-packages bpy`, Python module, headless) | Real 3D: blocky toy-town characters and sets for the "In this town" format. Starter: engine/blocktown/town_starter.py (+ .png). | Tested 2026-11-18 in the cloud container (2 CPU, no GPU): Cycles 12-24 samples + denoise ≈ 5-10 s per 576x1024 frame; EEVEE works but is slower here (software GL). Budget: render at 432x768 or 576x1024, 12-15 fps for held shots, 24 fps only for fast moves, upscale with ffmpeg; one ~90 s video ≈ 1-2 h, so start it first. Gotcha: `transform_apply` defaults to location=True, which moves every pivot to the world origin; use `transform_apply(location=False, rotation=False, scale=True)`. |
| Paper Shaders (`@paper-design/shaders`) | Animated backgrounds: gradients, grain, halftone, liquid metal. | Backgrounds inside HyperFrames compositions (never as the whole video). |

Rules: storyboard first → contact sheet → LOOK at it → fix → render. Every Short must pass the QUALITY GATE in MONEY.md before it is scheduled.
