# iter_021 Executive Report

## Decision

Keep semis-only `failed_breakdown_reclaim` as a shadow range-regime branch. It has real recent edge, but it failed the hostile `2024` window and does not deserve promotion into the frozen paper set.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Candidate | Window | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | `2024` | `24.375%` | `1.101` | `8.4%` | `0` |
| `Base semis failed breakdown` | `2025` | `14.506%` | `0.557` | `1.3%` | `15` |
| `Context above open` | `2025` | `14.004%` | `0.518` | `1.3%` | `14` |
| `Stronger weakness` | `2026 YTD` | `3.665%` | `1.055` | `1.2%` | `3` |
| `Base semis failed breakdown` | `2026 YTD` | `3.404%` | `0.939` | `1.4%` | `4` |
| `NVDA/TSLA fixed BSL 240m` | `2026 YTD` | `3.443%` | `1.849` | `1.2%` | `4` |

## Useful / Not Useful / Next

- Useful: the branch is real enough to keep as a future range-regime sleeve, especially around the simple semis-only base configuration.
- Not useful: there was no universal improvement knob. `pool 2`, `context above open`, `gap_max = 0.0`, and stronger-prior-weakness each failed at least one important window.
- Next: stop local threshold grinding on this branch and move the effort to regime routing, event filters, and premarket planning.
