# iter_019 Analysis

## Objective

Validate the surviving intraday branches across separate calendar windows before promoting any new range-regime idea toward the frozen paper shortlist.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Key Rows

| Structure | Window | Return | Drawdown | Sharpe | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | `2024` | `24.375%` | `8.4%` | `1.101` | `0` |
| `QQQ/VOO/GLD dual_momentum 126/7` | `2025` | `55.407%` | `7.1%` | `2.134` | `4` |
| `QQQ/VOO/GLD dual_momentum 126/7` | `2026 YTD` | `16.769%` | `14.1%` | `2.578` | `0` |
| `NVDA/TSLA fixed BSL 240m` | `2024` | `5.056%` | `4.2%` | `-0.407` | `12` |
| `NVDA/TSLA fixed BSL 240m` | `2025` | `7.982%` | `5.5%` | `0.034` | `14` |
| `NVDA/TSLA fixed BSL 240m` | `2026 YTD` | `3.443%` | `1.2%` | `1.849` | `4` |
| `Dynamic high-beta BSL 240m` | `2025` | `15.072%` | `6.6%` | `0.748` | `27` |
| `Dynamic high-beta BSL 240m` | `2026 YTD` | `3.683%` | `3.3%` | `0.993` | `8` |
| `Dynamic high-beta BSL 120m` | `2026 YTD` | `5.284%` | `3.3%` | `1.960` | `8` |
| `Dynamic VWAP reclaim 120m` | `2026 YTD` | `7.389%` | `1.5%` | `2.232` | `11` |
| `Failed breakdown reclaim` | `2025` | `12.820%` | `1.3%` | `0.426` | `13` |
| `Failed breakdown reclaim` | `2026 YTD` | `3.001%` | `1.4%` | `0.758` | `5` |

## Useful

- `NVDA/TSLA` fixed aggressive BSL remained the cleanest all-weather intraday control. It stayed positive in all three windows and kept the best drawdown behavior.
- `Dynamic high-beta BSL 240m` also stayed positive in all three windows. It remained the main aggressive dynamic control and was materially more robust than the `120m` version.
- `Failed breakdown reclaim` was the only fresh family with positive evidence in both `2025` and `2026 YTD`. That justified a dedicated branch study instead of immediate promotion.
- `QQQ/VOO/GLD dual_momentum 126/7` remained the main daily control. It dominated `2025` and `2026 YTD`, even though it lagged badly in `2024`.

## Not Useful

- `Fixed BSL + max_daily_loss 0.75%` did not improve broad robustness. It weakened `2024` and `2025`, and only looked cleaner in the short `2026` window.
- `Dynamic BSL 120m` was a `2026`-specific effect. It was negative in `2024` and nearly flat in `2025`.
- `Dynamic VWAP reclaim 120m` also looked regime-specific. It was strong in `2026 YTD` but clearly negative in `2025`.

## Invalid

- `candidate_19` initially failed from a Docker container race. The rerun completed cleanly, and the round should be judged from the rerun result.

## Next

- Keep the frozen paper shortlist unchanged.
- Run a narrow `failed_breakdown_reclaim` branch study on `2025` and `2026 YTD`.
- Do not spend more budget on `dynamic BSL 120m` or `dynamic VWAP reclaim` until they survive an earlier hostile window.
