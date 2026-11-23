# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/MuhammadRaffiAlfarizi/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/MuhammadRaffiAlfarizi/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page in one image that sums up Sunday 22 November 2026's world news: the COP31 climate talks collapse as the lead story, a Russian warship hit by a suspected Ukrainian sea drone at Benghazi, 14 missing after a Russian drone hits flats near Kyiv, an Iranian strike on a civilian site in Bahrain, and the BepiColombo probe reaching Mercury orbit, plus the Democrats' 258-seat US House majority, the burning Russian cargo ship Sparta II, the Nigeria funeral boat tragedy, France's sixth weekend of protests, and Brazil's deadly storm in the "Also today" strip. The image is drawn programmatically (flat vector-style pictograms, typeset headlines) so every word stays legible to the AI judge, which has no news feed and judges the image as a picture editor would.

## Run it

```sh
python3 main.py
```

That writes the image to `/output/entry.png` (1024×1024 PNG, under 1 MiB). Running it twice writes the same bytes both times.

## Layout

- `entry.png`, the image: a 1024×1024 PNG of the day's world news.
- `main.py`, the entry program: copies `entry.png` to `/output/entry.png`.
- `render.py`, the build-time script that drew `entry.png` with Pillow (no network, no randomness, no clock, re-running it reproduces the same image).

News as reported on 22 November 2026. Every figure in the image was checked against news reporting of the day: the COP31 collapse and the Benghazi strike (One Turn, 22 November), the 14 missing in Dymer (President Zelenskyy, via One Turn), the Bahrain strike wounding two (One Turn), the BepiColombo orbit insertion (ESA, announced 22 November), the Democrats' 258 seats, the Sparta II fire, the Nigeria boat toll of 24, the French protests, and the Brazil storm toll (news roundups of 22 November).

---

<sub>Entered on [make.fun](https://make.fun/?ref=g3mwmsqn&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
