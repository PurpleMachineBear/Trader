# iter_071 Analysis

## Objective

Refine the first cloud earnings winner by testing whether the `platform7` edge is specifically a `pre1` effect, a wider pre-event accumulation effect, or a short-lived post-event carry effect.

## Sample Coverage

- `2025-01-02` to `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades |
| --- | ---: | ---: | ---: | ---: |
| `platform7 pre1 hold2` | `38.970%` | `0.641` | `19.3%` | `50` |
| `platform7 pre1 hold1` | `37.444%` | `0.648` | `13.7%` | `28` |
| `platform7 pre1 hold3` | `59.951%` | `0.935` | `18.1%` | `64` |
| `platform7 pre2 hold2` | `14.778%` | `0.281` | `9.9%` | `39` |
| `platform7 pre3 hold2` | `5.322%` | `0.012` | `14.3%` | `60` |
| `platform7 post1 hold2` | `-10.238%` | `-0.636` | `23.6%` | `53` |

## Comparison Against Existing Context

- Same-sample `VOO buy-and-hold` local reference: `14.463%`, `19.0%` drawdown
- Same-sample `platform7` passive baseline from local research: `-1.170%`, `14.3%` drawdown
- Same-sample best local non-event `platform7 BSL`: `-4.847%`, `5.3%` drawdown

## Selection Distribution

- `pre1 hold3`:
  - `ORCL +54628`, `MSFT +13298`, `CRM +11067`, `NOW +8415`, `AAPL -1396`, `ADBE -9492`, `NFLX -16436`
- `pre1 hold1`:
  - `ORCL +42679`, `MSFT +12593`, `NOW +7383`, `AAPL +794`, `CRM -4285`, `ADBE -8386`, `NFLX -13236`
- `pre2 hold2`:
  - `CRM +12428`, `MSFT +10064`, `ORCL +3348`, `NFLX +528`, `AAPL +48`, `NOW -2206`, `ADBE -9346`

## Useful

- `platform7 pre1 hold3` was the clear winner. It improved the original `pre1 hold2` control by more than `20` percentage points of return while slightly reducing drawdown.
- `platform7 pre1 hold1` was a valid conservative variant. It kept almost all of the return of the original control with a much lower drawdown.
- `pre2 hold2` was still positive, so the branch does not begin only on the final day, but it was much weaker than `pre1`.

## Not Useful

- `pre3 hold2` gave up most of the edge. A wide pre-event window diluted the branch materially.
- `post1 hold2` was negative. The branch is not a simple post-event carry basket.
- Profit concentration remained high. `ORCL` dominated the winner, while `NFLX` and `ADBE` were persistent drags.

## Conclusion

The `platform7` cloud branch is primarily an anticipation-led event strategy. The strongest version enters on `pre1` and can hold through the event window, but the edge is not broad across all platform names. The branch is now more clearly defined, but it still needs basket-quality work before it can be treated as a serious shadow candidate.

## Next

- Keep `platform7 pre1 hold3` as the cloud event-aware control.
- Test whether the branch improves when persistent drag symbols are removed.
- Do not promote any row into the frozen paper set. This remains a cloud-only exploratory lane.
