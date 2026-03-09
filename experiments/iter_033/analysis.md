# iter_033 Analysis

## Objective

Validate the narrowed `AMZN/TSLA` large-cap branch across `2024`, `2025`, and `2026 YTD`.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06` (`YTD`)

## Summary Table

| Window | Structure | Return | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: |
| `2024` | `growth4 BSL pool2 hold180` | `-0.623%` | `5.6%` | `18` |
| `2024` | `AMZN/TSLA pool2 hold180` | `-4.019%` | `7.9%` | `11` |
| `2024` | `AMZN/TSLA pool2 hold120` | `-4.661%` | `7.6%` | `11` |
| `2025` | `growth4 BSL pool2 hold180` | `8.448%` | `5.1%` | `32` |
| `2025` | `AMZN/TSLA pool2 hold180` | `12.319%` | `4.6%` | `18` |
| `2025` | `AMZN/TSLA pool2 hold120` | `7.946%` | `4.2%` | `18` |
| `2026 YTD` | `growth4 BSL pool2 hold180` | `4.873%` | `1.8%` | `7` |
| `2026 YTD` | `AMZN/TSLA pool2 hold180` | `4.781%` | `1.8%` | `7` |
| `2026 YTD` | `AMZN/TSLA pool2 hold120` | `4.745%` | `1.1%` | `7` |

## Stability Table

| Structure | Average Return | Min Return | Max Return | Comment |
| --- | ---: | ---: | ---: | --- |
| `growth4 BSL pool2 hold180` | `4.233%` | `-0.623%` | `8.448%` | Best cross-window balance |
| `AMZN/TSLA pool2 hold180` | `4.360%` | `-4.019%` | `12.319%` | One strong year, weak hostile window |
| `AMZN/TSLA pool2 hold120` | `2.677%` | `-4.661%` | `7.946%` | Conservative only in favorable windows |

## Useful

- `AMZN/TSLA hold180` did materially improve `2025`, which confirms the current large-cap lane is heavily driven by those names in friendlier tapes.
- `AMZN/TSLA hold120` remained the cleaner current-window conservative variant.

## Not Useful

- The narrowed branch was materially worse in hostile `2024`.
- The narrowed branch did not beat the broader control in `2026 YTD`.
- `AMZN/TSLA hold120` lost too much in both `2024` and `2025` to justify promotion.

## Conclusion

The narrower `AMZN/TSLA` branch is not a better canonical large-cap strategy. It is a favorable-window specialization, not a stable replacement for `growth4 BSL pool2`.

## Next

- Keep `growth4 BSL pool2` as the large-cap current-regime reference.
- Stop spending more budget on narrowed large-cap watchlist aliases until a richer event or premarket layer exists.
