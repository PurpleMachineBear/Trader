`platform5 pre1 intraday BSL` stays the cloud intraday control. This round showed that the remaining obvious QuantConnect event metadata is exhausted for this lane: `after_close` filtering was completely inert, while `estimate required` materially damaged the strategy in both windows.

Key numbers:
- broad control: `3.246%`, `0.4%` drawdown, `10` orders
- broad `after_close`: identical
- broad `estimate required`: `0.313%`, `1.9%` drawdown, `8` orders
- `2024_2025` control: `2.498%`, `0.6%` drawdown, `8` orders
- `2024_2025` `estimate required`: `-0.422%`, `0.8%` drawdown, `6` orders

Decision:
- keep the no-weakness `pool2 ctx+1` row as the cloud intraday shadow control
- stop spending cloud budget on `report_time` and `estimate` subset tuning for this intraday lane
- if we continue, move to downstream integration, richer external event metadata, or risk/exit overlays rather than more subset slicing
