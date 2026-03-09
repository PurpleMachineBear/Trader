# iter_028 Analysis

## Objective

Test whether a true `daily regime gate` can improve the large-cap `growth4` BSL branch on the broad `2024-2026` sample.

## Sample Coverage

- `2024-01-02` to `2026-03-06`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades |
| --- | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | `42.608%` | `0.574` | `18.8%` | `0` |
| `growth4 passive` | `15.172%` | `0.007` | `20.9%` | `0` |
| `growth4 BSL pool2` | `13.685%` | `-0.147` | `5.6%` | `63` |
| `growth4 BSL pool1` | `10.232%` | `-0.351` | `6.1%` | `50` |
| `40d tech regime gate + pool1` | `6.138%` | `-0.848` | `5.4%` | `25` |
| `40d tech regime gate + pool2` | `4.828%` | `-1.042` | `3.5%` | `29` |
| `20d tech regime gate + pool1` | `3.032%` | `-1.890` | `2.3%` | `20` |
| `20d tech regime gate + pool2` | `1.627%` | `-1.912` | `2.3%` | `23` |
| `20d tech regime gate + 2% floor` | `-2.144%` | `-4.900` | `2.6%` | `14` |

## Useful

- This was a productive negative result. The existing no-gate `growth4 BSL pool2` remained the best active large-cap broad-sample row.
- The `40d` gates did reduce drawdown, so the regime logic was binding. It just did not create better overall strategy quality.
- The round proved that the large-cap branch does not simply need a bullish medium-term tape filter.

## Not Useful

- Every tested positive daily regime gate degraded broad-sample large-cap BSL performance.
- The stricter `20d >= 2%` regime floor was actively bad.
- `SPY/QQQ/XLK` broad-proxy gating also failed; this was not just a `SMH` or semis-overweight issue.

## Next

- Stop spending more budget on positive daily regime gates for large-cap BSL.
- Move to a `family map`: compare large-cap `BSL`, `failed_breakdown`, and `vwap_reclaim` by window.
