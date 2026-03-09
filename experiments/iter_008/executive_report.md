# Iteration `iter_008` Executive Report

## Decision

Continue. Batch 3 showed that the leveraged `TQQQ/*/GLD` edge survives explicit risk scaling, and that `0.75` size is currently the most credible leveraged compromise.

## Winners

Raw-return winner:

- `candidate_006`: `TQQQ/VOO/GLD`, `126-day` lookback, `7-day` rebalance, full size
- Net profit: `412.001%`
- Sharpe ratio: `1.076`
- Max drawdown: `33.4%`
- Composite score: `452.801`

Deployable leveraged compromise:

- `candidate_017`: `TQQQ/VOO/GLD`, `126-day` lookback, `7-day` rebalance, `0.75` size
- Net profit: `267.848%`
- Sharpe ratio: `0.952`
- Max drawdown: `27.9%`
- Composite score: `307.248`

Control-grade non-leveraged leader:

- `candidate_005`: `QQQ/VOO/GLD`, `126-day` lookback, `7-day` rebalance
- Net profit: `224.389%`
- Sharpe ratio: `1.316`
- Max drawdown: `13.9%`
- Composite score: `328.189`

## What Changed

- This batch stopped asking whether leverage works and started asking how much leverage is still worth carrying.
- `position_size` became the main experimental dimension across rotation, SMA trend, and Donchian trend families.
- The result was clear: de-risking matters, but not linearly. The sweet spot is currently near `0.75`, not `0.50` or lower.

## Summary Table

| Candidate | Description | Score | Return % | Sharpe | Drawdown % |
| --- | --- | ---: | ---: | ---: | ---: |
| `candidate_006` | `TQQQ/VOO/GLD`, `126d`, `7d`, `1.00x` | `452.801` | `412.001` | `1.076` | `33.4` |
| `candidate_097` | `TQQQ/SPY/GLD`, `126d`, `7d`, `1.00x` | `452.678` | `411.878` | `1.076` | `33.4` |
| `candidate_057` | `TQQQ/QQQ/GLD`, `126d`, `7d`, `1.00x` | `423.825` | `386.725` | `1.039` | `33.4` |
| `candidate_005` | `QQQ/VOO/GLD`, `126d`, `7d`, `1.00x` | `328.189` | `224.389` | `1.316` | `13.9` |
| `candidate_017` | `TQQQ/VOO/GLD`, `126d`, `7d`, `0.75x` | `307.248` | `267.848` | `0.952` | `27.9` |
| `candidate_008` | `GLD 20/120 + 189d` | `260.720` | `178.620` | `1.097` | `13.8` |

## Key Findings

- Full-size leveraged `TQQQ/*/GLD` is still the raw-return leader.
- `0.75` size is the first leveraged bucket that still looks strategically interesting after de-risking.
- `0.50` and `0.33` size reduce drawdown, but the return give-up is too large.
- The non-leveraged `QQQ/*/GLD` cluster remains the best control-grade path with much cleaner drawdowns.
- The legacy `QQQ/VOO/TLT` path still does not recover even when risk-scaled.

## Main Risks

- Full-size leveraged winners still live in a materially higher drawdown bucket than the non-leveraged leaders.
- This is still a single continuous historical sample, not a full walk-forward program.
- The offensive proxy within the leveraged bucket may matter less than assumed, which means the regime itself could be doing more of the work than the exact proxy choice.

## Recommendation For Next Round

- Use the next batch for robustness and subperiod validation instead of another broad search.
- Carry forward three tracks:
  - non-leveraged control-grade GLD rotation
  - `0.75` leveraged GLD rotation
  - full-size leveraged GLD rotation as a raw-return ceiling reference
- Keep one legacy `TLT` control to make sure the GLD shift remains real outside the full-sample ranking.
