# iter_066 Analysis

## Objective

Test whether the same premarket-quality and key-level-proximity selector improvements also help `failed_breakdown`, especially on the `hardware7` large-cap basket.

## Sample Coverage

- Broad sample: `2024-01-02` to `2026-03-06`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades | Comment |
| --- | ---: | ---: | ---: | ---: | --- |
| `VOO buy-and-hold` | `42.608%` | `0.574` | `18.8%` | `0` | Broad benchmark |
| `growth4 passive` | `15.172%` | `0.007` | `20.9%` | `0` | Growth4 passive |
| `hardware7 passive` | `1.516%` | `-1.588` | `5.6%` | `0` | Hardware7 passive |
| `growth4 failed_breakdown old` | `3.821%` | `-1.328` | `2.6%` | `31` | Old growth4 control |
| `growth4 failed_breakdown next-gen` | `1.834%` | `-1.500` | `3.8%` | `36` | Selector hurt growth4 |
| `hardware7 failed_breakdown old` | `21.233%` | `0.148` | `3.4%` | `73` | Validated shadow branch |
| `hardware7 failed_breakdown next-gen pool2` | `25.915%` | `0.326` | `3.4%` | `76` | Best row |
| `hardware7 failed_breakdown next-gen pool1` | `21.388%` | `0.156` | `4.5%` | `68` | No improvement |

## Selection Distribution

- `growth4 failed_breakdown old`:
  - `TSLA 20`, `AMZN 16`, `NVDA 14`, `META 12`
- `growth4 failed_breakdown next-gen`:
  - `TSLA 20`, `AMZN 20`, `NVDA 16`, `META 16`
- `hardware7 failed_breakdown old`:
  - `AMD 42`, `MRVL 28`, `MSFT 26`, `MU 22`, `NVDA 14`, `TSM 8`, `AVGO 6`
- `hardware7 failed_breakdown next-gen pool2`:
  - `AMD 50`, `MSFT 28`, `MRVL 26`, `MU 24`, `NVDA 16`, `TSM 4`, `AVGO 4`

## Useful

- The same selector upgrade that only partially helped `growth4 BSL` clearly helped `hardware7 failed_breakdown`.
- `hardware7 next-gen pool2` improved both return and Sharpe while keeping drawdown flat.
- The improvement was not caused by collapsing the branch into one symbol; the next-gen row still rotated through multiple hardware names.

## Not Useful

- The selector changes are not universal. They actively hurt `growth4 failed_breakdown`.
- `pool1` was not better than `pool2` for `hardware7 failed_breakdown`.
- This broad-sample improvement alone is still not enough for promotion.

## Conclusion

Selector improvements are family-specific. `failed_breakdown` benefits from them on `hardware7`, while `growth4` does not.

## Next

- Validate `hardware7 failed_breakdown next-gen pool2` across `2024`, `2025`, and `2026 YTD`.
- Compare the `2024` result directly against the old `growth4` hostile-window reference before any promotion decision.
