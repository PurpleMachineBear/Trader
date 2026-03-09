# iter_066 Executive Report

## Decision

The selector upgrade should continue only on `hardware7 failed_breakdown`.

## Winner

- `hardware7 failed_breakdown next-gen pool2`
  - `25.915%` return
  - `0.326` Sharpe
  - `3.4%` drawdown

## What Changed

- The same selector logic that improved `growth4 BSL` did not help all families.
- It hurt `growth4 failed_breakdown`.
- It clearly improved `hardware7 failed_breakdown`.

## Recommendation

- Validate the improved `hardware7` branch by window.
- Do not apply the same selector logic blindly across all large-cap families.
