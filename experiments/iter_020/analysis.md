# iter_020 Analysis

## Objective

Determine whether the new `failed_breakdown_reclaim` edge belongs in the mixed high-beta basket, a semis-only basket, or the original fixed `NVDA/TSLA` basket.

## Sample Coverage

- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Key Rows

| Structure | Window | Return | Drawdown | Sharpe | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `NVDA/TSLA fixed BSL 240m` | `2025` | `7.982%` | `5.5%` | `0.034` | `14` |
| `Dynamic high-beta BSL 240m` | `2025` | `15.072%` | `6.6%` | `0.748` | `27` |
| `Failed breakdown mixed high-beta` | `2025` | `12.820%` | `1.3%` | `0.426` | `13` |
| `Failed breakdown semis-only` | `2025` | `14.506%` | `1.3%` | `0.557` | `15` |
| `NVDA/TSLA fixed BSL 240m` | `2026 YTD` | `3.443%` | `1.2%` | `1.849` | `4` |
| `Dynamic high-beta BSL 240m` | `2026 YTD` | `3.683%` | `3.3%` | `0.993` | `8` |
| `Failed breakdown mixed high-beta` | `2026 YTD` | `3.001%` | `1.4%` | `0.758` | `5` |
| `Failed breakdown semis-only` | `2026 YTD` | `3.404%` | `1.4%` | `0.939` | `4` |

## Useful

- `Failed breakdown semis-only` beat the mixed high-beta version in both windows. The edge did not come from forcing the setup back into `NVDA/TSLA`.
- The `2025` semis-only branch rotated across `TSM`, `AVGO`, `MU`, `MRVL`, `NVDA`, and `AMD`, so the result was not a disguised single-name win.
- `NVDA/TSLA` fixed aggressive BSL remained the main intraday control. The new branch did not displace it.

## Not Useful

- Fixed `NVDA/TSLA` `failed_breakdown_reclaim` was weak in both windows and should not be pursued.
- `ctx+ 1`, `90m hold`, and `strict breakdown buffer` did not produce a durable improvement over the base branch.
- The `strict breakdown buffer` matched the base branch in `2025` only because it barely changed the actual trade set, then failed in `2026 YTD`.

## Invalid

- `candidate_18` initially failed from a Docker container race. The rerun completed cleanly, so the round conclusions are valid.

## Next

- Add a hostile `2024` window before promoting the semis-only branch.
- Test only a few high-information semis-only knobs:
  - `selection_pool_size`
  - `context_require_above_open`
  - `gap_max`
  - stronger prior weakness
