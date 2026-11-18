"""CPU half of the Oddwick x open-higgsfield pipeline (free, runs in every scheduled session).
python3 animate_stills.py <manifest.json> [--stills DIR] [--out out/<slug>.mp4] [--music mix_or_bed.wav]

1. Per shot: take the AI still made on Colab (DIR/<sid>_still*.png, from colab.py ingest or the outputs zip).
   If there is no still yet, draw a storyboard card instead (animatic preview).
2. Animate it on CPU with a gentle camera move picked from shot.camera (push-in, tilt, pan, crane, static drift).
3. Oddwick host: composited from brand/oddwick_avatar.png (never AI-generated): lights up in s01, sits in the corner,
   big again in the last shot, and blows out on the final frame.
4. Assemble with the pack's film-assembly (assemble.py, 9:16, voice from /home/claude/work/<slug>/voice.wav).
5. Burn 1-2 word captions (bold white, dark outline, centred) timed from vo.json, then measure with shot-qc."""
import json, os, re, sys, glob, subprocess, argparse, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PACK = os.environ.get("HIGGS", "/home/claude/tools/open-higgsfield-skills") + "/skills"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS = 1080, 1920, 24
STYLE_TXT = [""]
AV = Image.open(f"{REPO}/brand/oddwick_avatar.png").convert("RGBA")

def font(sz, bold=True):
    for p in [f"{REPO}/engine/fonts/{n}" for n in os.listdir(f"{REPO}/engine/fonts")] if os.path.isdir(f"{REPO}/engine/fonts") else []:
        if p.lower().endswith((".ttf", ".otf")) and ("bold" in p.lower() or "black" in p.lower()) == bold:
            return ImageFont.truetype(p, sz)
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)

def avatar_cutout(size):
    """The avatar PNG has a square purple background: keep only the candle via a soft radial-free key on brightness/hue."""
    a = AV.copy().resize((size, size), Image.LANCZOS); px = a.load()
    for y in range(size):
        for x in range(size):
            r, g, b, _ = px[x, y]
            if b > r and b > g and r < 140:  # purple / navy background
                px[x, y] = (r, g, b, 0)
    return a

