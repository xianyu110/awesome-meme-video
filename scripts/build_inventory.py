#!/usr/bin/env python3
"""Parse MakeViral .md + Remake HTML into inventory + per-template folders."""
from __future__ import annotations
import hashlib, json, re, html as HTML
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path('/workspace/awesome-meme-video')
RAW = ROOT / '_raw'
OUT_MV = ROOT / 'makeviral'
OUT_RM = ROOT / 'remakeyourmeme'

def sha1_text(s: str) -> str:
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:12]

def clean_url(u: str) -> str:
    u = u.rstrip('\\').split('#')[0].rstrip('\\')
    return u

def extract_fenced_prompts(md: str) -> list[dict]:
    """Extract ```text / ``` blocks that look like prompts, with nearby labels."""
    prompts = []
    # Find code fences
    for m in re.finditer(r'(?:^|\n)([^\n`]{0,200})\n\s*```(?:text|prompt|markdown)?\n(.*?)```', md, re.S):
        label = m.group(1).strip().strip(':').strip('*').strip()
        body = m.group(2).strip()
        if len(body) < 80:
            continue
        # skip tiny non-prompt fences
        kind = 'prompt'
        low = (label + ' ' + body[:200]).lower()
        if 'photo prompt' in low or 'image prompt' in low:
            kind = 'photo_prompt'
        elif 'video prompt' in low:
            kind = 'video_prompt'
        # Human / Pet variant from surrounding context
        variant = None
        ctx = md[max(0, m.start()-400):m.start()].lower()
        if re.search(r'\bhuman\b', ctx[-120:]) or 'human variant' in ctx or '### human' in ctx:
            variant = 'Human'
        if re.search(r'\bpet\b', ctx[-120:]) or 'pet variant' in ctx or '### pet' in ctx:
            variant = 'Pet'
        # Also check label
        if re.search(r'\bhuman\b', label, re.I):
            variant = 'Human'
        if re.search(r'\bpet\b', label, re.I):
            variant = 'Pet'
        prompts.append({
            'label': label[:200] if label else None,
            'variant': variant,
            'kind': kind,
            'text': body,
        })
    return prompts

def parse_makeviral_md(path: Path) -> dict:
    md = path.read_text(errors='ignore')
    slug = path.stem
    title_m = re.match(r'^#\s+(.+)$', md, re.M)
    title = title_m.group(1).strip() if title_m else slug
    blurb_m = re.search(r'^>\s+(.+)$', md, re.M)
    blurb = blurb_m.group(1).strip() if blurb_m else ''
    updated = re.search(r'^Updated:\s*(.+)$', md, re.M)
    published = re.search(r'^Published:\s*(.+)$', md, re.M)
    credits_m = re.search(r'(\d+)\s+credits', md, re.I)
    # media
    videos = sorted(set(clean_url(u) for u in re.findall(r'https://www\.makeviral\.ai/media/templates/[^\s\)\"]+\.mp4', md)))
    posters = sorted(set(clean_url(u) for u in re.findall(r'https://www\.makeviral\.ai/media/templates/[^\s\)\"]+\.(?:jpg|jpeg|png|webp)', md)))
    # also example-input etc already in posters
    prompts = extract_fenced_prompts(md)
    # section headings that look like variants
    variants = []
    for h in re.findall(r'^###?\s+(.+)$', md, re.M):
        if re.search(r'\b(Human|Pet|Duo|Solo|Photo|Video|Variant)\b', h, re.I):
            variants.append(h.strip())
    return {
        'source': 'makeviral',
        'source_site': 'https://www.makeviral.ai',
        'slug': slug,
        'name': title,
        'url': f'https://www.makeviral.ai/templates/{slug}',
        'markdown_url': f'https://www.makeviral.ai/templates/{slug}.md',
        'blurb': blurb,
        'updated': updated.group(1).strip() if updated else None,
        'published': published.group(1).strip() if published else None,
        'credits': int(credits_m.group(1)) if credits_m else None,
        'demo_videos': videos,
        'posters': posters,
        'prompts': prompts,
        'variant_headings': variants[:30],
        'prompt_count': len(prompts),
    }

def visible_text(html: str) -> str:
    t = re.sub(r'<script[^>]*>.*?</script>', '\n', html, flags=re.S|re.I)
    t = re.sub(r'<style[^>]*>.*?</style>', '\n', t, flags=re.S|re.I)
    t = re.sub(r'<[^>]+>', '\n', t)
    t = HTML.unescape(t)
    lines = [re.sub(r'\s+', ' ', l).strip() for l in t.splitlines()]
    return '\n'.join(l for l in lines if l)

