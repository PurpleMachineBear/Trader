# iter_020 Executive Report

## Decision

`Failed_breakdown_reclaim` should move to a semis-only shadow branch. It beat the mixed high-beta basket in both recent windows, but it still did not justify promotion past the fixed `NVDA/TSLA` BSL control.

## Sample Coverage

- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Candidate | Window | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `Dynamic high-beta BSL 240m` | `2025` | `15.072%` | `0.748` | `6.6%` | `27` |
| `Failed breakdown semis-only` | `2025` | `14.506%` | `0.557` | `1.3%` | `15` |
| `Failed breakdown mixed high-beta` | `2025` | `12.820%` | `0.426` | `1.3%` | `13` |
| `NVDA/TSLA fixed BSL 240m` | `2026 YTD` | `3.443%` | `1.849` | `1.2%` | `4` |
| `Failed breakdown semis-only` | `2026 YTD` | `3.404%` | `0.939` | `1.4%` | `4` |
| `Failed breakdown mixed high-beta` | `2026 YTD` | `3.001%` | `0.758` | `1.4%` | `5` |

## Useful / Not Useful / Next

- Useful: semis-only was cleaner than the mixed basket in both windows, and the branch traded a real semis basket rather than only one name.
- Not useful: fixed `NVDA/TSLA` `failed_breakdown_reclaim`, looser context, shorter hold, and stricter breakdown buffer.
- Next: test whether semis-only still survives an older hostile window before any paper-track discussion.
