`platform5 pre1 hold3` stayed in front. Conditioning hold duration on `report_time` did not improve the cloud event branch in either the recent broad window or the longer `2024_2025` aggregate.

The best explore row was `before_open=2 / after_close=3`, but it still lost to the fixed `hold3` control:
- broad: `93.841%` vs control `100.059%`
- `2024_2025`: `87.412%` vs control `93.491%`

The practical decision is simple: keep the canonical branch unchanged and stop spending budget on hold-schedule micro-tuning. The next useful round should move back to richer event-quality metadata inside `platform5`, not another report-time hold variant.
