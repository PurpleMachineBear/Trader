# iter_080 Analysis

## Objective

Complete the cloud event-basket family map by testing the surviving `platform5`, `enterprise4`, and `software3` baskets in the standalone `2025` window.

## Sample Coverage

- Cloud project: `Cloud_Earnings_Research`
- Window: `2025-01-02` to `2025-12-31`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades |
| --- | ---: | ---: | ---: | ---: |
| `platform5 pre1 hold3 any` | `97.990%` | `1.757` | `10.0%` | `38` |
| `enterprise4 pre1 hold3 any` | `105.047%` | `1.889` | `9.9%` | `28` |
| `software3 pre1 hold3 any` | `91.320%` | `1.642` | `9.1%` | `15` |

## Selection Distribution

- `platform5 2025`:
  - `ORCL +62958`, `MSFT +18626`, `NOW +18171`, `CRM +6882`, `AAPL -8560`
- `enterprise4 2025`:
  - `ORCL +65070`, `NOW +18182`, `MSFT +14622`, `CRM +7239`
- `software3 2025`:
  - `ORCL +60274`, `NOW +24568`, `CRM +6522`

## Useful

- `enterprise4` is the clean `2025` winner. It beat `platform5` on return, Sharpe, and drawdown while removing the persistent `AAPL` drag.
- `software3` remained viable, but it underperformed `enterprise4`, which means the best `2025` habitat was not the narrowest possible basket.
- The full family map is now coherent:
  - `software3` is best in hostile `2024`
  - `enterprise4` is best in clean `2025`
  - `2026 YTD` is too sparse to discriminate

## Not Useful

- This does not create a single all-window promoted basket.
- The basket story is now good enough that more symbol-permutation tuning is unlikely to add much without richer event metadata.

## Conclusion

The cloud event lane now has a usable basket map. `platform5` remains the safest canonical control because it is broadly acceptable across windows, `enterprise4` is the best positive-window refinement, and `software3` is the best hostile-window refinement. That means the next bottleneck is no longer basket discovery. It is event metadata and state detection.

## Next

- Stop near-term cloud basket permutation work.
- If this lane continues, the next serious step should be richer event metadata such as estimate / surprise context, macro conflict tagging, or more explicit premarket quality features.
- Keep `platform5` canonical, `enterprise4` as the positive-window alias, and `software3` as the hostile-window alias.
