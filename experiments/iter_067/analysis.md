# iter_067 Analysis

## Objective

Validate whether the improved `hardware7 failed_breakdown` selector is a real multi-window branch improvement and whether it clears the hostile `2024` blocker.

## Sample Coverage

- `2024-01-02` to `2024-12-31`
- `2025-01-02` to `2025-12-31`
- `2026-01-02` to `2026-03-06`

## Window Table

| Window | Structure | Return | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: |
| `2024` | `growth4 failed_breakdown reference` | `5.858%` | `2.5%` | `12` |
| `2024` | `hardware7 old` | `0.754%` | `3.6%` | `39` |
| `2024` | `hardware7 next-gen pool2` | `1.126%` | `3.6%` | `38` |
| `2025` | `hardware7 old` | `15.598%` | `2.7%` | `22` |
| `2025` | `hardware7 next-gen pool2` | `19.283%` | `1.6%` | `26` |
| `2026 YTD` | `hardware7 old` | `1.581%` | `2.2%` | `6` |
| `2026 YTD` | `hardware7 next-gen pool2` | `1.876%` | `2.0%` | `6` |

## Selection Distribution

- `2024 hardware7 next-gen`:
  - `AMD 30`, `MU 12`, `MSFT 12`, `MRVL 10`, `NVDA 8`, `TSM 2`, `AVGO 2`
- `2025 hardware7 next-gen`:
  - `AMD 14`, `MRVL 10`, `MU 10`, `MSFT 8`, `NVDA 6`, `TSM 2`, `AVGO 2`
- `2026 YTD hardware7 next-gen`:
  - `MSFT 4`, `AMD 4`, `NVDA 2`, `MU 2`

## Useful

- The next-gen selector improved `hardware7 failed_breakdown` in all three windows relative to the old hardware7 control.
- The biggest improvement came in `2025`, where both return and drawdown improved materially.
- `2026 YTD` also improved slightly without increasing risk.

## Not Useful

- The hostile `2024` blocker is still unresolved. The next-gen hardware7 row remained far below the old `growth4 failed_breakdown` reference.
- The improvement is real, but it still does not justify calling the branch all-weather.

## Conclusion

`hardware7 failed_breakdown next-gen pool2` is now the strongest large-cap alternative shadow branch we have tested. It is better than the old hardware7 version across all windows, but it still fails the final all-weather requirement because `2024` remains weaker than the old `growth4` hostile-window reference.

## Next

- Keep `hardware7 failed_breakdown next-gen pool2` as the main large-cap alternative shadow branch.
- Do not promote it into the frozen paper set.
- Future large-cap work should now shift from basket permutation to richer premarket ranking and, when possible, event-aware routing.
