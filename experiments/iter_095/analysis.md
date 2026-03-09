# Iteration 095 Analysis

## Sample Coverage

- Hostile window: `2024-01-02` to `2024-12-31`
- Positive window: `2025-01-02` to `2025-12-31`
- Sparse current window: `2026-01-02` to `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`

## Decision

Do not promote the event sleeve into the frozen production master.

The event sleeve is now much better understood:

- `2024`: mostly neutral to slightly worse on return, sometimes cleaner on drawdown
- `2025`: clearly additive
- `2026 YTD`: lower return than control, even if drawdown improves

So this is not an all-weather upgrade. It is a positive-window additive sleeve.

## Summary Table

| Window | Structure | Return | Sharpe | Drawdown | Orders |
| --- | --- | ---: | ---: | ---: | ---: |
| `2024` | `control` | `15.729%` | `0.587` | `6.1%` | `299` |
| `2024` | `platform5 sleeve 10%` | `15.614%` | `0.602` | `5.5%` | `345` |
| `2024` | `platform5 sleeve 15%` | `15.785%` | `0.610` | `6.2%` | `348` |
| `2024` | `enterprise4 sleeve 10%` | `14.672%` | `0.537` | `5.5%` | `330` |
| `2025` | `control` | `37.045%` | `1.749` | `5.4%` | `43` |
| `2025` | `platform5 sleeve 10%` | `39.573%` | `2.035` | `4.8%` | `96` |
| `2025` | `platform5 sleeve 15%` | `40.467%` | `2.090` | `4.4%` | `99` |
| `2025` | `enterprise4 sleeve 10%` | `40.771%` | `2.112` | `4.7%` | `79` |
| `2026 YTD` | `control` | `15.204%` | `2.791` | `10.8%` | `11` |
| `2026 YTD` | `platform5 sleeve 10%` | `14.112%` | `2.830` | `9.8%` | `26` |
| `2026 YTD` | `platform5 sleeve 15%` | `13.577%` | `2.857` | `9.4%` | `27` |
| `2026 YTD` | `enterprise4 sleeve 10%` | `13.430%` | `2.639` | `10.4%` | `22` |

## Stability Table

| Structure | `2024` Return | `2025` Return | `2026 YTD` Return | Verdict |
| --- | ---: | ---: | ---: | --- |
| `control` | `15.729%` | `37.045%` | `15.204%` | canonical master control |
| `platform5 sleeve 10%` | `15.614%` | `39.573%` | `14.112%` | positive-window additive, not all-weather |
| `platform5 sleeve 15%` | `15.785%` | `40.467%` | `13.577%` | strongest `2025`, weaker current window |
| `enterprise4 sleeve 10%` | `14.672%` | `40.771%` | `13.430%` | clean positive-window alias only |

## Useful

- The split windows gave a decisive classification:
  - event sleeve helps `2025`
  - does not improve `2026 YTD`
  - is only neutral in `2024`
- `platform5 15%` is the strongest positive-window variant.
- `enterprise4 10%` is a clean `2025` alias, not a universal improvement.

## Not Useful

- Promoting the event sleeve off aggregate windows alone would have been premature.
- `2026 YTD` Sharpe is too short-window inflated to justify promotion.

## Invalid

- None.

## Next

- Keep the production master unchanged.
- Reclassify the event sleeve as a `positive-window shadow sleeve`.
- If revisited, research should focus on detecting the positive event regime rather than forcing the sleeve into all windows.
