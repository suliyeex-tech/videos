"""Openverse (CC0 / CC BY only) retrieval for SFX and music: python3 fetch_audio.py name="query"[:music] ...
Saves to /home/claude/work/lib/<name>.mp3 and appends credits to /home/claude/work/lib/credits.json"""
import sys, json, os, urllib.request, urllib.parse
op = urllib.request.build_opener(); op.addheaders = [('User-Agent', 'Mozilla/5.0 oddwick-shorts')]; urllib.request.install_opener(op)
LIB = '/home/claude/work/lib'; os.makedirs(LIB, exist_ok=True)
cr_path = f'{LIB}/credits.json'; credits = json.load(open(cr_path)) if os.path.exists(cr_path) else {}
for arg in sys.argv[1:]:
    name, q = arg.split('=', 1); music = q.endswith(':music'); q = q.replace(':music', '')
    if os.path.exists(f'{LIB}/{name}.mp3'): continue
    url = 'https://api.openverse.org/v1/audio/?' + urllib.parse.urlencode({'q': q, 'license': 'cc0,by', 'page_size': 20})
    try: res = json.load(urllib.request.urlopen(url, timeout=30))['results']
    except Exception as e: print('ERR', name, e); continue
    def ok(r):
        d = (r.get('duration') or 0) / 1000
        return r['license'] in ('cc0', 'by') and (d >= 40 if music else 0.2 <= d <= 12) and r['url'].endswith('.mp3')
    c = [r for r in res if ok(r)]
    if not c: print('NONE', name, q); continue
    r = c[0]
    import subprocess
    if subprocess.run(['curl', '-sfL', '-o', f'{LIB}/{name}.mp3', r['url']]).returncode: print('DLERR', name); continue
    credits[name] = {'title': r['title'], 'creator': r['creator'], 'license': r['license'], 'url': r.get('foreign_landing_url') or r['url']}
    print(name, '<-', r['title'][:50], '|', r['creator'], '|', r['license'], '|', round((r.get('duration') or 0) / 1000, 1), 's')
json.dump(credits, open(cr_path, 'w'), indent=1)
