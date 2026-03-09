# iter_064 Analysis

## Objective

Test whether large-cap `BSL` improves when dynamic selection uses stronger premarket dollar-volume ranking and a filter for opening near the key reclaim level.

## Sample Coverage

- Broad sample: `2024-01-02` to `2026-03-06`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades | Comment |
| --- | ---: | ---: | ---: | ---: | --- |
| `VOO buy-and-hold` | `42.608%` | `0.574` | `18.8%` | `0` | Broad benchmark |
| `growth4 passive` | `15.172%` | `0.007` | `20.9%` | `0` | Same-basket passive baseline |
| `quality6 passive` | `34.187%` | `0.418` | `13.0%` | `0` | Higher-beta large-cap passive baseline |
| `hardware7 passive` | `1.516%` | `-1.588` | `5.6%` | `0` | Weak hardware-heavy passive baseline |
| `growth4 BSL pool2 old control` | `13.685%` | `-0.147` | `5.6%` | `63` | Canonical old control |
| `growth4 BSL next-gen pool2` | `24.033%` | `0.314` | `3.1%` | `47` | Best raw return improvement |
| `growth4 BSL next-gen pool1` | `23.775%` | `0.324` | `2.4%` | `40` | Best risk-adjusted row |
| `quality6 BSL next-gen pool2` | `22.973%` | `0.243` | `4.2%` | `58` | Viable but below quality6 passive |
| `hardware7 BSL next-gen pool2` | `-1.057%` | `-0.828` | `13.0%` | `72` | Still bad under `BSL` |

## Selection Distribution

- `growth4 BSL old control`:
  - `NVDA 40`, `TSLA 38`, `AMZN 28`, `META 20`
- `growth4 BSL next-gen pool2`:
  - `AMZN 28`, `NVDA 26`, `TSLA 24`, `META 16`
- `growth4 BSL next-gen pool1`:
  - `TSLA 24`, `AMZN 24`, `NVDA 20`, `META 12`
- `quality6 BSL next-gen pool2`:
  - `AMZN 26`, `NVDA 24`, `TSLA 22`, `AVGO 16`, `META 16`, `MSFT 12`
- `hardware7 BSL next-gen pool2`:
  - `NVDA 28`, `AMD 28`, `MRVL 26`, `AVGO 22`, `MSFT 20`, `MU 18`, `TSM 2`

## Useful

- The new `growth4` selector is a real broad-sample improvement, not a cosmetic tweak. Both `pool2` and `pool1` materially beat the old control on return and drawdown.
- `pool1` slightly reduced return versus `pool2`, but it improved drawdown further and produced the best broad-sample score.
- `quality6` became a viable active branch once selection quality improved, even though it still lagged its own passive basket.

## Not Useful

- `hardware7` still does not want `BSL`. Better ranking and proximity filters did not rescue that basket.
- No active large-cap `BSL` row beat `VOO` on raw broad-sample return.
- `quality6` active was directionally useful but still inferior to `quality6` passive, so it is not the new canonical large-cap lane.

## Next

- Validate `growth4` next-gen `pool2` and `pool1` across `2024`, `2025`, and `2026 YTD`.
- Test whether the same selector improvements help `failed_breakdown`, especially on `hardware7`.