def parse_remake_html(path: Path) -> dict:
    html = path.read_text(errors='ignore')
    slug = path.stem
    text = visible_text(html)
    title_m = re.search(r'<title>(.*?)</title>', html, re.I|re.S)
    title = HTML.unescape(re.sub(r'\s+', ' ', title_m.group(1))).strip() if title_m else slug
    title = title.split('|')[0].split(':')[0].strip()
    # h1
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I|re.S)
    if h1:
        h1t = re.sub(r'<[^>]+>', '', h1.group(1))
        h1t = HTML.unescape(re.sub(r'\s+', ' ', h1t)).strip()
        if h1t:
            title = h1t
    # media - prefer template-specific paths
    all_mp4 = sorted(set(clean_url(u) for u in re.findall(r'https://cdn\.remakeyourmeme\.com[^"\'\\\s#?]+\.mp4', html)))
    all_img = sorted(set(clean_url(u) for u in re.findall(r'https://cdn\.remakeyourmeme\.com[^"\'\\\s#?]+\.(?:jpg|jpeg|png|webp)', html)))
    # heuristic: template own folder
    # map slug fragments
    own_videos = [u for u in all_mp4 if '/templates/' in u and 'preview' not in u]
    own_previews = [u for u in all_mp4 if 'preview' in u]
    demo_videos = own_videos or all_mp4
    posters = [u for u in all_img if '/templates/' in u and ('poster' in u or u.endswith('.jpg'))]
    if not posters:
        posters = [u for u in all_img if 'poster' in u][:5]
    # photos / duration from text
    photos = None
    m = re.search(r'(\d+)\s*photos?\s*in', text, re.I)
    if m:
        photos = int(m.group(1))
    m2 = re.search(r'(\d+)\s*s\s*video', text, re.I)
    duration = int(m2.group(1)) if m2 else None
    # status
    ready = 'Ready to make' in text or 'Make yours' in text
    in_testing = 'in testing' in text.lower() or ('Raindance' in title and 'Make yours Photo' not in text[:500])
    # blurb: first substantial paragraph-ish line after title
    blurb = ''
    for line in text.splitlines():
        if len(line) > 60 and 'cookie' not in line.lower() and 'Skip to' not in line:
            if title.lower()[:20] not in line.lower() or len(line) > len(title)+20:
                blurb = line[:300]
                break
    # Remake does not publish full prompts on public pages
    prompts = []
    if re.search(r'```', html) or re.search(r'\bprompt\b', html, re.I):
        # attempt extract any long text blocks labeled prompt - usually none
        for m in re.finditer(r'(?:Prompt|prompt)[:\s]+(.{80,2000}?)(?:\n\n|<)', text, re.S):
            prompts.append({'label': 'extracted', 'variant': None, 'kind': 'prompt', 'text': m.group(1).strip()})
    return {
        'source': 'remakeyourmeme',
        'source_site': 'https://remakeyourmeme.com',
        'slug': slug,
        'name': title,
        'url': f'https://remakeyourmeme.com/templates/{slug}/',
        'blurb': blurb,
        'photos_in': photos,
        'duration_s': duration,
        'ready_to_make': ready,
        'demo_videos': demo_videos[:15],
        'preview_videos': own_previews[:10],
        'posters': posters[:15],
        'all_cdn_mp4': all_mp4[:40],
        'prompts': prompts,
        'prompt_count': len(prompts),
        'prompts_public': False,
        'note': 'Remake Your Meme does not publish copyable prompt text on public template pages (one-tap remake). Inventory keeps demos, posters, and metadata only.',
    }

