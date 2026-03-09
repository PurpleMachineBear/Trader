# Iteration 097 Executive Report

## Decision

`enterprise4 after_close` is now the strongest static event-sleeve alias inside the master on aggregate windows, but it is not ready for production promotion.

## What We Learned

Embedding cloud event baskets into the master is meaningful. The basket choice still matters after the event branch is combined with the daily core and the fixed intraday sleeve.

The key ranking is:

- best aggregate alias: `enterprise4 after_close`
- second best recent refinement: `platform5 after_close`
- weak transfer: `software3`

## Winner

The best aggregate row was `enterprise4 after_close`:

- recent broad: `61.714%` return, `Sharpe 2.105`, `10.5%` drawdown
- `2024_2025`: `63.334%` return, `Sharpe 1.388`, `5.4%` drawdown

## Main Risk

These are still aggregate windows. The improvement could still be mostly a `2025` phenomenon. Without hostile/current split validation, promotion would be premature.

## Recommendation

Keep the production master unchanged. Move immediately to split-window validation before treating `enterprise4 after_close` as anything more than the leading static alias.
