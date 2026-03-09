# Iter 087 Analysis

## Objective

Revalidate earlier-window same-basket passive baselines for `platform7` and `platform5` after repairing local daily and factor coverage for `CRM/NOW/ORCL/NFLX/ADBE`.

## Sample Coverage

- Local LEAN passive baselines
- `2024-01-02` to `2024-12-31`
- `2024-01-02` to `2025-12-31`

## Summary Table

| Structure | Window | Return | Sharpe | Drawdown |
| --- | --- | ---: | ---: | ---: |
| `VOO buy-and-hold` | `2024` | `24.385%` | `1.101` | `8.4%` |
| `platform7 passive equal-weight` | `2024` | `8.613%` | `0.105` | `3.3%` |
| `platform5 passive equal-weight` | `2024` | `12.097%` | `0.445` | `4.4%` |
| `platform7 passive equal-weight` | `2024_2025` | `12.458%` | `-0.088` | `15.6%` |
| `platform5 passive equal-weight` | `2024_2025` | `17.497%` | `0.085` | `20.0%` |

## Cloud Head-to-Head

Using the previously validated cloud event rows:

| Structure | Window | Cloud Event Return | Passive Return | Cloud DD | Passive DD |
| --- | --- | ---: | ---: | ---: | ---: |
| `platform7` | `2024` | `-23.061%` | `8.613%` | `33.9%` | `3.3%` |
| `platform5` | `2024` | `10.449%` | `12.097%` | `19.5%` | `4.4%` |
| `platform7` | `2024_2025` | `7.756%` | `12.458%` | `47.4%` | `15.6%` |
| `platform5` | `2024_2025` | `93.491%` | `17.497%` | `21.7%` | `20.0%` |

## Useful

- The earlier-window passive baselines are now valid after the local data repair.
- This materially sharpens the cloud interpretation:
  - `platform5` still has a real two-year event edge versus its same-basket passive baseline.
  - `platform7` does not.
- The strongest clean earlier-window statement is now:
  - `platform5 2024_2025` cloud event `93.491%` vs passive `17.497%`

## Not Useful

- The old narrative that `platform5` clearly beat its natural basket even in hostile `2024` is no longer supportable.
- In `2024` alone, `platform5` cloud event `10.449%` did not beat passive `12.097%`, and its drawdown was much worse.
- `platform7` is clearly not a viable cloud promotion path once the repaired passive baseline is included.

## Conclusion

The repaired earlier-window passive baselines improve confidence in the data and refine the cloud thesis. `platform5` still deserves to exist as the canonical cloud control because it massively outperformed passive on the full `2024_2025` window, but it should now be described more carefully:

- not a clear hostile-2024 winner versus passive
- yes, a strong two-year event-timing branch versus its natural basket

This makes the next step even clearer. The cloud lane should not keep tuning swing selector mechanics. It should either:

- move to richer event metadata, or
- be used as an event-quality reference for intraday integration.

## Next

- Keep `platform5 pre1 hold3` as the canonical cloud control, but downgrade the claim from `hostile-window winner` to `two-year event-edge branch`.
- Demote `platform7` further; it does not beat same-basket passive in the repaired earlier windows.
- Use this repaired passive evidence when deciding whether the cloud branch deserves downstream integration into intraday or portfolio logic.
