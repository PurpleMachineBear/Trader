# Iter 086 Analysis

## Sample Coverage

- Cloud project: `Cloud_Earnings_Research`
- Recent broad window: `2025-01-02` to `2026-03-06`
- Earlier aggregate window: `2024-01-02` to `2025-12-31`
- Family under test: `platform5 pre1 hold3` with hard rolling symbol-quality floors

## Summary Table

| Candidate | Window | Structure | Return | Sharpe | Drawdown | Orders | Score |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_01` | `broad` | control `any` | `100.059%` | `1.508` | `10.1%` | `89` | `230.659` |
| `candidate_02` | `broad` | `any floor min1` | `76.840%` | `1.222` | `17.8%` | `58` | `163.440` |
| `candidate_03` | `broad` | control `required` | `75.473%` | `1.201` | `10.1%` | `76` | `175.373` |
| `candidate_04` | `broad` | `required floor min1` | `47.445%` | `0.796` | `17.1%` | `42` | `92.845` |
| `candidate_05` | `2024_2025` | control `any` | `93.491%` | `0.806` | `21.7%` | `153` | `130.691` |
| `candidate_06` | `2024_2025` | `any floor min1` | `45.217%` | `0.441` | `19.5%` | `46` | `50.317` |
| `candidate_07` | `2024_2025` | control `required` | `64.370%` | `0.590` | `19.5%` | `132` | `84.370` |
| `candidate_08` | `2024_2025` | `required floor min1` | `45.217%` | `0.441` | `19.5%` | `46` | `50.317` |

## Useful

- The round cleanly ruled out another selector-mechanics explanation.
- Hard `min1` quality floors materially damaged the canonical branch instead of cleaning it up.
  - broad control `any`: `100.059%`, DD `10.1%`
  - broad `any floor min1`: `76.840%`, DD `17.8%`
  - broad `required control`: `75.473%`, DD `10.1%`
  - broad `required floor min1`: `47.445%`, DD `17.1%`
- The same pattern held on `2024_2025`.
  - control `any`: `93.491%`
  - `any floor min1`: `45.217%`
  - control `required`: `64.370%`
  - `required floor min1`: `45.217%`

## Not Useful

- Hard rolling quality floors are not the right improvement tool for `platform5`.
- They cut turnover and trade count, but they do it by removing profitable event paths as well as weak ones.
- The identical `2024_2025` results for `any floor min1` and `required floor min1` show that the floor effectively collapsed both branches into the same reduced path.

## Interpretation

This round makes the cloud bottleneck clearer.

The branch is not mainly missing:

- a better report-time hold schedule
- a simple hard symbol-quality floor

Instead, the current evidence points to a richer metadata problem:

- the event edge depends on information that these coarse mechanics cannot isolate
- forcing the branch through a rolling quality gate removes too much of the useful covered-event path

## Next

- Keep `platform5 pre1 hold3` as the canonical cloud control.
- Stop near-term spending on more selector mechanics inside this cloud lane.
- If the cloud lane continues, the next work should be richer event metadata or event-state labels, not more hold or quality gating.
- The practical next integration step is to use the cloud lane as an event-quality reference and start mapping that state back into the intraday stack instead of continuing to tune the swing selector itself.
