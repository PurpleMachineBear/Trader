# Iteration `iter_003` Executive Report

## Decision

Pause additional SMA window tuning after this round. The next useful iteration should change strategy structure, not just continue local window search.

## Winner

`candidate_01` (`SPY`, `40/180 SMA`) remains the best observed configuration.

- Net profit: `46.766%`
- Sharpe ratio: `0.633`
- Max drawdown: `10.3%`
- Composite score: `89.466`

## What Changed

This round kept `SPY 40/180` as the control, tested two shorter SPY variants to increase signal density, and validated the winner family on `AAPL`, which has confirmed local data coverage from `2022-01-01` to `2024-12-31`.

## Key Findings

- The `SPY 35/160` variant was the closest challenger. It increased activity to `3` total orders and `1` closed trade, but it still scored below the control (`84.170` vs. `89.466`).
- The more aggressive `SPY 25/125` variant raised activity further (`7` total orders, `3` trades) but sharply reduced both return quality and risk-adjusted performance.
- Cross-symbol validation on `AAPL` worked operationally, and the `AAPL 40/180` variant was profitable (`28.892%` net profit), but its Sharpe (`0.210`) and drawdown (`14.9%`) were much worse than the SPY control.
- `AAPL 25/125` was a clear negative result, with negative Sharpe and the worst drawdown of the round.

## Main Risks

- The best configuration still behaves very close to a buy-and-hold timing rule. `SPY 40/180` generated only `1` total order and `0` closed trades over the full sample.
- More active window variants consistently increased turnover faster than they improved edge.
- The current family shows weak transferability from `SPY` to `AAPL`.

## Recommendation

- Keep `SPY 40/180` as the current benchmark.
- Do not spend the next round on more nearby SMA window tweaks alone.
- If research continues, the next round should add a meaningful structural change such as an exit filter, regime filter, or risk overlay, with `SPY 40/180` retained as the control.
