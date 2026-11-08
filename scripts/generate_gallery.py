#!/usr/bin/env python3
"""Generate root index.html GitHub Pages gallery from inventory.json (newest first).

Date rule: use source listing date = published, else updated if published missing.
Never use scraped_at for sort, filter chips, or displayed card date.

Prompt bodies are not inlined into index.html (that blob is ~3MB). Each template
with public prompts gets prompts/<source>/<slug>.json, fetched when the modal opens.
Remake Your Meme stays marked as having no public prompts.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Topic buckets derived from name/slug/blurb (first match wins). Low-confidence → Other.
TOPIC_RULES = [
    ('Dance', re.compile(
        r'dance|dancing|ballet|choreograph|groove|twerk|hip.?hop|disco|'
        r'\bbop\b|navratri|raindance|wipe.?me.?down|head.?bop', re.I)),
    ('Pet', re.compile(
        r'\bpet\b|dog|cat|puppy|kitten|animal|hamster|parrot|bunny|rabbit|'
        r'polar.?bear|\bbear\b|whiny.?dog|smalltown.?boy.?cat', re.I)),
    ('Car', re.compile(
        r'\bcar\b|vehicle|drive|driving|truck|motorcycle|race|racing|drift|'
        r'parking|behind the wheel|luxury se', re.I)),
    ('Couple', re.compile(
        r'couple|romance|romantic|kiss|\bdate\b|wedding|boyfriend|girlfriend|'
        r'\blove\b|proposal|reunion|hug in heaven|heavenly reunion|zombie.?couple', re.I)),
    ('Filter-Prank', re.compile(
        r'filter|prank|joke|morph|swap|face.?swap|ai.?filter|ghostface|'
        r'ghost photo|arrested|abra.?kadabra', re.I)),
    ('Sports', re.compile(
        r'sport|football|soccer|basketball|tennis|golf|gym|workout|fitness|'
        r'boxing|swim|skate|baseball|nfl|rabona|ozil|\bgoal\b|keeper|lamine', re.I)),
    ('Birthday', re.compile(
        r'birthday|bday|\bcake\b|celebration|\bparty\b|anniversary', re.I)),
]


def listing_date(item: dict) -> str:
    """Source listing/inclusion date: published, else updated. Never scraped_at."""
    d = item.get('published') or item.get('updated') or ''
    return str(d)[:10] if d else ''


def sort_key(item):
    d = listing_date(item) or '0000-00-00'
    return (d, item.get('slug') or '')


def topic_of(t: dict) -> str:
    text = f"{t.get('name') or ''} {t.get('slug') or ''} {t.get('blurb') or ''}"
    for name, rx in TOPIC_RULES:
        if rx.search(text):
            return name
    return 'Other'


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


SAFE_ID = re.compile(r'^[A-Za-z0-9._-]+$')


def public_prompts(t: dict) -> list[dict]:
    """Prompt bodies safe to show on the public gallery.

    Remake Your Meme does not publish copyable prompts; ignore any extracted text.
    """
    if t.get('source') == 'remakeyourmeme':
        return []
    out = []
    for p in t.get('prompts') or []:
        text = p.get('text') or ''
        if not str(text).strip():
            continue
        out.append({
            'label': p.get('label'),
            'variant': p.get('variant'),
            'kind': p.get('kind'),
            'text': text,
        })
    return out


def prompts_relpath(src: str, slug: str) -> str:
    if not SAFE_ID.fullmatch(src or '') or not SAFE_ID.fullmatch(slug or ''):
        raise ValueError(f'unsafe prompts path: {src!r}/{slug!r}')
    return f'prompts/{src}/{slug}.json'


def write_prompt_files(templates: list[dict]) -> int:
    """Write one JSON file per template that has public prompt text. Drop stale files."""
    root = ROOT / 'prompts'
    keep: set[Path] = set()
    n = 0
    for t in templates:
        prompts = public_prompts(t)
        if not prompts:
            continue
        dest = ROOT / prompts_relpath(t['source'], t['slug'])
        dest.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            'source': t['source'],
            'slug': t['slug'],
            'prompts': prompts,
        }
        dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        keep.add(dest.resolve())
        n += 1
    if root.exists():
        for path in root.rglob('*.json'):
            if path.resolve() not in keep:
                path.unlink()
        for directory in sorted((p for p in root.rglob('*') if p.is_dir()), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
    return n


def main():
    inv = json.load(open(ROOT / 'inventory.json'))
    templates = list(inv.get('templates') or [])
    templates.sort(key=sort_key, reverse=True)
    cards = []
    for t in templates:
        src = t.get('source')
        label = {
            'makeviral': 'MakeViral',
            'remakeyourmeme': 'Remake',
            'mediaio': 'Media.io',
            'kavel': 'Kavel',
        }.get(src, src or 'Unknown')
        folder = f"{src}/{t['slug']}/"
        date = listing_date(t)
        prompts = public_prompts(t)
        pc = len(prompts)
        if src == 'remakeyourmeme' or pc == 0:
            badge, badge_cls = 'no prompts', 'none'
        else:
            badge = f'{pc} prompt' + ('s' if pc != 1 else '')
            badge_cls = 'ok'
        cards.append({
            'name': t.get('name') or t['slug'],
            'slug': t['slug'],
            'source': src,
            'label': label,
            'date': date,  # ISO YYYY-MM-DD or '' — never scraped_at
            'topic': topic_of(t),
            'badge': badge,
            'badge_cls': badge_cls,
            'cover': cover_url(t),
            'demo': (t.get('demo_videos') or [None])[0],
            'blurb': (t.get('blurb') or '')[:160],
            'folder': folder,
            'url': t.get('url') or '',
            'prompt_count': pc,
            'has_prompts': pc > 0,
            'prompts_url': prompts_relpath(src, t['slug']) if pc else '',
        })

    n_mv = sum(1 for c in cards if c['source'] == 'makeviral')
    n_rm = sum(1 for c in cards if c['source'] == 'remakeyourmeme')
    n_mio = sum(1 for c in cards if c['source'] == 'mediaio')
    n_kv = sum(1 for c in cards if c['source'] == 'kavel')
    n_total = len(cards)
    n_with_prompts = sum(1 for c in cards if c['has_prompts'])
    n_dated = sum(1 for c in cards if c['date'])
    n_unknown_date = n_total - n_dated
    s_mv = inv.get('sources', {}).get('makeviral') or {}
    s_rm = inv.get('sources', {}).get('remakeyourmeme') or {}
    s_mio = inv.get('sources', {}).get('mediaio') or {}
    s_kv = inv.get('sources', {}).get('kavel') or {}
    mv_prompts = int(s_mv.get('total_prompt_blocks') or 0)
    mio_prompts = int(s_mio.get('total_prompt_blocks') or 0)
    kv_prompts = int(s_kv.get('total_prompt_blocks') or 0)
    n_prompt_files = write_prompt_files(templates)
    data_json = json.dumps(cards, ensure_ascii=False, separators=(',', ':'))
    scraped = esc(inv.get('generated_at'))
    meta_desc = (
        f"Public inventory of {n_total} AI meme / viral video templates from "
        f"MakeViral ({n_mv}), Remake Your Meme ({n_rm}), Media.io ({n_mio}), and Kavel ({n_kv}). "
        f"Prompts, demos, and posters — filter by source, topic, date."
    )
    og_desc = (
        f"{n_mv} MakeViral + {n_rm} Remake + {n_mio} Media.io + {n_kv} Kavel templates "
        f"({n_with_prompts} with prompts)."
    )

    # Topic chip order (stable)
    topic_order = ['Dance', 'Pet', 'Car', 'Couple', 'Filter-Prank', 'Sports', 'Birthday', 'Other']
    topic_btns = '\n    '.join(
        f'<button type="button" data-topic="{esc(t)}">{esc(t)}</button>' for t in topic_order
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
  margin:0 -16px 14px;padding:10px 16px 12px;
  background:rgba(7,11,18,.88);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  border-bottom:1px solid rgba(36,50,71,.85);
}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:6px}}
.bar:first-child{{margin-top:0}}
.bar-label{{font-size:11px;color:var(--sub);text-transform:uppercase;letter-spacing:.04em;margin-right:2px;min-width:2.5em}}
.bar button{{background:var(--card);color:var(--txt);border:1px solid var(--line);border-radius:999px;padding:6px 12px;cursor:pointer;font-size:12.5px;transition:background .15s,border-color .15s}}
.bar button:hover{{border-color:#3a4d6a}}
.bar button.on{{background:var(--acc);border-color:var(--acc);color:#fff}}
.bar input{{flex:1;min-width:160px;background:var(--card);border:1px solid var(--line);color:var(--txt);border-radius:999px;padding:7px 14px;font-size:13px}}
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
.date.unk{{color:var(--sub)}}
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
.modal-panel{{position:relative;z-index:1;width:min(1080px,100%);height:min(92vh,920px);max-height:min(92vh,920px);display:flex;flex-direction:column;overflow:hidden;background:linear-gradient(180deg,var(--card),var(--card2));border:1px solid var(--line);border-radius:18px;box-shadow:0 24px 80px rgba(0,0,0,.55)}}
.modal-close{{position:absolute;top:10px;right:12px;z-index:3;width:36px;height:36px;border:0;border-radius:50%;background:rgba(0,0,0,.55);color:#fff;font-size:22px;cursor:pointer;line-height:1}}
.modal-close:hover{{background:rgba(124,108,255,.85)}}
.modal-layout{{display:grid;grid-template-columns:minmax(240px,.9fr) minmax(300px,1.15fr);min-height:0;flex:1}}
.modal-media{{background:#000;min-height:220px;display:grid;place-items:center;overflow:hidden}}
.modal-media video,.modal-media img{{width:100%;height:100%;object-fit:contain;background:#000}}
.modal-body{{padding:16px 18px 20px;overflow:auto;min-height:0}}
.modal-body h2{{margin:0 0 8px;font-size:20px;line-height:1.3;padding-right:36px}}
.modal-meta{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}}
.modal-blurb{{color:var(--sub);font-size:14px;margin:0 0 14px}}
.modal-prompts{{display:flex;flex-direction:column;gap:10px;margin:0 0 16px}}
.prompts-head{{display:flex;align-items:center;justify-content:space-between;gap:8px}}
.prompts-head h3{{margin:0;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--sub)}}
.prompt-block{{border:1px solid var(--line);background:#0c121c;border-radius:12px;overflow:hidden}}
.prompt-block header{{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;padding:10px 12px;border-bottom:1px solid var(--line);background:rgba(255,255,255,.03)}}
.prompt-label{{font-size:13px;font-weight:650;line-height:1.4}}
.prompt-meta{{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}}
.copy-btn{{flex:none;background:#152033;color:var(--txt);border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:12px;font-weight:700;cursor:pointer}}
.copy-btn:hover{{border-color:var(--acc)}}
.copy-btn.copied{{border-color:var(--ok);color:var(--ok)}}
.prompt-text{{margin:0;padding:12px 14px;white-space:pre-wrap;word-break:break-word;font:13px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:#d7e0ec;user-select:text}}
.prompts-empty,.prompts-status{{margin:0;color:var(--sub);font-size:14px;padding:12px 14px;border:1px dashed var(--line);border-radius:12px;background:rgba(0,0,0,.18)}}
.modal-actions{{display:flex;flex-wrap:wrap;gap:10px}}
.modal-actions a{{display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:999px;font-size:13px;font-weight:600;border:1px solid var(--line);background:var(--card);color:var(--txt);text-decoration:none}}
.modal-actions a:hover{{border-color:var(--acc);text-decoration:none}}
body.modal-open{{overflow:hidden}}
@media (max-width:800px){{
  .modal-panel{{height:auto;max-height:min(92vh,920px);overflow:auto}}
  .modal-layout{{display:block}}
  .modal-media{{max-height:36vh;aspect-ratio:3/4}}
  .modal-body{{overflow:visible}}
}}
@media (max-width:520px){{
  .grid{{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}}
  .preview-hint{{opacity:.85}}
  .bar-label{{min-width:auto}}
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
    <span class="chip"><b>{n_dated}</b> with listing date · <b>{n_unknown_date}</b> unknown</span>
    <span class="chip">Scraped <b>{scraped}</b> Asia/Shanghai</span>
  </div>
</header>
<div class="box"><b>What is this?</b> A public inventory of AI meme templates.
MakeViral pages publish copyable prompts (archived verbatim). Open a card to read them here — no need to leave for PROMPTS.md.
Remake Your Meme is one-tap only — demos/posters archived, marked <b>no public prompts</b>.
Media.io and Kavel prompts are kept when present on public pages. Media stays on source CDNs when local LFS demos are missing.
Dates are source <b>listing / publish</b> times (not scrape time); Remake / Media.io / Kavel often lack a public listing date.</div>
<div class="toolbar" id="toolbar">
  <div class="bar" id="bar-src">
    <span class="bar-label">源</span>
    <button type="button" class="on" data-src="all">All</button>
    <button type="button" data-src="makeviral">MakeViral</button>
    <button type="button" data-src="remakeyourmeme">Remake</button>
    <button type="button" data-src="mediaio">Media.io</button>
    <button type="button" data-src="kavel">Kavel</button>
  </div>
  <div class="bar" id="bar-topic">
    <span class="bar-label">题材</span>
    <button type="button" class="on" data-topic="all">全部</button>
    {topic_btns}
  </div>
  <div class="bar" id="bar-date">
    <span class="bar-label">日期</span>
    <button type="button" class="on" data-date="all">全部</button>
    <button type="button" data-date="today">今天</button>
    <button type="button" data-date="7d">近7天</button>
    <button type="button" data-date="30d">近30天</button>
    <button type="button" data-date="unknown">未知日期</button>
  </div>
  <div class="bar" id="bar-more">
    <span class="bar-label">提示</span>
    <button type="button" class="on" data-prompt="all">Any</button>
    <button type="button" data-prompt="yes">Has</button>
    <button type="button" data-prompt="no">No</button>
    <span class="bar-label" style="margin-left:6px">排序</span>
    <button type="button" class="on" data-sort="new">新→旧</button>
    <button type="button" data-sort="old">旧→新</button>
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
    <div class="modal-layout">
      <div class="modal-media" id="modal-media"></div>
      <div class="modal-body">
        <h2 id="modal-title"></h2>
        <div class="modal-meta" id="modal-meta"></div>
        <p class="modal-blurb" id="modal-blurb"></p>
        <div class="modal-prompts" id="modal-prompts"></div>
        <div class="modal-actions" id="modal-actions"></div>
      </div>
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
const modalPrompts = document.getElementById('modal-prompts');
const modalActions = document.getElementById('modal-actions');
const promptCache = new Map();
let promptReq = 0;
let activePrompts = [];
let srcFilter = 'all';
let topicFilter = 'all';
let dateFilter = 'all';
let promptFilter = 'all';
let sortOrder = 'new'; // new = 新→旧, old = 旧→新
let activeCard = null;
let searchTimer = null;
const coarse = window.matchMedia('(hover: none), (pointer: coarse)').matches;

function todayISO() {{
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth()+1).padStart(2,'0');
  const day = String(d.getDate()).padStart(2,'0');
  return y + '-' + m + '-' + day;
}}

function daysAgoISO(n) {{
  const d = new Date();
  d.setDate(d.getDate() - n);
  const y = d.getFullYear();
  const m = String(d.getMonth()+1).padStart(2,'0');
  const day = String(d.getDate()).padStart(2,'0');
  return y + '-' + m + '-' + day;
}}

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

function dateLabel(c) {{
  return c.date ? c.date : 'date unknown';
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
  const dspan = c.date
    ? '<span class="date" data-date="' + esc(c.date) + '">' + esc(c.date) + '</span>'
    : '<span class="date unk" data-date="">date unknown</span>';
  return '<div' + attrs + '>' + inner
    + '<span class="tag ' + tagClass(c.source) + '">' + esc(c.label) + '</span>'
    + dspan
    + (c.demo ? '<span class="preview-hint">Preview</span>' : '')
    + '</div>';
}}

function inDateWindow(c) {{
  if (dateFilter === 'all') return true;
  if (dateFilter === 'unknown') return !c.date;
  if (!c.date) return false; // 今天/近N天 never match scrape-less empty dates
  const today = todayISO();
  if (dateFilter === 'today') return c.date === today;
  if (dateFilter === '7d') return c.date >= daysAgoISO(7) && c.date <= today;
  if (dateFilter === '30d') return c.date >= daysAgoISO(30) && c.date <= today;
  return true;
}}

function filtered() {{
  const needle = (q.value || '').trim().toLowerCase();
  let list = DATA.filter(c => {{
    if (srcFilter !== 'all' && c.source !== srcFilter) return false;
    if (topicFilter !== 'all' && c.topic !== topicFilter) return false;
    if (!inDateWindow(c)) return false;
    if (promptFilter === 'yes' && !c.has_prompts) return false;
    if (promptFilter === 'no' && c.has_prompts) return false;
    if (!needle) return true;
    return (c.name + ' ' + c.slug + ' ' + c.blurb + ' ' + c.label + ' ' + c.topic).toLowerCase().includes(needle);
  }});
  list = list.slice();
  list.sort((a, b) => {{
    const da = a.date || '';
    const db = b.date || '';
    // undated sink to end for 新→旧, to start for 旧→新 (treat as oldest)
    if (!da && !db) return (a.slug || '').localeCompare(b.slug || '');
    if (!da) return sortOrder === 'new' ? 1 : -1;
    if (!db) return sortOrder === 'new' ? -1 : 1;
    if (da !== db) return sortOrder === 'new' ? (db > da ? 1 : -1) : (da > db ? 1 : -1);
    return (a.slug || '').localeCompare(b.slug || '');
  }});
  return list;
}}

function filterSummary() {{
  const parts = [];
  if (srcFilter !== 'all') {{
    const map = {{makeviral:'MakeViral', remakeyourmeme:'Remake', mediaio:'Media.io', kavel:'Kavel'}};
    parts.push(map[srcFilter] || srcFilter);
  }}
  if (topicFilter !== 'all') parts.push(topicFilter);
  if (dateFilter === 'today') parts.push('今天');
  else if (dateFilter === '7d') parts.push('近7天');
  else if (dateFilter === '30d') parts.push('近30天');
  else if (dateFilter === 'unknown') parts.push('未知日期');
  if (promptFilter === 'yes') parts.push('Has prompts');
  else if (promptFilter === 'no') parts.push('No prompts');
  parts.push(sortOrder === 'new' ? '新→旧' : '旧→新');
  const needle = (q.value || '').trim();
  if (needle) parts.push('"' + needle + '"');
  return parts.length ? parts.join(' · ') : 'all';
}}

function render() {{
  const list = filtered();
  countEl.innerHTML = 'Showing <b>' + list.length + '</b> of <b>' + TOTAL + '</b> · ' + esc(filterSummary());
  grid.innerHTML = list.map(c => {{
    const idx = DATA.indexOf(c);
    return '<article class="card" tabindex="0" data-i="' + idx + '" data-date="' + esc(c.date || '') + '" data-topic="' + esc(c.topic) + '" data-source="' + esc(c.source) + '" role="button" aria-label="Preview ' + esc(c.name) + '">'
      + coverHtml(c)
      + '<div class="bd"><h3>' + esc(c.name) + '</h3>'
      + '<p class="blurb">' + esc(c.blurb || '—') + '</p>'
      + '<div class="row"><span class="badge ' + esc(c.badge_cls) + '">' + esc(c.badge) + '</span>'
      + '<span class="badge">' + esc(c.topic) + '</span>'
      + '<span class="badge">' + esc(c.slug) + '</span></div>'
      + '<div class="links"><a href="' + esc(c.folder) + 'PROMPTS.md" data-stop>Folder</a>'
      + (c.url ? '<a href="' + esc(c.url) + '" target="_blank" rel="noopener" data-stop>Original</a>' : '')
      + '</div></div></article>';
  }}).join('');
  syncUrl();
}}

function kindLabel(kind) {{
  return kind ? String(kind).replace(/_/g, ' ') : '';
}}

function promptsEmptyHtml(c) {{
  if (c.source === 'remakeyourmeme') {{
    return '<p class="prompts-empty">No public prompts. Remake Your Meme does not publish copyable prompt text.</p>';
  }}
  return '<p class="prompts-empty">No public prompts for this template.</p>';
}}

function renderPromptBlocks(prompts) {{
  const head = '<div class="prompts-head"><h3>Prompts</h3><span class="badge ok">' + prompts.length + '</span></div>';
  const blocks = prompts.map((p, i) => {{
    const meta = [];
    if (p.variant) meta.push('<span class="badge">' + esc(p.variant) + '</span>');
    if (p.kind) meta.push('<span class="badge">' + esc(kindLabel(p.kind)) + '</span>');
    const label = p.label || ('Prompt ' + (i + 1));
    return '<section class="prompt-block">'
      + '<header><div><div class="prompt-label">' + esc(label) + '</div>'
      + (meta.length ? '<div class="prompt-meta">' + meta.join('') + '</div>' : '')
      + '</div><button type="button" class="copy-btn" data-copy="' + i + '">Copy</button></header>'
      + '<pre class="prompt-text">' + esc(p.text || '') + '</pre></section>';
  }}).join('');
  return head + blocks;
}}

function showPrompts(c) {{
  const req = ++promptReq;
  activePrompts = [];
  if (!c.has_prompts || !c.prompts_url) {{
    modalPrompts.innerHTML = promptsEmptyHtml(c);
    return;
  }}
  const cached = promptCache.get(c.prompts_url);
  if (cached) {{
    activePrompts = cached;
    modalPrompts.innerHTML = cached.length ? renderPromptBlocks(cached) : promptsEmptyHtml(c);
    return;
  }}
  modalPrompts.innerHTML = '<p class="prompts-status">Loading prompts…</p>';
  fetch(c.prompts_url)
    .then(r => {{ if (!r.ok) throw new Error(String(r.status)); return r.json(); }})
    .then(data => {{
      const prompts = (data && Array.isArray(data.prompts)) ? data.prompts : [];
      promptCache.set(c.prompts_url, prompts);
      if (req !== promptReq) return;
      activePrompts = prompts;
      modalPrompts.innerHTML = prompts.length ? renderPromptBlocks(prompts) : promptsEmptyHtml(c);
    }})
    .catch(() => {{
      if (req !== promptReq) return;
      const href = esc(c.folder) + 'PROMPTS.md';
      modalPrompts.innerHTML = '<p class="prompts-empty">Could not load prompts on this page. <a href="' + href + '">Open PROMPTS.md</a>.</p>';
    }});
}}

function fallbackCopy(text, done) {{
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.setAttribute('readonly', '');
  ta.style.position = 'fixed';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.select();
  try {{ document.execCommand('copy'); }} catch (_) {{}}
  ta.remove();
  done();
}}

function copyPrompt(i, btn) {{
  const text = (activePrompts[i] && activePrompts[i].text) || '';
  const done = () => {{
    btn.textContent = 'Copied';
    btn.classList.add('copied');
    setTimeout(() => {{
      if (!btn.isConnected) return;
      btn.textContent = 'Copy';
      btn.classList.remove('copied');
    }}, 1400);
  }};
  if (navigator.clipboard && navigator.clipboard.writeText) {{
    navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
  }} else {{
    fallbackCopy(text, done);
  }}
}}

function openModal(c) {{
  activeCard = c;
  modalTitle.textContent = c.name;
  modalMeta.innerHTML =
    '<span class="badge ' + esc(c.badge_cls) + '">' + esc(c.badge) + '</span>'
    + '<span class="tag ' + tagClass(c.source) + '" style="position:static">' + esc(c.label) + '</span>'
    + '<span class="badge">' + esc(dateLabel(c)) + '</span>'
    + '<span class="badge">' + esc(c.topic) + '</span>'
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
  showPrompts(c);
  const promptsUrl = esc(c.folder) + 'PROMPTS.md';
  // Pages has no directory index; the repo tree is the folder view.
  const folderUrl = 'https://github.com/xianyu110/awesome-meme-video/tree/main/' + esc(c.folder);
  let actions = '<a href="' + promptsUrl + '">PROMPTS.md</a>'
    + '<a href="' + folderUrl + '" target="_blank" rel="noopener">Folder</a>';
  if (c.url) actions += '<a href="' + esc(c.url) + '" target="_blank" rel="noopener">Original</a>';
  modalActions.innerHTML = actions;
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
  document.body.classList.add('modal-open');
}}

function closeModal() {{
  promptReq++;
  activePrompts = [];
  const v = modalMedia.querySelector('video');
  if (v) {{ try {{ v.pause(); }} catch(_){{}} }}
  modalMedia.innerHTML = '';
  modalPrompts.innerHTML = '';
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('modal-open');
  activeCard = null;
}}

function setToggle(groupSel, attr, value) {{
  document.querySelectorAll(groupSel + ' button[' + attr + ']').forEach(b => {{
    b.classList.toggle('on', b.getAttribute(attr) === value);
  }});
}}

function syncUrl() {{
  try {{
    const p = new URLSearchParams();
    if (srcFilter !== 'all') p.set('src', srcFilter === 'remakeyourmeme' ? 'remake' : (srcFilter === 'mediaio' ? 'mediaio' : srcFilter));
    if (topicFilter !== 'all') p.set('topic', topicFilter);
    if (dateFilter !== 'all') p.set('date', dateFilter);
    if (promptFilter !== 'all') p.set('prompt', promptFilter);
    if (sortOrder !== 'new') p.set('sort', sortOrder);
    const needle = (q.value || '').trim();
    if (needle) p.set('q', needle);
    const qs = p.toString();
    const next = qs ? ('?' + qs) : location.pathname;
    if (location.search.slice(1) !== qs) history.replaceState(null, '', next);
  }} catch(_){{}}
}}

function applyUrl() {{
  try {{
    const p = new URLSearchParams(location.search);
    const srcMap = {{all:'all', makeviral:'makeviral', remake:'remakeyourmeme', remakeyourmeme:'remakeyourmeme', mediaio:'mediaio', kavel:'kavel', mv:'makeviral', rm:'remakeyourmeme', mio:'mediaio', kv:'kavel'}};
    if (p.has('src') && srcMap[p.get('src')]) {{
      srcFilter = srcMap[p.get('src')];
      setToggle('#bar-src', 'data-src', srcFilter);
    }}
    if (p.has('topic')) {{
      topicFilter = p.get('topic') || 'all';
      setToggle('#bar-topic', 'data-topic', topicFilter);
    }}
    if (p.has('date') && ['all','today','7d','30d','unknown'].includes(p.get('date'))) {{
      dateFilter = p.get('date');
      setToggle('#bar-date', 'data-date', dateFilter);
    }}
    if (p.has('prompt') && ['all','yes','no'].includes(p.get('prompt'))) {{
      promptFilter = p.get('prompt');
      setToggle('#bar-more', 'data-prompt', promptFilter);
    }}
    if (p.has('sort') && (p.get('sort') === 'new' || p.get('sort') === 'old')) {{
      sortOrder = p.get('sort');
      setToggle('#bar-more', 'data-sort', sortOrder);
    }}
    if (p.has('q')) q.value = p.get('q') || '';
  }} catch(_){{}}
}}

document.getElementById('toolbar').addEventListener('click', e => {{
  const btn = e.target.closest('button');
  if (!btn) return;
  if (btn.dataset.src !== undefined) {{
    srcFilter = btn.dataset.src;
    setToggle('#bar-src', 'data-src', srcFilter);
    render();
  }} else if (btn.dataset.topic !== undefined) {{
    topicFilter = btn.dataset.topic;
    setToggle('#bar-topic', 'data-topic', topicFilter);
    render();
  }} else if (btn.dataset.date !== undefined) {{
    dateFilter = btn.dataset.date;
    setToggle('#bar-date', 'data-date', dateFilter);
    render();
  }} else if (btn.dataset.prompt !== undefined) {{
    promptFilter = btn.dataset.prompt;
    setToggle('#bar-more', 'data-prompt', promptFilter);
    render();
  }} else if (btn.dataset.sort !== undefined) {{
    sortOrder = btn.dataset.sort;
    setToggle('#bar-more', 'data-sort', sortOrder);
    render();
  }}
}});

q.addEventListener('input', () => {{
  clearTimeout(searchTimer);
  searchTimer = setTimeout(render, 120);
}});

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
  const copyBtn = e.target.closest('[data-copy]');
  if (copyBtn) {{
    copyPrompt(+copyBtn.dataset.copy, copyBtn);
    return;
  }}
  if (e.target.closest('[data-close]')) closeModal();
}});
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
}});

applyUrl();
render();
</script>
</body>
</html>
'''
    (ROOT / 'index.html').write_text(html)
    dated = sum(1 for c in cards if c['date'])
    print(
        f'Wrote index.html with {len(cards)} cards '
        f'(MV={n_mv} RM={n_rm} MIO={n_mio} KV={n_kv} prompts={n_with_prompts} '
        f'prompt_files={n_prompt_files} dated={dated} unknown_date={len(cards)-dated})'
    )


if __name__ == '__main__':
    main()
