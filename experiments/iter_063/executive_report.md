# iter_063 Executive Report

## Decision

The 30-round large-cap campaign is complete. No new all-weather large-cap intraday strategy was found.

## What Survived

- `growth4 BSL pool2` remains the canonical large-cap current-regime reference.
- `hardware7 failed_breakdown` is the only new large-cap shadow branch worth keeping.

## What Changed

- The campaign removed the remaining concern that prior large-cap scanner results were driven by symbol-order leakage.
- It also showed that most large-cap `BSL` basket expansion was negative value.
- The only real new branch came from changing `family`, not from changing `BSL` basket composition.

## Final Window Table

| Window | Winner | Return | Drawdown |
| --- | --- | ---: | ---: |
| `2024` | `growth4 failed_breakdown` | `5.858%` | `2.5%` |
| `2025` | `hardware7 failed_breakdown` | `15.598%` | `2.7%` |
| `2026 YTD` | `hardware7 failed_breakdown` | `1.581%` | `2.2%` |

## Recommendation

- Do not promote any large-cap branch into the frozen paper set.
- Keep `hardware7 failed_breakdown` as a shadow/regime branch only.
- Shift future large-cap research away from more basket swaps and toward event-aware ranking, context, and premarket selection design.
