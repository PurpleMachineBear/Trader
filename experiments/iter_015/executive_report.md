# Iteration `iter_015` Executive Report

## Decision

Drop `gap` from the paper-candidate track.

Keep the paper shortlist centered on:

- `QQQ/VOO/GLD dual_momentum 126/7`
- `Dynamic high-beta BSL pool 1`
- `Fixed NVDA/TSLA aggressive BSL`
- `Fixed clean/core clean BSL` only as lower-drawdown sleeves

## What Changed

This round was a deployment-validation pass, not a discovery pass. It extended the minute sample back to `2024-01-02` and forced the intraday branches through `1bps` and `2bps` slippage.

That changed the branch hierarchy. `Dynamic high-beta BSL` stayed good. `Dynamic high-beta gap` did not.

## Key Findings

| Branch | Best Row | Return % | Drawdown % | Trades |
| --- | --- | ---: | ---: | ---: |
| `Daily control` | `QQQ/VOO/GLD dual_momentum 126/7` | `92.392` | `13.9` | `11` |
| `Dynamic high-beta BSL` | `candidate_09` | `24.695` | `7.3` | `66` |
| `Dynamic high-beta BSL at 2bps` | `candidate_12` | `23.066` | `7.5` | `66` |
| `Fixed aggressive BSL control` | `candidate_06` | `20.995` | `5.8` | `35` |
| `Fixed clean BSL control` | `candidate_05` | `13.949` | `4.5` | `39` |
| `Core clean BSL control` | `candidate_08` | `8.049` | `2.6` | `30` |
| `VOO benchmark` | `candidate_01` | `42.608` | `18.8` | `0` |

## What Was Useful

- `Dynamic high-beta BSL pool 1` survived the longer sample and slippage stress.
- `Fixed NVDA/TSLA aggressive BSL` remained strong enough to keep as a secondary paper control.
- `Fixed clean` and `core clean` BSL still make sense as drawdown-first sleeves.

## What Was Not Useful

- `Dynamic high-beta gap` failed the longer-sample test.
- Broader dynamic BSL pools were not worth promoting over `pool 1`.
- `Gap` should no longer consume equal research budget in the paper track.

## Recommendation

Next round should stop treating this as a family search and start treating it as a frozen-shortlist validation problem:

1. keep the daily control
2. keep only the surviving BSL branches
3. test capital and sizing realism
4. prepare a final paper shortlist from the survivors
