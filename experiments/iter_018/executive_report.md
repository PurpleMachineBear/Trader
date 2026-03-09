# Iteration 018 Executive Report

## Decision

`iter_018` was a valid depth-and-breadth round. All `27` candidates completed. The main conclusion is not a strategy replacement. It is a branch split:

- `QQQ/VOO/GLD dual_momentum 126/7` stays the daily control.
- `NVDA/TSLA fixed aggressive BSL` stays the main all-weather intraday control.
- `Fixed BSL + daily_loss 0.75%` is now a credible conservative overlay candidate.
- `Dynamic BSL 120m` and `dynamic vwap_reclaim` should be treated as `2026 range-regime` branches only until they pass earlier-window validation.

## Sample Coverage

- Broad sample: `2025-01-02` to `2026-03-06`
- Current regime subset: `2026-01-02` to `2026-03-06`
- Completed rows: `27 / 27`
- Unique structures: `17`

## Summary Table

| Candidate | Window | Return % | Sharpe | Drawdown % | Trades | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `candidate_02` | Broad | 85.669 | 2.125 | 13.9 | 4 | Daily engine remains dominant. |
| `candidate_06` | Broad | 23.828 | 1.076 | 6.8 | 37 | Best broad intraday raw return. |
| `candidate_05` | Broad | 16.303 | 0.567 | 4.8 | 20 | Best stable all-weather intraday control. |
| `candidate_07` | Broad | 12.736 | 0.308 | 2.1 | 20 | Best conservative overlay in this round. |
| `candidate_27` | `2026 YTD` | 7.389 | 2.232 | 1.5 | 11 | Best new short-window exploration branch. |
| `candidate_25` | `2026 YTD` | 5.284 | 1.960 | 3.3 | 8 | Shorter-hold dynamic BSL fits the current tape better. |
| `candidate_22` | `2026 YTD` | 3.443 | 1.849 | 1.2 | 4 | Stable fixed control remained positive. |

## What Was Useful

- Strict context gates remained correct. Relaxing them hurt quality.
- Bucketed dynamic high-beta selection stayed valid and really rotated into `AMD`, `AVGO`, `MRVL`, `MU`, and `TSM`.
- A `0.75%` daily-loss cap improved the fixed `NVDA/TSLA` BSL branch as a conservative overlay.
- The current `2026` range regime clearly rewarded faster exits and softer reclaim-style entries.

## What Was Not Useful

- Semis-only dynamic BSL was weaker than the mixed high-beta basket.
- Broad-sample `vwap_reclaim` was too active and too weak to approve.
- Dynamic BSL with the daily-loss cap gave up too much raw return.

## Main Risk

The best new `2026` rows are still short-window results. They cannot replace the paper shortlist until they survive earlier choppy windows. There is also an execution-quality concern: the unguarded broad dynamic BSL rows generated heavy cancellation churn.

## Recommendation For Next Round

Do not reopen a broad grid. Run a narrow validation round focused on:

- `fixed BSL + daily_loss 0.75%`
- `dynamic BSL 120m hold`
- `dynamic vwap_reclaim 120m hold`

The goal is to decide whether these are real regime branches or just `2026 YTD` artifacts.
