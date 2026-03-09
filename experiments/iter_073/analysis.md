# iter_073 Analysis

## Objective

Validate whether the narrower `platform5 pre1 hold3` cloud winner survives a simple window split before treating it as more than an in-sample cleanup of the broader `platform7` event branch.

## Sample Coverage

- `2025`
- `2026 YTD` through `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`

## Summary Table

| Structure | Window | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `platform7 pre1 hold3` | `2025` | `58.295%` | `1.068` | `18.1%` | `53` |
| `platform7 pre1 hold3` | `2026 YTD` | `5.078%` | `1.301` | `3.5%` | `2` |
| `platform5 pre1 hold3` | `2025` | `97.990%` | `1.757` | `10.0%` | `38` |
| `platform5 pre1 hold3` | `2026 YTD` | `5.078%` | `1.301` | `3.5%` | `2` |

## Selection Distribution

- `2025 platform7`:
  - `ORCL +54628`, `MSFT +17290`, `NOW +16601`, `CRM +3323`, `AAPL -7514`, `ADBE -9492`, `NFLX -16436`
- `2025 platform5`:
  - `ORCL +62958`, `MSFT +18626`, `NOW +18171`, `CRM +6882`, `AAPL -8560`
- `2026 YTD both rows`:
  - only `CRM +5084` on `2` closed trades

## Useful

- `platform5 pre1 hold3` remained materially stronger than `platform7 pre1 hold3` in `2025`.
- The narrower basket improved both return and drawdown in the only window with enough trades to say anything meaningful.
- The `2026 YTD` rows matched each other exactly, so the narrower basket did not damage the sparse recent window.

## Not Useful

- `2026 YTD` is too sparse to validate promotion. Both rows had only `2` trades and both were just `CRM`.
- This round did not answer whether the branch is robust before `2025`. It only answered the first anti-overfit question inside the current cloud sample.

## Conclusion

`platform5 pre1 hold3` is now the strongest cloud-only event-aware large-cap shadow branch. The improvement is not just a broad-sample accident because it clearly survives the `2025` split. But the recent `2026 YTD` evidence is too sparse to treat it as deployment-grade, and this branch still needs either earlier-window validation or a stronger event-history sample.

## Next

- Keep `platform5 pre1 hold3` as the current cloud event-aware leader.
- Do not promote it into the frozen paper set.
- If the cloud earnings history allows, extend validation earlier than `2025`.
- If not, treat it as a focused shadow branch and avoid further over-tuning until a richer event sample is available.
