#!/bin/sh
# One-time setup for a fresh session: python deps + Kokoro TTS model files.
set -e
pip install --break-system-packages -q kokoro-onnx soundfile scipy opencv-python-headless pillow numpy 2>&1 | tail -1 || true
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
T=${TTS_DIR:-/home/claude/tts}; mkdir -p "$T"
[ -s "$T/kokoro.onnx" ] || curl -sSL -o "$T/kokoro.onnx" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s "$T/voices.bin" ] || curl -sSL -o "$T/voices.bin" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
ls -la "$T"

# ---- 2026-11-15 owner: new animation tools (HyperFrames, Lemo-Opuscar, Claude Animation Base, Paper Shaders). See TOOLS.md.
TL=/home/claude/tools; mkdir -p "$TL"
for r in heygen-com/hyperframes lemomo-ai/lemo-opuscar JohnHeibel/ClaudeAnimationBase paper-design/shaders; do
  d="$TL/$(basename $r)"; [ -d "$d/.git" ] || GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 https://github.com/$r "$d" || true
done
(cd /tmp && timeout 300 npx -y hyperframes skills update >/dev/null 2>&1) || true      # HyperFrames skills for Claude Code
(cd "$TL/lemo-opuscar" && timeout 600 sh plugin/skills/lemo-opuscar/scripts/setup.sh deps >/dev/null 2>&1) || true
(cd "$TL/ClaudeAnimationBase" && timeout 300 npm install --silent >/dev/null 2>&1) || true
(cd "$TL" && [ -d node_modules/@paper-design/shaders ] || timeout 300 npm i --silent @paper-design/shaders >/dev/null 2>&1) || true
echo "tools ready in $TL"

# ---- 2026-11-18 owner: Blender (bpy) for the blocky "In this town" format. See TOOLS.md.
(timeout 400 pip install --break-system-packages -q bpy >/dev/null 2>&1 && echo "bpy ready") || echo "bpy install failed"

# ---- 2026-11-18 owner: open-higgsfield-skills (pinned). See HIGGSFIELD.md.
HG=$TL/open-higgsfield-skills; HGC=5a1a2d492540d349a2d84d413e4b71f88aa94519
[ -d "$HG/.git" ] || git clone -q https://github.com/mojomast/open-higgsfield-skills "$HG" || true
(cd "$HG" && git fetch -q --depth 1 origin $HGC 2>/dev/null; git checkout -q $HGC) || true
mkdir -p ~/.claude/skills && cp -rn "$HG"/skills/* ~/.claude/skills/ 2>/dev/null || true
echo "open-higgsfield-skills ready in $HG (export HIGGS=$HG)"
