# Iteration 096 Analysis

## Sample Coverage

- Canary window: `2025-01-02` to `2026-03-06`
- Split windows:
  - `2024-01-02` to `2024-12-31`
  - `2025-01-02` to `2025-12-31`
  - `2026-01-02` to `2026-03-06`
  - `2024-01-02` to `2025-12-31`
- Cloud project: `Cloud_Earnings_Research`
- Base branch under test: `platform5 sleeve 10%`
- New regime proxies under test:
  - `event_sleeve_core_state_filter=offensive_only`
  - `event_sleeve_min_active_events=2`

## Decision

Current coarse positive-event regime detection is not solved.

`offensive_only` is not a usable positive-event regime detector. It improves the hostile `2024` window, but it materially weakens `2025`, weakens `2026 YTD`, and underperforms the aggregate `2024_2025` control.

`min_active_events=2` is clearly worse. It underperforms the control in every tested window and should be treated as an exhausted coarse proxy.

The production `IB` paper master stays unchanged. The cloud event sleeve remains a `positive-window shadow sleeve`, not a production-on switch.

## Process Check

- The broad canary exactly matched `iter_094 candidate_02`:
  - `60.602%`, `Sharpe 2.068`, `DD 9.9%`, `124` orders
- This means the new regime-proxy knobs did not distort the carryover `platform5 sleeve 10%` control path.

## Summary Table

| Candidate | Window | Regime Proxy | Return | Sharpe | Drawdown | Orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `candidate_01` | broad | `ungated canary` | `60.602%` | `2.068` | `9.9%` | `124` |
| `candidate_02` | `2024` | `control` | `15.614%` | `0.602` | `5.5%` | `345` |
| `candidate_03` | `2024` | `offensive_only` | `17.791%` | `0.780` | `5.3%` | `322` |
| `candidate_04` | `2024` | `min_active_events=2` | `13.429%` | `0.475` | `5.3%` | `299` |
| `candidate_05` | `2025` | `control` | `39.573%` | `2.035` | `4.8%` | `96` |
| `candidate_06` | `2025` | `offensive_only` | `31.964%` | `1.654` | `4.8%` | `52` |
| `candidate_07` | `2025` | `min_active_events=2` | `31.040%` | `1.593` | `4.8%` | `52` |
| `candidate_08` | `2026 YTD` | `control` | `14.112%` | `2.830` | `9.8%` | `26` |
| `candidate_09` | `2026 YTD` | `offensive_only` | `13.370%` | `2.643` | `9.6%` | `11` |
| `candidate_10` | `2026 YTD` | `min_active_events=2` | `12.054%` | `2.304` | `10.4%` | `18` |
| `candidate_11` | `2024_2025` | `offensive_only` | `56.834%` | `1.260` | `5.5%` | `373` |
| `candidate_12` | `2024_2025` | `min_active_events=2` | `49.867%` | `1.088` | `5.5%` | `350` |

## Knob Sensitivity Table

| Window | Control | `offensive_only` delta | `min_active_events=2` delta | Verdict |
| --- | ---: | ---: | ---: | --- |
| `2024` | `15.614% / 0.602 / 5.5%` | `+2.177 return`, `+0.178 Sharpe`, `-0.2 DD` | `-2.185 return`, `-0.127 Sharpe`, `-0.2 DD` | `offensive_only` helps only hostile window |
| `2025` | `39.573% / 2.035 / 4.8%` | `-7.609 return`, `-0.381 Sharpe`, `+0.0 DD` | `-8.533 return`, `-0.442 Sharpe`, `+0.0 DD` | both proxies materially harmful |
| `2026 YTD` | `14.112% / 2.830 / 9.8%` | `-0.742 return`, `-0.187 Sharpe`, `-0.2 DD` | `-2.058 return`, `-0.526 Sharpe`, `+0.6 DD` | both proxies harmful |
| `2024_2025` | `62.646% / 1.362 / 5.4%` | `-5.812 return`, `-0.102 Sharpe`, `+0.1 DD` | `-12.779 return`, `-0.274 Sharpe`, `+0.1 DD` | both proxies fail aggregate validation |

## Benchmark Table

### Recent broad reference: versus `VOO`, local master, and cloud master control

| Structure | Delta vs `VOO` Return | Delta vs local master Return | Delta vs cloud master control Return | Delta vs cloud master control Drawdown |
| --- | ---: | ---: | ---: | ---: |
| `platform5 sleeve 10%` canary | `+46.139` | `+1.456` | `+1.426` | `-1.0` |

### Split windows: regime proxies versus canonical `platform5 sleeve 10%` control

| Window | Proxy | Return Delta vs control | Sharpe Delta vs control | Drawdown Delta vs control | Orders Delta vs control |
| --- | --- | ---: | ---: | ---: | ---: |
| `2024` | `offensive_only` | `+2.177` | `+0.178` | `-0.2` | `-23` |
| `2024` | `min_active_events=2` | `-2.185` | `-0.127` | `-0.2` | `-46` |
| `2025` | `offensive_only` | `-7.609` | `-0.381` | `+0.0` | `-44` |
| `2025` | `min_active_events=2` | `-8.533` | `-0.442` | `+0.0` | `-44` |
| `2026 YTD` | `offensive_only` | `-0.742` | `-0.187` | `-0.2` | `-15` |
| `2026 YTD` | `min_active_events=2` | `-2.058` | `-0.526` | `+0.6` | `-8` |

## Useful

- `offensive_only` is a real hostile-window cleaner.
  - It improved `2024` return, Sharpe, and drawdown together.
- The canary matched exactly, so this round is trustworthy.
- `min_active_events=2` is now cleanly falsified and should not receive more budget.

## Not Useful

- `offensive_only` is not a positive-event regime detector.
  - It helped `2024`, but clearly damaged `2025`, `2026 YTD`, and `2024_2025`.
- Same-day event breadth is not the right regime representation.
  - Requiring at least two events harmed every tested window.

## Invalid

- None.

## Next

- Stop spending budget on coarse count-based or simple offensive-core regime proxies for the event sleeve.
- Keep `platform5 sleeve 10%` as the canonical cloud event-sleeve control.
- If this lane continues, the next step should be richer event metadata or a true positive-window classifier, not another coarse gate.
