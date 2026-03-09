# iter_075 Executive Report

## Decision

Reject additive rolling quality scores as a useful next direction for the cloud platform branch.

## Why

- All `platform7 any` quality-bonus rows were exactly identical to the baseline.
- `platform7 after_close` was still only `62.278%`, far below the `platform5` reference at `100.059%`.

## Final View

- Soft ranking adjustments are not moving the branch.
- If symbol-specific quality matters, it needs to act as a harder filter.

## Recommendation

- Move to rolling quality-floor tests.
- Do not spend more budget on additive quality bonuses.
