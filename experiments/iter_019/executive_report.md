# iter_019 Executive Report

## Decision

Keep `QQQ/VOO/GLD dual_momentum 126/7` as the main daily control and `NVDA/TSLA` fixed aggressive BSL as the main intraday control. Promote `failed_breakdown_reclaim` only into a narrow branch study, not into the paper shortlist.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Candidate | Window | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | `2024` | `24.375%` | `1.101` | `8.4%` | `0` |
| `QQQ/VOO/GLD dual_momentum 126/7` | `2025` | `55.407%` | `2.134` | `7.1%` | `4` |
| `QQQ/VOO/GLD dual_momentum 126/7` | `2026 YTD` | `16.769%` | `2.578` | `14.1%` | `0` |
| `NVDA/TSLA fixed BSL 240m` | `2026 YTD` | `3.443%` | `1.849` | `1.2%` | `4` |
| `Dynamic high-beta BSL 240m` | `2025` | `15.072%` | `0.748` | `6.6%` | `27` |
| `Failed breakdown reclaim` | `2025` | `12.820%` | `0.426` | `1.3%` | `13` |

## Useful / Not Useful / Next

- Useful: `fixed BSL 240m` and `dynamic BSL 240m` both survived all three windows, and `failed_breakdown_reclaim` became the first new range-regime family with positive evidence in both `2025` and `2026 YTD`.
- Not useful: `dynamic BSL 120m`, `dynamic VWAP reclaim`, and `fixed BSL + daily_loss 0.75%` still looked too window-specific.
- Next: narrow the `failed_breakdown_reclaim` branch, especially around universe choice, before any promotion decision.
