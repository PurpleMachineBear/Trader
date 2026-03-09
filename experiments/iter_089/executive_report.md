# iter_089 executive report

## Decision

Keep the cloud event-aware intraday lane and switch its control from `weak-only BSL` to `no-weakness BSL`.

## What Changed

- Removing the `recent weakness` requirement improved the branch in both windows.
- The score formula choice between `absolute` and `none` did not matter once that filter was removed.

## Winner

`platform5 pre1 intraday BSL` with:

- no recent-weakness requirement
- `selection_pool_size = 2`
- standard `QQQ/XLK` minute context gate

## Recommendation

Stop tuning recent-return scoring. Test pool size and context gating next.
