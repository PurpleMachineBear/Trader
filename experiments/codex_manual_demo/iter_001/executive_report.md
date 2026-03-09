# Executive Report iter_001

Decision: advance `candidate_01` as the lead configuration for the next round, but do not treat it as production-ready.

## What happened

- `candidate_01` (`AAPL`, SMA `20/100`) outperformed the control on return and Sharpe.
- `candidate_02` (`AAPL`, SMA `50/200`) remained cleaner on drawdown, but the evidence base was weak because it generated only 1 trade.

## Key numbers

- `candidate_01`
  - Net profit: `34.06%`
  - Sharpe: `0.279`
  - Max drawdown: `21.2%`
  - Trades: `3`
- `candidate_02`
  - Net profit: `27.305%`
  - Sharpe: `0.193`
  - Max drawdown: `15.4%`
  - Trades: `1`

## Interpretation

The faster `20/100` crossover appears more responsive than the classic `50/200` baseline on this sample. That said, the current lead still has a drawdown above `20%`, which is too high to ignore. The control's lower drawdown is encouraging, but with only one closed trade it is not strong evidence against the faster configuration.

## Risks

- The current lead candidate still has elevated drawdown.
- Both candidates have low trade counts, so the sample is thin.
- The observed edge may be AAPL-specific rather than a robust family-level improvement.

## Next round plan

- Exploit around `20/100` with nearby windows to see whether drawdown can be reduced without giving up too much return.
- Explore the same crossover family on `SPY` to test portability.
- Keep the original `50/200` AAPL control in the set.
