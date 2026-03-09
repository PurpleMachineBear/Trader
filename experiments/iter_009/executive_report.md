# Iteration `iter_009` Executive Report

## Decision

Continue. Batch 4 validated the leading GLD-defensive candidates across multiple windows and materially increased confidence that the campaign is following real structure rather than a single-sample mirage.

## Winners

Stable raw-return leader:

- `TQQQ/VOO/GLD 126/7 1.0x`
- Average score across windows: `277.122`
- Worst-window score: `147.131`
- Full-sample score: `452.801`

Stable deployable leveraged compromise:

- `TQQQ/VOO/GLD 126/7 0.75x`
- Average score across windows: `203.618`
- Worst-window score: `121.144`
- Full-sample score: `307.248`

Stable control-grade leader:

- `QQQ/VOO/GLD 126/7`
- Average score across windows: `199.008`
- Worst-window score: `110.928`
- Average drawdown: `12.10%`

## What Changed

- This batch stopped optimizing and started validating.
- Results were aggregated by strategy structure across `5` windows instead of judged only by single-run leaders.
- That produced a much clearer answer about what is robust:
  - leveraged `TQQQ/*/GLD` works across windows
  - non-leveraged `QQQ/*/GLD` works across windows
  - legacy `TLT` defense does not keep up

## Stability Table

| Structure | Avg Score | Worst-Window Score | Avg Drawdown % |
| --- | ---: | ---: | ---: |
| `TQQQ/VOO/GLD 126/7 1.0x` | `277.122` | `147.131` | `31.78` |
| `TQQQ/SPY/GLD 126/7 1.0x` | `277.040` | `146.955` | `31.78` |
| `TQQQ/QQQ/GLD 126/7 1.0x` | `263.292` | `128.336` | `31.78` |
| `TQQQ/VOO/GLD 126/7 0.75x` | `203.618` | `121.144` | `26.62` |
| `QQQ/VOO/GLD 126/7` | `199.008` | `110.928` | `12.10` |
| `QQQ/SPY/GLD 126/7` | `198.766` | `110.488` | `12.10` |

## Key Findings

- The best structures from the previous rounds did not collapse under window validation.
- `GLD` defensive rotation is now the strongest validated family theme in the project.
- The exact offensive proxy among `VOO`, `SPY`, and `QQQ` matters less than the presence of the `GLD` defensive leg and the chosen risk bucket.
- The campaign now has a validated menu of candidates instead of just a list of attractive backtests.

## Main Risks

- Full-size leveraged candidates still sit in a much higher drawdown bucket than the control-grade non-leveraged candidates.
- Some windows were dominated by simple `TQQQ` buy-and-hold, which means the final deployment round should not over-interpret one regime.
- The project still lacks a final decision layer that selects deployment candidates by risk class.

## Recommendation For Final Round

- Use the last batch to build a deployment shortlist, not to reopen broad exploration.
- Keep separate final buckets:
  - full-size leveraged
  - `0.75` leveraged
  - control-grade non-leveraged
- Carry only validated structures into the last round and keep one legacy `TLT` baseline for contrast.
