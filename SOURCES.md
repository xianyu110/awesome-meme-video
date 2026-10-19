# Sources

## MakeViral
- Listing: https://www.makeviral.ai/templates
- Per-template markdown: `https://www.makeviral.ai/templates/<slug>.md`
- Demo media: `https://www.makeviral.ai/media/templates/<slug>/...`

## Remake Your Meme
- Listing: https://remakeyourmeme.com/templates/
- CDN: https://cdn.remakeyourmeme.com/
- `llms.txt`: https://remakeyourmeme.com/llms.txt
- Public template pages do **not** expose copyable prompt text.

## Media.io
- Listing: https://www.media.io/ai/explore/zone/ai-video-trend-generator
- ZH: https://www.media.io/ai/zh/explore/zone/ai-video-trend-generator
- Prompts extracted verbatim from public `aigc_config` when present.

## Kavel
- Listing: https://www.kavel.ai/ai-video-trends
- Detail: `https://www.kavel.ai/video/<slug>`
- CDN: https://cdn.kavel.ai/ (videos + posters under `/videos/kavel-showcase/`, `/posters/kavel-showcase/`)
- Scrape: Next.js RSC flight HTML (no public list API). Prompts from form hub `prompt` + showcase `templatePrompt` when present.
- Within-source dedupe by canonical `/video/<slug>` (follow redirects).

## Sort rule
Inventory, README tables, PROMPTS.md, and the Pages gallery are sorted **newest first** by:
`updated` (MakeViral) → else `published` → else `scraped_at` (Asia/Shanghai scrape date).
Remake / Media.io / Kavel pages often have no public publish date, so they fall back to `scraped_at`.
Kavel README section preserves listing order (newest first from the site).

Synced 2026-10-19T12:29:22+08:00 (Asia/Shanghai) for the awesome-meme-video inventory.
