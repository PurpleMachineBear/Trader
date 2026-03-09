# Iteration 093 Analysis

## Sample Coverage

- Recent broad window: `2025-01-02` to `2026-03-06`
- Earlier validation window: `2024-01-02` to `2025-12-31`
- Cloud project: `Cloud_Earnings_Research`
- New style under test: `strategy_style=master_portfolio`
- Event state source: `platform5 pre1` upcoming earnings count from `EODHDUpcomingEarnings`

## Decision

Do not promote cloud event state into the production master as an activation or allocation rule.

The ungated master control remains best. Hard event-state gating sharply reduces intraday participation but does not improve return, Sharpe, or drawdown. A softer allocation tilt preserves trade frequency, but still underperforms the control in both windows.

## Process Check

Before the official round:

- The carryover cloud intraday canary exactly matched the remembered control from `iter_091`.
- A master smoke run matched the local master on the recent broad window closely enough to trust the new cloud style.

## Summary Table

| Candidate | Window | Event State | Return | Sharpe | Drawdown | Orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `candidate_01` | broad | `off` | `59.176%` | `1.836` | `10.9%` | `55` |
| `candidate_02` | broad | `gate >= 1` | `55.517%` | `1.712` | `11.0%` | `11` |
| `candidate_03` | broad | `gate >= 2` | `55.409%` | `1.707` | `11.0%` | `9` |
| `candidate_04` | broad | `tilt 0.30 / 0.10` | `57.531%` | `1.781` | `11.0%` | `55` |
| `candidate_05` | `2024_2025` | `off` | `60.255%` | `1.224` | `6.3%` | `341` |
| `candidate_06` | `2024_2025` | `gate >= 1` | `58.972%` | `1.197` | `6.4%` | `41` |
| `candidate_07` | `2024_2025` | `gate >= 2` | `59.029%` | `1.200` | `6.3%` | `33` |
| `candidate_08` | `2024_2025` | `tilt 0.30 / 0.10` | `59.775%` | `1.217` | `6.3%` | `341` |

## Benchmark Table

### Recent Broad: versus `VOO` and local master

| Structure | Return Delta vs `VOO` | Sharpe Delta vs `VOO` | Drawdown Delta vs `VOO` | Return Delta vs local master | Sharpe Delta vs local master | Drawdown Delta vs local master |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `off` | `+44.713` | `+1.567` | `-8.1` | `+0.030` | `+0.001` | `+0.0` |
| `gate >= 1` | `+41.054` | `+1.443` | `-8.0` | `-3.629` | `-0.123` | `+0.1` |
| `gate >= 2` | `+40.946` | `+1.438` | `-8.0` | `-3.737` | `-0.128` | `+0.1` |
| `tilt 0.30 / 0.10` | `+43.068` | `+1.512` | `-8.0` | `-1.615` | `-0.054` | `+0.1` |

### Earlier Window: versus `VOO` and local master

| Structure | Return Delta vs `VOO` | Sharpe Delta vs `VOO` | Drawdown Delta vs `VOO` | Return Delta vs local master | Sharpe Delta vs local master | Drawdown Delta vs local master |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `off` | `+15.655` | `+0.528` | `-12.5` | `-1.783` | `-0.050` | `+0.1` |
| `gate >= 1` | `+14.372` | `+0.501` | `-12.4` | `-3.066` | `-0.077` | `+0.2` |
| `gate >= 2` | `+14.429` | `+0.504` | `-12.5` | `-3.009` | `-0.074` | `+0.1` |
| `tilt 0.30 / 0.10` | `+15.175` | `+0.521` | `-12.5` | `-2.263` | `-0.057` | `+0.1` |

## Activation Table

| Window | Structure | Orders | Read |
| --- | --- | ---: | --- |
| broad | `off` | `55` | baseline master behavior |
| broad | `gate >= 1` | `11` | event-state gate disables most intraday activity |
| broad | `gate >= 2` | `9` | even stricter, still no quality gain |
| broad | `tilt 0.30 / 0.10` | `55` | same activity as control, only allocation changed |
| `2024_2025` | `off` | `341` | baseline master behavior |
| `2024_2025` | `gate >= 1` | `41` | large activation collapse |
| `2024_2025` | `gate >= 2` | `33` | even lower activation |
| `2024_2025` | `tilt 0.30 / 0.10` | `341` | same activity as control, still worse than control |

## Useful

- The cloud event state can now be wired into the master without causing drift in the older cloud lanes.
- The new cloud master style is valid: recent broad smoke matched the local master almost exactly.
- This round gave a clean answer to the production question:
  - `platform5 pre1` event state is not a good direct switch for the production `NVDA/TSLA` intraday sleeve.

## Not Useful

- Hard gating by `event_state_count >= 1` or `>= 2`
  - both windows lost return and Sharpe
  - both windows cut orders too aggressively
- Simple allocation tilt `0.30 / 0.10`
  - preserved activation
  - but still underperformed the ungated control

## Invalid

- The first `iter_093` cloud submission batch was stale because the newly added `master_portfolio` path missed the method hooks that reused sleeves expect.
- That batch was discarded and rerun from scratch after fixing the runtime plumbing.
- The remaining `master_integration.py` compile warnings are static type warnings from QuantConnect's checker; they do not reflect a surviving runtime failure after the rerun.

## Next

- Keep cloud event state as a `shadow state reference`, not as a production master activation or allocation rule.
- If event state is revisited, use it downstream on:
  - large-cap event branches
  - shadow branch promotion rules
  - or richer external event metadata
- Do not spend more budget on simple `count-based` master gating with the current QuantConnect event metadata.
