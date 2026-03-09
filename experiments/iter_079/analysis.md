# iter_079 Analysis

## Objective

Resolve whether the narrowed `enterprise4` basket improves both the hostile early window and the sparse current window, or whether `platform5` should remain the canonical cloud control.

## Sample Coverage

- Cloud project: `Cloud_Earnings_Research`
- Split windows:
  - `2024-01-02` to `2024-12-31`
  - `2026-01-02` to `2026-03-06`

## Summary Table

| Structure | Window | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `platform5 pre1 hold3 any` | `2024` | `10.449%` | `0.212` | `19.5%` | `34` |
| `enterprise4 pre1 hold3 any` | `2024` | `10.306%` | `0.206` | `22.6%` | `21` |
| `software3 pre1 hold3 any` | `2024` | `22.154%` | `0.512` | `22.5%` | `15` |
| `platform5 pre1 hold3 any` | `2026 YTD` | `5.078%` | `1.301` | `3.5%` | `2` |
| `enterprise4 pre1 hold3 any` | `2026 YTD` | `5.078%` | `1.301` | `3.5%` | `2` |
| `software3 pre1 hold3 any` | `2026 YTD` | `5.078%` | `1.301` | `3.5%` | `2` |

## Selection Distribution

- `platform5 2024`:
  - `ORCL +11651`, `NOW +9641`
  - `CRM -301`, `AAPL -1851`, `MSFT -8619`
- `enterprise4 2024`:
  - `ORCL +10753`, `NOW +8859`, `CRM +622`, `MSFT -9883`
- `software3 2024`:
  - `ORCL +10768`, `NOW +9674`, `CRM +1746`
- `2026 YTD` for all three rows:
  - only `CRM +5084`

## Useful

- `software3` is the clear hostile-window winner. Removing both `AAPL` and `MSFT` improved `2024` materially.
- `enterprise4` did not beat `platform5` in the hostile window, so it is not the clean answer to the promotion question.
- The current sparse window is non-discriminating. All three baskets collapsed to the exact same `CRM` path.

## Not Useful

- `2026 YTD` cannot decide basket promotion here. It only proves that the current event sample is too thin to separate these baskets.
- `enterprise4` remains in the middle: better than the broad basket on the two-year aggregate, but not better than `platform5` in hostile `2024`.

## Conclusion

The cloud branch now has a more complete map. `platform5` is still the canonical cross-window control, `software3` is the strongest hostile-window alias, and `enterprise4` is no longer the most interesting refinement because it failed to beat `platform5` in `2024`. Since `2026 YTD` offers no basket-specific information, the next meaningful split is `2025`, not more current-window micro-tuning.

## Next

- Run a clean `2025` comparison for `platform5`, `enterprise4`, and `software3`.
- Keep `platform5` canonical unless `software3` or another narrowed basket can show a coherent cross-window story rather than a single-window win.
- Treat current `2026 YTD` basket comparisons in this cloud lane as sparse evidence only.
