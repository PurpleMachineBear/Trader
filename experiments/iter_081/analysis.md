# iter_081 Analysis

## Objective

Measure same-basket passive baselines for the cloud `platform7` and `platform5` baskets so the event-aware branch can be judged against its natural universe rather than only against `VOO`.

## Sample Coverage

- Local LEAN passive baselines
- Main valid broad sample: `2025-01-02` to `2026-03-06`
- Attempted earlier windows:
  - `2024-01-02` to `2024-12-31`
  - `2024-01-02` to `2025-12-31`

## Summary Table

| Structure | Window | Return | Sharpe | Drawdown | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| `VOO buy-and-hold` | broad | `14.473%` | `0.269` | `19.0%` | common market reference |
| `platform7 passive equal-weight` | broad | `-1.169%` | `-0.669` | `14.3%` | valid |
| `platform5 passive equal-weight` | broad | `-1.650%` | `-0.412` | `19.3%` | valid |
| `platform7 passive equal-weight` | `2024_2025` | `2.397%` | `0.094` | `11.2%` | invalid / truncated by factor coverage |
| `platform5 passive equal-weight` | `2024_2025` | `3.384%` | `0.136` | `15.1%` | invalid / truncated by factor coverage |
| `platform7 passive equal-weight` | `2024` | `0.000%` | `0.000` | `0.0%` | invalid / no usable coverage |
| `platform5 passive equal-weight` | `2024` | `0.000%` | `0.000` | `0.0%` | invalid / no usable coverage |

## Useful

- The recent broad passive comparison is decisive.
  - cloud `platform7 pre1 hold3`: `59.951%` vs passive `platform7`: `-1.169%`
  - cloud `platform5 pre1 hold3`: `100.059%` vs passive `platform5`: `-1.650%`
- This means the cloud event-aware branch is not just piggybacking a strong underlying basket in the recent broad sample.
- `platform5` is especially strong because it beat its passive basket on both return and drawdown.

## Not Useful

- The earlier-window local passive rows are not trustworthy.
- Local factor files for `CRM`, `NOW`, and `ORCL` start at `2025-01-01`, which truncates or nullifies the `2024` and `2024_2025` passive baselines.

## Conclusion

The strongest clean same-basket evidence is now in the recent broad sample, and it supports a real event edge. `platform7` and especially `platform5` are not just "good stock baskets"; their event-aware cloud branches massively outperformed the corresponding passive baskets. For exact earlier-window passive comparisons, the local factor files for `CRM/NOW/ORCL` need to be refreshed or the passive baselines need to be moved to the cloud lane.

## Next

- Keep using the broad passive result as the strongest clean anti-story-check for the cloud event branch.
- Treat local `2024` and `2024_2025` passive rows as invalid until `CRM/NOW/ORCL` factor coverage is repaired.
- If earlier-window passive confirmation becomes important, either refresh those factor files or run cloud passive baselines for the same baskets.
