# Iter 085 Analysis

## Sample Coverage

- Cloud project: `Cloud_Earnings_Research`
- Recent broad window: `2025-01-02` to `2026-03-06`
- Earlier aggregate window: `2024-01-02` to `2025-12-31`
- Family under test: `platform5 pre1` with report-time-conditioned hold rules

## Summary Table

| Candidate | Window | Structure | Return | Sharpe | Drawdown | Orders | Score |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_01` | `broad` | control `hold3` | `100.059%` | `1.508` | `10.1%` | `89` | `230.659` |
| `candidate_02` | `broad` | `bmo1 amc3` | `86.178%` | `1.337` | `10.1%` | `85` | `199.678` |
| `candidate_03` | `broad` | `bmo2 amc3` | `93.841%` | `1.429` | `10.1%` | `88` | `216.541` |
| `candidate_04` | `broad` | `bmo1 amc2` | `80.468%` | `1.288` | `9.8%` | `75` | `189.468` |
| `candidate_05` | `2024_2025` | control `hold3` | `93.491%` | `0.806` | `21.7%` | `153` | `130.691` |
| `candidate_06` | `2024_2025` | `bmo1 amc3` | `80.162%` | `0.712` | `21.3%` | `150` | `108.762` |
| `candidate_07` | `2024_2025` | `bmo2 amc3` | `87.412%` | `0.763` | `21.9%` | `151` | `119.912` |
| `candidate_08` | `2024_2025` | `bmo1 amc2` | `63.040%` | `0.582` | `24.0%` | `134` | `73.240` |

## Useful

- The canonical fixed `hold3` control remained the winner in both windows.
- The best conditional variant in both windows was `bmo2 amc3`, which means `before_open` events are not obviously one-day-only.
  - broad: control `100.059%` vs `bmo2 amc3` `93.841%`
  - `2024_2025`: control `93.491%` vs `bmo2 amc3` `87.412%`
- Shortening only the `after_close` side was clearly harmful.
  - broad `bmo1 amc2`: `80.468%`
  - `2024_2025` `bmo1 amc2`: `63.040%`

## Not Useful

- Report-time-conditioned holding did not improve the canonical branch in either window.
- The whole family of tested variants underperformed the fixed `hold3` control.
- This means the event-state bottleneck is not a simple mismatch between `before_open` and `after_close` holding periods.

## Interpretation

This round rules out another plausible but still coarse explanation:

- the cloud branch is not mainly underperforming because it holds `before_open` and `after_close` events for the same number of days
- mild shortening of `before_open` events reduced performance
- shortening `after_close` events was worse still

So the next useful work should return to richer event-quality metadata, not more hold-schedule tuning.

## Next

- Keep `platform5 pre1 hold3` as the canonical cloud control.
- Stop spending near-term budget on report-time-conditioned hold micro-tuning unless new metadata later suggests a more specific interaction.
- Move next to `platform5` quality gating inside the canonical branch, especially around the covered-event subset.
