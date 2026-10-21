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
- CDN: https://cdn.kavel.ai/
- Scrape: Next.js RSC flight HTML; prompts from hub `prompt` + showcase `templatePrompt` when present.

## Sort rule
Inventory, README tables, PROMPTS.md, and the Pages gallery are sorted **newest first** by:
`published` → else `updated`. **Never** use `scraped_at` as the listing date.
If a source has no public publish/update date, display **unknown** (sort to the end).

Synced 2026-10-21T13:44:20+08:00 (Asia/Shanghai) for the awesome-meme-video inventory.
