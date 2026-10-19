#!/usr/bin/env python3
"""Generate root index.html GitHub Pages gallery from inventory.json (newest first)."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


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
        label = {'makeviral': 'MakeViral', 'remakeyourmeme': 'Remake', 'mediaio': 'Media.io', 'kavel': 'Kavel'}.get(src, src or 'Unknown')
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
            'date': str(date)[:10] if date else '',
            'badge': badge,
            'badge_cls': badge_cls,
            'cover': cover_url(t),
            'demo': (t.get('demo_videos') or [None])[0],
            'blurb': (t.get('blurb') or '')[:160],
            'folder': folder,
            'url': t.get('url') or '',
            'prompt_count': pc,
            'has_prompts': pc > 0 and src != 'remakeyourmeme',
        })

    # Prefer live counts from cards; fall back to inventory sources
    n_mv = sum(1 for c in cards if c['source'] == 'makeviral')
    n_rm = sum(1 for c in cards if c['source'] == 'remakeyourmeme')
    n_mio = sum(1 for c in cards if c['source'] == 'mediaio')
    n_kv = sum(1 for c in cards if c['source'] == 'kavel')
    n_total = len(cards)
    n_with_prompts = sum(1 for c in cards if c['has_prompts'])
    s_mv = inv.get('sources', {}).get('makeviral') or {}
    s_rm = inv.get('sources', {}).get('remakeyourmeme') or {}
    s_mio = inv.get('sources', {}).get('mediaio') or {}
    s_kv = inv.get('sources', {}).get('kavel') or {}
    mv_prompts = int(s_mv.get('total_prompt_blocks') or 0)
    mio_prompts = int(s_mio.get('total_prompt_blocks') or 0)
    kv_prompts = int(s_kv.get('total_prompt_blocks') or 0)
    data_json = json.dumps(cards, ensure_ascii=False)
    scraped = esc(inv.get('generated_at'))
    meta_desc = (
        f"Public inventory of {n_total} AI meme / viral video templates from "
        f"MakeViral ({n_mv}), Remake Your Meme ({n_rm}), Media.io ({n_mio}), and Kavel ({n_kv}). "
        f"Prompts, demos, and posters — newest first."
    )
    og_desc = (
        f"{n_mv} MakeViral + {n_rm} Remake + {n_mio} Media.io + {n_kv} Kavel templates "
        f"({n_with_prompts} with prompts)."
    )

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Awesome Meme Video · AI meme template gallery</title>
<meta name="description" content="{esc(meta_desc)}">
<meta property="og:title" content="Awesome Meme Video">
<meta property="og:description" content="{esc(og_desc)}">
<link rel="canonical" href="https://xianyu110.github.io/awesome-meme-video/">
<style>
:root{{
  --bg:#070b12;--card:#101826;--card2:#152033;--line:#243247;
  --txt:#e8eef6;--sub:#8b9bb0;--acc:#7c6cff;--acc2:#3dd6c6;--ok:#3dd6c6;
  --mio:#22d3ee;--rm:#f0a35e;--kv:#f472b6;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:radial-gradient(1200px 600px at 10% -10%,#1a1440 0%,transparent 50%),radial-gradient(900px 500px at 100% 0%,#0d2a2a 0%,transparent 45%),var(--bg);color:var(--txt);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}}
a{{color:var(--acc2);text-decoration:none}}a:hover{{text-decoration:underline}}
.wrap{{max-width:1240px;margin:0 auto;padding:20px 16px 72px}}
header{{margin-bottom:4px}}
header h1{{font-size:clamp(22px,3.5vw,30px);margin:0 0 4px;letter-spacing:-.02em}}
header h1 span{{background:linear-gradient(120deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent}}
header p.lead{{color:var(--sub);margin:0 0 8px;font-size:14px}}
.badges{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:8px 0 4px}}
.badges img{{height:20px}}
.stats{{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 6px}}
.chip{{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:12px;color:var(--sub)}}
.chip b{{color:var(--txt)}}
.box{{border:1px solid var(--line);background:linear-gradient(180deg,var(--card),var(--card2));border-radius:12px;padding:12px 14px;margin:10px 0 14px;color:var(--sub);font-size:13px}}
.box b{{color:var(--txt)}} .box code{{background:#1a2633;padding:2px 6px;border-radius:5px;font-size:12px}}
.toolbar{{
  position:sticky;top:0;z-index:40;
  margin:0 -16px 14px;padding:10px 16px;
  background:rgba(7,11,18,.82);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  border-bottom:1px solid rgba(36,50,71,.85);
}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
.bar button{{background:var(--card);color:var(--txt);border:1px solid var(--line);border-radius:999px;padding:7px 13px;cursor:pointer;font-size:13px;transition:background .15s,border-color .15s}}
.bar button:hover{{border-color:#3a4d6a}}
.bar button.on{{background:var(--acc);border-color:var(--acc);color:#fff}}
.bar button.sep{{margin-left:4px}}
.bar input{{flex:1;min-width:180px;background:var(--card);border:1px solid var(--line);color:var(--txt);border-radius:999px;padding:8px 14px;font-size:14px}}
.bar input:focus{{outline:none;border-color:var(--acc)}}
.count{{color:var(--sub);font-size:13px;margin:0 0 12px;padding:0 2px}}
.count b{{color:var(--txt)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;transition:transform .2s,border-color .2s,box-shadow .2s;cursor:pointer}}
.card:hover{{transform:translateY(-3px);border-color:#3a4d6a;box-shadow:0 14px 42px rgba(0,0,0,.4)}}
.card:focus-visible{{outline:2px solid var(--acc);outline-offset:2px}}
.cv{{position:relative;aspect-ratio:3/4;background:#000;overflow:hidden}}
.cv img,.cv video{{width:100%;height:100%;object-fit:cover;display:block}}
.cv video{{position:absolute;inset:0;opacity:0;transition:opacity .2s;pointer-events:none}}
.cv.playing video{{opacity:1}}
.cv.playing img{{opacity:0}}
.cv .ph{{width:100%;height:100%;display:grid;place-items:center;color:var(--sub);font-size:13px;background:repeating-linear-gradient(-45deg,#121a26,#121a26 8px,#0e1520 8px,#0e1520 16px)}}
.tag{{position:absolute;top:10px;left:10px;z-index:2;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:3px 10px;border-radius:999px;color:#fff}}
.tag.mv{{background:rgba(124,108,255,.88)}}
.tag.rm{{background:rgba(240,163,94,.92)}}
.tag.mio{{background:rgba(34,211,238,.9);color:#042f2e}}
.tag.kv{{background:rgba(244,114,182,.92);color:#3b0764}}
.date{{position:absolute;bottom:8px;left:10px;z-index:2;font-size:11px;background:rgba(0,0,0,.72);padding:2px 8px;border-radius:6px}}
.preview-hint{{position:absolute;bottom:8px;right:10px;z-index:2;font-size:11px;background:rgba(124,108,255,.85);padding:3px 9px;border-radius:999px;color:#fff;font-weight:600;opacity:0;transition:opacity .15s}}
.card:hover .preview-hint{{opacity:1}}
.bd{{padding:12px 13px 14px;flex:1;display:flex;flex-direction:column;gap:7px}}
.bd h3{{margin:0;font-size:15px;line-height:1.35}}
.blurb{{color:var(--sub);font-size:12px;margin:0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.row{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.badge{{font-size:11px;border-radius:999px;padding:3px 9px;border:1px solid var(--line);color:var(--sub)}}
.badge.ok{{border-color:rgba(61,214,198,.45);color:var(--ok);background:rgba(61,214,198,.08)}}
.links{{margin-top:auto;padding-top:6px;display:flex;gap:12px;font-size:13px;font-weight:600}}
.links a{{pointer-events:auto}}
footer{{color:var(--sub);font-size:13px;margin-top:40px;border-top:1px solid var(--line);padding-top:18px}}
/* Modal */
.modal{{position:fixed;inset:0;z-index:100;display:none;align-items:center;justify-content:center;padding:16px}}
.modal.open{{display:flex}}
.modal-bg{{position:absolute;inset:0;background:rgba(0,0,0,.72);backdrop-filter:blur(6px)}}
.modal-panel{{position:relative;z-index:1;width:min(720px,100%);max-height:min(92vh,900px);overflow:auto;background:linear-gradient(180deg,var(--card),var(--card2));border:1px solid var(--line);border-radius:18px;box-shadow:0 24px 80px rgba(0,0,0,.55)}}
.modal-close{{position:absolute;top:10px;right:12px;z-index:3;width:36px;height:36px;border:0;border-radius:50%;background:rgba(0,0,0,.55);color:#fff;font-size:22px;cursor:pointer;line-height:1}}
.modal-close:hover{{background:rgba(124,108,255,.85)}}
.modal-media{{background:#000;aspect-ratio:9/14;max-height:55vh;display:grid;place-items:center;overflow:hidden}}
.modal-media video,.modal-media img{{width:100%;height:100%;object-fit:contain;background:#000}}
.modal-body{{padding:16px 18px 20px}}
.modal-body h2{{margin:0 0 8px;font-size:20px;line-height:1.3}}
.modal-meta{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}}
.modal-blurb{{color:var(--sub);font-size:14px;margin:0 0 14px}}
.modal-actions{{display:flex;flex-wrap:wrap;gap:10px}}
.modal-actions a{{display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:999px;font-size:13px;font-weight:600;border:1px solid var(--line);background:var(--card);color:var(--txt);text-decoration:none}}
.modal-actions a:hover{{border-color:var(--acc);text-decoration:none}}
.modal-actions a.primary{{background:var(--acc);border-color:var(--acc);color:#fff}}
.modal-actions a.primary:hover{{filter:brightness(1.08)}}
body.modal-open{{overflow:hidden}}
@media (max-width:520px){{
  .grid{{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}}
  .preview-hint{{opacity:.85}}
}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>Awesome <span>Meme Video</span></h1>
  <p class="lead">AI meme &amp; viral video templates — MakeViral · Remake · Media.io · Kavel</p>
  <div class="badges">
    <a href="https://github.com/xianyu110/awesome-meme-video" target="_blank" rel="noopener"><img src="https://img.shields.io/badge/GitHub-Repo-black?logo=github" alt="GitHub"></a>
    <a href="https://github.com/xianyu110/awesome-meme-video/stargazers" target="_blank" rel="noopener"><img src="https://img.shields.io/github/stars/xianyu110/awesome-meme-video?style=social" alt="Stars"></a>
  </div>
  <div class="stats" id="stats">
    <span class="chip"><b>{n_total}</b> templates</span>
    <span class="chip"><b>{n_mv}</b> MakeViral · <b>{mv_prompts}</b> prompts</span>
    <span class="chip"><b>{n_rm}</b> Remake (no public prompts)</span>
    <span class="chip"><b>{n_mio}</b> Media.io · <b>{mio_prompts}</b> prompts</span>
    <span class="chip"><b>{n_kv}</b> Kavel · <b>{kv_prompts}</b> prompts</span>
    <span class="chip"><b>{n_with_prompts}</b> with prompts</span>
    <span class="chip">Sorted <b>newest first</b></span>
    <span class="chip">Scraped <b>{scraped}</b> Asia/Shanghai</span>
  </div>
</header>
<div class="box"><b>What is this?</b> A public inventory of AI meme templates.
MakeViral pages publish copyable prompts (archived verbatim). Remake Your Meme is one-tap only — demos/posters archived, marked <b>no public prompts</b>.
Media.io and Kavel prompts are kept when present on public pages. Media stays on source CDNs when local LFS demos are missing.</div>
<div class="toolbar">
  <div class="bar" id="bar">
    <button type="button" class="on" data-src="all">All</button>
    <button type="button" data-src="makeviral">MakeViral</button>
    <button type="button" data-src="remakeyourmeme">Remake</button>
    <button type="button" data-src="mediaio">Media.io</button>
    <button type="button" data-src="kavel">Kavel</button>
    <button type="button" class="sep on" data-prompt="all">Any prompts</button>
    <button type="button" data-prompt="yes">Has prompts</button>
    <button type="button" data-prompt="no">No prompts</button>
    <input id="q" type="search" placeholder="Search title, slug, blurb…" autocomplete="off">
  </div>
</div>
<p class="count" id="count">Showing <b>{n_total}</b> of <b>{n_total}</b></p>
<div class="grid" id="grid"></div>
<footer>
  Prompts &amp; demos © respective sites · inventory by <a href="https://github.com/xianyu110">xianyu110</a> ·
  <a href="https://github.com/xianyu110/awesome-meme-video">repo</a> ·
  <a href="inventory.json">inventory.json</a> ·
  <a href="README.md">README</a>
</footer>
</div>
<div class="modal" id="modal" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div class="modal-bg" data-close></div>
  <div class="modal-panel">
    <button type="button" class="modal-close" data-close aria-label="Close">&times;</button>
    <div class="modal-media" id="modal-media"></div>
    <div class="modal-body">
      <h2 id="modal-title"></h2>
      <div class="modal-meta" id="modal-meta"></div>
      <p class="modal-blurb" id="modal-blurb"></p>
      <div class="modal-actions" id="modal-actions"></div>
    </div>
  </div>
</div>
<script>
const DATA = {data_json};
const TOTAL = DATA.length;
const esc = s => String(s??'').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
const grid = document.getElementById('grid');
const q = document.getElementById('q');
const countEl = document.getElementById('count');
const modal = document.getElementById('modal');
const modalMedia = document.getElementById('modal-media');
const modalTitle = document.getElementById('modal-title');
const modalMeta = document.getElementById('modal-meta');
const modalBlurb = document.getElementById('modal-blurb');
const modalActions = document.getElementById('modal-actions');
let srcFilter = 'all';
let promptFilter = 'all';
let activeCard = null;
const coarse = window.matchMedia('(hover: none), (pointer: coarse)').matches;

function tagClass(src) {{
  if (src === 'makeviral') return 'mv';
  if (src === 'mediaio') return 'mio';
  if (src === 'kavel') return 'kv';
  return 'rm';
}}

function stopHoverVideo(cv) {{
  if (!cv) return;
  const v = cv.querySelector('video');
  if (v) {{ try {{ v.pause(); v.currentTime = 0; }} catch(_){{}} }}
  cv.classList.remove('playing');
}}

function playHoverVideo(cv) {{
  if (!cv || !cv.dataset.demo) return;
  let v = cv.querySelector('video');
  if (!v) {{
    v = document.createElement('video');
    v.muted = true;
    v.loop = true;
    v.playsInline = true;
    v.setAttribute('playsinline', '');
    v.preload = 'none';
    if (cv.dataset.cover) v.poster = cv.dataset.cover;
    v.src = cv.dataset.demo;
    cv.appendChild(v);
  }}
  cv.classList.add('playing');
  const p = v.play();
  if (p && p.catch) p.catch(() => {{}});
}}

function coverHtml(c) {{
  const attrs = ' class="cv"'
    + (c.demo ? ' data-demo="' + esc(c.demo) + '"' : '')
    + (c.cover ? ' data-cover="' + esc(c.cover) + '"' : '');
  let inner = '';
  if (c.cover) {{
    inner = '<img src="' + esc(c.cover) + '" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.replaceWith(Object.assign(document.createElement(\\'div\\'),{{className:\\'ph\\',textContent:\\'No cover\\'}}))">';
  }} else if (c.demo) {{
    inner = '<div class="ph">Tap / hover to play</div>';
  }} else {{
    inner = '<div class="ph">No cover</div>';
  }}
  return '<div' + attrs + '>' + inner
    + '<span class="tag ' + tagClass(c.source) + '">' + esc(c.label) + '</span>'
    + (c.date ? '<span class="date">' + esc(c.date) + '</span>' : '')
    + (c.demo ? '<span class="preview-hint">Preview</span>' : '')
    + '</div>';
}}

function filtered() {{
  const needle = (q.value || '').trim().toLowerCase();
  return DATA.filter(c => {{
    if (srcFilter !== 'all' && c.source !== srcFilter) return false;
    if (promptFilter === 'yes' && !c.has_prompts) return false;
    if (promptFilter === 'no' && c.has_prompts) return false;
    if (!needle) return true;
    return (c.name + ' ' + c.slug + ' ' + c.blurb + ' ' + c.label).toLowerCase().includes(needle);
  }});
}}

function render() {{
  const list = filtered();
  countEl.innerHTML = 'Showing <b>' + list.length + '</b> of <b>' + TOTAL + '</b>';
  grid.innerHTML = list.map((c, i) => {{
    const idx = DATA.indexOf(c);
    return '<article class="card" tabindex="0" data-i="' + idx + '" role="button" aria-label="Preview ' + esc(c.name) + '">'
      + coverHtml(c)
      + '<div class="bd"><h3>' + esc(c.name) + '</h3>'
      + '<p class="blurb">' + esc(c.blurb || '—') + '</p>'
      + '<div class="row"><span class="badge ' + esc(c.badge_cls) + '">' + esc(c.badge) + '</span>'
      + '<span class="badge">' + esc(c.slug) + '</span></div>'
      + '<div class="links"><a href="' + esc(c.folder) + 'PROMPTS.md" data-stop>Folder</a>'
      + (c.url ? '<a href="' + esc(c.url) + '" target="_blank" rel="noopener" data-stop>Original</a>' : '')
      + '</div></div></article>';
  }}).join('');
}}

function openModal(c) {{
  activeCard = c;
  modalTitle.textContent = c.name;
  modalMeta.innerHTML =
    '<span class="badge ' + esc(c.badge_cls) + '">' + esc(c.badge) + '</span>'
    + '<span class="tag ' + tagClass(c.source) + '" style="position:static">' + esc(c.label) + '</span>'
    + (c.date ? '<span class="badge">' + esc(c.date) + '</span>' : '')
    + '<span class="badge">' + esc(c.slug) + '</span>';
  modalBlurb.textContent = c.blurb || '—';
  let media = '';
  if (c.demo) {{
    media = '<video controls autoplay muted playsinline loop preload="metadata"'
      + (c.cover ? ' poster="' + esc(c.cover) + '"' : '')
      + ' src="' + esc(c.demo) + '"></video>';
  }} else if (c.cover) {{
    media = '<img src="' + esc(c.cover) + '" alt="" referrerpolicy="no-referrer">';
  }} else {{
    media = '<div class="ph" style="min-height:200px">No media</div>';
  }}
  modalMedia.innerHTML = media;
  const promptsUrl = esc(c.folder) + 'PROMPTS.md';
  let actions = '';
  if (c.has_prompts) actions += '<a class="primary" href="' + promptsUrl + '">View prompts (PROMPTS.md)</a>';
  actions += '<a href="' + promptsUrl + '">Folder</a>';
  if (c.url) actions += '<a href="' + esc(c.url) + '" target="_blank" rel="noopener">Original</a>';
  modalActions.innerHTML = actions;
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
  document.body.classList.add('modal-open');
}}

function closeModal() {{
  const v = modalMedia.querySelector('video');
  if (v) {{ try {{ v.pause(); }} catch(_){{}} }}
  modalMedia.innerHTML = '';
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('modal-open');
  activeCard = null;
}}

document.getElementById('bar').addEventListener('click', e => {{
  const btn = e.target.closest('button');
  if (!btn) return;
  if (btn.dataset.src !== undefined) {{
    srcFilter = btn.dataset.src;
    document.querySelectorAll('#bar button[data-src]').forEach(b => b.classList.toggle('on', b === btn));
    render();
  }} else if (btn.dataset.prompt !== undefined) {{
    promptFilter = btn.dataset.prompt;
    document.querySelectorAll('#bar button[data-prompt]').forEach(b => b.classList.toggle('on', b === btn));
    render();
  }}
}});
q.addEventListener('input', render);

grid.addEventListener('click', e => {{
  if (e.target.closest('[data-stop]')) return;
  const card = e.target.closest('.card');
  if (!card) return;
  const cv = e.target.closest('.cv');
  if (coarse && cv && cv.dataset.demo) {{
    if (cv.classList.contains('playing')) {{
      stopHoverVideo(cv);
    }} else {{
      grid.querySelectorAll('.cv.playing').forEach(stopHoverVideo);
      playHoverVideo(cv);
    }}
    e.stopPropagation();
    return;
  }}
  const i = +card.dataset.i;
  if (!Number.isNaN(i) && DATA[i]) openModal(DATA[i]);
}});
grid.addEventListener('keydown', e => {{
  if (e.key !== 'Enter' && e.key !== ' ') return;
  const card = e.target.closest('.card');
  if (!card) return;
  e.preventDefault();
  const i = +card.dataset.i;
  if (!Number.isNaN(i) && DATA[i]) openModal(DATA[i]);
}});

if (!coarse) {{
  grid.addEventListener('mouseover', e => {{
    const cv = e.target.closest('.cv');
    if (!cv || !cv.dataset.demo || cv.classList.contains('playing')) return;
    grid.querySelectorAll('.cv.playing').forEach(stopHoverVideo);
    playHoverVideo(cv);
  }});
  grid.addEventListener('mouseout', e => {{
    const cv = e.target.closest('.cv');
    if (!cv) return;
    const to = e.relatedTarget;
    if (to && cv.contains(to)) return;
    stopHoverVideo(cv);
  }});
}}

modal.addEventListener('click', e => {{
  if (e.target.closest('[data-close]')) closeModal();
}});
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
}});

render();
</script>
</body>
</html>
'''
    (ROOT / 'index.html').write_text(html)
    print(f'Wrote index.html with {len(cards)} cards (MV={n_mv} RM={n_rm} MIO={n_mio} KV={n_kv} prompts={n_with_prompts})')


if __name__ == '__main__':
    main()
