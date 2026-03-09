# iter_022 Analysis

## Objective

Keep the validated daily dual-momentum architecture fixed and test whether a leveraged beta ladder built from `TQQQ`, `QLD`, and `SSO` can produce a higher-risk branch that is cleaner than simply using `TQQQ` versus `VOO`.

## Sample Coverage

- Full sample: `2022-01-03` to `2026-03-06`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Important Data Fix

- The first `iter_022` pass exposed a stale local [tqqq factor file](/Users/chenchien/lean/data/equity/usa/factor_files/tqqq.csv) that started at `2025-06-01`. LEAN therefore adjusted `TQQQ` to a late starting date and made the first pass invalid for all `TQQQ` rows.
- `TQQQ` daily data was redownloaded from Polygon and the affected candidates were rerun. The results below reflect the corrected pass.

## Summary Table

| Structure | Window | Return | Drawdown | Sharpe | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | full sample | `40.361%` | `25.6%` | `0.160` | `0` |
| `QQQ/VOO/GLD 126/7` | full sample | `92.392%` | `13.9%` | `0.682` | `11` |
| `TQQQ/VOO/GLD 126/7 1.0x` | full sample | `411.121%` | `33.4%` | `1.076` | `10` |
| `TQQQ/VOO/GLD 126/7 0.75x` | full sample | `267.303%` | `27.9%` | `0.952` | `10` |
| `QLD/VOO/GLD 126/7` | full sample | `275.104%` | `22.6%` | `1.065` | `14` |
| `SSO/VOO/GLD 126/7` | full sample | `155.963%` | `20.7%` | `0.825` | `15` |
| `TQQQ/QLD/GLD 126/7` | full sample | `387.941%` | `33.4%` | `1.047` | `10` |
| `QLD/SSO/GLD 126/7` | full sample | `196.788%` | `23.2%` | `0.851` | `21` |
| `QQQ/VOO/GLD 126/7` | `2025` | `55.407%` | `7.1%` | `2.134` | `4` |
| `TQQQ/VOO/GLD 126/7 1.0x` | `2025` | `20.655%` | `23.0%` | `0.456` | `3` |
| `QLD/VOO/GLD 126/7` | `2025` | `24.142%` | `15.8%` | `0.623` | `6` |
| `SSO/VOO/GLD 126/7` | `2025` | `30.461%` | `8.3%` | `0.983` | `6` |
| all daily branches | `2026 YTD` | `16.769%` or `12.543%` | `14.1%` or `11.0%` | inflated | `0` |

## Useful

- `TQQQ/VOO/GLD 126/7 1.0x` remains the raw-return full-sample leader after the factor-file fix. It returned `411.121%` with `33.4%` drawdown.
- `QLD/VOO/GLD 126/7` is the new best leveraged compromise. It kept almost two-thirds of the `TQQQ` full-sample return while cutting drawdown from `33.4%` to `22.6%` and keeping similar Sharpe.
- `SSO/VOO/GLD 126/7` was the cleanest `2025` leveraged branch. It returned `30.461%` with only `8.3%` drawdown, beating the `TQQQ` rows on both return quality and drawdown in that window.
- `TQQQ/QLD/GLD` did not beat `TQQQ/VOO/GLD`. Replacing `VOO` with `QLD` inside the ladder preserved raw aggression but did not improve the broad full-sample result.

## Not Useful

- `QLD/SSO/GLD` was acceptable but still clearly behind `QLD/VOO/GLD` as a broad-sample leveraged compromise.
- `TQQQ/VOO/GLD 0.75x` is still a viable de-risked line, but it no longer looks like the best compromise once `QLD/VOO/GLD` is in the comparison set.
- `2026 YTD` did not differentiate the leveraged ladder. All unsized branches collapsed to the same defensive `GLD` outcome, so this short window should not drive ranking.

## Invalid Or Caution

- The first pass was invalid for all `TQQQ` rows because the local factor file started too late. The corrected rerun replaced those results.
- The `2026 YTD` rows are directionally useful only as a reminder that the whole family was in the same defensive state. They are not useful for choosing between `TQQQ`, `QLD`, and `SSO`.

## Next

- Keep the current paper master unchanged.
- Open a separate aggressive daily track with two leading candidates:
  - `TQQQ/VOO/GLD 126/7 1.0x` as the raw-return high-risk line
  - `QLD/VOO/GLD 126/7` as the cleaner leveraged compromise
- Next leveraged round should compare those two on separate calendar years and against passive `TQQQ`, `QLD`, and `SSO` buy-and-hold.
