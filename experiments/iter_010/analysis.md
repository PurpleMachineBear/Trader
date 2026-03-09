# Iteration `iter_010` Analysis

## Scope

- Raw candidates: `201`
- Status: `201/201 completed` after retry
- Unique structures: `193`
- Sample: `2022-01-01` to `2026-03-06` (`2026 YTD`, latest completed trading day before `2026-03-07`)
- Focus: final deployment refinement around validated GLD-defensive rotation and trend controls
- Benchmark: `VOO buy-and-hold`
- Process check: `201` order-event files inspected, `0` invalid orders

## Deployment Shortlist

| Bucket | Structure | Candidate | Score | Return % | Sharpe | Drawdown % | Trades | Why it matters |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Leveraged ceiling | `TQQQ/VOO/GLD dual_momentum 126/7 1.0x` | `candidate_006` | `452.801` | `412.001` | `1.076` | `33.4` | `10` | Raw-return leader of the whole campaign |
| Leveraged alternate | `TQQQ/SPY/GLD dual_momentum 126/7 1.0x` | `candidate_119` | `452.678` | `411.878` | `1.076` | `33.4` | `10` | Near-identical to the leader, so the middle index proxy matters little here |
| Leveraged deployable | `TQQQ/VOO/GLD dual_momentum 126/7 0.75x` | `candidate_007` | `307.248` | `267.848` | `0.952` | `27.9` | `10` | Current best leveraged compromise |
| Control-grade | `QQQ/VOO/GLD dual_momentum 126/7` | `candidate_005` | `328.189` | `224.389` | `1.316` | `13.9` | `21` | Best non-leveraged control |
| Control-grade alternate | `QQQ/SPY/GLD dual_momentum 126/7` | `candidate_008` | `327.778` | `224.178` | `1.314` | `13.9` | `21` | Confirms robustness across nearby market beta proxy choices |
| Tech-tilted control | `QQQ/XLK/GLD dual_momentum 126/7` | `candidate_059` | `313.789` | `217.589` | `1.240` | `13.9` | `26` | Best `QQQ/XLK/GLD` refinement, slightly ahead of the prior `126/14` control |
| Single-asset active | `GLD sma_regime 18/110 + 189d` | `candidate_175` | `277.323` | `189.423` | `1.155` | `13.8` | `6` | Best single-asset active configuration in the whole project |

## Risk Bucket Table

| Bucket | Count | Avg Score | Median Score | Avg Return % | Avg Sharpe | Avg Drawdown % | Best Structure |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `trend` | `12` | `224.261` | `231.447` | `149.678` | `1.012` | `13.292` | `GLD sma_regime 18/110 + 189d` |
| `non_leveraged_rotation` | `74` | `207.906` | `213.123` | `148.030` | `0.899` | `15.020` | `QQQ/VOO/GLD dual_momentum 126/7` |
| `leveraged` | `111` | `197.961` | `177.003` | `197.794` | `0.715` | `35.643` | `TQQQ/VOO/GLD dual_momentum 126/7 1x` |
| `passive` | `4` | `30.437` | `2.776` | `70.087` | `0.419` | `40.800` | `GLD buy-and-hold` |

Interpretation:

- The single best row is still leveraged, but the average quality of the round was cleaner in `trend` and `non_leveraged_rotation`.
- This is exactly why the project should keep separate deployment buckets instead of forcing one global winner.

## Passive Baseline Table

| Active Structure | Passive Baseline | Score Delta | Excess Return % | Sharpe Delta | Drawdown Delta % | Trades |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `GLD sma_regime 18/110 + 189d` | `GLD buy-and-hold` | `36.197` | `9.097` | `0.127` | `-7.200` | `6` |
| `TQQQ sma_regime 20/120 + 189d 1x` | `TQQQ buy-and-hold` | `380.966` | `244.166` | `0.490` | `-43.900` | `5` |
| `QQQ sma_regime 40/180 + 252d` | `QQQ buy-and-hold` | `123.655` | `54.555` | `0.433` | `-12.900` | `4` |

Interpretation:

- Active timing on `GLD`, `QQQ`, and `TQQQ` all beat their own passive baselines on this full sample.
- That said, the single-asset `TQQQ` trend path is still weaker than the best `TQQQ/*/GLD` rotation path once portfolio-level alternatives are allowed.

## Yearly Return Table

