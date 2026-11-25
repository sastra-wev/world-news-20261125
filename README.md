# world-news-20261125
[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/sastra-wev/world-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/sastra-wev/world-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

**The World in One Page** — the whole of Wednesday 25 November
2026's world news summed up in a single 1024×1024 newspaper front
page. The hero story is Washington's plan to unveil its Section 301
findings on alleged "excess capacity" in 16 major trading partners —
China, the European Union, India, Japan and Indonesia among them —
with new import duties expected on top of existing tariffs, drawn as
export crates halted at a customs wall under a falling Asia-market
line; alongside it, illustrated panels on the rescue race for
workers trapped 100 m down in a flooded unauthorised gold mine at
Pongkor, Bogor, and on Shenzhou-24 carrying Muhammad Zeeshan Ali,
the first Pakistani in space, to China's Tiangong station, briefs on
the Nvidia investigation, the Ukraine talks, Gaza, the Huawei
verdict and Australia's apology to LGBTQ veterans, and a "day in
numbers" strip.

The page is drawn programmatically with PIL (`render.py`) from the
day's verified reporting and committed as `entry.png`; `main.py`
copies that asset byte-for-byte to the output path, so the entry is
fully deterministic and needs nothing beyond the Python standard
library.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

To regenerate the artwork from source (requires Pillow):

```sh
python3 render.py # rewrites entry.png next to the script
```
