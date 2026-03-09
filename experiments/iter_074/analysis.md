# iter_074 Analysis

## Objective

Test whether the cloud platform event branch is primarily a `report_time` effect by splitting the strongest `pre1` branch into `after_close` and `before_open` variants.

## Sample Coverage

- `2025-01-02` to `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades |
| --- | ---: | ---: | ---: | ---: |
| `platform5 pre1 hold3 any` | `100.059%` | `1.508` | `10.1%` | `49` |
| `platform5 pre1 hold3 after_close` | `82.585%` | `1.299` | `10.1%` | `44` |
| `platform5 pre1 hold3 before_open` | `18.988%` | `0.468` | `5.8%` | `4` |
| `platform7 pre1 hold3 after_close` | `62.278%` | `1.005` | `18.1%` | `57` |
| `platform7 pre1 hold3 before_open` | `7.285%` | `0.017` | `16.8%` | `6` |
| `platform5 pre1 hold1 after_close` | `64.113%` | `1.130` | `10.6%` | `19` |

## Selection Distribution

- `platform5 after_close hold3`:
  - `ORCL +57424`, `CRM +18620`, `MSFT +13986`, `AAPL -816`, `NOW -6522`
- `platform5 before_open hold3`:
  - `NOW +22833`, `CRM -3838`
- `platform7 after_close hold3`:
  - `ORCL +55429`, `CRM +15146`, `MSFT +15068`, `ADBE +16`, `AAPL -1395`, `NOW -5546`, `NFLX -16316`

## Useful

- `after_close` clearly carries most of the branch. It materially outperformed `before_open` in both `platform5` and `platform7`.
- `platform7 after_close` even beat the old unfiltered `platform7` control from `iter_071`, which means report-time filtering is a real improvement for the broader basket.
- `platform5 hold1 after_close` stayed strongly positive, so the branch does not require a long hold just to remain viable.

## Not Useful

- `before_open` was too sparse to be a primary branch. It produced very few trades and almost all of the positive contribution came from `NOW`.
- `after_close` alone did not beat the full `platform5 any` control. This means the branch is not purely after-close; a small amount of before-open contribution is still additive.

## Conclusion

The cloud platform event branch is mostly an `after_close` anticipation setup, but not exclusively. `after_close` captures most of the edge and improves the broader `platform7` basket, while `before_open` is sparse but directionally additive inside the narrower `platform5` basket. The next quality step should therefore be symbol-specific event quality, not another global report-time filter sweep.

## Next

- Keep `platform5 pre1 hold3 any` as the cloud event-aware lead.
- Treat `after_close` as the main structural clue for quality scoring.
- Build the next round around symbol-specific event quality rather than another basket-only or report-time-only tweak.
