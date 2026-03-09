# Iteration `iter_007` Analysis

## Scope

- Candidates: `201`
- Status: `201/201 completed`
- Sample: `2022-01-01` to `2026-03-06`
- Focus: exploit around `GLD` defensive rotation, tighter `GLD/QQQ/TQQQ` trend sweeps, same-symbol passive references
- Benchmark: `VOO buy-and-hold`

## Summary Table

| Candidate | Description | Score | Return % | Sharpe | Drawdown % | Trades |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_101` | `TQQQ/VOO/GLD dual_momentum`, `126d`, `7d` | `452.801` | `412.001` | `1.076` | `33.4` | `10` |
| `candidate_104` | `TQQQ/VOO/GLD dual_momentum`, `126d`, `21d` | `433.404` | `402.704` | `1.047` | `37.0` | `9` |
| `candidate_081` | `TQQQ/QQQ/GLD dual_momentum`, `126d`, `7d` | `423.825` | `386.725` | `1.039` | `33.4` | `9` |
| `candidate_022` | `QQQ/VOO/GLD dual_momentum`, `126d`, `7d` | `328.189` | `224.389` | `1.316` | `13.9` | `21` |
| `candidate_041` | `QQQ/SPY/GLD dual_momentum`, `126d`, `7d` | `327.778` | `224.178` | `1.314` | `13.9` | `21` |
| `candidate_061` | `QQQ/XLK/GLD dual_momentum`, `126d`, `7d` | `313.789` | `217.589` | `1.240` | `13.9` | `26` |
| `candidate_135` | `GLD sma_regime`, `20/120`, `189d` | `260.720` | `178.620` | `1.097` | `13.8` | `6` |
| `candidate_146` | `TQQQ sma_regime`, `20/120`, `189d` | `256.036` | `254.836` | `0.760` | `37.4` | `5` |
| `candidate_008` | `GLD buy-and-hold` | `241.126` | `180.326` | `1.028` | `21.0` | `0` |
| `candidate_171` | `GLD donchian_regime`, `50/25`, `189d` | `235.468` | `159.168` | `1.041` | `13.9` | `4` |

## Family Table

| Family | Count | Avg Score | Median Score | Avg Return % | Avg Sharpe | Avg Drawdown % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `dual_momentum` | `121` | `188.721` | `179.512` | `158.369` | `0.760` | `22.820` |
| `sma_regime` | `38` | `113.426` | `90.237` | `105.326` | `0.574` | `24.632` |
| `donchian_regime` | `20` | `90.994` | `67.503` | `101.524` | `0.528` | `31.670` |
| `rotation_rsi` | `12` | `81.436` | `73.954` | `108.462` | `0.463` | `36.667` |
| `buy_and_hold` | `10` | `-29.013` | `-4.587` | `36.377` | `0.019` | `33.660` |

## Yearly Return Table

| Candidate | 2022 | 2023 | 2024 | 2025 | 2026 YTD |
| --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_001` `VOO buy-and-hold` | `-20.26%` | `24.33%` | `23.36%` | `16.39%` | `-1.39%` |
| `candidate_008` `GLD buy-and-hold` | `0.44%` | `12.69%` | `26.65%` | `63.67%` | `19.48%` |
| `candidate_013` `QQQ/VOO/GLD 126d/10d` | `-7.44%` | `37.67%` | `23.70%` | `53.16%` | `19.60%` |
| `candidate_022` `QQQ/VOO/GLD 126d/7d` | `0.82%` | `38.00%` | `24.00%` | `57.38%` | `19.48%` |
| `candidate_101` `TQQQ/VOO/GLD 126d/7d` | `0.82%` | `100.59%` | `61.88%` | `29.28%` | `20.98%` |

## Useful

- `GLD` defensive rotation was confirmed decisively. The strongest triplets were no longer isolated points:
  - `QQQ/VOO/GLD`
  - `QQQ/SPY/GLD`
  - `QQQ/XLK/GLD`
  - `TQQQ/QQQ/GLD`
  - `TQQQ/VOO/GLD`
- The parameter cluster tightened rather than dispersing. The best results consistently sat around `126-day` lookback and `7-14` day rebalance.
- The best non-leveraged exploit was `candidate_022` (`QQQ/VOO/GLD`, `126d`, `7d`) with `224.389%` return, `1.316` Sharpe, and only `13.9%` drawdown.
- The best raw-return exploit was `candidate_101` (`TQQQ/VOO/GLD`, `126d`, `7d`) with `412.001%` return and `1.076` Sharpe. This confirmed that the leveraged path is powerful enough to merit its own risk bucket.
- `GLD 20/120 + 189-day time stop` became the best single-asset active GLD strategy of the campaign so far. It slightly trailed passive `GLD` on raw return but improved Sharpe and cut drawdown by about `7.2` points.
- `TQQQ 20/120 + 189-day time stop` remained a viable high-risk timing path. It beat passive `TQQQ` by `244.166` percentage points of return and reduced drawdown by `43.9` points.

## Not Useful

- The legacy `QQQ/VOO/TLT` control was clearly dominated. Its score (`66.084`) was far below the GLD-defensive exploit cluster.
- `rotation_rsi` improved only cosmetically. It still required very high order counts and drawdown to produce its results.
- `donchian_regime` remained secondary. It was still useful on `GLD`, but the family did not challenge the best dual-momentum cluster.
- `IWM` and the old `TLT/IEF` defensive logic remained low-priority after the exploit batch. The round did not produce evidence that they deserved a renewed full-family sweep.

## Invalid Or Process Issues

- No template-level execution bug appeared this round.
- The latest `dual_momentum` order-event files again showed `0` invalid orders, which confirmed the template repair from `iter_006`.
- A small number of process-level failures occurred during the first pass and were cleared by a standard `--only-failed` retry.

## Experiment Design Issues

- This round made the leverage problem explicit. A single composite score is not enough once `TQQQ/*/GLD` variants enter the same ranking as unleveraged controls.
- The correct interpretation is now:
  - raw-return leader: leveraged `TQQQ/*/GLD`
  - control-grade leader: unleveraged `QQQ/*/GLD`
- The next rounds should preserve that split instead of pretending one ranking can serve both use cases.

## Next Round

- Keep `VOO buy-and-hold` as the common benchmark.
- Keep `QQQ/VOO/GLD 126d/10d` as the main non-leveraged rotation control.
- Keep `QQQ/VOO/TLT 126d/21d` as a legacy control only long enough to confirm its continued inferiority.
- Start a dedicated leveraged track around `TQQQ/*/GLD` using explicit `position_size` scaling.
- Keep a non-leveraged track around:
  - `QQQ/VOO/GLD`
  - `QQQ/SPY/GLD`
  - `QQQ/XLK/GLD`
- Refine `GLD` and `TQQQ` timing strategies with smaller, more targeted trend grids.
