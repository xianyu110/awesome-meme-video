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
- Listing (EN): https://www.media.io/ai/explore/zone/ai-video-trend-generator
- Listing (ZH): https://www.media.io/ai/zh/explore/zone/ai-video-trend-generator
- Zone API: `https://vapi.media.io/v1/workflow/zone/info?slug=explore_zone_viralnow_video`
- Prompts: extracted verbatim from public `aigc_config` JSON when the `prompt` param is present.

## Sort rule
Inventory, README tables, PROMPTS.md, and the Pages gallery are sorted **newest first** by:
`updated` → else `published` → else `scraped_at` (Asia/Shanghai scrape date).
Remake / some Media.io entries may lack a public publish date and fall back to `scraped_at`.

Synced 2026-10-17T22:46:34+08:00 (Asia/Shanghai) for the awesome-meme-video inventory.
