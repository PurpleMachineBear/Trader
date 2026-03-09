# iter_026 Analysis

## Objective

Exploit the `2026 YTD` large-cap `growth4` branch and test whether tighter current-regime tuning can improve the recent `AMZN/TSLA`-led BSL behavior.

## Sample Coverage

- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades |
| --- | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | `-2.057%` | `-1.326` | `3.3%` | `0` |
| `growth4 passive` | `-2.874%` | `-2.369` | `3.3%` | `0` |
| `growth4 base` | `4.346%` | `2.539` | `1.8%` | `6` |
| `growth4 above_open` | `4.490%` | `2.644` | `1.8%` | `6` |
| `growth4 hold120` | `4.539%` | `2.546` | `1.1%` | `6` |
| `growth4 ctx2` | `4.554%` | `2.687` | `1.8%` | `6` |
| `growth4 pool2` | `4.873%` | `2.977` | `1.8%` | `7` |

## Selection Distribution

- `base`, `above_open`, and `hold120` were effectively the same `AMZN/TSLA` traffic pattern.
- `pool2` was the first row that materially changed selection, adding a small `NVDA` contribution on top of the `AMZN/TSLA` core.

## Useful

- `pool2` was the first real incremental improvement over the base `growth4` branch in the current `2026` regime.
- `hold120` materially improved drawdown quality without destroying the branch. It is a valid conservative current-regime variant.
- The current `growth4` branch was already far better than both `VOO` and the growth4 passive basket in this short `2026` window.

## Not Useful

- `above_open` was only a cosmetic tweak. It changed almost nothing.
- `ctx2` and the `SPY/QQQ/XLK` context proxy behaved like aliases in this short window; they did not create clearly new evidence.
- Narrowing to `AMZN/TSLA` at this stage was not yet a proven improvement. The recent edge still looked like a `growth4` branch with concentrated actual traffic.

## Next

- Validate `pool2`, `hold120`, and the softer-context variants on `2024`, `2025`, and `2026 YTD`.
- Do not promote any `2026` large-cap row yet. This round only proved there is a recent-regime branch worth validating.
