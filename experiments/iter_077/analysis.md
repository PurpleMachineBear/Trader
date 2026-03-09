# iter_077 Analysis

## Objective

Validate whether the cloud `platform5 pre1 hold3` event branch survives the earlier hostile window and an extended `2024_2025` sample before treating it as anything more than a recent-regime shadow lead.

## Sample Coverage

- Cloud project: `Cloud_Earnings_Research`
- Validation windows:
  - `2024-01-02` to `2024-12-31`
  - `2024-01-02` to `2025-12-31`

## Summary Table

| Structure | Window | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `platform7 pre1 hold3 any` | `2024` | `-23.061%` | `-0.459` | `33.9%` | `44` |
| `platform5 pre1 hold3 any` | `2024` | `10.449%` | `0.212` | `19.5%` | `34` |
| `platform7 pre1 hold3 any` | `2024_2025` | `7.756%` | `0.115` | `47.4%` | `106` |
| `platform5 pre1 hold3 any` | `2024_2025` | `93.491%` | `0.806` | `21.7%` | `83` |
| `platform7 pre1 hold3 after_close` | `2024` | `-23.061%` | `-0.459` | `33.9%` | `44` |
| `platform5 pre1 hold3 after_close` | `2024` | `10.449%` | `0.212` | `19.5%` | `34` |

## Selection Distribution

- `platform7 2024`:
  - `ORCL +9700`, `NOW +8099`, `CRM +855`
  - `AAPL -1425`, `NFLX -3123`, `MSFT -7053`, `ADBE -30032`
- `platform5 2024`:
  - `ORCL +11651`, `NOW +9641`
  - `CRM -301`, `AAPL -1851`, `MSFT -8619`
- `platform7 2024_2025`:
  - `ORCL +46853`, `NOW +14985`
  - `CRM +3111`, `MSFT +1930`
  - `AAPL -8182`, `NFLX -14284`, `ADBE -36476`
- `platform5 2024_2025`:
  - `ORCL +73152`, `NOW +21027`, `CRM +6438`, `MSFT +5621`
  - `AAPL -12571`

## Useful

- The hostile-window blocker is gone for `platform5`. It stayed positive in `2024` while the broader `platform7` control was decisively negative.
- The two-year `2024_2025` aggregate is also strong. `platform5` kept most of the `2025` strength even after adding the weaker `2024` year.
- `NFLX` and especially `ADBE` are now clearly confirmed as structural drags for this branch, not merely recent-sample noise.

## Not Useful

- `after_close` did not add anything in `2024`. The filtered and unfiltered rows were identical there, so report-time refinement was not the missing blocker for the early hostile window.
- `AAPL` remained a persistent drag even inside the winning `platform5` basket.
- `MSFT` was negative in `2024` and only modestly positive in `2024_2025`, so the winning basket still looks more like an `ORCL/NOW/CRM`-led branch than a broad platform basket.

## Conclusion

`platform5 pre1 hold3` is no longer just a `2025` artifact. It survived the hostile `2024` window and remained very strong across `2024_2025`, which materially upgrades confidence in the cloud event-aware branch. That said, it still does not qualify for frozen deployment promotion because the most recent `2026 YTD` validation remains too sparse. The branch is now a more serious cloud shadow candidate, not yet a paper candidate.

## Next

- Test whether the true habitat is narrower than `platform5`, especially an `enterprise software / workflow` subset such as `MSFT/CRM/NOW/ORCL` or `CRM/NOW/ORCL`.
- Keep `platform5 pre1 hold3` as the canonical cloud control for those narrower-basket tests.
- Do not spend near-term budget on more report-time micro-tuning; the earlier-window blocker was basket quality, not `after_close` filtering.
