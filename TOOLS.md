# Animation tools (owner request 2026-11-15) — installed by engine/setup.sh into /home/claude/tools

Use them to raise quality; the old Python formats stay as fallback only.

| Tool | What it is | Use it for |
|---|---|---|
| HyperFrames (`npx hyperframes`) | Write HTML/CSS/JS (GSAP) → MP4. `init`, `check`, `render`, `beats`, `audio`. Tested OK in the cloud container (10 s render ≈ 22 s, software GPU). | Main engine for Shorts/Reels/TikTok: kinetic captions, UI/chat/game overlays, map zooms, 9:16 and 16:9. Read its CLAUDE.md/AGENTS.md before building. |
| Lemo-Opuscar (`tools/lemo-opuscar`) | 66 film styles in code (keynote, whiteboard, retro CRT…). Read DIRECTOR.md + MY-STYLES.md. | Explainers and long-form chapters; pick ONE style per video and keep it consistent. |
| Claude Animation Base (`tools/ClaudeAnimationBase`) | Hand-painted p5.js + p5.brush character animation. Read ANIMATION_GUIDE.md; `node render.mjs --clip --out=...`. | Story Shorts with a recurring ORIGINAL character, and the kids channel. Never use its demo mascot in published videos; design our own characters. Avoid watercolour fills (slow without GPU). |
| Paper Shaders (`@paper-design/shaders`) | Animated backgrounds: gradients, grain, halftone, liquid metal. | Backgrounds inside HyperFrames compositions (never as the whole video). |

Rules: storyboard first → contact sheet → LOOK at it → fix → render. Every Short must pass the QUALITY GATE in MONEY.md before it is scheduled.
