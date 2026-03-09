# iter_068 Analysis

## Objective

Validate whether the improved `growth4 BSL` selector transfers to an adjacent large-cap platform bucket instead of only working inside the original `AMZN/META/NVDA/TSLA` natural habitat.

## Sample Coverage

- `2025-01-02` to `2026-03-06`

## Summary Table

| Structure | Role | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `VOO buy_and_hold` | benchmark | `14.463%` | `0.269` | `19.0%` | `0` |
| `platform7 equal_weight_buy_and_hold` | passive baseline | `-1.170%` | `-0.669` | `14.3%` | `0` |
| `growth4 BSL next-gen pool2 reference` | reference | `21.595%` | `1.036` | `3.9%` | `33` |
| `platform7 BSL old selector pool2` | control | `-9.136%` | `-1.844` | `10.9%` | `28` |
| `platform7 BSL next-gen selector pool2` | explore | `-9.531%` | `-2.151` | `11.1%` | `25` |
| `platform7 BSL next-gen selector pool1` | explore | `-4.847%` | `-2.459` | `5.3%` | `20` |

## Selection Distribution

- `growth4 BSL next-gen pool2 reference`:
  - `AMZN 24`, `NVDA 16`, `TSLA 14`, `META 12`
- `platform7 BSL old selector pool2`:
  - `NFLX 16`, `ORCL 14`, `MSFT 10`, `NOW 6`, `AAPL 4`, `CRM 4`, `ADBE 2`
- `platform7 BSL next-gen selector pool2`:
  - `NFLX 18`, `MSFT 12`, `ORCL 8`, `NOW 4`, `CRM 4`, `AAPL 2`, `ADBE 2`
- `platform7 BSL next-gen selector pool1`:
  - `NFLX 16`, `MSFT 12`, `NOW 4`, `AAPL 2`, `CRM 2`, `ADBE 2`, `ORCL 2`

## Useful

- The round cleanly answered the anti-overfit question. The improved selector did **not** transfer from `growth4` to the adjacent `platform7` bucket.
- `pool1` was less bad than `pool2`, which suggests the adjacent bucket contains too many marginal names and the selector is not rescuing them.
- The same-sample passive basket baseline was only `-1.170%`, so the platform7 active rows were not merely facing a hard sample; they added negative alpha on top.

## Not Useful

- The next-gen selector did not improve the adjacent bucket at all. `pool2` was slightly worse than the old selector, and `pool1` only reduced the damage.
- This is not a near-miss promotion case. All active platform7 rows were materially negative while the original `growth4` reference remained strongly positive on the same dates.

## Conclusion

The improved `growth4 BSL` selector is still habitat-specific. It improves the original `growth4` branch, but it does not generalize to a nearby large-cap platform/software-style bucket. This means the next large-cap step should not be more adjacent basket permutation. The right next step is event-aware or catalyst-aware selection, ideally in a cloud-backed lane where `Upcoming Earnings` can be used.

## Next

- Keep `growth4 BSL next-gen` as the canonical large-cap current-regime reference.
- Do not promote `platform7` variants into any shadow shortlist.
- Shift the next large-cap research question from adjacent transfer to `event-aware large-cap selection`.
