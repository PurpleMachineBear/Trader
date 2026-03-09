# iter_090 analysis

## Sample Coverage

- recent broad: `2025-01-02` to `2026-03-06`
- earlier validation: `2024-01-02` to `2025-12-31`
- cloud project: `Cloud_Earnings_Research`

## Summary Table

| candidate | structure | window | return | sharpe | drawdown | orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| candidate_01 | `pool2 ctx+1 control` | broad | `3.246%` | `-2.053` | `0.4%` | `10` |
| candidate_02 | `pool3 ctx+1` | broad | `3.246%` | `-2.053` | `0.4%` | `10` |
| candidate_03 | `pool2 no context gate` | broad | `3.070%` | `-2.172` | `0.7%` | `10` |
| candidate_04 | `pool2 ctx+1 control` | `2024_2025` | `2.498%` | `-3.568` | `0.6%` | `8` |
| candidate_05 | `pool3 ctx+1` | `2024_2025` | `2.498%` | `-3.568` | `0.6%` | `8` |
| candidate_06 | `pool2 no context gate` | `2024_2025` | `2.706%` | `-3.520` | `0.4%` | `8` |

## Useful

- The no-weakness `pool2 ctx+1` row is now the right canonical cloud intraday control.
- Removing the context gate produced a split result:
  - broad got slightly worse: `3.246% -> 3.070%`, drawdown `0.4% -> 0.7%`
  - `2024_2025` got slightly better: `2.498% -> 2.706%`, drawdown `0.6% -> 0.4%`
- This is weak evidence that context gating may be mildly current-regime helpful but not universally dominant.

## Not Useful

- Raising `selection_pool_size` from `2` to `3` was completely inert in both windows.
- More pool-size tuning is not a good use of budget for this branch.

## Invalid

- None.

## Next

- Keep `pool2 ctx+1` as the cloud event-aware intraday control.
- Treat `no context gate` only as a mixed split-window alias, not as a promotion candidate.
- Stop tuning watchlist breadth.
- If this lane continues, move from selector mechanics to downstream integration:
  - use event-aware cloud state as an activation filter or allocation hint for the main intraday stack
  - or test exit / risk overlays on the new canonical no-weakness control instead of more premarket selection knobs
