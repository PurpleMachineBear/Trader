# iter_024 Executive Report

## Decision

Do not widen the frozen paper track. Large-cap broad-sample intraday work still lags passive beta, but `growth4 BSL + strict context` is strong enough to deserve proper window validation.

## Sample Coverage

- Broad sample: `2024-01-02` to `2026-03-06`

## Summary Table

| Structure | Return | Drawdown | Trades | Decision |
| --- | ---: | ---: | ---: | --- |
| `VOO buy-and-hold` | `42.608%` | `18.8%` | `0` | Benchmark |
| `core4 equal-weight passive` | `21.588%` | `14.2%` | `0` | Basket baseline |
| `core4 BSL + QQQ/XLK + 5m + 150m` | `5.347%` | `6.2%` | `30` | Keep only as control |
| `growth4 BSL + ctx+3 + 3m + 180m` | `10.232%` | `6.1%` | `50` | Promote to window validation |
| `all6 mega-cap BSL + ctx+2 + 5m + 150m` | `4.924%` | `8.2%` | `53` | Do not promote |
| `all6 vwap_reclaim + ctx+2 + 120m` | `5.312%` | `14.2%` | `202` | Do not promote |

## Useful / Not Useful / Next

- Useful: `growth4 BSL + strict context` is the only large-cap dynamic branch that clearly separated itself from the rest of the active field.
- Not useful: Core4 context tweaks, mixed mega-cap baskets, and large-cap reclaim variants all failed to justify promotion on the broad sample.
- Next: validate `growth4 BSL + strict context` against `core4` control and same-basket passive baselines across `2024`, `2025`, and `2026 YTD`.
