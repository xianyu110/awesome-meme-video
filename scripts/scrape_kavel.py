#!/usr/bin/env python3
"""Scrape Kavel AI Video Trends (https://www.kavel.ai/ai-video-trends) into kavel/<slug>/.

Listing + detail pages are Next.js App Router; trend cards and public prompts live in
RSC flight payloads (self.__next_f.push). No dedicated public JSON API.

Prompts are copied verbatim from public page payloads (form hub `prompt` + showcase
`templatePrompt` fields). Never invent prompts — if absent, prompt_count=0.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path('/workspace/awesome-meme-video')
RAW = ROOT / '_raw'
OUT = ROOT / 'kavel'
BLOB = ROOT / '_blobs'
SCRAPE_TZ = timezone(timedelta(hours=8))
NOW = datetime.now(SCRAPE_TZ)
SCRAPE_DATE = NOW.strftime('%Y-%m-%d')
SCRAPE_ISO = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
LISTING_URL = 'https://www.kavel.ai/ai-video-trends'
UA = 'Mozilla/5.0 (compatible; awesome-meme-video-sync/1.0)'

LISTING_ITEM_RE = re.compile(
    r'\{"slug":"([a-z0-9\-]+)",'
    r'"href":"(/video/[a-z0-9\-]+)",'
    r'"title":"((?:[^"\\]|\\.)*)",'
    r'"desc":"((?:[^"\\]|\\.)*)",'
    r'"thumb":"([^"]*)",'
    r'"video":"([^"]*)",'
    r'"poster":"([^"]*)",'
    r'"rank":([^}]+)\}'
)


def curl_follow(url: str, dest: Path, timeout: int = 90) -> tuple[bool, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + '.part')
    cmd = [
        'curl', '-fsSL', '--retry', '3', '--retry-delay', '1',
        '-A', UA, '--connect-timeout', '20', '--max-time', str(timeout),
        '-o', str(tmp), '-w', '%{url_effective}', url,
    ]
    try:
        effective = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
        tmp.replace(dest)
        return True, effective or url
    except subprocess.CalledProcessError:
        if tmp.exists():
            tmp.unlink()
        return False, url


def decode_flight(html: str) -> str:
    parts = re.findall(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)', html)
    out = []
    for p in parts:
        try:
            out.append(p.encode('utf-8').decode('unicode_escape'))
        except Exception:
            out.append(p)
    return '\n'.join(out)


def unescape_js_str(s: str) -> str:
    try:
        return json.loads('"' + s.replace('\n', '\\n').replace('\r', '\\r') + '"')
    except Exception:
        return (
            s.replace('\\"', '"')
            .replace('\\n', '\n')
            .replace('\\/', '/')
            .replace('\\u0026', '&')
        )


def slug_from_video_url(url: str) -> str | None:
    m = re.search(r'/video/([a-z0-9\-]+)/?', url or '')
    return m.group(1) if m else None


def filename_from_url(url: str) -> str:
    name = Path(unquote(urlparse(url).path)).name
    if not name or '.' not in name:
        name = hashlib.sha1(url.encode()).hexdigest()[:16] + '.bin'
    return name


def download_to(url: str, dest: Path) -> tuple[bool, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return True, 'exists'
    tmp = dest.with_suffix(dest.suffix + '.part')
    cmd = [
        'curl', '-fsSL', '--retry', '3', '--retry-delay', '1',
        '-A', UA, '--connect-timeout', '20', '--max-time', '120',
        '-o', str(tmp), url,
    ]
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        if tmp.exists():
            tmp.unlink()
        return False, 'fail'
    data = tmp.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    blob = BLOB / digest[:2] / digest
    blob.parent.mkdir(parents=True, exist_ok=True)
    if not blob.exists():
        tmp.replace(blob)
    else:
        tmp.unlink()
    if dest.exists():
        dest.unlink()
    try:
        dest.hardlink_to(blob)
    except OSError:
        import os
        os.symlink(os.path.relpath(blob, dest.parent), dest)
    return True, digest[:12]


def parse_listing(html: str) -> tuple[list[dict], list[dict]]:
    """Return (all_newest_first, this_week) trend cards from RSC flight data."""
    big = decode_flight(html)
    week: list[dict] = []
    all_list: list[dict] = []
    for m in LISTING_ITEM_RE.finditer(big):
        slug, href, title, desc, thumb, video, poster, rank_raw = m.groups()
        rank_raw = rank_raw.strip()
        item = {
            'slug': slug,
            'href': href,
            'title': unescape_js_str(title),
            'desc': unescape_js_str(desc),
            'thumb': thumb,
            'video': video,
            'poster': poster,
            'rank': int(rank_raw) if rank_raw.isdigit() else None,
        }
        if item['rank'] is not None:
            week.append(item)
        else:
            all_list.append(item)
    # Deduplicate all list by slug (preserve first = newest-first order)
    seen: set[str] = set()
    all_dedup: list[dict] = []
    for it in all_list:
        if it['slug'] in seen:
            continue
        seen.add(it['slug'])
        all_dedup.append(it)
    # Deduplicate this-week by slug
    wseen: set[str] = set()
    week_dedup: list[dict] = []
    for it in sorted(week, key=lambda x: x['rank'] or 999):
        if it['slug'] in wseen:
            continue
        wseen.add(it['slug'])
        week_dedup.append(it)
    return all_dedup, week_dedup


def extract_hub_prompt(flight: str) -> str | None:
    """Main template prompt from the video tool form (hub/model/mode/tab/prompt)."""
    m = re.search(
        r'"hub"\s*:\s*"[^"]*"\s*,\s*"model"\s*:\s*"[^"]*"\s*,\s*"mode"\s*:\s*"[^"]*"'
        r'\s*,\s*"tab"\s*:\s*"[^"]*"\s*,\s*"prompt"\s*:\s*"((?:[^"\\]|\\.){40,})"',
        flight,
    )
    if not m:
        # fallback: tab then long prompt
        m = re.search(
            r'"tab"\s*:\s*"[^"]*"\s*,\s*"prompt"\s*:\s*"((?:[^"\\]|\\.){80,})"',
            flight,
        )
    if not m:
        return None
    return unescape_js_str(m.group(1)).strip() or None


def extract_showcases(flight: str, slug: str) -> list[dict]:
    """Showcase demo clips with optional per-variant templatePrompt."""
    out: list[dict] = []
    # Objects that carry templatePrompt and tag the slug
    for m in re.finditer(r'"templatePrompt"\s*:\s*"((?:[^"\\]|\\.)*)"', flight):
        start = flight.rfind('{', max(0, m.start() - 2500), m.start())
        if start < 0:
            continue
        depth = 0
        end = None
        for i in range(start, min(len(flight), start + 10000)):
            ch = flight[i]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            continue
        raw = flight[start:end]
        if f'"{slug}"' not in raw and f'/{slug}' not in raw:
            # still accept if tags include slug-ish
            if slug not in raw:
                continue
        # Pull fields via regex (avoid brittle json on $undefined)
        def field(key: str) -> str | None:
            fm = re.search(rf'"{key}"\s*:\s*"((?:[^"\\]|\\.)*)"', raw)
            return unescape_js_str(fm.group(1)) if fm else None

        tp = unescape_js_str(m.group(1)).strip()
        video = field('video') or field('src')
        poster = field('poster')
        title = field('title')
        sid = field('id')
        if not tp and not video:
            continue
        out.append({
            'id': sid,
            'title': title,
            'video': video,
            'poster': poster,
            'template_prompt': tp or None,
        })
    # Deduplicate by video URL or prompt text
    seen: set[str] = set()
    dedup: list[dict] = []
    for s in out:
        key = s.get('video') or s.get('template_prompt') or s.get('id') or json.dumps(s)
        if key in seen:
            continue
        seen.add(key)
        dedup.append(s)
    return dedup


def parse_detail(html: str, slug: str, listing: dict) -> dict:
    flight = decode_flight(html)
    hub_prompt = extract_hub_prompt(flight)
    showcases = extract_showcases(flight, slug)

    prompts: list[dict] = []
    seen_text: set[str] = set()

    def add_prompt(text: str | None, label: str, variant: str | None = None):
        if not text or len(text.strip()) < 40:
            return
        text = text.strip()
        h = hashlib.sha1(text.encode()).hexdigest()
        if h in seen_text:
            return
        seen_text.add(h)
        prompts.append({
            'label': label,
            'variant': variant,
            'kind': 'video_prompt',
            'text': text,
        })

    add_prompt(hub_prompt, 'Template prompt')
    for sc in showcases:
        label = sc.get('title') or sc.get('id') or 'Showcase variant'
        add_prompt(sc.get('template_prompt'), label, variant=sc.get('id'))

    demo_videos: list[str] = []
    posters: list[str] = []
    for u in [listing.get('video'), *(sc.get('video') for sc in showcases)]:
        if u and u not in demo_videos and u.endswith('.mp4'):
            demo_videos.append(u)
    for u in [listing.get('poster'), listing.get('thumb'), *(sc.get('poster') for sc in showcases)]:
        if u and u not in posters:
            posters.append(u)

    return {
        'hub_prompt': hub_prompt,
        'showcases': showcases,
        'prompts': prompts,
        'demo_videos': demo_videos,
        'posters': posters,
    }


def write_template(item: dict) -> Path:
    d = OUT / item['slug']
    d.mkdir(parents=True, exist_ok=True)
    (d / 'meta.json').write_text(json.dumps(item, ensure_ascii=False, indent=2) + '\n')
    lines = [
        f"# {item['name']}",
        '',
        f"- Source: [kavel]({item['url']})",
        f"- Slug: `{item['slug']}`",
        f"- Listing: {item.get('listing_url')}",
        '',
    ]
    if item.get('blurb'):
        lines += [item['blurb'], '']
    if item.get('this_week_rank'):
        lines += [f"- This week rank on Kavel: #{item['this_week_rank']}", '']
    if item.get('demo_videos'):
        lines += ['## Demo videos (CDN)', ''] + [f"- {u}" for u in item['demo_videos']] + ['']
    if item.get('posters'):
        lines += ['## Posters', ''] + [f"- {u}" for u in item['posters'][:12]] + ['']
    prompts = item.get('prompts') or []
    if prompts:
        lines += ['## Prompts', '']
        for i, p in enumerate(prompts, 1):
            label = p.get('label') or f'Prompt {i}'
            variant = f" — {p['variant']}" if p.get('variant') else ''
            lines += [
                f"### {i}. {label}{variant}",
                '',
                f"*Kind: {p.get('kind') or 'prompt'}*",
                '',
                '```text',
                p['text'],
                '```',
                '',
            ]
    else:
        lines += [
            '## Prompts',
            '',
            item.get('note')
            or 'No public prompt text found on this Kavel template page; archived demos/posters only — prompts not invented.',
            '',
        ]
    (d / 'PROMPTS.md').write_text('\n'.join(lines) + '\n')
    media = [f"# Media — {item['name']}", '']
    for u in item.get('demo_videos') or []:
        media.append(f'- video: {u}')
    for u in item.get('posters') or []:
        media.append(f'- poster: {u}')
    (d / 'MEDIA.md').write_text('\n'.join(media) + '\n')
    return d


def sort_key(item: dict):
    d = item.get('published') or item.get('updated') or '0000-00-00'
    return (str(d)[:10], item.get('slug') or '')


def merge_into_inventory(kavel_items: list[dict], kavel_sync: dict) -> dict:
    """Merge kavel (+ keep mediaio from disk) into inventory.json with MV/RM."""
    inv_path = ROOT / 'inventory.json'
    if inv_path.exists():
        inv = json.loads(inv_path.read_text())
    else:
        inv = {'templates': [], 'sources': {}}

    # Prefer live mediaio folders if present
    mediaio_items = []
    mio_dir = ROOT / 'mediaio'
    if mio_dir.exists():
        for meta in sorted(mio_dir.glob('*/meta.json')):
            try:
                mediaio_items.append(json.loads(meta.read_text()))
            except Exception:
                pass
    if not mediaio_items:
        mediaio_items = [t for t in inv.get('templates', []) if t.get('source') == 'mediaio']

    others = [
        t for t in inv.get('templates', [])
        if t.get('source') not in ('kavel', 'mediaio')
    ]
    # Drop any stale kavel entries; replace with fresh scrape
    all_items = others + mediaio_items + kavel_items
    all_items.sort(key=sort_key, reverse=True)

    sources = dict(inv.get('sources') or {})
    sources['kavel'] = {
        'listing': LISTING_URL,
        'count': len(kavel_items),
        'with_prompts': sum(1 for i in kavel_items if i.get('prompt_count', 0) > 0),
        'total_prompt_blocks': sum(i.get('prompt_count', 0) for i in kavel_items),
        'total_demo_videos': sum(len(i.get('demo_videos') or []) for i in kavel_items),
        'note': (
            'Prompts extracted verbatim from public Next.js RSC payloads '
            '(form hub prompt + showcase templatePrompt) when present; '
            'detail URLs are /video/<slug>. Deduped by canonical slug.'
        ),
        'sync': {
            'added': kavel_sync.get('added', []),
            'updated': kavel_sync.get('updated', []),
            'failed': kavel_sync.get('failed', []),
        },
    }
    if mediaio_items:
        prev_mio = sources.get('mediaio') or {}
        sources['mediaio'] = {
            **prev_mio,
            'listing': prev_mio.get(
                'listing',
                'https://www.media.io/ai/explore/zone/ai-video-trend-generator',
            ),
            'count': len(mediaio_items),
            'with_prompts': sum(1 for i in mediaio_items if i.get('prompt_count', 0) > 0),
            'total_prompt_blocks': sum(i.get('prompt_count', 0) for i in mediaio_items),
            'total_demo_videos': sum(len(i.get('demo_videos') or []) for i in mediaio_items),
        }

    inv = {
        'generated_at': SCRAPE_DATE,
        'generated_at_iso': SCRAPE_ISO,
        'sorted_by': inv.get('sorted_by')
        or 'published || updated (newest first); undated=unknown; never scraped_at',
        'sources': sources,
        'templates': all_items,
    }
    inv_path.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + '\n')
    return inv


def scrape_one(listing: dict, week_ranks: dict[str, int]) -> tuple[str, dict | None, str]:
    slug = listing['slug']
    url = f'https://www.kavel.ai{listing["href"]}'
    dest = RAW / 'kavel-html' / f'{slug}.html'
    ok, effective = curl_follow(url, dest, timeout=90)
    if not ok:
        return ('fail', None, slug)
    canon = slug_from_video_url(effective) or slug
    if canon != slug:
        # Rename raw file to canonical
        canon_dest = RAW / 'kavel-html' / f'{canon}.html'
        if dest.exists():
            if canon_dest.exists():
                dest.unlink()
            else:
                dest.replace(canon_dest)
        dest = canon_dest
        listing = dict(listing)
        listing['slug'] = canon
        listing['href'] = f'/video/{canon}'
    html = dest.read_text(errors='ignore')
    detail = parse_detail(html, listing['slug'], listing)
    prompts = detail['prompts']
    item = {
        'source': 'kavel',
        'source_site': 'https://www.kavel.ai',
        'slug': listing['slug'],
        'name': listing['title'],
        'url': f'https://www.kavel.ai/video/{listing["slug"]}',
        'listing_url': LISTING_URL,
        'blurb': listing.get('desc') or '',
        'published': None,
        'updated': None,
        'scraped_at': SCRAPE_DATE,
        'listing_index': listing.get('listing_index'),
        'this_week_rank': week_ranks.get(listing['slug']),
        'demo_videos': detail['demo_videos'],
        'posters': detail['posters'],
        'prompts': prompts,
        'prompt_count': len(prompts),
        'prompts_public': len(prompts) > 0,
        'note': None
        if prompts
        else 'No public prompt text found on Kavel page payload; demos/posters only — prompts not invented.',
        'showcase_count': len(detail['showcases']),
    }
    write_template(item)
    # Download up to 2 demos + 2 posters
    for u in (item['demo_videos'] or [])[:2]:
        download_to(u, OUT / item['slug'] / 'demos' / filename_from_url(u))
    for u in (item['posters'] or [])[:2]:
        # Prefer full poster over thumb-240 when both listed
        download_to(u, OUT / item['slug'] / 'posters' / filename_from_url(u))
    kind = 'renamed' if canon != slug else 'ok'
    return (kind, item, slug if canon == slug else f'{slug}->{canon}')


def main():
    RAW.mkdir(exist_ok=True)
    BLOB.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    (RAW / 'kavel-html').mkdir(exist_ok=True)

    listing_path = RAW / 'kavel-ai-video-trends.html'
    print('== fetch listing ==', flush=True)
    ok, _ = curl_follow(LISTING_URL, listing_path, timeout=60)
    if not ok:
        print('FAIL listing', flush=True)
        sys.exit(1)
    html = listing_path.read_text(errors='ignore')
    all_trends, week = parse_listing(html)
    week_ranks = {w['slug']: w['rank'] for w in week if w.get('rank')}
    for i, t in enumerate(all_trends):
        t['listing_index'] = i  # 0 = newest
    (RAW / 'kavel-listing.json').write_text(
        json.dumps(
            {
                'scraped_at': SCRAPE_ISO,
                'listing': LISTING_URL,
                'count': len(all_trends),
                'this_week': week,
                'trends': all_trends,
            },
            ensure_ascii=False,
            indent=2,
        )
        + '\n'
    )
    (RAW / 'kavel-slugs.txt').write_text('\n'.join(t['slug'] for t in all_trends) + '\n')
    print(f'listing trends={len(all_trends)} this_week={len(week)}', flush=True)

    prev_slugs = set()
    inv_path = ROOT / 'inventory.json'
    if inv_path.exists():
        prev = json.loads(inv_path.read_text())
        prev_slugs = {t['slug'] for t in prev.get('templates', []) if t.get('source') == 'kavel'}

    print('== fetch detail pages ==', flush=True)
    results: list[dict] = []
    failed: list[str] = []
    renamed: list[str] = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(scrape_one, t, week_ranks) for t in all_trends]
        for f in as_completed(futs):
            kind, item, info = f.result()
            if kind == 'fail' or item is None:
                failed.append(info)
                print(f'FAIL {info}', flush=True)
                continue
            if kind == 'renamed':
                renamed.append(info)
            results.append(item)
            print(
                f"OK {item['slug']} prompts={item['prompt_count']} "
                f"demos={len(item['demo_videos'])} posters={len(item['posters'])}",
                flush=True,
            )

    # Preserve listing (newest-first) order
    by_slug = {r['slug']: r for r in results}
    ordered = [by_slug[t['slug']] for t in all_trends if t['slug'] in by_slug]
    # Any redirected canonical not in original list
    for r in results:
        if r['slug'] not in by_slug:
            continue
        if r not in ordered:
            ordered.append(r)
    # Deduplicate by slug (canonical)
    seen: set[str] = set()
    final: list[dict] = []
    for r in ordered:
        if r['slug'] in seen:
            continue
        seen.add(r['slug'])
        final.append(r)

    added = sorted(i['slug'] for i in final if i['slug'] not in prev_slugs)
    updated = sorted(i['slug'] for i in final if i['slug'] in prev_slugs)
    sync = {
        'added': added,
        'updated': updated,
        'failed': sorted(failed),
        'renamed': sorted(renamed),
    }
    summary = {
        'scraped_at': SCRAPE_ISO,
        'listing': LISTING_URL,
        'count': len(final),
        'with_prompts': sum(1 for i in final if i['prompt_count'] > 0),
        'total_prompt_blocks': sum(i['prompt_count'] for i in final),
        'total_demo_videos': sum(len(i.get('demo_videos') or []) for i in final),
        'this_week': [{'rank': w['rank'], 'slug': w['slug'], 'title': w['title']} for w in week],
        **sync,
        'templates': [
            {
                'slug': i['slug'],
                'name': i['name'],
                'prompt_count': i['prompt_count'],
                'url': i['url'],
            }
            for i in final
        ],
    }
    (RAW / 'kavel-sync-summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n'
    )
    (RAW / 'kavel-items.json').write_text(
        json.dumps(final, ensure_ascii=False, indent=2) + '\n'
    )

    print('== merge inventory ==', flush=True)
    inv = merge_into_inventory(final, sync)
    print(
        json.dumps(
            {
                'kavel_count': len(final),
                'with_prompts': summary['with_prompts'],
                'total_prompt_blocks': summary['total_prompt_blocks'],
                'added_n': len(added),
                'failed_n': len(failed),
                'inventory_total': len(inv['templates']),
                'sources': {
                    k: v.get('count') for k, v in inv.get('sources', {}).items()
                },
            },
            indent=2,
        ),
        flush=True,
    )
    return final, summary


if __name__ == '__main__':
    main()
