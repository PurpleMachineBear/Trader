# iter_023 Analysis

## Objective

Validate the approved high-beta intraday universe on the longer `2024-01-02` to `2026-03-06` minute sample and decide whether any branch should replace `NVDA/TSLA` fixed aggressive BSL as the main all-weather intraday sleeve.

## Sample Coverage

- Broad sample: `2024-01-02` to `2026-03-06`
- Validation windows:
  - `2024-01-02` to `2024-12-31`
  - `2025-01-02` to `2025-12-31`
  - `2026-01-02` to `2026-03-06` (`YTD`)
- Approved minute universe:
  - `NVDA`, `TSLA`, `AMD`, `AVGO`, `MU`, `TSM`, `MRVL`
  - context ETFs: `QQQ`, `SMH`

## Summary Table

| Structure | Window | Return | Sharpe | Drawdown | Orders |
| --- | --- | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | broad | `42.608%` | `0.574` | `18.8%` | `1` |
| `fixed NVDA/TSLA aggressive BSL` | broad | `20.995%` | `0.145` | `5.8%` | `310` |
| `fixed NVDA/TSLA aggressive BSL + daily_loss 0.75%` | broad | `12.948%` | `-0.236` | `5.4%` | `310` |
| `dynamic high-beta BSL 240m` | broad | `24.695%` | `0.273` | `7.3%` | `852` |
| `dynamic high-beta BSL 120m` | broad | `0.191%` | `-0.853` | `10.4%` | `134` |
| `semis failed_breakdown_reclaim` | broad | `19.632%` | `0.086` | `4.0%` | `98` |
| `VOO buy-and-hold` | `2024` | `24.375%` | `1.101` | `8.4%` | `1` |
| `fixed NVDA/TSLA aggressive BSL` | `2024` | `5.056%` | `-0.407` | `4.2%` | `264` |
| `dynamic high-beta BSL 120m` | `2024` | `-5.057%` | `-1.851` | `9.5%` | `54` |
| `semis failed_breakdown_reclaim` | `2024` | `-1.353%` | `-2.080` | `3.5%` | `54` |
| `VOO buy-and-hold` | `2025` | `16.073%` | `0.437` | `19.0%` | `1` |
| `fixed NVDA/TSLA aggressive BSL` | `2025` | `7.982%` | `0.034` | `5.5%` | `28` |
| `semis failed_breakdown_reclaim` | `2025` | `14.506%` | `0.557` | `1.3%` | `30` |
| `VOO buy-and-hold` | `2026 YTD` | `-2.057%` | `-1.326` | `3.3%` | `1` |
| `fixed NVDA/TSLA aggressive BSL` | `2026 YTD` | `3.443%` | `1.849` | `1.2%` | `8` |
| `dynamic high-beta BSL 120m` | `2026 YTD` | `5.284%` | `1.960` | `3.3%` | `16` |
| `semis failed_breakdown_reclaim` | `2026 YTD` | `3.404%` | `0.939` | `1.4%` | `8` |

## Stability Table

| Structure | Broad | `2024` | `2025` | `2026 YTD` | Judgment |
| --- | ---: | ---: | ---: | ---: | --- |
| `fixed NVDA/TSLA aggressive BSL` | `20.995%` | `5.056%` | `7.982%` | `3.443%` | Main all-weather intraday control |
| `fixed BSL + daily_loss 0.75%` | `12.948%` | `-1.322%` | `5.131%` | `3.000%` | Not a universal upgrade |
| `dynamic high-beta BSL 120m` | `0.191%` | `-5.057%` | `0.486%` | `5.284%` | Recent-regime only |
| `semis failed_breakdown_reclaim` | `19.632%` | `-1.353%` | `14.506%` | `3.404%` | Real shadow branch, not all-weather |

## Selection Distribution

- `dynamic high-beta BSL 240m` broad sample:
  - `AMD 18`, `TSLA 16`, `MU 11`, `NVDA 10`, `AVGO 6`, `MRVL 3`, `TSM 2`
- `semis failed_breakdown_reclaim` broad sample:
  - `AMD 19`, `MU 11`, `MRVL 7`, `NVDA 5`, `TSM 4`, `AVGO 3`
- `dynamic high-beta BSL 120m` `2026 YTD`:
  - `AMD 3`, `AVGO 2`, `TSLA 2`, `MRVL 1`
- `semis failed_breakdown_reclaim` `2026 YTD`:
  - `AMD 2`, `NVDA 1`, `MU 1`

## Useful

- Extending minute history to `2024-01-02` materially improved evidence quality. The approved high-beta intraday basket now has a real hostile historical window instead of only `2025+` evidence.
- `fixed NVDA/TSLA aggressive BSL` stayed positive in `2024`, `2025`, and `2026 YTD`. It remains the best all-weather intraday control even though it is not the raw-return leader versus `VOO`.
- `semis failed_breakdown_reclaim` is a real branch, not a one-symbol illusion. It was strong in `2025`, remained positive in `2026 YTD`, and rotated through multiple semis names.
- The broad `dynamic high-beta BSL 240m` row still looks directionally useful. It produced a real multi-symbol rotation instead of collapsing back to only `NVDA/TSLA`.

## Not Useful

- `fixed NVDA/TSLA aggressive BSL + daily_loss 0.75%` did not generalize. It reduced risk a little, but broad return fell sharply and `2024` turned negative.
- `dynamic high-beta BSL 120m` still behaves like a recent-regime branch, not a deployable all-weather engine. It was negative in `2024`, nearly flat in `2025`, and only clearly strong in `2026 YTD`.
- `semis failed_breakdown_reclaim` does not pass all-weather promotion because the hostile `2024` window was still negative.

## Invalid Or Caution

- Intraday order fills still rely on TradeBar fills because quote data is not available in this local setup. That is acceptable for research, but it limits execution realism.
- `dynamic high-beta BSL 240m` was only tested as a broad-sample row in this round. It should not be promoted from the broad result alone without its own explicit `2024/2025/2026` stability split and churn review.

## Next

- Keep the paper master unchanged.
- Keep `fixed NVDA/TSLA aggressive BSL` as the frozen main intraday sleeve.
- Keep `semis failed_breakdown_reclaim` as a `range-regime shadow branch`.
- Do not promote `dynamic high-beta BSL 120m`.
- Next useful intraday question is not another local threshold sweep. It is either:
  - a dedicated stability plus order-churn review for `dynamic high-beta BSL 240m`, or
  - a regime router and event layer that explains when to turn on `semis failed_breakdown_reclaim`.
