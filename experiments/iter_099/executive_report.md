# Iteration 099 Executive Report

## Decision

Do not promote a reduced-size `enterprise4 after_close` sleeve.

## What We Learned

Lowering the positive-window sleeve from `10%` to `5%` or `7.5%` does not solve its regime sensitivity.

- `7.5%` is the best reduced-allocation compromise
- but it still loses to `platform5 any 10%` in `2024` and `2026 YTD`
- `5%` gives up too much of the `2025` advantage and still does not improve risk enough

## Winner

Among the reduced-allocation rows, `enterprise4 after_close 7.5%` was the strongest:

- recent broad: `61.270%` return, `Sharpe 2.047`, `10.6%` drawdown
- `2025`: `40.356%` return, `Sharpe 2.072`, `4.9%` drawdown

## Main Risk

The reduced allocations do not turn this into an all-weather sleeve. The branch is still mainly a positive-window overlay.

## Recommendation

Keep the production master unchanged. Keep `platform5 any 10%` as the canonical cloud event-sleeve control, keep `enterprise4 after_close` as the positive-window alias, and stop spending budget on sleeve-size micro-tuning.
