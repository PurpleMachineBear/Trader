# Iteration 018 Analysis

## Sample Coverage

- Broad sample: `2025-01-02` to `2026-03-06`
- Current regime subset: `2026-01-02` to `2026-03-06`
- Completed candidates: `27 / 27`
- Raw completed rows: `27`
- Unique strategy structures after the reporting label fix: `17`
- Benchmark: `VOO buy-and-hold`

## Decision

- Keep `QQQ/VOO/GLD dual_momentum 126/7` as the daily control.
- Keep `NVDA/TSLA fixed aggressive BSL` as the main all-weather intraday control.
- Promote `NVDA/TSLA fixed aggressive BSL + max_daily_loss_pct 0.75%` only as a conservative overlay candidate, not as the new default engine.
- Treat `dynamic high-beta BSL 120m hold` and `dynamic vwap_reclaim` as `2026 range-regime` branches only. They are not broad-sample replacements yet.

## Key Comparison Table

| Candidate | Window | Structure | Return % | Sharpe | Drawdown % | Trades | Comment |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `candidate_02` | `2025-01-02..2026-03-06` | `QQQ/VOO/GLD dual_momentum 126/7` | 85.669 | 2.125 | 13.9 | 4 | Daily control remains dominant. |
| `candidate_05` | `2025-01-02..2026-03-06` | `NVDA/TSLA fixed aggressive BSL` | 16.303 | 0.567 | 4.8 | 20 | Main stable intraday control. |
| `candidate_06` | `2025-01-02..2026-03-06` | `Dynamic high-beta BSL 240m hold` | 23.828 | 1.076 | 6.8 | 37 | Best broad-sample intraday raw return. |
| `candidate_07` | `2025-01-02..2026-03-06` | `Fixed BSL + daily_loss 0.75%` | 12.736 | 0.308 | 2.1 | 20 | Best broad-sample conservative overlay in this round. |
| `candidate_15` | `2025-01-02..2026-03-06` | `Dynamic vwap_reclaim 120m hold` | 4.356 | -0.391 | 6.5 | 72 | Too active and weak on the broad sample. |
| `candidate_19` | `2026-01-02..2026-03-06` | `QQQ/VOO/GLD dual_momentum 126/7` | 16.769 | 2.578 | 14.1 | 0 | Current regime winner by raw score, mostly via defensive rotation. |
| `candidate_22` | `2026-01-02..2026-03-06` | `NVDA/TSLA fixed aggressive BSL` | 3.443 | 1.849 | 1.2 | 4 | Best all-weather intraday control in the short window too. |
| `candidate_23` | `2026-01-02..2026-03-06` | `Dynamic high-beta BSL 240m hold` | 3.683 | 0.993 | 3.3 | 8 | Dynamic 240m stayed positive, but not efficiently. |
| `candidate_25` | `2026-01-02..2026-03-06` | `Dynamic high-beta BSL 120m hold` | 5.284 | 1.960 | 3.3 | 8 | Shorter hold improved the current range regime. |
| `candidate_27` | `2026-01-02..2026-03-06` | `Dynamic vwap_reclaim 120m hold` | 7.389 | 2.232 | 1.5 | 11 | Best new `2026` exploration branch, but only on the short window. |

## Stability Table

| Structure | Broad Sample Return / DD | `2026 YTD` Return / DD | Read |
| --- | --- | --- | --- |
| `NVDA/TSLA fixed aggressive BSL` | `16.303 / 4.8` | `3.443 / 1.2` | Stable across both windows. |
| `NVDA/TSLA fixed aggressive BSL + daily_loss 0.75%` | `12.736 / 2.1` | `3.000 / 1.6` | Better drawdown control, lower raw return. |
| `Dynamic high-beta BSL 240m hold` | `23.828 / 6.8` | `3.683 / 3.3` | Strong broad sample, weaker current-regime efficiency. |
| `Dynamic high-beta BSL 120m hold` | `8.055 / 5.2` | `5.284 / 3.3` | Regime-specific improvement, not broad-sample robust. |
| `Dynamic vwap_reclaim 120m hold` | `4.356 / 6.5` | `7.389 / 1.5` | Clear short-window edge, not validated outside `2026 YTD`. |

