# iter_092 analysis

## Sample Coverage

- recent broad: `2025-01-02` to `2026-03-06`
- earlier validation: `2024-01-02` to `2025-12-31`
- cloud project: `Cloud_Earnings_Research`

## Summary Table

| candidate | structure | window | return | sharpe | drawdown | orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| candidate_01 | `control rr2.0 hold240` | broad | `3.246%` | `-2.053` | `0.4%` | `10` |
| candidate_02 | `rr2.0 hold120` | broad | `2.525%` | `-2.946` | `0.2%` | `10` |
| candidate_03 | `rr1.5 hold240` | broad | `2.701%` | `-2.866` | `0.4%` | `10` |
| candidate_04 | `rr1.5 hold120` | broad | `2.507%` | `-2.979` | `0.2%` | `10` |
| candidate_05 | `control rr2.0 hold240` | `2024_2025` | `2.498%` | `-3.568` | `0.6%` | `8` |
| candidate_06 | `rr2.0 hold120` | `2024_2025` | `2.145%` | `-4.728` | `0.1%` | `8` |
| candidate_07 | `rr1.5 hold240` | `2024_2025` | `1.957%` | `-4.868` | `0.6%` | `8` |
| candidate_08 | `rr1.5 hold120` | `2024_2025` | `2.129%` | `-4.776` | `0.1%` | `8` |

## Useful

- The canonical `rr2.0 hold240` control stayed best on return in both windows.
- Shorter holds reduced drawdown:
  - broad: `0.4% -> 0.2%`
  - `2024_2025`: `0.6% -> 0.1%`
- But those overlays did not improve the overall branch quality because return and Sharpe both got worse.

## Not Useful

- No tested exit/risk overlay beat the canonical control across both windows.
- `hold120` reduced return in both windows.
- `rr1.5` also reduced return in both windows.
- `rr1.5 + hold120` still failed to overtake the base row in either window.

## Invalid

- None.

## Conclusion

The cloud event-aware intraday branch is not being held back by an obviously too-slow hold window or too-ambitious profit target. The tested overlays mostly compressed drawdown at the cost of already modest return, which is not enough to justify a new control.

The canonical row therefore remains:

- `platform5 pre1 intraday BSL`
- no recent-weakness requirement
- `selection_pool_size = 2`
- `QQQ/XLK context_min_positive = 1`
- `risk_reward = 2.0`
- `max_holding_minutes = 240`

## Next

- Stop spending budget on simple exit/risk micro-tuning for this cloud intraday lane.
- Treat the branch as sufficiently mapped for now:
  - metadata slicing exhausted in `iter_091`
  - exit/risk overlays exhausted in `iter_092`
- Future work should move to:
  - downstream integration into a broader activation/allocation framework
  - or richer external event metadata rather than more tuning inside the current QuantConnect field set
