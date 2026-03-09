# iter_072 Analysis

## Objective

Test whether the `platform7 pre1 hold3` cloud winner can be improved by changing basket quality rather than timing, with emphasis on `max_names` and removal of persistent drag symbols.

## Sample Coverage

- `2025-01-02` to `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades |
| --- | ---: | ---: | ---: | ---: |
| `platform7 pre1 hold3 max3` | `59.951%` | `0.935` | `18.1%` | `64` |
| `platform7 pre1 hold3 max2` | `59.951%` | `0.935` | `18.1%` | `64` |
| `platform7 pre1 hold3 max1` | `58.108%` | `0.909` | `19.0%` | `62` |
| `platform5 pre1 hold3` | `100.059%` | `1.508` | `10.1%` | `49` |
| `platform6 no NFLX pre1 hold3` | `76.942%` | `1.185` | `16.8%` | `62` |
| `platform6 no ADBE pre1 hold3` | `80.838%` | `1.227` | `19.5%` | `51` |

## Selection Distribution

- `platform5 pre1 hold3`:
  - `ORCL +62958`, `CRM +16580`, `MSFT +13617`, `NOW +7921`, `AAPL -895`
- `platform6 no NFLX pre1 hold3`:
  - `ORCL +53787`, `CRM +13729`, `MSFT +12142`, `NOW +7095`, `AAPL -724`, `ADBE -8956`
- `platform6 no ADBE pre1 hold3`:
  - `ORCL +63995`, `MSFT +14988`, `CRM +13526`, `NOW +9368`, `AAPL -1625`, `NFLX -19289`

## Useful

- `max_names` was not the real issue. `max3` and `max2` produced the exact same result, and `max1` was only slightly worse.
- Symbol quality mattered a lot. Removing both `NFLX` and `ADBE` turned the branch into a much cleaner winner with `100.059%` return and only `10.1%` drawdown.
- Removing only one drag symbol also helped, which confirms the problem was basket composition rather than ranking breadth.

## Not Useful

- More restrictive `max_names` settings did not create the improvement. That line is now a low-value tuning direction.
- `NFLX` and `ADBE` were not soft drags. They were structurally harmful to the event basket.

## Conclusion

The cloud event-aware branch is not just a timing story. It is also strongly basket-quality sensitive. `platform5 pre1 hold3` became the new cloud event-aware leader, but this is still an in-sample refinement learned after observing symbol-level drags. It needs split-window validation before it earns any stronger status.

## Next

- Validate `platform5 pre1 hold3` against the broader `platform7 pre1 hold3` branch by sample window.
- Keep this work cloud-only. Do not mix it into the frozen paper track.
