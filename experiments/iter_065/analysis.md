# iter_065 Analysis

## Objective

Validate whether the new `growth4` premarket-quality selector is stable across `2024`, `2025`, and `2026 YTD`.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06`

## Window Table

| Window | Structure | Return | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: |
| `2024` | `old control` | `-0.623%` | `5.6%` | `18` |
| `2024` | `next-gen pool2` | `-0.581%` | `3.4%` | `12` |
| `2024` | `next-gen pool1` | `-0.001%` | `2.9%` | `11` |
| `2025` | `old control` | `8.448%` | `5.1%` | `32` |
| `2025` | `next-gen pool2` | `12.003%` | `3.6%` | `23` |
| `2025` | `next-gen pool1` | `10.991%` | `1.8%` | `19` |
| `2026 YTD` | `old control` | `4.873%` | `1.8%` | `7` |
| `2026 YTD` | `next-gen pool2` | `4.873%` | `1.8%` | `7` |
| `2026 YTD` | `next-gen pool1` | `4.346%` | `1.8%` | `6` |

## Selection Distribution

- `2024 next-gen pool2`: `TSLA 8`, `NVDA 8`, `META 4`, `AMZN 4`
- `2024 next-gen pool1`: `TSLA 8`, `NVDA 8`, `META 4`, `AMZN 2`
- `2025 next-gen pool2`: `AMZN 16`, `NVDA 14`, `META 10`, `TSLA 6`
- `2025 next-gen pool1`: `AMZN 16`, `NVDA 10`, `META 8`, `TSLA 4`
- `2026 YTD next-gen pool2`: `AMZN 8`, `TSLA 4`, `NVDA 2`
- `2026 YTD next-gen pool1`: `TSLA 6`, `AMZN 6`

## Useful

- The selector upgrade is real, but not in the way a naive broad-sample win would suggest.
- `2025` improved materially on both return and drawdown.
- `2024` did not become a positive edge, but the loss profile improved a lot.
- `2026 YTD` did not materially improve; the new selector mostly reproduced the old current-window traffic.

## Not Useful

- The new selector is not a clean all-weather promotion. It mostly improves `2025` and cleans up `2024`.
- `pool2` did not beat the old control in the current window that originally motivated the large-cap lane.
- `pool1` cut risk further, but gave up too much `2026 YTD` upside to become an automatic promotion.

## Conclusion

The new `growth4` selector is a better broad-sample large-cap branch, but it is still a current-plus-favorable-window large-cap lane, not a fully solved all-weather intraday strategy.

## Next

- Apply the same selector improvements to `failed_breakdown`.
- If they only help `hardware7`, treat the selector upgrade as family-specific rather than universal.
