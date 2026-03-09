# iter_027 Analysis

## Objective

Test whether the best `2026` large-cap variants from `iter_026` are real improvements or only recent-window noise.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Window | Structure | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `2024` | `base` | `0.397%` | `-0.953` | `5.4%` | `15` |
| `2024` | `hold120` | `-0.256%` | `-1.266` | `4.9%` | `15` |
| `2024` | `ctx2` | `-4.567%` | `-1.344` | `9.5%` | `18` |
| `2024` | `pool2` | `-0.623%` | `-1.245` | `5.6%` | `18` |
| `2025` | `base` | `3.361%` | `-0.558` | `6.7%` | `24` |
| `2025` | `hold120` | `2.344%` | `-0.754` | `6.4%` | `24` |
| `2025` | `ctx2` | `4.583%` | `-0.382` | `6.4%` | `26` |
| `2025` | `pool2` | `8.448%` | `0.078` | `5.1%` | `32` |
| `2026 YTD` | `base` | `4.346%` | `2.539` | `1.8%` | `6` |
| `2026 YTD` | `hold120` | `4.539%` | `2.546` | `1.1%` | `6` |
| `2026 YTD` | `ctx2` | `4.554%` | `2.687` | `1.8%` | `6` |
| `2026 YTD` | `pool2` | `4.873%` | `2.977` | `1.8%` | `7` |

## Selection Distribution

- `2024 pool2`: `TSLA 6`, `NVDA 6`, `AMZN 3`, `META 3`
- `2025 pool2`: `NVDA 11`, `TSLA 8`, `AMZN 7`, `META 6`
- `2026 pool2`: `AMZN 4`, `TSLA 2`, `NVDA 1`

## Useful

- `pool2` was the first large-cap variant with a real pattern: clearly better in `2025`, best again in `2026 YTD`, and more active than the base branch.
- `hold120` remained useful as a drawdown cleaner in `2026`.
- The large-cap current branch was now clearly a `growth4` branch led by `AMZN`, `TSLA`, and `NVDA`, not by the older core large-cap basket.

## Not Useful

- `pool2` did not solve the hostile `2024` window. It stayed negative there.
- `ctx2` was actively harmful in `2024`, so it failed as a robustness upgrade.
- `hold120` did not improve the full cross-window picture. It mostly moved the drawdown profile around.

## Next

- Stop treating large-cap `pool2` as a possible all-weather promotion candidate.
- Test whether a real `daily regime gate` can explain when the branch should be active.
- If that fails, move to a `family map` and eventually a `regime router` instead of more single-family micro-tuning.
