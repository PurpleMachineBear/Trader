# Iteration 096 Executive Report

## Decision

Do not promote either tested regime proxy.

`offensive_only` improved the hostile `2024` window, but it was materially worse in `2025`, worse in `2026 YTD`, and worse in the aggregate `2024_2025` window. `min_active_events=2` was worse everywhere.

## What Changed

- Added two coarse positive-regime proxies to the cloud event sleeve:
  - only allow sleeve entries when the master core is already in `QQQ/VOO`
  - only allow sleeve entries when at least two same-day qualified events exist
- Verified with a broad canary that the new knobs did not alter the baseline `platform5 sleeve 10%` path.

## Winner

There was no new winner. The canonical cloud event-sleeve control remains:

- `platform5 sleeve 10%`

## Key Metrics

- canary `platform5 sleeve 10%`: `60.602%`, `Sharpe 2.068`, `DD 9.9%`
- `2024 control`: `15.614%`, `Sharpe 0.602`, `DD 5.5%`
- `2024 offensive_only`: `17.791%`, `Sharpe 0.780`, `DD 5.3%`
- `2025 control`: `39.573%`, `Sharpe 2.035`, `DD 4.8%`
- `2025 offensive_only`: `31.964%`, `Sharpe 1.654`, `DD 4.8%`
- `2024_2025 control`: `62.646%`, `Sharpe 1.362`, `DD 5.4%`
- `2024_2025 offensive_only`: `56.834%`, `Sharpe 1.260`, `DD 5.5%`

## Main Risk

The event sleeve still lacks a usable positive-regime detector. Current coarse proxies either over-filter the profitable window or simply destroy the aggregate edge.

## Recommendation

- Keep the production `IB` paper master unchanged.
- Keep `platform5 sleeve 10%` as the cloud shadow control.
- If research continues on this lane, move to richer event metadata or a proper positive-window classifier.
