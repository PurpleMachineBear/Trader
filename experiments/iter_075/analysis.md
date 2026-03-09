# iter_075 Analysis

## Objective

Test whether a rolling symbol-specific event-quality bonus can improve the broader `platform7` cloud event branch without hand-curated symbol exclusions.

## Sample Coverage

- `2025-01-02` to `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades |
| --- | ---: | ---: | ---: | ---: |
| `platform7 any baseline` | `59.951%` | `0.935` | `18.1%` | `64` |
| `platform7 any quality 0.5 / min1` | `59.951%` | `0.935` | `18.1%` | `64` |
| `platform7 any quality 1.0 / min1` | `59.951%` | `0.935` | `18.1%` | `64` |
| `platform7 any quality 1.0 / min2` | `59.951%` | `0.935` | `18.1%` | `64` |
| `platform7 after_close quality 1.0 / min1` | `62.278%` | `1.005` | `18.1%` | `57` |
| `platform5 any reference` | `100.059%` | `1.508` | `10.1%` | `49` |

## Useful

- The round cleanly ruled something out: a soft additive quality bonus did nothing at all to the broad `platform7` branch.
- The stronger `after_close` structural clue still mattered more than the rolling quality bonus.

## Not Useful

- None of the `platform7 any` quality-bonus rows changed a single headline metric or trade path.
- This means the soft score was too weak to alter the watchlist ordering in practice, even after completed event trades accumulated.

## Conclusion

The cloud lane does not need more additive ranking tweaks right now. A soft rolling quality bonus is inert in this branch. If symbol-specific quality is going to matter, it must act as a harder gate rather than as a small score adjustment.

## Next

- Stop spending budget on additive quality-score variants.
- Test a hard rolling quality floor instead.
