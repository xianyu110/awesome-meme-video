#!/usr/bin/env python3
"""Generate root index.html GitHub Pages gallery from inventory.json (newest first)."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path('/workspace/awesome-meme-video')


def sort_key(item):
    d = item.get('updated') or item.get('published') or item.get('scraped_at') or '1970-01-01'
    return (str(d)[:10], item.get('slug') or '')


def cover_url(t: dict) -> str:
    posters = t.get('posters') or []
    if posters:
        return posters[0]
    demos = t.get('demo_videos') or []
    if demos:
        u = demos[0]
        if u.endswith('.mp4'):
            return u[:-4] + '.jpg'
    return ''


def esc(s):
    return (str(s or '')
            .replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;').replace("'", '&#39;'))


def main():
    inv = json.load(open(ROOT / 'inventory.json'))
    templates = list(inv.get('templates') or [])
    templates.sort(key=sort_key, reverse=True)
    cards = []
    for t in templates:
        src = t.get('source')
        label = {'makeviral':'MakeViral','remakeyourmeme':'Remake','mediaio':'Media.io'}.get(src, src or 'Unknown')
        folder = f"{src}/{t['slug']}/"
        date = t.get('updated') or t.get('published') or t.get('scraped_at') or ''
        pc = int(t.get('prompt_count') or 0)
        if src == 'remakeyourmeme':
            badge, badge_cls = 'no prompts', 'none'
        elif pc:
            badge = f'{pc} prompt' + ('s' if pc != 1 else '')
            badge_cls = 'ok'
        else:
            badge, badge_cls = 'no prompts', 'none'
        cards.append({
            'name': t.get('name') or t['slug'],
            'slug': t['slug'],
            'source': src,
            'label': label,
            'date': date,
            'badge': badge,
            'badge_cls': badge_cls,
            'cover': cover_url(t),
            'demo': (t.get('demo_videos') or [None])[0],
            'blurb': (t.get('blurb') or '')[:160],
            'folder': folder,
            'url': t.get('url') or '',
            'prompt_count': pc,
        })

    s_mv = inv['sources']['makeviral']
    s_rm = inv['sources']['remakeyourmeme']
    s_mio = inv['sources'].get('mediaio') or {'count': 0, 'total_prompt_blocks': 0}
    data_json = json.dumps(cards, ensure_ascii=False)
    scraped = esc(inv.get('generated_at'))

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Awesome Meme Video · AI meme template gallery</title>
<meta name="description" content="Public inventory of AI meme / viral video templates and prompts from MakeViral and Remake Your Meme. Newest first.">
<meta property="og:title" content="Awesome Meme Video">
<meta property="og:description" content="{s_mv['count']} MakeViral + {s_rm['count']} Remake templates with prompts and demos.">
<link rel="canonical" href="https://xianyu110.github.io/awesome-meme-video/">
<style>
:root{{--bg:#070b12;--card:#101826;--card2:#152033;--line:#243247;--txt:#e8eef6;--sub:#8b9bb0;--acc:#7c6cff;--acc2:#3dd6c6;--ok:#3dd6c6}}
*{{box-sizing:border-box}}
body{{margin:0;background:radial-gradient(1200px 600px at 10% -10%,#1a1440 0%,transparent 50%),radial-gradient(900px 500px at 100% 0%,#0d2a2a 0%,transparent 45%),var(--bg);color:var(--txt);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}}
a{{color:var(--acc2);text-decoration:none}}a:hover{{text-decoration:underline}}
.wrap{{max-width:1240px;margin:0 auto;padding:28px 18px 72px}}
header h1{{font-size:clamp(26px,4vw,34px);margin:0 0 8px;letter-spacing:-.02em}}
header h1 span{{background:linear-gradient(120deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent}}
header p{{color:var(--sub);margin:4px 0}}
.badges{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:14px 0 6px}}
.badges img{{height:20px}}
.stats{{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}}
.chip{{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-size:13px;color:var(--sub)}}
.chip b{{color:var(--txt)}}
.box{{border:1px solid var(--line);background:linear-gradient(180deg,var(--card),var(--card2));border-radius:14px;padding:14px 16px;margin:14px 0;color:var(--sub);font-size:14px}}
.box b{{color:var(--txt)}} .box code{{background:#1a2633;padding:2px 6px;border-radius:5px;font-size:12px}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:18px 0 14px}}
.bar button{{background:var(--card);color:var(--txt);border:1px solid var(--line);border-radius:999px;padding:7px 14px;cursor:pointer;font-size:13px}}
.bar button.on{{background:var(--acc);border-color:var(--acc);color:#fff}}
.bar input{{flex:1;min-width:200px;background:var(--card);border:1px solid var(--line);color:var(--txt);border-radius:999px;padding:8px 14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;transition:transform .2s,border-color .2s,box-shadow .2s}}
.card:hover{{transform:translateY(-2px);border-color:#3a4d6a;box-shadow:0 12px 40px rgba(0,0,0,.35)}}
.cv{{position:relative;aspect-ratio:16/10;background:#000;overflow:hidden}}
.cv img,.cv video{{width:100%;height:100%;object-fit:cover;display:block}}
.cv .ph{{width:100%;height:100%;display:grid;place-items:center;color:var(--sub);font-size:13px;background:repeating-linear-gradient(-45deg,#121a26,#121a26 8px,#0e1520 8px,#0e1520 16px)}}
.tag{{position:absolute;top:10px;left:10px;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:3px 10px;border-radius:999px;color:#fff}}
.tag.mv{{background:rgba(124,108,255,.85)}} .tag.rm{{background:rgba(240,163,94,.9)}}
.date{{position:absolute;bottom:8px;left:10px;font-size:11px;background:rgba(0,0,0,.7);padding:2px 8px;border-radius:6px}}
.bd{{padding:14px 15px 16px;flex:1;display:flex;flex-direction:column;gap:8px}}
.bd h3{{margin:0;font-size:16px;line-height:1.35}}
.blurb{{color:var(--sub);font-size:13px;margin:0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.row{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.badge{{font-size:11px;border-radius:999px;padding:3px 9px;border:1px solid var(--line);color:var(--sub)}}
.badge.ok{{border-color:rgba(61,214,198,.45);color:var(--ok);background:rgba(61,214,198,.08)}}
.links{{margin-top:auto;padding-top:8px;display:flex;gap:12px;font-size:13px;font-weight:600}}
footer{{color:var(--sub);font-size:13px;margin-top:40px;border-top:1px solid var(--line);padding-top:18px}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>Awesome <span>Meme Video</span></h1>
  <p>Public AI meme / viral video templates &amp; prompts — MakeViral + Remake Your Meme</p>
  <div class="badges">
    <a href="https://github.com/xianyu110/awesome-meme-video" target="_blank" rel="noopener"><img src="https://img.shields.io/badge/GitHub-Repo-black?logo=github" alt="GitHub"></a>
    <a href="https://github.com/xianyu110/awesome-meme-video/stargazers" target="_blank" rel="noopener"><img src="https://img.shields.io/github/stars/xianyu110/awesome-meme-video?style=social" alt="Stars"></a>
  </div>
  <div class="stats">
    <span class="chip"><b>{s_mv['count']}</b> MakeViral</span>
    <span class="chip"><b>{s_mv['total_prompt_blocks']}</b> MV prompts</span>
    <span class="chip"><b>{s_rm['count']}</b> Remake (no public prompts)</span>
    <span class="chip"><b>{s_mio['count']}</b> Media.io · <b>{s_mio.get('total_prompt_blocks', 0)}</b> prompts</span>
    <span class="chip">Sorted <b>newest first</b></span>
    <span class="chip">Scraped <b>{scraped}</b> Asia/Shanghai</span>
  </div>
</header>
<div class="box"><b>What is this?</b> An inventory / awesome-list of publicly listed AI meme templates.
MakeViral pages publish copyable prompts (archived verbatim). Remake Your Meme is one-tap only — we archive demos/posters and mark <b>no public prompts</b>.
Media stays on source CDNs when local LFS demos are missing. Sort: <code>updated → published → scraped_at</code>.</div>
<div class="bar" id="bar">
  <button type="button" class="on" data-f="all">All</button>
  <button type="button" data-f="makeviral">MakeViral</button>
  <button type="button" data-f="remakeyourmeme">Remake</button>
  <button type="button" data-f="mediaio">Media.io</button>
  <input id="q" placeholder="Search title, slug, blurb…">
</div>
<div class="grid" id="grid"></div>
<footer>
  Prompts &amp; demos © respective sites · inventory by <a href="https://github.com/xianyu110">xianyu110</a> ·
  <a href="https://github.com/xianyu110/awesome-meme-video">repo</a> ·
  <a href="inventory.json">inventory.json</a> ·
  <a href="README.md">README</a>
</footer>
</div>
<script>
const DATA = {data_json};
const esc = s => String(s??'').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
const grid = document.getElementById('grid');
const q = document.getElementById('q');
let filter = 'all';
function coverHtml(c) {{
  if (c.cover) {{
    return '<img src="'+esc(c.cover)+'" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.replaceWith(Object.assign(document.createElement(\\'div\\'),{{className:\\'ph\\',textContent:\\'No cover\\'}}))">';
  }}
  if (c.demo) return '<video muted playsinline preload="metadata" src="'+esc(c.demo)+'#t=0.1"></video>';
  return '<div class="ph">No cover</div>';
}}
function render() {{
  const needle = (q.value || '').trim().toLowerCase();
  const list = DATA.filter(c => {{
    if (filter !== 'all' && c.source !== filter) return false;
    if (!needle) return true;
    return (c.name + ' ' + c.slug + ' ' + c.blurb + ' ' + c.label).toLowerCase().includes(needle);
  }});
  grid.innerHTML = list.map(c => {{
    return '<article class="card"><div class="cv">' + coverHtml(c)
      + '<span class="tag ' + (c.source === 'makeviral' ? 'mv' : (c.source === 'mediaio' ? 'mio' : 'rm')) + '">' + esc(c.label) + '</span>'
      + (c.date ? '<span class="date">' + esc(c.date) + '</span>' : '')
      + '</div><div class="bd"><h3>' + esc(c.name) + '</h3>'
      + '<p class="blurb">' + esc(c.blurb || '—') + '</p>'
      + '<div class="row"><span class="badge ' + esc(c.badge_cls) + '">' + esc(c.badge) + '</span>'
      + '<span class="badge">' + esc(c.slug) + '</span></div>'
      + '<div class="links"><a href="' + esc(c.folder) + 'PROMPTS.md">Folder</a>'
      + '<a href="' + esc(c.url) + '" target="_blank" rel="noopener">Original</a></div>'
      + '</div></article>';
  }}).join('');
}}
document.querySelectorAll('.bar button').forEach(btn => btn.addEventListener('click', () => {{
  filter = btn.dataset.f;
  document.querySelectorAll('.bar button').forEach(b => b.classList.toggle('on', b === btn));
  render();
}}));
q.addEventListener('input', render);
render();
</script>
</body>
</html>
'''
    (ROOT / 'index.html').write_text(html)
    print(f'Wrote index.html with {len(cards)} cards')


if __name__ == '__main__':
    main()
