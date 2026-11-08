#!/usr/bin/env python3
"""Scrape MakeViral + Remake Your Meme, rebuild inventory (newest-first), docs, gallery.

Extra sources (Media.io, Kavel) are merged from on-disk folders after rebuild so a
MakeViral/Remake sync does not drop them. Run scripts/scrape_mediaio.py and
scripts/scrape_kavel.py separately (or via automation) to refresh those sources.
"""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse

# Checkout root (repo itself). Older runners used /workspace/awesome-meme-video.
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / '_raw'
SCRAPE_TZ = timezone(timedelta(hours=8))  # Asia/Shanghai
NOW = datetime.now(SCRAPE_TZ)
SCRAPE_DATE = NOW.strftime('%Y-%m-%d')
SCRAPE_ISO = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')

sys.path.insert(0, str(ROOT / 'scripts'))
from build_inventory import (  # noqa: E402
    parse_makeviral_md, parse_remake_html, write_template_folder,
)

def curl(url: str, dest: Path, timeout: int = 60) -> bool:
    ok, _ = curl_follow(url, dest, timeout=timeout)
    return ok

def curl_follow(url: str, dest: Path, timeout: int = 60) -> tuple[bool, str]:
    """Download URL following redirects; return (ok, final_url). Remake alias slugs 301 to shorter/trend URLs."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + '.part')
    cmd = ['curl', '-fsSL', '--retry', '3', '--retry-delay', '1',
           '-A', 'Mozilla/5.0 (compatible; awesome-meme-video-sync/1.0)',
           '--connect-timeout', '20', '--max-time', str(timeout),
           '-o', str(tmp), '-w', '%{url_effective}', url]
    try:
        effective = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
        tmp.replace(dest)
        return True, effective or url
    except subprocess.CalledProcessError:
        if tmp.exists():
            tmp.unlink()
        return False, url

def remake_slug_from_url(url: str) -> str | None:
    m = re.search(r'/templates/([a-z0-9\-]+)/?', url or '')
    return m.group(1) if m else None

def sha_file(p: Path) -> str:
    if not p.exists():
        return ''
    return hashlib.sha1(p.read_bytes()).hexdigest()

def fetch_makeviral_listing() -> list[str]:
    md_path = RAW / 'makeviral-templates.md'
    html_path = RAW / 'makeviral-templates.html'
    ok = curl('https://www.makeviral.ai/templates.md', md_path)
    curl('https://www.makeviral.ai/templates', html_path)
    text = md_path.read_text(errors='ignore') if ok else html_path.read_text(errors='ignore')
    slugs = sorted(set(re.findall(r'/templates/([a-z0-9][a-z0-9\-]{2,})(?:\.md|/|"|\'|\s|\)|\])', text)))
    skip = {'create', 'templates', 'index'}
    slugs = [s for s in slugs if s not in skip and not s.endswith('/create')]
    # Prefer .md listing when available — validate against known pattern
    if ok:
        md_slugs = sorted(set(re.findall(r'/templates/([a-z0-9][a-z0-9\-]*)\.md', text)))
        if len(md_slugs) >= 50:
            slugs = md_slugs
    (RAW / 'makeviral-slugs.txt').write_text('\n'.join(slugs) + '\n')
    return slugs

def fetch_remake_listing() -> list[str]:
    llms = RAW / 'remake-llms.txt'
    html_path = RAW / 'remake-templates.html'
    curl('https://remakeyourmeme.com/llms.txt', llms)
    curl('https://remakeyourmeme.com/templates/', html_path)
    slugs = []
    if llms.exists():
        urls = re.findall(r'https://remakeyourmeme\.com/templates/([a-z0-9\-]+)/?', llms.read_text(errors='ignore'))
        slugs = list(dict.fromkeys(urls))  # preserve order from llms (often newest-ish)
    if html_path.exists():
        hrefs = re.findall(r'href=["\']/?templates/([a-z0-9\-]+)/?["\']', html_path.read_text(errors='ignore'))
        # keep only full template slugs (not short aliases)
        href_set = set(hrefs)
        for s in hrefs:
            if s not in slugs and (
                s.endswith('-generator') or s.endswith('-trend') or s.endswith('-dance')
                or s.startswith('ai-') or 'video' in s or len(s) > 12
            ):
                # prefer lists that match existing inventory style
                pass
        # Prefer exact set from previous inventory if linked, else union of llms + catalog hrefs that look like templates
        catalog = []
        for s in hrefs:
            if s in ('templates',) or len(s) < 4:
                continue
            # Remake listing uses full slugs like hotel-lobby-ai-video-generator
            if s not in catalog:
                catalog.append(s)
        # Prefer llms order; fill missing from catalog that match known pattern
        if not slugs:
            slugs = catalog
        else:
            for s in catalog:
                if s not in slugs and ('-ai-' in s or s.startswith('ai-') or s.endswith('-dance')):
                    slugs.append(s)
    # Deduplicate preferring longer canonical names already in inventory
    (RAW / 'remake-slugs.txt').write_text('\n'.join(slugs) + '\n')
    return slugs

def fetch_all_makeviral(slugs: list[str]) -> dict:
    out = RAW / 'makeviral-md'
    out.mkdir(exist_ok=True)
    added, updated, unchanged, failed = [], [], [], []
    urls = [(s, f'https://www.makeviral.ai/templates/{s}.md', out / f'{s}.md') for s in slugs]

    def one(item):
        s, url, dest = item
        old = sha_file(dest)
        existed = dest.exists()
        ok = curl(url, dest)
        if not ok:
            return ('fail', s)
        new = sha_file(dest)
        if not existed:
            return ('added', s)
        if old != new:
            return ('updated', s)
        return ('unchanged', s)

    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(one, u) for u in urls]
        for f in as_completed(futs):
            kind, s = f.result()
            if kind == 'added':
                added.append(s)
            elif kind == 'updated':
                updated.append(s)
            elif kind == 'fail':
                failed.append(s)
            else:
                unchanged.append(s)
    log = RAW / 'makeviral-md-fetch.log'
    log.write_text(
        f'scrape={SCRAPE_ISO}\nadded={len(added)} updated={len(updated)} unchanged={len(unchanged)} fail={len(failed)}\n'
        + '\n'.join(f'ADDED {s}' for s in sorted(added)) + '\n'
        + '\n'.join(f'UPDATED {s}' for s in sorted(updated)) + '\n'
        + '\n'.join(f'FAIL {s}' for s in sorted(failed)) + '\n'
    )
    (RAW / 'makeviral-md-urls.txt').write_text(
        '\n'.join(f'https://www.makeviral.ai/templates/{s}.md' for s in slugs) + '\n'
    )
    return {'added': sorted(added), 'updated': sorted(updated), 'unchanged': sorted(unchanged), 'failed': sorted(failed)}

def fetch_all_remake(slugs: list[str]) -> dict:
    """Fetch Remake template HTML. Alias slugs that 301 to a new path are saved under the
    canonical slug only (treated as rename/update), so redirects do not create duplicates.
    """
    out = RAW / 'remake-html'
    out.mkdir(exist_ok=True)
    added, updated, unchanged, failed, renamed = [], [], [], [], []

    def one(s):
        url = f'https://remakeyourmeme.com/templates/{s}/'
        # Always land body in a temp path first so a redirect can retarget the dest slug.
        tmp_dest = out / f'{s}.html.partfetch'
        ok, effective = curl_follow(url, tmp_dest, timeout=90)
        if not ok:
            if tmp_dest.exists():
                tmp_dest.unlink()
            return ('fail', s, s)
        canon = remake_slug_from_url(effective) or s
        dest = out / f'{canon}.html'
        old = sha_file(dest)
        existed = dest.exists()
        # Move/replace canonical file
        if dest.exists():
            dest.unlink()
        tmp_dest.replace(dest)
        # Drop stale alias HTML if request slug redirected away
        if canon != s:
            alias = out / f'{s}.html'
            if alias.exists():
                alias.unlink()
            return ('renamed', s, canon)
        new = sha_file(dest)
        if not existed:
            return ('added', s, s)
        if old != new:
            return ('updated', s, s)
        return ('unchanged', s, s)

    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(one, s) for s in slugs]
        for f in as_completed(futs):
            kind, req, canon = f.result()
            if kind == 'added':
                added.append(canon)
            elif kind == 'updated':
                updated.append(canon)
            elif kind == 'renamed':
                renamed.append(f'{req}->{canon}')
                # A rename that lands on an existing page is an update of the canonical slug
                if canon not in updated and canon not in added:
                    updated.append(canon)
            elif kind == 'fail':
                failed.append(req)
            else:
                unchanged.append(canon)
    # Deduplicate list entries while preserving order
    def uniq(xs):
        seen, outl = set(), []
        for x in xs:
            if x not in seen:
                seen.add(x); outl.append(x)
        return outl
    added, updated, unchanged = uniq(added), uniq(updated), uniq(unchanged)
    (RAW / 'remake-html-fetch.log').write_text(
        f'scrape={SCRAPE_ISO}\nadded={len(added)} updated={len(updated)} unchanged={len(unchanged)} '
        f'renamed={len(renamed)} fail={len(failed)}\n'
        + '\n'.join(f'ADDED {s}' for s in sorted(added)) + '\n'
        + '\n'.join(f'UPDATED {s}' for s in sorted(updated)) + '\n'
        + '\n'.join(f'RENAMED {s}' for s in sorted(renamed)) + '\n'
        + '\n'.join(f'FAIL {s}' for s in sorted(failed)) + '\n'
    )
    # URL list = HTML stems actually on disk after redirect resolution
    on_disk = sorted(p.stem for p in out.glob('*.html'))
    (RAW / 'remake-urls.txt').write_text(
        '\n'.join(f'https://remakeyourmeme.com/templates/{s}/' for s in on_disk) + '\n'
    )
    return {
        'added': sorted(added),
        'updated': sorted(updated),
        'unchanged': sorted(unchanged),
        'renamed': sorted(renamed),
        'failed': sorted(failed),
    }

def listing_date(item: dict) -> str:
    """Source listing/inclusion date only. Never scraped_at (missing → empty/unknown)."""
    d = item.get('published') or item.get('updated') or ''
    return str(d)[:10] if d else ''


def sort_key(item: dict):
    """Newest-first by published||updated; undated → end; never scraped_at."""
    d = listing_date(item) or '0000-00-00'
    return (d, item.get('slug') or '')


def dedupe_remake_by_name(items: list[dict]) -> list[dict]:
    """Keep one Remake template per display name. Prefer non-*-ai-video-generator slugs
    (canonical trend/short URLs after site redirects) and richer demo lists.
    """
    def score(it: dict) -> tuple:
        slug = it.get('slug') or ''
        alias = 1 if slug.endswith('-ai-video-generator') else 0
        demos = len(it.get('demo_videos') or []) + len(it.get('preview_videos') or [])
        posters = len(it.get('posters') or [])
        return (-alias, demos, posters, -len(slug))  # higher better; prefer non-alias, more media, shorter slug

    best: dict[str, dict] = {}
    order: list[str] = []
    for it in items:
        key = (it.get('name') or it.get('slug') or '').strip().casefold()
        if not key:
            key = it.get('slug') or id(it)
        if key not in best:
            best[key] = it
            order.append(key)
        else:
            if score(it) > score(best[key]):
                best[key] = it
    return [best[k] for k in order]

def rebuild_inventory(mv_change: dict, rm_change: dict) -> dict:
    OUT_MV = ROOT / 'makeviral'
    OUT_RM = ROOT / 'remakeyourmeme'
    mv_items = []
    for p in sorted((RAW / 'makeviral-md').glob('*.md')):
        item = parse_makeviral_md(p)
        item['scraped_at'] = SCRAPE_DATE
        write_template_folder(item, OUT_MV)
        (OUT_MV / item['slug'] / 'source.md').write_text(p.read_text(errors='ignore'))
        mv_items.append(item)

    rm_items = []
    for p in sorted((RAW / 'remake-html').glob('*.html')):
        item = parse_remake_html(p)
        item['scraped_at'] = SCRAPE_DATE
        # Remake has no public publish date — use scrape date for sort consistency
        if not item.get('published'):
            item['published'] = None
        if not item.get('updated'):
            item['updated'] = None
        # Prefer slug from URL path when HTML still carries an old alias filename
        canon = remake_slug_from_url(item.get('url') or '')
        if canon and canon != item.get('slug'):
            item['slug'] = canon
        rm_items.append(item)

    # Collapse same-title Remake pairs (redirect aliases vs canonical trend/short slugs)
    rm_items = dedupe_remake_by_name(rm_items)
    for item in rm_items:
        write_template_folder(item, OUT_RM)

    # Sort each source newest-first, then concatenate MV then RM? Or global?
    # Spec: sort listings / inventory newest-first. Sort all together by date key.
    all_items = mv_items + rm_items
    all_items.sort(key=sort_key, reverse=True)

    inventory = {
        'generated_at': SCRAPE_DATE,
        'generated_at_iso': SCRAPE_ISO,
        'sorted_by': 'published || updated (newest first); undated=unknown; never scraped_at',
        'sources': {
            'makeviral': {
                'listing': 'https://www.makeviral.ai/templates',
                'count': len(mv_items),
                'with_prompts': sum(1 for i in mv_items if i['prompt_count'] > 0),
                'total_prompt_blocks': sum(i['prompt_count'] for i in mv_items),
                'total_demo_videos': sum(len(i['demo_videos']) for i in mv_items),
                'sync': {k: mv_change.get(k, []) for k in ('added', 'updated', 'failed')},
            },
            'remakeyourmeme': {
                'listing': 'https://remakeyourmeme.com/templates/',
                'count': len(rm_items),
                'with_prompts': sum(1 for i in rm_items if i['prompt_count'] > 0),
                'note': 'Public pages do not expose copyable prompts; alias *-ai-video-generator URLs that 301 are collapsed to the canonical slug',
                'total_demo_videos': sum(len(i.get('demo_videos') or []) for i in rm_items),
                'sync': {k: rm_change.get(k, []) for k in ('added', 'updated', 'failed')},
            },
        },
        'templates': all_items,
    }
    (ROOT / 'inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')

    # download lists
    all_videos, all_posters = [], []
    for i in all_items:
        for u in i.get('demo_videos') or []:
            all_videos.append((i['source'], i['slug'], u))
        for u in (i.get('posters') or [])[:3]:
            all_posters.append((i['source'], i['slug'], u))
    seen = set()
    videos_dedup = []
    for row in all_videos:
        if row[2] not in seen:
            seen.add(row[2]); videos_dedup.append(row)
    seen = set()
    posters_dedup = []
    for row in all_posters:
        if row[2] not in seen:
            seen.add(row[2]); posters_dedup.append(row)
    (RAW / 'download-videos.tsv').write_text('\n'.join(f'{s}\t{sl}\t{u}' for s, sl, u in videos_dedup) + '\n')
    (RAW / 'download-posters.tsv').write_text('\n'.join(f'{s}\t{sl}\t{u}' for s, sl, u in posters_dedup) + '\n')
    return inventory


def merge_extra_sources(inv: dict) -> dict:
    """Merge Media.io + Kavel items from on-disk folders into MV/RM inventory."""
    mediaio_items = []
    mio_dir = ROOT / 'mediaio'
    if mio_dir.exists():
        for meta in sorted(mio_dir.glob('*/meta.json')):
            try:
                mediaio_items.append(json.loads(meta.read_text()))
            except Exception:
                pass

    kavel_items = []
    kav_dir = ROOT / 'kavel'
    if kav_dir.exists():
        for meta in sorted(kav_dir.glob('*/meta.json')):
            try:
                kavel_items.append(json.loads(meta.read_text()))
            except Exception:
                pass

    # Keep only MV/RM from current rebuild; replace mediaio/kavel from disk
    others = [
        t for t in inv.get('templates', [])
        if t.get('source') not in ('mediaio', 'kavel')
    ]
    all_items = others + mediaio_items + kavel_items
    all_items.sort(key=sort_key, reverse=True)

    sources = dict(inv.get('sources') or {})
    if mediaio_items:
        prev_mio = sources.get('mediaio') or {}
        mio_sync = {}
        mio_sum = RAW / 'mediaio-sync-summary.json'
        if mio_sum.exists():
            try:
                mio_sync = json.loads(mio_sum.read_text())
            except Exception:
                pass
        sources['mediaio'] = {
            **prev_mio,
            'listing': prev_mio.get(
                'listing',
                'https://www.media.io/ai/explore/zone/ai-video-trend-generator',
            ),
            'listing_zh': prev_mio.get(
                'listing_zh',
                'https://www.media.io/ai/zh/explore/zone/ai-video-trend-generator',
            ),
            'count': len(mediaio_items),
            'with_prompts': sum(1 for i in mediaio_items if i.get('prompt_count', 0) > 0),
            'total_prompt_blocks': sum(i.get('prompt_count', 0) for i in mediaio_items),
            'total_demo_videos': sum(len(i.get('demo_videos') or []) for i in mediaio_items),
            'sync': {
                'added': mio_sync.get('added', []),
                'updated': mio_sync.get('updated', []),
                'failed': mio_sync.get('failed', []),
            },
        }
    if kavel_items:
        prev_kav = sources.get('kavel') or {}
        kav_sync = {}
        kav_sum = RAW / 'kavel-sync-summary.json'
        if kav_sum.exists():
            try:
                kav_sync = json.loads(kav_sum.read_text())
            except Exception:
                pass
        sources['kavel'] = {
            **prev_kav,
            'listing': prev_kav.get('listing', 'https://www.kavel.ai/ai-video-trends'),
            'count': len(kavel_items),
            'with_prompts': sum(1 for i in kavel_items if i.get('prompt_count', 0) > 0),
            'total_prompt_blocks': sum(i.get('prompt_count', 0) for i in kavel_items),
            'total_demo_videos': sum(len(i.get('demo_videos') or []) for i in kavel_items),
            'note': prev_kav.get('note') or (
                'Prompts extracted verbatim from public Next.js RSC payloads '
                '(form hub prompt + showcase templatePrompt) when present; '
                'detail URLs are /video/<slug>. Deduped by canonical slug.'
            ),
            'sync': {
                'added': kav_sync.get('added', []),
                'updated': kav_sync.get('updated', []),
                'failed': kav_sync.get('failed', []),
            },
        }

    inv = {
        'generated_at': SCRAPE_DATE,
        'generated_at_iso': SCRAPE_ISO,
        'sorted_by': inv.get('sorted_by')
        or 'published || updated (newest first); undated=unknown; never scraped_at',
        'sources': sources,
        'templates': all_items,
    }
    (ROOT / 'inventory.json').write_text(json.dumps(inv, ensure_ascii=False, indent=2) + '\n')
    return inv

def has_local_demo(src: str, slug: str) -> bool:
    d = ROOT / ('makeviral' if src == 'makeviral' else 'remakeyourmeme') / slug / 'demos'
    if not d.exists():
        return False
    return any(p.suffix.lower() in ('.mp4', '.webm') for p in d.iterdir())

def write_readme(inv: dict):
    def section(src: str) -> list[dict]:
        return sorted(
            [t for t in inv['templates'] if t.get('source') == src],
            key=sort_key,
            reverse=True,
        )

    mv = section('makeviral')
    rm = section('remakeyourmeme')
    mio = section('mediaio')
    kav = section('kavel')
    s = inv['sources']
    s_mv = s['makeviral']
    s_rm = s['remakeyourmeme']
    s_mio = s.get('mediaio') or {}
    s_kav = s.get('kavel') or {}
    total = len(inv['templates'])
    lines = [
        '# Awesome Meme Video',
        '',
        '> 公开 AI 迷因 / 病毒视频模板与提示词清单（MakeViral · Remake Your Meme · Media.io · Kavel）。',
        '>',
        '> Public inventory of AI meme / viral video templates and prompts.',
        '',
        '## Stats',
        '',
        f"- **Total**: {total} templates",
        f"- **MakeViral**: {s_mv['count']} templates · {s_mv['total_prompt_blocks']} prompt blocks · {s_mv['total_demo_videos']} demo videos",
        f"- **Remake Your Meme**: {s_rm['count']} templates · public prompts: **none** (one-tap remake only) · demos/posters archived",
        f"- **Media.io**: {s_mio.get('count', 0)} templates · {s_mio.get('total_prompt_blocks', 0)} prompt blocks · {s_mio.get('total_demo_videos', 0)} demo videos",
        f"- **Kavel**: {s_kav.get('count', 0)} templates · {s_kav.get('total_prompt_blocks', 0)} prompt blocks · {s_kav.get('total_demo_videos', 0)} demo videos",
        f"- Scraped: {inv['generated_at']} (Asia/Shanghai)",
        f"- Sort: **newest first** by `{inv['sorted_by']}`",
        f"- Gallery: https://xianyu110.github.io/awesome-meme-video/",
        '',
        '## Sources',
        '',
        '| Site | Listing | Notes |',
        '| --- | --- | --- |',
        '| [MakeViral](https://www.makeviral.ai/templates) | `/templates` + per-page `.md` | Full prompts published; demos under `/media/templates/...` |',
        '| [Remake Your Meme](https://remakeyourmeme.com/templates/) | `/templates/` | No copyable prompts on public pages; CDN demos kept |',
        '| [Media.io](https://www.media.io/ai/explore/zone/ai-video-trend-generator) | AI Video Trend Generator zone | Prompts from public `aigc_config` when present |',
        '| [Kavel](https://www.kavel.ai/ai-video-trends) | `/ai-video-trends` · `/video/<slug>` | Prompts from public RSC payloads when present |',
        '',
        '## Layout',
        '',
        '```',
        'awesome-meme-video/',
        '  index.html          # GitHub Pages gallery (newest first)',
        '  README.md',
        '  PROMPTS.md          # all MakeViral prompts concatenated',
        '  inventory.json      # machine-readable index',
        '  makeviral/<slug>/',
        '  remakeyourmeme/<slug>/',
        '  mediaio/<slug>/',
        '  kavel/<slug>/',
        '```',
        '',
        'Demo MP4s are stored via Git LFS when present. Each template folder also lists original CDN URLs in `MEDIA.md` / `PROMPTS.md`.',
        '',
        '## Contents',
        '',
    ]

    def has_demo(src: str, slug: str, t: dict) -> bool:
        d = ROOT / src / slug / 'demos'
        if d.exists() and any(p.suffix.lower() in ('.mp4', '.webm') for p in d.iterdir()):
            return True
        return bool(t.get('demo_videos'))

    def append_table(title: str, items: list[dict], src: str, prompt_cell):
        lines.append(f'### {title}')
        lines.append('')
        lines.append('| Template | Slug | Date | Prompts | Demo | Page |')
        lines.append('| --- | --- | --- | ---: | --- | --- |')
        for t in items:
            date = listing_date(t) or 'unknown'
            demo = '✅' if has_demo(src, t['slug'], t) else '—'
            pc = prompt_cell(t)
            lines.append(
                f"| [{t['name']}]({src}/{t['slug']}/PROMPTS.md) | `{t['slug']}` | {date} | {pc} | {demo} | [link]({t['url']}) |"
            )
        lines.append('')

    append_table('MakeViral', mv, 'makeviral', lambda t: t.get('prompt_count') or 0)
    append_table('Remake Your Meme', rm, 'remakeyourmeme', lambda t: 'no (one-tap)')
    append_table('Media.io', mio, 'mediaio', lambda t: t.get('prompt_count') or 0)
    append_table('Kavel', kav, 'kavel', lambda t: t.get('prompt_count') or 0)

    lines += [
        '## Attribution & license',
        '',
        'Templates, prompts, and demo media remain copyright of their respective sites and creators:',
        '',
        '- MakeViral — https://www.makeviral.ai',
        '- Remake Your Meme — https://remakeyourmeme.com',
        '- Media.io — https://www.media.io',
        '- Kavel — https://www.kavel.ai',
        '',
        'This repository is an **inventory / awesome-list** for discovery and research. Re-check each site’s terms before commercial reuse. Example people/pets in demos are described by the sources as AI-generated.',
        '',
        '## Disclaimer',
        '',
        'Prompts are copied verbatim from public pages — nothing invented. Remake Your Meme pages explicitly say there is no prompt to write; we do not fabricate prompts for those entries. Media.io / Kavel entries without a public prompt are marked accordingly.',
        '',
    ]
    (ROOT / 'README.md').write_text('\n'.join(lines))


def write_prompts_md(inv: dict):
    mv = [t for t in inv['templates'] if t['source'] == 'makeviral']
    mv = sorted(mv, key=sort_key, reverse=True)
    total = sum(t['prompt_count'] for t in mv)
    lines = [
        '# All prompts (MakeViral)',
        '',
        f'> {total} prompt blocks from {len(mv)} public template markdown pages.',
        '>',
        '> Remake Your Meme does not publish prompts; see `remakeyourmeme/*/PROMPTS.md` for metadata only.',
        '>',
        f"> Sorted newest-first by published||updated ({inv['generated_at']}; undated=unknown).",
        '',
    ]
    for t in mv:
        lines += [
            f"## {t['name']}",
            '',
            f"- Page: {t['url']}",
            f"- Markdown: {t.get('markdown_url')}",
            f"- Updated: {t.get('updated') or '—'} · Published: {t.get('published') or '—'}",
            f"- Local: [`makeviral/{t['slug']}/PROMPTS.md`](makeviral/{t['slug']}/PROMPTS.md)",
            '',
        ]
        for i, p in enumerate(t.get('prompts') or [], 1):
            label = p.get('label') or f'Prompt {i}'
            variant = f" — {p['variant']}" if p.get('variant') else ''
            lines += [f"### {label}{variant}", '', '```text', p['text'], '```', '']
        lines.append('---')
        lines.append('')
    (ROOT / 'PROMPTS.md').write_text('\n'.join(lines))

def write_sources():
    (ROOT / 'SOURCES.md').write_text(
        '# Sources\n\n'
        '## MakeViral\n'
        '- Listing: https://www.makeviral.ai/templates\n'
        '- Per-template markdown: `https://www.makeviral.ai/templates/<slug>.md`\n'
        '- Demo media: `https://www.makeviral.ai/media/templates/<slug>/...`\n\n'
        '## Remake Your Meme\n'
        '- Listing: https://remakeyourmeme.com/templates/\n'
        '- CDN: https://cdn.remakeyourmeme.com/\n'
        '- `llms.txt`: https://remakeyourmeme.com/llms.txt\n'
        '- Public template pages do **not** expose copyable prompt text.\n\n'
        '## Media.io\n'
        '- Listing: https://www.media.io/ai/explore/zone/ai-video-trend-generator\n'
        '- ZH: https://www.media.io/ai/zh/explore/zone/ai-video-trend-generator\n'
        '- Prompts extracted verbatim from public `aigc_config` when present.\n\n'
        '## Kavel\n'
        '- Listing: https://www.kavel.ai/ai-video-trends\n'
        '- Detail: `https://www.kavel.ai/video/<slug>`\n'
        '- CDN: https://cdn.kavel.ai/\n'
        '- Scrape: Next.js RSC flight HTML; prompts from hub `prompt` + showcase `templatePrompt` when present.\n\n'
        '## Sort rule\n'
        'Inventory, README tables, PROMPTS.md, and the Pages gallery are sorted **newest first** by:\n'
        '`published` → else `updated`. **Never** use `scraped_at` as the listing date.\n'
        'If a source has no public publish/update date, display **unknown** (sort to the end).\n\n'
        f'Synced {SCRAPE_ISO} (Asia/Shanghai) for the awesome-meme-video inventory.\n'
    )

def main():
    RAW.mkdir(exist_ok=True)
    print('== listing ==', flush=True)
    mv_slugs = fetch_makeviral_listing()
    rm_slugs = fetch_remake_listing()
    # Union previously fetched Remake HTML stems, but drop *-ai-video-generator aliases
    # when a non-alias sibling already appears in the listing (site 301 redirects).
    existing_rm = [p.stem for p in (RAW / 'remake-html').glob('*.html')]
    rm_set = set(rm_slugs)
    if existing_rm:
        for s in existing_rm:
            if s in rm_set:
                continue
            if s.endswith('-ai-video-generator'):
                # skip stale alias files; fetch_all_remake will also redirect-resolve
                continue
            rm_slugs.append(s)
            rm_set.add(s)
    print(f'makeviral slugs={len(mv_slugs)} remake slugs={len(rm_slugs)}', flush=True)

    print('== fetch makeviral md ==', flush=True)
    mv_change = fetch_all_makeviral(mv_slugs)
    print(json.dumps({k: len(v) for k, v in mv_change.items()}), flush=True)

    print('== fetch remake html ==', flush=True)
    rm_change = fetch_all_remake(rm_slugs)
    print(json.dumps({k: len(v) for k, v in rm_change.items()}), flush=True)

    print('== rebuild inventory ==', flush=True)
    inv = rebuild_inventory(mv_change, rm_change)
    print('== merge mediaio + kavel ==', flush=True)
    inv = merge_extra_sources(inv)
    write_readme(inv)
    write_prompts_md(inv)
    write_sources()
    print(json.dumps({
        'makeviral': inv['sources']['makeviral']['count'],
        'remake': inv['sources']['remakeyourmeme']['count'],
        'mv_added': mv_change['added'],
        'mv_updated': mv_change['updated'][:20],
        'mv_updated_n': len(mv_change['updated']),
        'rm_added': rm_change['added'],
        'rm_updated_n': len(rm_change['updated']),
        'sorted_by': inv['sorted_by'],
    }, indent=2), flush=True)
    # write sync summary for outer runner
    summary = {
        'scraped_at': SCRAPE_ISO,
        'makeviral': mv_change,
        'remakeyourmeme': rm_change,
        'totals': {
            'makeviral': inv['sources']['makeviral']['count'],
            'remakeyourmeme': inv['sources']['remakeyourmeme']['count'],
            'mediaio': (inv['sources'].get('mediaio') or {}).get('count', 0),
            'kavel': (inv['sources'].get('kavel') or {}).get('count', 0),
            'prompt_blocks': inv['sources']['makeviral']['total_prompt_blocks'],
        },
        'sorted_by': inv['sorted_by'],
    }
    (RAW / 'sync-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    return summary

if __name__ == '__main__':
    main()
