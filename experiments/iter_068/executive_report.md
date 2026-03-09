# iter_068 Executive Report

## Decision

Reject adjacent-bucket promotion. The improved `growth4 BSL` selector did not transfer to the nearby `platform7` large-cap bucket.

## Why

- Original reference on the same sample:
  - `growth4 BSL next-gen pool2`: `21.595%` return, `3.9%` drawdown
- Adjacent bucket results:
  - old selector: `-9.136%`, `10.9%` drawdown
  - next-gen `pool2`: `-9.531%`, `11.1%` drawdown
  - next-gen `pool1`: `-4.847%`, `5.3%` drawdown
- Same-basket passive baseline was only `-1.170%`, so the active selector made the bucket worse.

## Final View

- The improved selector is real inside `growth4`.
- It is not a general-purpose large-cap BSL selector.
- Large-cap progress now requires event-aware or catalyst-aware selection, not more adjacent basket expansion.

## Recommendation

- Freeze the local large-cap view unchanged:
  - `growth4 BSL next-gen` as the current-regime reference
  - `hardware7 failed_breakdown next-gen pool2` as the alternative shadow branch
- Open a cloud-backed earnings lane next.
