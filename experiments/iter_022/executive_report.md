# iter_022 Executive Report

## Decision

Keep the current paper master unchanged. Start a separate high-risk daily branch around `TQQQ/VOO/GLD 126/7 1.0x` and `QLD/VOO/GLD 126/7`; do not mix that branch into the master portfolio yet.

## Sample Coverage

- Full sample: `2022-01-03` to `2026-03-06`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Candidate | Window | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `TQQQ/VOO/GLD 126/7 1.0x` | full sample | `411.121%` | `1.076` | `33.4%` | `10` |
| `TQQQ/QLD/GLD 126/7` | full sample | `387.941%` | `1.047` | `33.4%` | `10` |
| `QLD/VOO/GLD 126/7` | full sample | `275.104%` | `1.065` | `22.6%` | `14` |
| `TQQQ/VOO/GLD 126/7 0.75x` | full sample | `267.303%` | `0.952` | `27.9%` | `10` |
| `SSO/VOO/GLD 126/7` | `2025` | `30.461%` | `0.983` | `8.3%` | `6` |
| `QQQ/VOO/GLD 126/7` | full sample | `92.392%` | `0.682` | `13.9%` | `11` |

## Useful / Not Useful / Next

- Useful: `TQQQ/VOO/GLD` is still the raw-return king, while `QLD/VOO/GLD` is now the best leveraged compromise and `SSO/VOO/GLD` was the cleanest 2025 branch.
- Not useful: `QLD/SSO/GLD` did not beat `QLD/VOO/GLD`, and `TQQQ/QLD/GLD` did not beat the simpler `TQQQ/VOO/GLD` control.
- Next: run a follow-up leveraged validation round against passive `TQQQ`, `QLD`, and `SSO`, and judge the branch separately from the existing paper master.
