# Iteration 099 Analysis

## Sample Coverage

- Recent broad window: `2025-01-02` to `2026-03-06`
- Hostile window: `2024-01-02` to `2024-12-31`
- Positive window: `2025-01-02` to `2025-12-31`
- Sparse current window: `2026-01-02` to `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`
- Alias under test: `enterprise4 after_close` with reduced `event_sleeve_allocation`

## Decision

Lowering `enterprise4 after_close` allocation does not solve the regime-sensitivity problem.

The best reduced-allocation compromise was `7.5%`, but it still failed to beat the canonical `platform5 any 10%` control in `2024` and `2026 YTD`. The smaller `5%` version was even less compelling because it gave up too much broad-window and positive-window edge while still not improving risk enough.

This means `enterprise4 after_close` should stay classified as a `positive-window alias`, and sleeve-size micro-tuning is now exhausted for this lane.

## Summary Table

| Candidate | Window | Structure | Return | Sharpe | Drawdown | Orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `candidate_01` | broad | `platform5 any 10%` canary | `60.602%` | `2.068` | `9.9%` | `124` |
| `candidate_02` | broad | `enterprise4 after_close 5%` | `60.574%` | `1.979` | `10.7%` | `94` |
| `candidate_03` | broad | `enterprise4 after_close 7.5%` | `61.270%` | `2.047` | `10.6%` | `95` |
| `candidate_04` | `2024` | `platform5 any 10%` control | `15.614%` | `0.602` | `5.5%` | `345` |
| `candidate_05` | `2024` | `enterprise4 after_close 5%` | `15.094%` | `0.560` | `5.5%` | `329` |
| `candidate_06` | `2024` | `enterprise4 after_close 7.5%` | `14.945%` | `0.555` | `5.1%` | `330` |
| `candidate_07` | `2025` | `platform5 any 10%` control | `39.573%` | `2.035` | `4.8%` | `96` |
| `candidate_08` | `2025` | `enterprise4 after_close 5%` | `39.145%` | `1.968` | `5.1%` | `73` |
| `candidate_09` | `2025` | `enterprise4 after_close 7.5%` | `40.356%` | `2.072` | `4.9%` | `73` |
| `candidate_10` | `2026 YTD` | `platform5 any 10%` control | `14.112%` | `2.830` | `9.8%` | `26` |
| `candidate_11` | `2026 YTD` | `enterprise4 after_close 5%` | `14.379%` | `2.725` | `10.6%` | `20` |
| `candidate_12` | `2026 YTD` | `enterprise4 after_close 7.5%` | `13.937%` | `2.684` | `10.5%` | `21` |

## Tradeoff Table

| Window | Control `platform5 any 10%` | `enterprise4 after_close 5%` delta | `enterprise4 after_close 7.5%` delta | Verdict |
| --- | ---: | ---: | ---: | --- |
| broad | `60.602 / 2.068 / 9.9` | `-0.028 return`, `-0.089 Sharpe`, `+0.8 DD` | `+0.668 return`, `-0.021 Sharpe`, `+0.7 DD` | `7.5%` helps return only |
| `2024` | `15.614 / 0.602 / 5.5` | `-0.520 return`, `-0.042 Sharpe`, `+0.0 DD` | `-0.669 return`, `-0.047 Sharpe`, `-0.4 DD` | neither beats hostile control |
| `2025` | `39.573 / 2.035 / 4.8` | `-0.428 return`, `-0.067 Sharpe`, `+0.3 DD` | `+0.783 return`, `+0.037 Sharpe`, `+0.1 DD` | `7.5%` keeps positive-window edge |
| `2026 YTD` | `14.112 / 2.830 / 9.8` | `+0.267 return`, `-0.105 Sharpe`, `+0.8 DD` | `-0.175 return`, `-0.146 Sharpe`, `+0.7 DD` | neither improves current window cleanly |

## Reference Table

### Reduced allocations versus the prior full-size positive-window alias from `iter_098`

| Window | `enterprise4 after_close 10%` | `5%` delta | `7.5%` delta |
| --- | ---: | ---: | ---: |
| broad | `61.714 / 2.105 / 10.5` | `-1.140 return`, `-0.126 Sharpe`, `+0.2 DD` | `-0.444 return`, `-0.058 Sharpe`, `+0.1 DD` |
| `2024` | `14.672 / 0.537 / 5.5` | `+0.422 return`, `+0.023 Sharpe`, `+0.0 DD` | `+0.273 return`, `+0.018 Sharpe`, `-0.4 DD` |
| `2025` | `41.391 / 2.157 / 4.7` | `-2.246 return`, `-0.189 Sharpe`, `+0.4 DD` | `-1.035 return`, `-0.085 Sharpe`, `+0.2 DD` |
| `2026 YTD` | `13.430 / 2.639 / 10.4` | `+0.949 return`, `+0.086 Sharpe`, `+0.2 DD` | `+0.507 return`, `+0.045 Sharpe`, `+0.1 DD` |

## Useful

- `enterprise4 after_close 7.5%` is the best reduced-allocation compromise.
- The positive-window alias still exists after reducing size; it was strongest in `2025` and slightly ahead on the recent broad window.
- The smaller `5%` sleeve did not rescue the branch; it mostly diluted the positive-window edge.

## Not Useful

- Lowering sleeve size does not make `enterprise4 after_close` an all-weather overlay.
- Neither reduced-allocation row beats the canonical `platform5 any 10%` control in both hostile and current windows.

## Invalid

- None.

## Next

- Stop spending budget on event-sleeve allocation micro-tuning for this alias.
- Keep `platform5 any 10%` as the canonical cloud event-sleeve control.
- Keep `enterprise4 after_close` as the best positive-window alias only.
- If this lane continues, move to richer metadata or a real positive-window classifier instead of more sleeve-size tuning.
