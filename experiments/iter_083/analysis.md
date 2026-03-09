# Iter 083 Analysis

## Sample Coverage

- Cloud project: `Cloud_Earnings_Research`
- Recent broad window: `2025-01-02` to `2026-03-06`
- Earlier aggregate window: `2024-01-02` to `2025-12-31`
- Family under test: `platform5 pre1 hold3`
- New knobs: `QQQ/XLK` tape-state gates and `after_close` interaction

## Summary Table

| Candidate | Window | Structure | Return | Sharpe | Drawdown | Orders | Score |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_01` | `broad` | control | `100.059%` | `1.508` | `10.1%` | `89` | `230.659` |
| `candidate_02` | `broad` | `QQQ/XLK positive tape` | `78.127%` | `1.255` | `12.5%` | `59` | `178.627` |
| `candidate_03` | `broad` | `QQQ/XLK weak tape` | `5.346%` | `-0.169` | `9.0%` | `17` | `-29.554` |
| `candidate_04` | `broad` | `after_close + positive tape` | `78.127%` | `1.255` | `12.5%` | `59` | `178.627` |
| `candidate_05` | `broad` | `after_close + weak tape` | `-3.204%` | `-1.240` | `9.0%` | `9` | `-145.204` |
| `candidate_06` | `2024_2025` | control | `93.491%` | `0.806` | `21.7%` | `153` | `130.691` |
| `candidate_07` | `2024_2025` | `QQQ/XLK positive tape` | `84.154%` | `0.772` | `19.5%` | `73` | `122.354` |
| `candidate_08` | `2024_2025` | `QQQ/XLK weak tape` | `-1.873%` | `-0.390` | `22.9%` | `48` | `-86.673` |

## Useful

- Simple `QQQ/XLK` tape gating also failed to improve the canonical cloud branch.
- The ungated `platform5 pre1 hold3` control stayed best in both windows.
- Positive tech tape was not the main hidden driver.
  - Recent broad dropped from `100.059%` to `78.127%`.
  - `2024_2025` dropped from `93.491%` to `84.154%`.
- Weak tape was actively harmful.
  - Recent broad fell to `5.346%`.
  - `2024_2025` fell to `-1.873%`.
- `after_close + positive tape` was behaviorally inert relative to `positive tape`.
  - Same return, Sharpe, drawdown, and order count.
  - This implies the positive-tape subset in the recent broad sample was already effectively an `after_close` subset.
- `after_close + weak tape` was clearly invalid as a branch candidate.

## Not Useful

- Simple market/sector tape gates are still too coarse for this cloud lane.
- The branch is not well explained by:
  - pre-event single-name pullback/strength
  - broad `QQQ/XLK` positive tape
  - broad `QQQ/XLK` weak tape

## Invalid

- No strategy-invalid rows this round.
- Cloud execution completed without stale-code issues.

## Interpretation

This narrows the event-state problem further:

- The cloud edge is real.
- But it is not a one-dimensional state conditional on trailing single-name return.
- And it is not a one-dimensional state conditional on simple `QQQ/XLK` tape.

That leaves richer event metadata as the more likely explanation:

- report-time interactions beyond the simple aggregate split
- estimate availability or estimate dispersion
- symbol-specific event quality
- possibly more specific sector-state or macro-conflict metadata

## Next

- Stop spending cloud budget on simple tape gating.
- Keep `platform5 pre1 hold3` as the canonical cloud control.
- The next cloud round should focus on richer event metadata rather than more state slicing:
  - estimate-required versus unrestricted
  - symbol-quality plus report-time interaction
  - macro-conflict or sector-conflict overlays if accessible
