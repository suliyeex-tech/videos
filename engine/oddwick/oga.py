"""Fetch CC0 OpenGameArt sound packs: python3 oga.py <content-slug> ...  -> /home/claude/work/oga/<slug>/ (zips extracted)
Also: python3 oga.py --km "Merry Go" ...  -> Kevin MacLeod (incompetech, CC BY 4.0) mp3s into /home/claude/work/lib/km_<Name>.mp3"""
import sys, os, re, subprocess, zipfile, urllib.parse
OGA = '/home/claude/work/oga'; LIB = '/home/claude/work/lib'; os.makedirs(OGA, exist_ok=True); os.makedirs(LIB, exist_ok=True)
args = sys.argv[1:]
if args and args[0] == '--km':
    for n in args[1:]:
        f = f"{LIB}/km_{n.replace(' ', '_')}.mp3"
        if os.path.exists(f) and os.path.getsize(f) > 100000: continue
        u = 'https://incompetech.com/music/royalty-free/mp3-royaltyfree/' + urllib.parse.quote(n) + '.mp3'
        r = subprocess.run(['curl', '-sfL', '-o', f, u]); print(n, 'OK' if r.returncode == 0 else 'FAIL')
    sys.exit()
for slug in args:
    d = f'{OGA}/{slug}'
    if os.path.isdir(d) and os.listdir(d): continue
    os.makedirs(d, exist_ok=True)
    html = subprocess.run(['curl', '-sL', f'https://opengameart.org/content/{slug}'], capture_output=True, text=True).stdout
    lic = 'CC0' if "license-name'>CC0" in html else 'OTHER'
    urls = sorted(set(u for u in re.findall(r'https://opengameart.org/sites/default/files/[^"\'<> ]+', html)
                      if re.search(r'\.(zip|ogg|wav|mp3|flac)$', u, re.I) and 'audio_preview' not in u and '/styles/' not in u))
    for u in urls:
        fn = f'{d}/' + urllib.parse.unquote(u.rsplit('/', 1)[1])
        subprocess.run(['curl', '-sfL', '-o', fn, u])
        if fn.lower().endswith('.zip'):
            try: zipfile.ZipFile(fn).extractall(d); os.remove(fn)
            except Exception as e: print('zip err', fn, e)
    print(slug, lic, len(urls), 'files')
