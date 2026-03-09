# Iteration `iter_005` Analysis

## Useful

- `candidate_06` (`QQQ 40/180 + 252-day time stop`) was the strongest score of the round at `137.070`. It materially outperformed the `VOO` benchmark on return, Sharpe, and drawdown.
- `candidate_08` (`MSFT 40/180 + 252-day time stop`) also showed a strong transfer of the trend structure, with `70.027%` net profit and `0.711` Sharpe.
- `candidate_09` (`dual_momentum` on `QQQ/VOO/TLT`) was the first non-trend family to produce clearly competitive results. It delivered `60.814%` net profit, `0.724` Sharpe, `13.5%` drawdown, and `15` total orders.
- `candidate_02` (`SPY 40/180 + 252-day time stop`) remains a robust control. It still beat `VOO buy-and-hold` by a large margin with much lower drawdown.
- `candidate_05` (`VOO 40/180 + 252-day time stop`) beat `VOO buy-and-hold` cleanly, which means the time-reset overlay is not only a `SPY` artifact.

## Not Useful

- `candidate_04` (`SPY 40/180 + 252-day time stop + 10% trailing stop`) produced metrics identical to the plain `252-day time stop` control. The trailing stop added no value in this sample.
- `candidate_03` (`SPY 189-day time stop`) increased trade count but degraded score versus the `252-day` control. The reset became too frequent.
- `candidate_07` (`IWM 40/180 + 252-day time stop`) underperformed both the active controls and the passive `VOO` benchmark. Small-cap transfer is weak for this structure.
- `candidate_10` (`QQQ/VOO rotation_rsi`) generated the most activity by far, but the drawdown (`26.0%`) and fee load were too high relative to the achieved Sharpe.

## Invalid Or Process Issues

- No runtime failures occurred this round.
- No compliance violations occurred. The declared blocklist (`GOOG`, `GOOGL`) was enforced and not used by any candidate.
- No symbol in the round suffered the prior ETF data-gap problem; `QQQ`, `VOO`, `TLT`, `IWM`, and `MSFT` all had valid `2022-01-01` to `2024-12-31` local coverage after Polygon backfill.

## Interpretation

- The research loop is now materially better than before because it includes a real passive benchmark, an explicit allowed universe, and a compliance blocklist.
- The current best results are no longer confined to one `SPY` trend rule. The strongest signals now come from:
  - growth-heavy trend exposure (`QQQ`)
  - approved mega-cap trend exposure (`MSFT`)
  - cross-asset momentum rotation (`QQQ/VOO/TLT`)
- The pure trend family still has a low-trade-count problem on its strongest single-asset winners. `QQQ` and `MSFT` look excellent, but they each still closed only `2` trades in-sample.
- `dual_momentum` is the most promising next family because it kept strong risk-adjusted performance while producing meaningfully more decisions than the top single-asset trend candidates.

## Next Round

- Keep `VOO buy-and-hold` as the passive benchmark.
- Keep `SPY 40/180 + 252-day time stop` as the trend-family control.
- Promote `QQQ 40/180 + 252-day time stop` to an aggressive trend control.
- Promote `QQQ/VOO/TLT dual_momentum` to a cross-family control.
- Test nearby `dual_momentum` variants:
  - shorter and longer lookbacks around `126`
  - slower rebalance cadence around `21` days
  - alternate defensive asset rules if needed
- Test whether the strong `QQQ` and `MSFT` trend results survive a stricter validation setup instead of only extending the same in-sample search.
