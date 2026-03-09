# Iter 082 Analysis

## Sample Coverage

- Cloud project: `Cloud_Earnings_Research`
- Recent broad window: `2025-01-02` to `2026-03-06`
- Earlier aggregate window: `2024-01-02` to `2025-12-31`
- Family under test: `platform5 pre1 hold3`
- New knob: hard pre-event trailing-return state gates

## Summary Table

| Candidate | Window | State Gate | Return | Sharpe | Drawdown | Orders | Score |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_01` | `broad` | none | `100.059%` | `1.508` | `10.1%` | `89` | `230.659` |
| `candidate_02` | `broad` | `recent_return <= 0` | `64.432%` | `1.083` | `10.1%` | `48` | `152.532` |
| `candidate_03` | `broad` | `recent_return <= -5%` | `15.600%` | `0.293` | `13.4%` | `20` | `18.100` |
| `candidate_04` | `broad` | `recent_return >= 0` | `4.755%` | `-0.073` | `16.7%` | `43` | `-35.945` |
| `candidate_05` | `2024_2025` | none | `93.491%` | `0.806` | `21.7%` | `153` | `130.691` |
| `candidate_06` | `2024_2025` | `recent_return <= 0` | `30.957%` | `0.294` | `25.8%` | `68` | `8.757` |
| `candidate_07` | `2024_2025` | `recent_return <= -5%` | `18.352%` | `0.099` | `9.1%` | `15` | `10.052` |
| `candidate_08` | `2024_2025` | `recent_return >= 0` | `38.691%` | `0.462` | `10.8%` | `81` | `63.291` |

## Useful

- The ungated `platform5 pre1 hold3` control stayed decisively best in both windows.
- A simple hard pullback gate is directionally wrong for this branch.
  - Recent broad fell from `100.059%` to `64.432%` with a mild pullback gate and to `15.600%` with a deeper pullback gate.
  - `2024_2025` fell from `93.491%` to `30.957%` and `18.352%` on the same gates.
- A pure positive-state gate is also wrong.
  - Recent broad strength-only collapsed to `4.755%` with negative Sharpe.
  - `2024_2025` strength-only was better than pullback-only but still far behind the ungated control.
- The branch is not a simple `pre-earnings pullback rebound` and not a simple `pre-earnings strength continuation` either.
- This is useful because it narrows the event-state problem:
  - the current alpha likely comes from a mixed set of pre-event states
  - the next metadata should describe event quality more directly than trailing return alone

## Not Useful

- Hard state slicing on trailing `15`-day return is too crude.
- Using recent-return sign as a promotion filter would have degraded the canonical cloud branch in both validation windows.

## Invalid

- Two cloud submissions initially hit QuantConnect backtest rate limits. They were rerun and completed successfully.
- This was an operational cloud artifact, not strategy failure.

## Data QA

- A local data integrity audit now exists at [data_integrity_audit_20260308.md](/Users/chenchien/lean/experiments/data_integrity_audit_20260308.md).
- The earlier factor-file truncation problem has been corrected for active daily symbols such as `QQQ/SPY/NVDA/TSLA/AMD/MU/TSM/MRVL/AVGO/XLK`.
- A separate rename-history issue remains for local `META` daily data:
  - it has a `132`-day internal gap caused by local ticker-history discontinuity
  - this does not invalidate the current `2024+` large-cap or cloud event conclusions
  - but it means local `META` daily work over `2022` should not be trusted without a rename-aware fix
- Missing minute data for `VOO/GLD/QLD/SSO` is not a blocker because those names are only used in daily families.

## Next

- Do not spend the next round on more hard `recent_return` slicing.
- The next event-state pass should target richer state metadata:
  - `after_close` versus `any` combined with state
  - estimate availability or estimate quality if accessible
  - sector tape / market-state overlays instead of symbol trailing return alone
- Keep `platform5 pre1 hold3` as the canonical cloud control.
- Keep the frozen `IB` paper master unchanged.
