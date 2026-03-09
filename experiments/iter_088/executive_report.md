# iter_088 executive report

## Decision

Keep the cloud event-aware intraday pilot alive, but only on the `BSL` path and only as a sparse shadow branch.

## What Changed

- `platform5 pre1 intraday BSL` traded and stayed positive in both windows.
- `failed_breakdown` never activated.
- `after_close` filtering was inert.

## Main Risk

The carryover cloud swing control drifted materially after the project refactor, so pre-`iter_088` cloud-control comparisons are not clean until invariance is explained.

## Recommendation

Continue only with event-aware intraday `BSL`, and test whether removing the inherited `recent weakness` assumption improves activation.
