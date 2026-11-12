#!/bin/sh
# One-time setup for a fresh session: python deps + Kokoro TTS model files.
set -e
pip install --break-system-packages -q kokoro-onnx soundfile scipy opencv-python-headless pillow numpy 2>&1 | tail -1 || true
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
T=${TTS_DIR:-/home/claude/tts}; mkdir -p "$T"
[ -s "$T/kokoro.onnx" ] || curl -sSL -o "$T/kokoro.onnx" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s "$T/voices.bin" ] || curl -sSL -o "$T/voices.bin" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
ls -la "$T"
