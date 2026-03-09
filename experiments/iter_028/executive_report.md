# iter_028 Executive Report

## Decision

Do not continue the bullish daily-gate line. The plain `growth4 BSL pool2` control remained the best active large-cap row on the broad sample.

## Sample Coverage

- `2024-01-02` to `2026-03-06`

## Summary Table

| Candidate | Return | Drawdown | Decision |
| --- | ---: | ---: | --- |
| `growth4 BSL pool2` | `13.685%` | `5.6%` | Keep as broad-sample active control |
| `40d regime gate + pool1` | `6.138%` | `5.4%` | Drawdown cleaner, but weaker overall |
| `20d regime gate + 2% floor` | `-2.144%` | `2.6%` | Reject |

## Useful / Not Useful / Next

- Useful: the round proved that a simple positive-tape gate is not the missing ingredient.
- Not useful: every tested daily regime gate underperformed the no-gate active control.
- Next: compare reversal families directly by window and test whether regime-awareness should come from `family switching`, not from `bullish gating`.