def card(sh, path):
    img = Image.new("RGB", (W, H), (38, 24, 66)); d = ImageDraw.Draw(img)
    glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse((90, 520, 990, 1420), fill=150)
    img.paste((240, 140, 70), (0, 0), glow.filter(ImageFilter.GaussianBlur(220)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((70, 300, 1010, 1500), 40, outline=(255, 214, 120), width=6)
    d.text((110, 340), f"{sh['id'].upper()}  ·  {sh['framing']}  ·  {sh['camera']}", font=font(38), fill=(255, 214, 120))
    d.text((110, 400), "AI STILL FROM COLAB GOES HERE", font=font(30), fill=(220, 200, 255))
    desc = sh["still"]["prompt"].replace(STYLE_TXT[0], "").strip()
    desc = re.split(r"(?<=\.)\s", desc)[0]
    y = 500
    for ln in textwrap.wrap(desc, 30)[:14]:
        d.text((110, y), ln, font=font(52), fill=(255, 248, 230)); y += 66
    img.save(path)

MOVES = {  # zoompan expressions over n = frame index, N = frames
    "push": ("1.0+0.10*on/N", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
    "tilt": ("1.12", "iw/2-(iw/zoom/2)", "(ih-ih/zoom)*(1-on/N)"),
    "crane": ("1.12", "iw/2-(iw/zoom/2)", "(ih-ih/zoom)*(1-on/N)"),
    "track": ("1.12", "(iw-iw/zoom)*on/N", "ih/2-(ih/zoom/2)"),
    "orbit": ("1.10", "(iw-iw/zoom)*(1-on/N)", "ih/2-(ih/zoom/2)"),
    "static": ("1.03+0.02*on/N", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
}

def move_for(cam):
    c = cam.lower()
    for k, key in (("static", "static"), ("tilt", "tilt"), ("crane", "crane"), ("track", "track"), ("around", "orbit"), ("drift", "orbit")):
        if k in c: return key
    return "push"

def shot_clip(sh, img_path, out, first, last):
    n = max(2, round(sh["duration_s"] * FPS))
    base = Image.open(img_path).convert("RGB")
    # cover-fit to 9:16 at 2x for clean zoompan
    s = max(2 * W / base.width, 2 * H / base.height); base = base.resize((int(base.width * s), int(base.height * s)), Image.LANCZOS)
    l, t = (base.width - 2 * W) // 2, (base.height - 2 * H) // 2; base = base.crop((l, t, l + 2 * W, t + 2 * H))
    tmp = out.replace(".mp4", "_src.png"); base.save(tmp)
    z, x, y = MOVES[move_for(sh["camera"])]
    vf = f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={W}x{H}:fps={FPS}".replace("N", str(n))
    ov = []
    if first or last:  # host big in first/last shot
        av = avatar_cutout(420); av.save(out.replace(".mp4", "_av.png")); ov = ["-i", out.replace(".mp4", "_av.png")]
        fade = f",fade=t=in:st=0:d=0.35:alpha=1" if first else f",fade=t=out:st={max(0.1, sh['duration_s'] - 0.45):.2f}:d=0.4:alpha=1"
        fc = f"[0:v]{vf}[bg];[1:v]format=rgba,loop=-1:1,trim=duration={sh['duration_s']:.3f}{fade}[a];[bg][a]overlay=(W-w)/2:H-h-170:shortest=1,format=yuv420p[v]"
    else:
        av = avatar_cutout(190); av.save(out.replace(".mp4", "_av.png")); ov = ["-i", out.replace(".mp4", "_av.png")]
        fc = f"[0:v]{vf}[bg];[1:v]format=rgba,loop=-1:1,trim=duration={sh['duration_s']:.3f}[a];[bg][a]overlay=W-w-30:40:shortest=1,format=yuv420p[v]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", tmp, *ov, "-filter_complex", fc, "-map", "[v]",
                    "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-profile:v", "high", out], check=True)

def ass_captions(vo, path):
    def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h}:{m:02d}:{s:05.2f}"
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: C,DejaVu Sans,104,&H00FFFFFF,&H00FFFFFF,&H00240E1E,&H64000000,1,0,0,0,100,100,0,0,1,9,3,5,60,60,0,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    ev = []
    for L in vo["lines"]:
        words = L["text"].split(); chunks = []
        while words:
            take = 1 if len(words[0]) > 7 else 2; chunks.append(" ".join(words[:take])); words = words[take:]
        tot = sum(len(c) + 3 for c in chunks); t = L["start"]
        for c in chunks:
            d = L["dur"] * (len(c) + 3) / tot
            txt = c.upper().replace("...", "…")
            if c.strip(".,!?").lower() in ("pole", "stairs", "horses", "hole", "first", "gravity"): txt = "{\\c&H00D7FF&}" + txt
            ev.append(f"Dialogue: 0,{ts(t)},{ts(t + d)},C,,0,0,0,,{{\\pos(540,1180)}}{txt}"); t += d
    open(path, "w").write(head + "\n".join(ev) + "\n")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("manifest"); ap.add_argument("--stills"); ap.add_argument("--out"); ap.add_argument("--music")
    a = ap.parse_args(); m = json.load(open(a.manifest)); slug = m["id"]; STYLE_TXT[0] = m["brief"]["style"]
    wd = f"/home/claude/work/{slug}/hf"; os.makedirs(wd, exist_ok=True)
    out = a.out or f"{REPO}/out/{slug}.mp4"; clips = []
    for i, sh in enumerate(m["shots"]):
        hits = sorted(glob.glob(f"{a.stills}/{sh['id']}_still*.png")) if a.stills else []
        img = hits[0] if hits else f"{wd}/{sh['id']}_card.png"
        if not hits: card(sh, img)
        c = f"{wd}/{sh['id']}.mp4"; shot_clip(sh, img, c, i == 0, i == len(m["shots"]) - 1); clips.append(c)
    film = f"{wd}/film.mp4"; voice = f"/home/claude/work/{slug}/voice.wav"
    cmd = [sys.executable, f"{PACK}/film-assembly/scripts/assemble.py", "--clips", *clips, "--narration", voice,
           "--aspect", "9:16", "--fps", str(FPS), "--durations", *[str(s["duration_s"]) for s in m["shots"]], "--out", film, "--run"]
    if a.music: cmd[cmd.index("--aspect"):cmd.index("--aspect")] = ["--music", a.music]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    vo = json.load(open(f"/home/claude/work/{slug}/vo.json")); ass = f"{wd}/caps.ass"; ass_captions(vo, ass)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", film, "-vf", f"ass={ass}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart", "-c:a", "copy", out], check=True)
    qc = subprocess.run([sys.executable, f"{PACK}/shot-qc/scripts/shot_qc.py", out, "--duration", str(m["brief"]["length_s"]),
                         "--ratio", "9:16", "--audio", "--fps", str(FPS), "--json"], capture_output=True, text=True)
    print(out); print(qc.stdout[-1500:] or qc.stderr[-800:])

if __name__ == "__main__":
    main()
