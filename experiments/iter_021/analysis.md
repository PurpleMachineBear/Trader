# iter_021 Analysis

## Objective

Test whether semis-only `failed_breakdown_reclaim` is a real all-weather branch or only a recent range-regime effect.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Semis Failed-Breakdown Table

| Structure | Window | Return | Drawdown | Sharpe | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `Base semis failed breakdown` | `2024` | `-1.353%` | `3.5%` | `-2.080` | `27` |
| `Pool 2 semis failed breakdown` | `2024` | `1.826%` | `2.5%` | `-1.058` | `31` |
| `Context above open` | `2024` | `-3.745%` | `4.2%` | `-4.147` | `21` |
| `Gap max = 0.0` | `2024` | `-0.163%` | `2.1%` | `-1.886` | `22` |
| `Stronger weakness` | `2024` | `-0.340%` | `2.6%` | `-1.938` | `21` |
| `Base semis failed breakdown` | `2025` | `14.506%` | `1.3%` | `0.557` | `15` |
| `Pool 2 semis failed breakdown` | `2025` | `12.353%` | `2.6%` | `0.384` | `19` |
| `Context above open` | `2025` | `14.004%` | `1.3%` | `0.518` | `14` |
| `Gap max = 0.0` | `2025` | `13.370%` | `2.3%` | `0.465` | `15` |
| `Stronger weakness` | `2025` | `11.049%` | `1.3%` | `0.291` | `11` |
| `Base semis failed breakdown` | `2026 YTD` | `3.404%` | `1.4%` | `0.939` | `4` |
| `Pool 2 semis failed breakdown` | `2026 YTD` | `3.104%` | `1.7%` | `0.801` | `4` |
| `Context above open` | `2026 YTD` | `2.751%` | `1.3%` | `0.761` | `4` |
| `Gap max = 0.0` | `2026 YTD` | `-1.700%` | `1.7%` | `-5.745` | `3` |
| `Stronger weakness` | `2026 YTD` | `3.665%` | `1.2%` | `1.055` | `3` |

## Useful

- `Semis-only failed_breakdown_reclaim` is a real recent branch. It remained strong in `2025` and positive in `2026 YTD`.
- No tested variant replaced the `2025` base branch. The cleanest `2025` result stayed the simple semis-only base configuration.
- `Stronger weakness` was the only tested knob that improved the short `2026` window, and it did so with even lower drawdown.
- Selection distribution mattered by window:
  - `2024` losers were dominated by `AMD` and `MU`
  - `2025` winners rotated across `TSM`, `MU`, `MRVL`, `NVDA`, `AMD`, and `AVGO`
  - `2026 YTD` winners concentrated mostly in `AMD` and `MU`

## Not Useful

- None of the semis-only variants survived `2024`. The branch is not all-weather.
- `selection_pool_size = 2` increased activity but did not improve robustness.
- `context_require_above_open = true` was not a universal cleanup filter.
- `gap_max = 0.0` was especially bad. It hurt `2025` and broke badly in `2026 YTD`.
- `Stronger weakness` improved only the short `2026` window and weakened the broader branch.

## Invalid

- None. All `24/24` candidates completed successfully.

## Next

- Keep semis-only `failed_breakdown_reclaim` as a `shadow` branch for future range-regime routing.
- Do not add it to the frozen paper shortlist.
- Shift the next research budget toward:
  - `Premarket Planning Engine`
  - `earnings/event regime`
  - a real intraday `regime router`
  - portfolio-level risk controls
