# Iteration `iter_004` Executive Report

## Decision

Continue to `iter_005` with `SPY 40/180 + 252-day time stop` as the new control.

## Winner

`candidate_04` (`SPY`, `40/180`, `max_holding_days=252`) is the round winner.

- Net profit: `47.494%`
- Sharpe ratio: `0.648`
- Max drawdown: `9.9%`
- Composite score: `92.494`
- Total orders: `5`
- Closed trades: `2`

## What Changed

This round expanded beyond pure window tuning by introducing a new `sma_regime` family with structural overlays. Ten candidates tested trailing stops, time stops, entry buffers, and AAPL cross-symbol transfer against a clean SPY control.

## Key Findings

- The `252-day time stop` was the first structural change that clearly improved on the old benchmark. It beat the prior best score (`92.494` vs. `89.466`) while increasing activity from `1` total order to `5`.
- The `10% trailing stop` on SPY created more evidence (`3` total orders, `1` closed trade) and stayed reasonably close to the control, but it did not beat the time-stop winner.
- The `15% trailing stop` was effectively inactive over this sample. Its metrics were identical to the control, which means the stop never materially changed path behavior.
- The shorter `SPY 35/160 + 10% trailing stop` variant was respectable (`81.390` score) but still inferior to the slower 40/180 base with structure.
- The more aggressive `126-day time stop + 20-day cooldown` on SPY generated the most useful activity among SPY variants (`10` orders, `5` trades) but damaged Sharpe and total score too much.
- `AAPL 40/180 + 126-day time stop` produced the highest raw return of the round (`60.913%`) and meaningful trade count (`11` orders, `5` trades), but its drawdown (`20.5%`) kept it well below the SPY winner on the round objective.
- `AAPL 40/180 + 10% trailing stop` confirmed that simply adding exits does not rescue AAPL as a risk-adjusted transfer of the SPY edge.

## Main Risks

- Even the new winner still has a modest sample size. `2` closed trades is better than zero, but not yet strong evidence of robustness.
- The stronger-activity variants tended to pay for that activity with lower Sharpe or larger drawdowns.
- AAPL transfer remains unstable: high raw upside is available, but the drawdown cost rises quickly.

## Recommendation For Next Round

- Keep `SPY 40/180 + 252-day time stop` as the control.
- Explore nearby annual-reset variants rather than reverting to pure SMA window search.
- Test shorter and longer time stops around `252` days.
- Test the winning time stop combined with a mild trailing stop.
- Test the winning time stop combined with small entry buffers or cooldown rules.
