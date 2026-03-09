# iter_023 Executive Report

## Decision

Keep the frozen paper master unchanged. The longer `2024-2026` minute validation did not dethrone `NVDA/TSLA` fixed aggressive BSL as the main intraday sleeve.

## Sample Coverage

- Broad sample: `2024-01-02` to `2026-03-06`
- Validation windows:
  - `2024`
  - `2025`
  - `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Structure | Window | Return | Sharpe | Drawdown | Orders |
| --- | --- | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | broad | `42.608%` | `0.574` | `18.8%` | `1` |
| `fixed NVDA/TSLA aggressive BSL` | broad | `20.995%` | `0.145` | `5.8%` | `310` |
| `dynamic high-beta BSL 240m` | broad | `24.695%` | `0.273` | `7.3%` | `852` |
| `semis failed_breakdown_reclaim` | broad | `19.632%` | `0.086` | `4.0%` | `98` |
| `fixed NVDA/TSLA aggressive BSL` | `2024` | `5.056%` | `-0.407` | `4.2%` | `264` |
| `semis failed_breakdown_reclaim` | `2025` | `14.506%` | `0.557` | `1.3%` | `30` |
| `fixed NVDA/TSLA aggressive BSL` | `2026 YTD` | `3.443%` | `1.849` | `1.2%` | `8` |
| `dynamic high-beta BSL 120m` | `2026 YTD` | `5.284%` | `1.960` | `3.3%` | `16` |

## Useful / Not Useful / Next

- Useful: `fixed NVDA/TSLA aggressive BSL` is still the only intraday branch that stayed positive across `2024`, `2025`, and `2026 YTD`. `semis failed_breakdown_reclaim` is real, but only as a regime-specific shadow branch.
- Not useful: `fixed BSL + daily_loss 0.75%` is not a universal improvement, and `dynamic high-beta BSL 120m` is still too recent-regime-specific for promotion.
- Next: keep the frozen paper master unchanged, keep `semis failed_breakdown_reclaim` in shadow, and spend the next intraday research budget on either `dynamic BSL 240m` stability plus churn review or on a regime router that decides when to activate the semis failed-breakdown branch.
