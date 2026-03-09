# iter_088 analysis

## Sample Coverage

- recent broad: `2025-01-02` to `2026-03-06`
- earlier validation: `2024-01-02` to `2025-12-31`
- cloud project: `Cloud_Earnings_Research`

## Summary Table

| candidate | structure | window | return | sharpe | drawdown | orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| candidate_01 | `platform5 pre1 hold3 swing control` | broad | `76.334%` | `1.175` | `18.1%` | `109` |
| candidate_02 | `platform5 pre1 intraday BSL any` | broad | `1.070%` | `-8.477` | `0.4%` | `8` |
| candidate_03 | `platform5 pre1 intraday failed_breakdown any` | broad | `0.000%` | `0.000` | `0.0%` | `0` |
| candidate_04 | `platform5 pre1 intraday BSL after_close` | broad | `1.070%` | `-8.477` | `0.4%` | `8` |
| candidate_05 | `platform5 pre1 hold3 swing control` | `2024_2025` | `90.053%` | `0.780` | `21.9%` | `165` |
| candidate_06 | `platform5 pre1 intraday BSL any` | `2024_2025` | `0.293%` | `-20.010` | `0.6%` | `4` |
| candidate_07 | `platform5 pre1 intraday failed_breakdown any` | `2024_2025` | `0.000%` | `0.000` | `0.0%` | `0` |
| candidate_08 | `platform5 pre1 intraday BSL after_close` | `2024_2025` | `0.293%` | `-20.010` | `0.6%` | `4` |

## Useful

- `platform5 pre1 intraday BSL` is a real but sparse branch.
  - broad: `1.070%` return, `0.4%` drawdown, `8` orders
  - `2024_2025`: `0.293%` return, `0.6%` drawdown, `4` orders
- The branch is more defensible as a low-activation shadow than as a deployable standalone strategy.

## Not Useful

- `platform5 pre1 intraday failed_breakdown` was completely inactive in both windows.
- Restricting the intraday branch to `after_close` earnings was inert.
  - recent broad `candidate_04` was identical to `candidate_02`
  - `2024_2025 candidate_08` was identical to `candidate_06`

## Invalid

- The carryover cloud swing control changed materially after the `Cloud_Earnings_Research` refactor.
  - broad control now reruns at `76.334%` return and `18.1%` drawdown
  - the pre-refactor remembered control was `100.059%` return and `10.1%` drawdown
- A direct invariance rerun reproduced the new `76.334%` result, so this is not a transient cloud glitch.
- This means direct comparison from `iter_088` to older cloud swing rounds is stale until the control-drift root cause is isolated.

## Next

- Stop spending budget on event-aware intraday `failed_breakdown` for this platform lane.
- Stop spending budget on `after_close` filtering for this intraday branch.
- Test whether the inherited local `recent weakness` assumption is the real bottleneck for event-aware intraday BSL.
