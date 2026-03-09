# iter_030 Analysis

## Objective

Test whether a simple large-cap `regime router` can beat the single-family controls by sending stronger tapes to `BSL` and weaker tapes to `failed_breakdown`.

## Sample Coverage

- `2024-01-02` to `2026-03-06`

## Summary Table

| Structure | Return | Drawdown | Trades | Comment |
| --- | ---: | ---: | ---: | --- |
| `VOO buy-and-hold` | `42.608%` | `18.8%` | `0` | Benchmark |
| `growth4 passive` | `15.172%` | `20.9%` | `0` | Same-basket passive beta |
| `growth4 BSL pool2` | `13.685%` | `5.6%` | `63` | Best prior active control |
| `growth4 failed_breakdown pool1` | `3.821%` | `2.6%` | `31` | Hostile-window control |
| `router tech40 -> BSL exits` | `16.757%` | `2.3%` | `30` | Best routed row |
| `router spy/qqq/xlk20 -> BSL exits` | `14.828%` | `2.3%` | `30` | Second-best routed row |
| `router tech20 -> BSL exits` | `12.667%` | `2.3%` | `31` | Better drawdown, weaker return |
| `router tech20 -> failed exits` | `2.831%` | `6.5%` | `30` | Poor exit mapping |
| `router tech40 -> failed exits` | `0.540%` | `7.9%` | `29` | Clearly weak |

## Useful

- A simple router did improve the broad-sample large-cap active lane relative to the single-family controls.
- The best routed row, `tech40 -> BSL exits`, beat `growth4 BSL pool2` on both return and drawdown.
- The broad-proxy router `SPY/QQQ/XLK 20d` also worked well enough to justify validation.
- The router only looked attractive when the exit profile stayed `BSL-style`. Failed-breakdown-style exits did not transfer into a better combined strategy.

## Not Useful

- No routed row beat `VOO buy-and-hold` on raw return.
- Routing into `failed_breakdown` exits was clearly the wrong implementation path.
- The result still might be cosmetic if the router only helped one subwindow, so this round alone was not enough for promotion.

## Next

- Validate the best routed rows across `2024`, `2025`, and `2026 YTD`.
- Treat zero-trade or near-zero-trade routed windows as informative failures, not neutral rows.
