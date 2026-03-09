# iter_089 analysis

## Sample Coverage

- recent broad: `2025-01-02` to `2026-03-06`
- earlier validation: `2024-01-02` to `2025-12-31`
- cloud project: `Cloud_Earnings_Research`

## Summary Table

| candidate | structure | window | return | sharpe | drawdown | orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| candidate_01 | `weak-only BSL control` | broad | `1.070%` | `-8.477` | `0.4%` | `8` |
| candidate_02 | `no-weakness + absolute-return score` | broad | `3.246%` | `-2.053` | `0.4%` | `10` |
| candidate_03 | `no-weakness + no recent-return score` | broad | `3.246%` | `-2.053` | `0.4%` | `10` |
| candidate_04 | `weak-only BSL control` | `2024_2025` | `0.293%` | `-20.010` | `0.6%` | `4` |
| candidate_05 | `no-weakness + absolute-return score` | `2024_2025` | `2.498%` | `-3.568` | `0.6%` | `8` |
| candidate_06 | `no-weakness + no recent-return score` | `2024_2025` | `2.498%` | `-3.568` | `0.6%` | `8` |

## Useful

- Removing the inherited `recent weakness` requirement materially improved event-aware intraday BSL in both windows.
  - broad: `1.070% -> 3.246%`, orders `8 -> 10`, drawdown unchanged at `0.4%`
  - `2024_2025`: `0.293% -> 2.498%`, orders `4 -> 8`, drawdown unchanged at `0.6%`
- This is the first strong evidence that the cloud event intraday lane should not inherit the generic local `weak-then-reclaim` assumption.

## Not Useful

- Once the recent-weakness filter was removed, `absolute` and `none` recent-return score modes were behaviorally identical.
- This means the recent-return score itself is not the remaining bottleneck.

## Invalid

- None.

## Next

- Promote the no-weakness `platform5 pre1 intraday BSL` row to the new cloud intraday control.
- Test `selection_pool_size` and `context gate` next.
- Do not reopen `failed_breakdown`; it has already failed the first event-aware activation test.