## Yearly Return Table

| Structure | `2025` | `2026 YTD` | Read |
| --- | ---: | ---: | --- |
| `QQQ/VOO/GLD dual_momentum 126/7` | 55.41% | 19.47% | Daily control still carries the campaign. |
| `NVDA/TSLA fixed aggressive BSL` | 7.98% | 7.71% | Best all-weather intraday profile. |
| `Dynamic high-beta BSL 240m hold` | 15.07% | 7.61% | Higher upside than fixed, higher drawdown too. |
| `Fixed BSL + daily_loss 0.75%` | 5.13% | 7.23% | Conservative, not dominant. |
| `Dynamic vwap_reclaim 120m hold` | -5.58% | 10.52% | Current-regime only until proven otherwise. |

## Selection Distribution

The dynamic winners did rotate into a broader high-beta set. The selection expansion was real.

| Candidate | Window | Filled Entry Distribution |
| --- | --- | --- |
| `candidate_06` | Broad sample | `AMD 10`, `TSLA 9`, `AVGO 6`, `NVDA 4`, `MRVL 3`, `MU 3`, `TSM 2` |
| `candidate_25` | `2026 YTD` | `AMD 3`, `AVGO 2`, `TSLA 2`, `MRVL 1` |
| `candidate_27` | `2026 YTD` | `AMD 4`, `TSLA 2`, `MU 2`, `TSM 1`, `NVDA 1`, `MRVL 1` |

## Useful

- Strict context gating still mattered. `context_min_positive = 2` beat the relaxed `1` version across fixed and dynamic BSL branches.
- `NVDA/TSLA fixed aggressive BSL + daily_loss 0.75%` was the cleanest new conservative overlay in this round. It cut broad-sample drawdown from `4.8%` to `2.1%` while keeping `20` trades.
- Bucketed dynamic high-beta BSL remained real. The broad winner did not just relabel `NVDA/TSLA`; it rotated heavily into `AMD`, `AVGO`, `MRVL`, `MU`, and `TSM`.
- The current `2026` range regime did favor faster exits. `Dynamic BSL 120m hold` and `dynamic vwap_reclaim` both improved materially versus the longer-hold dynamic control on the short window.

## Not Useful

- Relaxing the context threshold from `2` to `1` did not help. It lowered quality on both fixed and dynamic BSL branches.
- Removing `TSLA` from the high-beta basket was not useful. The semis-only branch lagged the mixed high-beta branch in both the broad sample and `2026 YTD`.
- Broad-sample `vwap_reclaim` was not robust. The main broad candidate produced only `4.356%` return with `72` trades and a negative Sharpe.
- Dynamic high-beta BSL with `daily_loss 0.75%` was too punitive. It dropped the broad-sample return from `23.828%` to `9.001%` without becoming the best conservative branch.

## Invalid Or Misleading

- The default composite score still over-ranks short `2026 YTD` rows. `candidate_27` looks elite by score, but it has not survived a prior-window validation yet.
- This round exposed a reporting bug: scanner structure labels initially omitted materially important context-gate parameters. That would have merged distinct rows in the stability table. The reporting tool was fixed before final analysis.
- Dynamic broad BSL without the daily-loss guard showed heavy order churn: `554` total orders with `480` cancellations on `37` trades. The guarded variant produced `74` total orders on the same trade count. This is an execution-quality flag until the order-management behavior is explained.

## Next

- Run a targeted validation round on earlier choppy windows for:
  - `fixed BSL + daily_loss 0.75%`
  - `dynamic BSL 120m hold`
  - `dynamic vwap_reclaim 120m hold`
- Inspect the dynamic scanner order-management path that produced high cancellation churn in the unguarded broad-sample BSL rows.
- Add a simple intraday regime router so the research can decide when to prefer:
  - all-weather `fixed NVDA/TSLA BSL`
  - aggressive `dynamic high-beta BSL`
  - shorter-hold `range-regime` branches
