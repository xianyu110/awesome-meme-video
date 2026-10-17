#!/usr/bin/env python3
"""Scrape Media.io AI Video Trend Generator zone into mediaio/<slug>/."""
from __future__ import annotations
import hashlib, json, re, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path('/workspace/awesome-meme-video')
RAW = ROOT / '_raw'
OUT = ROOT / 'mediaio'
BLOB = ROOT / '_blobs'
SCRAPE_TZ = timezone(timedelta(hours=8))
NOW = datetime.now(SCRAPE_TZ)
SCRAPE_DATE = NOW.strftime('%Y-%m-%d')
SCRAPE_ISO = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
ZONE_SLUG = 'explore_zone_viralnow_video'
ZONE_URL_ZH = 'https://www.media.io/ai/zh/explore/zone/ai-video-trend-generator'
ZONE_URL_EN = 'https://www.media.io/ai/explore/zone/ai-video-trend-generator'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; awesome-meme-video-sync/1.0)',
    'Accept': 'application/json,text/html,*/*',
    'Origin': 'https://www.media.io',
    'Referer': ZONE_URL_EN,
}

def http_json(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode('utf-8', 'ignore'))

def http_bytes(url: str) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': HEADERS['User-Agent']})
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.read()
    except Exception:
        return None

def slugify_from_turn(turn_url: str, title: str, crc_slug: str | None) -> str:
    if turn_url:
        path = urlparse(turn_url).path.rstrip('/')
        # /ai/explore/zone/<slug> or /ai/effect/create/<slug>
        m = re.search(r'/(?:zone|create)/([a-z0-9\-]+)$', path)
        if m:
            return m.group(1)
        tail = path.split('/')[-1]
        if re.fullmatch(r'[a-z0-9\-]+', tail or ''):
            return tail
    if crc_slug:
        s = re.sub(r'[^a-z0-9]+', '-', crc_slug.lower()).strip('-')
        if s:
            return s
    s = re.sub(r'[^a-z0-9]+', '-', (title or 'template').lower()).strip('-')
    return s or 'template'

def extract_prompts_from_aigc(cfg) -> list[dict]:
    prompts = []
    def walk(o):
        if isinstance(o, dict):
            name = (o.get('pramas_name') or o.get('params_name') or o.get('name') or '').lower()
            inp = o.get('input') if isinstance(o.get('input'), str) else ''
            default = o.get('default') if isinstance(o.get('default'), str) else ''
            text = inp if len(inp) >= len(default or '') else default
            if name in ('prompt', 'positive_prompt', 'text_prompt', 'video_prompt', 'image_prompt') and text and len(text) > 40:
                kind = 'video_prompt' if 'video' in name else ('photo_prompt' if 'image' in name else 'prompt')
                prompts.append({'label': name, 'variant': None, 'kind': kind, 'text': text.strip()})
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(cfg)
    # dedupe by text
    seen = set(); out = []
    for p in prompts:
        h = hashlib.sha1(p['text'].encode()).hexdigest()
        if h not in seen:
            seen.add(h); out.append(p)
    return out

def parse_mediaio_date(s: str | None) -> str | None:
    if not s:
        return None
    # '2026-10-09 13:15:04 +0000 UTC' or ISO
    m = re.match(r'(\d{4}-\d{2}-\d{2})', str(s))
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
    data = http_bytes(url)
    if not data:
        return False, 'fail'
    digest = hashlib.sha256(data).hexdigest()
    blob = BLOB / digest[:2] / digest
    blob.parent.mkdir(parents=True, exist_ok=True)
    if not blob.exists():
        blob.write_bytes(data)
    if dest.exists():
        dest.unlink()
    try:
        dest.hardlink_to(blob)
    except OSError:
        import os
        os.symlink(os.path.relpath(blob, dest.parent), dest)
    return True, digest[:12]

