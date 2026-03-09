# Iter 084 Analysis

## Sample Coverage

- Cloud project: `Cloud_Earnings_Research`
- Recent broad window: `2025-01-02` to `2026-03-06`
- Earlier aggregate window: `2024-01-02` to `2025-12-31`
- Family under test: `platform5 pre1 hold3`
- New metadata knobs: `estimate_mode` and `report_time_filter`

## Summary Table

| Candidate | Window | Structure | Return | Sharpe | Drawdown | Orders | Score |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_01` | `broad` | control | `100.059%` | `1.508` | `10.1%` | `89` | `230.659` |
| `candidate_02` | `broad` | `estimate required` | `75.473%` | `1.201` | `10.1%` | `76` | `175.373` |
| `candidate_03` | `broad` | `estimate missing` | `14.095%` | `0.321` | `5.8%` | `14` | `34.595` |
| `candidate_04` | `broad` | `after_close + estimate required` | `75.473%` | `1.201` | `10.1%` | `76` | `175.373` |
| `candidate_05` | `2024_2025` | control | `93.491%` | `0.806` | `21.7%` | `153` | `130.691` |
| `candidate_06` | `2024_2025` | `estimate required` | `64.370%` | `0.590` | `19.5%` | `132` | `84.370` |
| `candidate_07` | `2024_2025` | `estimate missing` | `5.254%` | `-0.416` | `13.1%` | `17` | `-62.546` |
| `candidate_08` | `2024_2025` | `after_close + estimate required` | `64.370%` | `0.590` | `19.5%` | `132` | `84.370` |

## Useful

- `estimate_mode` is the first richer event-metadata knob that clearly carries some information.
- The branch is concentrated in `required estimate` events rather than `missing estimate` events.
  - Recent broad:
    - control `100.059%`
    - `required` `75.473%`
    - `missing` `14.095%`
  - `2024_2025`:
    - control `93.491%`
    - `required` `64.370%`
    - `missing` `5.254%`
- This means the cloud branch is not dominated by opaque or estimate-less events.
- But `required` still underperformed the ungated control in both windows, so estimate availability is a partial quality signal, not the full explanation.

## Not Useful

- `after_close + estimate required` was behaviorally inert relative to `estimate required`.
  - Same return, Sharpe, drawdown, and order count in both windows.
- That means the `required estimate` subset in this branch was already effectively an `after_close` subset for the tested samples.
- Pure `missing estimate` slicing is not a viable promotion path.

## Interpretation

This refines the event-lane hypothesis again:

- The branch is not best explained by coarse price state.
- It is not best explained by coarse tape state.
- It is also not fully explained by estimate availability alone.

But estimate availability does tell us something real:

- the better part of the branch lives in ordinary covered earnings events
- the weak part lives in estimate-missing events

So the next useful metadata likely needs to be more detailed than presence/absence:

- estimate magnitude or estimate dispersion if accessible
- symbol-specific event quality within the covered-events subset
- report-time interaction only after a non-inert metadata split is found

## Next

- Keep `platform5 pre1 hold3` as the canonical cloud control.
- Do not spend more rounds on `estimate missing` or `after_close + required`; those are now explained enough.
- The next event-metadata pass should target richer covered-event fields instead of more binary filters.
