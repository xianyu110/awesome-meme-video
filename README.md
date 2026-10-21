# Awesome Meme Video

> 公开 AI 迷因 / 病毒视频模板与提示词清单（MakeViral · Remake Your Meme · Media.io · Kavel）。
>
> Public inventory of AI meme / viral video templates and prompts.

## Stats

- **Total**: 293 templates
- **MakeViral**: 169 templates · 429 prompt blocks · 270 demo videos
- **Remake Your Meme**: 20 templates · public prompts: **none** (one-tap remake only) · demos/posters archived
- **Media.io**: 18 templates · 12 prompt blocks · 12 demo videos
- **Kavel**: 86 templates · 270 prompt blocks · 310 demo videos
- Scraped: 2026-10-21 (Asia/Shanghai)
- Sort: **newest first** by `published || updated (newest first); undated=unknown; never scraped_at`
- Gallery: https://xianyu110.github.io/awesome-meme-video/ (repo is private — Pages may be unavailable)

## Sources

| Site | Listing | Notes |
| --- | --- | --- |
| [MakeViral](https://www.makeviral.ai/templates) | `/templates` + per-page `.md` | Full prompts published; demos under `/media/templates/...` |
| [Remake Your Meme](https://remakeyourmeme.com/templates/) | `/templates/` | No copyable prompts on public pages; CDN demos kept |
| [Media.io](https://www.media.io/ai/explore/zone/ai-video-trend-generator) | AI Video Trend Generator zone | Prompts from public `aigc_config` when present |
| [Kavel](https://www.kavel.ai/ai-video-trends) | `/ai-video-trends` · `/video/<slug>` | Prompts from public RSC payloads when present |

## Layout

```
awesome-meme-video/
  index.html          # GitHub Pages gallery (newest first)
  README.md
  PROMPTS.md          # all MakeViral prompts concatenated
  inventory.json      # machine-readable index
  makeviral/<slug>/
  remakeyourmeme/<slug>/
  mediaio/<slug>/
  kavel/<slug>/
```

Demo MP4s are stored via Git LFS when present. Each template folder also lists original CDN URLs in `MEDIA.md` / `PROMPTS.md`.

## Contents

### MakeViral

| Template | Slug | Date | Prompts | Demo | Page |
| --- | --- | --- | ---: | --- | --- |
| [ATM Glitch AI Trend: The Money Explosion on CCTV, Starring You](makeviral/atm-glitch-ai-trend/PROMPTS.md) | `atm-glitch-ai-trend` | 2026-10-21 | 2 | ✅ | [link](https://www.makeviral.ai/templates/atm-glitch-ai-trend) |
| [Victoria Secret AI Runway Video: Your Angel Walk in Giant Wings](makeviral/victoria-secret-runway-ai-trend/PROMPTS.md) | `victoria-secret-runway-ai-trend` | 2026-10-20 | 4 | ✅ | [link](https://www.makeviral.ai/templates/victoria-secret-runway-ai-trend) |
| [Nunca Ando Sola AI: You and the Holy Shadows](makeviral/nunca-ando-sola-ai-trend/PROMPTS.md) | `nunca-ando-sola-ai-trend` | 2026-10-20 | 2 | ✅ | [link](https://www.makeviral.ai/templates/nunca-ando-sola-ai-trend) |
| [Money Flex AI Trend: You or Your Pet Flex a Pile of Cash](makeviral/money-flex-ai-trend/PROMPTS.md) | `money-flex-ai-trend` | 2026-10-20 | 2 | ✅ | [link](https://www.makeviral.ai/templates/money-flex-ai-trend) |
| [Hand Pinch Filter AI: Close Your Eyes and a Hand Pinches Your Cheek](makeviral/hand-pinch-filter-ai/PROMPTS.md) | `hand-pinch-filter-ai` | 2026-10-20 | 3 | ✅ | [link](https://www.makeviral.ai/templates/hand-pinch-filter-ai) |
| [Facebook Marketplace Husband Meme: How Ima Look in a Couple Years](makeviral/facebook-marketplace-husband-ai-trend/PROMPTS.md) | `facebook-marketplace-husband-ai-trend` | 2026-10-20 | 2 | ✅ | [link](https://www.makeviral.ai/templates/facebook-marketplace-husband-ai-trend) |
| [Champagne Car Window Trend: Pop the Bottle Out of a Moving SUV](makeviral/champagne-car-window-ai-trend/PROMPTS.md) | `champagne-car-window-ai-trend` | 2026-10-20 | 2 | ✅ | [link](https://www.makeviral.ai/templates/champagne-car-window-ai-trend) |
| [C-Walk AI: Do the C-Walk From One Photo](makeviral/c-walk-ai-dance/PROMPTS.md) | `c-walk-ai-dance` | 2026-10-20 | 2 | ✅ | [link](https://www.makeviral.ai/templates/c-walk-ai-dance) |
| [AI Running on Banana Trees: Leap Across Giant Banana Leaves](makeviral/banana-tree-run-ai-trend/PROMPTS.md) | `banana-tree-run-ai-trend` | 2026-10-20 | 3 | ✅ | [link](https://www.makeviral.ai/templates/banana-tree-run-ai-trend) |
| [Anime Face Trend: Your Own Anime Twin in the Star Eye Photo](makeviral/anime-eye-ai-trend/PROMPTS.md) | `anime-eye-ai-trend` | 2026-10-20 | 3 | ✅ | [link](https://www.makeviral.ai/templates/anime-eye-ai-trend) |
| [Ali G Driving Scene AI: Grip the Blue Wheel and Head-Bang to the Drop](makeviral/ali-g-driving-scene-ai/PROMPTS.md) | `ali-g-driving-scene-ai` | 2026-10-20 | 5 | ✅ | [link](https://www.makeviral.ai/templates/ali-g-driving-scene-ai) |
| [AI Fruit Story: You as a 3D Fruit Person in a Soap Opera](makeviral/ai-fruit-story/PROMPTS.md) | `ai-fruit-story` | 2026-10-20 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-fruit-story) |
| [AI Cartoon Couple Video: You Two as a 3D Comedy Skit](makeviral/ai-cartoon-couple-video/PROMPTS.md) | `ai-cartoon-couple-video` | 2026-10-20 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-cartoon-couple-video) |
| [ABCDEFG I Need Money AI Trend: Your Pet (or You) Sings the Money Line](makeviral/abcdefg-i-need-money-ai-trend/PROMPTS.md) | `abcdefg-i-need-money-ai-trend` | 2026-10-20 | 2 | ✅ | [link](https://www.makeviral.ai/templates/abcdefg-i-need-money-ai-trend) |
| [You Talking Bout Me AI Trend: Star in the "I Be Thinking About My Bills" Meme](makeviral/you-talking-bout-me-ai-trend/PROMPTS.md) | `you-talking-bout-me-ai-trend` | 2026-10-19 | 3 | ✅ | [link](https://www.makeviral.ai/templates/you-talking-bout-me-ai-trend) |
| [I'm Gonna TOESA AI: Your 퇴사할게여 Stage Debut or Office Exit](makeviral/toesa-quit-job-ai-trend/PROMPTS.md) | `toesa-quit-job-ai-trend` | 2026-10-19 | 5 | ✅ | [link](https://www.makeviral.ai/templates/toesa-quit-job-ai-trend) |
| [多摩川で恋してみたい AI Dance: Do the Riverbank Hand Hearts](makeviral/tamagawa-koi-ai-dance/PROMPTS.md) | `tamagawa-koi-ai-dance` | 2026-10-19 | 4 | ✅ | [link](https://www.makeviral.ai/templates/tamagawa-koi-ai-dance) |
| [Ryuk AI: Put the Grinning Death God in Your Photo](makeviral/ryuk-ai-trend/PROMPTS.md) | `ryuk-ai-trend` | 2026-10-19 | 3 | ✅ | [link](https://www.makeviral.ai/templates/ryuk-ai-trend) |
| [Plug Walk Filter: Take the Dollar, Then Do the Plug Walk](makeviral/plug-walk-ai-filter/PROMPTS.md) | `plug-walk-ai-filter` | 2026-10-19 | 3 | ✅ | [link](https://www.makeviral.ai/templates/plug-walk-ai-filter) |
| [Perdon Trend: The Perfect AI Photo of You, Then "Perdón"](makeviral/perdon-ai-photo-trend/PROMPTS.md) | `perdon-ai-photo-trend` | 2026-10-19 | 2 | ✅ | [link](https://www.makeviral.ai/templates/perdon-ai-photo-trend) |
| [On The Radar AI: Rap Side by Side in the Green Booth](makeviral/on-the-radar-ai-trend/PROMPTS.md) | `on-the-radar-ai-trend` | 2026-10-19 | 2 | ✅ | [link](https://www.makeviral.ai/templates/on-the-radar-ai-trend) |
| [Love Options Dance: Do the 연애의 조건 Hand Gestures With AI](makeviral/love-options-ai-dance/PROMPTS.md) | `love-options-ai-dance` | 2026-10-19 | 3 | ✅ | [link](https://www.makeviral.ai/templates/love-options-ai-dance) |
| [IVE Looks Can Kill Dance: Be the Action Hero From Your Photo](makeviral/ive-looks-can-kill-ai-dance/PROMPTS.md) | `ive-looks-can-kill-ai-dance` | 2026-10-19 | 5 | ✅ | [link](https://www.makeviral.ai/templates/ive-looks-can-kill-ai-dance) |
| [ILLIT You're Under Arrest Dance: Do the 체포하겠어 Challenge From a Photo](makeviral/illit-youre-under-arrest-ai-dance/PROMPTS.md) | `illit-youre-under-arrest-ai-dance` | 2026-10-19 | 5 | ✅ | [link](https://www.makeviral.ai/templates/illit-youre-under-arrest-ai-dance) |
| [Fridge POV AI Trend: Put You and a Friend in the Tiramisu Fridge Meme](makeviral/fridge-pov-ai-trend/PROMPTS.md) | `fridge-pov-ai-trend` | 2026-10-19 | 3 | ✅ | [link](https://www.makeviral.ai/templates/fridge-pov-ai-trend) |
| [Charme Dance AI: Dance in a Rio Street Party From One Photo](makeviral/charme-dance-ai-trend/PROMPTS.md) | `charme-dance-ai-trend` | 2026-10-19 | 4 | ✅ | [link](https://www.makeviral.ai/templates/charme-dance-ai-trend) |
| [Cat in the Hat Trend: Make the AI Doorbell Cam Halloween Prank](makeviral/cat-in-the-hat-ai-trend/PROMPTS.md) | `cat-in-the-hat-ai-trend` | 2026-10-19 | 6 | ✅ | [link](https://www.makeviral.ai/templates/cat-in-the-hat-ai-trend) |
| [Bama Bound Trend: Hold the I'M BAMA BOUND Banner With AI](makeviral/bama-bound-ai-trend/PROMPTS.md) | `bama-bound-ai-trend` | 2026-10-19 | 5 | ✅ | [link](https://www.makeviral.ai/templates/bama-bound-ai-trend) |
| [Twilight Baseball Scene AI: Play the Vampire Baseball Game in the Storm](makeviral/twilight-baseball-scene-ai/PROMPTS.md) | `twilight-baseball-scene-ai` | 2026-10-18 | 3 | ✅ | [link](https://www.makeviral.ai/templates/twilight-baseball-scene-ai) |
| [Elevator Outfit Change AI: The Doors Close, a New Outfit Steps Out](makeviral/elevator-outfit-change-ai-trend/PROMPTS.md) | `elevator-outfit-change-ai-trend` | 2026-10-18 | 2 | ✅ | [link](https://www.makeviral.ai/templates/elevator-outfit-change-ai-trend) |
| [Devil Wears Prada Trend AI: From Your Room to a Night Street in Leather](makeviral/devil-wears-prada-ai-trend/PROMPTS.md) | `devil-wears-prada-ai-trend` | 2026-10-18 | 2 | ✅ | [link](https://www.makeviral.ai/templates/devil-wears-prada-ai-trend) |
| [Coldplay Kiss Cam Meme: You and a Friend on the Big Screen](makeviral/coldplay-affair-ai-trend/PROMPTS.md) | `coldplay-affair-ai-trend` | 2026-10-18 | 2 | ✅ | [link](https://www.makeviral.ai/templates/coldplay-affair-ai-trend) |
| [Bby Wow Guy AI: Put Your Face in the Guy Dancing at a Quince Meme](makeviral/bby-wow-guy-ai-trend/PROMPTS.md) | `bby-wow-guy-ai-trend` | 2026-10-18 | 1 | ✅ | [link](https://www.makeviral.ai/templates/bby-wow-guy-ai-trend) |
| [Abra Kadabra Trend AI: Snap, and Your Friend Appears](makeviral/abra-kadabra-ai-trend/PROMPTS.md) | `abra-kadabra-ai-trend` | 2026-10-18 | 3 | ✅ | [link](https://www.makeviral.ai/templates/abra-kadabra-ai-trend) |
| [You Look Lonely, I Can Fix That: The AI Hologram Video](makeviral/you-look-lonely-ai-trend/PROMPTS.md) | `you-look-lonely-ai-trend` | 2026-10-17 | 3 | ✅ | [link](https://www.makeviral.ai/templates/you-look-lonely-ai-trend) |
| [Susan Dell Dance AI: Do the Lord Farquaad Dance From One Photo](makeviral/susan-dell-dance-ai/PROMPTS.md) | `susan-dell-dance-ai` | 2026-10-17 | 1 | ✅ | [link](https://www.makeviral.ai/templates/susan-dell-dance-ai) |
| [Singing Dog AI Trend: Your Dog Blow-Dries Its Fur and Sings](makeviral/singing-dog-ai-trend/PROMPTS.md) | `singing-dog-ai-trend` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/singing-dog-ai-trend) |
| [Shan Shen Bu AI Dance: Do the Flash Step From One Photo](makeviral/shan-shen-bu-ai-dance/PROMPTS.md) | `shan-shen-bu-ai-dance` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/shan-shen-bu-ai-dance) |
| [Mi Chico Dance: Do the Trend From Your Photo](makeviral/mi-chico-dance-ai-trend/PROMPTS.md) | `mi-chico-dance-ai-trend` | 2026-10-17 | 3 | ✅ | [link](https://www.makeviral.ai/templates/mi-chico-dance-ai-trend) |
| [La Calabaza Dance: Your Pet Times Three, From One Photo](makeviral/la-calabaza-ai-dance/PROMPTS.md) | `la-calabaza-ai-dance` | 2026-10-17 | 3 | ✅ | [link](https://www.makeviral.ai/templates/la-calabaza-ai-dance) |
| [Sen Sağ Bek, Sen Sol Bek AI: Be the Halı Saha Captain Who Says "Konum Gönderin"](makeviral/hali-saha-konum-gonderin-ai-trend/PROMPTS.md) | `hali-saha-konum-gonderin-ai-trend` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/hali-saha-konum-gonderin-ai-trend) |
| [AI Grandma Parkour: Your Grandma (or Grandpa) Does the Stunts](makeviral/grandma-parkour-ai-trend/PROMPTS.md) | `grandma-parkour-ai-trend` | 2026-10-17 | 3 | ✅ | [link](https://www.makeviral.ai/templates/grandma-parkour-ai-trend) |
| [Gemini Rain AI Effect: Put Yourself, or the Two of You, in Cinematic Rain](makeviral/gemini-rain-ai-effect/PROMPTS.md) | `gemini-rain-ai-effect` | 2026-10-17 | 3 | ✅ | [link](https://www.makeviral.ai/templates/gemini-rain-ai-effect) |
| [Flying Tesla Roadster AI Video: Rocket Over the Traffic Jam](makeviral/flying-roadster-ai-trend/PROMPTS.md) | `flying-roadster-ai-trend` | 2026-10-17 | 8 | ✅ | [link](https://www.makeviral.ai/templates/flying-roadster-ai-trend) |
| [Damon Salvatore AI Trend: Walk Into the Church and Smirk as Damon](makeviral/damon-salvatore-ai-trend/PROMPTS.md) | `damon-salvatore-ai-trend` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/damon-salvatore-ai-trend) |
| [Closer Dance AI: You and a Friend in the Original Reel](makeviral/closer-dance-ai-trend/PROMPTS.md) | `closer-dance-ai-trend` | 2026-10-17 | 1 | ✅ | [link](https://www.makeviral.ai/templates/closer-dance-ai-trend) |
| [Closed on Sunday AI Trend: Stand Still While the Choir Sings](makeviral/closed-on-sunday-ai-trend/PROMPTS.md) | `closed-on-sunday-ai-trend` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/closed-on-sunday-ai-trend) |
| [Boombox Rap AI: Rap Down the Street While Your Friend Carries the Boombox](makeviral/boombox-rap-ai-trend/PROMPTS.md) | `boombox-rap-ai-trend` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/boombox-rap-ai-trend) |
| [High Altitude Trampoline AI Video: Leap, Bounce, Fly Back Up](makeviral/ai-high-altitude-trampoline/PROMPTS.md) | `ai-high-altitude-trampoline` | 2026-10-17 | 3 | ✅ | [link](https://www.makeviral.ai/templates/ai-high-altitude-trampoline) |
| [Hair Dye Filter: AI Dyes Your Hair Burgundy From One Photo](makeviral/ai-hair-dye-filter/PROMPTS.md) | `ai-hair-dye-filter` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-hair-dye-filter) |
| [Electric Shock Meme AI: You, Your Dog, Two Wires and Sooty Hair](makeviral/ai-electric-shock-pet-prank/PROMPTS.md) | `ai-electric-shock-pet-prank` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-electric-shock-pet-prank) |
| [Crochet Filter: AI Turns Your Photo Into a Crochet Doll of You](makeviral/ai-crochet-doll-filter/PROMPTS.md) | `ai-crochet-doll-filter` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-crochet-doll-filter) |
| [Celebrity Signature Filter: Sign Autographs for Your Fans with AI](makeviral/ai-celebrity-autograph-signing/PROMPTS.md) | `ai-celebrity-autograph-signing` | 2026-10-17 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-celebrity-autograph-signing) |
| [A2O LITE NEON Dance: Do the Duo Intro From Your Photos](makeviral/a2o-lite-neon-ai-dance/PROMPTS.md) | `a2o-lite-neon-ai-dance` | 2026-10-17 | 3 | ✅ | [link](https://www.makeviral.ai/templates/a2o-lite-neon-ai-dance) |
| [Yamal Rabona AI: Fake the Rabona and Leave the Defender on the Grass](makeviral/yamal-no-rabona-ai-trend/PROMPTS.md) | `yamal-no-rabona-ai-trend` | 2026-10-16 | 3 | ✅ | [link](https://www.makeviral.ai/templates/yamal-no-rabona-ai-trend) |
| [Topo Gigio Trend: Do the Enzo Fernandez Celebration With AI](makeviral/topo-gigio-celebration-ai-trend/PROMPTS.md) | `topo-gigio-celebration-ai-trend` | 2026-10-16 | 2 | ✅ | [link](https://www.makeviral.ai/templates/topo-gigio-celebration-ai-trend) |
| [The Jawn Dance: Wait for the Drop From One Photo](makeviral/the-jawn-ai-dance/PROMPTS.md) | `the-jawn-ai-dance` | 2026-10-16 | 2 | ✅ | [link](https://www.makeviral.ai/templates/the-jawn-ai-dance) |
| [La Tormenta de Arena AI Trend: Te He Perdido Entre la Gente](makeviral/te-he-perdido-entre-la-gente-ai-trend/PROMPTS.md) | `te-he-perdido-entre-la-gente-ai-trend` | 2026-10-16 | 2 | ✅ | [link](https://www.makeviral.ai/templates/te-he-perdido-entre-la-gente-ai-trend) |
| [Subway Outfit Change AI: Every Train Brings a New Outfit](makeviral/subway-outfit-change-ai-trend/PROMPTS.md) | `subway-outfit-change-ai-trend` | 2026-10-16 | 1 | ✅ | [link](https://www.makeviral.ai/templates/subway-outfit-change-ai-trend) |
| [Slap Everyone Meme: Slap the Whole Crowd in an AI Video](makeviral/slap-everyone-ai-trend/PROMPTS.md) | `slap-everyone-ai-trend` | 2026-10-16 | 1 | ✅ | [link](https://www.makeviral.ai/templates/slap-everyone-ai-trend) |
| [SaWaDiKa Dance: Do LISA's Trend From One Photo](makeviral/sawadika-dance-ai-trend/PROMPTS.md) | `sawadika-dance-ai-trend` | 2026-10-16 | 2 | ✅ | [link](https://www.makeviral.ai/templates/sawadika-dance-ai-trend) |
| [Backwards Hurdle AI: Do the Famous Reverse Hurdle From One Photo](makeviral/reverse-hurdle-ai-trend/PROMPTS.md) | `reverse-hurdle-ai-trend` | 2026-10-16 | 1 | ✅ | [link](https://www.makeviral.ai/templates/reverse-hurdle-ai-trend) |
| [No Renunciaré AI Trend: Sing the Bolero With a Giant Mustache](makeviral/no-renunciare-ai-trend/PROMPTS.md) | `no-renunciare-ai-trend` | 2026-10-16 | 2 | ✅ | [link](https://www.makeviral.ai/templates/no-renunciare-ai-trend) |
| [Glitch Makeup AI Transition: From Paint Swipe to Cyber Look](makeviral/glitch-makeup-ai-transition/PROMPTS.md) | `glitch-makeup-ai-transition` | 2026-10-16 | 1 | ✅ | [link](https://www.makeviral.ai/templates/glitch-makeup-ai-transition) |
| [Escalator Outfit Change AI: A New Look With Every Ride](makeviral/escalator-outfit-change-ai-trend/PROMPTS.md) | `escalator-outfit-change-ai-trend` | 2026-10-16 | 1 | ✅ | [link](https://www.makeviral.ai/templates/escalator-outfit-change-ai-trend) |
| [AI Couple Thriller: The Cliff Kiss With a Twist](makeviral/couple-thriller-ai-trend/PROMPTS.md) | `couple-thriller-ai-trend` | 2026-10-16 | 1 | ✅ | [link](https://www.makeviral.ai/templates/couple-thriller-ai-trend) |
| [Champagne Birthday Trend: Pop the Bottle, Freeze in Black and White](makeviral/champagne-birthday-ai-trend/PROMPTS.md) | `champagne-birthday-ai-trend` | 2026-10-16 | 2 | ✅ | [link](https://www.makeviral.ai/templates/champagne-birthday-ai-trend) |
| [Blue Screen Glitch AI Trend: You, a Burning Sofa and a System Crash](makeviral/blue-screen-glitch-ai-trend/PROMPTS.md) | `blue-screen-glitch-ai-trend` | 2026-10-16 | 1 | ✅ | [link](https://www.makeviral.ai/templates/blue-screen-glitch-ai-trend) |
| [Barbie and Raquelle AI Trend: You as a 3D Doll Cartoon](makeviral/barbie-and-raquelle-ai-trend/PROMPTS.md) | `barbie-and-raquelle-ai-trend` | 2026-10-16 | 2 | ✅ | [link](https://www.makeviral.ai/templates/barbie-and-raquelle-ai-trend) |
| [AI Werewolf Transformation: Watch Yourself Turn Into a Wolf](makeviral/ai-werewolf-transformation/PROMPTS.md) | `ai-werewolf-transformation` | 2026-10-16 | 3 | ✅ | [link](https://www.makeviral.ai/templates/ai-werewolf-transformation) |
| [Venom Car Trend: Black Liquid Builds Your Car](makeviral/venom-car-ai-trend/PROMPTS.md) | `venom-car-ai-trend` | 2026-10-15 | 1 | ✅ | [link](https://www.makeviral.ai/templates/venom-car-ai-trend) |
| [The End AI Trend: Your Dog or Cat Waving Goodbye, Then It Runs Off](makeviral/the-end-ai-trend/PROMPTS.md) | `the-end-ai-trend` | 2026-10-15 | 3 | ✅ | [link](https://www.makeviral.ai/templates/the-end-ai-trend) |
| [Otsukare Summer Dance: Do the Daijoubu Trend From One Photo](makeviral/otsukare-summer-dance-ai-trend/PROMPTS.md) | `otsukare-summer-dance-ai-trend` | 2026-10-15 | 2 | ✅ | [link](https://www.makeviral.ai/templates/otsukare-summer-dance-ai-trend) |
| [Lego Car Wash AI: Tiny Toy Workers Wash Your Ride](makeviral/lego-car-wash-ai-trend/PROMPTS.md) | `lego-car-wash-ai-trend` | 2026-10-15 | 2 | ✅ | [link](https://www.makeviral.ai/templates/lego-car-wash-ai-trend) |
| [I'm With You Trend: Sing Avril Lavigne on the Roller Coaster](makeviral/im-with-you-ai-trend/PROMPTS.md) | `im-with-you-ai-trend` | 2026-10-15 | 1 | ✅ | [link](https://www.makeviral.ai/templates/im-with-you-ai-trend) |
| [Happy Friday I'm Onnat: Drive the Football Toy Car](makeviral/im-onnat-football-ai-trend/PROMPTS.md) | `im-onnat-football-ai-trend` | 2026-10-15 | 2 | ✅ | [link](https://www.makeviral.ai/templates/im-onnat-football-ai-trend) |
| [Fergie Baby Trend: Your AI Swagger Walk Out of the Park Gate](makeviral/fergie-baby-ai-trend/PROMPTS.md) | `fergie-baby-ai-trend` | 2026-10-15 | 1 | ✅ | [link](https://www.makeviral.ai/templates/fergie-baby-ai-trend) |
| [ChatGPT Millionaire Trend: “How I Become a Millionaire?” “Get a Job.”](makeviral/chatgpt-millionaire-ai-trend/PROMPTS.md) | `chatgpt-millionaire-ai-trend` | 2026-10-15 | 2 | ✅ | [link](https://www.makeviral.ai/templates/chatgpt-millionaire-ai-trend) |
| [Chat GTT Lookin' Ahh AI: You or Your Pet in the Card Declined Meme](makeviral/chat-gtt-lookin-ahh-ai/PROMPTS.md) | `chat-gtt-lookin-ahh-ai` | 2026-10-15 | 2 | ✅ | [link](https://www.makeviral.ai/templates/chat-gtt-lookin-ahh-ai) |
| [Caught at the Window: AI Commercial Generator for Your Brand](makeviral/caught-at-the-window-ai-ad/PROMPTS.md) | `caught-at-the-window-ai-ad` | 2026-10-15 | 1 | ✅ | [link](https://www.makeviral.ai/templates/caught-at-the-window-ai-ad) |
| [BbY WOW Dance AI Trend: Garage Dance, Quince Meme or Your Pet](makeviral/bby-wow-dance-ai-trend/PROMPTS.md) | `bby-wow-dance-ai-trend` | 2026-10-15 | 2 | ✅ | [link](https://www.makeviral.ai/templates/bby-wow-dance-ai-trend) |
| [Babydoll Dance AI: Do the Viral Jamie Miller Dance From One Photo](makeviral/babydoll-dance-ai-trend/PROMPTS.md) | `babydoll-dance-ai-trend` | 2026-10-15 | 4 | ✅ | [link](https://www.makeviral.ai/templates/babydoll-dance-ai-trend) |
| [APT AI Video: You and a Friend in the Pink APT. Studio](makeviral/apt-ai-trend/PROMPTS.md) | `apt-ai-trend` | 2026-10-15 | 2 | ✅ | [link](https://www.makeviral.ai/templates/apt-ai-trend) |
| [AI Muscle Generator: You, With a Huge Bodybuilder Body](makeviral/ai-steroids-filter/PROMPTS.md) | `ai-steroids-filter` | 2026-10-15 | 3 | ✅ | [link](https://www.makeviral.ai/templates/ai-steroids-filter) |
| [Split Face Trend: Half Your Face, Half Your Parent's](makeviral/ai-family-resemblance-photo/PROMPTS.md) | `ai-family-resemblance-photo` | 2026-10-15 | 1 | ✅ | [link](https://www.makeviral.ai/templates/ai-family-resemblance-photo) |
| [AI Dunk Trend: Dunk in a Pro Game From One Photo](makeviral/ai-dunk-trend/PROMPTS.md) | `ai-dunk-trend` | 2026-10-15 | 6 | ✅ | [link](https://www.makeviral.ai/templates/ai-dunk-trend) |
| [Car Crash Prank: The AI Airbag Filter From One Photo](makeviral/ai-car-crash-prank-filter/PROMPTS.md) | `ai-car-crash-prank-filter` | 2026-10-15 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-car-crash-prank-filter) |
| [Wipe Me Down AI Dance: Do the Viral Dance From One Photo](makeviral/wipe-me-down-ai-dance/PROMPTS.md) | `wipe-me-down-ai-dance` | 2026-10-14 | 1 | ✅ | [link](https://www.makeviral.ai/templates/wipe-me-down-ai-dance) |
| [Walk It Like I Talk It AI: Your Squad in the Carpool Rap](makeviral/walk-it-like-i-talk-it-ai-trend/PROMPTS.md) | `walk-it-like-i-talk-it-ai-trend` | 2026-10-14 | 3 | ✅ | [link](https://www.makeviral.ai/templates/walk-it-like-i-talk-it-ai-trend) |
| [Toc Toc Dance AI: Do the Viral Jean Phil Dance From One Photo](makeviral/toc-toc-dance-ai-trend/PROMPTS.md) | `toc-toc-dance-ai-trend` | 2026-10-14 | 3 | ✅ | [link](https://www.makeviral.ai/templates/toc-toc-dance-ai-trend) |
| [Tim Burton Girls: Sit with the Gothic Dolls in One AI Photo](makeviral/tim-burton-girls-ai-trend/PROMPTS.md) | `tim-burton-girls-ai-trend` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/tim-burton-girls-ai-trend) |
| [Spooky Scary Skeletons AI Dance: You as the Vampire Under the Orange Moon](makeviral/spooky-scary-skeletons-ai-dance/PROMPTS.md) | `spooky-scary-skeletons-ai-dance` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/spooky-scary-skeletons-ai-dance) |
| [South Park Filter: You as a Paper Cut-Out Cartoon](makeviral/south-park-ai-filter/PROMPTS.md) | `south-park-ai-filter` | 2026-10-14 | 3 | ✅ | [link](https://www.makeviral.ai/templates/south-park-ai-filter) |
| [Sniffer Dog Meme AI: Put Yourself in the Viral “Bro Is So Cooked” Clip](makeviral/sniffer-dog-ai-trend/PROMPTS.md) | `sniffer-dog-ai-trend` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/sniffer-dog-ai-trend) |
| [Smash and Grab AI Video: Spot It, Smash the Window, Run](makeviral/smash-and-grab-ai-trend/PROMPTS.md) | `smash-and-grab-ai-trend` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/smash-and-grab-ai-trend) |
| [Polar Bear 2026 AI: Sing Remember November From One Photo](makeviral/polar-bear-ai-trend/PROMPTS.md) | `polar-bear-ai-trend` | 2026-10-14 | 3 | ✅ | [link](https://www.makeviral.ai/templates/polar-bear-ai-trend) |
| [Opa Opa Opa Trend AI: Bounce Your Hair to the Viral Sound](makeviral/opa-opa-bouncy-hair-ai/PROMPTS.md) | `opa-opa-bouncy-hair-ai` | 2026-10-14 | 3 | ✅ | [link](https://www.makeviral.ai/templates/opa-opa-bouncy-hair-ai) |
| [Mind Enterprises Balcony AI Video: You and a Friend as the Balcony DJ Duo](makeviral/mind-enterprises-balcony-ai-trend/PROMPTS.md) | `mind-enterprises-balcony-ai-trend` | 2026-10-14 | 1 | ✅ | [link](https://www.makeviral.ai/templates/mind-enterprises-balcony-ai-trend) |
| [I Wanna Love You Cat Trend: Your Pet Sings the Viral AI Selfie](makeviral/i-wanna-love-you-ai-pet/PROMPTS.md) | `i-wanna-love-you-ai-pet` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/i-wanna-love-you-ai-pet) |
| [Hit the Road Dude: Be the Private Property Meme Driver](makeviral/hit-the-road-dude-ai-trend/PROMPTS.md) | `hit-the-road-dude-ai-trend` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/hit-the-road-dude-ai-trend) |
| [Headbop Trend AI: Your Family's Heads Bop in a Row](makeviral/headbop-ai-trend/PROMPTS.md) | `headbop-ai-trend` | 2026-10-14 | 3 | ✅ | [link](https://www.makeviral.ai/templates/headbop-ai-trend) |
| [Ghost Filter Prank: A Creepy Ghost Rises Behind You](makeviral/ghost-filter-prank-ai-trend/PROMPTS.md) | `ghost-filter-prank-ai-trend` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ghost-filter-prank-ai-trend) |
| [Gang Gang Dance AI: Do the Viral Jean Phil Battle Dance From One Photo](makeviral/gang-gang-dance-ai-trend/PROMPTS.md) | `gang-gang-dance-ai-trend` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/gang-gang-dance-ai-trend) |
| [Crazy Frog AI Trend: You on the Invisible Motorbike](makeviral/crazy-frog-ai-trend/PROMPTS.md) | `crazy-frog-ai-trend` | 2026-10-14 | 3 | ✅ | [link](https://www.makeviral.ai/templates/crazy-frog-ai-trend) |
| [Car Roof Backflip AI Video: You Flip From One Car to the Next](makeviral/car-roof-backflip-ai-trend/PROMPTS.md) | `car-roof-backflip-ai-trend` | 2026-10-14 | 1 | ✅ | [link](https://www.makeviral.ai/templates/car-roof-backflip-ai-trend) |
| [Bad Times AI Trend: Argue With the Camera From One Photo](makeviral/bad-times-ai-trend/PROMPTS.md) | `bad-times-ai-trend` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/bad-times-ai-trend) |
| [Dimitri Meme AI: Amanhã é Feriado, Starring You](makeviral/amanha-e-feriado-ai-trend/PROMPTS.md) | `amanha-e-feriado-ai-trend` | 2026-10-14 | 1 | ✅ | [link](https://www.makeviral.ai/templates/amanha-e-feriado-ai-trend) |
| [Heaven Hug AI: Run Into Their Arms Above the Clouds](makeviral/ai-heaven-reunion-hug/PROMPTS.md) | `ai-heaven-reunion-hug` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-heaven-reunion-hug) |
| [Day of the Dead Pet AI: Your Pet's First Día de Muertos](makeviral/ai-day-of-the-dead-pet/PROMPTS.md) | `ai-day-of-the-dead-pet` | 2026-10-14 | 3 | ✅ | [link](https://www.makeviral.ai/templates/ai-day-of-the-dead-pet) |
| [Car Jump AI Video: A Truck Flies Over You, You Stay Calm](makeviral/ai-car-jump-trend/PROMPTS.md) | `ai-car-jump-trend` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-car-jump-trend) |
| [Bob Filter Prank: AI Cuts Your Long Hair Into a Bob](makeviral/ai-bob-haircut-filter/PROMPTS.md) | `ai-bob-haircut-filter` | 2026-10-14 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-bob-haircut-filter) |
| [Barn Find AI Trend: What Your Kids Will Find in the Barn](makeviral/ai-barn-find-truck-trend/PROMPTS.md) | `ai-barn-find-truck-trend` | 2026-10-14 | 4 | ✅ | [link](https://www.makeviral.ai/templates/ai-barn-find-truck-trend) |
| [Whining Dog Meme: Make Your Dog Whine Like the Viral Doberman](makeviral/whiny-dog-ai-trend/PROMPTS.md) | `whiny-dog-ai-trend` | 2026-10-13 | 1 | ✅ | [link](https://www.makeviral.ai/templates/whiny-dog-ai-trend) |
| [Squishy Face AI Trend: Turn Your Face Into a Squishy Toy From One Photo](makeviral/squishy-ai-trend/PROMPTS.md) | `squishy-ai-trend` | 2026-10-13 | 4 | ✅ | [link](https://www.makeviral.ai/templates/squishy-ai-trend) |
| [Popstar AI: Star in the Popstar Music Video From One Photo](makeviral/popstar-ai-trend/PROMPTS.md) | `popstar-ai-trend` | 2026-10-13 | 1 | ✅ | [link](https://www.makeviral.ai/templates/popstar-ai-trend) |
| [Cale Brown Dance AI: Do the Viral Keep On Steppin Steps From One Photo](makeviral/keep-on-steppin-ai-dance/PROMPTS.md) | `keep-on-steppin-ai-dance` | 2026-10-13 | 1 | ✅ | [link](https://www.makeviral.ai/templates/keep-on-steppin-ai-dance) |
| [Hawak Mo Ang Beat Dance AI: Do the Viral Filipino Dance From One Photo](makeviral/hawak-mo-ang-beat-ai-dance/PROMPTS.md) | `hawak-mo-ang-beat-ai-dance` | 2026-10-13 | 1 | ✅ | [link](https://www.makeviral.ai/templates/hawak-mo-ang-beat-ai-dance) |
| [Airplane Flying Over Head AI Trend: A Jet Right Above You](makeviral/ai-plane-over-head-trend/PROMPTS.md) | `ai-plane-over-head-trend` | 2026-10-13 | 4 | ✅ | [link](https://www.makeviral.ai/templates/ai-plane-over-head-trend) |
| [AI Baby Dance: Turn One Baby Photo Into the Viral Dance](makeviral/ai-baby-dance/PROMPTS.md) | `ai-baby-dance` | 2026-10-13 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-baby-dance) |
| [24 Unforgettable Car Trend AI: Flick the 2 and 4, Reveal Your Car](makeviral/unforgettable-car-trend-ai/PROMPTS.md) | `unforgettable-car-trend-ai` | 2026-10-12 | 4 | ✅ | [link](https://www.makeviral.ai/templates/unforgettable-car-trend-ai) |
| [Toz Pembe AI: Dance the Routine at the Giant Boombox](makeviral/toz-pembe-ai-trend/PROMPTS.md) | `toz-pembe-ai-trend` | 2026-10-12 | 3 | ✅ | [link](https://www.makeviral.ai/templates/toz-pembe-ai-trend) |
| [Thriller Dance AI: Do the Zombie Dance With a Friend or Your Pet](makeviral/thriller-dance-ai-trend/PROMPTS.md) | `thriller-dance-ai-trend` | 2026-10-12 | 2 | ✅ | [link](https://www.makeviral.ai/templates/thriller-dance-ai-trend) |
| [Tecktonik Dance AI: Your Turn on the String-Light Stage](makeviral/tecktonik-dance-ai-trend/PROMPTS.md) | `tecktonik-dance-ai-trend` | 2026-10-12 | 3 | ✅ | [link](https://www.makeviral.ai/templates/tecktonik-dance-ai-trend) |
| [Single Ladies Dog Dance: Your Pet Takes Center Stage](makeviral/single-ladies-dog-dance-ai/PROMPTS.md) | `single-ladies-dog-dance-ai` | 2026-10-12 | 2 | ✅ | [link](https://www.makeviral.ai/templates/single-ladies-dog-dance-ai) |
| [Phone on the Train Trend: Your Face in the Paris Metro Reel](makeviral/phone-on-train-trend/PROMPTS.md) | `phone-on-train-trend` | 2026-10-12 | 1 | ✅ | [link](https://www.makeviral.ai/templates/phone-on-train-trend) |
| [My Ride Is Here: Hop on the Broom and Fly Off Beside the Car](makeviral/my-ride-is-here-broom-trend/PROMPTS.md) | `my-ride-is-here-broom-trend` | 2026-10-12 | 1 | ✅ | [link](https://www.makeviral.ai/templates/my-ride-is-here-broom-trend) |
| [Halay AI Trend: Dance the TV Show Halay With Two Friends](makeviral/halay-ai-trend/PROMPTS.md) | `halay-ai-trend` | 2026-10-12 | 2 | ✅ | [link](https://www.makeviral.ai/templates/halay-ai-trend) |
| [Gömleği Cekete Dönüşen Adam AI: Dance the Viral Turkish Wedding Clip](makeviral/gomlegi-cekete-donusen-adam-ai/PROMPTS.md) | `gomlegi-cekete-donusen-adam-ai` | 2026-10-12 | 2 | ✅ | [link](https://www.makeviral.ai/templates/gomlegi-cekete-donusen-adam-ai) |
| [Gas Station Dance AI: Put You and Your Friends in the Viral Road Trip Reel](makeviral/gas-station-dance-ai-trend/PROMPTS.md) | `gas-station-dance-ai-trend` | 2026-10-12 | 3 | ✅ | [link](https://www.makeviral.ai/templates/gas-station-dance-ai-trend) |
| [Elsa AI Trend: Let It Go in the Ice Palace, Starring Your Kid](makeviral/elsa-ai-trend/PROMPTS.md) | `elsa-ai-trend` | 2026-10-12 | 2 | ✅ | [link](https://www.makeviral.ai/templates/elsa-ai-trend) |
| [Billie Jean Dance AI: Do the Famous Moves With One Photo](makeviral/billie-jean-dance-ai-trend/PROMPTS.md) | `billie-jean-dance-ai-trend` | 2026-10-12 | 4 | ✅ | [link](https://www.makeviral.ai/templates/billie-jean-dance-ai-trend) |
| [AI Lion Friend: A Lion Walks Up to You on a Night Road](makeviral/ai-lion-friend-video/PROMPTS.md) | `ai-lion-friend-video` | 2026-10-12 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-lion-friend-video) |
| [Catrina Makeup AI: See Yourself in Day of the Dead Makeup](makeviral/ai-day-of-the-dead-makeup/PROMPTS.md) | `ai-day-of-the-dead-makeup` | 2026-10-12 | 4 | ✅ | [link](https://www.makeviral.ai/templates/ai-day-of-the-dead-makeup) |
| [AI Arrest Trend: Make the “Getting Arrested Again” Video With One Photo](makeviral/ai-arrest-trend/PROMPTS.md) | `ai-arrest-trend` | 2026-10-12 | 4 | ✅ | [link](https://www.makeviral.ai/templates/ai-arrest-trend) |
| [AI Airport Celebrity Video: Walk Out of Arrivals Like a Star](makeviral/ai-airport-star-arrival/PROMPTS.md) | `ai-airport-star-arrival` | 2026-10-12 | 8 | ✅ | [link](https://www.makeviral.ai/templates/ai-airport-star-arrival) |
| [2016 vs 2026: Your 2016 Self Walks In and Meets You](makeviral/2016-me-meets-2026-me-ai/PROMPTS.md) | `2016-me-meets-2026-me-ai` | 2026-10-12 | 4 | ✅ | [link](https://www.makeviral.ai/templates/2016-me-meets-2026-me-ai) |
| [Ramalama Bang Bang Trend: Your Pet's Halloween Costume Walk](makeviral/ramalama-ai-trend/PROMPTS.md) | `ramalama-ai-trend` | 2026-10-11 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ramalama-ai-trend) |
| [Ozil Goal AI Trend: Score the Famous Solo Goal Yourself](makeviral/ozil-goal-ai-trend/PROMPTS.md) | `ozil-goal-ai-trend` | 2026-10-11 | 1 | ✅ | [link](https://www.makeviral.ai/templates/ozil-goal-ai-trend) |
| [Fredo Bang Oouuh AI Trend: Put the Two of You in the Kitchen](makeviral/oouuh-ai-trend/PROMPTS.md) | `oouuh-ai-trend` | 2026-10-11 | 1 | ✅ | [link](https://www.makeviral.ai/templates/oouuh-ai-trend) |
| [Nicole Kidman Dance AI: Do the Viral Routine With One Photo](makeviral/nicole-kidman-dance-ai-trend/PROMPTS.md) | `nicole-kidman-dance-ai-trend` | 2026-10-11 | 2 | ✅ | [link](https://www.makeviral.ai/templates/nicole-kidman-dance-ai-trend) |
| [Clapping Cat: Make Your Pet Grin and Clap Like the Black Cat](makeviral/clapping-cat-ai-video/PROMPTS.md) | `clapping-cat-ai-video` | 2026-10-11 | 2 | ✅ | [link](https://www.makeviral.ai/templates/clapping-cat-ai-video) |
| [Smalltown Boy Cats: Put Your Two Pets in the Viral AI Dance](makeviral/smalltown-boy-ai-dance/PROMPTS.md) | `smalltown-boy-ai-dance` | 2026-10-10 | 2 | ✅ | [link](https://www.makeviral.ai/templates/smalltown-boy-ai-dance) |
| [Raindance AI Trend: Put the Two of You on the Pier](makeviral/raindance-ai-trend/PROMPTS.md) | `raindance-ai-trend` | 2026-10-10 | 2 | ✅ | [link](https://www.makeviral.ai/templates/raindance-ai-trend) |
| [Burning Bridges AI Trend: Put Yourself in the "Where She At?" Party](makeviral/burning-bridges-ai-trend/PROMPTS.md) | `burning-bridges-ai-trend` | 2026-10-10 | 3 | ✅ | [link](https://www.makeviral.ai/templates/burning-bridges-ai-trend) |
| [Bulin 47 AI: Step Into the Dame Hombro Freestyle](makeviral/bulin-47-ai-trend/PROMPTS.md) | `bulin-47-ai-trend` | 2026-10-10 | 2 | ✅ | [link](https://www.makeviral.ai/templates/bulin-47-ai-trend) |
| [Alors On Danse AI: Put You and a Friend in the Studio Sketch](makeviral/alors-on-danse-ai-trend/PROMPTS.md) | `alors-on-danse-ai-trend` | 2026-10-10 | 2 | ✅ | [link](https://www.makeviral.ai/templates/alors-on-danse-ai-trend) |
| [AI School Photo: Classic School Pictures From a Phone Photo](makeviral/ai-school-photo/PROMPTS.md) | `ai-school-photo` | 2026-10-09 | 1 | ✅ | [link](https://www.makeviral.ai/templates/ai-school-photo) |
| [AI Pumpkin Head Photoshoot: The Halloween Trend From One Photo](makeviral/ai-pumpkin-head-photoshoot/PROMPTS.md) | `ai-pumpkin-head-photoshoot` | 2026-10-09 | 4 | ✅ | [link](https://www.makeviral.ai/templates/ai-pumpkin-head-photoshoot) |
| [Knight Sword Swap AI Video: The Big Knight Takes the Heavy Sword](makeviral/knight-sword-swap-ai-video/PROMPTS.md) | `knight-sword-swap-ai-video` | 2026-10-08 | 3 | ✅ | [link](https://www.makeviral.ai/templates/knight-sword-swap-ai-video) |
| [Remember Your Gym Bro AI Video: Your Tiny Knight Next to a Giant](makeviral/knight-standing-ai-video/PROMPTS.md) | `knight-standing-ai-video` | 2026-10-08 | 2 | ✅ | [link](https://www.makeviral.ai/templates/knight-standing-ai-video) |
| [Knight Cat AI Video: Make Your Cat or Dog the Kitten Knight](makeviral/knight-cat-ai-video/PROMPTS.md) | `knight-cat-ai-video` | 2026-10-08 | 8 | ✅ | [link](https://www.makeviral.ai/templates/knight-cat-ai-video) |
| [Ghostface AI Trend: Put Yourself in the 90s Horror Phone Call](makeviral/ghostface-ai-trend/PROMPTS.md) | `ghostface-ai-trend` | 2026-10-08 | 4 | ✅ | [link](https://www.makeviral.ai/templates/ghostface-ai-trend) |
| [Mom and Baby Knight AI Video: You and Your Little One as Knights](makeviral/baby-knight-ai-video/PROMPTS.md) | `baby-knight-ai-video` | 2026-10-08 | 1 | ✅ | [link](https://www.makeviral.ai/templates/baby-knight-ai-video) |
| [AI Zombie Trend: The Zombie Love Story With Your Partner or Pet](makeviral/ai-zombie-trend/PROMPTS.md) | `ai-zombie-trend` | 2026-10-08 | 3 | ✅ | [link](https://www.makeviral.ai/templates/ai-zombie-trend) |
| [Rumpelstiltskin AI: Make the Tip Toe Dance With Your Face](makeviral/ai-rumpelstiltskin-dance/PROMPTS.md) | `ai-rumpelstiltskin-dance` | 2026-10-08 | 6 | ✅ | [link](https://www.makeviral.ai/templates/ai-rumpelstiltskin-dance) |
| [AI Dog Costume: Your Dog or Cat in Any Halloween Costume](makeviral/ai-pet-halloween-costume/PROMPTS.md) | `ai-pet-halloween-costume` | 2026-10-08 | 4 | ✅ | [link](https://www.makeviral.ai/templates/ai-pet-halloween-costume) |
| [AI Halloween Costume Try-On: See Yourself in a Costume Before You Buy](makeviral/ai-halloween-costume/PROMPTS.md) | `ai-halloween-costume` | 2026-10-08 | 4 | ✅ | [link](https://www.makeviral.ai/templates/ai-halloween-costume) |
| [AI Ghost Photoshoot: The Sheet Ghost Trend From One Photo](makeviral/ai-ghost-photoshoot/PROMPTS.md) | `ai-ghost-photoshoot` | 2026-10-08 | 5 | ✅ | [link](https://www.makeviral.ai/templates/ai-ghost-photoshoot) |
| [AI Ceiling Fan Trend: Change Your Outfit on Every Blade Pass](makeviral/ai-ceiling-fan-trend/PROMPTS.md) | `ai-ceiling-fan-trend` | 2026-10-08 | 3 | ✅ | [link](https://www.makeviral.ai/templates/ai-ceiling-fan-trend) |
| [Storm AI Trend: Stand Still While the Crowd Bows](makeviral/storm-ai-trend/PROMPTS.md) | `storm-ai-trend` | 2026-09-30 | 1 | ✅ | [link](https://www.makeviral.ai/templates/storm-ai-trend) |
| [Giant Bed AI Trend: Make "The Bed of My Dreams" Video](makeviral/giant-bed-ai-trend/PROMPTS.md) | `giant-bed-ai-trend` | 2026-09-30 | 2 | ✅ | [link](https://www.makeviral.ai/templates/giant-bed-ai-trend) |
| [Earth Zoom Out AI: From a Selfie to Space in One Shot](makeviral/earth-zoom-out-ai/PROMPTS.md) | `earth-zoom-out-ai` | 2026-09-30 | 2 | ✅ | [link](https://www.makeviral.ai/templates/earth-zoom-out-ai) |
| [AI Hug Video: Turn Two Photos Into a Warm Hug](makeviral/ai-hug-video/PROMPTS.md) | `ai-hug-video` | 2026-09-30 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-hug-video) |
| [Hotel Lobby AI: Make the Hotel Lobby Trend Video](makeviral/ai-hotel-lobby-trend/PROMPTS.md) | `ai-hotel-lobby-trend` | 2026-09-30 | 5 | ✅ | [link](https://www.makeviral.ai/templates/ai-hotel-lobby-trend) |
| [AI Baby Generator: Make a Future Baby Home Video](makeviral/ai-future-baby-video/PROMPTS.md) | `ai-future-baby-video` | 2026-09-30 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-future-baby-video) |
| [AI Dog Dancing Video: Make Your Pet Dance](makeviral/ai-dancing-dog-video/PROMPTS.md) | `ai-dancing-dog-video` | 2026-09-30 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-dancing-dog-video) |
| [AI Crying Video: Make the Tears Effect From One Photo](makeviral/ai-crying-video/PROMPTS.md) | `ai-crying-video` | 2026-09-30 | 4 | ✅ | [link](https://www.makeviral.ai/templates/ai-crying-video) |
| [AI Cinema Breakout Video: The Train Comes Out of the Screen](makeviral/ai-cinema-breakout-video/PROMPTS.md) | `ai-cinema-breakout-video` | 2026-09-30 | 2 | ✅ | [link](https://www.makeviral.ai/templates/ai-cinema-breakout-video) |
| [80s AI Trend: Your 1985 Photo and Home Video](makeviral/80s-ai-trend/PROMPTS.md) | `80s-ai-trend` | 2026-09-30 | 2 | ✅ | [link](https://www.makeviral.ai/templates/80s-ai-trend) |

### Remake Your Meme

| Template | Slug | Date | Prompts | Demo | Page |
| --- | --- | --- | ---: | --- | --- |
| [Zombie Couple AI Video Generator](remakeyourmeme/zombie-couple-ai-trend/PROMPTS.md) | `zombie-couple-ai-trend` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/zombie-couple-ai-trend/) |
| [Smalltown Boy cat dance](remakeyourmeme/smalltown-boy-cat-dance/PROMPTS.md) | `smalltown-boy-cat-dance` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/smalltown-boy-cat-dance/) |
| [Rumpelstiltskin AI Video Generator](remakeyourmeme/rumpelstiltskin-ai-video/PROMPTS.md) | `rumpelstiltskin-ai-video` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/rumpelstiltskin-ai-video/) |
| [Raindance AI trend](remakeyourmeme/raindance-ai-trend/PROMPTS.md) | `raindance-ai-trend` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/raindance-ai-trend/) |
| [Hug in Heaven AI Video Generator](remakeyourmeme/hug-in-heaven/PROMPTS.md) | `hug-in-heaven` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/hug-in-heaven/) |
| [Ghostface AI trend](remakeyourmeme/ghostface-ai-trend/PROMPTS.md) | `ghostface-ai-trend` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/ghostface-ai-trend/) |
| [Crochet filter AI](remakeyourmeme/crochet-filter-ai/PROMPTS.md) | `crochet-filter-ai` | unknown | no (one-tap) | — | [link](https://remakeyourmeme.com/templates/crochet-filter-ai/) |
| [Crazy Frog AI Video Generator](remakeyourmeme/crazy-frog-ai-trend/PROMPTS.md) | `crazy-frog-ai-trend` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/crazy-frog-ai-trend/) |
| [Coldplay Kiss Cam AI Video Generator](remakeyourmeme/coldplay-kiss-cam-ai-video-generator/PROMPTS.md) | `coldplay-kiss-cam-ai-video-generator` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/coldplay-kiss-cam-ai-video-generator/) |
| [Closed on Sunday AI Video Generator](remakeyourmeme/closed-on-sunday-ai-trend/PROMPTS.md) | `closed-on-sunday-ai-trend` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/closed-on-sunday-ai-trend/) |
| [Burning Bridges AI Video Generator](remakeyourmeme/burning-bridges-ai-trend/PROMPTS.md) | `burning-bridges-ai-trend` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/burning-bridges-ai-trend/) |
| [Bulin 47 AI Video Generator](remakeyourmeme/bulin-47-ai-trend/PROMPTS.md) | `bulin-47-ai-trend` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/bulin-47-ai-trend/) |
| [Babydoll Dance AI Video Generator](remakeyourmeme/babydoll-dance-ai/PROMPTS.md) | `babydoll-dance-ai` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/babydoll-dance-ai/) |
| [Avatar Seven Havens AI](remakeyourmeme/avatar-seven-havens-ai/PROMPTS.md) | `avatar-seven-havens-ai` | unknown | no (one-tap) | — | [link](https://remakeyourmeme.com/templates/avatar-seven-havens-ai/) |
| [Alors On Danse AI Video Generator](remakeyourmeme/alors-on-danse-ai-trend/PROMPTS.md) | `alors-on-danse-ai-trend` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/alors-on-danse-ai-trend/) |
| [AI pumpkin head photoshoot](remakeyourmeme/ai-pumpkin-head-photoshoot/PROMPTS.md) | `ai-pumpkin-head-photoshoot` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/ai-pumpkin-head-photoshoot/) |
| [Hotel Lobby AI Video Generator](remakeyourmeme/ai-hotel-lobby-trend/PROMPTS.md) | `ai-hotel-lobby-trend` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/ai-hotel-lobby-trend/) |
| [AI Halloween costume](remakeyourmeme/ai-halloween-costume/PROMPTS.md) | `ai-halloween-costume` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/ai-halloween-costume/) |
| [AI ghost photoshoot](remakeyourmeme/ai-ghost-photoshoot/PROMPTS.md) | `ai-ghost-photoshoot` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/ai-ghost-photoshoot/) |
| [AI 90s school photo](remakeyourmeme/ai-90s-school-photo/PROMPTS.md) | `ai-90s-school-photo` | unknown | no (one-tap) | ✅ | [link](https://remakeyourmeme.com/templates/ai-90s-school-photo/) |

### Media.io

| Template | Slug | Date | Prompts | Demo | Page |
| --- | --- | --- | ---: | --- | --- |
| [Under the Fan AI Video](mediaio/under-the-fan-ai-video/PROMPTS.md) | `under-the-fan-ai-video` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/under-the-fan-ai-video) |
| [Ramalama Bang Bang](mediaio/ramalama-halloween-ai-video-trend/PROMPTS.md) | `ramalama-halloween-ai-video-trend` | unknown | 0 | — | [link](https://www.media.io/ai/explore/zone/ramalama-halloween-ai-video-trend) |
| [Raindance AI Trend](mediaio/raindance-ai-video-generator/PROMPTS.md) | `raindance-ai-video-generator` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/raindance-ai-video-generator) |
| [Polar Bear 2026 AI Video](mediaio/polar-bear-2026-ai-video/PROMPTS.md) | `polar-bear-2026-ai-video` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/polar-bear-2026-ai-video) |
| [Parking Lot Vibe AI Video Trend](mediaio/parking-lot-vibe-ai-video/PROMPTS.md) | `parking-lot-vibe-ai-video` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/parking-lot-vibe-ai-video) |
| [OOUUH AI Kitchen Duet](mediaio/oouuh-ai-kitchen-duet/PROMPTS.md) | `oouuh-ai-kitchen-duet` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/oouuh-ai-kitchen-duet) |
| [Not Bro Getting Arrested Again AI Video Generator](mediaio/not-bro-getting-arrested-again-ai-video-trend/PROMPTS.md) | `not-bro-getting-arrested-again-ai-video-trend` | unknown | 0 | — | [link](https://www.media.io/ai/explore/zone/not-bro-getting-arrested-again-ai-video-trend) |
| [NFL AI Fan](mediaio/nfl-ai-fan-cam-generator/PROMPTS.md) | `nfl-ai-fan-cam-generator` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/nfl-ai-fan-cam-generator) |
| [Navratri Metro Nine Forms AI Video](mediaio/navratri-metro-nine-forms-ai-video/PROMPTS.md) | `navratri-metro-nine-forms-ai-video` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/navratri-metro-nine-forms-ai-video) |
| [Gang Gang Dance](mediaio/gang-gang-dance-ai-video/PROMPTS.md) | `gang-gang-dance-ai-video` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/gang-gang-dance-ai-video) |
| [Flying Tesla Roadster AI Video](mediaio/flying-tesla-roadster-ai-video/PROMPTS.md) | `flying-tesla-roadster-ai-video` | unknown | 0 | — | [link](https://www.media.io/ai/explore/zone/flying-tesla-roadster-ai-video) |
| [Connor Price Slide Dance AI Video Generator](mediaio/connor-price-slide-dance-ai-video/PROMPTS.md) | `connor-price-slide-dance-ai-video` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/connor-price-slide-dance-ai-video) |
| [Coldplay Kiss Cam AI](mediaio/coldplay-kiss-cam-ai-filter/PROMPTS.md) | `coldplay-kiss-cam-ai-filter` | unknown | 1 | — | [link](https://www.media.io/ai/explore/zone/coldplay-kiss-cam-ai-filter) |
| [BbY Wow Guy AI Dance](mediaio/bby-wow-guy-ai-video/PROMPTS.md) | `bby-wow-guy-ai-video` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/bby-wow-guy-ai-video) |
| [Ausar AI Hotel Lobby](mediaio/ausar-ai-hotel-lobby/PROMPTS.md) | `ausar-ai-hotel-lobby` | unknown | 0 | ✅ | [link](https://www.media.io/ai/explore/zone/ausar-ai-hotel-lobby) |
| [Aura Farming Korean AI Video](mediaio/aura-farming-korean-ai-video/PROMPTS.md) | `aura-farming-korean-ai-video` | unknown | 0 | — | [link](https://www.media.io/ai/explore/zone/aura-farming-korean-ai-video) |
| [AI Food Drip Effect](mediaio/ai-food-drip-effect/PROMPTS.md) | `ai-food-drip-effect` | unknown | 0 | — | [link](https://www.media.io/ai/effect/create/ai-food-drip-effect) |
| [AI Car Video Generator](mediaio/ai-car-video-generator/PROMPTS.md) | `ai-car-video-generator` | unknown | 1 | ✅ | [link](https://www.media.io/ai/explore/zone/ai-car-video-generator) |

### Kavel

| Template | Slug | Date | Prompts | Demo | Page |
| --- | --- | --- | ---: | --- | --- |
| [Zombie Couple Video](kavel/zombie-couple-video/PROMPTS.md) | `zombie-couple-video` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/zombie-couple-video) |
| [Zombie AI Video](kavel/zombie-ai-video/PROMPTS.md) | `zombie-ai-video` | unknown | 6 | ✅ | [link](https://www.kavel.ai/video/zombie-ai-video) |
| [Wipe Me Down Dance AI](kavel/wipe-me-down-ai-dance-video/PROMPTS.md) | `wipe-me-down-ai-dance-video` | unknown | 2 | ✅ | [link](https://www.kavel.ai/video/wipe-me-down-ai-dance-video) |
| [Venom Car AI](kavel/venom-car-ai-video/PROMPTS.md) | `venom-car-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/venom-car-ai-video) |
| [Unforgettable Car Trend](kavel/unforgettable-car-ai-video/PROMPTS.md) | `unforgettable-car-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/unforgettable-car-ai-video) |
| [Twilight Baseball Scene AI Video](kavel/twilight-baseball-scene/PROMPTS.md) | `twilight-baseball-scene` | unknown | 2 | ✅ | [link](https://www.kavel.ai/video/twilight-baseball-scene) |
| [Toc Toc AI Dance](kavel/toc-toc-ai-dance/PROMPTS.md) | `toc-toc-ai-dance` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/toc-toc-ai-dance) |
| [Tip Toeing in My Jordans AI](kavel/tip-toeing-in-my-jordans-ai/PROMPTS.md) | `tip-toeing-in-my-jordans-ai` | unknown | 2 | ✅ | [link](https://www.kavel.ai/video/tip-toeing-in-my-jordans-ai) |
| [Thriller AI Dance](kavel/thriller-dance-ai-video/PROMPTS.md) | `thriller-dance-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/thriller-dance-ai-video) |
| [Tesla Flying Car AI Video](kavel/tesla-flying-car-ai-video/PROMPTS.md) | `tesla-flying-car-ai-video` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/tesla-flying-car-ai-video) |
| [Tecktonik Dance AI](kavel/tecktonik-dance-ai/PROMPTS.md) | `tecktonik-dance-ai` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/tecktonik-dance-ai) |
| [Susan Dell Dance AI](kavel/susan-dell-dance-ai-video/PROMPTS.md) | `susan-dell-dance-ai-video` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/susan-dell-dance-ai-video) |
| [STORM II AI Video](kavel/storm-ii-ai-video/PROMPTS.md) | `storm-ii-ai-video` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/storm-ii-ai-video) |
| [Smalltown Boy Dance Meme](kavel/smalltown-boy-dance-meme/PROMPTS.md) | `smalltown-boy-dance-meme` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/smalltown-boy-dance-meme) |
| [Smalltown Boy AI](kavel/smalltown-boy-ai/PROMPTS.md) | `smalltown-boy-ai` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/smalltown-boy-ai) |
| [Singing Pets AI Video](kavel/singing-pets-ai/PROMPTS.md) | `singing-pets-ai` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/singing-pets-ai) |
| [Shan Shen Bu](kavel/shan-shen-bu/PROMPTS.md) | `shan-shen-bu` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/shan-shen-bu) |
| [Ramalama Bang Bang Trend AI Video](kavel/ramalama-bang-bang-trend/PROMPTS.md) | `ramalama-bang-bang-trend` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/ramalama-bang-bang-trend) |
| [Raindance AI Trend](kavel/raindance-ai-trend/PROMPTS.md) | `raindance-ai-trend` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/raindance-ai-trend) |
| [Popstar AI Video](kavel/popstar-ai-video/PROMPTS.md) | `popstar-ai-video` | unknown | 2 | ✅ | [link](https://www.kavel.ai/video/popstar-ai-video) |
| [Plug Walk AI Filter](kavel/plug-walk-ai-filter/PROMPTS.md) | `plug-walk-ai-filter` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/plug-walk-ai-filter) |
| [Pet Memorial AI Video](kavel/pet-memorial-ai-video/PROMPTS.md) | `pet-memorial-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/pet-memorial-ai-video) |
| [Perdon AI Trend](kavel/perdon-ai-trend/PROMPTS.md) | `perdon-ai-trend` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/perdon-ai-trend) |
| [Patrick Swayze AI Dance](kavel/patrick-swayze-dance-ai-video/PROMPTS.md) | `patrick-swayze-dance-ai-video` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/patrick-swayze-dance-ai-video) |
| [Pata Chalega AI Video](kavel/pata-chalega-ai-video/PROMPTS.md) | `pata-chalega-ai-video` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/pata-chalega-ai-video) |
| [Paparazzi Red Carpet AI Video](kavel/paparazzi-red-carpet-ai-video/PROMPTS.md) | `paparazzi-red-carpet-ai-video` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/paparazzi-red-carpet-ai-video) |
| [Ozil Goal AI](kavel/ozil-goal-ai-video/PROMPTS.md) | `ozil-goal-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/ozil-goal-ai-video) |
| [Oouuh AI](kavel/oouuh-ai/PROMPTS.md) | `oouuh-ai` | unknown | 2 | ✅ | [link](https://www.kavel.ai/video/oouuh-ai) |
| [My Ride Is Here Broom Trend](kavel/my-ride-is-here-broom-trend/PROMPTS.md) | `my-ride-is-here-broom-trend` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/my-ride-is-here-broom-trend) |
| [LEGO Truck Wash AI Video](kavel/lego-truck-wash-ai-video/PROMPTS.md) | `lego-truck-wash-ai-video` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/lego-truck-wash-ai-video) |
| [Layoo AI Dance](kavel/layoo-ai-dance/PROMPTS.md) | `layoo-ai-dance` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/layoo-ai-dance) |
| [Lamine Yamal Rabona AI](kavel/lamine-yamal-rabona-ai/PROMPTS.md) | `lamine-yamal-rabona-ai` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/lamine-yamal-rabona-ai) |
| [La Calabaza Dance](kavel/la-calabaza-dance/PROMPTS.md) | `la-calabaza-dance` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/la-calabaza-dance) |
| [Knight Cat AI Video](kavel/knight-cat-ai-video/PROMPTS.md) | `knight-cat-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/knight-cat-ai-video) |
| [Keep On Steppin AI Dance](kavel/keep-on-steppin-ai-dance-video/PROMPTS.md) | `keep-on-steppin-ai-dance-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/keep-on-steppin-ai-dance-video) |
| [The Jawn Dance AI](kavel/jawn-dance-ai-video/PROMPTS.md) | `jawn-dance-ai-video` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/jawn-dance-ai-video) |
| [ILLIT You're Under Arrest AI Dance](kavel/illit-you-re-under-arrest-ai-dance/PROMPTS.md) | `illit-you-re-under-arrest-ai-dance` | unknown | 6 | ✅ | [link](https://www.kavel.ai/video/illit-you-re-under-arrest-ai-dance) |
| [I Feel Like Nicole AI](kavel/i-feel-like-nicole-ai-video/PROMPTS.md) | `i-feel-like-nicole-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/i-feel-like-nicole-ai-video) |
| [Hotel Lobby AI Video](kavel/hotel-lobby-ai-video/PROMPTS.md) | `hotel-lobby-ai-video` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/hotel-lobby-ai-video) |
| [Hit the Road Dude AI Video](kavel/hit-the-road-dude-ai-video/PROMPTS.md) | `hit-the-road-dude-ai-video` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/hit-the-road-dude-ai-video) |
| [Heavenly Reunion AI Video](kavel/heavenly-reunion-ai-video/PROMPTS.md) | `heavenly-reunion-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/heavenly-reunion-ai-video) |
| [Head Bop Animation](kavel/head-bop-animation/PROMPTS.md) | `head-bop-animation` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/head-bop-animation) |
| [Happy Friday I'm Onnat AI Video](kavel/happy-friday-im-onnat-ai-video/PROMPTS.md) | `happy-friday-im-onnat-ai-video` | unknown | 2 | ✅ | [link](https://www.kavel.ai/video/happy-friday-im-onnat-ai-video) |
| [Ghost Photoshoot Trend AI Video](kavel/ghost-photoshoot-trend/PROMPTS.md) | `ghost-photoshoot-trend` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/ghost-photoshoot-trend) |
| [Ghost Filter Prank AI](kavel/ghost-filter-prank-ai/PROMPTS.md) | `ghost-filter-prank-ai` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/ghost-filter-prank-ai) |
| [Genjutsu Video](kavel/genjutsu-video/PROMPTS.md) | `genjutsu-video` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/genjutsu-video) |
| [Gas Station Trend AI](kavel/gas-station-ai-video/PROMPTS.md) | `gas-station-ai-video` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/gas-station-ai-video) |
| [FNAF Jumpscare AI](kavel/fnaf-jumpscare-ai/PROMPTS.md) | `fnaf-jumpscare-ai` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/fnaf-jumpscare-ai) |
| [Flying Car AI Video](kavel/flying-car-ai-video/PROMPTS.md) | `flying-car-ai-video` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/flying-car-ai-video) |
| [Fergie Baby Harlem Walk AI](kavel/fergie-baby-harlem-walk-ai-video/PROMPTS.md) | `fergie-baby-harlem-walk-ai-video` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/fergie-baby-harlem-walk-ai-video) |
| [Enzo Fernandez Celebration AI](kavel/enzo-fernandez-celebration-ai-video/PROMPTS.md) | `enzo-fernandez-celebration-ai-video` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/enzo-fernandez-celebration-ai-video) |
| [Earth Zoom Out AI](kavel/earth-zoom-out-ai/PROMPTS.md) | `earth-zoom-out-ai` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/earth-zoom-out-ai) |
| [Dime Dime Baby AI Dance](kavel/dime-dime-baby-ai-dance/PROMPTS.md) | `dime-dime-baby-ai-dance` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/dime-dime-baby-ai-dance) |
| [Devil Wears Prada AI](kavel/devil-wears-prada-ai/PROMPTS.md) | `devil-wears-prada-ai` | unknown | 2 | ✅ | [link](https://www.kavel.ai/video/devil-wears-prada-ai) |
| [Damon Salvatore AI Video](kavel/damon-salvatore-ai-video/PROMPTS.md) | `damon-salvatore-ai-video` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/damon-salvatore-ai-video) |
| [Crazy Frog AI Video](kavel/crazy-frog-ai-video/PROMPTS.md) | `crazy-frog-ai-video` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/crazy-frog-ai-video) |
| [Corpse Bride AI](kavel/corpse-bride-ai/PROMPTS.md) | `corpse-bride-ai` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/corpse-bride-ai) |
| [Coldplay Kiss Cam Generator](kavel/coldplay-kiss-cam-generator/PROMPTS.md) | `coldplay-kiss-cam-generator` | unknown | 2 | ✅ | [link](https://www.kavel.ai/video/coldplay-kiss-cam-generator) |
| [Chinaza Dynamic Filter AI Video](kavel/chinaza-dynamic-filter-ai-video/PROMPTS.md) | `chinaza-dynamic-filter-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/chinaza-dynamic-filter-ai-video) |
| [ChatGPT Millionaire 30 Days AI Video](kavel/chatgpt-millionaire-30-days-ai-video/PROMPTS.md) | `chatgpt-millionaire-30-days-ai-video` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/chatgpt-millionaire-30-days-ai-video) |
| [Birthday Champagne AI Video](kavel/champagne-pop-birthday-ai-video/PROMPTS.md) | `champagne-pop-birthday-ai-video` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/champagne-pop-birthday-ai-video) |
| [Ceiling Fan Transition](kavel/ceiling-fan-transition/PROMPTS.md) | `ceiling-fan-transition` | unknown | 7 | ✅ | [link](https://www.kavel.ai/video/ceiling-fan-transition) |
| [Car Jump AI Video](kavel/car-jump-ai-video/PROMPTS.md) | `car-jump-ai-video` | unknown | 7 | ✅ | [link](https://www.kavel.ai/video/car-jump-ai-video) |
| [C-Walk AI Dance](kavel/c-walk-ai-dance/PROMPTS.md) | `c-walk-ai-dance` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/c-walk-ai-dance) |
| [Burning Bridges AI Video](kavel/burning-bridges-ai-video/PROMPTS.md) | `burning-bridges-ai-video` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/burning-bridges-ai-video) |
| [Bulin 47 AI Video](kavel/bulin-47-ai-video/PROMPTS.md) | `bulin-47-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/bulin-47-ai-video) |
| [Broccoli Throw Meme AI Video](kavel/broccoli-throw-ai-video/PROMPTS.md) | `broccoli-throw-ai-video` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/broccoli-throw-ai-video) |
| [Blocus Poursuite AI Video](kavel/blocus-poursuite-ai-video/PROMPTS.md) | `blocus-poursuite-ai-video` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/blocus-poursuite-ai-video) |
| [Black Friday Video Maker](kavel/black-friday-video-maker/PROMPTS.md) | `black-friday-video-maker` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/black-friday-video-maker) |
| [Barbie AI Dance](kavel/barbie-ai-dance/PROMPTS.md) | `barbie-ai-dance` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/barbie-ai-dance) |
| [Bama Bound Trend](kavel/bama-bound-trend/PROMPTS.md) | `bama-bound-trend` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/bama-bound-trend) |
| [Baile Charme Dance](kavel/baile-charme-dance/PROMPTS.md) | `baile-charme-dance` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/baile-charme-dance) |
| [Bad Times AI Trend Video](kavel/bad-times-ai-video/PROMPTS.md) | `bad-times-ai-video` | unknown | 4 | ✅ | [link](https://www.kavel.ai/video/bad-times-ai-video) |
| [Baby Dancing AI](kavel/baby-dancing-ai/PROMPTS.md) | `baby-dancing-ai` | unknown | 6 | ✅ | [link](https://www.kavel.ai/video/baby-dancing-ai) |
| [Alors on Danse AI](kavel/alors-on-danse-ai-meme/PROMPTS.md) | `alors-on-danse-ai-meme` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/alors-on-danse-ai-meme) |
| [Ali G Driving Scene](kavel/ali-g-driving-scene/PROMPTS.md) | `ali-g-driving-scene` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/ali-g-driving-scene) |
| [Airport Celebrity AI Video](kavel/airport-celebrity-ai-video/PROMPTS.md) | `airport-celebrity-ai-video` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/airport-celebrity-ai-video) |
| [AI Pet Dance Generator](kavel/ai-pet-dance-generator/PROMPTS.md) | `ai-pet-dance-generator` | unknown | 6 | ✅ | [link](https://www.kavel.ai/video/ai-pet-dance-generator) |
| [AI Mecha Transformation](kavel/ai-mecha-transformation/PROMPTS.md) | `ai-mecha-transformation` | unknown | 7 | ✅ | [link](https://www.kavel.ai/video/ai-mecha-transformation) |
| [AI Dunk Video](kavel/ai-dunk-video/PROMPTS.md) | `ai-dunk-video` | unknown | 1 | ✅ | [link](https://www.kavel.ai/video/ai-dunk-video) |
| [AI Crying Filter](kavel/ai-crying-filter/PROMPTS.md) | `ai-crying-filter` | unknown | 7 | ✅ | [link](https://www.kavel.ai/video/ai-crying-filter) |
| [AI Birthday Video Generator](kavel/ai-birthday-video-generator/PROMPTS.md) | `ai-birthday-video-generator` | unknown | 3 | ✅ | [link](https://www.kavel.ai/video/ai-birthday-video-generator) |
| [AI Arrest Filter](kavel/ai-arrest-filter/PROMPTS.md) | `ai-arrest-filter` | unknown | 7 | ✅ | [link](https://www.kavel.ai/video/ai-arrest-filter) |
| [Abra Kadabra AI Video](kavel/abra-kadabra-ai/PROMPTS.md) | `abra-kadabra-ai` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/abra-kadabra-ai) |
| [ABCDEFG I Need Money](kavel/abcdefg-i-need-money/PROMPTS.md) | `abcdefg-i-need-money` | unknown | 0 | ✅ | [link](https://www.kavel.ai/video/abcdefg-i-need-money) |
| [A2O LITE NEON Dance AI](kavel/a2o-lite-neon-dance/PROMPTS.md) | `a2o-lite-neon-dance` | unknown | 5 | ✅ | [link](https://www.kavel.ai/video/a2o-lite-neon-dance) |

## Attribution & license

Templates, prompts, and demo media remain copyright of their respective sites and creators:

- MakeViral — https://www.makeviral.ai
- Remake Your Meme — https://remakeyourmeme.com
- Media.io — https://www.media.io
- Kavel — https://www.kavel.ai

This repository is an **inventory / awesome-list** for discovery and research. Re-check each site’s terms before commercial reuse. Example people/pets in demos are described by the sources as AI-generated.

## Disclaimer

Prompts are copied verbatim from public pages — nothing invented. Remake Your Meme pages explicitly say there is no prompt to write; we do not fabricate prompts for those entries. Media.io / Kavel entries without a public prompt are marked accordingly.
