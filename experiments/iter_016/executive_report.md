# Iteration `iter_016` Executive Report

## Decision

Keep the main paper shortlist on the existing no-risk-sizing controls.

Do not promote risk-sized versions to the primary paper set. Use them only as optional conservative sleeves.

## What Changed

This round tested stop-based `risk_per_trade_pct` sizing on the frozen intraday shortlist from `iter_015`.

It worked exactly in one dimension:

- drawdown came down sharply

But it failed in the other dimension that matters for the primary paper track:

- return came down too much

## Key Findings

| Branch | Best Row | Return % | Drawdown % | Trades |
| --- | --- | ---: | ---: | ---: |
| `Daily control` | `QQQ/VOO/GLD dual_momentum 126/7` | `92.392` | `13.9` | `11` |
| `Dynamic high-beta BSL control` | `candidate_05` | `24.695` | `7.3` | `66` |
| `Fixed aggressive BSL control` | `candidate_06` | `20.995` | `5.8` | `35` |
| `Fixed clean BSL control` | `candidate_07` | `13.949` | `4.5` | `39` |
| `Core clean BSL control` | `candidate_08` | `8.049` | `2.6` | `30` |
| `Best risk-sized fixed row` | `candidate_16` | `7.295` | `1.6` | `35` |
| `Best risk-sized dynamic row` | `candidate_11` | `6.466` | `3.4` | `66` |

## What Was Useful

- `risk_per_trade_pct` is a real drawdown-control tool.
- `1.00%` risk sizing was the best conservative setting tested.
- `Fixed core clean BSL` and `fixed aggressive BSL` become credible conservative sleeves when risk-sized.

## What Was Not Useful

- Risk-sized versions did not beat the existing no-risk paper controls.
- Smaller risk budgets like `0.50%` and `0.75%` gave up too much return.
- This is not the right direction for finding the main paper winner.

## Recommendation

The paper shortlist should now split into two roles:

1. `Primary paper set`
   - `QQQ/VOO/GLD dual_momentum 126/7`
   - `dynamic high-beta BSL pool 1`
   - `fixed NVDA/TSLA aggressive BSL`
2. `Optional conservative sleeves`
   - `fixed core clean BSL risk 1.00%`
   - `fixed aggressive BSL risk 1.00%`

Next round should stop changing sizing and instead validate the frozen shortlist across multiple date windows.
