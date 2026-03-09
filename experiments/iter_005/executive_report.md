# Iteration `iter_005` Executive Report

## Decision

Continue. The upgraded research process is producing materially better information than the earlier single-symbol loop.

## Winner

`candidate_06` (`QQQ 40/180 + 252-day time stop`) is the round winner.

- Net profit: `73.670%`
- Sharpe ratio: `0.896`
- Max drawdown: `13.1%`
- Composite score: `137.070`

## What Changed

This round introduced a professional research structure:

- explicit `VOO buy-and-hold` benchmark
- explicit allowed universe and compliance blocklist
- multi-symbol validation
- multi-family comparison (`buy_and_hold`, `sma_regime`, `dual_momentum`, `rotation_rsi`)

## Key Findings

- The passive `VOO` benchmark was weak over this sample: `22.297%` net profit, `0.114` Sharpe, `25.6%` drawdown.
- The best active candidates beat that benchmark decisively.
- `QQQ 40/180 + 252-day time stop` was the strongest result of the round.
- `MSFT 40/180 + 252-day time stop` also transferred well, which means the trend structure is not limited to `SPY`.
- `QQQ/VOO/TLT dual_momentum` is the first clearly competitive non-trend family and is worth continued research.
- `QQQ/VOO rotation_rsi` produced high activity but too much drawdown and turnover for its achieved Sharpe.
- `IWM` was a weak transfer target for the current trend structure.

## Main Risks

- The top single-asset trend winners still have low closed-trade counts.
- Stronger-activity families can pay for that activity with materially higher drawdowns.
- The current findings are still from one historical window and need stricter validation.

## Recommendation For Next Round

- Keep `VOO buy-and-hold` as the benchmark.
- Keep `SPY 40/180 + 252-day time stop` as the trend control.
- Add `QQQ 40/180 + 252-day time stop` as an aggressive trend control.
- Add `QQQ/VOO/TLT dual_momentum` as a cross-family control.
- Spend the next round on `dual_momentum` parameter exploration and stricter validation of the strongest trend winners.
