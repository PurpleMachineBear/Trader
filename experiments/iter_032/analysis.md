# iter_032 Analysis

## Objective

Test whether the current large-cap dynamic lane can be improved by narrowing around the names it actually appears to be selecting in `2026`.

## Sample Coverage

- `2026-01-02` to `2026-03-06`

## Summary Table

| Structure | Return | Drawdown | Trades | Comment |
| --- | ---: | ---: | ---: | --- |
| `VOO buy-and-hold` | `-2.057%` | `3.3%` | `0` | Benchmark |
| `growth4 passive` | `-2.874%` | `3.3%` | `0` | Same-basket passive |
| `growth4 BSL pool2 hold180` | `4.873%` | `1.8%` | `7` | Current reference |
| `growth4 BSL pool2 hold120` | `4.281%` | `1.1%` | `7` | Conservative alias |
| `AMZN/NVDA/TSLA pool2 hold180` | `4.873%` | `1.8%` | `7` | Same as control |
| `AMZN/NVDA/TSLA pool2 hold120` | `4.281%` | `1.1%` | `7` | Same as hold120 alias |
| `AMZN/TSLA pool2 hold180` | `4.781%` | `1.8%` | `7` | Slightly lower return |
| `AMZN/TSLA pool2 hold120` | `4.745%` | `1.1%` | `7` | Cleaner conservative alias |
| `AMZN/NVDA/TSLA pool1 hold180` | `4.346%` | `1.8%` | `6` | Worse than pool2 |

## Useful

- The current large-cap dynamic traffic is concentrated enough that removing `META`, and sometimes even `NVDA`, barely changed the `2026 YTD` outcome.
- `AMZN/TSLA hold120` is a real conservative current-window alias. It preserved most of the return while lowering drawdown to `1.1%`.
- This round confirmed that the existing `growth4 BSL pool2` control is already capturing the current winners well enough.

## Not Useful

- Narrowing the basket did not create new alpha.
- Several variants were effectively aliases of the broader control, which means a narrower watchlist alone is not the missing ingredient.
- `pool1` was weaker than `pool2` even in the window that motivated the narrowing.

## Next

- Validate the narrowed `AMZN/TSLA` branch across `2024`, `2025`, and `2026 YTD`.
- If the narrower branch only improves one favorable window, keep the broader `growth4` control as canonical.
