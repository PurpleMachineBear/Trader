# iter_033 Executive Report

## Decision

Do not replace `growth4 BSL pool2` with a narrower `AMZN/TSLA` branch.

## Sample Coverage

- `2024`
- `2025`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Structure | `2024` | `2025` | `2026 YTD` | Decision |
| --- | ---: | ---: | ---: | --- |
| `growth4 BSL pool2 hold180` | `-0.623%` | `8.448%` | `4.873%` | Keep canonical |
| `AMZN/TSLA pool2 hold180` | `-4.019%` | `12.319%` | `4.781%` | Favorable-window alias only |
| `AMZN/TSLA pool2 hold120` | `-4.661%` | `7.946%` | `4.745%` | Conservative alias only |

## Useful / Not Useful / Next

- Useful: the narrowed basket did expose which names are carrying the large-cap lane in favorable conditions.
- Not useful: that narrower branch still failed the hostile earlier window and did not improve the current window.
- Next: keep the broader `growth4` control, demote the narrowed variants to alias status, and shift future effort toward event and premarket-aware selection rather than more watchlist narrowing.
