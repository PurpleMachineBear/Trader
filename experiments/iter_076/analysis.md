# iter_076 Analysis

## Objective

Test whether a hard rolling quality floor can improve the broader `platform7` event branch by excluding symbols with persistently negative realized event edge.

## Sample Coverage

- `2025-01-02` to `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades |
| --- | ---: | ---: | ---: | ---: |
| `platform7 any baseline` | `59.951%` | `0.935` | `18.1%` | `64` |
| `platform7 any floor min1` | `61.007%` | `0.962` | `17.8%` | `35` |
| `platform7 any floor min2` | `44.471%` | `0.728` | `17.8%` | `46` |
| `platform7 after_close floor min1` | `45.450%` | `0.771` | `17.1%` | `31` |
| `platform7 after_close floor min2` | `46.126%` | `0.779` | `15.7%` | `41` |
| `platform5 any reference` | `100.059%` | `1.508` | `10.1%` | `49` |

## Selection Distribution

- `platform7 any floor min1`:
  - `ORCL +61190`, `MSFT +8861`, `NOW +8445`, `NFLX +196`, `CRM -3838`, `AAPL -4259`, `ADBE -9513`
- `platform7 any floor min2`:
  - `ORCL +49037`, `MSFT +12432`, `NOW +8958`, `NFLX +438`, `AAPL -6237`, `CRM -9484`, `ADBE -10581`
- `platform7 after_close floor min2`:
  - `ORCL +55429`, `MSFT +6913`, `NOW +2530`, `NFLX +822`, `ADBE -4674`, `AAPL -6323`, `CRM -8491`

## Useful

- A hard floor with `min1` did something real. It improved the broad `platform7 any` branch slightly and cut the number of trades almost in half.
- The result proves that symbol-specific quality can matter when it is applied as a gate instead of as a soft score.

## Not Useful

- The improvement was small. `61.007%` is only a marginal step up from `59.951%`.
- Waiting for `2` negative events before exclusion hurt the branch.
- The `after_close` floor variants were worse than the simpler `platform7 after_close` row from `iter_074`.
- None of these rows came close to the curated `platform5` reference.

## Conclusion

The rolling quality-floor idea is directionally valid but not powerful enough to replace curated basket quality. It can slightly clean up the broader `platform7` branch, but it does not close the gap to `platform5`, and it becomes worse when the gate waits longer to act. This suggests the next bottleneck is not another selection tweak. It is either richer event metadata or a longer event history to validate and stabilize symbol-quality estimates.

## Next

- Keep `platform5 pre1 hold3` as the cloud event-aware lead.
- Keep `platform7 any floor min1` only as a minor shadow variant, not as a promotion candidate.
- Stop spending near-term budget on more selector micro-tuning inside this cloud lane.
