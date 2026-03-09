# iter_029 Analysis

## Objective

Map large-cap `BSL`, `failed_breakdown`, and `VWAP reclaim` across `2024`, `2025`, and `2026 YTD` to see whether regime-awareness should come from family switching.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Window | Structure | Return | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: |
| `2024` | `BSL pool2` | `-0.623%` | `5.6%` | `18` |
| `2024` | `failed_breakdown pool1` | `5.858%` | `2.5%` | `12` |
| `2024` | `VWAP reclaim pool1` | `2.767%` | `5.2%` | `44` |
| `2025` | `BSL pool2` | `8.448%` | `5.1%` | `32` |
| `2025` | `failed_breakdown pool1` | `0.652%` | `2.6%` | `14` |
| `2025` | `VWAP reclaim pool1` | `-6.595%` | `7.1%` | `36` |
| `2026 YTD` | `BSL pool2` | `4.873%` | `1.8%` | `7` |
| `2026 YTD` | `failed_breakdown pool1` | `-2.099%` | `2.1%` | `4` |
| `2026 YTD` | `VWAP reclaim pool1` | `0.582%` | `2.7%` | `9` |

## Useful

- `failed_breakdown pool1` was clearly the best hostile-window large-cap family in `2024`.
- `BSL pool2` was clearly the best family in both `2025` and `2026 YTD`.
- This was the first clean evidence that large-cap regime-awareness might come from `switching families`, not from adding a bullish filter to one family.

## Not Useful

- `VWAP reclaim` remained the weakest of the three large-cap reversal families. It did not justify more equal-budget exploration.
- `failed_breakdown pool2` did not improve on `pool1`.
- No large-cap single family was all-weather.

## Next

- Test a simple `regime router`: send stronger tapes to `BSL`, weaker tapes to `failed_breakdown`.
- Treat `VWAP reclaim` as demoted in the large-cap lane unless another explanation appears.
