# Paper Trading Shortlist

Last updated: `2026-03-07`

## Approved Set

### 1. Primary Daily Engine

- `QQQ/VOO/GLD dual_momentum 126/7`

Why keep it:

- strongest full-sample daily control
- strong `2025` and `2026 YTD`
- clear benchmark outperformance over the current full sample

Caution:

- `2024` lagged `VOO` badly, so it is not an all-weather replacement for passive exposure

### 2. Primary Intraday Engine

- `NVDA/TSLA fixed aggressive BSL`

Why keep it:

- positive in `2024`, `2025`, and `2026 YTD`
- lower average drawdown than the dynamic high-beta branch
- simpler and more stable than the broader dynamic scanner

Observed window profile:

- `2024`: `5.056%` return, `4.2%` drawdown
- `2025`: `7.982%` return, `5.5%` drawdown
- `2026 YTD`: `3.443%` return, `1.2%` drawdown

### 3. Secondary Intraday Engine

- `NVDA/TSLA/AMD/MU/TSM/MRVL/AVGO dynamic high-beta BSL pool 1`

Why keep it:

- positive in all three validation windows
- higher upside than the fixed aggressive branch when the regime is favorable

Why it is secondary, not primary:

- much weaker in `2024`
- higher drawdown than the fixed aggressive branch
- better treated as an aggressive paper sleeve or shadow branch

Observed window profile:

- `2024`: `1.676%` return, `7.7%` drawdown
- `2025`: `15.072%` return, `6.6%` drawdown
- `2026 YTD`: `3.683%` return, `3.3%` drawdown

### 4. Optional Conservative Variant

- `NVDA/TSLA fixed aggressive BSL risk 1.00%`

Why keep it:

- positive in all three validation windows
- much lower drawdown than the main high-beta branch

Use case:

- conservative comparison sleeve
- not the main paper winner

Observed window profile:

- `2024`: `0.655%` return, `1.6%` drawdown
- `2025`: `2.815%` return, `0.8%` drawdown
- `2026 YTD`: `1.740%` return, `0.6%` drawdown

## Benchmark Set

- `VOO buy-and-hold`

Keep it running alongside paper candidates so paper performance is judged against a live passive reference, not only against internal expectations.

## Rejected For Paper

- `gap` branches
- `AAPL/MSFT/AMZN/META core clean BSL`
- `AAPL/MSFT/AMZN/META core clean BSL risk 1.00%`

Why rejected:

- they did not survive the subwindow stability test
- they were too dependent on a single favorable year

## Recommended First Paper Stack

Run these first:

1. `QQQ/VOO/GLD dual_momentum 126/7`
2. `NVDA/TSLA fixed aggressive BSL`
3. `VOO buy-and-hold` benchmark

Optional shadow run:

- `dynamic high-beta BSL pool 1`

Optional conservative comparison:

- `fixed aggressive BSL risk 1.00%`

## Why This Is Enough

The shortlist has now passed:

- full-sample validation
- slippage stress
- sizing validation
- separate `2024`, `2025`, and `2026 YTD` window checks

At this point, the limiting factor is no longer idea generation. It is paper-deployment operations.
