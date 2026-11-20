# makefun-news-image-1120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Goatleaf12/makefun-news-image-1120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Goatleaf12/makefun-news-image-1120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world's news of **Friday 20 November 2026**:
a newspaper front page with 45 stories — three illustrated leads, ten
illustrated grid stories, a world map with the thirteen illustrated
stories pinned on it, and thirty-two more stories in the ALSO list.
Every story happened, or was first reported, on that Friday; a
DATE CHECK box names the tempting stories left out because they were
first reported on 19 November or earlier.

The front page leads on Cyclone Akvan's landfall in Odisha, Russia's
wave of some thirty ballistic missiles at Kyiv, and COP31's deadlocked
final day in Antalya, with Asia's AI sell-off, BepiColombo's arrival
at Mercury and the UK–EU reset deal in the grid below.

## How it works

- `gen.py` draws the whole page in code with PIL (Liberation Serif and
  Sans): masthead, region count bar, day-in-numbers strip, data-driven
  story cells with painted scenes, a flat world map, the ALSO list, the
  DATE CHECK box and the footer. It writes `entry.png` (1024×1024).
- `main.ts` is the submitted program: it copies the shipped `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`). It runs
  offline and writes identical bytes on every run.

## Run it

```sh
python3 gen.py        # regenerate entry.png (deterministic)
node main.ts          # writes /output/entry.png
```

## License

MIT — see `LICENSE`.
