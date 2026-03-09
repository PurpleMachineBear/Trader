# Iteration `iter_006` Analysis

## Scope

- Candidates: `201`
- Status: `201/201 completed`
- Sample: `2022-01-01` to `2026-03-06`
- Universe: `SPY`, `VOO`, `QQQ`, `TQQQ`, `DIA`, `TLT`, `IEF`, `GLD`, `XLK`, approved stock references
- Benchmark: `VOO buy-and-hold`

## Summary Table

| Candidate | Description | Score | Return % | Sharpe | Drawdown % | Trades |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_171` | `QQQ/VOO/GLD dual_momentum`, `126d`, `10d` | `275.941` | `188.741` | `1.150` | `13.9` | `20` |
| `candidate_172` | `QQQ/VOO/GLD dual_momentum`, `126d`, `21d` | `267.574` | `184.074` | `1.111` | `13.8` | `12` |
| `candidate_046` | `GLD sma_regime`, `30/150`, `252d` | `257.801` | `175.601` | `1.100` | `13.9` | `4` |
| `candidate_045` | `GLD sma_regime`, `50/200`, `252d` | `245.365` | `167.765` | `1.052` | `13.8` | `4` |
| `candidate_170` | `QQQ/VOO/GLD dual_momentum`, `126d`, `5d` | `244.572` | `168.072` | `1.041` | `13.8` | `18` |
| `candidate_004` | `GLD buy-and-hold` | `241.126` | `180.326` | `1.028` | `21.0` | `0` |
| `candidate_043` | `GLD sma_regime`, `40/180`, `252d` | `240.663` | `164.063` | `1.046` | `14.0` | `4` |
| `candidate_090` | `GLD donchian_regime`, `50/25`, `189d` | `235.468` | `159.168` | `1.041` | `13.9` | `4` |
| `candidate_026` | `TQQQ sma_regime`, `40/180`, `315d` | `193.927` | `243.527` | `0.702` | `59.9` | `3` |
| `candidate_191` | `TQQQ/QQQ rotation_rsi`, `70/35` | `132.560` | `183.260` | `0.595` | `55.1` | `163` |

## Family Table

| Family | Count | Avg Score | Median Score | Avg Return % | Avg Sharpe | Avg Drawdown % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `sma_regime` | `48` | `69.427` | `78.376` | `82.500` | `0.323` | `22.692` |
| `rotation_rsi` | `16` | `56.008` | `58.880` | `84.783` | `0.385` | `33.638` |
| `donchian_regime` | `48` | `21.138` | `28.674` | `59.455` | `0.090` | `23.673` |
| `dual_momentum` | `84` | `20.105` | `15.427` | `53.923` | `0.189` | `26.352` |
| `buy_and_hold` | `5` | `-17.233` | `0.381` | `48.447` | `0.165` | `41.100` |

## Yearly Return Table

| Candidate | 2022 | 2023 | 2024 | 2025 | 2026 YTD |
| --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_001` `VOO buy-and-hold` | `-20.26%` | `24.33%` | `23.36%` | `16.39%` | `-1.39%` |
| `candidate_004` `GLD buy-and-hold` | `0.44%` | `12.69%` | `26.65%` | `63.67%` | `19.48%` |
| `candidate_006` `SPY 40/180 + 252d` | `0.00%` | `19.06%` | `24.51%` | `13.46%` | `-0.13%` |
| `candidate_007` `QQQ 40/180 + 252d` | `0.00%` | `37.98%` | `27.34%` | `17.95%` | `-2.41%` |
| `candidate_171` `QQQ/VOO/GLD 126d/10d` | `-7.44%` | `37.67%` | `23.70%` | `53.16%` | `19.60%` |

## Useful

- `QQQ/VOO/GLD dual_momentum` became the strongest family configuration after the dual-momentum execution bug was fixed. The winning cluster was tightly concentrated around `126-day` lookback with `10-21` day rebalance.
- `GLD` was the most important single-asset discovery of the round. It won in passive form, in SMA trend form, and in Donchian breakout form.
- `GLD 30/150 + 252-day time stop` was especially useful because it preserved most of `GLD buy-and-hold` return while cutting drawdown by about `7.1` percentage points.
- `QQQ 40/180 + 252-day time stop` remained a valid aggressive control on the extended sample. It still beat passive `QQQ` by `54.555` percentage points of return with materially lower drawdown.
- `TQQQ` timing is worth continuing. `TQQQ 40/180 + 315-day time stop` beat passive `TQQQ` by `232.857` percentage points of return and reduced drawdown by `21.4` points, even though the absolute drawdown remained high.
- `12%` trailing stops improved `SPY` and `VOO` on the extended sample. The earlier conclusion that trailing stops were always inactive no longer holds across the longer window.

## Not Useful

- `IEF` remained a poor single-asset research target. Its best single-asset score in the round was still strongly negative.
- `TLT` and `IEF` were weak defensive legs for most rotation triplets. Outside the `QQQ/VOO/GLD` cluster, most dual-momentum triplets centered on `TLT` or `IEF` were mediocre or negative on average.
- `rotation_rsi` produced some strong headline returns, but it still came with excessive turnover and drawdown. The best `TQQQ/QQQ` variant generated `219` orders and `55.1%` drawdown.
- `donchian_regime` was not a generally strong family. It was compelling on `GLD` and selectively on `TQQQ`, but weak on `SPY`, `DIA`, and `IEF`.

## Invalid Or Process Issues

- The first `iter_006` batch at `--jobs 10` produced Docker container race failures. The round only became valid after retrying failed candidates at lower concurrency.
- The first `dual_momentum` results were invalid for research purposes because same-bar rotation logic generated invalid orders.
- `dual_momentum` was repaired by introducing staged rotation with a `pending_target`, then rerun.
- `worker.py` now clears the candidate `backtest/` directory before each run so reruns cannot accidentally mix old and new artifacts.
- After the template fix and reruns, the latest `dual_momentum` order-event files showed `0` invalid orders.

## Experiment Design Issues

- A single common benchmark is not enough when the universe spans `VOO`, `GLD`, `TQQQ`, `TLT`, and `IEF`. The round showed that single-asset winners must also be judged against their own passive baseline when available.
- The extended sample is now long enough to expose a regime shift, but it is still one continuous in-sample window. The next phase needs a stricter validation split or walk-forward structure.
- Family averages alone were not sufficient because one strong asset regime (`GLD`) could dominate multiple families at once. Triplet-level and symbol-level breakdowns were necessary to interpret the batch correctly.

## Next Round

- Keep `VOO buy-and-hold` as the campaign benchmark.
- Keep `QQQ 40/180 + 252-day time stop` as the aggressive trend control.
- Promote `QQQ/VOO/GLD dual_momentum` with `126-day` lookback and `10-21` day rebalance as the main rotation control.
- Keep `GLD buy-and-hold` as a reference whenever GLD-driven active candidates are being judged.
- Add same-symbol passive references for `SPY`, `DIA`, `XLK`, and `IEF`.
- Spend the next batch on:
  - `QQQ/VOO/GLD` nearby exploit variants
  - nearby `GLD` SMA and Donchian trend variants
  - selective `TQQQ` timing variants
- Deprioritize broad new sweeps of `TLT` and `IEF` defensive rotations until they show stronger evidence.