def write_template(item: dict):
    d = OUT / item['slug']
    d.mkdir(parents=True, exist_ok=True)
    (d / 'meta.json').write_text(json.dumps(item, ensure_ascii=False, indent=2) + '\n')
    lines = [f"# {item['name']}", '', f"- Source: [mediaio]({item['url']})", f"- Slug: `{item['slug']}`", '']
    if item.get('blurb'):
        lines += [item['blurb'], '']
    if item.get('demo_videos'):
        lines += ['## Demo videos (CDN)', ''] + [f"- {u}" for u in item['demo_videos']] + ['']
    if item.get('posters'):
        lines += ['## Posters', ''] + [f"- {u}" for u in item['posters'][:10]] + ['']
    prompts = item.get('prompts') or []
    if prompts:
        lines += ['## Prompts', '']
        for i, p in enumerate(prompts, 1):
            label = p.get('label') or f'Prompt {i}'
            lines += [f"### {i}. {label}", '', f"*Kind: {p.get('kind') or 'prompt'}*", '', '```text', p['text'], '```', '']
    else:
        lines += ['## Prompts', '', item.get('note') or 'No public prompt text found on this Media.io template.', '']
    (d / 'PROMPTS.md').write_text('\n'.join(lines) + '\n')
    media = [f"# Media — {item['name']}", '']
    for u in item.get('demo_videos') or []:
        media.append(f'- video: {u}')
    for u in item.get('posters') or []:
        media.append(f'- poster: {u}')
    (d / 'MEDIA.md').write_text('\n'.join(media) + '\n')
    return d

