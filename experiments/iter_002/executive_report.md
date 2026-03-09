# Iteration `iter_002` Executive Report

## Decision

Continue to `iter_003`.

## What Changed

This round reran the SMA family after fixing the template so the strategy can establish an initial post-warmup position. The round then tested one control, two tighter SPY window variants, and two cross-symbol checks.

## Winner

`candidate_02` (`SPY`, `40/180 SMA`) is the current round winner.

- Net profit: `46.766%`
- Sharpe ratio: `0.633`
- Max drawdown: `10.3%`
- Composite score: `89.466`

## Key Findings

- The best-performing setup improved on the `SPY 50/200` control across both return and Sharpe while keeping drawdown nearly unchanged.
- The more aggressive `SPY 30/150` variant increased activity (`5` total orders, `2` trades) but materially degraded return and Sharpe. The edge did not survive the extra turnover.
- The top two SPY candidates still produced only `1` total order and `0` closed trades over `2022-01-01` to `2024-12-31`. This means the current best result is still close to a timed buy-and-hold exposure, not a well-proven crossover engine.
- `QQQ` and `VOO` were not valid comparison runs in this date range. LEAN logs indicate local data effectively started on `2024-12-31` for both symbols, so those candidates produced zero orders and zero usable metrics.

## Main Risks

- Evidence quality remains weak because the winner generated almost no trading decisions.
- Cross-symbol validation failed due to local data availability, so the current edge is still only supported on `SPY`.
- A shorter window can raise signal count, but the first faster test (`30/150`) suggests a real whipsaw tradeoff.

## Recommendation For Next Round

- Keep `SPY 40/180` as the control.
- Search shorter SPY windows around the winner to increase signal density without collapsing Sharpe.
- Use `AAPL` rather than `QQQ` or `VOO` for cross-symbol validation because `AAPL` has confirmed local daily coverage in the `2022-01-01` to `2024-12-31` window.