| Strategy | 2022 | 2023 | 2024 | 2025 | 2026 YTD |
| --- | ---: | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | `-20.26%` | `24.33%` | `23.36%` | `16.39%` | `-1.39%` |
| `GLD buy-and-hold` | `0.44%` | `12.69%` | `26.65%` | `63.67%` | `19.48%` |
| `QQQ/VOO/GLD 126/7` | `0.82%` | `38.00%` | `24.00%` | `57.38%` | `19.48%` |
| `TQQQ/VOO/GLD 126/7 1.0x` | `0.82%` | `100.59%` | `61.88%` | `29.28%` | `20.98%` |
| `TQQQ/VOO/GLD 126/7 0.75x` | `0.65%` | `74.32%` | `48.32%` | `22.15%` | `15.73%` |
| `GLD 18/110 + 189d` | `4.10%` | `11.68%` | `25.74%` | `64.75%` | `20.17%` |
| `QQQ/XLK/GLD 126/7` | `-2.57%` | `37.33%` | `26.89%` | `56.55%` | `19.49%` |
| `TQQQ 20/120 + 189d 1.0x` | `0.00%` | `110.03%` | `72.90%` | `8.40%` | `-9.86%` |

Interpretation:

- The report no longer stops at `2024`; the live sample used here runs through `2026-03-06`.
- `2026 YTD` already separates cleaner defensive rotation from pure leveraged beta. The `TQQQ` trend single-asset path is negative `YTD`, while the GLD-defensive rotations remain positive.

## Useful

- `126-day` lookback with `7-day` rebalance remained the center of both the leveraged and non-leveraged GLD-defensive rotation cluster.
- `TQQQ/VOO/GLD 126/7 1.0x` and `TQQQ/SPY/GLD 126/7 1.0x` were effectively tied. The middle broad-market proxy is not the main driver of the leveraged edge.
- `QQQ/VOO/GLD 126/7` remained the best non-leveraged control, and `QQQ/SPY/GLD 126/7` stayed effectively tied.
- `QQQ/XLK/GLD 126/7` slightly improved on the earlier `QQQ/XLK/GLD 126/14` control, so the tech-tilted non-leveraged branch remains viable.
- `GLD sma_regime 18/110 + 189d` improved on the prior `20/120 + 189d` GLD control and is now the best active single-asset GLD specification.
- `TQQQ` trend timing still materially improved on passive `TQQQ buy-and-hold`, which means the trend family still has value as a secondary high-risk track.

## Not Useful

- More micro-tuning around leveraged `126` lookback variants with `5` or `10` day rebalance did not beat `126/7`.
- The `133` and `147` lookback variants produced some respectable second-tier candidates, but they did not replace `126` as the main deployment choice.
- The final `QQQ/VOO/TLT` legacy baselines remained far below the GLD-defensive cluster. The best final legacy row scored only `72.063`.
- `TQQQ buy-and-hold` remained a poor full-sample deployment reference despite looking strong in isolated subperiods.

## Invalid Or Process Issues

- First pass had `11` process-level failures, all resolved by `--only-failed --jobs 4`.
- No strategy-level invalid-order issue appeared in this round. Order-event inspection found `0` invalid events.
- This round had `201` raw candidates but only `193` unique structures. Reporting by `candidate_id` alone would have overstated how much new evidence the round actually produced.

## Experiment Design Problems

- The campaign is now near diminishing returns for local parameter sweeps inside the same GLD-defensive family. Another brute-force round around the same `126/7` neighborhood is unlikely to add much.
- The sample still begins at `2022-01-01`. That is better than stopping at `2024`, but it is still short for deployment confidence and still regime-specific.
- Full-sample ranking alone still over-rewards leverage. Bucketed interpretation is mandatory.
- Several candidates in the final round were intentional aliases or near-duplicates for control coverage. That is acceptable for execution, but analysis must deduplicate them.
- The current universe is strong for ETF rotation research, but still narrow. Further expansion should be rule-based, not ad hoc ticker collecting.

## Next Round

- Stop broad local optimization. The project has now completed `1004` official experiments across `iter_006` to `iter_010`.
- Use the next round for validation, not discovery:
  - extend history earlier than `2022` where data quality allows
  - keep separate final tracks for `leveraged`, `non-leveraged`, and `single-asset trend`
  - run walk-forward or rolling-window validation instead of one more dense parameter grid
  - keep `VOO buy-and-hold` as the common benchmark
  - keep `GLD buy-and-hold` and same-symbol passive baselines for single-asset active candidates
- If the universe expands again, do it intentionally:
  - unleveraged ETF additions should be chosen by role
  - leveraged ETF additions such as `TQQQ`-style proxies should remain in a separate risk bucket
