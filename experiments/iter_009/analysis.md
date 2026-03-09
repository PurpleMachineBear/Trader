# Iteration `iter_009` Analysis

## Scope

- Candidates: `200`
- Status: `200/200 completed`
- Sample design: `5` validation windows
- Focus: multi-window robustness of the top GLD-defensive structures
- Benchmark: `VOO buy-and-hold`

## Window Winners

| Window | Best Candidate | Structure | Score |
| --- | --- | --- | ---: |
| `w1_2022_2023` | `candidate_030` | `TQQQ sma_regime 20/120 + 189d` | `162.727` |
| `w2_2023_2024` | `candidate_044` | `TQQQ buy-and-hold` | `473.182` |
| `w3_2024_2026ytd` | `candidate_107` | `GLD sma_regime 30/150 + 252d` | `339.915` |
| `w4_2022_2024` | `candidate_150` | `TQQQ sma_regime 20/120 + 189d` | `300.745` |
| `w5_full_sample` | `candidate_173` | `TQQQ/VOO/GLD 126/7 1.0x` | `452.801` |

## Stability Table

| Structure | Avg Score | Median | Min | Max | Avg Drawdown % |
| --- | ---: | ---: | ---: | ---: | ---: |
| `TQQQ/VOO/GLD 126/7 1.0x` | `277.122` | `271.881` | `147.131` | `452.801` | `31.78` |
| `TQQQ/SPY/GLD 126/7 1.0x` | `277.040` | `271.769` | `146.955` | `452.678` | `31.78` |
| `TQQQ/QQQ/GLD 126/7 1.0x` | `263.292` | `250.503` | `128.336` | `423.825` | `31.78` |
| `TQQQ/VOO/GLD 126/7 0.75x` | `203.618` | `203.517` | `121.144` | `307.248` | `26.62` |
| `TQQQ/SPY/GLD 126/7 0.75x` | `203.531` | `203.335` | `120.986` | `307.156` | `26.62` |
| `QQQ/VOO/GLD 126/7` | `199.008` | `169.441` | `110.928` | `328.189` | `12.10` |
| `QQQ/SPY/GLD 126/7` | `198.766` | `169.316` | `110.488` | `327.778` | `12.10` |
| `QQQ/XLK/GLD 126/14` | `198.116` | `178.344` | `107.638` | `310.105` | `11.30` |
| `QQQ/SPY/GLD 147/7` | `193.001` | `190.661` | `102.652` | `291.521` | `12.54` |
| `QQQ/VOO/GLD 147/7` | `191.344` | `191.408` | `98.931` | `288.639` | `12.54` |

## Useful

- The top GLD-defensive structures survived validation. This is no longer a full-sample artifact.
- Full-size leveraged `TQQQ/*/GLD 126/7` variants were the most stable raw-return leaders. Their worst-window scores stayed above `128`, and their worst-window returns stayed above `92%`.
- The `0.75` leveraged bucket also validated well. Its worst-window scores stayed above `120`, which means the de-risked leveraged path remains credible.
- The strongest control-grade, non-leveraged structures were:
  - `QQQ/VOO/GLD 126/7`
  - `QQQ/SPY/GLD 126/7`
  - `QQQ/XLK/GLD 126/14`
- The validation batch showed that different windows can have different raw winners, but the cross-window ranking still converged back to the same GLD-defensive rotation family.

## Not Useful

- `TQQQ buy-and-hold` was spectacular in `2023-2024`, but that strength did not translate into a durable cross-window deployment baseline.
- Single-asset `TQQQ` trend timing had strong windows, but its worst-window behavior was materially weaker than the validated GLD-defensive rotation cluster.
- The legacy `QQQ/VOO/TLT` structures stayed well below the best GLD-defensive candidates across windows.

## Invalid Or Process Issues

- No template-level execution issue appeared.
- Standard process-level retry was sufficient to clean the batch.

## Interpretation

- The campaign now has evidence for both:
  - a stable high-risk track: leveraged `TQQQ/*/GLD`
  - a stable control-grade track: non-leveraged `QQQ/*/GLD`
- That is stronger evidence than any earlier round because it survived multiple windows, not only one in-sample ranking.

## Next Round

- Use the final round as a deployment-candidate round, not another discovery round.
- Restrict the search to structures that passed validation:
  - `QQQ/VOO/GLD 126/7`
  - `QQQ/SPY/GLD 126/7`
  - `QQQ/XLK/GLD 126/14`
  - `TQQQ/VOO/GLD 126/7` at `1.0x` and `0.75x`
  - `TQQQ/SPY/GLD 126/7` at `1.0x` and `0.75x`
  - `GLD 20/120 + 189d`
- Keep `QQQ/VOO/TLT` only as a final legacy baseline.
