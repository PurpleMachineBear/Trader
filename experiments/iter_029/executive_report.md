# iter_029 Executive Report

## Decision

Large-cap regime-awareness should be tested as `family routing`, not as more bullish gating on one family.

## Sample Coverage

- `2024`
- `2025`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Window | Best Active Family | Return | Drawdown | Decision |
| --- | --- | ---: | ---: | --- |
| `2024` | `failed_breakdown pool1` | `5.858%` | `2.5%` | Hostile-window family |
| `2025` | `BSL pool2` | `8.448%` | `5.1%` | Main active family |
| `2026 YTD` | `BSL pool2` | `4.873%` | `1.8%` | Main current-window family |

## Useful / Not Useful / Next

- Useful: `failed_breakdown` and `BSL` clearly map to different windows.
- Not useful: `VWAP reclaim` did not compete.
- Next: test a simple regime router and see whether the apparent family map survives when converted into one strategy.
