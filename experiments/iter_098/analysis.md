# Iteration 098 Analysis

## Sample Coverage

- Hostile window: `2024-01-02` to `2024-12-31`
- Positive window: `2025-01-02` to `2025-12-31`
- Sparse current window: `2026-01-02` to `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`
- Static sleeves under test:
  - `platform5 any`
  - `platform5 after_close`
  - `enterprise4 after_close`
  - `software3 any`

## Decision

`enterprise4 after_close` is now a clean `positive-window alias`, not a new all-weather control.

The split windows resolve the aggregate ambiguity from `iter_097`:

- `2024`: `platform5 any` remains best
- `2025`: `enterprise4 after_close` is clearly best
- `2026 YTD`: `platform5 any` remains best

`platform5 after_close` is mostly inert outside the positive window. `software3` does not retain its standalone hostile-window identity after being embedded in the master.

## Summary Table

| Candidate | Window | Static Sleeve | Return | Sharpe | Drawdown | Orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `candidate_01` | `2024` | `platform5 any` control | `15.614%` | `0.602` | `5.5%` | `345` |
| `candidate_02` | `2024` | `platform5 after_close` | `15.614%` | `0.602` | `5.5%` | `345` |
| `candidate_03` | `2024` | `enterprise4 after_close` | `14.672%` | `0.537` | `5.5%` | `330` |
| `candidate_04` | `2024` | `software3 any` | `15.279%` | `0.586` | `5.5%` | `320` |
| `candidate_05` | `2025` | `platform5 any` control | `39.573%` | `2.035` | `4.8%` | `96` |
| `candidate_06` | `2025` | `platform5 after_close` | `40.103%` | `2.076` | `4.7%` | `95` |
| `candidate_07` | `2025` | `enterprise4 after_close` | `41.391%` | `2.157` | `4.7%` | `74` |
| `candidate_08` | `2025` | `software3 any` | `38.681%` | `1.979` | `4.8%` | `69` |
| `candidate_09` | `2026 YTD` | `platform5 any` control | `14.112%` | `2.830` | `9.8%` | `26` |
| `candidate_10` | `2026 YTD` | `platform5 after_close` | `14.112%` | `2.830` | `9.8%` | `26` |
| `candidate_11` | `2026 YTD` | `enterprise4 after_close` | `13.430%` | `2.639` | `10.4%` | `22` |
| `candidate_12` | `2026 YTD` | `software3 any` | `12.944%` | `2.522` | `10.4%` | `19` |

## Stability Table

| Static Sleeve | `2024` Return | `2025` Return | `2026 YTD` Return | Verdict |
| --- | ---: | ---: | ---: | --- |
| `platform5 any` | `15.614%` | `39.573%` | `14.112%` | canonical all-window control |
| `platform5 after_close` | `15.614%` | `40.103%` | `14.112%` | mild positive-window refinement, inert elsewhere |
| `enterprise4 after_close` | `14.672%` | `41.391%` | `13.430%` | strongest positive-window alias only |
| `software3 any` | `15.279%` | `38.681%` | `12.944%` | weaker than control in all three splits |

## Useful

- `enterprise4 after_close` is a clean positive-window alias inside the master.
- `platform5 any` remains the best all-window control.
- `platform5 after_close` is behaviorally inert in `2024` and `2026 YTD`, which prevents further over-interpretation.

## Not Useful

- `software3` no longer deserves hostile-window master-alias status.
- The split windows do not support unconditional promotion of `enterprise4 after_close`.

## Invalid

- None.

## Next

- Keep the production `IB` paper master unchanged.
- Reclassify `enterprise4 after_close` as the best positive-window static alias.
- If this lane continues, test whether lowering the `enterprise4 after_close` allocation can preserve `2025` upside while reducing hostile/current drag.