def write_template_folder(item: dict, out_root: Path):
    d = out_root / item['slug']
    d.mkdir(parents=True, exist_ok=True)
    # meta.json without huge prompt duplication? keep prompts
    meta = {k: v for k, v in item.items()}
    (d / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    # PROMPTS.md
    lines = [f"# {item['name']}", '', f"- Source: [{item['source']}]({item['url']})", f"- Slug: `{item['slug']}`", '']
    if item.get('blurb'):
        lines += [item['blurb'], '']
    if item.get('demo_videos'):
        lines += ['## Demo videos (CDN)', '']
        for u in item['demo_videos']:
            lines.append(f'- {u}')
        lines.append('')
    if item.get('posters'):
        lines += ['## Posters', '']
        for u in item['posters'][:10]:
            lines.append(f'- {u}')
        lines.append('')
    prompts = item.get('prompts') or []
    if prompts:
        lines += ['## Prompts', '']
        for i, p in enumerate(prompts, 1):
            label = p.get('label') or f'Prompt {i}'
            variant = f" ({p['variant']})" if p.get('variant') else ''
            kind = p.get('kind') or 'prompt'
            lines += [f'### {i}. {label}{variant}', '', f'*Kind: {kind}*', '', '```text', p['text'], '```', '']
    else:
        if item.get('source') == 'remakeyourmeme':
            lines += ['## Prompts', '', item.get('note', 'No public prompts on this page.'), '']
        else:
            lines += ['## Prompts', '', '_No fenced prompt blocks found in the public markdown._', '']
    (d / 'PROMPTS.md').write_text('\n'.join(lines) + '\n')
    # MEDIA.md with links
    media_lines = [f"# Media — {item['name']}", '']
    for u in item.get('demo_videos') or []:
        media_lines.append(f'- video: {u}')
    for u in item.get('posters') or []:
        media_lines.append(f'- poster: {u}')
    (d / 'MEDIA.md').write_text('\n'.join(media_lines) + '\n')
    return d

def main():
    mv_items = []
    for p in sorted((RAW / 'makeviral-md').glob('*.md')):
        item = parse_makeviral_md(p)
        write_template_folder(item, OUT_MV)
        # also keep raw md copy
        dest = OUT_MV / item['slug'] / 'source.md'
        dest.write_text(p.read_text(errors='ignore'))
        mv_items.append(item)

    rm_items = []
    for p in sorted((RAW / 'remake-html').glob('*.html')):
        item = parse_remake_html(p)
        write_template_folder(item, OUT_RM)
        rm_items.append(item)

    inventory = {
        'generated_at': '2026-10-17',
        'sources': {
            'makeviral': {
                'listing': 'https://www.makeviral.ai/templates',
                'count': len(mv_items),
                'with_prompts': sum(1 for i in mv_items if i['prompt_count'] > 0),
                'total_prompt_blocks': sum(i['prompt_count'] for i in mv_items),
                'total_demo_videos': sum(len(i['demo_videos']) for i in mv_items),
            },
            'remakeyourmeme': {
                'listing': 'https://remakeyourmeme.com/templates/',
                'count': len(rm_items),
                'with_prompts': sum(1 for i in rm_items if i['prompt_count'] > 0),
                'note': 'Public pages do not expose copyable prompts',
                'total_demo_videos': sum(len(i.get('demo_videos') or []) for i in rm_items),
            },
        },
        'templates': mv_items + rm_items,
    }
    (ROOT / 'inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')

    # Collect unique media URLs for download
    all_videos = []
    all_posters = []
    for i in mv_items + rm_items:
        for u in i.get('demo_videos') or []:
            all_videos.append((i['source'], i['slug'], u))
        for u in (i.get('posters') or [])[:3]:  # cap posters per template
            all_posters.append((i['source'], i['slug'], u))
    # dedup by URL
    seen = set()
    videos_dedup = []
    for src, slug, u in all_videos:
        if u not in seen:
            seen.add(u)
            videos_dedup.append((src, slug, u))
    seen = set()
    posters_dedup = []
    for src, slug, u in all_posters:
        if u not in seen:
            seen.add(u)
            posters_dedup.append((src, slug, u))

    (RAW / 'download-videos.tsv').write_text('\n'.join(f'{s}\t{sl}\t{u}' for s,sl,u in videos_dedup) + '\n')
    (RAW / 'download-posters.tsv').write_text('\n'.join(f'{s}\t{sl}\t{u}' for s,sl,u in posters_dedup) + '\n')

    print(json.dumps({
        'makeviral': inventory['sources']['makeviral'],
        'remake': inventory['sources']['remakeyourmeme'],
        'unique_videos': len(videos_dedup),
        'unique_posters_capped': len(posters_dedup),
        'mv_prompt_stats': {
            'min': min((i['prompt_count'] for i in mv_items), default=0),
            'max': max((i['prompt_count'] for i in mv_items), default=0),
            'zero_prompt_slugs': [i['slug'] for i in mv_items if i['prompt_count']==0][:20],
        }
    }, indent=2))

if __name__ == '__main__':
    main()
