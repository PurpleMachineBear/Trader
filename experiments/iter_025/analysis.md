# iter_025 Analysis

## Objective

Test whether `growth4 BSL + strict context` is a real all-weather large-cap intraday branch or only a recent-regime effect.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Window | Structure | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `2024` | `VOO buy-and-hold` | `24.375%` | `1.101` | `8.4%` | `0` |
| `2024` | `growth4 equal-weight passive` | `15.883%` | `0.483` | `10.3%` | `0` |
| `2024` | `core4 BSL control` | `-3.701%` | `-2.133` | `5.3%` | `7` |
| `2024` | `growth4 BSL + ctx+3 + 3m + 180m` | `0.397%` | `-0.953` | `5.4%` | `15` |
| `2025` | `VOO buy-and-hold` | `16.073%` | `0.437` | `19.0%` | `0` |
| `2025` | `growth4 equal-weight passive` | `4.432%` | `-0.159` | `13.0%` | `0` |
| `2025` | `core4 BSL control` | `4.739%` | `-0.482` | `3.1%` | `15` |
| `2025` | `growth4 BSL + ctx+3 + 3m + 180m` | `3.361%` | `-0.558` | `6.7%` | `24` |
| `2026 YTD` | `VOO buy-and-hold` | `-2.057%` | `-1.326` | `3.3%` | `0` |
| `2026 YTD` | `growth4 equal-weight passive` | `-2.874%` | `-2.369` | `3.3%` | `0` |
| `2026 YTD` | `core4 BSL control` | `0.574%` | `-2.637` | `1.3%` | `4` |
| `2026 YTD` | `growth4 BSL + ctx+3 + 3m + 180m` | `4.346%` | `2.539` | `1.8%` | `6` |

## Selection Distribution

- `2024 growth4 BSL`:
  - `NVDA 6`, `TSLA 5`, `META 3`, `AMZN 1`
- `2025 growth4 BSL`:
  - `TSLA 7`, `NVDA 6`, `AMZN 6`, `META 5`
- `2026 YTD growth4 BSL`:
  - `TSLA 3`, `AMZN 3`

## Useful

- `growth4 BSL + strict context` is real in the current `2026` regime. It beat both `VOO` and the growth4 passive basket in `2026 YTD` with low drawdown.
- `core4` control was also at least usable in `2025`, but still not strong enough to argue for all-weather promotion.
- The `2026 YTD` selection distribution simplified down to `TSLA` and `AMZN`, which is a useful clue that the current branch is not really a six-style mega-cap edge. It is a narrower recent-regime effect.

## Not Useful

- `growth4 BSL + strict context` is not an all-weather large-cap branch. It was only marginally positive in `2024` and underwhelming in `2025`.
- `core4` control was outright bad in `2024` and still not convincing in `2026 YTD`.
- Large-cap BSL as a broad all-weather replacement for the fixed high-beta sleeve is not supported by this validation.

## Next

- Pivot large-cap intraday work into `range-regime` research.
- Focus on `2026`-style choppy or risk-off windows rather than forcing a full-cycle all-weather thesis.
- Next round should test whether stronger regime gating, shorter holds, or open-strength filters can improve the current `growth4` branch without pretending it is a universal engine.