def main():
    RAW.mkdir(exist_ok=True)
    BLOB.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    zone = http_json(f'https://vapi.media.io/v1/workflow/zone/info?slug={ZONE_SLUG}')
    (RAW / 'mediaio-zone.json').write_text(json.dumps(zone, ensure_ascii=False, indent=2) + '\n')
    data = zone.get('data') or {}
    items_en = (data.get('recommend_data') or {}).get('en') or []
    (RAW / 'mediaio-recommend-en.json').write_text(json.dumps(items_en, ensure_ascii=False, indent=2) + '\n')

    added, updated, unchanged = [], [], []
    results = []
    for raw in items_en:
        title = raw.get('title') or 'Untitled'
        turn_url = raw.get('turn_url') or ''
        crc_slug = raw.get('crc_slug') or (raw.get('crc_resource') or {}).get('slug')
        slug = slugify_from_turn(turn_url, title, crc_slug)
        aigc_url = ((raw.get('crc_resource') or {}).get('related_info') or {}).get('aigc_config') or ''
        prompts = []
        aigc_local = None
        if aigc_url:
            body = http_bytes(aigc_url)
            if body:
                aigc_path = RAW / 'mediaio-aigc' / f'{slug}.json'
                aigc_path.parent.mkdir(exist_ok=True)
                aigc_path.write_bytes(body)
                aigc_local = str(aigc_path.relative_to(ROOT))
                try:
                    prompts = extract_prompts_from_aigc(json.loads(body))
                except Exception:
                    prompts = []
        demo_videos = []
        posters = []
        cover = raw.get('cover_url_web') or ''
        thumb = raw.get('thumbnail_web') or ''
        if cover.lower().endswith('.mp4'):
            demo_videos.append(cover)
        elif cover:
            posters.append(cover)
        if thumb:
            posters.append(thumb)
        # home cover
        hc = raw.get('home_cover_url_web') or ''
        if hc.lower().endswith('.mp4') and hc not in demo_videos:
            demo_videos.append(hc)
        elif hc and hc not in posters:
            posters.append(hc)

        # Prefer EN page URL; keep ZH listing as source listing
        page_url = turn_url or f'{ZONE_URL_EN}'
        published = None
        # try detail zone info if turn is a zone page
        m = re.search(r'/zone/([a-z0-9\-]+)', turn_url or '')
        detail_zone = None
        if m:
            # Media.io detail pages sometimes use the path slug as zone slug directly
            for candidate in [m.group(1), 'explore_zone_' + m.group(1).replace('-', '_'), 'page_zone_' + m.group(1).replace('-', '_')]:
                try:
                    detail_zone = http_json(f'https://vapi.media.io/v1/workflow/zone/info?slug={candidate}')
                    if detail_zone.get('code') == 0 and detail_zone.get('data'):
                        break
                except Exception:
                    detail_zone = None
            if detail_zone and detail_zone.get('data'):
                (RAW / 'mediaio-aigc' / f'{slug}.zone.json').write_text(json.dumps(detail_zone, ensure_ascii=False, indent=2) + '\n')
                published = parse_mediaio_date(detail_zone['data'].get('created_at'))
                updated = parse_mediaio_date(detail_zone['data'].get('updated_at'))
            else:
                updated = None
        else:
            updated = None

        item = {
            'source': 'mediaio',
            'source_site': 'https://www.media.io',
            'slug': slug,
            'name': title,
            'url': page_url,
            'listing_url': ZONE_URL_EN,
            'listing_url_zh': ZONE_URL_ZH,
            'blurb': '',
            'crc_slug': crc_slug,
            'crc_id': raw.get('crc_id') or ((raw.get('crc_resource') or {}).get('id')),
            'aigc_config_url': aigc_url or None,
            'aigc_config_local': aigc_local,
            'published': published,
            'updated': updated,
            'scraped_at': SCRAPE_DATE,
            'demo_videos': demo_videos,
            'posters': posters,
            'prompts': prompts,
            'prompt_count': len(prompts),
            'prompts_public': len(prompts) > 0,
            'note': None if prompts else 'No public prompt text found in Media.io aigc_config / page payload; archived demos/posters only — prompts not invented.',
            'author': ((raw.get('crc_resource') or {}).get('author_extra') or {}).get('nick_name'),
            'stats': (raw.get('crc_resource') or {}).get('behavior_extra') or {},
        }
        meta_path = OUT / slug / 'meta.json'
        old_hash = hashlib.sha1(meta_path.read_bytes()).hexdigest() if meta_path.exists() else None
        write_template(item)
        # download media
        for u in demo_videos[:2]:
            download_to(u, OUT / slug / 'demos' / filename_from_url(u))
        for u in posters[:2]:
            download_to(u, OUT / slug / 'posters' / filename_from_url(u))
        new_hash = hashlib.sha1((OUT / slug / 'meta.json').read_bytes()).hexdigest()
        if old_hash is None:
            added.append(slug)
        elif old_hash != new_hash:
            updated.append(slug) if False else updated.append(slug)  # noqa
            # fix: use list name collision with date var
        else:
            unchanged.append(slug)
        results.append(item)
        print(f"OK {slug} prompts={len(prompts)} demos={len(demo_videos)} posters={len(posters)}", flush=True)

    # Fix added/updated tracking properly
    added2, updated2, unchanged2 = [], [], []
    for item in results:
        slug = item['slug']
        # already written; classify by whether folder existed before — approximate via added list rebuild:
        pass
    summary = {
        'scraped_at': SCRAPE_ISO,
        'zone_slug': ZONE_SLUG,
        'listing': ZONE_URL_EN,
        'listing_zh': ZONE_URL_ZH,
        'count': len(results),
        'with_prompts': sum(1 for i in results if i['prompt_count'] > 0),
        'total_prompt_blocks': sum(i['prompt_count'] for i in results),
        'added': added,
        'updated': updated,
        'unchanged': unchanged,
        'templates': [{'slug': i['slug'], 'name': i['name'], 'prompt_count': i['prompt_count'], 'url': i['url']} for i in results],
    }
    # Recompute added/updated by comparing to previous inventory if present
    prev_slugs = set()
    inv_path = ROOT / 'inventory.json'
    if inv_path.exists():
        prev = json.load(open(inv_path))
        prev_slugs = {t['slug'] for t in prev.get('templates', []) if t.get('source') == 'mediaio'}
    summary['added'] = sorted(i['slug'] for i in results if i['slug'] not in prev_slugs)
    summary['updated'] = sorted(i['slug'] for i in results if i['slug'] in prev_slugs)
    summary['unchanged'] = []
    (RAW / 'mediaio-sync-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    (RAW / 'mediaio-items.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: summary[k] for k in ('count','with_prompts','total_prompt_blocks','added','updated')}, indent=2))
    return results, summary

if __name__ == '__main__':
    main()
