# iter_091 analysis

## Sample Coverage

- recent broad: `2025-01-02` to `2026-03-06`
- earlier validation: `2024-01-02` to `2025-12-31`
- cloud project: `Cloud_Earnings_Research`

## Summary Table

| candidate | structure | window | return | sharpe | drawdown | orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| candidate_01 | `control any estimate` | broad | `3.246%` | `-2.053` | `0.4%` | `10` |
| candidate_02 | `estimate required` | broad | `0.313%` | `-10.079` | `1.9%` | `8` |
| candidate_03 | `after_close only` | broad | `3.246%` | `-2.053` | `0.4%` | `10` |
| candidate_04 | `after_close + estimate required` | broad | `0.313%` | `-10.079` | `1.9%` | `8` |
| candidate_05 | `control any estimate` | `2024_2025` | `2.498%` | `-3.568` | `0.6%` | `8` |
| candidate_06 | `estimate required` | `2024_2025` | `-0.422%` | `-27.583` | `0.8%` | `6` |
| candidate_07 | `after_close only` | `2024_2025` | `2.498%` | `-3.568` | `0.6%` | `8` |
| candidate_08 | `after_close + estimate required` | `2024_2025` | `-0.422%` | `-27.583` | `0.8%` | `6` |

## Useful

- `report_time_filter=after_close` was behaviorally identical to `any` in both windows.
  - broad: `3.246%`, `0.4%` drawdown, `10` orders for both rows
  - `2024_2025`: `2.498%`, `0.6%` drawdown, `8` orders for both rows
- This is strong evidence that the current cloud intraday lane does not gain discrimination from simple `after_close` filtering.

## Not Useful

- `estimate_mode=required` was clearly harmful in both windows.
  - broad: `3.246% -> 0.313%`, drawdown `0.4% -> 1.9%`, orders `10 -> 8`
  - `2024_2025`: `2.498% -> -0.422%`, drawdown `0.6% -> 0.8%`, orders `8 -> 6`
- The combined `after_close + estimate required` row collapsed to the same worse path as `estimate required` alone.
- This means the currently available QuantConnect event metadata is not producing a cleaner intraday branch on top of the canonical no-weakness control.

## Invalid

- No strategy rows were invalid.
- A process bug did appear in the first local parser pass for this round: QuantConnect CLI prints duplicate labels such as `Net Profit` and `Sharpe Ratio`, so naive label matching can pull the wrong value. `results.json` was rebuilt from the saved `cloud_runs/*.txt` logs using table-cell parsing.

## Conclusion

The cloud event-aware intraday lane has now exhausted the obvious event metadata available from the current QuantConnect dataset:

- `after_close` is inert
- `estimate required` is harmful
- `after_close + estimate required` is just the same harmful subset

The canonical cloud intraday control therefore remains:

- `platform5 pre1 intraday BSL`
- no recent-weakness requirement
- `selection_pool_size = 2`
- `QQQ/XLK context_min_positive = 1`

## Next

- Stop funding more `report_time` or `estimate_mode` tuning on this cloud intraday lane.
- Treat the current QuantConnect event metadata as exhausted for intraday filtering.
- If this lane continues, move to one of:
  - downstream integration as an activation or allocation hint for the main intraday stack
  - richer external event metadata beyond the current QuantConnect fields
  - risk and exit overlays on the canonical no-weakness control instead of more event-subset slicing
