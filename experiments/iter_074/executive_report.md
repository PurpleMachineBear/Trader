# iter_074 Executive Report

## Decision

Keep `platform5 pre1 hold3 any` as the cloud event-aware lead and record `after_close` as the main structural signal behind the branch.

## Why

- `platform5 pre1 hold3 any`: `100.059%` return, `10.1%` drawdown
- `platform5 pre1 hold3 after_close`: `82.585%`, `10.1%` drawdown
- `platform5 pre1 hold3 before_open`: `18.988%`, `4` trades
- `platform7 pre1 hold3 after_close`: `62.278%`, `18.1%` drawdown
- `platform5 pre1 hold1 after_close`: `64.113%`, `10.6%` drawdown

## Final View

- Most of the branch is driven by `after_close` earnings setups.
- `before_open` is too sparse to stand alone, but it is not worthless.
- The next quality improvement should be symbol-specific, not another global filter sweep.

## Recommendation

- Keep the frozen paper set unchanged.
- Carry the cloud lane forward with symbol-specific event quality scoring.
