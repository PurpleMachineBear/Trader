# iter_076 Executive Report

## Decision

Do not promote the rolling quality-floor branch. Keep it only as a minor cloud shadow variant.

## Why

- `platform7 any floor min1`: `61.007%` return, `17.8%` drawdown
- `platform7 any baseline`: `59.951%`, `18.1%` drawdown
- `platform5 any reference`: `100.059%`, `10.1%` drawdown
- `min2` and `after_close` floor variants were worse

## Final View

- Hard quality floors are more meaningful than soft score bonuses.
- But the improvement is too small to change the roadmap.
- The cloud lane now looks more limited by event-history depth and metadata richness than by another ranking tweak.

## Recommendation

- Freeze the cloud hierarchy as:
  - `platform5 pre1 hold3` lead
  - `platform7 any floor min1` minor shadow
- Deprioritize more selector micro-tuning for now.
