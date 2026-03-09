# iter_078 Analysis

## Objective

Test whether the validated `platform5 pre1 hold3` cloud branch is actually a narrower enterprise-software habitat by removing the weaker consumer/platform names while keeping the same event trigger.

## Sample Coverage

- Cloud project: `Cloud_Earnings_Research`
- Windows:
  - `2024-01-02` to `2025-12-31`
  - `2025-01-02` to `2026-03-06`

## Summary Table

| Structure | Window | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `platform5 pre1 hold3 any` | `2024_2025` | `93.491%` | `0.806` | `21.7%` | `83` |
| `enterprise4 pre1 hold3 any` | `2024_2025` | `103.986%` | `0.888` | `22.6%` | `54` |
| `software3 pre1 hold3 any` | `2024_2025` | `104.955%` | `0.888` | `22.5%` | `35` |
| `platform5 pre1 hold3 any` | `broad` | `100.059%` | `1.508` | `10.1%` | `49` |
| `enterprise4 pre1 hold3 any` | `broad` | `99.700%` | `1.519` | `10.4%` | `35` |
| `software3 pre1 hold3 any` | `broad` | `80.548%` | `1.243` | `11.8%` | `19` |

## Selection Distribution

- `enterprise4 2024_2025`:
  - `ORCL +75483`, `NOW +20311`, `CRM +7852`, `MSFT +458`
- `software3 2024_2025`:
  - `ORCL +75358`, `NOW +20964`, `CRM +8721`
- `enterprise4 broad`:
  - `ORCL +65070`, `CRM +16916`, `MSFT +9385`, `NOW +8427`
- `software3 broad`:
  - `ORCL +60274`, `CRM +15273`, `NOW +5072`

## Useful

- Removing `AAPL` was directionally right for the extended `2024_2025` window. Both narrower baskets beat the canonical `platform5` control there.
- `ORCL/NOW/CRM` are now clearly the economic center of the branch. The narrower baskets made that concentration explicit instead of relying on `AAPL` or `MSFT` diversification.
- `enterprise4` is the cleaner narrowed variant than `software3` because it stayed effectively tied with the broad recent control instead of clearly falling behind.

## Not Useful

- The narrower baskets did not produce a clear cross-window promotion case.
- `software3` was materially worse in the recent broad sample, so the pure three-name basket is too narrow to become the new canonical branch.
- `enterprise4` improved the longer window but was slightly worse than `platform5` in recent broad return and drawdown, so it is still unresolved rather than clearly superior.

## Conclusion

The cloud branch probably is narrower than `platform5`, but not as narrow as `software3`. `enterprise4` looks like the best structural refinement so far: it improves the extended `2024_2025` window without clearly breaking the recent broad sample. That is not enough to replace `platform5`, but it is enough to justify one more split-window validation pass before this lane is considered saturated.

## Next

- Run explicit `2024` and `2026 YTD` split-window validation for `platform5`, `enterprise4`, and `software3`.
- Keep `platform5 pre1 hold3` as the canonical cloud control until a narrower basket improves both hostile and recent windows.
- Keep `software3` exploratory only; do not treat it as a promotion candidate unless it clears the split-window test.
