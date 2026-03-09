# Iteration 098 Executive Report

## Decision

Do not promote `enterprise4 after_close` into the frozen production master.

## What We Learned

The split windows gave a clean classification:

- `platform5 any` is still the canonical all-weather event sleeve
- `enterprise4 after_close` is the best positive-window alias
- `software3` does not transfer into the master

## Winner

Inside the positive `2025` window, the best row was `enterprise4 after_close`:

- `41.391%` return
- `Sharpe 2.157`
- `4.7%` drawdown

## Main Risk

That edge does not survive the hostile or sparse-current windows. In `2024` and `2026 YTD`, `platform5 any` remains better.

## Recommendation

Keep the production master unchanged. Treat `enterprise4 after_close` as a `positive-window alias` only, and if this lane continues, test reduced allocation rather than unconditional promotion.
