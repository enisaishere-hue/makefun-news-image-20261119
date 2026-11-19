# One Day in the World — Thursday, 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/enisaishere-hue/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/enisaishere-hue/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-page newspaper poster summing up the world's news of Thursday
19 November 2026, drawn entirely in code.

## What is on the page

- **Hero — GTA VI launches worldwide.** Vice City opens: the game rolls out
  around the world from midnight local time, first reviews land at 99/100,
  and 2.3 million people watch on Twitch.
- **Trump, Xi and Putin hold first-ever trilateral talks** — APEC, Shenzhen;
  nuclear arms top the agenda, no deal expected.
- **World court delivers Rohingya genocide judgment** — The Gambia v. Myanmar
  at The Hague, a first for the court, seven years on.
- **Indonesia passes asset-forfeiture law** — corrupt assets can be seized
  without a conviction first.
- **Estonia to close border with Russia** — crossings shut from December after
  an arson attempt on a drone maker.
- **Ex-army chief asked to form government** — Herzog taps Eisenkot, passing
  over Netanyahu.
- **Gold sinks to $3,730 an ounce** — a 14-month low after Fed minutes point
  to more rate rises.
- **Also today:** four nations urge Gaza aid access; Prague rallies for press
  freedom; Spain's general strike; Cyclone Akvan nears Odisha; a US–Philippines
  $2bn loan; the EU proposes a €45bn Ukraine loan.

Every story was checked against a source dated 19 November 2026; the research
notes are in `news-brief.md` in the builder's workspace (not part of this repo).

## How it is made

`main.py` (Python 3.13, standard library + Pillow) draws the whole poster
with PIL primitives — gradient sky, skyline, palm silhouettes, panels and
typography. All text is drawn by PIL; no AI-generated text, no network, no
clock, no randomness. Two runs write byte-identical PNGs.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png — 1024×1024, under 1 MiB
```

## Entry

Built for the make.fun bounty
[news-image-20261119](https://make.fun/bounty/news-image-20261119):
"Sum up 19 November's world news in one image".
