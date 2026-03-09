# iter_031 Analysis

## Objective

Validate the broad-sample router winners from `iter_030` across `2024`, `2025`, and `2026 YTD`.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Window | Structure | Return | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: |
| `2024` | `BSL pool2` | `-0.623%` | `5.6%` | `18` |
| `2024` | `failed_breakdown pool1` | `5.858%` | `2.5%` | `12` |
| `2024` | `router tech40 -> BSL exits` | `9.278%` | `2.5%` | `8` |
| `2024` | `router spy/qqq/xlk20 -> BSL exits` | `7.155%` | `2.5%` | `11` |
| `2025` | `BSL pool2` | `8.448%` | `5.1%` | `32` |
| `2025` | `failed_breakdown pool1` | `0.652%` | `2.6%` | `14` |
| `2025` | `router tech40 -> BSL exits` | `0.894%` | `1.2%` | `9` |
| `2025` | `router spy/qqq/xlk20 -> BSL exits` | `5.184%` | `2.1%` | `11` |
| `2026 YTD` | `BSL pool2` | `4.873%` | `1.8%` | `7` |
| `2026 YTD` | `failed_breakdown pool1` | `-2.099%` | `2.1%` | `4` |
| `2026 YTD` | `router tech40 -> BSL exits` | `0.000%` | `0.0%` | `0` |
| `2026 YTD` | `router spy/qqq/xlk20 -> BSL exits` | `0.145%` | `1.6%` | `5` |

## Useful

- The router hypothesis was directionally right in one sense: different families do map to different windows.
- `tech40 -> BSL exits` was strong in hostile `2024`, which means the broad-sample `iter_030` win was not random.
- `spy/qqq/xlk20 -> BSL exits` was less extreme than `tech40` and stayed alive in both `2024` and `2025`.

## Not Useful

- The best broad-sample router did not survive the current window. `tech40 -> BSL exits` went to zero trades in `2026 YTD`.
- The broader-proxy router still lagged the base `BSL pool2` in the window that currently matters most.
- No routed branch improved all three windows relative to the existing family references.

## Conclusion

The router win from `iter_030` was real but not stable enough for promotion. It improved earlier windows by giving up too much of the current regime.

## Next

- Keep `growth4 BSL pool2` as the large-cap current-regime reference.
- Stop spending budget on this simple router unless a richer event or premarket layer can explain when routing should change.
- Test whether the current large-cap lane can be improved by narrowing around the names it is actually selecting now.
