# iter_031 Executive Report

## Decision

Do not promote the large-cap router. The broad-sample improvement failed split-window validation.

## Sample Coverage

- `2024`
- `2025`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Window | Best Active Structure | Return | Drawdown | Decision |
| --- | --- | ---: | ---: | --- |
| `2024` | `router tech40 -> BSL exits` | `9.278%` | `2.5%` | Earlier-window improvement |
| `2025` | `BSL pool2` | `8.448%` | `5.1%` | Main active family |
| `2026 YTD` | `BSL pool2` | `4.873%` | `1.8%` | Current-window leader |

## Useful / Not Useful / Next

- Useful: the validation round showed exactly where the router helped and where it failed.
- Not useful: a routed row that goes flat or zero-trade in the current window is not deployable evidence.
- Next: keep the simpler `growth4 BSL pool2` as the canonical large-cap branch and test narrower current-regime baskets instead of more router grids.
